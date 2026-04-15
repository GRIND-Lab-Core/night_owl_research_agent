# OUTPUT_CONVENTIONS.md — folder layout, file names, round conventions

> Inherited from `paper-draft`; adds review-loop-specific conventions.

---

## Folder layout

```
output/manuscript/
├── DRAFT_README.md                 # paper-draft
├── MANUSCRIPT_DRAFT.md             # paper-draft — unchanged by this skill
├── MANUSCRIPT_REVIEWED.md          # this skill — inline <!-- REVIEW: ... --> annotations
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
├── sections/                       # paper-draft — read-only from this skill
│   ├── 00_title.md
│   ├── 01_abstract.md
│   └── ...
└── sections_revised/               # this skill — mirrors sections/ structure
    ├── 00_title.md
    ├── 01_abstract.md
    └── ...
```

---

## File-naming rules

- Section files use two-digit zero-padded prefixes in manuscript order (`01_`, `02_`, ...).
- No `_v2` / `_round2` suffixes on artifact filenames. Rounds are distinguished by entries *inside* the files (see below).
- Side-by-side versions (`MANUSCRIPT_REVISED_v2.md`) are only created when the user explicitly asks.

---

## Round conventions

- Round counter lives in `REVIEW_LOOP_STATE.json`. It increments per invocation.
- Files are overwritten each round. Prior rounds are preserved in git.
- `MAJOR_ISSUES.md`, `MINOR_ISSUES.md`, `CLAIM_RISK_REPORT.md` keep resolved rows in history with `round_resolved` set; they are not deleted.
- `REVISION_LOG.md` gains a new `## Round N` section per round; earlier sections stay.
- `REVIEW_REPORT.md` has a top-level `## Round N — <date>` block per round, newest first; this is the one artifact that accumulates within a single file.

---

## Section front matter (revised)

```yaml
---
section: introduction
mode: full            # inherited from paper-draft's front matter
word_target: 1000
review_round: 2
revision_mode: partial   # full | partial | conservative
---
```

---

## Inline review annotations in `MANUSCRIPT_REVIEWED.md`

Inline annotations use HTML comments so the Markdown still renders cleanly:

```markdown
Our method achieves state-of-the-art performance on the [dataset] benchmark.
<!-- REVIEW: M3 · CRITICAL-overclaim · APPROVED_CLAIMS.md has no SOTA comparison.
     Revision: soften to "competitive with the strongest published baseline on [dataset]." -->
```

Annotations never modify the prose — `MANUSCRIPT_REVIEWED.md` is the *annotated* input draft. Actual edits land in `MANUSCRIPT_REVISED.md` and `sections_revised/*.md`.

---

## `REVIEW_LOOP_STATE.json` schema

```json
{
  "round": 2,
  "review_mode": "integrated",
  "revision_mode": "partial",
  "target_venue": "IJGIS",
  "paper_type": "system",
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
  "unresolved_moderate_ids": ["Mo4"],
  "status": "in_progress",
  "timestamp": "2026-04-14T22:00:00"
}
```

- `status = in_progress` → the next invocation resumes; `status = completed` → fresh start.
- `timestamp` older than 24 hours on resume → treat as stale; start fresh.
- `threadId` is the Codex MCP conversation thread, reused via `mcp__codex__codex-reply`.

---

## `REVIEW_REPORT.md` skeleton

```markdown
# Review Report

## Round 2 — 2026-04-14

### Verdict
Almost ready for [TARGET_VENUE]. 2 major issues open (M3, M7). Round 1 closed M1, M2, M4.

### Per-dimension scores
| Dimension | Round 1 | Round 2 | Δ |
|---|---|---|---|
| Gap clarity | 5.5 | 6.5 | +1.0 |
| Novelty precision | 5.0 | 6.0 | +1.0 |
| Methods rigor | 6.5 | 7.0 | +0.5 |
| Results discipline | 5.5 | 6.5 | +1.0 |
| Discussion depth | 5.0 | 6.0 | +1.0 |
| Literature positioning | 6.0 | 6.5 | +0.5 |
| Journal fit | 6.5 | 7.0 | +0.5 |
| Language and flow | 7.0 | 7.5 | +0.5 |

### What is working well
- ...

### Top remaining majors
1. M3 — ...
2. M7 — ...

### Claim-risk summary
- CRITICAL-overclaim: 0 (down from 3)
- CRITICAL-unsupported: 0 (down from 2)
- MAJOR-uncited: 1 (was 4)

### Journal-fit highlights
- ...

### Next-loop priorities
See `NEXT_LOOP_PRIORITIES.md`.

---

## Round 1 — 2026-04-13
[earlier round, preserved]
```

---

## `REVISION_LOG.md` skeleton

```markdown
# Revision Log

## Round 2 — 2026-04-14

### M3 — overclaim softened (Abstract, Introduction §1.5)
**Before**: "We achieve state-of-the-art macro-F1 of 0.87 on [dataset]."
**After**: "We achieve a macro-F1 of 0.87 on [dataset], competitive with the strongest published baseline ([CITE: ...])."
**Rationale**: APPROVED_CLAIMS.md#C1 records the number but no SOTA comparison.

### Mo4 — Related Work cluster rewrite
[before / after snippets]
[rationale]

## Round 1 — 2026-04-13
[earlier round, preserved]
```

---

## `NEXT_LOOP_PRIORITIES.md` skeleton

```markdown
# Next-Loop Priorities

## Carry-over majors
- M7 — spatial unit and CRS undefined in Methods §4.3; depends on confirming CRS in DATA_MANIFEST.md.

## New issues discovered this round
- Mo12 — Discussion §7.3 now repeats Results §6.2 after the rewrite; trim.

## Evidence blockers
- EXP-4 still pending; C4 remains a placeholder.

## Suggested next mode
`mode:methods` if M7 is the only major blocker; `integrated` if EXP-4 completes and C4 needs to be re-audited.
```
