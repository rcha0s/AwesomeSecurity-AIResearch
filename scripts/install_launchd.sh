#!/usr/bin/env bash
# install_launchd.sh - Install (or remove) the Mac fallback scan as a launchd job.
#
# Runs scripts/run_scan_local.sh daily at HOUR:MINUTE local time. Schedule it
# after the cloud routine: the wrapper is idle on days the cloud run succeeded.
#
# macOS privacy rules (TCC) stop a launchd job from reading ~/Desktop,
# ~/Documents or ~/Downloads, so the job runs from its own clone in
# ~/.local/share/awesomesec-runner (with its own .venv), fast-forwarded to
# origin/main before every run. Its log: <runner>/data/_scan.log.
#
#   scripts/install_launchd.sh              # install, daily 09:30
#   scripts/install_launchd.sh 10 15        # install, daily 10:15
#   scripts/install_launchd.sh --uninstall
#   launchctl kickstart -k "gui/$(id -u)/com.rcha0s.awesomesecurity.daily-scan"   # run now
set -euo pipefail
LABEL="com.rcha0s.awesomesecurity.daily-scan"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
RUNNER="${SCAN_RUNNER_HOME:-$HOME/.local/share/awesomesec-runner}"
DOMAIN="gui/$(id -u)"

if [[ "${1:-}" == "--uninstall" ]]; then
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed $LABEL"
  exit 0
fi

HOUR="${1:-9}"
MINUTE="${2:-30}"
if [[ ! -d "$RUNNER/.git" ]]; then
  mkdir -p "$(dirname "$RUNNER")"
  git clone -q "$(git -C "$SRC" remote get-url origin)" "$RUNNER"
fi
git -C "$RUNNER" pull -q --ff-only origin main
# macOS's /usr/bin/python3 is too old for requirements.txt; uv brings 3.12.
rm -rf "$RUNNER/.venv"
uv venv -q --python 3.12 "$RUNNER/.venv"
VIRTUAL_ENV="$RUNNER/.venv" uv pip install -q -r "$RUNNER/requirements.txt"
mkdir -p "$HOME/Library/LaunchAgents" "$RUNNER/data"
# Fast-forward first, so the wrapper itself is main's current version.
# No '&' or '<': this string goes into the plist's XML unescaped.
RUN="cd '$RUNNER' || exit 1; git pull -q --ff-only origin main; exec /bin/bash scripts/run_scan_local.sh"
cat >"$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>-c</string><string>$RUN</string></array>
  <key>WorkingDirectory</key><string>$RUNNER</string>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>$HOUR</integer><key>Minute</key><integer>$MINUTE</integer></dict>
  <key>StandardOutPath</key><string>$RUNNER/data/_scan_launchd.log</string>
  <key>StandardErrorPath</key><string>$RUNNER/data/_scan_launchd.log</string>
</dict>
</plist>
EOF
plutil -lint "$PLIST" >/dev/null
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
echo "Installed $LABEL: daily at $(printf '%02d:%02d' "$HOUR" "$MINUTE"), runs from $RUNNER (logs in its data/)"
