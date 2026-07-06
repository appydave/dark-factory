# T7-09 — KDD structural SDLC gates

| field | value |
|---|---|
| ticket | wg-t7-09-kdd-sdlc-gates |
| track / size / priority | T7 Self-learning / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

David's PO direction (2026-07-04, recorded verbatim at the bottom of
`backlog/2026-07-04-kdd-read-gate-handover.done.md` and in ADR-0028's Revision Log
"superseded (partially)" entry): the kdd-bridge MCP was the *mechanism*, not the integration —
the real home for KDD-reading is **structural SDLC gates**: (a) "PR created → BEFORE developing
it, validate against KDD decisions"; (b) "absorbing worker output → write back through Lisa" —
checkpoints in the workflow, not a session-start advisory. This ticket designs and builds the
advisory-first version of BOTH gates inside dark-factory's own SDLC, which is the engine ticket
lifecycle (this repo has no PRs — David works on main and engine workers commit directly, so
"PR created" maps to "ticket dispatched"). Deliverables: **(1)** a design doc
`docs/kdd/sdlc-gates.md` pinning both gate contracts + the enforcement ladder + the cross-repo
generalization as future scope; **(2) Gate A built** — the engine's dispatch prompt
(`engine/orchestrator.py::task_prompt()`) gains a pre-work KDD-decisions checkpoint instructing
every worker to check accepted decisions before its first edit and to park a conflict to
`needs-decision/` instead of proceeding; **(3) Gate B built** — a stdlib-only
`engine/kdd_absorb.py` that tracks which `done/` tickets have been absorbed through Lisa (ledger
`engine/store/kdd-absorbed.jsonl`), and emits ONE deferred absorption ticket batching the
unabsorbed backlog (17 done tickets at authoring) for a Lisa Mode-1 capture pass; **(4)** three
append-only wiring edits (kdd index pointer, ADR-0028 Revision Log line, engine/README layout
line); **(5)** proof report + commit + push. Done = both gates demonstrably in place (executable
checks below), the first absorption ticket sits in `queue/` as `status:"deferred"` awaiting
David's un-defer, and nothing else in the engine's behavior changed.

## Locked context

- **Q4 (plans/wargames/decisions.md):** everything through the engine — this war game is
  written for sonnet Swagger dispatch; self-report to `engine/store/results/` per the
  orchestrator's task prompt.
- **Q9 (decisions.md):** "complement don't replace" — the gates COMPLEMENT the kdd-bridge MCP
  and the SessionStart advisory hook (both stay untouched); ADR-0028's own Revision Log says the
  MCP "serves those checkpoints, it doesn't replace them."
- **ADR-0028's stated enforcement preference:** "try advisory-injection first … only harden to a
  hard-block if it's still skipped in practice." Both gates ship advisory-first. Hardening is a
  design-doc v2 line item, not built here.
- **No `-p`/headless/SDK ever; interactive `claude` only** (spec rule + ADR-0004): the engine
  cannot run Lisa itself — Gate B therefore works by EMITTING a ticket that a Swagger worker
  session (which has the Lisa plugin skill) executes. Ticket-first standing rule
  (`engine/store/queue/.CONVENTION.md`) says every unit of work gets a ticket anyway.
- **Repo hard rule (CLAUDE.md):** never write skill code into `~/dev/ad/appydave-plugins/`.
  "Lisa owns these structures" long-term, but the Lisa-side checkpoint skill for PR-based repos
  (SupportSignal etc.) is design-doc future scope only — nothing in appydave-plugins is edited.
- **Assessment-mode default (CLAUDE.md) + DF-ADR format:** ratified artifacts are never
  rewritten in place; ADR-0028's Revision Log is explicitly append-only
  (`docs/kdd/ADR-FORMAT-SPEC.md` line ~107: "Revision Log ← append-only") and already carries
  three post-ratification appends — one more line is the sanctioned change mechanism.
- **No cron / no standing schedule** (unknowns-map §B: a live cron is a standing commitment
  needing an explicit go): running `kdd_absorb.py` stays manual; trigger options are documented,
  not wired.

## Recon (verify before any work)

Repo root `/Users/davidcruwys/dev/ad/apps/dark-factory`; all paths relative to it unless
absolute. Docs lag code — trust only these checks.

1. **The mandate exists on disk.**
   `grep -n "STRUCTURAL SDLC GATES" backlog/2026-07-04-kdd-read-gate-handover.done.md` → the
   "David's design direction on the read-gate" section (verified present 2026-07-06, final
   section of the file, names both gates (a) and (b) and "Lisa owns these structures").
   `grep -n "superseded (partially)" docs/kdd/decisions/0028-close-the-kdd-lisa-read-gate-the-write-loop-is-built-read-en.md`
   → the Revision Log entry restating the same direction (verified). **Either missing** →
   Abort A1.
2. **No prior build.** `ls docs/kdd/sdlc-gates.md engine/kdd_absorb.py engine/store/kdd-absorbed.jsonl 2>&1`
   → all three "No such file" (verified 2026-07-06); `grep -rin "sdlc.gate" docs/ engine/ | grep -v wargames`
   → no hits. **Any exists** → Fork F1.
3. **Gate A's anchor.** `grep -n "def task_prompt" engine/orchestrator.py` → line ~242
   (verified); the function's docstring says "Kept single-line for tmux send-keys -l safety"
   — any text you inject MUST keep the returned string newline-free. `grep -n "^NEEDS, DEC"
   engine/orchestrator.py` → line ~57: `NEEDS, DEC = (os.path.join(STORE, d) for d in
   ("needs-decision", "decisions"))` — `NEEDS` is module-level and usable inside
   `task_prompt()` (the gated branch already does `nd = os.path.join(NEEDS, tid)`).
   **`task_prompt` absent/renamed** → Fork F3.
4. **The advisory-gate honesty fact.** `grep -n 'if a\["gated"\] and not artifact_ok' engine/orchestrator.py`
   → line ~600: the reap loop polls `needs-decision/` ONLY for HITL-gated tickets (verified).
   Consequence you must carry into the design doc: an UNGATED worker that parks
   `needs-decision/<tid>` and stops will eventually read as `failed(timeout)` in the run
   report — the parked file is the durable surfaced question, the status line is cosmetic v1
   debt. Do not "fix" the reap loop (T1-track territory).
5. **Gate B's dispatch-safety anchor.** `grep -n '"deferred" in' engine/orchestrator.py` →
   inside `dispatchable()` (line ~197, verified): tickets with "deferred" in `status` or
   `priority` are skipped by the pool and stay in `queue/` untouched. This is what makes
   emitting the absorption ticket into a live queue safe. **Check absent** → Fork F2.
6. **Absorption source shape.** `ls engine/store/done/*.json | wc -l` → 17 at authoring;
   `ls engine/store/results/*.json | wc -l` → 4 at authoring. The asymmetry is real: most done
   tickets have NO results file (pre-results-era tickets, builder-agent tickets,
   external-research answers). Gate B must absorb from `done/<t>.json` always and treat
   `results/<t>.json` as optional enrichment. Record the counts you actually observe.
7. **Lisa is loadable where absorption will run.**
   `grep -n "Mode 1 — Capture" ~/dev/ad/appydave-plugins/appydave/skills/lisa/SKILL.md` → the
   capture-mode heading (verified; dedup-first, bump-don't-mint, "never scaffold a KDD tree as
   a side effect"). `grep -o '"appydave@appydave-plugins"' ~/.claude/plugins/installed_plugins.json`
   → installed (v5.12.1+ expected per `backlog/2026-07-04-kdd-uniformity-findings.md`). Record
   the version. **Skill dir absent** → not a blocker for BUILDING the gate (Lisa is invoked at
   absorption-run time, not now) — flag prominently in the report instead.
8. **What must stay untouched.** `grep -n "kdd-bridge" .mcp.json .claude/settings.json` → MCP
   registration + `grep -c "SessionStart" .claude/settings.json` → 1 (the ADR-0028 advisory
   hook). Both verified present 2026-07-06; both survive this ticket byte-identical.
9. **KDD tree + ratification state.** `ls docs/kdd/` → `ADR-FORMAT-SPEC.md index.md _runs
   decisions learnings patterns`; `grep -c "accepted" docs/kdd/decisions/index.md` → only
   ~3 ADRs are `accepted` (0009, 0028, 0031); the other ~39 are `proposed`, ratified lazily
   "whenever each one is about to matter." Gate A validates against ACCEPTED decisions; a
   ticket whose territory touches a PROPOSED one is exactly the lazy-ratification trigger —
   this observation goes in the design doc, not into more machinery.
10. **Queue state at execution time.** `ls engine/store/queue/` → 1 non-dispatchable deferred
    ticket at authoring (`20260704T0630Z-project-digest-list-and-project-2.json`). Whatever you
    find, your only addition to `queue/` is the single `kdd-absorb-*` ticket from M6.

## Moves

### M1 — Read the mandate and the Lisa contract (no writes)

- **Do:** Read in full: (1) the final two sections of
  `backlog/2026-07-04-kdd-read-gate-handover.done.md` (David's design direction + the Roamy
  note); (2) ADR-0028 end-to-end, especially Alternatives ("advisory-injection first") and all
  Revision Log entries; (3) `~/dev/ad/appydave-plugins/appydave/skills/lisa/SKILL.md` Mode 1
  (Capture) only — the 6-step procedure and its scope guard; (4)
  `docs/kdd/ADR-FORMAT-SPEC.md` (Revision Log append rule, ~line 107). Write down, before
  designing anything, the two gate statements in David's own words and the one enforcement
  preference sentence from ADR-0028.
- **Expect:** you can state Gate A and Gate B in one line each, cite where each came from, and
  name why v1 is advisory.
- **Failure signal:** the handover's direction section and ADR-0028's revision entry disagree
  about what the gates are.
- **Counter-move:** the handover doc wins — it is David's verbatim PO feedback; the ADR entry
  is a paraphrase. Note the discrepancy in the report. If the handover section itself is
  missing → Abort A1.

### M2 — Write the design doc `docs/kdd/sdlc-gates.md`

- **Do:** Create `docs/kdd/sdlc-gates.md`, ≤200 lines, with exactly these sections:
  1. **Mandate** — the two gates quoted from the handover doc (cite path + section name) and
     ADR-0028's revision entry; one line on why the MCP bridge serves-not-replaces them.
  2. **The dark-factory mapping** — no PRs here: "PR created" → "ticket dispatched"
     (`task_prompt()`); "absorbing worker output" → "done/ ticket reaped". State that the
     PR-form of Gate A applies to PR-based repos (SupportSignal etc.) and is future scope.
  3. **Gate A contract** — trigger: every ungated dispatch. Check: worker reads
     `docs/kdd/decisions/index.md`, opens any ACCEPTED decision touching the ticket's
     territory; contradiction → write `engine/store/needs-decision/<tid>` naming the ADR id +
     the conflict, reply `BLOCKED_BY_DECISION`, make no edits. Honesty paragraph (Recon 4):
     v1, an ungated park reads as `failed(timeout)` in the run report; the parked file is the
     durable question. Note the gated/HITL branch is deliberately not modified (it already has
     a human in the loop pre-work). Note Gate A doubles as the lazy-ratification trigger for
     PROPOSED ADRs (Recon 9).
  4. **Gate B contract** — the engine cannot run Lisa (interactive-only rule), so absorption is
     ticket-shaped: `engine/kdd_absorb.py` tracks a ledger
     (`engine/store/kdd-absorbed.jsonl`, append-only JSONL: `ticket`, `absorbed_at`, `by`,
     `verdict`), `--status` lists unabsorbed done tickets, `--emit-ticket` writes ONE batched
     absorption ticket (deferred). The absorption worker runs Lisa Mode 1 per ticket:
     verdict ∈ learning / decision / pattern-bump / none — **none is a fine verdict; absorb ≠
     always write** (Lisa's dedup discipline governs). Ledger line appended per ticket
     regardless of verdict.
  5. **Enforcement ladder** — v1 advisory (this ticket) → v2 reap-loop polls `needs-decision/`
     for ALL tickets, not just gated (T1-track territory, not built here) → v3 hard-block only
     if advisory is measurably skipped (ADR-0028's own bar).
  6. **Triggers deliberately not wired** — manual `--status`/`--emit-ticket` only; cron/launchd
     is a standing commitment needing David's explicit go; candidate trigger points listed
     (end of an orchestrator run, status.py surfacing, morning briefing).
  7. **Relations** — kdd-bridge MCP + SessionStart hook (session-level, untouched); T7-04
     lineage log (skim layer under ADRs); T7-05 daily digest (human-facing summary, different
     purpose); T1-04 return leg (surfacing to David, not knowledge write-back).
- **Expect:** file exists, all 7 sections present, `wc -l` ≤ 200.
- **Failure signal:** you are speccing Lisa skill changes, PR webhooks, or hook enforcement
  code — that is v2+/cross-repo scope.
- **Counter-move:** move that text into section 5/2 as future scope (one line each) and return
  to the two v1 contracts.

### M3 — Build Gate A: the dispatch-prompt checkpoint

- **Do:** In `engine/orchestrator.py::task_prompt()`, ungated branch only: (1) move/add
  `nd = os.path.join(NEEDS, tid)` so it is computed before BOTH branches (it currently exists
  only inside the `if gated:` block); (2) in the ungated `return` f-string, immediately after
  `"…and execute them exactly, in this repo. "`, insert this text (keep it inside the same
  single-line f-string; `{{`/`}}` are the required f-string escapes for literal braces):
  ```
  GATE-A (KDD, ADR-0028): before your first edit, read docs/kdd/decisions/index.md and open any ACCEPTED decision whose territory this ticket touches; if the ticket's instructions would contradict an accepted decision, make NO edits — use the Write tool to create {nd} containing {{"ticket":"{tid}","question":"Ticket conflicts with <ADR-id>: <one line>","note":"<the conflicting instruction vs the ADR line>"}} , reply with exactly BLOCKED_BY_DECISION and stop.
  ```
  (3) `python3 -m py_compile engine/orchestrator.py` → exit 0. Do NOT touch the gated branch,
  `resume_prompt()`, the reap loop, `dispatchable()`, or anything else in the file.
- **Expect:** `git diff engine/orchestrator.py` shows changes confined to `task_prompt()`;
  py_compile silent.
- **Failure signal:** py_compile error (usually brace-escaping in the f-string), or the diff
  leaks outside `task_prompt()`.
- **Counter-move:** fix the f-string escapes (`{{` `}}` for literal braces; `{nd}`/`{tid}`
  interpolated); if the diff leaked, `git checkout -- engine/orchestrator.py` and redo as a
  single surgical edit. Second failure → Fork F3.

### M4 — Prove Gate A without running the engine

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory/engine && python3 - <<'EOF'
  import orchestrator as o
  p = o.task_prompt("wg-test-dummy.json")
  assert "GATE-A" in p and "BLOCKED_BY_DECISION" in p, "gate sentence missing"
  assert "\n" not in p, "prompt no longer single-line (tmux send-keys -l unsafe)"
  assert "needs-decision" in p, "park path not interpolated"
  g = o.task_prompt("wg-test-dummy.json", gated=True)
  assert "GATE-A" not in g, "gated branch must be unchanged"
  print("GATE-A-PROOF-PASS")
  EOF
  ```
  (Safe: `task_prompt()` only joins paths — verified at authoring it reads no files; importing
  `orchestrator` executes only constant definitions, `main()` is `__main__`-guarded.)
- **Expect:** `GATE-A-PROOF-PASS`.
- **Failure signal:** an assertion fires, or import itself errors.
- **Counter-move:** single-line assert firing → your inserted text contains a literal newline;
  re-edit to one physical line. Import error → py_compile lied about nothing; read the
  traceback, fix, re-run M3's compile. Second failure → Fork F3.

### M5 — Build Gate B: `engine/kdd_absorb.py`

- **Do:** Write `engine/kdd_absorb.py`, stdlib-only (json/os/sys/argparse/datetime), mirroring
  orchestrator.py's path idiom (`STORE` relative to the file's own dir). Contract:
  - `LEDGER = engine/store/kdd-absorbed.jsonl`; missing ledger == empty ledger (never crash,
    never auto-create on read).
  - `unabsorbed()` = `.json` files in `store/done/` MINUS ticket names in the ledger MINUS any
    filename containing `kdd-absorb` (self-exclusion: absorption tickets are never themselves
    absorption input — no recursion).
  - `--status`: print total done / absorbed / unabsorbed counts + the unabsorbed filenames,
    one per line; exit 0 always.
  - `--emit-ticket [--batch N]` (default N=10): **guard first** — if any filename in
    `store/queue/` or `store/running/` contains `kdd-absorb`, print
    `absorption ticket already pending: <name>` and exit 1 (never two in flight). Otherwise
    write `store/queue/kdd-absorb-<UTC yyyymmddThhmmZ>.json`, Family-A shape:
    `kind:"instruction"`, `title:"Gate B: absorb worker output through Lisa (<n> done tickets)"`,
    `source:"engine/kdd_absorb.py (docs/kdd/sdlc-gates.md Gate B, wg-t7-09)"`,
    `executor:"swagger"`, `priority:"normal"`, **`status:"deferred"`**, real UTC
    `requested_at`, `requested_by:"engine/kdd_absorb.py (Gate B)"`, `depends_on:[]`; `prompt`
    self-contained: list the batch's ticket filenames explicitly; for each, read
    `engine/store/done/<t>` plus `engine/store/results/<t>` if present; apply Lisa Mode 1
    (capture) judgment with its dedup discipline — verdict learning / decision / pattern-bump /
    none, "none is a valid verdict, do not force a write"; for every verdict append one JSONL
    line `{"ticket":"<t>","absorbed_at":"<UTC>","by":"<ticket-id>","verdict":"<verdict>"}` to
    `engine/store/kdd-absorbed.jsonl`; `verify`: "one ledger line exists in
    engine/store/kdd-absorbed.jsonl for every batch ticket".
  - `python3 -m py_compile engine/kdd_absorb.py` → exit 0.
- **Expect:** file ≈100–150 lines; compiles clean.
- **Failure signal:** you are importing non-stdlib modules, adding a scheduler/daemon loop, or
  writing the ledger from `--emit-ticket` (the ledger is written by the ABSORPTION WORKER, not
  the emitter).
- **Counter-move:** delete the extras — the script is a ledger-diff + one ticket-writer,
  nothing more. If tempted to auto-run the orchestrator after emitting: don't (deferred by
  design, Assumption 3).

### M6 — Prove Gate B end-to-end at the file level

- **Do:** From `engine/`:
  1. `python3 kdd_absorb.py --status` → counts match Recon 6 (unabsorbed = done count, since
     no ledger exists yet); exit 0.
  2. `python3 kdd_absorb.py --emit-ticket` → prints the created ticket path; exactly one new
     `store/queue/kdd-absorb-*.json` exists; `python3 -c "import json;
     t=json.load(open('<path>')); assert t['status']=='deferred' and t['executor']=='swagger'
     and t['kind']=='instruction'; print('TICKET-SHAPE-PASS')"`.
  3. `python3 kdd_absorb.py --emit-ticket` again → guard message, exit 1, still exactly ONE
     `kdd-absorb-*` file in `queue/`.
  4. Dispatch-safety: `python3 -c "import orchestrator; print(orchestrator.dispatchable('<the
     kdd-absorb filename>'))"` → `False` (the deferred skip, Recon 5) — the live pool will not
     pick it up.
  5. `python3 kdd_absorb.py --status` → the emitted ticket does NOT appear as unabsorbed
     (self-exclusion) and done-ticket counts are unchanged.
- **Expect:** all five observations as stated.
- **Failure signal:** step 4 prints `True` — the deferred skip is not honored by the
  orchestrator version on disk.
- **Counter-move:** → Fork F2 immediately (remove the ticket from `queue/` first:
  `mv store/queue/kdd-absorb-*.json store/kdd-absorb-DRAFT.json`). Any other step failing is a
  bug in YOUR script — fix and re-run; the guard test (step 3) failing twice → re-read the
  guard spec in M5, it is a substring check on two directories, nothing clever.

### M7 — Wiring: three append-only edits

- **Do:**
  1. Append to the END of `docs/kdd/index.md`:
     ```markdown

     ## SDLC gates (structural read/write checkpoints)

     [sdlc-gates.md](sdlc-gates.md) — Gate A (pre-work decisions checkpoint in the engine
     dispatch prompt) + Gate B (worker-output absorption through Lisa,
     `engine/kdd_absorb.py`). David's 2026-07-04 direction; ADR-0028's structural successor.
     ```
  2. Append ONE line to ADR-0028's `## Revision Log` (nothing above it changes):
     `- <today ISO> — extended — structural SDLC gates designed + built per the 2026-07-04 PO direction: Gate A (dispatch-prompt decisions checkpoint) + Gate B (engine/kdd_absorb.py → Lisa absorption tickets). Design: docs/kdd/sdlc-gates.md (wg-t7-09).`
  3. In `engine/README.md`'s layout block, add one line after the `consumer.py` entry:
     `  kdd_absorb.py     Gate B (docs/kdd/sdlc-gates.md): ledger-diff of done/ vs kdd-absorbed.jsonl; --status / --emit-ticket (emits a DEFERRED Lisa-absorption ticket)`
- **Expect:** `git diff --numstat docs/kdd/index.md docs/kdd/decisions/0028-*.md` → 0 deleted
  lines on both (pure appends); README diff is one added line.
- **Failure signal:** any deletion count > 0, or the ADR edit landed outside the Revision Log.
- **Counter-move:** `git checkout -- <file>` and re-append with `cat >>` (index) / a
  single-line Edit anchored on the last existing Revision Log entry (ADR).

### M8 — Proof report, commit, push

- **Do:** `mkdir -p backlog/wargames/proof/T7-09` and write
  `backlog/wargames/proof/T7-09/REPORT.md`: (1) what was built (paths); (2) Gate A proof output
  (M4) + Gate B proof observations (M6, all five); (3) mandatory findings: (a) the advisory-gap
  honesty fact (ungated park reads as failed(timeout) — v2 pointer); (b) only ~3/42 ADRs
  accepted — Gate A doubles as the lazy-ratification trigger; (c) the done/results asymmetry
  you observed (Recon 6 counts); (d) Lisa plugin version found (Recon 7); (e) the emitted
  absorption ticket path + explicit instruction to David: "un-defer by removing
  `\"status\":\"deferred\"` from <path> (or via triage) to run the first absorption batch";
  (f) anything else surfaced. Then:
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add docs/kdd/sdlc-gates.md docs/kdd/index.md docs/kdd/decisions/0028-*.md \
    engine/orchestrator.py engine/kdd_absorb.py engine/README.md \
    engine/store/queue/kdd-absorb-*.json backlog/wargames/proof/T7-09/
  git commit -m "feat(kdd): structural SDLC gates — Gate A dispatch checkpoint + Gate B Lisa absorption (wg-t7-09)"
  git push
  ```
  Finally write the results JSON to `engine/store/results/` per your dispatch instructions.
- **Expect:** commit exists containing exactly the listed paths; push succeeds (a failed push
  is a report note, not a blocker); `git status --short` clean under those paths.
- **Failure signal:** unrelated files staged (a dirty shared tree is a known hazard —
  `docs/kdd/learnings/blind-git-add-*.md`).
- **Counter-move:** `git restore --staged <stray>`, re-commit with the explicit path list
  above only. Never `git add -A`.

## Forks

**F1 — Some of it already exists.**
Trigger: Recon 2 finds `docs/kdd/sdlc-gates.md`, `engine/kdd_absorb.py`, or the ledger already
on disk.
→ **Route A** (partial — e.g. the doc exists but no code, or a differently-named absorption
script exists): read what exists first; build only the missing halves and make the design doc
reconcile with (never duplicate) the existing piece; record in the report who/what built the
prior piece if discoverable via `git log --oneline -- <path>`.
→ **Route B** (both gates demonstrably built and wired — the M4/M6-equivalent checks already
pass against existing code): the ticket is already done → Abort A2.

**F2 — The deferred-skip is not in the orchestrator at execution time.**
Trigger: Recon 5's grep misses, or M6 step 4 prints `True`.
→ **Route A** (the skip exists under a changed shape — `dispatchable()` still filters
deferred somehow): adapt the M6 step-4 check to the current mechanism, verify `False`,
proceed.
→ **Route B** (no deferred filtering at all): do NOT leave the absorption ticket in a live
`queue/` — write it to `engine/store/kdd-absorb-DRAFT.json` instead, state in the report and
the design doc that promotion = `mv` into `queue/` once a skip mechanism exists, and flag the
regression (the kind-filter shipped 2026-07-06, commit 7c619f7 — its absence means someone
removed it → report finding, T8 territory).

**F3 — `task_prompt()` has drifted or vanished.**
Trigger: Recon 3 can't find the function, or M3/M4 fail twice on a shape mismatch (another
ticket — T1 track exercises this file — may land engine changes first).
→ **Route A** (function exists, string shape differs): inject the same GATE-A sentence into
whatever the current ungated dispatch text is, preserving its single-line property; re-run M4.
→ **Route B** (function renamed/removed, dispatch prompting restructured): stop touching the
engine → Abort A3.

## Assumptions ledger

1. **"PR created" maps to "ticket dispatched" in this repo.** Plausible: dark-factory has no
   PR flow (solo-main preference; engine workers commit directly; `commit()` in
   orchestrator.py is just a rename running→done). The literal-PR form of Gate A belongs to
   PR-based repos and is documented as future scope (design doc §2). If David meant
   PR-gates-first-everywhere → the design doc still stands as the dark-factory instance;
   park the cross-repo question to needs-decision only if he raises it at review.
2. **Advisory-first is the sanctioned enforcement level.** Grounded in ADR-0028's own
   Alternatives text. False branch (David wants hard-block now): the design doc's enforcement
   ladder names exactly what v2/v3 require; write needs-decision and stop rather than building
   reap-loop changes that collide with T1 tickets.
3. **The first absorption ticket ships `status:"deferred"`.** Grounded in: `dispatchable()`'s
   deferred skip (Recon 5), the wait-for-go-on-irreversible-actions preference (a 17-ticket
   Lisa run is a real spend), and HITL-by-default for first runs of new machinery. False
   branch (David wanted it live immediately): un-deferring is a one-field edit, named
   explicitly in the report.
4. **A one-line Revision Log append to ratified ADR-0028 is sanctioned.** Grounded in
   ADR-FORMAT-SPEC's "append-only" Revision Log design + ADR-0028's three existing
   post-ratification appends. False branch (spec read says otherwise at execution): skip M7
   step 2, note in the report — the design doc's mandate section carries the link anyway.
5. **`engine/store/kdd-absorbed.jsonl` is the right ledger home.** Grounded in: the store is a
   growing ledger by design (orchestrator header comment; `audit.jsonl` precedent lives
   there). False branch (David prefers `docs/kdd/_runs/`): `mv` + one path constant change;
   flag in report, don't ask first.
6. **The Lisa plugin will be present in the absorption worker's session.** Grounded in Recon 7
   (installed v5.12.1+ per the uniformity findings). If absent at absorption time, that run —
   not this build — fails visibly; the emitted ticket's prompt tells the worker to park to
   needs-decision if `/lisa` is unavailable rather than imitating Lisa by hand. Bake that
   sentence into the emitted prompt.

## Abort conditions

Park action for ALL aborts: write
`engine/store/needs-decision/wg-t7-09-kdd-sdlc-gates.json` containing
`{"ticket":"wg-t7-09-kdd-sdlc-gates","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort.

- **A1 — Mandate unverifiable.** The handover doc's "David's design direction" section AND
  ADR-0028's "superseded (partially)" revision entry are both missing/changed (Recon 1). The
  ticket's entire premise is David's stated direction; if it can't be verified on disk, do not
  reconstruct it from this war game's own summary. Question: "T7-09's mandate texts are
  missing from backlog/2026-07-04-kdd-read-gate-handover.done.md / ADR-0028 — has the SDLC-gates
  direction been superseded, or were the files moved?"
- **A2 — Already built** (F1 Route B). Question: "Both SDLC gates appear already built and
  passing proofs (<paths>) — mark T7-09 obsolete, or is a v2/hardening pass wanted?"
- **A3 — Engine restructured** (F3 Route B). Question: "engine/orchestrator.py no longer has a
  task_prompt()-shaped dispatch seam (<what was found>) — where should Gate A's checkpoint
  attach in the new engine shape?"

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory`. Positive:

```bash
test -f docs/kdd/sdlc-gates.md && [ "$(wc -l < docs/kdd/sdlc-gates.md)" -le 200 ] && echo PASS-1
grep -q "Gate A" docs/kdd/sdlc-gates.md && grep -q "Gate B" docs/kdd/sdlc-gates.md && grep -qi "advisory" docs/kdd/sdlc-gates.md && echo PASS-2
grep -q "GATE-A" engine/orchestrator.py && echo PASS-3
python3 -m py_compile engine/orchestrator.py engine/kdd_absorb.py && echo PASS-4
cd engine && python3 -c "
import orchestrator as o
p = o.task_prompt('wg-test-dummy.json')
assert 'GATE-A' in p and chr(10) not in p
assert 'GATE-A' not in o.task_prompt('wg-test-dummy.json', gated=True)
print('PASS-5')" && cd ..
cd engine && python3 kdd_absorb.py --status > /dev/null && echo PASS-6 && cd ..
ls engine/store/queue/kdd-absorb-*.json 2>/dev/null | wc -l | grep -qx '1' && echo PASS-7   # (or the DRAFT file if F2 Route B fired — then check store/kdd-absorb-DRAFT.json)
python3 -c "import json,glob; t=json.load(open(glob.glob('engine/store/queue/kdd-absorb-*.json')[0])); assert t['status']=='deferred' and t['executor']=='swagger' and 'lisa' in t['prompt'].lower(); print('PASS-8')"
cd engine && python3 kdd_absorb.py --emit-ticket >/dev/null 2>&1; [ $? -eq 1 ] && echo PASS-9 && cd ..   # guard blocks a second emission
tail -8 docs/kdd/index.md | grep -q "sdlc-gates" && echo PASS-10
grep -q "wg-t7-09" docs/kdd/decisions/0028-*.md && echo PASS-11
grep -q "kdd_absorb" engine/README.md && echo PASS-12
test -f backlog/wargames/proof/T7-09/REPORT.md && echo PASS-13
git log --oneline -5 | grep -qi "sdlc gates\|wg-t7-09" && echo PASS-14
```

Negative (must NOT be true):

```bash
test -f engine/store/kdd-absorbed.jsonl && echo FAIL-ledger-prewritten || echo NEG-1        # ledger is written by the absorption WORKER, not this ticket
git diff HEAD~1 --numstat -- docs/kdd/index.md docs/kdd/decisions/0028-*.md | awk '$2>0{f=1} END{exit f}' && echo NEG-2   # both appends: 0 deleted lines
git diff HEAD~1 -- engine/orchestrator.py | grep -E '^[-+].*def ' | grep -v task_prompt | grep -q . || echo NEG-3          # no other function touched
git diff HEAD~1 --name-only | grep -q '.claude/settings.json\|.mcp.json' || echo NEG-4      # SessionStart hook + MCP registration untouched
git -C ~/dev/ad/appydave-plugins diff --quiet && echo NEG-5                                 # Lisa/plugins repo untouched
ls engine/store/done | grep -qi 'kdd-absorb' || echo NEG-6                                  # the absorption ticket was NOT executed by this run (it is deferred)
git diff HEAD~1 --name-only | grep -qE 'docs/kdd/(learnings|patterns)/' || echo NEG-7       # no KDD content written by hand — that is the absorption worker's job, through Lisa
```

## Executor notes (sonnet)

- **Scope fence:** write ONLY `docs/kdd/sdlc-gates.md`, `engine/kdd_absorb.py`, ONE
  `engine/store/queue/kdd-absorb-*.json` (or the F2 DRAFT), the three append-only wiring edits
  (kdd index / ADR-0028 Revision Log / engine README), `backlog/wargames/proof/T7-09/`, and
  your results JSON. NEVER touch: the reap loop / `dispatchable()` / `resume_prompt()` /
  gated branch in orchestrator.py, `status.py`, `consumer.py`, `.claude/settings.json`,
  `.mcp.json`, anything in `~/dev/ad/appydave-plugins/` or `~/dev/ad/apps/kdd-bridge/`
  (read-only evidence), `docs/kdd/learnings|patterns/`, and every other ADR.
- **Do not run `orchestrator.py` (main) at any point** — you are almost certainly being run BY
  it. Your engine proofs are py_compile + function-level imports only (M4, M6). The edited
  `task_prompt()` takes effect on the pool's next boot, which is not your concern.
- **Do not perform any Lisa capture yourself.** Gate B's whole point is that absorption goes
  THROUGH Lisa in a worker session David has un-deferred. Hand-writing learnings/decisions
  into `docs/kdd/` from the done tickets would defeat the ticket you are implementing (NEG-7
  checks this).
- Prefer HITL over guessing: conflicting mandate texts → handover wins + report note; missing
  mandate → abort; engine shape drift → Fork F3, never improvise a new dispatch seam.
- **The rabbit hole:** the 17 done tickets are full of interesting content (a 13-source
  research answer sits in `results/`). Do not read them all, summarize them, or start
  classifying verdicts — Gate B ships the MECHANISM; the batch's content is the absorption
  worker's job. Your only contact with `done/` is `ls`-level counting and filenames for the
  emitted ticket's batch list.
