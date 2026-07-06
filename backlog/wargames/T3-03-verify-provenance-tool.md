# T3-03 — Build tools/verify-provenance.py

| field | value |
|---|---|
| ticket | wg-t3-03-verify-provenance-tool |
| track / size / priority | T3 Ingestion / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Build `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/verify-provenance.py` — the executable
form of the 8 validation rules in `docs/provenance-spec.md` §"Validation rules" (lines 121–132 at
authoring), which today exist only as a manual checklist (`docs/ingestion-workflow.md` Step 8).
Every later T3 ingestion ticket (starting with T3-01 `review-dimensional`) gates on this tool, so
it must ship BEFORE any artifact exists to validate: `canonical/` holds only `INDEX.md` today
(verified 2026-07-06). Therefore the tool carries its own proof — a `--self-test` mode that
builds pass/fail fixtures in a temp dir and demonstrates every rule firing correctly. Done looks
like: a single stdlib-only Python script at `tools/verify-provenance.py`; self-test green; sane
behaviour on the empty real `canonical/`; the two docs that say "when written" / "until … exists"
updated to point at the real tool; committed and pushed.

## Locked context

- **Q2 (decisions.md):** ingestion is a full campaign — validators are explicitly in scope; this
  is the first validator.
- **Q4 (decisions.md):** everything through the engine — this war game is written for sonnet
  Swagger dispatch.
- **No YLO/POEM work; no `-p`/headless/SDK ever; interactive `claude` only** — moot here (pure
  Python + docs; nothing spawns Claude).
- **Hard rule (CLAUDE.md): never auto-rewrite a ratified canonical artifact.** The validator
  READS artifacts and reports; it must never modify anything under `canonical/`. If Fork F1
  Route B finds real artifacts that fail validation, you report — you do not fix them.
- **Docs lag code (wargame-spec):** the 8 rules were read from disk at authoring; your Recon
  re-reads them at execution time and aborts if they changed semantically (A1).

## Recon (verify before any work)

All paths absolute; repo root `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`.

1. `ls $DF/tools/verify-provenance.py` → expect **No such file** (did not exist 2026-07-06;
   `tools/` held only `design-lint/`, `mocha-census/`, `youtube-assets/`, `serve.sh`, `stop.sh`).
   If it exists → the work landed in a race → **Abort A2**.
2. `sed -n '121,132p' $DF/docs/provenance-spec.md` → expect the section
   `## Validation rules (for `tools/verify-provenance.py`)` followed by exactly 8 numbered rules
   covering, in order: (1) JSON parses, (2) required fields present, (3) every
   `origins[i].verbatim_copy` exists relative to the artifact folder, (4) no orphan files in
   `_source/`, (5) `rewrite_status` in draft|in-style|ratified, (6) `version` positive integer,
   (7) `version_history[]` has `version - 1` entries, (8) no empty `origins[i].kept`. Line
   numbers may drift — search for the heading if 121 is off. If the rule COUNT or any rule's
   SUBJECT differs from this list → the spec moved under the war game → **Abort A1**.
3. `sed -n '85,110p' $DF/docs/provenance-spec.md` → expect the field-rules table marking
   `source_commit`, `source_url`, and `research_sources.*` as **recommended** (not required) —
   this grounds the FAIL-vs-WARN split in Move 1. Table gone/reshaped → **Abort A1**.
4. `ls $DF/canonical/` → expect exactly `INDEX.md` (zero artifacts, verified 2026-07-06). If
   artifact folders exist (e.g. `canonical/skills/review-dimensional/`) → T3-01 or another
   ingestion landed first → **Fork F1 Route B** (not an abort — it changes Move 3, nothing else).
5. `python3 --version` → expect ≥ 3.9 (authored against 3.14.5). Only stdlib is needed
   (`json`, `sys`, `argparse`, `pathlib`, `tempfile`, `shutil`, `re`). Python missing/ancient →
   **Abort A3**.
6. `grep -n "Manual checklist (until" $DF/docs/ingestion-workflow.md` → expect one hit (~line 99:
   ``Manual checklist (until `tools/verify-provenance.py` and `tools/style-check.py` exist):``)
   and `grep -n "(when written)" $DF/docs/provenance-spec.md` → expect one hit (~line 5). These
   are Move 4's edit targets. If a wording drifted, find the equivalent sentence and adapt the
   edit; if a target sentence is gone entirely, skip that single edit and note it in the result.
7. `git -C $DF status --porcelain -- tools/ docs/provenance-spec.md docs/ingestion-workflow.md`
   → expect empty. Dirt on any of these exact paths → someone is mid-change on your seam →
   **Abort A2** (same park question: race or concurrent edit).

## Moves

1. **Do:** Write `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/verify-provenance.py` — one
   stdlib-only Python file (imports limited to: `json`, `sys`, `os`, `re`, `argparse`,
   `pathlib`, `tempfile`, `shutil`). Implement this contract exactly:
   - **Invocation:** `python3 tools/verify-provenance.py <artifact-dir> [<artifact-dir>...]`
     where each artifact-dir is a folder containing `provenance.json`
     (e.g. `canonical/skills/review-dimensional`). Plus two flag modes: `--all` (glob
     `canonical/*/*/provenance.json` under the repo root, computed as
     `Path(__file__).resolve().parent.parent` so it works from any cwd) and `--self-test`
     (Move 2). No args and no flag → print usage to stderr, **exit 2**.
   - **Exit codes:** `0` = every checked artifact passes all 8 rules (including `--all` finding
     zero artifacts — print `no artifacts found under canonical/` and exit 0; an empty library
     is not an error). `1` = at least one FAIL finding. `2` = usage/IO error (a named
     artifact-dir doesn't exist or lacks `provenance.json`).
   - **Output:** one line per finding — `FAIL <artifact-dir> R<n>: <detail>` for rule
     violations, `WARN <artifact-dir>: <detail>` for non-fatal advisories — then a summary line
     `checked N artifact(s): P pass, F fail`. WARNs never affect the exit code.
   - **The 8 rules (FAIL class), numbered R1–R8 matching the spec:**
     - **R1** `provenance.json` parses as JSON (`json.JSONDecodeError` → FAIL R1 and skip
       R2–R8 for that artifact — nothing else is checkable).
     - **R2** all required fields present, one FAIL line per missing field using dotted paths
       (e.g. `origins[1].set_aside`). Required top-level: `canonical_id`, `canonical_type`,
       `canonical_name`, `version`, `rewrite_status`, `rewrite_date`, `rewrite_author`,
       `origins` (must be a non-empty list), `version_history` (must be a list). Required
       per-origin: `source_repo`, `source_path`, `harvested_at`, `verbatim_copy`, `kept`,
       `modified`, `set_aside`.
     - **R3** every `origins[i].verbatim_copy`, resolved relative to the artifact dir, exists
       on disk. A **directory** is acceptable (the spec's multi-file-origin subfolder rule,
       provenance-spec.md "Verbatim copy rules"); a missing path is the failure.
     - **R4** no orphans: walk `_source/` recursively (skip `.DS_Store`); each file must be
       referenced — its artifact-relative path either equals some `verbatim_copy` value or sits
       under a directory named by one. Unreferenced file → one FAIL R4 line naming it. No
       `_source/` dir → no orphans possible → R4 passes.
     - **R5** `rewrite_status` ∈ {`draft`, `in-style`, `ratified`}.
     - **R6** `version` is an integer ≥ 1 — reject bools explicitly (`type(v) is int`, not
       `isinstance`, because `True` is an `int` in Python) and reject numeric strings.
     - **R7** `len(version_history) == version - 1`. Only evaluated when R6 passes (a garbage
       version can't anchor the count).
     - **R8** every `origins[i].kept` is a non-empty list.
   - **WARN class (advisory only, grounded in the spec's "recommended" markers — Recon 3):**
     origin missing `source_commit` or `source_url`; top-level `research_sources` absent;
     `canonical_id` not matching `dark-factory:<canonical_type>:<canonical_name>`;
     `rewrite_date`/`harvested_at` not `YYYY-MM-DD`.
   - Top-of-file docstring: state the source of truth (`docs/provenance-spec.md` §Validation
     rules), the exit-code contract, and the directory-tolerant R3/R4 semantics (Assumption 1).
   **Expect:** file exists; `python3 $DF/tools/verify-provenance.py` (no args) exits 2 with a
   usage line; `grep -E "^(import|from)" $DF/tools/verify-provenance.py` shows only the stdlib
   modules listed above.
   **Failure signal:** any third-party import, or the no-args call exits 0/crashes.
   **Counter-move:** rewrite the offending part — there is no dependency this tool could
   legitimately need. If you can't get argparse behaviour right (argparse exits 2 on its own
   usage errors; the no-args case you must raise yourself via `parser.error(...)`), fall back to
   manual `sys.argv` handling; a second full failure to produce a runnable script → **Abort A3**.

2. **Do:** Implement `--self-test` inside the same file: using `tempfile.mkdtemp()`, build
   fixture artifact dirs and assert the validator's behaviour on each, printing one line per
   case (`ok <case>` / `FAILED <case>: <why>`) and a final `self-test: <n>/<n> cases ok`; exit 0
   iff all pass, else 1; always `shutil.rmtree` the temp dir. Exactly these 11 cases:
   1. `clean` — fully valid artifact: all required fields; 2 origins — one with a plain-file
      `verbatim_copy` (`_source/repo-a--skill.md`), one with a **directory** `verbatim_copy`
      (`_source/repo-b--bundle/` containing `SKILL.md` + `references/notes.md`); `version: 2`
      with exactly 1 `version_history` entry; recommended fields present → expect 0 FAIL, 0 WARN,
      artifact passes.
   2. `r1-garbage` — `provenance.json` containing `{not json` → expect FAIL R1 and NO other
      rule ids reported.
   3. `r2-missing-fields` — clean copy minus `rewrite_author` and minus `origins[0].set_aside`
      → expect exactly 2 FAIL R2 lines, naming both dotted paths.
   4. `r3-missing-verbatim` — an origin whose `verbatim_copy` names a nonexistent file →
      expect FAIL R3.
   5. `r4-orphan` — an extra unreferenced `_source/stray.md` → expect FAIL R4 naming
      `stray.md`.
   6. `r5-bad-status` — `rewrite_status: "final"` → expect FAIL R5.
   7. `r6-zero` — `version: 0` → expect FAIL R6.
   8. `r6-bool` — `version: true` → expect FAIL R6 (the bool trap).
   9. `r7-history-mismatch` — `version: 3` with 1 history entry → expect FAIL R7.
   10. `r8-empty-kept` — one origin with `kept: []` → expect FAIL R8.
   11. `warn-only` — valid artifact with NO `source_commit`/`source_url`/`research_sources` →
      expect ≥1 WARN, 0 FAIL, and per-artifact verdict **pass** (proves recommended ≠ required).
   Each case must assert both the presence of the expected rule id AND the absence of unexpected
   FAIL rule ids (a validator that fails everything would otherwise self-test green).
   **Expect:** `python3 $DF/tools/verify-provenance.py --self-test` exits 0 printing 11 `ok`
   lines and `self-test: 11/11 cases ok`.
   **Failure signal:** any `FAILED <case>` line, nonzero exit, or a traceback.
   **Counter-move:** the failing case names the broken rule — fix that rule's implementation
   (usual culprits: path-relativity in R3/R4 — everything resolves against the artifact dir, not
   cwd; the R6 bool trap; R7 firing when R6 already failed). Re-run after each fix. If after
   three fix rounds self-test still fails → **Abort A3** with the failing case output.

3. **Do:** Run the tool against the real repo, all invocation shapes:
   `python3 $DF/tools/verify-provenance.py --all` (per Recon 4 / Fork F1: on today's empty
   library this is the honest-zero path); then the error shapes:
   `python3 $DF/tools/verify-provenance.py /nonexistent-dir` and
   `python3 $DF/tools/verify-provenance.py $DF/tools` (exists, but no provenance.json).
   **Expect:** `--all` → exit 0, prints `no artifacts found under canonical/` (Route A) or a
   per-artifact report (Route B — see Fork F1 for what to do with failures). Both error shapes
   → exit 2 with a one-line explanation, no traceback.
   **Failure signal:** traceback on any shape, `--all` exiting nonzero on the empty library, or
   error shapes exiting 0/1.
   **Counter-move:** fix and re-run Move 2's self-test afterwards (a fix here must not break a
   fixture there). Second-order failure → **Abort A3**.

4. **Do:** Update the two docs that promised this tool (Recon 6 targets; minimal, surgical
   edits): **(a)** `$DF/docs/provenance-spec.md` line ~5 — replace
   `Validate with `tools/verify-provenance.py` (when written) or manually against the checklist below.`
   with
   `Validate with `tools/verify-provenance.py` (run `python3 tools/verify-provenance.py <artifact-dir>`, or `--all` for the whole library; `--self-test` proves the rules) or manually against the checklist below.`
   **(b)** `$DF/docs/ingestion-workflow.md` line ~99 — replace
   ``Manual checklist (until `tools/verify-provenance.py` and `tools/style-check.py` exist):``
   with
   ``Checklist — the first three items are now automated: run `python3 tools/verify-provenance.py <artifact-dir>` (exit 0 = pass). The style items remain manual until `tools/style-check.py` exists:``
   Touch nothing else in either file — in particular do NOT renumber, restate, or "improve" the
   8 rules themselves (the spec stays the single source of truth; the script cites it).
   **Expect:** `grep -c "(when written)" $DF/docs/provenance-spec.md` → 0;
   `grep -c "Manual checklist (until" $DF/docs/ingestion-workflow.md` → 0; both files' diffs are
   one-line substitutions (`git -C $DF diff --stat docs/` shows 2 files, ~2 insertions,
   ~2 deletions).
   **Failure signal:** diff shows edits beyond the two sentences.
   **Counter-move:** `git -C $DF checkout -- docs/` and redo as pure single-sentence
   substitutions.

5. **Do:** Commit and push (dark-factory only — everything lives in this one repo). Stage
   exactly: `tools/verify-provenance.py`, `docs/provenance-spec.md`,
   `docs/ingestion-workflow.md`. Message:
   `feat(tools): verify-provenance.py — the 8 provenance rules, executable (self-test 11/11)`.
   Leave any stranger's dirt unstaged.
   **Expect:** `git push` succeeds; `git -C $DF status --porcelain` no longer lists your three
   files.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; on a conflict in a file you touched, resolve
   keeping both intents; on a conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — does `canonical/` contain real artifacts at execution time?**
Trigger: Recon 4's `ls` (and `ls $DF/canonical/*/*/provenance.json 2>/dev/null`).
→ **Route A** (default; state at authoring): only `INDEX.md` exists. Move 3's `--all` proves the
honest-zero path (`no artifacts found`, exit 0). Nothing else changes.
→ **Route B**: one or more real artifacts exist (T3-01 or another ingestion landed first). Run
`--all`; the report over real artifacts becomes part of your result notes. **Do not edit any
artifact under `canonical/` regardless of what fails** (locked context: never auto-rewrite; a
draft's defects belong to its ingestion ticket, not to you). If a **ratified** artifact FAILs
any rule, that is a contradiction between the library's ratification claim and its own spec —
additionally write `engine/store/needs-decision/wg-t3-03-verify-provenance-tool.json` with the
finding (this park is informational; it does NOT stop the ticket — the tool itself is done and
verified via self-test, so finish Moves 4–5 and mark done).

## Assumptions ledger

1. **Directory-valued `verbatim_copy` is legal (R3/R4 semantics).** The spec's schema comment
   says verbatim_copy is a path to `_source/<repo>--<file>.md`, but its "Verbatim copy rules"
   section explicitly allows multi-file origins to live in a `_source/<repo>--<name>/` subfolder
   — without saying what `verbatim_copy` holds in that case. Pinned default: a `verbatim_copy`
   may name a directory; files under a referenced directory count as referenced for R4. This is
   the only reading that lets the two spec sections coexist. **If false** (David later rules
   file-only): it's a two-line tightening in R3/R4 plus one fixture change — note the pinned
   semantics in the script docstring and the result notes so the decision is visible; no park
   needed.
2. **Checks beyond the 8 numbered rules are WARN, never FAIL.** Plausible: the spec numbers
   exactly 8 enforcement rules for this tool by name; everything else in the field table is
   schema commentary, and `source_commit`/`source_url`/`research_sources` are explicitly
   "recommended". **If false** (David wants id-format or date-format fatal): flip those findings
   from WARN to FAIL — they're already computed; note the split in the result so triage can
   object cheaply.
3. **A single file at `tools/verify-provenance.py` (not a subfolder tool like `design-lint/`) is
   the right shape.** Plausible: both `docs/provenance-spec.md` and `docs/ingestion-workflow.md`
   name that exact path, twice. **If false**: moving a self-contained script into a folder later
   is trivial; do not pre-build the folder.
4. **The exit-code contract (0/1/2) is this ticket's to pin.** No doc specifies exit codes;
   later T3 tickets (T3-01's Step-8 gate) need SOMETHING checkable, and 0-pass/1-fail/2-usage is
   the POSIX-conventional choice already used implicitly by the repo's Python CLIs. **If false**
   (a later consumer needs a different contract): additive change; the contract is documented in
   the docstring so no consumer can be surprised silently.

## Abort conditions

- **A1 — the spec moved.** Recon 2/3 find the validation-rules section changed semantically
  (different rule count, different subjects, or the required/recommended split gone). The tool
  must encode the living spec, not this war game's snapshot of it. Park: write
  `engine/store/needs-decision/wg-t3-03-verify-provenance-tool.json` with
  `{"ticket": "wg-t3-03-verify-provenance-tool", "question": "provenance-spec.md's validation rules no longer match the war-gamed 8-rule contract — re-author the validator contract against the current spec, or was the spec edit unintended?", "observed": "<the current rules section verbatim>"}`.
  Leave the ticket in `running/`. Never encode a rule set nobody ratified.
- **A2 — race or seam conflict.** `tools/verify-provenance.py` already exists (Recon 1), or
  Recon 7 shows uncommitted edits on the exact target files. Park with question:
  "wg-t3-03's target exists / is mid-edit (found: <what and where>). Verify-and-close against
  the existing implementation, or redo per the war game?" Do not overwrite someone's
  half-landed work.
- **A3 — the tool can't be made sound.** Python env broken (Recon 5), Move 1 twice fails to
  produce a runnable script, Move 2 self-test still red after three fix rounds, or a Move 3 fix
  breaks self-test irrecoverably. Park with the failing output attached. A provenance validator
  that is itself unverified is worse than the manual checklist — never ship it red.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory

# 1. The tool exists and is stdlib-only
test -f $DF/tools/verify-provenance.py && echo exists-ok
grep -E "^(import|from) " $DF/tools/verify-provenance.py   # only: json/sys/os/re/argparse/pathlib/tempfile/shutil

# 2. Self-test: all 11 cases green
python3 $DF/tools/verify-provenance.py --self-test; echo "exit=$?"          # prints 11 'ok' lines + 'self-test: 11/11 cases ok'; exit=0

# 3. Real library: honest zero (or Route-B report), exit 0
python3 $DF/tools/verify-provenance.py --all; echo "exit=$?"                # 'no artifacts found under canonical/' (or per-artifact report); exit=0

# 4. Error shapes exit 2, no tracebacks
python3 $DF/tools/verify-provenance.py /nonexistent-dir 2>&1; echo "exit=$?"          # exit=2
python3 $DF/tools/verify-provenance.py $DF/tools 2>&1;       echo "exit=$?"           # exit=2 (no provenance.json)
python3 $DF/tools/verify-provenance.py 2>&1;                 echo "exit=$?"           # usage; exit=2

# 5. Live negative demo: a hand-broken artifact FAILs R8 and exits 1
T=$(mktemp -d); mkdir -p $T/art/_source; echo x > $T/art/_source/repo--f.md
cat > $T/art/provenance.json <<'EOF'
{"canonical_id":"dark-factory:skill:demo","canonical_type":"skill","canonical_name":"demo",
 "version":1,"rewrite_status":"draft","rewrite_date":"2026-07-06","rewrite_author":"test",
 "origins":[{"source_repo":"repo","source_path":"/tmp/x","harvested_at":"2026-07-06",
 "verbatim_copy":"_source/repo--f.md","kept":[],"modified":[],"set_aside":[]}],
 "version_history":[]}
EOF
python3 $DF/tools/verify-provenance.py $T/art; echo "exit=$?"               # FAIL … R8 …; exit=1
python3 $DF/tools/verify-provenance.py $T/art 2>&1 | grep -c "R8"           # ≥ 1
rm -rf $T

# 6. Docs updated, surgically
grep -c "(when written)" $DF/docs/provenance-spec.md                        # → 0
grep -c "Manual checklist (until" $DF/docs/ingestion-workflow.md            # → 0
grep -c "verify-provenance.py" $DF/docs/ingestion-workflow.md               # → ≥ 1 (still referenced)

# 7. Negative checks — what must NOT have changed
ls $DF/tools/style-check.py 2>&1                                            # No such file (NOT built here)
git -C $DF status --porcelain -- canonical/ research/ | wc -l               # → 0 (validator is read-only on the library)
git -C $DF diff HEAD~1 --stat -- docs/ | tail -1                            # ~2 insertions/2 deletions across the 2 docs

# 8. Committed and pushed
git -C $DF log --oneline -1                                                 # the feat(tools) commit
git -C $DF status --porcelain | grep -c "verify-provenance\|provenance-spec\|ingestion-workflow"   # → 0
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT build `tools/style-check.py` (its own T3 ticket). Do NOT perform any
  ingestion or create anything under `canonical/` — fixtures live ONLY in `tempfile` dirs that
  you delete. Do NOT touch `research/` (frozen corpus, read-only). Do NOT modify `canonical/INDEX.md`.
  Do NOT restate or renumber the 8 rules inside the docs — the spec owns them; the script cites
  the spec. Do NOT touch `engine/*.py`, `tools/design-lint/`, or `tools/mocha-census/`.
- **The rabbit hole: validating SKILL.md form.** `docs/ingestion-workflow.md` Step 8 mixes
  provenance checks (items 1–3) with style/form checks (frontmatter fields, trigger-only
  description, David-style sections, ≤400 lines). Those last five belong to `style-check.py` /
  `canonical-form-spec.md` — a different tool, a different ticket. If you find yourself parsing
  SKILL.md frontmatter, stop: this tool reads `provenance.json` and the `_source/` tree, nothing
  else.
- **Style:** match the repo's Python-tool idiom (project-digest, mocha-census): stdlib only,
  small pure functions, honest degradation ("no artifacts found" is a pass, not an error), no
  cleverness. One finding per line, machine-greppable (`FAIL … R<n>:` prefix) — later ingestion
  tickets will grep this output in their own verify blocks.
- **Prefer parking over guessing** on any A1/A2 signal — this tool becomes the gate for the
  whole T3 campaign; a validator built on a guessed rule set poisons every downstream ticket.
