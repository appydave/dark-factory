# Concepts register — ideas to expand into specs over time

**Living register, started 2026-06-06.** The place for *concepts* (bigger than a backlog task, not yet a spec). Each is a "little idea that needs to be expanded out" — capture it, **categorize** it, mark whether it needs a spec, rank importance later. **Capture, don't chase** (see memory `priority-and-no-distraction`): little ideas go here so they're not lost AND don't derail the spine. This is the lightweight stand-in until the Symphony work-management layer + Watchtower triage formalize priority.

**Status legend:** 💡 idea · 📋 needs-spec · 🔨 building · ✅ done
**Priority:** to be ranked once the priority system exists (Symphony/Watchtower). For now: 🔴 spine · 🟡 soon · 🟢 idle-time fruit.

---

## Communication layer (Switchboard)
| Concept | Status | Pri |
|---|---|---|
| Bus runs + Marshall wakes on it (SSE + Monitor) | ✅ | 🔴 |
| Queue/job-ingest (`POST /jobs` → `job.queued`) | ✅ | 🔴 |
| Durable + claimable tickets (bus = wake, file = exactly-once claim) | ✅ (proven live; earlier "fail" was a stale daemon, not a bug) | 🔴 |
| **Swagger SELF-CLOSE on success** (baked into marshall spawn doctrine 2026-06-06) + reaper backstop — teardown must NOT depend on Marshall remembering (proven to fail) | 🔨 self-close in skill; reaper 📋 | 🔴 |
| Topic-selective durable log (job/session/alert logged+replayed; process.snapshot pushed live, never persisted) | ✅ **proven live 2026-06-06** (post-compact: restarted daemon PID 23883; raw SSE shows process.snapshot flows live every 15s but durable log stays empty of it; job.queued POST → ticket + durable-log entry + replay-from-id-0 all ✅) | 🔴 |
| Verify-reload-after-deploy + daemon version visibility (launchctl kickstart reload is racy — test hit stale code) | 📋 **lesson reinforced 2026-06-06** — the committed refactor (`d1506ba`) was NOT live; old daemon kept bloating the log until `launchctl kickstart -k` deployed PID 23883. Committed ≠ deployed. Want: daemon exposes its running git-sha on /health so "is the refactor live?" is one curl, not a forensic log-grep. | 🟡 |
| `Last-Event-ID` / dedup so Marshall only gets NEW work | 📋 (replay mechanism proven; Marshall-side cursor tracking still owed) | 🟡 |
| Reaper = harness-driven, NOT remembered: **staleness detector in Switchboard** (polls own process state + queries AngelEye session liveness; rule "no activity >10min + job done = stale") → pushes `session.stale`/`alert.*` → **Marshall's Monitor wakes + reaps**. Switchboard detects+tells (observe-only); Marshall acts. | 🔨 **detector half WIRED + LIVE 2026-06-06** (in daemon main.ts:64; scans swagger-* tmux every 30s, BFS for claude proc, etime>10m → emits session.stale; logic verified by read, emit not yet observed live). **Owed: Marshall-consume+reap half** — prove END-TO-END on next real Swagger dispatch (lower threshold, strand one, confirm session.stale → Marshall reaps). Don't write reaper doctrine as "proven" until that live run. | 🔴 |
| Marshall's Monitor = FEEDBACK channel (senses), not just jobs: subscribe `job.queued` + `alert.*`/`session.stale` | 📋 | 🟡 |
| Event-log pruning (unbounded growth) | 💡 | 🟢 |

## Visual communication (Watchtower) — NEW 2026-06-06
*Visual communication IS communication. Watchtower = the visible surface of the comms system.*
| Concept | Status | Pri |
|---|---|---|
| Kanban board of tickets/jobs | 💡 | 🟡 |
| "What are the agents doing right now" — live agent-activity view | 💡 | 🟡 |
| Live view of the communication going on (messages on the bus) | 💡 | 🟡 |
| App-switching between Watchtower ↔ AngelEye (and others) | 💡 | 🟢 |
| Capped decision-queue triage (the original Watchtower spec) | 📋 | 🟡 |

## Telemetry (AngelEye)
| Concept | Status | Pri |
|---|---|---|
| Refresh: fix Claude-Code version-compat (hook transport broke v2.1.89) | 📋 | 🟡 |
| Daemonize it (no manual start) | 📋 | 🟡 |
| Session liveness/stall detection for Swaggers | 💡 | 🟡 |
| dark-factory classification overlay | 💡 | 🟢 |

## Work-management / priority (Symphony)
*David 2026-06-06: the system now spawns concepts faster than we can organize them (4 apps + documentary + many loose ends) and there's **no way to SEE them, know which have gone stale, or tell what lane an idea fits in**. This markdown register is the MVP that the items below supersede. Cross-cuts **Watchtower** (the visual board that renders the lanes) — "being able to visualise stuff will be important."*
| Concept | Status | Pri |
|---|---|---|
| Projects (folders) → epics → stories/tickets → importance | 📋 | 🟡 |
| Ticket priority/project/epic metadata (beyond queue_id/kind/prompt) | 📋 | 🟡 |
| Idle-time low-hanging-fruit triage (capture, don't distract) | 💡 | 🟡 |
| Port Symphony state machine (§7/§16) to the factory floor | 📋 | 🟡 |
| **This concepts register** (categorize ideas → specs over time) | 🔨 | 🟡 |
| **Lane/epic structure for IDEAS (not just jobs)** — BMAD analogy: epics = lanes, stories under them; "open a new lane = create a new epic"; every loose-end / concept / app / idea belongs to a lane. Natural lanes today = the apps (Watchtower/Switchboard/AngelEye/AppyCtrl/Chronicle) + cross-cutting (robustness, observability, distribution). | 📋 | 🟡 |
| **Idea-staleness** — surface which concepts haven't been touched (per-item last-modified). Stale ≠ dead: needs a "still relevant?" judgment, not auto-reaping. (Mirror of the SESSION staleness-detector, applied to ideas.) | 📋 | 🟡 |
| **Periodic REFRESH + recategorization pass** — re-read all concepts, re-bucket, merge/split lanes, re-rank. A standing task, not one-off (David 2026-06-06). | 📋 | 🟡 |
| **Design resolution — LLM *and* data structures, not either/or (David's open Q):** JSON + schema = the **source of truth** (lanes, per-item last-touched → staleness is date math, counts, stable shape Watchtower can render; **NO database — files are fine**, "schemas and JSON and scaffold applications"). **LLM = the maintainer/judge** that does the fuzzy work on a refresh pass: categorize a new idea into a lane, detect overlap/merges, propose a new lane, flag stale-but-important vs stale-and-droppable. Deterministic state in the schema; judgment from the LLM. | 📋 | 🟡 |
| **Recursion noted:** managing the concepts is itself a concept; this is the Symphony work-mgmt layer + Watchtower visual layer meeting. A "think-do." | 💡 | 🟡 |

## Robustness & observability
| Concept | Status | Pri |
|---|---|---|
| Robustness bar: comms/return/shutdown/no-leaks, clean teardown | ✅ (doctrine) | 🔴 |
| Verify the 60GB Claude-Code RAM-leak claim with our own numbers | 📋 | 🟢 |
| System-health view (per-process RAM/CPU, open-Swagger count) | 💡 | 🟡 |

## Distribution
| Concept | Status | Pri |
|---|---|---|
| M4 Mini as a remote Swagger worker (SSH+tmux, tested-reachable) | 📋 | 🟡 |
| Per-machine Switchboard (each agent-running box daemonized) | 📋 | 🟡 |
| Other minis (M2, jan, mary) as workers | 💡 | 🟢 |

## Story / build-documentary (the "Chronicle" — provisional name, David to rename) — NEW 2026-06-06
*David's Tesla-Gigafactory analogy: a complex system being built deserves a **documentary** — the decisions, the rollbacks, the changes, the journey, the growing complexity. Captures the STORY OF BUILDING the factory, distinct from the factory's own runtime/telemetry. **Capture-and-understand stage — not building yet** (David wants the ORDER/method first, not ad-hoc agent-spraying). Can be spun up as separate parallel tasks (not system-build work).*
| Concept | Status | Pri |
|---|---|---|
| The Chronicle concept: record/narrate the build journey (decisions, rollbacks, changes) | 💡 (North-Star-adjacent direction) | 🟡 |
| Mechanism A — **parallel "story" agents that just run** (observe + narrate, separate from build tasks) | 💡 | 🟡 |
| Mechanism B — **hooks baked into regular agents** (capture moments on-the-fly, inline) | 💡 | 🟡 |
| Timing — on-the-fly capture vs **retrospective mining** (track all build conversations, revisit later with fresh eyes) | 💡 | 🟡 |
| Raw material ALREADY EXISTS, unmined: session transcripts (.jsonl), git history (= literal change/rollback log), concepts.md, build-state.md, proof/ files, auto-memories | ✅ sources exist | — |
| Proposed first cut: **retrospective transcript-mining** (low-risk, doesn't interrupt build) → a `docs/chronicle/` narrative; on-the-fly hooks come later | 💡 | 🟡 |
| Define an ORDER/method for how we document (David's explicit ask) | 📋 | 🟡 |

## Architecture principles & reassessment — NEW 2026-06-06
*David: we need stated principles for (1) WHERE a capability should live, and (2) HOW we re-judge past decisions with distance — the builder is too close to judge their own architecture; it's better observed later. See memory `capability-placement-and-reassessment`.*
| Concept | Status | Pri |
|---|---|---|
| **Capability-placement principle** — for any capability, consciously choose the LOCUS: model-in-session vs harness/runtime vs MCP vs external API vs which-app-owns-it. Worked example: a true timestamp belongs to the OS/harness/engine (mtime, `date`), NOT a language model — blocking `date` pushed time-of-truth into the model, which hallucinated it. Wrong-locus. | 📋 | 🟡 |
| **Reassessment loop** — a built-in mechanism that revisits past decisions later, with DISTANCE, and reassesses for better capability. Make it INTEGRAL, not ad-hoc. Likely a separate-perspective agent (builder can't review itself well). | 📋 | 🟡 |
| **Convergence:** recategorize-ideas + mine-chronicle-fresh-eyes + idea-staleness + architecture-reassessment = ONE reflective-review pattern (a later pass re-judges in-the-moment work). Build once, apply many places. | 💡 | 🟡 |

---
*Add freely. Re-categorize as understanding sharpens. Expand a 📋 into a real spec when it reaches the top of the priority list — not before.*
