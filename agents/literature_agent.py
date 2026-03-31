"""
Literature Agent — searches, retrieves, and synthesizes academic literature.
Performs geo-domain-aware query expansion and gap analysis.
"""

from __future__ import annotations

import json
from typing import Any

import anthropic

from core.config import AgentConfig

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

    def __init__(self, client: anthropic.Anthropic, config: AgentConfig) -> None:
        self.client = client
        self.config = config

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

        prompt = f"""Generate {self.config.literature.max_papers // 5} optimized ArXiv/Semantic Scholar search queries for:

Topic: {topic}
Domain: {domain}
Domain keywords: {domain_kws}

Rules:
- Each query should target a different aspect of the topic
- Include both specific method terms and broader conceptual terms
- Format: one query per line, no numbering
- Optimize for recall (broad) not precision for the first 2 queries, then precision for the rest"""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        queries = [q.strip() for q in response.content[0].text.strip().split("\n") if q.strip()]
        return queries[:6]  # cap at 6 queries

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
                            "abstract": result.summary[:500],
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
        papers_text = "\n\n".join(
            f"**{p.get('title', 'Unknown')}** ({p.get('year', 'n.d.')})\n"
            f"Authors: {', '.join(p.get('authors', ['Unknown']))}\n"
            f"Abstract: {p.get('abstract', 'Not available')}"
            for p in papers[:20]  # use top 20 for synthesis
        )

        prompt = f"""Write a structured literature review for the following research topic.

## Topic
{topic}

## Domain Context
{json.dumps(geo_context, indent=2)}

## Retrieved Papers
{papers_text}

## Required Sections
1. **Introduction to the Research Area** — overview and significance
2. **Key Methods and Approaches** — what methods have been used and their limitations
3. **Key Findings** — major empirical findings in the literature
4. **Research Gaps** — what is missing, contradictory, or underexplored
5. **Proposed Novel Hypotheses** — 3 specific, testable hypotheses grounded in the gaps

Be specific. Reference actual papers when possible. Use academic writing style."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=4096,
            system=LITERATURE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _extract_hypotheses(self, review_text: str) -> list[dict[str, str]]:
        """Extract structured hypotheses from the review text."""
        prompt = f"""Extract the research hypotheses from this literature review.
Return a JSON array of objects, each with: "id", "hypothesis", "rationale", "suggested_method", "suggested_dataset".

Literature Review:
{review_text[:3000]}

Return ONLY valid JSON, no other text."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return [{"id": "H1", "hypothesis": "See literature review", "rationale": "", "suggested_method": "", "suggested_dataset": ""}]
