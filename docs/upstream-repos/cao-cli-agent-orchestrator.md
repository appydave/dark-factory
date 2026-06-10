# CAO — awslabs/cli-agent-orchestrator

**Repo:** https://github.com/awslabs/cli-agent-orchestrator
**Local clone:** `~/dev/upstream/repos/cli-agent-orchestrator/` (cloned 2026-06-10; registered in `brains/source-repos.md`)
**Stars:** ~694 · **License:** Apache-2.0 · **Latest:** v2.2.0 (2026-06-04) · **Status:** active
**Relevance rank:** #1 (closest architectural match to Dark Factory)
**Review status:** ☐ not yet reviewed — flagged for deep source-read

> ⚠️ Star count / release date captured 2026-06-10 — re-verify before citing.

## What it is

A supervisor-worker orchestrator that drives multiple coding-agent CLIs — **Claude Code, Codex, Gemini, Kiro** — as isolated workers, coordinated over MCP. The only surveyed project that combines a **central dispatch service + explicit liveness model + reap-with-post-mortem**.

## Architecture

- **Isolation:** each agent worker runs in its **own tmux session with a real PTY** — "humans can `tmux attach` to steer mid-task."
- **Dispatch:** centralized in a **local HTTP server** (default `localhost:9889`). Callers are identified by a unique `CAO_TERMINAL_ID` env var.
- **Liveness:** the server tracks each terminal's status — **IDLE / PROCESSING / COMPLETED / ERROR**.
- **Coordination modes:** `handoff` / `assign` / `send_message`.
- **Reaping:** on success it **auto-deletes the worker terminal**, but first saves **scrollback + metadata** to `~/.cao/logs/terminal/`, restorable via `cao terminal restore <id>`.

## HITL model

Mixed — humans can attach to a live tmux session to steer mid-task; supervisor coordinates handoffs between workers.

## Observability

Per-terminal status tracking via the local server + preserved scrollback logs (post-mortem). No separate visual control plane / dashboard.

## Overlap with Dark Factory — and where it differs

**Closest analogue to the factory floor.** Its dispatch server ≈ Switchboard, its terminal-status model ≈ AngelEye liveness, its reap-with-scrollback ≈ our reaper + "tears down clean" bar.

**Differs:** state and dispatch are **fused into one local HTTP server** — no separation into distinct planes (comms bus / telemetry / resource-health), and **no visual control plane** (no Watchtower equivalent).

## What to steal

- The **reap-with-post-mortem** pattern (save scrollback + metadata *before* deletion, make it restorable) — directly applicable to our reaper and the dispatch-loop-robustness bar.
- The **explicit liveness state machine** (IDLE/PROCESSING/COMPLETED/ERROR) as a typed contract, not ad-hoc.
- **Per-worker identity via env var** (`CAO_TERMINAL_ID`) — clean way for a stateless worker to address the dispatch service.

## What it gets wrong (for our purposes)

- Single fused server = no plane separation; can't independently scale/replace comms vs telemetry vs health.
- No visual control plane.

## Next-action if we review

Source-read the dispatch server + reap logic; compare its liveness state machine and `CAO_TERMINAL_ID` scheme against Switchboard/AngelEye. Test reliability **under failure** (stuck/partial workers) — the open question most relevant to our teardown bar.
