---
name: generate-report
description: Consolidates literature review, idea discovery, refined proposal, experiment plan, experiment results, and automated review into a single NARRATIVE_REPORT.md that is rich enough to drive the downstream paper-writing-pipeline (paper-plan → paper-figure-generate → paper-draft → paper-review-loop → paper-convert).
argument-hint: [optional-focus-or-output-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Skill: generate-report

You build `output/NARRATIVE_REPORT.md` — the single source-of-truth narrative that the downstream `paper-writing-pipeline` reads in its first phase. The report must contain every claim, number, figure spec, citation hook, and limitation the paper-plan / paper-draft skills need so they do not have to re-derive context from scattered logs.

Focus / override: **$ARGUMENTS**

---

## Constants

- **REVIEWER_MODEL = `gpt-5.4`** — Optional Codex MCP review pass over the final narrative.
- **TARGET_VENUE** — Read from `program.md` Section 2 or `research_contract.md`. Default `IJGIS`.
- **OUTPUT_PATH = `output/NARRATIVE_REPORT.md`**
- **TEMPLATE = `skills/generate-report/templates/NARRATIVE_REPORT_TEMPLATE.md`**

---

## Phase 1: Gather Inputs

Read all of the following. Any missing file is a soft failure — record it under "Missing Inputs" in the narrative and continue.

Primary inputs (MUST read):
- `output/LIT_REVIEW_REPORT.md` — themes, gap analysis, key citations
- `output/IDEA_REPORT.md` — ranked idea candidates, pilot scores, chosen idea rationale
- `output/refine-logs/FINAL_PROPOSAL.md` — refined research proposal (problem / method / contributions)
- `output/refine-logs/EXPERIMENT_PLAN.md` — experiment design, run order, success criteria
- `output/EXPERIMENT_RESULT.md` — actual quantitative results
- `output/AUTO_REVIEW._REPORT.md` — adversarial review feedback and required fixes

Supporting inputs (read if referenced or needed for gap-filling):
- `research_contract.md`, `program.md` — active idea, venue, success criteria
- `memory/APPROVED_CLAIMS.md` — verified claims only
- `output/FINDINGS.md` — compact discovery log
- `output/EXPERIMENT_LOG.md` — full experiment record
- `data/DATA_MANIFEST.md` — dataset provenance
- `output/spatial-analysis/` — spatial diagnostics and maps
- `output/figures/` — any already-generated plots or JSONs

> If context remains under budget, scan the entire `night_owl_research_agent/` project for anything that materially changes the story (e.g., new figures, last-minute claims, deprecated methods). Err on the side of reading more context — the downstream pipeline cannot.

---

## Phase 2: Reconcile Evidence

Before writing, resolve conflicts between sources:

1. **Claim vs. result**: Every claim must trace to a row in `memory/APPROVED_CLAIMS.md` or a specific number in `output/EXPERIMENT_RESULT.md`. Flag unsupported claims as `[NEEDS_EVIDENCE]`.
2. **Proposal vs. executed plan**: If `FINAL_PROPOSAL.md` proposed an experiment that was not actually run per `EXPERIMENT_RESULT.md`, record it under "Deferred / Not Executed".
3. **Review fixes applied?**: Cross-check `AUTO_REVIEW._REPORT.md` CRITICAL/MAJOR items against `EXPERIMENT_RESULT.md` and method descriptions. Items not yet addressed go into "Outstanding Review Issues".
4. **Numbers must be exact**: Quote metrics verbatim (e.g., `R² = 0.78`, `Moran's I = 0.12 (p < 0.01)`). Never round or paraphrase.

---

## Phase 3: Write NARRATIVE_REPORT.md

Follow `skills/generate-report/templates/NARRATIVE_REPORT_TEMPLATE.md`. Fill every section — do not ship a template with empty placeholders. If a section genuinely does not apply, write "N/A — reason".

Required content, at minimum:

1. **One-paragraph paper summary** + one-sentence contribution (this is what paper-plan uses to frame the abstract and hero figure).
2. **Problem & motivation** — quantified scale, drawn from LIT_REVIEW_REPORT and FINAL_PROPOSAL.
3. **Gap analysis** — explicit gaps closed by this work, with boundary citations from LIT_REVIEW_REPORT.
4. **Contributions** — numbered, each tied to a specific experiment / claim / figure.
5. **Method** — enough detail for paper-draft to write Methods without re-reading FINAL_PROPOSAL: datasets, study area, preprocessing, model, hyperparameters, evaluation protocol.
6. **Experiments & results** — per-experiment: hypothesis, setup, headline numbers, tables/figures produced, pass/fail vs. success criteria from EXPERIMENT_PLAN.
7. **Claims–evidence matrix** — table: claim | evidence source | quantitative support | figure/table id.
8. **Figure & table plan** — for each: id, type (hero / architecture / map / plot / table), caption draft, data source path, priority. The hero figure needs extra detail (what it compares, visual expectation, why a skim reader gets it).
9. **Related work synthesis** — themes and key papers already verified in LIT_REVIEW_REPORT; group them the way the paper will cite them.
10. **Limitations & threats to validity** — concrete, not generic; include anything from AUTO_REVIEW._REPORT.md not yet fixed.
11. **Reviewer-raised issues and their resolution status** — mirror of AUTO_REVIEW._REPORT.md with status column (`addressed` / `deferred` / `rejected — rationale`).
12. **Future work** — 3–5 specific directions derived from limitations and deferred experiments.
13. **Venue target & page budget** — from program.md / research_contract.md.
14. **Citation seed list** — already-verified keys from LIT_REVIEW_REPORT the paper-draft bib will draw from. Do NOT invent BibTeX here.
15. **Appendix: file-level provenance** — path + one-line summary of every input file consumed, plus a "Missing Inputs" subsection.

---

## Phase 4: Self-Check

Before saving, verify:

- [ ] Every numbered contribution maps to ≥1 row in the claims–evidence matrix.
- [ ] Every claim in the matrix has a file path + line-level reference (e.g., `EXPERIMENT_RESULT.md §3.2`).
- [ ] Every figure in the figure plan has a concrete data source or is flagged as manual.
- [ ] Every CRITICAL/MAJOR item from AUTO_REVIEW._REPORT.md appears in Section 11 with a status.
- [ ] No claim exceeds what APPROVED_CLAIMS.md supports (no fabrication).
- [ ] Venue and page budget are consistent with program.md.
- [ ] Hero figure description is detailed enough that paper-figure-generate can draft it.

If any check fails, fix the narrative before writing.

---

## Phase 5: Optional Cross-Review

If `REVIEWER_MODEL` is reachable via Codex MCP, send the final narrative for a pass:

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    This NARRATIVE_REPORT.md will be the sole input to a paper-writing pipeline.
    Score 1–10 on: (1) story clarity, (2) claim–evidence coverage, (3) figure plan
    completeness, (4) gap articulation, (5) venue fit. For each weakness, give the
    MINIMUM edit required. Be specific and actionable.

    [paste full narrative]
```

If external LLM is not configured, spawn a subagent review instead. Apply feedback, then save.

---

## Phase 6: Output

Write the final narrative to `output/NARRATIVE_REPORT.md`. Append a one-line entry to `output/FINDINGS.md`:

```
[YYYY-MM-DD] generate-report: NARRATIVE_REPORT.md built from LIT_REVIEW / IDEA_REPORT / FINAL_PROPOSAL / EXPERIMENT_PLAN / EXPERIMENT_RESULT / AUTO_REVIEW._REPORT — [N] claims, [M] figures, venue=[VENUE]
```

Report back to the user:

```
📝 NARRATIVE_REPORT.md generated:
- Contributions: [N]
- Claims–evidence rows: [M]
- Figures planned: [auto: X, manual: Y, hero: 1]
- Outstanding review issues: [K]
- Missing inputs: [list or "none"]

Ready to invoke /paper-writing-pipeline "output/NARRATIVE_REPORT.md".
```

---

## Key Rules

- **Large file handling**: If Write fails due to size, fall back to Bash heredoc writes in chunks. Do not ask the user.
- **Never fabricate claims, numbers, or citations.** If an input is missing, flag it; do not guess.
- **Quote numbers verbatim** from `EXPERIMENT_RESULT.md` and `APPROVED_CLAIMS.md`.
- **Preserve provenance.** Every non-trivial statement in the narrative should point to an input file.
- **The narrative is a contract with the next pipeline** — paper-plan, paper-figure-generate, and paper-draft will not re-read the scattered logs. If it is not in NARRATIVE_REPORT.md, it will not appear in the paper.
- **Do NOT generate author info, BibTeX entries, or LaTeX** — those belong to the downstream skills.
- **Respect Prohibited Behaviors in `CLAUDE.md`** — especially the ban on fabricated results and skipping `result-to-claim`.
