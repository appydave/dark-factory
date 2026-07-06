# T10-02 — Cross-machine HALT broadcast

| field | value |
|---|---|
| ticket | wg-t10-02-fleet-halt-broadcast |
| track / size / priority | T10 Fleet / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The kill switch (`engine/halt.py`, `docs/kill-switch-spec.md`) is per-machine: halting the
factory on the M4 Mini does nothing to a dark-factory clone on Roamy. Per decisions.md Q8 the
fleet scope is **+ Roamy**, so a fleet-wide halt must reach Roamy's engine too. The mechanism
is deliberately the dumbest one that honors the existing convention: HALT is a flag file whose
*existence* is the whole protocol, so a broadcast is just "write/remove the same file on each
fleet machine over SSH" — no daemon, no Switchboard dependency (the Switchboard state plane is
a deferred fork, T1-11; do NOT build on it). Done looks like: (1) Roamy's clone is synced so
its engine code actually checks HALT (verified at authoring: Roamy's `engine/` predates
`halt.py` entirely), (2) `engine/halt.py` gains a `--fleet` flag on `halt`/`resume`/`status`
that broadcasts by direct SSH file write/remove to the machines in a new `engine/fleet.json`,
(3) a live round-trip is proven (halt --fleet → flag present on both machines → resume --fleet
→ flag absent on both), (4) `docs/kill-switch-spec.md` §2+§6 are updated to match, and (5)
everything is committed + pushed and Roamy is re-pulled so the new halt.py exists there too.
No flag file is left behind on either machine.

## Locked context

- decisions.md Q8: fleet scope is **+ Roamy** — cross-machine HALT is explicitly in scope;
  other machines (m2, jan, mary) are NOT.
- decisions.md Q3: Switchboard state-authority fork is **deferred** (T1-11) — this broadcast
  must not depend on Switchboard; SSH file-write only.
- decisions.md Q4: everything through the engine — sonnet-Swagger engine ticket.
- Spec globals: no `-p`/headless/SDK ever; interactive `claude` only; HALT/BACKOFF respected
  implicitly by the engine; no YLO/POEM work.
- `docs/kill-switch-spec.md` §5: HALT stops the *next* thing, never kills running work; §1:
  file existence is ground truth, JSON payload is informational only. The broadcast inherits
  both properties unchanged.
- `docs/comms-flow.md` §4 convention: state under a trusted repo path, never `/tmp` — the
  remote flag path is Roamy's own `engine/store/HALT`, same as local.

## Recon (verify before any work)

All paths absolute. Authoring-time state noted; docs lag code — trust only what you see.

1. **Local kill switch intact and factory not halted.**
   `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/halt.py && ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT 2>&1`
   → expect halt.py present, HALT absent ("No such file"). HALT present → the factory is
   halted; stop immediately, park per the engine's standing HALT rule (do not "helpfully"
   resume). halt.py missing → the engine changed shape since authoring → **Abort A1**.
2. **`--fleet` not already built.** `grep -n "fleet" /Users/davidcruwys/dev/ad/apps/dark-factory/engine/halt.py`
   → expect empty (authoring: halt.py is 136 lines, subcommands halt/resume/status, no fleet
   anything; `engine/fleet.json` does not exist). Non-empty → **Fork F3**.
3. **Roamy reachable with key auth.**
   `ssh -o BatchMode=yes -o ConnectTimeout=8 macbook-pro-m4 'echo ok; whoami; hostname'`
   → expect `ok` / `davidcruwys` / `Roamy`. (`~/.ssh/config` pins Host `macbook-pro-m4` →
   100.89.32.35, User davidcruwys — verified working from a subagent shell at authoring.)
   Timeout or "Could not resolve" → check `tailscale status | grep -i roamy` (fall back to
   `/Applications/Tailscale.app/Contents/MacOS/Tailscale status`); Roamy offline/asleep →
   **Fork F2**. `Permission denied (publickey)` → **Fork F2 Route B**.
4. **Roamy's clone state.**
   `ssh -o BatchMode=yes macbook-pro-m4 'cd ~/dev/ad/apps/dark-factory && git branch --show-current && git status --porcelain | head -20 && git log --oneline -1 && ls engine/halt.py 2>&1'`
   → authoring state: branch `main`, status clean, HEAD `2eae942` (an ancestor of local
   main), `engine/halt.py` **absent** ("No such file") — Roamy's engine predates the kill
   switch. Dirty tracked files or a non-main branch → **Fork F1**. halt.py already present →
   the sync already happened; skip Move 1, continue.
5. **Origin has the kill switch.**
   `cd /Users/davidcruwys/dev/ad/apps/dark-factory && git fetch origin -q && git cat-file -e origin/main:engine/halt.py && echo origin-has-halt`
   → expect `origin-has-halt` (verified at authoring). Missing → local halt.py was never
   pushed; push local main first (`git push origin main` — if rejected, `git pull --rebase`
   then push), re-check, then proceed. Still missing → **Abort A1**.
6. **Roamy's HALT absent too.**
   `ssh -o BatchMode=yes macbook-pro-m4 'ls ~/dev/ad/apps/dark-factory/engine/store/HALT 2>&1'`
   → expect "No such file". Present → someone halted Roamy deliberately; **Abort A2** (never
   clear another machine's HALT without a human decision).

## Moves

1. **Sync Roamy's clone so its engine respects HALT.**
   - **Do:** `ssh -o BatchMode=yes macbook-pro-m4 'cd ~/dev/ad/apps/dark-factory && git pull --ff-only origin main && ls engine/halt.py'`
   - **Expect:** fast-forward output, then `engine/halt.py` listed. (Authoring: Roamy HEAD is
     a clean ancestor of origin/main, so ff-only succeeds.)
   - **Failure signal:** `fatal: Not possible to fast-forward` (diverged) or merge-conflict
     text.
   - **Counter-move:** → **Fork F1**. If F1 routes to abort, do so before touching any code.

2. **Create `engine/fleet.json` — the broadcast target list.**
   - **Do:** write `/Users/davidcruwys/dev/ad/apps/dark-factory/engine/fleet.json`:
     ```json
     {
       "_comment": "Fleet HALT broadcast targets (wg-t10-02). Remotes only — the local store is always handled first, directly. ssh values must be BatchMode-able aliases/hosts from ~/.ssh/config or MagicDNS. Scope per decisions.md Q8: + Roamy only.",
       "machines": [
         {
           "name": "roamy",
           "ssh": "macbook-pro-m4",
           "store": "/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store"
         }
       ]
     }
     ```
   - **Expect:** `python3 -c "import json; print(json.load(open('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/fleet.json'))['machines'][0]['name'])"` prints `roamy`.
   - **Failure signal:** JSON parse error.
   - **Counter-move:** fix the syntax; this file is yours, no fork needed.

3. **Extend `engine/halt.py` with `--fleet`.**
   - **Do:** add a `--fleet` store_true flag to all three subparsers (`halt`, `resume`,
     `status`) and implement broadcast helpers. Contract (implement exactly; internals are
     yours):
     - `load_fleet()` → list of machine dicts from `engine/fleet.json`; missing or corrupt
       file → `[]` plus a one-line warning to stderr (the switch must never crash — same
       defensive rule as `is_halted()`).
     - All SSH calls: `subprocess.run(["ssh", "-o", "BatchMode=yes", "-o",
       "ConnectTimeout=8", m["ssh"], <remote-cmd>], capture_output=True, text=True,
       timeout=20)` — never interactive, never hangs the CLI.
     - `halt --fleet`: **local write FIRST** (local safety never waits on the network), then
       per machine pipe the same JSON payload — plus `"origin": "<local hostname>"` — via
       stdin to remote-cmd `mkdir -p '<store>' && cat > '<store>/HALT'`. Print one line per
       machine: `<name>: HALTED` or `<name>: FAILED (<first line of stderr>)`.
     - `resume --fleet`: local remove FIRST, then remote-cmd `rm -f '<store>/HALT' && echo
       removed`. Print `<name>: RESUMED` / `<name>: FAILED (...)`.
     - `status --fleet`: local status as today, then per machine remote-cmd
       `cat '<store>/HALT' 2>/dev/null || echo __ABSENT__`; print `<name>: RUNNING`,
       `<name>: HALTED since <ts> by <by>` (parse the JSON; unparseable-but-present still
       reads HALTED — existence is ground truth), or `<name>: UNREACHABLE`.
     - Exit codes: local action always applies; process exits `0` only if every remote also
       succeeded, else `1`. Without `--fleet`, behavior is byte-identical to today.
     - Do NOT modify `is_halted()`, `halt_info()`, `write_halt()`, `clear_halt()` signatures —
       orchestrator.py, warm_pool.py, wake.py and status.py import/read these.
   - **Expect:** `python3 /Users/davidcruwys/dev/ad/apps/dark-factory/engine/halt.py status`
     (no flag) still prints `RUNNING -- no HALT file present.`, and
     `python3 engine/halt.py halt --help` shows `--fleet`.
   - **Failure signal:** any exception, or changed no-flag output.
   - **Counter-move:** `git -C /Users/davidcruwys/dev/ad/apps/dark-factory checkout engine/halt.py`
     (it's tracked and was committed clean), re-apply more carefully. Second failure →
     **Abort A1**.

4. **Local-only regression check before touching the network.**
   - **Do:**
     ```bash
     cd /Users/davidcruwys/dev/ad/apps/dark-factory
     python3 engine/halt.py halt "wg-t10-02 local regression" --by wg-t10-02
     python3 engine/halt.py status --json
     python3 engine/halt.py resume
     python3 engine/halt.py status
     ```
   - **Expect:** halted:true JSON with reason `wg-t10-02 local regression`, then
     `RESUMED -> removed ...`, then `RUNNING -- no HALT file present.` — the pre-existing
     local path is untouched by your edit.
   - **Failure signal:** any deviation.
   - **Counter-move:** fix halt.py; if broken beyond one retry, restore via Move 3's
     counter-move and **Abort A1**. Never proceed to broadcast with a broken local switch.

5. **Live fleet round-trip (the proof).**
   - **Do:**
     ```bash
     cd /Users/davidcruwys/dev/ad/apps/dark-factory
     python3 engine/halt.py halt "wg-t10-02 fleet round-trip test" --by wg-t10-02 --fleet
     ssh -o BatchMode=yes macbook-pro-m4 'cat ~/dev/ad/apps/dark-factory/engine/store/HALT'
     ssh -o BatchMode=yes macbook-pro-m4 'cd ~/dev/ad/apps/dark-factory && python3 engine/halt.py status --json'
     python3 engine/halt.py status --fleet
     python3 engine/halt.py resume --fleet
     ssh -o BatchMode=yes macbook-pro-m4 'ls ~/dev/ad/apps/dark-factory/engine/store/HALT 2>&1'
     python3 engine/halt.py status --json
     ```
     Capture the full transcript to
     `/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t10-02-roundtrip.txt`
     (tee or copy-paste — it's the evidence artifact).
   - **Expect:** in order — `roamy: HALTED`; remote cat shows the JSON payload with
     `"reason": "wg-t10-02 fleet round-trip test"` and an `"origin"` field; **Roamy's own
     halt.py** reports `"halted": true` (proving the synced remote engine reads the broadcast
     flag); `status --fleet` shows local HALTED + `roamy: HALTED since ...`; resume prints
     `roamy: RESUMED`; remote ls says "No such file"; final local status `"halted": false`.
   - **Failure signal:** any step deviates — most critically, `resume --fleet` failing after
     `halt --fleet` succeeded (Roamy left halted by a test).
   - **Counter-move:** if resume's broadcast failed, retry the remote removal directly:
     `ssh -o BatchMode=yes macbook-pro-m4 'rm -f ~/dev/ad/apps/dark-factory/engine/store/HALT'`
     and re-verify absence. If SSH itself died mid-test → **Fork F2** (and the same manual
     `rm` attempt is mandatory before parking — never leave a test flag behind; if even that
     fails, say so explicitly in the park question, per **Abort A3**). Logic bugs in your
     `--fleet` code → fix, re-run Move 4 then Move 5 from the top.

6. **Update `docs/kill-switch-spec.md` to match reality.**
   - **Do:** two edits:
     (a) §2 CLI line — extend to
     `halt.py halt ["reason"] [--by <name>] [--fleet]`, `halt.py resume [--fleet]`,
     `halt.py status [--json] [--fleet]`, with one added sentence: `--fleet` broadcasts the
     same write/remove to every machine in `engine/fleet.json` by direct SSH file write —
     local action always applies first and never depends on remote success.
     (b) §6 — replace the first paragraph ("Per-machine flag, for now. … not built here.")
     with a short paragraph stating: broadcast built 2026-07-06 (wg-t10-02); targets live in
     `engine/fleet.json` (Roamy only, per fleet-scope decision Q8); mechanism is SSH
     file-write, deliberately independent of Switchboard; the Switchboard state plane
     (deferred fork, T1-11) remains the eventual richer home for fleet control, and this
     broadcast is forward-compatible with it (the flag file stays the ground truth either
     way). Keep the rest of the doc untouched.
   - **Expect:** `grep -n "fleet.json" /Users/davidcruwys/dev/ad/apps/dark-factory/docs/kill-switch-spec.md`
     shows hits in §2 and §6; `git diff --stat` shows only kill-switch-spec.md among docs.
   - **Failure signal:** §6 wording no longer matches what edit (b) expects (doc changed
     since authoring).
   - **Counter-move:** apply the same *semantic* update to whatever §6 now says (state the
     broadcast exists, where targets live, that Switchboard is not required); if the doc now
     claims a DIFFERENT cross-machine mechanism already exists, that contradicts Recon 2 →
     **Abort A1**.

7. **Commit, push, re-sync Roamy, self-report.**
   - **Do:**
     ```bash
     cd /Users/davidcruwys/dev/ad/apps/dark-factory
     git add engine/halt.py engine/fleet.json docs/kill-switch-spec.md \
             engine/store/results/wg-t10-02-roundtrip.txt
     git commit -m "feat(engine): cross-machine HALT broadcast — halt.py --fleet over SSH file-write (wg-t10-02)"
     git pull --rebase origin main && git push origin main
     ssh -o BatchMode=yes macbook-pro-m4 'cd ~/dev/ad/apps/dark-factory && git pull --ff-only origin main && grep -c "fleet" engine/halt.py'
     ```
     Then write the results self-report JSON to the exact path your dispatch prompt gave you;
     name any fork/counter-move that fired.
   - **Expect:** push accepted; Roamy's pull fast-forwards and its halt.py now contains
     `fleet` (count ≥ 1). Stage ONLY the four listed paths — the repo will be mid-portfolio
     with other sessions' wargame files present; never `git add -A`.
   - **Failure signal:** push rejected even after rebase; or Roamy's second pull won't
     fast-forward.
   - **Counter-move:** push race → repeat `git pull --rebase && git push` once more; still
     failing, leave the commit local and record "push pending — remote diverged" in the
     report. Roamy pull failure at this stage → record "Roamy re-sync pending" in the report
     (the broadcast itself already works against Roamy's store path; only Roamy-side
     `--fleet` initiation waits on the sync). Neither blocks completion.

## Forks

**F1 — Roamy's clone is dirty (tracked files) or diverged from origin/main.**
Trigger: Recon 4 shows tracked modifications, a non-main branch, or Move 1's ff-only pull
refuses.
→ **Route A** (dirt is untracked files only, e.g. under `engine/store/` — untracked files
don't block an ff-only pull unless a pulled path collides): run the pull; if it completes,
continue. If a specific untracked file collides with an incoming path, do NOT delete or stash
anything — Route B.
→ **Route B** (tracked dirt, divergence, wrong branch, or a collision): **Abort A1**. Never
resolve another machine's uncommitted state or divergence without a human — that clone may be
mid-session for a Roamy-side agent.

**F2 — Roamy unreachable (asleep, off tailnet, or key auth denied) at execution time.**
Trigger: Recon 3 fails, or SSH dies during Moves 1/5/7.
→ **Route A** (transient — `tailscale status` shows roamy but SSH timed out): retry once
after 60 s; success → continue where you left off.
→ **Route B** (roamy offline in tailscale, or `Permission denied (publickey)` persists):
complete everything machine-local — Moves 2, 3, 4, 6 all run without Roamy; in Move 5 run
only the local legs plus one broadcast attempt to CAPTURE the designed failure behavior
(`roamy: FAILED (...)`, exit 1, local flag still applied — that output is itself evidence;
save it in the round-trip transcript, then `resume` locally). Skip Move 1 and Move 7's Roamy
re-sync. Commit + push per Move 7, then **Abort A2** (park for the live proof). The code
lands; only the end-to-end proof waits.

**F3 — `--fleet` already exists in halt.py at recon.**
Trigger: Recon 2 grep is non-empty (another session or a human got there first).
→ **Route A** (the existing implementation matches this contract — fleet.json targets, local
first, direct file write, per-machine report lines): verification-only run — execute Move 5
and the Verification block, fix `docs/kill-switch-spec.md` if it still says per-machine-only
(Move 6), commit any doc fix, report "no-op: already built, verified live".
→ **Route B** (a *different* mechanism exists — e.g. it shells into remote halt.py, uses
Switchboard, or reads targets from somewhere else): do not layer a second mechanism →
**Abort A1** with a side-by-side description of found-vs-specified.

## Assumptions ledger

1. **Roamy's identity and path stay stable** — ssh alias `macbook-pro-m4` → 100.89.32.35,
   user `davidcruwys`, clone at `/Users/davidcruwys/dev/ad/apps/dark-factory` (all verified
   live at authoring, incl. `whoami`/`hostname` = davidcruwys/Roamy). If the alias vanishes
   from `~/.ssh/config`, try MagicDNS `davidcruwys@roamy`; if the clone path is gone →
   Abort A1.
2. **No engine processes run on Roamy today** (verified at authoring: no orchestrator/warm
   pool, no tmux server). The broadcast is therefore prophylactic on Roamy — correct and
   intended: the flag must be *waiting* before Roamy's engine ever runs. If a Roamy-side
   orchestrator IS running at execution, nothing changes for this ticket (HALT is graceful by
   spec §5), but note it in the report — it means fleet delegation started; T10 siblings care.
3. **Fleet scope stays Roamy-only** (decisions.md Q8). The other minis (m2, jan, mary) have
   ssh aliases but are deliberately NOT in fleet.json. If David wants them added later, it's
   a one-line JSON append — do not pre-add them.
4. **Flag files are untracked by design** (verified: `git check-ignore` says nothing ignores
   `engine/store/HALT`, and no HALT/BACKOFF/WAKE-ARMED has ever been committed). Never stage
   a flag file; verification checks this.
5. **Roamy-initiated fleet halt (Roamy → Mini) is out of scope.** fleet.json as committed
   lists remotes from the M4 Mini's perspective; after Move 7's re-sync Roamy *has* the code
   and the file, but `macbook-pro-m4` may not resolve from Roamy and reverse key auth is
   unverified. If it matters, that's a follow-up ticket — record one line in the report if
   you notice it, build nothing.

## Abort conditions

- **A1 — engine or deployment world changed / conflicting mechanism / Roamy clone diverged.**
  (Recon 1/5 failures, F1-B, F3-B, Move 3/4 unrecoverable, Move 6's contradicting doc.)
  FIRST restore any half-edited tracked file (`git -C /Users/davidcruwys/dev/ad/apps/dark-factory checkout engine/halt.py docs/kill-switch-spec.md` as applicable) so the local kill
  switch is never left broken. Park: write
  `engine/store/needs-decision/wg-t10-02-fleet-halt-broadcast.json` with
  `{"ticket":"wg-t10-02-fleet-halt-broadcast","question":"<what you found, verbatim observations — e.g. Roamy clone diverged: <git output> / a different fleet mechanism exists: <describe>>. How should the fleet HALT broadcast proceed?","proposed":"<your best single next step>","note":"per war game T10-02 A1"}`.
  Leave the ticket in `running/`.
- **A2 — Roamy has a deliberate pre-existing HALT (Recon 6), or Roamy is unreachable and the
  live proof cannot complete (F2-B).** For the pre-existing-HALT case: touch NOTHING remote,
  park immediately with the remote flag's payload quoted in the question ("Roamy is already
  halted by <by> since <ts> — proceed with broadcast build and leave its flag alone, or is
  this stale?"). For the unreachable case: land the local work per F2-B first, then park with
  question "Roamy is asleep/unreachable (<evidence>) so the fleet round-trip proof cannot
  complete. Wake Roamy and say go — the code is committed; the proof is Move 5 + Move 7's
  re-sync." Leave the ticket in `running/`.
- **A3 — a test HALT flag may be stranded on Roamy** (Move 5's counter-move exhausted: resume
  broadcast failed AND the direct `rm -f` over SSH also failed, e.g. Roamy died mid-test).
  This is the one state that must never be silent: park immediately with question
  "WARNING: Roamy may have a stranded test HALT at ~/dev/ad/apps/dark-factory/engine/store/HALT
  (payload reason 'wg-t10-02 fleet round-trip test'). When Roamy is back:
  `ssh macbook-pro-m4 'rm -f ~/dev/ad/apps/dark-factory/engine/store/HALT'` — then say go to
  finish verification." Local flag must still be cleared (`python3 engine/halt.py resume`)
  before parking. Leave the ticket in `running/`.

## Verification

Executable acceptance (mirrors the ticket's `verify` field). Under F2-B, checks 3–5 are
replaced by the captured `roamy: FAILED` behavior evidence and the A2 park.

```bash
cd /Users/davidcruwys/dev/ad/apps/dark-factory

# 1. fleet.json exists, Roamy-only, correct shape
python3 -c "
import json
f=json.load(open('engine/fleet.json'))
ms=f['machines']
assert [m['name'] for m in ms]==['roamy'], ms
assert ms[0]['ssh'] and ms[0]['store'].endswith('engine/store')
print('fleet.json OK:', ms[0])"

# 2. Backward compat — no-flag CLI byte-identical to the old contract
python3 engine/halt.py status | grep -q "RUNNING -- no HALT file present." && echo local-status OK
python3 -c "
import sys; sys.path.insert(0,'engine')
from halt import is_halted, halt_info
assert is_halted() is False and halt_info() is None
print('reader API intact')"

# 3. Live round-trip (safe to re-run any time; leaves no flag behind)
python3 engine/halt.py halt "wg-t10-02 verify" --by verify --fleet | grep -q "roamy: HALTED" && echo broadcast-halt OK
ssh -o BatchMode=yes macbook-pro-m4 'python3 -c "import json;d=json.load(open(\"/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT\"));assert d[\"reason\"]==\"wg-t10-02 verify\" and \"origin\" in d;print(\"remote flag OK\")"'
python3 engine/halt.py status --fleet | grep -q "roamy: HALTED" && echo fleet-status OK
python3 engine/halt.py resume --fleet | grep -q "roamy: RESUMED" && echo broadcast-resume OK
ssh -o BatchMode=yes macbook-pro-m4 'test ! -e /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT' && echo remote-clear OK
test ! -e engine/store/HALT && echo local-clear OK

# 4. Roamy's engine is HALT-aware (synced) — its own halt.py answers
ssh -o BatchMode=yes macbook-pro-m4 'cd ~/dev/ad/apps/dark-factory && python3 engine/halt.py status --json' | grep -q '"halted": false' && echo roamy-engine OK

# 5. Docs + evidence + commit
grep -q "fleet.json" docs/kill-switch-spec.md && echo spec OK
test -s engine/store/results/wg-t10-02-roundtrip.txt && echo evidence OK
git log --oneline -5 | grep -qi "wg-t10-02" && echo commit OK
```

Negative checks (what must NOT have changed):

```bash
cd /Users/davidcruwys/dev/ad/apps/dark-factory

# No flag file ever committed
test -z "$(git ls-files engine/store | grep -E 'HALT|BACKOFF|WAKE-ARMED')" && echo no-flags-tracked OK

# Readers untouched — the broadcast is writer-side only
test -z "$(git log --oneline -5 --format= --name-only | grep -E 'engine/(orchestrator|warm_pool|wake|status)\.py')" && echo readers-untouched OK

# bin wrappers still exec-through (they pass --fleet along for free)
grep -q 'exec python3 "$DIR/engine/halt.py" halt "$@"' bin/factory-halt && echo wrappers OK

# Fleet scope not widened
python3 -c "
import json
assert len(json.load(open('engine/fleet.json'))['machines'])==1
print('scope OK: roamy only')"
```

## Executor notes (sonnet)

- **Scope fence:** touch exactly four repo paths — `engine/halt.py`, `engine/fleet.json`
  (new), `docs/kill-switch-spec.md`, `engine/store/results/wg-t10-02-roundtrip.txt` (new
  evidence) — plus the two `git pull` syncs on Roamy. Never edit `orchestrator.py`,
  `warm_pool.py`, `wake.py`, `status.py`, the `bin/` wrappers, or ANYTHING else on Roamy.
  Do not broadcast BACKOFF or WAKE-ARMED — HALT only (BACKOFF is a self-clearing local
  governor; fleet-wide backoff is a different, unasked question).
- **The safety invariant that outranks everything:** never leave a flag file behind — on
  either machine — that you wrote as a test. Every halt you write, you resume; if you can't,
  it's A3, loudly.
- **Local-first is load-bearing, not style:** the local HALT write must succeed before any
  SSH is attempted, and local success is never rolled back on remote failure. A kill switch
  that waits on the network is worse than none.
- **HITL over guessing:** anything ambiguous about Roamy's clone state (divergence, dirt, a
  pre-existing HALT, a competing fleet mechanism) → park. Roamy may be another agent's live
  workspace; a parked ticket with a sharp question beats a remote `git stash`.
- **The rabbit hole:** generalizing the fleet — adding m2/jan/mary to fleet.json, building a
  Roamy→Mini reverse leg, retrying/queueing offline broadcasts, or wiring this into
  Switchboard/status.py dashboards. All of it is other tickets (T10 siblings, T1-11, T5).
  This ticket is: one JSON file, one flag on halt.py, one proven round-trip, one doc update.
  Skip everything else.
