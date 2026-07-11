# T1-19 — Worktree-per-worker isolation (make pool>1 safe for editing tickets)

| field | value |
|---|---|
| ticket | wg-t1-19-worktree-per-worker-isolation |
| track / size / priority | T1 Engine / L / high |
| executor | sonnet Swagger via engine (build); live pool=2 proof is ATTENDED — see Abort/notes |
| depends_on | none (pairs with T1-06 warm-pool-n2 — the two halves of safe parallelism) |
| authored | 2026-07-11, from the factory-console session — "run more than one ticket at a time" |

## Mission

Today `WarmPool.__init__` hands **every** worker the same working tree:
`WarmWorker(i+1, model, cwd, …)` with one `cwd=REPO`, and each boots `cd {REPO} && claude …`
(`engine/warm_pool.py:129-130`, `:83`). There is **no `git worktree`** anywhere — all N workers
edit, stage, and commit in the *same* repo tree. At `--pool 1` that's fine; at `--pool 2+` two
workers editing files at once **stomp each other**: interleaved edits, and the in-tree commit path
scoops up a neighbour's half-finished work. That is why the engine can *boot* up to CAP=3 workers
but can only safely *dispatch editing tickets one at a time*. This ticket removes that ceiling for
editing work: **each worker gets its own `git worktree`, so N workers can edit in parallel without
colliding, while the engine store stays the single shared coordination substrate.**

Done looks like: two workers dispatched at `--pool 2` each edit the *same* source file for
different tickets, both commits land cleanly on `main`, neither sees the other's uncommitted
changes, and the shared store (queue/running/done/audit) is read/written correctly by both.

## The one hard decision (make it in Move 0, don't skip it)

Isolate the **code**, keep the **store shared**. The store (`engine/store/…`) is the coordination
bus — orchestrator + all workers must see one copy. The orchestrator already addresses it by
**absolute path** (`STORE = os.path.join(...)` at module load, `cwd=REPO` on its own git calls), so
the orchestrator side needs no change. Only the *worker's* working tree moves. Pick the mechanism:

- **(A) `git worktree` per worker** — RECOMMENDED. `git worktree add <wt>/df-worker-N -b wg/worker-N`.
  Shares the one `.git` object store (cheap), isolated working tree per worker. Worker commits land
  on a per-worker branch; orchestrator consolidates to `main` at reap (fast-forward or cherry-pick).
- **(B) full clone per worker** — heavier (duplicate object store per worker), but dead-simple
  isolation and it mirrors the cross-machine model (T10-01). Fallback if worktree + shared-store
  path resolution proves too tangled.

Recommend **(A)**. If Recon shows the store is *only* reachable via the working tree (it is not —
it's an abspath), fall back to (B) and record why.

## Locked context
- Q4: sonnet Swagger dispatch, interactive `claude` only; `safety_check()` still governs.
- CAP=3 stays (the 429 wall) — this ticket does not raise the pool cap, it makes the existing cap
  *usable* for editing tickets.
- The **store stays in the main REPO tree**, addressed absolutely. Do NOT move `engine/store/` into
  worktrees — that would fork the coordination bus and is the failure mode, not the goal.
- Append-only store idiom unchanged.

## Recon (verify before any work)
1. `grep -n "cwd" engine/warm_pool.py` → confirm `cwd` flows `WarmPool → WarmWorker → boot()`'s
   `cd {self.cwd}` (one shared value today).
2. `grep -n "STORE\|REPO\|cwd=REPO\|os.path.join" engine/orchestrator.py | head` → confirm STORE is
   an **absolute** path set once, and the orchestrator's own git calls pass `cwd=REPO`. This is what
   lets the store stay shared while workers move.
3. `git worktree list` → confirm none exist yet (clean baseline).
4. Confirm the collision is real: two edits to one file from two shells in one tree race on
   `git add`/commit (the failure this removes).

## Moves
### Move 0 — Decide isolation mechanism (A worktree vs B clone)
- **Do:** confirm store-is-abspath (Recon 2). If yes → choose (A). Record the choice + evidence in
  the results JSON.
- **Failure signal:** store turns out to be resolved relative to cwd → (A) alone would fork it.
- **Counter-move:** switch to (B) full-clone, or make every worker export an absolute
  `DARK_FACTORY_STORE` the orchestrator honours.

### Move 1 — Per-worker worktree at pool boot
- **Do:** in `WarmPool.__init__`, give each worker its own working tree. Sketch:
  ```python
  # per worker i: <REPO>/.worktrees/df-worker-<i>, branch wg/worker-<i> off main
  wt = os.path.join(REPO, ".worktrees", f"df-worker-{i+1}")
  subprocess.run(["git", "worktree", "add", "-B", f"wg/worker-{i+1}", wt, "HEAD"], cwd=REPO, check=True)
  WarmWorker(i+1, model, cwd=wt, …)   # worker edits HERE, not in REPO
  ```
  `.worktrees/` goes in `.gitignore`. Pool size 1 may keep using REPO directly (fast path) or a
  single worktree for uniformity — pick and note it.
- **Expect:** `git worktree list` shows one tree per worker; each worker's `cd {cwd}` lands in its
  own tree.
- **Failure signal:** a stale `.worktrees/df-worker-N` from a prior run blocks `worktree add`.
- **Counter-move:** `git worktree remove --force` (or prune) each expected path before add;
  idempotent boot.

### Move 2 — Consolidate worker commits to main at reap; keep store shared
- **Do:** the worker commits on its `wg/worker-N` branch inside its worktree. At reap, the
  orchestrator consolidates that commit onto `main` (fast-forward if linear, else cherry-pick the
  worker's HEAD). Store writes (running→done, audit, events) continue to use the **absolute** store
  path and are unaffected by the worker's cwd.
- **Expect:** the reaped ticket's code change appears on `main`; the store transition is recorded
  exactly as at pool=1.
- **Failure signal:** two workers' branches touch the same file and the second consolidation
  conflicts.
- **Counter-move:** consolidate serially in the reap loop (the orchestrator is single-threaded at
  the reap point); on a real content conflict, park that ticket to `needs-decision/` with the diff
  rather than force-merging.

### Move 3 — Teardown returns worktrees cleanly
- **Do:** on `--teardown` (and on boot, defensively), `git worktree remove` each worker tree and
  delete its `wg/worker-N` branch if merged. Leave `main` clean.
- **Expect:** after a run, `git worktree list` shows only the main tree; no orphan branches.
- **Failure signal:** unmerged worker branch blocks removal.
- **Counter-move:** `--force` remove the tree (commit already consolidated in Move 2); keep the
  branch only if its HEAD isn't yet on main, and log it.

### Move 4 — Prove it
- **Do:** isolated proof that does NOT require booting the live pool (keeps this dispatchable):
  create two worktrees by hand, have each append a distinct line to the *same* file, commit on each
  branch, consolidate both to main → both lines present, no clobber, clean tree. THEN, if running
  attended, a real `--pool 2` drain of two small editing tickets (e.g. two throwaway
  `wg-t1-19-selftest-{a,b}`) confirms end-to-end.
- **Expect:** both changes survive; store shows both tickets reaped.
- **Counter-move:** if the live pool=2 proof needs an attended run (it reboots the pool — overlaps
  T1-06 self-hosting), stop at the isolated proof and hand the live-N proof to an attended session,
  noting it explicitly.

### Move 5 — Self-report, commit, push
- **Do:** results JSON (record the Move 0 decision + whether live-N was proven or deferred) +
  commit `feat(engine): per-worker git worktrees — pool>1 can edit in parallel without collision (wg-t1-19)`.

## Assumptions ledger
1. Store is reached by absolute path, so it stays shared across worktrees — verified in Recon 2;
   if false, Move 0 counter-move (full clone or explicit STORE env) applies.
2. The reap loop is single-threaded at the consolidation point, so serial merge-to-main is safe —
   verify at the `commit(tid)` call site.

## Abort conditions
- **A1 — store turns out to be cwd-relative** in a way (A) can't isolate → switch to (B) full clone,
  or park to needs-decision/ with the coupling documented.
- **A2 — live pool=2 proof requires killing/rebooting the running engine** (self-hosting hazard,
  same class as T1-06): do the isolated proof (Move 4 first half) and DEFER the live-N proof to an
  attended run — do not self-murder the dispatching engine.

## Verification
```bash
python3 -c "import ast; ast.parse(open('engine/warm_pool.py').read()); ast.parse(open('engine/orchestrator.py').read()); print('parses')"
grep -n "git.*worktree\|\.worktrees\|worktree add\|worktree remove" engine/warm_pool.py engine/orchestrator.py   # isolation present
grep -n "worktrees" .gitignore                                                                                  # not tracked
git worktree list                                                                                               # after teardown: only the main tree
```
Behavioural (isolated, no live pool): two hand-made worktrees each edit the SAME file on their own
branch → both commits consolidate to `main` with both changes present and a clean tree (Move 4
first half). Negative: pool=1 dispatch still reaps exactly as before; the shared store
(queue/running/done/audit) is read/written by the worker despite its cwd being a worktree.

## Executor notes
- Scope fence: `engine/warm_pool.py` (per-worker worktree at boot/teardown) + `engine/orchestrator.py`
  (consolidate worker commit to main at reap) + `.gitignore` (`.worktrees/`). Do NOT move the store,
  do NOT raise CAP, do NOT touch the reap *decision* logic (artifact_ok/verify).
- Rabbit hole: building a full multi-tree merge queue / conflict resolver. Don't — consolidation is
  serial in the single-threaded reap loop; a genuine conflict parks to needs-decision/, it is not
  auto-resolved.
- Self-host caveat: the live `--pool 2` end-to-end proof reboots the worker pool (T1-06 class) —
  run that half attended; the isolated two-worktree proof is dispatchable and is the gate.
- Run this war game's Verification block yourself before self-reporting done.
