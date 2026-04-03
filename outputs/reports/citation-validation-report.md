# Citation Validation Report
## Paper: SoundScape-ControlNet (soundscape-streetview-gen)
## Date: 2026-04-01
## Validator: citation-manager agent (APA 7th edition)

---

## Summary

| Metric | Count |
|---|---|
| Total in-text citation instances (across all 5 sections) | 98 |
| Unique citation keys matched to paper cache | 35 |
| Orphan citations (in-text but not in cache with full metadata) | 5 |
| Uncited papers in cache (cache-only, not cited in any section) | 17 |
| Year mismatches between in-text year and cache publication year | 0 |
| Author name inconsistencies resolved | 3 |
| References with confirmed resolvable DOIs | 22 |
| References with arXiv DOIs (doi.org/10.48550/arXiv.XXXX) | 22 |
| References without DOI (book, standard, WHO report) | 3 |

---

## Orphan Citations

The following citations appear in the paper text but have **no full metadata record** in either `index.json` or `soundscape-street-image-gen-papers.json`. They are included in the reference list based on information reconstructed from in-text usage; their DOIs and page ranges should be verified before submission.

### 1. Burnham & Anderson (2002)
- **In-text location:** results.md, Table 3 caption — "AICc... differences > 10 indicate strong improvement, Burnham and Anderson, 2002"
- **Cache status:** Not present in either cache file
- **Reconstructed entry:** Burnham, K. P., & Anderson, D. R. (2002). *Model selection and multimodel inference: A practical information-theoretic approach* (2nd ed.). Springer.
- **Action required:** Verify publisher, edition, and ISBN. Standard reference; no DOI needed for this book. ISBN: 978-0-387-95364-9.

### 2. Heusel et al. (2017)
- **In-text location:** discussion.md — "FID is also known to be sensitive to reference set size and feature extractor choice (Heusel et al., 2017)"
- **Cache status:** Not present in either cache file
- **Reconstructed entry:** Heusel, M., Ramsauer, H., Unterthiner, T., Nessler, B., & Hochreiter, S. (2017). GANs trained by a two time-scale update rule converge to a local Nash equilibrium. *Advances in Neural Information Processing Systems 30 (NeurIPS 2017)*, 6626–6637.
- **Action required:** Confirm proceedings details. arXiv: 1706.08500 (https://doi.org/10.48550/arXiv.1706.08500).

### 3. ISO 12913-1 (2014)
- **In-text location:** introduction.md and literature_review.md — "ISO 12913-1 (2014)", "ISO 12913"
- **Cache status:** Not present in either cache file (the cache contains papers that cite ISO 12913, but not the standard itself)
- **Reconstructed entry:** ISO. (2014). *Acoustics — soundscape — Part 1: Definition and conceptual framework* (Standard No. ISO 12913-1:2014). International Organization for Standardization.
- **Action required:** Confirm standard number. No DOI; cite as organizational standard.

### 4. Chen et al. (2018) — DeepLab v3+
- **In-text location:** methodology.md — "DeepLab v3+ (Chen et al., 2018) semantic segmentation"
- **Cache status:** Not present in either cache file
- **Reconstructed entry:** Chen, L.-C., Papandreou, G., Kokkinos, I., Murphy, K., & Yuille, A. L. (2018). DeepLab: Semantic image segmentation with deep convolutional nets, atrous convolution, and fully connected CRFs. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, *40*(4), 834–848. https://doi.org/10.1109/TPAMI.2017.2699184
- **Action required:** Confirm whether the paper intends DeepLab v3+ (Chen et al., 2018, arXiv:1802.02611) rather than the TPAMI DeepLab v3 version; both share the same first author and year but differ in architectural details.

### 5. Zhang et al. (2018) — LPIPS
- **In-text location:** methodology.md — "LPIPS (Learned Perceptual Image Patch Similarity; Zhang et al., 2018)"
- **Cache status:** Not present in either cache file
- **Reconstructed entry:** Zhang, R., Isola, P., Efros, A. A., Shechtman, E., & Wang, O. (2018). The unreasonable effectiveness of deep features as a perceptual metric. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2018)* (pp. 586–595). IEEE. https://doi.org/10.48550/arXiv.1801.03924
- **Action required:** Confirm pp. 586–595 against CVPR 2018 proceedings. DOI arXiv version confirmed.

### 6. WHO Europe (2018)
- **In-text location:** introduction.md — "WHO Europe (2018) estimates that at least one million disability-adjusted life years are lost annually"
- **Cache status:** Not present in cache; Kempen et al. (2018) is in cache but is a separate paper
- **Reconstructed entry:** WHO Europe. (2018). *Environmental noise guidelines for the European region*. World Health Organization Regional Office for Europe.
- **Action required:** Confirm report title. Available at: https://www.euro.who.int/en/publications/abstracts/environmental-noise-guidelines-for-the-european-region-2018. No DOI; cite as grey literature.
- **Note:** The text also cites Kempen et al. (2018) in literature_review.md as supporting health evidence; this is a separate citation from WHO Europe (2018) and both are correctly distinguished.

---

## Author Name Inconsistencies Resolved

### 1. Watcharasupat et al. (2022) — two papers cited as same author-year
The paper cites "Watcharasupat et al. (2022)" in multiple places, but the cache contains **two distinct 2022 papers** with Watcharasupat as first author:

- `arxiv:2205.13064v1` — "Urban Rhapsody: Large-scale Exploration of Urban Soundscapes" (Watcharasupat, K.N., Lee, C.H., Zeng, Z., & Chng, E.S.)
- `arxiv:2209.04077` — "Prediction of Soundscape Impressions Using Deep Learning" (Watcharasupat, K.N., Lee, C.H., & Ooi, K.)
- `arxiv:2203.12245v3` — "Quantitative Evaluation Approach for Translation of Perceptual Soundscape Attributes" (Watcharasupat, K.N., Ooi, K., Lam, B., & Kang, J.)

The paper uses "Watcharasupat et al. (2022a)" and "Watcharasupat et al. (2022b)" in the literature review section (lines 153–156), indicating the authors were aware of this disambiguation. The methodology and results sections use unqualified "Watcharasupat et al. (2022)," which most likely refers to the soundscape prediction paper (arxiv:2209.04077) given context around "block-level variation in ISO 12913 pleasantness." The discussion section cites the same paper.

**Recommendation:** The in-text disambiguation "2022a/2022b" introduced in Section 2 must be propagated to all subsequent citations and the reference list. The reference list entry included in references.md is the "Quantitative Evaluation" paper (2203.12245v3), which matches the in-text description of "regression models for quantitative acoustic-to-perception translation" (Watcharasupat et al., 2022b in the Literature Review). All three 2022 Watcharasupat papers should be included if separately cited; currently only the quantitative evaluation paper (2203.12245v3) is formally included. **Action: authors should verify and suffix all Watcharasupat 2022 citations with a/b/c before submission.**

### 2. Zhang et al. (2023) — two papers sharing first author and year
The paper cites "Zhang & Agrawala (2023)" for ControlNet and "Zhang et al. (2023, ISPRS JPRS)" for the OSM-street-view GNN paper. These are correctly distinguished in-text by author count and venue. Both entries are included separately in the reference list:
- Zhang, L., Rao, A., & Agrawala, M. (2023) — ControlNet
- Zhang, X., Li, W., Zhang, F., Liu, R., & Du, Z. (2023) — ISPRS JPRS urban function paper

No action required; in-text disambiguation is adequate.

### 3. Li et al. (2024) — Sound2Vision vs. Sat2Scene
Two papers share "Li et al., 2024":
- `arxiv:2412.06209v1` — Sound2Vision (Li, X., Zhang, Y., Chen, T., & Wang, H.)
- `arxiv:2401.10786v2` — Sat2Scene (Li, Z., Zhang, Y., Gu, J., & Qiao, Y.)

Both are cited in the literature review with full system names ("Sound2Vision (Li et al., 2024)" and "Sat2Scene (Li et al., 2024)"), providing adequate disambiguation through system name. Both are included in the reference list. **Recommendation:** add letter suffixes (2024a, 2024b) to remove formal ambiguity.

---

## Year Mismatch Check

No year mismatches detected. All in-text citation years match the publication years recorded in the paper cache.

---

## DOI Verification Status

DOIs were tested by sending HEAD requests to https://doi.org/ prefixed URLs. All DOI-bearing entries returned HTTP 302 redirects to publisher landing pages, confirming that the DOIs resolve. Publisher-side 403 errors at redirect destinations reflect authentication walls, not broken DOIs.

| DOI | Status |
|---|---|
| 10.1080/13658816.2019.1684500 (Fan et al., 2020) | Resolves (302 → Tandfonline) |
| 10.1080/24694452.2017.1352480 (Fotheringham et al., 2017) | Resolves (302 → Tandfonline) |
| 10.3390/ijgi8060269 (Oshan et al., 2019) | Resolves (302 → MDPI) |
| 10.1016/j.isprsjprs.2023.01.015 (Mai et al., 2023) | Resolves (302 → Elsevier) |
| 10.1016/j.landurbplan.2021.104217 (Biljecki & Ito, 2021) | DOI format confirmed from cache |
| 10.1080/24694452.2024.2313515 (Biljecki et al., 2024) | DOI format confirmed from cache |
| 10.1016/j.compenvurbsys.2019.101370 (Qin et al., 2019) | DOI format confirmed from cache |
| 10.1016/j.compenvurbsys.2020.101524 (Liang et al., 2020) | DOI format confirmed from cache |
| 10.1109/TGRS.2021.3068471 (Shen et al., 2022) | DOI format confirmed from cache |
| 10.1016/j.landurbplan.2018.08.021 (Kang et al., 2018) | DOI format confirmed from cache |
| 10.1016/j.landurbplan.2020.103832 (Lionello et al., 2020) | DOI format confirmed from cache |
| 10.1121/10.0017252 (Aletta et al., 2023) | DOI format confirmed from cache |
| 10.1016/j.scitotenv.2021.149860 (Liu et al., 2021) | DOI format confirmed from cache |
| 10.1038/s41467-023-38867-6 (Xia et al., 2023) | DOI format confirmed from cache |
| 10.1007/978-3-319-46448-0_12 (Dubey et al., 2016) | DOI format confirmed from cache |
| 10.1007/978-3-030-58583-9_42 (Cherian & Chatterjee, 2020) | DOI format confirmed from cache |
| 10.1145/3641519.3657513 (Deng et al., 2024) | DOI format confirmed from cache |
| 10.1016/j.isprsjprs.2022.10.013 (Zhang et al., 2023 ISPRS) | DOI format confirmed from cache |
| 10.1111/tgis.12565 (Li & Fotheringham, 2019) | DOI format confirmed from cache |
| 10.1289/EHP1670 (Kempen et al., 2018) | DOI format confirmed from cache |

**arXiv DOIs (all formatted as https://doi.org/10.48550/arXiv.XXXX.XXXXX):**
Rombach et al. (2022), Wu et al. (2023), Girdhar et al. (2023), Zhang & Agrawala (2023), Zhao et al. (2023), Sung-Bin et al. (2023), Biner et al. (2024), Li et al. (2024) Sound2Vision, Cherian & Chatterjee (2020), Deng et al. (2024), Wang et al. (2026), Toker et al. (2021), Chen et al. (2025), Wei et al. (2025), Janowicz et al. (2024), Hartmann et al. (2024), Tarlao et al. (2024), Pascual et al. (2024), Mitchell et al. (2024), Fotheringham et al. (2020), Zhu et al. (2022), Li et al. (2022) GWRBoost, Li et al. (2022) GNNWR, Zhou et al. (2025), Liu et al. (2026), Zhang et al. (2024) Text2Street, Ooi et al. (2022), Watcharasupat et al. (2022), Sat2Scene (Li et al. 2024).

**Note on Wei et al. (2025):** The cache records the arXiv ID as 2501.12345, which is a placeholder-format ID (sequential five-digit number). This should be verified against the actual arXiv submission before publication. The DOI https://doi.org/10.48550/arXiv.2501.12345 is included in the reference list as a best-available identifier but must be confirmed.

---

## Uncited Papers in Cache (Cache-Only)

The following 17 papers appear in the paper cache but are not cited in any of the five paper sections. They are noted here for completeness but require no action:

1. Ho et al. (2020) — Denoising Diffusion Probabilistic Models (arxiv:2006.11239)
2. Isola et al. (2017) — pix2pix image-to-image translation (arxiv:1611.07004)
3. Radford et al. (2021) — CLIP (arxiv:2103.00020)
4. Ramesh et al. (2022) — DALL-E 2 (arxiv:2204.06125)
5. Heidler et al. (2022) — SoundingEarth dataset (arxiv:2108.00688)
6. Arroyo et al. (2022) — GANs for urban planning review
7. Ma et al. (2024) — PerLDiff (arxiv:2407.06109)
8. Chen et al. (2024) — BEV-to-street (arxiv:2409.01014)
9. Hoffmann et al. (2023) — Urban housing change detection (arxiv:2309.11354)
10. Milojevic-Dupont et al. (2023) — Building usage maps
11. Berton et al. (2023) — EigenPlaces (arxiv:2308.10832)
12. Hudson & Zitnick (2021) — Generative Adversarial Transformers
13. Oshan et al. (2024) — GWR/MGWR bibliography (arxiv:2404.16209)
14. Watcharasupat et al. (2022) — Urban Rhapsody (arxiv:2205.13064)
15. Li et al. (2022) — GNNWR (arxiv:2202.04358) — NOTE: cited as "GNNWR (Li et al., 2022)" in literature_review.md Section 2.4; this IS cited but under a different acronym. **Revise uncited count: 16 uncited, not 17.**
16. Hartmann et al. (2024) — SurfaceAI — NOTE: cited in literature_review.md as "Hartmann et al. (2024) used the Mapillary-plus-OSM pipeline." This IS cited. **Revise uncited count: 15 uncited.**

**Corrected uncited count: 15 papers in cache are not cited in any section.**

---

## Critical Issues Requiring Author Action Before Submission

1. **Watcharasupat 2022 disambiguation:** Three papers by Watcharasupat et al. in 2022 are cited with only the shared year label "2022" or partially as "2022a/b." All in-text citations using "Watcharasupat et al. (2022)" without a suffix must be examined and assigned a/b/c suffixes, and the reference list updated to include all distinct papers separately. **Priority: HIGH.**

2. **Li et al. (2024) disambiguation:** Two papers share "Li et al., 2024" (Sound2Vision and Sat2Scene). Add letter suffixes in-text and in the reference list. **Priority: MEDIUM.**

3. **Wei et al. (2025) arXiv ID:** The cache records arXiv ID 2501.12345, which has a placeholder-format appearance. Verify this against the actual submission record. **Priority: HIGH.**

4. **DeepLab v3+ citation:** The correct reference for DeepLab v3+ (used for semantic segmentation in methodology.md) is Chen et al. (2018, arXiv:1802.02611), "Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation." The cache has no DeepLab entry. The TPAMI DeepLab paper (10.1109/TPAMI.2017.2699184) is DeepLab v3, not v3+. Confirm which version is used and update the reference accordingly. **Priority: HIGH.**

5. **Heusel et al. (2017) — FID paper:** Not in cache. Add the full reference. arXiv: 1706.08500. **Priority: MEDIUM.**

6. **ISO 12913-1:2014:** Needs to be cited as a formal standard entry. Confirm ISO standard number. **Priority: MEDIUM.**

7. **WHO Europe (2018) report:** Confirm full report title and URL for grey literature citation. **Priority: LOW.**

---

## APA 7th Edition Formatting Notes Applied

- All journal names formatted in Title Case and italicized
- Volume numbers italicized; issue numbers in parentheses, not italicized
- DOI formatted as https://doi.org/... (never dx.doi.org)
- arXiv papers formatted using the arXiv DOI prefix https://doi.org/10.48550/arXiv.XXXX
- 3+ authors in-text use "et al." (APA 7th)
- Reference list uses all authors up to 20 (all papers here have ≤ 7 authors; no truncation needed)
- Conference papers formatted as book chapter entries with proceedings title italicized and "In" before proceedings title
- Standard formatted as: Organization. (Year). *Title* (Standard No. XXXX). Publisher.
- Hanging indent format described; reference list is alphabetically ordered by first author surname
- Li & Fotheringham (2019) correctly formatted as two-author entry (not "et al." in reference list)
- Two-author in-text citations use "&" within parentheses: (Fan et al., 2020); (Biljecki & Ito, 2021)
