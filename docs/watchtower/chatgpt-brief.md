# Watchtower v0 — Strategic Brief (from ChatGPT)

> **⚠️ ARCHIVE-BOUND (2026-06-06) — see [`RE-BUCKETING.md`](RE-BUCKETING.md).** Process/history from the v0 drafting
> era; kept for provenance, not current design. For the live three-plane model read RE-BUCKETING.md +
> [`../dark-factory-constellation.md`](../dark-factory-constellation.md).

**Origin**: ChatGPT synthesis, 2026-05-28
**Status**: input to requirements gathering — not a spec, not a plan
**Purpose**: shared context for the three parallel requirements-gathering agents

---

You are not stuck because you lack ideas. You are stuck because the system has no control surface yet.

Right now you have:

```text
research corpus
workflow experiments
Mochaccino visualisations
canonical skill ideas
POEM roles
BMAD-style orchestration ideas
Dark Factory architecture
```

But you do **not yet have a small operating system** that says:

```text
What are we trying today?
Who owns it?
What experiment is being run?
What evidence came back?
What learning was captured?
Did this promote into a real workflow?
What should David look at next?
```

That missing layer is the Watchtower app.

Your instinct is right: **Mochaccino is good for proof-of-concept visuals, but not enough as the long-term command surface.** The existing docs already define the Watchtower as the place where you observe workflows, variants, bottlenecks, failures, cost, dashboards, projections, and promotion decisions.

## Recommendation

Build **Dark Factory Watchtower** as a first-class AppyStack app, but keep it **inside the Dark Factory repo for now**.

Not separate yet.

The reason is simple: the data model, agents, workflow events, experiment schema, and promotion logic are still changing. Splitting it out too early will add friction. Keep it colocated until the interfaces harden.

```text
dark-factory/
  canonical/
  research/
  .claude/workflows/
  apps/watchtower/          ← first-class app
  data/
    experiments/
    runs/
    learnings/
    promotions/
```

Later, when the boundary stabilises, Watchtower can become its own app or plugin.

## The North Star

Your North Star is not "build lots of workflows."

It is:

```text
Build a factory that can design, run, observe, learn from,
improve, and promote its own workflows.
```

That means the first useful product is not the thumbnail workflow. It is not the SDLC workflow. It is not the census dashboard.

The first useful product is this:

```text
A tiny architect/orchestrator loop that turns:
"I want to do X today"

into:

1. an experiment spec
2. a runnable workflow/harness
3. an execution record
4. a visual result
5. a captured learning
6. a decision: discard / rerun / improve / promote
```

That is the spine.

## Swagger + Watchtower v0

Swagger is the daily interface. Not Penny, Alec, or Oscar directly.

```text
David
  │
  ▼
Swagger
  │
  ├── reads today's ticket
  ├── decides which worker to call
  ├── delegates one worker at a time
  ├── receives the result
  ├── recommends the next move
  └── asks David only at decision gates
```

Behind Swagger, specialist roles:

```text
Swagger
  ├── Architect        designs experiment/workflow
  ├── Builder          creates runnable harness/workflow
  ├── Runner           executes it
  ├── Evaluator        checks result against rubric
  ├── Learning Miner   extracts reusable learnings
  └── Promoter         decides whether experiment becomes workflow
```

## The four machine-readable records

### 1. `experiment.yml`

```yaml
id: exp-2026-05-28-thumbnail-ideas-v1
status: proposed

intent:
  user_goal: "Turn a transcript into thumbnail ideas"
  domain: youtube
  lane: thumbnail
  station: ideation

hypothesis:
  claim: "A transcript can produce 5 usable thumbnail concepts with visual composition notes"
  success_signal: "David marks at least 2 concepts as usable"

inputs:
  transcript_path: data/input/transcript.md

workflow:
  type: experiment
  harness: thumbnail-ideation-v0
  agents:
    - transcript-reader
    - thumbnail-concept-designer
    - evaluator

outputs:
  expected:
    - thumbnail_concepts.json
    - evaluation.json
    - learning.yml

decision:
  options:
    - discard
    - rerun
    - improve
    - promote_to_workflow
```

### 2. `run.json`

```json
{
  "run_id": "run-2026-05-28-001",
  "experiment_id": "exp-2026-05-28-thumbnail-ideas-v1",
  "status": "complete",
  "started_at": "2026-05-28T09:00:00",
  "ended_at": "2026-05-28T09:08:00",
  "steps": [
    {"name": "read-transcript", "status": "pass", "duration_seconds": 31},
    {"name": "generate-thumbnail-ideas", "status": "pass", "duration_seconds": 242},
    {"name": "evaluate-output", "status": "fail", "reason": "Ideas lacked strong visual contrast"}
  ],
  "cost": {"tokens": 18231, "usd_estimate": 0.41}
}
```

### 3. `learning.yml`

```yaml
id: learn-2026-05-28-thumbnail-contrast
source_run: run-2026-05-28-001
layer: prompt

learning:
  summary: "Thumbnail concepts need explicit foreground/background contrast instructions."
  evidence: "All five concepts described subject and emotion but not composition contrast."
  applies_to:
    - youtube.thumbnail.ideation
    - visual-design.prompting

recommendation:
  change_type: prompt_patch
  target: agents/thumbnail-concept-designer.md
  patch: "Add a required field: contrast_strategy."

confidence: medium
promotion_candidate: true
```

### 4. `promotion.yml`

```yaml
id: promote-2026-05-28-thumbnail-ideation
candidate: exp-2026-05-28-thumbnail-ideas-v1

decision: not_yet

reason:
  - "Workflow produced valid output"
  - "Evaluation found a repeatable gap"
  - "Needs one prompt patch and rerun before promotion"

next_action:
  type: rerun_with_patch
  owner: swagger
```

## Watchtower first screens

Build four. Today is the key one.

```text
1. Today        — "What should David look at now?"
2. Experiments  — proposed / running / completed / promoted / killed
3. Runs         — timeline, step status, cost, failure point, output links
4. Learnings    — by layer, with promotion candidates
```

```text
TODAY
────────────────────────────────────────

Needs David decision
- exp-thumbnail-ideas-v1
  Result: pass with weak visual contrast
  Recommendation: rerun with prompt patch
  Buttons: Accept / Rerun / Promote / Kill

Recently completed
- census-batch-0
  5 assessed, 3 adopt, 2 evaluate
  Recommendation: continue batch 1

System warnings
- Learnings not attached to canonical target: 3
- Experiments completed without promotion decision: 2
```

You do not browse 1,150 artifacts. You do not browse 20 dashboards. You look at a queue of decisions.

## System diagram

```text
                         DARK FACTORY SYSTEM

┌────────────────────────────────────────────────────────────────┐
│                            DAVID                               │
│                 chooses intent, reviews decisions              │
└──────────────────────────────┬─────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────┐
│                           SWAGGER                              │
│              daily conductor / right-hand operator             │
│  Reads ticket → delegates worker → receives result → decides   │
│  next move → asks David only when judgement is required        │
└──────────────────────────────┬─────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  Architect   │       │   Builder    │       │   Evaluator  │
│ designs exp  │       │ builds run   │       │ scores run   │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       └──────────────────────┼──────────────────────┘
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                         FACTORY FLOOR                          │
│             workflows / agents / skills / tools run            │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌────────────────────────────────────────────────────────────────┐
│                       MACHINE RECORDS                          │
│ experiment.yml · run.json · learning.yml · promotion.yml       │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌────────────────────────────────────────────────────────────────┐
│                         WATCHTOWER APP                         │
│      Today · Experiments · Runs · Learnings · Promotions       │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌────────────────────────────────────────────────────────────────┐
│                         CANONICAL                              │
│       promoted workflows / skills / agents / harnesses         │
└────────────────────────────────────────────────────────────────┘
```

## Experiment vs Workflow

```text
Experiment
  temporary
  rough
  allowed to fail
  designed to learn

Workflow
  promoted
  repeatable
  has a harness
  has telemetry
  has known inputs/outputs
  has promotion/provenance records
```

Promotion rule:

```text
An experiment only becomes a workflow when it has:
1. a successful run
2. a captured learning
3. a repeatable harness
4. a Watchtower view
5. a named owner/agent
6. a promotion decision
```

## What counts as a learning — the 9-layer taxonomy

A learning must have a **layer**:

```yaml
layer:
  - prompt
  - agent
  - skill
  - workflow
  - harness
  - evaluation
  - data_schema
  - watchtower_ui
  - orchestration
```

Examples:

```text
Prompt:           "Thumbnail prompt needs contrast_strategy."
Agent:            "Evaluator is too soft; it accepts vague ideas."
Workflow:         "Transcript summarisation should happen before ideation."
Harness:          "Run needs a visual diff, not just JSON output."
Watchtower UI:    "Dashboard should group by decision needed, not by artifact count."
Skill:            "image-gen skill needs fail-fast API handling."
```

## First ticket (proposed by ChatGPT)

```markdown
# Build Watchtower v0: Experiment Registry

Goal: first usable control surface for Dark Factory experiments.

Scope:
- Define experiment.yml, run.json, learning.yml, promotion.yml
- Build Today + Experiments screens
- Seed with one experiment

Out of scope:
- Dashboard polish
- Census pagination
- Real-time workflow execution
- Automatic promotion

Acceptance:
- I can see all current experiments
- I can see what needs my decision today
- I can open one experiment and see runs, learnings, promotion status
- I can mark an experiment as rerun / improve / promote / kill
- State is stored in machine-readable files
```

---

**Note for downstream agents**: this is the *strategic* brief. It is opinionated input, not finalized requirements. Your job is to interrogate, refine, structure, or challenge it as appropriate to the skill you're invoking. The final spec/plan/schema you produce is what David will act on, not this brief.
