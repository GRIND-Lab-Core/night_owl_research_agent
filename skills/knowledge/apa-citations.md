# APA 7th Edition Citation Skill

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. In-Text Citations

### 1.1 Basic Forms

**One author:**
(Smith, 2023) or Smith (2023) demonstrated that...

**Two authors:**
Use "&" inside parentheses; "and" outside:
- Inside: (Smith & Jones, 2023)
- Outside: Smith and Jones (2023) found that...

**Three or more authors:**
Always use "et al." from first citation (APA 7th changed from "et al. for 6+" to "et al. for 3+"):
- (Smith et al., 2023) — regardless of number of authors
- Smith et al. (2023) showed that...

**Corporate/institutional author:**
- (World Health Organization, 2021) — spell out in full on first use
- Subsequent citations: (WHO, 2021) if abbreviation introduced: "World Health Organization (WHO, 2021)"

**No author:**
Use first few words of title in quotes (article/chapter) or italics (book/report):
- ("Flood Risk Assessment," 2023)
- (*Global Disaster Report*, 2022)

### 1.2 Multiple Works in One Parenthetical
- Same parenthetical, multiple authors: list alphabetically by first author last name, semicolons between
- (Janowicz et al., 2020; Mai et al., 2024; Wang et al., 2022)

**Same author, multiple years:** (Smith, 2020, 2022, 2024)

**Same author, same year:** add lowercase a, b, c after year:
- (Smith, 2023a, 2023b)
- Determined by order in reference list (alphabetical by title)

### 1.3 Direct Quotations
Include page number: (Smith, 2023, p. 47) or (Smith, 2023, pp. 47-48)
For works without page numbers (online, e-reader): use paragraph number: (Smith, 2023, para. 3)

### 1.4 Secondary Sources (Citing a Citation)
Avoid if possible — find the original source. If unavoidable:
- In-text: (Janowicz, 2019, as cited in Mai et al., 2024)
- Reference list: include only Mai et al. (2024)

---

## 2. Reference List Format by Type

### 2.1 Journal Article

**Standard format:**
```
Author, A. A., & Author, B. B. (Year). Title of article in sentence case.
    *Journal Name in Title Case*, *volume*(issue), page–page.
    https://doi.org/xxxxx
```

**Rules:**
- Article title: sentence case (only first word, proper nouns, first word after colon capitalized)
- Journal name: title case AND italicized
- Volume: italicized
- Issue: NOT italicized, in parentheses after volume
- DOI: always include if available; format as https://doi.org/ (never dx.doi.org)
- If no DOI: include URL of journal homepage

**Examples:**

Janowicz, K., Gao, S., McKenzie, G., Hu, Y., & Bhaduri, B. (2020). GeoAI: Spatially explicit artificial intelligence techniques for geographic knowledge discovery and beyond. *International Journal of Geographical Information Science*, *34*(4), 625–636. https://doi.org/10.1080/13658816.2019.1684500

Mai, G., Janowicz, K., Hu, Y., Gao, S., Yan, B., Zhu, R., Cai, L., & Lao, N. (2020). Multi-scale representation learning for spatial feature distributions using grid cells. In *International Conference on Learning Representations*. https://openreview.net/forum?id=rJljdh4KDH

### 2.2 Conference Paper (Proceedings)

```
Author, A. A., & Author, B. B. (Year). Title of paper. In A. Editor & B. Editor (Eds.),
    *Proceedings of the Conference Name* (pp. xx–xx). Publisher.
    https://doi.org/xxxxx
```

OR (without named editors):
```
Author, A. A. (Year). Title of paper. *Proceedings of the Conference Name*,
    *volume*, page–page. https://doi.org/xxxxx
```

**For major ML/CV conferences (NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV):** follow the doi format from the proceedings. Many are now also in arXiv — cite the published proceedings version if available.

**Examples:**

Vivanco Cepeda, V., Nayak, G. K., & Shah, M. (2023). GeoCLIP: Clip-inspired alignment between locations and images for effective worldwide geo-localization. In *Advances in Neural Information Processing Systems 36* (NeurIPS 2023). https://doi.org/10.48550/arXiv.2309.16020

### 2.3 arXiv Preprint

```
Author, A. A., & Author, B. B. (Year). Title of preprint. *arXiv*.
    https://doi.org/10.48550/arXiv.XXXX.XXXXX
```

**Notes:**
- The DOI format 10.48550/arXiv.XXXX.XXXXX is the official Crossref DOI for arXiv papers
- Italicize "arXiv" as the source
- Include arXiv ID in the DOI link
- If the paper has been published in a journal, use the journal reference instead
- If the preprint version differs substantially from the published version (extended methods, additional experiments), it is permissible to cite both

**Example:**

Jakubik, J., Roy, S., Phillips, C. E., Fraccaro, P., Godwin, D., Zadrozny, B., Szwarcman, D., Gomes, C., Nyirjesy, G., Edwards, B., Kimura, D., Simumba, N., Chu, L., Mukkavilli, S. K., Non, D., Krishnamurthy, R., Das, K., Weldemariam, K., & Singh, R. (2023). *Prithvi-100M: A geospatial foundation model*. arXiv. https://doi.org/10.48550/arXiv.2310.18660

### 2.4 Book

```
Author, A. A. (Year). *Title of book in sentence case*. Publisher.
    https://doi.org/xxxxx (if available)
```

**Multi-edition:**
```
Author, A. A. (Year). *Title of book* (3rd ed.). Publisher.
```

**Translated work:**
```
Author, A. A. (Year). *Title* (T. Translator, Trans.). Publisher. (Original work published YYYY)
```

### 2.5 Book Chapter (Edited Volume)

```
Author, A. A., & Author, B. B. (Year). Title of chapter. In E. E. Editor & F. F. Editor (Eds.),
    *Title of book* (pp. xx–xx). Publisher. https://doi.org/xxxxx
```

**Notes:**
- Chapter title: sentence case
- Book title: sentence case AND italicized
- Editor names follow "In" with initials first, then (Eds.) or (Ed.)

### 2.6 Software and Code

```
Author, A. A. (Year). *Software name* (Version X.X.X) [Computer software].
    Publisher/Repository. URL or DOI
```

**Examples:**

Gillies, S., van der Wel, C., Van den Bossche, J., Taves, M. W., Arnott, J., Ward, B. C., & others. (2023). *Shapely* (Version 2.0.2) [Computer software]. GitHub. https://github.com/shapely/shapely

Boeing, G. (2017). *OSMnx* [Computer software]. GitHub. https://github.com/gboeing/osmnx

### 2.7 Technical Report / Government Report

```
Organization or Author. (Year). *Title of report*. Publishing Organization. URL
```

Or with report number:
```
Organization. (Year). *Title of report* (Report No. XXX). Organization. URL
```

**Examples:**

Federal Emergency Management Agency. (2023). *National preparedness report 2023*. U.S. Department of Homeland Security. https://www.fema.gov/...

Intergovernmental Panel on Climate Change. (2021). *Climate change 2021: The physical science basis*. Cambridge University Press. https://doi.org/10.1017/9781009157896

### 2.8 Website / Webpage

```
Author/Organization. (Year, Month Day). *Title of page*. Site Name. URL
```

If no date: use (n.d.)
If no author: start with title

**Example:**

European Space Agency. (2024, January 15). *Sentinel-2 mission overview*. ESA Earth Online. https://sentinel.esa.int/web/sentinel/missions/sentinel-2

### 2.9 Dataset (Cite the Paper, Not the Portal)

Preferred: cite the data descriptor paper or the study that released the data.

```
Tellman, B., Sullivan, J. A., Kuhn, C., Kettner, A. J., Doyle, C. S., Brakenridge, G. R.,
    Erickson, T. A., & Slayback, D. A. (2021). Satellite imaging reveals increased
    proportion of population exposed to floods. *Nature*, *596*(7870), 80–86.
    https://doi.org/10.1038/s41586-021-03695-w
```

If no paper exists, cite the data source directly:
```
U.S. Environmental Protection Agency. (2023). *Air Quality System (AQS) data* [Dataset].
    EPA. https://www.epa.gov/aqs
```

---

## 3. Special Cases

### 3.1 Same Author, Same Year
Add lowercase letters (a, b, c) after year in both in-text and reference list.
Order determined by title alphabetical order in the reference list.

In-text: (Smith, 2023a, 2023b)
Reference list:
```
Smith, J. A. (2023a). Earlier paper title...
Smith, J. A. (2023b). Later paper title...
```

### 3.2 No Author
Use organization name: (World Bank, 2022)
If no organization: use shortened title in italics or quotes.

### 3.3 Translator
```
Author, A. (Year). *Title* (T. Translator, Trans.; Nth ed.). Publisher.
    (Original work published YYYY)
```

### 3.4 Edition Number
Include after title: *(2nd ed.)* or *(Rev. ed.)* NOT in parentheses, part of title field.

---

## 4. Common Errors

### 4.1 "et al." in Reference List
**APA 7th rule:** list ALL authors in reference list up to 20.
For 21+ authors: list first 19, then an ellipsis (...), then the last author.
Never use "et al." in the reference list entry itself.

Correct for 21+ authors:
```
Smith, A. A., Jones, B. B., Brown, C. C., ... (19 more names) ..., Williams, Z. Z. (2023).
```

### 4.2 Missing DOI
Always search for DOI even if not obvious. Use https://doi.org to look up by title.
If DOI does not exist: include URL of the paper or journal page.

### 4.3 Inconsistent Journal Name Formatting
The journal name must be in title case AND italicized. The volume number is italicized. The issue number in parentheses is NOT italicized.

Wrong: *international journal of geographical information science*, 34(4)
Wrong: *International Journal of Geographical Information Science*, *34*(*4*)
Correct: *International Journal of Geographical Information Science*, *34*(4)

### 4.4 dx.doi.org vs. doi.org
Always use **https://doi.org/** prefix. Never use http://dx.doi.org/ (deprecated).

### 4.5 Preprint to Published Version
If a paper was initially cited as an arXiv preprint but has since been published:
- Update the reference to the published journal version
- Use the journal DOI
- Check if the published version differs substantially (some papers are revised significantly)

### 4.6 Alphabetical Ordering
Reference list is ordered alphabetically by first author's last name. Then by first author's first name initial. Then by year (earliest first). Same author, same year: use a, b, c.

Special cases:
- "Mc" and "Mac": alphabetize as written (MacArthur before McClellan)
- Numbers in names: alphabetize as if spelled out
- Hyphenated names: alphabetize by first part (Chang-Price → Ch-)

---

## 5. DOI Format Details

- Always use the full URL form: `https://doi.org/10.1080/13658816.2019.1684500`
- Do NOT use angle brackets around DOIs in APA 7th (changed from APA 6th)
- Do NOT add a period after a DOI that ends a reference entry (the DOI IS the end)
- If URL is very long (>100 chars): shorten with DOI shortener only if the full DOI resolves correctly

---

## 6. Italics Rules Summary

| Element | Italicized? |
|---|---|
| Journal name | YES |
| Volume number | YES |
| Issue number | NO (in parentheses after volume) |
| Book title | YES |
| Report title | YES |
| Article/chapter title | NO |
| arXiv (as source name) | YES |
| Website page title | YES (if it stands alone, not a webpage within a larger work) |

---

## 7. GeoAI-Specific Edge Cases

### 7.1 Institutional Authors (IEEE, NASA, ESA)
These are treated as organizational authors. Spell out in full in the reference list.
In-text: (NASA, 2023) after first introduction as "National Aeronautics and Space Administration (NASA, 2023)."

### 7.2 Dataset Papers
Always prefer citing the academic paper that describes/releases the dataset over citing the data portal or website alone. Example: cite Deng et al. (2009) for ImageNet, not the website. Cite Tellman et al. (2021) for the Global Flood Database, not the UNEP website.

### 7.3 GitHub Repositories
If no software citation paper exists:
```
AuthorLastName, A. (Year). *Repository name* [Computer software]. GitHub.
    https://github.com/user/repo
```
If a Zenodo DOI exists for the repository (preferred): use the Zenodo DOI.

### 7.4 Conference Workshop Papers
Format as conference paper; include workshop name in the title of the proceedings:
```
Author, A. (2023). Title. In *Proceedings of the Workshop on GeoAI at ACM SIGSPATIAL 2023* (pp. xx–xx). ACM. https://doi.org/...
```

---

## 8. Validation Checklist Before Submitting

Run through this checklist for every submission:

- [ ] Every in-text citation has a matching reference list entry
- [ ] Every reference list entry has at least one in-text citation (no orphan references)
- [ ] All DOIs formatted as https://doi.org/ (not dx.doi.org/, not bare DOI without prefix)
- [ ] Reference list is sorted alphabetically by first author last name
- [ ] Same author, same year: a/b/c suffixes applied consistently in both in-text and reference list
- [ ] No "et al." used in reference list entries
- [ ] All 21+ author papers use first 19 + ... + last format
- [ ] Journal names in title case AND italicized
- [ ] Volume numbers italicized; issue numbers NOT italicized
- [ ] Article titles in sentence case; journal/book titles in sentence case in reference list
- [ ] arXiv preprints: if published version exists, reference list uses published version
- [ ] No missing page numbers for print journal articles (use complete page range)
- [ ] All URLs tested and resolving (especially important for dataset and report citations)
- [ ] Software/code versions specified
- [ ] For papers with 2 authors: "&" used in parenthetical, "and" used in running text

---

## 9. Formatting Shortcuts for Common GeoAI Venues

**IJGIS (International Journal of Geographical Information Science):** APA 7th; no deviation.

**Remote Sensing of Environment:** Elsevier author-year (very similar to APA; minor formatting differences — check author guidelines per submission).

**ACM SIGSPATIAL proceedings:** ACM reference format (different from APA; numbered references). When submitting to ACM venues, switch to ACM format: [1] style citations.

**NeurIPS / ICML / ICLR:** Custom author-year format similar to APA but with specific proceedings notation. Always download the venue's bibliography style file (`.bst` for LaTeX, `.csl` for Zotero/Pandoc).

**APA strict use cases:** journal submissions to IJGIS, AAG Annals, Transactions in GIS, GeoHealth, Environmental Health Perspectives, GeoHealth, and most geography/public health journals.
