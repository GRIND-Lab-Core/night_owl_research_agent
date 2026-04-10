"""
Paper Generator — high-level wrapper for assembling complete papers.
Delegates to WritingAgent and handles LaTeX/PDF conversion.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


class PaperGenerator:
    """Assembles and formats final paper outputs."""

    def __init__(self, output_dir: str | Path = "output") -> None:
        self.output_dir = Path(output_dir)

    def markdown_to_latex(self, markdown_path: Path) -> Path | None:
        """Convert Markdown to LaTeX using pandoc."""
        latex_path = markdown_path.with_suffix(".tex")
        try:
            subprocess.run(
                ["pandoc", str(markdown_path), "-o", str(latex_path),
                 "--standalone", "--bibliography=references.bib"],
                check=True, capture_output=True,
            )
            return latex_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def latex_to_pdf(self, latex_path: Path) -> Path | None:
        """Compile LaTeX to PDF using pdflatex."""
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(latex_path)],
                check=True, capture_output=True, cwd=str(latex_path.parent),
            )
            return latex_path.with_suffix(".pdf")
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def generate(self, markdown_content: str, output_name: str, format: str = "markdown") -> Path:
        """Save paper in the requested format."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        md_path = self.output_dir / f"{output_name}.md"
        md_path.write_text(markdown_content)

        if format == "latex":
            latex_path = self.markdown_to_latex(md_path)
            return latex_path or md_path
        elif format == "pdf":
            latex_path = self.markdown_to_latex(md_path)
            if latex_path:
                pdf_path = self.latex_to_pdf(latex_path)
                return pdf_path or latex_path or md_path
        return md_path
