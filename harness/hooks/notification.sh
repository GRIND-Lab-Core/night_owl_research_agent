#!/usr/bin/env bash
# GeoResearchAgent-247 — Notification Hook
# Sends desktop/Slack/email notifications for long-running task completion.

MESSAGE="${1:-GeoResearchAgent-247: Task complete}"

# --- Desktop notification ---

# macOS
if command -v osascript &>/dev/null; then
    osascript -e "display notification \"${MESSAGE}\" with title \"GeoResearchAgent-247\"" 2>/dev/null || true

# Linux (notify-send)
elif command -v notify-send &>/dev/null; then
    notify-send "GeoResearchAgent-247" "${MESSAGE}" 2>/dev/null || true

# Windows (PowerShell via WSL or Git Bash)
elif command -v powershell.exe &>/dev/null; then
    powershell.exe -Command "
Add-Type -AssemblyName System.Windows.Forms
\$notification = New-Object System.Windows.Forms.NotifyIcon
\$notification.Icon = [System.Drawing.SystemIcons]::Information
\$notification.BalloonTipTitle = 'GeoResearchAgent-247'
\$notification.BalloonTipText = '${MESSAGE}'
\$notification.Visible = \$true
\$notification.ShowBalloonTip(5000)
" 2>/dev/null || true
fi

# --- Slack notification (optional) ---
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"
if [ -n "$SLACK_WEBHOOK" ]; then
    curl -s -X POST "$SLACK_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \":satellite: GeoResearchAgent-247: ${MESSAGE}\"}" \
        2>/dev/null || true
fi

# --- Email notification (optional) ---
EMAIL_TO="${GEO_AGENT_EMAIL:-}"
if [ -n "$EMAIL_TO" ] && command -v mail &>/dev/null; then
    echo "${MESSAGE}" | mail -s "GeoResearchAgent-247 Notification" "$EMAIL_TO" 2>/dev/null || true
fi

exit 0
