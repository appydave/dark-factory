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
