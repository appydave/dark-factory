# T1-07 — Golden-job regression suite (Gap A)

| field | value |
|---|---|
| ticket | wg-t1-07-golden-job-suite |
| track / size / priority | T1 Engine / L / normal |
| executor | sonnet Swagger via engine |
| depends_on | none (design-first; trajectory fidelity upgrades later via T1-08 stability-1 — see Fork F1) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The engine ships machinery changes (kind-filter, CAP governor, verifier registry, auto-wake — four in the last 3 days) with zero replay gate: nothing catches "a change to the reap loop silently broke the HITL gate". This ticket is **design-first (size L)**: produce (1) a frozen set of ~5 golden jobs as ticket JSONs in `engine/golden/jobs/`, (2) the envelope/baseline schema + diff rules in a spec at `backlog/specs/golden-job-suite-spec.md`, with cost/trajectory extraction proven against the one real dispatch transcript that exists today, and (3) a queued follow-on build ticket for the replay runner (`engine/golden/replay.py`) + baseline-capture runbook. Done looks like: frozen jobs + spec + follow-on ticket on disk, all JSON parsing, no engine `.py` touched, nothing executed live.

## Locked context

- **Q4 (decisions.md):** everything through the engine — the follow-on build ticket is written for sonnet-Swagger/builder dispatch, not a Ralphy campaign.
- **No `-p` / headless / Agent SDK ever** (metered billing); interactive `claude` only. The replay harness design must not assume API access.
- **Ticket-first standing rule** (queue/.CONVENTION.md): the follow-on build work gets a real ticket JSON in `engine/store/queue/`.
- **Docs lag code:** every claim about engine state below was verified on disk 2026-07-06 or is re-verified by your Recon; never trust `docs/eval-architecture.md` status lines without checking.
- **HALT/BACKOFF** flags are respected implicitly by the engine; this ticket never needs to read them (it never dispatches anything).

## Recon (verify before any work)

1. `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/` → expect `orchestrator.py`, `warm_pool.py`, `status.py`, `consumer.py`, `store/`. If `orchestrator.py` is missing or the layout is materially different → **Abort A1**.
2. `grep -n "VERIFIERS\|CHECK_REGISTRY\|def dispatchable" engine/orchestrator.py` → expect all three symbols (as of 2026-07-06: `CHECK_REGISTRY` ~line 418, `VERIFIERS` ~line 470, `dispatchable` ~line 183, with check types `file_exists / json_parses / must_contain / git_commit_present / script / command`). Missing → the verifier registry was refactored → **Abort A1**.
3. `ls engine/golden/ 2>/dev/null` → expect **no such directory**. If it exists → **Fork F3**.
4. `wc -l engine/store/audit.jsonl` and for each entry check the `transcript` path exists (`python3 -c "import json,os; [print(r['ticket'], os.path.exists(r['transcript'])) for r in map(json.loads, open('engine/store/audit.jsonl'))]"`). As of authoring: exactly 1 entry (ticket `20260703T125625Z-constellation-2026-07-03-apps.json`, transcript exists, 99 lines, 40 messages with `usage`, 22 `tool_use` blocks). If NO audit entry has a surviving transcript → **Fork F2**.
5. `ls backlog/specs/stability-1-instrument-loop-spec.md` → expect it exists and its header still says `Status: SPEC ONLY — no build`. Also `ls engine/store/events/` → as of authoring, 1 file (`job.completed`). If lifecycle events beyond `job.completed` exist (e.g. `dispatched`, `teardown`) or an emitter module landed, stability-1 was built → **Fork F1 Route B**.
6. `grep -n "Gap A" docs/eval-architecture.md` → expect the Gap A section (~line 61) still describing the suite as unbuilt. If it already says built/landed → cross-check with recon 3; contradiction → **Abort A2**.
7. `ls ~/dev/ad/brains/evals/eval-harness-and-metrics.md && grep -n "Golden-job regression" ~/dev/ad/brains/evals/eval-harness-and-metrics.md` → expect the methodology section (~line 41). Missing → proceed using the design constraints inlined in Move 2 (this war game carries enough), and note the gap in the spec's provenance line.
8. `grep -n "WORKER_TIMEOUT\|MAX_RETRY\|HITL_TIMEOUT" engine/orchestrator.py` → expect `WORKER_TIMEOUT = 240`, `MAX_RETRY = 2`, `HITL_TIMEOUT = 1800` (constants feed envelope math in Move 4). Different values → use the on-disk values, not these.

## Moves

1. **Do:** Run Recon 1–8; record actual values (audit count, constants, stability-1 state) in a scratch note — they parameterize Moves 3–5.
   **Expect:** All checks land on their expected branch; you know which fork routes apply.
   **Failure signal:** Recon 1 or 2 misses → engine refactored under you.
   **Counter-move:** → Abort A1.

2. **Do:** Read `~/dev/ad/brains/evals/eval-harness-and-metrics.md` § "Golden-job regression suite" and `engine/README.md` § "Verifying a new ticket kind". Write down the binding design constraints: (a) goldens = frozen known-good jobs replayed on every machinery change, diffing **outcome + cost envelope + trajectory shape**; (b) budget to refresh goldens when the machinery legitimately changes (else false regressions); (c) verification must use the existing `verify_kind: "generic"` DSL — no new Python check types; (d) replay is **top-level only** — the runner boots `orchestrator.py` and therefore may NEVER itself run inside a df-worker (nested pools would collide on `df-worker-*` tmux names and the shared `store/`).
   **Expect:** A constraints list covering (a)–(d), kept for the spec's Design Constraints section.
   **Failure signal:** Brain file unreadable/section gone (Recon 7 already flagged).
   **Counter-move:** Use constraints (a)–(d) exactly as written here; cite this war game as the fallback source in the spec.

3. **Do:** Create `engine/golden/jobs/` and author **5 frozen golden-job ticket JSONs**, one per machinery leg, every one side-effect-fenced to `engine/golden/sandbox/` (the replay runner will reset that dir; jobs must create/modify files ONLY under it). Use the queue idiom (`ticket`, `kind`, `title`, `executor: "swagger"`, `prompt`, plus verify fields), names `g1-...json` … `g5-...json`:
   - **g1-happy-generic** — prompt: create `engine/golden/sandbox/g1/report.md` containing the literal line `GOLDEN-G1-OK` and write the standard `results/<ticket>.json` self-report. `verify_kind: "generic"`, checks: `file_exists` + `must_contain` on that file. Expected outcome: `done`.
   - **g2-artifacts-fallback** — no `verify_kind`; instead top-level `"artifacts": ["engine/golden/sandbox/g2/data.json"]` + `"verify_command"` that json-parses it (exercises `verify_artifacts_fallback`). Expected outcome: `done`.
   - **g3-hitl-scripted** — a two-step job (write `engine/golden/sandbox/g3/draft.md`, then request a decision via `engine/store/needs-decision/<ticket>` per the HITL flow, then on approve write `final.md`). Replay runner dispatches it with `--hitl <ticket-filename>` and itself writes `{"action":"approve"}` to `engine/store/decisions/<ticket>` when the needs-decision file appears — the gate is exercised mechanically, no human. Expected outcome: `done` with a `[HITL] resumed` line in orchestrator output.
   - **g4-verify-fail** — prompt: write `engine/golden/sandbox/g4/out.md` containing `WRONG-MARKER`; `verify_kind: "generic"` check `must_contain: "GOLDEN-G4-OK"` (deliberately unsatisfiable). Expected outcome: `failed(verify)` after `WORKER_TIMEOUT` (240s at authoring) — the golden proves bad work cannot slip into `done/`. Note the wall-cost in the ticket's comment field.
   - **g5-kind-filter-negative** — a `kind: "external-research"` ticket. Replay runner drops it in `queue/`, runs the engine, and asserts it is **still in `queue/` untouched** with a `[skip]` line emitted (exercises `dispatchable()`). Expected outcome: not dispatched. No worker cost.
   Also write `engine/golden/jobs/README.md` (5 lines): these are FROZEN — never place them in `engine/store/queue/` at rest (auto-wake would dispatch them); the runner copies them in per replay, fresh timestamp prefix each run.
   **Expect:** 6 files under `engine/golden/jobs/`; every `.json` parses; every sandbox path starts `engine/golden/sandbox/`.
   **Failure signal:** A job can't be expressed without a new `CHECK_REGISTRY` type or without touching files outside the sandbox.
   **Counter-move:** Simplify that job until it fits the existing DSL + sandbox; if the machinery leg genuinely can't be exercised within existing checks, drop to 4 jobs and record the uncovered leg in the spec's Known Gaps — do NOT write Python.

4. **Do:** Define the baseline/envelope schema and prove extraction. Create `engine/golden/baselines/SCHEMA.md` specifying per-job `baselines/<job>.json`: `{"job", "expected_outcome" ("done"|"failed(verify)"|"not-dispatched"), "wall_s": {"min","max"}, "cost": {"assistant_turns":{"min","max"}, "output_tokens":{"min","max"}}, "trajectory": {"tools_used": [names], "tool_calls":{"min","max"}}, "captured_at", "engine_git_sha"}`. Diff rule: outcome mismatch = HARD FAIL; envelope breach (any min/max) = FLAG (report, non-blocking); trajectory = compare the SET of tool names + call-count range, never exact sequences (sequences are non-deterministic — Goodhart trap). Then prove the extraction fields exist: run a read-only python snippet over the audit.jsonl transcript found in Recon 4, counting messages-with-`usage`, summing `output_tokens`, and listing `tool_use` names; paste the snippet + its real output into SCHEMA.md as the worked example. Baselines themselves are NOT computed here (they come from the capture run — follow-on).
   **Expect:** `SCHEMA.md` exists with schema + working snippet + real numbers from the 2026-07-03 constellation transcript.
   **Failure signal:** Snippet errors or transcript lacks `usage`/`tool_use` fields.
   **Counter-move:** → Fork F2.

5. **Do:** Write `backlog/specs/golden-job-suite-spec.md` (match the house style of `backlog/specs/stability-1-instrument-loop-spec.md`: Purpose / Problem / Goals / Non-Goals / Scope / Design / Build plan). Must contain: the 5 jobs table with expected outcomes; the envelope schema (point at SCHEMA.md); diff rules incl. HARD-FAIL vs FLAG; **replay protocol** — top-level session or cron ONLY, never inside a df-worker (constraint (d)), runner copies jobs→`queue/` with fresh timestamp prefixes, resets `engine/golden/sandbox/`, boots `python3 orchestrator.py --pool 1 --model sonnet --teardown`, scripts the g3 decision file, then diffs store state + transcripts against `baselines/`; **trigger** — run before committing any change to `engine/*.py` (advisory CI gate, human-invoked; no hook/cron installed by this ticket); **refresh policy** — an intentional machinery change that legitimately shifts an envelope gets new baselines via a fresh capture run, recorded with `engine_git_sha` (methodology constraint (b)); **fidelity note per Fork F1** (transcript-derived trajectories now; stability-1 lifecycle events upgrade fidelity when T1-08 lands); **Non-Goals**: no judge/LLM scoring (that's Gap B), no artifact-eval Surface-1 anything, no retention policy (T1-10).
   **Expect:** Spec file exists; `grep -c "^## " backlog/specs/golden-job-suite-spec.md` ≥ 6.
   **Failure signal:** You find yourself re-speccing trace capture (stability-1's job) or comparison registries (DF-8's job).
   **Counter-move:** Delete the overlap, reference the owning spec by path instead — `docs/eval-architecture.md` names the owners.

6. **Do:** Write the follow-on build ticket to `engine/store/queue/<UTCstamp>-golden-replay-runner.json` (stamp via `date -u +%Y%m%dT%H%MZ` prefix, queue idiom, `executor: "swagger"`, `priority: "normal"`, `requested_by: "wg-t1-07-golden-job-suite"`): build `engine/golden/replay.py` per the spec §Design + a `RUNBOOK.md` documenting the human-invoked baseline-capture run; the ticket's prompt must state the runner is top-level-only and that the BUILD ticket itself must not execute a replay (same nesting rule); `verify_kind: "generic"` with `file_exists` checks on `engine/golden/replay.py` + `RUNBOOK.md` and a `command` check `python3 -m py_compile engine/golden/replay.py`.
   **Expect:** Ticket JSON parses; sitting in `queue/`; `dispatchable()` would accept it (no `kind: external-research`, not deferred).
   **Failure signal:** Queue dir missing or convention file demands fields you can't infer.
   **Counter-move:** Re-read `engine/store/queue/.CONVENTION.md` and mimic the newest ticket in `engine/store/done/` field-for-field; if still ambiguous → Abort A3.

7. **Do:** Update `docs/eval-architecture.md` Gap A bullet only: append one line — "2026-07-06+: design + frozen jobs landed (`engine/golden/`, `backlog/specs/golden-job-suite-spec.md`); replay runner ticket queued; trajectory fidelity upgrades when stability-1 lands." Touch nothing else in that file.
   **Expect:** `git diff docs/eval-architecture.md` shows a 1–2 line addition inside the Gap A section only.
   **Failure signal:** Diff bleeds into Gap B or the tables.
   **Counter-move:** `git checkout -- docs/eval-architecture.md`, redo as a single appended line.

8. **Do:** Run the Verification block below, then commit everything created/edited with message `feat(engine): golden-job regression suite — design, 5 frozen jobs, replay-runner ticket (wg-t1-07)` and push to main.
   **Expect:** All verification commands exit 0; `git push` succeeds.
   **Failure signal:** Any check fails, or push rejected (remote moved).
   **Counter-move:** Fix the failing artifact and re-verify; on push rejection `git pull --rebase` then push; if rebase conflicts touch files you didn't author → Abort A3.

## Forks

**F1 — trajectory-envelope source.** Trigger: Recon 5 outcome.
- **Route A (stability-1 still spec-only — expected):** baselines/diffs derive cost + trajectory from the audit.jsonl→transcript chain (orchestrator-written, external to the worker — good enough). Spec carries the fidelity note.
- **Route B (stability-1 events landed):** spec's Design section names lifecycle events as the primary trajectory source with transcripts as fallback; envelope schema gains an `events` block (names only, no build). Everything else unchanged.

**F2 — no usable historical transcript.** Trigger: Recon 4 finds zero surviving transcripts, or Move 4's snippet finds no `usage`/`tool_use` fields.
- **Route A (fields absent in the found transcript only):** try any other `~/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/*.jsonl` newer than 2026-07-01 as the worked example.
- **Route B (none work):** ship SCHEMA.md with the snippet marked UNPROVEN and add "validate extraction on first capture run" as an explicit acceptance item in the follow-on ticket's prompt. Do not block the design on it.

**F3 — `engine/golden/` already exists.** Trigger: Recon 3.
- **Route A (empty or stub — a placeholder):** adopt the dir, continue from Move 2.
- **Route B (populated with jobs/ or baselines/ or replay.py):** someone built or started the suite since authoring → **Abort A2** (never overwrite parallel work).

## Assumptions ledger

- **`engine/golden/` is the right home** (engine-owned CI gate, beside the machinery it gates) rather than `tools/`. Plausible: engine/ is the live convention for engine-adjacent code; CLAUDE.md's write-table predates the engine. If David objects at triage → paths are self-contained under one dir; a `git mv` relocates cleanly. Executor: proceed.
- **5 jobs / these 5 legs** is Fable's selection (happy-generic, artifacts-fallback, HITL-scripted, verify-fail, kind-filter-negative). 4–6 is acceptable if Move 3's counter-move fires; fewer than 4 → the suite is too thin → note in spec and continue, flag in commit message.
- **Replay-is-top-level-only** is asserted here from mechanism (tmux name + store collisions), not from a David ruling. If any future doc mandates engine-dispatched replays → write `engine/store/needs-decision/wg-t1-07-golden-job-suite.json` asking which wins; do not design around nesting.
- **Queueing the follow-on ticket immediately** (vs staging for triage) follows the ticket-first standing rule; auto-wake may dispatch it unattended. Plausible per Q4 doctrine. If that feels wrong at execution time (e.g. a HALT flag is up), still queue it — the engine's flags govern dispatch, not you.
- **`failed(verify)` outcome for g4 is observable only in orchestrator stdout + absence from `done/`** (failed tickets stay in `running/` after settle — verify this during the capture run, not now). If capture shows a different failure surface, the runner ticket owner adjusts the diff rule; envelope schema already treats outcome as a string.

## Abort conditions

- **A1 — engine refactored:** `orchestrator.py` missing, or `VERIFIERS`/`CHECK_REGISTRY`/`dispatchable` gone (Recon 1–2). Park: write `engine/store/needs-decision/wg-t1-07-golden-job-suite.json` — `{"ticket":"wg-t1-07-golden-job-suite","question":"Engine layout/verifier registry diverged from the 2026-07-06 war-game recon (<what you found>). Golden-job design targets a moving surface — re-author against current engine?","proposed":"re-recon and re-author","ts":"<UTC now>"}`. Leave the ticket in `running/`. Never guess past this.
- **A2 — suite already exists / doc contradicts disk:** Fork F3 Route B, or Recon 6 contradiction. Park with question: "engine/golden/ already populated by <evidence> — adopt, merge, or supersede?" Same file, same rules.
- **A3 — cannot proceed without live execution or without overwriting foreign work:** any path where completing a move would require booting `orchestrator.py`/`warm_pool.py` from inside this worker session, or force-pushing over unrecognized commits. Park with the specific blocker. NEVER run the engine from inside a df-worker.

## Verification

All from repo root; every command must exit 0:

```bash
# frozen jobs exist and parse (>=4 jobs + README)
ls engine/golden/jobs/*.json | wc -l                       # >= 4
python3 - <<'EOF'
import json, glob
for f in glob.glob("engine/golden/jobs/*.json"): json.load(open(f))
print("jobs parse OK")
EOF
test -f engine/golden/jobs/README.md
# every job is sandbox-fenced (no job writes outside engine/golden/sandbox/)
! grep -L "engine/golden/sandbox/" engine/golden/jobs/g*.json | grep -v g5   # g5 (negative) exempt
# schema + worked example
grep -q "engine_git_sha" engine/golden/baselines/SCHEMA.md
grep -q "tool_use" engine/golden/baselines/SCHEMA.md
# spec exists with required sections
test -f backlog/specs/golden-job-suite-spec.md
grep -q "top-level" backlog/specs/golden-job-suite-spec.md
grep -qi "refresh" backlog/specs/golden-job-suite-spec.md
# follow-on ticket queued and parses
python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('engine/store/queue/*golden-replay-runner.json')]" && ls engine/store/queue/*golden-replay-runner.json
# Gap A status line appended
grep -q "frozen jobs landed" docs/eval-architecture.md
```

Negative checks (must be true):

```bash
git diff HEAD~1 --name-only | grep -E "engine/(orchestrator|warm_pool|status|consumer)\.py" | wc -l   # 0 — no engine code touched
ls engine/golden/baselines/*.json 2>/dev/null | wc -l    # 0 — no baselines invented without a capture run
ls engine/golden/replay.py 2>/dev/null | wc -l           # 0 — runner is the follow-on ticket's job
ls engine/store/queue/g[1-5]-*.json 2>/dev/null | wc -l  # 0 — frozen jobs never rest in the live queue
```

## Executor notes (sonnet)

- **Scope fence:** do NOT modify `engine/*.py`, `engine/store/done|running|results|audit.jsonl`, anything under `research/`, or any other spec in `backlog/specs/`. Your writes: `engine/golden/{jobs,baselines}/`, one new spec file, one queue ticket, one appended line in `docs/eval-architecture.md`.
- **Never execute:** no `orchestrator.py`, no `warm_pool.py`, no tmux, no `claude` invocations. Design-first means files only; the only python you run is read-only extraction (Move 4) and the verification block.
- **Style:** specs mirror stability-1's register — terse, numbered sections, no marketing prose. Ticket JSONs mirror the newest `done/` ticket field-for-field.
- **Prefer HITL over guessing** on anything that smells like a David taste call (job count outside 4–6, a sixth machinery leg, relocating the suite) — that's what `needs-decision/` is for.
- **The rabbit hole:** trying to compute real numeric baselines from the single 2026-07-03 transcript. Don't. One worked extraction example proves the fields exist; actual baselines come from the supervised capture run (follow-on ticket, RUNBOOK). Envelope min/max values in SCHEMA.md are schema, not data — leave them as placeholders with a `captured_at: null` convention.
