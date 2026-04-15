# OUTPUT_CONVENTIONS.md

## Folder layout

```
output/manuscript/
├── DRAFT_README.md             # mode, venue, paper type, readiness, word counts, next actions
├── MANUSCRIPT_DRAFT.md         # assembled draft (title → declarations)
├── ABSTRACT_DRAFT.md           # stand-alone abstract + keywords
├── CLAIM_SUPPORT_MAP.md        # every non-trivial claim → evidence row
├── COVERAGE_GAPS.md            # missing content / claims / figures / citations
├── CITATION_GAPS.md            # claims needing a citation we do not yet have
├── SECTION_NOTES.md            # per-section scope, softening, deferred content
├── REVISION_NOTES.md           # prioritized next-pass actions
└── sections/
    ├── 00_title.md
    ├── 01_abstract.md
    ├── 02_introduction.md
    ├── 03_related_work.md
    ├── 04_data.md              # or 04_study_area.md for applied case studies
    ├── 05_methodology.md
    ├── 06_experimental_design.md
    ├── 07_results.md
    ├── 08_discussion.md
    ├── 09_limitations.md
    ├── 10_conclusion.md
    └── 11_declarations.md
```

## File naming

- Two-digit zero-padded prefixes (`01_`, `02_`, ...) in manuscript order.
- Revisions overwrite the same path; prior versions live in git, not filename suffixes.
- Use a `_v2` / `_v3` suffix **only** when the user explicitly requests side-by-side versions.
- System / agent papers may add `05a_system_architecture.md` after `05_methodology.md` without renumbering downstream files.

## Front matter

Every section file starts with:

```yaml
---
section: <name>
mode: <full|partial|skeleton>
word_target: <int>
---
```

Followed by a single `# N. <Section Name>` heading, then prose.

## In-prose markers

- `[PLACEHOLDER — ...]` — planned content not yet supported by evidence.
- `[CITE: <topic>]` — citation needed, not yet in cache.
- `[FIGURE PENDING REVISION]` — figure exists but is being reworked.
- `[NEEDS EVIDENCE]` — claim lacks a row in `CLAIM_SUPPORT_MAP.md`.
- `[VERIFY]` — imported from `PAPER_PLAN.md`; do not strip without resolving.

These markers must all be tracked in `COVERAGE_GAPS.md` / `CITATION_GAPS.md` / `REVISION_NOTES.md`.

## Word-target norms

| Section | Target (words) |
|---|---|
| Abstract | 150–250 |
| Introduction | 800–1200 |
| Related Work | 1000–1600 |
| Study Area / Data | 500–1000 |
| Methodology | 1200–2000 |
| Experimental Design | 400–800 |
| Results | 1000–2000 |
| Discussion | 800–1400 |
| Limitations | 300–600 |
| Conclusion | 300–500 |

Adjust ± 30% by venue and paper type. Record the final targets in `DRAFT_README.md`.
