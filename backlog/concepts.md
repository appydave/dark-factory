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
| Reaper = harness-driven, NOT remembered: **staleness detector in Switchboard** (polls own process state + queries AngelEye session liveness; rule "no activity >10min + job done = stale") → pushes `session.stale`/`alert.*` → **Marshall's Monitor wakes + reaps**. Switchboard detects+tells (observe-only); Marshall acts. | 📋 | 🔴 |
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
| Concept | Status | Pri |
|---|---|---|
| Projects (folders) → epics → stories/tickets → importance | 📋 | 🟡 |
| Ticket priority/project/epic metadata (beyond queue_id/kind/prompt) | 📋 | 🟡 |
| Idle-time low-hanging-fruit triage (capture, don't distract) | 💡 | 🟡 |
| Port Symphony state machine (§7/§16) to the factory floor | 📋 | 🟡 |
| **This concepts register** (categorize ideas → specs over time) | 🔨 | 🟡 |

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

---
*Add freely. Re-categorize as understanding sharpens. Expand a 📋 into a real spec when it reaches the top of the priority list — not before.*
