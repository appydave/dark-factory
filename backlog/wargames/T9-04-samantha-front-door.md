# T9-04 — Samantha Q&A front door v1

| field | value |
|---|---|
| ticket | wg-t9-04-samantha-front-door |
| track / size / priority | T9 Voice / L / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t2-01-ba-agent |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Build the factory's spoken front door — the intake agent intake.md calls "the Q&A bot — think
Samantha". The voice channel already exists end-to-end (OMI wearable → `omi-fetch` pulse →
enriched, signal-classified captures on disk); what is MISSING is exactly what
`docs/comms-flow.md` §3a names: *"no consumer turns this into a ticket — still a human's
judgment call"*. Size L = design-first: done means **(a)** `docs/samantha-spec.md` exists — the
front-door design (two intake lanes, Q&A read-only surface, triage protocol, ticket contract,
hard laws, v1 limits); **(b)** a working v1 skill at `.claude/skills/samantha/` (SKILL.md +
stdlib `intake-scan.py` helper) that David invokes in an interactive session to (i) answer
"what's in flight?" read-only and (ii) drain untriaged OMI captures into read-back-approved
tickets in `engine/store/queue/` via T2-01's emitter; **(c)** the drain mechanics are proven by
a fixture self-test (scratch dir + scratch index — NEVER the live queue, NEVER a write into
omi-fetch's store); **(d)** docs are wired (intake.md, human-comms.md, comms-flow.md §3a
annotation, INDEX.md line) and a pilot note tells David how to run the first live drain. The
live drain itself is HITL — the pilot note's job, not this ticket's verify. This ticket does
NOT build the always-on auto-consumer (event → ticket with no human) — that is explicitly
deferred; the spec names it as the upgrade path.

## Locked context

- **Hard law (candidate brief + intake.md, 2026-06-01):** Samantha *"captures ideas and files
  tickets, never spawns sessions."* intake.md: *"kicking off a task writes a ticket; it does not
  spawn a Claude Code session."* Nothing in this ticket spawns `claude`, a worker, a pool, or
  the orchestrator.
- **Voice Law (comms-flow.md §8, David go 2026-07-06):** voice-triggered surfaces are
  constitutionally READ-ONLY; any state change goes through the file-contract queue path
  (`queue/ → running/ → done/`), never a direct voice-to-mutation shortcut. Consequence for v1:
  Samantha answers questions read-only, and the ONE mutation she performs is writing a
  David-approved ticket file into `queue/` — the sanctioned path.
- **Q7 (decisions.md):** voice/human-comms is IN the portfolio; Samantha front door is this
  ticket. **Q4:** everything through the engine — output is ticket JSONs per
  `engine/store/queue/.CONVENTION.md`.
- **T9-05 is a LATER candidate** (intake physical home: `backlog/` vs dedicated `intake/`).
  This ticket must NOT create a new `intake/` directory — v1 uses `queue/` for tickets and
  `backlog/` for parked notes, and the spec names the home question as open.
- **Warehouse hard rule (intake.md):** nothing enters `research/` from intake. Samantha never
  writes there.
- **No `-p`/headless/SDK ever; interactive `claude` only.** Samantha runs inside a
  David-attended interactive session. No launchd agent, no cron, no daemon is added by this
  ticket.
- **No YLO/POEM work** — out of scope entirely.
- **Privacy (daily-operating-model §5):** work lane only. OMI captures can contain life/PII
  content — such captures are SKIPPED (marked, never ticketed, transcript never quoted into a
  repo file).

## Recon (verify before any work)

Docs lag code. Run every check from `/Users/davidcruwys/dev/ad/apps/dark-factory`.

1. `sed -n '160,166p' docs/comms-flow.md` → expect the §8 Voice Law heading
   (`## 8. Voice law — voice-triggered surfaces are read-only`) and the "David go 2026-07-06"
   source line. `sed -n '48,60p' docs/comms-flow.md` → expect §3a's "MISSING — no consumer
   turns this into a ticket". Voice Law gone or materially changed → **Abort A3**. §3a gap
   already annotated as closed → **Fork F1** (someone built a consumer).
2. **Dependency gate (wg-t2-01-ba-agent):** `ls .claude/skills/producer/emit-ticket.py 2>&1 ||
   ls .claude/skills/ba-producer/emit-ticket.py 2>&1` → expect exactly one to exist (T2-01's
   Fork F1-A may have renamed the skill `ba-producer`), and
   `python3 <found-path> --help` exits 0 showing `--slug --title --prompt --verify --out`
   flags. Found under `ba-producer` → **Fork F3** (adjust every emitter path below). Neither
   exists → **Abort A2** — the dependency has not landed; never build a second emitter.
3. `ls .claude/skills/` → expect NO `samantha` entry (as of 2026-07-06:
   `comprehend-visualise conductor image-gen marshall millwright store swagger` + whatever
   T2-01 added); `ls docs/samantha-spec.md 2>&1` → expect "No such file";
   `grep -rli "samantha" ~/.claude/skills/ /Users/davidcruwys/dev/ad/appydave-plugins/*/skills/ 2>/dev/null`
   → expect no hits (authoring-time recon 2026-07-06 found none — only a passing mention in a
   plugins doc, not a skill). Any exists → **Fork F1**.
4. **omi-fetch liveness:** `launchctl list | grep com.appydave.omi-fetch` → expect a row
   (exit-code column 0). `ls ~/dev/ad/apps/omi-fetch/store/index.jsonl` → exists.
   `python3 ~/dev/ad/apps/omi-fetch/lookup.py --list | head -5` → prints capture codes.
   `python3 ~/dev/ad/apps/omi-fetch/lookup.py --signal idea --since 2026-07-01 | head -5` →
   prints filtered captures. Index missing or lookup.py tracebacks → **Fork F2 Route B**.
5. **Enrichment coverage:** `python3 -c "import json; rows=[json.loads(l) for l in open('$HOME/dev/ad/apps/omi-fetch/store/index.jsonl')]; print(len(rows), sum(1 for r in rows if r.get('enriched_at')), sorted({r.get('signal') for r in rows}))"`
   → expect total ≈ enriched (2026-07-06 baseline: 291/291) and the signal set
   `['direction', 'feedback', 'idea', 'noise']`. A large unenriched tail → **Fork F2 Route A**
   (design already tolerates it). Index row shape baseline (13 keys, verified 2026-07-06):
   `archive_path code enriched_at enrichment_engine fetched_at id segments signal started_at
   status synopsis tags title`.
6. `sed -n '39,47p' docs/intake.md` → expect the `## The Q&A bot — the spoken front door`
   section with the never-spawns rule. `sed -n '43,48p' docs/human-comms.md` → expect the
   Open decisions block incl. *"Does the Q&A bot get a name? Samantha is the reference, not
   yet the name."* Either section gone → **Abort A3**.
7. `cat engine/store/queue/.CONVENTION.md` and one recent real ticket (any file in
   `engine/store/done/`) → confirm the id idiom `<YYYYMMDD>T<HHMM>Z-<slug>` with filename ==
   `<ticket>.json`. Shifted → **Abort A3**.
8. `python3 engine/status.py --json > /dev/null && echo status-ok` → expect `status-ok`
   (the Q&A read surface). Traceback → status answers degrade to raw `ls` of the store dirs;
   note it in the spec's Edges, do not fix status.py (not this ticket's seam).
9. `ls engine/store/queue/ > /tmp/t9-04-queue-before.txt; cat /tmp/t9-04-queue-before.txt` →
   snapshot for the Move-6 guard (do not assume contents — Phase-5 promotion drains war-game
   tickets in progressively). `launchctl list | grep com.appydave.dark-factory-wake` → note
   the wake watcher is loaded: a test ticket in the live queue would notify David. Tests NEVER
   write there.
10. `stat -f %m ~/dev/ad/apps/omi-fetch/store/index.jsonl` → record the mtime (Move-6 guard:
    scan is read-only against the live index; mtime may legitimately advance by the pulse —
    the guard is that YOUR code opened it read-only, enforced by the fixture test + a grep
    that `intake-scan.py` never opens the omi-fetch path in write mode).
11. `git -C /Users/davidcruwys/dev/ad/apps/dark-factory status --porcelain` → expect clean or
    dirt only in files this ticket never touches. Dirt in `docs/intake.md`,
    `docs/human-comms.md`, `docs/comms-flow.md`, `docs/INDEX.md`, or `.claude/skills/` →
    someone is mid-change on your seam → **Abort A1**.

## Moves

1. **Do:** Deep-read the design inputs, notes in the scratchpad (not the repo):
   `docs/intake.md` (all), `docs/human-comms.md` (all), `docs/comms-flow.md` §1 + §3a + §8,
   `docs/ba-agent-spec.md` + `.claude/skills/producer/SKILL.md` (or `ba-producer/` per F3 —
   T2-01's landed shape: the emitter flags, the read-back-approval idiom, the house skill
   style), `engine/store/queue/.CONVENTION.md`, `.claude/skills/marshall/SKILL.md` (hard-rules
   block idiom), `python3 ~/dev/ad/apps/omi-fetch/lookup.py --help`, and 3 real index rows
   (`head -3 ~/dev/ad/apps/omi-fetch/store/index.jsonl`).
   **Expect:** you can answer without re-reading: the Voice Law's one permitted mutation, the
   four signal values and which two are drain candidates (`direction`, `idea`), the emitter's
   required flags, why Samantha ≠ the Producer, and what the seen-ledger must record.
   **Failure signal:** any of those five is still fuzzy.
   **Counter-move:** re-read the specific source; two sources contradicting on a LAW (not a
   status line) → **Abort A3**.

2. **Do:** Write `docs/samantha-spec.md` — the front-door design. Required sections, in order:
   - `## Charter & hard laws` — Samantha is the factory's front door: Q&A in, tickets out.
     Restate verbatim-in-substance: captures ideas and files tickets, NEVER spawns sessions
     (intake.md); voice surfaces are read-only, the one sanctioned mutation is a David-approved
     ticket file in `queue/` (comms-flow.md §8, David go 2026-07-06); work lane only, PII
     captures are skipped unquoted.
   - `## Boundaries (what Samantha is NOT)` — not the Producer (the BA runs a deep
     one-project-at-a-time morning interview; Samantha is whole-factory intake + status Q&A —
     when a raw idea needs a real BA conversation, Samantha files it as a normal ticket or
     suggests a producer session, never runs the interview herself); not Marshall (files
     tickets, never claims/dispatches/reaps); not the auto-consumer (v1 drains in-session with
     David present; the event-driven no-human consumer is the named upgrade, not built); not
     audio-out (speaking back is T9-01's engine decision — v1 answers in text; the spec names
     the seam).
   - `## The two intake lanes` — **Lane 1, live:** David talks to Samantha directly in an
     interactive session (dictation or typing); she shapes the idea into a ticket draft on the
     spot. **Lane 2, OMI drain:** David talked to his wearable hours ago; `omi-fetch` pulsed,
     archived, enriched it; Samantha's drain lists untriaged captures with
     `signal ∈ {direction, idea}` via `intake-scan.py`, reads each transcript
     (`lookup.py <code> --archive-only` → read the file), and proposes: ticket / backlog note /
     skip (noise, PII, already-done).
   - `## Q&A surface (read-only)` — "what's in flight?" → `python3 engine/status.py`;
     "what's queued?" → `ls engine/store/queue/`; "did I mention X?" →
     `lookup.py --search X`. Every answer is a read; cite the Voice Law. Degradation: if
     status.py errors, fall back to raw `ls` of queue/running/done and say so.
   - `## Triage protocol` — per candidate capture: synopsis + Samantha's take (ticket-worthy?
     which priority?) → David decides → on "ticket": draft title/prompt/verify, read it back,
     emit ONLY on approval via the T2-01 emitter → confirm printed path → mark the capture
     `filed` in the seen-ledger with the ticket id. On "note": write
     `backlog/<date>-<slug>.md` (2–5 lines, the intake.md capture form), mark `noted`. On
     "skip": mark `skipped` with a one-word reason. Zero tickets is a valid session. Unmarked
     captures reappear next drain — nothing is silently lost.
   - `## Ticket contract` — reuse `.claude/skills/producer/emit-ticket.py` (path per F3)
     verbatim; field table matching `.CONVENTION.md`: `ticket` = `<YYYYMMDD>T<HHMM>Z-<slug>` ·
     `kind: instruction` · `source: "samantha intake <date> (OMI capture <code>)"` (or
     `"samantha live session <date>"` for Lane 1) · `executor: swagger` default ·
     `priority` David's call · `requested_by: "david (via samantha, <date>)"` · self-contained
     `prompt` · David-approved `verify`. No new emitter is written — the emitter is
     producer-owned, samantha-consumed; the spec notes the shared-lib question as open.
   - `## Seen-ledger` — `.claude/skills/samantha/intake-seen.jsonl`, append-only, one JSON
     line per triaged capture: `{code, verdict: filed|noted|skipped, ticket: <id|null>,
     ts: <UTC>}`. This is Samantha's ONE owned mutating store (the comms-flow §4 one-write
     rule); it never touches omi-fetch's store, which stays read-only to her.
   - `## Edges` — omi-fetch index unreadable (Lane 2 blocked; Lane 1 still works; say so);
     unenriched captures (list them flagged `unenriched`, Samantha reads the transcript and
     judges signal herself); PII/life capture (skip, mark `skipped:pii`, never quote the
     transcript into any repo file); David cuts the session (emitted tickets stand, unmarked
     captures reappear next drain); capture describes work that already shipped (skip with
     reason, cite what shipped).
   - `## v1 limits & upgrade path` — in-session drain only, no auto-consumer (upgrade: an
     event-driven consumer building on `engine/consumer.py`'s omi-fetch event bridge — a
     future ticket, gated on the auto-file trust question below); text answers only (audio-out
     = T9-01); intake home = `queue/` + `backlog/` pending T9-05; no `learning.yml` emission
     (T9-06); single machine (omi-fetch is machine-local, comms-flow §5).
   - `## First live drain — pilot protocol` — exact steps David runs (open `claude` at repo
     root → invoke samantha → drain since 2026-07-01 → triage ~10 captures), what to capture
     (misclassified signals, ticket quality, drain fatigue — is 10 too many?), where to note
     it (`backlog/<date>-samantha-pilot.md`, created by Move 8).
   - `## Open questions for David` — (1) the name: human-comms.md says "Samantha is the
     reference, not yet the name" — christen or rename; (2) auto-file threshold: should
     high-confidence `direction` captures ever file WITHOUT read-back (Voice Law tension —
     default NO in v1); (3) should the emitter move to a shared location now that two skills
     consume it; (4) OMI wake-word convention ("hey Samantha…" tagging at capture time) worth
     asking omi-fetch enrichment to detect?
   **Expect:** the file exists; every section present; nothing contradicts Locked context;
   150–300 lines.
   **Failure signal:** a section missing, or the spec invents ungrounded machinery (a daemon,
   a launchd agent, an `intake/` dir, a new emitter, an omi-fetch code change).
   **Counter-move:** cut the invention — the v1 surface is exactly: skill + scan helper +
   seen-ledger + reused emitter + queue writes + read-only lookups. If a new mechanism seems
   genuinely required → **Abort A5**, never build it silently.

3. **Do:** Write `.claude/skills/samantha/SKILL.md`. Frontmatter: `name: samantha` and a
   trigger-only description in David's voice (marshall/producer are the live pattern), e.g.:
   `"Samantha — the factory's spoken front door: Q&A + intake. Use when David says 'samantha',
   'drain my captures', 'what did I record', 'what's in flight' (front-door flavour), 'turn
   that idea into a ticket', or wants OMI voice ideas triaged into the queue. In = OMI captures
   (omi-fetch) or live conversation; out = read-back-approved tickets in engine/store/queue/.
   Read-only otherwise; never spawns sessions."` Body (terse, marshall-style): Preflight
   (check omi-fetch index readable; degrade to Lane-1-only) → Q&A surface (the read-only
   commands) → Drain (run `intake-scan.py`, triage per the spec protocol) → Emission (via the
   T2-01 emitter path) → Hard-rules block: never spawn a session/worker/pool/orchestrator ·
   never emit an unapproved ticket · never write to omi-fetch's store or `research/` · never
   quote a PII capture into a repo file · voice surfaces read-only, mutation = approved queue
   ticket only (comms-flow §8) · no auto-file in v1. Each phase points to its
   `docs/samantha-spec.md` section (spec is canonical; skill is the operating card).
   **Expect:** SKILL.md exists; description trigger-only ("Use when" present); body under
   ~120 lines; hard-rules block present.
   **Failure signal:** description narrates workflow; body duplicates whole spec sections.
   **Counter-move:** rewrite triggers-only; replace duplication with spec pointers.

4. **Do:** Write `.claude/skills/samantha/intake-scan.py` — stdlib-only, ~90–130 lines.
   Behaviour: argparse with `--index` (default
   `~/dev/ad/apps/omi-fetch/store/index.jsonl`, expanduser), `--ledger` (default
   `<skill-dir>/intake-seen.jsonl`), `--signal` (repeatable, default `direction` + `idea`),
   `--since YYYY-MM-DD` (filter on `started_at`), `--all` (include unenriched rows, flagged),
   `--json` (JSON-lines out instead of the table), and a mark mode:
   `--mark CODE --verdict {filed,noted,skipped} [--ticket ID] [--reason TXT]`.
   Scan mode: open the index READ-ONLY (`open(path)` — literally never `"w"`/`"a"` on any
   path containing `omi-fetch`), skip rows whose `code` appears in the ledger, skip
   `signal ∈ {noise, feedback}` unless `--all`, print per candidate: `code · started_at ·
   signal · title · synopsis` (table) and exit 0 (exit 3 when zero candidates — a clean
   "inbox empty" signal). Mark mode: append one JSON line
   `{"code":…,"verdict":…,"ticket":…,"reason":…,"ts":"<UTC ISO Z>"}` to the ledger (create
   file if absent), refuse an unknown verdict (exit 2), refuse `--verdict filed` without
   `--ticket` (exit 2). Missing/unparseable index → exit 4 with a one-line error naming
   Lane-1-only degradation.
   **Expect:** `python3 .claude/skills/samantha/intake-scan.py --help` exits 0 showing all
   flags; `grep -c 'open(' intake-scan.py` shows no write-mode open on the index path.
   **Failure signal:** traceback on --help, any non-stdlib import, or any code path that
   writes inside `omi-fetch/`.
   **Counter-move:** fix; stdlib-only and read-only-index are non-negotiable (engine
   convention + Voice Law).

5. **Do:** Fixture self-test (positive path), entirely in the scratchpad dir. Build
   `<scratch>/t9-04/fixture-index.jsonl` with 4 handwritten rows mimicking the 13-key real
   shape (Recon 5): codes `X001` signal `idea`, `X002` signal `direction`, `X003` signal
   `noise`, `X004` with `enriched_at` null/absent. Then:
   (a) `intake-scan.py --index <fixture> --ledger <scratch>/t9-04/ledger.jsonl` → expect
   exactly X001 + X002 listed, exit 0.
   (b) `--all` variant → X004 additionally listed, flagged unenriched; X003 still excluded
   only when `--signal` defaults apply — with `--all` include it too (all = everything
   untriaged): expect X001 X002 X003 X004.
   (c) `--mark X001 --verdict filed --ticket 20260706T1200Z-dryrun-samantha-selftest
   --ledger <same>` → exit 0; re-run (a) → only X002; ledger line parses with all four keys +
   UTC `ts`.
   (d) `--mark X002 --verdict skipped --reason noise --ledger <same>` then (a) → zero
   candidates, exit 3.
   (e) Emitter integration: emit ONE ticket via the T2-01 emitter with
   `--slug dryrun-samantha-selftest --title "DRYRUN: samantha self-test — ignore" --prompt p
   --verify v --out <scratch>/t9-04/queue` → file lands there; validate with a python
   heredoc: json loads · `ticket` == filename stem · matches
   `^\d{8}T\d{4}Z-dryrun-samantha-selftest$` · `requested_at` matches
   `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$` · non-empty prompt/verify.
   **Expect:** all five sub-checks pass.
   **Failure signal:** wrong candidate set, ledger malformed, or the emitted ticket lands
   anywhere but the scratch queue.
   **Counter-move:** fix intake-scan.py and re-run Move 5 from a fresh scratch dir. Emitter
   itself misbehaving (it is T2-01's artifact, not yours) → do NOT patch it → **Abort A2**
   with the failing invocation.

6. **Do:** Negative + guard checks. (a) `--mark X009 --verdict bogus` → exit 2, ledger
   unchanged. (b) `--verdict filed` without `--ticket` → exit 2. (c) `--index /nonexistent`
   → exit 4, one-line Lane-1 message, no traceback. (d) Live-store guard:
   `ls engine/store/queue/ | grep -ci dryrun` → `0`;
   `diff <(ls engine/store/queue/) /tmp/t9-04-queue-before.txt` → tolerate lines OTHER
   sessions added, but zero lines containing `samantha` or `dryrun`. (e) omi-fetch guard:
   `git -C ~/dev/ad/apps/omi-fetch status --porcelain` shows nothing newly changed by you
   (the pulse may touch `store/`; your name appears in no diff) and
   `grep -n '"a"\|"w"' .claude/skills/samantha/intake-scan.py` shows write modes only on the
   ledger path. (f) `rm -rf <scratch>/t9-04`.
   **Expect:** exits 2/2/4; zero dryrun/samantha files in the live queue; omi-fetch
   untouched; scratch cleaned.
   **Failure signal:** a dryrun ticket in `engine/store/queue/` (the wake watcher will have
   pinged David).
   **Counter-move:** `rm engine/store/queue/*dryrun*` IMMEDIATELY, note the escape in the
   ticket result, and fix the test command that dropped `--out` before proceeding.

7. **Do:** Doc wiring, tightly fenced — four one-liners:
   (i) `docs/intake.md`, end of the `## The Q&A bot — the spoken front door` section: append
   one line: `**v1 landed <date>** — docs/samantha-spec.md + .claude/skills/samantha/
   (in-session drain, read-back-gated; auto-consumer still open).`
   (ii) `docs/human-comms.md`, the `## Open decisions` block: annotate the Q&A-bot-name line
   with ` — v1 shipped under working name samantha (<date>); christening still David's call
   (samantha-spec.md open questions).`
   (iii) `docs/comms-flow.md` §3a, directly under the "MISSING — no consumer" diagram line:
   one-line annotation: `> <date>: PARTIALLY closed — samantha skill drains captures →
   read-back-approved tickets in-session (docs/samantha-spec.md); the no-human auto-consumer
   remains open.` Do NOT mark the gap closed.
   (iv) `docs/INDEX.md`, "The human side" section: one line for `samantha-spec.md`
   immediately after the `intake.md` entry.
   **Expect:** four files, diff of 1–2 lines each.
   **Failure signal:** any diff restructures more than its one line.
   **Counter-move:** `git checkout -- <file>` and redo as a pure append/insert.

8. **Do:** Write the pilot note `backlog/$(date +%Y-%m-%d)-samantha-pilot.md` — directive,
   ~20 lines: what landed (spec + skill paths, absolute), how David runs the first live drain
   (open `claude` at repo root → "samantha, drain my captures since 2026-07-01" → triage →
   approved tickets land in `queue/` → wake watcher notifies), what to capture (signal
   misclassifications, ticket quality, fatigue point), and the four open questions from the
   spec. End with: the front door counts as OPEN when one real drain has produced ≥1
   schema-valid ticket David didn't hand-edit, from a capture he spoke ≥1 hour earlier.
   **Expect:** the file exists and names only artifacts that exist.
   **Failure signal:** the note references anything unbuilt (auto-consumer, audio-out,
   wake-word).
   **Counter-move:** trim to what Moves 2–7 shipped.

9. **Do:** Commit and push (dark-factory only). Stage exactly: `docs/samantha-spec.md`,
   `.claude/skills/samantha/SKILL.md`, `.claude/skills/samantha/intake-scan.py`,
   `docs/intake.md`, `docs/human-comms.md`, `docs/comms-flow.md`, `docs/INDEX.md`,
   `backlog/<date>-samantha-pilot.md`. (Do NOT stage `intake-seen.jsonl` — it does not exist
   yet; the first live drain creates it. Add nothing to .gitignore — the ledger is meant to
   be committed by future sessions.) Message:
   `feat(samantha): Q&A front door v1 — intake spec + samantha skill + capture drain (T9-04)`.
   **Expect:** `git push` succeeds; `git status --porcelain` clean of your files.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — a samantha/front-door artifact already exists.**
Trigger: Recon 1 finds §3a annotated closed, or Recon 3 finds a `samantha` skill/spec anywhere.
→ **Route A** (same NAME, different purpose — the name-collision class): keep building, name
the skill `samantha-intake` instead, note the collision in the spec's Open questions + pilot
note, adjust every path in Moves 3–9.
→ **Route B** (a real capture→ticket front door exists — race with another session):
**Abort A1**. Never build a rival front door.

**F2 — omi-fetch baseline degraded vs broken.**
Trigger: Recon 4/5 misbehaves.
→ **Route A** (index readable but a large unenriched tail, or signal values drifted): proceed
— the design tolerates it (`--all` flag + Samantha judges unenriched transcripts herself);
record the observed state in the spec's Edges and the ticket result.
→ **Route B** (index.jsonl missing/unparseable or lookup.py tracebacks): the voice channel's
ground truth is down. Build cannot self-test Lane 2 against reality → **Abort A2** with the
traceback (fix omi-fetch first — separate ticket — or David okays fixture-only proof).

**F3 — T2-01 landed under a different name.**
Trigger: Recon 2 finds the emitter at `.claude/skills/ba-producer/emit-ticket.py` (T2-01's own
Fork F1-A) or another skill-dir name.
→ Use the found path in the spec's Ticket contract, SKILL.md's Emission section, and Move 5e.
No other change — the emitter's flag contract is what matters, not its directory.

## Assumptions ledger

1. **Working name `samantha` is acceptable for v1.** Plausible: it is intake.md's and the
   candidate's own reference name; human-comms.md explicitly says "reference, not yet the
   name", so the spec lists christening as open question #1. If David objects at triage →
   directory rename + description edit, not a park.
2. **Read-back approval on EVERY emission (no auto-file) is the right v1 posture.** Plausible:
   it is the Voice Law's own failure-mode rationale (misheard utterance must not silently
   mutate state) applied at the door. If David wants high-confidence auto-file → that is the
   spec's open question #2 and a follow-on ticket, never a silent v1 loosening.
3. **Reusing producer's emit-ticket.py cross-skill is acceptable.** Plausible: one emitter =
   one ticket idiom, and duplicating it is exactly the drift the factory fights; the shared-lib
   question is open question #3. If T2-01's emitter proves samantha-hostile (e.g. hardcodes
   BA-flavoured defaults that flags can't override) → **Abort A5** with the specific flag gap,
   do not fork the emitter.
4. **`signal ∈ {direction, idea}` is the right drain filter.** Plausible: taxonomy verified
   live 2026-07-06 (291/291 enriched; idea 109 · direction 85 · noise 61 · feedback 36);
   `feedback` and `noise` are not ticket-shaped. If triage shows ticket-worthy content hiding
   in `feedback` → the pilot note captures it; `--signal feedback` already works.
5. **The seen-ledger lives in the skill dir.** Plausible: comms-flow §4's one-write rule and
   no better home until T9-05 decides the intake home. If T9-05 later lands a dedicated
   `intake/` → the ledger migration is one file move; the spec says so.
6. **No concurrent war game rewrites the touched docs.** T9-01/T9-02 (audio-out, sounds) touch
   consumer.py/TTS, not intake.md/human-comms.md/comms-flow §3a; T2-01 touches
   daily-operating-model/north-star, not these. Recon 11 catches a live collision → Abort A1.

## Abort conditions

- **A1 — front door already exists / seam under concurrent edit.** Park: write
  `engine/store/needs-decision/wg-t9-04-samantha-front-door.json` with
  `{"ticket":"wg-t9-04-samantha-front-door","question":"A capture→ticket front door already exists (or the seam is mid-edit): <what/where>. Verify-and-close against it, or rebuild per the war game?","observed":"<paths + evidence>"}`.
  Leave the ticket in `running/`. Never build a rival.
- **A2 — a load-bearing dependency is down.** T2-01's emitter absent (Recon 2), the emitter
  misbehaves under test (Move 5e), or omi-fetch's index is broken (Fork F2-B). Park with the
  evidence and question: "Samantha needs <emitter|omi-fetch index>; it is <absent|broken>:
  <detail>. Land/fix the dependency first, or approve fixture-only proof?"
- **A3 — a LAW or contract moved.** The §8 Voice Law changed, intake.md's never-spawns rule
  gone, or the queue id idiom shifted. Park with the diff and question: "the war game (authored
  2026-07-06) is pinned to a law/idiom that has moved: <diff>. Re-author, or proceed against
  the new text?" Never redesign around a moved law by guesswork.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths.
- **A5 — the design genuinely needs an ungrounded mechanism** (a daemon/launchd agent, an
  `intake/` dir, an omi-fetch code change, an emitter fork, auto-file). Park with the proposed
  mechanism and why; never build it silently.

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
# 1. Spec exists with every mandated section
for h in "Charter & hard laws" "Boundaries" "two intake lanes" "Q&A surface" "Triage protocol" \
         "Ticket contract" "Seen-ledger" "Edges" "v1 limits" "First live drain" "Open questions"; do
  grep -qi "$h" docs/samantha-spec.md && echo "ok: $h" || echo "MISSING: $h"; done   # 11 × ok

# 2. Skill exists, trigger-only description, hard rules present
grep -c "^name: samantha" .claude/skills/samantha/SKILL.md        # → 1 (or samantha-intake per F1-A)
grep -c "Use when" .claude/skills/samantha/SKILL.md               # → ≥1
grep -ci "never spawn" .claude/skills/samantha/SKILL.md           # → ≥1
grep -ci "unapproved" .claude/skills/samantha/SKILL.md            # → ≥1

# 3. Scanner works — positive, negative, ledger round-trip (fixture, scratch)
python3 .claude/skills/samantha/intake-scan.py --help >/dev/null && echo help-ok
T=$(mktemp -d)
cat > "$T/idx.jsonl" <<'EOF'
{"code":"X001","signal":"idea","started_at":"2026-07-05T01:00:00Z","enriched_at":"x","title":"t1","synopsis":"s1"}
{"code":"X002","signal":"noise","started_at":"2026-07-05T02:00:00Z","enriched_at":"x","title":"t2","synopsis":"s2"}
EOF
python3 .claude/skills/samantha/intake-scan.py --index "$T/idx.jsonl" --ledger "$T/led.jsonl" | grep -c X001   # → 1
python3 .claude/skills/samantha/intake-scan.py --index "$T/idx.jsonl" --ledger "$T/led.jsonl" | grep -c X002   # → 0
python3 .claude/skills/samantha/intake-scan.py --mark X001 --verdict filed --ticket 20260706T1200Z-x --ledger "$T/led.jsonl"
python3 .claude/skills/samantha/intake-scan.py --index "$T/idx.jsonl" --ledger "$T/led.jsonl"; echo "exit=$?"  # → exit=3 (inbox empty)
python3 .claude/skills/samantha/intake-scan.py --mark X009 --verdict bogus --ledger "$T/led.jsonl" \
  && echo BAD-accepted-bogus || echo negative-ok                                                               # → negative-ok
rm -r "$T"

# 4. Negative checks — what must NOT have changed
ls engine/store/queue/ | grep -ci "dryrun\|samantha"                              # → 0
git -C ~/dev/ad/apps/omi-fetch status --porcelain | grep -cv "^?? store/"         # → 0 (no code touched there)
ls .claude/skills/samantha/intake-seen.jsonl 2>/dev/null | wc -l                  # → 0 (live ledger born at first real drain)
grep -rci "spawn\|tmux new-window\|subprocess.*claude" .claude/skills/samantha/intake-scan.py  # → 0
grep -c "MISSING" docs/comms-flow.md                                              # → ≥1 (gap annotated, NOT deleted)

# 5. Docs wired + pilot note + pushed
grep -c "samantha-spec" docs/INDEX.md docs/intake.md docs/comms-flow.md           # ≥1 each
grep -ci "samantha" docs/human-comms.md                                           # ≥2 (existing ref + annotation)
ls backlog/*samantha-pilot.md | wc -l                                             # → 1
git log --oneline -1     # shows the feat(samantha) commit; git status clean of your files
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT touch `~/dev/ad/apps/omi-fetch/` (read its store, run its CLIs,
  change nothing — it is a separate git repo with its own launchd pulse). Do NOT touch
  `engine/*.py` (consumer.py's event bridge is T9-01/T9-02 territory), `.claude/skills/`
  dirs other than `samantha/`, `research/`, `experiments/`, or appydave-plugins (samantha
  stays dark-factory-local; promotion is a separate David decision).
- **The rabbit hole: building the auto-consumer.** The moment you see
  `engine/consumer.py` already polling omi-fetch events, you will want to make it file
  tickets automatically. Do NOT — that removes the human from the door, violates the
  read-back rule this v1 is built on, and is explicitly the named upgrade path, not this
  ticket. v1 is in-session, David present, every emission approved.
- **Second rabbit hole: speech.** No TTS, no ElevenLabs, no kokoro wiring, no wake-word
  detection — audio-out is T9-01's decision; Samantha v1 hears through omi-fetch's existing
  store and answers in text.
- **Style:** spec and skill in David's voice — terse, tables over prose, trigger-only
  descriptions, laws quoted with dates (see marshall's SKILL.md and T2-01's producer for the
  live pattern). intake-scan.py stdlib-only, small functions, no cleverness.
- **Prefer parking over guessing** on anything that smells like a moved law (A3), a rival
  build (A1), a broken dependency (A2), or a needed-but-ungrounded mechanism (A5). The front
  door is the factory's most human-facing seam — a parked question costs minutes; a guessed
  law (auto-filing a misheard idea into a live dispatch queue) costs David's trust in the
  whole voice channel.
