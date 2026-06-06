# Reaper live-fire — finding (2026-06-06)

**Goal:** prove the auto-reaper end-to-end — Switchboard staleness-detector emits `session.stale` → Marshall's Monitor reaps the stranded Swagger window.

**Method:** lowered the detector threshold reversibly (`STALE_MINUTES=1`, `STALE_CHECK_MS=10000` via the installed launchd plist + `bootout`/`bootstrap` reload — `kickstart` alone reuses the cached job def and does NOT re-read an edited plist), stranded one idle Swagger (`swagger-staletest`, empty queue), armed a Marshall Monitor on `?subscribe=session.stale` that reaps by window name.

**Result: NO reap. The detector is broken — not merely unproven.**

**Root cause — process-tree detection is a dead end under Claude Code v2.x.** The detector finds a window's claude session by BFS from the tmux **pane pid**. But the interactive `claude` session is **reparented to the claude daemon** (`claude daemon run`, PPID 1) — it is NOT in the pane's subtree. The pane's only children are the **MCP servers** claude spawned (`codex`, `playwright-mcp`, `brave-search-mcp`, `chrome-devtools-mcp`, `notebooklm`, `blackboard`). So `findClaudeDescendant(panePid)` returns nothing → `etime > threshold` never evaluated → no `session.stale` → nothing to reap. Reading the code looked correct; only the live test exposed it.

**Redesign — two process-INDEPENDENT signals:**
- **(a) Engine-state reaper (common orphan: finished but window still open):** a `swagger-<slug>` window whose ticket handback has landed in `reports/`/`done/`, still open after a grace window → reap. Uses the engine's own source of truth; zero process detection. Covers the orphan we keep hitting.
- **(b) Session-liveness (stuck / no handback):** query **AngelEye** (session last-active via hooks) or the **claude daemon registry** (`~/.claude/daemon.json`) to map a window → its session's liveness, since the OS process tree can't.

**Consequence:** **AngelEye is load-bearing for the reaper**, not just telemetry. It is currently NOT running and NOT hook-wired (needs its version-compat refresh). The reaper's stuck-case is blocked on that.

**Teardown:** threshold restored to 10min/30s (plist env back to just HOME), `swagger-staletest` reaped manually, 0 swagger windows, daemon healthy. No fragile state left.

**Lesson:** verify-don't-trust earned its keep — a "wired + reads-correct" detector was actually inert against the real runtime. A mechanism isn't proven until a live test fires it end-to-end.
