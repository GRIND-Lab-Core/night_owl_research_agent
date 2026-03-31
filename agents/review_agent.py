"""
Review Agent — simulates multi-reviewer peer review for geo/GIS papers.
Provides structured feedback mirroring real journal review criteria.
"""

from __future__ import annotations

import anthropic
from core.config import AgentConfig

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

    def __init__(self, client: anthropic.Anthropic, config: AgentConfig) -> None:
        self.client = client
        self.config = config

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
        prompt = f"""You are {persona['name']}, an expert reviewer in {persona['expertise']}.
Your review style: {persona['style']}.

Review the following paper for {journal} (Round {round_num}).

## Evaluation Criteria
{criteria_str}

## Paper
{paper[:6000]}

## Your Review
Provide a detailed review with:
1. **Summary** (2–3 sentences)
2. **Major Concerns** (numbered list — issues that must be addressed)
3. **Minor Concerns** (bulleted — optional improvements)
4. **Recommendation**: Major Revision / Minor Revision / Accept / Reject

Be constructive but critical. Focus on geo/spatial aspects specifically."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        return f"## {persona['name']}\n\n{response.content[0].text}"

    def _get_editor_summary(self, reviews: list[str], journal: str) -> str:
        combined_reviews = "\n\n---\n\n".join(reviews)
        prompt = f"""As the Editor-in-Chief of {journal}, summarize the reviews and make a decision.

## Reviewer Comments
{combined_reviews}

Provide:
1. **Editorial Decision**: Accept / Minor Revision / Major Revision / Reject
2. **Rationale** (2–3 sentences)
3. **Priority Issues** to address (if not Accept/Reject)"""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

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
