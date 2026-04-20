# Conversion Checklist

> Run through this before reporting the package as complete. One box per row.

## Phase 1 — Source

- [ ] Primary manuscript source identified and readiness labelled.
- [ ] `PAPER_PLAN.md` read for title, venue, keywords, figure/table plan, declarations.
- [ ] `DRAFT_README.md` and `REVIEW_REPORT.md` inspected for readiness signals.

## Phase 2 — Venue

- [ ] Target venue resolved (argument → plan → contract → default).
- [ ] Venue profile `./profiles/<venue>.yaml` loaded, or fallback `generic.yaml` used.
- [ ] Every inferred default recorded in `FORMATTING_ASSUMPTIONS.md`.

## Phase 3 — LaTeX tree

- [ ] `latex/main.tex`, `preamble.tex`, `metadata.tex` written.
- [ ] One `.tex` file per manuscript section under `latex/sections/`.
- [ ] Appendices written when `PAPER_PLAN.md` prescribes them.
- [ ] All Markdown headings mapped to correct section depth.
- [ ] Placeholders wrapped in `placeholder` environment, visible in PDF.
- [ ] Figures copied into `latex/figures/`; paths relative.
- [ ] Tables inlined or extracted into `latex/tables/`.
- [ ] `FIGURE_TABLE_MAP.md` written with full id → file → label trace.

## Phase 4 — Bibliography

- [ ] `references.bib` copied or synthesized.
- [ ] Citation keys resolve against the bib where possible.
- [ ] Unresolved citations listed in `BIBLIOGRAPHY_GAPS.md`.
- [ ] Bibliography style and engine match venue profile.

## Phase 5 — PDF

- [ ] `build.sh` written.
- [ ] Compilation attempted.
- [ ] `latex/build.log` preserved on failure.
- [ ] On success: PDF copied to `pdf/MANUSCRIPT_SUBMISSION_READY.pdf`.
- [ ] On success: `pdf/PDF_BUILD_REPORT.md` written with warnings / page count.
- [ ] On failure: diagnosis recorded; LaTeX tree preserved.

## Phase 6 — DOCX

- [ ] Conversion pathway chosen and documented in `DOCX_CONVERSION_NOTES.md`.
- [ ] Figure count in DOCX = figure count in LaTeX.
- [ ] Table count in DOCX = table count in LaTeX.
- [ ] Citation count in DOCX ≥ resolved citation count in LaTeX.
- [ ] Section hierarchy preserved.

## Phase 7 — Manifest

- [ ] `SUBMISSION_MANIFEST.md` written with source, venue, outputs, status.
- [ ] `CONVERSION_REPORT.md` logs every decision.
- [ ] `READINESS_NOTES.md` states honest readiness per format.
- [ ] `CONVERSION_GAPS.md` lists placeholders, broken refs, missing assets.
- [ ] `ASSET_STATUS.md` lists copied / missing figures and tables.
- [ ] One line appended to `output/PROJ_NOTES.md`.

## Do-not ship flags

If any of these are true, readiness **cannot** be marked `ready`:

- [ ] Any `[PLACEHOLDER ...]` block remains.
- [ ] Any unresolved `CRITICAL-*` row in `CLAIM_RISK_REPORT.md`.
- [ ] Any unresolved row in `BIBLIOGRAPHY_GAPS.md`.
- [ ] PDF or DOCX build failed.
- [ ] Venue profile is fallback `generic`.
