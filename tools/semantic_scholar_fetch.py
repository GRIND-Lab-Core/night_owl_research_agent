#!/usr/bin/env python3
"""
Semantic Scholar paper fetch utility.

Called by skills (geo-lit-review, novelty-check) when they need citation metadata.
Agents decide when and how to call this tool.

Usage:
    python tools/semantic_scholar_fetch.py --query "geographically weighted regression urban heat"
    python tools/semantic_scholar_fetch.py --query "MGWR spatial non-stationarity" --max-results 50 --output memory/paper-cache/mgwr_s2.json
    python tools/semantic_scholar_fetch.py --paper-id "10.1080/13658816.2019.1684500"

Set SEMANTIC_SCHOLAR_KEY environment variable for higher rate limits (100 req/min vs 1 req/s).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


S2_BASE = "https://api.semanticscholar.org/graph/v1"

DEFAULT_FIELDS = (
    "title,authors,year,abstract,venue,citationCount,"
    "externalIds,fieldsOfStudy,openAccessPdf,publicationDate"
)

# Priority venues for geo/RS/GIScience — papers from these get priority_venue=True
PRIORITY_VENUES = {
    "international journal of geographical information science",
    "remote sensing of environment",
    "isprs journal of photogrammetry and remote sensing",
    "ieee transactions on geoscience and remote sensing",
    "annals of the american association of geographers",
    "computers, environment and urban systems",
    "transactions in gis",
    "geophysical research letters",
    "environmental health perspectives",
    "nature communications",
    "nature geoscience",
    "international journal of digital earth",
    "annals of gis",
    "international journal of applied earth observation and geoinformation",
}


def _make_request(url: str, api_key: str | None = None) -> dict:
    headers: dict[str, str] = {"Accept": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.reason} — {url}") from e


def search_papers(
    query: str,
    fields: str = DEFAULT_FIELDS,
    max_results: int = 50,
    year_start: int = 2015,
    api_key: str | None = None,
) -> list[dict]:
    params = urllib.parse.urlencode({
        "query": query,
        "fields": fields,
        "limit": min(max_results, 100),
    })
    url = f"{S2_BASE}/paper/search?{params}"
    data = _make_request(url, api_key)
    papers = data.get("data", [])
    return [_normalize(p) for p in papers if _year_ok(p, year_start)]


def fetch_paper(paper_id: str, fields: str = DEFAULT_FIELDS, api_key: str | None = None) -> dict:
    """Fetch a single paper by S2 ID, DOI, or arXiv ID."""
    url = f"{S2_BASE}/paper/{urllib.parse.quote(paper_id, safe='')}?fields={fields}"
    data = _make_request(url, api_key)
    return _normalize(data)


def _year_ok(paper: dict, year_start: int) -> bool:
    year = paper.get("year")
    return year is None or year >= year_start


def _normalize(p: dict) -> dict:
    ext = p.get("externalIds") or {}
    doi = ext.get("DOI")
    arxiv_id = ext.get("ArXiv")

    if doi:
        pid = f"doi:{doi}"
    elif arxiv_id:
        pid = f"arxiv:{arxiv_id}"
    else:
        pid = f"s2:{p.get('paperId', 'unknown')}"

    venue = (p.get("venue") or "").strip()
    priority = venue.lower() in PRIORITY_VENUES

    abstract = (p.get("abstract") or "").replace("\n", " ")

    oa = p.get("openAccessPdf") or {}
    pdf_url = oa.get("url")

    return {
        "id": pid,
        "s2_id": p.get("paperId"),
        "title": (p.get("title") or "").strip(),
        "authors": [a.get("name", "") for a in (p.get("authors") or [])],
        "year": p.get("year"),
        "abstract": abstract[:320],
        "abstract_full": abstract,
        "venue": venue,
        "citation_count": p.get("citationCount", 0),
        "doi": doi,
        "arxiv_id": arxiv_id,
        "url": pdf_url or (f"https://doi.org/{doi}" if doi else f"https://www.semanticscholar.org/paper/{p.get('paperId', '')}"),
        "fields_of_study": p.get("fieldsOfStudy") or [],
        "priority_venue": priority,
        "source": "semantic_scholar",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch papers from Semantic Scholar")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="Search query")
    group.add_argument("--paper-id", help="S2 paper ID, DOI, or arXiv ID")

    parser.add_argument("--fields", default=DEFAULT_FIELDS)
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--year-start", type=int, default=2015)
    parser.add_argument("--output", help="JSON output path (default: stdout)")
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()

    api_key = os.environ.get("SEMANTIC_SCHOLAR_KEY")
    if api_key:
        print(f"Using Semantic Scholar API key (higher rate limits)", file=sys.stderr)

    try:
        if args.query:
            papers = search_papers(
                args.query,
                fields=args.fields,
                max_results=args.max_results,
                year_start=args.year_start,
                api_key=api_key,
            )
        else:
            papers = [fetch_paper(args.paper_id, fields=args.fields, api_key=api_key)]
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    result = {
        "source": "semantic_scholar",
        "query": args.query or args.paper_id,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(papers),
        "priority_venue_count": sum(1 for p in papers if p["priority_venue"]),
        "papers": papers,
    }

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Saved {len(papers)} papers ({result['priority_venue_count']} priority venues) → {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    time.sleep(args.sleep)


if __name__ == "__main__":
    main()
