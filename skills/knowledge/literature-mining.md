# Literature Mining Skill — Systematic Retrieval and Analysis

**Last Updated:** 2026-03-13
**Maintainer:** Research Agent — GeoAI Lab

---

## 1. Search Strategy Design

### 1.1 PICO Framework Adapted for GeoAI Research

PICO is standard in clinical epidemiology but requires adaptation for GeoAI/geography research:

**P — Population / Problem / Place:**
- What geographic context? (urban vs. rural, country, region, scale)
- What phenomenon or system? (e.g., building damage, air pollution, flood risk)
- What population is exposed or studied?

**I — Intervention / Method / Index:**
- What AI/ML method is being applied? (e.g., U-Net, BERT, Random Forest)
- What geographic data source is used? (e.g., Sentinel-2, OSM, social media)
- What is the "treatment" in causal studies?

**C — Comparison / Context / Control:**
- What is the comparison method or baseline? (traditional GIS, simpler ML, prior state-of-the-art)
- What time period or counterfactual?

**O — Outcome / Objective Metric:**
- What is the performance metric? (F1, RMSE, Kappa, AUC)
- What is the downstream decision or impact?

**S — Study Design / Spatial Scale:**
- Cross-sectional, longitudinal, experimental?
- Local, regional, national, global?

Example PICO formulation for GeoAI disaster paper:
- P: Urban areas in earthquake-affected regions
- I: Sentinel-1 SAR + deep learning (U-Net) for damage detection
- C: Traditional change detection / prior CNN methods
- O: F1 score for damage class, geographic generalization
- S: Multi-event evaluation, regional scale

### 1.2 SPIDER Framework for Qualitative/Mixed Methods

**S — Sample:** who/what is being studied
**P — Phenomenon of Interest:** the GeoAI application or concept
**I — Design:** the research design or algorithm type
**E — Evaluation:** metrics, case study, user evaluation
**R — Research Type:** empirical, theoretical, review, application

### 1.3 Boolean Operator Strategy

**AND:** narrows search to papers containing all terms
- Example: "GeoAI" AND "damage assessment" AND "satellite"

**OR:** broadens to synonyms and related terms (critical for comprehensive coverage)
- Example: ("GeoAI" OR "geospatial AI" OR "geospatial deep learning" OR "remote sensing AI")

**NOT:** exclude irrelevant topic overlap (use cautiously)
- Example: "flood mapping" NOT "biochemical flood" (rare but possible false match)

**Proximity operators** (Web of Science / Scopus): NEAR/n for terms within n words
- Example: "deep learning" NEAR/3 "damage assessment"

**Wildcard:** * for variant endings
- Example: "geospat*" matches geospatial, geospatially, geospatiotemporally

### 1.4 Query Construction Protocol

1. Start with core concept terms (3-5 keywords from PICO)
2. Expand each concept with synonyms/variants connected by OR
3. Connect concept groups with AND
4. Test in one database; review first 20 results for relevance
5. If recall too low: add synonyms, relax constraints
6. If precision too low: add AND terms, filter by venue or year
7. Document final query string for reproducibility

---

## 2. Database Coverage

### 2.1 Semantic Scholar
**Strengths:** free, comprehensive CS/engineering/science coverage, open API, citation graph, abstract extraction, author disambiguation, field-of-study filtering.

**Coverage:** 200M+ papers with full citation graphs. Strong for CS, engineering, environmental science. Integrates with arXiv.

**Best for:** GeoAI, computer vision, NLP, remote sensing methods papers. Citation network analysis.

**API endpoint:** `https://api.semanticscholar.org/graph/v1/paper/search`

### 2.2 arXiv
**Strengths:** free preprint server; most cutting-edge GeoAI work appears here months before journal publication.

**Coverage:** CS (cs.*), Electrical Engineering and Systems Science (eess.*), Physics, Mathematics, Statistics, Quantitative Biology.

**Best for:** newest methods, preprints of NeurIPS/ICLR/CVPR/ECCV papers, foundation model papers.

**API:** `http://export.arxiv.org/api/query`

### 2.3 Google Scholar
**Strengths:** broadest coverage including gray literature, theses, conference proceedings, non-English papers; cited-by function; "related articles."

**Weaknesses:** no programmatic API (requires scraping, fragile); inconsistent metadata; no field-of-study filtering.

**Best for:** comprehensive sweeps, finding theses and working papers, verifying citation counts.

### 2.4 Web of Science
**Strengths:** high-quality metadata, journal impact factors, citation analysis tools, "Highly Cited Papers," field normalization.

**Coverage:** curated; misses some CS conference proceedings and many preprints.

**Best for:** bibliometric analysis, identifying top-cited papers, journal-based filtering, SCIE/SSCI filtering.

### 2.5 Scopus
**Strengths:** broader coverage than WoS for non-English journals; author h-index calculation; affiliation search.

**Coverage:** 87M+ documents across 25,100 journals.

**Best for:** comprehensive coverage for systematic reviews; author-level metrics.

### 2.6 PubMed / MEDLINE
**Strengths:** MeSH (Medical Subject Headings) controlled vocabulary; highly structured; clinical and biomedical focus.

**Best for:** environmental health epidemiology papers (EHP, Environmental Research, Lancet Planetary Health).

**Key MeSH terms for env health GeoAI:** "Geographic Information Systems," "Air Pollution/analysis," "Environmental Exposure," "Satellite Imagery," "Spatial Analysis."

---

## 3. Semantic Scholar API Usage

### 3.1 Paper Search Endpoint

```
GET https://api.semanticscholar.org/graph/v1/paper/search
Parameters:
  - query: search string (same Boolean logic)
  - fields: paperId,title,abstract,year,authors,venue,citationCount,
            externalIds,fieldsOfStudy,influentialCitationCount
  - limit: max 100 per request
  - offset: for pagination
  - fieldsOfStudy: "Computer Science", "Environmental Science", "Geography"
  - year: e.g., "2020-2026" or "2023-"
```

Rate limits: 100 requests/minute with API key; 5,000 requests/day without key. Always include API key in header: `x-api-key: YOUR_KEY`.

### 3.2 Paper Details Endpoint

```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}
paper_id can be: S2 paper ID, DOI (DOI:...), arXiv ID (ARXIV:...),
                 PubMed ID (PMID:...)
```

### 3.3 Citation Graph Navigation

**Get papers that cite a given paper (forward citation):**
```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations
Fields: paperId, title, year, authors, citationCount
```

**Get papers cited by a given paper (backward citation / references):**
```
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references
```

### 3.4 Author Search

```
GET https://api.semanticscholar.org/graph/v1/author/search
Parameters:
  - query: author name
  - fields: authorId, name, affiliations, paperCount, citationCount, hIndex
```

### 3.5 Recommendations Endpoint

```
POST https://api.semanticscholar.org/recommendations/v1/papers
Body: {"positivePaperIds": ["paper_id_1", "paper_id_2"]}
Returns: recommended papers based on content similarity
```

---

## 4. arXiv API Usage

### 4.1 Search Endpoint

```
GET http://export.arxiv.org/api/query
Parameters:
  - search_query: ti:flood AND cat:cs.CV (title contains flood, CS Computer Vision)
  - id_list: specific arXiv IDs
  - start: offset for pagination
  - max_results: max 2000 per request (recommend ≤200 for stability)
  - sortBy: relevance | submittedDate | lastUpdatedDate
  - sortOrder: ascending | descending
```

### 4.2 Relevant Category Codes for GeoAI

| Category | Description |
|---|---|
| cs.LG | Machine Learning |
| cs.CV | Computer Vision and Pattern Recognition |
| cs.IR | Information Retrieval |
| cs.CL | Computation and Language (NLP) |
| cs.AI | Artificial Intelligence |
| cs.SI | Social and Information Networks |
| eess.SP | Signal Processing |
| eess.IV | Image and Video Processing |
| physics.ao-ph | Atmospheric and Oceanic Physics |
| q-bio.PE | Populations and Evolution (for epidemiology) |

For geospatial foundation models: cs.CV AND eess.IV
For spatial NLP: cs.CL AND cs.IR
For disaster remote sensing: cs.CV AND eess.SP

### 4.3 Date Filtering

```
submittedDate:[20230101 TO 20260313]
```

Or use `lastUpdatedDate` to capture revised papers.

---

## 5. Snowballing Techniques

### 5.1 Forward Citation Search (Who Cited This Paper?)

Also called "forward snowballing." Starting from a seed paper, find all papers that have cited it. Purpose: identify work that built on, extended, or critiqued the seed paper; trace the influence of foundational methods.

Steps:
1. Identify 3-10 seed papers from initial search
2. For each seed: retrieve citing papers via Semantic Scholar citations API
3. Screen titles and abstracts of citing papers for relevance
4. Add relevant papers to corpus
5. Repeat for new papers (multi-level snowballing, but limit to 2 levels to avoid explosion)

### 5.2 Backward Citation Search (Who Did This Paper Cite?)

Also called "backward snowballing." From a seed paper's reference list, identify foundational prior work. Purpose: identify key prior work that may not appear in keyword searches (different terminology).

Steps:
1. Retrieve references of seed paper via Semantic Scholar references API
2. Screen for relevance
3. Follow relevant references one additional level if needed

### 5.3 Co-Citation Analysis

Papers frequently cited together are likely related in topic. Build co-citation network: nodes = papers, edge weight = number of papers citing both. Community detection on this network reveals research clusters.

Tools: VOSviewer (co-citation network visualization), Bibliometrix (R package), CitNetExplorer.

---

## 6. Deduplication

Duplicate papers arise when the same paper appears in multiple databases, as preprint and published version, or with variant titles/spellings.

**Matching strategies (in priority order):**
1. **DOI match:** exact DOI string match. Most reliable. Note: arXiv DOIs (10.48550/arXiv.XXXX.XXXXX) and published DOIs may coexist for the same paper.
2. **arXiv ID match:** if both records have arXiv ID, match.
3. **Title normalization match:** lowercase, strip punctuation, strip stop words, compare. Threshold: ≥95% character similarity (Levenshtein or Jaro-Winkler).
4. **Author + year + title fragment:** require same first author last name, same year, ≥80% title match.

When deduplicated, prefer the published journal version (has DOI, page numbers, final reviewed content) over preprint unless the preprint is significantly newer or contains supplemental material not in the published version.

---

## 7. Relevance Scoring

### 7.1 Automated Scoring Criteria

Score each paper 0-100 for relevance to the research question:

| Criterion | Weight | How to Measure |
|---|---|---|
| Title keyword match | 20 | Count of query terms in title |
| Abstract keyword density | 25 | TF-IDF score of abstract against query |
| Venue tier | 15 | A* venue = 15, A = 10, B = 5, workshop/arxiv = 3 |
| Citation count (normalized by age) | 15 | Normalize by years since publication |
| Recency (2022-2026 preferred) | 10 | Linear decay for older papers |
| Author domain match | 10 | Known GeoAI/disaster/env health researcher |
| Field of study match | 5 | Matches target subfields |

Papers with score ≥ 50: include in full-text screening.
Papers with score 30-49: abstract screen by human.
Papers with score < 30: exclude (log reason).

---

## 8. Full-Text Retrieval

### 8.1 Open Access Sources
- **arXiv.org:** direct download for CS, physics, stats preprints. URL: `https://arxiv.org/pdf/XXXX.XXXXX`
- **Semantic Scholar:** links to open access PDFs for ~50% of indexed papers. Field: `openAccessPdf` in API response.
- **Unpaywall API:** `https://api.unpaywall.org/v2/{doi}?email=your@email.com` — returns best legal open access PDF URL.
- **CORE:** `https://core.ac.uk/search` — aggregates open access repositories.
- **PubMed Central (PMC):** full text for NIH-funded research; relevant for env health papers.
- **ResearchGate / Academia.edu:** author-posted PDFs; legal in most cases.

### 8.2 When Full Text Is Not Available
- Check if corresponding author has a personal/lab website with PDF
- Email author directly (cite purpose: systematic review / academic research)
- Request via interlibrary loan
- Note: do NOT use Sci-Hub (copyright violation concerns in institutional contexts)

---

## 9. Knowledge Extraction Template

For each included paper, extract the following structured fields:

```
Paper ID: [Semantic Scholar ID or DOI]
Citation: [APA 7th edition formatted citation]
Year: [YYYY]
Venue: [Journal/Conference name]
Open Access: [Yes/No/Preprint]

## Core Contribution
[1-2 sentences: what is the main novel contribution?]

## Method
- Input data: [what modalities/datasets are used as input?]
- Architecture/approach: [name and brief description of key technical method]
- Key innovation: [what is technically novel vs prior work?]

## Dataset(s)
- Name: [dataset name]
- Scale: [global, national, regional, city-level]
- Size: [number of samples/images/records]
- Availability: [open/restricted/commercial]

## Results
- Best metric: [value and metric name, e.g., F1 = 0.87]
- Comparison: [vs. which baseline, by how much]
- Statistical significance: [reported? p-value?]

## Limitations (as stated by authors)
[Bullet list]

## GeoAI Relevance
- Subfield: [spatial representation / RS computer vision / GeoAI agent / etc.]
- Geographic scope: [where evaluated; global generalizability?]
- Equity/bias considerations: [noted by authors?]

## Notes for Synthesis
[Connections to other papers, contradictions with other findings, gaps it opens]
```

---

## 10. Synthesis Matrices

### 10.1 Methods Comparison Matrix

| Paper | Year | Method | Dataset | Geography | Metric | Value | Limitations |
|---|---|---|---|---|---|---|---|
| Smith et al. | 2023 | U-Net | xBD | Multi-event | F1 | 0.84 | Limited SAR |
| Jones et al. | 2024 | ViT | SpaceNet | Urban | mIoU | 0.79 | Urban only |

### 10.2 Theme-based Organization

Group papers by:
- Method type: supervised / self-supervised / semi-supervised / LLM-based
- Data modality: optical / SAR / multi-modal / text + imagery
- Hazard type: earthquake / flood / wildfire / hurricane / multi-hazard
- Task: damage detection / flood mapping / risk assessment / early warning
- Geography: global / regional / local

---

## 11. PRISMA Flow Tracking

PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses): standard reporting for systematic literature reviews.

```
PRISMA Flow for [Review Topic]
================================
Database Search Results:
  - Semantic Scholar: N = [n1]
  - arXiv: N = [n2]
  - Web of Science: N = [n3]
  - Google Scholar: N = [n4]
  Total records identified: N = [total]

After deduplication: N = [dedup_total]
  Records removed as duplicates: N = [total - dedup_total]

Title/Abstract Screening:
  Records screened: N = [dedup_total]
  Records excluded: N = [excluded_title_abstract]
  Reason: not relevant to [topic], wrong method, wrong geographic scope

Full-Text Eligibility Assessment:
  Full texts assessed: N = [eligible]
  Full texts excluded: N = [full_text_excluded]
  Reasons: no primary data, methodology unclear,
           behind paywall + not retrievable [n],
           geographic scope mismatch [n]

Included in Review:
  Final included papers: N = [final_n]
  From database search: N = [from_search]
  From snowballing: N = [from_snow]
```

Update PRISMA counts in MEMORY.md after each search session.

---

## 12. Quality Indicators

### 12.1 Paper-Level Quality
- **Citation count / citation velocity:** citations per year since publication; high velocity = rapidly influential
- **Venue tier:** CORE ranking (A*, A, B, C) for conferences; journal impact factor (JIF) or CiteScore for journals
- **Reproducibility:** does paper provide code? data? — check GitHub/Zenodo/HuggingFace links in paper
- **Methodological rigor:** cross-validation strategy, statistical significance reporting, ablation study presence
- **Peer review status:** published (peer-reviewed) > preprint > technical report

### 12.2 Author-Level Quality
- **h-index:** number h such that author has h papers each cited ≥ h times
- **Author affiliation:** track record of institution/lab in the domain
- **Self-citation rate:** excessive self-citation inflates citation counts; check in Semantic Scholar

### 12.3 Journal-Level Quality
- **Impact Factor (JIF 2024):** citations in 2024 to papers published 2022-2023 / total papers 2022-2023
- **CiteScore:** Scopus metric over 3-year window; more stable than JIF
- **h5-index (Google Scholar Metrics):** h-index for papers published in last 5 years
- **Subject-normalized impact:** compare JIF within subfield, not across fields
