---
name: geo-search
description: "Invoke skill geo-lit-review for a geo topic. Calls tools/arxiv_fetch.py and tools/semantic_scholar_fetch.py with domain-aware keyword expansion, builds synthesis matrix, identifies research gaps. Saves to memory/paper-cache/ and memory/synthesis-*.md. Usage: /geo-search <topic>"
---

# Command: /geo-search

Perform a targeted literature search for the given topic using geo-domain-aware retrieval.

## Protocol

1. Parse `<topic>` from the command arguments. If no topic given, read from program.md Section 1.
2. Expand keywords using domain_keywords in configs/default.yaml (add synonyms, domain-specific terms)
3. Delegate to **literature-scout** agent with:
   - Expanded keyword list
   - Priority venues from configs/default.yaml
   - Year range: 2019-2026 (default)
   - Target: ≥ 30 papers
4. Display results summary:
```
Geo-Search Results: <topic>
Papers found: N
  ArXiv: N
  Semantic Scholar: N
  CrossRef: N
Top venues: RSE (N), IJGIS (N), IEEE TGRS (N), ...
Year range: XXXX–XXXX
Saved: memory/paper-cache/<topic-slug>-papers.json
```
5. Show top 10 papers by priority score with title, authors, year, venue, citation count.
