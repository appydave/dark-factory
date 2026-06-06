# AngelEye refresh — promote to first-class session/work telemetry sentinel

**Raised**: 2026-06-06 (David — "research AngelEye, maybe a first-class tool"). **Status**: open.
**Decision (from research)**: adopt AngelEye as the **Claude Code session/work telemetry sentinel** — complementary to Switchboard (resource/process). Both feed Watchtower. See memory `angeleye-telemetry-sentinel`.

## Role in the factory
- **AngelEye** answers *"what is each Swagger doing — active / stalled / failed, and what kind of work?"* (semantic liveness + classification). Direct fit for dispatch-loop robustness (the comms/return failure modes).
- **Switchboard** answers *"per-process RAM/CPU, open-Swagger count"* (resource health — the 60GB question, the leaks/shutdown failure modes). AngelEye has **zero** resource data — do NOT use it for that.

## What needs doing (it's built but ~3-4 weeks stale, not running)
1. **Fix the Claude Code version-compat blocker** — hook HTTP transport broke at v2.1.89 (latest commit `935bc2e` "reject HTTP transport — SessionStart drops"). Until fixed, **live ingestion is dead** (transcript backfill still works, but real-time is the point for the loop). This is the gating task.
2. **Daemonize it (no manual start)** — David's core pain with AngelEye is having to manually turn on the web UI just to get file-watching. Give it a daemon (launchd LaunchAgent, like Switchboard's `register-as-launchd`) so it's auto-running whenever the machine is on. A Sentinel you have to remember to start isn't a Sentinel. Then `POST /api/sync?force=true` to reclassify stale data (last write May 13, 154MB).
3. **Add a dark-factory classification overlay** (`server/src/config/overlays/`) so it classifies Marshall/Swagger sessions by role — documented extension, no code change.
4. **Add pruning** — data dir grows unbounded (154MB now, 222MB peak); startup backfill scans all JSONL.
5. **(Later) MCP surface** — not built; would let Marshall query session health as a tool. Or Marshall reads `registry.json` directly (simpler).
6. **(Later) feed Watchtower** alongside Switchboard's resource snapshots.

## Done when
- Live hook ingestion works against current Claude Code (version-compat fixed).
- Marshall can see, per Swagger: active/warm/idle/stalled + work-type, without babysitting.
- Runs as a per-machine sentinel (pairs with Switchboard; both → Watchtower).
