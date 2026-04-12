#!/usr/bin/env bash
# NORA — PostToolUse Hook
# Updates experiment state after tool execution; caches written files.

set -euo pipefail

TOOL_INPUT="${1:-}"
TOOL_RESPONSE="${2:-}"
LOG_DIR="${GEO_AGENT_LOG_DIR:-harness/logs}"
STATE_FILE="experiment_state.json"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

mkdir -p "$LOG_DIR"

# Log the tool response (truncated)
echo "${TS} | POST | INPUT=${TOOL_INPUT:0:100} | RESPONSE=${TOOL_RESPONSE:0:100}" >> "${LOG_DIR}/tool_calls.log"

# Update experiment state if a Python script was executed successfully
if echo "$TOOL_INPUT" | grep -qE '"command".*python'; then
    if echo "$TOOL_RESPONSE" | grep -qi '"status".*success\|returncode.*0'; then
        # Update state file
        if [ -f "$STATE_FILE" ]; then
            python3 -c "
import json, sys, datetime
try:
    with open('$STATE_FILE') as f:
        state = json.load(f)
except:
    state = {}
state.setdefault('executed_scripts', [])
state['executed_scripts'].append({'ts': '$TS', 'input': '${TOOL_INPUT:0:100}'})
state['last_updated'] = '$TS'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
" 2>/dev/null || true
        fi
    fi
fi

# If a file was written to output/, log it
if echo "$TOOL_INPUT" | grep -qE '"file_path".*output/'; then
    WRITTEN_FILE=$(echo "$TOOL_INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null || echo "unknown")
    echo "${TS} | FILE_WRITTEN | ${WRITTEN_FILE}" >> "${LOG_DIR}/file_writes.log"
fi

exit 0
