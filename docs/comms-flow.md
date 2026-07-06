# Dark Factory — Switchboard/Watchtower Communication Flow

**Purpose**: Pin the event/ticket/acknowledge flow between David, the factory's orchestrator/worker sessions, and the human-facing surfaces (Switchboard, Watchtower, +AngelEye/AppyRadar as data sources) — so builds can target one shared shape instead of each app inventing its own. Answers David's framing directly: communication is three-directional (David→factory, factory→David spoken, factory→David visual), and Switchboard+Watchtower exist to "communicate and acknowledge between David, the AI, and what's being built."

**For Agents**: This is a synthesis doc, not a new spec — every claim below traces to an existing spec or a shipped app. Where sources disagree or a piece is still spec-only, it's named, not smoothed over (see §7). Read `suborch-demo/CONTEXT.md` first if you need the deepest mechanics; this doc is the promotion of its laws into the dark-factory-wide picture.

**Created**: 2026-07-03
**Status**: canonical — describes what's real today plus what's specced; re-check against `constellation-map.md` before trusting a status claim (it rots — see that doc's own lesson).

---

## 1. The triad

```
                 ┌─────────────────────────┐
   David ──────▶ │                         │   David → factory
   (OMI voice)   │       THE FACTORY       │   "speak to it" — omi-fetch pulse (live)
                 │  Marshall → Swagger      │
   David ◀────── │  workflows/agents        │   factory → David, VERBALLY
   (kokoro-tts,  │  Switchboard (data/bus)  │   status, completions, exceptions
    unwired)     │  Watchtower (decisions)  │
                 │                         │
   David ◀────── │                         │   factory → David, VISUALLY
   (stores,      └─────────────────────────┘   tickets/projects/decisions in flight
    UI stubs)
```

David directs by talking (never types a ticket by hand day-to-day); the factory must close the loop back two ways — a voice that speaks and a wall of glass that shows. Today only the first leg (David→factory) is live end-to-end. The other two exist as proven *pieces* (kokoro-tts, store schemas, a stub UI) with no wiring between them yet — that gap is the point of this doc.

---

## 2. The actors

| Actor | Role | Where |
|---|---|---|
| **David** | Director. Talks to the factory (OMI), reads/hears back. Never on the floor. | — |
| **Marshall** | The orchestrator/conductor. Holds the single Monitor, routes tickets to job-agents, reaps on completion. Routes; does not coordinate. | `.claude/skills/marshall/` |
| **Swagger** | The job-agent. One per job/ticket, root of a tmux-pane cluster, runs workflows and/or sub-agent panes with judgment. Isolated — never talks to another Swagger. | dispatched via `tmux new-window` |
| **Switchboard** | Headless data plane. Today: passive observer (SSE+MCP, polls `ps`/`tmux`/`pgrep`), `POST /jobs` enqueue+emit. Specced-not-built: full job-state plane (claim/start/complete/fail, ownership, liveness reaping). | `~/dev/ad/apps/switchboard`, live on MacBook Pro `:5099`/`:5100` |
| **Watchtower** | The decision-queue surface — "what needs me," capped, never a full dashboard. Today: design doc only + a 1-commit RVETS stub. | `docs/watchtower/`, `apps/watchtower` (stub) |
| **AngelEye / AppyRadar** | The "+ maybe one more app" — Watchtower's other two data sources: AngelEye (session liveness), AppyRadar (tmux/process liveness across machines). Watchtower visualises all three (Switchboard, AngelEye, AppyRadar) together, per the app-pipeline candidate. | `apps/angeleye`, `apps/appyradar(-sentinel)` |
| **The micro-app stores** | Loose-coupling event/state producers any consumer can poll. omi-fetch (`store/events/*.json` — the first real event producer, live), app-registry (`store/registry.json`, live, no events yet), project-digest (specced, not built — the status-out gate-opener). | each app's `store/` |

---

## 3. The flows

### (a) Direction-in — David speaks, a ticket should result

```
David (OMI voice) ──▶ omi-fetch pulse (launchd, ~10min)      [LIVE]
                          └─ archives to raw-intake/
                          └─ writes store/events/<id>.json    [write-only, no reader yet]
                                                    │
                                    ▼ MISSING — no consumer turns this into a ticket
                          (today: David/a session reads the capture by hand,
                           decides what's ticket-shaped, writes queue/ manually)
```
The channel is real and shipped (`omi-fetch`, 2026-07-03). The synapse from *event landed* to *ticket exists* is not wired — this is exactly the "C3 auto-wake" gap in reverse: omi-fetch produces events nobody consumes yet, same shape of gap as job.queued nobody was subscribed to before C3 was specced.

### (b) Work dispatch — ticket → done, the proven doing-loop

```
queue/<ticket>.json ──rename(2)──▶ running/<ticket>.json      [claim-next.sh, 200×8 stress-proven]
                                       │
                                dispatch-swagger.sh: tmux new-window "claude '<prompt>'"
                                       │
                              Swagger runs run-next-workflow (workflow and/or sub-agent panes)
                                       │
                     artifact lands ──▶ done/ + reports/<ticket>.json   [artifact-is-truth]
                                       │
                     Marshall reaper: tmux kill-window on done/          [external-signal teardown]
```
This chain is **proven by hand** — 35 real jobs through it (`c3-marshall-auto-wake-spec.md` §3). What's missing is the **trigger**: Marshall today is invoked by a human typing "process the queue." The auto-wake wire (Marshall's Monitor subscribes to Switchboard's `job.queued` SSE topic, tracks `Last-Event-ID`, dispatches on wake) is **DF-10/C3 — spec only, not built**.

> **Reference mechanics, not yet ported**: `suborch-demo`'s warm-pool (reusable tmux REPL + `send-keys`, boot paid once) and CAS-lease-with-`results/` are a *faster, more mature* version of the same primitives, proven in the POC — but dark-factory's real engine still cold-spawns one `tmux new-window` per ticket. The POC is prior art David explicitly parked for later adoption ("concepts proven here get rebuilt properly" — `constellation-map.md` §3), not the live mechanism.

### (c) Needs-David — a decision blocks the loop

Two distinct shapes exist, not yet merged:

```
CURATION queue (Watchtower's actual design):
  experiment.yml/run.json/learning.yml ──▶ Watchtower reads, human clicks Promote
                                        ──▶ writes promotion.yml (records verdict only,
                                            NEVER mutates canonical/ — a human does that edit)

MID-TASK HITL gate (suborch's PROVEN pattern, not yet in dark-factory's real Swaggers):
  worker hits a judgment call ──▶ writes needs-decision/<tid>.json (question + options + "my take")
                                ──▶ idles at the REPL (blocked, not exited)
  David ──▶ drops decisions/<tid>.json {approve|decline|redirect}
                                ──▶ orchestrator send-keys the decision into the live worker
                                ──▶ worker resumes; completion still gates on the real artifact
```
Both are "decision queue, not dashboard" in spirit — cap the list, show only what needs a human — but they are mechanically different systems today. Watchtower's curation queue has a design doc + a stub app; suborch's blocking gate is proven end-to-end (approve/decline/redirect all demonstrated) but lives only in the POC. **Neither is wired to an attention alert** — the "charm/sound so David doesn't have to poll" requirement is named (`app-pipeline/watchtower.md`, 2026-07-02 addendum) and built nowhere.

### (d) Status-out — stores → something David can see or hear

```
omi-fetch/store/index.jsonl  ─┐
app-registry/store/registry.json ─┼──▶  MISSING: a digest/briefing reader
project-digest (specced, not built) ─┘        │
                                                ▼
                                   Watchtower UI (stub) / kokoro-tts (unwired) /
                                   a session summarising by hand (today's actual path)
```
Every store is independently queryable right now (`query.py running|drift|stale`, `index.jsonl` filters) — but nothing regularly reads across them and either speaks it (kokoro-tts exists as a skill, wired to nothing) or renders it (Watchtower is a 1-commit stub; Mochaccino visualises *designs*, not live state). Today's real status-out path is David asking a session to look.

---

## 4. File-contract conventions (the factory's actual convention, proven three times)

Every shipped micro-app (omi-fetch, app-registry, watchtower-engine) and the POC (suborch-demo) independently converged on the same idiom — treat this as **the** dark-factory store convention, not a per-app choice:

| Convention | Meaning | Seen in |
|---|---|---|
| `store/` under the trusted repo path | Never `/tmp` — triggers Claude Code's folder-trust dialog and silently stalls a worker forever | suborch Law 6; every shipped app |
| `state.json` | One overwriting snapshot — "last known good," not history | omi-fetch (`last_pulse_ts`), snapshot-store pattern |
| `index.jsonl` / `registry.json` | The durable ledger — append-only or full-snapshot record set, reads like a REST resource shape on purpose | omi-fetch, app-registry |
| `events/*.json` | Write-only, loose-coupling fact drops — "something happened," no reader assumed | omi-fetch (built); app-registry (named gap, not built) |
| `queue/ → running/ → done/|failed/` + `rename(2)` | Atomic claim, zero infrastructure — the OS guarantees exactly one claimer wins | watchtower-engine, suborch-demo (same primitive, different vocab: "CAS lease") |
| `audit.jsonl` | Append-only run history for the observer to tail | suborch-demo `store/audit.jsonl` |
| **One-write rule** | Each store owns exactly one piece of mutating state (project-digest: only a last-briefing timestamp; Watchtower v0: only `promotion.yml`, never `canonical/`) | daily-operating-model.md, watchtower-control-surface.md |

Consumers **poll or scan** these files; nothing pushes today except Switchboard's SSE fan-out of `job.queued` (which nothing outside the POC subscribes to yet — Marshall's Monitor subscribing is exactly what C3 specs).

---

## 5. What exists vs what's missing

| | Exists | Missing |
|---|---|---|
| **Direction-in** | omi-fetch pulse live, archives + writes events (2026-07-03) | No consumer turns an event into a ticket — still a human's judgment call |
| **Dispatch engine** | rename(2) claim, dispatch, reap — proven, 35 real jobs, 200×8 stress test | Auto-wake trigger (DF-10/C3) — **spec only** |
| **Switchboard** | Live observer: SSE+MCP, `ps`/`tmux`/`pgrep` polling, `POST /jobs` enqueue+emit, zero-coupling `swagger-*` visibility | Full state plane — claim/start/complete/fail, ownership, liveness reaping (DF-7) — **spec only** |
| **Watchtower** | Design doc (decision-queue-not-dashboard, in-session execution, files-as-truth) | The app itself — 1-commit stub; no UI surfaces `needs-decision/` or `promotion.yml` today |
| **HITL gate** | Proven in suborch-demo (approve/decline/redirect, native, subscription-safe) | Not ported into dark-factory's real Swagger workers |
| **Voice-out** | kokoro-tts skill exists, local, free | Not wired to any event or status source |
| **Attention alerts** | Named requirement (charms/sounds, "pull don't demand polling") | Zero implementation anywhere |
| **Status-out digest** | Every store is independently queryable (`query.py`, `index.jsonl`) | project-digest generator not built (even for one project); no cross-store reader |
| **Cross-machine transport** | Switchboard reachable via Tailscale (MacBook Pro); constellation.json names the fleet | omi-fetch/app-registry are machine-local only; app-registry's own docs name this its biggest gap |

---

## 6. Constraints (why the gaps are shaped this way)

- **Subscription-safe, always.** Every dispatch step uses interactive `claude` (`--bg` / `tmux new-window`), never `-p` or the Agent SDK — metered billing since 2026-06-15 makes headless execution a real cost, not a style choice. This is why Watchtower's "Run" button only *writes a queue entry* rather than spawning anything directly, and why Marshall's future auto-wake is an in-session Monitor + SSE subscription, not a cron job or webhook handler.
- **Imperfect-now, document-always.** omi-fetch and app-registry both shipped v1 with named, undone stage-2 work (LLM classify/route, transition events, cross-machine probing) rather than waiting for full design — the rule from the 2026-07-03 direction. This doc inherits that posture: the gaps in §5 are declared, not hidden, so the next build knows exactly what it's closing.
- **KBDE seam later, not now.** Both shipped micro-apps already draft their ③ Data / ④ Events channel mapping (`docs/extension-notes.md` in each) against the KBDE capability model — but Layer-2 surface work (a real Watchtower *extension*) is blocked until the Extension SDK handover lands (`constellation-map.md` Build constraint #2). Layer-1 data sources (omi-fetch, app-registry, and eventually Switchboard-state-as-data) are **not** blocked and are exactly what's shipping now.

---

## 7. Contradictions/gaps found while writing this (named, not resolved)

1. **Two "decision queue" concepts share a name but not a mechanism** — Watchtower's curation queue (promote/reject a canonical skill) vs suborch's mid-task HITL gate (approve/decline/redirect a running worker). Both are real, both are "decision queue not dashboard," neither has been reconciled into one system.
2. **Switchboard is described three different ways across sources**, only reconciled by date: `app-pipeline/switchboard.md` (2026-06-13) says it "doesn't exist," `suborch-demo` calls it a passive zero-coupling *observer*, and `df7-switchboard-state-plane-spec.md` (2026-06-09, still SPEC ONLY) describes it as the future full *state plane*. All three are simultaneously "true" of different maturity stages of the same app — read the date, not just the claim.
3. **Two dispatch mechanisms, not one.** suborch-demo's warm-pool + CAS lease is proven and faster; dark-factory's real engine (`watchtower-engine`) still cold-spawns a `tmux new-window` per ticket. The POC is explicitly reference architecture ("concepts proven here get rebuilt properly in #1"), not yet adopted — a reader could easily assume the warm-pool IS the live mechanism; it is not.

---

## 8. Voice law — voice-triggered surfaces are read-only

**Voice-triggered surfaces are constitutionally READ-ONLY (explain/report only, never mutate)** [source: Mark Kashef v3 Jarvis pattern + David go 2026-07-06].

David directs the factory by talking (§1) — but "David spoke a command" must never, by itself, be sufficient authority for a mutating action (a ticket claim, a canonical edit, a HALT/resume, a commit). A voice surface may **read** state and **report** it back (status, completions, exceptions — the "factory → David, VERBALLY" leg in §1's triad) but any action that changes factory state still goes through the same file-contract/queue path everything else does (`queue/` → `running/` → `done/`, or a human-written `decisions/<tid>.json`, per §3b/§3c) — never a direct voice-to-mutation shortcut. This closes off the failure mode where a misheard or ambiguous utterance silently mutates state with no artifact trail — the same "artifact-is-truth" principle (§4, `docs/comms-flow.md`) applied to the input side, not just the output side.

---

## Related

- `~/dev/ad/apps/suborch-demo/CONTEXT.md` + `PHASE-5-PLAN.md` — the proven kernel mechanics this doc promotes
- `~/dev/ad/brains/dark-factory/watchtower-control-surface.md` — Watchtower's design law
- `~/dev/ad/brains/dark-factory/app-pipeline/{switchboard,watchtower}.md` — the (partly stale) app-pipeline candidates
- `docs/runtime-model.md` — Marshall/Swagger roles
- `docs/north-star.md` — why in-session execution is non-negotiable
- `docs/constellation-map.md` — the whole-stack map this doc's actors are drawn from
- `backlog/specs/c3-marshall-auto-wake-spec.md`, `backlog/specs/df7-switchboard-state-plane-spec.md` — the two named SPEC-ONLY gaps this doc leans on most
