# T2-06 — Five-day briefing→BA→tickets proof

| field | value |
|---|---|
| ticket | wg-t2-06-five-day-briefing-proof |
| track / size / priority | T2 Producer/BA / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t2-01 (BA agent build — gate by artifact, not by ticket id; see Recon 2) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Run the daily operating model's own acceptance test: the full Step-0 morning loop —
briefing (project-digest) → BA conversation (Producer/C2) → day's tickets into the engine —
executed live for five days, with every friction point captured and distilled into a verdict.
`docs/daily-operating-model.md` §6 defines done as *"a real day run start-to-finish"*; this
ticket makes that measurable ×5. **A single Swagger dispatch cannot span a week and cannot
speak for David**, so (precedent: T1-05's drill-card done-bar) this ticket's done-bar is:
the five-day proof **staged, mechanically rehearsed, and armed** — a run harness
(`backlog/wargames/runs/T2-06/`) with a one-page morning PROTOCOL, a day-log template, a
friction register pre-seeded with known capability gaps, five staged per-day auditor tickets
(day-5 carries the retro + verdict), a day-0 mechanical rehearsal proving every non-David leg,
and a kickoff note David's own next briefing will surface. The proof itself then runs over the
following week, carried by the day tickets; day-5's auditor writes `RETRO.md` with a
PASS/PARTIAL/FAIL verdict against the bar in PROTOCOL.md.

## Locked context

- **Q4 (decisions.md): everything through the engine** — the per-day audit work is itself
  engine tickets in `engine/store/queue/`, moving queue→running→done like any other.
- **Ticket-first standing rule** (`engine/store/queue/.CONVENTION.md`): every unit of work gets
  a ticket JSON; BA-produced day tickets and the auditor tickets both follow the queue idiom.
- **No `-p`/headless/SDK ever; interactive `claude` only** — the BA conversation is an
  interactive session; PROTOCOL.md must never instruct a headless invocation.
- **Q7: voice is in the portfolio but as track T9** — the protocol is text/terminal only; do
  not build or wire any audio/Samantha surface here.
- **No YLO/POEM work** — out of scope entirely.
- **Life-lane privacy boundary** (daily-operating-model §5): day logs and the friction register
  live in this work repo and must never absorb life/PII data — work-lane observations only.
- **Absorption principle as acceptance criteria** (daily-operating-model §7): the retro scores
  the week on uptake ("if David reads only NEEDS YOU, he's caught everything") not on output.

## Recon (verify before any work)

Docs lag code — run every check; these replace doc-trust. Record the outputs of 1, 3, 4, 5, 6
verbatim: Move 2 writes them into `STATE.json` as the capability snapshot.

1. `python3 /Users/davidcruwys/dev/ad/apps/project-digest/digest.py dark-factory --format json --no-write`
   → valid JSON with keys `briefing_n`, `needs_you`, `since_last_looked`, `generated_at`
   (all present at authoring; briefing_n printed 3 = would-be-next, store held #2 @
   2026-07-03T03:17Z). Crash or missing keys → the briefing source is broken → **Abort A2**.
   ⚠️ Use `--no-write` for EVERY digest run this ticket makes — a real run bumps `briefing_n`
   and resets the since-window, eating Day 1's delta.
2. **BA agent exists (the hard gate — this proof is meaningless without it).** Check in order:
   (a) `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done/ | grep -i "wg-t2-01"`
   (b) `ls /Users/davidcruwys/dev/ad/apps/dark-factory/.claude/skills/` for a new BA/producer
   entry (at authoring: comprehend-visualise, conductor, image-gen, marshall, millwright,
   store, swagger — no BA agent), (c) `grep -rli "ba agent\|producer" ~/dev/ad/apps/dark-factory/backlog/wargames/T2-01*.md`
   for where T2-01 said it would put the artifact, then verify that path exists.
   Found → note its exact invocation surface (skill name / command / doc) for Move 1 and F1.
   Not found anywhere → **Abort A1**.
3. Which projects are configured: `ls /Users/davidcruwys/dev/ad/apps/project-digest/projects/`
   (authoring: `dark-factory.json` only) and does `--list` exist:
   `python3 /Users/davidcruwys/dev/ad/apps/project-digest/digest.py --list` (authoring: no such
   flag — T2-03's deferred queue ticket `20260704T0630Z-project-digest-list-and-project-2.json`
   adds it). ≥2 projects → **Fork F2 Route A**; 1 project → **Fork F2 Route B**. Either way
   proceed — absence is friction data, not a blocker.
4. Engine store intact: `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/queue /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/needs-decision /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done`
   → all three exist (17 done tickets at authoring) and `python3 engine/status.py` (from repo
   root) exits 0. Missing dirs or status crash → **Abort A3**.
5. Dispatch path available: `ls engine/store/WAKE-ARMED 2>/dev/null` (authoring: absent —
   auto-wake ships disarmed) and `launchctl list | grep dark-factory-wake` (authoring: loaded,
   notify-only). Record which → **Fork F3** decides the PROTOCOL's dispatch wording. Do NOT arm
   or disarm anything.
6. Optional-capability probes (record found/absent; absences become pre-seeded friction rows in
   Move 3, never blockers): activity registry (T2-02 — check
   `ls ~/dev/ad/apps/ | grep -i activity` and `grep -rli "activity registry" ~/dev/ad/apps/dark-factory/backlog/wargames/T2-02*.md`
   for its declared artifact path), engine-tickets-in-briefing feed (T2-05/T1-04 —
   `grep -n "engine" /Users/davidcruwys/dev/ad/apps/project-digest/lib/needs_you.py /Users/davidcruwys/dev/ad/apps/project-digest/lib/shipped.py`;
   authoring: no hits).
7. `ls /Users/davidcruwys/dev/ad/apps/dark-factory/backlog/wargames/runs/T2-06 2>/dev/null`
   → expect **absent** (authoring: no `runs/` dir at all). If it exists AND contains any
   `day-logs/day-[1-5]*.md` → a proof run is already in flight → **Abort A4**. If it exists but
   holds only harness files (no day logs) → a prior dispatch built the harness and died before
   arming; verify each existing file against Moves 1–4's specs and continue from the first gap.
8. `git -C /Users/davidcruwys/dev/ad/apps/dark-factory status --porcelain` → clean or unrelated
   paths only. Dirt inside `backlog/wargames/runs/` → treat as Recon 7's re-entry case.

## Moves

1. **Do:** Create `backlog/wargames/runs/T2-06/` and write `PROTOCOL.md` — ONE page — the
   morning ritual David + the BA agent follow each day. It must contain exactly these sections:
   **(i) The loop** — per morning, target ≤60 min total: 1. BRIEFING — for each configured
   project run `python3 ~/dev/ad/apps/project-digest/digest.py <id>` (real run, NO `--no-write`:
   the bump IS the briefing); read NEEDS YOU first. 2. BA CONVERSATION — interactive `claude`
   session, invoke the BA agent by the exact surface found in Recon 2 (F1 if ambiguous), one
   project at a time, digest as opening state. 3. OUTPUT — the day's tickets/specs land in
   `engine/store/queue/` per `.CONVENTION.md` (specs may live in `backlog/specs/`, but each
   gets a queue ticket). 4. DISPATCH — per the F3 route recorded in STATE.json. 5. LOG — copy
   `templates/day-log-template.md` → `day-logs/day-N.md`, fill every field; append friction
   rows to `friction-register.md` (write "none observed" explicitly if so). 6. AUDIT — copy
   `tickets/day-N.json` → `engine/store/queue/` so the auditor rides the day's dispatch.
   **(ii) The bar** — the week PASSES if ≥4 of 5 days complete steps 1–6 with ≥1 ticket
   emitted; PARTIAL if 2–3 days; FAIL otherwise. One missed day is tolerated by design.
   **(iii) Stall rule** — two consecutive missed days → the next auditor parks a
   needs-decision (extend / restart / call it with partial data), never silently continues.
   **(iv) Privacy** — work-lane observations only; no life/PII in any log (operating model §5).
   **Expect:** `PROTOCOL.md` exists, ≤ ~80 lines, every command in it copy-paste runnable.
   **Failure signal:** you can't write step 2 concretely because the BA invocation surface is
   unclear.
   **Counter-move:** → Fork F1. If F1 Route B also fails → Abort A1.

2. **Do:** Write `STATE.json` in the run dir:
   `{"armed_at": "<UTC now>", "dispatch_route": "<F3 route>", "capability_snapshot": {<Recon 1,3,5,6 findings: projects_configured, list_flag, ba_agent_surface, wake_armed, activity_registry, engine_feed>}, "briefing_n_at_arm": {"<project-id>": <n from store/last-briefing/<id>.json, 0 if absent>}, "days": {"1": "pending", "2": "pending", "3": "pending", "4": "pending", "5": "pending"}}`.
   **Expect:** `python3 -c "import json; json.load(open('backlog/wargames/runs/T2-06/STATE.json'))"` exits 0.
   **Failure signal:** invalid JSON or a snapshot field you can't fill.
   **Counter-move:** unfillable fields get the literal string `"unknown-at-arm"` — never guess
   a value; the auditors treat unknown as "verify from scratch".

3. **Do:** Write `templates/day-log-template.md` (fields, all mandatory: date/ts ·
   projects_briefed with per-project briefing_n · needs_you_count per project · ba_minutes per
   project · tickets_emitted as ids/paths · dispatch_path used · friction entries with
   phase[briefing|ba|ticketing|dispatch] / what happened / minutes lost / candidate fix ·
   david_verdict_line — one line from David: "did the brief cover what I needed?") and
   `friction-register.md` (append-only table: date · phase · observation · cost-min ·
   severity[low|med|high] · candidate fix), pre-seeded with one row per capability gap found in
   Recon 3/6 (e.g. "only 1 project configured — operating model wants 3–4/day",
   "no --list flag", "no engine feed in NEEDS YOU"), each dated today, phase=briefing,
   source-noted as `pre-registered at arm`.
   **Expect:** both files exist; register has ≥1 pre-seeded row (at authoring 3 gaps were open;
   sibling tickets may have closed some — seed only what Recon actually found absent).
   **Failure signal:** register empty AND Recon 3/6 found gaps (you dropped data).
   **Counter-move:** re-derive rows from STATE.json's capability_snapshot — the two must agree.

4. **Do:** Stage five auditor tickets `tickets/day-1.json` … `tickets/day-5.json`
   (NOT in the engine queue — David copies one in per morning, step 6 of the loop). Each is
   Family-A: `{"ticket": "wg-t2-06-day-N-audit", "kind": "instruction", "title": "T2 Producer/BA: Step-0 proof — day N audit", "source": "backlog/wargames/T2-06-five-day-briefing-proof.md", "executor": "swagger", "priority": "normal", "requested_at": "<arm-time UTC>", "requested_by": "wg-t2-06 harness (proof run)", "depends_on": [], "prompt": "<per template below>", "verify": "<per template below>"}`.
   Day 1–4 prompt template: *"Audit day N of the Step-0 proof (run dir
   backlog/wargames/runs/T2-06/, protocol PROTOCOL.md). Verify: day-logs/day-N.md exists with
   every template field filled; store/last-briefing/<id>.json ts advanced past the previous
   day's for each project in STATE.json briefing_n_at_arm; every ticket id named in
   tickets_emitted exists in engine/store/{queue,running,done}/. Append any mechanical friction
   you find (missing fields, ts gaps, dead ticket refs) to friction-register.md. Set
   STATE.json days.N = done, or missed (reconstruct what you can from durable artifacts and log
   the omission as friction). Stall rule: if days N-1 and N are both missed, write
   engine/store/needs-decision/wg-t2-06-day-N-audit.json asking extend/restart/call-partial and
   stop."* — verify: *"STATE.json days.N is done or missed; friction-register.md row count ≥
   its pre-audit count; no day-log file was created or backdated by the auditor itself."*
   Day-5 prompt additionally: *"Then write RETRO.md: friction register distilled into themes
   with total minutes lost; top-5 fixes drafted as Family-A ticket JSONs in
   runs/T2-06/follow-on/ (staged, not queued); absorption score — for each day, did
   david_verdict_line confirm NEEDS YOU sufficed?; final verdict PASS/PARTIAL/FAIL against
   PROTOCOL.md §The bar, with the evidence lines quoted. Notify David (osascript, wake.py
   idiom) with the verdict one-liner. Mark the kickoff note in backlog/ done per its own
   footer instruction."*
   **Expect:** `for f in backlog/wargames/runs/T2-06/tickets/day-*.json; do python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$f" || echo BAD $f; done`
   prints nothing bad; exactly 5 files.
   **Failure signal:** any BAD line, or a ticket whose prompt references a path this harness
   didn't create.
   **Counter-move:** fix the JSON; re-run the loop check. Paths must all be repo-relative and
   exist by end of Move 5 — cross-check each against `ls`.

5. **Do:** Day-0 mechanical rehearsal — prove every non-David leg once, touching nothing
   durable: (i) for each configured project run the digest **with `--no-write`** and confirm
   the box/JSON renders; (ii) confirm the BA invocation surface from Recon 2 resolves (the
   skill file/command exists and its own doc describes an interview entry point — do NOT run a
   real BA conversation; there is no David in this session); (iii) dry-parse one auditor ticket
   through the engine's own filter: from repo root,
   `python3 -c "import json; t=json.load(open('backlog/wargames/runs/T2-06/tickets/day-1.json')); assert t.get('kind')!='external-research' and 'deferred' not in (str(t.get('status','')),str(t.get('priority',''))); print('dispatchable-shape OK')"`
   (mirrors `orchestrator.py dispatchable()`, ~line 183); (iv) write
   `day-logs/day-0-rehearsal.md` using the template, marking david-dependent fields
   `n/a — rehearsal`, and record rehearsal friction (anything that surprised you) in the
   register.
   **Expect:** all four sub-checks pass; `store/last-briefing/*.json` mtimes/contents are
   byte-identical to before the move (the `--no-write` discipline held); no file appeared in
   `engine/store/queue/`.
   **Failure signal:** briefing_n advanced, a queue file appeared, or the digest crashed on a
   project that Recon 1/3 said was configured.
   **Counter-move:** briefing_n advanced → you ran a real digest; restore is impossible (the
   window moved) — log it as day-0 friction with the honest note "rehearsal consumed the
   delta; Day 1 SINCE field will under-report", do not attempt to hand-edit
   `store/last-briefing/` (it's another app's store). Queue file → remove it immediately and
   log the near-miss. Digest crash on project #2 only → drop to F2 Route B and log friction.

6. **Do:** Arm and surface: (i) write the drill card `runs/T2-06/DRILL.md` — ten lines max:
   what starts tomorrow, the one command to open the protocol, the six loop steps as a
   checklist, the bar, where friction goes; (ii) write the kickoff note
   `backlog/<today's date>-step0-proof-armed.md` containing the literal marker `waiting:david`
   plus: "Step-0 five-day proof is armed — start Day 1 next working morning:
   `open backlog/wargames/runs/T2-06/PROTOCOL.md`" and a footer "when RETRO.md lands, rename
   this file to `.done.md`" (the `waiting:david` marker makes David's own next briefing surface
   it in NEEDS YOU — verified against project-digest's marker scan); (iii) fire one macOS
   notification (wake.py's osascript idiom, title `dark-factory`, message
   `Step-0 five-day proof armed — Day 1 starts next morning`).
   **Expect:** both files exist;
   `python3 ~/dev/ad/apps/project-digest/digest.py dark-factory --no-write | grep -i "step0-proof\|step-0"`
   (or the JSON `needs_you` array) shows the kickoff note surfaced.
   **Failure signal:** the note doesn't appear in NEEDS YOU.
   **Counter-move:** check the marker scan's actual vocabulary
   (`grep -n "waiting" /Users/davidcruwys/dev/ad/apps/project-digest/lib/needs_you.py`) and
   adjust the note's wording to a marker it does catch; NEEDS YOU is capped at 3 — if the note
   is merely outranked by 3 other open decisions, that's acceptable: confirm it's in the JSON's
   fuller scan or note the cap and rely on the osascript notification.

7. **Do:** Commit and push (dark-factory only — nothing outside this repo was written):
   `backlog/wargames/runs/T2-06/` (all files), `backlog/<date>-step0-proof-armed.md`. Message:
   `feat(wargames): T2-06 five-day Step-0 proof armed — harness + day tickets + rehearsal`.
   Stage only your files; `git status --porcelain` first.
   **Expect:** push succeeds; nothing of yours left dirty.
   **Failure signal:** push rejected.
   **Counter-move:** `git pull --rebase` then push; conflict in a file you never touched →
   park per the A-conditions' idiom (write needs-decision with the conflicting paths) rather
   than resolving strangers' conflicts.

## Forks

**F1 — BA agent exists but its invocation surface is ambiguous.**
Trigger: Recon 2 finds a BA artifact but no single obvious "run the morning interview" entry
point (T2-01's internals were an open design — the contract was pinned, the mechanism wasn't).
→ **Route A:** read T2-01's war game + done-ticket result for the declared surface; if its own
docs name a skill/command, use that verbatim in PROTOCOL.md step 2 and record it in STATE.json.
→ **Route B:** artifact exists but genuinely documents no entry point → treat as **Abort A1**
with the twist noted ("BA agent landed but is not invocable as a morning interview — surface
missing").

**F2 — how many projects the protocol covers.**
Trigger: Recon 3's count of `projects/*.json`.
→ **Route A (≥2 configured):** PROTOCOL step 1 loops all configured ids (cap at 3/morning per
the operating model's "David can only really do ~2/day well"); day-log carries one
briefing_n per project.
→ **Route B (1 configured):** single-project protocol on `dark-factory`; pre-seed the register
with the coverage gap (the operating model wants 3–4). The proof still stands — it tests the
loop, and the gap is exactly the friction data this ticket exists to capture.

**F3 — dispatch path for the day's tickets + auditor.**
Trigger: Recon 5's WAKE-ARMED state.
→ **Route A (WAKE-ARMED present):** PROTOCOL step 4 = "drop tickets in queue/; auto-wake
dispatches; watch `engine/store/wake.log`".
→ **Route B (absent — authoring-time state):** PROTOCOL step 4 = "drop tickets in queue/, then
run `python3 engine/orchestrator.py` from repo root in a spare terminal and let it drain
(MAX_WALL 900s default); wake.py will have notified regardless". Record the route in
STATE.json; the morning session may also execute an auditor itself as `builder-agent` per
`.CONVENTION.md` if the orchestrator is unavailable — note that fallback in PROTOCOL verbatim.

## Assumptions ledger

1. **T2-01's BA agent lands before this ticket dispatches.** Plausible: T2-01 is bucket-now/L,
   this is bucket-next/M, and Phase 5's promotion script drains progressively — but
   `dispatchable()` does NOT enforce `depends_on` (verified at authoring, orchestrator.py ~183),
   so nothing mechanical stops an early dispatch. False → **Abort A1** (the recon gate, not the
   ticket field, is the real guard).
2. **David will actually run five mornings.** The harness can't make him; the stall rule +
   day-auditor parking convert absence into a decision instead of a silent rot. If David
   rejects the whole cadence at kickoff → he says so at triage; the parked needs-decision from
   the stall rule is the formal capture.
3. **The ≥4-of-5 PASS bar and ≤60-min morning target are acceptable.** Chosen from the
   operating model's own numbers (~4h morning across 3–4 projects ⇒ ≤60 min for
   briefing+BA-per-project is conservative). If David wants a different bar, DRILL.md tells him
   to edit PROTOCOL.md §The bar before Day 1 — a bar edit before Day 1 is legitimate, not a
   proof failure.
4. **`backlog/wargames/runs/` is an acceptable new home** (CLAUDE.md's where-to-write table
   predates the war-game portfolio). Plausible: it's the portfolio's own namespace, mirrored on
   `experiments/ylo/*/runs/`. If David objects, moving the dir post-hoc is one `git mv` —
   proceed, don't park.
5. **Nobody else runs a real (write-mode) digest mid-week.** A stray real run bumps briefing_n
   and shrinks the next morning's SINCE window. Not preventable from here (it's another app's
   store); PROTOCOL's day-log briefing_n field makes it detectable (a jump >1 between
   consecutive day logs), and the auditor logs it as friction. Accept and observe.

## Abort conditions

- **A1 — no BA agent** (Recon 2 exhausted / F1 Route B). The loop's middle leg doesn't exist;
  a "proof" of briefing→tickets without the BA conversation would test the wrong model. Park:
  write `engine/store/needs-decision/wg-t2-06-five-day-briefing-proof.json` with
  `{"ticket": "wg-t2-06-five-day-briefing-proof", "question": "Step-0 five-day proof is blocked: no invocable BA agent found (T2-01 not landed, or landed without an interview entry point). Options: (a) wait for T2-01 and re-queue this ticket unchanged, (b) run a degraded briefing-only proof now (tests digest cadence, not the operating model), (c) drop. Which?", "observed": "<exactly what Recon 2 found at each of its three checks>"}`.
  Leave the ticket in `running/`. Never substitute goal-plan or a generic interview for the BA
  agent — David explicitly ruled they are not the same (daily-operating-model §3).
- **A2 — briefing source broken.** Recon 1's untouched digest run crashes or lacks the contract
  keys. Park with the traceback and question: "project-digest is broken before any T2-06 work;
  the Step-0 gate (§2) is closed. Fix digest first (separate ticket) or hold the proof?"
- **A3 — engine store layout moved.** Recon 4 fails. Park with what was found; the day-ticket
  mechanics all assume `queue/`/`needs-decision/`/`done/` — never guess a new layout.
- **A4 — a proof run is already in flight.** Recon 7 finds `day-logs/day-[1-5]*.md`. Park with
  question: "runs/T2-06/ already holds day logs — is a proof week live (do not re-arm over it)?
  Options: let it finish / restart clean / audit-and-close." Never clobber or re-stage over a
  live run's state.

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory` unless pathed:

```bash
# 1. Harness complete
ls backlog/wargames/runs/T2-06/PROTOCOL.md backlog/wargames/runs/T2-06/STATE.json \
   backlog/wargames/runs/T2-06/DRILL.md \
   backlog/wargames/runs/T2-06/friction-register.md \
   backlog/wargames/runs/T2-06/templates/day-log-template.md \
   backlog/wargames/runs/T2-06/day-logs/day-0-rehearsal.md            # all exist
python3 - <<'EOF'
import json, glob
s = json.load(open("backlog/wargames/runs/T2-06/STATE.json"))
assert set(s["days"]) == {"1","2","3","4","5"} and set(s["days"].values()) == {"pending"}
assert "capability_snapshot" in s and "dispatch_route" in s
ts = sorted(glob.glob("backlog/wargames/runs/T2-06/tickets/day-*.json"))
assert len(ts) == 5, ts
for f in ts:
    t = json.load(open(f))
    assert t["executor"] == "swagger" and t["kind"] == "instruction", f
print("harness OK — 5 day tickets staged, STATE armed")
EOF

# 2. Protocol is concrete (commands present, bar present, stall rule present)
grep -c "digest.py" backlog/wargames/runs/T2-06/PROTOCOL.md            # ≥ 1
grep -ci "stall\|missed" backlog/wargames/runs/T2-06/PROTOCOL.md       # ≥ 1
grep -ci "PASS" backlog/wargames/runs/T2-06/PROTOCOL.md                # ≥ 1

# 3. Kickoff note surfaces to David
ls backlog/*step0-proof-armed.md
grep -c "waiting:david" backlog/*step0-proof-armed.md                  # ≥ 1

# 4. Friction register pre-seeded iff gaps were found (compare with STATE snapshot)
grep -c "pre-registered at arm" backlog/wargames/runs/T2-06/friction-register.md  # ≥ 1 at authoring-time gap levels

# 5. Negative checks — what must NOT have changed
ls engine/store/queue/ | grep -c "wg-t2-06"                            # → 0 (no day ticket queued by the harness)
cat /Users/davidcruwys/dev/ad/apps/project-digest/store/last-briefing/dark-factory.json
#   → briefing_n unchanged from Recon 1's read (rehearsal used --no-write throughout)
ls backlog/wargames/runs/T2-06/day-logs/ | grep -c "day-[1-5]"         # → 0 (the week hasn't run; only day-0)
ls backlog/wargames/runs/T2-06/RETRO.md 2>&1 | grep -c "No such"       # → 1 (retro belongs to day-5's auditor)

# 6. Committed and pushed
git log --oneline -1        # shows the T2-06 arm commit
git status --porcelain | grep -c "wargames/runs/T2-06"                 # → 0
```

The week-phase bar (owned by the day tickets, not re-verified here): five day-logs, a
friction register with real entries, `RETRO.md` with a quoted-evidence PASS/PARTIAL/FAIL
verdict, follow-on ticket drafts under `runs/T2-06/follow-on/`, kickoff note renamed `.done.md`.

## Executor notes (sonnet)

- **Scope fence.** Do NOT edit project-digest code, config, or store (this ticket only READS
  it — `--no-write` always); do NOT edit the BA agent or any `.claude/skills/` entry; do NOT
  touch `engine/*.py`, WAKE-ARMED, HALT, or BACKOFF; do NOT put anything into
  `engine/store/queue/` — the day tickets are staged OUTSIDE the queue and enter it one per
  morning, by David, per the protocol.
- **You are arming a proof, not running one.** No BA conversation happens in this dispatch —
  there is no David in your session. Rehearsal (Move 5) proves the mechanical legs only.
- **The rabbit hole: building briefing improvements.** Recon 3/6 will show you real gaps
  (no --list, one project, no engine feed). Fixing any of them is T2-03/T2-02/T2-05's work.
  Your ONLY move on a gap is a pre-seeded friction row. A single line each — the register is
  the deliverable, not the fix.
- **Style:** PROTOCOL.md and DRILL.md are for a tired human at 7am — short lines, numbered
  steps, every command paste-ready with absolute paths where they leave the repo. Day-ticket
  prompts are for a sonnet Swagger with zero context — self-contained, repo-relative paths,
  no reference to this conversation.
- **Prefer parking over guessing** on: any A-condition, any sign the BA agent's contract
  differs from daily-operating-model §3 (in=state, process=one-project conversation,
  out=tickets), and any evidence a proof week already ran (A4). A parked question costs a day;
  a clobbered live run costs the whole acceptance test.
