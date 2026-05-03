---
name: submit-check
description: Validates a manuscript against target journal requirements before submission. Checks word count, section structure, figure/table count, reference format, and geo-specific reporting standards. Writes a PASS/FAIL checklist report to output/reports/.
tools: Read, Write, Bash
---

# Skill: submit-check

You validate a paper manuscript against a target journal's requirements and geo-domain reporting standards. You read the paper and journal template, run through each checklist item, and produce a submission readiness report.

---

## Inputs

- Argument: journal code (e.g. `IJGIS`, `RSE`, `IEEE_TGRS`, `GRL`, `ISPRS`, `TGIS`, `AAG`, `CEUS`)
- Paper file: `output/papers/<slug>/paper_final.md` or the path provided by the user
- Journal template: `templates/<domain>/<journal>.md`

If no paper path is given, look for the most recently modified `.md` file under `output/papers/`.
If no journal is given, read the target journal from `research_contract.md`.

---

## Checklist

Run each item and record **PASS**, **FAIL**, or **WARN** with a specific note.

### 1. Structure

| Item | How to check |
|---|---|
| All required sections present | Look for headings: Abstract, Introduction, Methods/Methodology, Results, Discussion, Conclusion, References |
| Abstract within word limit | Count words in abstract block; limit from journal template |
| Total word count within limit | `wc -w` on paper file (excluding references); compare to template limit |
| Keywords provided (5–8) | Look for "Keywords:" line after abstract |
| Highlights provided | Required for Elsevier journals (RSE, CEUS); 3–5 bullet highlights ≤ 85 chars each |
| Author contributions statement | Required by most journals since 2022 |

### 2. Content

| Item | How to check |
|---|---|
| Research objectives explicitly stated in Introduction | Scan for "The objectives of this study are..." or equivalent |
| Methods reproducible | Check that software names, library versions, and key parameters are listed |
| All figures referenced in text | Every "Figure N" in text must have a corresponding figure caption |
| All tables referenced in text | Every "Table N" in text must be referenced |
| Statistical results include effect sizes | R², p-values, confidence intervals, not just "significant" |
| Limitations explicitly discussed | Scan Discussion or dedicated Limitations section |
| Ethical statement / data access statement | Required by most journals; check for presence |

### 3. Geo-Specific

These items apply **only when the paper's claims actually depend on them**. For each conditional item, mark **PASS**, **FAIL**, **WARN**, or **N/A** with a one-line reason. Do NOT mark **FAIL** when an item is genuinely irrelevant to the paper's question — mark **N/A** with reason.

| Item | Conditional? | How to check |
|---|---|---|
| CRS / EPSG specified for all spatial data | **Always** when spatial data is used | Every dataset description must include CRS (e.g. WGS84 EPSG:4326, UTM Zone 10N EPSG:32610) |
| Spatial resolution of all datasets stated | **Always** when spatial data is used | E.g. "30 m resolution", "500 m MODIS grid" |
| Map projections appropriate for study area | **Always** when distance/area is computed | No distance/area analysis in geographic (degree) CRS |
| Moran's I (or equivalent) reported for regression residuals | **Only if** the paper fits a regression that assumes residual independence on spatially structured data | Check Results section. Mark **N/A** for non-regression papers, descriptive cartography, deep-learning models reported by held-out spatial CV, or non-spatial outcome models. |
| Moran's I p-value reported | **Only if** Moran's I is reported | Statistic alone is insufficient when reported |
| Scale of analysis justified | **Always** when an aggregated areal unit is chosen by the researcher | Why this spatial scale? Discuss MAUP **only when** the conclusion could plausibly change at a different aggregation; otherwise a one-line "fixed unit by data-generating process" is sufficient. |
| Open data with DOIs or repository links | **Always** | Every dataset must have a citable source |
| Software citations included | **When** the listed library is load-bearing for a reported result | mgwr, statsmodels, geopandas, etc. cited with version and DOI |

**Reviewer principle**: a paper whose research question is non-spatial in substance (even if the data have coordinates) should not be penalized in this section for omitting spatial diagnostics. When uncertain whether an item applies, ask the user before marking **FAIL**.

### 4. References

| Item | How to check |
|---|---|
| All in-text citations appear in reference list | Cross-reference citation keys |
| All reference list entries cited in text | No orphan references |
| Reference format matches journal style | APA 7th (most geo journals), or IEEE, or Chicago — check template |
| DOIs included where available | |
| Self-citations within normal range | Typically < 15% of total citations |

### 5. Figures and Tables

| Item | How to check |
|---|---|
| Figure files exist at stated paths | Check `output/figures/` |
| All map figures have scale bar, north arrow, legend | Read captions in `output/figures/captions.md` |
| CRS stated in each map caption | |
| Color maps accessible for color-blind readers | Prefer viridis, RdYlBu, cividis; avoid pure red-green |
| Figure captions are self-explanatory | Caption alone must describe what is shown, data source, CRS |
| Tables have clear headers and units | All numeric columns must include units |

---

## Journal Word Limits Reference

| Journal | Main text limit | Abstract | Figures |
|---|---|---|---|
| IJGIS | 9,000 words | 250 words | 10 |
| RSE (Remote Sensing of Environment) | 10,000 words | 300 words | 12 |
| IEEE TGRS | 8 pages (double column) | 250 words | 8 |
| GRL (Geophysical Research Letters) | 4,000 words | 150 words | 4 |
| ISPRS JPRS | 10,000 words | 300 words | 12 |
| TGIS (Transactions in GIS) | 8,000 words | 200 words | 10 |
| AAG Annals | 10,000 words | 200 words | 10 |
| CEUS (Computers, Environment and Urban Systems) | 9,000 words | 250 words | 12 |

If journal template file exists at `templates/<domain>/<journal>.md`, use that as the authoritative source — it overrides this table.

---

## Output

Write the report to `output/reports/submit_check_<journal>_<YYYY-MM-DD>.md`:

```markdown
# Submission Check Report — <JOURNAL> — <DATE>

Paper: <path>
Journal: <journal>
Run by: submit-check skill

## Summary
- Total items checked: N
- PASS: N
- FAIL: N
- WARN: N

**Overall verdict: READY / NOT READY**

## Failed Items (must fix before submission)
| Section | Item | Issue |
|---|---|---|
| Geo-Specific | Moran's I p-value | Not reported for GWR residuals in Results §3.2 |
| References | DOIs missing | 4 references lack DOIs |

## Warnings (review before submission)
| Section | Item | Note |
|---|---|---|
| Content | Self-citation rate | 18% — above typical 15% guideline |

## Passed Items
[collapsible list or count]

## Recommended Fixes
1. [Specific, actionable fix]
2. [Specific, actionable fix]
```

After writing the report, display the **Summary** and **Failed Items** sections in the response so the user sees them immediately.
