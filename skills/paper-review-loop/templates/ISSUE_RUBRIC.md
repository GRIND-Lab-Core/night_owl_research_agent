# ISSUE_RUBRIC.md — major / moderate / minor schema

> Row schema used by `MAJOR_ISSUES.md` and `MINOR_ISSUES.md`.
> Issue ids are stable across rounds. Once `M7` exists, it stays `M7`.

---

## Schema

| Column | Meaning |
|---|---|
| `id` | Stable id. Majors: `M1`, `M2`, ... · Moderates: `Mo1`, `Mo2`, ... · Minors: `m1`, `m2`, ... |
| `severity` | `major` · `moderate` · `minor` |
| `section` | Section name and subsection locator if any. |
| `description` | One-sentence diagnosis. |
| `evidence` | Pointer into the draft (section + quoted snippet) or into the plan / evidence file. |
| `proposed_revision` | Specific, actionable edit. No rewrites-as-criticism. |
| `round_introduced` | Round the issue was first raised. |
| `round_resolved` | Round the issue was fixed, or `—` if still open. |
| `carry_over` | `yes` if unresolved and moved to `NEXT_LOOP_PRIORITIES.md`. |
| `notes` | Rationale for softening / cutting / deferring, if any. |

---

## Example rows

```markdown
| id | severity | section | description | evidence | proposed_revision | round_introduced | round_resolved | carry_over | notes |
|---|---|---|---|---|---|---|---|---|---|
| M3 | major | Introduction §1.5 | Contribution 2 claims "state-of-the-art" without support from APPROVED_CLAIMS.md | draft L142; APPROVED_CLAIMS has no benchmark-leading row | Soften to "competitive with the strongest published baseline on [dataset]" | 1 | 2 | no | — |
| M7 | major | Methods §4.3 | Spatial unit and CRS never stated; all distance claims ambiguous | draft L321–L340 | Add subsection "Spatial unit and projection" with unit, CRS (EPSG:32610), area, boundary rule | 1 | — | yes | depends on confirming CRS in DATA_MANIFEST.md |
| Mo4 | moderate | Related Work | Laundry-list paragraph on GNN baselines; no synthesis | draft L215–L240 | Rewrite as one synthesis paragraph with 4 representative studies grouped by task formulation | 2 | — | yes | — |
| m2 | minor | Results §6.1 | "As can be seen in Fig. 3" phrasing | draft L402 | Replace with "the confusion matrix in Fig. 3 shows ..." | 2 | 2 | no | — |
```

---

## Severity criteria

**Major** — blocks publication at IJGIS / ISPRS JPRS / RSE / TGIS. Examples:
- weak or missing gap articulation
- unclear novelty or novelty unsupported by differentiation
- claims whose strength exceeds evidence (overclaims)
- insufficient methods detail to grasp the method
- weak experiment description (unclear protocol, metrics, baselines)
- results interpreted more strongly than the data support
- poor connection to GIScience / GeoAI / RS literature
- missing or defanged limitations
- mismatch with target journal expectations (tone, structure, declarations)
- structural problems (section ordering, missing sections, dangling contributions)

**Moderate** — would trigger reviewer complaints but not reject. Examples:
- repetitive writing across sections
- vague transitions
- inconsistent terminology
- weak paragraph topic sentences
- figure/table references that do not integrate with the narrative
- incomplete contextualization of findings against prior work

**Minor** — polish. Examples:
- awkward wording
- local clarity problems
- caption / title mismatches
- redundant phrases
- sentence-level polish

---

## Prioritization rule

Revise in this order, and do not polish minors while majors are open:

1. All unresolved majors.
2. Moderates in sections where majors were just resolved (to avoid regression).
3. Remaining moderates.
4. Minors — only after majors and moderates for this round are closed or explicitly deferred.
