# T2-01 — Build the BA agent (Producer / C2)

| field | value |
|---|---|
| ticket | wg-t2-01-ba-agent |
| track / size / priority | T2 Producer/BA / L / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Build the Producer (C2) — the morning BA agent whose **contract is pinned** in
`docs/daily-operating-model.md` §3 (in = per-project state from the §2 digest · process = deep
one-project-at-a-time conversation · out = tickets/specs into the engine queue) and whose
**internals are the open design this ticket closes**. Size L = design-first: done means
**(a)** `docs/ba-agent-spec.md` exists — the internals design (session shape, interview protocol,
state ingestion, ticket-emission contract, edges, v1 limits); **(b)** a working v1 skill at
`.claude/skills/producer/` (SKILL.md + `emit-ticket.py` helper) that David can invoke in a
morning session against dark-factory (the one digest-configured project); **(c)** the emission
mechanics are proven by a dry-run self-test (simulated interview → schema-valid tickets in a
scratch dir — NEVER the live queue); **(d)** docs are wired (daily-operating-model §7 row,
north-star C2 annotation, INDEX.md line) and a pilot note tells David exactly how to run the
first live morning. The live morning itself is HITL — it is the pilot note's job, not this
ticket's verify. C2 is NOT claimed closed by this ticket.

## Locked context

- **§3 daily-operating-model (David, session 7683bd09):** the BA agent is a **distinct agent,
  NOT a `goal-plan` variant** — goal-plan is a downstream compressor only, invoked after a BA
  conversation produces something worth setting as a goal. Binding design constraint.
- **Q4 (decisions.md):** everything through the engine — the BA's output is ticket JSONs in
  `engine/store/queue/` per `engine/store/queue/.CONVENTION.md` (ticket-first standing rule,
  David-ratified 2026-07-04).
- **No `-p`/headless/SDK ever; interactive `claude` only.** The BA runs inside a David-attended
  interactive session. Nothing in this ticket spawns `claude`, an orchestrator, or a worker.
- **Q7 (decisions.md):** voice/Samantha is IN the portfolio but lives in track T9 — producer v1
  is text-only; the spec names the voice seam, builds none of it.
- **§5 privacy boundary (daily-operating-model):** work lane only. Life/PII content never enters
  a ticket, the spec, or this repo.
- **No YLO/POEM work** — out of scope entirely.

## Recon (verify before any work)

Docs lag code. Run every check from `/Users/davidcruwys/dev/ad/apps/dark-factory`.

1. `sed -n '84,95p' docs/daily-operating-model.md` → expect the §3 heading
   `## 3. The BA agent = the Producer (C2)` and the pinned contract line
   (`in = current project state (§2) · process = deep one-project-at-a-time conversation · out = tickets / specs / requirements`).
   If §3 is gone or the contract materially differs from this war game → **Abort A3**.
2. `ls .claude/skills/` → expect `comprehend-visualise conductor image-gen marshall millwright
   store swagger` (as of 2026-07-06) and NO `producer`/`ba*` entry;
   `ls docs/ba-agent-spec.md 2>&1` → expect "No such file". Either exists → **Fork F1**.
3. `grep -rli "producer\|ba agent" /Users/davidcruwys/dev/ad/appydave-plugins/*/skills/*/SKILL.md 2>/dev/null`
   → expect no skill whose PURPOSE is a morning BA interview (authoring-time recon found none;
   `appydave:goal-plan` and `agent-skills:interview-me` exist but are different tools — §3
   explicitly separates goal-plan). A same-name skill with a different purpose → **Fork F1
   Route A**; a real BA/morning-interview implementation → **Fork F1 Route B**.
4. `python3 /Users/davidcruwys/dev/ad/apps/project-digest/digest.py dark-factory --format json --no-write | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted(d.keys()))"`
   → expect the 15 keys verified 2026-07-06: `autonomy_stage, briefing_n, first_run,
   generated_at, goal, health, in_flight, last_commit_days, live_now, needs_you, project_id,
   project_name, shipped_recently, since_last_looked, since_ts`. Degraded-but-parses →
   **Fork F2 Route A**; crash/no JSON → **Fork F2 Route B**.
5. `cat engine/store/queue/.CONVENTION.md` and read TWO real tickets for the field idiom:
   `cat engine/store/done/20260706T0932Z-auto-wake-and-notify-watcher.json` (or any recent
   done ticket) and `cat engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json`
   (the deferred digest ticket — note its `priority: deferred` + `status` idiom). Confirm the
   id format `<YYYYMMDD>T<HHMM>Z-<slug>` with filename == `<ticket>.json`. If the store layout
   or id idiom has shifted → **Abort A3** (the emission contract would be guesswork).
6. `launchctl list | grep com.appydave.dark-factory-wake` → note whether the wake watcher is
   loaded (it watches `engine/store/queue/` and notifies David on new tickets). Loaded or not,
   the rule stands: **the self-test never writes into `engine/store/queue/`** — a test ticket
   there would notify David and could be dispatched by a live pool.
7. `ls engine/store/queue/ > /tmp/t2-01-queue-before.txt; cat /tmp/t2-01-queue-before.txt` →
   snapshot the queue for the Move-6 guard check. (Do not assume it holds only the deferred
   ticket — Phase-5 promotion drains war-game tickets into it progressively.)
8. `sed -n '75,85p' docs/north-star.md` → expect the build spine with
   `2. **C2 — Producer: talk → a schema-valid ticket in \`queue/\`.** ← next.` and the C1 line's
   `✅ DONE 2026-06-05` annotation style (the style Move 7 mirrors). Missing → **Abort A3**.
9. `head -30 docs/morning-briefing-vision.md` → expect David's 2026-07-04 parking of
   "project #2" as premature + the dependency chain (activity registry → digest-over-activity
   → feed layer). This is why v1 is single-project BY DESIGN — cite it in the spec.
10. `git -C /Users/davidcruwys/dev/ad/apps/dark-factory status --porcelain` → expect clean or
    dirt only in files this ticket never touches (proceed, stage only your own files at Move 9).
    Dirt in `.claude/skills/`, `docs/daily-operating-model.md`, `docs/north-star.md`, or
    `docs/INDEX.md` → someone is mid-change on your seam → **Abort A1**.

## Moves

1. **Do:** Deep-read the design inputs, in this order, taking notes in the scratchpad (not the
   repo): `docs/daily-operating-model.md` (all of it), `docs/north-star.md` lines 50–90 (C2 +
   the Producer/Consumer/Trigger framing), `docs/morning-briefing-vision.md`,
   `engine/store/queue/.CONVENTION.md`, `.claude/skills/marshall/SKILL.md` and
   `.claude/skills/swagger/SKILL.md` (the house skill idiom: trigger-only description, hard
   rules, David's corrections quoted with dates), and the digest JSON from Recon 4.
   **Expect:** you can answer, without re-reading: what the §2 briefing box contains, the three
   §1 interview questions, why goal-plan is downstream-only, the ticket field idiom, and which
   digest JSON fields feed which briefing lines.
   **Failure signal:** any of those five is still fuzzy.
   **Counter-move:** re-read the specific source; if two sources contradict on the CONTRACT
   (not on status lines — those lag) → **Abort A3**.

2. **Do:** Write `docs/ba-agent-spec.md` — the internals design. Required sections, in order:
   - `## Contract (pinned)` — restate §3 verbatim-in-substance: in = §2 digest state · process
     = deep one-project conversation · out = tickets/specs. Cite daily-operating-model §3 and
     David's session-7683bd09 correction (quote it — it is in §3).
   - `## Boundaries (what the Producer is NOT)` — not goal-plan (downstream compressor only);
     not Marshall (the Producer QUEUES, never dispatches — Marshall/engine own dispatch); not a
     builder (never edits code mid-interview); work-lane only (§5 privacy: no life/PII in
     tickets); one project at a time.
   - `## Session shape` — David opens an interactive `claude` session at the dark-factory repo
     root and invokes the producer skill naming a project (v1: `dark-factory` only, the one
     `projects/<id>.json` config in project-digest). No cron, no headless, no auto-fire.
   - `## Phase 1 — Brief` — run
     `python3 /Users/davidcruwys/dev/ad/apps/project-digest/digest.py <project> --format box`
     (real mornings WRITE the last-briefing counter — that is digest's one designed write;
     tests always add `--no-write`), show David the box, then open with the §2 closing line:
     *"What do you want to get out of <project> today? My take: <recommended focus>"* — the
     take derived from `needs_you` items first, then `in_flight`, then `since_last_looked`.
   - `## Phase 2 — Interview` — the deep loop, anchored on §1's three questions ("Where are we
     up to? What do you want to get out of it today? What's the next level of improvement?").
     Rules: lead with a take, never bounce a bare question back; ≤3 open questions per turn;
     outcome first, then constraints, then decomposition into 1–5 ticket-sized units; stop when
     David says done, redirects, or the day's units are shaped. Digest fields that render
     "dark"/error degrade gracefully — say so and interview anyway.
   - `## Phase 3 — Emission` — per ticket: read back title + one-line prompt summary + priority
     → David approves → emit via `emit-ticket.py` (below) into `engine/store/queue/` → confirm
     the printed path. Zero tickets is a VALID outcome (a pure status/steering morning); close
     with a one-line session summary either way. End of project = list every emitted filename.
   - `## Ticket contract` — a field table matching `.CONVENTION.md` + the real store idiom
     verified in Recon 5: `ticket` (== filename stem, `<YYYYMMDD>T<HHMM>Z-<slug>`) · `kind`
     ("instruction" default in v1; "external-research" only per the .CONVENTION.md idiom and
     then NEVER left in queue/ while a pool runs) · `title` · `source` ("BA session <date>
     (producer skill)") · `executor` ("swagger" default; "unassigned" + `priority: deferred`
     when David parks it — the existing deferred-ticket idiom) · `priority`
     (high|normal|deferred, David's call per ticket) · `requested_at` (real UTC) ·
     `requested_by` ("david (BA session <date>)") · `prompt` (self-contained, repo-relative
     paths) · `verify` (prose acceptance bar; David supplies or approves it).
   - `## goal-plan seam` — when David says "make this a goal", the BA hands the finished
     spec/ticket to `appydave:goal-plan` for the /goal compression. Downstream only, never the
     interviewer.
   - `## Edges` — digest crash (fall back to `git log` + `backlog/` skim, flag the gate as
     broken, still interview); David cuts the session short (emit what was approved, summarise
     the rest as a backlog note, never auto-emit unapproved tickets); scope explosion
     mid-interview (park the tangent as one `backlog/<date>-<slug>.md` note, return to the
     project).
   - `## v1 limits & upgrade path` — single project (dark-factory) by design (cite
     morning-briefing-vision.md's deliberate parking); multi-project waits on the activity
     registry + digest-over-activity (portfolio T2-02/T2-04); feed layer T2-05; voice front
     door Q7/T9; the 5-day proof T2-06.
   - `## First live morning — pilot protocol` — the exact steps David runs, what to capture
     (friction points, questions the BA should have asked, ticket quality), where to note it
     (`backlog/<date>-ba-agent-pilot.md`, created by Move 8).
   - `## Open questions for David` — (1) persona name (working name "producer" is the C2 role
     name, not a christening — David names his agents: Marshall, Swagger, Samantha); (2) should
     each BA session write a durable per-day record (e.g. `backlog/ba-sessions/`) beyond the
     emitted tickets?
   **Expect:** the file exists; every section above present; no section contradicts Locked
   context; total length in the 150–300 line range (a spec, not a book).
   **Failure signal:** a section missing, or the spec invents machinery this war game didn't
   ground (e.g. a daemon, a cron, a new store directory).
   **Counter-move:** cut the invention; the v1 surface is exactly: skill + helper + queue
   writes + digest reads. If you believe a new mechanism is genuinely required → **Abort A5**
   with the question, never build it silently.

3. **Do:** Write `.claude/skills/producer/SKILL.md`. Frontmatter: `name: producer` and a
   trigger-only description in David's voice (see `docs/david-style-patterns.md` if unsure;
   the marshall/swagger descriptions are the live house pattern), e.g.:
   `"Producer (C2) — the morning BA conversation. Use when David says 'producer', 'BA session', 'morning briefing', 'plan my day on <project>', 'be the BA', or opens the morning interview on a project. In = the project digest; process = deep one-project interview; out = tickets in engine/store/queue/. Never dispatches; goal-plan is downstream, not this."`
   Body (terse, marshall-style): Preflight (run the digest, box format; degrade gracefully) →
   Phase 1 Brief → Phase 2 Interview → Phase 3 Emission via
   `python3 .claude/skills/producer/emit-ticket.py ...` → Hard rules block: never dispatch or
   start the orchestrator/pool · never edit code mid-interview · never emit an unapproved
   ticket · one project per conversation · work-lane only, no life/PII · goal-plan only on
   David's explicit "make this a goal". Each phase references the spec section rather than
   duplicating it (`docs/ba-agent-spec.md` is canonical; the skill is the operating card).
   **Expect:** SKILL.md exists; description is trigger-only (starts naming the agent, contains
   "Use when"); body under ~120 lines; hard-rules block present.
   **Failure signal:** description narrates workflow instead of triggers, or the body
   duplicates whole spec sections.
   **Counter-move:** rewrite the description to triggers-only; replace duplicated prose with a
   pointer to the spec section.

4. **Do:** Write `.claude/skills/producer/emit-ticket.py` — stdlib-only, ~80–120 lines.
   Behaviour: argparse with required `--title`, `--prompt`, `--verify`, `--slug`; optional
   `--kind` (default `instruction`), `--executor` (default `swagger`), `--priority` (default
   `normal`, choices high|normal|deferred), `--source` (default `BA session <today> (producer
   skill)`), `--requested-by` (default `david (BA session <today>)`), `--out` (default:
   `<repo>/engine/store/queue` where repo root = `Path(__file__).resolve().parents[3]`).
   Computes `ticket = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M") + "Z-" + slug`
   (matching the store idiom from Recon 5); refuses to overwrite an existing file (exit 1);
   rejects empty/whitespace title, prompt, verify, or slug (exit 2, nothing written); slug must
   match `[a-z0-9][a-z0-9-]*` (exit 2 otherwise); writes the JSON with `requested_at` = real
   UTC ISO (`%Y-%m-%dT%H:%M:%SZ`), `depends_on: []`, and prints the absolute written path as
   its only stdout line; exit 0.
   **Expect:** `python3 .claude/skills/producer/emit-ticket.py --help` exits 0 and shows all
   flags.
   **Failure signal:** traceback on --help, or any non-stdlib import.
   **Counter-move:** fix; stdlib-only is the engine convention (orchestrator/wake are
   stdlib-only) — do not reach for a package.

5. **Do:** Dry-run self-test (positive path). You play David from this fixture — a simulated
   morning on dark-factory: David's goal is "harden the wargame portfolio", yielding exactly
   two approved tickets: (a) slug `dryrun-ba-selftest-one` (slugs are lowercase per the Move-4
   regex; "DRYRUN" goes in the title), title "DRYRUN: BA self-test one — ignore", priority
   normal; (b) slug `dryrun-ba-selftest-two`, title "DRYRUN: BA self-test two — ignore",
   priority high, executor swagger. Both with a one-sentence prompt and verify.
   Emit BOTH via emit-ticket.py with `--out <scratchpad-dir>/t2-01-dryrun` (create the dir
   first; the scratchpad path is in your environment prompt — NEVER `engine/store/queue/`).
   Then validate:
   `python3 - <<'EOF'` asserting for each file: json loads · `ticket` == filename stem ·
   ticket matches `^\d{8}T\d{4}Z-dryrun-ba-selftest-(one|two)$` · `kind == "instruction"` ·
   `executor == "swagger"` · `priority in {"high","normal","deferred"}` · `requested_at`
   matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$` · `prompt` and `verify` non-empty ·
   `depends_on == []`. `EOF`
   **Expect:** two files in the scratch dir; all asserts pass; emit-ticket printed each path.
   **Failure signal:** assert failure or a file landing anywhere but the scratch dir.
   **Counter-move:** fix emit-ticket.py and re-run this move from scratch (delete the scratch
   files first). If the two emissions collide on the same minute-resolution id → that is a real
   idiom limit: add a `-2` de-dup suffix to the second (`slug` untouched, ticket id suffixed)
   inside emit-ticket.py, matching "refuse to overwrite" upgraded to "auto-suffix"; re-run.

6. **Do:** Self-test (negative + guard). (a) Run emit-ticket.py omitting `--verify` → expect
   exit 2 and NO file written to the scratch dir. (b) Run with `--slug 'Bad Slug!'` → exit 2,
   no file. (c) Guard: `ls engine/store/queue/ > /tmp/t2-01-queue-after.txt && diff /tmp/t2-01-queue-before.txt /tmp/t2-01-queue-after.txt`
   → expect empty diff (tolerate lines OTHER sessions added — the guard is specifically
   `ls engine/store/queue/ | grep -ci dryrun` → `0`). (d) `rm -r` the scratch dry-run dir.
   **Expect:** exits 2 twice, zero dryrun files in the live queue, scratch cleaned.
   **Failure signal:** a dryrun ticket in `engine/store/queue/`.
   **Counter-move:** remove it IMMEDIATELY (`rm engine/store/queue/*dryrun*`), note the escape
   in the result, and fix the default-out logic before proceeding — the default must still be
   queue/ (real mornings) but the SKILL.md self-test instructions and this war game always pass
   `--out`; the escape means a test command dropped the flag.

7. **Do:** Doc wiring, tightly fenced — three one-liners:
   (i) `docs/daily-operating-model.md` §7 build-decisions table, the "BA agent shape" row:
   append to its State cell: ` — **spec + v1 skill landed <date>** (docs/ba-agent-spec.md,
   .claude/skills/producer/); live pilot pending`. Do not restructure the table.
   (ii) `docs/north-star.md` C2 spine line (~line 79): append a suffix annotation in the C1
   style: ` 🔨 **v1 landed <date>** — spec (docs/ba-agent-spec.md) + producer skill; C2 closes
   on the first live morning (pilot note in backlog/).` Do NOT mark it ✅ — talk→ticket has not
   run live.
   (iii) `docs/INDEX.md`, "The human side" section: one line for `ba-agent-spec.md` right after
   the `daily-operating-model.md` entry ("when a new design doc lands, it gets a line here or
   it doesn't exist" — the index's own rule).
   **Expect:** three files, diff of a few lines each.
   **Failure signal:** any of the three diffs restructures more than its one line/cell.
   **Counter-move:** `git checkout -- <file>` and redo as a pure suffix/insert.

8. **Do:** Write the pilot note `backlog/$(date +%Y-%m-%d)-ba-agent-pilot.md` — directive,
   self-contained, ~20 lines: what landed (spec + skill paths, absolute), how David runs the
   first live morning (open `claude` at the repo root → invoke producer on dark-factory →
   have the conversation → tickets land in `engine/store/queue/` → wake watcher notifies),
   what to capture (friction, missing questions, ticket quality), and the two open questions
   from the spec (persona name, per-day BA record). End with: C2 closes when one real morning
   has produced ≥1 schema-valid ticket David didn't hand-edit.
   **Expect:** the file exists and names only artifacts that exist.
   **Failure signal:** the note references anything unbuilt (e.g. multi-project, voice).
   **Counter-move:** trim to what Moves 2–7 actually shipped.

9. **Do:** Commit and push (dark-factory only — no other repo was touched). Stage exactly:
   `docs/ba-agent-spec.md`, `.claude/skills/producer/SKILL.md`,
   `.claude/skills/producer/emit-ticket.py`, `docs/daily-operating-model.md`,
   `docs/north-star.md`, `docs/INDEX.md`, `backlog/<date>-ba-agent-pilot.md`. Message:
   `feat(producer): BA agent v1 — internals spec + producer skill + ticket emitter (C2, T2-01)`.
   **Expect:** `git push` succeeds; `git status --porcelain` shows none of your files left.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — a producer/BA artifact already exists.**
Trigger: Recon 2/3 finds a `producer`/`ba*` skill dir, a `docs/ba-agent-spec.md`, or a plugin
skill whose purpose is the morning BA interview.
→ **Route A** (same NAME, different purpose — the unknowns-map name-collision class): keep
building, but name the skill `ba-producer` instead of `producer`, note the collision explicitly
in the spec's Open-questions section and in the pilot note (David decides the final name), and
adjust every path in Moves 3–9 accordingly.
→ **Route B** (a real BA/morning-interview implementation exists — race with another session):
**Abort A1**. Never build a second BA agent beside an existing one.

**F2 — digest baseline degraded vs broken.**
Trigger: Recon 4's digest run misbehaves.
→ **Route A** (JSON parses but fields carry `error` values / `live_now` dark / health flag
degraded): proceed — graceful degradation is IN the design (spec `## Edges`); record what was
degraded in the ticket result.
→ **Route B** (traceback / no JSON at all): the P1 gate is broken → **Abort A2**. The BA's
input contract cannot be designed against a crashed gate.

## Assumptions ledger

1. **Working name `producer` is acceptable for v1.** Plausible: it is north-star's own role
   name for C2 ("Producer — talk → ticket") and no skill of that name exists in dark-factory or
   appydave-plugins (verified 2026-07-06). David christens his agents (Marshall, Swagger,
   Samantha), so the spec lists naming as an open question. If David objects at triage → rename
   is a directory move + description edit, not a park.
2. **v1 single-project (dark-factory) is the right scope.** Plausible: David himself parked
   "project #2" as premature on 2026-07-04 (morning-briefing-vision.md) pending the activity
   registry. If false (David wants multi-project now) → that is T2-02/T2-03/T2-04 territory →
   park to `needs-decision/` rather than hand-rolling a second project config here.
3. **Default `executor: "swagger"` on emitted tickets.** Plausible per Q4
   (everything-through-the-engine) and the live idiom (recent real tickets carry it); the spec
   keeps the deferred/unassigned idiom for parked items. If a live pool dispatches a
   BA-emitted ticket David considered draft → the read-back-approval step (Phase 3) is the
   guard; if that proves insufficient in the pilot, the pilot note captures it as friction.
4. **This ticket's DoD excludes the live morning.** The executor cannot converse with David;
   verify stops at spec + skill + dry-run mechanics + pilot note. If David expected C2 closed
   by this ticket → the north-star annotation (Move 7) states the closure condition explicitly;
   flag stands in the portfolio ticket too.
5. **Digest's one write (the last-briefing counter) SHOULD fire on real BA mornings.**
   Plausible: it is digest.py's documented designed seam ("the briefing counter + 'since'
   timestamp for next time"). If double-counting with other digest consumers becomes an issue,
   it surfaces in the pilot — note it, do not redesign the seam now.
6. **No concurrent war game rewrites the touched docs.** T2-03 (digest --list) touches
   project-digest, not these files; T1-04 touches north-star's C4 line, not C2. Recon 10
   catches a live collision → Abort A1 on the seam-dirt case.

## Abort conditions

- **A1 — BA implementation already exists / seam under concurrent edit.** Park: write
  `engine/store/needs-decision/wg-t2-01-ba-agent.json` with
  `{"ticket":"wg-t2-01-ba-agent","question":"A producer/BA artifact already exists (or the exact seam is mid-edit by another session): <what/where>. Verify-and-close against it, or rebuild per the war game?","observed":"<paths + evidence>"}`.
  Leave the ticket in `running/`. Never build a rival.
- **A2 — the P1 gate (project-digest) is broken.** Recon 4 / Fork F2-B traceback. Park with the
  traceback and question: "digest.py crashes; the BA's input contract has no live ground truth.
  Fix digest first (separate ticket) or design against the documented JSON shape only?"
- **A3 — the pinned contract moved.** §3's contract materially differs, the queue idiom shifted,
  or the north-star spine is restructured. Park with the diff and question: "daily-operating-model
  §3 / store idiom no longer matches the war game (authored 2026-07-06). Re-recon and re-author,
  or proceed against the new contract?" Never redesign around a moved contract by guesswork.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting paths.
- **A5 — the design genuinely needs a mechanism this war game didn't ground** (a new store dir,
  a daemon, a cron, a cross-repo write). Park with the proposed mechanism and why; never build
  it silently.

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
# 1. Spec exists with every mandated section
for h in "Contract (pinned)" "Boundaries" "Session shape" "Phase 1" "Phase 2" "Phase 3" \
         "Ticket contract" "goal-plan seam" "Edges" "v1 limits" "First live morning" "Open questions"; do
  grep -q "$h" docs/ba-agent-spec.md && echo "ok: $h" || echo "MISSING: $h"; done   # 12 × ok

# 2. Skill exists, trigger-only description, hard rules present
grep -c "^name: producer" .claude/skills/producer/SKILL.md      # → 1  (or ba-producer per F1-A)
grep -c "Use when" .claude/skills/producer/SKILL.md             # → ≥1
grep -ci "never dispatch" .claude/skills/producer/SKILL.md      # → ≥1

# 3. Emitter works — positive, negative, and id idiom
python3 .claude/skills/producer/emit-ticket.py --help >/dev/null && echo help-ok
T=$(mktemp -d)
python3 .claude/skills/producer/emit-ticket.py --slug dryrun-verify --title "DRYRUN verify — ignore" \
  --prompt "p" --verify "v" --out "$T"
python3 - "$T" <<'EOF'
import json, os, re, sys
d = sys.argv[1]; f = [x for x in os.listdir(d) if x.endswith(".json")][0]
t = json.load(open(os.path.join(d, f)))
assert t["ticket"] == f[:-5] and re.match(r"^\d{8}T\d{4}Z-dryrun-verify", t["ticket"])
assert t["kind"] == "instruction" and t["executor"] == "swagger" and t["priority"] == "normal"
assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", t["requested_at"])
assert t["prompt"] and t["verify"] and t["depends_on"] == []
print("emitter-ok")
EOF
python3 .claude/skills/producer/emit-ticket.py --slug dryrun-x --title t --prompt p --out "$T" \
  && echo BAD-accepted-missing-verify || echo negative-ok        # → negative-ok
rm -r "$T"

# 4. Negative checks — what must NOT have changed
ls engine/store/queue/ | grep -ci dryrun                                        # → 0
ls /Users/davidcruwys/dev/ad/appydave-plugins/*/skills/ 2>/dev/null | grep -ci "^producer$"  # → 0 (never staged into plugins)
grep -c "✅.*C2" docs/north-star.md                                             # → 0 (C2 not claimed done)
git diff HEAD~1 --stat -- .claude/skills/marshall .claude/skills/swagger | wc -l  # → 0

# 5. Docs wired + pilot note + pushed
grep -c "ba-agent-spec" docs/INDEX.md docs/north-star.md docs/daily-operating-model.md  # ≥1 each
ls backlog/*ba-agent-pilot.md | wc -l                                           # → 1
git log --oneline -1     # shows the feat(producer) commit; git status clean of your files
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT touch `/Users/davidcruwys/dev/ad/apps/project-digest/` (T2-03/T2-04
  own it — you only RUN digest.py, never edit it). Do NOT touch `.claude/skills/marshall/` or
  `swagger/`, `engine/*.py`, anything under `experiments/`, or the appydave-plugins repo
  (producer stays a dark-factory-local skill; promotion to plugins is a separate David
  decision per this repo's CLAUDE.md).
- **The rabbit hole: building the multi-project morning.** The moment you touch the interview
  loop you will want `digest.py --list`, project #2, or an activity sweep. Skip ALL of it —
  David parked multi-project deliberately (Recon 9); those are portfolio tickets T2-02/03/04.
  v1 is one project, hard-coded to the one existing digest config.
- **Second rabbit hole: making the BA autonomous.** No cron, no launchd, no self-firing, no
  headless anything — the BA is the one place the human is the bottleneck BY DESIGN
  (daily-operating-model §1). The self-test simulates David only to prove emission mechanics.
- **Style:** spec and skill in David's voice — terse, tables over prose, trigger-only
  descriptions, decisions carry dates, corrections quoted (see marshall's SKILL.md for the
  live pattern). emit-ticket.py stdlib-only, small functions, no cleverness.
- **Prefer parking over guessing** on anything that smells like a moved contract (A3), a rival
  build (A1), or a needed-but-ungrounded mechanism (A5). The spec you write becomes the
  factory's morning front door — a parked question costs minutes; a guessed contract poisons
  every downstream T2 ticket.
