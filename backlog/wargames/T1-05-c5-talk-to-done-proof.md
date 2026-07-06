# T1-05 — C5 proof: one real workflow job via talking

| field | value |
|---|---|
| ticket | wg-t1-05-c5-talk-to-done-proof |
| track / size / priority | T1 Engine / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Close the C1→C5 build spine (`docs/north-star.md` §"The build spine") by staging and de-risking
the full north-star loop, run once with evidence: **David speaks intent → Marshall writes a
`kind:workflow` ticket into `engine/store/queue/` → the engine dispatches it to a warm-pool
Swagger → the artifact is verified by the orchestrator (never the worker's word) → David is
told.** One leg of that loop — David speaking — cannot be automated by any ticket, so this war
game's done-bar is: every mechanical leg proven or rehearsed, the one known gap closed (Marshall's
skill predates the engine and doesn't know where the queue is), and a **10-minute drill card**
handed to David that makes the live proof near-certain to succeed on first attempt. The C5 proof
document completes when David runs the drill; this ticket completes when the drill is staged,
de-risked, and surfaced to David.

## Locked context

- Q4 (decisions.md): **everything through the engine** — Marshall's dispatch target IS the engine
  queue; every job ticket is written for sonnet Swagger dispatch. This ratifies teaching Marshall
  the engine-queue idiom.
- Q7: voice/human-comms is IN the portfolio — but as track T9, not here. C5's "talking" is the
  north-star's conversational sense (C2: "Producer: talk → ticket"), satisfied by a live
  interactive Marshall session.
- Spec hard rules: no `-p`/headless/SDK ever; interactive `claude` only; HALT/BACKOFF respected
  implicitly.
- Ticket-first standing rule (`engine/store/queue/.CONVENTION.md`): every unit of work is a
  ticket JSON in the queue — the drill ticket Marshall writes must follow it.

## Recon (verify before any work)

Docs lag code — run every check; these replace doc-trust.

1. `ls engine/orchestrator.py engine/status.py engine/wake.py engine/consumer.py engine/warm_pool.py`
   → all five exist. Missing any → the engine has moved/been refactored since authoring → **Abort A1**.
2. `python3 engine/status.py` → exits 0, prints queue/running/done sections. Errors → **Abort A1**.
3. `ls engine/store/HALT engine/store/BACKOFF 2>/dev/null` → expect **no output** (neither flag
   present). Either present → **Abort A2**.
4. `ls engine/store/WAKE-ARMED 2>/dev/null` → expect absent (dispatch leg ships disarmed; an
   arming anomaly was seen once on 2026-07-06 — see the auto-wake done-ticket's notes). If
   present, note it in the proof scaffold but do NOT disarm or arm anything — record and move on.
5. `launchctl list | grep dark-factory-wake` → expect `com.appydave.dark-factory-wake` loaded
   (the notify leg of the loop). Not loaded → the drill's "notification on ticket queued"
   evidence line won't fire; note it in the drill card as an optional pre-step
   (`bash engine/launchd/install.sh`) — do not install it yourself.
6. `grep -c "engine/store/queue" .claude/skills/marshall/SKILL.md` → expect **0** (the gap this
   ticket closes: Marshall's skill predates the engine, still points at
   `experiments/watchtower-engine/` + a Switchboard/AngelEye preflight). If ≥1 → **Fork F2**
   (a sibling ticket already patched it).
7. `ls .claude/workflows/daily-review.workflow.js .claude/workflows/hello.workflow.js` → both
   exist (verified at authoring). daily-review is the canonical drill payload: real (end-of-day
   digest), read-only gathering, returns a schema'd digest JSON **but writes no file** — the
   drill ticket must name the artifact path explicitly.
8. `ls experiments/watchtower-engine/proof/c1-first-real-run.md` → exists (the proof-doc format
   exemplar; C3 proofs live in the same directory — follow that convention).
9. `python3 engine/status.py` output from check 2: note which queue tickets are **dispatchable**
   (the engine's `dispatchable()` skips external-research/deferred; at authoring the only queued
   ticket, `20260704T0630Z-project-digest-list-and-project-2.json`, is deferred and skipped).
   Other war-game tickets may have been promoted into `queue/` by Phase 5 since — record the
   count; it feeds drill-card Fork F3.

## Moves

**M1 — Rehearse the Workflow tool in this session (the drill's biggest technical unknown).**
- **Do:** In your own session (you ARE a warm-pool sonnet worker — the same species that will run
  the drill job), invoke the Workflow tool on the `hello` workflow (`.claude/workflows/hello.workflow.js`)
  — the cheapest possible payload. Capture the invocation result verbatim.
- **Expect:** The workflow runs to completion and returns output — proving an engine-dispatched
  worker session can execute `kind:workflow` payloads via the Workflow tool.
- **Failure signal:** Workflow tool not present in your tool schema / invocation errors /
  lazy-registration never resolves.
- **Counter-move:** Try invoking `hello` via the Skill tool instead (a `hello` skill is
  registered). If the skill path works, → **Fork F1** (drill executes workflow-as-skill). If
  neither path works, still → **Fork F1 Route B** (drill ticket carries the workflow's own
  gathering steps inline) — record the failure verbatim in the proof scaffold either way.

**M2 — Close the Marshall gap: teach the skill where the engine queue is.**
- **Do:** (Skip if Fork F2 fired.) Append a new section to `.claude/skills/marshall/SKILL.md`
  titled `## Dispatching to the engine (the 2026-07 production engine)` — **additive only, change
  no existing line.** Content, terse and Marshall-voiced: (a) a job dispatch = write a ticket
  JSON into `engine/store/queue/` per `engine/store/queue/.CONVENTION.md`; (b) filename idiom
  `$(date -u +%Y%m%dT%H%MZ)-<slug>.json`; (c) required fields per the convention + existing done/
  tickets: `ticket`, `kind` (workflow|skill|instruction), `title`, `source`, `executor`,
  `priority`, `requested_at`, `requested_by`, `prompt` (self-contained — the worker reads ONLY
  the ticket), plus a verification block (`verify_kind:"generic"` + `verify_spec.checks[]`, or
  the lightweight `artifacts:[...]`/`verify_command` fallback — see `engine/README.md`
  §"Verifying a new ticket kind"); (d) the engine runs via `python3 engine/orchestrator.py
  --pool 1 --teardown` or the armed wake watcher — Marshall never runs workers by hand;
  (e) read state via `python3 engine/status.py` (`--json` for agents).
- **Expect:** `grep -c "engine/store/queue" .claude/skills/marshall/SKILL.md` returns ≥ 2 (the
  section head reference + at least one path in the body); `git diff --stat` shows only
  insertions in that one file.
- **Failure signal:** SKILL.md's structure is unrecognizable vs the 72-line file described here
  (headings like "## The loop", "## Preflight…" absent) — someone rewrote it.
- **Counter-move:** Do not guess a merge → **Abort A3** with your proposed section text in the
  needs-decision payload.

**M3 — Author the drill ticket template.**
- **Do:** Write `backlog/wargames/T1-05-drill-ticket-template.json` — the exact shape Marshall
  should produce during the drill, with `<PLACEHOLDER>` markers for what comes from David's
  actual words. Fields: `"ticket": "<UTC>Z-c5-drill-<slug-from-intent>"`, `"kind": "workflow"`,
  `"title": "C5 drill: <David's intent, near-verbatim>"`, `"source": "spoken intent, David →
  Marshall session, C5 drill (backlog/wargames/T1-05-c5-talk-to-done-proof.md)"`,
  `"executor": "swagger"`, `"priority": "high"`, `"requested_at"/"requested_by"`, a `"prompt"`
  that (for the canonical daily-review intent) instructs the worker: run the `daily-review`
  workflow via the Workflow tool (fallback per Fork F1's rehearsal result — state which path M1
  proved), save the returned digest JSON verbatim to `backlog/wargames/T1-05-drill-digest.json`,
  then write the results self-report as the engine's task prompt directs. Verification block:
  `"verify_kind": "generic"`, `"verify_spec": {"checks": [{"type": "file_exists", "path":
  "backlog/wargames/T1-05-drill-digest.json"}, {"type": "json_parses", "path":
  "backlog/wargames/T1-05-drill-digest.json"}]}`.
- **Expect:** `python3 -c "import json; json.load(open('backlog/wargames/T1-05-drill-ticket-template.json'))"`
  exits 0 (placeholders live inside string values, so the file itself is valid JSON).
- **Failure signal:** json.load raises.
- **Counter-move:** Fix the JSON; placeholders must be `<LIKE-THIS>` inside quoted strings, never
  bare.

**M4 — Author the drill card.**
- **Do:** Write `backlog/wargames/T1-05-drill-card.md` — David's 10-minute runbook, ≤ 90 lines,
  terse. Required sections, in order:
  1. **Preconditions (2 min):** `python3 engine/status.py` clean; no HALT/BACKOFF
     (`ls engine/store/HALT engine/store/BACKOFF` → empty); if other **dispatchable** tickets sit
     in queue/ → drill-Fork D-F3 below; pick dispatch mode → drill-Fork D-F4.
  2. **Leg 1 — talk:** David opens a fresh interactive `claude` session in
     `~/dev/ad/apps/dark-factory`, activates Marshall ("be Marshall" / `/marshall`), and speaks
     (dictation or typed — both are "talking" per north-star C2) his intent. Canonical intent:
     *"Give me the factory's end-of-day review."* If Marshall's constellation preflight fails on
     Switchboard/AngelEye being down, David says: "skip the constellation preflight — C5 drill,
     engine substrate only" (the human waives; the drill must not rabbit-hole into reviving
     Switchboard).
  3. **Leg 2 — ticket:** Marshall writes the ticket into `engine/store/queue/` from the template
     at `backlog/wargames/T1-05-drill-ticket-template.json`, filling placeholders from David's
     actual words. **David must not author or hand-edit the ticket — Marshall-authored is the
     proof point.** Evidence 1: within ~15 s the wake watcher fires a macOS notification
     ("1 ticket(s) queued: …") and appends a `wake:` line to `engine/store/wake.log`.
  4. **Leg 3 — dispatch (D-F4):** Route A (preferred, most lights-off): `bin/factory-wake arm`
     was run in preconditions → wake.py auto-launches `orchestrator.py --teardown --max-wall 900`;
     Route B: David runs `cd engine && python3 orchestrator.py --pool 1 --teardown` himself.
     Evidence 2: a `[dispatch] ticket … -> df-worker-1` line; `tmux attach -t df-worker-1` to
     watch live.
  5. **Leg 4 — verified done:** the orchestrator reaps only after its own `verify()` passes.
     Evidence 3: ticket lands in `engine/store/done/`, digest artifact at
     `backlog/wargames/T1-05-drill-digest.json` parses, `job.completed` event in
     `engine/store/events/`, a line in `engine/store/audit.jsonl`.
  6. **Leg 5 — David told:** `python3 engine/consumer.py --once` (Glass chime on the new event) +
     `python3 engine/status.py` (the "what ran" line) + Marshall surfaces the digest headline
     in-session. (The always-on C4 return leg is a separate T1 ticket — out of drill scope.)
  7. **Evidence harvest + closeout:** a verbatim command block that appends outputs to
     `experiments/watchtower-engine/proof/c5-talk-to-done.md` (ticket JSON from done/, results
     file, event file, wake.log lines, audit line, digest headline), flips the proof doc's status
     line to `PROVEN <date>`, then `bin/factory-wake disarm` if Route A was used, and commits.
  8. **Drill forks:** D-F3 (queue busy: Route A = run anyway, evidence is keyed to the drill
     ticket id and CAP=3 governs; Route B = postpone drill until queue drains) and D-F4 (above).
- **Expect:** file exists; contains all five legs, both drill forks, and the harvest block.
- **Failure signal:** any leg or fork missing on self-read.
- **Counter-move:** Fix before proceeding; the drill card is the deliverable David actually uses
  — an incomplete card fails the whole ticket.

**M5 — Write the proof scaffold.**
- **Do:** Write `experiments/watchtower-engine/proof/c5-talk-to-done.md` following
  `c1-first-real-run.md`'s convention: status line `**Status: STAGED — awaiting David's drill
  (see backlog/wargames/T1-05-drill-card.md)**`, the five-leg loop diagram (one line per leg with
  its evidence source), the M1 rehearsal evidence verbatim (Workflow-tool availability in an
  engine-species worker — including which path worked, per Fork F1), the recon snapshot (flags
  state, launchd wake loaded y/n, queue state), and an empty `## Drill evidence` section the
  harvest block appends into.
- **Expect:** file exists, contains `STAGED` and the M1 evidence.
- **Failure signal:** —
- **Counter-move:** — (pure write; if the proof/ directory is missing, that contradicts recon
  check 8 → **Abort A1**).

**M6 — Commit and tell David.**
- **Do:** `git add` the four files (Marshall SKILL.md patch, drill card, ticket template, proof
  scaffold) + `git commit` with message starting `feat(engine): C5 staged — talk-to-done drill
  card + Marshall engine-queue pointer (wg-t1-05)`. Then fire one macOS notification:
  `osascript -e 'display notification "C5 drill staged — 10 min when ready: backlog/wargames/T1-05-drill-card.md" with title "dark-factory" sound name "Glass"'`.
  Then write your results self-report exactly as your task prompt directs, with the drill-card
  path in `notes`.
- **Expect:** `git log --oneline -1` shows the commit; osascript exits 0.
- **Failure signal:** commit fails (pre-existing dirty/conflicting tree state).
- **Counter-move:** Commit ONLY your four files with explicit paths (`git add <paths> && git
  commit`) — never `git add -A`; if even that conflicts, leave the tree, record the state in
  results notes, and finish (the files on disk are the deliverable; the commit is hygiene).

**M7 — Self-verify.**
- **Do:** Run the Verification block below, top to bottom.
- **Expect:** every check passes; negative checks show no change.
- **Failure signal:** any check fails.
- **Counter-move:** Fix the failing artifact and re-run; if a negative check fails (you modified
  something out of scope), revert that change before finishing.

## Forks

**F1 — Workflow tool unavailable to warm-pool workers.**
Trigger: M1's Workflow-tool invocation fails in your session.
→ **Route A** (skill path works): the drill ticket's prompt says "run the daily-review workflow
via the Skill tool (`daily-review`)" — the ticket keeps `"kind": "workflow"` (the queue idiom
classifies the JOB; the execution mechanism is the worker's business). Record the substitution in
the proof scaffold.
→ **Route B** (neither works): the drill ticket's prompt inlines the daily-review workflow's own
gathering commands + digest schema (copy them from `.claude/workflows/daily-review.workflow.js`
— the agent-prompt block is self-contained). Same artifact path, same verify_spec. Record it —
this is honest evidence that C5's letter ("kind:workflow") is provable while the Workflow-tool-in-
worker mechanism needs its own follow-up ticket.

**F2 — Marshall SKILL.md already knows the engine queue.**
Trigger: Recon check 6 returns ≥ 1 (a sibling war game landed first).
→ **Route A** (existing content covers ticket-writing: queue path + convention + verify block):
skip M2 entirely; note "gap pre-closed by <the section you found>" in the proof scaffold.
→ **Route B** (it mentions the path but not how to author a ticket): add ONLY the missing bullets
to the existing section — never a duplicate section.

*(Drill-time forks D-F3 / D-F4 live inside the drill card — they are David's choices at drill
time, not yours.)*

## Assumptions ledger

1. **"Talking" = a live interactive Marshall session** (voice-dictated or typed), per
   north-star.md's own C2 definition ("Producer: talk → a schema-valid ticket"). OMI capture and
   audio-out are T9's scope (decisions.md Q7), not C5 preconditions. If David rejects this at
   drill time and wants literal voice-in/voice-out → park to needs-decision; do not bolt voice on.
2. **An additive patch to Marshall's SKILL.md is sanctioned** by decisions.md Q4 ("everything
   through the engine"). It is not a `canonical/` artifact, so the no-auto-rewrite rule doesn't
   apply — but it IS David's daily driver, hence additive-only + Abort A3 if its structure has
   changed. If the executor is in any doubt mid-patch → needs-decision with the proposed diff.
3. **daily-review is the canonical drill payload** — chosen because it's real, read-only, and
   self-verifying (digest JSON artifact). David may speak a different intent at drill time; the
   drill card and template accommodate any intent that maps to an existing
   `.claude/workflows/*.workflow.js`. If his intent maps to nothing runnable, the drill card
   tells Marshall to counter-offer the canonical intent rather than improvise a new workflow.
4. **The "David told" bar for C5** = wake queue-notification + consumer chime + status.py line +
   Marshall surfacing the result in-session. The always-on C4 return leg ("every run surfaces a
   one-line what-ran") is a separate T1 ticket; C5 does not wait for it. If David finds the drill's
   told-leg too thin, that's C4 feedback, not a C5 failure.
5. **The drill runs within days of this ticket.** If Phase 5 has since flooded queue/ with
   promoted war-game tickets, drill-Fork D-F3 governs; nothing here goes stale except the recon
   snapshot in the proof scaffold (re-run `python3 engine/status.py` before the drill — the drill
   card's precondition step already does).

## Abort conditions

**A1 — Engine spine missing or broken.** Recon checks 1–2 fail (files absent, status.py errors),
or proof/ directory gone (M5). Park: write `engine/store/needs-decision/wg-t1-05-c5-talk-to-done-proof.json`
— `{"ticket":"wg-t1-05-c5-talk-to-done-proof","question":"Engine layout has changed since this war game was authored (2026-07-06) — which paths moved?","proposed":"Re-recon and re-author the drill against the current engine layout","note":"<what you found instead, exactly>"}`.
Leave the ticket in running/. Never guess new paths.

**A2 — HALT or BACKOFF present.** The factory's governance flags outrank any ticket. Park:
needs-decision as A1's shape with `"question":"HALT/BACKOFF was present when wg-t1-05 started — proceed after clearing, or hold?"`
and the flag file's contents in `note`. Do not clear either flag yourself; do not proceed to any
move (M1 spends tokens; M2 edits David's daily skill — neither happens under a halt).

**A3 — Marshall SKILL.md unrecognizable.** M2's failure signal. Park: needs-decision with
`"question":"Marshall SKILL.md was rewritten since authoring — apply this engine-dispatch section?"`
and your full proposed section text in `proposed`/`note`. Leave the file untouched.

## Verification

Executor's bar (all from repo root; every command must pass):

```bash
# the Marshall gap is closed (or was pre-closed per F2)
grep -q "engine/store/queue" .claude/skills/marshall/SKILL.md

# the drill kit exists and is well-formed
test -f backlog/wargames/T1-05-drill-card.md
grep -q "Leg 5" backlog/wargames/T1-05-drill-card.md         # all five legs present
grep -qi "disarm" backlog/wargames/T1-05-drill-card.md        # closeout step present
python3 -c "import json; json.load(open('backlog/wargames/T1-05-drill-ticket-template.json'))"
grep -q '"kind": "workflow"' backlog/wargames/T1-05-drill-ticket-template.json

# the proof scaffold exists, staged, with rehearsal evidence
test -f experiments/watchtower-engine/proof/c5-talk-to-done.md
grep -q "STAGED" experiments/watchtower-engine/proof/c5-talk-to-done.md

# the work landed as a commit
git log --oneline -20 | grep -q "wg-t1-05"
```

Negative checks (what must NOT have changed):

```bash
# no ticket was queued by this executor — the drill ticket enters queue/ only via Marshall
ls engine/store/queue/ | grep -c "c5-drill" | grep -qx 0

# engine code untouched
git diff HEAD~1 --stat -- engine/*.py | wc -l | grep -qx 0    # (adjust HEAD~1 if unrelated commits intervened: git log --follow -1 -- engine/orchestrator.py predates this ticket)

# wake dispatch leg not armed by this executor
test ! -f engine/store/WAKE-ARMED   # (unless recon check 4 found it already present — then it must be unchanged)
```

Post-drill acceptance (checked by David/Marshall at drill closeout, recorded in the proof doc —
NOT part of this ticket's exit bar): drill ticket in `engine/store/done/`; digest artifact
parses; `job.completed` event exists; audit.jsonl line for the ticket; wake.log shows the
queue-notification; proof doc status flipped to `PROVEN`.

## Executor notes (sonnet)

- **Scope fence:** you may create the four named files and append one section to
  `.claude/skills/marshall/SKILL.md`. You may NOT edit `engine/*.py`, `bin/factory-*`,
  `.claude/workflows/*`, anything under `research/` or `canonical/`, or any other skill. You may
  NOT drop anything into `engine/store/queue/`, arm the wake watcher, or clear HALT/BACKOFF.
- **Never run `orchestrator.py` yourself.** You are (very likely) inside a `df-worker-<n>` tmux
  session dispatched by a live orchestrator; booting a second WarmPool collides on the
  `df-worker-1..N` tmux session names. The engine pass belongs to the drill (David's terminal or
  the armed wake watcher), never to you.
- **Style:** terse, David's voice — short phrases, no marketing prose, no walls. The drill card
  is ≤ 90 lines. The Marshall section is additive and reads like the rest of that skill.
- **HITL preference:** anything that smells like a judgment call on Marshall's behavior beyond
  the one additive section → needs-decision, not initiative.
- **The rabbit hole:** the constellation preflight (Switchboard/AngelEye DOWN) will tempt you to
  "fix the preflight" or revive Switchboard so Marshall starts clean. **Skip it.** The drill card
  handles it with one human sentence; Switchboard's state authority is its own war game (T1-11).
