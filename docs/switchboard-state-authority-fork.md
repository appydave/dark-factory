# Switchboard state-authority fork — decision artifact (Q3, T1-11)

**Status:** decision deferred (Q3 in `plans/wargames/decisions.md` line 9). This doc is the
tripwire map David asked for, not a verdict. **Verified 2026-07-08** (all commands below
re-run at authoring of this doc; re-verify before relying on any row past that date).

---

## 1. The fork

"State authority" = which system's record IS the truth about job state — the pool of
pending work, who claims each job, and its lifecycle (`pool → claimed → running →
done|failed`). Two candidates:

- **Branch A — filesystem store.** `engine/store/` flat JSON files, claimed via a
  `rename(2)` mutex, ownership now recorded (`claimed_by`/`claimed_at`).
- **Branch B — DF-7 durable Switchboard state plane.** A service-backed job-state plane
  inside `../switchboard` (`backlog/specs/df7-switchboard-state-plane-spec.md`), spec-only,
  never built.

Q3 ruling: **defer**. This document does not pick a winner — it maps both branches from
verified disk evidence and defines the triggers that would force a decision later.

---

## 2. Ground truth (verified 2026-07-08)

### Branch A — `engine/store/` consumers

| Module | Reads | Writes | Treats as truth |
|---|---|---|---|
| `orchestrator.py` | `queue/`, `running/`, ticket JSON | `rename(2)` queue→running (claim, `lease()` L215-234), running→done (`commit()`, L499), running→queue (requeue on reboot, L666-672) | The rename(2) result — exclusive-open-then-write ownership stamp (`claimed_by`/`claimed_at`, L227-228) |
| `wake.py` | `engine/store/queue/` mtimes, `.wake-state.json` | `.wake-state.json` debounce set, `wake.log` | launchd `WatchPaths` fire = "something changed"; gated by `WAKE-ARMED`/`HALT`/`BACKOFF`/`.wake.lock` (all flag-files under `store/`) |
| `consumer.py` | `engine/store/events/*.json` + `~/dev/ad/apps/omi-fetch/store/events/` | `events-consumed.jsonl` | Append-only consumed-log; never re-plays a recorded event |
| `status.py` | `queue/`, `running/`, `done/`, `results/`, `audit.jsonl` (read-only) | nothing | Derives every number fresh each run — no cached state of its own |
| `halt.py` | `engine/store/HALT` | `HALT` flag file | Presence/absence of one file, factory-wide, this-machine-only |
| `warm_pool.py` | tmux session state (`df-worker-<n>`) | reboots wedged sessions | Artifact-is-truth reaping — verifies a real file landed, never trusts REPL text |

Two facts that matter most to the fork:

- **(a) Ownership IS recorded today.** `orchestrator.py:227-228` stamps `claimed_by`/
  `claimed_at` into the ticket immediately after the `rename(2)` (`lease()`, confirmed
  read at L215-234) — this closes the gap DF-7 §2 calls "today's claim is anonymous."
  It is not anonymous; it has been closing that exact gap on the floor already.
- **(b) The wake wire is a filesystem poll, explicitly documented as the swap seam.**
  `docs/auto-wake.md` §7 (verified, last table row + closing paragraph): "When DF-7 lands,
  this filesystem watcher is the piece that gets swapped for a real SSE subscribe."

### Branch B — Switchboard: built vs specced

**Built** (`../switchboard/appysentinel.json`, verified verbatim):
```
"recipes": {
  "input": ["poll-command"], "storage": ["snapshot-store"],
  "interface": ["mcp-binding", "api-binding"], "transport": ["sse-deliver"],
  "enrichment": [], "runtime": ["register-as-launchd"],
  "coordination": ["staleness-detector"]
}
```
No `job-state-store`, no `job-coordinator`. `git -C ../switchboard log`: 6 commits, all
2026-06-06, newest `d1506ba` (topic-selective replay) — nothing since. One commit name
sounds close — `489117c "feat: durable + claimable job tickets"` — read in full: it makes
`POST /jobs` durable-write-first (`queue/<queue_id>.json`) before emitting `job.queued`; the
"claimable" part is that a **consumer** claims the file via the same `rename(2)` pattern as
the floor. Switchboard itself still implements **zero** claim/coordinator verbs:
`grep -rn "job-coordinator\|job_claim\|/jobs/claim" ../switchboard/src/` → **0 hits**.

**Specced but never built** (DF-7 §6–§8): `job-state-store` (storage recipe, one durable
record per job under `jobs/`), `job-coordinator` (coordination recipe: claim-by-id,
claim-next, complete/fail, liveness-keyed reap, lifecycle Signals), the HTTP+MCP verb table
(`POST /jobs/claim`, `/jobs/{id}/claim`, `/start`, `/complete`, `/fail`), and ownership
enforcement (`claimant` must match `claimed_by` or `409`).

**Liveness at verification time (Fork F1):**
- `curl -s -m 3 http://localhost:5099/health` → `EXIT:7` (connection refused — nothing
  listening on this machine).
- `launchctl list | grep -i switchboard` → no output (not loaded here).
- `curl -s -m 5 http://roamy:5099/health` → `EXIT:28` (timeout).
- `ssh -o ConnectTimeout=5 roamy '...'` → `ssh: connect ... port 22: Operation timed out`
  (SSH itself unreachable, not just the port).
- **Verdict: down/unloaded on this machine; Roamy is unverifiable from here, not confirmed
  down** (Assumption 2 — a timeout is not proof of absence; do not write "down on Roamy"
  from this alone). Route B of Fork F1 applies: the resurrection-cost line in §4 stays on
  Branch B's bill, and Roamy's status is recorded as unverifiable, not down.

---

## 3. Branch A — filesystem store stays truth

**What it gives:** a proven mutex (`rename(2)`) that now also records ownership — the
exact gap DF-7 was written to close already partially closed on the floor; zero new build;
no daemon commitment (no always-on service to keep alive, patch, or trust); the whole engine
already speaks it end-to-end (5 of 6 modules above operate against it daily).

**Hard ceilings:**
- Single-machine by construction — `rename(2)` is a local-filesystem primitive; two hosts
  cannot share one `queue/` this way without git-sync merge-hell (the exact failure mode
  DF-7 §2 rejects by name).
- Wake is a local poll (`launchd WatchPaths` on `engine/store/queue/`), not a push — cannot
  wake a worker on a different machine.
- No durable cross-restart replay for consumers other than the files themselves — there is
  no event log a second reader can catch up from.
- Cross-machine HALT/status is blind: `docs/kill-switch-spec.md` confirms HALT is a single
  flag file, checked only at decision points, with **no cross-process signal** — a second
  machine has no way to see it.

**Residual cost of staying on A:** ≈zero — no migration, no new service to operate.

**No-regret moves valid under either branch:** ticket retention (T1-10), golden-job replay
(T1-07), and keeping the ticket JSON schema stable — DF-7 §7's data model is a superset of
today's schema (verified field-by-field against a real ticket,
`engine/store/done/wg-t1-04-c4-return-leg.json`): `ticket`≈`queue_id` (renamed key, same
role), `kind` matches verbatim, `prompt` matches, `claimed_by`/`claimed_at` **already
present** on the floor (not a DF-7-only field), `requested_by`/`requested_at` match. DF-7
adds `experiment_id`, `workflow`/`args` (workflow-kind tickets), `state` (currently implicit
in directory location), `started_at`/`ended_at` (currently absent — timing lives in
`audit.jsonl` instead), `result`/`error` as first-class fields (currently split across a
`verify` field on the ticket and a separate `results/<ticket>.json` handback), and
`attempts` (currently tracked only in the orchestrator's in-memory `retries` dict, never
persisted to the ticket). None of these are contradictions — DF-7's model was designed to
absorb today's shape plus the fields the floor never persisted.

---

## 4. Branch B — DF-7 durable state plane

**What it unlocks:** N thin clients on one state plane (parallel Marshalls); factory
portability (state not tied to `dark-factory/`'s working directory); SSE wake in place of
filesystem polling; durable cross-restart replay; ownership enforced *in the service*
(`409` on claimant mismatch) rather than only recorded after the fact.

**The honest bill:**
1. **Resurrect Switchboard.** Down/unloaded here; Roamy unverifiable (§2). Per locked
   context, this ticket does not start it — the cost is "bring a stopped service back up
   and confirm it still loads its recipe set," an unknown-until-tried step, not a known
   quantity.
2. **Re-baseline the spec against today's engine** — §5 below; the spec targets a retired
   floor.
3. **Build 2 recipes + 7 verbs** (`job-state-store`, `job-coordinator`; `claim-next`,
   `claim-by-id`, `start`, `complete`, `fail`, plus read verbs) modeled on the existing
   `staleness-detector`/`snapshot-store` shape (DF-7 §6, §14).
4. **Run the §11 four-step shadow→cutover** (shadow-write, read-shadow-compare, flagged
   cutover, retire floor) — each step independently reversible, but four real steps.
5. **Accept an always-on Bun/TS daemon as a standing commitment** — launchd-managed,
   someone's job to keep patched and alive; today nothing depends on Switchboard staying up.
6. **Inherit the event-log growth gap.** Switchboard's durable log has the same
   grow-forever characteristic the engine's own `audit.jsonl`/`events/` has today
   (`docs/unknowns-map.md` §E) — moving state does not solve retention, it relocates it.

---

## 5. Re-baseline table — DF-7 spec vs today's engine

The spec (`backlog/specs/df7-switchboard-state-plane-spec.md`, authored 2026-06-09) targets
`experiments/watchtower-engine/`, retired-but-present on disk, superseded by `engine/` on
2026-07-04. `grep -c "claim-next\|run-next-workflow\|WT_STATE_PLANE"` on the spec → **11**
hits (matches the war game's authoring-time count exactly — the spec has not been
re-baselined since). Mapping, verified against Move 1's file+line evidence:

| Spec reference (old floor) | Today's equivalent | Migration note |
|---|---|---|
| `bin/claim-next.sh` — `rename(2)` mutex, anonymous claim | `orchestrator.py` `lease()` (L215-234) — `rename(2)` **+ recorded** `claimed_by`/`claimed_at` | Branch B's "lift the mutex into the service, recording ownership" now starts from a **richer** client than the spec assumed — ownership recording is already done on the floor; the service only needs to make it atomic *across machines*, not invent it |
| `run-next-workflow` lifecycle (claim → execute → report) | `orchestrator.py`'s dispatch/verify/settle loop + `warm_pool.py`'s tmux-session reuse | The §10 thin-client mapping (claim→start→execute→complete/fail) still applies 1:1; the executor is now a persistent tmux worker pool, not a one-shot script per job |
| `WT_STATE_PLANE=service` env flag (§11 step 3) | Would gate `orchestrator.py`'s claim/commit paths, not a shell script | Same flip-flag *shape*, different owner — the cutover point moves from a bash conditional to a Python one |
| `experiments/watchtower-engine/{queue,running,done,reports}/` | `engine/store/{queue,running,done,results}/` | Directory names differ (`reports/`→`results/`) but the four-stage shape is unchanged; migration script would need this rename accounted for |
| `bin/reaper.sh` — `done/`-mtime-keyed reaping | `orchestrator.py`'s in-process reboot/retry (wedge detection via tmux pane content, not `done/` mtime) | The spec's own §9 already prefers AngelEye-liveness reaping over the old mtime approach — today's engine has *also* moved off mtime-keying independently, converging with the spec's intent from a different direction |
| §7 job-state data model | Today's ticket JSON (see §3 field-by-field above) | Confirmed superset; no field conflicts found |
| §11 four-step shadow→cutover migration | Not started; carried forward unchanged as the plan **if** Branch B is ever chosen | No current equivalent — this is forward-looking design, not a stale reference |
| D1–D5 rulings (§12) | Not yet consumed by any build | Carried forward unchanged (§8 below) — these govern HOW if/when Branch B starts, not IF |

**Holes found:** one — `bin/reaper.sh`'s mtime-keyed reaping has no direct file in
`engine/` (it was replaced by a different mechanism, tmux-content wedge detection, not a
port of the old reaper). This is a single hole, not a blocker (Move 3's threshold for
"bigger job than a mapping table" is >3 holes) — recorded here as a Branch B prerequisite:
a future build should confirm the tmux-wedge detector covers every case the old mtime
reaper did before treating reaping as solved prior art.

---

## 6. Prerequisites Branch B inherits

- Switchboard's own ownership/liveness story would need to exist before DF-7's reaper
  (§9) can key off AngelEye liveness as designed.
- The greenfield charter question is still open (§7 below, Fork F2) — Branch B's build
  order and framing may depend on whatever that charter eventually rules.
- D2's AngelEye session-id contingency ("⚠️ contingent on AngelEye exposing a stable
  session-id — verify before build") is unverified as of this doc; it is a build-time
  precondition, not yet checked.

---

## 7. Charter status (Fork F2)

Recon confirms the KICKOFF/seed/grounding trio exists (`backlog/2026-06-09-switchboard-
greenfield-KICKOFF.md`, `-seed.md`, `-charter-grounding.md`) but no charter OUTPUT —
`grep -rln "greenfield charter" docs/ ../switchboard/ | grep -v backlog` returns only two
unrelated KDD learning docs, neither the charter itself. The grounding doc states this
itself: "This is the INPUT to `/agent-skills:spec`, not the charter." T8-09 (the sibling
war game meant to feed this one — `backlog/wargames/T8-09-switchboard-charter-recon.md`)
has **not been executed**: no `docs/switchboard-charter-recon.md`, no
`engine/store/{done,results}/` entry for it. **Route B applies** (charter still unwritten):
this document doubles as a primary input to that future charter and says so here.

---

## 8. Triggers

Each row's observation is an executable command or an unambiguous event; the "status
today" column is dated and was run against the live system, not inferred.

| # | Trigger | Observation | Forces / leans | Status today (2026-07-08) |
|---|---|---|---|---|
| 1 | Second machine dispatches work | `grep -h claimed_by engine/store/done/*.json engine/store/audit.jsonl \| grep -v "$(hostname)"` returns rows from a **different host** | Forces B | **Fired, ambiguous — Fork F3 Route B.** Returns 16 rows, all `claimed_by: "fable-orchestrator"` — a synthetic claimant used when tickets were filed *retroactively* by the Fable orchestrator session directly (bypassing the engine's rename(2) claim path entirely — see `engine/store/done/20260704T0230Z-omi-fetch-v2.json`, `"note": "retroactive — filed after dispatch; the miss that triggered the ticket-first rule"`). This is same-machine, different code path — not a second host. `audit.jsonl`'s own claim records (the rename-path audit trail) are 100% `mac-mini-m4.local-pid*`. Trigger stands armed for a recurrence with an actual foreign hostname. |
| 2 | Anyone proposes syncing `engine/store/` across machines via git/rsync | Such a plan/backlog item appears | Forces B immediately | Quiet — no such proposal found in `backlog/` |
| 3 | Double-claim or lost-ticket incident | Same ticket filename claimed twice in `audit.jsonl`, or a `running/` entry whose `claimed_by` pid is dead with no requeue | Forces B's ownership/liveness plane | Quiet, with one look-alike: this very ticket (`wg-t1-11...json`) shows 4 claim records across 3 different pids over 2026-07-08 in `audit.jsonl`. Not a double-claim — sequential re-claims after wedge/reboot retries (the documented `MAX_RETRY` reap path, `orchestrator.py` L666-672), same host throughout, no concurrent overlap. |
| 4 | Cross-machine wake needed | First fleet-delegation war game needing a queue-drop on one machine to wake a worker on another | Forces B's SSE leg | Quiet — no fleet-delegation war game has run yet (Q8 fleet is "in" per decisions.md but not yet exercised) |
| 5 | Cross-machine HALT needed | A HALT incident where a second machine kept running | Forces B's bus | Quiet — confirmed HALT is single-file, single-machine, no cross-process signal (`docs/kill-switch-spec.md`); no incident on record |
| 6 | Watchtower real app consumes live job state | A T5 build ticket needs job state over HTTP/SSE rather than local file reads | Leans B (a read-only projection could bridge it without a full fork) | Quiet — no such ticket found |
| 7 | Factory portability in anger | Engine driving jobs whose working state must follow work into other repos/machines (DF-7 §2 goal 2) | Leans B | Quiet — engine still operates only against `dark-factory/`'s own `engine/store/` |

**Counter-triggers (entrench A):** Switchboard stays down with no owner assigned to bring
it back (true today); fleet work deferred again past Q8's "in" status; the always-on-daemon
posture stays unwanted per the no-standing-daemon-without-a-go rule
(`docs/unknowns-map.md` §B) and the metered-billing caution that keeps this and other
tickets on interactive `claude` only.

---

## 9. Default posture

**Branch A remains truth until a forcing trigger fires.** Leaning triggers (#6, #7)
accumulate as pressure but do not flip authority by themselves. Any flip is a David ruling —
via `needs-decision/` or triage — never an executor call. This is Q3's "defer" restated as
a standing default, not a new decision. Trigger #1 fired today in ambiguous form (§8) and
does not, on its own evidence, force the fork — it is recorded as an armed trigger with one
near-miss, not as a resolution.

---

## 10. Standing rulings honoured

- **D1–D5** (`backlog/specs/df7-switchboard-state-plane-spec.md` §12, David 2026-06-09) —
  by reference, unchanged: file-per-job JSON (D1), AngelEye session-id as `claimed_by` (D2,
  contingency unverified — §6), MCP-first with HTTP retained (D3), coordinator may requeue
  dead-claimant state but never kill a process (D4), coordinator records `attempts`/client
  owns retry (D5).
- **Constellation placement rule** (`docs/dark-factory-constellation.md`): shared state
  belongs in services, the floor is a stateless client — "second orchestrator" means N
  thin clients on one plane, never repo-cloning. Unaffected by which branch wins; both
  branches already agree on this rule, they differ only on whether the plane is a
  filesystem or a service today.
- **Voice law** (`docs/comms-flow.md` §8): voice-triggered surfaces stay read-only
  regardless of which branch holds state — a mutation always goes through the same
  file-contract/queue path, never a direct voice-to-mutation shortcut. Neither branch
  changes this.

---

## 11. Contradictions found (docs-lag ledger)

Recorded as findings for T8's truth-reconciliation work — none fixed here beyond the two
pins in §12:

- `docs/comms-flow.md` line 39 states Switchboard is "**live on MacBook Pro `:5099`/`:5100`**".
  Verified today: refused on this machine, timeout+unreachable-SSH on Roamy. Not live from
  either vantage point checked.
- `docs/dark-factory-constellation.md` line 64 calls Switchboard's state role
  "**substantially built**". True of the bus/observer half (SSE, MCP, `POST /jobs`
  durable-enqueue); false of the state plane specifically — zero claim/coordinator verbs
  exist (§2).
- `docs/auto-wake.md` §7 cites "this repo's `CLAUDE.md` — 'Switchboard is DOWN'" as the
  reason for the filesystem-wake divergence. Verified: `CLAUDE.md` today does not mention
  Switchboard at all (`grep -n -i switchboard CLAUDE.md` → no hits). The citation is stale;
  the underlying claim (Switchboard is down) is still independently true per §2's liveness
  sweep, just no longer sourced from that file.
- The DF-7 spec's own client contract (`bin/claim-next.sh`, `run-next-workflow`) targets
  `experiments/watchtower-engine/`, retired 2026-07-04 in favor of `engine/` — §5 above is
  the re-baseline this contradiction requires.

---

## 12. Cross-links (this ticket's two edits)

- `docs/INDEX.md` — one line added in the contracts/decisions region pointing here.
- `backlog/specs/df7-switchboard-state-plane-spec.md` — status banner added under its
  title pointing here.
