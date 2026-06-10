# Fleet-of-CLI-Sessions Orchestrators — Research Findings & Method

**Date:** 2026-06-10
**Author:** Marshall (deep-research workflow)
**Question:** Who else is building Dark Factory's *class* of thing — an open-source control plane that spawns, dispatches to, monitors, and reaps **fleets of coding-agent CLI sessions** (Claude Code / Codex) as isolated workers under a conductor?

> This doc captures **both the method** (the research prompt + the workflow that ran it, so it's repeatable) **and the findings**. The three "closest to study" repos get their own files in this folder — see the index in [`README.md`](./README.md).

---

## 1. Why we ran this

Dark Factory is — in plain terms — a **talk-to-it agent factory**: a stateless floor where a conductor (Marshall) dispatches jobs to isolated workers (Swaggers, real Claude Code sessions), watches them, reaps them, and keeps the operator oriented. The deeper architectural bet is that **shared state lives in separate services** (a comms bus, session telemetry, resource-health, a visual control plane) and the floor is a thin, replaceable client.

**What *class* of thing is it?** Not a chatbot, not one app — its closest name is an **agentic Manufacturing-Execution-System (MES) + control plane**: the software equivalent of a factory floor where the "machines" are LLM agent (Claude Code) sessions. Three lenses, one thing:
- **Industrial:** an MES / air-traffic-control for a fleet of agents — jobs enter, get scheduled to machines (Swaggers), status reports up to a control room (Watchtower); Symphony is the work-management layer on top (the ERP to the MES).
- **Software-architecture:** a **distributed work-execution system with a human-in-the-loop conductor**, built as single-responsibility, MCP-talkable services (a service-oriented constellation, not a monolith); HITL gates sit *between* jobs at Marshall, never inside a worker.
- **Plain-English:** an **operating system for a fleet of Claude Code sessions** — spawns, talks to, watches, kills, and learns from the run.

What makes it *not* "just an orchestrator": the floor is meant to be **stateless and replaceable**, with intelligence in the model/harness and durable state in services. It only earns the word "factory" if a second floor could plug into the same state plane and just work. **This is exactly the design the survey below found no one else has built** — see §3.

Before investing more, we wanted to know: **who's doing something similar, open-source, with visible code, with traction?** Specifically to (a) avoid reinventing, (b) steal good mechanics, and (c) confirm whether the constellation/state-plane split is genuinely novel.

## 2. The method (repeatable)

### 2.1 The research prompt

The prompt was deliberately shaped to **pin the class** and **fence out the noise**. The key moves:

- **Define the class precisely** — "fleet of coding-agent CLI sessions … spawned/monitored/reaped as isolated workers under a conductor."
- **Hard `NOT` clauses** — explicitly exclude single-agent chat wrappers, IDE plugins, and in-process agent *libraries*. Without these, the search drowns in CrewAI/AutoGen/LangGraph (the library class).
- **Hard requirements per result** — OSS with readable code, star count + activity, must drive Claude Code/Codex or be CLI-agnostic.
- **A fixed report shape per project** — what-it-is, architecture (dispatch / state location / liveness / reaping), HITL model, observability, and overlap-with-our-reference-design.
- **Named repos to verify, not assume** — claude-flow/ruflo, Claude Squad, Conductor, Crystal, Swarm/Agents SDK, worktree + tmux runners — with an instruction to confirm each is real and report *current* stars (counts drift fast).
- **Contrast, don't list** — AutoGen/CrewAI/LangGraph to be classified as the library class and contrasted, not counted as matches.
- **Deliverable** — ranked by *relevance to the class, not by stars*, plus a "closest 3 to study" section, flag vaporware.

The full prompt is preserved verbatim in [`research-prompt.md`](./research-prompt.md).

**Lesson for future research prompts:** the `NOT` clauses and the "verify by name, report current stars" instruction did the heavy lifting. Pinning the *class* and forcing per-result structure is what turned a vague "who else does this" into a fact-checked comparison.

### 2.2 The workflow that ran it

Ran via the **`deep-research`** skill → `Workflow` harness (background, multi-agent). Pipeline:

| Phase | What happened |
|-------|---------------|
| **Scope** | Decomposed the question into **6 search angles** (named-tool verification, broad fleet-orchestrators, architecture/worktree+tmux, Codex/model-agnostic, library-class contrast, Anthropic harness + observability) |
| **Search** | Parallel WebSearch agents, one per angle |
| **Fetch** | URL-dedup → fetched **19 sources** → extracted **94 falsifiable claims** |
| **Verify** | **3-vote adversarial verification** per claim (need 2/3 *refutes* to kill). Verified top 25 → **24 confirmed, 1 killed** |
| **Synthesize** | Merged semantic dupes, ranked by confidence, cited sources → 8 findings |

**Run stats:** 102 agents, ~4.0M subagent tokens, 499 tool uses, ~26 min wall-clock.
**Run ID:** `wf_cab05fdc-97e` (resumable via the script under the session's `workflows/scripts/`).

**How to re-run / extend:** re-invoke the `deep-research` skill with an updated prompt, or resume the existing run from its `scriptPath` + `resumeFromRunId` to add angles without re-paying for cached agents.

## 3. The finding (headline)

**The class is real, active, and crowded as of 2026-06-10 — but nobody ships our architecture.**

Seven OSS projects genuinely spawn → dispatch → monitor → reap fleets of coding-agent CLI sessions. The **dominant pattern is tmux-session-per-agent + git-worktree-per-task** for isolation, with shared state living **per-worker (worktree files)** or **in GitHub** — **not** in a separate state-plane.

> **No surveyed project ships the reference design's full split:** stateless floor + separate comms-bus + session-telemetry + resource-health + visual control-plane services. The closest analogues centralize only *dispatch* (CAO) or lean on *GitHub* as the de-facto state plane (agent-orchestrator). **This is a genuine green-field gap** — the constellation is a defensible thesis, not a reinvention.

## 4. Ranked by relevance to the class (NOT by stars)

| # | Project | Stars | Activity | State model | File |
|---|---------|------:|----------|-------------|------|
| 1 | **awslabs/cli-agent-orchestrator (CAO)** | ~694 | v2.2.0, 2026-06-04 | **Central dispatch** (localhost:9889), explicit liveness, auto-reap **w/ scrollback** | [cao](./cao-cli-agent-orchestrator.md) |
| 2 | **unohee/OpenSwarm** | 803 | 2026-06-06 | Cron daemon, Linear→Worker/Reviewer, tested CLI adapters | — |
| 3 | **ComposioHQ/agent-orchestrator** | 7,479 | 2026-06-09 | **GitHub as state plane** (PR/CI/review signals) | [composio](./composio-agent-orchestrator.md) |
| 4 | **smtg-ai/claude-squad** | ~7,800 | v1.0.18, May 2026 | Per-worktree TUI; hybrid HITL (`--autoyes`) | — |
| 5 | **nwiizo/ccswarm** | 139 | v0.9.1, 2026-06-10 | Per-worktree; **declarative YAML workflows + personas** | [ccswarm](./ccswarm.md) |
| 6 | **johannesjo/parallel-code** | 712 | v1.10.0, 2026-06-01 | Per-worktree Electron GUI launcher | — |
| 7 | ~~stravu/crystal~~ | ~3,100 | **DEPRECATED Feb 2026** (→ closed-source Nimbalyst) | Readable exemplar, unmaintained | — |

### Excluded — false twins (important)

- **Ruflo / claude-flow** — **NOT a fleet manager.** It's an MCP meta-harness Claude Code calls *into*, with **central Queen-led shared state** (Raft/Byzantine consensus + vector store). Its own README calls itself "a departure from stateless isolated workers toward agents sharing central state" — **the exact inverse of our stateless floor.** Note: our `appydave:ruflo` skill wraps this; architecturally it is the opposite of Dark Factory's premise.
- **superbasicstudio/claude-conductor** — name collision; scaffolds *docs*, not agents.
- **OpenAI Swarm / Agents SDK, AutoGen, CrewAI, LangGraph** — the *library* class: in-process agent objects sharing memory in one runtime. Correctly contrasted, not matched.
- **nielsgroen/claude-tmux** (179★) — a monitoring *pane* (idle/working/waiting status), explicitly "does not dispatch work or orchestrate jobs." Useful as a liveness-viewer reference only.

## 5. Closest 3 to study (what to steal / what they get wrong)

1. **CAO** — steal **dispatch + liveness + reap-with-post-mortem**. Only one with a central dispatch *service*, an explicit liveness state machine (IDLE/PROCESSING/COMPLETED/ERROR), and reaping that **preserves scrollback before deletion** (restorable). Maps ~1:1 onto Switchboard + AngelEye + our reaper. *Gets wrong:* state + dispatch fused into one local server; no plane separation, no visual control plane.
2. **ComposioHQ/agent-orchestrator** — steal **liveness-via-external-signals** (PR status, CI, review reactions + a 30-min stuck timeout). Validates our "observe the loop externally, don't trust the worker's bookkeeping" principle at 7.5k stars. *Gets wrong:* GitHub *is* the state plane — elegant but welds you to GitHub, no resource-health/comms layer.
3. **ccswarm** — steal the **declarative-workflow + persona model** (YAML flows: plan → consensus → implement → review → fix → PR, sequential or parallel). Closest anyone gets to Symphony + Marshall/Swagger roles expressed as data. *Gets wrong:* no state-plane services, no visual control plane.

## 6. Open questions (unresolved this round)

- Does Anthropic ship a **public OSS** multi-agent research harness driving multiple Claude Code CLI sessions as fleet workers, or is its orchestrator-worker system closed/internal? Not resolved.
- Does **any** project implement separate state-plane services (comms bus + telemetry + resource-health + visual control plane) as distinct services rather than folding state into git/GitHub or one local server? None found — green-field, or search miss?
- Is **Nimbalyst** (Crystal's successor) open or closed source, and does it move toward a central plane?
- How reliable in practice are CAO's reap-and-restore and agent-orchestrator's PR/CI-signal liveness **under failure** (stuck agents, partial PRs)? Not load-tested — directly relevant to our "tears down clean" bar.

## 7. Caveats

- **Star counts and release dates are point-in-time (2026-06-10) and drift fast** in this class — re-verify before citing (e.g. in a video).
- Two verification votes were split 2-1 (agent-orchestrator "no central state service" framing; Ruflo tool-count) — flagged, did not change conclusions.
- The library-class contrast (Swarm/AutoGen/CrewAI/LangGraph) was **not** primary-source verified this round — it's a structural classification, not a fact-checked claim.

## Sources (primary)

awslabs/cli-agent-orchestrator · ComposioHQ/agent-orchestrator · smtg-ai/claude-squad · unohee/OpenSwarm · nwiizo/ccswarm · johannesjo/parallel-code · stravu/crystal · ruvnet/ruflo · superbasicstudio/claude-conductor · nielsgroen/claude-tmux · anthropic.com/engineering/multi-agent-research-system
