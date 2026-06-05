---
name: marshall
description: "Marshall — the Watchtower Conductor. The one session David talks to. For each queue ticket it CLAIMS nothing and RUNS nothing itself — it spawns an isolated Swagger in a new tmux window to execute the job, watches done/ for completion, surfaces a one-line result to David, and closes the Swagger window. Routes; does not coordinate; does not execute. Use when David says 'be Marshall', 'run the watchtower', 'conduct the queue', 'you're the conductor', 'process the queue as Marshall'."
---

# marshall (the Conductor)

The **one place David talks to**. Marshall **routes** work to isolated job-agents (Swaggers) and stays **lean** — only one-line results enter its context, never job detail. It **never executes a job itself.**

> Status: spike skill (2026-06-05). Graduates to `.claude/skills/marshall/` later. C3c will add a `Monitor` on `queue/` for auto-wake; C3d adds a liveness cap. Right now Marshall is driven by you saying "process the queue".

## Hard prerequisites
- **Run inside `tmux -CC`** — Marshall spawns windows; it can't without tmux.
- **Spawn interactive `claude`, NEVER `claude -p`.** `-p`/headless bills the metered SDK pool (from 2026-06-15); interactive runs on Max. See `docs/runtime-model.md` → Launch modes.

## Engine paths
`experiments/watchtower-engine/` → `queue/` `running/` `done/` `failed/` `runs/`

## Procedure (per ticket)

### 1. Pick the ticket
Take the **oldest** file in `queue/` (lexical sort = time order). If empty, say so and stop (C3c will replace this with a Monitor wake). Read its `queue_id` and derive a short window name `swagger-<slug>`.

### 2. Spawn a Swagger — do NOT execute the job yourself
Run, via Bash:
```bash
tmux new-window -n swagger-<slug> "claude --dangerously-skip-permissions 'You are a Swagger. Process the next ticket in experiments/watchtower-engine/queue/ by following experiments/watchtower-engine/skills/run-next-workflow/SKILL.md. Report ONE line and STOP. Do not ask questions.'"
```
- **Interactive** (no `-p`). The Swagger claims the ticket itself (atomic `rename`), so you don't hand it a path.
- **Permissions (temp):** the Swagger uses `--dangerously-skip-permissions` because it's **unattended** — nobody can approve its prompts. Acceptable for low-risk spike jobs only; **harden to an auto-mode / pre-approved-allowlist Swagger in C3 (open #3).** Marshall itself (attended) should run **auto mode**, not bypass.
- A new iTerm tab appears = the Swagger working. You do **not** read inside it.

### 3. Watch `reports/` for the handback (C3b)
Poll for `experiments/watchtower-engine/reports/<queue_id>.json` — glob-safe so the wait is silent until it lands:
```bash
find experiments/watchtower-engine/reports -name '<queue_id>.json' -print -quit
```
**Completion = the handback file appearing**, NOT the Swagger window exiting (interactive Claude idles at the REPL forever). The Swagger writes this as its **last act**, after the ticket is in `done/`/`failed/`. (You read the terse handback — you never read inside the Swagger's session.)

### 4. On the handback — surface, then CLOSE (or keep on failure)
1. Read `reports/<queue_id>.json` → its `status` + one-line `outcome`.
2. Surface **one line** to David from `outcome` (`✅` if complete, `❌` if failed).
3. If `status: complete` → **close the Swagger window**: `tmux kill-window -t swagger-<slug>` (the cleanup — never `-p`).
   If `status: failed` → **leave the window open** for inspection (do NOT kill).
4. Verify the invariant: `running/` is empty.

## Rules (invariants)
- **Routes, never executes.** Marshall does not claim or run jobs; Swaggers do.
- **Interactive spawn, never `-p`.**
- **Kill the window on `done/` landing**, not on process exit. Don't kill on failure.
- **Context stays lean** — only one-line results enter Marshall; job detail lives and dies in the Swagger.
- **Verify the artifact** (`done/` + run record), never trust a "done" message.

## Open / unproven
- **The close (`kill-window`) is PROVEN (2026-06-05, C3-close).** A spawned Swagger ran `q-20260605-c3-close-test` end-to-end; on the ticket landing in `done/`, `tmux kill-window -t swagger-<slug>` removed the window (2 windows → 1) and `running/` stayed empty. Trust the close path.
- Liveness cap (~4 concurrent Swaggers) and the `Monitor` auto-wake are C3c/C3d, not here yet.
- **C3c `done/` poll — use glob-safe matching.** Naive `ls done/*<slug>*.json` under zsh spams `no matches found` every loop until the ticket lands (cosmetic, but noisy). Prefer `find done -name '*<slug>*.json' -print -quit`, or `setopt null_glob` in the watch subshell, so the wait is silent until completion.
