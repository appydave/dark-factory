# T1-20 — Reap settles a verify-fail promptly (retry-with-findings, don't spin)

| field | value |
|---|---|
| ticket | wg-t1-20-reap-settles-verify-fail |
| track / size / priority | T1 Engine / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-11, from the T1-16 live wedge (verify failed → engine spun ~30min re-running verify every 3s) |

## Mission

When `verify()` FAILS at reap, the orchestrator does **not** settle the ticket — it spins.
`engine/orchestrator.py` reap branch (≈934-942):
```python
else:  # verify failed
    print(f"[verify]   ticket {tid}: artifact present but verification FAILED: {findings}")
    if time.time() - a["started"] > worker_timeout:      # ONLY exit after 30 min
        record_verdict(... "failed(verify)" ...); settle(tid, a)
    # else: nothing — loop re-runs the FULL verify() next poll, every POLL=3s
```
`verify()` re-runs the ticket's `## Verification` bash checks **every 3s** until
`started + worker_timeout` (1800s). The result is **deterministic** — the artifact and code are
static after the worker goes idle — so re-running it hundreds of times cannot change the verdict.
Proven live 2026-07-11 (T1-16): verify failed, the engine printed the identical failure dozens of
times and wedged for ~30 minutes, holding the worker hostage and drowning the log. Two defects:
1. **Spin** — a deterministic verify-fail is re-run every poll instead of being decided once.
2. **No retry** — a verify-fail gets ZERO re-dispatch, unlike the timeout path which re-queues with
   findings up to MAX_RETRY. The worker never gets the engine's independent findings to fix its work.

Done looks like: a verify-fail is decided on the FIRST detection — re-dispatch the ticket with the
engine's findings appended (retry, up to MAX_RETRY), and only after retries are exhausted settle it
as `failed(verify)`. No re-running verify() every poll; the worker is freed immediately, not in 30
minutes; the log shows one FAILED line per attempt, not hundreds.

## Locked context
- Q4: sonnet Swagger dispatch, interactive claude only.
- Do NOT change the *verdict* logic (`verify()` / `verify_wargame` from wg-t1-15) — this is about
  what the reap loop DOES with a fail, not how the fail is judged.
- Keep `record_verdict()` (wg-t1-16) as the single write-site; add the retry+settle transitions
  through it.
- Retry semantics must mirror the existing timeout retry path (re-queue, bump `retries[tid]`,
  reboot/clear the worker) so there's ONE retry idiom, not two.

## Recon (verify before any work)
1. `sed -n '924,975p' engine/orchestrator.py` → confirm the fail branch keys on `a["started"]` and
   does nothing until worker_timeout; confirm the timeout path (≈966-971) is the retry idiom to
   mirror (re-queue + `retries[tid]` + reboot).
2. `grep -n "MAX_RETRY\|retries\[" engine/orchestrator.py` → how retry count is tracked/capped.
3. Confirm verify() is a pure read of static state (no side effects), so caching the first verdict
   for an attempt is safe.

## Moves
### Move 1 — Decide the verify-fail on first detection
- **Do:** in the `else` (verify failed) branch, stop gating settle on `started > worker_timeout`.
  On the first fail for this attempt:
  - if `retries[tid] < MAX_RETRY`: record `failed(verify)` interim (embed=False), append the
    engine's `findings` to a re-dispatch prompt, re-queue the ticket, bump `retries[tid]`, and
    reboot/clear the worker — mirroring the timeout retry path so the worker gets a fresh, clean
    attempt WITH the engine's independent findings.
  - else (retries exhausted): `record_verdict(... "failed(verify)" ...)`, `settle(tid, a)`, emit a
    `job.failed` (or `job.completed` result="failed(verify)") event, free the worker.
- **Expect:** one FAILED line per attempt; worker freed at once; ticket ends `failed(verify)` after
  MAX_RETRY, or `done` if a retry fixes it.
- **Failure signal:** re-dispatching re-runs verify against the SAME stale artifact and loops
  attempts without progress.
- **Counter-move:** the re-dispatch must hand the worker the findings + instruct a real re-do
  (clear context, re-read the ticket); if the artifact is unchanged between attempts, that's a
  genuine `failed(verify)` — let MAX_RETRY bound it.

### Move 2 — Don't re-run verify() every poll
- **Do:** ensure verify() runs ONCE per (tid, attempt). If Move 1 re-dispatches or settles on first
  detection, this falls out naturally (the ticket leaves `running/`). Guard against any path that
  would re-enter verify for the same attempt.
- **Expect:** verify's bash checks execute once per attempt, not once per 3s poll.
- **Counter-move:** if the loop structure makes single-eval awkward, memoize `verified[(tid,attempt)]`.

### Move 3 — Prove it
- **Do:** dispatch a throwaway ticket whose `## Verification` deliberately fails (e.g. `grep -q
  NONEXISTENT`). Confirm from the log: verify runs once per attempt, the ticket re-dispatches with
  findings up to MAX_RETRY, then settles `failed(verify)` and frees the worker — no 30-minute spin,
  no repeated identical FAILED blocks.
- **Expect:** total FAILED lines ≈ (MAX_RETRY+1), not hundreds; worker released in seconds.
- **Counter-move:** use a `wg-t1-20-selftest` id and clean it from the store after.

### Move 4 — Self-report, commit, push
- **Do:** results JSON + commit `fix(engine): reap settles a verify-fail promptly (retry-with-findings, no spin) (wg-t1-20)`.

## Assumptions ledger
1. verify() is side-effect-free, so deciding on first eval is safe — verify in Recon 3.
2. The timeout retry path is the canonical retry idiom to mirror — verify at ≈966-971.

## Abort conditions
- **A1 — retry-on-verify-fail is undesirable** (e.g. a fail should NEVER re-dispatch, only settle):
  park to needs-decision/ with both options (retry-with-findings vs settle-immediately) and the
  trade-off, since this is a policy call, not a pure bug.

## Verification
```bash
python3 -c "import ast; ast.parse(open('engine/orchestrator.py').read()); print('parses')"
grep -n "failed(verify)" engine/orchestrator.py                          # settle path present
# the anti-spin guard: verify-fail no longer gates settle purely on started>worker_timeout
grep -n "started.*worker_timeout" engine/orchestrator.py                 # this old spin-gate should be gone/changed
grep -n "retries\[tid\].*MAX_RETRY\|record_verdict" engine/orchestrator.py # retry idiom wired to verify-fail
```
Behavioural (the real gate): a deliberately-failing throwaway ticket produces ~MAX_RETRY+1 FAILED
lines and frees the worker in seconds — NOT a 30-minute spin of identical FAILED blocks. Negative: a
verify-PASS path (the happy path) is unchanged (`git diff` touches only the fail branch); wg-t1-15
verdict logic and wg-t1-16 record_verdict are not modified beyond adding the retry/settle calls.

## Executor notes
- Scope fence: `engine/orchestrator.py` reap loop verify-fail branch (≈934-942) only, mirroring the
  existing timeout retry path. Do NOT touch verify()/verify_wargame (verdict logic) or the
  happy-path commit.
- Rabbit hole: building a general retry/backoff policy engine. Don't — reuse the ONE existing retry
  idiom (re-queue + retries[tid] + reboot) the timeout path already uses.
- Run this war game's Verification block yourself before self-reporting done.
