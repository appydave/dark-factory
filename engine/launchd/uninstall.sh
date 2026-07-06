#!/usr/bin/env bash
DEST="$HOME/Library/LaunchAgents/com.appydave.dark-factory-wake.plist"
launchctl unload "$DEST" 2>/dev/null; rm -f "$DEST"; echo "dark-factory-wake watcher removed."
