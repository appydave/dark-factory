# T1-15 — Independent re-verification at reap (the Swagger discipline)

| field | value |
|---|---|
| ticket | wg-t1-15-independent-reverify-at-reap |
| track / size / priority | T1 Engine / M / high |
| executor | sonnet Swagger via engine (once T1-14 lands) |
| depends_on | wg-t1-14-worker-timeout-activity-reset (long tickets must be able to finish first) |
| authored | 2026-07-08, from BMAD-Swagger research (research/bmad-pattern-mining/bmad-machinery-pattern.md) |

## Mission

Today the engine reaps mostly on `artifact_ok()` (does `results/<ticket>.json` exist) plus a
`VERIFIERS` registry that has ~1 real entry — so for almost every ticket, "done" is the worker's
own self-report. BMAD Swagger's proven discipline (71 runs, caught a real degraded report on
story 15.4) is the opposite: **never trust the worker's self-report — independently re-derive the
verdict from primary evidence before advancing state.** This ticket makes the engine's reap step
run each ticket's own `## Verification` block (the war games already carry executable checks +
negative checks) and cross-check `git diff --stat`, exit codes, and named artifacts against what
the worker claimed — passing only when the independent evidence agrees. Done looks like: reap
executes a ticket's verification commands, compares to the worker's `results` claim, and marks
`done` only on agreement; a mismatch (claimed done, evidence disagrees) marks `failed(verify)`
with the findings recorded — turning the war games' negative-checks into enforced gates instead of
hopeful prose.

## Locked context
- Q4: runs as a sonnet Swagger dispatch. Interactive claude only.
- Extends the existing `VERIFIERS` registry + `generic` declarative DSL — do NOT replace it;
  add a war-game-aware verifier that reads the `## Verification` fenced block from the ticket's
  referenced `backlog/wargames/<ID>.md`.
- Never edit the worker's produced artifacts to make them pass — verify only, never "fix to green".

## Recon (verify before any work)
1. `grep -n "def verify\|VERIFIERS\|artifact_ok\|def commit\|def settle\|verify_kind\|verify_spec" engine/orchestrator.py`
   → map the current reap path: `artifact_ok()` gate → `verify()` (registry dispatch) → `commit()`
   + `settle()`. Confirm where a new verifier hooks in.
2. `sed -n '/VERIFIERS *=/,/}/p' engine/orchestrator.py` → see the registry shape + the `generic`
   check DSL (`CHECK_REGISTRY`: file_exists/json_parses/must_contain/git_commit_present/script/command).
3. Pick 3 landed war-game tickets (e.g. T1-04 done) and confirm their `## Verification` blocks are
   fenced ```bash blocks with runnable commands + `git diff --stat` negative checks. That block is
   the machine-readable spec this ticket consumes.
4. Confirm a ticket JSON references its war game (the `source` / `prompt` path to
   `backlog/wargames/<ID>.md`) so the verifier can locate the verification block.

## Moves
### Move 1 — Extract the verification block from a war game
- **Do:** Add a function that, given a ticket, resolves its `backlog/wargames/<ID>.md`, extracts
  the fenced commands under `## Verification` (positive + negative), and returns them as a check list.
- **Expect:** for T1-04 it returns its grep/test/`git diff --stat` lines.
- **Failure signal:** war games vary in block formatting; extraction misses some.
- **Counter-move:** define a strict contract (checks live in ```bash fences under `## Verification`);
  tickets whose block doesn't parse fall back to today's behaviour + a logged warning (never
  silently pass).

### Move 2 — Run the checks as the reap verifier
- **Do:** Register `verify_kind: "wargame"` (and/or auto-apply when a war game exists). Run each
  extracted command in the repo; a non-zero exit or a failed negative check = verify fail. Capture
  outputs into the findings.
- **Expect:** a ticket whose worker really did the work passes; a ticket where the worker skipped a
  step or touched a forbidden file fails on the negative check.
- **Failure signal:** a check is destructive or has side effects.
- **Counter-move:** war-game verification blocks are read-only by authoring rule; if one isn't,
  that's a war-game defect — skip that command, log it, flag for the T8 truth pass. Never run an
  editing command as a "check".

### Move 3 — Cross-check the worker's claim
- **Do:** Compare the independent verdict to the worker's `results/<ticket>.json` `status`. Log
  BOTH. On disagreement (worker said done, evidence says fail) record `verdict_source: engine`,
  mark `failed(verify)`, and — mirroring Swagger's degraded-report catch — note "worker self-report
  contradicted by independent evidence" in the ticket.
- **Expect:** agreement is the norm; disagreements are loud and rare.
- **Failure signal:** frequent disagreement → either the extractor is wrong or workers routinely
  over-claim.
- **Counter-move:** if disagreement is extractor noise, fix Move 1; if workers genuinely over-claim,
  that's the finding this ticket exists to surface — report the rate.

### Move 4 — Self-report, commit, push
- **Do:** results JSON + commit `feat(engine): reap re-verifies from the war game's own checks, not the worker's word (wg-t1-15)`.

## Assumptions ledger
1. War games carry runnable `## Verification` blocks — true of the 57 authored 2026-07-06. Tickets
   without one fall back to today's reap + a warning (Move 1 counter-move).
2. Read-only verification commands — authoring rule; violations are war-game defects, logged not run.

## Abort conditions
- **A1 — the reap path has been refactored** away from `artifact_ok → verify → commit` such that
  this hook point is gone. Park to `needs-decision/` with the observed new shape.
- **A2 — scope creep toward "auto-fix to green"**: if you find yourself editing a worker's artifact
  to pass a check, stop and park. This ticket verifies; it never repairs.

## Verification
```bash
grep -n "wargame" engine/orchestrator.py                       # new verifier registered
python3 -c "import ast; ast.parse(open('engine/orchestrator.py').read()); print('parses')"
# behavioural: a ticket with a deliberately-unmet negative check reaps as failed(verify), not done
```
Negative: the `generic`/`constellation-4-apps` verifiers still work (existing tickets unaffected);
no worker artifact was modified by the reap step (`git diff` within a verify run is empty).

## Executor notes
- Scope fence: `engine/orchestrator.py` (verifier registry + extractor) and its docs. Do not touch
  claim/dispatch/reboot logic (that's T1-14) or worker artifacts.
- Prefer HITL over guessing if the reap path moved (A1).
- Rabbit hole: building a general test-runner/DSL. Don't — reuse the war games' existing fenced
  commands; you're an executor of blocks that already exist, not a framework author.
