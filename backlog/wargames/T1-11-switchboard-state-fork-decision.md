# T1-11 — DECISION war-game: Switchboard state-authority fork

| field | value |
|---|---|
| ticket | wg-t1-11-switchboard-state-fork-decision |
| track / size / priority | T1 Engine / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none (soft input: T8-09 charter recon — read its output if it exists, do not block on it) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Per decisions.md Q3, David DEFERRED the state-authority fork: does `engine/store/` (flat files,
rename(2) claims) stay the truth about job state, or does truth move to the DF-7 durable
Switchboard state plane (`backlog/specs/df7-switchboard-state-plane-spec.md`)? This ticket
produces a DECISION ARTIFACT, not a build: `docs/switchboard-state-authority-fork.md`, mapping
both branches with verified ground truth, honest costs, the observable TRIGGERS that would
force the fork later, and the default posture in the meantime. Done looks like: the doc exists
with every pinned section filled from disk evidence (not doc claims), each trigger carries an
executable observation command plus its status-today result, the doc is linked from
`docs/INDEX.md`, the DF-7 spec carries a status banner pointing at it, and NOT ONE line of
engine or Switchboard code changed. The decision itself is NOT made here — unless a trigger has
already fired (Fork F3), in which case the question is parked to David.

## Locked context

- **Q3 (decisions.md):** Switchboard state fork = **defer** → this decision war-game with both
  branches + triggers. Do not pick a winner; define what would pick it.
- **Q4 (decisions.md):** everything through the engine — this ticket runs as a sonnet Swagger
  dispatch and self-reports to `results/`.
- **Q8 (decisions.md):** fleet is IN (+Roamy worker delegation). Fleet work is the strongest
  standing pressure toward Branch B — the trigger table must reflect that, still without
  pre-deciding.
- **DF-7 D1–D5 (df7 spec §12):** David already ruled the HOW of Branch B on 2026-06-09
  (file-per-job JSON · AngelEye session-id as claimant · MCP-first · coordinator may requeue
  state, never kills processes · client owns retry). Those rulings are inputs to reuse, not
  questions to reopen.
- **No standing daemon/cron without an explicit go** (unknowns-map §B): do NOT resurrect,
  install, or launchctl-load Switchboard in this ticket, even "just to check".
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs.
- **Ticket-first (`engine/store/queue/.CONVENTION.md`):** queue/running/done movement +
  `results/<ticket>.json` is the audit trail.

## Recon (verify before any work)

Docs lag code — several docs contradict each other on exactly this topic (that's part of what
the decision doc must record). Repo root `/Users/davidcruwys/dev/ad/apps/dark-factory`; the
Switchboard repo is `/Users/davidcruwys/dev/ad/apps/switchboard`. All verified 2026-07-06 at
authoring; re-verify everything.

1. `ls engine/store/` → expect `queue/ running/ done/ results/ events/ needs-decision/
   decisions/` + `audit.jsonl`, `events-consumed.jsonl`, `wake.log`. This layout IS Branch A.
   Missing/renamed dirs or a new lifecycle dir → **Abort A1**.
2. `grep -n "claimed_by\|os.rename" engine/orchestrator.py | head` → expect the rename(2)
   claim (`os.rename` queue→running, ≈line 221) immediately followed by ownership stamping
   (`ticket["claimed_by"] = CLAIMANT`, ≈line 227, `CLAIMANT = hostname-pid`), a
   running→done rename (≈499) and a requeue rename running→queue (≈666). If claiming is no
   longer rename(2)-based → **Abort A1** (Branch A as described here is fiction).
3. `cat ../switchboard/appysentinel.json` → expect recipes exactly: `poll-command`,
   `snapshot-store`, `mcp-binding`, `api-binding`, `sse-deliver`, `register-as-launchd`,
   `staleness-detector` — and NO `job-state-store` / `job-coordinator`. If either DF-7 recipe
   IS listed → **Abort A2** (the fork may already be resolved de facto).
4. `git -C ../switchboard log --format="%h %ad %s" --date=short` → expect 6 commits, all
   2026-06-06, newest `d1506ba` (topic-selective replay). Any commit after 2026-06-06 →
   read it; if it builds claim/state verbs → **Abort A2**, otherwise note it as new evidence.
5. Liveness sweep (evidence for the doc, not a gate):
   `curl -s -m 3 http://localhost:5099/health; echo EXIT:$?` (authoring: EXIT:7, refused) ·
   `launchctl list | grep -i switchboard` (authoring: nothing) ·
   `curl -s -m 5 http://roamy:5099/health; echo EXIT:$?` (authoring: EXIT:28, timeout —
   Roamy was Tailscale-active via relay, so timeout ≠ proof of down; see Assumption 2).
   Whatever you observe → **Fork F1** routes how Branch B's resurrection cost is written.
6. Prior-ruling sweep — the fork must not already be decided:
   `grep -rn "state.authority\|state-plane\|Q3" engine/store/decisions/ engine/store/done/
   backlog/ --include="*.json" --include="*.md" -il | head` and
   `ls docs/switchboard-state-authority-fork.md 2>&1` (expect missing) and check
   `ls backlog/wargames/T8-09* backlog/wargames/tickets/T8-09.json 2>&1` — if a T8-09
   charter-recon output exists (its war game or a produced report), READ it and reuse its
   findings; if a David ruling on Q3 postdating 2026-07-06 exists anywhere → **Abort A2**.
7. Charter reality: `ls backlog/2026-06-09-switchboard-greenfield-*.md
   backlog/2026-06-09-switchboard-charter-grounding.md` → expect KICKOFF + seed + grounding
   present. Then confirm no charter OUTPUT exists:
   `grep -rln "greenfield charter" docs/ ../switchboard/ 2>/dev/null | grep -v backlog` →
   authoring found none (the grounding doc says itself "This is the INPUT to
   /agent-skills:spec, not the charter"). If a real charter doc surfaced since → Fork F2.
8. Stale-reference count in the DF-7 spec:
   `grep -c "claim-next\|run-next-workflow\|WT_STATE_PLANE" backlog/specs/df7-switchboard-state-plane-spec.md`
   → authoring: 11. These target the RETIRED floor (`experiments/watchtower-engine/bin/`
   still on disk but superseded by `engine/` on 2026-07-04) — the raw material for Move 4's
   re-baseline table. If 0 → someone already re-baselined the spec; read the new version and
   fold it in instead of redoing the mapping.

## Moves

### Move 1 — Pin Branch A ground truth (what "filesystem store stays truth" actually is)

- **Do:** From the recon evidence, write (scratchpad notes for Move 5) the Branch A inventory:
  every reader/writer of `engine/store/` and what each treats as authoritative. Enumerate by
  command, not memory: `grep -ln "store" engine/*.py` then, for each of `orchestrator.py`
  (claim/requeue/settle, CAP/BACKOFF, HITL via needs-decision→decisions), `wake.py` (launchd
  WatchPaths on queue/, WAKE-ARMED/HALT/BACKOFF gates), `consumer.py` (events/ +
  events-consumed.jsonl, plus omi-fetch's external events dir), `status.py`, `halt.py`,
  `warm_pool.py` — one line each: what it reads, what it writes, which file is its truth.
  Include the two facts that most matter to the fork: (a) ownership IS recorded today
  (`claimed_by`/`claimed_at` — closing the gap DF-7 §2 called "anonymous claim"), (b) the
  wake wire is a filesystem poll explicitly documented as the piece that gets swapped for SSE
  when DF-7 lands (`docs/auto-wake.md` §7, last paragraph).
- **Expect:** an inventory of ~6 modules, each grounded in a grep/read you actually ran.
- **Failure signal:** a store consumer exists that this war game never named (a new module
  writing to `engine/store/`).
- **Counter-move:** add it to the inventory and to the doc's Branch A section; if it
  implements an ALTERNATIVE claim path (not rename(2)) → Abort A1.

### Move 2 — Pin Branch B ground truth (what Switchboard actually has vs what DF-7 needs)

- **Do:** Write the Branch B inventory from Recon 3–5: what EXISTS in
  `../switchboard/src/` (api-binding `POST /jobs` = durable enqueue to its own `queue/` dir +
  `job.queued` emit; sse-deliver with topic-selective durable replay; staleness-detector;
  snapshot-store; MCP binding; port from `SSE_PORT` env, default 5099) versus what DF-7 SPECS
  but was never built (job-state-store recipe, job-coordinator recipe, claim/start/complete/
  fail verbs, ownership enforcement, liveness reaping). Read spec §5–§8 for the second list —
  and verify each named absence with a grep, e.g.
  `grep -rn "job-coordinator\|job_claim\|/jobs/claim" ../switchboard/src/ | wc -l` (authoring:
  0). Record the liveness verdict from Recon 5 per Fork F1's route.
- **Expect:** a built-vs-specced two-column list where every "absent" claim has a grep behind
  it.
- **Failure signal:** grep finds claim verbs or coordinator code the recon missed.
- **Counter-move:** → Abort A2 (the fork's premise — DF-7 unbuilt — is wrong; do not
  re-litigate a moved landscape, park it).

### Move 3 — Re-baseline the DF-7 spec against today's engine (the honest Branch B cost)

- **Do:** The DF-7 spec (2026-06-09) was written against the RETIRED floor. Build the mapping
  table that a future Branch B build would need — for each of the ~11 stale references
  (Recon 8), the old target → today's equivalent → migration note. At minimum:
  `bin/claim-next.sh` (rename mutex, anonymous) → `orchestrator.py` claim (rename + recorded
  `claimed_by`) — the "lift the mutex into the service" move now starts from a RICHER client;
  `run-next-workflow` lifecycle → `orchestrator.py`'s dispatch/verify/settle loop + WarmPool;
  `WT_STATE_PLANE=service` env flag → would now gate orchestrator paths, not a shell script;
  `experiments/watchtower-engine/{queue,running,done,reports}/` → `engine/store/{queue,
  running,done,results}/`; reaper `done/`-mtime keying → orchestrator's artifact-is-truth
  reaping. Also carry forward, unchanged: the §7 job-state data model (superset of today's
  ticket JSON — confirm field-by-field against a real `engine/store/done/` ticket), the §11
  four-step shadow→cutover migration, and the D1–D5 rulings.
- **Expect:** a table with one row per stale reference; every "today's equivalent" cites a
  file+line you verified in Move 1.
- **Failure signal:** a spec reference has NO current equivalent (a capability the old floor
  had that engine/ dropped).
- **Counter-move:** that's a finding, not a blocker — record it in the doc as a Branch B
  prerequisite ("engine must first regain X"). If more than three such holes appear, the
  spec re-baseline is a bigger job than a mapping table: say so in the doc and scope it as
  the first Branch B build step instead of completing it here.

### Move 4 — Build the trigger table (the observations that force the fork)

- **Do:** Draft the trigger table for the doc. Each row: trigger · observation (an executable
  command or an unambiguous event) · branch it forces · pressure (forcing vs leaning).
  Include AT LEAST these seven, plus any the evidence suggests:
  1. **Second machine dispatches work** (Q8 fleet delegation live): observe
     `grep -h claimed_by engine/store/done/*.json engine/store/audit.jsonl 2>/dev/null |
     grep -v "$(hostname)"` returning rows, or an engine clone running on Roamy → forces B
     (two rename(2) stores cannot share one truth).
  2. **Anyone proposes syncing `engine/store/` across machines via git/rsync**: observe such
     a plan/backlog item appearing → forces B immediately (this is the fork/merge-hell DF-7
     §2 explicitly rejects — the trigger exists to catch it BEFORE someone builds it).
  3. **Double-claim or lost-ticket incident**: observe the same ticket filename appearing
     twice in `audit.jsonl` claims, or a `running/` entry whose `claimed_by` pid is dead with
     no requeue → forces B's ownership/liveness plane (or at minimum a hardening ticket).
  4. **Cross-machine wake needed**: a ticket queued on one machine must wake a worker on
     another; observe the first fleet-delegation war game needing it → forces B's SSE leg
     (auto-wake v2 — `docs/auto-wake.md` §7 names this exact swap seam).
  5. **Cross-machine HALT needed**: a HALT incident where a second machine kept running
     (kill-switch is per-machine today, `docs/kill-switch-spec.md`) → forces B's bus.
  6. **Watchtower real app starts consuming live job state** (Q6): a T5 build ticket needs
     job state over HTTP/SSE rather than local file reads → leans B (a read-only projection
     could bridge it; say so).
  7. **Factory portability in anger**: engine driving jobs whose working state must follow
     work into other repos/machines (DF-7 §2 goal 2) → leans B.
  Also list the COUNTER-triggers that entrench A: Switchboard stays down with no owner;
  fleet work deferred again; the always-on-daemon posture stays unwanted (metered-billing
  caution, no-cron-without-go rule).
- **Expect:** ≥7 triggers, each with an observation a future session could execute or
  recognise without judgment.
- **Failure signal:** a trigger whose observation is a vibe ("when scale demands it").
- **Counter-move:** rewrite it as a measurable observation or drop it — an unobservable
  trigger is decoration, and this artifact's whole value is that its triggers fire.

### Move 5 — Evaluate every trigger NOW (status-today column)

- **Do:** Run each trigger's observation command from Move 4 against the current system and
  record the result in a `status today` column (authoring expectation: all quiet — single
  machine, no store-sync proposals, no double-claims in `audit.jsonl`, no live cross-machine
  demand). Date-stamp the column.
- **Expect:** every row shows quiet/not-fired.
- **Failure signal:** any trigger observably ALREADY fired.
- **Counter-move:** → Fork F3 (the "defer" premise is stale; David must actually rule).

### Move 6 — Write `docs/switchboard-state-authority-fork.md`

- **Do:** Author the decision doc with EXACTLY this section skeleton (fill from Moves 1–5;
  every factual claim carries its evidence command or file+line):
  1. **The fork** — one paragraph: "state authority" = which system's record IS the truth
    about job state (pool/claims/ownership/lifecycle). Q3 ruling: deferred; this doc is the
    tripwire map.
  2. **Ground truth (verified <date>)** — the Move 1 + Move 2 inventories, side by side.
  3. **Branch A — filesystem store stays truth** — what it gives (proven mutex now WITH
    ownership; zero new build; no daemon commitment; whole engine already speaks it), its
    hard ceilings (single-machine by construction; wake = local poll; no durable cross-restart
    replay for consumers; cross-machine HALT/status blind), residual costs (≈zero), and the
    no-regret moves valid under both branches (retention T1-10, golden jobs T1-07, keeping
    the ticket JSON schema stable — DF-7 §7's model is a superset of it).
  4. **Branch B — DF-7 durable state plane** — what it unlocks (N thin clients on one plane,
    fleet, portability, SSE wake, durable replay, ownership enforced in-service), the honest
    bill: resurrect Switchboard (down at authoring — see liveness evidence), re-baseline the
    spec (the Move 3 table, embedded verbatim), build 2 recipes + verbs, run the §11 4-step
    shadow→cutover, accept an always-on bun/TS daemon as a standing commitment, and note its
    event log has the same grow-forever gap as the engine store (unknowns-map §E).
  5. **Prerequisites Branch B inherits** — Switchboard ownership/liveness resolved; the
    greenfield charter question (grounding exists, charter does not — per Recon 7 / Fork F2);
    AngelEye session-id stability (D2's own stated contingency).
  6. **Triggers** — the Move 4/5 table, including counter-triggers.
  7. **Default posture** — Branch A remains truth until a forcing trigger fires; leaning
    triggers accumulate as pressure but do not flip authority by themselves; any flip is a
    David ruling (via needs-decision/ or triage), never an executor call. State this as the
    standing default Q3's "defer" establishes — it is a restatement, not a new decision.
  8. **Standing rulings honoured** — D1–D5 verbatim-by-reference; the constellation placement
    rule (shared state in services, floor stateless — DF-7 §2 note); the voice law
    (comms-flow §8) unaffected by either branch.
  9. **Contradictions found (docs-lag ledger)** — at authoring: `docs/comms-flow.md` §2 says
    Switchboard "live on MacBook Pro :5099/:5100" while nothing answers on either machine;
    `docs/dark-factory-constellation.md` calls it "substantially built" (true of the bus,
    false of the state plane); `docs/auto-wake.md` §7 cites "this repo's CLAUDE.md —
    'Switchboard is DOWN'" but CLAUDE.md no longer mentions Switchboard at all; the DF-7
    spec's client contract targets the retired floor. Add anything your recon found; fix
    NONE of them here beyond Move 7's two pins — name them for T8's truth-reconciliation.
- **Expect:** the doc exists; `grep -c "^## " docs/switchboard-state-authority-fork.md` ≥ 9.
- **Failure signal:** a section you cannot fill from evidence gathered in Moves 1–5.
- **Counter-move:** gather the missing evidence (one bounded grep/read), or write the gap
  into the doc explicitly as "unverified — check before relying"; never pad with doc-sourced
  claims.

### Move 7 — Cross-link + pin doc truth (two edits only)

- **Do:** (a) Add one line to `docs/INDEX.md` in its decision/spec region: the doc name, one
  sentence ("the Q3 state-authority fork: both branches mapped, triggers armed, default =
  filesystem-truth until a trigger fires"), and date. (b) Insert a status banner as the first
  line under the title of `backlog/specs/df7-switchboard-state-plane-spec.md`:
  `> **STATUS (2026-07-06+): spec-only, not built. Decision deferred per Q3 — branches,
  triggers, and the re-baseline of this spec against engine/ (which superseded the floor this
  spec targets) live in docs/switchboard-state-authority-fork.md.**` No other file edits.
- **Expect:** `grep -n "switchboard-state-authority-fork" docs/INDEX.md
  backlog/specs/df7-switchboard-state-plane-spec.md` → exactly two hits.
- **Failure signal:** INDEX.md's structure changed so much there's no sane insertion point.
- **Counter-move:** append under the last section with a dated line — a slightly misplaced
  index line beats a skipped one; note it in the results JSON.

### Move 8 — Self-report, commit, push

- **Do:** Write the worker self-report to `engine/store/results/<this-ticket-filename>.json`
  in the form the orchestrator's task prompt demands, including: liveness verdict (F1 route
  taken), charter verdict (F2), trigger status-today summary, and whether F3 fired. Commit
  the three touched docs (new decision doc, INDEX line, DF-7 banner) + results in one commit:
  `docs(engine): T1-11 state-authority fork mapped — branches, triggers, default posture
  (wg-t1-11)` with the standard Co-Authored-By trailer; push.
- **Expect:** `git log --oneline -1` shows the commit; `git status --porcelain` clean apart
  from pre-existing dirt.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git pull --rebase` then push; on conflict in the docs you touched,
  re-apply your edits on top (yours are pure additions). Second failure → leave committed
  locally, note in results JSON.

## Forks

**F1 — Switchboard liveness at execution time.**
Trigger: Recon 5's three probes.
→ **Route A (up somewhere — /health answers on either machine):** Branch B's bill drops the
"resurrect" line; verify which recipes the live instance actually loaded
(`curl -s http://<host>:5099/health` then re-check appysentinel.json on that machine's copy)
and record it. The fork itself is unchanged — a live bus without claim verbs is still Branch A.
→ **Route B (down everywhere, or Roamy unverifiable):** write the resurrection cost into
Branch B's bill; if Roamy was merely unreachable (timeout ≠ refused), record "unverifiable
from this machine" — never write "down on Roamy" from a timeout alone (Assumption 2). Do NOT
start it yourself (locked context: no daemon without a go).

**F2 — Greenfield charter exists by execution time.**
Trigger: Recon 7 finds a charter OUTPUT (not the KICKOFF/seed/grounding inputs), or T8-09's
artifacts answer it.
→ **Route A (charter exists):** read it; where it rules on state authority or Switchboard
identity, the doc's Branch B section quotes the charter as governing and this ticket's own
analysis becomes secondary — flag any conflict with D1–D5 explicitly in section 9.
→ **Route B (still unwritten — the authoring-time state):** record that; the decision doc
then doubles as a primary input to the future charter, and says so in its header.

**F3 — A forcing trigger already fired.**
Trigger: Move 5 finds any forcing-class observation true today (second-machine claims, a
store-sync proposal, an observed double-claim).
→ **Route A (evidence is unambiguous):** finish the doc anyway (it's now urgent, not moot),
then ALSO write `engine/store/needs-decision/wg-t1-11-switchboard-state-fork-decision.json`:
`{"ticket":"wg-t1-11-switchboard-state-fork-decision","question":"Q3 deferred the state-authority fork, but trigger <name> has already fired: <evidence>. Rule now: keep filesystem truth and mitigate, or start Branch B (DF-7)?","proposed":"<the doc's default posture applied to this trigger>","note":"full map in docs/switchboard-state-authority-fork.md §6"}`
and leave the ticket in `running/` per the HITL idiom.
→ **Route B (ambiguous — e.g. a foreign hostname in audit.jsonl from a one-off manual
experiment):** record it in the status-today column as "fired once, context: <what you
found>", do not park; the doc's trigger stands armed for a recurrence.

## Assumptions ledger

1. **DF-7's D1–D5 rulings still govern Branch B's HOW.** Plausible: David ruled them
   explicitly on 2026-06-09 and nothing on disk retracts them. If execution-time evidence
   (charter, a decisions/ artifact, a David note) contradicts any of them → quote both in
   section 9 and let the newer ruling win in the doc's text; if they conflict irreconcilably
   → needs-decision/, don't arbitrate.
2. **Roamy's :5099 timeout is not evidence of "down".** Authoring saw Roamy Tailscale-active
   via relay but the port timing out — could be firewall/no-listener/relay quirk. The
   executor may try `ssh roamy 'curl -s -m 3 http://localhost:5099/health'` if SSH works;
   if it doesn't, write "unverifiable", never "down".
3. **The decision doc's home is `docs/`** (CLAUDE.md's "document a procedure → docs/"), name
   `switchboard-state-authority-fork.md`. If David prefers `backlog/specs/` at triage, it's
   a `git mv` + two link fixes — note, don't block.
4. **T8-09 (charter recon) may or may not have run first.** This war game carries its own
   recon for everything it needs, so no hard dependency; if T8-09 output exists, prefer its
   findings where fresher and cite it.
5. **`experiments/watchtower-engine/` is retired-but-present.** Authoring verified its bin/
   scripts still exist on disk. The doc treats it as prior art (the proven mutex lineage),
   never as a live system. If a future session finds it re-activated → that's a section-9
   contradiction to record.

## Abort conditions

**A1 — Branch A ground truth has moved.** Recon 1/2 fails: store layout drifted, or claiming
is no longer rename(2)+ownership in `orchestrator.py`. The fork as framed would be fiction.
Park: write `engine/store/needs-decision/wg-t1-11-switchboard-state-fork-decision.json` with
`{"ticket":"wg-t1-11-switchboard-state-fork-decision","question":"T1-11 (authored 2026-07-06) maps a fork whose Branch A no longer matches the engine: <what differs>. Re-author the war game against current state?","proposed":"re-author","note":"<observed layout/claim mechanism>"}`.
Leave the ticket in `running/`. Never write a decision doc describing a system that isn't there.

**A2 — The fork is already resolved (either direction).** DF-7 recipes/verbs found built in
Switchboard, a post-2026-07-06 David ruling on Q3 found on disk, or Switchboard commits show
state-plane work landed. Park to needs-decision/ (same shape, question: "Q3's fork appears
already resolved by <evidence>. Confirm, and should T1-11 become a document-what-happened
ticket instead?"). Do not write a "decision pending" doc over a decided landscape.

**A3 — Scope breach imminent.** You find yourself about to edit any `.py`, any `.ts`, any
file in `../switchboard/`, or to launchctl-load anything, to "make the evidence cleaner".
Stop, park to needs-decision/ describing what tempted you. This ticket ships prose + two doc
pins, nothing else.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
test -f docs/switchboard-state-authority-fork.md && echo OK            # doc exists
grep -c "^## " docs/switchboard-state-authority-fork.md                 # ≥ 9 sections
grep -ci "trigger" docs/switchboard-state-authority-fork.md            # ≥ 7 (table present)
grep -n "status today" docs/switchboard-state-authority-fork.md        # dated column present
grep -n "claim-next" docs/switchboard-state-authority-fork.md          # re-baseline table embedded
grep -n "switchboard-state-authority-fork" docs/INDEX.md               # index line
grep -n "switchboard-state-authority-fork" backlog/specs/df7-switchboard-state-plane-spec.md  # banner
ls engine/store/results/ | grep -c wg-t1-11                             # 1 — self-report exists
git log --oneline -3 | grep wg-t1-11                                    # commit landed
```

Negative checks (this was a decision artifact, not a build):
```bash
git diff HEAD~1 --stat -- engine/ | grep -v "store/results" | grep "\.py" ; echo "py-diff-exit:$?"  # exit 1 (no .py touched)
git -C ../switchboard status --porcelain                                # empty — repo untouched
launchctl list | grep -i switchboard                                    # unchanged vs Recon 5
ls engine/store/queue/ engine/store/running/                            # only this ticket's own lifecycle moved
```
And: `engine/store/needs-decision/` contains a wg-t1-11 file ONLY if Fork F3-A or an abort
fired — otherwise it must not exist.

## Executor notes (sonnet)

- **Scope fence:** writes are exactly — `docs/switchboard-state-authority-fork.md` (new),
  one line in `docs/INDEX.md`, one banner line in
  `backlog/specs/df7-switchboard-state-plane-spec.md`, your results self-report, and (only
  per F3/aborts) one needs-decision file. Read anything; change nothing else. The
  Switchboard repo is READ-ONLY for you, including its git state.
- **You are mapping, not deciding.** If your analysis converges on "obviously Branch B",
  that goes in the doc as pressure-noted, not as a verdict. The default posture (A until a
  forcing trigger) is Q3's ruling restated — you have no authority to move it.
- **Evidence over eloquence.** Every claim in the doc carries the command or file+line that
  proved it. A shorter doc with 100% verified claims beats a richer doc with one doc-sourced
  claim — this artifact exists precisely because the surrounding docs contradict each other.
- **Prefer HITL over guessing** whenever the landscape has moved (A1/A2 conditions, D1–D5
  contradictions): a parked question costs minutes; a decision doc built on a stale premise
  poisons the actual decision later.
- **The rabbit hole:** resurrecting Switchboard "just to confirm the bus works", prototyping
  a claim verb "to estimate effort", or fixing the docs-lag contradictions you catalogue.
  All of it is out of scope — the contradictions are FINDINGS for section 9 and T8's
  reconciliation work; the effort estimate comes from the Move 3 mapping table, not from
  code. Skip it.
