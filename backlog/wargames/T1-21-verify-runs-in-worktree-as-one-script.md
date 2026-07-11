# T1-21 — Verify runs the block as ONE script, from the worker's worktree

| field | value |
|---|---|
| ticket | wg-t1-21-verify-runs-in-worktree-as-one-script |
| track / size / priority | T1 Engine / M / high |
| executor | sonnet Swagger via engine — **RUN AT POOL=1 ONLY** (see Abort A1) |
| depends_on | none (it fixes what wg-t1-19 exposed) |
| authored | 2026-07-11, from the T3-03+T3-04 parallel run — both tools built fine, both false-failed |

## Mission

`verify_wargame` (engine/orchestrator.py) runs a war game's `## Verification` block **wrong in two
ways**, both proven live 2026-07-11 when T3-03 and T3-04 built perfect tools in their worktrees and
BOTH false-failed:

1. **Line-by-line execution.** Each check line runs as its OWN subprocess, so state set on one line
   is gone on the next — `DF=/…` on line 1 is empty by line 2 (`$DF/tools/x.py` → `/tools/x.py` →
   not found), and `T=$(mktemp)`, heredocs (`cat <<EOF`), and `cd` all break the same way.
2. **Wrong working directory (the deadlock).** In the wg-t1-19 worktree model the worker builds and
   commits its artifact **inside its worktree** (`.worktrees/df-worker-N/`). But verify runs from
   the **main REPO tree**, where the artifact does not exist — consolidation to main only happens
   *after* a passing verify. So a worktree-isolated, file-creating job can **never** pass:
   verify → "file not found" → fail → never consolidates. Both T3 tools sat committed on
   `wg/worker-N` branches, invisible to a verify looking at main, and had to be rescued by hand.

Done looks like: the ENTIRE `## Verification` block runs as **one script** (so vars/heredocs/`cd`
persist), with **cwd = the worker's worktree** (so it sees the artifact the worker just built),
BEFORE consolidation. Then consolidate-to-main happens on a real pass. A var-using, file-creating
verification block passes when the tool is genuinely built — no hand-rescue.

## Locked context
- Do NOT change the **verdict** logic (pass = all-checks-exit-0; the independent-re-verify intent of
  wg-t1-15). Only change HOW the block is executed (one script) and WHERE (worktree cwd).
- Keep wg-t1-16 `record_verdict` + wg-t1-20 retry/settle exactly as they are.
- Pool=1 (no worktree) must still work: cwd falls back to REPO when the worker has no worktree.

## Recon (verify before any work)
1. `grep -n "def verify_wargame\|def run_check\|subprocess\|## Verification\|checks\b" engine/orchestrator.py`
   → find where the block's lines are extracted and how each is executed (the per-line subprocess).
2. `grep -n "worktree\|\.worktrees\|cwd=\|df-worker" engine/orchestrator.py engine/warm_pool.py`
   → find how a worker's worktree path is known at reap time (wg-t1-19 added it), so verify can cd there.
3. Confirm the deadlock: a file created only in `.worktrees/df-worker-N/` is absent from the main
   tree during verify (that's the whole bug).

## Moves
### Move 1 — Run the whole block as ONE script
- **Do:** instead of running each extracted line as its own subprocess, write the full fenced
  `bash` block to a temp file (or `bash -c` the joined block) and run it once, capturing combined
  output + a single exit status. A non-zero exit (or a per-check failure the block itself reports)
  is the fail. Preserve the current "which check failed" detail in findings if feasible (e.g. run
  with `set -x` or keep the per-line report but in ONE shell so state persists).
- **Expect:** `DF=…`, `T=$(mktemp)`, heredocs, and `cd` now work across the block.
- **Counter-move:** if per-line findings are hard to keep, at minimum surface the block's stdout+
  stderr + exit code so a human sees what failed.

### Move 2 — Run it from the worker's worktree
- **Do:** set the verify subprocess cwd to the worker's worktree dir (from Recon 2) when it has one,
  else REPO. So the artifact the worker built+committed in its worktree is visible to verify.
- **Expect:** `test -f tools/x.py` (relative) and repo-relative checks see the worker's real output.
- **Counter-move:** if the worktree path isn't threaded to the reap point, thread it via the active
  worker record `a["worker"]` (it knows its cwd from wg-t1-19).

### Move 3 — Prove it
- **Do:** a throwaway ticket whose `## Verification` block BOTH uses a variable across lines AND
  checks a file the "worker" creates — run it (pool=1 is fine for the proof) and confirm it PASSES
  when the file exists and FAILS when it doesn't. Then note that pool=2 worktree runs now verify
  against the worktree (the T3-03/T3-04 scenario).
- **Expect:** var-using + file-creating blocks pass honestly; no "file not found" when the file was
  built in the worktree.
- **Counter-move:** clean up the throwaway from the store.

### Move 4 — Self-report, commit, push
- **Do:** results JSON + commit `fix(engine): verify runs the block as one script from the worker's worktree (wg-t1-21)`.

## Assumptions ledger
1. The worker's worktree path is available at the reap/verify point (wg-t1-19 introduced it) —
   verify in Recon 2; if not, thread it through `active[tid]`.
2. Running the block as one script does not change the pass/fail verdict for blocks that already
   passed line-by-line (they're a strict subset) — spot-check one existing passing block.

## Abort conditions
- **A1 — this ticket must run at POOL=1.** Running it at pool=2 would build the fix inside a
  worktree and hit the very bug it fixes (verify can't see the worktree). Dispatch it single-worker.
- **A2 — verify_wargame turns out to already run as one script** (someone fixed Move 1 already):
  then only Move 2 (worktree cwd) remains — do that and note it.

## Verification
```bash
python3 -c "import ast; ast.parse(open('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/orchestrator.py').read()); print('parses')"
grep -q "def verify_wargame" /Users/davidcruwys/dev/ad/apps/dark-factory/engine/orchestrator.py && echo "verify_wargame present"
grep -qE "worktree|a\[.worker.\].*cwd|\.cwd" /Users/davidcruwys/dev/ad/apps/dark-factory/engine/orchestrator.py && echo "worktree-cwd wiring present"
grep -qE "bash.*-c|tempfile|NamedTemporary|write.*\.sh|\.executable" /Users/davidcruwys/dev/ad/apps/dark-factory/engine/orchestrator.py && echo "one-script execution present"
```
(NB: every check above is SELF-CONTAINED — absolute paths, no `$VAR` reused across lines, no
heredoc, no `cd` — because until THIS ticket lands, the engine still runs each line separately.
That is the exact trap this ticket removes; its own proof must not fall into it.)
Behavioural: the Move-3 throwaway (var across lines + file-creating) PASSES when the file exists.
Negative: a pool=1 ticket that passed before still passes; wg-t1-15 verdict logic + wg-t1-20
retry/settle untouched.

## Executor notes
- Scope fence: `engine/orchestrator.py` `verify_wargame` (and its check-runner) — how the block is
  executed + the cwd. Do NOT touch the verdict derivation, record_verdict, or the retry/settle path.
- Rabbit hole: rewriting the whole reap loop. Don't — this is (a) run the block as one script and
  (b) point its cwd at the worktree.
- Run this war game's Verification block yourself before self-reporting done.
