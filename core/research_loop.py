"""
GeoResearchAgent-247 Research Loop
Implements the iterative research cycle: literature → hypothesis → experiment → write → review.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import anthropic

from .config import AgentConfig


class ResearchLoop:
    """
    Orchestrates the full research pipeline as a multi-agent chain.
    Each stage is a separate Claude API call, allowing for state persistence
    and resumability via checkpoints.
    """

    STAGE_ORDER = ["literature", "experiment", "writing", "review"]

    def __init__(self, config: AgentConfig, run_dir: Path) -> None:
        self.config = config
        self.run_dir = run_dir
        self.client = anthropic.Anthropic()
        self.state: dict[str, Any] = {}
        self._load_checkpoint()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> dict[str, Any]:
        """Execute the configured research pipeline stages in order."""
        enabled = set(self.config.enabled_agents)

        if "geo_specialist" in enabled:
            self.state["geo_context"] = self._build_geo_context()

        if "literature" in enabled:
            self.state["literature"] = self._run_literature_stage()

        if "experiment" in enabled:
            self.state["experiment"] = self._run_experiment_stage()

        if "writing" in enabled:
            self.state["writing"] = self._run_writing_stage()

        if "review" in enabled:
            for i in range(self.config.writing.review_rounds):
                self.state[f"review_round_{i+1}"] = self._run_review_stage(round_num=i + 1)
                if i < self.config.writing.review_rounds - 1:
                    self.state["writing"] = self._run_revision_stage(round_num=i + 1)

        self._save_final_outputs()
        return self.state

    def save_checkpoint(self) -> None:
        checkpoint_dir = Path(self.config.output.checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_file = checkpoint_dir / f"{self.run_dir.name}.json"
        with open(checkpoint_file, "w") as f:
            json.dump(self.state, f, indent=2, default=str)

    # ------------------------------------------------------------------
    # Stage implementations
    # ------------------------------------------------------------------

    def _build_geo_context(self) -> dict[str, str]:
        """Build geo-domain context to inject into all subsequent stages."""
        return {
            "domain": self._infer_domain(self.config.topic),
            "relevant_methods": self._infer_methods(self.config.topic),
            "relevant_software": "Python (geopandas, mgwr, rasterio, pysal), R (spdep, GWmodel), QGIS",
            "data_sources": "OpenStreetMap, GADM, Census, Copernicus, USGS EarthExplorer",
        }

    def _run_literature_stage(self) -> dict[str, Any]:
        """Search and synthesize literature."""
        from agents.literature_agent import LiteratureAgent

        agent = LiteratureAgent(client=self.client, config=self.config)
        result = agent.run(
            topic=self.config.topic,
            geo_context=self.state.get("geo_context", {}),
        )

        # Save intermediate output
        out_path = self.run_dir / "literature_review.md"
        out_path.write_text(result.get("markdown", ""))

        hypotheses_path = self.run_dir / "hypotheses.json"
        hypotheses_path.write_text(json.dumps(result.get("hypotheses", []), indent=2))

        self.save_checkpoint()
        return result

    def _run_experiment_stage(self) -> dict[str, Any]:
        """Design and execute experiments."""
        from agents.experiment_agent import ExperimentAgent
        from agents.codex_worker import CodexWorker

        agent = ExperimentAgent(
            client=self.client,
            config=self.config,
            run_dir=self.run_dir,
        )

        # Optionally delegate coding to Codex workers
        coding_backend = None
        if self.config.backend.coding_workers.provider == "openai":
            coding_backend = CodexWorker(config=self.config.backend.coding_workers)

        result = agent.run(
            hypotheses=self.state.get("literature", {}).get("hypotheses", []),
            geo_context=self.state.get("geo_context", {}),
            coding_backend=coding_backend,
        )

        out_path = self.run_dir / "experiment_log.json"
        out_path.write_text(json.dumps(result, indent=2, default=str))

        self.save_checkpoint()
        return result

    def _run_writing_stage(self) -> dict[str, Any]:
        """Generate the paper draft."""
        from agents.writing_agent import WritingAgent

        agent = WritingAgent(client=self.client, config=self.config)
        result = agent.run(
            topic=self.config.topic,
            literature=self.state.get("literature", {}),
            experiment=self.state.get("experiment", {}),
            geo_context=self.state.get("geo_context", {}),
            journal=self.config.writing.journal,
        )

        draft_path = self.run_dir / "draft_v1.md"
        draft_path.write_text(result.get("paper", ""))

        self.save_checkpoint()
        return result

    def _run_review_stage(self, round_num: int) -> dict[str, Any]:
        """Run simulated peer review."""
        from agents.review_agent import ReviewAgent

        agent = ReviewAgent(client=self.client, config=self.config)
        draft_key = "paper" if round_num == 1 else "revised_paper"
        draft = self.state.get("writing", {}).get(draft_key, "")

        result = agent.run(
            paper=draft,
            journal=self.config.writing.journal,
            round_num=round_num,
        )

        review_path = self.run_dir / f"review_round_{round_num}.md"
        review_path.write_text(result.get("feedback", ""))

        self.save_checkpoint()
        return result

    def _run_revision_stage(self, round_num: int) -> dict[str, Any]:
        """Revise paper based on review feedback."""
        from agents.writing_agent import WritingAgent

        agent = WritingAgent(client=self.client, config=self.config)
        result = agent.revise(
            paper=self.state.get("writing", {}).get("paper", ""),
            feedback=self.state.get(f"review_round_{round_num}", {}).get("feedback", ""),
        )

        revised_path = self.run_dir / f"draft_v{round_num + 1}.md"
        revised_path.write_text(result.get("revised_paper", ""))

        self.save_checkpoint()
        return result

    def _save_final_outputs(self) -> None:
        """Copy the final paper version to paper_final.md."""
        final_paper = ""
        # Find the latest revision
        for round_num in range(self.config.writing.review_rounds, 0, -1):
            rev = self.state.get(f"review_round_{round_num}", {})
            if rev.get("revised_paper"):
                final_paper = rev["revised_paper"]
                break
        if not final_paper:
            final_paper = self.state.get("writing", {}).get("paper", "")

        if final_paper:
            (self.run_dir / "paper_final.md").write_text(final_paper)

        self.save_checkpoint()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_checkpoint(self) -> None:
        checkpoint_dir = Path(self.config.output.checkpoint_dir)
        checkpoint_file = checkpoint_dir / f"{self.run_dir.name}.json"
        if checkpoint_file.exists():
            with open(checkpoint_file) as f:
                self.state = json.load(f)

    @staticmethod
    def _infer_domain(topic: str) -> str:
        topic_lower = topic.lower()
        if any(kw in topic_lower for kw in ["sar", "optical", "radar", "satellite", "lidar", "hyperspectral"]):
            return "remote_sensing"
        if any(kw in topic_lower for kw in ["gwr", "mgwr", "gis", "spatial regression", "spatial autocorrelation"]):
            return "giscience"
        if any(kw in topic_lower for kw in ["seismic", "geology", "geophysics", "hydrology", "climate"]):
            return "geoscience"
        return "giscience"

    @staticmethod
    def _infer_methods(topic: str) -> str:
        topic_lower = topic.lower()
        methods = []
        if any(kw in topic_lower for kw in ["gwr", "geographically weighted"]):
            methods.append("GWR/MGWR")
        if any(kw in topic_lower for kw in ["kriging", "geostatistic"]):
            methods.append("Kriging/Geostatistics")
        if any(kw in topic_lower for kw in ["deep learning", "cnn", "transformer", "neural"]):
            methods.append("Deep Learning")
        if any(kw in topic_lower for kw in ["spatial autocorrelation", "moran"]):
            methods.append("Spatial Autocorrelation Analysis")
        return ", ".join(methods) if methods else "Spatial Statistics"
