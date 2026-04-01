"""
Literature Agent — searches, retrieves, and synthesizes academic literature.
Performs geo-domain-aware query expansion and gap analysis.
"""

from __future__ import annotations

import json
from typing import Any

import anthropic

from core.config import AgentConfig
from core.token_optimizer import (
    ResponseCache,
    TokenLedger,
    build_windowed_prompt,
    optimized_call,
    truncate_papers,
)

GEO_DOMAIN_KEYWORDS = {
    "giscience": [
        "spatial", "geospatial", "GIS", "geographic information",
        "spatial autocorrelation", "spatial regression", "spatial heterogeneity",
        "GWR", "MGWR", "kriging", "spatial econometrics", "geostatistics",
    ],
    "remote_sensing": [
        "remote sensing", "satellite", "SAR", "optical imagery", "LiDAR",
        "hyperspectral", "change detection", "image classification",
        "deep learning remote sensing", "Sentinel", "Landsat",
    ],
    "geoscience": [
        "geophysics", "geology", "Earth system", "hydrology", "climate",
        "seismology", "geomorphology", "atmospheric science",
    ],
}

LITERATURE_SYSTEM_PROMPT = """\
You are a senior geoscientist and GIScientist with deep expertise in spatial analysis,
remote sensing, and geographic information science. Your task is to:

1. Analyze a research topic and identify key concepts, methods, and gaps
2. Generate optimized search queries for ArXiv and Semantic Scholar
3. Synthesize retrieved papers into a structured literature review
4. Identify 2–4 novel, feasible research hypotheses based on identified gaps

Always produce output in structured Markdown with clear sections.
Be specific about methods, datasets, and metrics used in the literature.
"""


class LiteratureAgent:
    """
    Searches ArXiv and Semantic Scholar for relevant papers and synthesizes
    a structured literature review with gap analysis and novel hypotheses.
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
        self.ledger = ledger
        self.cache = cache
        self._abstract_budget = config.token_optimizer.abstract_token_budget

    def run(self, topic: str, geo_context: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Execute the full literature review pipeline.

        Returns:
            Dict with keys: markdown, hypotheses, papers, search_queries
        """
        geo_context = geo_context or {}

        # Step 1: Generate search queries
        queries = self._generate_queries(topic, geo_context)

        # Step 2: Search (real search via arxiv/semantic_scholar tools or web)
        papers = self._fetch_papers(queries)

        # Step 3: Synthesize literature review
        review = self._synthesize(topic, papers, geo_context)

        # Step 4: Extract hypotheses
        hypotheses = self._extract_hypotheses(review)

        return {
            "markdown": review,
            "hypotheses": hypotheses,
            "papers": papers,
            "search_queries": queries,
        }

    def _generate_queries(self, topic: str, geo_context: dict[str, Any]) -> list[str]:
        """Use Claude to generate optimized search queries with geo-domain expansion."""
        domain = geo_context.get("domain", "giscience")
        domain_kws = " OR ".join(GEO_DOMAIN_KEYWORDS.get(domain, [])[:5])
        n_queries = max(2, self.config.literature.max_papers // 5)

        prompt = (
            f"Generate {n_queries} ArXiv search queries for: {topic}\n"
            f"Domain: {domain} | Keywords: {domain_kws}\n"
            "One query per line. Vary specificity: first 2 broad, rest precise."
        )
        text = optimized_call(
            self.client, LITERATURE_SYSTEM_PROMPT, prompt,
            task_type="query_generation",
            preferred_model=self.config.backend.orchestrator,
            task_complexity="simple",
            ledger=self.ledger,
            cache=self.cache,
        )
        queries = [q.strip() for q in text.strip().split("\n") if q.strip()]
        return queries[:6]

    def _fetch_papers(self, queries: list[str]) -> list[dict[str, str]]:
        """
        Fetch papers from ArXiv. In a full deployment, this would use the arxiv MCP
        or the arxiv Python library. Returns mock data if library unavailable.
        """
        try:
            import arxiv

            papers = []
            seen_ids = set()
            max_per_query = max(1, self.config.literature.max_papers // len(queries))

            for query in queries:
                search = arxiv.Search(query=query, max_results=max_per_query)
                for result in search.results():
                    if result.entry_id not in seen_ids:
                        seen_ids.add(result.entry_id)
                        papers.append({
                            "title": result.title,
                            "authors": [str(a) for a in result.authors[:3]],
                            # Truncate abstract to budget at fetch time — saves tokens in synthesis
                            "abstract": result.summary[: self._abstract_budget * 4],
                            "year": result.published.year,
                            "url": result.entry_id,
                            "source": "arxiv",
                        })
            return papers[: self.config.literature.max_papers]

        except ImportError:
            # Fallback: return placeholder structure
            return [{"title": f"Paper from query: {q[:50]}", "abstract": "", "source": "arxiv"} for q in queries]

    def _synthesize(self, topic: str, papers: list[dict], geo_context: dict[str, Any]) -> str:
        """Synthesize papers into a structured literature review."""
        # Truncate abstracts to per-paper budget before assembling the prompt
        opt_cfg = self.config.token_optimizer
        papers_trunc = truncate_papers(papers[:20], budget_per_paper=self._abstract_budget)

        papers_text = "\n\n".join(
            f"**{p.get('title', 'Unknown')}** ({p.get('year', 'n.d.')})\n"
            f"Authors: {', '.join(p.get('authors', ['Unknown']))}\n"
            f"Abstract: {p.get('abstract', 'Not available')}"
            for p in papers_trunc
        )

        # Use context windowing: domain context gets lower priority than papers
        context_block = build_windowed_prompt(
            sections=[
                ("Topic", topic, 2.0),
                ("Domain Context", json.dumps(geo_context), 1.0),
                ("Retrieved Papers", papers_text, 1.8),
            ],
            token_budget=opt_cfg.context_token_budget,
            header="Synthesize a literature review from the materials below.",
        )

        instructions = (
            "\n\nRequired sections:\n"
            "1. Introduction to the Research Area\n"
            "2. Key Methods and Limitations\n"
            "3. Key Findings\n"
            "4. Research Gaps\n"
            "5. Proposed Novel Hypotheses (3, testable, grounded in gaps)\n\n"
            "Be specific. Reference papers by title. Use academic writing style."
        )

        return optimized_call(
            self.client, LITERATURE_SYSTEM_PROMPT, context_block + instructions,
            task_type="synthesis",
            preferred_model=self.config.backend.orchestrator,
            task_complexity="complex",
            ledger=self.ledger,
            cache=self.cache,
        )

    def _extract_hypotheses(self, review_text: str) -> list[dict[str, str]]:
        """Extract structured hypotheses from the review text."""
        from core.token_optimizer import truncate_field
        review_snippet = truncate_field(review_text, 1_500)  # limit context for JSON extraction

        prompt = (
            "Extract research hypotheses from the review below.\n"
            'Return a JSON array; each object: {"id","hypothesis","rationale","suggested_method","suggested_dataset"}.\n'
            "Return ONLY valid JSON.\n\n"
            f"Review:\n{review_snippet}"
        )
        text = optimized_call(
            self.client, "", prompt,
            task_type="json",
            preferred_model=self.config.backend.orchestrator,
            task_complexity="simple",
            ledger=self.ledger,
            cache=self.cache,
        )
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return [{"id": "H1", "hypothesis": "See literature review", "rationale": "",
                     "suggested_method": "", "suggested_dataset": ""}]
