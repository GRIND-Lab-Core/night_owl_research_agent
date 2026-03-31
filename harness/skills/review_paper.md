---
name: review-paper
description: Simulate multi-reviewer peer review for a geoscience/GIScience paper. Returns structured feedback from multiple expert personas and an editorial decision.
---

Review paper: $ARGUMENTS

Follow these steps:

1. **Parse arguments**: Accept a file path to the paper. If no path given, look for the most recent `draft_*.md` in `output/`.

2. **Identify target journal**: Check the paper's header or ask if unclear. Supported journals: IJGIS, RSE, IEEE_TGRS, GRL, ISPRS, TGIS, AAG, CAGIS.

3. **Simulate Reviewer 1** (Spatial Statistics Expert):
   - Focus: statistical validity, spatial autocorrelation handling, model assumptions
   - Provide: Summary, Major Concerns (numbered), Minor Concerns (bullets), Recommendation

4. **Simulate Reviewer 2** (Applied Domain Expert):
   - Focus: real-world relevance, study area choice, data quality, physical interpretation
   - Provide: Summary, Major Concerns, Minor Concerns, Recommendation

5. **Editorial Decision**: Based on both reviews:
   - Accept / Minor Revision / Major Revision / Reject
   - List priority issues to address

6. **Specific geo-checks** always applied:
   - [ ] CRS and projection reported?
   - [ ] Spatial autocorrelation of residuals tested?
   - [ ] Scale dependency discussed?
   - [ ] Benchmark/baseline comparison included?
   - [ ] Data reproducibility (open data, DOIs)?
   - [ ] Figures show spatial distribution, not just statistics?

7. **Output**: Save to `output/peer_review_{timestamp}.md` and display in response.
