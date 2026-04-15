---
name: paper-draft
description: Transforms output/PAPER_PLAN.md into a journal-quality Markdown manuscript draft for GIScience, GeoAI, spatial data science, and remote sensing venues (IJGIS, ISPRS JPRS, RSE, TGIS, AAG Annals). Consults referenced literature, experiment, figure, and claim artifacts; supports full drafts, partial drafts, and skeleton drafts depending on readiness. Never fabricates results, metrics, or citations — produces a claim-to-evidence map and coverage-gap report alongside the manuscript.
argument-hint: [section-name-or-"all"-or-plan-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Skill: paper-draft

You turn the plan in **`output/PAPER_PLAN.md`** into a journal-quality manuscript draft for: **$ARGUMENTS**

This skill is the drafting counterpart to `paper-plan` and `paper-figure-generate`. It produces Markdown manuscript files in `output/manuscript/` that downstream skills (`paper-write`, `paper-convert`, `paper-review-loop`) can consume for LaTeX conversion, review, and polish. When invoked inside `paper-writing-pipeline`, this skill is Phase 3's content generator — it writes the *prose*, not the LaTeX scaffolding.

The skill supports the full GIScience / GeoAI / remote sensing manuscript spectrum:
- methodological innovation papers
- system / platform / autonomous-agent papers
- benchmark and evaluation papers
- applied case-study papers
- conceptual / framework papers
- multimodal GeoAI papers
- remote sensing analysis papers
- GIScience theory + method papers

---

## Constants

- **PLAN_PATH = `output/PAPER_PLAN.md`** — source of truth for manuscript intent.
- **MS_DIR = `output/manuscript/`** — all draft artifacts go here.
- **MAIN_DRAFT = `output/manuscript/MANUSCRIPT_DRAFT.md`** — integrated manuscript.
- **SECTIONS_DIR = `output/manuscript/sections/`** — per-section drafts.
- **TARGET_VENUE** — read from `PAPER_PLAN.md` header, else `research_contract.md`, else default `IJGIS`.
- **PAPER_TYPE** — read from `PAPER_PLAN.md` §21 framing, else infer from contributions in §5.
- **APPROVED_CLAIMS = `memory/APPROVED_CLAIMS.md`** — only verified claims may be asserted.
- **LIT_REVIEW_REPORT = `output/LIT_REVIEW_REPORT.md`** — consolidated literature review; Synthesis and Gap Analysis sections ground Related Work and gap framing.
- **FIGURE_MANIFEST = `output/figures/FIGURE_MANIFEST.md`** — figures that actually exist.
- **FIGURE_CAPTIONS = `output/figures/FIGURE_CAPTIONS.md`** — manuscript-ready captions.
- **REVIEWER_MODEL = `gpt-5.4`** — used via Codex MCP for section-level critique (optional).
- **DRAFT_MODE** — one of `full`, `partial`, `skeleton`. Decided in Phase 2 from readiness signals; may be forced by argument.

Override inline: `/paper-draft all — venue: ISPRS, mode: partial`.

---

## Core Philosophy

1. **Evidence over eloquence.** Every non-trivial claim must trace to `APPROVED_CLAIMS.md`, an experiment result file, a literature synthesis, or the `PAPER_PLAN.md` claim-to-evidence map. If a claim cannot be traced, it is softened, marked `[NEEDS EVIDENCE]`, or cut.
2. **Plan is intent, referenced files are truth.** `PAPER_PLAN.md` says *what the paper wants to argue*. The referenced experiment logs, synthesis notes, and figure manifests say *what the project can actually support*. Draft against the intersection.
3. **Readiness-aware drafting.** The skill produces a full, partial, or skeleton manuscript — never a polished-looking draft that silently papers over missing results.
4. **Journal voice is non-negotiable.** IJGIS, ISPRS JPRS, RSE, and TGIS reviewers expect formal, precise, rigor-first prose. No hype, no startup-style framing, no "revolutionary."
5. **Terminology discipline.** Model names, dataset names, system names, metric names, experiment labels, and geographic names are fixed at first use and never drift across sections.
6. **Generator-evaluator separation.** This skill writes. Section scoring and adversarial review happen in `auto-review-loop` / `paper-review-loop`, not here.

---

## Inputs

### Primary
- **`output/PAPER_PLAN.md`** — required. The manuscript orchestration artifact (see `templates/PAPER_PLAN_TEMPLATE.md` for the expected §0–§26 structure).

### Secondary (read on demand when the plan references them, or when specificity demands it)
- `research_contract.md` — active idea, problem, method, success criteria.
- `memory/APPROVED_CLAIMS.md` — the only source of verified numerical / empirical claims.
- `output/LIT_REVIEW_REPORT.md` — consolidated literature review (Findings, Synthesis by theme, ranked Gap Analysis).
- `memory/paper-cache/*.json` — per-paper bibliographic + finding records.
- `output/EXPERIMENT_LOG.md` — full experiment record.
- `output/EXPERIMENT_PLAN.md` — experiment roadmap, baselines, metrics.
- `output/FINDINGS.md` — compact one-line discovery log.
- `output/spatial-analysis/` — ESDA outputs, diagnostics, interpretation notes.
- `output/figures/FIGURE_MANIFEST.md`, `output/figures/FIGURE_CAPTIONS.md` — which figures exist, with captions.
- `output/AUTO_REVIEW.md` — prior reviewer feedback to incorporate.
- `templates/giscience/` · `templates/remote_sensing/` · `templates/geoscience/` — venue style guides.
- `skills/knowledge/academic-writing.md` · `skills/knowledge/apa-citations.md` · `skills/knowledge/spatial-methods.md` · `skills/knowledge/geoai-domain.md` — domain and style references.
- `skills/shared-references/writing-principles.md` · `skills/shared-references/venue-checklists.md` — load only when drafting Abstract, Introduction, Related Work, or finalizing a venue pass.

### Argument forms
- `all` — draft the full manuscript.
- `abstract` · `introduction` · `related-work` · `data` · `methods` · `experiments` · `results` · `discussion` · `limitations` · `conclusion` — draft a single section.
- A path to an alternative plan file — use instead of `PLAN_PATH`.

---

## Outputs

All outputs live under `output/manuscript/`:

| File | Purpose |
|---|---|
| `MANUSCRIPT_DRAFT.md` | Integrated Markdown manuscript (title → conclusion). |
| `ABSTRACT_DRAFT.md` | Stand-alone abstract + keywords. |
| `sections/01_introduction.md` ... `sections/NN_conclusion.md` | Per-section drafts. |
| `CLAIM_SUPPORT_MAP.md` | Every non-trivial claim in the draft mapped to its evidence source and confidence. |
| `COVERAGE_GAPS.md` | Sections, claims, figures, or citations that are missing, weak, or flagged. |
| `CITATION_GAPS.md` | Claims that need a supporting citation we do not yet have. |
| `SECTION_NOTES.md` | Per-section notes on scope decisions, softened claims, deferred content. |
| `REVISION_NOTES.md` | Outstanding items for the next drafting pass or human review. |
| `DRAFT_README.md` | Header summary: mode, venue, paper type, readiness, word counts, next actions. |

File-naming convention:
- Section files use two-digit zero-padded prefixes in manuscript order (`01_`, `02_`, ...).
- Revisions of a section are saved over the same path; prior versions are preserved in git, not in filename suffixes.
- A `v` suffix (`MANUSCRIPT_DRAFT_v2.md`) is used only when the user explicitly requests side-by-side versions.

---

## Workflow

### Phase 1 — Read and interpret `PAPER_PLAN.md`

Read the full plan. Extract, at minimum:

- §0 Document Status → plan version, target journal, manuscript type, **readiness level**.
- §1 Paper summary → working title, one-sentence claim, short abstract, keywords.
- §2 Journal strategy → audience, tone expectations, rigor / application emphasis.
- §3–§4 Motivation + Gap → the story arc for Introduction.
- §5 Novelty and contributions → contribution list and contribution *types* (methodological / system / benchmark / applied / conceptual).
- §6 Research questions and hypotheses.
- §7–§8 Scope, data, materials → Data / Study Area section.
- §9 Methodological plan → Methods section spine.
- §10 Experiments + §11 Results → Experiments and Results sections.
- §12 Claim-to-evidence map → the backbone this skill enforces.
- §13–§14 Figures and tables plan.
- §15 Related work synthesis.
- §16 Discussion plan.
- §17 Limitations and future work.
- §18 Reproducibility plan.
- §19 Manuscript structure plan → the authoritative section list for this paper.
- §20 Abstract blueprint.
- §21 Title and framing options → selects `PAPER_TYPE`.
- §22 Citation and evidence bank.
- §23 Writing instructions for downstream agent → style directives.
- §24 Open issues.
- §25 Readiness assessment → selects `DRAFT_MODE`.
- §26 Executive summary.

Log missing sections of the plan in `COVERAGE_GAPS.md`; do not abort.

### Phase 2 — Determine `DRAFT_MODE`

Decision rule (apply top-down, first match wins):

1. **`full`** — §25 says "Ready for Full Draft: Yes", §12 maps every core claim to existing evidence, §10 has no experiment marked Missing that feeds a core claim, §13 figures are Ready, and §5 contributions are specific.
2. **`partial`** — ≥60% of the core claims in §12 are supported and figures/tables for the Methods + ≥1 Results subsection exist, but some Results/Discussion content is unsupported.
3. **`skeleton`** — core experiments incomplete, claim-to-evidence map mostly empty, or readiness marked "No". Produce headings + targeted placeholders + a detailed `COVERAGE_GAPS.md`.

Record the chosen mode, its justification, and the specific signals that triggered it in `DRAFT_README.md`.

### Phase 3 — Consult referenced project files

For each plan section that will be drafted, pull ground truth from the referenced files before writing. Minimum checks:

- **Introduction / Related Work** → `output/LIT_REVIEW_REPORT.md` (Synthesis and Gap Analysis sections), plan §15 and §22.
- **Data / Study Area** → plan §7–§8, `data/DATA_MANIFEST.md` if present.
- **Methods** → plan §9, `output/EXPERIMENT_PLAN.md`, `skills/knowledge/spatial-methods.md`.
- **Experiments / Results** → `output/EXPERIMENT_LOG.md`, `memory/APPROVED_CLAIMS.md`, `output/spatial-analysis/` reports, `output/FINDINGS.md`.
- **Figures / Tables** → `output/figures/FIGURE_MANIFEST.md`, `output/figures/FIGURE_CAPTIONS.md`. Never reference a figure ID that is not in the manifest.
- **Discussion / Limitations** → plan §16–§17, `AUTO_REVIEW.md`.

If a referenced file is missing, record it in `COVERAGE_GAPS.md` and either (a) soften the relevant claims, (b) insert a marked placeholder, or (c) drop the sub-claim. Do not guess.

### Phase 4 — Select section structure

The default GIScience / remote sensing structure is:

1. Title
2. Abstract + Keywords
3. Introduction
4. Related Work
5. Study Area / Data *(merged with Methods for method-heavy papers)*
6. Methodology
7. Experimental Design
8. Results
9. Discussion
10. Limitations
11. Conclusion
12. Declarations (data / code availability, ethics) when relevant

Adapt by `PAPER_TYPE`:

- **Methodological innovation** — expand Methodology; Related Work clusters around algorithmic lines; add an Ablation subsection in Results.
- **System / agent paper** — add "System Architecture" section after Methodology; Methods becomes workflow + module decomposition; include a component-ablation subsection; Discussion covers design rationale.
- **Benchmark / evaluation** — combine Data + Benchmark Design; expand Experimental Design; Results organized by evaluation axis.
- **Applied case study** — expand Study Area; Discussion emphasizes practical / policy implications.
- **Conceptual / framework** — Related Work is load-bearing; Methodology becomes a formalization / framework section; Results may be illustrative rather than empirical.
- **Multimodal GeoAI** — add "Modalities and Alignment" subsection; explicit discussion of cross-modal failure modes in Limitations.
- **Remote sensing analysis** — Data section expands with sensor / preprocessing detail; Results lead with quantitative tables then spatial maps.

Record the chosen outline (section list + subsections + target word counts) in `DRAFT_README.md` before writing prose.

### Phase 5 — Draft section by section

For each section, follow the section-specific guidance below. Write one section at a time, save to `sections/NN_<name>.md`, and update `CLAIM_SUPPORT_MAP.md` and `COVERAGE_GAPS.md` as you go. Use terminology fixed at first use; never drift.

After all sections are drafted, assemble `MANUSCRIPT_DRAFT.md` by concatenating the section files in order, plus a title block and author placeholder.

### Phase 6 — Consistency and support pass

Run these checks (mechanically, not by feel):

- **Terminology table** — grep the draft for the canonical names (model, dataset, system, metric). Flag variants.
- **Figure / table references** — every `Fig. N` / `Table N` mention must match `FIGURE_MANIFEST.md`. No orphans, no phantoms.
- **Claim-support closure** — every numbered contribution in Introduction must reappear in Results and Conclusion with consistent phrasing.
- **Citation coverage** — every empirical claim about prior work cites a paper present in the synthesis or paper cache; every "first," "novel," "state-of-the-art" is either cut, softened, or directly supported.
- **Limitation honesty** — every limitation listed in plan §17 appears in the Limitations section.
- **Responsible use** — for GeoAI / RS papers, Discussion or Limitations touches fairness, privacy, interpretability, or reproducibility as §16 of the plan dictates.

Record failures in `REVISION_NOTES.md`.

### Phase 7 — Optional cross-review with `REVIEWER_MODEL`

When AUTO_PROCEED permits and the draft is `full` or `partial`, send each section (or the full draft) to `gpt-5.4` via Codex MCP:

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are reviewing a draft Markdown manuscript section for a [TARGET_VENUE] submission.
    Paper type: [PAPER_TYPE].
    Section: [name].
    Plan extract (claim-evidence map for this section): [paste relevant rows of §12].

    Score 1–10 on: (1) claim-evidence alignment, (2) journal-appropriate rigor and tone,
    (3) GIScience / GeoAI positioning, (4) specificity vs. filler, (5) terminology and figure/table consistency.
    For each weakness, give the minimum edit. No rewrites.
```

If Codex is unavailable, skip — do not fall back to self-scoring.

### Phase 8 — Final artifacts and handoff

Emit, in order:

1. `sections/*.md` — all section drafts.
2. `MANUSCRIPT_DRAFT.md` — assembled manuscript.
3. `ABSTRACT_DRAFT.md` — stand-alone abstract.
4. `CLAIM_SUPPORT_MAP.md` — final claim-evidence table.
5. `COVERAGE_GAPS.md` — missing content, unsupported claims, phantom figures.
6. `CITATION_GAPS.md` — claims needing citations.
7. `SECTION_NOTES.md` — per-section scope / softening notes.
8. `REVISION_NOTES.md` — prioritized next-pass actions.
9. `DRAFT_README.md` — mode, venue, readiness, word counts, deliverable index.

Append a one-line entry to `output/FINDINGS.md`:

```
YYYY-MM-DD paper-draft  mode=<full|partial|skeleton>  venue=<...>  words=<N>  gaps=<K>  next=<...>
```

---

## Section-specific drafting guidance

### Title
Prefer the strongest option from plan §21. Keep ≤ 18 words, specific, noun-phrase style, include the geographic / methodological / system descriptor that locates the paper. Avoid "Towards," "Revolutionizing," "A Novel."

### Abstract (150–250 words)
Follow the §20 blueprint: background → gap → method / system → data / case study → main findings (with at least one specific number from `APPROVED_CLAIMS.md`) → significance. One paragraph. No citations. No figure references.

### Keywords
5–7 terms. Mix one domain term (e.g., *urban flood risk*), one method term (e.g., *graph neural network*), one GIScience framing term (e.g., *spatial data science*), and one data / modality term. Align with the target journal's indexing.

### 1. Introduction (≈ 800–1200 words)
Six-paragraph default, adapt as needed:
1. Broad scientific or practical problem; why it matters now (cite 2–3 authoritative sources from plan §22 Introduction list).
2. GIScience / GeoAI / remote sensing framing of the problem; quantify scale or significance where the synthesis supports it.
3. Current approaches, grouped into 2–3 threads; name the threads.
4. The specific gap (from plan §4), with why existing methods are insufficient.
5. The proposed work: one sentence of method + one of data + one of evaluation. Followed by an **explicit numbered contribution list** mirroring §5. Each contribution must be a claim that the Results section actually supports.
6. Manuscript roadmap (optional for short papers; expected by IJGIS / ISPRS).

Do not promise experiments or results that are not in `APPROVED_CLAIMS.md`.

### 2. Related Work (≈ 1000–1600 words)
Cluster-first, paper-second. Use the §15 clusters as subsections. Within each cluster: synthesize the *thread*, name 3–8 representative studies, then state what the cluster does well and where it falls short relative to the gap. Close the section with a one-paragraph differentiation that names the nearest competing approach(es) from plan §5 and states the specific dimension of difference (problem formulation / data regime / spatial reasoning / scale / evaluation).

Avoid: literature dumping, one sentence per paper, listing surveys without engagement.

### 3. Study Area / Data (≈ 500–1000 words; expand for applied case studies)
For each dataset in plan §8: name, provider, spatial coverage, temporal coverage, resolution, variables used, preprocessing, licensing. For spatial studies: state CRS, spatial unit of analysis, area, and any boundary or inclusion rule. Flag data-quality caveats honestly — missingness, class imbalance, temporal mismatch, geographic bias. End with a paragraph on ethics / privacy / responsible use if §16 of the plan flags it.

### 4. Methodology (≈ 1200–2000 words)
Spine from plan §9. Cover, as applicable:
- Problem formulation (task, input, output, unit of analysis).
- Study-specific preprocessing and feature construction.
- The proposed method / model / framework, with equations or algorithmic steps where the plan provides them.
- For system / agent papers: architecture diagram reference, module inventory, orchestration logic, information flow across artifacts, skill decomposition, harness-level constraints.
- For spatial methods: spatial unit, neighborhood / adjacency definition, handling of spatial dependency and autocorrelation, scale / MAUP considerations, CRS handling, uncertainty propagation.
- Baselines and why each is included.
- Implementation notes that matter for reproducibility.

Be specific enough that a reader could re-implement the *shape* of the method. Do not include runtime numbers, loss curves, or scores here — those belong in Results.

### 5. Experimental Design (≈ 400–800 words; can be a subsection of Methodology for short papers)
Train / val / test protocol, spatial cross-validation if used, evaluation metrics with precise definitions, statistical tests, ablation axes, sensitivity / robustness axes, compute environment. State the *decision rules* (what counts as success) when plan §10 supplies them.

### 6. Results (≈ 1000–2000 words)
Lead with the headline result from plan §11 §5 + `APPROVED_CLAIMS.md` — the single most important finding, stated concretely. Then organize by experiment or claim, not by figure. Integrate figures and tables by referencing their purpose, not by paraphrasing their contents. For each result: observation → the metric / number → what experiment produced it → a measured interpretation (one sentence). Separate observation from overinterpretation. Report mixed or negative findings when they exist.

Only reference figures listed in `FIGURE_MANIFEST.md`. Only cite numbers present in `APPROVED_CLAIMS.md` or `EXPERIMENT_LOG.md`. When a planned result is missing, insert a clearly marked placeholder:

```
> [PLACEHOLDER — Result R3 depends on EXP-4 (status: in progress). Expected metric: macro-F1
> on the holdout region. Replace with a specific value once EXP-4 completes.]
```

### 7. Discussion (≈ 800–1400 words)
Interpret, do not repeat. Structure:
1. What the findings mean mechanistically or conceptually.
2. How the findings connect back to the gap stated in Introduction (close the loop).
3. GIScience / GeoAI implications — what changes for the field if these findings hold.
4. Practical / operational implications where the paper type warrants.
5. Responsible-use considerations (fairness, geoprivacy, interpretability, reproducibility, representativeness) proportional to the §16 plan.
6. Generalizability — name the conditions under which the claims should transfer and the conditions under which they should not.

### 8. Limitations (≈ 300–600 words)
Specific, not generic. Mirror plan §17 one-to-one. For each limitation: what it is, why it matters for the claims, and how a reader should qualify interpretation. No "future work will solve everything" framing.

### 9. Conclusion (≈ 300–500 words)
Restate the contributions as outcomes (not promises), in the same numbering used in the Introduction. Close with the broader significance. Add 2–4 concrete future-work directions grounded in the limitations.

### Declarations
Data availability, code availability, ethics statement, conflict of interest placeholder, acknowledgement placeholder. Pull from plan §18.

---

## Decision rules

### When evidence is incomplete
- Claim is directly supported by `APPROVED_CLAIMS.md` → state precisely, with the metric.
- Claim is implied by experiment logs but not yet approved → state cautiously ("we observed"), and add to `CITATION_GAPS.md` / `REVISION_NOTES.md`.
- Claim is planned but not yet run → insert a `[PLACEHOLDER — ...]` block and list in `COVERAGE_GAPS.md`. Do not write a fabricated number, even as a "stub."
- Claim is speculative → move to Discussion with hedged language ("may suggest," "is consistent with"), never to Results or Abstract.

### When a figure is planned but missing
- If the figure appears in `FIGURE_MANIFEST.md` as `Status: Ready` → reference it.
- If `Status: Needs revision` → reference it with a trailing `[FIGURE PENDING REVISION]` tag.
- If the figure is not in the manifest → **do not mention it**. Record in `COVERAGE_GAPS.md`.

### When a citation is needed but absent
- Check `memory/paper-cache/` and the Synthesis section of `output/LIT_REVIEW_REPORT.md`. If present, cite.
- If absent, write the sentence with `[CITE: <topic>]` and record in `CITATION_GAPS.md`. Never fabricate a citation key.

### When the plan conflicts with an evidence file
Evidence wins. Soften the claim, update `SECTION_NOTES.md` with the conflict, and flag for the next revision pass.

### When the paper type is ambiguous
Default to the framing with the strongest evidence: if the experiments are empirical and the contribution is a method, draft as *methodological innovation*; if the contribution is an orchestration / harness / agent, draft as *system paper*. Record the decision in `DRAFT_README.md`.

### Mode selection at section granularity
Individual sections can be drafted at a different fidelity than the manuscript as a whole. E.g., a `partial` manuscript can still have a `full` Methods section if `EXPERIMENT_PLAN.md` is complete. Record per-section fidelity in `SECTION_NOTES.md`.

---

## Style guidance

### Journal-appropriate prose (IJGIS / ISPRS / RSE / TGIS)
- Formal, scholarly, third-person. First-person plural ("we") is acceptable and expected in Methods and Discussion.
- Precise vocabulary. Prefer *heterogeneous land-cover patches* over *diverse landscapes*.
- Paragraphs open with a topic sentence that states a claim, not a transition.
- One idea per paragraph; each paragraph ≤ 180 words except in Methods.
- Vary sentence length; never stack three long sentences in a row.
- Define every abbreviation at first use. Fix terminology at first use and never drift.
- Use present tense for established knowledge, past tense for what you did in the study.
- Figures and tables are referenced *by purpose*, e.g., "the confusion matrix in Fig. 3 shows..." — never "as can be seen in Fig. 3."

### GIScience / GeoAI / remote sensing expectations
- Name the spatial unit of analysis explicitly.
- State the CRS when it matters for the claim.
- Distinguish global from local statistics; report Moran's I (or equivalent) when spatial autocorrelation is relevant.
- For remote sensing: name the sensor, band combination, and spatial / temporal resolution.
- For GeoAI: distinguish model family from training regime from evaluation protocol.
- For system / agent papers: distinguish engineering novelty, workflow novelty, and scientific contribution — do not conflate.

### Contribution framing
- State contributions as outcomes, not promises.
- Distinguish conceptual novelty from engineering novelty; do not hide one behind the other.
- Avoid "first," "state-of-the-art," "outperforms all existing methods" unless `APPROVED_CLAIMS.md` directly supports it on the named benchmark.
- Prefer "to our knowledge, this is the first evaluation of X on Y" over "the first X."

---

## Guardrails (non-negotiable)

Do **not**:
- Fabricate results, metrics, sample sizes, effect sizes, or confidence intervals.
- Invent citation keys, authors, years, or venues. Use `[CITE: ...]` placeholders instead.
- Reference figures or tables that are not in `FIGURE_MANIFEST.md`.
- Assert a novelty claim unsupported by the differentiation table in plan §5.
- Hide missing experiments behind vague language. Mark them.
- Downgrade or remove limitations listed in plan §17.
- Use promotional / startup / hype language ("revolutionary," "game-changing," "unlock," "leverage the power of").
- Self-score the draft. Scoring is handled by `auto-review-loop` / `paper-review-loop`.
- Overwrite accepted sections listed in `memory/MEMORY.md` without the user's explicit instruction.

Do:
- Soften claims under pressure from evidence.
- Prefer one strong paragraph to three weak ones.
- Cut before padding.

---

## Deliverable conventions

Folder layout:

```
output/manuscript/
├── DRAFT_README.md
├── MANUSCRIPT_DRAFT.md
├── ABSTRACT_DRAFT.md
├── CLAIM_SUPPORT_MAP.md
├── COVERAGE_GAPS.md
├── CITATION_GAPS.md
├── SECTION_NOTES.md
├── REVISION_NOTES.md
└── sections/
    ├── 00_title.md
    ├── 01_abstract.md
    ├── 02_introduction.md
    ├── 03_related_work.md
    ├── 04_data.md            # or 04_study_area.md
    ├── 05_methodology.md
    ├── 06_experimental_design.md
    ├── 07_results.md
    ├── 08_discussion.md
    ├── 09_limitations.md
    ├── 10_conclusion.md
    └── 11_declarations.md
```

Each section file begins with a 3-line YAML front matter:

```yaml
---
section: introduction
mode: full            # full | partial | skeleton
word_target: 1000
---
```

Followed by a single `# N. <Section Name>` heading and the prose.

`CLAIM_SUPPORT_MAP.md` uses one row per claim (see `templates/CLAIM_SUPPORT_CHECKLIST.md`).

`COVERAGE_GAPS.md` uses one row per gap, categorized as `missing-experiment`, `missing-figure`, `missing-citation`, `weak-claim`, or `plan-evidence-conflict`.

---

## Supporting templates

- `templates/MANUSCRIPT_SECTION_TEMPLATE.md` — per-section scaffold with front matter + structure prompts.
- `templates/CLAIM_SUPPORT_CHECKLIST.md` — row-per-claim table to populate `CLAIM_SUPPORT_MAP.md`.
- `templates/DRAFT_READINESS_CHECKLIST.md` — the Phase 2 readiness signals, in checkbox form.
- `templates/SECTION_EVIDENCE_CHECKLIST.md` — minimum evidence each section must cite before it is considered drafted.
- `templates/OUTPUT_CONVENTIONS.md` — folder layout, file naming, front-matter rules.

Load templates on demand; do not paste full template contents into the draft.

---

## Key Rules (summary)

- **Large file handling**: If `Write` fails on size, retry with chunked `Bash` (`cat << 'EOF' > file`). Do not ask the user.
- **Never fabricate** results, metrics, figures, or citations.
- **Never reference a missing figure**; use the manifest.
- **Never silently drop a limitation** from plan §17.
- **Always emit `CLAIM_SUPPORT_MAP.md` and `COVERAGE_GAPS.md`** — they are how downstream skills and human reviewers know what the draft actually supports.
- **Mode over polish**: a well-marked `partial` draft is more valuable than a prettified `full` draft with phantom evidence.
- **Terminology is frozen at first use** across all sections.
- **Do not self-score**; that is the reviewer skill's job.
- **Respect `memory/MEMORY.md` and `REVIEW_STATE.json`** — do not overwrite accepted sections.

---

## Composing with other workflows

```
/paper-plan "NARRATIVE_REPORT.md"          → output/PAPER_PLAN.md
/paper-figure-generate all                  → output/figures/
/paper-draft all                            ← you are here  → output/manuscript/
/paper-write "output/manuscript/"           → output/paper/ (LaTeX)
/paper-compile "output/paper/"              → output/paper/main.pdf
/paper-review-loop "output/paper/"          → polished final PDF
```

Or invoked directly via `paper-writing-pipeline` Phase 3.

---

## Acknowledgements

Structure informed by `paper-plan` (claim-evidence backbone), `paper-figure-generate` (two-pathway artifact discipline and manifest-driven referencing), and the PAPER_PLAN template in `templates/PAPER_PLAN_TEMPLATE.md`. Writing-quality overlay adapted from Orchestra Research's paper-writing guidance and the shared references in `skills/shared-references/`.
