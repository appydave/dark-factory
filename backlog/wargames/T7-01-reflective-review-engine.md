# T7-01 — The ONE reflective-review engine

| field | value |
|---|---|
| ticket | wg-t7-01-reflective-review-engine |
| track / size / priority | T7 Self-learning / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Build `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/reflective-review/` — ONE config-driven
staleness scanner + review-brief generator, pointed at 4 targets: **concepts** (`backlog/concepts.md`
table rows), **docs** (`docs/**/*.md` excl. `kdd/`), **workflows** (`.claude/workflows/` +
`.claude/skills/`), **memory** (the project auto-memory dir, outside the repo). This is the pattern
`backlog/concepts.md` itself demanded (rows 55–56: "Idea-staleness" + "Periodic REFRESH +
recategorization pass") and David's design-resolution row already answered the how: **JSON + schema =
source of truth, staleness is date math, no database, LLM = the judge on a refresh pass**. So: the
deterministic half is a stdlib-only Python CLI (`scan` → JSON report per target, `brief` → a markdown
review packet combining stale items + per-target review questions); the judgment half is an LLM pass
that READS a brief and writes a proposal — demonstrated once in this ticket (on concepts) to prove the
brief is actionable. Done looks like: self-test green; `scan --all` produces 4 honest JSON reports
over the real targets; 4 briefs rendered; one demonstration judgment written (proposals only, nothing
auto-applied); tool registered in `docs/tool-registry.md`; the two concepts.md rows flipped from 📋 to
🔨; committed and pushed. Recurring cadence/trigger wiring is explicitly NOT this ticket.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this war game is written for sonnet Swagger
  dispatch.
- **Q9 (decisions.md): complement, don't replace.** Existing review machinery stays untouched: the
  `doc-drift` / `doc-review` skills, the `delivery-review` orchestrator, and
  `.claude/workflows/daily-review.workflow.js` (whose `idle_or_stale` facet may later CONSUME these
  reports — a separate ticket). This tool adds deterministic DATA; it replaces nothing.
- **No YLO/POEM work (Q5).** The workflows target SCANS the YLO-probe workflow files sitting in
  `.claude/workflows/` (file-date arithmetic is not YLO work) but you never open, run, or edit YLO
  content, and `experiments/**` is excluded from every target.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot: nothing here spawns Claude; the
  demonstration judgment is done by YOU, the executing Swagger, in-session.
- **Hard rules (CLAUDE.md):** never touch `research/` (frozen) or `canonical/`; don't write skill code
  into appydave-plugins. This tool lives in `tools/`, reads its targets, writes only under
  `tools/reflective-review/out/` plus the two surgical doc edits in Move 7.
- **Ticket-first (queue .CONVENTION.md):** honoured by this run itself being a ticket. The tool emits
  NO tickets and drops nothing into `engine/store/queue/` — future review runs get queued by humans or
  a later trigger ticket.
- **Docs lag code (wargame-spec):** every target shape below was verified on disk 2026-07-06; Recon
  re-verifies at execution time.

## Recon (verify before any work)

All paths absolute; repo root `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`;
memory dir `MEM=/Users/davidcruwys/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory`.

1. `ls $DF/tools/reflective-review 2>&1` → expect **No such file** (2026-07-06: `tools/` held only
   `design-lint/`, `mocha-census/`, `youtube-assets/`, `serve.sh`, `stop.sh`). If it exists →
   **Abort A2**.
2. `grep -c "^| " $DF/backlog/concepts.md` → expect ≥ 60 (71 at authoring: 62 data rows + 9 header
   rows; separators start `|---` and don't match) and `grep -c "^## " $DF/backlog/concepts.md` →
   expect ≥ 7 (9 lanes at authoring). Under 10 data rows or 0 lanes → the register was restructured
   or superseded → **Abort A1**.
3. `find $DF/docs -name "*.md" -not -path "*/kdd/*" | wc -l` → expect ≥ 40 (60 at authoring). Also
   `ls $DF/docs/kdd/ >/dev/null && echo kdd-present` → expect `kdd-present` (it's excluded on
   purpose — Lisa's KDD discipline owns its lifecycle). Zero docs → wrong repo/branch → **Abort A2**.
4. `ls $DF/.claude/workflows/*.workflow.js | wc -l` → expect ≥ 8 (11 at authoring) and
   `ls $DF/.claude/skills/*/SKILL.md | wc -l` → expect ≥ 5 (7 at authoring). All git-tracked
   (verified via `git ls-files .claude/` 2026-07-06).
5. `ls $MEM/*.md | wc -l` → expect ≥ 10 (17 at authoring, incl. `MEMORY.md`), and
   `git -C $MEM rev-parse --git-dir 2>&1` → expect **fatal: not a git repository** (this is WHY the
   memory target uses mtime). Dir missing entirely → **Fork F2 Route B** (not an abort).
6. `python3 --version` → expect ≥ 3.9 (authored against 3.14.5). Stdlib only (`json`, `sys`, `os`,
   `re`, `argparse`, `pathlib`, `subprocess`, `datetime`, `tempfile`, `shutil`, `fnmatch`). Missing →
   **Abort A3**. Also `which jq` → used only by Verification; if absent, use the python fallbacks
   given there.
7. `git -C $DF blame --line-porcelain -L 55,56 backlog/concepts.md | grep committer-time | wc -l` →
   expect 2 (per-line blame works; this is the concepts date source). And
   `git -C $DF log -1 --format=%cs -- docs/north-star.md` → expect a `YYYY-MM-DD` date (per-file log
   works; this is the docs/workflows date source).
8. `grep -n "Idea-staleness" $DF/backlog/concepts.md` and `grep -n "Periodic REFRESH" $DF/backlog/concepts.md`
   → expect one hit each (~lines 55–56), both rows ending `| 📋 | 🟡 |`. These are Move 7's edit
   targets. Wording drifted → adapt the substitution to the current row; rows GONE → skip that edit
   and note it in the result (do not abort).
9. `grep -n "tools/youtube-assets" $DF/docs/tool-registry.md` → expect one hit inside the
   "Index — Repo scripts" table (~line 50) — Move 7's insertion anchor. Table gone → append a new
   row wherever the repo-scripts index now lives; if the whole file is gone → note it, skip.
10. `git -C $DF status --porcelain -- tools/ docs/tool-registry.md backlog/concepts.md` → expect
    empty. (Untracked `backlog/wargames/` and other wargame-wave files elsewhere are EXPECTED and
    fine — only dirt on these three exact paths matters.) Dirt here → **Abort A2**.

## Moves

1. **Do:** Write `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/reflective-review/targets.json`
   with exactly this content (thresholds are David-tunable defaults — Assumption 1):

   ```json
   {
     "schema": "reflective-review/targets.v1",
     "targets": {
       "concepts": {
         "description": "backlog/concepts.md — the ideas register; items are table rows",
         "root": ".",
         "include": ["backlog/concepts.md"],
         "exclude": [],
         "granularity": "table-row",
         "date_source": "git",
         "stale_after_days": 21,
         "review_questions": [
           "Still relevant, or overtaken by shipped work?",
           "Right lane, or should it move (which lane)?",
           "Merge candidate — does another row now cover this?",
           "Is the status emoji honest (idea/needs-spec/building/done)?",
           "Promote (to spec / engine ticket) or archive-candidate?"
         ]
       },
       "docs": {
         "description": "docs/**/*.md excluding kdd/ (Lisa's KDD lifecycle owns that)",
         "root": "docs",
         "include": ["**/*.md"],
         "exclude": ["kdd/**"],
         "granularity": "file",
         "date_source": "git",
         "stale_after_days": 30,
         "review_questions": [
           "Does this doc still match shipped code (docs-lag-code)?",
           "Is it still listed in docs/INDEX.md, and is its one-liner accurate?",
           "Superseded-by or merge-into candidate (which doc)?",
           "Status line inside the doc stale (says planned/missing for things that shipped)?"
         ]
       },
       "workflows": {
         "description": "the factory's own SOPs: .claude/workflows/ + .claude/skills/ (experiments/ excluded everywhere)",
         "root": ".claude",
         "include": ["workflows/*.workflow.js", "skills/*/SKILL.md", "skills/*/*.workflow.js"],
         "exclude": [],
         "granularity": "file",
         "date_source": "git",
         "stale_after_days": 45,
         "review_questions": [
           "Still invoked, or dead weight (check tool-registry.md's workflow index)?",
           "YLO-lane (parked per decisions.md Q5) vs live factory SOP — labelled honestly?",
           "Does the description/meta header still match what it does?",
           "Canonical-vs-variant: has a newer sibling quietly replaced it?"
         ]
       },
       "memory": {
         "description": "project auto-memory (outside the repo, not git-tracked — mtime basis)",
         "root": "~/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory",
         "include": ["*.md"],
         "exclude": [],
         "granularity": "file",
         "date_source": "mtime",
         "stale_after_days": 21,
         "review_questions": [
           "Does this memory match the CURRENT architecture (the /loop+mutex note went stale exactly this way)?",
           "Contradicted by a newer decision in decisions.md / concepts.md?",
           "Delete, rewrite, or keep verbatim?"
         ]
       }
     }
   }
   ```
   **Expect:** `python3 -c "import json;json.load(open('$DF/tools/reflective-review/targets.json'))"`
   exits 0.
   **Failure signal:** JSON parse error.
   **Counter-move:** fix the syntax; this file is pure data, there is no second way to fail it. Still
   broken after re-write → **Abort A3**.

2. **Do:** Write `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/reflective-review/review.py` —
   one stdlib-only Python file (imports limited to: `json`, `sys`, `os`, `re`, `argparse`,
   `pathlib`, `subprocess`, `datetime`, `tempfile`, `shutil`, `fnmatch`). Contract:
   - **Invocation:** `python3 review.py scan <target>|--all`, `python3 review.py brief <target>|--all`,
     `python3 review.py --self-test`. Repo root = `Path(__file__).resolve().parent.parent.parent`
     (works from any cwd). Config = `targets.json` beside the script (overridable with
     `--config <path>` — the self-test needs this). No command → usage on stderr, **exit 2**.
     Unknown target name or malformed config → **exit 2**.
   - **`scan <target>`** writes `tools/reflective-review/out/<target>.json` (create `out/` on
     demand), overwrite-in-place, schema:
     ```
     { "schema": "reflective-review/scan.v1", "target", "generated_at" (UTC ISO-8601),
       "root" (resolved absolute), "granularity", "date_source", "stale_after_days",
       "item_count", "stale_count", "error" (null | string),
       "items": [ { "id", "path" (relative to root), "line" (int, table-row only, else null),
                    "last_touched" ("YYYY-MM-DD"), "age_days" (int), "stale" (bool),
                    "date_basis" ("git" | "mtime" | "mtime-untracked") } ] }
     ```
     Items sorted stalest-first. `stale = age_days > stale_after_days`; ages measured against
     today's UTC date. Also print one summary line per target to stdout:
     `<target>: <item_count> items, <stale_count> stale (threshold <n>d)`.
   - **Date resolution, `file` granularity:** collect files under `root` matching any `include`
     glob (fnmatch on the root-relative path) and no `exclude` glob; `root` supports `~`
     (expanduser) and repo-relative paths. `date_source: git` → `git -C <repo> log -1 --format=%ct
     -- <path>` per file; a tracked-and-clean file uses that commit time (`date_basis: "git"`); a
     file that is untracked OR locally modified (per `git status --porcelain -- <path>`) uses
     filesystem mtime (`date_basis: "mtime-untracked"` — an uncommitted edit means touched now,
     which is honest). `date_source: mtime` → `st_mtime` (`date_basis: "mtime"`), no git calls.
   - **Date resolution, `table-row` granularity:** for each include file: one
     `git blame --line-porcelain` pass mapping line-number → committer-time. Items = lines matching
     `^\| ` EXCLUDING separator lines (`^\|-`) and header rows (a `^\| ` line whose NEXT line
     matches `^\|-`). `id` = `"<lane> :: <first-cell>"` where lane = text of the nearest preceding
     `^## ` heading (truncated 40 chars) and first-cell = the row's first `|`-delimited cell,
     `**`-markers stripped, truncated 60 chars. `line` = 1-based line number.
   - **Honest degradation:** target root missing, or zero files matched → report still written with
     `error` set and `items: []`, one `WARN <target>: <why>` line to stderr, **exit still 0** (a
     missing per-machine dir must not fail the fleet — Fork F2). Only usage/config problems exit 2.
   - **`brief <target>`** runs the scan logic itself (always fresh — no stale-staleness-report
     problem), writes BOTH `out/<target>.json` and `out/<target>-brief.md`. Brief content: title
     `# Reflective review — <target>`, the generated_at/threshold/counts header, a markdown table
     of STALE items only (id · path:line · last_touched · age_days), then `## Review questions`
     listing the target's `review_questions`, then a fixed footer:
     `> Judgment pass: read the items above against the questions. Write PROPOSALS to tools/reflective-review/out/judgments/ — never auto-apply edits to the target.`
     Zero stale items → the table is replaced by `No stale items — nothing to review.` (still a
     valid brief).
   - Top-of-file docstring: source-of-truth pointers (`backlog/concepts.md` rows 55–56 — the
     Idea-staleness + Periodic-REFRESH concepts; David's design-resolution row: deterministic state
     in JSON, LLM as judge), the exit-code contract, and the proposals-only rule.
   **Expect:** `python3 $DF/tools/reflective-review/review.py` (no args) exits 2 with usage;
   `grep -E "^(import|from) " review.py` shows only the stdlib modules above.
   **Failure signal:** any third-party import; no-args exits 0 or tracebacks.
   **Counter-move:** rewrite the offending part (argparse subcommands: use `parser.error` for the
   no-command case, or manual `sys.argv` handling). Second full failure → **Abort A3**.

3. **Do:** Implement `--self-test` in the same file: build fixtures under `tempfile.mkdtemp()` with
   a THROWAWAY config (via the `--config` override) pointing at fixture roots; print `ok <case>` /
   `FAILED <case>: <why>` per case and `self-test: <n>/<n> cases ok`; exit 0 iff all green; always
   `shutil.rmtree` the temp dir. Exactly these 7 cases:
   1. `mtime-stale-split` — mtime-source target, two files, one `os.utime`'d to 100 days ago, one
      fresh → item_count 2, stale_count 1, correct file flagged, `date_basis: "mtime"`.
   2. `git-file-dates` — temp git repo (`git init -q`, local `user.name`/`user.email` config), two
      files committed with `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` forced to 100 days ago and to
      today respectively → both `date_basis: "git"`, stale_count 1.
   3. `git-untracked-fallback` — add an uncommitted third file to that repo → its item has
      `date_basis: "mtime-untracked"` and `age_days: 0`.
   4. `table-row-parse` — a fixture md in a temp git repo: 2 `## ` lanes, a header+separator and 3
      data rows per lane, committed 100 days ago; then ONE row edited and re-committed today →
      item_count 6 (headers/separators excluded), exactly 5 stale, the edited row fresh, ids carry
      the correct lane prefix.
   5. `missing-root` — target whose root doesn't exist → exit 0, report has `error` set,
      `items: []`.
   6. `zero-stale-brief` — brief over an all-fresh target → brief file contains
      `No stale items — nothing to review.` and the review questions.
   7. `stale-brief` — brief over case-1's target → brief lists the stale item's id and age in the
      table and ends with the proposals-only footer.
   Each case asserts the expected values AND the absence of wrong flags (a scanner that marks
   everything stale must fail cases 1/2/4).
   **Expect:** `python3 $DF/tools/reflective-review/review.py --self-test` exits 0, prints 7 `ok`
   lines + `self-test: 7/7 cases ok`.
   **Failure signal:** any `FAILED` line, nonzero exit, traceback, or temp dirs left behind.
   **Counter-move:** the failing case names the broken area (usual culprits: fnmatch against
   root-relative vs absolute paths; blame header-row exclusion off-by-one; git env dates not
   exported to the commit subprocess). Fix and re-run. Still red after three fix rounds →
   **Abort A3**.

4. **Do:** Run the real scan: `cd $DF && python3 tools/reflective-review/review.py scan --all`.
   Then sanity-check with jq (or the python fallback from Verification):
   `jq -e '.item_count >= 50' out/concepts.json`, `>= 40` for docs, `>= 15` for workflows,
   `>= 10` for memory (authoring-day actuals: 62 / 60 / 19 / 17); and
   `jq -e '.items[0].date_basis == "mtime"' out/memory.json`.
   **Expect:** exit 0; four summary lines; all four `out/<target>.json` written; jq checks pass;
   every `last_touched` a plausible date (2026-05 onward for repo targets).
   **Failure signal:** a count wildly under floor (glob bug), epoch-1970 dates (parse bug), scan
   exiting nonzero, or memory reporting `date_basis: "git"`.
   **Counter-move:** fix, re-run Move 3's self-test (a real-world fix must not break fixtures),
   re-run the scan. If memory's root is missing → that's **Fork F2 Route B**, not a bug. Second
   unexplained failure → **Abort A3**.

5. **Do:** `cd $DF && python3 tools/reflective-review/review.py brief --all`.
   **Expect:** four `out/<target>-brief.md` files; each carries its target's review questions and
   either a stale-items table or the honest-zero line; spot-read `out/concepts-brief.md` — stale
   rows should be recognisable concepts-register rows (id = `<lane> :: <concept>`).
   **Failure signal:** empty brief, missing questions, or ids that are separator/header junk.
   **Counter-move:** fix the brief renderer / row parser, re-run self-test + Moves 4–5. →
   **Abort A3** on a second full failure.

6. **Do:** The demonstration judgment pass — YOU are the LLM judge; this proves the brief is
   actionable. Read `out/concepts-brief.md` in full, plus `backlog/concepts.md` for context. Write
   `tools/reflective-review/out/judgments/2026-<MM>-<DD>-concepts.md`: for each stale concepts item
   (Fork F1 if zero), one verdict line — `KEEP` (still right, just old) / `RE-LANE → <lane>` /
   `MERGE → <other row>` / `STATUS-FIX → <emoji>` (register claims 📋 but the thing shipped) /
   `ARCHIVE-CANDIDATE` — each with a ≤2-line reason grounded in something you can point at (a
   shipped file, a decisions.md ruling, a duplicate row). Cap effort: if more than 25 items are
   stale, judge the 25 stalest and say so in the doc header. End the doc with:
   `> Proposals only — nothing above has been applied. David/PO triages this file.`
   **Apply NOTHING to `backlog/concepts.md`** (the register's own words: staleness "needs a 'still
   relevant?' judgment, not auto-reaping" — and the judgment is David's).
   **Expect:** the judgment file exists, ≥ 1 verdict line per judged item, every verdict one of the
   5 forms above.
   **Failure signal:** you catch yourself editing `backlog/concepts.md` rows, inventing verdicts
   with no pointable ground, or spiralling into re-designing the register.
   **Counter-move:** stop, re-read this move's verdict vocabulary, restart the judgment doc from
   the brief. This move is bounded LLM work with a fixed output shape — if the brief itself is too
   thin to judge from, that's a tool defect: improve the brief's table columns (Move 5) once, then
   redo. Second failure → finish the ticket WITHOUT the judgment doc and note the gap in the result
   (the engine still shipped; the demonstration is evidence, not the deliverable).

7. **Do:** Two surgical doc edits. **(a)** `$DF/docs/tool-registry.md`, "Index — Repo scripts"
   table: insert one row directly above the `tools/youtube-assets/` row (Recon 9 anchor):
   `| `tools/reflective-review/review.py` | The ONE staleness scanner — scan/brief over 4 targets (concepts · docs · workflows · memory); judgment passes read the briefs, propose, never auto-apply | `
   **(b)** `$DF/backlog/concepts.md` — flip ONLY the status cell of the two rows found in Recon 8:
   row "Idea-staleness": `| 📋 | 🟡 |` → `| 🔨 detection shipped — `tools/reflective-review/` scan | 🟡 |`
   row "Periodic REFRESH + recategorization pass": `| 📋 | 🟡 |` → `| 🔨 engine + briefs shipped; recurring cadence still owed | 🟡 |`
   Touch nothing else in either file — no re-ranking, no new rows, no prose "improvements".
   **Expect:** `git -C $DF diff --stat docs/tool-registry.md backlog/concepts.md` → 2 files,
   ~3 insertions, ~2 deletions.
   **Failure signal:** diff bleeding beyond one added table row + two edited cells.
   **Counter-move:** `git -C $DF checkout -- docs/tool-registry.md backlog/concepts.md`, redo as
   exact-string substitutions.

8. **Do:** Commit and push (dark-factory only). Stage exactly:
   `tools/reflective-review/` (targets.json, review.py, out/ — the reports, briefs, and judgment
   doc are the proof artifacts; scans overwrite in place so out/ does not grow unboundedly),
   `docs/tool-registry.md`, `backlog/concepts.md`. Message:
   `feat(tools): reflective-review — the ONE staleness engine, 4 targets (self-test 7/7)`.
   Leave the wargame-wave's untracked files and any stranger's dirt unstaged.
   **Expect:** push succeeds; `git -C $DF status --porcelain -- tools/reflective-review docs/tool-registry.md backlog/concepts.md` empty.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; conflict in a file you touched → resolve keeping
   both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — zero stale concepts items at execution time.**
Trigger: Move 4's `out/concepts.json` has `stale_count: 0` (possible if David refreshes the register
between authoring and execution; at authoring most rows dated 2026-06-06/08, so ≥ 40 stale at a
21-day threshold is the likely state).
→ **Route A** (default): ≥ 1 stale item — Move 6 judges the stale set as written.
→ **Route B**: zero stale — still prove the pattern: judge the 5 OLDEST items, header the judgment
doc `dry-run: no items over threshold; judging the 5 oldest`, verdict vocabulary unchanged.

**F2 — the memory dir is missing or has moved.**
Trigger: Recon 5 / Move 4 finds
`~/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory` absent (harness updates can
relocate auto-memory; the path is also per-machine).
→ **Route A** (default; verified present with 17 files on 2026-07-06): scan normally.
→ **Route B**: ship the memory target CONFIGURED anyway; the scan writes its honest-error report
(`error` set, exit 0), the brief says the root is missing, and your result notes flag "memory target
needs a per-machine path decision" for triage. The other 3 targets are unaffected. Never hunt the
filesystem for a lookalike dir.

## Assumptions ledger

1. **Thresholds 21/30/45/21 days.** David never picked numbers; these are authoring defaults sized
   to observed churn (concepts/memory move weekly; docs monthly; workflows are stable SOPs). They
   live in `targets.json` precisely so being wrong is a config edit, not a code change. **If David
   objects at triage:** edit the JSON; nothing else moves.
2. **`docs/kdd/**` excluded from the docs target.** Plausible: KDD has its own librarian (Lisa) and
   lifecycle timestamps; double-scanning invites contradictory verdicts. **If false:** delete one
   exclude line.
3. **`tools/reflective-review/out/` is the interim home for reports, briefs, and judgment docs**
   (committed to git). Watchtower/Symphony will eventually own the surface where reviews are
   triaged; until then the repo is the shared store. **If false** (David wants them in backlog/ or
   un-committed): move/gitignore `out/` — one-line change, no code impact.
4. **The detection half is deterministic CODE, not a skill.** concepts.md's open Q ("code or
   skills?") is resolved for DETECTION only, per David's own design-resolution row ("schemas and
   JSON and scaffold applications"; LLM = judge). Also avoids the skill-flood + T6 name-collision
   class ("daily-review" and "review" skills already exist). **If false** (David wants a skill
   wrapper): additive later; do NOT create a SKILL.md in this ticket.
5. **mtime is an acceptable date basis for memory.** The dir is not a git repo (verified Recon 5);
   mtime is the only date there is. It's a weak signal (any rewrite bumps it) — the brief's
   questions do the real work. **If false** (memory gets git-tracked later): flip its
   `date_source` to `git`; the code already supports both.
6. **Judgments are proposals only — the tool and its passes never auto-apply recategorization.**
   Grounded in the register's own "not auto-reaping" line and the assessment-mode default. **If
   David wants auto-apply:** that is a NEW ticket with an HITL gate design, not a flag on this one.

## Abort conditions

- **A1 — the concepts register was restructured.** Recon 2 finds < 10 data rows or no `## ` lanes
  (e.g. superseded by a Symphony/Watchtower board). The table-row contract is void. Park: write
  `engine/store/needs-decision/wg-t7-01-reflective-review-engine.json` with
  `{"ticket": "wg-t7-01-reflective-review-engine", "question": "backlog/concepts.md no longer matches the lane/table shape the concepts target was war-gamed against — re-point the concepts target at the register's successor, or drop to 3 targets?", "observed": "<what the file/its successor looks like now>"}`.
  Leave the ticket in `running/`.
- **A2 — race or seam conflict.** `tools/reflective-review/` already exists (Recon 1), Recon 3
  finds an empty/foreign docs tree, or Recon 10 shows uncommitted edits on the three seam files.
  Park with: "wg-t7-01's target exists / is mid-edit (found: <what and where>). Verify-and-close
  against the existing implementation, or redo per the war game?" Never overwrite half-landed work.
- **A3 — the engine can't be made sound.** Python broken (Recon 6), Move 2 twice fails to produce
  a runnable script, Move 3 self-test red after three fix rounds, or a Move 4/5 fix breaks the
  self-test irrecoverably. Park with the failing output attached. A staleness scanner whose own
  dates are wrong poisons every review that reads it — never ship it red.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting paths;
  do not resolve other people's conflicts.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
RR=$DF/tools/reflective-review

# 1. The tool exists, stdlib-only, config parses
test -f $RR/review.py && test -f $RR/targets.json && echo exists-ok
grep -E "^(import|from) " $RR/review.py    # only: json/sys/os/re/argparse/pathlib/subprocess/datetime/tempfile/shutil/fnmatch
python3 -c "import json;print(len(json.load(open('$RR/targets.json'))['targets']))"   # → 4

# 2. Self-test green
python3 $RR/review.py --self-test; echo "exit=$?"        # 7 'ok' lines + 'self-test: 7/7 cases ok'; exit=0

# 3. Usage shapes exit 2, no tracebacks
python3 $RR/review.py 2>&1;              echo "exit=$?"  # usage; exit=2
python3 $RR/review.py scan nonsense 2>&1; echo "exit=$?" # unknown target; exit=2

# 4. Real scan: 4 honest reports (floors, not exact — targets drift by design)
python3 $RR/review.py scan --all; echo "exit=$?"         # 4 summary lines; exit=0
jq -e '.item_count >= 50 and .granularity == "table-row"' $RR/out/concepts.json    # 62 at authoring
jq -e '.item_count >= 40' $RR/out/docs.json                                        # 60 at authoring
jq -e '.item_count >= 15' $RR/out/workflows.json                                   # 19 at authoring
jq -e '(.item_count >= 10) or (.error != null)' $RR/out/memory.json                # 17, or F2-Route-B honest error
jq -e '.items[0].date_basis == "mtime"' $RR/out/memory.json                        # (skip if F2 Route B)
jq -e '[.items[].age_days] | min >= 0' $RR/out/docs.json
# no jq? python3 -c "import json;r=json.load(open('$RR/out/docs.json'));assert r['item_count']>=40"

# 5. Briefs render, carry the questions + the proposals-only footer
for t in concepts docs workflows memory; do test -f $RR/out/$t-brief.md && echo "$t-brief-ok"; done
grep -c "Review questions" $RR/out/concepts-brief.md                               # → 1
grep -c "never auto-apply" $RR/out/concepts-brief.md                               # → 1

# 6. Demonstration judgment exists, proposal-shaped (may be absent only per Move 6's second-failure note)
ls $RR/out/judgments/*-concepts.md
grep -cE "KEEP|RE-LANE|MERGE|STATUS-FIX|ARCHIVE-CANDIDATE" $RR/out/judgments/*-concepts.md   # → ≥ 1
grep -c "Proposals only" $RR/out/judgments/*-concepts.md                            # → 1

# 7. Doc edits, surgically
grep -c "reflective-review/review.py" $DF/docs/tool-registry.md                     # → 1
grep -c "detection shipped" $DF/backlog/concepts.md                                 # → 1
grep -c "recurring cadence still owed" $DF/backlog/concepts.md                      # → 1

# 8. Negative checks — what must NOT have changed
git -C $DF status --porcelain -- research/ canonical/ experiments/ engine/ | wc -l  # → 0
git -C $DF diff HEAD~1 --stat -- .claude/ | wc -l                                   # → 0 (daily-review & skills untouched)
ls $RR/SKILL.md 2>&1                                                                # No such file (no skill wrapper — Assumption 4)
ls $DF/engine/store/queue/ | grep -c reflective                                     # → 0 (tool queued nothing)
git -C $DF diff HEAD~1 --numstat -- backlog/concepts.md                             # ~2 added / ~2 deleted lines only

# 9. Committed and pushed
git -C $DF log --oneline -1                                                         # the feat(tools) commit
git -C $DF status --porcelain -- tools/reflective-review docs/tool-registry.md backlog/concepts.md | wc -l   # → 0
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT edit `backlog/concepts.md` beyond the two status cells (Move 7) — the
  judgment doc PROPOSES, David applies. Do NOT touch `.claude/workflows/` or `.claude/skills/`
  (the workflows target only READS file dates). Do NOT touch `experiments/**` (YLO parked; the old
  watchtower-engine is history), `research/`, `canonical/`, `engine/*.py`, or the other tools
  (`design-lint/`, `mocha-census/`). Do NOT create a SKILL.md, a cron, a launchd job, or any
  recurring trigger — cadence wiring is a separate ticket (tool-registry.md's "Open decisions"
  already flags that a live schedule needs David's explicit go). Do NOT drop anything into
  `engine/store/queue/`.
- **The rabbit hole: doing the reviews instead of building the reviewer.** The docs brief will
  surface genuinely stale docs (docs-lag-code is a known class — that's T8's campaign) and the
  memory brief will surface wrong memories. You will be tempted to FIX them. Don't. This ticket
  ships the detector + one bounded demonstration judgment on concepts. Everything the briefs
  surface is downstream work for other tickets; listing it in your result notes is the win.
- **Style:** match the repo's Python-tool idiom (mocha-census, project-digest): stdlib only, small
  pure functions, honest degradation (missing root = reported error + exit 0, zero stale = a valid
  brief), machine-greppable output, no cleverness. One `git blame` subprocess per table-row file
  and one `git log`/`status` pair per file-target file is fine at this scale (~80 files); don't
  build a caching layer.
- **Prefer parking over guessing** on any A1/A2 signal. The whole point of the ONE engine is that
  four future review lanes trust its dates — a scanner with quietly-wrong date math is worse than
  no scanner.
