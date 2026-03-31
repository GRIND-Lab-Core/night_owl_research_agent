---
name: write-section
description: Draft a specific section of an academic paper using journal-appropriate style and the current experiment results. Sections: abstract, introduction, study_area, data, methods, results, discussion, conclusion.
---

Write paper section: $ARGUMENTS

Follow these steps:

1. **Parse section name and journal**: Arguments can be:
   - `methods` → write methods section for default journal
   - `results IJGIS` → write results for IJGIS
   - `abstract RSE` → write abstract for Remote Sensing of Environment

2. **Load context**: Read the most recent files from `output/`:
   - `literature_review.md` for background
   - `experiment_log.json` for methods and results
   - `hypotheses.json` for research questions

3. **Load journal template**: Read the appropriate template from `templates/{domain}/{journal}.md` for formatting guidance.

4. **Write the section** following these section-specific rules:

   - **abstract**: ≤250 words. Background → gap → objective → methods → key result → implication.
   - **introduction**: 4–5 paragraphs. Broad → specific → gap → objectives. End with "The objectives of this study are..."
   - **study_area**: Geography, climate, data availability rationale. Include bounding box coordinates.
   - **data**: One subsection per dataset. Source, temporal range, spatial resolution, preprocessing.
   - **methods**: Reproducible. Include equations if applicable. Reference software/library versions.
   - **results**: Report statistics. Reference figures/tables. No interpretation here.
   - **discussion**: Interpret results, compare to literature, explain spatial patterns, limitations.
   - **conclusion**: 3–4 paragraphs. Summary → contributions → future work.

5. **Save output**: Write to `output/sections/{section}_{journal}_{timestamp}.md`.

6. **Show the written section** in the response.
