"""
Review Agent — simulates multi-reviewer peer review for geo/GIS papers.
Provides structured feedback mirroring real journal review criteria.
"""

from __future__ import annotations

import anthropic
from core.config import AgentConfig
from core.token_optimizer import ResponseCache, TokenLedger, optimized_call, truncate_field

JOURNAL_REVIEW_CRITERIA = {
    "IJGIS": [
        "Theoretical contribution to GIScience",
        "Methodological rigor and reproducibility",
        "Spatial analysis appropriateness",
        "Novelty over existing GIS methods",
        "Clarity and structure",
    ],
    "RSE": [
        "Remote sensing data quality and validation",
        "Algorithm novelty and comparison to baselines",
        "Accuracy assessment (OA, kappa, RMSE)",
        "Generalizability across scenes/sensors",
        "Reproducibility",
    ],
    "IEEE_TGRS": [
        "Signal processing and algorithm design",
        "Theoretical soundness",
        "Experimental validation",
        "Comparison to state-of-the-art",
        "Manuscript quality",
    ],
    "GRL": [
        "Scientific significance and urgency",
        "Data quality and analysis",
        "Conciseness (letter format: ≤4000 words)",
        "Impact on the field",
    ],
    "DEFAULT": [
        "Novelty and significance",
        "Methodological rigor",
        "Clarity of writing",
        "Statistical validity",
        "Reproducibility",
    ],
}

REVIEWER_PERSONAS = [
    {
        "name": "Reviewer 1",
        "expertise": "Spatial statistics and GWR/MGWR methodology",
        "style": "detailed and technical, focuses on method validity",
    },
    {
        "name": "Reviewer 2",
        "expertise": "Applied geoscience and domain knowledge",
        "style": "practical, focuses on real-world relevance and data quality",
    },
    {
        "name": "Reviewer 3",
        "expertise": "Machine learning and computational methods",
        "style": "critical, compares to modern baselines",
    },
]


class ReviewAgent:
    """
    Simulates peer review from multiple expert reviewers.
    Provides structured feedback mirroring real journal review processes.
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

    def run(self, paper: str, journal: str, round_num: int = 1) -> dict[str, str]:
        """
        Run multi-reviewer peer review simulation.

        Args:
            paper: Paper text (Markdown)
            journal: Target journal code (e.g. "IJGIS", "RSE")
            round_num: Review round number

        Returns:
            Dict with 'feedback' (combined review) and 'decision' (Accept/Revise/Reject)
        """
        criteria = JOURNAL_REVIEW_CRITERIA.get(journal, JOURNAL_REVIEW_CRITERIA["DEFAULT"])
        reviews = []

        for persona in REVIEWER_PERSONAS[:2]:  # Use 2 reviewers by default (save tokens)
            review = self._get_single_review(paper, persona, criteria, journal, round_num)
            reviews.append(review)

        editor_summary = self._get_editor_summary(reviews, journal)
        combined = self._format_combined_review(reviews, editor_summary)

        return {
            "feedback": combined,
            "decision": self._extract_decision(editor_summary),
            "reviews": reviews,
        }

    def _get_single_review(
        self,
        paper: str,
        persona: dict[str, str],
        criteria: list[str],
        journal: str,
        round_num: int,
    ) -> str:
        criteria_str = "\n".join(f"- {c}" for c in criteria)
        # Truncate paper to budget — review quality degrades little past ~4k tokens
        paper_trunc = truncate_field(paper, 4_000)

        prompt = (
            f"You are {persona['name']}, expert in {persona['expertise']} ({persona['style']}).\n"
            f"Review for {journal} (Round {round_num}).\n\n"
            f"Criteria:\n{criteria_str}\n\n"
            f"Paper:\n{paper_trunc}\n\n"
            "Provide:\n1. Summary (2–3 sentences)\n"
            "2. Major Concerns (numbered)\n3. Minor Concerns (bullets)\n"
            "4. Recommendation: Major Revision / Minor Revision / Accept / Reject\n"
            "Focus on geo/spatial aspects."
        )
        text = optimized_call(
            self.client, "", prompt,
            task_type="review",
            preferred_model=self.config.backend.orchestrator,
            task_complexity="default",
            ledger=self.ledger,
            cache=self.cache,
        )
        return f"## {persona['name']}\n\n{text}"

    def _get_editor_summary(self, reviews: list[str], journal: str) -> str:
        combined = truncate_field("\n\n---\n\n".join(reviews), 2_000)
        prompt = (
            f"As Editor-in-Chief of {journal}, summarize these reviews and decide.\n\n"
            f"Reviews:\n{combined}\n\n"
            "Provide:\n1. Editorial Decision (Accept/Minor Revision/Major Revision/Reject)\n"
            "2. Rationale (2–3 sentences)\n3. Priority issues to address"
        )
        return optimized_call(
            self.client, "", prompt,
            task_type="section_short",
            preferred_model=self.config.backend.orchestrator,
            task_complexity="simple",
            ledger=self.ledger,
            cache=self.cache,
        )

    def _format_combined_review(self, reviews: list[str], editor_summary: str) -> str:
        return (
            "# Peer Review Feedback\n\n"
            f"## Editor Decision\n\n{editor_summary}\n\n"
            "---\n\n"
            "## Individual Reviews\n\n"
            + "\n\n---\n\n".join(reviews)
        )

    @staticmethod
    def _extract_decision(editor_summary: str) -> str:
        for decision in ["Accept", "Minor Revision", "Major Revision", "Reject"]:
            if decision.lower() in editor_summary.lower():
                return decision
        return "Major Revision"
