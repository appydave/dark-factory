---
distillation_id: planning-session-and-context-continuity
stage: planning
intent: "Preserve planning context across sessions — checkpoint current state, resume a plan after interruption, track decisions made, and surface what to do next without re-reading everything"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:session-checkpoint
  - appydave-plugins:skill:omi-extract-haiku
  - appydave-plugins:skill:omi-query
  - appydave-plugins:skill:ralphy
  - appydave-plugins:skill:relay-register
  - gsd:command:gsd:check-todos
  - gsd:command:gsd:review-backlog
  - compound-knowledge:skill:kw:work
  - compound-knowledge:agent:past-work-researcher
  - everything-claude-code:skill:loop-start
  - everything-claude-code:skill:context-budget
  - everything-claude-code:agent:plan-orchestrate
  - ruflo:skill:neural-training
  - ruflo:skill:agent-arch-system-design
winner_mechanism: appydave-plugins:skill:session-checkpoint
---

# Unified Skill: planning-session-and-context-continuity

**Purpose**: At any planning boundary — session end, handover, context compaction, or day change — checkpoint the current plan state so the next session can resume exactly where the last one stopped. Prevents the "re-read-to-resume" tax.

**For Agents**: Use when David says "checkpoint this", "save state before we stop", "where were we", "what's next", "pick up where we left off", "what did we decide", "summarise progress", "handover this session", or when context is about to be compacted. This is the **cross-session continuity** skill — it is invoked at boundaries, not during active planning.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Planning work is interrupted constantly: context windows fill, sessions end, days change, David switches machines. Each interruption creates a re-read-to-resume tax: load the plan, skim decisions, reconstruct what step comes next, remember what was tried and failed. At scale, this tax is the dominant planning overhead.

The session-continuity skill eliminates the tax: at each boundary, it writes a compact checkpoint (current phase, plan units done/in-progress/blocked, decisions locked, next action) that enables a cold-start resume without re-reading the full plan chain.

This is explicitly **not** spec-writing or plan creation — it is the continuity layer that makes all other planning work resumable.

## Winner's Mechanism

`appydave-plugins:skill:session-checkpoint` is already in David's stack and wins as the baseline: it produces a structured session summary (what was done, what was decided, what comes next) at conversation end. The mechanism gap is that it is invoked manually and produces a summary for human reading, not a machine-parseable state file that can drive autonomous resume.

The pattern worth lifting from `gsd` is the **STATE.md design**: a single file with Current Position (phase, plan, status, progress bar), Performance Metrics, Accumulated Context (decisions, todos, blockers), and Session Continuity. STATE.md is the checkpoint artifact — it is written at end-of-session and read at start-of-session. Every GSD planning command reads STATE.md before acting; it is the shared memory bus for the whole planning pipeline.

`compound-knowledge:skill:kw:work` (knowledge worker loop) adds the **past-work-researcher** pattern: before starting a new planning session on a topic, search prior work for relevant decisions and outcomes. This is the "don't reinvent what was decided last week" gate. The past-work-researcher dispatches against the docs/solutions/ folder to surface institutional memory.

## Non-overlapping ideas folded in

- From `gsd:command:gsd:check-todos` + `review-backlog`: **Structured todo and backlog state** — checkpoint includes not just "where are we in the plan" but "what is on the backlog and what are the open todos". Resuming a session without knowing the backlog state means the next session re-discovers the backlog by reading code.
- From `everything-claude-code:skill:context-budget`: **Context-budget checkpoint** — include remaining context budget in the checkpoint state. "We have 40% context remaining; the next unit requires ~30%" is a planning decision. A checkpoint that ignores context budget forces the next session to re-assess it.
- From `appydave-plugins:skill:omi-query`: **Ambient capture → plan state** — OMI transcripts often contain planning decisions made in conversation ("we decided to use X not Y"). The omi-query skill can surface these decisions from ambient capture and integrate them into the checkpoint. Decisions captured in audio should flow into STATE.md, not stay isolated.
- From `ruflo:skill:neural-training`: **Decision persistence** — the neural-training pattern (capture what worked, what failed, what was decided) is a more structured version of checkpoint that feeds future agent behavior. Decisions locked during one planning session become implicit context for the next session's agents.
- From `everything-claude-code:skill:loop-start`: **Clean-state session initialization** — at the start of a new planning session, explicitly load the checkpoint, verify state is consistent, and announce the starting position. This is the resume-from-checkpoint complement to the checkpoint-at-end pattern.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|--------------------|
| appydave:session-checkpoint | Baseline checkpoint structure, manual invocation at session end | AppyDave-specific format |
| gsd:STATE.md pattern | Machine-parseable state file design; current position + accumulated context + session continuity | GSD workspace format |
| compound-knowledge:past-work-researcher | Past-work search before starting new planning session | kw: folder format |
| gsd:check-todos / review-backlog | Todo and backlog state in checkpoint | GSD command format |
| ecc:context-budget | Context budget in checkpoint state | ECC tooling |
| appydave:omi-query | Ambient decisions flowing into checkpoint | OMI MCP specifics |
| ecc:loop-start | Clean-state session initialization from checkpoint | ECC loop format |

## Boundary with adjacent sub-clusters

- **planning-roadmap-architect / sprint-planner / task-breakdown**: These produce the artifacts that session-continuity checkpoints. Session-continuity does not create plans; it tracks plan state across sessions.
- **orchestration cluster**: The GSD STATE.md pattern overlaps with the orchestration cluster's autonomous-pipeline-runner pattern. The distinction: session-continuity is human-paced (David stops and resumes); autonomous-pipeline-runner is agent-paced (pipeline runs without human stops). Same mechanism, different pace.
- **knowledge-capture cluster**: Decision persistence and OMI-capture overlap with knowledge-capture. The distinction: session-continuity captures decisions for immediate use in the next planning session; knowledge-capture captures decisions for long-term retrieval. A decision can flow through both.

## Draft SKILL.md frontmatter

```yaml
name: planning-session-continuity
description: >
  Checkpoint current plan state at session boundaries and resume cleanly from any prior checkpoint.
  Writes STATE.md with current phase/unit/decision/blocker/next-action; reads it on resume.
  Eliminates re-read-to-resume tax across session boundaries, machine switches, and context compactions.
  Use when: "checkpoint this", "save state before we stop", "where were we", "what's next",
  "pick up where we left off", "what did we decide", "summarise progress", "handover this session".
```

## Open questions for David

- STATE.md (GSD's machine-readable checkpoint) vs session-checkpoint (human-readable summary): Should David maintain both, or collapse to one format that is both machine-parseable and human-readable?
- OMI-to-STATE.md flow: decisions captured in ambient audio transcripts are valuable plan state. How much automation is wanted here? Fully automatic (omi-query runs at checkpoint time and merges relevant decisions)? Manual curation? Or separate?
- This sub-cluster has the fewest source artifacts (12) of the five planning sub-clusters. Is session-continuity actually under-represented in the corpus, or is it embedded in the workflow structure of GSD and not surfaced as its own artifact type?
