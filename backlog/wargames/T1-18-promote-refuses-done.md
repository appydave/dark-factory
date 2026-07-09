# T1-18 — promote refuses a done ticket (no re-injecting completed work)

| field | value |
|---|---|
| ticket | wg-t1-18-promote-refuses-done |
| track / size / priority | T1 Engine / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-09, from the T1-14 re-promote crash incident |

## Mission

`bin/promote-wargame.py` only refuses a ticket that's already in `queue/` (the `dest.exists()`
check). It does NOT check `done/` — so `promote-wargame <ID>` happily re-injects a completed
ticket back into the queue, which is what set up the T1-14 re-run crash (2026-07-08). This ticket
makes `promote()` refuse a ticket already in `done/` unless `--force`, with a clear message
("already done — use --force to re-run"). Done looks like: promoting a done ticket exits non-zero
with an explanatory message and does NOT copy it into `queue/`; `--force` still allows a
deliberate re-run; promoting a fresh ticket is unchanged.

## Locked context
- Q4: sonnet Swagger dispatch, interactive claude only.
- `promote-wargame.py` already computes `state_sets()` → `(queued, running, done)`; the `done`
  set is already available in `promote()` — this is wiring an existing signal, not new machinery.
- Keep `--force` as the escape hatch (it already exists for unmet-deps / self-hosting overrides).

## Recon (verify before any work)
1. `grep -n "def promote\|state_sets\|dest.exists\|already queued\|force\|done" bin/promote-wargame.py`
   → confirm `promote(sid, staged, force=False)` already unpacks `_, _, done = state_sets()`
   (it's fetched but currently only used for dep-checking), and the `dest.exists()` "already
   queued" guard.
2. Confirm the ticket's runtime name: `promote()` maps `sid` (e.g. T1-14) → `j["ticket"]`
   (e.g. wg-t1-14-...); the `done` set is keyed on that same ticket name — so the check compares
   like with like.

## Moves
### Move 1 — Add the done-guard
- **Do:** In `promote()`, after resolving the ticket `j` and before the `dest.exists()` check,
  add:
  ```python
  if j["ticket"] in done and not force:
      sys.exit(f"{sid} ({j['ticket']}) is already in done/ — use --force to deliberately re-run.")
  ```
  (place it alongside the existing self-hosting / unmet-deps `--force` guards, same idiom.)
- **Expect:** `promote-wargame <a-done-id>` exits with that message, queue unchanged.
- **Failure signal:** the `done` set is keyed differently from `j["ticket"]` (e.g. filename vs
  ticket-name) so the membership test never matches.
- **Counter-move:** normalize both sides to the ticket-name (strip `.json`); Recon 2 confirms the
  keying — fix the comparison to match, don't ship a guard that never fires.

### Move 2 — Prove it
- **Do:** `python3 bin/promote-wargame.py T1-14` (a known-done ticket) → expect the refusal, exit
  1, and `ls engine/store/queue/` shows no new wg-t1-14. Then `--force` → it does promote (then
  remove it from queue/ to leave state clean, OR just confirm the message path without forcing).
- **Expect:** refused without --force; allowed with.
- **Failure signal:** it still promotes a done ticket.
- **Counter-move:** → Move 1 counter-move (keying mismatch).

### Move 3 — Self-report, commit, push
- **Do:** results JSON + commit `fix(promote): refuse re-promoting a done ticket without --force (wg-t1-18)`.

## Assumptions ledger
1. `state_sets()`'s `done` set is keyed on `j["ticket"]` (ticket-name) — Recon 2 verifies; if it's
   keyed on filename, normalize (Move 1 counter-move).
2. `--force` is the right escape hatch (consistent with the existing self-hosting/deps overrides).
   If David wants done-tickets to require a distinct flag, note it — don't block.

## Abort conditions
- **A1 — promote.py has been substantially rewritten** (no `state_sets`/`promote(force=...)`
  shape). Park to needs-decision/ with the observed structure.

## Verification
```bash
python3 -c "import ast; ast.parse(open('bin/promote-wargame.py').read()); print('parses')"
python3 bin/promote-wargame.py T1-14 2>&1 | grep -qi "already in done" && echo "✓ refuses done"
ls engine/store/queue/ | grep -qi t1-14 && echo "✗ leaked into queue" || echo "✓ queue clean"
grep -n "already in done\|in done and not force" bin/promote-wargame.py   # guard present
```
Negative: promoting a genuinely-ready ticket still works (`--list` unaffected); `--force` path
still promotes.

## Executor notes
- Scope fence: `bin/promote-wargame.py` `promote()` only. Don't touch `--list`/`--next`/status
  rendering.
- Rabbit hole: adding a whole state-machine of allowed transitions. Don't — it's one membership
  check against a set that's already computed three lines up.
- Run the Verification block yourself before self-reporting (no auto-verify yet).
