---
name: paper-covert
description: Converts the final Markdown manuscript from `paper-draft` / `paper-review-loop` into a submission package for the target venue — modular LaTeX (one file per section), compiled PDF, and Word `.docx`. Venue is read from `output/PAPER_PLAN.md` (or argument) and routed through a small YAML profile. Does not rewrite prose, score, or invent citations.
argument-hint: [venue-or-manuscript-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Skill: paper-covert

Convert the final manuscript in `output/manuscript/` into a submission package for: **$ARGUMENTS**

> Naming: the pipeline in `paper-writing-pipeline` references this as `/paper-convert`. Folder name is `paper-covert` per invocation; they resolve to the same skill.

---

## Constants

- **SRC** — first existing of: `output/manuscript/MANUSCRIPT_REVISED.md` → `output/manuscript/MANUSCRIPT_DRAFT.md` → concatenated `sections_revised/*.md` → concatenated `sections/*.md`.
- **SECTIONS_SRC** — `output/manuscript/sections_revised/` if present, else `sections/`.
- **PLAN = `output/PAPER_PLAN.md`** — for title, keywords, venue, figure/table plan, declarations.
- **OUT = `output/submission/`**
- **VENUE** — argument `venue:<name>` → `PAPER_PLAN.md` §0/§2 → `research_contract.md` → `IJGIS`.
- **PROFILE** — `./profiles/<venue>.yaml`, else `./profiles/generic.yaml`.

Inline override: `/paper-covert — venue: ISPRS, mode: latex`. Modes: `all` (default), `latex`, `pdf`, `docx`.

---

## Inputs

Primary:
- `SRC` (Markdown manuscript)
- `SECTIONS_SRC/*.md`
- `PLAN`

Supporting (read when present):
- `output/manuscript/CLAIM_RISK_REPORT.md`, `COVERAGE_GAPS.md`, `CITATION_GAPS.md` — surface unresolved items into the manifest, do not fix them.
- `output/figures/FIGURE_MANIFEST.md`, `output/figures/FIGURE_CAPTIONS.md`, `output/figures/`
- `memory/paper-cache/*.json`, local `references.bib`
- `data/DATA_MANIFEST.md`, `research_contract.md`
- `./profiles/<venue>.yaml`

---

## Outputs

```
output/submission/
├── SUBMISSION_MANIFEST.md      # source, venue, files, readiness, unresolved items
├── latex/
│   ├── main.tex                # lean entry: \input's only
│   ├── preamble.tex            # packages + placeholder env
│   ├── metadata.tex            # title, authors, keywords, highlights
│   ├── references.bib          # copied or synthesized; else stub
│   ├── build.sh                # latexmk → pdflatex fallback
│   ├── sections/
│   │   ├── 01_abstract.tex
│   │   ├── 02_introduction.tex
│   │   ├── 03_related_work.tex
│   │   ├── 04_data.tex
│   │   ├── 05_methodology.tex
│   │   ├── 06_experiments.tex
│   │   ├── 07_results.tex
│   │   ├── 08_discussion.tex
│   │   ├── 09_limitations.tex
│   │   ├── 10_conclusion.tex
│   │   ├── 11_declarations.tex
│   │   └── appendix_*.tex
│   └── figures/                # copied from output/figures/ per FIGURE_MANIFEST
├── pdf/MANUSCRIPT_SUBMISSION_READY.pdf
└── docx/MANUSCRIPT_SUBMISSION_READY.docx
```

Filenames are stable; overwrite in place. Two-digit zero-padded section prefixes match `paper-draft`.

---

## Workflow

### 1. Resolve source and venue
Pick `SRC` by priority above. Read `PLAN` for title, keywords, venue, declarations, figure/table plan. Load `PROFILE`. Record the source path, venue, and profile choice at the top of `SUBMISSION_MANIFEST.md`.

### 2. Build the LaTeX tree
- Write `main.tex`, `preamble.tex`, `metadata.tex` from `./templates/`, filling in profile fields (`documentclass`, `class_options`, `bib_style`, `bib_engine`) and manuscript metadata (title, keywords, highlights when the venue requires them).
- For each section in `SECTIONS_SRC/`, write one `.tex` file under `latex/sections/` using these conversion rules:
  - `#`/`##`/`###` → `\section`/`\subsection`/`\subsubsection` with a `\label{sec:...}`.
  - Markdown emphasis, lists, block quotes, inline/display math → LaTeX equivalents.
  - Markdown tables → `booktabs` `tabular`; tables ≥ 15 rows extracted to `tables/`.
  - Images `![cap](figures/X.png)` → `figure` env with `\includegraphics`, `\caption`, `\label{fig:X}`.
  - Citations: `\cite{key}` kept as-is when resolvable in `references.bib`; `[CITE: topic]` rendered via a visible `\citeplaceholder{topic}` macro and logged in the manifest.
  - `[PLACEHOLDER — …]` blocks wrapped in a visible `placeholder` environment so they show in the PDF.
- Copy figures listed in `FIGURE_MANIFEST.md` into `latex/figures/`. Do not reference figures not in the manifest.

Section file mapping adapts to the manuscript's actual section list; `PLAN` §19 is authoritative when it differs from the default 01–11 layout. Appendices use `appendix_<letter>.tex`.

### 3. Wire the bibliography
- If a `.bib` exists under `output/manuscript/` or repo root → copy to `latex/references.bib`.
- Else synthesize from `memory/paper-cache/*.json` — copy only entries whose keys appear in the manuscript; never invent.
- Use `bib_style` and `bib_engine` from the profile. Unresolved `[CITE: …]` or missing keys → list in the manifest's **Bibliography gaps** section; do not fabricate.

### 4. Build the PDF
Write `build.sh` from `./templates/build_script_template.sh`. Run it (`latexmk -pdf`; fallback to `pdflatex + bibtex + pdflatex ×2`). Copy `main.pdf` to `pdf/MANUSCRIPT_SUBMISSION_READY.pdf`. On failure, keep the LaTeX tree intact and record the first error + likely cause in the manifest under **Build**.

### 5. Export the DOCX
Prefer `pandoc latex/main.tex -o docx/MANUSCRIPT_SUBMISSION_READY.docx --citeproc --bibliography=latex/references.bib`. If Pandoc rejects venue LaTeX, fall back to `pandoc` on the source Markdown (concatenated `SECTIONS_SRC/*.md`). If Pandoc is unavailable, record `docx: blocked` in the manifest.

### 6. Write the manifest
Write `SUBMISSION_MANIFEST.md` from `./templates/SUBMISSION_MANIFEST_TEMPLATE.md`:
- source manuscript path + readiness (`reviewed` / `revised` / `draft-only`)
- venue + profile (flag fallback `generic` explicitly)
- files generated with paths
- **Bibliography gaps** (unresolved citations) — carried from `CITATION_GAPS.md` plus anything new.
- **Asset gaps** — figures referenced but missing from the manifest; figures marked `Needs revision`.
- **Content gaps** — `[PLACEHOLDER …]` blocks remaining in the LaTeX.
- **Build** — PDF engine, pass/fail, warning counts; DOCX pathway, pass/fail.
- **Readiness** — honest per-format statement. Do not mark "submission-ready" while any gap above is open or a build failed.

Append one line to `output/FINDINGS.md`:
```
YYYY-MM-DD paper-covert venue=<V> source=<revised|draft> pdf=<ok|fail> docx=<ok|fail> gaps=<K>
```

---

## Decision rules

- **Venue structure**: `PROFILE` defaults → `PLAN` §19 overrides. Log the final structure in the manifest.
- **No publisher class bundled**: use `article` + the profile's bib style; record in the manifest that a publisher re-wrap is needed at submission time. Never claim the output is an official publisher template.
- **Incomplete manuscript**: still produce the package; placeholders stay visible; readiness is `partial`.
- **Mode restriction**: `mode:latex` stops after step 3; `mode:pdf` skips DOCX; `mode:docx` still needs LaTeX for the Pandoc path unless Markdown→DOCX is forced.

---

## Guardrails

Do **not**:
- rewrite, soften, or restructure prose — that is `paper-review-loop`.
- invent citations, bibliographic entries, figure files, or publisher-private rules.
- reference figures not listed in `FIGURE_MANIFEST.md`.
- silently drop content when a format conversion can't handle it — log it.
- label the package "submission-ready" with open gaps or a failed build.
- modify `output/manuscript/`. This skill is read-only on it.

---

## Supporting files

Under this skill:
- `templates/main_template.tex`, `preamble_template.tex`, `metadata_template.tex`, `section_template.tex`, `build_script_template.sh`, `SUBMISSION_MANIFEST_TEMPLATE.md`, `CONVERSION_CHECKLIST.md`, `VENUE_ROUTING_README.md`, `BIBLIOGRAPHY_GAP_CHECKLIST.md`.
- `profiles/`: `generic.yaml`, `ijgis.yaml`, `isprs_jprs.yaml`, `rse.yaml`, `tgis.yaml`, `aag_annals.yaml`, `ieee_tgrs.yaml`. Each profile declares `documentclass`, `class_options`, `bib_style`, `bib_engine`, word/abstract/figure limits, highlights requirement, and a note on publisher-class availability.

## Composing with other skills

```
/paper-draft → /paper-review-loop → /paper-covert → /submit-check
```

`paper-covert` packages; `submit-check` validates venue compliance. They do not overlap.
