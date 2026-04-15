# FIGURE_MANIFEST.md — Template

> Save the filled version at `output/figures/FIGURE_MANIFEST.md`. Maintain in place; never delete rows.

---

## Summary

- **Venue:** <IJGIS | ISPRS JPRS | RSE | TGIS | …>
- **Total figures:** <N>
- **Pathway split:** code=<n>, prompt=<n>, hybrid=<n>
- **Status split:** ready=<n>, stub=<n>, draft-prompt=<n>, blocked=<n>
- **Last updated:** <YYYY-MM-DD>

## Figure Index

| ID | Title | Type | Pathway | Priority | Status | Data Source | Script / Prompt | Claims | Missing Inputs | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Fig01 | <title> | <type> | prompt | HIGH | draft-prompt | - | prompts/Fig01_prompt.md | C1,C2 | - | widescreen |
| Fig02 | <title> | choropleth map | code | HIGH | ready | data/processed/<file> | scripts/Fig02_<slug>.py | C3 | - | EPSG:5070 |
| Fig03 | <title> | ablation bars | code | MEDIUM | stub | output/results/<file>.json | scripts/Fig03_<slug>.py | C5 | <file>.json | blocked on experiment X |

## Provenance

For each figure, one paragraph:

- **Fig0N** — input files (with commit/hash if available), script or prompt path, command used to render, output files produced, claim IDs supported, known assumptions.

## Consistency Issues

- [ ] Figure numbering contiguous and matches `PAPER_PLAN.md`
- [ ] Typography / palette / line weights consistent across code figures
- [ ] Dataset and model names match `APPROVED_CLAIMS.md` and Methods section
- [ ] Every caption number is backed by `APPROVED_CLAIMS.md`
- [ ] Every map states CRS + EPSG and includes scale bar, north arrow, legend, inset

List any violations here with the figure ID and a one-line description.

## Outstanding Blockers

- <figure ID> — <missing input or decision needed>
