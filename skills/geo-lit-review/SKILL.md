---
name: geo-lit-review
description: Geo-domain literature review. Retrieves papers from ArXiv and Semantic Scholar using domain-aware keyword expansion, builds synthesis matrix, identifies gaps. Calls tools/arxiv_fetch.py and tools/semantic_scholar_fetch.py. Writes to memory/paper-cache/.
tools: Bash, Read, Write, WebFetch
---

# Skill: geo-lit-review

You perform a targeted literature review for a geo/RS/GIScience topic. Your outputs feed idea discovery and paper writing.

---

## Phase 1: Query Preparation

1. Read `research_contract.md` or `program.md` to extract:
   - Core topic and synonyms
   - Domain focus (Geoscience, RS, GIScience, GeoAI, Disaster, EH)
   - Geographic scope
   - Any seed papers listed
2. Read `configs/default.yaml` → `domain_keywords` section to expand with domain-specific terms.
3. Build 4-6 search queries combining topic + domain terms.

---

## Phase 2: Paper Retrieval

For each query, call these tools in order:

**ArXiv:**
```bash
python tools/arxiv_fetch.py --query "<query>" --max-results 30 --output memory/paper-cache/arxiv_<slug>.json
```

**Semantic Scholar:**
```bash
python tools/semantic_scholar_fetch.py --query "<query>" --fields "title,authors,year,abstract,venue,citationCount,externalIds" --max-results 50 --output memory/paper-cache/s2_<slug>.json
```

Merge results, deduplicate by DOI/arXiv ID, truncate abstracts to 320 characters.

**Minimum requirements**: ≥ 30 papers, ≥ 60% from 2020+, ≥ 30% from priority geo venues listed in `configs/default.yaml`.

If < 30 papers found: broaden queries (add synonyms, relax year filter to 2015+) and retry.

---

## Phase 3: Synthesis

Read `skills/knowledge/synthesis-analyst.md` for the synthesis protocol, then:
1. Group papers by theme (not chronology).
2. Build a synthesis matrix: paper × (method, dataset, key metric, finding, limitation).
3. Identify consensus views, contradictions, and geographic biases.
4. Write synthesis to `memory/synthesis-YYYY-MM-DD.md`.

---

## Phase 4: Gap Analysis

For each gap dimension (Methodological, Geographic, Temporal, Data, Equity, Validation):
- Score gap: Novelty × 0.4 + Feasibility × 0.35 + Impact × 0.25
- Rank top 5 gaps
- Write to `memory/gap-analysis.md`

---

## Outputs

- `memory/paper-cache/` — JSON paper metadata files
- `memory/synthesis-YYYY-MM-DD.md` — thematic synthesis
- `memory/gap-analysis.md` — ranked gaps
- One-line summary appended to `findings.md`

**Update** `memory/MEMORY.md` Pipeline Stage Status: Stage 1 complete with N papers.
