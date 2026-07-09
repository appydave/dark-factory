# T1-17 — Guard commit()'s rename (one stale ticket must not crash the engine)

| field | value |
|---|---|
| ticket | wg-t1-17-commit-rename-guard |
| track / size / priority | T1 Engine / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-09, from the T1-14 re-promote crash incident |

## Mission

`commit()` in `engine/orchestrator.py` is a bare `os.rename(running/tid → done/tid)` with no
existence check. When the `running/` file is already gone (a re-run of a done ticket, a
double-commit, a race), the rename raises `FileNotFoundError` and takes the **entire engine
process** down — every other in-flight ticket dies with it. Proven live 2026-07-08: re-promoting
an already-`done` T1-14 crashed the whole orchestrator. This ticket makes commit idempotent and
crash-safe: if `running/tid` is missing but `done/tid` already exists, treat it as already
committed and move on; if both are missing, log a loud warning and drop that one ticket — never
let one ticket's file-state anomaly kill the kernel. Done looks like: re-running/committing a
ticket whose `running/` file is gone logs and continues instead of raising; a normal commit is
unchanged.

## Locked context
- Q4: sonnet Swagger dispatch, interactive claude only.
- Do NOT change the reap *decision* logic (artifact_ok → verify → commit) — only make the file
  move defensive.
- Append-only store idiom; don't delete done/ artifacts.

## Recon (verify before any work)
1. `grep -n "def commit\|os.rename\|def settle\|del active" engine/orchestrator.py` → confirm
   `commit()` is the bare `os.rename(RUN/tid → DONE/tid)` (≈line 499) and find `settle()` (does
   the `del active[tid]` cleanup, ≈557).
2. `grep -n "commit(tid)" engine/orchestrator.py` → the single call site in the reap branch.
3. Confirm the crash mode: `python3 -c "import os; os.rename('engine/store/running/NOPE','engine/store/done/NOPE')"` → FileNotFoundError (the unguarded failure this ticket removes).

## Moves
### Move 1 — Make commit idempotent
- **Do:** Rewrite `commit(tid)` to guard the move:
  ```python
  def commit(tid):
      src = os.path.join(RUN, tid); dst = os.path.join(DONE, tid)
      if not os.path.exists(src):
          if os.path.exists(dst):
              return  # already committed — idempotent, not an error
          print(f"[reap]     WARN commit({tid}): neither running/ nor done/ present — skipping", flush=True)
          return
      os.rename(src, dst)
  ```
- **Expect:** a missing `running/tid` no longer raises; a normal commit still moves the file.
- **Failure signal:** callers rely on commit raising to signal failure.
- **Counter-move:** grep the call site — commit's result isn't inspected (fire-and-forget in the
  reap branch), so returning silently is safe. If a caller DID depend on the exception, make it
  return a bool and check it there.

### Move 2 — Prove it
- **Do:** Unit-style check: call `commit("does-not-exist.json")` → returns without raising, logs
  the WARN. Then a real commit (create a dummy running/ file, commit, confirm it's in done/).
- **Expect:** first is a no-op+warn; second moves the file.
- **Failure signal:** the dummy pollutes the real store.
- **Counter-move:** use a throwaway ticket id like `wg-t1-17-selftest.json`, clean it up after.

### Move 3 — Self-report, commit, push
- **Do:** results JSON + commit `fix(engine): commit() is idempotent — a missing running/ file no longer crashes the kernel (wg-t1-17)`.

## Assumptions ledger
1. commit's return value is unused by callers (fire-and-forget) — verified in Recon 2; if not,
   Move 1 counter-move returns a bool instead.

## Abort conditions
- **A1 — commit() has already been refactored** into a multi-step transaction. Park to
  needs-decision/ with the observed shape rather than guessing.

## Verification
```bash
python3 -c "import ast; ast.parse(open('engine/orchestrator.py').read()); print('parses')"
grep -n "already committed\|idempotent\|os.path.exists(src)" engine/orchestrator.py   # guard present
# behavioural: committing a non-existent ticket returns cleanly (no traceback)
```
Negative: a normal commit still moves running/→done/ (verify with the Move 2 dummy); reap
decision logic (artifact_ok/verify) untouched (`git diff` shows only commit()).

## Executor notes
- Scope fence: `engine/orchestrator.py` `commit()` only (+ its call site if Move 1 counter-move
  applies). Do NOT touch claim/lease renames, settle's `del active`, or verify.
- Rabbit hole: turning the store into a transactional DB. Don't — this is a 5-line existence
  guard on one rename.
- Run the war game's Verification block yourself before self-reporting done (T1-15 auto-verify
  isn't built yet).
