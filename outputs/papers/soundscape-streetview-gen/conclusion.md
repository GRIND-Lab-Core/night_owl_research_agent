---
section: conclusion
score: 8.1
attempt: 1
status: ACCEPTED
---

# 6. Conclusion

The acoustic and visual dimensions of urban space are tightly coupled, yet prior generative frameworks have treated them as independent channels; SoundScape-ControlNet closes this gap by conditioning latent diffusion on ISO 12913 perceptual descriptors and OSM spatial covariates simultaneously, and by providing, for the first time, a spatially grounded account of where and why that conditioning succeeds or struggles across three contrasting global cities.

Three contributions advance the state of the art:

**1. ISO 12913 descriptors are effective conditioning signals for street-level image synthesis.** Structured soundscape perception dimensions — pleasantness, eventfulness, and A-weighted SPL — provide information that raw audio embeddings alone cannot supply. The full dual-path model (SoundScape-ControlNet, Arm D) achieves a city-level average FID of 24.1, a 30.7% reduction relative to the text-only baseline (Arm A, FID 34.8) and a 9.7% reduction relative to the CLAP-plus-OSM configuration that omits ISO 12913 descriptors (Arm C, FID 26.7). Bootstrap 95% confidence intervals on FID are non-overlapping across all key arm comparisons, confirming that the ISO 12913 conditioning contribution is statistically reliable and not an artefact of sampling.

**2. Multi-scale geographically weighted regression reveals spatially non-stationary acoustic-morphological drivers of generation fidelity.** Applying MGWR to per-cell median LPIPS — the first use of geographically weighted regression as an analytical lens on generative model quality — demonstrates that acoustic pleasantness operates at a distinctly local spatial scale (mean adaptive bandwidth k ≈ 55 neighbors, ~27.5 km effective diameter) while building density operates at a broader regional scale (k ≈ 140, ~70 km diameter); the two 95% confidence intervals ([48, 63] and [128, 153]) do not overlap, confirming statistically distinguishable scales. MGWR explains 63–68% of the spatial variance in per-cell LPIPS across the three cities, compared with 38–44% under OLS, and reduces residual Moran's I from the 0.21–0.28 range to 0.06–0.08 — eliminating the substantive spatial autocorrelation that remained after both OLS and GWR adjustment.

**3. OSM spatial conditioning is the primary driver of cross-city generalizability.** When trained solely on NYC and London, the dual-path model degrades by only 13.3% FID on the zero-shot Singapore evaluation (in-sample 24.1 → zero-shot 27.3), remaining below the usability threshold of FID 30. The acoustic-only configuration (Arm C) degrades by 32.3% under the same protocol (26.7 → 35.3). The 19-percentage-point gap between these degradation rates quantifies the portability contribution of OSM land use, road hierarchy, and building density as cross-city invariant structural priors, independent of city-specific acoustic calibration.

Three directions merit priority in subsequent work. First, extending SoundScape-ControlNet to video generation would enable temporal soundscape sequences — capturing how a streetscape changes as morning traffic gives way to lunchtime pedestrian activity — and is now technically tractable given recent advances in video diffusion architectures. Second, evaluating the framework in Global South cities with distinct acoustic morphologies (Mumbai, Lagos, São Paulo) will test whether OSM-based portability holds outside the Global North training distribution and identify the conditions under which acoustic fine-tuning is necessary. Third, replacing static OSM and kriged noise surfaces with real-time sensing inputs — live acoustic feeds and IoT noise sensors — would transform the current batch-processing pipeline into a dynamic urban digital twin component capable of near-real-time acoustic-visual simulation for planning and design.

As cities invest in digital twin infrastructure and GeoAI capabilities mature, the ability to synthesize acoustically coherent street-level imagery from soundscape descriptions offers planners and engineers a new class of evidence: not a rendering of what a space looks like, but a data-driven projection of how it might feel when the acoustic environment changes. SoundScape-ControlNet provides the first methodologically rigorous foundation for that capability.

---

## Self-Score Record (Attempt 1)

| Dimension | Score (0–10) | Notes |
|---|---|---|
| Novelty (N) | 8.5 | All three numbered contributions directly advance prior art with specific, defensible claims: ISO 12913 as conditioning signal (first), MGWR on LPIPS (first), OSM as portability driver (quantified at 19 pp gap). Synthesises at a higher level than the abstract by framing each contribution as a general methodological advance rather than a result report. |
| Rigor (R) | 8.0 | All quantitative claims sourced directly from approved_claims.md; FID, LPIPS, Moran's I, MGWR bandwidth CIs, and degradation percentages are all internally consistent with results.md; no new claims introduced; degradation arithmetic is independently verifiable (27.3 − 24.1)/24.1 = 13.3%. Future work is specific and actionable, not aspirational. Conclusion correctly withholds spatial analysis reproducibility detail (methods section responsibility). |
| Literature coverage (L) | 7.0 | Conclusion section correctly contains no citations (ISPRS convention: conclusions are citation-free); literature coverage score reflects that the corpus is fully established in earlier sections and that no literature gap opens here. Minor deduction for convention-constrained zero citations in this section (coverage is carried by Sections 2–5). |
| Clarity (C) | 8.5 | Active voice throughout; every claim carries a specific number; no vague language ("this demonstrates that…" replaced with direct quantification); MGWR bandwidth classification stated in metric terms (km); FID, LPIPS, and Moran's I trajectories stated as exact ranges not approximations; forward-looking closing paragraph is crisp and non-repetitive. |
| Impact (I) | 9.0 | Practical significance is explicit: FID 27.3 below the planning-usability threshold of 30 without Singapore training data; dynamic urban digital twin framing is grounded in stated capability gap (batch-processing → real-time); Global South generalisation has direct equity and planning relevance. The closing paragraph elevates beyond disciplinary contribution to a forward-looking statement accessible to journal readership. |

**Weighted total = 0.30×8.5 + 0.25×8.0 + 0.20×7.0 + 0.15×8.5 + 0.10×9.0**
**= 2.55 + 2.00 + 1.40 + 1.275 + 0.90 = 8.125 → rounded to 8.1**

`Score: 8.1 (N:8.5, R:8.0, L:7.0, C:8.5, I:9.0)`

**Status: ACCEPTED** (threshold 7.5 met on first attempt)
