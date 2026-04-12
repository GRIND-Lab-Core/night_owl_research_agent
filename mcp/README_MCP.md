# MCP Servers for NORA

Model Context Protocol (MCP) servers extend Claude Code's capabilities with domain-specific tools.

## Configured Servers (`.mcp.json`)

### `filesystem`
Local file system access. Allows Claude to read/write files in the project directory.
- **Package**: `@modelcontextprotocol/server-filesystem`
- **Install**: `npm install -g @modelcontextprotocol/server-filesystem`

### `fetch`
Fetches web content: ArXiv papers, data portal pages, documentation.
- **Package**: `@modelcontextprotocol/server-fetch`
- **Install**: `npm install -g @modelcontextprotocol/server-fetch`

### `geo_mcp` (custom)
Geo-specific tools: GADM boundaries, OSM, Census, CRS suggestions.
- **File**: `mcp/geo_mcp_server.py`
- **Tools**:
  - `get_gadm_boundaries` — download admin boundaries by country + level
  - `get_osm_data` — query OpenStreetMap via Overpass API
  - `search_open_geo_datasets` — curated open data catalog
  - `get_census_data` — US Census ACS variables
  - `get_epsg_info` — CRS metadata lookup
  - `suggest_crs` — recommend projection for area + analysis type

### `arxiv_mcp` (custom)
ArXiv paper search and retrieval.
- **File**: `mcp/arxiv_mcp.py`

### `github`
Read GitHub repositories, issues, and code.
- **Package**: `@modelcontextprotocol/server-github`
- **Requires**: `GITHUB_TOKEN` environment variable

### `brave_search`
Web search for literature and documentation.
- **Package**: `@modelcontextprotocol/server-brave-search`
- **Requires**: `BRAVE_API_KEY` environment variable

---

## Installing MCP Packages

```bash
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-brave-search
```

---

## Adding a Custom MCP Server

1. Create `mcp/your_server.py` implementing the stdio JSON-RPC protocol
2. Add to `.mcp.json`:
```json
{
  "mcpServers": {
    "your_server": {
      "command": "python",
      "args": ["mcp/your_server.py"],
      "env": {"YOUR_API_KEY": "${YOUR_API_KEY}"}
    }
  }
}
```
3. Restart Claude Code to load the new server

---

## Useful MCP Servers for Geo Research

| Server | Purpose | Source |
|--------|---------|--------|
| `filesystem` | File I/O | Official |
| `fetch` | Web scraping | Official |
| `brave-search` | Web search | Official |
| `github` | Code repos | Official |
| `postgres` | Spatial DB | Official (use with PostGIS) |
| `jupyter` | Notebook exec | Community |
| Custom `geo_mcp` | Geo data access | This project |
| Custom `arxiv_mcp` | Literature | This project |
