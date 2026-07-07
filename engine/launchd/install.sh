#!/usr/bin/env bash
# dark-factory auto-wake watcher as a launchd WatchPaths agent.
# Fires wake.py whenever engine/store/queue/ changes. Notification leg is
# active the moment this is loaded; the dispatch leg stays gated behind
# engine/store/WAKE-ARMED (see bin/factory-wake / docs/auto-wake.md) --
# loading this job does NOT arm dispatch.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(cd "$DIR/../.." && pwd)"
LABEL=com.appydave.dark-factory-wake; DEST="$HOME/Library/LaunchAgents/$LABEL.plist"
sed "s|__APP_ROOT__|$ROOT|g" "$DIR/$LABEL.plist" > "$DEST"
launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"
echo "Loaded $LABEL — watching $ROOT/engine/store/{queue,done} for changes."
echo "Dispatch is DISARMED by default. Arm with: bin/factory-wake arm"
echo "Uninstall: engine/launchd/uninstall.sh"
