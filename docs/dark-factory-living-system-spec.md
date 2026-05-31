# Dark Factory — Living System Spec

**Status**: draft v1 — 2026-05-26
**Author**: David Cruwys (via design session)
**Grounding**: SkillOpt arXiv:2605.23904 (Microsoft Research, 2026-05-22)
**Companion docs**: `architecture.md`, `phase-b-next-steps.md`, `ylo-to-poem-blueprint.md`

---

## 1. Objective

Build and operate a **self-improving capability factory** — a living system that:

1. Continuously harvests agent skills, commands, and workflows from 14+ upstream provider repos
2. Evaluates every artifact at multiple depth levels (triage → deep eval → rollout scoring)
3. Synthesizes the best version of each capability and presents it for ratification
4. Maintains a canonical library in David's voice, with full provenance back to every source it beat
5. Optimizes canonical artifacts over time using workflow results as training signal

**Core principle (SkillOpt)**: The skill document is the external trainable state of a frozen agent. The agent model never changes; only the skill file does. Optimization is text-space: bounded add/delete/replace edits, accepted only when they strictly improve a held-out validation score.

**Meta-principle**: The dark factory builds itself using the very workflow patterns it researches. Running the factory management workflows IS the proof-of-concept for YouTube launch, software dev, and any other workflow domain.

**Target user**: David Cruwys — sole author, PO, and ratifier. All automation serves his attention, not replaces it.

---

## 2. The Three Roles

The system has three coexisting roles. Choosing between them is a mistake — they are three layers of the same thing.

| Role | Location | Job |
|------|----------|-----|
| **The Library** | `canonical/` | Master records: one winner per capability station, in David's voice, with provenance. Projects out to appydave-plugins and other targets. |
| **The Warehouse** | `research/` | All raw material: 1,100+ artifacts from 14 upstream repos, frozen corpus plus continuous refresh. |
| **The Platform** | `.claude/workflows/` | The factory: creates, runs, evaluates, and promotes skills. Uses the Library to do the production work. |

**The Intake (the front door).** The three roles assume the material already exists. Ideas — David's, papers, others' work — land first in **Intake** (`backlog/` + `experiments/` for now), get tested as experiments, and only cross into the Warehouse/Library through the validation gate. Anything can enter Intake; nothing is trusted until validated. See `intake.md`.

### Naming: `canonical/` stays

`canonical/` is the authoritative reference — the version everything else defers to. It is derived from sources but it IS the source of truth for David's toolset. The deployed artifact (projected to appydave-plugins) is a derivative of `canonical/`, not the other way around.

---

## 3. The Five Evaluation Levels

Evaluation is a pipeline, not a one-time event. Each level is a dependency for the next.

### Level 0 — Repo Scorecard
**Scope**: 14 upstream provider repos (one scorecard per repo)
**Question**: Is this repo worth continued investment?
**Fields**:
- `repo_id` — canonical identifier
- `quality_tier` — 1–5 (signal-to-noise across its artifacts)
- `relevance` — how much maps to David's actual use cases
- `freshness` — last commit date, maintenance cadence, deprecation risk
- `overlap` — which other repos cover similar ground
- `unique_contribution` — what only this repo has
- `priority` — high / medium / low / retire
- `assessed_at` — ISO date
- `source_version` — commit hash at assessment time

**Refresh trigger**: repo gets a major update, or on monthly scheduled pulse
**Stored in**: `research/repos.jsonl`
**Current state**: partial — recon reports in `research/recon/` exist but not uniform/machine-readable

---

### Level 1 — Artifact Census
**Scope**: All 1,150 artifacts (one record per artifact)
**Question**: What is this thing, and is it worth deeper attention?
**Fields**:
- `artifact_id` — repo:type:name
- `cluster` — capability station it belongs to
- `quality_tier` — 1–5 quick score
- `verdict` — `adopt` / `evaluate` / `skip` / `defer`
- `verdict_reason` — one line
- `assessed_at` — ISO date
- `source_version` — commit hash or file date at assessment

**Refresh trigger**: new artifact detected in upstream repo (via scheduled pulse)
**Stored in**: `research/census.jsonl` (append-only; new assessments append, superseded by `source_version` diff)
**Current state**: `artifacts.jsonl` has 1,150 records. `level-1-census.workflow.js` is built and running (parallel fan-out, 5 agents per batch, schema-validated). Batch 0 complete on 2026-05-26 (5 records, all `agent-skills-osmani`, verdicts: 3 adopt / 2 evaluate, no skip/defer yet). Gap: 1,112 census records remaining. Live dashboard at `mochaccino/designs/09-census-progress/`.

---

### Level 2a — Qualitative Scorecard (Triage)
**Scope**: Artifacts with `verdict: evaluate` from Level 1
**Question**: How good is this specific artifact, what's worth keeping?
**Fields**:
- `quality_score` — 1–5 with rationale
- `adoption_fit` — strong / partial / weak
- `uniqueness` — rare / common / duplicate
- `composability` — standalone / called-by-others / calls-others
- `description_craft` — trigger / marketing / neutral / missing
- `mineable_phrasing` — verbatim quotes worth keeping
- `gap_analysis` — what does this add that David doesn't have?
- `deprecated` — boolean + reason if true
- `source_version` — commit hash at evaluation time

**Refresh trigger**: source artifact changes materially (detectable via `source_version` diff)
**Stored in**: `research/evals.jsonl` (machine-readable) + `research/evaluations/<id>.md` (human-readable)
**Current state**: 88 of ~1,150 complete. These are triage, not deep eval.

---

### Level 2b — Rollout Evaluation
**Scope**: High-priority artifacts, one per cluster before Level 3 can run
**Question**: Does this skill actually perform well when run on real tasks?
**What it is**: Run the skill on a held-out task set, score the outputs. This is what SkillOpt means by evaluation — not reading the skill, but running it.
**Fields**:
- `task_set` — which held-out task set was used
- `rollout_score` — numeric, benchmark-specific
- `baseline_comparison` — score vs no-skill baseline, vs current canonical
- `run_date` — ISO date
- `model` — which model was used
- `harness` — direct-chat / claude-code / codex

**Infrastructure needed**: rollout harness — held-out task sets per capability station, scoring rubric, execution environment. **Not yet built.**
**Refresh trigger**: new version of skill available, or model changes

---

### Level 3 — Cluster Distillation
**Scope**: One distillation per capability station
**Question**: If we were building the best version of this capability, what would it look like?
**Dependency**: Level 2a AND Level 2b complete for all artifacts in the cluster before this runs.

> **Current state caveat**: 76 distillations exist but were written with incomplete Level 2 coverage. Treat as provisional sketches, not ratified designs. Do not ingest from them until the cluster's Level 2 is complete.

**Fields**:
- `cluster` — capability station name
- `winner_mechanism` — artifact with the strongest design
- `non_overlapping_ideas` — best bits from runners-up that don't conflict
- `proposed_structure` — draft skeleton of the canonical artifact
- `open_questions` — things only David can decide
- `cluster_coverage` — how many Level 2a/2b evals were considered
- `source_versions` — version hashes of all inputs

**Refresh trigger**: new artifact enters the cluster at Level 2, or an existing one is deprecated.
**Stored in**: `research/distillations/<cluster>.md` (existing format, retain)

---

### Level 4 — Ratification
**Scope**: Approved cluster distillations
**Question**: Is this ready to become a canonical artifact?
**Process**:
1. David reviews Level 3 distillation, answers open questions
2. Validation gate applied: new canonical must strictly improve on held-out score vs current canonical (or vs no-skill baseline if no current canonical exists)
3. SKILL.md written in David's voice, bounded edits from the distillation
4. `provenance.json` written
5. Verbatim source copies placed in `canonical/<type>/<name>/_source/`
6. Registered in `canonical/INDEX.md`

**Ratification mode**: HITL for now — David approves every artifact. Auto-promotion when validation gate is proven (Phase 3+).
**Textual learning rate discipline**: when updating an already-ratified artifact, make bounded add/delete/replace edits. Never rewrite from scratch. Version, don't overwrite.

---

## 4. The Three-Level Optimization Hierarchy

Skills live inside agents, agents live inside workflows. The optimization signal flows in both directions.

```
Workflow result  ←── ground truth anchor
      ↓ attribution
Agent performance  ←── which agent contributed well or poorly
      ↓ attribution
Skill quality  ←── SkillOpt bounded edits
```

**Top-down**: workflow result → attribute back to constituent agents → flag skills for re-evaluation
**Bottom-up**: skill optimized on held-out tasks → agent uses improved skill → workflow outcome improves

The dark factory running its own management workflows generates real training signal. Every Level 1 census workflow run that David reviews is a scored rollout for the skills those agents used. The factory doesn't need synthetic benchmarks — it generates its own.

---

## 5. The Three Trigger Types

### Scheduled
- **Nightly upstream pulse**: scan all 14 upstream repos for new or changed artifacts → append new Level 1 census records → flag changed artifacts for Level 2 re-evaluation
- **Weekly freshness check**: diff `source_version` in Level 2 records against current repo state → surface stale evals
- **Monthly repo scorecard refresh**: re-run Level 0 for any repo that has had significant commits

**Implementation**: Claude Code Desktop scheduled tasks or `CronCreate`. No human needed. Output queued as backlog items or appended to JSONL.

### Event-Driven
- **New artifact detected** → Level 1 census record created
- **Artifact changed materially** → Level 2 flagged for re-evaluation
- **Level 2 completes for full cluster** → Level 3 distillation workflow triggered
- **Repo deprecated/abandoned** → Level 0 scorecard updated; bulk `deprecated: true` on all Level 2 evals for that repo

**Implementation**: state changes in JSONL files trigger dependent workflows. The event is a record in the store; the workflow polls or is triggered by the record.

### Human-in-the-Loop (HITL)
- **Level 4 ratification**: David reviews distillation, answers open questions, approves or rejects
- **Open question resolution**: David answers questions surfaced by Level 3 distillations
- **Verdict override**: David overrides a machine `skip` or `defer` verdict

HITL gates are first-class workflow steps, not ad-hoc interruptions. They appear as explicit pause-and-wait steps in the Workflow Tool JS.

---

## 6. Technology Stack

### Available Now
| Tool | Role | Notes |
|------|------|-------|
| Workflow Tool | Orchestration | `DISABLE_GROWTHBOOK=1 CLAUDE_CODE_WORKFLOWS=1 claude` |
| Blackboard MCP | Transient within-run state | Confirmed: subagents can read/write via key. Not persistent across runs. |
| Scheduled cron | Timed triggers | Claude Code Desktop scheduled tasks or CronCreate |
| JSONL files | Persistent evaluation records | `census.jsonl`, `evals.jsonl`, `repos.jsonl` in `research/` |

### Substrate Decision (from YLO experiments)
| Workflow shape | Substrate | Reason |
|---------------|-----------|--------|
| Bulk parallel fan-out (Level 1 census) | Workflow Tool | Native `pipeline()`, schema per-item |
| Sequential store-heavy (Level 2 eval loop) | Blackboard | Store writes are free; WT no-filesystem penalty |
| HITL gates (Level 4 ratification) | Workflow Tool | Native pause-and-wait |
| Scheduled refresh (nightly pulse) | Workflow Tool + cron | Headless, resumable |

### Not Yet Available
- **Persistent queryable store** (Brain MCP or equivalent) — needed for cross-run queries over evaluation records. Interim: JSONL + jq. Future: proper store TBD.
- **Rollout harness** — held-out task sets per capability station + scoring rubric. Needed for Level 2b and the validation gate. Design TBD.

---

## 7. Data Schemas

### Level 0 — Repo Scorecard Record (`research/repos.jsonl`)
```json
{
  "repo_id": "compound-engineering",
  "quality_tier": 5,
  "relevance": "high",
  "freshness": "active",
  "last_commit": "2026-05-01",
  "overlap": ["agent-skills-osmani", "bmad-method"],
  "unique_contribution": "Single-axis specialist reviewer pattern with depth calibration",
  "priority": "high",
  "assessed_at": "2026-05-26",
  "source_version": "abc123"
}
```

### Level 1 — Census Record (`research/census.jsonl`)
```json
{
  "artifact_id": "compound-engineering:agent:ce-adversarial-reviewer",
  "cluster": "code-review",
  "quality_tier": 5,
  "verdict": "evaluate",
  "verdict_reason": "Most complete single-axis specialist design in corpus",
  "assessed_at": "2026-05-26",
  "source_version": "abc123"
}
```

### Level 2a — Qualitative Scorecard (`research/evals.jsonl`)
```json
{
  "artifact_id": "compound-engineering:agent:ce-adversarial-reviewer",
  "quality_score": 5,
  "adoption_fit": "strong",
  "uniqueness": "rare",
  "composability": "called-by-others",
  "description_craft": "trigger",
  "mineable_phrasing": ["25-or-below suppress rule eliminates speculative findings"],
  "gap_analysis": "Depth calibration (Quick/Standard/Deep) is missing from David's current 6 specialists",
  "deprecated": false,
  "evaluated_at": "2026-05-26",
  "source_version": "abc123"
}
```

### Canonical Artifact (`canonical/<type>/<name>/`)
```
canonical/
  skills/
    code-review/
      SKILL.md           ← David's voice, schema-validated
      provenance.json    ← winner mechanism, sources, version hashes
      _source/
        compound-engineering--ce-adversarial-reviewer.md   ← verbatim copy
        appydave-plugins--review-blind-hunter.md           ← verbatim copy
```

### `provenance.json` (per canonical artifact)
```json
{
  "artifact_id": "skills/code-review",
  "version": "1.0.0",
  "ratified_at": "2026-05-26",
  "winner_mechanism": "compound-engineering:agent:ce-adversarial-reviewer",
  "sources": [
    {
      "artifact_id": "compound-engineering:agent:ce-adversarial-reviewer",
      "source_version": "abc123",
      "what_was_kept": "Depth calibration 3-tier, technique taxonomy, non-overlap section",
      "what_was_set_aside": "Ruflo JSON output format"
    }
  ],
  "validation_score": null,
  "validation_baseline": null
}
```

---

## 8. Workflows to Build (Phased)

### Phase 1 — Census Foundation (buildable now)
1. **`level-1-census.workflow.js`** — reads `artifacts.jsonl`, fans out in parallel (Workflow Tool `pipeline()`), produces census record per artifact, appends to `research/census.jsonl`. Input: batch of artifact IDs. Output: census records.
2. **`level-0-repo-scorecard.workflow.js`** — reads each upstream repo's recon report, produces Level 0 scorecard, writes to `research/repos.jsonl`.

### Phase 2 — Evaluation Pipeline (requires Phase 1)
3. **`level-2a-eval.workflow.js`** — takes artifact IDs with `verdict: evaluate`, fans out deep eval per artifact, appends to `research/evals.jsonl` and writes markdown to `research/evaluations/`.
4. **`prepare-ingestion-brief.workflow.js`** — reads a backlog item, fans out to read all relevant Level 2 records, synthesizes brief. (Already planned in phase-b-next-steps.)

### Phase 3 — Distillation and Ratification (requires Phase 2)
5. **`level-3-distillation.workflow.js`** — triggered when a cluster's Level 2 coverage is complete. Synthesizes winner + bounded edits + open questions.
6. **`level-4-ratification.workflow.js`** — HITL gate. Presents distillation to David, collects answers, writes canonical artifact.

### Phase 4 — Refresh and Pulse (requires Phase 1–3)
7. **`upstream-pulse.workflow.js`** — scheduled nightly. Scans 14 repos, detects new/changed artifacts, queues Level 1 census runs.
8. **`freshness-check.workflow.js`** — scheduled weekly. Diffs `source_version` in evals against current repo state, surfaces stale records.

### Phase 5 — Rollout Evaluation (requires Phase 3 + rollout harness)
9. **`level-2b-rollout-eval.workflow.js`** — runs a skill on a held-out task set, scores outputs, records rollout score.
10. **`validation-gate.workflow.js`** — challenger vs canonical: accept edit only if strictly improves validation score.

---

## 9. Boundaries

### Always do
- Every canonical artifact gets a `provenance.json` and at least one verbatim source copy in `_source/`. No exceptions.
- Skills are stack-agnostic. Stack-specific terminology in a canonical skill body is a defect.
- Use David's voice in `canonical/` — trigger-only YAML descriptions, terse, no marketing prose.
- When updating a ratified artifact, make bounded add/delete/replace edits. Version, don't overwrite.
- Append to JSONL records; never mutate existing records in place (they are the audit trail).
- Every evaluation record includes `source_version` so staleness is detectable.

### Ask David first
- Any change to a ratified canonical artifact (even a typo fix — these are versioned)
- Adding a new upstream provider repo to the warehouse
- Changing the evaluation schema (breaks existing records)
- Skipping the validation gate for a promotion
- Answering open questions in a Level 3 distillation (only David can resolve these)
- Any decision that collapses two capability stations or splits one

### Never do
- Don't move or rename `research/`. It is the frozen corpus — referenced by skills in appydave-plugins.
- Don't add data to `research/` that wasn't sourced from a recon/discover/distill/eval phase.
- Don't ingest from the 76 existing distillations until the cluster's Level 2 coverage is confirmed complete.
- Don't write skill code directly into the appydave-plugins repo. `canonical/` is the staging ground; copying to plugins is a separate explicit decision.
- Don't rewrite a ratified canonical artifact in-place. New version only.
- Don't treat the Blackboard MCP as persistent storage — it's within-run state only.

---

## 10. Open Decisions (David input needed before Phase 2+)

| Decision | Stakes | Options |
|----------|--------|---------|
| Rollout harness design | Required for Level 2b and the validation gate | Held-out task sets per cluster? Synthetic benchmarks? Real workflow outputs? |
| Persistent queryable store | Required for cross-run queries at scale | JSONL + jq (now), Brain MCP (future), SQLite, other |
| Schema validation tooling | Ensures canonical artifacts meet the spec | JSON Schema + CI check? Manual + checklist? |
| SkillOpt as provider #15 | Should the paper's techniques be formally harvested into the warehouse? | Add as research input with its own recon → eval → distillation |
| Handling the 76 suspect distillations | They were written with incomplete Level 2 coverage | Mark all as provisional? Delete and regenerate? Keep as-is with caveat? |

---

## 11. Success Criteria

**Phase 1 complete when:**
- Level 0 repo scorecards exist for all 14 repos (machine-readable in `repos.jsonl`)
- Level 1 census records exist for all 1,100 artifacts in `census.jsonl`
- `level-1-census.workflow.js` runs end-to-end on a batch of 100 artifacts

**Phase 2 complete when:**
- Level 2a scorecards exist for all artifacts with `verdict: evaluate` in `evals.jsonl`
- `prepare-ingestion-brief.workflow.js` produces a consolidated brief from research files

**Phase 3 complete when:**
- First canonical artifact ratified (code-review cluster)
- `canonical/INDEX.md` has 1+ entries
- Level 3 distillation for code-review cluster rebuilt from complete Level 2 coverage

**Living system complete when:**
- Nightly upstream pulse runs unattended and queues new census work
- Stale evals are surfaced automatically
- Validation gate applied to at least one canonical promotion
- David's attention is reserved for HITL gates and open questions, not routine processing
