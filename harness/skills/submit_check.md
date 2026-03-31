---
name: submit-check
description: Validate a manuscript against target journal requirements before submission. Checks word count, section structure, figure count, reference format, and geo-specific reporting standards.
---

Validate manuscript for submission to: $ARGUMENTS

Follow these steps:

1. **Identify journal**: Parse the argument as a journal code (IJGIS, RSE, IEEE_TGRS, GRL, ISPRS, TGIS, AAG).

2. **Load the paper**: Read the most recent `output/paper_final.md` or the path provided.

3. **Load journal requirements** from `templates/{domain}/{journal}.md`.

4. **Run checklist** and report PASS/FAIL for each item:

### Structure Checks
- [ ] All required sections present (Abstract, Introduction, Methods, Results, Discussion, Conclusion, References)
- [ ] Abstract within word limit
- [ ] Total word count within journal limit
- [ ] Keywords provided (typically 5–8)
- [ ] Highlights provided (for Elsevier journals)

### Content Checks
- [ ] Research objectives clearly stated in Introduction
- [ ] Methods are reproducible (software, versions, parameters listed)
- [ ] All figures referenced in text
- [ ] All tables referenced in text
- [ ] Statistical results include p-values and effect sizes
- [ ] Limitations explicitly discussed

### Geo-Specific Checks
- [ ] Coordinate Reference System (CRS/EPSG) specified for all spatial data
- [ ] Spatial resolution of all datasets stated
- [ ] Map projections appropriate for study area
- [ ] Moran's I or similar spatial autocorrelation statistic reported
- [ ] Scale of analysis justified
- [ ] Open data with DOIs / access links provided

### Reference Checks
- [ ] All citations in text appear in reference list
- [ ] Reference format matches journal style
- [ ] DOIs included where available
- [ ] Software/library citations included (if required)

### Figure/Table Checks
- [ ] Figures at 300 DPI (for final submission)
- [ ] Figure captions are self-explanatory
- [ ] Color maps accessible to color-blind readers
- [ ] Tables have clear headers and units

5. **Generate submission report**: Save to `output/submit_check_{journal}_{timestamp}.md` with PASS/FAIL status for each item and specific recommendations for any failures.
