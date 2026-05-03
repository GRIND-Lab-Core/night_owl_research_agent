# REVIEW_CHECKLIST.md — template

> Checklist used by `paper-review-loop` Phase 5. Run the subset selected by `REVIEW_MODE`.
> Every box is either `[x] ok` · `[~] moderate` · `[!] major` · `[-] n/a`.

---

## Structural

- [ ] All sections required by plan §19 are present and in the expected order.
- [ ] Word balance matches plan targets (±20%); no section is a single short paragraph while another is bloated.
- [ ] Heading hierarchy is consistent (H1 title, H2 sections, H3 subsections); no skipped levels.
- [ ] Each paragraph opens with a topic sentence that states a claim, not a transition.
- [ ] Section transitions connect forward and back to the argument arc; no orphan sections.
- [ ] Figures and tables appear near their first reference, not dumped at the end.
- [ ] Declarations (data / code / ethics) present when the venue requires them.

## Argument

- [ ] The gap is stated explicitly in the Introduction (not merely implied).
- [ ] Why prior work is insufficient is named specifically, not gestured at.
- [ ] Contributions are a numbered list of outcomes; each appears in Results and Conclusion with the same numbering.
- [ ] The lead result in Results matches the headline claim from the Abstract and plan §5.
- [ ] Introduction → Results → Conclusion form a closed loop; nothing introduced is dropped, nothing concluded is unintroduced.
- [ ] Research questions / hypotheses (plan §6) are stated and then answered.

## Novelty

- [ ] The novelty statement is specific ("to our knowledge, the first evaluation of X on Y under Z condition") rather than vague ("a novel method").
- [ ] Nearest competing approaches from plan §5 are named and differentiated on a specific dimension (problem formulation / data regime / spatial reasoning / scale / evaluation).
- [ ] No "first," "state-of-the-art," "outperforms all existing methods" claims unless directly supported by `APPROVED_CLAIMS.md`.
- [ ] Engineering novelty, workflow novelty, and scientific contribution are distinguished — not conflated.

## Methods

- [ ] Problem formulation: task, input, output, unit of analysis.
- [ ] Spatial unit of analysis and CRS stated where they matter.
- [ ] Preprocessing is specific enough to reproduce the shape of the pipeline.
- [ ] Model / framework / algorithm described with equations or algorithmic steps the plan supplies.
- [ ] For system / agent papers: architecture, module inventory, orchestration logic, artifact flow across skills, harness-level constraints.
- [ ] For spatial methods, when the claim depends on them: neighborhood definition, handling of spatial dependency, MAUP / scale considerations, CRS handling, uncertainty propagation. Mark `[-] n/a` (with one-line reason) when the question does not turn on these — do NOT flag absence as a weakness in that case.
- [ ] Baselines listed with rationale for each.
- [ ] Evaluation metrics with precise definitions.
- [ ] Implementation notes sufficient for a reader to grasp reproducibility in spirit.

## Experiments / Evaluation

- [ ] Train / val / test protocol explicit; spatial cross-validation used **when the prediction task is on spatially structured data and leakage across folds is plausible**. Standard CV is acceptable otherwise — mark `[-] n/a` with reason instead of `[!] major`.
- [ ] Metric definitions precise; unit included on every numeric column.
- [ ] Statistical tests named; effect sizes or intervals reported, not just p-values.
- [ ] Ablation axes chosen to isolate the proposed contributions.
- [ ] Sensitivity / robustness axes documented.
- [ ] Compute environment stated (hardware, framework, versions) to the extent plan §18 requires.

## Results

- [ ] Lead result stated concretely with a specific number from `APPROVED_CLAIMS.md`.
- [ ] Results organized by claim, not by figure.
- [ ] Each result: observation → metric → source experiment → one-sentence measured interpretation.
- [ ] Mixed / negative findings reported honestly when they exist.
- [ ] Every figure referenced is in `FIGURE_MANIFEST.md`.
- [ ] Every cited number is in `APPROVED_CLAIMS.md` or `EXPERIMENT_LOG.md`.
- [ ] No results interpreted more strongly than the data support.

## Discussion

- [ ] Interprets rather than repeats.
- [ ] Closes the loop to the gap stated in the Introduction.
- [ ] GIScience / GeoAI / remote sensing implications stated.
- [ ] Practical / operational implications where the paper type warrants.
- [ ] Responsible-use considerations (fairness, geoprivacy, interpretability, reproducibility, representativeness) proportional to plan §16.
- [ ] Generalizability: conditions of transfer and non-transfer named.

## Limitations

- [ ] Every plan §17 limitation appears; none silently dropped.
- [ ] Limitations are specific, not generic.
- [ ] No "future work will solve everything" framing.

## Literature positioning

- [ ] Related Work is cluster-first, not a laundry list.
- [ ] Each cluster synthesizes the thread, names 3–8 representative studies, and states what the cluster does well and where it falls short relative to the gap.
- [ ] Differentiation paragraph names nearest competitors from plan §5.
- [ ] Citations match `memory/paper-cache/` and the Synthesis section of `output/LIT_REVIEW_REPORT.md`; no fabricated keys.
- [ ] Majority of citations are recent (≥ 2020) where the field warrants.

## Journal fit

- [ ] Tone matches target venue (IJGIS / TGIS → GIScience rigor; ISPRS JPRS / RSE → sensor / quantitative rigor).
- [ ] Abstract within venue word limit (IJGIS 250, ISPRS JPRS 300, RSE 300, TGIS 200).
- [ ] Declarations present for the venue (data availability, code availability, ethics).
- [ ] Figure / table count within venue expectations.
- [ ] No hype, startup framing, or marketing language.

## Language and flow

- [ ] Terminology consistent (model / dataset / system / metric / geographic names) across sections.
- [ ] Abbreviations defined at first use and fixed.
- [ ] Sentence length varied; no three-long-sentence stacks.
- [ ] Figures referenced by purpose, not by position.
- [ ] Present tense for established knowledge, past tense for what was done in the study.
- [ ] No redundant paragraphs across sections.

---

## Scoring rubric (1–10 per dimension)

Used to populate `REVIEW_REPORT.md` scores.

| Dimension | 4 = major issues | 6 = weak accept | 7 = accept | 8+ = strong |
|---|---|---|---|---|
| Gap clarity | Gap implied, prior-work insufficiency vague | Gap stated, some specificity | Gap specific, prior-work gap named | Gap + differentiation sharp |
| Novelty precision | Vague ("a novel X") | Claimed but weakly differentiated | Differentiated on named dimension | Differentiated + supported by evidence |
| Methods rigor | Key pieces missing | Shape grasped, details thin | Reproducible in spirit | Reproducible + well-motivated |
| Results discipline | Overclaims, figure-paraphrasing | Claim-organized, some overreach | Claim-organized, measured | Claim-organized, honest on mixed findings |
| Discussion depth | Repeats results | Some interpretation | Interprets + field implications | Interprets + responsible-use + generalizability |
| Literature positioning | Laundry list | Clustered loosely | Clustered + differentiated | Clustered + differentiated + recent |
| Journal fit | Tone off, missing declarations | Tone close, minor gaps | Venue-ready tone and structure | Venue-ready + polished declarations |
| Language and flow | Terminology drift, filler | Readable, some drift | Consistent, tight | Consistent, varied, precise |
