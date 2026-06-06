#!/usr/bin/env bash
# constellation-status.sh — Marshall PREFLIGHT: are the Dark Factory apps UP?
#
# David's rule (2026-06-06): Marshall should NOT operate blind. The constellation
# apps are meant to be turned on. A REQUIRED app being down must be surfaced
# BOLDLY — not discovered hours later (we lost a whole session's AngelEye
# telemetry because nothing told us it was off).
#
# Run this on Marshall activation ("be marshall") and before any dispatch.
# Exit 0 = safe to operate. Exit 1 = a required app is DOWN (warn David loudly).
set -uo pipefail

req_down=0
line() { printf '  %-13s %-6s %s\n' "$1" "$2" "$3"; }

echo "🏭 Dark Factory — constellation preflight"
echo "──────────────────────────────────────────────"

# Switchboard (REQUIRED) — the comms bus.
# Process-managed-and-running is the strong signal; health is a softer confirm
# (a tight-timeout health curl gave false DOWN under load — don't cry wolf).
# NB: capture-then-test, not `| grep -q` — grep -q closes the pipe early and
# launchctl gets SIGPIPE, which under `set -o pipefail` reads as a false DOWN.
sb_running=$(launchctl list 2>/dev/null | grep com.appydave.switchboard || true)
if [ -n "$sb_running" ]; then
  if curl -s --max-time 5 http://127.0.0.1:5099/health >/dev/null 2>&1; then
    line "Switchboard" "UP" "comms bus :5099/:5100 (launchd, healthy)"
  else
    line "Switchboard" "WARN" "process up (launchd) but :5099/health not responding — check"
  fi
else
  line "Switchboard" "DOWN" "REQUIRED — start: cd ~/dev/ad/apps/switchboard && ./scripts/install-service.sh"
  req_down=1
fi

# AngelEye (REQUIRED) — session telemetry (load-bearing for the reaper)
if lsof -nP -iTCP:5051 -sTCP:LISTEN >/dev/null 2>&1; then
  line "AngelEye" "UP" "session telemetry :5051"
else
  line "AngelEye" "DOWN" "REQUIRED — start: cd ~/dev/ad/apps/angeleye && bash scripts/start.sh"
  req_down=1
fi

# Watchtower board (optional) — the visual surface
if lsof -nP -iTCP:7430 -sTCP:LISTEN >/dev/null 2>&1; then
  line "Watchtower" "UP" "board :7430"
else
  line "Watchtower" "down" "optional — board :7430 (node experiments/watchtower-board/server.mjs)"
fi

# AppyCtrl (optional, not yet wired) — resource health across Tailscale
line "AppyCtrl" "?" "resource health — investigate/wire (TBD)"

echo "──────────────────────────────────────────────"
if [ "$req_down" -ne 0 ]; then
  echo "⛔ A REQUIRED app is DOWN. Marshall must NOT operate blind."
  echo "   → Surface this to David BOLDLY and start the missing app before dispatching."
  exit 1
fi
echo "✅ Required apps (Switchboard + AngelEye) are UP — safe to operate."
exit 0
