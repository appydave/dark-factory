# T3-17 — LLM-judge calibration (Gap B)

| field | value |
|---|---|
| ticket | wg-t3-17-judge-calibration |
| track / size / priority | T3 Ingestion / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Close eval-architecture Gap B (`docs/eval-architecture.md` §"Gap B", line ~67): the factory's
LLM-judges run uncalibrated while David's human labels sit unused as a ready-made calibration set.
Build `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/judge-calibration/` — a stdlib-only
scorer + a pinned judge prompt — then run one blind calibration pass: a sonnet judge tiers a
stratified 60-shot sample of David-rated design screenshots
(`tools/mocha-census/out/ratings/round-02.json`, 159 entries: 47 love / 54 good / 55 average /
3 null, every one with a PNG in `out/shots/` — verified 2026-07-06), and the scorer reports
agreement (exact %, adjacent %, linear-weighted Cohen's kappa, confusion matrix) plus a
spot-check of design-lint's F3/F4 flags against David's free-text labels. Done looks like: a
`CALIBRATION.md` verdict document pinning judge identity (model string + prompt sha256) and
stating a trust band; the machine report committed under `out/`; the Gap B status line in
`docs/eval-architecture.md` updated; pushed. **Scope honesty (Assumption 5):** this calibrates
the DESIGN judge (design-lint / taste judging). L1-census and L2a-triage judge TEXT artifacts
and have no human-labeled set — they inherit the protocol, not the numbers.

## Locked context

- **Q2 (decisions.md):** ingestion is a full campaign — judge calibration is explicitly named in
  the campaign scope.
- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only (wargame-spec).** The judge therefore
  runs as **in-session subagents** (Read-tool vision on PNGs), never as an API call. "Pin
  model+version" is satisfied as: record the exact model string this session reports + the
  sha256 of `JUDGE-PROMPT.md` (Assumption 2). The engine dispatches workers with
  `MODEL = "sonnet"` (`engine/orchestrator.py` line ~61, verified 2026-07-06).
- **Design-lint guardrails carry over (`tools/design-lint/RUBRIC.md`):** judgment over rules; no
  count-policing; a calibration number is a *report*, never a target to iterate the prompt
  against (the round-04 Goodhart trap).
- **Mocha-census ratings are David's data — READ-ONLY.** Nothing under
  `tools/mocha-census/out/` may be modified by this ticket.
- **Docs lag code (wargame-spec):** all counts above were read from disk at authoring; Recon
  re-verifies at execution and aborts if the calibration set moved (A1).

## Recon (verify before any work)

All paths absolute; repo root `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`.

1. `ls $DF/tools/judge-calibration` → expect **No such file** (did not exist 2026-07-06; `tools/`
   held `design-lint/`, `mocha-census/`, `youtube-assets/`, `serve.sh`, `stop.sh`, plus whatever
   T3-03 added). If it exists → the work landed in a race → **Abort A2**.
2. Truth set intact:
   `python3 -c "import json,collections; d=json.load(open('$DF/tools/mocha-census/out/ratings/round-02.json')); print(len(d), collections.Counter(x.get('rating') for x in d))"`
   → expect ~159 entries and a Counter over exactly `{'love','good','average',None}` with ≥40
   per named tier (authoring: 47/54/55/3). Vocabulary changed, file missing, or any named tier
   <40 → the calibration set moved under the war game → **Abort A1**. Also
   `ls $DF/tools/mocha-census/out/ratings/` — authoring found `round-01.json` (older vocab
   good/meh/shit — NOT the truth set), `round-02.json`, `round-03-result.json` (summary object,
   not per-item), `exemplars.json`, `features.json`, `health.json`. If a **newer full per-item
   round** exists (e.g. `round-04.json` with ≥100 entries in the love/good/average vocabulary)
   → **Fork F2 Route B**.
3. `cat $DF/tools/mocha-census/out/ratings/round-03-result.json` → expect the recalibration
   warning ("round-02 had 47 loves, round-03 has 1… anchor on LABELS + relative order, not tier
   counts"). This grounds the choice of kappa/adjacent as primary metrics. Missing → proceed,
   but note in CALIBRATION.md that the drift evidence is authoring-time only.
4. PNG coverage:
   `python3 -c "import json,os; b='$DF/tools/mocha-census/out/'; r=json.load(open(b+'ratings/round-02.json')); m=[x for x in r if x.get('rating') and not os.path.exists(b+'shots/'+x['repo']+'__'+x['design_id']+'.png')]; print(len(m),'missing')"`
   → expect `0 missing` (authoring: 193 PNGs, avg ~288KB, max ~2MB — all Read-tool readable).
   If >0: sample only from entries whose PNG exists (do NOT re-shoot — screenshots may live on
   the other machine and cross-machine capture is out of scope). If usable tiered entries <30
   total → **Abort A3**.
5. `ls $DF/tools/design-lint/RUBRIC.md $DF/docs/david-design-patterns.md` → both exist (they
   ground JUDGE-PROMPT.md and the flag spot-check). Either missing → **Abort A1**.
6. `grep -n "Gap B" $DF/docs/eval-architecture.md` → expect the heading
   `### Gap B — LLM-judge calibration against the mocha-census labels` (~line 67) with **no**
   status line saying it's closed/calibrated. If a status line already marks it done → **Abort
   A2** (someone ran the calibration already).
7. `python3 --version` → ≥3.9 (authored against 3.14.x; only stdlib needed: `json`, `sys`,
   `os`, `argparse`, `pathlib`, `random`, `hashlib`, `datetime`, `re`). Missing/ancient →
   **Abort A3**.
8. `git -C $DF status --porcelain -- tools/judge-calibration/ tools/design-lint/README.md docs/eval-architecture.md`
   → expect empty. Dirt on these exact paths → someone is mid-change on your seam → **Abort A2**.

## Moves

1. **Do:** Scaffold `/Users/davidcruwys/dev/ad/apps/dark-factory/tools/judge-calibration/` with
   three files:
   - **`calibrate.py`** — one stdlib-only Python file (imports limited to: `json`, `sys`, `os`,
     `argparse`, `pathlib`, `random`, `hashlib`, `datetime`). Three subcommands:
     - `--sample [--per-tier N]` (default N=20): load `round-02.json` (path resolved relative to
       the repo root, computed as `Path(__file__).resolve().parent.parent.parent` — works from
       any cwd); keep entries with `rating` ∈ {love, good, average} AND an existing PNG at
       `tools/mocha-census/out/shots/<repo>__<design_id>.png`; sort by `(repo, design_id)`; per
       tier, `random.Random(42).sample` N entries (or all if the tier has fewer). Write
       **`out/sample.json`** — the judge-facing file: a list of `{"id": "<repo>__<design_id>",
       "img": "<absolute PNG path>"}` with **NO rating field** — and **`out/answers.json`** —
       `{"<id>": "<tier>"}`. Print `sampled <n> (<a>/<b>/<c> love/good/average), seed=42`.
     - `--score`: read `out/verdicts.json` (Move 3's output) + `out/answers.json`; drop ids
       missing from either side (report the drop count); compute over tiers ordered
       average=0 < good=1 < love=2: **n**, **exact agreement %**, **adjacent agreement %**
       (|diff| ≤ 1), **linear-weighted Cohen's kappa**, the 3×3 **confusion matrix** (rows =
       David, cols = judge), per-tier recall/precision, and the **verdict band** (Assumption 1):
       kappa ≥ 0.6 → `calibrated-trusted`; 0.4 ≤ kappa < 0.6 → `calibrated-caution`;
       kappa < 0.4 → `not-trusted`. Write
       `out/calibration-<UTC YYYY-MM-DD>.json` containing all of the above **plus** the
       `judge_meta` object copied verbatim from `verdicts.json`, `sample_seed`, and
       `truth_source: "round-02.json"`; print a human-readable table. Exit 0 when computable;
       exit 2 on IO/schema error.
     - `--self-test`: no fixtures on disk — pure math checks, exactly 4 cases, printing
       `ok <case>` / `FAILED <case>` and `self-test: 4/4 cases ok`, exit 0 iff green:
       1. `perfect` — truth == pred (any mix) → kappa == 1.0, exact == 100%.
       2. `known-fixture` — truth `[2,2,2,1,1,1,0,0,0]`, pred `[2,1,2,1,1,0,0,0,2]` →
          kappa == 0.5 (±0.001), exact == 66.7% (6/9), adjacent == 88.9% (8/9). (Precomputed at
          authoring; if your implementation disagrees, YOUR kappa is wrong — linear weights
          `w[i][j] = 1 - |i-j|/2`.)
       3. `constant-judge` — balanced truth, pred all-`good` → kappa == 0.0 (±0.001) (a judge
          that always says "good" must score zero skill).
       4. `length-mismatch` — mismatched arrays → exit-2 path raised as a caught error, not a
          traceback.
   - **`JUDGE-PROMPT.md`** — the pinned judge instruction. Content: the three tiers defined in
     David's own observed semantics (grounded in `docs/david-design-patterns.md` + the round-02
     label texts): **love** = exemplar-worthy, would go in the love-tier pack; **good** = solid
     and on-brand, gripes are minor; **average** = boring, off-brand, broken, or colour shouting
     over content. Include the design-lint guardrail language (warm-anchor / cool-on-content /
     amber-on-brown / loudness as *judgment*, never counts). Instruct: look at ONE screenshot,
     return strict JSON `{"id": "...", "tier": "love|good|average", "reason": "<=25 words"}`;
     a broken/blank render → `average` with reason "broken" (matches David's own practice in
     round-02). Explicitly: no external context, no file access beyond the named PNG, never
     mention or count colours/diagrams as a rule.
   - **`README.md`** — what this tool is (Gap B closer), the no-API judge mechanism, how to
     re-run on a judge upgrade (`--sample` → judge pass → `--score`, compare kappa across
     `out/calibration-*.json`), and the scope-honesty note (design judge only; census/triage
     text judges need their own human-labeled set — protocol reusable, numbers not).
   **Expect:** `python3 $DF/tools/judge-calibration/calibrate.py --self-test` exits 0 printing
   4 `ok` lines + `self-test: 4/4 cases ok`; `grep -E "^(import|from) " calibrate.py` shows only
   the stdlib modules listed.
   **Failure signal:** any `FAILED` case, traceback, or a third-party import.
   **Counter-move:** case 2 failing means the kappa implementation is wrong — fix against the
   formula (observed/expected weighted agreement over marginals), re-run. Three fix rounds still
   red → **Abort A3**.

2. **Do:** Run `python3 $DF/tools/judge-calibration/calibrate.py --sample`.
   **Expect:** `sampled 60 (20/20/20 love/good/average), seed=42`; `out/sample.json` has 60
   items, each `img` an existing absolute path, **no rating key anywhere in the file**
   (`grep -c rating out/sample.json` → 0); `out/answers.json` has the same 60 ids. Re-running
   produces byte-identical files (deterministic).
   **Failure signal:** <60 items (a tier ran short per Recon 4), rating leakage into
   sample.json, or non-deterministic output.
   **Counter-move:** tier short → proceed with what exists and record actual per-tier counts
   (floor: 30 total, else **Abort A3**). Leakage/non-determinism → fix calibrate.py, re-run
   Move 1's self-test, then re-sample.

3. **Do:** The blind judge pass. **Do not open `out/answers.json` or `round-02.json` from here
   until Move 4** — the judging must be blind. Split `out/sample.json` into 12 batches of 5.
   For each batch, spawn one general-purpose **subagent** (in-session Task; sonnet-class —
   subagents inherit the session model) whose prompt is exactly: read
   `$DF/tools/judge-calibration/JUDGE-PROMPT.md`, then Read each of these 5 PNG paths, and
   return ONLY a JSON array of 5 verdict objects per the prompt's schema. Collect all batches
   into `out/verdicts.json`:
   `{"judge_meta": {"judge_model": "<the exact model string this session reports>", "prompt_sha256": "<sha256 of JUDGE-PROMPT.md>", "mechanism": "in-session subagent, Read-tool vision, interactive Claude Code (no API)", "date": "<UTC ISO>"}, "verdicts": [ ... 60 objects ... ]}`.
   Validate every verdict: `tier` ∈ {love, good, average}, `id` matches a sample id, no
   duplicates. A malformed batch gets ONE retry (same 5 images, fresh subagent); still
   malformed → drop those items and count them.
   **Expect:** ≥48 valid verdicts (≥80%); `judge_meta` complete; every tier value in-vocabulary.
   **Failure signal:** >20% of items dropped after retries, or subagents returning prose
   instead of JSON.
   **Counter-move:** prose responses usually mean the batch prompt buried the schema — restate
   "return ONLY the JSON array" and retry once more (this is a dispatch fix, not a
   JUDGE-PROMPT.md edit — do NOT iterate the judge prompt itself; see Executor notes). Still
   >20% dropped → **Abort A3**. If you cannot determine the exact model string, record
   `"judge_model": "sonnet (session default, exact version string unavailable)"` and note the
   weaker pin in CALIBRATION.md — not an abort.

4. **Do:** Run `python3 $DF/tools/judge-calibration/calibrate.py --score`.
   **Expect:** a printed table + `out/calibration-<date>.json` with n ≥ 48, all metrics present,
   `judge_meta` embedded, and a verdict band. Sanity: kappa must lie in [-1, 1]; the confusion
   matrix must sum to n. **Whatever the number is, it is the result — a low kappa is a
   successful calibration run, not a failure** → route via **Fork F1**.
   **Failure signal:** exit 2, metrics out of range, or matrix sum ≠ n.
   **Counter-move:** a schema mismatch between verdicts.json and answers.json is the usual
   culprit (id normalisation) — fix calibrate.py, re-run self-test, re-score. Do NOT re-run the
   judge pass to "improve" the number. Second-order failure → **Abort A3**.

5. **Do:** Flag spot-check (design-lint's F3/F4 against David's own words). From round-02's 74
   free-text labels (you may read round-02 again now — judging is done), select entries whose
   label matches `orange.{0,15}brown|brown.{0,15}orange` (→ expect F3 flagged; authoring found
   3) or `busy|too much|noisy|loud|overwhelm` (→ expect F4 flagged; authoring found 5). For
   each matched entry with an existing PNG (expect ~8), spawn one lint subagent per the
   design-lint mode-A pattern: read `$DF/tools/design-lint/RUBRIC.md`, Read the PNG, return the
   rubric's JSON verdict. Record into the calibration JSON as
   `"flag_spot_check": {"cases": [{"id", "expected_flag", "flags_returned", "hit": bool}], "hits": X, "total": Y}`.
   This is **descriptive evidence, not a gate** — no threshold, no verdict change.
   **Expect:** Y ≥ 4 cases recorded, each with a boolean hit.
   **Failure signal:** fewer than 4 label-mapped shots found or lint subagents unparseable
   after one retry.
   **Counter-move:** <4 mappable cases → skip the spot-check entirely, write
   `"flag_spot_check": {"skipped": "fewer than 4 label-mapped shots"}`, and continue —
   Move 6 proceeds regardless.

6. **Do:** Write the verdict + surgical doc updates, then ship:
   - **`tools/judge-calibration/CALIBRATION.md`** — the human verdict document: pinned judge
     identity (model string + prompt sha256 + date), sample design (60, stratified, seed 42,
     truth = round-02), the metrics table, the verdict band, the flag spot-check result, the
     **drift warning** (round-03: David tightened love 47→1 between sessions — absolute tiers
     drift; kappa + adjacent + labels are the durable signals, exact-tier agreement has a
     ceiling), the re-check procedure on judge upgrades, and the residual gap (census/triage
     text judges uncalibrated — no human-labeled text set exists yet).
   - **`docs/eval-architecture.md`** — append ONE status line at the end of the Gap B section
     (before the `---`): `**Status (<UTC date>):** first calibration run complete — see
     tools/judge-calibration/CALIBRATION.md (verdict: <band>, kappa <value>). Judge pinned:
     <model string> + prompt sha256.` Touch nothing else in the file.
   - **`tools/design-lint/README.md`** — append ONE line to the "Proven on" section:
     `Judge calibration: see tools/judge-calibration/CALIBRATION.md (<band>, <UTC date>).` On
     **Fork F1 Route B** the line instead reads: `⚠️ Judge NOT calibrated-trusted — treat lint
     verdicts as advisory; see tools/judge-calibration/CALIBRATION.md.`
   - Commit and push (dark-factory only). Stage exactly: `tools/judge-calibration/` (all files
     incl. `out/` — outputs are small JSON/md, and `.gitignore` line ~51 ignores only
     `tools/design-lint/out/`, verified 2026-07-06), `docs/eval-architecture.md`,
     `tools/design-lint/README.md`. Message:
     `feat(tools): judge-calibration — Gap B closed, design judge scored vs mocha-census labels (kappa <value>, <band>)`.
     Leave any stranger's dirt unstaged.
   **Expect:** push succeeds; `git -C $DF status --porcelain` no longer lists your files;
   `git -C $DF status --porcelain -- tools/mocha-census/` is empty (ratings untouched).
   **Failure signal:** push rejected, or census paths dirty.
   **Counter-move:** push rejected → `git pull --rebase` then push; conflict in a file you did
   NOT touch → **Abort A4**. Census paths dirty → you modified David's data: `git -C $DF
   checkout -- tools/mocha-census/` and re-verify your outputs only wrote under
   `tools/judge-calibration/out/`.

## Forks

**F1 — what the agreement number says.**
Trigger: Move 4's verdict band.
→ **Route A** (kappa ≥ 0.4: `calibrated-trusted` or `calibrated-caution`): CALIBRATION.md states
the judge is usable at that band; design-lint README gets the plain pointer line; done.
→ **Route B** (kappa < 0.4: `not-trusted`): the finding IS the deliverable — CALIBRATION.md
says plainly that census/triage/lint scores from this judge class are advisory until the judge
or prompt improves; design-lint README gets the ⚠️ warning line; ADDITIONALLY write
`engine/store/needs-decision/wg-t3-17-judge-calibration.json` with
`{"ticket": "wg-t3-17-judge-calibration", "question": "Design judge scored not-trusted (kappa <value>) against David's round-02 labels. Options: (a) accept judge-as-advisory and move on, (b) authorise ONE prompt-iteration round with a fresh held-out sample (never re-scored on the same 60 — Goodhart), (c) authorise a pinned API judge (metered billing decision).", "report": "tools/judge-calibration/out/calibration-<date>.json"}`.
This park is **informational** — finish Move 6 and mark the ticket done; the calibration ran
and reported honestly.

**F2 — which ratings round is truth.**
Trigger: Recon 2's `ls` of `out/ratings/`.
→ **Route A** (default; state at authoring): `round-02.json` is the newest full per-item round —
use it. round-01 (good/meh/shit vocab) and round-03 (summary-only re-rate note) are not truth
sets.
→ **Route B**: a newer full per-item round in the love/good/average vocabulary exists (≥100
entries) → use THAT file as truth instead: point calibrate.py's truth-path at it, record it in
`truth_source`, and say so in CALIBRATION.md. Nothing else changes.

## Assumptions ledger

1. **The verdict bands (weighted kappa 0.4 / 0.6) are this ticket's to pin.** No doc sets an
   agreement bar; 0.4/0.6 are the conventional moderate/substantial cut-points and *some*
   checkable bar is the whole point of Gap B. **If false** (David wants different bands): edit
   the bands in calibrate.py + CALIBRATION.md and re-run `--score` only — the verdicts data
   doesn't change.
2. **An in-session subagent judge satisfies "pin judge model+version".** Forced by the locked
   no-API/no-headless rule — the pin is the recorded session-model string + JUDGE-PROMPT.md
   sha256, not an API snapshot id. Plausible: it's the strongest pin available without metered
   billing, and re-runs are comparable via the recorded meta. **If false** (David wants a true
   API-pinned judge): that's a billing decision → the F1 Route B park question already offers
   it as option (c); if David raises it outside Route B, park to needs-decision with the same
   option set.
3. **round-02 is the truth set.** It is the newest full per-item round, the only one with
   free-text labels (74), and the only one in the love/good/average vocabulary. round-03's note
   even warns its own re-rate was "mostly unlabeled". **If false** → Fork F2 Route B handles a
   newer round; if David wants round-01's vocabulary instead, that's a resample + tier-remap,
   trivially re-runnable.
4. **60 stratified items (20/tier, seed 42) is enough for an S ticket.** Kappa CI at n=60 is
   roughly ±0.15 — enough to place the verdict band, not enough to split hairs. **If false**
   (David wants the full 156): `--sample --per-tier 60` + a longer judge pass re-runs Moves 2–4
   unchanged; note it as the obvious follow-on in CALIBRATION.md.
5. **The design labels calibrate the DESIGN judge only.** The Gap B text says census/triage/lint
   "all run LLM-judges", but L1 census (`.claude/workflows/level-1-census.workflow.js` →
   `research/census.jsonl`, quality_tier 1–5 over TEXT artifacts) and L2a triage have no
   human-labeled set — David's design ratings cannot score a text judge. **If false** (David
   believes the numbers transfer): CALIBRATION.md's residual-gap paragraph makes the limit
   explicit so triage can object cheaply; building a text-judge calibration set is its own
   future ticket.

## Abort conditions

- **A1 — the calibration set or its specs moved.** Recon 2 finds round-02 missing/reshaped/
  re-vocabularied, or Recon 5 finds RUBRIC.md / david-design-patterns.md gone. The whole ticket
  rests on that data; never substitute a guessed truth set. Park: write
  `engine/store/needs-decision/wg-t3-17-judge-calibration.json` with
  `{"ticket": "wg-t3-17-judge-calibration", "question": "mocha-census round-02 ratings (or the design spec/rubric) no longer match the war-gamed calibration contract — where is the current human-label set?", "observed": "<what recon found>"}`.
  Leave the ticket in `running/`.
- **A2 — race or seam conflict.** `tools/judge-calibration/` already exists (Recon 1),
  eval-architecture already marks Gap B closed (Recon 6), or Recon 8 shows uncommitted edits on
  the target files. Park with question: "wg-t3-17's target exists / is mid-edit (found: <what
  and where>). Verify-and-close against the existing run, or redo per the war game?" Never
  overwrite a half-landed calibration.
- **A3 — the calibration can't be made sound.** Python broken (Recon 7), <30 usable sampled
  PNGs (Recon 4 / Move 2), self-test red after three fix rounds (Move 1), >20% of judge
  verdicts unparseable after retries (Move 3), or a Move 4 scoring fix breaks self-test
  irrecoverably. Park with the failing output attached. A calibration whose own math or data is
  unverified is worse than no calibration — never ship it red.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory

# 1. The tool exists, stdlib-only, self-test green
test -d $DF/tools/judge-calibration && echo exists-ok
grep -E "^(import|from) " $DF/tools/judge-calibration/calibrate.py   # only: json/sys/os/argparse/pathlib/random/hashlib/datetime
python3 $DF/tools/judge-calibration/calibrate.py --self-test; echo "exit=$?"   # 4 'ok' lines + 'self-test: 4/4 cases ok'; exit=0

# 2. Sample is deterministic, blind, and covered
python3 $DF/tools/judge-calibration/calibrate.py --sample            # 'sampled 60 (20/20/20 ...), seed=42' (or recorded smaller counts)
grep -c '"rating"' $DF/tools/judge-calibration/out/sample.json       # → 0  (no leakage to the judge)
python3 -c "import json; s=json.load(open('$DF/tools/judge-calibration/out/sample.json')); import os; print(sum(1 for x in s if not os.path.exists(x['img'])), 'missing pngs')"   # → 0 missing

# 3. Verdicts: pinned judge meta + in-vocabulary tiers, >=80% coverage
python3 -c "
import json; v=json.load(open('$DF/tools/judge-calibration/out/verdicts.json'))
m=v['judge_meta']; assert m['judge_model'] and m['prompt_sha256'] and 'no API' in m['mechanism'], m
ts={x['tier'] for x in v['verdicts']}; assert ts <= {'love','good','average'}, ts
print(len(v['verdicts']), 'verdicts, meta ok')"                      # → >=48 verdicts, meta ok

# 4. Calibration report: metrics sane, verdict band present
ls $DF/tools/judge-calibration/out/calibration-*.json
python3 -c "
import json,glob; c=json.load(open(sorted(glob.glob('$DF/tools/judge-calibration/out/calibration-*.json'))[-1]))
assert -1 <= c['kappa'] <= 1 and c['verdict'] in ('calibrated-trusted','calibrated-caution','not-trusted')
assert sum(sum(r) for r in c['confusion_matrix']) == c['n']
assert 'flag_spot_check' in c and c['truth_source']
print('report ok:', c['verdict'], 'kappa', c['kappa'], 'n', c['n'])"

# 5. Verdict + doc updates landed, surgically
test -f $DF/tools/judge-calibration/CALIBRATION.md && echo verdict-doc-ok
grep -c "judge-calibration/CALIBRATION.md" $DF/docs/eval-architecture.md      # → 1 (the one status line)
grep -c "judge-calibration/CALIBRATION.md" $DF/tools/design-lint/README.md    # → 1 (pointer or ⚠️ warning per Fork F1)

# 6. Negative checks — what must NOT have changed
git -C $DF status --porcelain -- tools/mocha-census/ | wc -l         # → 0 (David's ratings/shots untouched)
git -C $DF diff HEAD~1 --stat -- docs/eval-architecture.md | tail -1 # ~1 insertion, 0 deletions
ls $DF/tools/judge-calibration/*.png 2>&1                            # No such file (no re-shooting; PNGs stay in mocha-census)
grep -rc "api.anthropic\|ANTHROPIC_API_KEY" $DF/tools/judge-calibration/calibrate.py   # → 0 (no API judge)

# 7. Committed and pushed
git -C $DF log --oneline -1                                          # the feat(tools) judge-calibration commit
git -C $DF status --porcelain | grep -c "judge-calibration\|eval-architecture\|design-lint/README"   # → 0
```

## Executor notes (sonnet)

- **Scope fence.** READ-ONLY on everything under `tools/mocha-census/` — David's ratings and
  screenshots are the ground truth, never regenerate, edit, or re-shoot them. Do NOT edit
  `tools/design-lint/RUBRIC.md` or `docs/david-design-patterns.md` (the spec owns the rules;
  you cite them). Do NOT build census/triage text-judge calibration (no human-labeled set
  exists — Assumption 5). Do NOT touch `engine/*.py`, `canonical/`, `research/`, or
  `.claude/workflows/`. No Anthropic API calls, no `claude -p`, no SDK — subagents in THIS
  session are the judge.
- **The rabbit hole: iterating the judge prompt to chase a better kappa.** If Move 4's number
  disappoints, the overwhelming temptation is to tweak JUDGE-PROMPT.md and re-judge the same 60
  shots until the number looks good. That is Goodhart on the calibration set itself and
  invalidates the result — the round-04 design-lint history is the standing warning. ONE
  prompt, ONE blind pass, report the number honestly; prompt iteration needs a fresh held-out
  sample and David's go (F1 Route B option b). Skip the rabbit hole.
- **Blindness discipline.** Between Move 2 and Move 4 you must not read `answers.json` or
  `round-02.json`, and no subagent prompt may contain a human tier. If you realise a leak
  happened, the pass is void — resample with a different seed (record it) and re-judge.
- **Style:** match the repo's Python-tool idiom (mocha-census, project-digest): stdlib only,
  small pure functions, honest degradation ("fewer than 4 spot-check cases → skip and say so"),
  machine-greppable output. The calibration JSON is the interface — later census/triage
  calibration tickets will reuse `--score` unchanged.
- **Prefer parking over guessing** on any A1/A2 signal — a calibration run against the wrong
  truth set poisons every downstream trust decision the factory makes about its judges.
