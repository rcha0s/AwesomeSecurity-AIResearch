#!/usr/bin/env bash
# install_launchd.sh - Install (or remove) the Mac fallback scan as a launchd job.
#
# Runs scripts/run_scan_local.sh daily at HOUR:MINUTE local time. Schedule it
# after the cloud routine: the wrapper is idle on days the cloud run succeeded.
#
#   scripts/install_launchd.sh              # install, daily 09:30
#   scripts/install_launchd.sh 10 15        # install, daily 10:15
#   scripts/install_launchd.sh --uninstall
#   launchctl kickstart -k "gui/$(id -u)/com.rcha0s.awesomesecurity.daily-scan"   # run now
set -euo pipefail
LABEL="com.rcha0s.awesomesecurity.daily-scan"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DOMAIN="gui/$(id -u)"

if [[ "${1:-}" == "--uninstall" ]]; then
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed $LABEL"
  exit 0
fi

HOUR="${1:-9}"
MINUTE="${2:-30}"
mkdir -p "$HOME/Library/LaunchAgents" "$REPO/data"
cat >"$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$REPO/scripts/run_scan_local.sh</string></array>
  <key>WorkingDirectory</key><string>$REPO</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>$HOUR</integer><key>Minute</key><integer>$MINUTE</integer></dict>
  <key>StandardOutPath</key><string>$REPO/data/_scan_launchd.log</string>
  <key>StandardErrorPath</key><string>$REPO/data/_scan_launchd.log</string>
</dict>
</plist>
EOF
plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
echo "Installed $LABEL: daily at $(printf '%02d:%02d' "$HOUR" "$MINUTE"), logs in data/_scan_launchd.log"
