#!/usr/bin/env python3
"""
ArXiv paper fetch utility.

Called by skills (geo-lit-review, novelty-check) when they need to search for papers.
Agents decide when to call this tool — it is not called automatically.

Usage:
    python tools/arxiv_fetch.py --query "GWR spatial non-stationarity" --max-results 30
    python tools/arxiv_fetch.py --query "flood mapping SAR deep learning" --output memory/paper-cache/flood_arxiv.json
    python tools/arxiv_fetch.py --ids "2310.18660,2309.16020" --output memory/paper-cache/seeds.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ARXIV_API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch_by_query(query: str, max_results: int = 30, start: int = 0) -> list[dict]:
    params = urllib.parse.urlencode({
        "search_query": f"all:{query}",
        "max_results": max_results,
        "start": start,
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        xml_data = resp.read()
    return _parse_feed(xml_data)


def fetch_by_ids(ids: list[str]) -> list[dict]:
    id_str = ",".join(ids)
    params = urllib.parse.urlencode({"id_list": id_str})
    url = f"{ARXIV_API}?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        xml_data = resp.read()
    return _parse_feed(xml_data)


def _parse_feed(xml_data: bytes) -> list[dict]:
    root = ET.fromstring(xml_data)
    papers = []
    for entry in root.findall("atom:entry", NS):
        arxiv_id_raw = entry.findtext("atom:id", default="", namespaces=NS)
        arxiv_id = arxiv_id_raw.split("/abs/")[-1].strip()

        title = (entry.findtext("atom:title", default="", namespaces=NS) or "").strip().replace("\n", " ")
        abstract = (entry.findtext("atom:summary", default="", namespaces=NS) or "").strip().replace("\n", " ")
        published = (entry.findtext("atom:published", default="", namespaces=NS) or "")[:4]

        authors = [
            a.findtext("atom:name", default="", namespaces=NS)
            for a in entry.findall("atom:author", NS)
        ]

        categories = [
            c.get("term", "")
            for c in entry.findall("atom:category", NS)
        ]

        doi_el = entry.find("arxiv:doi", NS)
        doi = doi_el.text.strip() if doi_el is not None and doi_el.text else None

        papers.append({
            "id": f"arxiv:{arxiv_id}",
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "year": int(published) if published.isdigit() else None,
            "abstract": abstract[:320],  # truncate to ~80 tokens
            "abstract_full": abstract,
            "venue": "arXiv",
            "categories": categories,
            "doi": doi,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "citation_count": None,
            "priority_venue": False,
            "source": "arxiv",
        })
    return papers


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch papers from ArXiv")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="Search query string")
    group.add_argument("--ids", help="Comma-separated arXiv IDs")

    parser.add_argument("--max-results", type=int, default=30)
    parser.add_argument("--output", help="JSON output path (default: stdout)")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep seconds between requests")
    args = parser.parse_args()

    try:
        if args.query:
            papers = fetch_by_query(args.query, max_results=args.max_results)
        else:
            ids = [i.strip() for i in args.ids.split(",")]
            papers = fetch_by_ids(ids)
    except Exception as exc:
        print(f"Error fetching from ArXiv: {exc}", file=sys.stderr)
        sys.exit(1)

    result = {
        "source": "arxiv",
        "query": args.query or args.ids,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(papers),
        "papers": papers,
    }

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Saved {len(papers)} papers → {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    time.sleep(args.sleep)


if __name__ == "__main__":
    main()
