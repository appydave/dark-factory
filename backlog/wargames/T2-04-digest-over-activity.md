# T2-04 — Digest-over-activity

| field | value |
|---|---|
| ticket | wg-t2-04-digest-over-activity |
| track / size / priority | T2 Producer/BA / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t2-02-universal-activity-registry |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Make the morning briefing iterate **what actually changed** instead of a hand-config list.
Today `~/dev/ad/apps/project-digest/digest.py` (its OWN git repo, `appydave/project-digest` —
NOT inside dark-factory) briefs exactly one hand-configured project per invocation
(`projects/<id>.json` is the entry ticket). This ticket adds `digest.py --active`: it asks
T2-02's universal activity registry "what changed since yesterday, everywhere", renders the
existing full briefing box for each **changed project that has a config file**, and a compact
one-line "ALSO ACTIVE" entry for every changed path that doesn't — so per-project config becomes
an **override/richness dial**, not the entry ticket (canonical framing:
`docs/morning-briefing-vision.md` step 2 of the dependency chain, in THIS repo, dark-factory).
Done looks like: `python3 digest.py --active --no-write` prints a multi-project briefing driven
by real registry output; `python3 digest.py dark-factory --format md --no-write` behaves exactly
as before (the daily briefing must not break); both repos committed and pushed; the vision doc's
step 2 marked done.

**Locked design (no taste calls left open):**
- New adapter seam `lib/activity.py` wraps the registry via subprocess + JSON with graceful
  degradation — copy the exact pattern of `lib/live.py` (which wraps app-registry's `query.py`).
- Two tiers: full briefing box **only** for changed projects with a `projects/<id>.json`
  (absorption law — a wall of 30 synthesized boxes is noise); compact line for everything else.
- Compact tier: display path + name (basename) + change summary; capped at 20 entries with a
  final `… +N more` line; writes NO state, needs NO id.
- `last-briefing` store writes: full tier only, same semantics as a single run; `--no-write`
  skips them exactly as today.
- Single-project mode stays byte-path identical: positional `project` becomes optional
  (`nargs="?"`), `--active` added; error out if both or neither given.

## Locked context

- Q4 (decisions.md): everything through the engine — this ticket is written for sonnet Swagger
  dispatch. No `-p`/headless/SDK ever; interactive `claude` only.
- decisions.md D-parked defaults: this ticket **complements, doesn't replace** — extend
  project-digest in place; do not fork a new briefing app.
- morning-briefing-vision.md dependency chain is the binding build order: registry (T2-02) →
  digest-over-activity (THIS) → feed layer (T2-05, NOT this ticket) → life feeds (out of scope).
- Ticket-first convention (`engine/store/queue/.CONVENTION.md`): this work moves
  queue/ → running/ → done/ in dark-factory's engine store; results JSON per dispatch wrapper.

## Recon (verify before any work)

Paths are absolute where cross-repo (you will be dispatched with cwd in dark-factory but the code
lives in project-digest). Authoring-time state (2026-07-06) noted. Docs lag code — trust these
checks, not prose.

1. **The registry exists and is locatable.** In dark-factory:
   `ls engine/store/done/ | grep -i "t2-02"` and `ls engine/store/results/ | grep -i "t2-02"` —
   read the results JSON for the paths it built. Independently:
   `ls ~/dev/ad/apps/ | grep -i "activ"` (authoring time: NO such app exists — the registry is
   entirely future work) and `grep -rl "activity registry" ~/dev/ad/apps/*/README.md 2>/dev/null`.
   If T2-02's done ticket names a different home (it may live inside app-registry or
   project-digest itself), that home wins. Found nowhere → **Abort A1**.
2. **The registry is runnable and answers "changed since".** Read the registry's README/CONTEXT
   for its query command; do NOT guess flags. Run the documented "what changed" query once,
   read-only. Machine-readable (JSON) output with per-path entries → good, note the exact command
   and field names for Move 1. Output exists but isn't JSON → **Fork F1**. Store empty / never
   swept → **Fork F3**. No such query at all → **Abort A1**.
3. **project-digest is intact at its known seams.**
   `ls ~/dev/ad/apps/project-digest/lib/` → expect `activity.py` ABSENT (you create it) and
   `config.py`, `assemble.py`, `live.py`, `box.py`, `render_md.py`, `view.py`, `store.py` present.
   `grep -n "list_project_ids\|def load_config" ~/dev/ad/apps/project-digest/lib/config.py` →
   expect both (were lines 42/46). `grep -n 'add_argument("project"' ~/dev/ad/apps/project-digest/digest.py`
   → expect the required positional (was line 31). Any of these gone → the app was refactored
   since authoring → re-read `digest.py` + `lib/config.py` fully and adapt move details to the
   current shape; if the app no longer resembles a per-project digest at all → **Abort A2**.
4. **Baseline single-project run is green.**
   `python3 ~/dev/ad/apps/project-digest/digest.py dark-factory --format md --no-write > "$SCRATCH/baseline.md"; echo $?`
   → expect exit 0 and `grep -c "^## " "$SCRATCH/baseline.md"` ≥ 5 (GOAL, NEEDS YOU, SINCE YOU
   LAST LOOKED, IN FLIGHT, SHIPPED RECENTLY…). Non-zero exit or empty output → the app is broken
   BEFORE your change → **Abort A2**. (`$SCRATCH` = any temp dir you own; keep it out of both repos.)
5. **Config inventory.** `ls ~/dev/ad/apps/project-digest/projects/` → authoring time: exactly
   `dark-factory.json`. More configs present (T2-03 may have onboarded project #2) → fine, they
   simply become additional full-tier candidates; note them.
6. **`--list` flag state.** `grep -n "\-\-list\|--projects" ~/dev/ad/apps/project-digest/digest.py`
   → authoring time: absent (that's T2-03 / the deferred queue ticket's job). Present → fine,
   coexist with it; either way do NOT build or modify `--list` here.
7. **project-digest git state.** `cd ~/dev/ad/apps/project-digest && git remote -v && git status --short`
   → expect origin `appydave/project-digest`; a pre-existing modified `view/dark-factory.html` is
   EXPECTED and harmless (the HTML view regenerates on every run, even `--no-write` — verified in
   `digest.py` source 2026-07-06). Other uncommitted changes to `lib/` or `digest.py` → someone
   left work in flight → **Abort A5** (don't build on an unknown diff).
8. **Deferred ticket untouched-check baseline.** In dark-factory:
   `ls engine/store/queue/ | grep project-digest-list` → may or may not still exist (T2-03 may
   have drained it). Record what you see; your negative check later is only that YOU didn't
   change it.

## Moves

1. **Pin the registry adapter contract.**
   - **Do:** From Recon 2's working query command, capture one real run:
     `<registry-query-cmd> > "$SCRATCH/registry-sample.json"`. Write down (in a comment block you
     will paste at the top of `lib/activity.py`): the exact command, the JSON shape, and the
     mapping to the adapter's output — for each entry: `path` (absolute), `name` (basename of
     path if the registry gives no name), `kind` (git/mtime/whatever field the registry uses to
     say HOW it detected change), `summary` (its human-readable change line, e.g. "12 commits" /
     "3 files touched"), `last_change_ts` (if present, else null). Apply Fork F2 here for the
     "since" semantics.
   - **Expect:** a saved sample with ≥ 1 changed-path entry (dark-factory itself commits daily —
     the sweep should always see SOMETHING within 24 h) and an unambiguous field mapping.
   - **Failure signal:** sample parses but has zero entries, or fields don't identify a
     filesystem path.
   - **Counter-move:** zero entries → **Fork F3**. No path field → re-read the registry README
     once for an alternate query mode; still nothing → **Abort A1**.

2. **Build `lib/activity.py` (the seam that isolates registry drift).**
   - **Do:** Create `~/dev/ad/apps/project-digest/lib/activity.py` modeled line-for-line on
     `lib/live.py`'s pattern (module docstring naming the wrapped tool; absolute path constant to
     the registry query; `subprocess.run` with `timeout=30`, `capture_output=True, text=True`;
     graceful degradation). One public function:
     `changed_since(since_hours=24) -> {"entries": [...], "since_ts": "<iso>", "error": None|str}`
     where each entry is the Move-1 mapped dict. Registry missing / timeout / bad JSON → return
     `{"entries": [], "error": "<one line>"}` — never raise. Smoke it:
     `cd ~/dev/ad/apps/project-digest && python3 -c "from lib import activity; r = activity.changed_since(); print(r['error'], len(r['entries']))"`
   - **Expect:** prints `None <n>` with n ≥ 1.
   - **Failure signal:** traceback, or `error` non-None with the registry demonstrably up
     (Recon 2 worked).
   - **Counter-move:** diff your subprocess invocation against the exact Recon-2 command line
     (cwd matters if the registry resolves its store relatively — pass `cwd=<registry app dir>`
     if so). One fix attempt; still failing → **Fork F1 Route B** (read the registry's store
     files directly).

3. **Config-override resolution in `lib/config.py`.**
   - **Do:** Add `resolve_override(path)` → iterate `PROJECTS_DIR.glob("*.json")` (reuse `_read`),
     return the first cfg whose resolved `path` equals the resolved input path, else `None`.
     (This is the same matching logic `load_config` branch 3 already uses — factor it, don't
     duplicate: have branch 3 call `resolve_override`.) Smoke:
     `python3 -c "import sys; sys.path.insert(0,'/Users/davidcruwys/dev/ad/apps/project-digest'); from lib import config; print(config.resolve_override('/Users/davidcruwys/dev/ad/apps/dark-factory')['id']); print(config.resolve_override('/tmp'))"`
   - **Expect:** `dark-factory` then `None`.
   - **Failure signal:** exception, or dark-factory not matched (path resolution mismatch,
     e.g. symlinks).
   - **Counter-move:** compare `str(Path(p).resolve())` on both sides (exactly what branch 3
     does today — reuse it verbatim). Second failure → **Abort A2** (the existing matching seam
     itself is broken; that predates you).

4. **Assemble the active briefing (`lib/active.py`).**
   - **Do:** New module with `build(since_hours=24, write=True)`:
     (a) call `activity.changed_since(since_hours)`; (b) for each entry, `config.resolve_override(entry["path"])`;
     (c) matched → run the EXISTING `assemble.build(cfg, write=write)` (full digest, unchanged
     semantics, last-briefing write included unless `write=False`) into a `projects` list, each
     with its `recommend_focus` line; (d) unmatched → append the compact entry dict to
     `also_active` (no state written, no id needed); (e) return
     `{"generated_at": <store.now_iso()>, "since_ts": ..., "registry_error": ..., "projects": [...], "also_active": [...], "also_active_total": <n before cap>}`
     with `also_active` capped at 20. Smoke:
     `python3 -c "... from lib import active; r = active.build(write=False); print(len(r['projects']), r['also_active_total'])"`
   - **Expect:** `projects` length = number of configured projects the registry saw as changed
     (≥ 1 if dark-factory changed within the window — it almost always has); `also_active_total`
     = the rest.
   - **Failure signal:** dark-factory changed per the registry but lands in `also_active`
     (override resolution failed at scale), or an exception from `assemble.build` on a
     configured project.
   - **Counter-move:** the first is Move 3's bug — go back one move. The second: run that
     project through the single-project CLI to confirm it fails standalone too; if standalone
     also fails it's pre-existing → note it, exclude nothing, let the error surface honestly in
     the output (assemble's sources already degrade gracefully); if only-in-active fails, fix
     your call signature. Registry returns > 200 entries → **Abort A4**.

5. **CLI + renderers.**
   - **Do:** In `digest.py`: positional `project` → `nargs="?"`; add `--active` (store_true) and
     `--since-hours` (int, default 24; drop this flag entirely if Fork F2 Route B applied — never
     expose a knob that does nothing). Guard: `--active` with a project given, or neither flag
     nor project → `parser.error(...)`. `--active` path: `r = active.build(...)`; `--format json`
     → dump `r`; `--format md` → existing `render_md.render` per project, joined, then an
     `## ALSO ACTIVE (n)` section of `- <name> — <path> — <summary>` lines (+ `… +N more`);
     `--format box` (default) → existing `box.render` per project stacked, then a plain compact
     section in the same style. HTML views: keep per-project `view.render` for full-tier projects
     exactly as the single-project path does; no new index page. Run:
     `python3 digest.py --active --no-write` and `python3 digest.py --active --format json --no-write | python3 -m json.tool > /dev/null`.
   - **Expect:** exit 0 both; box output shows ≥ 1 full briefing box then an ALSO ACTIVE section;
     json parses.
   - **Failure signal:** argparse conflict with an existing flag (e.g. a `--list` that landed via
     T2-03), or renderers choke on being called in a loop (module-level state).
   - **Counter-move:** argparse conflict → rename nothing existing; adjust only your new flags.
     Renderer statefulness → wrap per-project calls, don't refactor `box.py`/`render_md.py`
     internals. If preserving single-project behavior forces a breaking change → **Abort A3**.
   - Note: `--active` without `--no-write` will bump `briefing_n` for each full-tier project —
     that is the intended semantic (identical to briefing them singly); don't "fix" it.

6. **Regression: the daily briefing is untouched.**
   - **Do:** `python3 digest.py dark-factory --format md --no-write > "$SCRATCH/after.md"; echo $?`
     then `diff <(grep "^## " "$SCRATCH/baseline.md") <(grep "^## " "$SCRATCH/after.md")` (section
     structure only — timestamps/counts legitimately drift between runs). Also re-check exit 0
     for `--format box` and `--format json`.
   - **Expect:** exit 0, empty structural diff.
   - **Failure signal:** missing section, nonzero exit, or a new mandatory-argument error on the
     old invocation shape.
   - **Counter-move:** fix forward once (it will be the argparse change); if a second attempt
     still breaks single-project mode → **Abort A3** (revert first — the daily briefing outranks
     this feature).

7. **Docs — both repos.**
   - **Do:** (a) project-digest `README.md`: add a `## --active (digest-over-activity)` usage
     section: the command, the two tiers, "config = override/richness dial, not entry ticket",
     the registry it consumes (name + path + the exact query command from Move 1), and the
     degradation behavior when the registry is absent. (b) dark-factory
     `docs/morning-briefing-vision.md`: in the "Dependency chain" list, annotate item 2:
     `**Digest-over-activity** — ✅ done <date> (wg-t2-04): digest.py --active, full boxes for configured projects, compact lines otherwise.`
     Do not rewrite anything else in either doc.
   - **Expect:** `grep -c "\-\-active" ~/dev/ad/apps/project-digest/README.md` ≥ 1;
     `grep -c "wg-t2-04" docs/morning-briefing-vision.md` = 1.
   - **Failure signal:** vision doc moved/renamed since authoring.
   - **Counter-move:** `grep -rn "Digest-over-activity" ~/dev/ad/apps/dark-factory/docs/` to find
     its new home; annotate there. Nowhere → add one line to your results-file note instead;
     don't create a new doc.

8. **Commit both repos, push, finish.**
   - **Do:** (a) `cd ~/dev/ad/apps/project-digest && git add -A && git status --short` — confirm
     the diff is ONLY: `lib/activity.py` (new), `lib/active.py` (new), `lib/config.py`,
     `digest.py`, `README.md`, and regenerated `view/*.html`. Commit:
     `feat(digest): --active — briefing iterates registry-detected change; config becomes an override (wg-t2-04)`
     and push. (b) `cd ~/dev/ad/apps/dark-factory && git add docs/morning-briefing-vision.md`,
     commit `docs: morning-briefing vision step 2 (digest-over-activity) done — wg-t2-04`, push.
     (c) write your dispatch results JSON (`engine/store/results/<your ticket>.json`) with
     status done, both commit shas, and one line noting how many full-tier vs compact-tier
     entries the first real `--active` run produced.
   - **Expect:** clean `git status` in both repos; both commits visible in `git log --oneline -1`.
   - **Failure signal:** push rejected (remote moved), or unexpected files in either diff.
   - **Counter-move:** `git pull --rebase` then push; a conflict in any file you did not author
     this session → stop rebasing, **Abort A5**. Unexpected files → `git checkout --` anything
     you didn't intend, re-check, then commit.

## Forks

**F1 — Registry interface shape.**
**Trigger:** Recon 2 / Move 2 — the registry exists but its query output isn't clean JSON, or the
CLI keeps failing under subprocess while working interactively.
**Route A** (CLI emits JSON): wrap the CLI — the adapter stays a subprocess call, zero coupling to
registry internals. Preferred; matches `lib/live.py` exactly.
**Route B** (no JSON CLI, but the registry keeps a readable store — JSON files on disk, the
app-registry `store/registry.json` pattern): read the newest store file(s) directly from
`lib/activity.py`; name the exact file path in the adapter docstring AND in README's --active
section as a declared coupling ("reads <path> directly — replace with its CLI when one exists").
If there is neither a JSON CLI nor a readable store → **Abort A1**.

**F2 — "Since" semantics.**
**Trigger:** Move 1 — does the registry query accept a since/window parameter?
**Route A** (it does): pass `since_hours` through; keep the `--since-hours` CLI flag.
**Route B** (fixed window, e.g. a hardwired "since yesterday" sweep): if entries carry a
`last_change_ts`, filter client-side in the adapter and keep the flag; if they don't, adopt the
registry's window as-is, DROP the `--since-hours` flag, and say so in README. Never fake a
filter.

**F3 — Registry present but never swept (empty store / zero entries).**
**Trigger:** Recon 2 or Move 1 returns zero changed paths — implausible on any day David worked
(dark-factory alone commits near-daily), so treat zero as "not swept", not "quiet day".
**Route A:** the registry README documents a sweep/refresh command → run it ONCE (it is
read-only over David's dirs by design — a sweep, not a mutation), re-query; entries appear →
proceed.
**Route B:** sweep command fails or still zero entries → the dependency landed in name only →
**Abort A1** with the sweep output as evidence.

## Assumptions ledger

- **T2-02's ticket id is `wg-t2-02-universal-activity-registry`.** Plausible: slug derived from
  its candidate title the same way every portfolio ticket is. False → the engine's depends_on
  gate never satisfies and this ticket never dispatches; David/promotion-script must fix the
  string in `tickets/T2-04.json` (flagged to David at authoring).
- **T2-02 lands a RUNNABLE registry, not just a design.** T2-02 is L-size and the portfolio spec
  says L ≈ design-first — its war game may produce a spec + follow-on build tickets, with
  `wg-t2-02` reaching done/ while no registry binary exists. Recon 1–2 exist precisely for this.
  False → **Abort A1** (the needs-decision question proposes waiting on the build ticket).
- **Registry entries expose at least a path + change summary; both git and non-git (mtime/brains)
  sources appear in one list.** Plausible: that's the T2-02 candidate's own one-line contract.
  Partially false (git-only) → proceed; the compact tier renders whatever exists and the gap is a
  T2-02 finding for your results note, not your fix.
- **`projects/` may have gained configs by execution time** (T2-03 onboards project #2).
  Plausible and welcome — more full-tier boxes; zero code impact.
- **Flag names `--active` / `--since-hours` were never put to David.** Defaults chosen here;
  renaming later is a one-line change. Don't park over naming.
- **Full-box-only-for-configured honors the absorption law.** If David wants synthesized full
  digests for unconfigured repos too, that's a later richness dial (note it in README as the
  obvious extension), not this ticket.

## Abort conditions

Every abort: write `engine/store/needs-decision/wg-t2-04-digest-over-activity.json` (in
dark-factory) as
`{"ticket": "wg-t2-04-digest-over-activity", "question": "<one sentence>", "proposed": "<your recommended answer>", "note": "<evidence paths>"}`,
leave this ticket in `running/` if engine-dispatched, and stop. Never guess past an abort.

- **A1 — no consumable registry.** Recon 1/2, Move 1, F1-neither, or F3 Route B: T2-02's
  artifact is absent, design-only, unrunnable, or emits nothing machine-consumable. Question:
  "T2-04 needs a runnable activity registry with machine-readable changed-since output; found
  <state>. Wait on a T2-02 build ticket, or should T2-04 build a minimal git-only sweep itself?"
- **A2 — project-digest broken or unrecognizable before any change.** Recon 3/4 or Move 3's
  second failure. Question: "digest.py fails at baseline / core seams gone — fix under a separate
  ticket before T2-04 re-runs?" Do not fix pre-existing breakage inside this ticket.
- **A3 — cannot add --active without breaking single-project mode.** Move 5/6 second failure.
  Revert all working-tree changes in project-digest first (`git checkout -- .` — safe: Recon 7
  guaranteed you started clean apart from the generated view), THEN park. Question: "--active
  conflicts structurally with single-project CLI — accept a breaking CLI change, or ship
  --active as a separate entrypoint script?"
- **A4 — pathological registry volume.** Move 4 sees > 200 changed paths — that's the
  locations.json conflation debt (T2-07) leaking through, not a briefing. Park with a 10-entry
  sample in the note. Question: "Registry returns <n> changed paths — cap/filter in the digest,
  or fix the registry's source list (T2-07) first?"
- **A5 — foreign work in the way.** Recon 7's unknown uncommitted diff, or Move 8's rebase
  conflict in a file you didn't author. Question: "project-digest has in-flight foreign changes
  (<files>) — rebase over them, discard them, or hold T2-04?"

## Verification

Run after completion. Single-project regression from the dark-factory root is checked via
absolute paths; --active checks run in project-digest.

```bash
cd ~/dev/ad/apps/project-digest

# 1. The new mode works end-to-end against the real registry:
python3 digest.py --active --no-write                                  # exit 0; ≥1 full box; ALSO ACTIVE section
python3 digest.py --active --format json --no-write | python3 -m json.tool | grep -c '"also_active"'   # → 1
python3 digest.py --active --format md --no-write | grep -c "^## ALSO ACTIVE"                           # → 1

# 2. The adapter degrades, never raises (registry unreachable simulation is NOT required;
#    just confirm the error seam exists):
grep -c '"error"' lib/activity.py                                      # ≥ 1 (graceful-degradation path present)

# 3. Single-project mode unchanged (the daily briefing):
python3 digest.py dark-factory --format md --no-write | grep -c "^## "  # ≥ 5 sections, exit 0
python3 digest.py dark-factory --format box --no-write > /dev/null && echo OK   # → OK

# 4. Docs + commits:
grep -c "\-\-active" README.md                                          # ≥ 1
grep -c "wg-t2-04" ~/dev/ad/apps/dark-factory/docs/morning-briefing-vision.md   # → 1
git log --oneline -3 | grep -c "wg-t2-04"                                # ≥ 1 (project-digest commit)
cd ~/dev/ad/apps/dark-factory && git log --oneline -5 | grep -c "wg-t2-04"      # ≥ 1 (docs commit)

# 5. Negative checks — what must NOT have changed:
grep -c "def build" ~/dev/ad/apps/project-digest/lib/assemble.py         # → 1 (assemble untouched at its seam)
ls ~/dev/ad/apps/project-digest/projects/ | grep -c dark-factory.json    # → 1 (no config deleted/renamed)
# The deferred/list ticket (if it still existed at recon): byte-identical — you never touched it.
git -C ~/dev/ad/apps/dark-factory diff --stat HEAD~1 -- engine/ | wc -l  # → 0 in your docs commit
```

Partial pass (Abort A1 with the registry missing/design-only): NO code changes committed, plus
`needs-decision/wg-t2-04-digest-over-activity.json` naming the exact registry state found. That
is a legitimate exit — this ticket must not build the registry itself.

## Executor notes (sonnet)

- **Two repos, one ticket.** Code + README → `~/dev/ad/apps/project-digest` (own repo). Vision-doc
  annotation + engine-store movement → `~/dev/ad/apps/dark-factory`. Use absolute paths
  everywhere; your cwd resets between shell calls.
- **Scope fence — do NOT touch:** the registry app's code (you are a read-only consumer; its
  defects become findings in your results note, or Abort A1), `engine/` in dark-factory, the
  deferred `project-digest-list-and-project-2` queue ticket (T2-03's business), `lib/assemble.py`
  / `lib/box.py` / `lib/render_md.py` internals (call them, don't refactor them),
  `~/.config/appydave/locations.json` (its conflation debt is T2-07).
- **Not this ticket:** the feed layer (Linear/Watchtower/engine tickets into NEEDS-YOU — that's
  T2-05), `--list` (T2-03), onboarding project #2 (T2-03), email/calendar (explicitly out of
  scope in the vision doc), any new daemon/cron (the digest is read-on-demand by contract).
- **Prefer HITL over guessing:** every ambiguity that matters already has an abort lane; a parked
  ticket with a crisp needs-decision question beats an improvised registry-shaped guess.
- **Rabbit hole #1:** synthesizing full briefing boxes for every changed repo ("it's only a small
  config generator…"). Banned — the two-tier rule is locked; the compact line IS the deliverable
  for unconfigured paths. **Rabbit hole #2:** redesigning the box/HTML renderer for a slick
  multi-project layout. Stacked existing boxes + a plain compact section is the deliverable;
  stop there.
