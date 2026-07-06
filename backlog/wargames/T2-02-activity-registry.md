# T2-02 — Universal activity registry

| field | value |
|---|---|
| ticket | wg-t2-02-activity-registry |
| track / size / priority | T2 Producer/BA / L / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Answer "what changed since yesterday, everywhere" for the first time. Today nothing can: the
morning briefing covers exactly ONE hand-configured project (`project-digest/projects/` holds
only `dark-factory.json`), app-registry probes only its ~42 factory-lens apps, and nothing at
all tracks brains or client dirs (`docs/morning-briefing-vision.md` dependency chain, step 1).
Authoring recon (2026-07-06) proved the premise hard: **11 off-registry git repos** exist that
locations.json doesn't know — including `switchboard` and `watchtower`, two of the factory's
own four sister projects. This is an **L / design-first** ticket, so done means three things,
not a production app: **(a)** a staged evidence build `tools/activity-registry/` (stdlib-only
`sweep.py` + `query.py` + `store/activity.json`, mirroring app-registry's probe/query split)
that sweeps the full deduped universe — locations.json paths + the brains repo + discovery
scans over `~/dev/clients` and `~/dev/ad/apps` — via git-log/mtime and proves itself live;
**(b)** the design spec `docs/activity-registry-design.md` pinning universe rules, data model,
CLI contract, and home, with a `Ratification: PENDING` marker for David; **(c)** ONE follow-on
engine ticket (promotion + register-at-birth), staged `status: deferred` until ratification.
This unblocks T2-04 (digest-over-activity) and un-defers the parked
`20260704T0630Z-project-digest-list-and-project-2` chain.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this ticket is written for sonnet
  Swagger dispatch. Nothing in it spawns `claude`; no `-p`/headless/SDK ever.
- **Q9 (decisions.md): complement, don't replace** — app-registry is NOT modified; its
  `probe.py`/`query.py` idiom is copied, never edited.
- **Staging doctrine** (CLAUDE.md + the design-lint precedent): dark-factory `tools/` stages
  new tooling; promotion to `~/dev/ad/apps/` is a separate David decision → the follow-on
  ticket, not this one.
- **Ticket-first standing rule** (`engine/store/queue/.CONVENTION.md`): the follow-on work
  unit gets a queue ticket JSON, even though it is deferred.
- **Register-every-new-app standing rule** applies at PROMOTION time (it is the follow-on
  ticket's payload); the staged tool registers nothing.
- **T2-07 fence:** the locations.json conflation fix is its OWN candidate. This ticket never
  edits `~/.config/appydave/locations.json` — the registry overlays exclusion rules on top of
  it, read-only.
- **No YLO/POEM work.** HALT/BACKOFF respected implicitly by the engine.

## Recon (verify before any work)

Docs lag code. Run every check; each replaces doc-trust. All grounded numbers below are
as-of 2026-07-06 — months may have passed; tolerances are stated per check.

1. `ls /Users/davidcruwys/dev/ad/apps/dark-factory/tools/activity-registry 2>&1` → expect
   "No such file or directory". If it exists → someone built this in a race → **Abort A1**.
2. Parse the source of truth:
   `python3 -c "import json; d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json')); locs=d['locations']; print(type(locs).__name__, len(locs), sorted(locs[0].keys()))"`
   → expect `list 134` (±15) and keys including `key`, `path`, `type`. If `locations` is not a
   list of such dicts → the T2-07 conflation fix probably landed and reshaped it → **Fork F1**.
3. Record the read-only baseline hash (re-checked at Verification):
   `shasum /Users/davidcruwys/.config/appydave/locations.json` → note the hash. No expected
   value — this is your own tamper-check.
4. Type census: `python3 -c "import json,collections; d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json')); print(dict(collections.Counter(l.get('type') for l in d['locations'])))"`
   → expect roughly `product 35 · gem 22 · client 12 · tool 9 · video 8 · monorepo 6 · archive 6
   · reference 6 · site 5 · brain 4 · docs 4 …` and, critically, that the exclusion types
   `config`/`archive`/`reference` exist (~13 entries). If those type names vanished →
   re-derive the exclusion set from what exists and document the mapping in the spec §2 —
   do not abort.
5. Missing-path count:
   `python3 -c "import json,os; d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json')); m=[l['key'] for l in d['locations'] if not os.path.isdir(os.path.expanduser(l['path']))]; print(len(m), m)"`
   → expect ≤ 3 (exactly 1 at authoring: `awb-team`). If > 10 are missing you are on the wrong
   machine or the config is broken → **Abort A3**.
6. `git -C /Users/davidcruwys/dev/ad/brains rev-parse --show-toplevel` → expect
   `/Users/davidcruwys/dev/ad/brains` (brains is ONE git repo; the 4 brain-keyed locations
   entries must collapse into a single target). If brains is not a git repo → treat brains as
   a dir target instead; record the change in spec §2; do not abort.
7. Off-registry ground truth — run this and KEEP the output (it calibrates Moves 2 and 4):
   `python3 -c "
import json,os
d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json'))
reg={os.path.realpath(os.path.expanduser(l['path'])) for l in d['locations']}
for root,depth in [('/Users/davidcruwys/dev/clients',2),('/Users/davidcruwys/dev/ad/apps',1)]:
    for dp,dns,fns in os.walk(root):
        rel=os.path.relpath(dp,root)
        lvl=0 if rel=='.' else rel.count(os.sep)+1
        if lvl>=depth: dns[:]=[]
        if '.git' in dns or os.path.isdir(os.path.join(dp,'.git')):
            if os.path.realpath(dp) not in reg: print('OFF-REGISTRY', dp)
            dns[:]=[]
"` → at authoring this printed **11** repos: 6 under clients (`supportsignal-sentinal`,
   `kiros-portal-poc`, `kiros-quality-portal`, `kiros-sentinal`, `chiangmai-ai/community`,
   `lars-projects/growth-intelligence`) and 5 under apps (`appyradar-sentinal`,
   `appyradar-sentinel`, `suborch-demo`, `switchboard`, `watchtower`). Any count ≥ 1 is fine
   (repos get registered over time — shrinkage is success, not failure). Count 0 → still
   proceed; Move 6's dummy probe is then the only discovery proof.
8. `ls /Users/davidcruwys/dev/ad/apps/app-registry/query.py /Users/davidcruwys/dev/ad/apps/app-registry/store/registry.json`
   → expect both (the probe/query + committed-store idiom you will copy). If missing, proceed
   anyway — the idiom is fully specified in Move 1; note the absence in the spec.
9. `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/queue/.CONVENTION.md` exists,
   and `cat engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json | python3 -m json.tool > /dev/null && echo ok`
   → expect `ok` — this deferred ticket is the shape precedent for Move 9 (`priority` +
   `status: "deferred"` + `deferred_reason`). If that ticket is gone (undeferred/moved), the
   shape is still binding — it is restated fully in Move 9.
10. Timing baseline — the dedupe pass over every locations path:
    `time python3 -c "
import json,os,subprocess
d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json'))
n=0
for l in d['locations']:
    p=os.path.expanduser(l['path'])
    if os.path.isdir(p) and subprocess.run(['git','-C',p,'rev-parse','--show-toplevel'],capture_output=True).returncode==0: n+=1
print(n,'git paths')
"` → expect ~100 git paths in well under 60s. If it takes > 5 minutes → **Fork F2**.

## Moves

1. **Do:** Build `tools/activity-registry/sweep.py` (stdlib only: `json os sys subprocess
   argparse time platform`). Pin the algorithm exactly:
   **Universe assembly** — (i) read `~/.config/appydave/locations.json` → `d["locations"]`;
   (ii) drop entries with `type` in `{"config","archive","reference"}`; (iii) drop entries
   whose path doesn't exist (count into `meta`); (iv) discovery scan the roots
   `~/dev/clients` (max depth 2) and `~/dev/ad/apps` (max depth 1) — exactly the Recon-7
   walker: a dir containing `.git` is a repo, never descend INTO a found repo, skip hidden
   dirs; repos whose realpath is not covered by any locations entry are targets with
   `"off_registry": true`; off-registry NON-git dirs are not targets — list their paths in
   `meta.off_registry_dirs` for human review; (v) resolve every survivor: if
   `git -C <path> rev-parse --show-toplevel` succeeds → git target keyed by realpath of the
   toplevel, MERGING duplicates (collect all contributing locations keys into
   `"locations_keys": [...]` — brains' 4 keys and flivideo/flivoice must collapse); (vi)
   remaining non-git paths: if the path is an ancestor of any other target's path → classify
   as group dir (record in `meta.group_dirs`, no scan — prevents double counting); else → dir
   target.
   **Per git target** (each subprocess `timeout=15`, whole target wrapped in try/except →
   failures append `{path, stage, err}` to `meta.errors`, never kill the sweep):
   `git log -1 --format=%ct|%s` → `last_commit_ts`, `last_subject`;
   `git log --since=<window-start ISO> --oneline` line count → `commits_in_window`;
   `git status --porcelain` line count → `dirty_files`.
   **Per dir target:** `os.walk` pruning hidden dirs, `node_modules`, `vendor`,
   `__pycache__`, capped at 20,000 files → `latest_mtime_ts`, `files_changed_in_window`.
   **Target fields:** `id` (the locations key whose path == the toplevel, shortest if several;
   else basename; on collision append `-2`), `path`, `kind` (`git`|`dir`), `type` (from
   locations, else null), `locations_keys`, `off_registry`, `source` (`locations`|`scan`),
   `last_activity_ts` (git: `last_commit_ts`; dir: `latest_mtime_ts`), `active`
   (`commits_in_window > 0 or dirty_files > 0 or files_changed_in_window > 0`), plus the
   per-kind fields above.
   **Output:** `store/activity.json` = `{"meta": {swept_at, window_hours, machine
   (platform.node()), duration_s, counts {locations_entries, excluded_by_type, missing_paths,
   git_targets, dir_targets, group_dirs, off_registry_git, errors}, off_registry_dirs,
   group_dirs, errors}, "targets": [ ... sorted by last_activity_ts desc ]}`. CLI:
   `python3 sweep.py [--hours N]` (default 24), prints the meta counts line to stdout, exit 0.
   **Expect:** `python3 -m py_compile tools/activity-registry/sweep.py` exits 0.
   **Failure signal:** compile error.
   **Counter-move:** fix and recompile; this move has no external state.

2. **Do:** First full sweep: `cd /Users/davidcruwys/dev/ad/apps/dark-factory && python3 tools/activity-registry/sweep.py --hours 24`.
   **Expect:** exit 0 in < 180s; `store/activity.json` written; meta counts sane against
   recon: `git_targets` ≈ 95–115, `off_registry_git` ≥ the Recon-7 count minus any since
   registered, `errors` ≤ 5, `group_dirs` includes the known parents (`dev`, `ad`, `apps`,
   `clients`, `gems`, `ss`, `voz` were the authoring-time ancestors).
   **Failure signal:** crash, hang, or `errors` > 20% of targets.
   **Counter-move:** a hang means a subprocess without its timeout — audit every
   `subprocess.run` for `timeout=15`; a crash on one target means the try/except wrapper is
   leaky — wrap tighter and re-run. If after both fixes > 20% of targets still error →
   **Abort A4**.

3. **Do:** Truth spot-checks against independently computed values:
   (i) `python3 -c "import json,subprocess; a=json.load(open('tools/activity-registry/store/activity.json')); t=[x for x in a['targets'] if x['path'].endswith('/apps/dark-factory')][0]; real=int(subprocess.run(['git','-C',t['path'],'log','-1','--format=%ct'],capture_output=True,text=True).stdout.strip()); assert t['git']['last_commit_ts']==real,(t['git']['last_commit_ts'],real); print('dark-factory ts ok')"`
   (ii) brains dedupe: `python3 -c "import json; a=json.load(open('tools/activity-registry/store/activity.json')); b=[x for x in a['targets'] if x['path']=='/Users/davidcruwys/dev/ad/brains']; assert len(b)==1, len(b); assert len(b[0]['locations_keys'])>=2, b[0]['locations_keys']; print('brains collapsed:', b[0]['locations_keys'])"`
   (iii) re-run with `--hours 168` and confirm ≥ 5 targets have `"active": true` (David's
   week always touches ≥ 5 repos; if genuinely fewer, print the active list and eyeball —
   an empty list is the failure, not a small one).
   **Expect:** all three print their ok lines.
   **Failure signal:** any assertion fires.
   **Counter-move:** (i) failing → your `%ct` parse or target keying is wrong; (ii) failing →
   toplevel realpath dedupe is broken (likely symlink: brains has a known symlink alias —
   always `os.path.realpath` the toplevel before keying); (iii) empty → your `--since`
   ISO format is wrong (use `datetime.utcfromtimestamp(start).isoformat()`); fix and re-run
   Move 2. Second consecutive failure of the same check → **Abort A4**.

4. **Do:** Build `tools/activity-registry/query.py` — reads `store/activity.json` ONLY, never
   sweeps (the app-registry idiom). Commands, each printing clean JSON to stdout:
   `since --hours N` (targets with `last_activity_ts` ≥ now−N·3600, plus any with
   `dirty_files > 0`), `active --days N` (same, N·86400), `off-registry` (targets with
   `off_registry == true`), `target <id>` (one full record), `all`. No args → usage + exit 1.
   **Expect:** `python3 tools/activity-registry/query.py off-registry` lists the Recon-7
   repos (e.g. switchboard, watchtower) or `[]` if Recon 7 found zero;
   `python3 tools/activity-registry/query.py since --hours 24 | python3 -m json.tool` parses.
   **Failure signal:** query output disagrees with a direct
   `python3 -c "..."` filter over activity.json (run one as a cross-check).
   **Counter-move:** fix the filter; query.py holds zero logic beyond filtering — if you are
   tempted to make it re-sweep or mutate state, stop (see Executor notes).

5. **Do:** Idempotence: run `python3 tools/activity-registry/sweep.py --hours 24` a second
   time, unchanged.
   **Expect:** exit 0; target count within ±2 of Move 2's run; `store/activity.json` is
   overwritten in place (no `activity-2.json`, no append).
   **Failure signal:** count drift > 2 (nondeterministic universe assembly) or a second file.
   **Counter-move:** drift usually means unsorted set iteration leaking into inclusion
   decisions — assembly must be pure-functional over the same inputs; fix, re-run Moves 2–5.

6. **Do:** Live discovery proof (the T1-04 dummy-file pattern, adapted): create a throwaway
   repo at depth 2 under a clients scan root —
   `mkdir -p /Users/davidcruwys/dev/clients/kiros/wg-t2-02-dummy-probe && cd $_ && git init -q && echo probe > probe.txt && git add -A && git -c user.email=probe@wg -c user.name=wg commit -qm probe` —
   then re-sweep (`--hours 24`) and query.
   **Expect:** `query.py off-registry` now includes `wg-t2-02-dummy-probe` with
   `"active": true` (its commit is minutes old); `query.py since --hours 24` includes it.
   **Failure signal:** the dummy is absent from targets.
   **Counter-move:** your depth accounting is off (kiros nests repos at depth 2 —
   `clients/kiros/<repo>`); fix the walker against the Recon-7 reference implementation and
   re-sweep. If it still cannot see the dummy after the walker matches Recon 7 verbatim →
   **Abort A4**.
   **Cleanup (mandatory, same move):**
   `rm -rf /Users/davidcruwys/dev/clients/wg-t2-02-dummy-probe 2>/dev/null; rm -rf /Users/davidcruwys/dev/clients/kiros/wg-t2-02-dummy-probe`,
   re-sweep once, and confirm the dummy is gone from `store/activity.json`. Zero probe
   residue may remain in any client directory.

7. **Do:** Write the design spec `docs/activity-registry-design.md` with EXACTLY these
   sections: **§1 Problem** (the project-list-isn't-known evidence: one digest config,
   app-registry's ~42-app lens, the Recon-7 off-registry list you actually measured — real
   numbers from YOUR run, not authoring's); **§2 Universe rules** (the assembly algorithm as
   built, incl. type-exclusion set, group-dir rule, discovery roots as a config constant,
   dedupe-by-realpath-toplevel); **§3 Data model** (the activity.json shape, field by field);
   **§4 CLI contract** (sweep/query commands, the query-never-sweeps law); **§5 Home —
   recommendation and variant** (recommended: standalone app `~/dev/ad/apps/activity-registry`
   at promotion, per the different-charter argument vs app-registry's curated factory lens;
   PLUS a short "fold-in variant" mapping what changes if David rules it becomes a second
   probe inside app-registry — so a reversal loses no work); **§6 Non-goals** (edits to
   locations.json = T2-07 · digest integration = T2-04 · per-brain granularity = T2-10 ·
   cross-machine/Roamy = T10 · daemon/cron scheduling = explicitly out until David asks);
   **§7 Known imprecisions** (dirty files don't advance `last_activity_ts`; mtime scans are
   capped; upgrade paths named); **§8 Ratification** — verbatim final line:
   `Ratification: PENDING (David — flip to RATIFIED and un-defer the promotion ticket in engine/store/queue/)`.
   **Expect:** file exists; `grep -c "Ratification: PENDING" docs/activity-registry-design.md` → 1.
   **Failure signal:** missing sections or marker.
   **Counter-move:** add them; the section list is the contract.

8. **Do:** Two small doc touches: (i) `tools/activity-registry/README.md` — operator manual
   (what it is, one-line run + query examples, the staged-not-promoted status pointing at the
   spec §5 and the deferred promotion ticket); (ii) append ONE line to the dependency-chain
   item 1 in `docs/morning-briefing-vision.md` (the dark-factory copy ONLY — a twin exists in
   `~/dev/ad/apps/project-digest/docs/`; leave it to T2-04, note the twin in your result
   notes): ` **→ STAGED 2026-XX-XX** (tools/activity-registry/ + docs/activity-registry-design.md, awaiting ratification — wg-t2-02)`
   with the real date.
   **Expect:** README exists; `git diff docs/morning-briefing-vision.md` shows exactly one
   changed line.
   **Failure signal:** the vision doc diff is more than one line.
   **Counter-move:** `git checkout -- docs/morning-briefing-vision.md` and redo as a pure
   one-line suffix.

9. **Do:** Stage the follow-on promotion ticket. Write
   `engine/store/queue/<UTC-stamp>-activity-registry-promotion.json` (stamp via
   `date -u +%Y%m%dT%H%MZ`) with exactly this shape (the deferred-ticket precedent from
   Recon 9):
   ```json
   {
     "ticket": "<UTC-stamp>-activity-registry-promotion",
     "kind": "instruction",
     "title": "activity-registry: promote staged tool to ~/dev/ad/apps + register at birth",
     "source": "backlog/wargames/T2-02-activity-registry.md (move 9) + docs/activity-registry-design.md",
     "executor": "unassigned",
     "priority": "normal",
     "requested_at": "<real UTC now, date -u +%Y-%m-%dT%H:%M:%SZ>",
     "requested_by": "wg-t2-02-activity-registry (war-game portfolio 2026-07-06)",
     "depends_on": [],
     "prompt": "PRECONDITION — read docs/activity-registry-design.md §8: if the marker still says 'Ratification: PENDING', park this ticket to engine/store/needs-decision/ asking David to ratify or amend the spec, and stop. Once RATIFIED: promote tools/activity-registry/ out of dark-factory to ~/dev/ad/apps/activity-registry/ per spec §5 (or per the §5 fold-in variant if David amended the home), then register at birth per the standing rule: locations.json entry (list schema), app-registry seed, constellation map, ad/CLAUDE.md apps table. Remove the staged copy from dark-factory tools/ (leave a one-line pointer in tools/README or the spec). Commit and push every touched repo.",
     "verify": "New home exists and both `python3 sweep.py --hours 24` and `python3 query.py since --hours 24` run clean from it; locations.json contains the new key; dark-factory tools/activity-registry/ is gone (pointer only); if unratified instead: a needs-decision file exists and nothing was promoted.",
     "status": "deferred",
     "deferred_reason": "Awaiting David's ratification of docs/activity-registry-design.md §8 (flip PENDING → RATIFIED, then clear this field and set executor to swagger)."
   }
   ```
   **Expect:** `python3 -m json.tool` parses it; it sits in queue/ exactly like the
   `20260704T0630Z` deferred precedent.
   **Failure signal:** JSON invalid, or you find yourself performing the promotion now.
   **Counter-move:** fix the JSON; the promotion itself is hard-fenced out of this ticket.

10. **Do:** Commit and push dark-factory (the ONLY repo this ticket touches). Stage:
    `tools/activity-registry/` (sweep.py, query.py, README.md, `store/activity.json` — the
    committed-store precedent is app-registry's tracked `store/registry.json`),
    `docs/activity-registry-design.md`, the one-line `docs/morning-briefing-vision.md` edit,
    and the queue ticket. Message:
    `feat(t2-02): universal activity registry — staged sweep+query, design spec, deferred promotion ticket`.
    **Expect:** `git push` succeeds; `git status --porcelain` afterwards shows nothing of
    yours left.
    **Failure signal:** push rejected (remote ahead).
    **Counter-move:** `git pull --rebase` then push; on a conflict in a file you touched,
    resolve keeping both intents; on a conflict in a file you did NOT touch → **Abort A5**.

## Forks

**F1 — locations.json reshaped (T2-07 landed first).**
Trigger: Recon 2 finds `locations` is not a list of `{key, path, type}` dicts.
→ **Route A** (fields recognizable under new names/nesting — e.g. split into
`repos`/`apps`/`ports` sections): adapt the reader to the new shape, and document the exact
mapping in spec §2 with a dated note; everything downstream is unchanged.
→ **Route B** (shape unrecognizable — you cannot find a path+type-bearing list anywhere in
the file): **Abort A2**; never guess a schema.

**F2 — sweep pathologically slow (> 5 min).**
Trigger: Recon 10's baseline or Move 2's run blows the 180s budget badly.
→ **Route A** (broad slowness): add a `ThreadPoolExecutor(max_workers=8)` over the per-target
probes (each already an independent subprocess; the assembly stays serial), re-run — this is
the only concurrency permitted in the tool.
→ **Route B** (one or two paths hang — network mount / dead volume): exclude those paths,
record them in `meta.errors` with `stage: "hang"`, and continue; name them in the result notes.

## Assumptions ledger

1. **Home = staged in dark-factory `tools/`, standalone app at promotion (not folded into
   app-registry).** Plausible: the design-lint staging precedent is explicit in CLAUDE.md, and
   app-registry's charter is a curated ~42-app factory lens with layers/verdicts — a different
   data model and cadence from a whole-universe activity sweep. If David rules "fold into
   app-registry" at ratification → the deferred promotion ticket gets re-pointed; spec §5's
   fold-in variant exists precisely so nothing is lost. No abort needed.
2. **"Active" = commits in window OR dirty files (OR changed files for dir targets).**
   Plausible: matches morning-briefing-vision's "what changed since yesterday" and catches
   David's uncommitted brain edits via `dirty_files`. If David wants finer signal (per-brain
   file lists, per-file diffs) that is T2-10's territory — note in §6, don't build.
3. **`store/activity.json` is committed to git.** Precedent: app-registry tracks
   `store/registry.json` (verified 2026-07-06 via `git ls-files`). If churn annoys at review,
   gitignoring it is a one-line follow-up, not a blocker.
4. **Discovery roots `~/dev/clients` (depth 2) + `~/dev/ad/apps` (depth 1) cover the known
   blind spots.** Plausible: authoring recon found all 11 off-registry repos exactly there,
   and every other populated area (kgems, flivideo, brains) is registered. Roots are a config
   constant in sweep.py + spec §2, so extending is trivial. If David names more roots at
   ratification → promotion ticket scope, not a redo.
5. **No concurrent work on this seam.** Recon 1 (tool exists) and Recon 2 (schema drift)
   catch the two plausible races → A1 / F1 rather than merge-by-guess.

## Abort conditions

Park action for all: write `engine/store/needs-decision/wg-t2-02-activity-registry.json` as
`{"ticket": "wg-t2-02-activity-registry", "question": "<per-abort text>", "observed": "<what you actually found>"}`,
leave the ticket in `running/`, stop. Never guess past an abort.

- **A1 — `tools/activity-registry/` already exists.** Question: "activity-registry already
  staged (found: <file list, dates>). Verify-and-close this war game against the existing
  build, or rebuild per the spec?"
- **A2 — locations.json unrecognizable** (Fork F1 Route B). Question: "locations.json no
  longer contains a recognizable path+type list (T2-07 reshape?). The universe reader needs a
  re-spec against the new schema. Proceed how?" Include the file's top-level keys in
  `observed`.
- **A3 — >10 locations paths missing on disk.** Question: "locations.json disagrees with this
  machine's filesystem at scale — wrong machine (this must run on mac-mini-m4) or stale
  config. Sweep results would be garbage. Proceed how?"
- **A4 — >20% of git targets error after counter-moves, or a truth spot-check /
  discovery proof fails twice.** Question: "the sweep cannot produce trustworthy numbers
  (<which check> failed twice; error sample attached). Environment or schema has drifted from
  the war game's grounding. Re-recon or re-spec?"
- **A5 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
# 1. Staged tool exists and runs clean, twice, fast
ls tools/activity-registry/sweep.py tools/activity-registry/query.py tools/activity-registry/README.md
time python3 tools/activity-registry/sweep.py --hours 168     # exit 0, < 180s
python3 tools/activity-registry/sweep.py --hours 24           # exit 0 (idempotent re-run)

# 2. The artifact answers the mission question
python3 - <<'EOF'
import json, time
a = json.load(open("tools/activity-registry/store/activity.json"))
m, t = a["meta"], a["targets"]
assert m["counts"]["git_targets"] >= 90, m["counts"]
assert m["counts"]["errors"] <= 0.2 * len(t), m["counts"]
assert time.time() - time.mktime(time.strptime(m["swept_at"][:19], "%Y-%m-%dT%H:%M:%S")) < 86400
b = [x for x in t if x["path"] == "/Users/davidcruwys/dev/ad/brains"]
assert len(b) == 1 and len(b[0]["locations_keys"]) >= 2, b   # dedupe proof
assert all("last_activity_ts" in x and "active" in x for x in t)
print("activity.json ok:", len(t), "targets,", m["counts"]["off_registry_git"], "off-registry")
EOF
python3 tools/activity-registry/query.py since --hours 168 | python3 -c "import json,sys; d=json.load(sys.stdin); assert len(d)>=1, d; print('since ok:', len(d))"
python3 tools/activity-registry/query.py off-registry | python3 -m json.tool > /dev/null && echo off-registry-ok

# 3. Design spec + deferred promotion ticket staged
grep -c "Ratification: PENDING" docs/activity-registry-design.md          # → 1
for s in "Universe rules" "Data model" "CLI contract" "Home" "Non-goals"; do grep -q "$s" docs/activity-registry-design.md || echo "MISSING: $s"; done
ls engine/store/queue/*activity-registry-promotion.json | wc -l           # → 1
python3 -c "import json,glob; t=json.load(open(glob.glob('engine/store/queue/*activity-registry-promotion.json')[0])); assert t['status']=='deferred' and t['kind']=='instruction', t; print('promotion ticket staged, deferred')"

# 4. Negative checks — what must NOT have changed
shasum ~/.config/appydave/locations.json      # → identical to the hash recorded at Recon 3
git -C /Users/davidcruwys/dev/ad/apps/app-registry status --porcelain | grep -c "" | grep -qx 0 && echo app-registry-untouched   # or: none of ITS files touched by you
ls /Users/davidcruwys/dev/clients/kiros/ | grep -ci dummy                 # → 0 (probe cleaned)
ls /Users/davidcruwys/dev/ad/apps/activity-registry 2>&1 | grep -c "No such"   # → 1 (promotion NOT done)
git diff HEAD~1 --stat -- docs/morning-briefing-vision.md | grep -c "1 +"      # one-line annotation only

# 5. Committed and pushed
git log --oneline -1        # shows the t2-02 commit
git status --porcelain      # empty
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT touch: `~/.config/appydave/locations.json` or `apps.json`
  (read-only — the conflation fix is T2-07); anything in `~/dev/ad/apps/app-registry/` or
  `~/dev/ad/apps/project-digest/` (T2-04 wires the digest in later); `engine/orchestrator.py`
  / `wake.py`; any client repo except the Move-6 dummy (created and destroyed in one move);
  and do NOT create `~/dev/ad/apps/activity-registry/` — promotion is the deferred ticket's
  job, after David ratifies.
- **The rabbit hole: scheduling.** A sweep begs to become a launchd/cron job feeding the
  briefing automatically. Skip it entirely — cadence is a standing commitment that needs
  David's explicit go (unknowns-map §B), and T2-04 owns the consumption side. The tool is
  run-on-demand; one sentence in README saying so is enough.
- **Second rabbit hole: enriching targets.** No ports, no liveness, no verdicts, no README
  parsing — that is app-registry's charter. This tool answers one question (what changed,
  where, when) with ~8 fields per target. If a field doesn't serve "what changed since
  yesterday", it doesn't ship.
- **Style:** stdlib only; probe/query split copied from app-registry (`query.py` never
  sweeps, `sweep.py` never filters); every subprocess call carries `timeout=15`; every
  per-target probe wrapped so one bad repo can never kill the sweep; `os.path.realpath`
  before any dedupe comparison (brains reaches through a symlink alias).
- **Prefer parking over guessing** on any locations.json shape surprise (F1/A2) and on any
  sign someone already built this (A1). A parked question costs minutes; a second
  half-compatible activity registry costs the whole premise of the ticket.
