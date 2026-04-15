# SECTION_REVIEW_TEMPLATE.md — per-section review + revision scaffold

> One scaffold instance per section. Used to populate `SECTION_REVIEW_NOTES.md`
> and to drive revisions in `sections_revised/NN_<name>.md`.

---

## Section: <name>

- **Draft mode** (from `paper-draft` front matter): full | partial | skeleton
- **Review round**: N
- **Revision mode this round**: full | partial | conservative
- **Word target vs. actual**: <target> / <actual>

### Plan alignment
- Plan §§ that govern this section: <list>
- Intended claims (from `PAPER_PLAN.md` §12): <list of ClaimIDs>
- Required evidence artifacts: <list of files>

### Strengths (what to preserve)
- [ ] ...
- [ ] ...

### Weaknesses (diagnosis)
- [ ] **Major**: ...
- [ ] **Moderate**: ...
- [ ] **Minor**: ...

### Claim-risk flags (from `CLAIM_RISK_REPORT.md`)
- C<id>: wording vs. evidence → revision action.

### Revision plan
- What to rewrite end-to-end vs. surgically edit.
- Paragraphs to add (with evidence pointers).
- Paragraphs to cut (with rationale).
- Terminology normalizations.
- Figure / table reference updates.

### Revised draft location
- `output/manuscript/sections_revised/NN_<name>.md`

### Carry-over to next loop
- Unresolved issue ids: <list>
- New evidence needed before further revision: <list>

---

## Section-specific prompts

### Abstract
- Does it hit background → gap → method → data → headline finding → significance in one paragraph?
- Is the headline number from `APPROVED_CLAIMS.md`?
- Within venue word limit?

### Introduction
- Six-paragraph arc intact?
- Contributions numbered; each a claim the Results actually supports?
- Any "first / novel / state-of-the-art" language softened where unsupported?

### Related Work
- Cluster-first, not laundry list?
- Each cluster synthesizes + names studies + states shortcoming relative to the gap?
- Differentiation paragraph names nearest competitors on a specific dimension?

### Data / Study Area
- Every dataset: name, provider, spatial + temporal coverage, resolution, variables, preprocessing, licensing, CRS, spatial unit?
- Caveats honest?
- Responsible-use paragraph when plan §16 flags it?

### Methods
- Problem formulation explicit?
- Spatial unit + CRS stated where they matter?
- Baselines with rationale?
- For system / agent papers: architecture + module inventory + orchestration + artifact flow?

### Experiments
- Protocol, metrics, statistical tests, ablation axes, sensitivity axes, compute environment — all present?
- Decision rules stated when plan §10 supplies them?

### Results
- Lead result concrete?
- Claim-organized, not figure-organized?
- Mixed / negative findings reported?
- Only figures in `FIGURE_MANIFEST.md` referenced?

### Discussion
- Closes the gap loop?
- GIScience / GeoAI / RS implications named?
- Responsible-use discussed proportional to plan §16?
- Generalizability conditions named?

### Limitations
- All plan §17 items present?
- Specific, not generic?

### Conclusion
- Contributions restated as outcomes with the same numbering as Introduction?
- 2–4 concrete future-work directions grounded in limitations?

### Declarations
- Data / code availability, ethics, conflict of interest, acknowledgements per plan §18?
