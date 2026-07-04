# Engine Notes — what was promoted from where, and why

Companion to `docs/harness-evaluation.md` (the authority this build follows). That doc is
the evaluation; this is the as-built record — what actually landed in `engine/`, file by
file, against the evaluation's promotion plan.

## Promotion table (plan vs what landed)

| Mechanism | Evaluation's verdict | What landed in `engine/` |
|---|---|---|
| Dispatch | Promote suborch's `warm_pool.py` | `engine/warm_pool.py` — ported near-verbatim from `suborch-demo/warm_pool.py`. Only changes: tmux sessions renamed `df-worker-<n>` (visibility requirement — `tmux ls` / `tmux attach -t df-worker-1`), default pool size 1 (real jobs, not 3 cheap trivia workers). |
| Claim/lease | Keep dark-factory's `rename(2)`, add ownership recording | `engine/orchestrator.py:lease()` — same CAS mutex as `claim-next.sh`, extended: the instant the rename wins, the ticket JSON is rewritten with `claimed_by` (host+pid) and `claimed_at` (ISO ts). Closes the gap both dark-factory and suborch shared (evaluation row 2). |
| Reaping | Keep dark-factory's artifact-is-truth, import suborch's starvation fix | `engine/orchestrator.py`: reap gates purely on `artifact_ok()` (a real file, `results/<ticket>.json`) + a ticket-specific `verify()` — never on a worker's chat reply or a `state==done` flag. This IS the fix suborch found the hard way (546s/9-of-10 -> 52s/10-of-10 once it stopped trusting `state==done`). |
| State model | Rebuild fresh, per DF-7 (future) | NOT rebuilt here — DF-7's service-backed plane is explicitly future work per the day's build instructions ("DF-7 service plane is FUTURE — do not build it"). `engine/store/` stays flat files, dark-factory's existing convention, seeded with suborch's `audit.jsonl` shape (ticket -> worker -> session_id -> transcript) as instructed. |
| HITL | Promote suborch's gate wholesale, additively | `engine/orchestrator.py` — `needs-decision/<tid>.json` -> `decisions/<tid>.json` -> `send-keys` resume, ported natively (`task_prompt(gated=True)`, `resume_prompt()`, the block/resume loop). Present and wired, gated via `--hitl <ticket>`. NOT exercised on the real proof ticket (by design — see the day's build instructions). |
| Observability | Keep switchboard, add suborch's audit trail | `engine/store/audit.jsonl` is net-new (K3 from the evaluation) — ticket/attempt/worker/session_id/transcript/claimed_by/claimed_at per dispatch. Switchboard itself is untouched — out of scope for this build. |
| Events consumer | Named as "the missing brick" | `engine/consumer.py` — net-new, not in either lineage. Polls `engine/store/events/` AND `~/dev/ad/apps/omi-fetch/store/events/`, appends to `engine/store/events-consumed.jsonl`, plays `afplay Glass.aiff`. Closes `docs/comms-flow.md` §5's "events have no consumer" gap for the first time, for two producers. |
| Concurrency governor (CAP=N) | Promote suborch's CAP gate | **Not built.** Out of the day's explicit build scope (not listed under "Build scope"). With default pool=1, `pool.free_worker()` already caps concurrency at the pool size — but there is no separate 429-wall admission-control gate above that. Named honestly as a gap, not silently skipped: build it before any pool size >1 goes into real multi-ticket use. |
| DF-7 state plane | Future | Not built, per explicit instruction. |
| Auto-wake (DF-10/C3) | Orthogonal, build separately | Not built — out of scope for this session. The engine as built still needs a human (or a future Marshall Monitor) to invoke `orchestrator.py`; it does not yet wake itself on a Switchboard `job.queued` SSE. |

## Divergences from suborch's shape (deliberate, not oversights)

- **No `reset()`.** suborch wipes its whole store every run (a disposable 10-toy-task
  harness). This engine's store is a growing ledger — `done/`, `audit.jsonl`,
  `events/`, `events-consumed.jsonl` all accumulate across runs, matching dark-factory's
  actual convention (`comms-flow.md` §4's "one-write rule" / durable ledger idiom).
- **No hardcoded `TASKS` dict.** suborch's kernel processes exactly 10 predefined
  toy tickets. This engine scans `store/queue/` fresh every poll pass — any ticket
  file dropped in (by a human, a future omi-fetch-driven auto-ticket-writer, or a
  future Switchboard wake) gets picked up, not just a fixed list.
- **Worker cwd is the repo root**, not the engine store. suborch's workers run with
  `cwd=STORE` because its tickets are self-contained toy prompts. dark-factory's real
  tickets reference ordinary repo-relative paths (`mochaccino/data/constellation.json`)
  the way a human operator would type them, so workers need the actual repo root as
  their working directory. The ticket file itself is still handed to the worker as an
  absolute path (SPK-D1 — pointer, not payload).
- **Verification is two-layered, not one.** suborch's `artifact_ok()` is "does
  `results/<tid>.txt` exist and have bytes" — suficient for toy trivia where the
  artifact IS the whole deliverable. Here, `results/<ticket>.json` is the worker's
  self-report (necessary, catches "did it even finish"), but `verify()` independently
  re-opens the REAL deliverable files and checks them against the ticket's own
  acceptance criteria (`verify_kind: "constellation-4-apps"` — JSON parses, the 4 new
  app ids are present, the embedded HTML copy matches). A ticket only reaches `done/`
  when BOTH pass. This is artifact-is-truth taken one level more seriously than either
  prior lineage needed to, because a real ticket's "artifact" is usually a diff to an
  existing file, not a fresh file from nothing.

## Known limitations (named, not hidden)

- No CAP=N 429-wall governor (see table above) — fine at pool=1, a real gap at pool>1.
- No auto-wake — a human (or a future skill) still has to run `orchestrator.py` by hand.
- ~~`verify()`'s `VERIFIERS` dict currently has exactly one entry...~~ **Closed
  2026-07-04** (ticket `engine-status-and-verifiers`, per
  `docs/six-app-evaluation-2026-07-04.md` #5). `VERIFIERS` is now a registry:
  `constellation-4-apps` unchanged, plus a `generic` declarative check DSL
  (`verify_spec.checks[]` — `file_exists` / `json_parses` / `must_contain` /
  `git_commit_present` / `script` / `command`, each a small function in
  `CHECK_REGISTRY`) and an `artifacts`/`verify_command` fallback for tickets with no
  `verify_kind` at all. A new ticket kind composes existing check types instead of
  needing a bespoke Python function — see `engine/README.md`'s "Verifying a new
  ticket kind" section. Exercised via a dry lifecycle (`lease()` -> simulated
  worker self-report -> `verify()` -> `commit()`, no warm pool booted) before being
  trusted against real tickets.
- ~~There is zero aggregation...~~ **Closed 2026-07-04** (same ticket).
  `engine/status.py` now reads `store/queue/`, `store/running/`, `store/done/`,
  `store/results/`, and `audit.jsonl` and prints queue depth + oldest-ticket age,
  running tickets + claimant, last N done outcomes, live `df-worker-*` tmux
  sessions, and the last N audit lines — human report by default, `--json` for
  agents. No new state; pure aggregation over the existing ledger.
- HITL gate is ported and wired but has not been exercised end-to-end inside THIS
  engine (only inside suborch's own prior proof runs) — `--hitl` is present, untested
  here beyond a code read. Flag this explicitly if David wants a live HITL demo before
  trusting it under real stakes.
- Switchboard integration (naming workers so switchboard's existing collector sees
  them "for free") is NOT wired here — `df-worker-*` is a distinct naming scheme from
  suborch's planned `swagger-*`. If/when switchboard's collector is pointed at this
  engine, either rename the workers or extend switchboard's pattern match.

## Proof run

See the end-of-session report in the backlog item / session transcript for the actual
evidence chain (tmux ls, audit.jsonl lines, artifact diff, events-consumed.jsonl line,
commit hashes). This file documents the promotion decisions; it is not the proof itself.
