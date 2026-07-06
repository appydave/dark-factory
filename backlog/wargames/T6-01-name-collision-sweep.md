# T6-01 — Name-collision sweep, all apps

| field | value |
|---|---|
| ticket | wg-t6-01-name-collision-sweep |
| track / size / priority | T6 Constellation / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Close the invisibility class six-app-eval named its single worst finding: a new constellation
app loses natural-language resolution to an older skill that shares its trigger vocabulary, so
the app's richer capability is functionally invisible to David and to agents. Two instances were
found and fixed empirically (`appydave:omi-fetch` skill vs the omi-fetch app,
`appydave:apps-registry` skill vs the app-registry app — commit `0754317` in appydave-plugins);
the other ~38 constellation apps have never been checked. This war game (a) sweeps all 40
constellation apps against all ~145 David-owned skills, (b) classifies every overlap
(collision / intentional-pair / benign / third-party), (c) applies the proven additive
bidirectional-pointer fix to confirmed collisions, and (d) fixes the fix: authoring-time recon
found the two landed pointer fixes live in the dev repo at plugin v6.1.0 while the live cache
runs v5.9.1 WITHOUT them — every description-level fix is invisible until propagated, so
propagation (reload-plugins.sh) is a first-class move, not an afterthought. Done looks like: a
full 40-row sweep report in `docs/`, pointer fixes landed AND live in the cache, both repos
committed and pushed.

## Locked context

- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (file audit + edits; this
  ticket spawns nothing).
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — six-app-eval's claims were re-verified on disk 2026-07-06;
  your Recon re-verifies at execution time.
- **Q9 default "complement, don't replace"** — every fix is additive disambiguation: nothing
  renamed, deleted, or replaced; old skills keep their jobs and gain routing pointers, exactly
  per the `0754317` precedent.

## Recon (verify before any work)

Run every check. Absolute roots: dark-factory = `/Users/davidcruwys/dev/ad/apps/dark-factory`,
plugins dev repo = `/Users/davidcruwys/dev/ad/appydave-plugins`, personal skills =
`/Users/davidcruwys/.claude/skills`, plugin cache = `/Users/davidcruwys/.claude/plugins`.

1. App universe:
   `python3 -c "import json; d=json.load(open('/Users/davidcruwys/dev/ad/apps/dark-factory/mochaccino/data/constellation.json')); print(len(d['apps']))"`
   → expect `40` (exact count at authoring; 38–45 tolerable — the universe is whatever it says
   today). Each app dict carries `id`, `name`, `layer`, `path`, `purpose`, `status` (verified
   2026-07-06). File missing or no `apps` key → **Abort A1**.
2. Skill universe — four David-owned sources, count `SKILL.md` files:
   `ls /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/*/SKILL.md | wc -l` → ~88;
   same for `brand-dave/skills` → ~11; `flivideo/skills` → ~1;
   `ls /Users/davidcruwys/.claude/skills/*/SKILL.md | wc -l` → ~45. Exact counts will drift;
   any source at 0 or missing → **Abort A1**. NOTE: `appydave-plugins/_archived/` exists —
   always exclude it (archived skills don't resolve).
3. The precedent fixes exist in the DEV repo:
   `grep -c "Related app" /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/omi-fetch/SKILL.md`
   → ≥1, and same for `skills/apps-registry/SKILL.md` → ≥1. Zero on either → the pattern you're
   told to replicate is gone (reverted or moved) → **Abort A2** (state drifted from authoring).
4. Propagation gap (the authoring-time finding — re-verify, it may have closed):
   `python3 -c "import json; d=json.load(open('/Users/davidcruwys/.claude/plugins/installed_plugins.json')); print(d['plugins']['appydave@appydave-plugins'][0]['version'])"`
   vs `python3 -c "import json; print(json.load(open('/Users/davidcruwys/dev/ad/appydave-plugins/appydave/.claude-plugin/plugin.json'))['version'])"`.
   At authoring: installed `5.9.1`, dev `6.1.0`, and
   `grep -c "Related app" /Users/davidcruwys/.claude/plugins/cache/appydave-plugins/appydave/<installed-version>/skills/omi-fetch/SKILL.md`
   → `0` (fix not live). If versions already match AND the cache grep is ≥1 → the gap closed in
   a race; skip the propagation half of Move 4 and say so in the report.
5. Propagation mechanism exists and self-updates the pointer:
   `ls /Users/davidcruwys/dev/ad/appydave-plugins/reload-plugins.sh` exists;
   `grep -c "installed_plugins.json" /Users/davidcruwys/dev/ad/appydave-plugins/reload-plugins.sh`
   → ≥1 (verified 2026-07-06: the script rm-rf's the cache version dir, copies fresh from
   source, and rewrites the installed_plugins.json entry to the new version). Missing →
   **Fork F1 Route B**.
6. `git -C /Users/davidcruwys/dev/ad/appydave-plugins status --porcelain` → expect clean
   (verified 2026-07-06). Dirty on any `skills/*/SKILL.md` or `.claude-plugin/plugin.json` →
   someone is mid-change on your exact seam → **Abort A3**. Dirty elsewhere → proceed, stage
   only your files at Move 5.
7. No prior sweep landed (race check):
   `ls /Users/davidcruwys/dev/ad/apps/dark-factory/docs/name-collision-sweep-*.md 2>/dev/null`
   → expect no match. A report exists → **Abort A2**.
8. `/Users/davidcruwys/.claude/skills` is NOT a git repo (verified 2026-07-06:
   `git -C /Users/davidcruwys/.claude/skills rev-parse` fails). Consequence, not a blocker: any
   edit there has no commit trail — Move 3 must quote such diffs verbatim in the report.

## Moves

1. **Do:** Build the candidate-pair matrix, mechanical prefilter. Write a throwaway script in
   the scratchpad (never into the repo) that: loads all apps from
   `mochaccino/data/constellation.json` (fields `id`, `name`, `purpose`, `layer`, `status`);
   enumerates the four skill sources from Recon 2, parsing each SKILL.md's YAML frontmatter
   `name:` and `description:`; then emits a candidate pair for every app × skill where (a) the
   skill name and app id match exactly, as substring, or as hyphen/spelling variants
   (`apps-registry`≈`app-registry`, `sentinal`≈`sentinel`), OR (b) they share ≥1 distinctive
   token after splitting ids/names on hyphens and dropping generic tokens (`app`, `apps`,
   `appydave`, `dark`, `factory`, `the`, `old`, `suite`, `data`, `tool`, `tools`). Output a
   JSON list of `{app_id, skill_source, skill_name, match_reason}` to the scratchpad.
   **Expect:** the two known pairs surface — (`omi-fetch` app, `appydave/omi-fetch` skill) and
   (`app-registry` app, `appydave/apps-registry` skill). That is the matcher's self-test.
   Plausible other candidates at authoring (verify, don't assume): `media-studio` app ×
   `appydave/media-studio` skill; `angeleye` app × personal `angeleye-install`/
   `angeleye-name-session`; `mochaccino-mocha-census` app × `appydave/mochaccino`/`mocha`;
   `watchtower`, `kdd-viewer`, `project-digest`, `switchboard`, `blackboard-mcp` × whatever
   tokens hit.
   **Failure signal:** either known pair missing from the candidate list, or the list is empty,
   or it explodes past ~80 pairs (generic-token filter too weak).
   **Counter-move:** fix the tokenizer (the usual slips: frontmatter descriptions are
   multi-line `>` blocks — parse the whole frontmatter, not line 2; hyphen variants need both
   directions). A second failed self-test → **Abort A1** (can't trust a sweep whose matcher
   misses the two proven cases).

2. **Do:** Judgment pass — classify every candidate pair, then write the report. For each pair,
   read the skill's full `description:` (trigger phrases) and the app's constellation entry
   (plus the app's README at its `path` if the call is close) and assign exactly one class:
   - **collision** — the skill's trigger vocabulary captures asks the app answers better, and
     the skill does NOT already route to the app. The two 0754317 fixes were this class.
   - **intentional-pair** — the skill IS the app's driver or already points at it (e.g.
     `media-studio` skill drives the media-studio app via its API; `mochaccino` skill drives
     that workspace; a skill whose body already carries a "Related app" section). No fix.
   - **benign** — token overlap without ask overlap (e.g. shared word `query` but disjoint
     domains). No fix.
   Then a reverse pass: list every constellation app (status not `dead`/`parked`) with ZERO
   candidate skills at all — the invisible-by-absence class. Report-only; creating skills is
   NOT this ticket. Also add one line noting MCP servers (e.g. `appyradar-sentinel`,
   `blackboard`) are a separate resolution channel deliberately out of scope. Write the full
   report to
   `/Users/davidcruwys/dev/ad/apps/dark-factory/docs/name-collision-sweep-$(date -u +%Y-%m-%d).md`:
   a 40-row table (one row per constellation app: id, layer, status, matched skills, class,
   action taken), a "confirmed collisions" section with the per-pair fix plan, the
   invisible-by-absence list, and a "propagation state" section recording Recon 4's finding.
   The report is the collision ledger going forward — the old ledger home
   (`skills-registry/SKILL.md`, where 0754317 put its "Known name collisions" note) is archived
   under `_archived/` and must not be resurrected.
   **Expect:** report exists; every one of the 40 apps has exactly one row; the two known pairs
   are rows marked `collision (fixed 2026-07-04, commit 0754317)`.
   **Failure signal:** rows missing, or you find yourself unable to classify a pair after
   reading both sides.
   **Counter-move:** an unclassifiable pair gets class `ambiguous` with a one-line
   recommendation and NO edit — ambiguity is report-only, never guessed into a fix. If more
   than a quarter of pairs land ambiguous, your classes are wrong, re-read the 0754317 commit
   message (`git -C /Users/davidcruwys/dev/ad/appydave-plugins show 0754317 --stat`) and redo
   the pass once; still stuck → **Abort A4**.

3. **Do:** Apply the pointer fix to each NEW confirmed collision (the two 2026-07-04 fixes are
   already landed — do not re-edit them). Count the new collisions first → **Fork F2** decides
   how many you fix. Per pair, replicate the 0754317 pattern exactly, additive only:
   (a) in the OLD skill's SKILL.md `description:` add one routing sentence naming the ask that
   should go to the app ("for <liveness/capture/…> questions, a newer <app> APP also exists,
   see 'Related app' below"); (b) add a `## Related app` body section with the app's absolute
   path and its 1–3 real invocations (copy the command lines from the app's own README —
   verify each runs with `--help` or equivalent before writing it down); (c) if the app has a
   README, add the mirror one-liner pointing back at the skill ("an older skill
   `appydave:<name>` handles <its remaining job>"). Nothing renamed, nothing deleted, no
   trigger phrase removed from the old skill. Edits in `~/.claude/skills/*` take effect
   immediately but have no git — quote each such diff verbatim in the report (Recon 8).
   **Expect:** per fixed pair, `grep -c "Related app" <skill>/SKILL.md` → ≥1; the skill's
   frontmatter still parses (description block intact); `git -C .../appydave-plugins diff
   --stat` shows only modified files, zero deletions.
   **Failure signal:** YAML frontmatter broken (skill won't load), or a diff that removes lines
   that aren't pure whitespace.
   **Counter-move:** `git -C /Users/davidcruwys/dev/ad/appydave-plugins checkout -- <file>` and
   redo as a pure addition. A fix that cannot be expressed additively (the old skill's
   description is fundamentally wrong, needs restructuring) is out of scope → class it
   `collision-needs-redesign` in the report, skip the edit, list it in the Move 6 result notes.

4. **Do:** Propagate. If Move 3 touched any `appydave-plugins` skill, bump the patch version in
   the edited plugin's `.claude-plugin/plugin.json` (e.g. appydave `6.1.0` → `6.1.1` — re-read
   the current value first, Recon 4's may be stale). Then run
   `bash /Users/davidcruwys/dev/ad/appydave-plugins/reload-plugins.sh <plugin>` once per edited
   plugin — AND run it for `appydave` regardless, because Recon 4's gap means the 2026-07-04
   fixes are not live either (skip only if Recon 4 found the gap already closed and you edited
   no appydave skills).
   **Expect:** script prints `✓ <plugin>@<version> reloaded`; installed_plugins.json's entry
   now carries the dev version;
   `grep -c "Related app" /Users/davidcruwys/.claude/plugins/cache/appydave-plugins/appydave/<new-version>/skills/omi-fetch/SKILL.md`
   → ≥1 (the 07-04 fix is finally live), and same for each skill you edited in Move 3.
   **Failure signal:** script errors (jq missing, path wrong), or the cache copy still lacks
   the pointer text, or installed_plugins.json still names the old version.
   **Counter-move:** → **Fork F1**.

5. **Do:** Commit and push BOTH repos (separate git repos — verified at authoring).
   appydave-plugins: the edited SKILL.md files + plugin.json bump(s). Message:
   `docs(skills): name-collision sweep — routing pointers for <n> app/skill pairs (wg-t6-01)`.
   dark-factory: the sweep report only. Message:
   `docs: name-collision sweep report — 40 constellation apps vs ~145 skills (wg-t6-01)`.
   Stage ONLY your files; leave any stranger's dirt (Recon 6) uncommitted. If Move 3 fixed
   zero new collisions, the plugins repo may still have the version bump from Move 4's
   propagation of the 07-04 fixes — commit that as
   `chore(plugins): bump appydave — propagate 07-04 collision pointers to live cache (wg-t6-01)`.
   **Expect:** both `git push` succeed; `git status --porcelain` in each shows none of YOUR
   files left.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A5**.

6. **Do:** Close the loop in the report: append a short `## Outcome` section — pairs found /
   fixed / ambiguous / needs-redesign, propagation verified yes-no, and the one-line standing
   rule this class implies ("a new app that shares vocabulary with an existing skill gets its
   routing pointer ON THE DAY it's born — cf. the register-every-new-app standing rule").
   Amend the dark-factory commit or add a second one.
   **Expect:** report's Outcome section exists; numbers match the table.
   **Failure signal:** counts in Outcome disagree with the table rows.
   **Counter-move:** recount from the table (the table is the truth); fix Outcome, not the
   table.

## Forks

**F1 — propagation mechanism.**
Trigger: Move 4's reload-plugins.sh fails, is missing (Recon 5), or completes without the cache
actually updating.
→ **Route A** (script exists but errored on something trivial — jq absent, permission): fix the
trivial cause (e.g. `brew list jq || brew install jq` is NOT yours to run — instead read the
version with python3 as in Recon 4 and do Route B) — only proceed down Route A when the rerun
prints the ✓ line and the cache grep passes.
→ **Route B** (script missing or unfixable): perform its three verified steps by hand —
`rm -rf` the cache dir for the NEW version only, `cp -R` the plugin dir from the dev repo to
`/Users/davidcruwys/.claude/plugins/cache/appydave-plugins/<plugin>/<new-version>`, then update
that plugin's entry in `installed_plugins.json` (`installPath`, `version`, `lastUpdated`,
`gitCommitSha`) with a python3 one-liner mirroring the script's own logic. Never touch other
plugins' entries. If the hand-rolled copy also fails verification → **Abort A6**.

**F2 — collision count (scope governor).**
Trigger: Move 2 confirms N new collisions.
→ **Route A** (N ≤ 5): fix all N in Move 3.
→ **Route B** (N > 5): fix the 5 whose apps are `running`/`active` in constellation status
(liveness = user-facing pain), mark the remainder `collision-deferred` in the report, and list
them in the result notes as ready-made follow-up work — do NOT park; the report plus deferral
IS the deliverable at that scale. (S-size ticket; a 12-fix editing spree across live skill
descriptions without David seeing the report first is scope creep, not diligence.)

## Assumptions ledger

1. **constellation.json is the app universe.** The brief says "~40 apps unchecked" and
   constellation.json holds exactly 40 (authoring); the alternative registry
   `~/.config/appydave/apps.json` holds only 15 and is itself fronted by the (already-fixed)
   apps-registry skill. **If false** (David meant a wider universe, e.g. every dir under
   `~/dev/ad/apps/` — 27 dirs at authoring, some absent from constellation like `kdd-bridge`,
   `yt-mirror`, `suborch-demo`): the sweep is additive — note the uncovered ids in the report's
   Outcome section as a follow-up line; do not silently expand scope.
2. **Editing appydave-plugins SKILL.md files directly is sanctioned for this maintenance
   class.** Precedent: David's own commit `0754317` (2026-07-04) did exactly this for the same
   problem. dark-factory's "don't write skill code into appydave-plugins" rule governs NEW
   canonical artifacts staged in `canonical/`, not additive routing pointers in existing
   skills. **If false** (David objects at triage): every edit is additive and revertible with
   one `git revert`; note it and await the revert instruction — no park needed.
3. **Reloading the plugin cache is safe mid-day.** reload-plugins.sh is the repo's own
   sanctioned mechanism ("Hot-reload plugins from source into Claude Code cache", its header);
   it affects only sessions started after the reload. **If false** (David is mid-session and
   objects to a live swap): the dev-repo commits stand; park ONLY the propagation step to
   `engine/store/needs-decision/wg-t6-01-name-collision-sweep.json` with the question "fixes
   committed at plugin v<new>; cache still serves v<old> — reload now or at next session
   boundary?".
4. **Third-party marketplaces are report-only.** Skills under
   `~/.claude/plugins/marketplaces/{addy-agent-skills, thedotmack, claude-plugins-official,
   agent-browser, jarrodwatts-claude-delegator}` are not David's to edit; any collision found
   there gets a report row and no fix. **If false** (David wants a third-party pair handled):
   that's a fork he takes at review — nothing in this ticket blocks it.
5. **The engine ticket for this war game sits wherever Phase 5 promotion put it** — this war
   game does not manage its own ticket lifecycle beyond the standard running/→done/ handled by
   the orchestrator; no deferred sibling ticket exists for T6-01 (checked
   `engine/store/queue/` at authoring — none references name collisions).

## Abort conditions

- **A1 — universe undefined or matcher untrustworthy.** constellation.json missing/unparseable,
  any skill source empty (Recon 1–2), or the matcher's self-test fails twice (Move 1). Park:
  write `engine/store/needs-decision/wg-t6-01-name-collision-sweep.json` with
  `{"ticket": "wg-t6-01-name-collision-sweep", "question": "sweep universe is broken — <what/where>. Re-point the sweep at the right registry or fix the source first?", "observed": "<paths + errors>"}`.
  Leave the engine ticket in `running/`. Never sweep a universe you can't enumerate.
- **A2 — the work already landed (race).** A `docs/name-collision-sweep-*.md` exists (Recon 7),
  or the precedent fixes vanished/moved (Recon 3), or you find fresh post-authoring
  routing-pointer commits across many skills (`git -C .../appydave-plugins log --oneline
  --since=2026-07-06 -- appydave/skills` shows a sweep-shaped commit). Park with question:
  "wg-t6-01's target state partially/fully exists (found: <what and where>).
  Verify-and-close against it, or redo per the war game?" Do not duplicate a landed sweep.
- **A3 — seam conflict.** Recon 6 finds uncommitted changes on `skills/*/SKILL.md` or
  `plugin.json`. Park with the `git status` evidence and "who owns this seam right now?".
- **A4 — classification meltdown.** Move 2's counter-move ran and >25% of pairs are still
  ambiguous. Park with the candidate list attached and the question "collision taxonomy
  doesn't fit these pairs — <examples>; refine the classes or hand-classify?".
- **A5 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.
- **A6 — propagation impossible.** Fork F1 Route B also fails verification. Park with the
  evidence and the question "pointer fixes are committed but cannot be made live — cache/
  installed_plugins mechanism broken; investigate plugin loader?" This is itself a
  first-order finding (the invisibility class eating its own fix) — say so in the park file.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
AP=/Users/davidcruwys/dev/ad/appydave-plugins
CACHE=/Users/davidcruwys/.claude/plugins

# 1. Report exists, covers the full universe, carries the known pairs + outcome
ls $DF/docs/name-collision-sweep-*.md                                  # exactly one file
REPORT=$(ls $DF/docs/name-collision-sweep-*.md | head -1)
grep -c "omi-fetch" $REPORT                                            # ≥ 1
grep -c "apps-registry\|app-registry" $REPORT                          # ≥ 1
grep -c "0754317" $REPORT                                              # ≥ 1 (precedent cited)
grep -c "## Outcome" $REPORT                                           # → 1
# row count ≈ app count (one table row per app):
python3 -c "import json; print(len(json.load(open('$DF/mochaccino/data/constellation.json'))['apps']))"
grep -cE '^\| *[a-z0-9-]+ *\|' $REPORT                                 # ≥ that number

# 2. The 2026-07-04 fixes are finally LIVE in the cache (the propagation gap is closed)
python3 - <<'EOF'
import json
inst = json.load(open('/Users/davidcruwys/.claude/plugins/installed_plugins.json'))
dev  = json.load(open('/Users/davidcruwys/dev/ad/appydave-plugins/appydave/.claude-plugin/plugin.json'))
iv = inst['plugins']['appydave@appydave-plugins'][0]['version']
assert iv == dev['version'], f"cache {iv} != dev {dev['version']}"
print('propagation ok:', iv)
EOF
V=$(python3 -c "import json; print(json.load(open('$AP/appydave/.claude-plugin/plugin.json'))['version'])")
grep -c "Related app" $CACHE/cache/appydave-plugins/appydave/$V/skills/omi-fetch/SKILL.md      # ≥ 1
grep -c "Related app" $CACHE/cache/appydave-plugins/appydave/$V/skills/apps-registry/SKILL.md  # ≥ 1

# 3. Every NEW fix (report's confirmed-collision fix list) is present in dev AND cache
#    (substitute each fixed skill path from the report):
#    grep -c "Related app" $AP/<plugin>/skills/<skill>/SKILL.md   → ≥ 1
#    grep -c "Related app" $CACHE/cache/appydave-plugins/<plugin>/$V/skills/<skill>/SKILL.md → ≥ 1

# 4. Negative checks — additive-only, nothing renamed/deleted/created
git -C $AP log --oneline -3                                            # sweep commit present
git -C $AP show --stat HEAD | grep -c " delete "                       # → 0 (no deletions)
ls $AP/appydave/skills/omi-fetch/SKILL.md $AP/appydave/skills/apps-registry/SKILL.md  # both still exist
ls $AP/_archived/appydave-skills/skills-registry/SKILL.md              # archived registry untouched, still archived
git -C $DF status --porcelain -- research/ | wc -l                     # → 0 (frozen corpus untouched)
# no new skill directories were created:
git -C $AP show --stat HEAD | grep -c "skills/.*/SKILL.md.*new file"   # → 0 unless report justifies it (should be 0)

# 5. Both repos pushed
git -C $AP status --porcelain | wc -l                                  # → 0 (or only pre-existing stranger dirt noted in report)
git -C $DF log --oneline -1 -- docs/name-collision-sweep-*.md          # shows the report commit
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT create new skills for the invisible-by-absence apps — that is the
  "every-app-exposes-API+MCP doctrine sweep", a separate T6 seed; here it's a report list only.
  Do NOT rename, delete, or merge any skill. Do NOT edit third-party marketplace content under
  `~/.claude/plugins/marketplaces/`. Do NOT resurrect `_archived/appydave-skills/skills-registry`
  — the sweep report is the ledger now. Do NOT audit MCP-tool naming (different resolution
  channel; one report line saying so is the whole treatment). Do NOT touch `research/` or any
  `engine/*.py` in dark-factory. Do NOT re-edit the two already-fixed skills beyond what Move 4
  propagates.
- **The rabbit hole: fixing invisibility by ADDING skills.** Halfway through Move 2 you will
  notice apps (watchtower, switchboard, kdd-bridge…) that no skill mentions at all, and it will
  feel cheap to write tiny pointer skills for them. Skip it entirely — new skills are new
  NL-surface area, exactly the thing this sweep exists to audit, and creating them mid-sweep
  contaminates your own matrix.
- **Style:** pointer sections follow the two landed exemplars word-shape for word-shape (read
  both before writing any): description gets ONE routing sentence; body gets a short
  `## Related app` with absolute path, 3–7 command lines copied from the app's README, and a
  one-line "use the app for X / use this skill for Y" split. Terse, trigger-only, no marketing.
- **Prefer parking over guessing** on any classification you cannot defend in one sentence
  (`ambiguous` class exists precisely so you never force a call), and on anything that smells
  like a concurrent sweep (A2). The propagation move (4) is the one most likely to feel
  optional under time pressure — it is not; an unpropagated fix is the bug this ticket is about.
