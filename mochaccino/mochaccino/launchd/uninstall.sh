#!/usr/bin/env bash
DEST="$HOME/Library/LaunchAgents/com.appydave.mochaccino.plist"
launchctl unload "$DEST" 2>/dev/null; rm -f "$DEST"; echo "Mochaccino service removed (server stopped)."
