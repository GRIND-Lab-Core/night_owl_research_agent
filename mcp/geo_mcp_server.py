"""
NORA Custom MCP Server
Provides geo-specific tools: GADM boundaries, OSM data, Census access, GEE queries.

This implements the Model Context Protocol (MCP) server spec.
Run: python mcp/geo_mcp_server.py

Compatible with Claude Code's MCP integration (.mcp.json).
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Any

# MCP server using stdio transport
# Follows the MCP specification: https://modelcontextprotocol.io


def send_response(response: dict) -> None:
    """Write a JSON-RPC response to stdout."""
    print(json.dumps(response), flush=True)


def handle_list_tools() -> list[dict]:
    """Return the list of tools this MCP server provides."""
    return [
        {
            "name": "get_gadm_boundaries",
            "description": "Download GADM administrative boundaries for a country. Returns GeoJSON.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "country_code": {"type": "string", "description": "ISO 3166-1 alpha-3 country code (e.g. 'USA', 'CHN', 'GBR')"},
                    "level": {"type": "integer", "description": "Admin level: 0=country, 1=state, 2=county", "default": 1},
                },
                "required": ["country_code"],
            },
        },
        {
            "name": "get_osm_data",
            "description": "Fetch OpenStreetMap data using Overpass API. Returns GeoJSON.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Overpass QL query"},
                    "bbox": {"type": "string", "description": "Bounding box: 'south,west,north,east' (WGS84)"},
                },
                "required": ["query"],
            },
        },
        {
            "name": "search_open_geo_datasets",
            "description": "Search for open geospatial datasets by topic and geographic area.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Dataset topic (e.g. 'land cover', 'elevation', 'population')"},
                    "region": {"type": "string", "description": "Geographic region (e.g. 'United States', 'Europe', 'global')"},
                    "format": {"type": "string", "description": "Preferred format: 'raster', 'vector', 'tabular'", "default": "any"},
                },
                "required": ["topic"],
            },
        },
        {
            "name": "get_census_data",
            "description": "Fetch US Census American Community Survey (ACS) data via Census API.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "variables": {"type": "array", "items": {"type": "string"}, "description": "ACS variable codes (e.g. ['B01003_001E', 'B19013_001E'])"},
                    "geography": {"type": "string", "description": "Geographic level: 'county', 'tract', 'state'", "default": "county"},
                    "state": {"type": "string", "description": "State FIPS code (e.g. '06' for California). Optional."},
                    "year": {"type": "integer", "description": "ACS year (2019-2022)", "default": 2022},
                },
                "required": ["variables"],
            },
        },
        {
            "name": "get_epsg_info",
            "description": "Get information about a coordinate reference system (CRS) by EPSG code.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "epsg_code": {"type": "integer", "description": "EPSG code (e.g. 4326, 3857, 32618)"},
                },
                "required": ["epsg_code"],
            },
        },
        {
            "name": "suggest_crs",
            "description": "Suggest the appropriate CRS for a geographic area and analysis type.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "country": {"type": "string", "description": "Country name"},
                    "analysis_type": {"type": "string", "description": "Type of analysis: 'area', 'distance', 'web_display', 'global'"},
                    "lat": {"type": "number", "description": "Approximate latitude of study area center"},
                    "lon": {"type": "number", "description": "Approximate longitude of study area center"},
                },
            },
        },
    ]


def handle_call_tool(name: str, arguments: dict[str, Any]) -> Any:
    """Execute a tool call and return the result."""

    if name == "get_gadm_boundaries":
        return _get_gadm_boundaries(**arguments)
    elif name == "get_osm_data":
        return _get_osm_data(**arguments)
    elif name == "search_open_geo_datasets":
        return _search_open_geo_datasets(**arguments)
    elif name == "get_census_data":
        return _get_census_data(**arguments)
    elif name == "get_epsg_info":
        return _get_epsg_info(**arguments)
    elif name == "suggest_crs":
        return _suggest_crs(**arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


def _get_gadm_boundaries(country_code: str, level: int = 1) -> dict:
    """Download GADM boundaries from geoBoundaries (open license alternative to GADM)."""
    url = f"https://www.geoboundaries.org/api/current/gbOpen/{country_code}/ADM{level}/"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
        return {
            "status": "success",
            "country": country_code,
            "level": level,
            "download_url": data.get("gjDownloadURL", ""),
            "source": "geoBoundaries (open license)",
            "note": f"Download GeoJSON from: {data.get('gjDownloadURL', 'N/A')}",
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "fallback": f"Try: https://gadm.org/download_country.html"}


def _get_osm_data(query: str, bbox: str = "") -> dict:
    """Fetch OSM data via Overpass API."""
    overpass_url = os.getenv("OVERPASS_API_URL", "https://overpass-api.de/api/interpreter")
    if bbox and "[bbox" not in query:
        query = query.replace("[out:json]", f"[out:json][bbox:{bbox}]")

    try:
        data = urllib.parse.urlencode({"data": query}).encode()
        req = urllib.request.Request(overpass_url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        n_elements = len(result.get("elements", []))
        return {
            "status": "success",
            "n_elements": n_elements,
            "elements_preview": result.get("elements", [])[:5],
            "note": f"Retrieved {n_elements} OSM elements. Full result available at Overpass Turbo.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "tip": "Try simplifying the query or adding a bounding box to limit the response size.",
        }


def _search_open_geo_datasets(topic: str, region: str = "global", format: str = "any") -> dict:
    """Return curated list of open geo datasets matching the topic."""
    # Curated dataset index
    datasets = {
        "land cover": [
            {"name": "ESA WorldCover 2021", "resolution": "10m", "url": "https://worldcover2021.esa.int/", "format": "raster"},
            {"name": "NLCD 2021 (USA)", "resolution": "30m", "url": "https://www.mrlc.gov/", "format": "raster"},
            {"name": "Copernicus Global Land Cover", "resolution": "100m", "url": "https://lcviewer.vito.be/", "format": "raster"},
        ],
        "elevation": [
            {"name": "SRTM 1 Arc-Second", "resolution": "30m", "url": "https://earthexplorer.usgs.gov/", "format": "raster"},
            {"name": "Copernicus DEM GLO-30", "resolution": "30m", "url": "https://doi.org/10.5270/ESA-c5d3d65", "format": "raster"},
            {"name": "ALOS World 3D", "resolution": "30m", "url": "https://www.eorc.jaxa.jp/ALOS/en/aw3d30/", "format": "raster"},
        ],
        "population": [
            {"name": "WorldPop 2020", "resolution": "100m/1km", "url": "https://www.worldpop.org/", "format": "raster"},
            {"name": "LandScan HD", "resolution": "90m", "url": "https://landscan.ornl.gov/", "format": "raster"},
            {"name": "US Census ACS", "resolution": "tract/county", "url": "https://data.census.gov/", "format": "tabular"},
        ],
        "climate": [
            {"name": "ERA5 Reanalysis", "resolution": "0.25°", "url": "https://cds.climate.copernicus.eu/", "format": "raster"},
            {"name": "CHELSA Climatologies", "resolution": "30 arcsec (~1km)", "url": "https://chelsa-climate.org/", "format": "raster"},
            {"name": "WorldClim 2.1", "resolution": "30 arcsec – 10 arcmin", "url": "https://worldclim.org/", "format": "raster"},
        ],
        "air quality": [
            {"name": "EPA AQS (USA)", "resolution": "station", "url": "https://aqs.epa.gov/aqsweb/documents/data_api.html", "format": "tabular"},
            {"name": "OpenAQ", "resolution": "station/global", "url": "https://openaq.org/", "format": "tabular"},
            {"name": "Copernicus Atmosphere Monitoring (CAMS)", "resolution": "0.1°", "url": "https://atmosphere.copernicus.eu/", "format": "raster"},
        ],
    }

    matches = []
    topic_lower = topic.lower()
    for key, ds_list in datasets.items():
        if key in topic_lower or topic_lower in key:
            matches.extend(ds_list)

    if not matches:
        matches = [{"name": f"No curated datasets for '{topic}'", "note": "Try searching: https://opendatasoft.com or https://earthdata.nasa.gov/"}]

    return {"status": "success", "topic": topic, "region": region, "datasets": matches}


def _get_census_data(variables: list[str], geography: str = "county", state: str = "", year: int = 2022) -> dict:
    """Fetch US Census ACS data."""
    api_key = os.getenv("CENSUS_API_KEY", "")
    base_url = f"https://api.census.gov/data/{year}/acs/acs5"

    vars_str = ",".join(["NAME"] + variables)
    if geography == "county":
        geo_str = "county:*"
        if state:
            geo_str = f"county:*&in=state:{state}"
    elif geography == "tract":
        geo_str = f"tract:*&in=state:{state or '*'}"
    else:
        geo_str = "state:*"

    url = f"{base_url}?get={vars_str}&for={geo_str}"
    if api_key:
        url += f"&key={api_key}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        headers = data[0]
        rows = data[1:6]  # preview first 5 rows
        return {
            "status": "success",
            "url": url,
            "variables": variables,
            "geography": geography,
            "year": year,
            "columns": headers,
            "preview_rows": rows,
            "total_rows": len(data) - 1,
            "note": "Use pandas.read_json() or requests to download the full dataset.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "url": url,
            "tip": "Get a free Census API key at: https://api.census.gov/data/key_signup.html",
        }


def _get_epsg_info(epsg_code: int) -> dict:
    """Return CRS info for an EPSG code."""
    common_crs = {
        4326: {"name": "WGS 84", "type": "Geographic", "units": "degrees", "use": "Global GPS/lat-lon data"},
        3857: {"name": "Web Mercator", "type": "Projected", "units": "meters", "use": "Web maps (Google Maps, OpenStreetMap)"},
        5070: {"name": "NAD83 / Conus Albers", "type": "Projected", "units": "meters", "use": "Continental US area calculations"},
        3035: {"name": "ETRS89-LAEA Europe", "type": "Projected", "units": "meters", "use": "European area calculations"},
        4269: {"name": "NAD83", "type": "Geographic", "units": "degrees", "use": "North America data"},
        32618: {"name": "WGS 84 / UTM zone 18N", "type": "Projected", "units": "meters", "use": "Eastern US local analysis"},
    }
    info = common_crs.get(epsg_code, {"name": f"EPSG:{epsg_code}", "note": "Look up at https://epsg.io/"})
    info["epsg_code"] = epsg_code
    info["epsg_io_url"] = f"https://epsg.io/{epsg_code}"
    return info


def _suggest_crs(country: str = "", analysis_type: str = "area", lat: float = 0, lon: float = 0) -> dict:
    """Suggest appropriate CRS based on location and analysis type."""
    suggestions = []

    if analysis_type == "web_display":
        suggestions.append({"epsg": 3857, "name": "Web Mercator", "reason": "Standard for web map display"})
    elif analysis_type == "global":
        suggestions.append({"epsg": 4326, "name": "WGS 84", "reason": "Standard for global datasets"})
    elif "united states" in country.lower() or "usa" in country.lower():
        suggestions.append({"epsg": 5070, "name": "NAD83/Conus Albers", "reason": "Equal-area for continental US analysis"})
        suggestions.append({"epsg": 4269, "name": "NAD83", "reason": "US geographic coordinates"})
    elif "europe" in country.lower():
        suggestions.append({"epsg": 3035, "name": "ETRS89-LAEA Europe", "reason": "Equal-area for European analysis"})
    else:
        # Suggest UTM zone based on lon
        utm_zone = int((lon + 180) / 6) + 1
        hemisphere = "N" if lat >= 0 else "S"
        utm_epsg = 32600 + utm_zone if lat >= 0 else 32700 + utm_zone
        suggestions.append({
            "epsg": utm_epsg,
            "name": f"WGS 84 / UTM zone {utm_zone}{hemisphere}",
            "reason": "Appropriate UTM zone for local/regional analysis",
        })
        suggestions.append({"epsg": 4326, "name": "WGS 84", "reason": "For data storage and interchange"})

    return {"status": "success", "suggestions": suggestions, "tip": "For area/distance analysis, always use a projected CRS"}


def main() -> None:
    """Run as stdio MCP server."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            method = request.get("method")
            req_id = request.get("id")
            params = request.get("params", {})

            if method == "initialize":
                send_response({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "geo_mcp", "version": "247.0"},
                    },
                })
            elif method == "tools/list":
                send_response({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {"tools": handle_list_tools()},
                })
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = handle_call_tool(tool_name, arguments)
                send_response({
                    "jsonrpc": "2.0", "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
                })
            else:
                send_response({"jsonrpc": "2.0", "id": req_id, "result": {}})

        except Exception as e:
            send_response({
                "jsonrpc": "2.0", "id": request.get("id") if "request" in dir() else None,
                "error": {"code": -32603, "message": str(e)},
            })


if __name__ == "__main__":
    main()
