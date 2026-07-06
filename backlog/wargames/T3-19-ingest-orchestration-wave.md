# T3-19 — Second ingestion wave: orchestration cluster (Session 1: harvest + draft ×3)

| field | value |
|---|---|
| ticket | wg-t3-19-ingest-orchestration-wave |
| track / size / priority | T3 Ingestion / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t3-01-first-ingestion-review-dimensional, wg-t3-02-ratify-first-ingestion (the REAL gate is their disk artifacts — Recon 1) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Run the factory's SECOND ingestion wave using the pipeline T3-01/T3-02 proved on
`review-dimensional`. The orchestration cluster is already distilled (9 unified-skill drafts in
`research/distillations/orchestration-*.md`, verified on disk 2026-07-06); its own index ranks
three as the gap-closers: **swarm-topology**, **autonomous-pipeline-runner**, and
**governance-and-observability** — those three are this wave, locked at authoring. This ticket
is **Session 1 only** for all three: harvest verbatim origins into each artifact's `_source/`,
write spec-valid `provenance.json`, draft each `SKILL.md` in David's voice, end every artifact
at `rewrite_status: "in-style"` — NEVER "ratified" (ratification is a Session-2 HITL follow-on;
no wave-2 ratify ticket exists yet, so the report must hand David a ready-to-run Session-2
checklist per artifact). Done = 3 (or, via Fork F3, 2) canonical skill folders with verbatim
origins + valid draft provenance + in-style SKILL.md, in-progress rows in `canonical/INDEX.md`,
a handoff report at `backlog/wargames/proof/T3-19/REPORT.md`, and a commit. The pipeline is now
proven, so unlike T3-01 this is not a workflow test — but spec gaps and doc drift are still
findings for the report, never silent workarounds.

## Locked context

- decisions.md Q2: ingestion is a **full campaign** — this is its first at-scale wave after the
  proof.
- decisions.md Q9 (session split, set by the first ingestion and reused here): Session 1 =
  harvest+draft ending at in-style / Session 2 = voice-review+ratify with an HITL pause. This
  ticket never ratifies anything.
- decisions.md Q9: **complement, don't replace** — these canonicals complement David's live
  skills (`ralphy`, `delivery-review`, `remote-machines`…); nothing in his plugins repo is
  edited, and the drafts must not claim to supersede any live skill.
- CLAUDE.md hard rules: no canonical artifact without `provenance.json` + ≥1 verbatim `_source/`
  copy; skills are **stack-agnostic** (Ruflo daemon/MCP/npx syntax in a canonical body is a
  defect); never write into `~/dev/ad/appydave-plugins/`; `research/` is frozen, read-only.
- Wave picks locked at authoring from the cluster index's own "Top 3 unified skills that close
  real gaps" (`research/distillations/INDEX.md`, Orchestration Cluster section): swarm-topology
  (vocabulary gap) · autonomous-pipeline-runner (mechanism gap) · governance-and-observability
  (significant gap). Sub-clusters marked PATTERN (parallel-review-fan-out, multi-machine-
  coordinator, data-pipeline-orchestrator) duplicate live David skills and are NOT in this wave;
  ones flagged "need David's judgment" (swarm-memory-coordinator, workflow-design-advisor,
  agent-lifecycle-coordinator) are NOT in this wave.
- Governing specs (verified present 2026-07-06): `docs/canonical-form-spec.md`,
  `docs/provenance-spec.md`, `docs/ingestion-workflow.md`, `docs/david-style-patterns.md`.

## Recon (verify before any work)

Docs lag code — trust only these checks. Paths repo-relative to `~/dev/ad/apps/dark-factory`
unless absolute.

1. **The pipeline really was proven.** `ls canonical/skills/review-dimensional/` →
   `SKILL.md` + `provenance.json` + `_source/` exist (T3-01's output; at authoring `canonical/`
   held only INDEX.md), and
   `python3 -c "import json;print(json.load(open('canonical/skills/review-dimensional/provenance.json'))['rewrite_status'])"`
   → ideally `ratified` (T3-02 done — best voice anchor available). `in-style` → T3-02 hasn't
   ratified yet; proceed anyway (Session 1 doesn't need the ratified stamp) but record that the
   wave ran against an unratified exemplar. **Folder missing entirely** → Abort A1 (the
   "proven pipeline" this ticket is built on never landed).
2. **Wave targets don't already exist.**
   `ls canonical/skills/swarm-topology canonical/skills/autonomous-pipeline-runner canonical/skills/governance-and-observability 2>&1`
   → three "No such file". **Any exists** → Fork F1 for that artifact before touching it.
3. **Distillations present (mission input; research/ is frozen so absence means trouble).**
   `ls research/distillations/orchestration-swarm-topology.md research/distillations/orchestration-autonomous-pipeline-runner.md research/distillations/orchestration-governance-and-observability.md`
   → all three (verified 2026-07-06; winner_mechanism frontmatter =
   `ruflo:skill:agent-hierarchical-coordinator` / `superpowers:skill:subagent-driven-development`
   / `ruflo:command:observe` respectively). **Any missing** → Abort A1. Known discrepancy to
   carry into the report: `research/distillations/INDEX.md` frontmatter says
   `sub_cluster_count: 8 / distillation_files: 8` but 9 `orchestration-*.md` files exist and the
   index table has 9 rows — do NOT edit the frozen file; report only.
4. **Origin files on disk** (all verified 2026-07-06 with repo SHAs; record the ACTUAL SHAs you
   observe — they go into `source_commit`):
   ```bash
   R=/Users/davidcruwys/dev/upstream/repos
   # swarm-topology origins (all ruflo; 331 / 712 / 400 lines at authoring)
   ls -l $R/ruflo/.agents/skills/agent-hierarchical-coordinator/SKILL.md
   ls -l $R/ruflo/.agents/skills/hive-mind-advanced/SKILL.md
   ls -l $R/ruflo/.agents/skills/agent-adaptive-coordinator/SKILL.md
   # autonomous-pipeline-runner origins (279+3 companions / 41 (+449 companion) / 273 lines)
   ls $R/superpowers/skills/subagent-driven-development/          # SKILL.md + implementer-prompt.md + spec-reviewer-prompt.md + code-quality-reviewer-prompt.md
   ls -l $R/GSD/commands/gsd/execute-phase.md $R/GSD/get-shit-done/workflows/execute-phase.md
   ls -l $R/everything-claude-code/skills/autonomous-agent-harness/SKILL.md
   # governance-and-observability origins (39 / 30+102 / 133 lines)
   ls -l $R/ruflo/plugins/ruflo-observability/commands/observe.md
   ls $R/ruflo/plugins/ruflo-observability/skills/                # observe-trace + observe-metrics companions
   ls -l $R/ruflo/plugins/ruflo-core/commands/witness.md $R/ruflo/plugins/ruflo-core/skills/witness/SKILL.md
   ls /Users/davidcruwys/dev/ad/appydave-plugins/_archived/appydave-skills/truth-trail/   # SKILL.md + references/
   for repo in ruflo superpowers GSD everything-claude-code; do echo -n "$repo "; git -C $R/$repo rev-parse --short HEAD; done
   git -C /Users/davidcruwys/dev/ad/appydave-plugins rev-parse --short HEAD
   # at authoring: ruflo 455f0b17b · superpowers f2cbfbe · GSD 7f5ae23 · everything-claude-code 4423f10c · appydave-plugins ce62fc2
   ```
   **Any file missing** → Fork F2 for that origin. Note: truth-trail lives under `_archived/` —
   the distillation's claim that it is "already in David's stack" is STALE (verified archived
   2026-07-06); that drift is a mandatory report finding and strengthens the case for this
   canonical (the knowledge-integrity layer is no longer live anywhere).
5. **Validators: use them if they landed.** `ls tools/verify-provenance.py tools/style-check.py 2>&1`
   → at authoring both missing (T3-03/T3-04 build them; both staged high-priority, likely landed
   before this NEXT-bucket ticket runs). **Present** → run them in M7; their verdict supersedes
   the manual checklist (a tool crash = fall back to manual + report finding). **Absent** →
   manual checklist in M7.
6. **Voice anchors.** `ls canonical/skills/review-dimensional/SKILL.md` (the factory's own
   exemplar — primary anchor) and
   `grep -c 'evidence: review-dimensional' docs/david-style-patterns.md` → ≥1 if T3-02's
   evidence pass ran (0 = seed version; still usable). Also confirm 2–3 live skills for tone:
   `head -5 ~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md` (read-only).
7. **No name collisions** (the T6 invisibility class):
   `ls ~/dev/ad/appydave-plugins/appydave/skills/ | grep -iE '^(swarm-topology|autonomous-pipeline-runner|governance-and-observability)$'`
   → empty (verified 2026-07-06: no active skill carries any of the three names). **Hit** →
   that name would shadow/be shadowed by a live skill → park that artifact's name question via
   the F3 deferral mechanics (needs-decision note inside the report + skip the artifact) and
   continue the wave with the rest.
8. **canonical/INDEX.md current counts** — `grep -A3 '## Count' canonical/INDEX.md` → record the
   numbers you see (T3-01/T3-02 will have changed them from the authored-time zeros). Your M8
   edit INCREMENTS what's there; never reset to absolutes computed from this document.
9. **No evaluations exist for these artifacts** (verified 2026-07-06: `research/evaluations/`
   holds 88 files, none matching orchestration/swarm/superpowers/subagent/observe/witness).
   `research_sources.evaluations` will be empty for all three — expected, record once in the
   report, don't hunt for files that aren't there.

## Moves

Artifacts are processed as a loop: A = swarm-topology, B = autonomous-pipeline-runner,
C = governance-and-observability. M2–M7 run per-artifact in that order (A fully, then B, then
C) so a Fork F3 deferral of C never blocks A/B.

### M1 — Read the wave context (no writes)

- **Do:** Read in order: (1) `research/distillations/INDEX.md` Orchestration Cluster section
  (sub-cluster table, Top-3, open questions); (2) the three distillation files from Recon 3 in
  full — each carries winner mechanism, folded ideas, a Provenance kept/set-aside table, and
  draft frontmatter that seeds your SKILL.md; (3) `docs/canonical-form-spec.md` +
  `docs/provenance-spec.md` + `docs/ingestion-workflow.md` + `docs/david-style-patterns.md`;
  (4) `backlog/wargames/proof/T3-01/REPORT.md` and `backlog/wargames/proof/T3-02/REPORT.md` if
  they exist — the proof run's findings (spec bugs, e.g. the provenance-spec `source_repo`
  example-vs-field-rule contradiction) are precedents you follow, not rediscover.
- **Expect:** you can state per artifact, without re-reading: the winner mechanism, the 2 folds
  you will carry (A: hive-mind-advanced's queen/byzantine layer + adaptive-coordinator's runtime
  topology switching; B: gsd execute-phase's dependency-ordered parallel waves +
  autonomous-agent-harness's cross-run instincts accumulator; C: witness's
  evidence-before-"fixed" gate + truth-trail's knowledge-integrity rules), and what stays
  set-aside (ruflo daemon/crypto machinery, GSD file formats, ECC infrastructure, ce:lfg,
  gsd:plan-phase, ralphy internals).
- **Failure signal:** a distillation contradicts this war game's origin list (e.g. names a
  different winner than Recon 3 recorded).
- **Counter-move:** the distillation file is the authority on WHAT wins; this war game is the
  authority on WHICH sub-clusters ship. Winner mismatch inside a listed sub-cluster → follow
  the distillation file, adjust that artifact's origin set accordingly, record the drift in the
  report. Sub-cluster mismatch (the file says this sub-cluster shouldn't exist) → Abort A3.

### M2 — Create folders and harvest verbatim (per artifact)

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory
  R=/Users/davidcruwys/dev/upstream/repos
  P=/Users/davidcruwys/dev/ad/appydave-plugins
  # A — swarm-topology (3 origins, all ruflo)
  mkdir -p canonical/skills/swarm-topology/_source
  cp $R/ruflo/.agents/skills/agent-hierarchical-coordinator/SKILL.md canonical/skills/swarm-topology/_source/ruflo--agent-hierarchical-coordinator.md
  cp $R/ruflo/.agents/skills/hive-mind-advanced/SKILL.md             canonical/skills/swarm-topology/_source/ruflo--hive-mind-advanced.md
  cp $R/ruflo/.agents/skills/agent-adaptive-coordinator/SKILL.md     canonical/skills/swarm-topology/_source/ruflo--agent-adaptive-coordinator.md
  # B — autonomous-pipeline-runner (3 origins)
  mkdir -p canonical/skills/autonomous-pipeline-runner/_source
  cp $R/superpowers/skills/subagent-driven-development/SKILL.md      canonical/skills/autonomous-pipeline-runner/_source/superpowers--subagent-driven-development.md
  cp $R/superpowers/skills/subagent-driven-development/implementer-prompt.md          canonical/skills/autonomous-pipeline-runner/_source/superpowers--subagent-driven-development--implementer-prompt.md
  cp $R/superpowers/skills/subagent-driven-development/spec-reviewer-prompt.md        canonical/skills/autonomous-pipeline-runner/_source/superpowers--subagent-driven-development--spec-reviewer-prompt.md
  cp $R/superpowers/skills/subagent-driven-development/code-quality-reviewer-prompt.md canonical/skills/autonomous-pipeline-runner/_source/superpowers--subagent-driven-development--code-quality-reviewer-prompt.md
  cp $R/GSD/commands/gsd/execute-phase.md                            canonical/skills/autonomous-pipeline-runner/_source/gsd--execute-phase.md
  cp $R/GSD/get-shit-done/workflows/execute-phase.md                 canonical/skills/autonomous-pipeline-runner/_source/gsd--execute-phase-workflow.md
  cp $R/everything-claude-code/skills/autonomous-agent-harness/SKILL.md canonical/skills/autonomous-pipeline-runner/_source/everything-claude-code--autonomous-agent-harness.md
  # C — governance-and-observability (3 origins)
  mkdir -p canonical/skills/governance-and-observability/_source
  cp $R/ruflo/plugins/ruflo-observability/commands/observe.md        canonical/skills/governance-and-observability/_source/ruflo--observe.md
  cp $R/ruflo/plugins/ruflo-observability/skills/observe-trace/SKILL.md   canonical/skills/governance-and-observability/_source/ruflo--observe--observe-trace.md
  cp $R/ruflo/plugins/ruflo-observability/skills/observe-metrics/SKILL.md canonical/skills/governance-and-observability/_source/ruflo--observe--observe-metrics.md
  cp $R/ruflo/plugins/ruflo-core/commands/witness.md                 canonical/skills/governance-and-observability/_source/ruflo--witness.md
  cp $R/ruflo/plugins/ruflo-core/skills/witness/SKILL.md             canonical/skills/governance-and-observability/_source/ruflo--witness--skill.md
  cp $P/_archived/appydave-skills/truth-trail/SKILL.md               canonical/skills/governance-and-observability/_source/appydave-plugins--truth-trail.md
  cp -R $P/_archived/appydave-skills/truth-trail/references          canonical/skills/governance-and-observability/_source/appydave-plugins--truth-trail--references
  ```
  Verbatim means verbatim: `cp` only, no edits, no whitespace tidying. Companion files (the
  `--`-suffixed extras) belong to their parent origin, not separate origins. Do NOT create
  `references/` dirs in the canonical folders unless M5 needs overflow.
- **Expect:** every copy byte-identical — for each pair run `diff <src> <dest>`; for the
  truth-trail references dir `diff -r`; all empty, then
  `ls canonical/skills/*/_source/ | grep -c '\--'` style spot-count matches the 17 entries above
  (7 A+B files… concretely: A=3, B=7, C=7 entries).
- **Failure signal:** any non-empty diff, or a cp failing on a path that Recon 4 had confirmed.
- **Counter-move:** re-copy with `cp`. Path newly gone between Recon 4 and now → Fork F2 for
  that origin.

### M3 — Write provenance.json (draft, per artifact)

- **Do:** Per `docs/provenance-spec.md`, one file per artifact. Pinned values:
  - Common: `canonical_type: "skill"` · `version: 1` · `version_history: []` ·
    `rewrite_status: "draft"` · `rewrite_author: "Claude (under direction)"` · `rewrite_date`
    today ISO.
  - `canonical_id`/`canonical_name`: `dark-factory:skill:swarm-topology` /
    `dark-factory:skill:autonomous-pipeline-runner` /
    `dark-factory:skill:governance-and-observability` with matching names.
  - `source_repo` values MUST match `research/recon/<repo>.md` filenames (the field rule wins
    over the spec's example — precedent set by T3-01): `ruflo`, `superpowers`, `gsd`,
    `everything-claude-code`, `appydave-plugins`.
  - `origins[]` — exactly 3 per artifact, per the M2 layout. Each: absolute `source_path`,
    `source_commit` = the SHA recorded in Recon 4 for that repo, `harvested_at` today,
    `verbatim_copy` = the `_source/`-relative path, `kept[]` (≥1) / `modified[]` / `set_aside[]`
    seeded from that distillation's Provenance table. Companion files: note them per-origin the
    way T3-01's provenance did (a `verbatim_copy_companions` extension field or `kept[]` prose —
    findable either way).
  - `research_sources`: `distillation` = the artifact's `research/distillations/orchestration-*.md`
    path; `evaluations` = `[]` (Recon 9 — none exist; that emptiness is a report finding once,
    not per-artifact); `cluster_distill_index`:
    `"research/distillations/INDEX.md#orchestration-cluster"`.
  - The truth-trail origin's `source_path` is the ARCHIVED path — record it as-is plus a note in
    that origin's `kept[]`/prose that the skill was live appydave stock later archived (drift
    finding).
- **Expect:** `for d in swarm-topology autonomous-pipeline-runner governance-and-observability; do python3 -m json.tool canonical/skills/$d/provenance.json >/dev/null && echo VALID-$d; done`
  → three VALID lines; every `verbatim_copy` resolves; no empty `kept[]`.
- **Failure signal:** parse error, or an origin whose `kept[]` you cannot honestly fill.
- **Counter-move:** fix and re-validate. An origin with honestly-empty `kept[]` gets dropped per
  the spec (note why in the report) — but each artifact's WINNER must survive; a winner you'd
  have to drop → Abort A3 (A or B) / Fork F3 Route B (C).

### M4 — Absorb the voice anchors (no writes)

- **Do:** Read `canonical/skills/review-dimensional/SKILL.md` (the factory's own ratified-or-
  in-style exemplar — Recon 1), `docs/david-style-patterns.md` (§Voice rules + templates + any
  `evidence: review-dimensional` additions), and 2 live skills for rhythm
  (`review-blind-hunter`, `remote-machines` — read-only in appydave-plugins). Note concretely:
  trigger-only descriptions with quoted trigger phrases, terse numbered behavior steps,
  anti-patterns section, no marketing prose, no workflow summary in the description.
- **Expect:** you can name ≥3 concrete voice features you will reproduce, and you can say how
  the review-dimensional exemplar renders each of: frontmatter shape, section order, verdict/
  output conventions.
- **Failure signal:** review-dimensional's shape and david-style-patterns.md disagree.
- **Counter-move:** the ratified/in-style exemplar wins for VOICE; the spec doc wins for the
  required SECTION SET. Record the divergence in the report.

### M5 — Draft SKILL.md ×3 (per artifact, in David's voice)

- **Do:** Each file gets the 4 frontmatter fields (`name`, trigger-only `description` with ≥3
  quoted trigger phrases and ≤2 sentences, `argument-hint` (or noted N/A), `allowed-tools`) and
  a stack-agnostic body ≤400 lines (sane band 100–250). Per artifact:
  - **A — swarm-topology.** A DESIGN-VOCABULARY skill, not a launcher (conservative reading of
    the distillation's open question — flagged for Session 2). Body: the 7-topology
    quick-reference table (hierarchical / mesh / queen / raft / quorum / gossip / byzantine —
    shape + best-for, seeded from the distillation), when-to-pick decision steps, the two folds
    (queen-as-persistent-coordinator surviving agent churn; adaptive runtime topology
    switching), and an explicit mapping line that fan-out review panels are "hierarchical,
    one-level" so existing patterns become nameable. Anti-patterns ≥2 (e.g. consensus machinery
    for a 3-agent task; picking topology after building). Strip ALL `$agent-*` invocation
    syntax, daemon/MCP references, `npx` commands.
  - **B — autonomous-pipeline-runner.** Body: the winner's three-part mechanism verbatim-in-
    spirit (deliberate context exclusion — each subagent gets ONLY its task text; hard two-stage
    gate — spec review then quality review, separate subagents; anti-rationalization table
    embedded before execution), plus the folds: dependency-ordered parallel waves within a
    phase, cross-run instincts/learnings accumulator, report-per-wave interrupt points. One
    "complements, does not replace" line acknowledging campaign UX layers (Ralphy-shaped
    front-ends) may delegate here — no deeper coupling, never name ralphy's internals.
    Anti-patterns ≥2 (e.g. passing the whole plan file to a task subagent; skipping the spec
    gate on "small" tasks).
  - **C — governance-and-observability.** Body: the three composable layers as the distillation
    frames them — observe (non-blocking runtime telemetry: what agents are doing, correlated
    with outcomes), witness (evidence-before-"fixed": a fix claim requires a recorded manifest
    entry — carry the IDEA, set aside the cryptographic signing machinery, per the
    distillation's own suggested simplification), truth-trail (knowledge-integrity rules: no
    phantom citations, no false memory claims). Plus cost/drift as the observe layer's named
    extensions (model-routing rationale, long-horizon drift checkpoints). Anti-patterns ≥2
    (e.g. accepting "I verified it works" without evidence; governance that blocks the swarm).
    If while drafting you find this can't be made coherent + stack-agnostic from the thin
    sources (the ruflo origins total ~200 lines of infra-flavored text) → Fork F3.
- **Expect:** three files; `wc -l` ≤400 each; every description passes the "knows WHEN to fire,
  not HOW it works" read.
- **Failure signal:** a body needs >400 lines, or reads as a transcription of an origin.
- **Counter-move:** overflow → `canonical/skills/<name>/references/<topic>.md` (the only reason
  to create references/). Transcription smell — especially hive-mind-advanced's 712 lines — cut
  to the mechanism; the distillation's "kept" column is the scope contract.

### M6 — Refine provenance to in-style ×3

- **Do:** Re-open each `provenance.json`; make `kept[]`/`modified[]`/`set_aside[]` reflect the
  SHIPPED body (voice rewrite, stack-agnostic strips, what you deliberately left out — e.g. A:
  SPARC phase mapping, raft/gossip protocol internals; B: ce:lfg one-command UX, gsd:plan-phase
  triple-subagent planning, superpowers state-machine IDs; C: crypto signing, ruflo cost DB,
  claims infrastructure). Set `rewrite_status: "in-style"` on all three (or the two survivors
  under F3).
- **Expect:** all still parse; `grep -h '"rewrite_status"' canonical/skills/*/provenance.json`
  → only `"in-style"` values (review-dimensional's file excepted — don't touch it).
- **Failure signal:** ledger arrays no longer match the real SKILL.md text.
- **Counter-move:** re-derive from a fresh read of your own drafts — a stale ledger defeats the
  repo's value proposition.

### M7 — Validate ×3

- **Do:** Per Recon 5: if the validators exist, run
  `python3 tools/verify-provenance.py canonical/skills/swarm-topology canonical/skills/autonomous-pipeline-runner canonical/skills/governance-and-observability`
  and `python3 tools/style-check.py` over the same dirs, fix FAILs, re-run to green (WARNs are
  report notes). If absent, run the manual gate per artifact from repo root:
  ```bash
  for d in swarm-topology autonomous-pipeline-runner governance-and-observability; do
    a=canonical/skills/$d
    python3 -m json.tool $a/provenance.json >/dev/null && echo CK1-$d
    python3 - "$a" <<'EOF'
  import json,os,sys
  a=sys.argv[1]; p=json.load(open(f'{a}/provenance.json'))
  for o in p['origins']:
      assert os.path.exists(os.path.join(a,o['verbatim_copy'])), o['verbatim_copy']
      assert o['kept'], 'empty kept'
  print('CK2')
  EOF
    head -10 $a/SKILL.md | grep -c 'name:\|description:\|argument-hint:\|allowed-tools:'   # → 4 (CK3)
    wc -l < $a/SKILL.md                                                                    # ≤400 (CK4)
    grep -icE 'npx|ruflo|claude-flow|mcp__|daemon|npm|typescript|python3?|\$agent-' $a/SKILL.md  # → 0 body hits (CK5; justify any frontmatter hit)
  done
  ```
- **Expect:** every check green for every shipped artifact.
- **Failure signal:** a check fails.
- **Counter-move:** fix and re-run — drafts iterate freely. Two specs conflicting with no
  satisfiable reading → record both, satisfy the stricter, flag in report; neither satisfiable
  → Abort A3. CK5 hits that are genuinely part of a quoted "origin says X" example → allowed
  with a per-hit justification in the report (style-check.py's `<!-- stack-ok -->` marker if
  that tool exists).

### M8 — Register in INDEX + write the Session-2 handoff report

- **Do:**
  1. `canonical/INDEX.md` Skills table: add one row per shipped artifact —
     `| <name> | <first clause of its description> | 3 | in-style | <today> |` — appending
     below the review-dimensional row (never restructuring existing rows). Update `## Count`
     by INCREMENT from Recon 8's recorded values: in-progress +3 (or +2), upstream origins
     ingested +9 (or +6 — count ORIGINS, not companion files, matching how T3-01 counted).
     Bump `Last Updated`.
  2. `mkdir -p backlog/wargames/proof/T3-19` → write `backlog/wargames/proof/T3-19/REPORT.md`:
     per artifact — origins harvested (paths + SHAs), draft shape, drafting calls made on the
     distillations' open questions (A: advisor-not-launcher; B: standalone canonical, ralphy
     untouched; C: witness-idea-without-crypto) each explicitly marked "Session-2 confirm";
     wave-level findings (mandatory minimum: (a) truth-trail archived — distillation's
     "already in David's stack" is stale; (b) zero evaluations exist for orchestration
     artifacts — this wave ingested on distillation evidence alone; (c) the INDEX
     8-vs-9-files frontmatter discrepancy; (d) anything else surfaced); and a **Session-2
     checklist per artifact** (voice review → approve/redirect/decline → ratify flip → INDEX
     flip) with the explicit note that NO wave-2 ratify ticket exists — David should clone the
     wg-t3-02 pattern (one ratify session can batch all three).
- **Expect:** INDEX renders coherently (row count grew by the number of shipped artifacts);
  REPORT.md exists with per-artifact sections + findings + Session-2 checklists.
- **Failure signal:** INDEX's current shape differs from expectation (T3-01/02 reshaped it).
- **Counter-move:** append in whatever shape the live file uses; keep existing rows
  byte-identical; note the reshape.

### M9 — Commit + push

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add canonical/ backlog/wargames/proof/T3-19/
  git commit -m "feat(canonical): second ingestion wave — orchestration cluster ×3 drafted in-style (wg-t3-19, Session 1)"
  git push
  ```
- **Expect:** `git log --oneline -1` shows the commit; `git status --short` clean under
  `canonical/` and the proof dir; push succeeds on main.
- **Failure signal:** unexpected staged files, or push rejected.
- **Counter-move:** `git restore --staged` anything outside the two path groups, inspect,
  revert accidentals, re-commit. Push failure (offline/diverged) = pull-rebase once, retry;
  still failing = report note, not a blocker.

## Forks

**F1 — A wave target already exists in canonical/.**
Trigger: Recon 2 finds any of the three folders.
→ **Route A** (`rewrite_status` draft/in-style, or provenance absent/partial): salvage — keep
byte-identical `_source/` files (verify with M2's diffs), redo provenance + SKILL.md per this
war game for that artifact, note the salvage.
→ **Route B** (`rewrite_status: "ratified"`): that artifact is DONE or contested — exclude it
from the wave (never touch ratified artifacts), proceed with the remaining artifacts, and
record in the report why the wave shipped short. All three ratified → Abort A2.

**F2 — An origin file moved or vanished upstream.**
Trigger: Recon 4 or M2 can't find a source path.
→ **Route A** (relocatable): `find <repo-root> -name '<filename>'` or
`git -C <repo> log --diff-filter=R --name-status -- '<old-path>'`. Found → use the new path,
record old→new in provenance and the report, continue.
→ **Route B** (gone): FOLD origin → keep the origin entry with
`verbatim_copy: "[origin removed before harvest]"`, mine its content from the distillation's
Provenance table, flag in report. WINNER origin → for A or B: Abort A3 (no-verbatim-no-canonical
is a hard rule); for C: → Fork F3 Route B.

**F3 — Governance-and-observability won't cohere.**
Trigger: M5-C can't produce a stack-agnostic, honest body from the thin sources (~200 infra-
flavored ruflo lines + a 133-line archived skill), or its winner is unharvestable (F2), or its
name collides (Recon 7).
→ **Route A** (coherent enough): ship it with the drafting calls flagged loudly for Session 2.
→ **Route B** (not coherent / winner gone): ship the wave as TWO artifacts (A + B — the brief's
"2–3 winners" makes 2 in-scope), delete any partial `canonical/skills/governance-and-observability/`
folder (drafts may be deleted; only ratified artifacts are protected), and give the report a
dedicated section: what blocked it, plus the recommendation (re-distill from richer sources vs
PO decision on the witness/observe ambition) so David can spawn a follow-up. Do NOT park the
whole ticket for this — 2 shipped artifacts is a success, not an abort.

## Assumptions ledger

1. **The cluster index's Top-3 = the "2–3 winners" the candidate brief meant.** Plausible: it is
   the cluster's own ranked gap analysis, and the PATTERN/"needs-judgment" sub-clusters are
   explicitly poor ingestion targets. If David disagrees at Session 2, swapping a sub-cluster is
   a new S-ticket, not a rework of this one — say so in the report.
2. **Distillation names become canonical names** (swarm-topology, autonomous-pipeline-runner,
   governance-and-observability). The distillations are `status: draft` and David never formally
   approved sub-clusters — but Q9's rename precedent (code-review → review-dimensional) was
   David's call at review time, so: draft under distillation names, list "rename?" in every
   Session-2 checklist. A rename is one `git mv` + provenance/INDEX edit at ratification.
3. **The distillations' open questions are drafting calls, not blockers.** Conservative
   readings locked in M5 (advisor-not-launcher / standalone-not-ralphy-fold /
   witness-without-crypto), each flagged "Session-2 confirm" in the report. If David's later
   verdicts flip one, that's a Session-2 redirect, not a Session-1 fault.
4. **Empty `research_sources.evaluations` is spec-legal** (Recon 9: no orchestration evals
   exist; T3-03's validator treats missing research_sources as WARN-only). If a validator FAILs
   on it → satisfy it with an explicit `"evaluations": []` plus a report finding; if it demands
   non-empty content → that's a spec/tool conflict → Abort A3.
5. **Session-2 ratification has no ticket yet.** The REPORT.md checklists are the handoff;
   David clones the wg-t3-02 pattern (this is flagged in the report AND in this war game's
   StructuredOutput flags so the portfolio owner sees it).
6. **Harvesting FROM appydave-plugins' `_archived/` is read-only and legal** — the hard rule
   forbids WRITING to the plugins repo, not reading; `appydave-plugins` is a reconned corpus
   repo (`research/recon/appydave-plugins.md`). If David objects to archived material as an
   origin, dropping the truth-trail origin at Session 2 is a provenance edit + body trim.

## Abort conditions

Park action for ALL aborts: write ATOMICALLY (temp file then `mv`)
`engine/store/needs-decision/wg-t3-19-ingest-orchestration-wave.json` containing
`{"ticket":"wg-t3-19-ingest-orchestration-wave","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave the ticket in `running/`, stop. Never guess past an abort.

- **A1 — Pipeline or mission input missing.** `canonical/skills/review-dimensional/` absent
  (the proof this wave builds on never landed), any governing spec doc missing, or any of the
  three distillation files missing from the frozen corpus. Question: "T3-19's foundation is
  missing: <what>. Run/repair T3-01/T3-02 first, or re-scope the wave?"
- **A2 — All three targets already ratified** (F1 Route B ×3). Question: "The orchestration
  wave already exists ratified — is wg-t3-19 obsolete, or do you want v2 tickets?"
- **A3 — Winner unrecoverable (A/B) or unresolvable spec conflict.** swarm-topology's or
  autonomous-pipeline-runner's winner origin is gone with no relocation (F2), a distillation
  disowns its sub-cluster (M1), or two specs/tools give unsatisfiable conflicting requirements
  (M7, ledger 4). Question: "T3-19 blocked: <the conflict / the missing winner>. Substitute a
  different sub-cluster, amend the spec, or park the wave?"
- **A4 — HALT present** (`engine/store/HALT` exists at any point). Question: "Factory halted
  (<payload>). Resume T3-19 when clear?" (BACKOFF: wait for expiry once; second occurrence →
  this abort.)

## Verification

From `~/dev/ad/apps/dark-factory`. Positive — run for each shipped artifact
(`swarm-topology`, `autonomous-pipeline-runner`, and unless F3 Route B fired,
`governance-and-observability`):

```bash
for d in swarm-topology autonomous-pipeline-runner governance-and-observability; do
  test -f canonical/skills/$d/SKILL.md        && echo PASS-skill-$d
  test -f canonical/skills/$d/provenance.json && echo PASS-prov-$d
  python3 - "$d" <<'EOF'
import json,os,sys
d=sys.argv[1]; a=f'canonical/skills/{d}'
p=json.load(open(f'{a}/provenance.json'))
assert p['rewrite_status']=='in-style', p['rewrite_status']
assert len(p['origins'])==3 and all(o['kept'] and o.get('source_commit') for o in p['origins'])
assert all(os.path.exists(os.path.join(a,o['verbatim_copy'])) for o in p['origins'])
print(f'PASS-provcontent-{d}')
EOF
  [ "$(wc -l < canonical/skills/$d/SKILL.md)" -le 400 ] && echo PASS-len-$d
  grep -q "name: $d" canonical/skills/$d/SKILL.md && echo PASS-name-$d
  grep -q "| $d " canonical/INDEX.md && echo PASS-index-$d
done
# verbatim really verbatim (winner spot-checks)
diff /Users/davidcruwys/dev/upstream/repos/ruflo/.agents/skills/agent-hierarchical-coordinator/SKILL.md canonical/skills/swarm-topology/_source/ruflo--agent-hierarchical-coordinator.md && echo PASS-verbatim-A
diff /Users/davidcruwys/dev/upstream/repos/superpowers/skills/subagent-driven-development/SKILL.md canonical/skills/autonomous-pipeline-runner/_source/superpowers--subagent-driven-development.md && echo PASS-verbatim-B
test -f backlog/wargames/proof/T3-19/REPORT.md && grep -qc 'Session-2' backlog/wargames/proof/T3-19/REPORT.md && echo PASS-report
git log --oneline -5 | grep -q 'wg-t3-19' && echo PASS-commit
# validators, if present, are green over the wave
test -f tools/verify-provenance.py && python3 tools/verify-provenance.py canonical/skills/swarm-topology canonical/skills/autonomous-pipeline-runner && echo PASS-validator
```

(F3 Route B: the governance lines are replaced by
`test ! -d canonical/skills/governance-and-observability && echo PASS-F3-clean` plus a
`grep -q 'governance' backlog/wargames/proof/T3-19/REPORT.md` deferral-section check.)

Negative (must NOT be true, any path):

```bash
grep -l '"rewrite_status": *"ratified"' canonical/skills/*/provenance.json | grep -v review-dimensional && echo FAIL-ratified-in-session1
git -C /Users/davidcruwys/dev/ad/appydave-plugins status --short | grep . && echo FAIL-touched-plugins
git -C /Users/davidcruwys/dev/upstream/repos/ruflo diff --quiet && git -C /Users/davidcruwys/dev/upstream/repos/superpowers diff --quiet && git -C /Users/davidcruwys/dev/upstream/repos/GSD diff --quiet && git -C /Users/davidcruwys/dev/upstream/repos/everything-claude-code diff --quiet || echo FAIL-touched-upstream
git status --short research/ | grep . && echo FAIL-touched-research
git status --short docs/ | grep . && echo FAIL-touched-specs
git status --short -- canonical/skills/review-dimensional/ | grep . && echo FAIL-touched-first-ingestion
```

## Executor notes (sonnet)

- **Scope fence:** write ONLY under `canonical/skills/swarm-topology/`,
  `canonical/skills/autonomous-pipeline-runner/`,
  `canonical/skills/governance-and-observability/`, `backlog/wargames/proof/T3-19/`, the
  rows+counts edit to `canonical/INDEX.md`, and your own `engine/store/` files. NEVER write to
  `~/dev/ad/appydave-plugins/` (including its `_archived/` — you read the truth-trail source,
  nothing more), `~/dev/upstream/` (evidence), `research/` (frozen — even to fix the 8-vs-9
  discrepancy; that's a report finding), `docs/` (spec amendments are findings), or
  `canonical/skills/review-dimensional/` (first ingestion, not yours).
- Session 1 stops at `in-style` for every artifact. Setting `ratified` anywhere is a defect —
  ratification is David's HITL call in a Session-2 ticket that doesn't exist yet (your report
  tells him to spawn it).
- Verbatim copies via `cp` only; catch yourself "tidying" a `_source/` file → stop, re-copy.
- Process artifacts serially A → B → C so a governance deferral (F3) never contaminates the two
  clean ingestions.
- Prefer HITL over guessing: drafting judgment (what goes in the body vs `set_aside[]`) is
  yours; anything touching the TARGET set, ratification, David's live skills, or a locked
  decision is not → park per the abort convention.
- **The rabbit hole:** Ruflo. Its 91 orchestration artifacts, 712-line hive-mind-advanced, and
  daemon/MCP/crypto machinery will tempt you into transcription or into harvesting "just two
  more" coordinator variants (mesh, raft, gossip files exist right next to the winner). You
  harvest NINE origin files total, carry the distillations' kept-columns, and write three small
  in-style skills. The topology TABLE carries the other five topologies as vocabulary — you do
  not need their source files.
