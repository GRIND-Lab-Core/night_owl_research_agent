"""
Writing Agent — drafts and revises full academic papers using journal-specific templates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import anthropic

from core.config import AgentConfig

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

    def __init__(self, client: anthropic.Anthropic, config: AgentConfig) -> None:
        self.client = client
        self.config = config
        self.template_dir = Path("templates")

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
        prompt = f"""Revise the following paper based on the reviewer feedback.

## Reviewer Feedback
{feedback}

## Original Paper
{paper}

## Instructions
- Address each reviewer comment specifically
- Add a "Response to Reviewers" section at the end documenting changes made
- Maintain the paper's original length (±10%)
- Do not change correct content that was not criticized

Return the complete revised paper."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=8192,
            system=WRITING_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"revised_paper": response.content[0].text}

    def write_section(self, section_name: str, context: dict[str, Any]) -> str:
        """Public method: write a single section. Used by /write-section skill."""
        return self._write_section(section_name, context)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _write_section(self, section: str, context: dict[str, Any]) -> str:
        """Generate a single paper section."""
        section_guidance = self._get_section_guidance(section, context.get("journal", ""))
        prompt = f"""Write the **{section.replace('_', ' ').title()}** section for a {context.get('journal', 'scientific')} paper.

## Paper Topic
{context.get('topic', '')}

## Key Context
- Research domain: {context.get('geo_context', {}).get('domain', 'GIScience')}
- Methods used: {', '.join(context.get('methods_used', ['spatial regression']))}
- Hypotheses: {json.dumps(context.get('hypotheses', [])[:2], indent=2)}

## Results Summary
{json.dumps(context.get('results', {}), indent=2)[:1000]}

## Section Guidance
{section_guidance}

Write the complete {section} section. Use Markdown formatting."""

        response = self.client.messages.create(
            model=self.config.backend.orchestrator,
            max_tokens=2048,
            system=WRITING_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

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
