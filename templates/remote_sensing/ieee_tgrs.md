# IEEE Transactions on Geoscience and Remote Sensing (TGRS)
## Paper Template & Formatting Guide

**Publisher**: IEEE
**Impact Factor**: ~8
**Scope**: Signal processing, image analysis, algorithms, sensor design, applications

---

## Submission Requirements

| Requirement | Specification |
|-------------|--------------|
| Page limit | 14 pages (double-column) for regular papers |
| Abstract | 250 words maximum |
| Index Terms | 4–8 IEEE taxonomy terms |
| Format | IEEE two-column, 10pt Times New Roman |
| References | IEEE style [1], [2], ... |
| Figures | 300 DPI, separate figure files |
| Code | MATLAB/Python encouraged, GitHub link accepted |

---

## Paper Structure

### Abstract (≤250 words)
No citations. Describe: problem, proposed method, key technical contribution, experimental results, comparison metrics.

### Index Terms
Use IEEE Thesaurus terms. Include: signal processing term + application domain.

### I. Introduction
- Problem formulation (mathematical if appropriate)
- Limitations of existing methods (with specific citations)
- Summary of contributions (bulleted list is acceptable)
- Paper organization paragraph

### II. Related Work
- Prior art organized by method category
- Clear differentiation from your approach

### III. Proposed Method
- Mathematical formulation with equations numbered (1), (2), ...
- Algorithm pseudocode (Algorithm 1, 2, ...)
- Complexity analysis (O-notation)
- Implementation details

### IV. Experimental Setup
- Datasets: name, size, spatial resolution, wavelengths, source
- Baselines for comparison (must include state-of-the-art)
- Evaluation metrics and their definitions
- Computational environment (GPU/CPU, RAM, framework)

### V. Results and Discussion
- Quantitative comparison table (your method vs. all baselines)
- Ablation study (if applicable)
- Visual comparison figures
- Statistical significance testing (paired t-test or Wilcoxon)

### VI. Conclusion

### Acknowledgment

### References
IEEE style. No URLs without DOI. Software citations accepted.

---

## IEEE TGRS-Specific Notes

- **Algorithm novelty is paramount**: Must clearly demonstrate algorithmic advancement
- **Comparison baselines**: Must include recent (≤3 years) state-of-the-art
- **Reproducibility**: Upload code to IEEE CodeOcean or GitHub
- **Figures**: Must be in grayscale-readable format (no color-only distinction)
- **Statistical testing**: Comparisons should include significance tests

## Checklist

- [ ] Abstract ≤250 words, no citations
- [ ] IEEE Index Terms included
- [ ] Mathematical notation consistent throughout
- [ ] Algorithm pseudocode included
- [ ] Comparison includes ≥3 recent baselines
- [ ] Tables use IEEE formatting (no vertical lines)
- [ ] Statistical significance reported
- [ ] Code available (GitHub/CodeOcean link)
