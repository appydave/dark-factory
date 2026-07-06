# T8-09 — Switchboard greenfield charter recon

| field | value |
|---|---|
| ticket | wg-t8-09-switchboard-charter-recon |
| track / size / priority | T8 Doc truth / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none (T1-11 consumes THIS ticket's output, not the reverse) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Two disputed facts block clean thinking about Switchboard, and the docs contradict each other
on both: (1) **was the greenfield charter ever written?** (the KICKOFF/seed/grounding trio from
2026-06-09 exists, but did step 4 — the actual charter — ever run?) and (2) **is Switchboard
actually running, and where?** (docs claim simultaneously "live on MacBook Pro :5099" and
"Switchboard is DOWN"). This ticket answers both with disk and network evidence — never doc
claims — and ships a dated recon report `docs/switchboard-charter-recon.md` that
T1-11 (the state-authority fork decision war game) reads as its Fork F1/F2 input, plus exactly
two truth pins (a STATUS banner on the KICKOFF backlog file, one `docs/INDEX.md` line). Done
looks like: report on disk with a liveness matrix and a charter-paper-trail verdict, both pins
placed, results self-report written, commit pushed, and **nothing started, stopped, installed,
or edited in either machine's Switchboard**.

## Locked context

- **Q3 (decisions.md):** Switchboard state fork = **defer** → T1-11 decision war game. This
  ticket is that war game's recon feeder; it decides NOTHING, it verifies.
- **Q4 (decisions.md):** everything through the engine — this runs as a sonnet Swagger dispatch
  and self-reports to `engine/store/results/`.
- **Q8 (decisions.md):** fleet is IN (+Roamy) — probing Roamy over Tailscale/SSH is in scope,
  **read-only commands only**.
- **No standing daemon/cron without an explicit go** (unknowns-map §B): never start, stop,
  restart, install, or launchctl-load/kickstart Switchboard on ANY machine, even "to test".
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs.
- **Ticket-first (`engine/store/queue/.CONVENTION.md`):** queue/running/done movement +
  `results/<ticket>.json` is the audit trail.

## Recon (verify before any work)

Repo root `/Users/davidcruwys/dev/ad/apps/dark-factory` (run everything from here); the
Switchboard repo is `/Users/davidcruwys/dev/ad/apps/switchboard`. All authoring claims below
were verified 2026-07-06 on mac-mini-m4; re-verify everything — this is a truth ticket, its
own claims must not be doc-trusted either.

1. `ls backlog/2026-06-09-switchboard-greenfield-KICKOFF.md backlog/2026-06-09-switchboard-greenfield-seed.md backlog/2026-06-09-switchboard-charter-grounding.md`
   → all three exist (the charter INPUTS). Any missing → the paper trail this ticket audits
   has been moved/reworked since authoring → **Abort A1**.
2. `ls backlog/wargames/T1-11-switchboard-state-fork-decision.md` → the consumer war game
   exists. Also `ls docs/switchboard-state-authority-fork.md 2>&1` → authoring: missing
   (T1-11 not yet executed). If it EXISTS → T1-11 already ran → **Fork F3**.
3. `ls ../switchboard/src/main.ts && git -C ../switchboard log --oneline | head -3` → repo
   present, HEAD `d1506ba` (topic-selective replay), 6 commits all 2026-06-06. A newer local
   HEAD → read the new commits first; if they build claim/state verbs (`job-state-store`,
   `job-coordinator`, `/jobs/claim`) → **Abort A2**.
4. `sed -n '44,57p' ../switchboard/src/main.ts` → expect the two-port wiring with the
   host-local comments: SSE `:5099` (`SSE_PORT` default 5099, "Host-local by default") and
   ingest `:5100` (`INGEST_PORT` default 5100). This is why REMOTE curl to `roamy:5099`
   times out even when Switchboard is UP there — liveness on another machine is only
   provable via `ssh <host> 'curl http://localhost:5099/health'`. If the binding changed
   (e.g. now listens on all interfaces) → note it in the report; probe both ways.
5. `tailscale status | grep -i roamy` → authoring: `100.89.32.35 roamy david@ macOS idle`.
   Absent/offline → **Fork F1** (Roamy leg unverifiable).
6. `ls engine/store/` → expect `queue/ running/ done/ results/ events/ needs-decision/
   decisions/` + `audit.jsonl`, `events-consumed.jsonl`, `wake.log` (where the self-report
   and any park go). Layout drifted → still write the report, but flag the drift in the
   results JSON.

## Moves

### Move 1 — Charter paper-trail verdict

- **Do:** Establish whether any charter OUTPUT exists (as opposed to the three INPUTS from
  Recon 1). Run all four probes:
  (a) `grep -rln "greenfield charter" docs/ ../switchboard/ ~/dev/ad/brains/dark-factory/ 2>/dev/null | grep -v backlog`
  — authoring found only `docs/kdd/learnings/design-charter-grounding-needs-direct-design-origin-docs-not-kdd.md`
  and `docs/kdd/learnings/build-dev-history-claims-stated-without-verifying-against-gi-kdd.md`
  (process learnings ABOUT the grounding work, not a charter).
  (b) `find docs ../switchboard -iname "*charter*" -not -path "*/node_modules/*"` — authoring:
  only the two KDD learnings above plus nothing in the Switchboard repo.
  (c) `grep -il "charter" engine/store/done/*.json 2>/dev/null` — any done ticket that
  authored a charter. Authoring: none for Switchboard (ignore Watchtower-charter hits, e.g.
  T5-01 artifacts — different app).
  (d) `head -6 backlog/2026-06-09-switchboard-charter-grounding.md` — confirm its own header
  still says "This is the INPUT to `/agent-skills:spec`, not the charter."
- **Expect:** verdict = **charter never authored**. The 2026-06-09 chain stopped after phase 1:
  KICKOFF (instructions) ✓, seed ✓, grounding ✓ — but KICKOFF step 4 (the
  `/agent-skills:spec` interview with David) never ran, and no charter document exists in
  dark-factory, the Switchboard repo, or the dark-factory brain.
- **Failure signal:** any probe surfaces a real charter document (an output that defines
  Switchboard's identity/bounded responsibility/surface — not instructions, not grounding,
  not a KDD learning about the process).
- **Counter-move:** → Fork F2.

### Move 2 — Local liveness sweep (this machine, mac-mini-m4)

- **Do:** Three read-only probes:
  `lsof -nP -iTCP:5099 -sTCP:LISTEN; lsof -nP -iTCP:5100 -sTCP:LISTEN` ·
  `launchctl list | grep -i switchboard` ·
  `ps aux | grep "switchboard/src/main.ts" | grep -v grep`.
- **Expect:** all three empty (authoring 2026-07-06: nothing on either port, no launchd job,
  no process — Switchboard is DOWN on mac-mini-m4). Record each command + result verbatim for
  the report's liveness matrix.
- **Failure signal:** a listener/process/launchd job IS present locally.
- **Counter-move:** that's data, not a problem — record it (including `launchctl list
  com.appydave.switchboard` detail if the label matches), touch nothing, and carry the
  "UP locally" fact into the matrix. If what's listening on 5099 is NOT Switchboard
  (some other app claimed the port), name the process in the report — that's a port-collision
  finding T1-11 needs.

### Move 3 — Roamy liveness sweep (SSH only — never trust remote curl)

- **Do:** One read-only SSH batch (BatchMode so a password prompt fails fast instead of
  hanging):
  ```bash
  ssh -o ConnectTimeout=4 -o BatchMode=yes roamy '
    curl -s -m 3 http://localhost:5099/health; echo " SSE-EXIT:$?";
    curl -s -m 3 http://localhost:5100/health; echo " INGEST-EXIT:$?";
    launchctl list | grep -i switchboard;
    git -C ~/dev/ad/apps/switchboard log --oneline | head -3'
  ```
- **Expect (authoring 2026-07-06):** SSE `/health` →
  `{"status":"ok","subscribers":0,"lastEventId":0,"buffered":0}` EXIT:0; ingest `/health` →
  `{"status":"ok","accepts":"/jobs","emits":"job.queued"}` EXIT:0; launchd
  `com.appydave.switchboard` loaded (authoring pid 10848); Roamy HEAD `d1506ba` — identical
  to local. **Switchboard is UP on Roamy.** Record all output verbatim.
- **Failure signal:** SSH itself fails (timeout, refused, auth prompt), or health returns
  non-ok / connection refused on Roamy's localhost.
- **Counter-move:** SSH failure → **Fork F1**. SSH works but health fails → that's a real
  "down on Roamy" observation (localhost-refused IS evidence, unlike a remote-curl timeout) —
  record it with the exact exit code and check `launchctl list` output for a loaded-but-dead
  job; if the counter-observation is itself ambiguous (e.g. launchd job listed but port
  refused), record both facts side by side and let the report say "inconsistent — job loaded,
  port dead", never resolve it by restarting anything (**Abort A3** if tempted).

### Move 4 — Divergence + state-plane tripwire (feeds T1-11's Abort A2)

- **Do:** Confirm the code landscape T1-11 assumes is still true on BOTH machines:
  (a) compare HEADs — local `git -C ../switchboard log --oneline | head -1` vs Roamy's from
  Move 3 (authoring: both `d1506ba`).
  (b) `cat ../switchboard/appysentinel.json` and
  `ssh -o ConnectTimeout=4 -o BatchMode=yes roamy 'cat ~/dev/ad/apps/switchboard/appysentinel.json'`
  → expect recipes identical, `coordination: ["staleness-detector"]` only — NO
  `job-state-store` / `job-coordinator`.
  (c) `grep -rn "job-coordinator\|job_claim\|/jobs/claim" ../switchboard/src/ | wc -l` →
  authoring: 0.
- **Expect:** identical HEADs, no state-plane recipes or claim verbs anywhere.
- **Failure signal:** Roamy has commits local lacks (or vice versa), or any probe finds
  state-plane code.
- **Counter-move:** state-plane code found → **Abort A2** (Q3's "defer" and T1-11's whole
  premise are stale; park, don't paper over it). Mere commit divergence without state-plane
  content → read the divergent commit subjects (`git log` output you already have), record
  the delta in the report as a docs-lag-code-ACROSS-MACHINES finding, and continue.

### Move 5 — Contradiction ledger (verify each cited line still exists)

- **Do:** Build the report's ledger. For each row: claim · file:line · what recon actually
  found · verdict (`true` / `false` / `stale` / `dangling-citation`). Re-verify each citation
  with the grep given — docs may have changed since authoring:
  1. `grep -n "live on MacBook Pro" docs/comms-flow.md` (authoring: line 39, ":5099/:5100") —
     authoring verdict: **TRUE** (Move 3 confirmed UP on Roamy = the MacBook Pro, renamed
     2026-07-03) — but the doc omits the host-local binding, which is why earlier probes
     (including T1-11's authoring, remote curl EXIT:28) wrongly read it as down. Verdict
     text: "true, but unverifiable by the method most sessions try; doc should note
     host-local binding".
  2. `grep -n "Switchboard.*DOWN\|is DOWN" docs/auto-wake.md` (authoring: lines 131–132 cite
     «this repo's `CLAUDE.md` — "Switchboard is DOWN"») then
     `grep -in switchboard CLAUDE.md` (authoring: zero hits) — verdict:
     **dangling-citation** (CLAUDE.md no longer says it), and the underlying claim is
     machine-ambiguous: down on mac-mini-m4, UP on Roamy.
  3. `grep -n "substantially built" docs/dark-factory-constellation.md` (authoring: line 64) —
     verdict: **half-true** — true of the bus (SSE, durable replay, ingest), false of the
     state plane (claims/ownership/lifecycle = DF-7, spec-only, Move 4 proved unbuilt).
  4. `sed -n '39p' backlog/problems.md` (authoring: fleet collector reports macbook-pro-2
     "offline" while ping+ssh OK and Switchboard :5099 UP) — verdict: **consistent with
     findings**; the sentinel-blind-to-Roamy problem is T6-03's, not this ticket's — cite,
     don't fix.
- **Expect:** ≥4 ledger rows, every one re-verified at execution time with its command.
- **Failure signal:** a cited line no longer exists or the text moved.
- **Counter-move:** grep for the phrase file-wide; if genuinely gone, the row's verdict
  becomes "already fixed since 2026-07-06" — that is a finding too, keep the row. Fix NONE
  of these docs here — they belong to T8's broader reconciliation and to T1-11's §9 ledger.

### Move 6 — Write the report + exactly two pins

- **Do:** (a) Author `docs/switchboard-charter-recon.md` with EXACTLY this section skeleton,
  filled only from Moves 1–5 evidence (every claim carries its command or file:line):
  1. **Verdicts** — the two headline answers, one line each, date-stamped: charter
     written? (authoring: NO — inputs complete through grounding, step-4 interview never
     ran) · Switchboard up? (authoring: DOWN on mac-mini-m4, UP on Roamy via launchd
     `com.appydave.switchboard`, both ports healthy).
  2. **Charter paper trail** — the three inputs (KICKOFF → seed → grounding) with one-line
     descriptions, what step 4 was supposed to produce, and the Move 1 probe results.
  3. **Liveness matrix** — machine × port × probe method × result, verbatim outputs, dated.
  4. **Probe protocol** — the host-local binding fact (`src/main.ts` ~line 45): remote
     `curl <host>:5099` timing out is NOT evidence of down; only
     `ssh <host> 'curl http://localhost:5099/health'` proves anything. One paragraph; this
     alone retires the biggest recurring false claim.
  5. **Code state** — HEADs both machines, recipe list, state-plane absence (Move 4).
  6. **Contradiction ledger** — the Move 5 table.
  7. **What this means for T1-11** — explicitly route its forks: F1 → Route A variant
     ("up on Roamy, down locally" — Branch B's resurrection bill shrinks to
     'resurrect per-machine instances where needed', it does not vanish because the daemon
     is per-machine by design); F2 → Route B (charter still unwritten — unless this run hit
     Fork F2, then say so); note `subscribers:0` (nothing consumes the bus today).
  (b) Pin 1: insert as the first line under the title of
  `backlog/2026-06-09-switchboard-greenfield-KICKOFF.md`:
  `> **STATUS (<today's date>): never executed — the charter this kickoff commissions was NOT authored as of this date. Phase-1 grounding (…charter-grounding.md) is complete; step 4 (the /agent-skills:spec interview with David) never ran. Liveness + paper-trail recon: docs/switchboard-charter-recon.md (wg-t8-09).**`
  (c) Pin 2: one line in `docs/INDEX.md` (place near other recon/decision entries; if no sane
  slot, append at the end of the nearest list with the date):
  `- **switchboard-charter-recon.md** — T8-09 verdicts: greenfield charter never authored (inputs only); Switchboard UP on Roamy / DOWN on mac-mini-m4, host-local-bound (probe via ssh-localhost only). Feeds T1-11. (2026-07-06+)`
- **Expect:** `grep -c "^## " docs/switchboard-charter-recon.md` ≥ 7;
  `grep -n "switchboard-charter-recon" docs/INDEX.md backlog/2026-06-09-switchboard-greenfield-KICKOFF.md`
  → exactly two hits.
- **Failure signal:** a section you cannot fill from evidence actually gathered this run.
- **Counter-move:** run the one missing probe (bounded — a single grep/ssh), or write the gap
  explicitly as "unverified this run: <what and why>"; never fill from a doc claim — that
  defect is the exact disease this ticket treats.

### Move 7 — Self-report, commit, push

- **Do:** Write `engine/store/results/<this-ticket-filename>.json` in the form the
  orchestrator's task prompt demands, including: charter verdict, liveness matrix summary
  (per machine), which forks fired (F1/F2/F3 or none), and the one-line handoff for T1-11.
  Commit the three touched files (report, KICKOFF banner, INDEX line) + results in one
  commit: `docs(t8): T8-09 switchboard recon — charter unwritten, up-on-Roamy/down-local
  pinned (wg-t8-09)` with the standard Co-Authored-By trailer; push.
- **Expect:** `git log --oneline -1` shows the commit; `git status --porcelain` clean apart
  from pre-existing dirt.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git pull --rebase` then push; on conflict in the files you touched,
  re-apply your edits (yours are pure additions). Second failure → leave committed locally,
  note it in the results JSON.

## Forks

**F1 — Roamy unreachable at execution time.**
Trigger: Recon 5 shows roamy absent/offline in tailscale, or Move 3's SSH fails (timeout,
refused, BatchMode auth failure).
→ **Route A (reachable):** full two-machine matrix as written.
→ **Route B (unreachable):** the Roamy row of the matrix reads "unverifiable from mac-mini-m4
this run: <exact failure>" — NEVER "down on Roamy" (a remote timeout proves nothing; see the
probe-protocol section). The report still ships; the headline liveness verdict weakens to
"DOWN locally; last verified UP on Roamy 2026-07-06 (this war game's authoring)". T1-11's F1
input is then "unverified, presumed-stale" and the report says exactly that.

**F2 — A charter output exists after all.**
Trigger: Move 1 surfaces a real charter document.
→ **Route A (found):** the report's charter verdict flips to "authored at <path>, dated <x>";
read it and add a §2 summary of its rulings on identity / bounded responsibility / state
authority; flag prominently in §7 that T1-11 must take its own Fork F2 Route A (charter
governs, T1-11's analysis becomes secondary). Still ship the pins — the KICKOFF banner text
changes to "executed: charter at <path>".
→ **Route B (not found — the authoring-time state):** verdict "never authored", as written.

**F3 — T1-11 already executed before this ticket.**
Trigger: Recon 2 finds `docs/switchboard-state-authority-fork.md` on disk, or a wg-t1-11
entry in `engine/store/done/`.
→ **Route A (already ran):** this report is still worth shipping (it carries fresher liveness
truth than T1-11 had — T1-11's authoring could not verify Roamy). Add to §7: "T1-11 executed
before this recon; its §9 contradiction ledger and Branch B resurrection bill may need an
addendum — flagged for triage, NOT edited here." Do not touch T1-11's decision doc.
→ **Route B (not yet run):** normal path; this report becomes T1-11's Recon-7 input.

## Assumptions ledger

1. **"MacBook Pro" / "macbook-pro-2" / "Roamy" are one machine** (renamed 2026-07-03,
   Tailscale name `roamy`). Plausible: fleet-identity memory + tailscale status shows exactly
   one MacBook-class host. If tailscale lists MORE than one candidate (e.g. both
   `macbook-pro-2` and `roamy`) → probe each via SSH, record every row, and note the identity
   ambiguity in the report — don't pick.
2. **`subscribers:0, lastEventId:0, buffered:0` ≠ "never used".** Authoring saw a fresh/empty
   event window; that reads as "no current consumers, no buffered events", not "no history".
   Report only what `/health` returns at execution time; make no usage-history claims.
3. **Non-interactive SSH to roamy works** (key auth; worked at authoring). If it prompts or
   fails, that's Fork F1-B — never sit on an interactive prompt, never add keys or edit SSH
   config to "fix" it.
4. **The report's home is `docs/`** (CLAUDE.md: "document a procedure → docs/<topic>.md"),
   name `switchboard-charter-recon.md`. If David prefers `backlog/` or a dated name at
   triage, it's a `git mv` + two link fixes — note, don't block.
5. **The KICKOFF file is safe to banner.** It's a backlog instruction doc, not a ratified
   canonical artifact, so the assessment-mode rule (no in-place edits to ratified artifacts)
   doesn't bar an additive status banner. If execution-time evidence shows it was promoted
   somewhere canonical → skip Pin 1, note why in the results JSON.

## Abort conditions

**A1 — The charter paper trail has been restructured.** Recon 1 fails: the KICKOFF/seed/
grounding trio is missing or moved. The two questions this ticket answers were framed against
those files; auditing a reshuffled landscape blind produces false verdicts. Park: write
`engine/store/needs-decision/wg-t8-09-switchboard-charter-recon.json` with
`{"ticket":"wg-t8-09-switchboard-charter-recon","question":"T8-09 (authored 2026-07-06) audits the 2026-06-09 charter trio, but it has moved/changed: <what you found>. Re-scope the recon against the new layout?","proposed":"re-author recon section","note":"<observed layout>"}`.
Leave the ticket in `running/`.

**A2 — State-plane code found built.** Move 4 (or Recon 3) finds `job-state-store` /
`job-coordinator` / claim verbs in either machine's Switchboard. Q3's "defer" and T1-11's
premise are stale — this recon must not quietly report around a moved landscape. Park to
needs-decision/ (same shape; question: "Switchboard state-plane code exists on <machine>:
<evidence>. Q3 deferred this fork assuming it was unbuilt — re-triage T1-11 and this recon?").
Leave in `running/`.

**A3 — Scope breach imminent.** You are about to start/stop/restart/install Switchboard on
either machine, run any WRITE command over SSH (anything beyond `curl localhost/health`,
`cat`, `git log`, `launchctl list`, `ls`), edit any file under `../switchboard/`, or edit any
doc beyond the report + two pins — stop, park to needs-decision/ describing what tempted you.
This ticket ships one report and two banner lines, nothing else.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
test -f docs/switchboard-charter-recon.md && echo OK                    # report exists
grep -c "^## " docs/switchboard-charter-recon.md                        # >= 7 sections
grep -ci "verdict" docs/switchboard-charter-recon.md                    # >= 2 (both headline answers)
grep -n "localhost:5099" docs/switchboard-charter-recon.md              # probe protocol present
grep -n "T1-11" docs/switchboard-charter-recon.md                       # consumer handoff section present
grep -n "switchboard-charter-recon" docs/INDEX.md                       # pin 2
grep -n "switchboard-charter-recon" backlog/2026-06-09-switchboard-greenfield-KICKOFF.md  # pin 1
ls engine/store/results/ | grep -c wg-t8-09                             # 1 — self-report exists
git log --oneline -3 | grep wg-t8-09                                    # commit landed
```

Negative checks (this was recon, not a build or a fix):
```bash
git -C ../switchboard status --porcelain                                # empty — repo untouched
ssh -o ConnectTimeout=4 -o BatchMode=yes roamy 'git -C ~/dev/ad/apps/switchboard status --porcelain'  # empty (skip if F1-B)
launchctl list | grep -i switchboard                                    # unchanged vs Move 2's result
git diff HEAD~1 --name-only | grep -v "docs/switchboard-charter-recon\|docs/INDEX\|2026-06-09-switchboard-greenfield-KICKOFF\|engine/store/results"; echo "extra-files-exit:$?"  # exit 1 — nothing else touched
grep -n "live on MacBook Pro" docs/comms-flow.md                        # STILL present — ledger items were catalogued, not fixed
```
And: `engine/store/needs-decision/` contains a wg-t8-09 file ONLY if an abort fired —
otherwise it must not exist.

## Executor notes (sonnet)

- **Scope fence:** writes are exactly — `docs/switchboard-charter-recon.md` (new), one banner
  line in `backlog/2026-06-09-switchboard-greenfield-KICKOFF.md`, one line in
  `docs/INDEX.md`, your results self-report, and (only on abort) one needs-decision file.
  Read anything on either machine; change nothing else. Both Switchboard repos — local AND
  Roamy's, including their git state — are READ-ONLY. Every SSH command must be from the
  read-only set listed in Abort A3.
- **You are a camera, not a repairman.** The contradiction ledger names stale docs; fixing
  them is T8's broader reconciliation work and T1-11's §9. The ONLY doc-truth writes you make
  are the two pins, both purely additive.
- **A timeout is not a corpse.** The single most important discipline in this ticket: remote
  `curl <host>:5099` failing proves nothing (host-local binding, `src/main.ts` ~line 45).
  "Down" may only be written next to a probe that ran ON that machine's localhost. If you
  can't run one, write "unverifiable".
- **Prefer HITL over guessing** whenever the landscape moved (A1/A2 conditions, a surprise
  charter, divergent Switchboard code): a parked question costs minutes; a false verdict in a
  truth report poisons T1-11's decision doc downstream.
- **The rabbit hole:** resurrecting Switchboard locally "to complete the matrix", fixing the
  four stale docs you catalogue, or wandering into the grounding doc's 9-question interview
  agenda ("maybe I could draft the charter while I'm here"). All out of scope — the charter
  is David-interview-first by explicit KICKOFF design (step 4: "I (David) am the primary
  source… do NOT fabricate answers"), and no agent may author it solo. Skip it.
