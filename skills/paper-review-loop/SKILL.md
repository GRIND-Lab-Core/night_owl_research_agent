---
name: paper-review-loop
description: Reviews the manuscript produced by `paper-draft` (in `output/manuscript/`) as a demanding IJGIS / ISPRS JPRS reviewer-editor, cross-checks it against `output/PAPER_PLAN.md` and its evidence artifacts, then revises it into a stronger draft. Produces a reviewed manuscript, a revised manuscript, a structured review report, a prioritized issue log, a revision log, claim-risk notes, journal-fit notes, and next-loop priorities. Supports full, section-scoped, and mode-scoped review (structural / argument / novelty / methods / results-discussion / journal-fit / language / integrated). Safe on partial or skeletal drafts. Never fabricates results, citations, or figures.
argument-hint: [section-or-"all"-or-mode-or-manuscript-path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch, mcp__codex__codex, mcp__codex__codex-reply
---

# Skill: paper-review-loop

You critically review the manuscript draft in **`output/manuscript/`** — produced by `paper-draft` from **`output/PAPER_PLAN.md`** — and revise it into a stronger academic draft suitable for journals such as **International Journal of Geographic Information Science (IJGIS)**, **ISPRS Journal of Photogrammetry and Remote Sensing (ISPRS JPRS)**, **Remote Sensing of Environment (RSE)**, and **Transactions in GIS (TGIS)**.

Scope argument: **$ARGUMENTS**

This skill is the review-and-revise counterpart to `paper-draft`. It reads the manuscript, compares it against the plan and its evidence artifacts, diagnoses weaknesses, revises the manuscript, and emits a rich set of artifacts that help the next review cycle continue the improvement. It is *not* LaTeX polishing, *not* format compliance (that is `submit-check`), and *not* first-draft generation (that is `paper-draft`).

Supported manuscript types (mirrored from `paper-draft`):
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

- **PLAN_PATH = `output/PAPER_PLAN.md`** — manuscript intent and evidence blueprint.
- **MS_DIR = `output/manuscript/`** — drafts live here.
- **MAIN_DRAFT = `output/manuscript/MANUSCRIPT_DRAFT.md`** — current manuscript.
- **SECTIONS_DIR = `output/manuscript/sections/`** — per-section drafts.
- **TARGET_VENUE** — read from `PAPER_PLAN.md` §0/§2, else `research_contract.md`, else default `IJGIS`.
- **PAPER_TYPE** — read from `PAPER_PLAN.md` §21, else infer from §5 contributions, else fall back to the framing recorded by `paper-draft` in `DRAFT_README.md`.
- **APPROVED_CLAIMS = `memory/APPROVED_CLAIMS.md`** — the only source of verified numeric/empirical claims.
- **LIT_REVIEW_REPORT = `output/LIT_REVIEW_REPORT.md`** — consolidated literature review (Findings, Synthesis, Gap Analysis).
- **FIGURE_MANIFEST = `output/figures/FIGURE_MANIFEST.md`** — figures that actually exist.
- **REVIEWER_MODEL = `gpt-5.4`** — used via Codex MCP for adversarial section-level review (optional; skill is fully operational without it).
- **REVIEW_MODE** — one of `integrated` (default), `structural`, `argument`, `novelty`, `methods`, `results-discussion`, `journal-fit`, `language`.
- **REVISION_MODE** — one of `full`, `partial`, `conservative`. Chosen in Phase 3; may be overridden inline.
- **MAX_ROUNDS = 3** — cap per invocation to avoid unbounded work. Quality is set by artifact content, not round count.
- **LOOP_STATE = `output/manuscript/REVIEW_LOOP_STATE.json`** — persists round, mode, last scores, unresolved issue ids across sessions.
- **HUMAN_CHECKPOINT** — read from `CLAUDE.md` Control Flags, default `true`. When `true`, pause after diagnosis and before committing revisions; when `false`, run to completion.

Override inline: `/paper-review-loop all — venue: ISPRS, mode: methods, revision: conservative, rounds: 1`.

Argument forms:
- `all` — review + revise the whole manuscript.
- `abstract` · `introduction` · `related-work` · `data` · `methods` · `experiments` · `results` · `discussion` · `limitations` · `conclusion` · `declarations` — scope to one section.
- A `MODE:` prefix — e.g. `mode:novelty`, `mode:journal-fit`. Combines with a section scope.
- A path to a manuscript file — review that file instead of `MAIN_DRAFT`.

---

## Core Philosophy

1. **Review is a means, revision is the deliverable.** Critique that does not land as an improved draft is half the job. Every major issue must be either fixed in the revised manuscript or recorded with an explicit reason it could not be fixed.
2. **Evidence binds claims.** The manuscript may only assert what is supported by `APPROVED_CLAIMS.md`, entries in `output/EXPERIMENT_LOG.md`, rows in `PAPER_PLAN.md` §12, or the paper-cache synthesis. Anything else is softened, flagged, or cut.
3. **Plan is intent, evidence is truth.** Discrepancies between the manuscript and `PAPER_PLAN.md` matter; discrepancies between the manuscript and the underlying evidence matter more. When they conflict, evidence wins.
4. **Journal voice is non-negotiable.** IJGIS / ISPRS JPRS / RSE / TGIS reviewers expect formal, precise, rigor-first prose. No hype, no startup framing, no vague "leverage the power of."
5. **Diagnose, prioritize, revise.** Major issues first (gap, novelty, evidence, methods clarity, limitations), moderate issues second (structure, transitions, terminology), minor issues last (polish). Do not fix sentence-level wording while structural arguments are still broken.
6. **Generator-evaluator separation respected in reverse.** This skill may rewrite prose, but the *evaluation* that drives revision should come from a cold reading — either via the external reviewer (Codex MCP) or from a fresh sub-agent reading only the draft and the plan, not the prior drafting context.
7. **Readiness-aware behavior.** On skeletal drafts, do not pretend the manuscript is close to submission. Produce a revision plan and a conservative refinement of supported sections instead.
8. **Loops are monotonic.** Each round should strictly improve the manuscript on at least one named axis, and never silently reintroduce a previously-resolved issue.

---

## Inputs

### Primary
- **`output/manuscript/MANUSCRIPT_DRAFT.md`** — the integrated manuscript from `paper-draft`.
- **`output/manuscript/sections/*.md`** — per-section drafts with front matter (`section`, `mode`, `word_target`).
- **`output/PAPER_PLAN.md`** — manuscript intent and claim-to-evidence map (§12 especially).

### Companion artifacts from `paper-draft` (read on demand)
- `output/manuscript/DRAFT_README.md` — mode, venue, paper type, readiness, per-section fidelity.
- `output/manuscript/CLAIM_SUPPORT_MAP.md` — the claim-to-evidence rows this skill must re-verify.
- `output/manuscript/COVERAGE_GAPS.md` — missing experiments, figures, citations flagged at draft time.
- `output/manuscript/CITATION_GAPS.md` — claims missing citations.
- `output/manuscript/SECTION_NOTES.md` — per-section scope decisions and softened claims.
- `output/manuscript/REVISION_NOTES.md` — unfinished items from the drafting pass.
- `output/manuscript/ABSTRACT_DRAFT.md` — stand-alone abstract.

### Evidence and context (read as needed)
- `research_contract.md`, `program.md` — active idea and constraints.
- `memory/APPROVED_CLAIMS.md`, `output/LIT_REVIEW_REPORT.md` (Gap Analysis + Synthesis sections).
- `memory/paper-cache/*.json` — bibliographic + finding records.
- `output/EXPERIMENT_LOG.md`, `output/EXPERIMENT_PLAN.md`, `output/PROJ_NOTES.md`.
- `output/spatial-analysis/` — ESDA and diagnostic reports.
- `output/figures/FIGURE_MANIFEST.md`, `output/figures/FIGURE_CAPTIONS.md`.
- `output/AUTO_REVIEW.md` — prior adversarial-review scores and pending fixes.
- `templates/giscience/`, `templates/remote_sensing/`, `templates/geoscience/` — venue guides.
- `skills/knowledge/academic-writing.md`, `skills/knowledge/apa-citations.md`, `skills/knowledge/spatial-methods.md`, `skills/knowledge/geoai-domain.md`.
- `skills/shared-references/writing-principles.md`, `skills/shared-references/venue-checklists.md` — load only when acting on Abstract / Introduction / Related Work / journal-fit.

### Prior-loop state
- `output/manuscript/REVIEW_LOOP_STATE.json` — round counter, unresolved issue ids, prior scores, timestamp.
- `output/manuscript/REVIEW_REPORT.md`, `MAJOR_ISSUES.md`, `MINOR_ISSUES.md`, `REVISION_LOG.md`, `NEXT_LOOP_PRIORITIES.md` — if present, treated as the incoming queue for this round.

---

## Outputs

All outputs live under `output/manuscript/`. Filenames are stable across rounds (the skill overwrites); rounds are distinguished by entries *inside* the files, not by filename suffixes.

| File | Purpose |
|---|---|
| `MANUSCRIPT_REVIEWED.md` | The input draft with inline review annotations (`<!-- REVIEW: ... -->` blocks), for traceability. Not a revised draft. |
| `MANUSCRIPT_REVISED.md` | The revised manuscript after this round. Becomes the basis for the next loop. |
| `sections_revised/NN_<name>.md` | Per-section revised drafts, parallel to `sections/`. Used when revising partial or conservative scopes. |
| `REVIEW_REPORT.md` | Structured reviewer-style report: summary, per-section assessment, per-dimension scores, verdict. |
| `MAJOR_ISSUES.md` | Ranked list of major issues with diagnosis, evidence pointer, revision action, resolved-yes/no, and carry-over flag. |
| `MINOR_ISSUES.md` | Ranked list of moderate + minor issues (structure, transitions, wording, terminology). |
| `REVISION_LOG.md` | What changed in `MANUSCRIPT_REVISED.md` this round, keyed to issue ids, with before/after snippets. |
| `SECTION_REVIEW_NOTES.md` | Per-section notes on strengths, weaknesses, and revision decisions. Feeds the next round. |
| `CLAIM_RISK_REPORT.md` | Every claim from `CLAIM_SUPPORT_MAP.md` re-verified against the draft; flags overclaims, softened claims, unsupported claims. |
| `JOURNAL_FIT_NOTES.md` | Alignment against the target venue's expectations (IJGIS / ISPRS JPRS / RSE / TGIS) — framing, rigor, methods reporting, limitations, declarations. |
| `NEXT_LOOP_PRIORITIES.md` | What the next round should focus on; carries forward unresolved majors and newly discovered moderates. |
| `REVIEW_LOOP_STATE.json` | Round counter, prior scores, unresolved issue ids, mode, timestamp. |

File-naming conventions are inherited from `paper-draft`: two-digit section prefixes, no `_v2` suffixes, prior versions preserved via git not filenames.

---

## Workflow

The skill has eight phases. Phases 1–4 are diagnosis; Phase 5 is the optional human checkpoint; Phases 6–7 are revision and verification; Phase 8 is handoff. On tight scopes (e.g. `mode:language`), phases can be compressed but not skipped.

### Phase 1 — Load state and scope

1. Read `CLAUDE.md` Control Flags. Honour `HUMAN_CHECKPOINT`.
2. If `REVIEW_LOOP_STATE.json` exists with `status: in_progress` and timestamp within 24 hours: resume. Increment round. Read prior `REVIEW_REPORT.md`, `MAJOR_ISSUES.md`, `NEXT_LOOP_PRIORITIES.md` as the incoming queue.
3. If not resuming: initialize round = 1, load scope from `$ARGUMENTS`.
4. Resolve `REVIEW_MODE` and section scope:
   - No mode given → `integrated`.
   - `mode:<x>` given → use that mode; other phases still run but are minimized.
5. Locate the manuscript:
   - If `$ARGUMENTS` is a path → use it.
   - Else use `MAIN_DRAFT`. If absent, emit a stub `REVIEW_REPORT.md` explaining that `paper-draft` must run first, and stop.

### Phase 2 — Read manuscript and its companion artifacts

Read in this order (cheap → expensive):

1. `DRAFT_README.md` — get declared `DRAFT_MODE` (full / partial / skeleton), venue, paper type, readiness signals, and per-section fidelity.
2. `MANUSCRIPT_DRAFT.md` and relevant `sections/*.md`. Determine whether the draft is full, partial, or skeletal regardless of what `DRAFT_README.md` claims (cross-check against actual content length, `[PLACEHOLDER ...]` blocks, and `[CITE: ...]` tags).
3. `CLAIM_SUPPORT_MAP.md` — pull the claim-to-evidence rows; this is the backbone of the claim-risk audit.
4. `COVERAGE_GAPS.md`, `CITATION_GAPS.md`, `SECTION_NOTES.md`, `REVISION_NOTES.md` — known-at-draft-time weaknesses.
5. `ABSTRACT_DRAFT.md` — the stand-alone abstract.

### Phase 3 — Cross-check against `PAPER_PLAN.md`

Open `PAPER_PLAN.md`. For each plan section that drives the draft, answer a specific question and record the answer in `SECTION_REVIEW_NOTES.md`:

| Plan § | Question to answer about the draft |
|---|---|
| §1 Title & one-sentence claim | Does the draft's title and abstract-leading sentence match this framing? If drift, is it justified by evidence? |
| §2 Journal strategy | Does the prose tone match this venue (IJGIS / ISPRS JPRS / RSE / TGIS)? |
| §3–§4 Motivation + gap | Is the gap explicit in the Introduction? Is prior work's insufficiency named? |
| §5 Novelty + contributions | Does the Introduction list contributions as numbered outcomes? Do Results and Conclusion return to them with the same numbering? |
| §6 RQs / hypotheses | Are they stated? Are they answered in Results + Discussion? |
| §7–§8 Scope + data | Are data sources, CRS, spatial unit, coverage, and caveats stated? |
| §9 Methodology | Are the algorithmic / workflow steps specific enough for a reader to grasp the *shape* of the method? |
| §10 Experiments | Are train/val/test, metrics, baselines, and ablations defined with precision? |
| §11 Results | Does the lead result match §5's headline claim? Are results ordered by claim, not by figure? |
| §12 Claim-to-evidence map | For every row, does the draft state the claim at the right strength? |
| §13–§14 Figures / tables | Is every mentioned figure in `FIGURE_MANIFEST.md`? Are figures referenced by *purpose*? |
| §15 Related work synthesis | Is related work cluster-organized or a laundry list? |
| §16 Discussion | Does Discussion close the loop to the gap, name GIScience / GeoAI / RS implications, address responsible-use where relevant? |
| §17 Limitations | Are all planned limitations present? None silently dropped? |
| §18 Reproducibility | Data / code availability statements present? |
| §20 Abstract blueprint | Abstract hits background → gap → method → data → findings → significance? |
| §21 Title/framing + paper type | Does the manuscript genuinely behave like that paper type (e.g. system paper actually describes architecture, modules, information flow)? |
| §25 Readiness | Does the draft acknowledge readiness honestly, or does it pretend it is stronger than the evidence? |

Record each answer with a severity tag: `ok` · `moderate` · `major` · `placeholder-expected`.

### Phase 4 — Re-verify evidence (Claim Risk Audit)

Open `CLAIM_SUPPORT_MAP.md` and walk every row. For each:

1. Find the claim in the draft (grep by claim id or phrasing).
2. Compare the strength of the claim's wording to the evidence confidence:
   - **High-confidence evidence + cautious wording** → upgrade to precise ("we observed" → "on the [dataset] holdout, [metric] = [value]").
   - **Medium-confidence evidence + strong wording** → soften ("outperforms" → "is competitive with," "consistent with").
   - **Low-confidence evidence in Abstract / Results headline** → move the claim to Discussion with hedged language, or cut.
   - **No evidence (`—`)** → the claim must be a marked placeholder or cut. If it is asserted as fact in the current draft, flag as `CRITICAL-overclaim`.
3. Check for claims in the draft that are *not* in `CLAIM_SUPPORT_MAP.md` — these are almost always unsupported and must be added to the map with evidence located, or softened / cut.
4. Check for planned claims that are missing from the draft — these may be silently dropped evidence; restore if the plan intended them and evidence supports them.

Emit `CLAIM_RISK_REPORT.md` with one row per claim, columns: `ClaimID · Section · Wording · Evidence · Confidence · Risk · Revision Action`.

Never invent evidence. Never invent a citation key. Never invent a metric number. When evidence is genuinely missing, the revision is to soften or remove, not to fabricate.

### Phase 5 — Diagnose and classify issues

Run through the **review checklist** (see `templates/REVIEW_CHECKLIST.md`) using the `REVIEW_MODE`:

- **structural** — section presence, order, word balance, paragraph topic sentences, section transitions, heading hierarchy, figure/table placement.
- **argument** — gap clarity, contribution clarity, claim-to-evidence consistency, Introduction → Results → Conclusion coherence, lead results discipline.
- **novelty** — precision of novelty statement, differentiation from nearest prior work, avoidance of "first / state-of-the-art" unless `APPROVED_CLAIMS.md` supports it.
- **methods** — problem formulation, input/output, unit of analysis, spatial unit, CRS, preprocessing, model/framework specificity, baselines, evaluation metrics, reproducibility detail, system architecture for system papers.
- **results-discussion** — ordering by claim, interpretation discipline, mixed/negative findings honesty, GIScience / GeoAI implications, responsible-use discussion, generalizability conditions, limitations completeness.
- **journal-fit** — venue tone, rigor conventions, expected section presence, declarations (data / code availability), ethics statements.
- **language** — paragraph topic sentences, sentence-length variation, terminology drift, figure/table reference style ("shows" vs. "as can be seen in"), abbreviation management.
- **integrated** — all of the above, prioritized.

Classify each finding into:

**Major**
- weak or missing gap articulation
- unclear novelty or novelty unsupported by differentiation
- claims whose strength exceeds evidence ("overclaim")
- insufficient methods detail to grasp the method
- weak experiment description (unclear protocol, unclear metrics, unclear baselines)
- results interpreted more strongly than the data support
- poor connection to GIScience / GeoAI / remote sensing literature
- missing or defanged limitations
- mismatch with target journal expectations (tone, structure, declarations)
- structural problems (section ordering, missing sections, dangling contributions)

**Moderate**
- repetitive writing, redundant paragraphs across sections
- vague section transitions
- inconsistent terminology (model / dataset / system / metric names drift)
- weak paragraph topic sentences
- figure/table references that do not integrate with the narrative
- incomplete contextualization of findings against prior work

**Minor**
- awkward wording, local clarity problems
- caption / title mismatches
- redundant phrases and filler
- sentence-level polish needs

Write `MAJOR_ISSUES.md` and `MINOR_ISSUES.md` using the schema in `templates/ISSUE_RUBRIC.md`. Each issue has: `id · severity · section · description · evidence · proposed revision · resolved-in-this-round (yes/no) · carry-over (yes/no)`.

### Phase 5.5 — Optional external reviewer pass (`REVIEWER_MODEL`)

If Codex MCP is available and `HUMAN_CHECKPOINT` does not block it, send the revised-candidate to `gpt-5.4` for an independent adversarial read. This is the generator-evaluator separation check.

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are reviewing a manuscript draft for [TARGET_VENUE] ([IJGIS | ISPRS JPRS | RSE | TGIS]).
    Paper type: [PAPER_TYPE].
    This is Round [N] of an iterative review loop. Prior unresolved major issues: [...].

    Focus: [REVIEW_MODE].

    Please provide a structured review:
    1. Score 1–10 per dimension: gap clarity, novelty precision, methods rigor, results discipline,
       discussion depth, literature positioning, journal fit, language and flow.
    2. Ranked list of remaining CRITICAL > MAJOR > MODERATE issues, each with a minimum edit.
    3. Claim-risk flags: which sentences in the draft look stronger than the evidence supports?
    4. Verdict: ready / almost / not ready for [TARGET_VENUE].
    5. One paragraph on what is working well — do not just list weaknesses.

    Do not rewrite. Do not fabricate evidence. Be specific to GIScience / GeoAI / remote sensing expectations.

    [Paste MANUSCRIPT_REVIEWED.md content or the scoped section(s).]
    [Paste PAPER_PLAN.md §5, §12, §16, §17, §21 for context.]
```

If round 2+, use `mcp__codex__codex-reply` with the saved `threadId` from `REVIEW_LOOP_STATE.json` so the reviewer has continuity.

If Codex is unavailable, skip — do not fall back to self-scoring. A cold-read sub-agent (`Agent` tool) can substitute.

### Phase 6 — Human checkpoint (if enabled)

Skip if `HUMAN_CHECKPOINT = false`.

Present to the user:
- per-dimension scores (this round vs. prior round if any)
- top 3 major issues with proposed revision summaries
- claim-risk flags count (overclaims, unsupported, placeholder-expected)
- proposed `REVISION_MODE` (full / partial / conservative)

Accept: `go` (apply all revisions) · `custom: <instructions>` · `skip N` (skip issue id N) · `stop` (write artifacts, end loop). Default on no response within the session's interaction budget: `go`.

### Phase 7 — Revise the manuscript

Revision is ordered by severity: Majors → Moderates → Minors. Never polish sentence-level wording before structural arguments are resolved.

Decision rules for the revision:

1. **`REVISION_MODE = full`** — rewrite affected paragraphs/sections end-to-end when structural or argument issues dominate; preserve accepted sections per `memory/MEMORY.md` and `REVIEW_STATE.json`.
2. **`REVISION_MODE = partial`** — rewrite only the sections with major issues; surgically edit moderate issues in others.
3. **`REVISION_MODE = conservative`** — when evidence is incomplete or readiness is low, prefer softening, tightening, and marking placeholders over large rewrites. Do not upgrade claims. Do not invent new content to paper over gaps.

Section-specific revision behavior (see `templates/SECTION_REVIEW_TEMPLATE.md`):

#### Abstract
Rebuild against plan §20 blueprint: background → gap → method / system → data / case study → headline finding (with one specific number from `APPROVED_CLAIMS.md`) → significance. One paragraph. No citations. No figure references. Cap per venue: 250 words (IJGIS, TGIS), 300 words (ISPRS JPRS, RSE).

#### Introduction
Verify the six-paragraph arc: broad problem → GIScience / GeoAI / RS framing → current approaches (named threads) → specific gap → proposed work + numbered contribution list → roadmap. Ensure each contribution is a claim the Results actually supports. Soften "first / novel / state-of-the-art" unless directly supported.

#### Related Work
Enforce cluster-first synthesis. Each cluster: synthesize the thread → name 3–8 representative studies → state what the cluster does well and where it falls short relative to the gap. Close with a differentiation paragraph naming nearest competing approaches and the dimension of difference.

#### Data / Study Area
For each dataset: name, provider, spatial coverage, temporal coverage, resolution, variables used, preprocessing, licensing, CRS, spatial unit of analysis. Flag caveats honestly (missingness, class imbalance, geographic bias). Add responsible-use paragraph if plan §16 flags it.

#### Methods
Ensure problem formulation (task, input, output, unit of analysis), preprocessing, model/framework specificity, baselines and rationale, evaluation metrics with precise definitions, implementation reproducibility notes. For system / agent papers: architecture, module inventory, orchestration logic, artifact flow across skills, harness-level constraints. For spatial methods: neighborhood definition, handling of spatial dependency, MAUP / scale considerations, CRS handling, uncertainty propagation.

#### Experiments
Train / val / test protocol, spatial cross-validation if used, metric definitions, statistical tests, ablation axes, sensitivity / robustness axes, compute environment. State decision rules when plan §10 supplies them.

#### Results
Lead with the headline finding stated concretely. Organize by claim, not by figure. Each result: observation → metric / number → source experiment → one-sentence measured interpretation. Separate observation from interpretation. Report mixed / negative findings. Reference only figures in `FIGURE_MANIFEST.md`. Only cite numbers in `APPROVED_CLAIMS.md` / `EXPERIMENT_LOG.md`. Replace overclaims with the strongest defensible wording.

#### Discussion
Interpret, don't repeat. Structure: (1) what the findings mean mechanistically or conceptually, (2) how they answer the gap, (3) GIScience / GeoAI / RS implications, (4) practical / operational implications when applicable, (5) responsible-use (fairness, geoprivacy, interpretability, reproducibility, representativeness) proportional to plan §16, (6) generalizability — conditions of transfer and non-transfer.

#### Limitations
Specific, not generic. Mirror plan §17 one-to-one. No "future work will solve everything" framing.

#### Conclusion
Restate contributions as outcomes in the same numbering used in Introduction. Close with broader significance. 2–4 concrete future-work directions grounded in limitations.

#### Declarations
Data availability, code availability, ethics, conflict of interest, acknowledgement placeholders per plan §18 and the venue's conventions.

Write revised sections to `sections_revised/NN_<name>.md`. Assemble `MANUSCRIPT_REVISED.md` by concatenating in order plus the title block. Do not overwrite `sections/*.md` — `paper-draft` owns those.

Maintain terminology consistency: grep for canonical names (model, dataset, system, metric, geographic terms, abbreviations) and normalize drift in the revised draft. Record renames in `REVISION_LOG.md`.

### Phase 8 — Verify, log, and hand off

Mechanical post-revision checks:

- **Claim closure**: every `CRITICAL-overclaim` in `CLAIM_RISK_REPORT.md` is either softened in `MANUSCRIPT_REVISED.md` or carried over with an explicit reason.
- **Limitation closure**: every plan §17 limitation appears in the revised Limitations section.
- **Figure closure**: every figure mentioned in the revised draft exists in `FIGURE_MANIFEST.md`.
- **Contribution closure**: every numbered contribution in Introduction appears, in the same numbering, in Results and Conclusion.
- **Terminology closure**: grep confirms no mixed casing / spelling for canonical names.
- **Placeholder discipline**: `[PLACEHOLDER ...]` blocks remain only where evidence is genuinely missing; none have been silently deleted.

Write all output artifacts (see **Outputs** table). Update `REVIEW_LOOP_STATE.json`:

```json
{
  "round": 2,
  "review_mode": "integrated",
  "revision_mode": "partial",
  "threadId": "019ce736-...",
  "last_scores": {
    "gap_clarity": 6.5,
    "novelty_precision": 6.0,
    "methods_rigor": 7.0,
    "results_discipline": 6.5,
    "discussion_depth": 6.0,
    "literature_positioning": 6.5,
    "journal_fit": 7.0,
    "language_flow": 7.5
  },
  "unresolved_major_ids": ["M3", "M7"],
  "status": "in_progress",
  "timestamp": "2026-04-14T22:00:00"
}
```

On the final round of this invocation, set `status: completed` *only if* no unresolved majors remain; otherwise leave `in_progress` so the next invocation resumes cleanly.

Append a one-line entry to `output/PROJ_NOTES.md`:

```
YYYY-MM-DD paper-review-loop round=N mode=<...> revision=<...> majors=<open/total> verdict=<ready|almost|not-ready>
```

Append a cumulative entry to `output/AUTO_REVIEW.md` with the per-dimension scores and top 3 majors, respecting the generator-evaluator protocol noted in `CLAUDE.md`.

---

## Decision rules (summary)

- **Full vs. partial vs. conservative revision**: full when structural/argument issues dominate and evidence is mostly in place; partial when only some sections have major issues; conservative when readiness is low or evidence is incomplete.
- **Handling unsupported claims**: soften first; mark as placeholder second; cut third. Never fabricate.
- **When the plan and the draft disagree**: if evidence supports the draft, update `SECTION_REVIEW_NOTES.md` with a rationale and keep the draft's framing; if evidence supports the plan, revise the draft back toward the plan.
- **Paper-type adaptation**: review criteria shift by `PAPER_TYPE` (e.g. benchmark papers are held to stricter evaluation-protocol standards; system papers to stricter architecture + information-flow clarity; applied case studies to study-area specificity and practical implications).
- **Journal adaptation**: IJGIS / TGIS emphasize GIScience theory, spatial framing, and scale/MAUP discipline. ISPRS JPRS / RSE emphasize sensor / resolution / preprocessing rigor and quantitative evaluation. Adjust the review accordingly (see `templates/JOURNAL_FIT_CHECKLIST.md`).
- **Incomplete drafts**: produce `MAJOR_ISSUES.md`, a revised partial draft, a marked-up section-by-section improvement memo in `SECTION_REVIEW_NOTES.md`, and `NEXT_LOOP_PRIORITIES.md`. Do not pretend a skeletal draft is publication-ready.
- **Round budget**: cap at `MAX_ROUNDS = 3` per invocation. Diminishing returns beyond three rounds for writing-quality improvements; continuation requires fresh evidence or a new scope.

---

## Style guidance for the revised prose

- Formal, scholarly, third-person. First-person plural ("we") is acceptable in Methods and Discussion.
- Precise vocabulary. Prefer *heterogeneous land-cover patches* over *diverse landscapes*; *spatial units of analysis* over *areas*; *spatial cross-validation* over *held-out test*.
- Paragraphs open with a topic sentence that states a claim, not a transition.
- One idea per paragraph; ≤ 180 words except in Methods.
- Vary sentence length; do not stack three long sentences.
- Define every abbreviation at first use and fix it. Canonical names are frozen at first use across sections.
- Present tense for established knowledge; past tense for what you did in the study.
- Reference figures by purpose: "the confusion matrix in Fig. 3 shows..." — never "as can be seen in Fig. 3."
- State spatial unit of analysis and CRS when they matter for the claim.
- Distinguish model family from training regime from evaluation protocol.
- For system / agent papers: distinguish engineering novelty, workflow novelty, and scientific contribution — do not conflate.

Contribution framing:
- State contributions as outcomes, not promises.
- Avoid "first," "state-of-the-art," "outperforms all existing methods" unless `APPROVED_CLAIMS.md` directly supports it on the named benchmark.
- Prefer "to our knowledge, this is the first evaluation of X on Y" over "the first X."

---

## Guardrails (non-negotiable)

Do **not**:
- Fabricate results, metrics, sample sizes, effect sizes, or confidence intervals.
- Invent citation keys, authors, years, or venues. Use `[CITE: ...]` placeholders instead.
- Reference figures or tables that are not in `FIGURE_MANIFEST.md`.
- Strengthen a claim beyond what `CLAIM_SUPPORT_MAP.md` + `APPROVED_CLAIMS.md` support.
- Hide missing experiments behind vague language. Mark them.
- Drop a limitation listed in plan §17 without a recorded reason.
- Use promotional / startup / hype language ("revolutionary," "game-changing," "unlock," "leverage the power of," "paradigm shift").
- Flatten the author's intended contribution into something too generic in the name of "clarity."
- Write only sentence-level polish while structural arguments are still broken.
- Self-score the draft without a cold reader. Use Codex MCP or a fresh `Agent`.
- Overwrite accepted sections listed in `memory/MEMORY.md` or `output/REVIEW_STATE.json` without explicit user instruction.
- Overwrite `sections/*.md` — those are owned by `paper-draft`. Write to `sections_revised/*.md`.

Do:
- Soften under pressure from evidence.
- Revise for publishability, not flashiness.
- Prefer one strong paragraph to three weak ones.
- Cut before padding.
- Make the reasoning behind the revision traceable via `REVISION_LOG.md`.

---

## Deliverable conventions

Folder layout after one round:

```
output/manuscript/
├── DRAFT_README.md                 # from paper-draft
├── MANUSCRIPT_DRAFT.md             # from paper-draft (unchanged)
├── MANUSCRIPT_REVIEWED.md          # this skill — with <!-- REVIEW: ... --> annotations
├── MANUSCRIPT_REVISED.md           # this skill — revised draft
├── CLAIM_SUPPORT_MAP.md            # paper-draft
├── CLAIM_RISK_REPORT.md            # this skill
├── COVERAGE_GAPS.md                # paper-draft (this skill may append)
├── CITATION_GAPS.md                # paper-draft (this skill may append)
├── SECTION_NOTES.md                # paper-draft
├── SECTION_REVIEW_NOTES.md         # this skill
├── MAJOR_ISSUES.md                 # this skill
├── MINOR_ISSUES.md                 # this skill
├── REVIEW_REPORT.md                # this skill
├── REVISION_LOG.md                 # this skill
├── JOURNAL_FIT_NOTES.md            # this skill
├── NEXT_LOOP_PRIORITIES.md         # this skill
├── REVIEW_LOOP_STATE.json          # this skill
├── REVISION_NOTES.md               # paper-draft (this skill may append)
├── sections/                       # paper-draft (read-only)
│   ├── 00_title.md
│   ├── 01_abstract.md
│   └── ...
└── sections_revised/               # this skill
    ├── 00_title.md
    ├── 01_abstract.md
    └── ...
```

Each revised section file keeps the same three-line YAML front matter as `paper-draft`, with two added fields:

```yaml
---
section: introduction
mode: full
word_target: 1000
review_round: 2
revision_mode: partial
---
```

`MAJOR_ISSUES.md`, `MINOR_ISSUES.md`, and `CLAIM_RISK_REPORT.md` follow row schemas in `templates/ISSUE_RUBRIC.md` and `templates/CLAIM_RISK_CHECKLIST.md`.

Issue ids are stable across rounds (e.g. `M3` stays `M3` once assigned). Resolution flips `resolved-in-this-round` to `yes` but the row stays in history.

---

## Loop iteration conventions

- **Monotonic improvement**: each round must strictly improve at least one named dimension. Regressions are bugs; investigate before shipping.
- **Stable issue ids**: once `M7` exists, it stays `M7` across rounds; its status and round-resolved columns change, not its id.
- **Carry-over flag**: unresolved majors move to the top of `NEXT_LOOP_PRIORITIES.md`.
- **Round cap**: `MAX_ROUNDS = 3` per invocation. Beyond that, the skill stops and asks whether new evidence has arrived (new experiments, new figures, new approved claims). Without new evidence, further loops produce diminishing returns.
- **Compaction recovery**: if context fills mid-round, write `REVIEW_LOOP_STATE.json` and `REVISION_LOG.md` before compaction; the next session reads them, picks up from the next phase.

---

## Supporting templates

- `templates/REVIEW_CHECKLIST.md` — full review checklist by mode (structural / argument / novelty / methods / results-discussion / journal-fit / language / integrated).
- `templates/SECTION_REVIEW_TEMPLATE.md` — per-section review + revision scaffold.
- `templates/ISSUE_RUBRIC.md` — major / moderate / minor schema, row format, severity criteria.
- `templates/CLAIM_RISK_CHECKLIST.md` — claim-wording-vs-evidence audit, one row per claim.
- `templates/JOURNAL_FIT_CHECKLIST.md` — IJGIS / ISPRS JPRS / RSE / TGIS expectations by section and by paper type.
- `templates/OUTPUT_CONVENTIONS.md` — folder layout, file names, front-matter, round conventions.

Load templates on demand; do not paste their full contents into review outputs.

---

## Composing with other workflows

```
/paper-plan              → output/PAPER_PLAN.md
/paper-figure-generate   → output/figures/
/paper-draft all         → output/manuscript/         (draft + claim map + gap reports)
/paper-review-loop all   ← you are here               (review + revise + next-loop priorities)
/paper-write             → output/paper/ (LaTeX)
/paper-compile           → output/paper/main.pdf
/submit-check            → venue-compliance gate
```

Relationship to sibling skills:
- `paper-draft` — writes the first manuscript; owns `sections/*.md`. This skill never overwrites those.
- `auto-review-loop` — adversarial research-quality review (novelty, rigor, literature, clarity, impact); operates earlier in the pipeline on the research itself, not the manuscript prose. This skill borrows its generator-evaluator discipline.
- `result-to-claim` — the safety gate that populates `memory/APPROVED_CLAIMS.md`. This skill trusts that file absolutely.
- `submit-check` — final venue-compliance gate (word count, declarations, geo-specific reporting). This skill can precede it; it does not replace it.

---

## Key Rules (summary)

- **Review is a means, revision is the deliverable.** Ship `MANUSCRIPT_REVISED.md`, not just a report.
- **Evidence binds claims.** `CLAIM_RISK_REPORT.md` is as important as the revised prose.
- **Terminology is frozen at first use** — the revision normalizes drift, does not introduce new variants.
- **Never reference a missing figure**, never invent a citation, never fabricate a metric.
- **Readiness-aware**: conservative revisions on skeletal drafts; no pretending.
- **Majors before minors** — structure and argument before polish.
- **Generator-evaluator separation**: evaluate with Codex MCP or a fresh `Agent`, not the drafting context.
- **Stable issue ids and monotonic improvement** across rounds.
- **Respect `memory/MEMORY.md` and `output/REVIEW_STATE.json`** — do not overwrite accepted sections.
- **Overwrite to `sections_revised/`**, never `sections/`.
- **Large file handling**: if `Write` fails on size, retry with chunked `Bash` (`cat << 'EOF' > file`) without asking.

---

## Acknowledgements

Structure adapted from `paper-draft` (claim-evidence discipline, readiness-aware modes, output richness), `auto-review-loop` (generator-evaluator separation, per-dimension scoring, round-state persistence, Codex MCP integration), `paper-plan` (section backbone and venue selection), and `submit-check` (venue-compliance sensitivity). GIScience / GeoAI / remote sensing review expectations informed by `skills/knowledge/academic-writing.md`, `skills/knowledge/spatial-methods.md`, `skills/knowledge/geoai-domain.md`, and the shared references in `skills/shared-references/`.
