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
| Reaper = harness-driven, NOT remembered → **REDESIGN after live-fire (2026-06-06)**: process-tree detection is a DEAD END — the claude session is reparented to the claude daemon, not under the tmux pane, so BFS finds nothing. Robust signals instead: (a) engine-state — handback in reports/ + window still open after grace → reap (process-independent); (b) AngelEye / claude-daemon session-liveness for the stuck-no-handback case. Marshall's Monitor still does the reap. | ✅ **COMMON case PROVEN live 2026-06-07** — engine-state reaper (`bin/reaper.sh` Monitor + dispatch registry): handback + grace → kill still-open window + deregister, no Marshall memory. Process-tree path abandoned (dead). **STUCK case** (no handback) still owed → AngelEye/AppyCtrl session-liveness. `docs/watchtower/reaper-brief.md`, `proof/reaper-livefire-finding.md`. | 🔴 |
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
| **Tool USAGE telemetry** — count invocations of self-made tools (command/skill/plugin/MCP/workflow). Two undecided mechanisms: (a) retrospective read in AngelEye, (b) real-time hook counters (David 2026-06-06). | 📋 | 🟡 |
| **Usage → self-evolution:** heavily-used = optimize more often; rarely-used = deprecate / repurpose / fix the description-header (bad "Use when…" = under-invocation). The DATA that drives reassessment of the tool catalog + manages the "flood of skills" (measure what's used). See memory `tool-usage-telemetry-for-self-evolution`. | 📋 | 🟡 |
| **Open Q:** are the reflective-review concepts (recategorize/chronicle/staleness/reassessment) deterministic *code* or *skills*? If skills, they add to the flood → usage telemetry becomes the management handle. | 💡 | 🟡 |

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
| **Fragment → convergence funnel (front of the work pipeline)** — David 2026-06-07: lots of loose questions / idea-thoughts that aren't tickets; need to QUEUE them and later bring a related cluster together into ONE cohesive **research brief / architecture-decision / coding epic**. Stages: **capture** (cheap inbox) → **accrete** (loosely tagged) → **converge** (a JUDGMENT pass = dispatchable Swagger / reflective-review job: cluster + synthesize) → **promote** to dispatched work. Distinct from lanes (categorized concepts); fragments are PRE-concept. | 💡 | 🟡 |

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
| **Factory-metaphor storytelling** — Floor/Lanes/Swaggers/Marshall/Watchtower is a deliberate NARRATIVE asset for David's YouTube; keep naming + metaphor coherent; develops over time (see memory `factory-metaphor-storytelling`). | 💡 | 🟡 |
| **Floor↔Lanes bridge** — "promote a lane item → a floor job" (the unbuilt planning→execution link; where the two board views become one workflow). | 📋 | 🟡 |
| **Storytelling spans the whole constellation** — every app + their relationships are one journey; aspiration to GENERATE an animated/3D graphic of the factory from a structured system-model (David 2026-06-06). Structured model → drives both the live board AND a future render. | 💡 | 🟢 |

## Architecture principles & reassessment — NEW 2026-06-06
*David: we need stated principles for (1) WHERE a capability should live, and (2) HOW we re-judge past decisions with distance — the builder is too close to judge their own architecture; it's better observed later. See memory `capability-placement-and-reassessment`.*
| Concept | Status | Pri |
|---|---|---|
| **Capability-placement principle** — for any capability, consciously choose the LOCUS: model-in-session vs harness/runtime vs MCP vs external API vs which-app-owns-it. Worked example: a true timestamp belongs to the OS/harness/engine (mtime, `date`), NOT a language model — blocking `date` pushed time-of-truth into the model, which hallucinated it. Wrong-locus. | 📋 | 🟡 |
| **Reassessment loop** — a built-in mechanism that revisits past decisions later, with DISTANCE, and reassesses for better capability. Make it INTEGRAL, not ad-hoc. Likely a separate-perspective agent (builder can't review itself well). | 📋 | 🟡 |
| **Convergence:** recategorize-ideas + mine-chronicle-fresh-eyes + idea-staleness + architecture-reassessment = ONE reflective-review pattern (a later pass re-judges in-the-moment work). Build once, apply many places. | 💡 | 🟡 |

## Constellation: interfaces, ownership & capability gaps — NEW 2026-06-07
*David thinking out loud: with 4-5 cooperating apps we need to understand what each solves, where each is deficient, and patch holes in the overall capability surface. Unifying frame (Marshall's synthesis, David broadly agreed): **the sentinel apps OBSERVE + ANSWER queries; only the factory floor (Marshall/Swaggers) ACTS.***
| Concept | Status | Pri |
|---|---|---|
| **Observers answer, the floor acts** — AngelEye/AppyCtrl/Switchboard = queryable sources of truth, NOT actors. "Stuck Swagger — whose job?" → mostly just **query capability** (AngelEye answers "is session X alive?"); Marshall queries + reaps. New tooling only if the query doesn't exist yet. | 💡 | 🟡 |
| **Every app = API + MCP-over-API** — API for harnesses/Monitors (curl); MCP for skills/agents (conversational). AngelEye HAS the API (`/api/sessions`); the MCP wrapper is the missing half. | 📋 | 🟡 |
| **AppyCtrl owns process/tmux state** — could hold all tmux sessions in memory, queryable by any system ("state of the tmux sessions now?"), paired with AngelEye's claude-session state. The clean home for the window→liveness mapping the reaper needs (process-tree is dead). | 💡 | 🟡 |
| **App owns its own features; build them THERE** — a cross-app need (e.g. AngelEye roll-ups/summaries) is written up as a requirement IN the target app and built with that app's own dev technique. Not all work flows through the factory (now; maybe later). | 💡 | 🟡 |
| **Capability-surface gap analysis** — periodically map each app's capabilities + deficiencies, decide which gap to fill where. The reflective-review/reassessment pattern applied to the CONSTELLATION (AngelEye already has a `gap-analysis-data-capture.md`). | 💡 | 🟢 |
| **AngelEye roll-ups/summaries** — capture is linear/temporal; rich roll-ups are an AngelEye feature (requirement in AngelEye, built there). Factory-controlled later, not now. | 💡 | 🟢 |
| **AngelEye doc port drift** — docs say `:5501`, server runs `:5051`; fix in AngelEye (fold into hook-refresh requirement), not from here. | 📋 | 🟢 |

---
*Add freely. Re-categorize as understanding sharpens. Expand a 📋 into a real spec when it reaches the top of the priority list — not before.*
