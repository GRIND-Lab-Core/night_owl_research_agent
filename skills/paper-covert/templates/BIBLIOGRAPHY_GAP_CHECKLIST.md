# BIBLIOGRAPHY_GAPS.md — schema

> One row per unresolved citation surfaced during conversion.

| Column | Meaning |
|---|---|
| `id` | Stable id (`B1`, `B2`, ...). |
| `location` | LaTeX file + line, and the surrounding phrase. |
| `form` | How the citation appears: `[CITE: topic]` · `(Author, Year)` · `\cite{key}`. |
| `resolved_key` | Key in `references.bib`, or `—` if unresolved. |
| `candidate_sources` | Pointers to `memory/paper-cache/*.json` or the Synthesis section of `output/LIT_REVIEW_REPORT.md` that look plausible. |
| `action` | `add-to-bib` · `find-source` · `cut-claim` · `already-in-bib-but-key-mismatch`. |
| `notes` | Why the auto-resolver could not match. |

## Example

```markdown
| id | location | form | resolved_key | candidate_sources | action | notes |
|---|---|---|---|---|---|---|
| B1 | sections/02_introduction.tex:42 | `[CITE: urban heat island review]` | — | paper-cache/chakraborty2019.json | find-source | multiple candidate reviews; author must choose |
| B3 | sections/07_results.tex:118 | `\cite{smith2020}` | — | — | add-to-bib | key used but entry missing from references.bib |
```

## Rules

- Do not invent a bibliographic entry to close a gap. Leave the gap visible.
- If `CITATION_GAPS.md` (from `paper-draft`) already records the gap, reuse that reason and set `notes = "inherited from CITATION_GAPS.md"`.
- On closure (user or later loop resolves the gap), keep the row and set `action = resolved` with the round/date.
