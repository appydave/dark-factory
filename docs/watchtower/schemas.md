# Watchtower v0 — Data Contracts & API Surface

**Status**: draft v0 — 2026-05-28
**Author**: agent — `agent-skills:api-and-interface-design`
**Scope**: v0 only. Single user, local-only, file-backed. No auth, no multi-tenancy, no network exposure beyond `127.0.0.1`.
**Companion**: `chatgpt-brief.md` (strategic), `context.md` (decisions made), `../dark-factory-living-system-spec.md` (parent).

> **Design stance.** This document treats every observable field as a commitment (Hyrum's Law). v0 is small on purpose. Each field added now is a forever-field unless explicitly marked `unstable`. Where the brief is loose, this doc tightens it; dissent is marked **[DISSENT]**.

---

## 1. Common Envelope

Every record — `experiment`, `run`, `learning`, `promotion` — shares a header. This is the contract: if you read any of these files, these fields are guaranteed.

```yaml
# Envelope (all records)
id:           string    # see ID conventions §1.1, required, immutable
kind:         enum      # "experiment" | "run" | "learning" | "promotion", required
schema_version: string  # "0.1", required — bumps on breaking change
created_at:   string    # ISO-8601 with offset, required, immutable
updated_at:   string    # ISO-8601 with offset, required, set on every write
owner:        string    # "david" | "swagger" | "<agent-name>", required
source_refs:  array     # see §1.2, optional, additive
tags:         array     # array[string], optional, free-form
notes:        string    # optional, human prose, never parsed
```

### 1.1 ID conventions

IDs are filename-stable. They are the canonical reference across records.

| Kind        | Format                              | Example                                          |
|-------------|-------------------------------------|--------------------------------------------------|
| experiment  | `exp-YYYYMMDD-<kebab-slug>`         | `exp-20260528-thumbnail-ideas`                   |
| run         | `run-<experiment-suffix>-NNN`       | `run-thumbnail-ideas-001`                        |
| learning    | `learn-YYYYMMDD-<kebab-slug>`       | `learn-20260528-thumbnail-contrast`              |
| promotion   | `promote-YYYYMMDD-<kebab-slug>`     | `promote-20260528-thumbnail-ideation`            |

Rules:
- ASCII lowercase, digits, dashes only. Validated by regex `^(exp|run|learn|promote)-[a-z0-9-]+$`.
- IDs **are** filenames (minus extension). One record per file.
- Slug max 40 chars. Total id max 64 chars.
- **[DISSENT vs brief]** The brief used `run-2026-05-28-001`. I drop the dashes in the date (`20260528`) and key runs to the experiment, not the date — runs are children of experiments, not of days. This makes `ls data/runs/run-thumbnail-ideas-*.json` work.

### 1.2 `source_refs` shape

Provenance pointer back into the dark-factory corpus. Optional but strongly encouraged on learnings and promotions.

```yaml
source_refs:
  - kind: artifact      # "artifact" | "census" | "eval" | "distillation" | "canonical" | "external"
    id:   "agent-skills-osmani:skill:api-and-interface-design"
    path: "research/artifacts.jsonl"   # optional file pointer
    line: 1                            # optional line number for jsonl
```

`kind=external` allows links to URLs, papers, ChatGPT transcripts — anything outside the repo.

---

## 2. Record Schemas

All schemas below are pseudo-JSON-Schema for readability. Authoritative versions live in `apps/watchtower/schemas/*.schema.json` (to be generated from this doc).

### 2.1 `experiment.yml`

```yaml
# inherits envelope
id:           "exp-20260528-thumbnail-ideas"
kind:         "experiment"
schema_version: "0.1"
status:       "proposed"   # see §2.1.1 — required, enum
title:        "Turn a transcript into 5 thumbnail ideas"  # required, <=120 chars

intent:                              # required block
  user_goal:  string                 # required, <=200 chars
  domain:    string                  # required, free-form ("youtube", "dark-factory", ...)
  lane:      string                  # optional
  station:   string                  # optional

hypothesis:                          # required block
  claim:           string            # required
  success_signal:  string            # required — concrete, testable in plain English

inputs:                              # optional, free-form key/path map
  transcript_path: "data/input/transcript.md"

workflow:                            # required block — how this gets executed
  type:    enum                      # "workflow_tool" | "manual" | "shell"  (see §7)
  harness: string                    # required if type=workflow_tool: path under .claude/workflows/
  agents:  array[string]             # optional, informational
  args:    object                    # optional, JSON-passed to harness verbatim

outputs:                             # optional block
  expected: array[string]            # filenames or globs the experiment is expected to produce

decision:                            # required block
  options: array[enum]               # subset of: ["discard","rerun","improve","promote_to_workflow"]
  chosen:  enum|null                 # null until David decides; one of the options above
  decided_at: string|null            # ISO timestamp when chosen was set
  decided_by: string|null            # "david" almost always

run_ids:     array[string]           # references run.json ids; appended by runner, never edited by Watchtower
learning_ids: array[string]          # references learning ids; appended by Learning Miner
promotion_id: string|null            # set when a promotion record is created against this exp
```

#### 2.1.1 `experiment.status` lifecycle

Single status field. Enum, no implicit transitions.

```
proposed  ──► running  ──► complete  ──► (decided)
   │           │
   └─► killed  └─► failed
```

Allowed values: `proposed`, `running`, `complete`, `failed`, `killed`.

> **Note on overloading.** `status` covers execution state only. The *decision* lives in `decision.chosen`. The *promotion* lives in `promotion_id`. Three separate fields, three separate concerns. (See §8 red flags.)

### 2.2 `run.json`

```json
{
  "id": "run-thumbnail-ideas-001",
  "kind": "run",
  "schema_version": "0.1",
  "created_at": "2026-05-28T09:00:00+10:00",
  "updated_at": "2026-05-28T09:08:00+10:00",
  "owner": "swagger",
  "experiment_id": "exp-20260528-thumbnail-ideas",
  "status": "complete",
  "started_at": "2026-05-28T09:00:00+10:00",
  "ended_at":   "2026-05-28T09:08:00+10:00",
  "steps": [
    {
      "name": "read-transcript",
      "status": "pass",
      "started_at": "2026-05-28T09:00:00+10:00",
      "ended_at":   "2026-05-28T09:00:31+10:00",
      "duration_ms": 31000,
      "output_ref": "data/runs/run-thumbnail-ideas-001/step-01.json",
      "reason": null
    }
  ],
  "cost": {
    "tokens_input":  12000,
    "tokens_output": 6231,
    "usd_estimate":  0.41,
    "model":         "claude-opus-4-7"
  },
  "artifacts": [
    { "kind": "file", "path": "data/runs/run-thumbnail-ideas-001/thumbnail_concepts.json" }
  ],
  "error": null
}
```

Constraints:
- `run.status` enum: `pending`, `running`, `complete`, `failed`, `aborted`. **Different enum from experiment.status** — these are different machines. Don't reuse.
- `steps[].status` enum: `pending`, `running`, `pass`, `fail`, `skipped`.
- `duration_ms` is integer milliseconds — not seconds (the brief used seconds; ms is what every runtime emits).
- `cost.usd_estimate` is non-authoritative — never bill from this; it's display-only.
- `error` is null on success, `{ code, message, step }` on failure. Same shape across all errors (see §6).

**[DISSENT vs brief]** Brief used `duration_seconds`. I use `duration_ms` because every step timer in JS/Python emits ms and rounding to seconds loses signal on fast steps.

### 2.3 `learning.yml`

```yaml
id:           "learn-20260528-thumbnail-contrast"
kind:         "learning"
schema_version: "0.1"
created_at:   "2026-05-28T09:09:00+10:00"
updated_at:   "2026-05-28T09:09:00+10:00"
owner:        "swagger"

source_run:   "run-thumbnail-ideas-001"   # required
source_experiment: "exp-20260528-thumbnail-ideas"  # required, denormalized for queryability
layer:        "prompt"                    # required — see §3 taxonomy

learning:                                  # required block
  summary:   string                        # required, <=200 chars, one sentence
  evidence:  string                        # required, what in the run showed this
  applies_to: array[string]                # optional, free-form scope tags

recommendation:                            # optional block
  change_type: enum   # "prompt_patch" | "agent_edit" | "skill_edit" | "workflow_edit"
                      # | "harness_edit" | "schema_edit" | "ui_edit" | "orchestration_edit"
                      # | "data_fix" | "none"
  target:      string  # path or canonical id of the thing to change
  patch:       string  # plain English description of the change (NOT a diff in v0)

confidence:           enum    # "low" | "medium" | "high" — required
promotion_candidate:  boolean # required — does this warrant a promotion record?

superseded_by: string|null    # learning id that replaces this one (versioning hook)
```

### 2.4 `promotion.yml`

```yaml
id:           "promote-20260528-thumbnail-ideation"
kind:         "promotion"
schema_version: "0.1"
created_at:   "2026-05-28T09:10:00+10:00"
updated_at:   "2026-05-28T09:10:00+10:00"
owner:        "swagger"

candidate_experiment: "exp-20260528-thumbnail-ideas"   # required
candidate_learnings:  ["learn-20260528-thumbnail-contrast"]  # required, may be empty array
candidate_run:        "run-thumbnail-ideas-001"        # required — the proof-run

decision:     enum     # "promote" | "not_yet" | "reject"  — required
reason:       array[string]  # required, non-empty — bullet list of reasons

# Promotion criteria (from living-system-spec §3, Level 4 ratification)
criteria:
  successful_run:        boolean  # required
  captured_learning:     boolean  # required
  repeatable_harness:    boolean  # required
  watchtower_view:       boolean  # required
  named_owner:           boolean  # required
  validation_gate_passed: boolean|null  # null in v0 (gate not yet built)

next_action:
  type:  enum   # "rerun_with_patch" | "ratify_canonical" | "park" | "discard"
  owner: string                       # "david" | "swagger" | "<agent>"
  due_by: string|null                 # ISO date, optional

canonical_target: string|null   # if decision=promote: target path under canonical/ (e.g. "canonical/skills/thumbnail-ideation")
```

Rule: `decision: promote` is only valid if **all** `criteria.*` booleans are true (except `validation_gate_passed`, which is `null` in v0). Schema enforces this with a validation hook in the API layer.

---

## 3. Layer Taxonomy

The `learning.layer` field uses a closed enum. New layers require a schema bump.

```yaml
layer:
  enum:
    - prompt           # text inside an agent or skill prompt
    - agent            # an agent's role/instructions/tools
    - skill            # a SKILL.md file (canonical or upstream)
    - workflow         # .claude/workflows/*.workflow.js shape
    - harness          # how a workflow is invoked / its runtime scaffolding
    - evaluation       # rubric, scoring, success_signal definition
    - data_schema      # any record schema in this doc, census, evals, etc.
    - watchtower_ui    # screen, table, button, layout in Watchtower itself
    - orchestration    # Swagger / Architect / Builder / Evaluator coordination patterns
```

One-line examples:

| Layer            | Example learning                                                                  |
|------------------|-----------------------------------------------------------------------------------|
| prompt           | "Thumbnail prompt needs an explicit `contrast_strategy` field."                   |
| agent            | "Evaluator agent accepts vague ideas — add scoring rubric reference."             |
| skill            | "`browser-testing-with-devtools` skill needs MCP availability precheck."          |
| workflow         | "Level-1 census should checkpoint between batches, not after."                    |
| harness          | "Workflow Tool runs need filesystem-write step; Blackboard alone insufficient."   |
| evaluation       | "Success signal 'David marks 2 usable' too binary — needs 1–5 scale."             |
| data_schema      | "`run.json` needs `experiment_id` denormalized into every step for query speed."  |
| watchtower_ui    | "Today screen should group by decision-needed, not by recency."                   |
| orchestration    | "Swagger should ask David before promoting, not after writing promotion.yml."     |

---

## 4. Cross-Record Relationships

```
                ┌────────────────────────┐
                │  experiment.yml        │
                │  (status, decision)    │
                └─────────┬──────────────┘
                          │ 1
                ┌─────────┴─────────────┐
                │                       │
            1..n│                    0..1│
                ▼                       ▼
        ┌───────────────┐       ┌────────────────────┐
        │  run.json     │       │  promotion.yml     │
        │  (steps,cost) │       │  (decision,        │
        └───────┬───────┘       │   criteria)        │
            1   │               └────────────────────┘
                │ produces                ▲
            0..n│                    0..n │ references
                ▼                         │
        ┌────────────────┐                │
        │  learning.yml  │────────────────┘
        │  (layer,       │
        │   recommendation)│
        └────────────────┘
```

**Foreign-key rules**:
- A `run.experiment_id` MUST reference an existing experiment.
- A `learning.source_run` MUST reference an existing run.
- A `learning.source_experiment` MUST equal `runs[source_run].experiment_id` (denormalized but checked).
- A `promotion.candidate_experiment` MUST exist; `candidate_run` MUST belong to it.
- An `experiment.promotion_id` is **derived** — only Watchtower's index sets it; never hand-edited.
- Cycles are forbidden. `learning.superseded_by` must point forward in time.

---

## 5. Filesystem Layout

```
dark-factory/
  data/
    experiments/  exp-20260528-thumbnail-ideas.yml
    runs/         run-thumbnail-ideas-001.json
                  run-thumbnail-ideas-001/    # optional sidecar dir for step artifacts
                    step-01.json
                    thumbnail_concepts.json
    learnings/    learn-20260528-thumbnail-contrast.yml
    promotions/   promote-20260528-thumbnail-ideation.yml
    index.json    # auto-generated by Watchtower; not hand-edited
```

Decisions:

1. **YAML for human-edited records, JSON for machine-emitted records.** Experiments, learnings, promotions are human-touched (David tweaks them, Swagger drafts them). Runs are pure telemetry — never hand-edited — so JSON. This matches the brief.
2. **One file per record.** No JSONL aggregation at this layer. The `research/*.jsonl` files are append-only audit logs and stay where they are (frozen corpus per the living-system spec). Watchtower records are mutable individual files.
3. **Run sidecars colocated.** `data/runs/<run-id>/` holds large step outputs; `data/runs/<run-id>.json` is the index. Path stable enough to link from UI.
4. **`index.json` is derived state.** Watchtower scans the four dirs on boot and emits `index.json` for fast list/filter. Deleting `index.json` is always safe — it rebuilds.

**Alternative considered**: SQLite for the index. Rejected for v0 — adds a binary file to version-control awkwardness and one more thing that can be out of sync. JSON index can be regenerated in <1s for v0 volumes (hundreds of records).

---

## 6. Watchtower API Surface

### 6.1 Position: Watchtower is a thin reader, not a mutator (with two exceptions)

**The core decision**: Watchtower mostly reads files; it mutates **only David's decision fields**. Workflow harnesses own everything else.

| Field domain                              | Who writes                          |
|-------------------------------------------|-------------------------------------|
| Run telemetry (`run.json` in full)        | Workflow harness only               |
| Learning records                          | Learning Miner agent (via harness)  |
| Experiment status transitions             | Workflow harness                    |
| Experiment **decision** (`decision.chosen`) | **Watchtower** (button click)     |
| Promotion records                         | **Watchtower** (button click), then harness can append `next_action.*` |
| Index file                                | Watchtower                          |

Rationale: Hyrum's Law. If Watchtower can rewrite `run.json`, someone will eventually use a button to "fix" telemetry. That's a data-integrity hole. Lock telemetry-writes to the harness; UI only writes the human-decision deltas.

### 6.2 REST routes

Local HTTP on `127.0.0.1:<port>`, no auth, JSON in/out, standard error envelope (§6.3).

```
GET    /api/today                          → curated queue for the Today screen
GET    /api/experiments                    → list, with ?status= ?decision= ?limit= ?cursor=
GET    /api/experiments/:id                → full experiment
POST   /api/experiments/:id/decision       → set decision.chosen   (Watchtower-writable)
POST   /api/experiments/:id/trigger        → launch run            (see §7)
DELETE /api/experiments/:id                → soft-delete (sets status=killed; no file removal)

GET    /api/runs                           → list, with ?experiment_id= ?status= ?limit=
GET    /api/runs/:id                       → full run
GET    /api/runs/:id/stream                → SSE stream of step events (read-only)

GET    /api/learnings                      → list, with ?layer= ?promotion_candidate= ?limit=
GET    /api/learnings/:id                  → full learning

GET    /api/promotions                     → list, with ?decision=
GET    /api/promotions/:id                 → full promotion
POST   /api/promotions                     → create promotion record (Watchtower-writable)
POST   /api/promotions/:id/decide          → set decision + reason (Watchtower-writable)

GET    /api/index                          → list of all records, denormalized for UI tables
POST   /api/index/rebuild                  → force rebuild from files (idempotent)

GET    /api/health                         → { ok: true, version, schema_version }
```

Notes:
- All list endpoints paginate. Default `limit=50`, max `200`. Cursor is the last-seen `id`.
- `PATCH` is **not exposed**. Mutations are explicit named actions (`/decision`, `/decide`) so the API surface is small and audit-friendly. Adding generic PATCH later would be additive and safe.
- `DELETE` is soft. Files are never removed by Watchtower; status flips to `killed`.

### 6.3 Error envelope

Single shape, every error:

```json
{
  "error": {
    "code":    "VALIDATION_ERROR",
    "message": "experiment.decision.chosen must be one of decision.options",
    "details": { "got": "promote_to_workflow", "allowed": ["discard","rerun","improve"] }
  }
}
```

Codes (closed enum for v0): `VALIDATION_ERROR`, `NOT_FOUND`, `CONFLICT`, `FK_VIOLATION`, `HARNESS_UNAVAILABLE`, `SCHEMA_MISMATCH`, `INTERNAL`.

HTTP status mapping is standard (400/404/409/422/500). The body shape is the contract; the status code is a hint.

### 6.4 File operations

- Reads use `fs.readFile` + YAML/JSON parse + schema-validate. Invalid files surface as warnings on `/api/index`, never crash the server.
- Writes use atomic write-temp-then-rename (`*.tmp` then `rename()`). Crash-safe.
- Watchtower watches the four `data/` subdirs with `chokidar` (or equivalent) and refreshes the in-memory index. SSE pushes deltas to open Today screens.

---

## 7. Workflow Integration Contract

Three options were on the table. I evaluated all three; recommendation is **(a) file-trigger + harness watcher** for v0, with a clean upgrade path to (c) MCP later.

| Option                            | Pros                                       | Cons                                                  |
|-----------------------------------|--------------------------------------------|-------------------------------------------------------|
| **(a) File trigger**              | Decoupled, restartable, audit trail = files | Latency (~1s watcher poll); needs a runner process    |
| **(b) Shell out from Watchtower** | Simplest; no extra process                  | Watchtower owns subprocess lifecycle (logs, OOMs, zombies); kills the "thin reader" stance |
| **(c) MCP bridge**                | Clean protocol; reusable                    | Premature; MCP for workflow-trigger isn't standardised here yet |

**Choice: (a).** Rationale:

1. Watchtower stays a reader. No subprocess management leaking into the UI server.
2. The file IS the audit trail. `experiment.status: proposed` → harness picks it up → flips to `running`. No hidden state.
3. The harness runner can be `nohup node .claude/workflow-runner.js` started by a separate launchd job or a Watchtower-launched helper — but logically separate.
4. Upgrade to MCP is purely additive: add a second trigger mechanism without changing the experiment record shape.

### 7.1 Contract

**Trigger** (Watchtower → harness):

1. Watchtower writes `data/experiments/<id>.yml` with `status: proposed` and `workflow.type: workflow_tool` plus `workflow.harness: .claude/workflows/level-1-census.workflow.js` plus `workflow.args: {...}`.
2. Watchtower writes a single-line trigger file `data/experiments/<id>.trigger` containing `{ "requested_at": "...", "by": "watchtower" }`.
3. Harness watcher polls `data/experiments/*.trigger` every 2s.

**Execution** (harness):

4. Harness picks up trigger; deletes the `.trigger` file (claims the work).
5. Harness flips `experiment.status` → `running`, sets `updated_at`.
6. Harness creates `data/runs/<run-id>.json` with `status: running`.
7. Harness streams step events into the run file (append `steps[]`, update `updated_at`).
8. On completion: writes final run state; flips experiment to `complete` or `failed`; appends `run_id` to `experiment.run_ids`.
9. Learning Miner (separate agent in same harness) writes `learning.yml` files and appends ids to `experiment.learning_ids`.

**Discovery** (Watchtower → user):

10. File watcher in Watchtower sees the updates, pushes SSE to open UI.

### 7.2 Concurrency

v0 single-user. The trigger-file claim (step 4) is the only mutex. If two runners are accidentally active, one will lose the race on `unlink` — acceptable. No locking infrastructure for v0.

### 7.3 The census workflow specifically

`level-1-census.workflow.js` currently takes `{ artifactsPath, censusPath, batchStart, batchSize, ts }`. The mapping:

```yaml
workflow:
  type: workflow_tool
  harness: ".claude/workflows/level-1-census.workflow.js"
  args:
    artifactsPath: "research/artifacts.jsonl"
    censusPath:    "research/census.jsonl"
    batchStart:    5
    batchSize:     5
    ts:            "2026-05-28T00:00:00+10:00"
```

No changes required to the existing workflow. The harness wrapper does the experiment/run bookkeeping around it.

---

## 8. Red Flags / Anti-Patterns Avoided

| Anti-pattern                                                | How this design avoids it                                                  |
|-------------------------------------------------------------|----------------------------------------------------------------------------|
| Overloaded `status` field (mixes execution + decision)      | Three fields: `status`, `decision.chosen`, `promotion_id`. Each one job.   |
| Mixed error formats across endpoints                        | Single envelope §6.3, closed code enum.                                    |
| Leaking implementation in URLs (`/api/createExperiment`)    | Resources only; verbs on sub-paths (`/decision`, `/decide`) where needed.  |
| Reusing `run.status` enum as `experiment.status`            | **Separate enums** — different state machines, never conflated.            |
| List endpoint with no pagination                            | All list endpoints paginate, hard `limit` cap of 200.                      |
| Silent defaulting of required fields                        | Required fields are schema-enforced; missing → `VALIDATION_ERROR`, never a default. |
| PATCH that quietly accepts unknown fields                   | `PATCH` deliberately not exposed in v0. Named actions only.                |
| Reading external data without validation                    | All file reads pass through schema validation before reaching the API.    |
| Duration in seconds (loses sub-second signal)               | `duration_ms` (integer ms) everywhere.                                     |
| Cycles in references                                        | `learning.superseded_by` is forward-in-time only; FK validator rejects cycles. |
| Watchtower mutating telemetry (data-integrity hole)         | Watchtower is read-only except for two named decision actions (§6.1).      |
| Stringly-typed enums spread across the codebase             | Every enum is declared once here; schemas generate TS types.               |
| Underscored "private" fields that leak into responses       | No underscore fields. If it's in the schema, it's public.                  |
| Date strings without timezone                               | All timestamps ISO-8601 with offset, required.                             |
| `null` vs missing field ambiguity                           | All optional fields are explicitly `null` when unset, never absent.        |

---

## 9. Out of Scope (v0)

Anything below is explicitly **not** v0. Listed so they don't sneak in.

- Authentication / multi-user / RBAC
- Remote access (CORS, public hosting, TLS)
- Real-time collaborative editing
- Workflow execution inside the Watchtower process
- Validation gate / rollout score field enforcement (`promotion.criteria.validation_gate_passed` stays `null`)
- Cost rollups across experiments / billing-grade cost tracking
- Search beyond simple filter params (no full-text, no embeddings)
- Schema migrations (v0 bumps schema_version; no automated migration tooling)
- Webhooks / event bus / external notifications
- A "diagram view" auto-generated from workflow JS (open question §10)
- Auto-promotion (decision.chosen is always set by a human in v0)
- SQLite or any binary store

---

## 10. Open Questions

Surfaced ambiguities the design could not resolve unilaterally:

1. **Where do ratified canonical artifacts live relative to a promotion?**
   `promotion.canonical_target` points at `canonical/skills/<name>` — but the actual writing of a ratified artifact (the Level 4 process in living-system-spec §3) is a separate workflow. Should Watchtower trigger it, or just record intent? **Current design: records intent only; ratification stays manual in v0.**

2. **Diagram view auto-generation.**
   `phases` array exists in `level-1-census.workflow.js` `meta.phases`. Could Watchtower render this directly? Feels like a v0.1 feature; flagging because the brief implied a visual run timeline.

3. **Re-run semantics.**
   If David clicks "rerun" on a completed experiment, does it (a) mutate the existing experiment + add a new run, or (b) clone the experiment? **Current design: option (a)** — experiment is the long-lived container, runs accumulate. But it's a real ergonomic question if reruns diverge in inputs.

4. **`research/*.jsonl` ↔ `data/` boundary.**
   The census workflow writes to `research/census.jsonl` (frozen-corpus rule). The experiment that triggered it lives in `data/experiments/`. Should the experiment record carry a copy of the census output, a pointer, or nothing? **Current design: pointer via `outputs.expected` and the run's `artifacts` block.**

5. **Multi-step learning attribution.**
   If a run produces three learnings of different layers, all from the same step, is that one learning record with `layer: array` or three records? **Current design: three records.** Cleaner queries, simpler schema, but more files.

6. **`schema_version` bump policy.**
   v0 says `"0.1"`. When does it become `"0.2"`? Proposed: any change that removes or retypes a required field. Adding optional fields stays at `0.1`. Not yet committed.

7. **Promotion of a learning, not just an experiment.**
   The brief frames promotion as experiment → workflow. But a learning marked `promotion_candidate: true` might warrant its own promotion (e.g., promote a prompt patch). Schema currently only supports `candidate_experiment`. **Open: should `promotion.candidate_kind` allow `learning`?**

8. **Index rebuild on conflict.**
   If `data/experiments/<id>.yml` exists with a conflicting `kind` or malformed schema, `/api/index` currently logs a warning. Should it 500 the entire index instead? **Current design: graceful degrade.** Could be wrong.

---

## 11. Verification Checklist

Before this schema is built against:

- [ ] Every record kind has a JSON-Schema file under `apps/watchtower/schemas/`.
- [ ] FK validator implemented (rejects orphan run_ids, learning.source_run, promotion.candidate_*).
- [ ] All enums declared once, imported everywhere.
- [ ] Atomic write helper (write-temp-rename) used for every mutation.
- [ ] Error envelope used by every error path, including unhandled exceptions (mapped to `INTERNAL`).
- [ ] `id` regex validator wired up.
- [ ] Trigger-file claim semantics tested with two concurrent runners (race resolved cleanly).
- [ ] One end-to-end test: trigger census batch via API → run.json appears → experiment.status flips → SSE event fires.

---

**End of v0 schema spec.**
