# JOURNAL_FIT_CHECKLIST.md — venue expectations by section and paper type

> Feeds `JOURNAL_FIT_NOTES.md`. Supplements `submit-check` — this is about prose
> expectations, not format compliance (page count, reference style).

---

## Cross-venue expectations (all targets)

- Formal, scholarly, third-person (first-person plural acceptable in Methods / Discussion).
- Precise vocabulary; no hype or startup framing.
- Contributions stated as outcomes, not promises.
- Methods reproducible in spirit.
- Limitations specific, not generic.
- Declarations present: data availability, code availability, ethics, conflict of interest.
- Recent literature (majority ≥ 2020 where the field warrants).

---

## IJGIS — International Journal of Geographic Information Science

**Editorial emphasis**: GIScience theory + method. Spatial reasoning, representation, algorithms, scale, uncertainty.

- [ ] Spatial framing: unit of analysis, scale, and MAUP discussed where relevant.
- [ ] Spatial dependency and autocorrelation addressed when methods touch them.
- [ ] CRS stated for every spatial dataset.
- [ ] Discussion engages GIScience literature, not only application-side citations.
- [ ] Contribution distinguishes GIScience theoretical / methodological advance from application.
- [ ] Abstract ≤ 250 words, one paragraph.
- [ ] Main text ≤ 9,000 words.
- [ ] Keywords include at least one GIScience framing term.

**Failure modes to watch**:
- Application-only story dressed up as GIScience.
- Method reported without spatial scale / uncertainty discussion.
- Overreliance on CS-venue citations while ignoring IJGIS / TGIS / AAG lineage.

---

## ISPRS Journal of Photogrammetry and Remote Sensing (ISPRS JPRS)

**Editorial emphasis**: Remote sensing, photogrammetry, geospatial image analysis, quantitative evaluation.

- [ ] Sensors named with band combinations, spatial and temporal resolution, preprocessing chain.
- [ ] Data characteristics (cloud cover, radiometric calibration, atmospheric correction, geometric correction) stated when they affect the method.
- [ ] Ground truth / reference data: source, sampling strategy, spatial coverage, balance.
- [ ] Evaluation: quantitative metrics with uncertainty; comparison to established baselines; ablations isolate the contribution.
- [ ] Abstract ≤ 300 words.
- [ ] Main text ≤ 10,000 words.
- [ ] Results lead with quantitative tables, then spatial maps.
- [ ] Discussion addresses transferability across sensors, regions, seasons.

**Failure modes to watch**:
- Over-reliance on a single sensor / region / season without transfer discussion.
- Qualitative-only evaluation.
- Missing preprocessing detail (atmospheric / geometric correction).
- Figures that show maps without legend, scale bar, north arrow, CRS.

---

## Remote Sensing of Environment (RSE)

**Editorial emphasis**: Environmental science via remote sensing. Physical interpretation, validation, environmental significance.

- [ ] Environmental motivation specific and quantified.
- [ ] Validation against independent ground truth or established products.
- [ ] Uncertainty quantified; error propagation discussed.
- [ ] Physical or biophysical interpretation of remote-sensing signals.
- [ ] 3–5 highlights ≤ 85 chars each (Elsevier requirement).
- [ ] Abstract ≤ 300 words.
- [ ] Main text ≤ 10,000 words.

**Failure modes to watch**:
- Pure algorithmic contribution without environmental implication.
- Validation against model output rather than independent ground truth.

---

## Transactions in GIS (TGIS)

**Editorial emphasis**: GIScience with an applied / methodological slant; broader audience than IJGIS.

- [ ] Accessible problem framing for a GIScience audience that may not be ML specialist.
- [ ] Clear link between GIScience theory and the applied contribution.
- [ ] Abstract ≤ 200 words.
- [ ] Main text ≤ 8,000 words.

---

## By paper type

### Methodological innovation paper
- Method exposition takes the largest share of the Methods section.
- Ablations isolate the novel components.
- Baselines include the strongest published methods on the named benchmark.
- Discussion names the conditions under which the method transfers.

### System / agent paper
- Architecture, module inventory, orchestration logic, and artifact flow across skills are explicit.
- Engineering novelty, workflow novelty, and scientific contribution are separated.
- Evaluation includes component ablation, not only end-to-end numbers.
- Discussion addresses harness engineering decisions.

### Benchmark / evaluation paper
- Benchmark design rationale: coverage, representativeness, failure modes probed.
- Baseline suite justified as comprehensive.
- Metrics aligned with the claim axis.
- Reproducibility artifacts specified.

### Applied case study
- Study area rich and specific.
- Method is a reasonable instantiation of established techniques (not itself the contribution).
- Results speak to practical / policy implications.
- Generalizability scope named honestly.

### Conceptual / framework paper
- Related Work is load-bearing and well-organized.
- Formalization or framework is specific enough to be applied by a reader.
- Illustrative examples rather than full empirical evaluation are acceptable, but scope is stated.

### Multimodal GeoAI paper
- Modalities and alignment explicitly described.
- Cross-modal failure modes discussed in Limitations.
- Evaluation addresses each modality's contribution.

### Remote sensing analysis paper
- Sensor / preprocessing detail in Data section.
- Results lead with quantitative tables then spatial maps.
- Discussion addresses transferability.

### GIScience theory + method paper
- Theoretical advance distinguished from methodological demonstration.
- Scale, spatial dependency, uncertainty, representation addressed where relevant.

---

## Adaptation rule

If the draft's `PAPER_TYPE` and `TARGET_VENUE` mismatch (e.g. a system paper submitted to RSE), record the mismatch in `JOURNAL_FIT_NOTES.md` and recommend either reframing or changing venue. Do not silently revise the draft toward a different paper type without user confirmation.
