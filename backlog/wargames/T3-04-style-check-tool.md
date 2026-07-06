# T3-04 — Build tools/style-check.py

| field | value |
|---|---|
| ticket | wg-t3-04-style-check-tool |
| track / size / priority | T3 Ingestion / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Build `tools/style-check.py` in `/Users/davidcruwys/dev/ad/apps/dark-factory/` — the automated
form of the **ratification checklist** in `docs/canonical-form-spec.md` (frontmatter fields,
trigger-only description, David-style sections, stack-agnostic body, layout existence). Both
`canonical-form-spec.md` (line 5) and `ingestion-workflow.md` (step 8) have promised this tool
"(when written)" since 2026-05-18; every future ingestion ticket (T3-01/02/19/20…) wants it as
its validation gate. `canonical/` holds ZERO artifacts today (verified 2026-07-06 — only
INDEX.md), so the tool ships with a **built-in fixture self-test** as its executable proof: no
real artifact is needed to demonstrate every check fires. Done = the script exists, `--self-test`
passes, it degrades gracefully on the empty library, the two docs stop saying "(when written)",
and everything is committed and pushed. This ticket does NOT validate provenance.json *content*
— that is `tools/verify-provenance.py`, sibling ticket T3-03; style-check only checks that
provenance.json and `_source/` *exist*.

## Locked context

- **Q2 (decisions.md):** ingestion is a full campaign — validators (this ticket) are in-scope now.
- **Q4 (decisions.md):** everything through the engine — this war game is written for sonnet
  Swagger dispatch; the work itself is pure local Python, no dispatch machinery touched.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (no Claude is spawned;
  the tool is a deterministic script, no LLM calls).
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — the ratification checklist was re-read on disk at authoring;
  your Recon re-reads it at execution time and the LIVE spec file is authoritative over the
  check table below if they differ (see Abort A3 for the contradictory case).
- **Assessment-mode default (CLAUDE.md):** the tool REPORTS, never auto-fixes. No flag that
  edits an artifact may exist in v1.

## Recon (verify before any work)

All paths relative to `/Users/davidcruwys/dev/ad/apps/dark-factory` unless absolute. Run every check.

1. `ls tools/style-check.py` → expect **No such file** (verified absent 2026-07-06). If it
   exists → someone landed this in a race → **Abort A1**.
2. `grep -n "Ratification checklist" docs/canonical-form-spec.md` → expect exactly 1 hit
   (~line 105), followed by 7 checkbox items (frontmatter 4 fields · trigger-only description ·
   body ≤400 lines or references/ · _source per origin · provenance validates · no stack terms ·
   no anti-patterns). Read the whole file. If the file is missing or the checklist section is
   gone → **Abort A3**. If the checklist has EXTRA items versus the check table below →
   implement them too from the live spec (live spec wins); if an item now *contradicts* the
   table → **Abort A3**.
3. `sed -n '25,35p;140,160p' docs/david-style-patterns.md` → expect the marketing-word list
   ("powerful", "comprehensive", "robust", "seamlessly" ~line 30; "advanced", "intelligent"
   ~line 149) and the stack-locked→agnostic table (npm/prettier/eslint/TypeScript examples,
   with `gh` explicitly acceptable). These seed SC7/SC8's word lists. Missing file → **Abort A3**
   (both spec docs are this tool's ground truth).
4. `ls canonical/` → expect only `INDEX.md` (state at authoring). If `canonical/skills/` (or
   agents/commands) contains one or more artifact dirs → T3-01's ingestion landed first →
   **Fork F1 Route B** (extra report-only run; changes nothing else).
5. `ls tools/verify-provenance.py` → expect **No such file** (T3-03 not landed at authoring).
   Exists → **Fork F2 Route A** wording for the docs move; absent → **Route B**.
6. `python3 --version` → expect ≥ 3.10 (3.14.5 on the M4 Mini at authoring). Also
   `grep -rn "import yaml" engine/ tools/` → expect zero hits (house style is stdlib-only;
   verified 2026-07-06). If other tools now import third-party libs freely, you MAY use PyYAML
   (installed, 6.0.3) instead of the minimal parser in Move 1 — note the choice in the result.
7. `git status --porcelain -- tools/ docs/canonical-form-spec.md docs/ingestion-workflow.md canonical/`
   → expect empty (clean at authoring). Dirty in any of these paths → someone is mid-change on
   your exact seam → **Abort A2**.

## Moves

1. **Do:** Write `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/style-check.py` — a single
   stdlib-only Python 3 script (no pip installs; write a ~30-line minimal frontmatter parser
   handling `key: value`, quoted scalars, and `>`/`|` block scalars — the description exemplar
   in david-style-patterns.md uses `description: >`). CLI contract, exactly:
   ```
   python3 tools/style-check.py <artifact-dir> [<artifact-dir> ...]  # check named artifacts
   python3 tools/style-check.py --all        # scan canonical/{skills,agents,commands}/*/
   python3 tools/style-check.py --self-test  # built-in fixture suite (see Move 2)
   --format json                             # machine-readable findings instead of text lines
   ```
   Exit codes: **0** = every checked artifact passes (WARNs allowed; `--all` over an empty
   library prints `no artifacts found under canonical/ — nothing to check` and exits 0),
   **1** = ≥1 FAIL finding, **2** = usage error / path not a directory / no primary file.
   Primary file: the artifact dir must contain exactly one of `SKILL.md`, `AGENT.md`,
   `COMMAND.md` (canonical-form-spec only names SKILL.md; the other two are accepted defensively
   — Assumption 4). Checks, each reported as `<artifact> <ID> <LEVEL> <message>`:

   | ID | Level | Check |
   |----|-------|-------|
   | SC1 | FAIL | frontmatter block (`---`…`---` at top) parses; `name` and `description` present and non-empty |
   | SC2 | FAIL | `name` is kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`) AND equals the artifact directory name |
   | SC3 | WARN | `argument-hint` present (frontmatter template says "Omit if none" → absence is a warning, never a failure — Assumption 2) |
   | SC4 | FAIL/WARN | `allowed-tools`: FAIL if absent while the body contains a fenced code block tagged `bash`/`sh`/`shell`/`zsh` (anti-pattern "missing allowed-tools when the skill calls bash"); WARN if absent otherwise |
   | SC5 | FAIL | description is trigger-shaped: contains `use when` (case-insensitive) AND ≥3 trigger phrases — count quoted segments (`'…'` or `"…"`) in the description; if none are quoted, count comma-separated items in the clause following "use when" |
   | SC6 | FAIL | description ≤2 sentences (sentence boundary = `.` followed by space/EOL, ignoring `.` inside quoted segments) |
   | SC7 | FAIL | no marketing words anywhere in the file (word-boundary, case-insensitive): powerful, comprehensive, robust, seamless, seamlessly, advanced, intelligent, cutting-edge, state-of-the-art |
   | SC8 | FAIL | no stack-specific terms in the BODY (below frontmatter; inline and fenced code ARE scanned — the canonical anti-pattern example is inline ``npm test``). Seed list (module-level constant, word-boundary, case-insensitive): npm, npx, yarn, pnpm, eslint, prettier, typescript, tsc, jest, vitest, pytest, rubocop, rspec, bundler, cargo, rustc, gradle, maven, webpack, vite, rails, django, flask, react, vue, svelte, next.js. `gh` is NOT on the list (explicitly acceptable per david-style-patterns). Suppression = the checklist's "noted intentional exception": a line containing `<!-- stack-ok -->` is exempt; `<!-- stack-ok: file -->` anywhere exempts the whole file (report as WARN `SC8 suppressed` instead) |
   | SC9 | FAIL | body ≤400 lines OR `references/` exists in the artifact dir with ≥1 file |
   | SC10 | FAIL | body has an `## Anti-patterns` heading AND at least one of `## Behavior` / `## Modes` (Template C mode-skills legitimately have Modes instead of Behavior) |
   | SC11 | WARN | `## Output` heading present (warn-only: Template C lacks it) |
   | SC12 | FAIL | `provenance.json` exists in the artifact dir — **existence only**; content validation is verify-provenance.py (T3-03), do not parse beyond `json.load` succeeding |
   | SC13 | FAIL | `_source/` exists in the artifact dir and contains ≥1 file |
   | SC14 | WARN | first non-blank line after the H1 is a prose line (the one-line purpose statement), not a heading or table |

   JSON output shape (`--format json`): `{"artifacts": [{"path": …, "verdict": "pass|fail",
   "findings": [{"id": "SC8", "level": "FAIL", "message": …}]}], "verdict": "pass|fail"}`.
   Top of file: docstring stating purpose, the SC-table summary, and the scope note
   "provenance CONTENT is tools/verify-provenance.py's job". No auto-fix code paths.
   **Expect:** `python3 tools/style-check.py --help` exits 0 showing the three modes;
   `python3 tools/style-check.py /nonexistent` exits 2 with a one-line error.
   **Failure signal:** traceback on `--help`, or exit 0 on the nonexistent path.
   **Counter-move:** fix argparse wiring. If the minimal frontmatter parser is what's fighting
   you after two attempts (block scalars are the classic trap), switch to
   `try: import yaml … except ImportError: sys.exit("PyYAML required — pip install pyyaml")`
   and note the dependency in the docstring + result notes. If a third attempt still can't
   produce a clean `--help` → **Abort A2** (something environmental is wrong; park with the
   traceback).

2. **Do:** Implement `--self-test`: using `tempfile.TemporaryDirectory()`, write fixture
   artifacts and assert verdicts. Fixtures (each a dir with primary file + `provenance.json`
   (`{}` is fine — existence only) + `_source/origin.md` unless the fixture is ABOUT breaking
   layout): **good** — passes everything (trigger-only description with "Use when:" + 3 quoted
   phrases, ≤2 sentences, Behavior/Output/Anti-patterns sections, no stack/marketing words,
   kebab-case name matching dir); **bad-frontmatter** — no `description` key → SC1;
   **bad-description** — workflow-summary description ("This skill will read all the comments,
   decide which are valid, then fix them.") → SC5; **bad-marketing** — body contains
   "comprehensive" and "powerful" → SC7; **bad-stack** — body line "Run `npm test` to check
   tests pass" → SC8; **stack-ok-suppressed** — same npm line plus `<!-- stack-ok -->` on it →
   NO SC8 FAIL; **bad-layout** — no provenance.json, empty `_source/` → SC12 + SC13;
   **bad-sections** — no `## Anti-patterns` → SC10. Assertions: `good` verdict == pass; each
   `bad-*` verdict == fail AND its named SC id is among the findings; `stack-ok-suppressed`
   verdict == pass. Print one line per assertion + summary `self-test: N/N passed`; exit 0
   all-pass else 1.
   **Expect:** `python3 tools/style-check.py --self-test` exits 0, summary shows ≥10 assertions,
   all passing.
   **Failure signal:** any assertion fails, or the self-test crashes.
   **Counter-move:** a failing assertion here is the tool telling you a check is mis-implemented
   — fix the CHECK (or, if the fixture itself is wrong, the fixture) and re-run. Iterate freely;
   this loop is the point of self-test. If after real effort one specific check can't be made
   mechanically reliable (SC6 sentence-counting is the likely one) → **Fork F3**.

3. **Do:** Prove graceful degradation on today's empty library, from the repo root:
   `python3 tools/style-check.py --all` and
   `python3 tools/style-check.py --all --format json`.
   **Expect:** exit 0 both times; text mode prints the `no artifacts found` line; JSON mode
   prints `{"artifacts": [], "verdict": "pass"}`. If Recon 4 hit **Fork F1 Route B** instead:
   exit 0 or 1 is fine — record the per-artifact report in your result notes and change NOTHING
   in canonical/ (report-only; fixing artifacts is T3-02's job).
   **Failure signal:** traceback, or exit 2 on the empty scan (empty is not an error).
   **Counter-move:** fix the `--all` glob/empty-list path (`canonical/skills` etc. not existing
   yet must not raise). Re-run.
4. **Do:** Update the two promising docs (surgical, additive-minimal edits only). **(a)**
   `docs/canonical-form-spec.md` line 5: delete the words `(when written) ` so it reads
   "Validate after authoring with `tools/style-check.py` or by manual review against the
   checklist at the bottom." **(b)** `docs/ingestion-workflow.md` step 8: per **Fork F2** —
   Route B (verify-provenance.py still absent, the authoring-time state): change the preamble
   line to `Run \`python3 tools/style-check.py canonical/<type>/<name>/\` — it covers the
   style/layout items below. Provenance-content items stay manual until
   \`tools/verify-provenance.py\` exists:` and keep every checkbox bullet intact; Route A
   (T3-03 landed first): the preamble instead names both tools and drops the "until…exist"
   clause — still keep the bullets. Do not renumber steps or touch anything else in either doc.
   **Expect:** `grep -c "when written" docs/canonical-form-spec.md` → 0;
   `grep -c "style-check.py" docs/ingestion-workflow.md` → ≥1; `git diff --stat` shows exactly
   these two docs changed with single-digit line counts.
   **Failure signal:** diff shows other hunks, or a checklist bullet vanished.
   **Counter-move:** `git checkout -- <doc>` and redo the edit surgically.
5. **Do:** Commit and push (dark-factory repo only). Stage exactly: `tools/style-check.py`,
   `docs/canonical-form-spec.md`, `docs/ingestion-workflow.md`. Message:
   `feat(tools): style-check.py — automated ratification checklist (wg-t3-04)`.
   **Expect:** push succeeds; `git status --porcelain` shows none of YOUR files remaining.
   **Failure signal:** push rejected (remote ahead — other war-game tickets land in parallel
   this cycle).
   **Counter-move:** `git pull --rebase` then push. Conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — canonical/ artifacts exist at execution time.**
Trigger: Recon 4 finds artifact dirs under `canonical/skills|agents|commands/` (T3-01's first
ingestion raced ahead of this ticket).
→ **Route A** (default; library empty as at authoring): verification rests entirely on
`--self-test` + the empty-`--all` run. Nothing else changes.
→ **Route B** (artifacts exist): additionally run `python3 tools/style-check.py --all` and paste
the per-artifact report into your result notes — **report-only**. Do not edit any artifact, do
not touch canonical/INDEX.md, do not "helpfully fix" failures: draft artifacts legitimately fail
pre-ratification, and acting on the report is T3-02's (voice-review + ratify) job.

**F2 — verify-provenance.py existence (docs wording).**
Trigger: Recon 5.
→ **Route A** (T3-03 landed; the file exists): ingestion-workflow step-8 preamble names both
tools; no "until…exist" clause remains.
→ **Route B** (absent — authoring-time state): preamble names style-check.py only and keeps the
"provenance items manual until verify-provenance.py exists" caveat.

**F3 — a check resists mechanical implementation.**
Trigger: Move 2's counter-move loops — one specific SC check (most likely SC6
sentence-counting) cannot be made to pass its own fixtures reliably.
→ **Route A** (heuristic is close but edge-casey): demote that check's level to WARN, add a
`# HEURISTIC:` comment in code naming the failure mode, adjust its fixture assertion to
expect WARN, and note it in the result. The checklist item stays *surfaced*, just non-blocking.
→ **Route B** (check is genuinely non-mechanical): emit it as level `MANUAL` (a third level that
never affects exit code, printed so a human ratifier sees the reminder), fixture asserts the
MANUAL line appears. Never silently drop a checklist item — every ratification-checklist item
must appear in output as FAIL, WARN, or MANUAL.

## Assumptions ledger

1. **Scope split with T3-03 (verify-provenance.py):** style-check owns SKILL.md style + layout
   *existence* (SC12/SC13); provenance *content* validation (the 8 schema rules) is T3-03's.
   Plausible: both docs name the two tools separately with exactly this division. **If false**
   (David wants one merged tool): the split is additive — verify-provenance can later import or
   absorb this file; note the question in your result, no park needed.
2. **`argument-hint` absence is WARN, not FAIL.** The frontmatter template says "Omit if none"
   while the ratification checklist says "argument-hint (or noted N/A)" — a genuine internal
   contradiction in canonical-form-spec.md, resolved here in favor of the template (omission =
   the N/A note). **If false** (David wants strict presence): it's a one-character level flip in
   the LEVELS constant; note in result.
3. **SC7/SC8 word lists are seeds, not law.** Sourced from david-style-patterns.md's examples;
   real artifacts will surface false positives (e.g. "advanced" in a legit phrase). **If false**
   (first real run is noisy): tune the module-level constants, don't re-architect; the
   `stack-ok` suppression marker is the pressure valve. If David objects to the marker syntax
   itself, park to needs-decision with a proposed alternative.
4. **Primary-file name for agents/commands.** canonical-form-spec.md shows `SKILL.md` and says
   "same shape" for agents/commands without naming their primary file; the tool accepts
   `SKILL.md`/`AGENT.md`/`COMMAND.md`. **If false** (first real agent artifact uses another
   name): add it to the accepted-names constant; if the spec gets amended to a single answer,
   follow the spec.
5. **Stdlib-only is the right dependency posture.** engine/ and tools/ have zero `import yaml`
   today and project-digest's ethos is stdlib-only; PyYAML exists locally but is unverified on
   Roamy/fleet. **If false** (the minimal parser proves unreliable — Move 1's counter-move):
   fall back to PyYAML with a clear ImportError message; note the new dependency in the result.

## Abort conditions

- **A1 — the work already landed (race).** Recon 1 finds `tools/style-check.py` exists. Park:
  write `engine/store/needs-decision/wg-t3-04-style-check-tool.json` with
  `{"ticket": "wg-t3-04-style-check-tool", "question": "tools/style-check.py already exists (found at recon). Verify-and-close against the existing implementation, or rebuild per the war game?", "observed": "<ls -la output + first 30 lines of the existing file>"}`.
  Leave this ticket in `running/`. Do not overwrite or "improve" the existing file.
- **A2 — seam conflict or environment failure.** Recon 7 shows uncommitted changes in tools/ or
  the two target docs, or Move 1's counter-move fails three times on basic CLI wiring. Park with
  the `git status` / traceback evidence and the question "who owns this seam right now / is the
  python env broken?".
- **A3 — ground-truth docs missing or self-contradictory.** canonical-form-spec.md or
  david-style-patterns.md is missing/moved, the Ratification checklist section is gone, or a
  live checklist item contradicts this war game's check table (not merely extends it). Park with
  the diff/quote and the question "spec moved under wg-t3-04 — which document is authoritative
  for the checker's rules?". Never implement checks against a spec you can't locate.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting paths;
  do not resolve other people's conflicts.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
cd $DF

# 1. Tool exists and the three modes work
test -f tools/style-check.py && echo exists-ok
python3 tools/style-check.py --help > /dev/null && echo help-ok
python3 tools/style-check.py --self-test          # exit 0, "self-test: N/N passed", N >= 10
python3 tools/style-check.py --all; echo "all-exit=$?"          # exit 0 (empty library: prints 'no artifacts found'; F1-B: real report, 0 or 1)
python3 tools/style-check.py --all --format json | python3 -c "import json,sys; d=json.load(sys.stdin); assert 'artifacts' in d and 'verdict' in d; print('json ok', d['verdict'])"

# 2. Exit-code contract
python3 tools/style-check.py /nonexistent-dir >/dev/null 2>&1; test $? -eq 2 && echo "exit-2 ok"

# 3. A live bad artifact FAILs with the right check ids (throwaway, never under canonical/)
T=$(mktemp -d)/bad-skill && mkdir -p $T
printf -- '---\nname: bad-skill\ndescription: This skill will comprehensively review your code.\n---\n\n# Bad\n\nRun `npm test` to check.\n' > $T/SKILL.md
python3 tools/style-check.py $T >/dev/null 2>&1; test $? -eq 1 && echo "fail-exit ok"
python3 tools/style-check.py $T --format json | python3 -c "import json,sys; d=json.load(sys.stdin); ids={f['id'] for a in d['artifacts'] for f in a['findings']}; assert {'SC5','SC7','SC8','SC12','SC13'} <= ids, ids; print('check-ids ok')"

# 4. Docs updated
grep -c "when written" docs/canonical-form-spec.md               # → 0
grep -c "style-check.py" docs/canonical-form-spec.md             # → ≥ 1 (the promise line survives, minus the caveat)
grep -c "style-check.py" docs/ingestion-workflow.md              # → ≥ 1
grep -c '\[ \]' docs/ingestion-workflow.md                       # → ≥ 8 (step-8 checklist bullets all preserved)

# 5. Negative checks — what must NOT have changed
git diff HEAD~1 --stat -- canonical/ | wc -l                     # → 0 (canonical/ untouched, incl. INDEX.md)
git diff HEAD~1 --stat -- research/ engine/ | wc -l              # → 0 (frozen corpus + engine untouched)
test ! -f tools/verify-provenance.py && echo "no-scope-creep ok" # (skip this line if F2 Route A — T3-03 owns that file)
grep -c "def fix\|--fix\|autofix" tools/style-check.py           # → 0 (report-only, no auto-fix)

# 6. Committed and pushed
git status --porcelain -- tools/style-check.py docs/canonical-form-spec.md docs/ingestion-workflow.md | wc -l   # → 0
git log --oneline -1 -- tools/style-check.py                     # shows the wg-t3-04 commit
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT build `tools/verify-provenance.py` or validate provenance.json content
  (sibling ticket T3-03). Do NOT ingest anything, create anything under `canonical/`, or edit
  `canonical/INDEX.md`. Do NOT touch `research/` (frozen corpus), `engine/` (no orchestrator
  wiring, no hooks, no cron — a standing scheduled check is a commitment David hasn't made).
  Do NOT add an auto-fix mode. Do NOT pip-install anything. Fixtures live ONLY in tempdirs —
  never commit fixture artifacts into the repo.
- **The rabbit hole: linguistic perfection on SC5/SC6.** Sentence-splitting and trigger-phrase
  counting invite an NLP yak-shave. Don't. These are heuristics anchored by the self-test
  fixtures; if a heuristic can't be made reliable, Fork F3 gives you WARN/MANUAL demotion —
  a surfaced reminder beats a clever false-positive machine. Timebox each check; the whole
  script should stay under ~350 lines.
- **The live spec is authoritative.** This war game's SC table is a snapshot of
  canonical-form-spec.md as of 2026-07-06. If the live checklist gained items, implement them;
  if it contradicts the table, Abort A3 — never ship a checker that disagrees with its own spec.
- **Style:** stdlib-only, small pure functions, module-level constants for word lists and
  levels (they WILL be tuned after the first real ingestion), honest degradation (empty library
  → friendly exit 0, not a stack trace). Match project-digest's tone: report honestly, never
  guess.
- **Prefer parking over guessing** on any race signal (A1/A2) — T3-01/T3-02/T3-03 all touch this
  neighbourhood in the same portfolio cycle; if you find half-landed work, park, don't merge by
  guess.
