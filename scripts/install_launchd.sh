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

# Optional, opt-in: the X list collector (scripts/ingest_x_list.py --collect), every
# 3 hours, from the runner clone. A background tab loads only 5 to 10 posts per
# read, so one read per day would miss most of a 24h window; each run upserts into
# data/_x_list_seen.json (48h) and the daily scan merges it. Local Mac only, read-only,
# never activates the tab. Needs the runner clone (install the daily job first).
#   scripts/install_launchd.sh --xlist            # install
#   scripts/install_launchd.sh --uninstall-xlist  # remove
XLABEL="com.rcha0s.awesomesecurity.xlist"
XPLIST="$HOME/Library/LaunchAgents/$XLABEL.plist"
if [[ "${1:-}" == "--uninstall-xlist" ]]; then
  launchctl bootout "$DOMAIN/$XLABEL" 2>/dev/null || true
  rm -f "$XPLIST"
  echo "Removed $XLABEL"
  exit 0
fi
if [[ "${1:-}" == "--xlist" ]]; then
  if [[ "$RUNNER" == *[\'\&\<\>]* || ! -d "$RUNNER/.git" ]]; then
    echo "install_launchd: install the daily job first (runner clone missing or unsafe path)" >&2
    exit 1
  fi
  mkdir -p "$HOME/Library/LaunchAgents" "$RUNNER/data"
  XRUN="cd '$RUNNER' || exit 1; export PATH=\"\$PATH:/opt/homebrew/bin:/usr/local/bin:\$HOME/.local/bin\" SCAN_RUNNER=local; git fetch -q origin main; git reset -q --hard origin/main; .venv/bin/python scripts/ingest_x_list.py --collect 2>&1 | sed 's/^/[x-list] /' >> data/_scan.log"
  NEW="$XPLIST.new"
  cat >"$NEW" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$XLABEL</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>-c</string><string>$XRUN</string></array>
  <key>WorkingDirectory</key><string>$RUNNER</string>
  <key>StartInterval</key><integer>10800</integer>
  <key>StandardOutPath</key><string>$RUNNER/data/_scan_launchd.log</string>
  <key>StandardErrorPath</key><string>$RUNNER/data/_scan_launchd.log</string>
</dict>
</plist>
EOF
  plutil -lint "$NEW" >/dev/null
  mv "$NEW" "$XPLIST"
  launchctl bootout "$DOMAIN/$XLABEL" 2>/dev/null || true
  launchctl bootstrap "$DOMAIN" "$XPLIST"
  echo "Installed $XLABEL: every 3 hours, logs [x-list] lines to $RUNNER/data/_scan.log"
  exit 0
fi

if [[ "${1:-}" == "--uninstall" ]]; then
  launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed $LABEL"
  exit 0
fi

HOUR="${1:-9}"
MINUTE="${2:-30}"
# The path goes into XML and a single-quoted shell string unescaped.
if [[ "$RUNNER" == *[\'\&\<\>]* ]]; then
  echo "install_launchd: runner path can't contain ' & < >: $RUNNER" >&2
  exit 1
fi
if [[ ! -d "$RUNNER/.git" ]]; then
  mkdir -p "$(dirname "$RUNNER")"
  git clone -q "$(git -C "$SRC" remote get-url origin)" "$RUNNER"
fi
# Machine-owned clone: always match main, even if it diverged.
git -C "$RUNNER" fetch -q origin main
git -C "$RUNNER" reset -q --hard origin/main
# macOS's /usr/bin/python3 is too old for requirements.txt; uv brings 3.12.
# Built aside and swapped in only once it works, so a failed re-install
# leaves the scheduled job its old venv.
rm -rf "$RUNNER/.venv.new"
uv venv -q --python 3.12 "$RUNNER/.venv.new"
VIRTUAL_ENV="$RUNNER/.venv.new" uv pip install -q -r "$RUNNER/requirements.txt"
rm -rf "$RUNNER/.venv"
mv "$RUNNER/.venv.new" "$RUNNER/.venv"
mkdir -p "$HOME/Library/LaunchAgents" "$RUNNER/data"
# Match main first, so the wrapper itself is main's current version. If that
# fails (offline), the wrapper's own fetch fails too and raises the alert.
RUN="cd '$RUNNER' || exit 1; git fetch -q origin main; git reset -q --hard origin/main; exec /bin/bash scripts/run_scan_local.sh"
NEW="$PLIST.new"
cat >"$NEW" <<EOF
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
plutil -lint "$NEW" >/dev/null
mv "$NEW" "$PLIST"
launchctl bootout "$DOMAIN/$LABEL" 2>/dev/null || true
launchctl bootstrap "$DOMAIN" "$PLIST"
echo "Installed $LABEL: daily at $(printf '%02d:%02d' "$HOUR" "$MINUTE"), runs from $RUNNER (logs in its data/)"
