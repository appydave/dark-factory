# Watchtower Build State — the C-spine

**Status**: living state — 2026-06-05. The single "where are we / what's next / the rules" doc for the runtime build.
**For a fresh session**: read THIS first, then `docs/north-star.md`, `docs/runtime-model.md`, `experiments/watchtower-engine/README.md`, and the two skills (`producer`, `marshall`). That fully orients you.

---

## One line

We are proving the factory runtime **one mechanism per session, N=1, do-not-theorise** — the **C1→C5 spine**. The "build the factory" path (North Star Path 1), not the content cargo.

## The spine — status

| Step | What it proves | Status |
|------|----------------|--------|
| **C1** | Consumer runs one job by hand (claim→execute→record→done) | ✅ proven 2026-06-05 (`proof/c1-first-real-run.md`) |
| **C2** | Producer: talk → schema-valid ticket; ran across two sessions | ✅ proven (`skills/producer/`, `proof/` + doc-organiser run) |
| **C3a** | Marshall spawns a Swagger via `tmux new-window` | ✅ proven (`proof/c3a-spawn-proof.md`) |
| **C3-close** | Marshall closes the Swagger window (`tmux kill-window`) on `done/` landing | ✅ proven (`proof/c3-close-proof.md`; 2 windows → 1) |
| **C3b** | Report-back: Swagger result → `reports/` → Marshall surfaces it (kills the manual relay) | ✅ proven 2026-06-06 (`proof/c3b-report-proof.md`; non-bypass Swagger wrote `reports/q-20260606-c3b-report-test.json`, Marshall read it, surfaced one line, killed window) |
| **C3c** | Monitor: Marshall auto-wakes on a ticket (replaces "you say process the queue") | 🟡 **mechanism proven 2026-06-06** — Marshall's `Monitor` subscribed to the daemonized **Switchboard** SSE (`?subscribe=process.snapshot`) and woke on real live events (incl. a fresh `id:26` ~15s after connect) + replayed the buffered backlog. Topic-filtering + durable-log replay work. **Remaining:** point it at a *job/ticket* topic once Switchboard carries the queue, and have Marshall track `Last-Event-ID` so it only gets NEW work (replaying all old tickets would re-process done jobs). |
| **C3d (perm)** | Swagger permissions: **non-bypass allowlist, not `--dangerously-skip-permissions`** | ✅ proven 2026-06-06 — see "Permission model" below. Replaces open #3. |
| **C3d (rest)** | `marshall` hardened: liveness cap (~4 Swaggers), graduate to `.claude/skills/marshall/` | ⬜ |
| **Concurrency (N>1)** | Multiple Swaggers run at once on a shared queue | ✅ proven 2026-06-06 (`proof/concurrency-demo-result.md`; 3 Swaggers, real-mtime 22s interleaved window, atomic claim 1:1, clean teardown). Caveat: agent self-reported timestamps were hallucinated — real timing came from filesystem mtimes (capability-placement lesson). Auto-reaper still owed (reaped manually). |
| **Watchtower board v1** | Live read-only view of the floor (#19 surface) | ✅ spike 2026-06-06 (`experiments/watchtower-board/server.mjs`, :7430; reads engine + tmux; eventual home = AppyStack Watchtower instance) |
| **C4** | Return-leg / dashboard so nothing runs silently (#19) | later |
| **C5** | One real `kind:workflow` job end-to-end, triggered by talking | later |

**Right now Marshall is driven manually** ("process the queue") and the report-back is **me reading `done/` by hand**. C3b+C3c automate those.

## C3 acceptance checks (what each remaining step must nail)
- **C3b:** Swagger writes a terse `reports/<id>.json`; Marshall's watch reads it and surfaces one line. Proves the handback without a human relay.
- **C3c:** a single `Monitor` on `queue/` (macOS: `fswatch` or a glob-safe poll — see marshall skill note) wakes Marshall; one watcher only, never N.
- **C3d:** liveness count so Marshall never exceeds ~4 concurrent Swaggers (the ~5–7 session wall). *(Permission half done — see below.)*

## Permission model — PROVEN 2026-06-06 (the real C3d deliverable)

The original spec spawned Swaggers with `--dangerously-skip-permissions`. **That is incompatible with an auto-mode Marshall** and is now retired. Two classifier denials taught the correct model:
1. Auto-mode Marshall **cannot spawn a bypass agent** — "unsafe agent loop with no approval gate."
2. Auto-mode Marshall **cannot edit its own `permissions` settings** — "self-modification not requested."

Both denials are *correct* — auto mode refuses self-escalation. The model that works:

> **The trust boundary is a one-time human act; dispatch within it is autonomous.**

David establishes, once, in `.claude/settings.local.json` → `permissions.allow`:
- `Read/Write/Edit(experiments/watchtower-engine/**)` + scoped engine Bash (`claim-next.sh`, `find/mv/ls/cat …engine…`, `date`) → the **Swagger** runs unattended, **no bypass, no prompts**.
- `Bash(tmux new-window* | kill-window* | list-windows*)` → **Marshall** spawns/closes Swaggers without the classifier blocking.

Proven run: a **non-bypass** Marshall (plain `claude`, not auto, not bypass) spawned a **non-bypass** Swagger via allowlisted `tmux new-window`; the Swagger claimed `q-20260606-c3b-report-test`, ran the instruction, wrote the run record + `reports/` handback entirely within the allowlist (zero prompts), and Marshall closed the window. ✅ both C3b and the C3d permission half in one run.

**Known gap (⚠️):** a `kind:instruction` job that writes *outside* `experiments/watchtower-engine/` will prompt and hang (non-bypass, unattended) — correct fail-safe, but general instruction-jobs need a wider boundary. Widen deliberately when a real job demands it; don't pre-grant.

## Operating rules established this build (the durable principles)
1. **One watcher, never N.** Competing self-watchers thunder-herd; the mutex gives correctness, never fairness/distribution. One Marshall routes to isolated Swaggers. (`runtime-model.md`, brain `swarm-teams.md`)
2. **Marshall routes, never executes.** Heavy job context lives and dies in the Swagger; only one-line results reach Marshall. Keeps Marshall lean + clients un-crossed.
3. **Spawn interactive, NEVER `-p`.** `-p`/headless bills the metered SDK pool (from 2026-06-15); interactive runs on Max. Interactive doesn't self-close → watcher `kill-window`s on `done/` landing, not on process exit. (brain `subscription-enforcement.md`)
4. **Permissions: non-bypass allowlist, bypass retired.** Attended Marshall → auto mode; unattended Swagger → non-prompting via the `permissions.allow` boundary (one-time human grant). `--dangerously-skip-permissions` is **gone** — incompatible with auto mode + classifier-blocked as self-escalation. See "Permission model" above (proven 2026-06-06).
5. **Swagger is a talkable orchestrator, not a sealed batch job.** It delegates to sub-agents/workflows AND **David may engage it directly** — interject, answer, help. It may surface a help-request **to David** (visibly), not just to Marshall. What's banned is the doc-organiser failure: *silently blocking* on an unexpected interactive Q&A. Default = put open questions in the deliverable and keep moving; but a live Swagger David can talk to is the intended design. ⟹ this is *why* the lifecycle (rule 8) must be deliberate, not auto-kill-on-done.
6. **Verify the artifact, never trust a "done" message.** Always check `done/` + run record + invariant (`running/` empty).
7. **Side-quest discipline:** every side-quest gets a **backlog line at birth**, then keep moving on the spine. Side-quests are the factory's *cargo*, not noise — the backlog (and later the Watchtower decision-queue) is the **register** that resurfaces them. "Fix the class, not the instance." (`systemic-fixes.md`)
9. **Robustness is the bar (David, 2026-06-06, paramount).** The dispatch loop must be reliable whatever the mechanism — engineer against the four failure modes every time: **comms** (message arrives), **return** (result comes back), **shutdown** (worker/window/process closes — no orphans), **leaks** (RAM/processes don't accumulate). Fragility = whack-a-mole = no factory. A mechanism isn't "proven" until it **tears down clean**. Not all solved at once, but a first-class concern in every experiment.
8. **No orphans — every Swagger is identifiable and reliably reaped.** Interactive `claude` idles at the REPL **forever** after finishing; `kill-window` only works if the window is in Marshall's tmux server AND Marshall catches the handback. Anything else strands an invisible process (evidence: a 22h-idle "Process the next ticket" Swagger + ~4 stray bypass sessions found 2026-06-06). Required: (a) named window + a registry entry stating each Swagger's purpose, so a live one is always explainable; (b) a reaper that kills + deregisters a Swagger once its job is in `done/` and a grace window (for rule-5 talk) has elapsed. This is the C3d-lifecycle work — see `backlog/2026-06-06-swagger-lifecycle.md`.

## Active side-quests (parked, not lost)
- `backlog/2026-06-05-doc-organiser.md` — doc-organiser audit skill; proposal decided, build parked.
- `backlog/2026-06-06-swagger-lifecycle.md` — no-orphan Swagger lifecycle (registry + reaper + self-close); talkable-orchestrator constraint. **Next C3d work.**

## Where reusable (non-dark-factory) knowledge lives
Platform-level Claude Code knowledge discovered here is in the brain, not here:
`~/dev/ad/brains/anthropic-claude/claude-code/{subscription-enforcement, swarm-teams, workflow-tool}.md`. Dark-factory holds the *application*; the brain holds the *reusable rule*. Keep them cross-linked.
