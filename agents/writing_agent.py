"""
Writing Agent — drafts and revises full academic papers using journal-specific templates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import anthropic

from core.config import AgentConfig
from core.token_optimizer import (
    ResponseCache,
    TokenLedger,
    build_windowed_prompt,
    optimized_call,
    truncate_field,
)

WRITING_SYSTEM_PROMPT = """\
You are an expert academic writer specializing in geoscience, remote sensing, and GIScience.
You write clear, precise, and compelling scientific papers. Your writing:
- Uses active voice where appropriate
- Provides quantitative results with confidence intervals and effect sizes
- Clearly connects methods to research questions
- Discusses limitations honestly
- Follows the target journal's style and length requirements

Always produce complete, well-structured sections, not outlines.
"""

SECTIONS_ORDER = ["abstract", "introduction", "study_area", "data", "methods", "results", "discussion", "conclusion", "references"]


class WritingAgent:
    """
    Generates full academic paper drafts using journal-specific templates,
    with support for section-by-section generation and iterative revision.
    """

    def __init__(
        self,
        client: anthropic.Anthropic,
        config: AgentConfig,
        ledger: TokenLedger | None = None,
        cache: ResponseCache | None = None,
    ) -> None:
        self.client = client
        self.config = config
        self.template_dir = Path("templates")
        self.ledger = ledger
        self.cache = cache
        self._ctx_budget = config.token_optimizer.context_token_budget

    def run(
        self,
        topic: str,
        literature: dict[str, Any],
        experiment: dict[str, Any],
        geo_context: dict[str, Any],
        journal: str,
    ) -> dict[str, Any]:
        """Generate a complete paper draft."""
        template = self._load_template(journal)
        sections = {}

        context = {
            "topic": topic,
            "literature_summary": literature.get("markdown", "")[:2000],
            "hypotheses": literature.get("hypotheses", []),
            "results": experiment.get("results", {}),
            "methods_used": experiment.get("methods", []),
            "geo_context": geo_context,
            "journal": journal,
            "template_guidance": template,
        }

        for section in SECTIONS_ORDER:
            sections[section] = self._write_section(section, context)

        paper = self._assemble_paper(sections, journal)
        return {"paper": paper, "sections": sections}

    def revise(self, paper: str, feedback: str) -> dict[str, Any]:
        """Revise the paper based on reviewer feedback."""
        # Truncate both inputs so revision stays within context window
        paper_trunc = truncate_field(paper, 6_000)
        feedback_trunc = truncate_field(feedback, 1_200)

        prompt = (
            "Revise the paper below based on the reviewer feedback.\n\n"
            f"## Reviewer Feedback\n{feedback_trunc}\n\n"
            f"## Original Paper\n{paper_trunc}\n\n"
            "Instructions:\n"
            "- Address each reviewer comment specifically\n"
            "- Add a 'Response to Reviewers' section at the end\n"
            "- Maintain original length (±10%)\n"
            "Return the complete revised paper."
        )
        text = optimized_call(
            self.client, WRITING_SYSTEM_PROMPT, prompt,
            task_type="revision",
            preferred_model=self.config.backend.orchestrator,
            task_complexity="complex",
            ledger=self.ledger,
            cache=self.cache,
        )
        return {"revised_paper": text}

    def write_section(self, section_name: str, context: dict[str, Any]) -> str:
        """Public method: write a single section. Used by /write-section skill."""
        return self._write_section(section_name, context)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _write_section(self, section: str, context: dict[str, Any]) -> str:
        """Generate a single paper section using windowed context and tiered models."""
        section_guidance = self._get_section_guidance(section, context.get("journal", ""))
        geo_ctx = context.get("geo_context", {})
        results_raw = json.dumps(context.get("results", {}), default=str)

        # Use context windowing: pack the most relevant fields within budget
        task_type = "section_long" if section in ("methods", "results", "discussion") else "section_short"
        user_prompt = build_windowed_prompt(
            sections=[
                (f"Write: {section.replace('_', ' ').title()} ({context.get('journal', '')} paper)", "", 2.5),
                ("Topic", context.get("topic", ""), 2.0),
                ("Domain & Methods",
                 f"Domain: {geo_ctx.get('domain', 'GIScience')}\n"
                 f"Methods: {', '.join(context.get('methods_used', ['spatial regression']))}",
                 1.5),
                ("Hypotheses", json.dumps(context.get("hypotheses", [])[:2]), 1.3),
                ("Results Summary", truncate_field(results_raw, 400), 1.2),
                ("Section Guidance", section_guidance, 1.8),
            ],
            token_budget=self._ctx_budget,
            header=f"Write the complete **{section.replace('_', ' ').title()}** section. Use Markdown.",
        )

        return optimized_call(
            self.client, WRITING_SYSTEM_PROMPT, user_prompt,
            task_type=task_type,
            preferred_model=self.config.backend.orchestrator,
            task_complexity="default",
            ledger=self.ledger,
            cache=self.cache,
        )

    def _get_section_guidance(self, section: str, journal: str) -> str:
        """Return journal-specific guidance for a section."""
        journal_limits = {
            "IJGIS": {"abstract": 200, "total": 8000},
            "RSE": {"abstract": 300, "total": 10000},
            "IEEE_TGRS": {"abstract": 250, "total": 8000},
            "GRL": {"abstract": 150, "total": 4000},
        }
        limits = journal_limits.get(journal, {"abstract": 250, "total": 8000})

        guidance_map = {
            "abstract": f"Max {limits['abstract']} words. Include: background, objective, methods, key results, conclusion.",
            "introduction": "3–5 paragraphs. End with explicit research objectives/questions.",
            "study_area": "Describe geographic extent, key characteristics, why chosen. Include coordinates.",
            "data": "Detail each dataset: source, temporal/spatial resolution, preprocessing steps.",
            "methods": "Be reproducible: formulas, parameters, software versions.",
            "results": "Report statistics, confidence intervals, significance levels. Reference figures/tables.",
            "discussion": "Interpret results, compare to literature, discuss spatial patterns, acknowledge limitations.",
            "conclusion": "Summarize contributions, implications, future work.",
            "references": "Format per journal style. Include DOIs.",
        }
        return guidance_map.get(section, "Write this section following standard academic conventions.")

    def _load_template(self, journal: str) -> str:
        """Load journal-specific template guidance."""
        journal_to_file = {
            "IJGIS": "giscience/ijgis.md",
            "RSE": "remote_sensing/remote_sensing_env.md",
            "IEEE_TGRS": "remote_sensing/ieee_tgrs.md",
            "GRL": "geoscience/grl_template.md",
            "ISPRS": "remote_sensing/isprs_jprs.md",
            "AAG": "giscience/annals_aag.md",
            "TGIS": "giscience/transactions_gis.md",
        }
        template_file = self.template_dir / journal_to_file.get(journal, "giscience/ijgis.md")
        if template_file.exists():
            return template_file.read_text()
        return f"Follow standard formatting guidelines for {journal}."

    def _assemble_paper(self, sections: dict[str, str], journal: str) -> str:
        """Assemble all sections into a complete paper."""
        header = f"# [Title: Replace with your paper title]\n\n*Target journal: {journal}*\n\n---\n\n"
        body = "\n\n---\n\n".join(
            f"## {section.replace('_', ' ').title()}\n\n{content}"
            for section, content in sections.items()
            if content
        )
        return header + body
