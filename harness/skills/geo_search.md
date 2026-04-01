---
name: geo-search
description: Invoke skill geo-lit-review for a geo topic. The skill calls tools/arxiv_fetch.py and tools/semantic_scholar_fetch.py — do not call these tools directly. Results saved to memory/paper-cache/.
---

Invoke skill `skills/geo-lit-review/SKILL.md` for: $ARGUMENTS

The skill calls the appropriate Python tools. Follow these steps:

1. **Query expansion**: Identify the sub-domain (GIScience / Remote Sensing / Geoscience) and expand the query with relevant technical terms (e.g., if query mentions "house prices" + spatial, add "spatial heterogeneity", "GWR", "spatial lag").

2. **Search ArXiv**: Search for papers using the arxiv MCP or WebFetch to query `https://arxiv.org/search/?searchtype=all&query={QUERY}`. Retrieve the top 10 most relevant results.

3. **Search Semantic Scholar**: Use WebFetch to query the Semantic Scholar API for additional papers.

4. **Synthesize results**: For each paper found, extract:
   - Title, authors, year
   - Key method used
   - Main finding (1 sentence)
   - Relevance to the query (1 sentence)

5. **Identify gaps**: After reviewing all papers, identify 2-3 research gaps that could motivate new work.

6. **Output format**:
```markdown
## Literature Search: {QUERY}

### Key Papers Found
| # | Title | Year | Method | Key Finding |
|---|-------|------|--------|------------|
...

### Research Gaps
1. ...
2. ...

### Suggested Next Steps
- ...
```

Save results to `output/lit_search_{timestamp}.md`.
