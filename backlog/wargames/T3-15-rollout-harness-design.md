# T3-15 — L2b rollout harness DESIGN

| field | value |
|---|---|
| ticket | wg-t3-15-rollout-harness-design |
| track / size / priority | T3 Ingestion / L / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Produce the DESIGN — not the build — for the L2b rollout harness: the "run the skill on
held-out tasks, score the outputs" stage that `docs/eval-architecture.md` (line 36) marks
**"unbuilt — known gap"** and `docs/dark-factory-living-system-spec.md` (§Level 2b, §6 "Not
Yet Available") marks **"Design TBD"**. It is the biggest named infra gap in the whole eval
ladder: without it, L2b evals can't run, Level 3 distillation's stated dependency ("L2a AND
L2b complete") is unsatisfiable, and Level 4's validation gate ("new canonical must strictly
improve on held-out score") has no score to gate on — skills get ratified on vibes. Done =
`backlog/specs/l2b-rollout-harness-spec.md` exists at `spec-written` state covering the three
named components (held-out task sets per capability station · scoring rubric · execution
environment) plus record schema, baseline protocol, leakage/refresh discipline, cost envelope,
a concrete 5-task pilot appendix, and an ordered build plan that T3-16 executes; the spec is
registered in `backlog/specs/tickets.json` (next free DF-key, expected DF-11); the
eval-architecture gap register's two L2b status lines are updated; a REPORT.md hands David a
ratification checklist. **Zero harness code, zero new data dirs** — building is T3-16, a
separate later decision per the specs-dir doctrine ("write the requirements, store them for
future ticketing, build later").

## Locked context

- decisions.md Q2: ingestion is a **full campaign** — rollout harness explicitly in scope.
- decisions.md Q4: **everything through the engine** — the harness's runner design must target
  sonnet-Swagger engine-ticket dispatch as its default substrate.
- Portfolio-wide: **no `-p`/headless/SDK ever** (metered billing), **interactive `claude`
  only** — the execution-environment design must not assume headless batch runs.
- eval-architecture boundaries (binding): **DF-8 owns pairwise/N-way comparison — don't
  re-spec it**; **stability-1 owns external trace capture — don't re-spec it**; **methodology
  lives in `~/dev/ad/brains/evals/` — reference it, never restate it** ("update the brain for
  'how to eval'; update this doc for 'how Dark Factory evals'").
- Repo hard rule (CLAUDE.md): `research/` is the frozen corpus — no additions that aren't
  recon/discover/distill/eval phase outputs; propose new data homes, don't create them.
- living-system spec §Level 2b pins the record fields the design must carry: `task_set`,
  `rollout_score`, `baseline_comparison`, `run_date`, `model`, `harness`.

## Recon (verify before any work)

Docs lag code — trust only these checks. All paths repo-relative to
`~/dev/ad/apps/dark-factory` unless absolute.

1. `grep -n 'L2b' docs/eval-architecture.md` → line 36 row says `**unbuilt — known gap**` and
   line 78 says `L2b ❌gap-ish` (verified 2026-07-06). **Row says spec-written/built instead**
   → Fork F1 (someone got here first). File missing entirely → Abort A2 (the gap register this
   design slots into is gone; the eval architecture may have been restructured).
2. `ls backlog/specs/ | grep -i 'l2b\|rollout'` → no hits (verified 2026-07-06: dir holds
   c3/df7/df8/self-learning/stability-1/untracked-rot specs + README + tickets.json). **Hit**
   → Fork F1.
3. `grep -n 'Level 2b — Rollout Evaluation' docs/dark-factory-living-system-spec.md` → the
   section exists (~line 110 at authoring) with the 6 record fields and the line
   "**Infrastructure needed**: rollout harness — held-out task sets per capability station,
   scoring rubric, execution environment. **Not yet built.**" **Section gone or L2b removed
   from the ladder** → Abort A2.
4. `ls ~/dev/ad/brains/evals/` → 4 files: `agentic-eval-fundamentals.md`,
   `eval-harness-and-metrics.md`, `long-horizon-failure-modes.md`, `INDEX.md` (verified
   2026-07-06). **Missing** → Fork F3.
5. Boundary specs on disk: `ls backlog/specs/df8-comparison-registry-spec.md
   backlog/specs/stability-1-instrument-loop-spec.md` → both exist (44 and 330 lines at
   authoring). **Either missing** → its boundary still binds (eval-architecture asserts it);
   note the missing file in the report and design around the boundary as documented in
   eval-architecture.md.
6. Pipeline ground truth (numbers go into the spec's "current state" framing — measure, don't
   copy these):
   ```bash
   wc -l research/census.jsonl                 # 10 rows at authoring (L1 barely started)
   ls research/evaluations/ | wc -l            # 88 at authoring (L2a triage)
   ls research/distillations/*.md | wc -l      # 76 at authoring (L3, all provisional)
   ls research/evals.jsonl 2>&1                # No such file at authoring — the living-system
                                               # spec's L2a jsonl home never materialized (a
                                               # finding to carry into the spec)
   ls canonical/ canonical/skills 2>&1         # INDEX.md only at authoring; skills/ absent
   ```
   `canonical/skills/review-dimensional/` existing means T3-01 landed → Fork F2 Route A for
   the pilot section.
7. `python3 -c "import json; print([t['key'] for t in json.load(open('backlog/specs/tickets.json'))['tickets']])"`
   → DF-1..DF-10 at authoring; your registration key is the next free integer (expected
   DF-11). **File missing or reshaped** → Assumption 1's false branch.
8. Engine exists as the dispatch substrate the design targets:
   `ls engine/orchestrator.py engine/store/queue/.CONVENTION.md` → both exist (verified
   2026-07-06). **Missing** → the Q4 doctrine's substrate is gone; Abort A2.
9. Judge-calibration asset exists: `ls tools/mocha-census/out/ratings/*.json` → ≥3 rating
   files (round-01/02/03 etc., verified 2026-07-06) — cite as the proven human-label
   calibration pattern in the rubric section. **Missing** → cite the pattern from
   eval-architecture Gap B prose instead; note in report.
10. `ls backlog/wargames/tickets/ | grep -i 'T3-16\|T3-17'` → whether the build ticket
    (T3-16) and judge-calibration ticket (T3-17) exist yet as staged war-game tickets
    (neither existed at authoring). Existing T3-17 → cross-reference its ticket id in the
    rubric section; existing T3-16 → your build-plan section must not contradict its prompt
    (skim it; contradictions are report findings).

## Moves

### M1 — Read the binding corpus (no writes)

- **Do:** Read, in order: (1) `docs/eval-architecture.md` in full — the two-surface reframe,
  the L2b row, the two boundary "don't re-spec" rulings, Gaps A and B. (2)
  `docs/dark-factory-living-system-spec.md` §3 (all eval levels, especially Level 2b's fields
  and Level 4's validation gate), §4 (three-level optimization; "the factory generates its own
  benchmarks"), §5 (triggers), §6 (substrate table + "Not Yet Available"), §7 (data schemas —
  the jsonl record shapes yours must rhyme with). (3) `~/dev/ad/brains/evals/`:
  `agentic-eval-fundamentals.md` (outcome-vs-process, altitude ladder) then
  `eval-harness-and-metrics.md` (assertion→golden→judge→human ladder, externality principle,
  judge guards, metrics menu, build order). (4) `backlog/specs/df8-comparison-registry-spec.md`
  and skim `backlog/specs/stability-1-instrument-loop-spec.md` §headings — these define what
  your spec must NOT contain. (5) `backlog/specs/README.md` — the spec-registry conventions
  (states, priority integers, tickets.json shape).
- **Expect:** you can state without re-reading: the 6 L2b record fields; the externality
  principle in one line; why DF-8's `baseline_comparison` overlap is a boundary to manage (a
  rollout comparing skill-vs-baseline is a SCORE input, not a registry contest — contests
  between artifacts belong to DF-8); the assertion-first ladder; the validation-gate sentence
  from Level 4.
- **Failure signal:** eval-architecture and the living-system spec disagree on what L2b IS
  (not just its status).
- **Counter-move:** eval-architecture is the later doc (2026-06-24) and self-describes as the
  map — it wins on boundaries; the living-system spec wins on record fields. Record the
  disagreement in the report. If the disagreement is structural (L2b dissolved/merged) →
  Abort A2.

### M2 — Ground the design in real pipeline state (no writes)

- **Do:** Enumerate the capability stations the harness must eventually serve: list cluster
  names from `research/distillations/INDEX.md` frontmatter blocks + section headings (at
  authoring: orchestration, workflow-architecture, delivery-readiness, code-implementation,
  code-review, knowledge-capture, system-comprehension, spec-writing,
  verification-validation, planning, prompt-engineering, security-review, documentation —
  count what's actually there). Note per-station distillation-file counts (the `ls
  research/distillations/ | awk` grouping is fine). Then apply Recon 6's canonical/ result to
  pick the pilot station → Fork F2. Record the chosen pilot and its rationale in a scratch
  note for M7.
- **Expect:** a concrete station list (~13 at authoring) and one pilot station chosen with a
  one-line rationale (default: code-review — it has 6 distillation files, the corpus's
  strongest winner analysis, and is T3-01's ingestion target, so it's where a rollout score
  is first NEEDED for ratification).
- **Failure signal:** `research/distillations/INDEX.md` missing or unparseable.
- **Counter-move:** derive the station list from `ls research/distillations/*.md` filename
  prefixes alone; note the INDEX gap in the report. If distillations/ itself is empty or
  gone, research/ has been tampered with → Abort A2.

### M3 — Create the spec skeleton

- **Do:** Write `backlog/specs/l2b-rollout-harness-spec.md` with this exact section set (fill
  with one-line placeholders now; M4–M8 fill them):
  ```markdown
  # L2b Rollout Harness — held-out task sets · scoring rubric · execution environment

  **State:** spec-written · build-later (build = war-game T3-16)
  **Origin:** 2026-07-06 war-game portfolio T3-15; closes the "unbuilt — known gap" row in docs/eval-architecture.md
  **Methodology:** ~/dev/ad/brains/evals/ (referenced, not restated)

  ## What this is / what done looks like
  ## Boundaries (what this spec does NOT own)
  ## Component 1 — Held-out task sets
  ## Component 2 — Scoring rubric
  ## Component 3 — Execution environment
  ## Record schema (evals/rollouts.jsonl)
  ## Baseline protocol
  ## Leakage & refresh discipline
  ## Cost envelope & governance
  ## Pilot — <station> (appendix: 5 concrete tasks)
  ## Build plan (T3-16 decomposition)
  ## Open questions for David
  ```
  Match sibling-spec register style (df8 is 44 dense lines, stability-1 is 330; target
  **150–300 lines** final). The **Boundaries** section states, with file paths: comparison
  contests → DF-8; trace capture → stability-1; golden-job regression of the LOOP → Gap A
  (not this); judge calibration mechanics → Gap B / T3-17 (this spec CONSUMES a calibrated
  judge, it doesn't build one); eval methodology → the brain.
- **Expect:** file exists, all 12 headings present, State header line exact.
- **Failure signal:** a sibling spec already claims one of these sections' territory in a way
  you didn't expect (found while writing Boundaries).
- **Counter-move:** shrink your section to a pointer at the owning spec (that is the
  eval-architecture doctrine). If the OWNED territory is the harness core itself (task
  sets/rubric/execution env already specced elsewhere) → Abort A3.

### M4 — Design Component 1: held-out task sets

- **Do:** Fill Component 1. Pin these design decisions (defaults chosen at authoring — the
  executor drafts, David ratifies via Open Questions):
  - **Task sourcing protocol**, in priority order: (a) **factory-harvested** — real tasks
    from David's own repos and past factory runs (living-system §4: "the factory generates
    its own benchmarks. Every census workflow run David reviews is a scored rollout"); (b)
    **distillation-derived** — each cluster distillation's winner mechanism implies the tasks
    it must perform well on; (c) **synthetic** — last resort, must be flagged
    `provenance: synthetic` in the task record.
  - **Task record shape** (JSON, one file per task): `task_id`, `station`, `input` (fixture
    path or inline prompt + files), `expected_signals[]` (programmatic assertions a scorer
    can check deterministically), `rubric_dims[]` (the fuzzy dimensions a judge scores),
    `split` (`held-out` | `train`), `provenance` (harvested | distillation-derived |
    synthetic, + source path), `created`, `frozen` (bool — frozen tasks never edited, only
    superseded).
  - **Sizing:** minimum 5 held-out tasks per station before an L2b score is reportable
    (golden-suite sizing per the brain's "~5 representative runs"); train-split tasks
    unlimited.
  - **Proposed home:** `evals/task-sets/<station>/<task_id>.json` — a NEW top-level `evals/`
    dir, NOT `research/` (frozen-corpus rule) and NOT created by this ticket (build = T3-16).
    Document the `research/` alternative (living-system §7 puts eval jsonls there) and route
    the choice to Open Questions.
- **Expect:** section states sourcing order, full task schema, min-N, home proposal, each in
  ≤ a short paragraph or table.
- **Failure signal:** you can't ground sourcing (a) — no scored factory runs exist to harvest
  (true at authoring: census has 10 rows, zero rollouts).
- **Counter-move:** keep the protocol order but state honestly that bootstrap tasks will be
  (b) distillation-derived, and the pilot appendix (M7) must therefore be
  distillation-derived; (a) becomes the steady-state source. This is expected, not a defect.

### M5 — Design Component 2: scoring rubric

- **Do:** Fill Component 2. Pin:
  - **Assertion-first ladder** (per the brain): maximize deterministic `expected_signals`
    checks (file written? finding-N recalled? JSON valid? verdict line present?); LLM-judge
    ONLY for dims assertions can't reach — cap judge dims at **≤4 per station**
    (design-lint's "only 4 reliable flags" precedent, the proven Goodhart dodge).
  - **Judge policy:** judge model+version pinned in every rollout record; a judge is
    trusted for a station only after calibration against human labels — cite the
    mocha-census ratings files (Recon 9) as the in-house precedent and cross-reference the
    Gap-B/T3-17 work (by ticket id if Recon 10 found it, by eval-architecture Gap B
    otherwise). The harness CONSUMES a calibrated judge; calibration mechanics stay out.
  - **Score shape:** per-task `assert_pass_rate` (0–1) + per-judge-dim scores (1–5) →
    per-task composite → task-set mean = the record's `rollout_score`; always accompanied by
    at least one **efficiency** metric (steps or cost per task — the brain: "pure success
    rate hides an agent that wins expensively").
  - **Bias note:** rollout scores are single-artifact-absolute. Any skill-vs-skill reading
    of two rollout scores is a COMPARISON and belongs in DF-8's registry with its
    `task_type`/`bias_caveat` machinery — one cross-reference sentence, no more.
- **Expect:** section carries the ladder, the ≤4-judge-dims cap, pinning + calibration
  consumption, composite formula, efficiency metric, DF-8 sentence.
- **Failure signal:** while writing, the rubric drifts into designing judge prompts or
  calibration procedure.
- **Counter-move:** delete the drift; replace with the pointer (brain § LLM-as-judge +
  Gap B). Calibration is out of scope by locked boundary.

### M6 — Design Component 3: execution environment

- **Do:** Fill Component 3. Pin:
  - **Isolation:** each rollout runs in a throwaway fixture workspace (fresh dir or git
    worktree under a scratch root); the skill-under-test is injected into the fixture's own
    `.claude/skills/` — NEVER into `~/dev/ad/appydave-plugins/` (repo hard rule) and never
    onto the machine's global skill path.
  - **Dispatch:** engine ticket-chain per the Q4 doctrine — one Swagger ticket per rollout
    batch (station × artifact × arm), workers are interactive tmux `claude` sessions under
    the existing CAP=3 governor; **explicitly no `-p`/headless/SDK** (locked). State the
    consequence honestly: rollouts are serialized through the warm pool, so a 5-task
    3-arm pilot ≈ 15 task-runs ≈ several worker-hours — the cost envelope section carries
    the numbers.
  - **Externality (load-bearing):** the rolled-out agent NEVER scores itself. A separate
    scorer step (deterministic script for assertions; separate judge session for rubric
    dims) reads the fixture's end state and writes the score — cite the brain's externality
    principle verbatim-by-reference, one line.
  - **Arms:** defined here, protocol in the Baseline section: `no-skill` (same fixture, no
    injected skill) · `candidate` (skill under test) · `current-canonical` (only when one
    exists). `baseline_comparison` = candidate minus no-skill, and minus current-canonical
    when present — exactly what Level 4's validation gate consumes.
  - **Record home:** `evals/rollouts.jsonl`, one row per (artifact × task_set × arm) run,
    carrying the living-system §Level 2b six fields (`task_set`, `rollout_score`,
    `baseline_comparison`, `run_date`, `model`, `harness`) + `judge_model`, `arm`,
    `task_detail[]`, `cost`. Fill the Record schema section with the full row example while
    you're here.
- **Expect:** Component 3 + Record schema + Baseline protocol sections all filled; the
  schema example is valid JSON when extracted.
- **Failure signal:** the design needs a capability the engine demonstrably lacks (e.g.
  per-ticket workspace isolation semantics you couldn't verify).
- **Counter-move:** don't invent engine features — write the requirement into the Build
  plan as "engine precondition, verify at T3-16 build time" and keep the design
  substrate-honest. If the whole execution model is impossible under interactive-only (it
  isn't — it's just slow), that would be a locked-decision conflict → Abort A3.

### M7 — Write the pilot appendix: 5 concrete tasks

- **Do:** In the Pilot section, spec 5 held-out tasks for the pilot station chosen in M2/F2
  — described in prose+schema, NOT built as fixture repos. For code-review (default): the
  **seeded-defect pattern** — each task is a smallish diff/fixture with N planted defects of
  known type and location; `expected_signals` = planted-defect recall (found/N) +
  false-positive count; `rubric_dims` (judge, ≤4) = e.g. severity-justification quality,
  actionability of findings. Each of the 5 tasks gets: `task_id`, one-line scenario, defect
  classes planted, the assertions, the judge dims. Source them distillation-derived (M4
  counter-move): the code-review distillations name the failure classes that matter — mine
  those files for the defect taxonomy. State which arm set the pilot runs (F2's route
  decides whether `current-canonical`/`candidate` maps to `review-dimensional`).
- **Expect:** 5 task blocks, each self-contained enough that T3-16 can build the fixture
  without re-deriving intent; the appendix names its distillation sources by path.
- **Failure signal:** the code-review distillations don't yield 5 distinct defect-class
  scenarios (too thin).
- **Counter-move:** fill the remainder from `research/evaluations/` code-review rows or
  David's live review skills' stated lenses (read-only), marking those tasks
  `provenance: synthetic` per M4's flag rule. Fewer than 3 groundable tasks total →
  the pilot station is wrong; re-run M2's choice on the next-best station and note why.

### M8 — Build plan + open questions

- **Do:** Fill the last two sections.
  - **Build plan (T3-16 decomposition)** — ordered, each slice one line with its acceptance
    check: (1) `evals/` scaffold + task-record JSON-schema validator; (2) pilot task-set
    authored as real fixtures (the M7 five); (3) runner — fixture setup + skill injection +
    engine-ticket emission per arm; (4) deterministic scorer + `rollouts.jsonl` writer; (5)
    judge-dim scoring wired to the calibrated judge (blocked-by: Gap B/T3-17); (6) pilot
    rollout executed: pilot artifact vs no-skill baseline, first real `rollout_score` +
    `baseline_comparison` recorded; (7) surfacing — rollout state visible via status.py or
    canonical/INDEX.md column (one-line proposal only). Mark slice 5 as the only one with an
    external dependency; slices 1–4+6 must be buildable without it (assertions-only pilot
    score is still a score).
  - **Open questions for David** — minimum four, each with the default the spec assumes:
    (Q-a) storage home `evals/` top-level vs `research/` (default: `evals/`); (Q-b) cost
    ceiling per rollout batch in worker-hours (default: pilot ≤ ~15 task-runs, no
    steady-state commitment yet); (Q-c) does L2b retroactively gate the 76 provisional
    distillations (living-system says L3 requires L2b complete — currently violated
    corpus-wide; default: no retro-gate, policy belongs to the provisional-sweep ticket
    T3-21); (Q-d) pilot station confirm (default: code-review). Plus anything M1–M7 surfaced.
- **Expect:** both sections filled; every build slice has an acceptance check; every open
  question has a default.
- **Failure signal:** the build plan exceeds ~8 slices or starts specifying implementation
  detail (function names, file-level code layout).
- **Counter-move:** collapse to the 7 slices above — T3-16's own war game owns build detail;
  this spec owns WHAT and in what order.

### M9 — Register the spec (DF-key + gap-register update)

- **Do:** Two surgical edits:
  1. `backlog/specs/tickets.json` — append one ticket object (next free DF-key per Recon 7,
     expected `DF-11`): `key`, `title: "L2b rollout harness — held-out task sets, scoring
     rubric, execution environment"`, `project: "ingestion"`, `priority: 2`, `state:
     "spec-written"`, `spec_path: "backlog/specs/l2b-rollout-harness-spec.md"`, `build_via:
     "engine Swagger ticket-chain (war-game T3-16)"`. Preserve every existing entry
     byte-identical.
  2. `docs/eval-architecture.md` — exactly two lines: line-36 row status
     `**unbuilt — known gap**` → `**spec-written — `backlog/specs/l2b-rollout-harness-spec.md` (build = T3-16)**`;
     line-78 `L2b ❌gap-ish` → `L2b 📝spec-written`. Nothing else in the file changes.
- **Expect:** `python3 -m json.tool backlog/specs/tickets.json >/dev/null && echo VALID` →
  VALID; `git diff --stat docs/eval-architecture.md` → 1 file, ±2 lines.
- **Failure signal:** tickets.json edit produced invalid JSON, or the eval-architecture diff
  touched more than 2 lines.
- **Counter-move:** `git checkout -- <file>` and redo the single edit. tickets.json missing
  or reshaped beyond the documented structure → Assumption 1's false branch (skip
  registration, report it).

### M10 — Report + commit

- **Do:** `mkdir -p backlog/wargames/proof/T3-15` and write
  `backlog/wargames/proof/T3-15/REPORT.md`: what was designed (one paragraph); the pilot
  station + F2 route taken; every finding (mandatory minimum: (a) `research/evals.jsonl`
  never materialized despite the living-system spec §7 defining it — Recon 6; (b) the
  living-system spec's Phase-5 `level-2b-rollout-eval.workflow.js` (Workflow Tool substrate)
  is superseded by the Q4 engine doctrine in this design — flag for the T8
  truth-reconciliation pass; (c) L3's "requires L2b complete" dependency is violated by all
  76 existing distillations — routed to Q-c; (d) anything else surfaced); and a **David
  ratification checklist**: read the spec top-to-bottom, answer the four+ open questions,
  confirm the two-line eval-architecture edit, greenlight (or re-scope) T3-16. Then:
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add backlog/specs/l2b-rollout-harness-spec.md backlog/specs/tickets.json docs/eval-architecture.md backlog/wargames/proof/T3-15/
  git commit -m "spec(evals): L2b rollout harness design — task sets + rubric + execution env (wg-t3-15, build=T3-16)"
  ```
- **Expect:** commit lands; `git status --short` shows nothing left in the four staged path
  groups.
- **Failure signal:** unexpected staged/dirty files outside the fence.
- **Counter-move:** `git restore --staged` the strays, inspect, revert accidental changes,
  note deliberate ones in the report, re-commit. Push if main is clean; a failed push is a
  report note, not a blocker.

## Forks

**F1 — Prior L2b design work exists.**
Trigger: Recon 1 shows a changed status row, or Recon 2 finds an existing
`backlog/specs/l2b*`/`*rollout*` spec.
→ **Route A** (a draft/partial spec or notes exist, state not `spec-written`+registered):
absorb — read it, keep what's sound, produce THIS war game's full section set as the
superseding text in the same file (or the pinned filename if it lived elsewhere — then leave
a one-line tombstone pointer at the old path), and credit the prior text in the report.
→ **Route B** (a registered `spec-written` L2b spec, or built harness code, already exists):
→ Abort A1 — this ticket is obsolete or a duplicate; David decides.

**F2 — Pilot grounding depends on whether T3-01 landed.**
Trigger: Recon 6's `canonical/skills/` check.
→ **Route A** (`canonical/skills/review-dimensional/` exists): pilot arms =
`no-skill` vs `candidate: review-dimensional` (its draft/in-style SKILL.md is the
skill-under-test; a ratified one would also serve). The pilot doubles as T3-01's missing
rollout evidence — say so in the spec.
→ **Route B** (canonical/ still INDEX-only): pilot arms = `no-skill` vs `candidate: the
code-review distillation's winner source` (the verbatim upstream artifact named in
`research/distillations/code-review-*.md` frontmatter), and the spec notes that the first
canonical draft slots in as a third arm when it exists. Design otherwise identical.

**F3 — The methodology brain is missing or moved.**
Trigger: Recon 4 fails.
→ **Route A** (moved): `ls ~/dev/ad/brains/ | grep -i eval` or check
`~/dev/ad/brains/INDEX*`/brains index for a rename; found → update every brain reference in
the spec to the new path, note in report.
→ **Route B** (gone): design from `docs/eval-architecture.md`'s inline summaries + this war
game's pinned decisions (they encode the brain's load-bearing rules: externality,
assertion-first, judge pinning+calibration, ≤4 judge dims, efficiency metric); keep the
spec's Methodology header pointing at the brain path with "(missing at authoring — restore)"
and flag prominently in the report. Do NOT restate methodology as if newly invented here.

## Assumptions ledger

1. **The specs-dir registration convention (tickets.json, DF-keys) is still live.** Plausible:
   README + tickets.json verified on disk 2026-07-06, DF-10 added recently. If false
   (file gone/reshaped): skip M9-1, register however the current mechanism works if obvious,
   otherwise report-only — the spec file itself is the deliverable; registration is
   discoverability.
2. **A new top-level `evals/` home is an acceptable proposal.** Plausible: `research/` is
   frozen by hard rule and nothing else owns eval-run data. If David prefers
   `research/rollouts.jsonl` (living-system §7 precedent), it's a spec-text change at
   ratification — already routed to Open Question Q-a; nothing is built either way.
3. **Engine ticket-chain is the right runner substrate (over Workflow Tool).** Plausible:
   decisions.md Q4 "everything through the engine" + the portfolio's interactive-only rule;
   the living-system spec's workflow.js plan predates Q4. If David rules Workflow Tool at
   ratification, only Component 3's dispatch paragraph changes — M4/M5's task-set and rubric
   designs are substrate-agnostic by construction; note this isolation explicitly in the spec.
4. **Two surgical status lines in `docs/eval-architecture.md` are sanctioned.** Plausible:
   the doc self-describes as the gap register ("this doc [tracks] how Dark Factory evals");
   leaving "unbuilt — known gap" after a spec lands would itself be docs-lag-code rot. If a
   standing instruction against docs edits surfaces at execution time: skip M9-2, put the
   two-line diff in the report for David to apply.
5. **Seeded-defect tasks are legitimate held-out signal for the code-review pilot.** Invented
   at authoring from the brain's golden/assertion doctrine (deterministic, replayable,
   objective recall). If David objects at ratification, the 5 task blocks swap out; the
   harness design (schema, arms, scorer, record) survives unchanged — the appendix is
   deliberately the only place they live.

## Abort conditions

Park action for ALL aborts: write
`engine/store/needs-decision/wg-t3-15-rollout-harness-design.json` containing
`{"ticket":"wg-t3-15-rollout-harness-design","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort.

- **A1 — L2b already designed or built.** F1 Route B: a registered spec-written L2b spec or
  actual harness code (e.g. `tools/rollout-harness/`, an `evals/` dir with runner code)
  exists. Question: "L2b rollout harness already has <spec|code> at <path> — is T3-15
  obsolete, or do you want this design to supersede it?"
- **A2 — The eval ladder itself has moved.** Recon 1/3/8 failures: eval-architecture.md gone,
  Level 2b removed/renamed from the living-system spec, distillations vanished, or the engine
  substrate gone. The design would target a structure that no longer exists. Question: "The
  eval ladder / engine substrate looks restructured since 2026-07-06 (<observation>) — does
  the L2b harness design still target the L1→L4 ladder as specced?"
- **A3 — Boundary or locked-decision collision with no conservative resolution.** M3/M6: a
  sibling spec already owns the harness core, or the execution environment cannot be designed
  without violating a locked rule (headless required, DF-8 re-spec unavoidable). Question:
  "T3-15 design collides with <spec/rule>: <the two readings>. Which wins?"

## Verification

All from `~/dev/ad/apps/dark-factory`. Positive:

```bash
test -f backlog/specs/l2b-rollout-harness-spec.md && echo PASS-1
grep -q '^\*\*State:\*\* spec-written' backlog/specs/l2b-rollout-harness-spec.md && echo PASS-2
for h in 'Held-out task sets' 'Scoring rubric' 'Execution environment' 'Record schema' 'Baseline protocol' 'Leakage & refresh' 'Cost envelope' 'Pilot' 'Build plan' 'Open questions'; do grep -q "$h" backlog/specs/l2b-rollout-harness-spec.md || echo "MISSING: $h"; done   # no MISSING lines (PASS-3)
for f in task_set rollout_score baseline_comparison run_date model harness; do grep -q "$f" backlog/specs/l2b-rollout-harness-spec.md || echo "MISSING-FIELD: $f"; done   # no MISSING-FIELD lines (PASS-4)
grep -q 'brains/evals' backlog/specs/l2b-rollout-harness-spec.md && grep -q 'df8-comparison-registry' backlog/specs/l2b-rollout-harness-spec.md && grep -q 'stability-1' backlog/specs/l2b-rollout-harness-spec.md && echo PASS-5   # boundaries reference their owners
grep -c 'task_id' backlog/specs/l2b-rollout-harness-spec.md   # ≥5 → the pilot's five task blocks exist (PASS-6)
python3 -m json.tool backlog/specs/tickets.json >/dev/null && python3 -c "import json; ts=json.load(open('backlog/specs/tickets.json'))['tickets']; t=[x for x in ts if x['spec_path']=='backlog/specs/l2b-rollout-harness-spec.md']; assert len(t)==1 and t[0]['state']=='spec-written'; print('PASS-7')"
grep -q 'spec-written' docs/eval-architecture.md && ! grep -q 'L2b ❌gap-ish' docs/eval-architecture.md && echo PASS-8
test -f backlog/wargames/proof/T3-15/REPORT.md && echo PASS-9
git log --oneline -5 | grep -q 'wg-t3-15' && echo PASS-10
```

Negative (must NOT be true — design only, nothing built):

```bash
test ! -d evals && echo NEG-1                                   # no evals/ dir created
test ! -d tools/rollout-harness && echo NEG-2                   # no harness code
git status --short research/ | grep -q . || echo NEG-3          # frozen corpus untouched
git diff --quiet engine/ && echo NEG-4                          # engine code untouched
git status --short canonical/ | grep -q . || echo NEG-5         # canonical untouched
git diff --quiet docs/dark-factory-living-system-spec.md && echo NEG-6   # living-system spec untouched (its stale lines are report findings, not edits)
git -C ~/dev/ad/appydave-plugins diff --quiet && echo NEG-7     # David's plugins untouched
[ "$(git diff HEAD~1 --numstat -- docs/eval-architecture.md | awk '{print $1+$2}')" -le 6 ] && echo NEG-8   # eval-architecture edit stayed surgical
```

## Executor notes (sonnet)

- **Scope fence:** write ONLY `backlog/specs/l2b-rollout-harness-spec.md`, the one appended
  entry in `backlog/specs/tickets.json`, the two status lines in
  `docs/eval-architecture.md`, and `backlog/wargames/proof/T3-15/`. NEVER touch `research/`
  (frozen), `engine/` (code), `canonical/`, `docs/dark-factory-living-system-spec.md` (its
  stale lines are REPORT findings for the T8 reconciliation pass, not your edits),
  `~/dev/ad/brains/` (reference-only), or `~/dev/ad/appydave-plugins/`.
- **DESIGN ONLY.** Creating `evals/`, writing a fixture, a runner script, a task JSON file
  on disk, or "just a quick prototype" is a defect even if it works — the build is T3-16,
  gated on David ratifying this spec. The 5 pilot tasks live as text INSIDE the spec.
- **Reference, don't restate.** Any paragraph re-deriving eval methodology (why judges need
  pinning, what golden runs are) should be a one-line pointer at
  `~/dev/ad/brains/evals/eval-harness-and-metrics.md`. Same for DF-8's comparison machinery
  and stability-1's traces. The spec's value is the Dark-Factory-specific application, not
  the theory.
- **Prefer HITL over guessing:** design defaults + open questions are yours to draft (that
  IS the job); anything that would change the eval ladder's structure, unlock builds, or
  edit ratified/foreign artifacts is not → park per the abort convention.
- **The rabbit hole:** the corpus around this ticket is enormous (76 distillations, 88
  evals, a 400-line living-system spec, 4 brain files, 6 sibling specs) and every one
  invites "while I'm here" side-designs — a task-authoring workflow, a judge-prompt library,
  a rollout dashboard, retro-gating the distillations. Design exactly three components + one
  pilot + one build plan for T3-16, route everything else to Open Questions or the report,
  and stop at ~300 spec lines.
