# Dark Factory — Runtime Model (who runs what)

**Status**: 2026-06-02 — resolved in design session. The shape of how the factory actually executes.

---

## Three layers

1. **Marshall — the Conductor** — David's **primary daily orchestrator**, in the Watchtower. The one place David talks to. Receives a problem → decides what's a job → **dispatches** each job to a job-agent. Holds the **single Monitor**. **Routes; does not coordinate** (jobs are independent). Keeps David oriented; reports results back. (Skill: `.claude/skills/marshall/`.)

2. **Swagger — the job-agent** (one per job). The root of a tmux-pane cluster for **one** problem. Owns it with **judgment**: runs a workflow *and/or* spins up sub-agent panes; **listens to the result, decides if more is needed, spins up the next workflow/agent.** Isolated — never coordinates with other Swaggers. Reports up to the Conductor.

3. **Workflows & sub-agents — execution.** A **workflow** is a long, deterministic route (the SOP). A **sub-agent pane** is a flexible agent. *A workflow is just a longer, more-deterministic version of an agent in a pane* — so Swagger **chooses** per step: deterministic route (workflow) or flexible agent (pane).

## The verbs

The factory **builds / improves / runs** workflows. Conductor and Swaggers operate on workflows; the **target** (client / project / problem) is a **label on the job**, orthogonal to the machinery.

## Why this shape (the discomfort it resolves)

- **Jobs are independent** (different clients/projects/problems). So there is **no team coordinating across jobs** — only isolated Swaggers. The Conductor **routes**; it doesn't run a team.
- **One Monitor on the Conductor** kills the thundering-herd problem (3 jobs no longer fire into one draining conversation) — the Conductor distributes them to separate Swaggers.
- **Execution alone isn't enough.** A workflow can't decide "is more needed?" That judgment is **Swagger's** — which is why a job-agent (not a bare workflow) owns each job.

## Naming

- **Conductor = Marshall** (chosen 2026-06-02). To *marshal* = route / organize / dispatch — the role's verb. (Considered: Atlas, Sentinel.)
- **Job-agent = Swagger.**

## Constraints (Agent Teams reality)

- Teammates can't spawn sub-*teams* — but a Swagger CAN run workflows + sub-agents. Fits.
- ~5–7 concurrent-session ceiling → **Conductor + ~4 Swaggers** max.
- Task status lags → the Conductor **verifies the artifact**, never trusts a "done" message.

---

## Launch modes — how to start it each time

The only thing that changes between "now" and "C3" is **who opens the worker session**. That single fact decides whether you need tmux.

| Who opens the worker | tmux needed? | When |
|----------------------|--------------|------|
| **You, by hand** | No — any iTerm pane/tab/window | C1, C2, manual C3 preview (today) |
| **Marshall, automatically** | **Yes** — `tmux new-window` *is* the spawn mechanism | C3+ (Marshall does the spawning) |

A Claude session can't conjure a new iTerm pane on its own; it shells out to **tmux** to do it. So tmux is required *only* when the software (Marshall) opens workers — not when your hands do.

### Mode A — Manual worker (now)
You are the talk-session; you open the worker yourself.
```bash
# 1) talk session: wherever you already are (this becomes Marshall later)
# 2) open a SECOND iTerm pane/tab/window, then:
cd ~/dev/ad/apps/dark-factory
claude
# 3) tell that worker session:
#    "Process the next ticket in experiments/watchtower-engine/queue/ by following
#     experiments/watchtower-engine/skills/run-next-workflow/SKILL.md."
```
Permissions: for a **watched, one-off** run, `--dangerously-skip-permissions` is tolerable. For anything repeated/unattended, use **`defaultMode` + a pre-approved allowlist** instead.

### Mode B — Auto-spawn (C3+)
Marshall opens Swaggers itself, so Marshall must run **inside tmux**.
```bash
# 1) open iTerm, start tmux control mode (gives native iTerm tabs per pane)
tmux -CC
# 2) launch Marshall (arms the single Monitor on queue/)
cd ~/dev/ad/apps/dark-factory
claude   # Marshall skill
# 3) Marshall, on a ticket, runs:
#    tmux new-window -n swagger-<job> "claude '<swagger prompt>'"
#    -> a new iTerm TAB appears = the Swagger. Its sub-agents = panes inside that tab.
```
Permissions: autonomous Swaggers need a **pre-approved allowlist (`defaultMode`)** — **never** `--dangerously-skip-permissions` unattended (that's the documented destructive-action risk).

**Spawn interactive, NEVER `-p` (billing-critical — proven 2026-06-05).** Spawn with interactive `claude "<prompt>"`, not `claude -p`. As of **2026-06-15**, `-p`/headless/SDK-mode runs on a **separate metered API credit pool**, *not* the Max plan; interactive `claude` runs on the **Max subscription**. So `-p` costs real money; interactive doesn't. (The `$x.xx` an interactive session shows is the *notional* would-be-API figure, not a charge — verified on Roamy with no API key/Bedrock/Vertex set.) Matches the North Star "in sessions, never cron/API" and `watchtower/HANDOVER.md` decision #1.

**Window lifecycle (locked 2026-06-05).** Interactive Claude does **not** exit after its turn — it sits at the REPL, so a spawned Swagger window **won't self-close**. Do **not** "fix" that with `-p` (see above). The pattern:
1. completion = **the ticket landing in `done/`**, *not* the window exiting;
2. **the watcher (Marshall) runs `tmux kill-window`** on that window the instant `done/` lands.
- **Open item:** fold kill-on-`done/` into Marshall's spawn-and-watch step (C3d).
- **Alternative to weigh at C3d:** the Swagger `tmux kill-window`s *itself* as its last action — simpler, no watcher-race; Marshall's reaper covers crash-before-cleanup. (Decision currently = watcher-kills; revisit when building the skill.)

### Recommendation
**Always launch inside `tmux -CC` from the start** — even in Mode A. It costs nothing for manual use and means **no environment switch** when you move to auto-spawn: hand-opened panes and Marshall's `new-window` spawns both live in the same tmux session.
