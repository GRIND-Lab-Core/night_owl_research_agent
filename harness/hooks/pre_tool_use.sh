#!/usr/bin/env bash
# GeoResearchAgent-247 — PreToolUse Hook
# Validates tool calls before execution, blocks dangerous patterns, logs intent.

set -euo pipefail

TOOL_INPUT="${1:-}"
LOG_DIR="${GEO_AGENT_LOG_DIR:-harness/logs}"
LOG_FILE="${LOG_DIR}/tool_calls.log"

mkdir -p "$LOG_DIR"

# Timestamp
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Log the tool call
echo "${TS} | PRE | ${TOOL_INPUT:0:200}" >> "$LOG_FILE"

# --- Safety checks ---

# Block destructive rm commands
if echo "$TOOL_INPUT" | grep -qE '"rm\s+-rf|rm -rf\s+/'  ; then
    echo "BLOCKED: Destructive rm -rf command detected" >&2
    exit 1
fi

# Block force push
if echo "$TOOL_INPUT" | grep -qE '"git push.*--force|git push.*-f"'; then
    echo "BLOCKED: Force push requires explicit user confirmation" >&2
    exit 1
fi

# Block writes outside allowed directories
if echo "$TOOL_INPUT" | grep -qE '"path":\s*"(\/etc|\/usr|\/bin|\/sbin|~\/\.ssh|~\/\.aws)"'; then
    echo "BLOCKED: Write to system directory not allowed" >&2
    exit 1
fi

# Warn if writing large data (>100MB)
if echo "$TOOL_INPUT" | grep -qE '"content":.{102400,}'; then
    echo "WARNING: Very large write detected (>100KB). Proceeding..." >&2
fi

# Log success
echo "${TS} | PRE | ALLOWED" >> "$LOG_FILE"
exit 0
