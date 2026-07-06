# T8-08 — Repo hygiene sweep — fleet verdicts + safe pushes

| field | value |
|---|---|
| ticket | wg-t8-08-repo-hygiene-sweep |
| track / size / priority | T8 Doc truth / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

On 2026-06-15 a machine-wide scan flagged 16 dirty repos plus remote/push debt
(`backlog/2026-06-15-cortex-architecture-handover.md` §PARKED, lines 72–75) — never confirmed
resolved. Authoring-time recon (2026-07-06) shows the picture has MOVED: on mac-mini-m4 the
named repos (beauty-and-joy, deckhand, appydave-plugins, kiros-hq) now all have remotes AND
tracking, but the machine now has **48 dirty repos, 4 with no remote at all, 5 with unpushed
commits, 1 tracked-but-untracked-branch** — and on Roamy, **deckhand STILL has no remote and 28
dirty files at risk**. This ticket re-sweeps BOTH machines (Q8: fleet = +Roamy), executes only
the provably-safe actions (fast-forward pushes of already-committed work; setting upstream
tracking, which is config-only), assigns every other repo an explicit verdict
(needs-David / ignore / registry-drift), and publishes one report that formally closes or
re-opens each June-15 claim. Done looks like: the verdicts report exists in `backlog/`, the
safe pushes verify at zero-ahead, no commit/remote/rebase was ever created in any swept repo,
and the June-15 handover carries a pointer to the closure.

## Locked context

- **Q8 (decisions.md):** fleet scope = this machine + Roamy — the Roamy half of the sweep is
  in-scope, not optional.
- **Q4 (decisions.md):** everything through the engine — worker self-reports to
  `engine/store/results/` per the orchestrator's task prompt.
- **T8 doctrine (path-map.md):** docs lag code — the June-15 numbers are claims to VERIFY, not
  facts to repeat. The fresh sweep supersedes them.
- **David's standing preference (CLAUDE-PREFERENCES.md):** "commit and push finished work
  without being asked" pre-authorizes pushing existing commits; "wait for an explicit go on
  irreversible / setup actions" forbids creating remotes, committing dirty trees, or any
  rebase/force in someone's working repo. That line is the safe/unsafe boundary of this
  entire ticket.
- **Register-every-app standing rule:** unregistered repos are a registration problem, not a
  hygiene-sweep problem — list, don't chase.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs.

## Recon (verify before any work)

All commands from `/Users/davidcruwys/dev/ad/apps/dark-factory` unless pathed.

1. `hostname` → expect `mac-mini-m4.local`. If not, you are on the wrong machine for the
   "local" half of this war game → **Abort A1** (the safe-action authorization was reasoned
   for this machine's repo set).
2. `python3 -c "import json; d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json')); print(len(d['locations']))"`
   → expect ≈134 (a dict with a `locations` list; each entry has `path`). Missing file,
   parse error, or no `locations` key → **Abort A1**. This file is the canonical repo
   enumeration (per `~/dev/ad/CLAUDE.md`); there is no fallback enumeration in this ticket.
3. `sed -n '72,75p' backlog/2026-06-15-cortex-architecture-handover.md` → expect the four
   June-15 claims: 16 dirty repos; `v-appydave` (82 mod + 61 untracked); `beauty-and-joy`
   remote-but-no-tracking; `deckhand` no remote; 4 clean-but-unpushed (`appydave-plugins`,
   `appyctrl`, `kiros-hq`, `vibedeck`). If the lines moved, `grep -n "16 dirty"` the file.
   If the whole PARKED entry is gone (someone already closed it) → **Fork F4**.
4. `ssh -o ConnectTimeout=5 -o BatchMode=yes roamy 'hostname; which python3 && echo PY3-OK; ls ~/.config/appydave/locations.json'`
   → expect `Roamy`, `PY3-OK`, and the locations.json path (all three verified present
   2026-07-06). Any failure → note it now; Move 2 will hit **Fork F1**.
5. `ls backlog/ | grep -i "repo-hygiene"` → expect nothing. If a
   `*-repo-hygiene-verdicts.md` already exists, someone ran this sweep already → **Abort
   A1** (park with "supersede or refresh the existing report?").
6. Baseline the executor's own workbench: `git -C ~/dev/ad/apps/dark-factory status
   --porcelain | wc -l` → record the count. dark-factory WILL appear dirty (in-flight
   war-game authoring is untracked here by design) — that dirt is `active-workbench`, not
   debt; Move 4 must not verdict it as needs-David.

## Moves

### Move 1 — Build the scanner, sweep mac-mini-m4

- **Do:** Write this scanner to the scratchpad as `hygiene_scan.py` (verbatim — it ran clean
  at authoring time):

  ```python
  #!/usr/bin/env python3
  """Repo hygiene scanner. Read-only: never mutates any repo. Emits JSON to stdout."""
  import json, os, subprocess, sys
  def g(p, *a):
      return subprocess.run(["git", "-C", p] + list(a), capture_output=True, text=True)
  d = json.load(open(os.path.expanduser("~/.config/appydave/locations.json")))
  locs = d["locations"] if isinstance(d, dict) else d
  out, errors = [], 0
  for item in locs:
      p = item.get("path")
      if not p:
          continue
      rec = {"path": p, "key": item.get("key")}
      if not os.path.isdir(p):
          rec["state"] = "path-missing"; out.append(rec); continue
      if not os.path.isdir(os.path.join(p, ".git")):
          rec["state"] = "not-a-repo"; out.append(rec); continue
      try:
          rec["state"] = "repo"
          rec["head"] = g(p, "rev-parse", "HEAD").stdout.strip()
          rec["branch"] = g(p, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
          rec["dirty"] = len([l for l in g(p, "status", "--porcelain").stdout.splitlines() if l.strip()])
          rec["remotes"] = g(p, "remote").stdout.split()
          u = g(p, "rev-parse", "--abbrev-ref", "@{u}")
          rec["upstream"] = u.stdout.strip() if u.returncode == 0 else None
          if rec["upstream"]:
              rec["ahead"] = int(g(p, "rev-list", "--count", "@{u}..HEAD").stdout.strip() or 0)
              rec["behind"] = int(g(p, "rev-list", "--count", "HEAD..@{u}").stdout.strip() or 0)
      except Exception as e:
          rec["state"] = "scan-error"; rec["error"] = str(e); errors += 1
      out.append(rec)
  json.dump({"machine": os.uname().nodename, "repos": out, "scan_errors": errors}, sys.stdout, indent=1)
  ```

  Run it: `python3 <scratchpad>/hygiene_scan.py > <scratchpad>/local.json; echo $?`.
  It is read-only by construction — every git call is a query.
- **Expect:** exit 0; `local.json` parses; repo records ≈128 (134 locations minus
  `path-missing`/`not-a-repo` entries). Authoring-time truth to sanity-check against: 48
  dirty, 4 no-remote (`digital-stage-summit-2026`, `screentour`, `bank-reconciliation`,
  `brain-cowork-upgrade`), 5 ahead (`ansible` +1, `appystack` +1, `awb` +22, `flilaunch` +2,
  `signal-studio` +1), 1 upstream-null-with-remote (`appydave-tools`, which is otherwise
  clean and in sync). Drift from these numbers is EXPECTED (days pass); a different SHAPE
  (e.g. zero repos found) is not.
- **Failure signal:** nonzero exit; `scan_errors` > 20% of repo count; zero repos.
- **Counter-move:** one debugging pass on the scanner (it's your file, in scratchpad). If
  still >20% errors → **Abort A3**.

### Move 2 — Sweep Roamy (report-only)

- **Do:** `ssh -o ConnectTimeout=5 -o BatchMode=yes roamy 'python3 -' < <scratchpad>/hygiene_scan.py > <scratchpad>/roamy.json; echo $?`
  Roamy's paths differ per-machine only via its own locations.json — the scanner reads the
  remote copy, so no path translation is needed. **No actions are ever executed on Roamy in
  this ticket** — its half is inventory + verdicts only (Assumption 4).
- **Expect:** exit 0; `roamy.json` parses with `"machine": "Roamy"` (or similar nodename).
  Authoring-time spot-truth to sanity-check: `deckhand` on Roamy = branch `main`, NO
  remotes, 28 dirty; `beauty-and-joy` and `appydave-plugins` clean+tracked; `v-appydave`
  144 dirty.
- **Failure signal:** ssh times out / refuses; python errors remotely; empty output.
- **Counter-move:** → **Fork F1**.

### Move 3 — Execute the safe actions (mac-mini-m4 only)

- **Do:** Two action classes, nothing else. Work from `local.json`:
  1. **Set upstream tracking (config-only)** — for every repo with `remotes` non-empty and
     `upstream: null`: if `git -C <p> rev-parse --verify origin/<branch>` succeeds, run
     `git -C <p> branch --set-upstream-to=origin/<branch> <branch>` (pure config; touches no
     history, no remote). If origin lacks that branch → **Fork F3**. (Authoring-time: only
     `appydave-tools` is in this class, branch `main`, `origin/main` exists and is in sync —
     so the expected action is exactly one `--set-upstream-to`.)
  2. **Fast-forward push of committed work** — for every repo with `upstream` set and
     `ahead > 0`: first `git -C <p> fetch origin` (refresh staleness), re-check
     `ahead`/`behind`; push ONLY if `behind == 0`: `git -C <p> push`. If `behind > 0` after
     fetch → **Fork F2**, no push. Never `--force`, never `pull`, never rebase/merge — a
     hygiene sweep does not resolve divergence, it reports it.

  Hard fence: no `git add`/`commit`/`stash`/`checkout`/`reset`/`clean` in ANY swept repo; no
  `gh repo create`; the 4 no-remote repos get a verdict in Move 4, not a remote.
- **Expect:** each push prints a fast-forward ref update (`<old>..<new>  <branch> ->
  <branch>`) and exits 0; after all actions, re-running the scanner shows `ahead: 0` and
  `upstream` non-null for every actioned repo, and every repo's `head` sha is byte-identical
  to Move 1's record (pushes and tracking config never move HEAD).
- **Failure signal:** push rejected; push output containing `forced update` or ` - [deleted]`;
  any `head` sha changed; auth failure (`Permission denied (publickey)` / `Repository not
  found`).
- **Counter-move:** rejected non-fast-forward → **Fork F2**. Auth/404 → **Fork F2 Route B**.
  `forced update`/`deleted` in output or a changed HEAD → **Abort A2** immediately (stop all
  remaining pushes first).

### Move 4 — Assign verdicts to everything

- **Do:** Re-run the scanner locally (post-action state), then classify EVERY repo record
  from both machines into exactly one verdict:

  | verdict | rule |
  |---|---|
  | `clean` | dirty=0, ahead=0, upstream set |
  | `pushed-now` / `tracking-set` | actioned in Move 3, now clean per rule above |
  | `no-remote` → needs-David | `remotes` empty (remote creation is a David-go setup action) |
  | `diverged` → needs-David | ahead>0 AND behind>0 after fetch (Fork F2 Route A) |
  | `remote-broken` → needs-David | push/fetch failed with auth/404 (Fork F2 Route B) |
  | `dirty-wip` → needs-David | dirty ≥ 10 (someone's live working state; never auto-commit) |
  | `dirty-light` → needs-David (batchable) | 1 ≤ dirty < 10 (a one-session tidy batch for David or a follow-up ticket) |
  | `active-workbench` → ignore | dark-factory itself (Recon 6), and any repo whose dirt is THIS ticket's own artifacts |
  | `registry-drift` | `path-missing` / `not-a-repo` entries (locations.json points at nothing — authoring-time: 5 missing paths) |
  | `unswept` | Roamy repos if Fork F1 Route B fired |

  Rules are mechanical on the scanner JSON — no taste calls. A repo matching two rows takes
  the FIRST matching row top-down.
- **Expect:** every record has exactly one verdict; needs-David bucket is non-empty
  (authoring-time it plainly will be: 4 no-remote + v-appydave alone guarantee it).
- **Failure signal:** a record fits no row.
- **Counter-move:** add it to the report under `unclassified` with its raw JSON — do NOT
  invent a verdict row; one-off anomalies are report content, not policy.

### Move 5 — Publish the report + close the June-15 claims

- **Do:** Write `backlog/<today UTC yyyy-mm-dd>-repo-hygiene-verdicts.md` containing, in
  order: (a) header — ticket id, machines swept, scan timestamps, totals per verdict;
  (b) **June-15 claims closure table** — one row per claim from Recon 3, columns: claim ·
  mac-mini-m4 state today · Roamy state today · verdict CLOSED / STILL-OPEN / MOVED
  (authoring-time preview: beauty-and-joy CLOSED both machines; deckhand CLOSED on M4 Mini,
  **STILL-OPEN on Roamy** — no remote, 28 dirty, at-risk; the 4 clean-but-unpushed CLOSED
  on M4 Mini; "16 dirty" MOVED — the local count is now ~48); (c) full per-machine verdict
  tables (repo · dirty · ahead/behind · verdict · action taken); (d) a **NEXT — David**
  block listing every needs-David verdict as a one-line decision each (e.g. "deckhand@Roamy:
  create remote? which org?" · "v-appydave: 306 dirty local / 144 Roamy — commit, ignore, or
  gitignore-tune?" · "4 no-remote repos: create remotes? org/visibility per repo"). Then
  append ONE line to the PARKED bullet in
  `backlog/2026-06-15-cortex-architecture-handover.md` (after its line 75):
  `  — Re-swept <date> by wg-t8-08: see backlog/<date>-repo-hygiene-verdicts.md (deckhand@Roamy still at risk; local count now <N>).`
  No other edit to that historical file.
- **Expect:** both files as described; the report's numbers are the scanner's numbers (no
  hand-adjusted counts).
- **Failure signal:** you cannot fill a closure-table cell because a machine wasn't swept.
- **Counter-move:** fill the cell `unswept (see F1)` — an honest hole beats a guessed CLOSED.

### Move 6 — Self-report, commit, push (dark-factory only)

- **Do:** Write the worker self-report to `engine/store/results/` in the exact form the
  orchestrator's task prompt demands, including: totals per verdict, actions executed (each
  repo + command), the needs-David list, and any fork/abort routes taken. Commit ONLY the
  dark-factory changes (the report, the one-line handover append, the results file) —
  message `chore(t8): repo hygiene sweep — fleet verdicts + safe pushes (wg-t8-08)` with the
  standard Co-Authored-By trailer; push. Do not commit other in-flight dark-factory dirt
  noted in Recon 6 (stage the three paths explicitly, no `git add -A`).
- **Expect:** `git log --oneline -1` shows the commit; `git status --porcelain` shows only
  the pre-existing Recon-6 dirt.
- **Failure signal:** push rejected (non-fast-forward — parallel war-game sessions land
  constantly in this repo).
- **Counter-move:** `git pull --rebase` then push (dark-factory is the ONE repo where this
  ticket may rebase — it's the executor's own workbench). Conflicts in files this ticket
  didn't author → prefer the other side, re-apply this ticket's three files, push. Second
  failure → leave committed locally, note in results JSON.

## Forks

**F1 — Roamy sweep fails.**
Trigger: Move 2's ssh or remote python fails (Recon 4 forewarns).
→ **Route A (ssh works, python route broken):** retry once with a shell fallback executed
remotely: for each of the four June-15-named Roamy paths (`~/dev/ad/joy/beauty-and-joy`,
`~/dev/ad/apps/deckhand`, `~/dev/ad/appydave-plugins`, `~/dev/video-projects/v-appydave`) run
`git -C <p> status -sb | head -1; git -C <p> status --porcelain | wc -l; git -C <p> remote`
over ssh — a partial Roamy picture covering the actual claims.
→ **Route B (ssh itself dead — Roamy offline/roaming):** mark every Roamy cell `unswept` in
the report, add "re-run Roamy half when reachable" to the NEXT block, and complete the
ticket. Roamy's absence degrades the report; it does not block it.

**F2 — Push candidate won't fast-forward.**
Trigger: Move 3's fetch shows `behind > 0`, or the push is rejected.
→ **Route A (diverged — ahead>0 and behind>0):** verdict `diverged`, needs-David, take NO
action (no pull, no rebase, no force — this sweep never rewrites anyone's history).
→ **Route B (auth failure / repository not found):** verdict `remote-broken`, needs-David,
take no further action against that remote (retrying auth failures in a loop looks like an
attack and fixes nothing).

**F3 — Upstream-set candidate has no matching remote branch.**
Trigger: Move 3 class-1 repo where `origin/<branch>` does not exist.
→ **Route A (repo is clean or ahead-only of nothing — the branch simply was never
published):** `git -C <p> push -u origin <branch>` — additive, creates the remote branch,
rewrites nothing.
→ **Route B (anything murkier — detached HEAD, branch name that looks temporary, e.g.
`backup/*`):** verdict `needs-David` with the observed state quoted; no action.

**F4 — June-15 claims already closed by someone else.**
Trigger: Recon 3 finds the PARKED hygiene entry gone or already annotated as resolved.
→ **Route A (annotated with a pointer to a newer report):** this ticket's report becomes a
refresh; link the older report in the header, proceed normally.
→ **Route B (entry deleted, no trace of a report):** proceed normally but say so in the
closure table's header — the fresh sweep IS the missing evidence either way.

## Assumptions ledger

1. **The June-15 scan was of Roamy.** Inferred: that handover session addressed cortex "on
   M4 Mini (Tailscale)" remotely, i.e. it ran on the MacBook Pro. Plausible but unproven —
   and it doesn't matter: the fresh two-machine sweep supersedes the old count whichever
   machine produced it. If Roamy's numbers today match neither 16 nor the local 48, note
   "original scan machine unconfirmed" in the report and move on.
2. **locations.json is the complete enumeration.** Repos not registered there are invisible
   to this sweep — accepted, per the register-every-app standing rule (registration debt is
   its own ticket). If the executor happens to SEE an obviously-missing major repo, list it
   under `registry-drift`, don't scan it ad hoc.
3. **Fast-forward pushes of committed work are pre-authorized.** Grounded in David's
   standing preference ("commit and push finished work without being asked") and in the
   fact that a fast-forward push of existing commits to the owner's own configured remote is
   non-destructive. If David objects mid-run (HITL message, decisions/ file), stop all
   pushes and downgrade the ticket to verdicts-only — the report is still the deliverable.
4. **Roamy is report-only.** Pushing from Roamy depends on its ssh-agent/keychain GitHub
   auth state, unverified at authoring. If any Roamy repo needs action, it appears in the
   NEXT block as a decision/follow-up, never as a remote command from this ticket.
5. **The dirty≥10 / dirty<10 wip-vs-light threshold is Fable's number, not David's.** It
   only shades the report's grouping, never an action. If it misclassifies (e.g. 12 lines of
   pure lockfile noise), the executor may note the nuance in the verdict row's comment —
   the verdict column itself stays mechanical.

## Abort conditions

**A1 — Wrong footing.** Not on mac-mini-m4 (Recon 1), locations.json missing/unparseable
(Recon 2), or a prior hygiene report already exists (Recon 5). Park: write
`engine/store/needs-decision/wg-t8-08-repo-hygiene-sweep.json` containing
`{"ticket":"wg-t8-08-repo-hygiene-sweep","question":"<which precondition failed and what was observed>. Proceed how?","proposed":"<one line>"}`.
Leave the ticket in `running/`. Never enumerate repos by improvised `find` — the canonical
registry is the contract.

**A2 — A push did something destructive-looking.** Push output contains `forced update` or a
branch deletion, or any swept repo's HEAD sha differs from Move 1's record. Should be
unreachable (no `--force` exists in this war game) — so it means the executor left the
script. STOP all remaining pushes immediately, record the exact output in the needs-decision
file (same shape as A1), leave the ticket in `running/`. Do not attempt remote rollback —
that is itself a force-push and is David's call.

**A3 — Inventory untrustworthy.** Scanner errors on >20% of registered repos after one fix
attempt (Move 1 counter-move). A verdicts report built on garbage data is worse than none —
park to needs-decision/ with the error sample, leave in `running/`.

## Verification

From `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
ls backlog/*-repo-hygiene-verdicts.md                          # exactly 1 report
grep -c "STILL-OPEN\|CLOSED\|MOVED" backlog/*-repo-hygiene-verdicts.md   # ≥ 4 (closure table populated)
grep -n "wg-t8-08" backlog/2026-06-15-cortex-architecture-handover.md    # the one appended pointer line
ls engine/store/results/ | grep wg-t8-08                       # worker self-report exists
# safe actions landed:
git -C ~/dev/ad/appydave-tools rev-parse --abbrev-ref @{u}     # exit 0 (upstream now set)
for p in ~/dev/ad/agent-os/ansible ~/dev/ad/apps/appystack ~/dev/ad/apps/awb \
         ~/dev/ad/flivideo/flilaunch ~/dev/clients/supportsignal/signal-studio; do
  git -C $p rev-list --count @{u}..HEAD; done                  # all 0 (or the repo appears as diverged/remote-broken in the report)
```

Negative checks (nothing beyond the mandate happened):

```bash
# the 4 no-remote repos STILL have no remote — this ticket must not have created any:
for p in ~/dev/ad/apps/digital-stage-summit-2026 ~/dev/ad/apps/screentour \
         ~/dev/bank-reconciliation ~/dev/labs/brain-cowork-upgrade; do
  git -C $p remote | wc -l; done                               # all 0
git -C ~/dev/video-projects/v-appydave log --oneline -1        # HEAD unchanged vs Move 1 record — no commit was created there
git -C ~/dev/ad/apps/deckhand status --porcelain | wc -l       # still dirty — WIP was reported, not committed
```

And: the dark-factory commit touches only the report, the handover pointer line, and the
results file (`git show --stat HEAD`); Roamy either has verdict rows or explicit `unswept`
cells — never silent absence.

## Executor notes (sonnet)

- **Scope fence:** in swept repos the ONLY permitted commands are read-only git queries plus
  `git fetch origin`, `git push` (never forced), `git push -u origin <branch>`, and
  `git branch --set-upstream-to=...` — and those last three on mac-mini-m4 only. File writes
  land ONLY in dark-factory (report, one pointer line, results JSON) and the scratchpad.
  Never `gh repo create`, never edit/commit/stash/clean anything in a swept repo, never any
  git action on Roamy.
- **You are a surveyor, not a janitor.** The deliverable is the verdicts report. 48 dirty
  repos will scream to be tidied — committing WIP in v-appydave (306 entries of David's live
  video-project state) or "just gitignoring" noise would destroy exactly the information
  David needs to make the call. That is THE rabbit hole: skip it entirely; every dirty tree
  is a report row.
- **Second rabbit hole:** wiring this scan into AppyRadar/sentinel (`git_dirty` MCP exists
  but sentinel is blind to Roamy — a T6 problem). Out of scope; a one-line suggestion in the
  report's NEXT block is the maximum.
- **Prefer HITL over guessing:** any repo whose state doesn't fit the verdict table, any
  push output you don't recognise → report row or needs-decision/, never improvisation.
  A wrong verdict misleads David for months; an `unclassified` row costs nothing.
