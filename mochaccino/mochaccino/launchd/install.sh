#!/usr/bin/env bash
# Mochaccino gallery as a KeepAlive launchd service (mode 2: always-on server).
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(cd "$DIR/.." && pwd)"
LABEL=com.appydave.mochaccino; DEST="$HOME/Library/LaunchAgents/$LABEL.plist"
lsof -ti :7420 | xargs kill -9 2>/dev/null || true   # clear any bare nohup instance
sed "s|__APP_ROOT__|$ROOT|g" "$DIR/$LABEL.plist" > "$DEST"
launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"
echo "Loaded $LABEL — :7420 always-on, auto-restarts. Uninstall: launchd/uninstall.sh"
