#!/usr/bin/env bash
# GeoResearchAgent-247 — Stop Hook
# Saves session checkpoint and generates a summary when the agent stops.

set -euo pipefail

CHECKPOINT_DIR="${GEO_AGENT_CHECKPOINT_DIR:-.checkpoints}"
LOG_DIR="${GEO_AGENT_LOG_DIR:-harness/logs}"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID="${GEO_AGENT_SESSION_ID:-session_$(date +%s)}"

mkdir -p "$CHECKPOINT_DIR" "$LOG_DIR"

echo "${TS} | STOP | Session ${SESSION_ID} ended" >> "${LOG_DIR}/sessions.log"

# Copy current output to checkpoint
if [ -d "output" ]; then
    cp -r output "${CHECKPOINT_DIR}/${SESSION_ID}_output" 2>/dev/null || true
fi

# Generate a brief session summary
python3 -c "
import json, os, glob, datetime

summary = {
    'session_id': '${SESSION_ID}',
    'ended_at': '${TS}',
    'files_written': [],
    'experiments_run': 0,
}

# Count output files
for f in glob.glob('output/**/*', recursive=True):
    if os.path.isfile(f):
        summary['files_written'].append(f)

# Read experiment state if available
try:
    with open('experiment_state.json') as f:
        state = json.load(f)
    summary['experiments_run'] = len(state.get('executed_scripts', []))
except:
    pass

# Save summary
summary_path = '${CHECKPOINT_DIR}/${SESSION_ID}_summary.json'
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f'Session summary saved to {summary_path}')
print(f'Files written: {len(summary[\"files_written\"])}')
print(f'Experiments run: {summary[\"experiments_run\"]}')
" 2>/dev/null || echo "Could not generate session summary"

# Send desktop notification (cross-platform)
bash harness/hooks/notification.sh "GeoResearchAgent-247 session ended: ${SESSION_ID}" 2>/dev/null || true

exit 0
