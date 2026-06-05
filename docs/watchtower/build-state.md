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
| **C3b** | Report-back: Swagger result → `reports/` → Marshall surfaces it (kills the manual relay) | ⬜ next |
| **C3c** | Monitor: Marshall auto-wakes on a ticket (replaces "you say process the queue") | ⬜ |
| **C3d** | `marshall` skill hardened: liveness cap (~4 Swaggers), Swagger permissions (auto/allowlist, not bypass), graduate to `.claude/skills/marshall/` | ⬜ |
| **C4** | Return-leg / dashboard so nothing runs silently (#19) | later |
| **C5** | One real `kind:workflow` job end-to-end, triggered by talking | later |

**Right now Marshall is driven manually** ("process the queue") and the report-back is **me reading `done/` by hand**. C3b+C3c automate those.

## C3 acceptance checks (what each remaining step must nail)
- **C3b:** Swagger writes a terse `reports/<id>.json`; Marshall's watch reads it and surfaces one line. Proves the handback without a human relay.
- **C3c:** a single `Monitor` on `queue/` (macOS: `fswatch` or a glob-safe poll — see marshall skill note) wakes Marshall; one watcher only, never N.
- **C3d:** liveness count so Marshall never exceeds ~4 concurrent Swaggers (the ~5–7 session wall); replace Swagger `--dangerously-skip-permissions` with auto-mode/allowlist (open #3).

## Operating rules established this build (the durable principles)
1. **One watcher, never N.** Competing self-watchers thunder-herd; the mutex gives correctness, never fairness/distribution. One Marshall routes to isolated Swaggers. (`runtime-model.md`, brain `swarm-teams.md`)
2. **Marshall routes, never executes.** Heavy job context lives and dies in the Swagger; only one-line results reach Marshall. Keeps Marshall lean + clients un-crossed.
3. **Spawn interactive, NEVER `-p`.** `-p`/headless bills the metered SDK pool (from 2026-06-15); interactive runs on Max. Interactive doesn't self-close → watcher `kill-window`s on `done/` landing, not on process exit. (brain `subscription-enforcement.md`)
4. **Permissions:** attended Marshall → **auto mode**; unattended Swagger → must be non-prompting; bypass is a **temporary** spike shortcut, harden to auto/allowlist at C3d. Never bypass an unattended worker in production.
5. **Workers report + terminate — never interview the human.** Open questions go in the *deliverable*, not an interactive Q&A. You talk only to Marshall. (the doc-organiser worker over-stepped — that's the failure this prevents)
6. **Verify the artifact, never trust a "done" message.** Always check `done/` + run record + invariant (`running/` empty).
7. **Side-quest discipline:** every side-quest gets a **backlog line at birth**, then keep moving on the spine. Side-quests are the factory's *cargo*, not noise — the backlog (and later the Watchtower decision-queue) is the **register** that resurfaces them. "Fix the class, not the instance." (`systemic-fixes.md`)

## Active side-quests (parked, not lost)
- `backlog/2026-06-05-doc-organiser.md` — doc-organiser audit skill; proposal decided, build parked.

## Where reusable (non-dark-factory) knowledge lives
Platform-level Claude Code knowledge discovered here is in the brain, not here:
`~/dev/ad/brains/anthropic-claude/claude-code/{subscription-enforcement, swarm-teams, workflow-tool}.md`. Dark-factory holds the *application*; the brain holds the *reusable rule*. Keep them cross-linked.
