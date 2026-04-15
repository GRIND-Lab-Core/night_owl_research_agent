# SECTION_EVIDENCE_CHECKLIST.md — template

> Minimum evidence each section must cite before it is considered drafted (not merely outlined).
> Use this during Phase 5 drafting and Phase 6 consistency pass.

## Abstract
- [ ] At least one specific number from `APPROVED_CLAIMS.md`
- [ ] Gap phrase traces to plan §4
- [ ] Contribution phrase traces to plan §5
- [ ] No citations, no figure references

## Introduction
- [ ] 2–3 authoritative citations in ¶1 from plan §22 Introduction list
- [ ] Gap sentence matches plan §4 almost verbatim (allow stylistic edit)
- [ ] Numbered contributions match plan §5 in count and ordering
- [ ] Every contribution reappears in Results or Conclusion

## Related Work
- [ ] Cluster names match plan §15
- [ ] Each cluster names ≥3 representative studies drawn from `memory/paper-cache/` or synthesis
- [ ] Differentiation paragraph names ≥1 competing approach from plan §5 table
- [ ] No paper cited here that is absent from the cache / synthesis

## Study Area / Data
- [ ] Each dataset in plan §8 has name + source + coverage + resolution + preprocessing + license
- [ ] CRS stated if spatial analysis depends on it
- [ ] Data-quality caveats from plan §8 acknowledged

## Methodology
- [ ] Problem formulation matches plan §9.1
- [ ] Every baseline in plan §9.4 appears with a justification
- [ ] Spatial-method considerations from plan §9.6 (MAUP, autocorrelation, CRS) addressed
- [ ] Implementation details sufficient for the reproducibility statement

## Experimental Design
- [ ] Split / cross-validation / spatial CV protocol stated
- [ ] Every metric in plan §9.5 defined on first use
- [ ] Ablation axes from plan §10 enumerated
- [ ] Decision rules (success criteria) stated when plan supplies them

## Results
- [ ] Headline result matches the top finding in plan §11 and `APPROVED_CLAIMS.md`
- [ ] Every number traces to `APPROVED_CLAIMS.md` or `EXPERIMENT_LOG.md`
- [ ] Every figure/table reference exists in `FIGURE_MANIFEST.md`
- [ ] Mixed / negative findings from plan §11 included
- [ ] No claim lacks an evidence row in `CLAIM_SUPPORT_MAP.md`

## Discussion
- [ ] Closes the loop to the Introduction gap
- [ ] Interprets, does not repeat
- [ ] Names at least one GIScience / GeoAI / remote-sensing implication
- [ ] Responsible-use considerations from plan §16 present if relevant
- [ ] Generalizability conditions stated

## Limitations
- [ ] Every item in plan §17 appears
- [ ] Severity phrasing matches plan §17 severity table
- [ ] No "future work will fix this" shortcuts

## Conclusion
- [ ] Contributions restated as outcomes (not promises)
- [ ] Numbering matches Introduction
- [ ] 2–4 concrete future-work directions grounded in the limitations

## Declarations
- [ ] Data availability statement drafted per plan §18
- [ ] Code availability statement drafted per plan §18
- [ ] Ethics / privacy note if plan §8 or §16 flags it
