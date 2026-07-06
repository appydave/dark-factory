# T6-10 — Retire-or-fix com.appydave.omi-sync

| field | value |
|---|---|
| ticket | wg-t6-10-omi-sync-retire-or-fix |
| track / size / priority | T6 Constellation / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Close the `com.appydave.omi-sync` rot for good. The "decide" half is already taken: the plist was
retired 2026-07-06 ~15:02 (loose-ends ledger D3, backed up to
`~/Library/LaunchAgents/retired/com.appydave.omi-sync.plist.retired-2026-07-06`) after failing
`exit 1` on every scheduled run since ~forever — its `git pull --rebase` died on unstaged changes
in `~/dev/raw-intake`, so it never fetched, committed, or pushed. But retiring it orphaned the one
job it owned that nothing else does: **the cross-machine git sync of the OMI transcript archive**.
The replacement (`com.appydave.omi-fetch` pulse, every 600s) fetches and commits but — by its own
deliberate design law — never pushes and never pulls. Authoring-time recon found the debris:
raw-intake `ahead 41, behind 3` of origin (Roamy is pushing; this machine is invisible to it),
30 stranded untracked `omi/*.md` transcripts that omi-sync failed to ever commit, and 11 modified
June-14 files (the original rot cause). Done looks like: retirement verified still in effect,
replacement proven healthy, the stranded transcripts adopted, raw-intake fully reconciled and
in sync with origin, a guarded push-with-catchup sync leg living in `pulse.py` (the design-law
amendment recorded), stale "omi-sync is live" doc claims truth-fixed, and a closure report at
`backlog/wargames/proof/T6-10/REPORT.md`.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this is written for sonnet Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (launchctl + git + one
  small Python patch; this ticket spawns nothing).
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — all claims below were disk-verified 2026-07-06; your Recon
  re-verifies at execution time. The loose-ends ledger already marks D3 DONE — trust launchctl,
  not the ledger.
- **Q8 fleet = +Roamy:** Roamy demonstrably writes to raw-intake's origin (commits dated
  2026-07-04/05 at authoring). Roamy-side job audit is NOT this ticket — it belongs to the
  T6/T10 fleet seeds; here you fix the M4-Mini side only.
- **Never commit secrets** (global rule): every `git add` in this war game is pathspec-fenced to
  `omi/*.md` transcript files — no blanket adds, ever, in raw-intake.

## Recon (verify before any work)

Absolute roots: raw-intake = `/Users/davidcruwys/dev/raw-intake`, omi-fetch app =
`/Users/davidcruwys/dev/ad/apps/omi-fetch` (its OWN git repo, separate from dark-factory),
LaunchAgents = `/Users/davidcruwys/Library/LaunchAgents`, dark-factory =
`/Users/davidcruwys/dev/ad/apps/dark-factory`.

1. Retirement state:
   `ls /Users/davidcruwys/Library/LaunchAgents/retired/com.appydave.omi-sync.plist.retired-*`
   → expect exactly one file (authoring: suffix `-2026-07-06`), AND
   `ls /Users/davidcruwys/Library/LaunchAgents/com.appydave.omi-sync.plist` → expect "No such
   file". Any other combination → **Fork F1** decides.
2. Job truly unloaded: `launchctl print gui/$(id -u)/com.appydave.omi-sync 2>&1` → expect
   `Could not find service`. If the service prints instead → **Fork F1 Route B**.
3. Dead job's log is silent: `tail -5 /Users/davidcruwys/.cache/omi-sync.log` → expect the last
   timestamped lines on/before the retirement date from Recon 1 (authoring: last entry
   `2026-07-06 15:00` ERROR "git pull --rebase failed"). Lines NEWER than the retired-plist date →
   something still runs `omi_sync.sh` → **Fork F1 Route B** (find and stop it first). Log file
   absent entirely → fine, note it and move on.
4. Replacement job loaded: `launchctl print gui/$(id -u)/com.appydave.omi-fetch 2>&1 | head -20`
   → expect service details (plist at authoring: StartInterval 600, runs
   `/usr/bin/python3 .../omi-fetch/pulse.py`). Missing → **Abort A1**.
5. Replacement actually pulsing:
   `tail -3 /Users/davidcruwys/dev/ad/apps/omi-fetch/store/pulse.log` → expect entries within the
   last ~30 minutes with `errors=-` (or benign errors), and
   `python3 -c "import json; print(json.load(open('/Users/davidcruwys/dev/ad/apps/omi-fetch/store/state.json'))['last_pulse_ts'])"`
   → within 30 min. Stale >24h or all-error lines → **Abort A1**. Also
   `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT 2>/dev/null` → expect
   missing (a present HALT flag makes every pulse a no-op skip — pulse.log would say "halted";
   if HALT is up, this whole ticket shouldn't be running: stop, leave everything untouched).
6. raw-intake topology: `git -C /Users/davidcruwys/dev/raw-intake fetch origin` (must succeed —
   auth failure → **Abort A4**), then `git -C /Users/davidcruwys/dev/raw-intake status -sb | head -1`
   → record ahead/behind (authoring: `ahead 41, behind 3` — both numbers will have grown).
   `git -C /Users/davidcruwys/dev/raw-intake status --porcelain | awk '{print $1}' | sort | uniq -c`
   → authoring: `30 ??` (all under `omi/`) and `11 M` (June-14 transcripts). Record the actual
   counts. Untracked files OUTSIDE `omi/` → do not touch them, list them in the report.
7. pulse.py shape (race check + patch target):
   `grep -n "def git_commit_one\|def git_sync\|append_pulse_log" /Users/davidcruwys/dev/ad/apps/omi-fetch/pulse.py`
   → expect `def git_commit_one` (~line 60), NO `def git_sync`, and `append_pulse_log` call sites
   including one near the end of `run_pulse` (~line 204). If `def git_sync` already exists →
   the fix landed in a race: skip Move 5's patch, verify its behaviour instead and say so in the
   report. If `git_commit_one` is gone or the file is restructured beyond recognition →
   **Fork F2 Route B**.
8. omi-fetch repo seam is clean:
   `git -C /Users/davidcruwys/dev/ad/apps/omi-fetch status --porcelain` → expect empty (verified
   2026-07-06). Dirty on `pulse.py` or `README.md` → someone is mid-change on your exact seam →
   **Abort A3**. Dirty elsewhere (e.g. `store/` artifacts) → proceed; stage only your files.

## Moves

1. **Do:** Settle the retirement (Fork F1 routes this). Route A (the expected case — Recon 1–3
   all show retired): take no launchd action; capture the evidence (the three command outputs)
   for the report. Route B (still loaded / plist back / log still growing): execute the
   retirement now — `launchctl bootout gui/$(id -u)/com.appydave.omi-sync` then
   `mv /Users/davidcruwys/Library/LaunchAgents/com.appydave.omi-sync.plist /Users/davidcruwys/Library/LaunchAgents/retired/com.appydave.omi-sync.plist.retired-$(date +%Y-%m-%d)`
   (the `retired/` dir exists; verified 2026-07-06), then re-run Recon 2 to confirm.
   **Expect:** `launchctl print gui/$(id -u)/com.appydave.omi-sync` says `Could not find service`;
   exactly one retired plist backup exists; active LaunchAgents dir has no omi-sync plist.
   **Failure signal:** bootout errors with anything other than "No such process"/not-found, or
   the service reappears on a fresh `launchctl print`.
   **Counter-move:** `launchctl bootout gui/$(id -u) /Users/davidcruwys/Library/LaunchAgents/com.appydave.omi-sync.plist`
   (path form) and retry once. Still loaded after both forms → **Abort A2** (something re-loads
   it — do not fight an unknown re-loader).

2. **Do:** Prove the replacement is a real replacement. Run one manual pulse:
   `cd /Users/davidcruwys/dev/ad/apps/omi-fetch && python3 pulse.py` — it is idempotent and
   lock-protected by design (its own docstring).
   **Expect:** exit 0 and a printed dict like
   `{'bootstrapped': False, 'fetched': <n>, 'new': <n>, ..., 'errors': []}` (authoring baseline:
   `fetched=26 new=0 index_count=291`); `store/pulse.log` gains one line with `errors=-`.
   **Failure signal:** `{'skipped': True}` (another pulse holds the lock), `{'halted': True}`,
   an `api-key` error, or a non-empty errors list.
   **Counter-move:** `skipped` → wait 90s, retry once (launchd fires every 600s; a collision is
   transient). `halted` → see Recon 5, stop entirely. `api-key` or persistent errors → the
   replacement is NOT healthy → **Abort A1**.

3. **Do:** Adopt the stranded transcripts in raw-intake — the debris omi-sync failed to ever
   commit. Enumerate untracked files under `omi/` ONLY:
   `git -C /Users/davidcruwys/dev/raw-intake ls-files --others --exclude-standard -- omi` (30
   files at authoring, `2026-06-14` → `2026-07-03`). Eyeball the list: every entry must be a
   `omi/*.md` transcript (date-slug filename). Then stage exactly that list (xargs the
   enumeration into `git add --`; never `git add omi/` — it would sweep the 11 modified files,
   which are NOT yours to commit) and commit:
   `git -C /Users/davidcruwys/dev/raw-intake commit -m "omi: adopt stranded uncommitted transcripts — omi-sync failure debris (wg-t6-10)"`.
   Do NOT touch the modified (` M`) files; do NOT touch untracked files outside `omi/`.
   **Expect:** commit succeeds; `git status --porcelain` now shows the 11 ` M` lines (and any
   non-omi untracked strangers) but zero `?? omi/` lines.
   **Failure signal:** a non-`.md` or non-transcript file in the enumeration (e.g. a stray
   directory, a `.tmp`), or the commit picks up paths you didn't stage.
   **Counter-move:** exclude the odd file from the add-list, commit the rest, list the exclusion
   in the report. If `git commit` itself fails (hooks, identity), capture stderr → **Abort A2**.

4. **Do:** Reconcile and drain. From `/Users/davidcruwys/dev/raw-intake`:
   `git pull --rebase --autostash` (autostash carries the 11 modified files across the rebase —
   the exact failure that killed omi-sync, now handled), then `git push`.
   **Expect:** rebase replays the local commits (41+ at authoring, plus Move 3's) onto origin
   cleanly, the autostash pops back (the ` M` files return), push succeeds, and
   `git status -sb | head -1` reads `## main...origin/main` with NO ahead/behind bracket.
   **Failure signal:** (a) rebase conflict — most plausible collision: Roamy independently
   archived the SAME conversation to the same `omi/<date>-<slug>.md` path with different content
   (its 07-04 commits include omi captures), colliding with Move 3's adoption commit; (b) stash
   pop conflict (an incoming commit rewrote one of the 11 locally-modified June-14 files);
   (c) push rejected non-fast-forward (origin moved again mid-move).
   **Counter-move:** (a)/(b) → `git rebase --abort` (working tree back to pre-pull state,
   autostash restored automatically; verify with `git status`), then **Abort A2** with the
   conflicting paths — never resolve transcript-content conflicts by guessing. (c) → re-run
   `git pull --rebase --autostash && git push` once; a second rejection → **Abort A2** (origin
   is too hot; something else is pushing rapidly).

5. **Do:** Give the recurring sync a home — the "fix" half (Fork F2 routes this; skip the patch
   entirely if Recon 7 found `git_sync` already landed). In
   `/Users/davidcruwys/dev/ad/apps/omi-fetch/pulse.py` add, below `git_commit_one`, a
   `def git_sync(errors):` implementing exactly this contract — push-with-catchup, only when
   ahead, never raises, never leaves a rebase in progress:
   - `git -C <RAW_INTAKE_ROOT> rev-list --count @{u}..HEAD` (capture, text, timeout 30); on
     nonzero returncode or count 0 → return (no network ops when there is nothing to push).
   - else `git -C <RAW_INTAKE_ROOT> pull --rebase --autostash` (timeout 120); on failure →
     best-effort `git -C <RAW_INTAKE_ROOT> rebase --abort` (timeout 30, ignore its result),
     append `git-sync pull: <stderr[:200]>` to `errors`, return.
   - else `git -C <RAW_INTAKE_ROOT> push` (timeout 120); on failure append
     `git-sync push: <stderr[:200]>` to `errors`.
   - wrap the whole body in try/except appending `git-sync: <e>` — a sync failure must never
     crash a pulse (match the file's existing belt-and-braces ethos).
   Call it as `git_sync(errors)` inside `run_pulse`'s final `if not dry_run:` block, immediately
   BEFORE the `store.append_pulse_log(...)` call (~line 204), so failures land in pulse.log.
   Then truth-fix the docs this patch invalidates, same repo: (a) `README.md` §"A known
   neighbour: `com.appydave.omi-sync`" (~line 233) — rewrite to past tense: retired
   <date from Recon 1>, plist archived at the retired path, this app's `git_sync` now owns
   push-with-catchup; (b) `README.md` §"Git behaviour (deliberately conservative)" — replace the
   "This app **never pushes**" sentence with the amended law: pushes only when ahead, pull
   --rebase --autostash first, failures logged non-fatally, amended 2026-07-06 because the job
   that owned pushing (omi-sync) is retired; (c) the `pulse.py` comment in the
   filename-collision branch (~line 151) that calls omi-sync "the older omi-sync launchd job,
   which runs independently every 2h" — mark it retired; (d)
   `grep -n "omi-sync" /Users/davidcruwys/dev/ad/apps/omi-fetch/docs/extension-notes.md` — if it
   describes coexistence with a live omi-sync, append a one-line dated status note (do not
   rewrite the doc). Commit the app repo:
   `git -C /Users/davidcruwys/dev/ad/apps/omi-fetch add pulse.py README.md docs/extension-notes.md && git commit -m "feat(pulse): git_sync push-with-catchup — omi-sync retired, sync leg moves here (wg-t6-10)" && git push`.
   **Expect:** `python3 -c "import ast; ast.parse(open('/Users/davidcruwys/dev/ad/apps/omi-fetch/pulse.py').read())"`
   exits 0; `grep -c "def git_sync" pulse.py` → 1; `grep -c "never pushes" README.md` → 0;
   commit and push succeed.
   **Failure signal:** syntax error, grep counts wrong, or push rejected.
   **Counter-move:** syntax error → fix and re-parse (max two attempts, then revert the file
   with `git checkout -- pulse.py` → **Abort A3**). Push rejected → `git pull --rebase` then
   push; conflict in a file you touched → resolve keeping both intents; in a file you did NOT
   touch → **Abort A3**.

6. **Do:** Live-prove the sync leg, then close the loop. Create a probe:
   `git -C /Users/davidcruwys/dev/raw-intake commit --allow-empty -m "wg-t6-10: sync-leg live probe"`,
   then `cd /Users/davidcruwys/dev/ad/apps/omi-fetch && python3 pulse.py`. Then write
   `/Users/davidcruwys/dev/ad/apps/dark-factory/backlog/wargames/proof/T6-10/REPORT.md`
   (mkdir -p the dir) containing: retirement evidence (Move 1 outputs); pulse-health evidence
   (Move 2 dict); raw-intake before/after (`ahead X, behind Y` → in-sync), stranded-adoption
   count, the probe result; the pulse.py diff summary (`git -C .../omi-fetch show --stat HEAD`);
   a "left for David" section listing the 11 still-modified June-14 files verbatim
   (`git status --porcelain | grep '^ M'`) plus any non-omi untracked strangers — content
   adjudication is deliberately NOT this ticket; and one line on the design-law amendment
   (Assumption 3). Commit dark-factory:
   `git -C /Users/davidcruwys/dev/ad/apps/dark-factory add backlog/wargames/proof/T6-10 && git commit -m "proof(constellation): T6-10 omi-sync retirement verified + sync leg restored" && git push`.
   **Expect:** pulse exits 0 with `errors: []`; afterwards
   `git -C /Users/davidcruwys/dev/raw-intake status -sb | head -1` shows NO ahead/behind bracket
   (the probe was pushed by the pulse, not by hand — that is the proof); REPORT.md exists and
   both commits are pushed.
   **Failure signal:** pulse prints a `git-sync ...` error, or the repo is still ahead 1 after
   the pulse (leg didn't fire), or `{'skipped': True}` (lock collision with the launchd pulse).
   **Counter-move:** `skipped` → wait 90s, re-run pulse.py (the probe commit is still there; the
   next pulse will push it). Leg didn't fire → re-check the call site is inside the
   `if not dry_run:` block before `append_pulse_log` and that Recon 7's line numbers matched;
   one fix attempt, re-probe; still dead → `git -C /Users/davidcruwys/dev/raw-intake push` by
   hand so the repo is not left ahead, then **Abort A3** with the evidence.

## Forks

**F1 — retirement state at arrival.**
Trigger: Recon 1–3 disagree with the expected already-retired state.
→ **Route A** (retired plist present, active plist absent, service not found, log silent —
the authoring-time state): verify-only; Move 1 records evidence and takes no launchd action.
→ **Route B** (service loaded, or active plist exists, or omi-sync.log has post-retirement
entries): the retirement reverted or never fully landed — execute Move 1's bootout+archive
sequence, then continue. If evidence shows David deliberately re-enabled it (e.g. a fresh plist
with new content, or a note in loose-ends re-opening D3) → do NOT retire it → **Abort A2** with
the question "omi-sync appears deliberately re-enabled — is retire still the decision?".

**F2 — pulse.py patchability.**
Trigger: Recon 7's shape check.
→ **Route A** (shape matches authoring: `git_commit_one` ~line 60, `append_pulse_log` tail call
in `run_pulse`, no `git_sync`): apply Move 5's patch exactly as specced.
→ **Route B** (commit logic moved but recognizably similar — e.g. extracted to `lib/store.py`
or renamed): implement the same contract adjacent to wherever single-file commits now live,
call it from the same end-of-pulse position, and quote the full diff in REPORT.md. If the git
layer is gone entirely or unrecognizable → **Abort A3** (attach the intended contract from
Move 5 so David can place it).

## Assumptions ledger

1. **The retire decision is David's and final.** Evidence: loose-ends ledger D3 said "say the
   word, I execute", and is marked `DONE 2026-07-06 — omi-sync retired`; the plist was archived,
   not deleted. **If false** (any sign of dispute or re-enable, per F1): stop retiring, park via
   **Abort A2** — un-retiring is one `mv` + `launchctl bootstrap`, so nothing is lost either way.
2. **The 11 modified June-14 transcripts are content edits this ticket must not adjudicate.**
   Plausible: they look like local clean/repair output never committed; whose intent they carry
   is unknowable from here. The war game carries them across the rebase via `--autostash` and
   lists them verbatim in REPORT.md's "left for David" section. **If false** (they conflict with
   incoming commits at Move 4): → **Abort A2** with the paths; David adjudicates content.
3. **Amending omi-fetch's "never pushes" design law is within retire-or-fix scope.** The law was
   written when omi-sync owned pushing ("nothing leaves the machine without a human choosing");
   with omi-sync retired the law guarantees permanent silent drift — and David's own standing
   global rule is "commit and push finished work without being asked so it lands on the other
   machines". The amendment is one revertible commit and is called out in REPORT.md. **If false**
   (David objects at triage/review): `git -C .../omi-fetch revert <sha>` restores never-push;
   then write `engine/store/needs-decision/wg-t6-10-omi-sync-retire-or-fix.json` asking where the
   recurring sync should live instead (a fixed omi_sync.sh under a new schedule is the fallback).
4. **The 30 untracked omi/*.md files are stranded fetch output, safe to adopt.** Plausible: they
   span exactly the window when omi-sync was dying before its commit step, and pulse only commits
   files it writes itself. **If false** (any enumerated file is not a transcript): Move 3's
   counter-move excludes it and reports it — never force-adopt.
5. **Roamy keeps writing to origin and no second sync daemon appears there.** Its 07-04/05
   commits prove it pushes; whether by hand or by job is unknowable from this machine (sentinel
   is blind to Roamy — known T6 debt). The guarded leg tolerates a busy origin (pull-rebase
   first, failures logged non-fatally, retried next pulse). **If false** (origin churns so hard
   Move 4/6 can't land): → **Abort A2**; the Roamy-side audit is a fleet-track ticket, not this
   one.

## Abort conditions

- **A1 — replacement is not healthy.** The omi-fetch launchd job is missing, pulse.log is stale
  >24h, or pulses persistently error (Recon 4–5, Move 2). The retire decision was premised on
  "omi-fetch pulse healthy" (loose-ends D3 wording) — a dead replacement voids the premise. Park:
  write `engine/store/needs-decision/wg-t6-10-omi-sync-retire-or-fix.json` with
  `{"ticket": "wg-t6-10-omi-sync-retire-or-fix", "question": "omi-fetch pulse (the omi-sync replacement) is unhealthy: <evidence>. Revive the pulse first (new ticket), or un-retire omi-sync?", "observed": "<log lines + launchctl output>"}`.
  Leave the engine ticket in `running/`. Do NOT touch raw-intake in this state.
- **A2 — human-judgment wall.** Rebase/stash-pop conflict on transcript content, a re-loader or
  deliberate re-enable of omi-sync, a failing commit, or an origin too hot to land a push. Park
  with the same JSON shape: question naming the exact fork David must call, `observed` carrying
  the conflicting paths / command output verbatim. Working tree must be left clean of
  in-progress state (`git rebase --abort` already run; `git status` output included in the park
  file as proof).
- **A3 — the fix cannot land safely.** pulse.py unrecognizable (F2 both routes dead), a
  mid-change seam (Recon 8), unresolvable syntax after two attempts, or the patched leg won't
  fire and one fix attempt failed. Revert any half-applied edit
  (`git -C /Users/davidcruwys/dev/ad/apps/omi-fetch checkout -- pulse.py README.md`), push
  raw-intake by hand if a probe commit would otherwise strand, then park with the intended
  `git_sync` contract pasted into the question so the decision is "where/how", not "what".
- **A4 — origin unreachable.** `git fetch origin` fails (SSH/auth/network) at Recon 6. Retry
  once after 60s; still failing → park with the stderr. Do not retire, adopt, or patch anything
  on a machine that cannot reach origin — every later move depends on it.

## Verification

```bash
RAW=/Users/davidcruwys/dev/raw-intake
OF=/Users/davidcruwys/dev/ad/apps/omi-fetch
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
LA=/Users/davidcruwys/Library/LaunchAgents

# 1. omi-sync is retired and silent
launchctl print gui/$(id -u)/com.appydave.omi-sync 2>&1 | grep -c "Could not find service"  # → 1
ls $LA/com.appydave.omi-sync.plist 2>/dev/null | wc -l                                      # → 0
ls $LA/retired/com.appydave.omi-sync.plist.retired-* | wc -l                                # → 1 (backup intact, NOT deleted)
# last omi-sync log line predates this run (no new firings):
tail -1 /Users/davidcruwys/.cache/omi-sync.log                                              # timestamp ≤ retirement date

# 2. replacement alive and now owns sync
launchctl print gui/$(id -u)/com.appydave.omi-fetch | grep -c "interval = 600"              # → 1
grep -c "def git_sync" $OF/pulse.py                                                         # → 1
grep -c "git_sync(errors)" $OF/pulse.py                                                     # → 1 (call site wired)
python3 -c "import ast; ast.parse(open('$OF/pulse.py').read()); print('ok')"                # → ok

# 3. raw-intake reconciled — the headline number
git -C $RAW fetch origin && git -C $RAW status -sb | head -1        # → "## main...origin/main" (no ahead/behind; a small ahead is OK only if a pulse just committed fresh captures — re-run after the next pulse and it must clear)
git -C $RAW ls-files --others --exclude-standard -- omi | wc -l     # → 0 (stranded transcripts adopted)
git -C $RAW log --oneline --grep="wg-t6-10" | wc -l                 # → 2 (adoption + probe)

# 4. docs tell the truth now
grep -c "never pushes" $OF/README.md                                 # → 0
grep -ci "retired" $OF/README.md                                     # → ≥1 (neighbour section updated)

# 5. proof + commits
ls $DF/backlog/wargames/proof/T6-10/REPORT.md                        # exists
grep -c "left for David" $DF/backlog/wargames/proof/T6-10/REPORT.md  # → ≥1
git -C $OF status --porcelain | wc -l                                # → 0-ish (only store/ pulse artifacts tolerated)
git -C $OF log --oneline -1 | grep -c "wg-t6-10"                     # → 1 (and pushed)

# 6. negative checks — nothing beyond the ask
git -C $RAW status --porcelain | grep -c '^ M'                       # → 11 (the modified files were NOT committed/stashed away — authoring count; must match REPORT.md's list)
git -C $DF status --porcelain -- research/ engine/ | wc -l           # → 0 (frozen corpus + engine untouched)
git -C /Users/davidcruwys/dev/ad/appydave-plugins status --porcelain -- appydave/skills/omi-fetch | wc -l  # → 0 (skill repo untouched; omi_sync.sh NOT deleted)
ls /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/omi-fetch/scripts/omi_sync.sh | wc -l        # → 1
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT delete the retired plist, `omi_sync.sh`, or `~/.cache/omi-sync.log` —
  they are the audit trail. Do NOT edit anything in `appydave-plugins` (the omi-fetch SKILL is
  T6-01's seam, not yours). Do NOT commit or stash the 11 modified raw-intake files, and never
  run a blanket `git add` in raw-intake. Do NOT touch Roamy over Tailscale — its side is a fleet
  ticket. Do NOT touch dark-factory `engine/*` or `research/`. Do NOT add pull-on-every-pulse:
  the leg is push-with-catchup, gated on `ahead > 0` — 144 network git ops/day against a repo
  that changes a few times a day is exactly the kind of "improvement" to skip.
- **The rabbit hole: the 11 modified June-14 transcripts.** You will be tempted to diff them,
  decide they're "just cleanup", and commit them so the tree is finally clean. Skip it entirely —
  their intent is unknowable from here, they are the original rot that killed omi-sync, and
  adjudicating them is David's 5-minute job with the REPORT.md list in hand. `--autostash`
  exists so you never need to touch them.
- **Style:** README amendments are 2–4 terse sentences each, dated, past-tense factual — no
  apology prose, no history essay. The `git_sync` docstring states the contract in ≤4 lines and
  names this ticket.
- **Prefer parking over guessing** on anything involving transcript CONTENT (conflicts, the
  modified files, a weird untracked file) — content is David's; plumbing is yours. A parked
  ticket with clean evidence beats a "fixed" repo with silently-merged transcripts every time.
