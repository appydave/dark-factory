---
distillation_id: knowledge-capture-learning-instinct-promotion
stage: knowledge-capture
intent: "Extract durable learnings from sessions and promote them into reusable instincts, skills, or knowledge docs"
created: 2026-05-17
status: draft
source_artifacts:
  - everything-claude-code:skill:continuous-learning-v2
  - everything-claude-code:skill:learn
  - everything-claude-code:skill:learn-eval
  - everything-claude-code:skill:evolve
  - everything-claude-code:skill:promote
  - everything-claude-code:skill:prune
  - everything-claude-code:skill:instinct-status
  - everything-claude-code:skill:instinct-export
  - everything-claude-code:skill:instinct-import
  - everything-claude-code:skill:ck
  - compound-engineering:skill:ce-compound
  - compound-engineering:skill:ce-compound-refresh
  - compound-engineering:skill:ce-sessions
  - compound-engineering:skill:ce-session-historian
  - compound-knowledge:skill:kw:compound
  - appydave-plugins:skill:knowledge-capture
  - appydave-plugins:skill:skill-miner
  - gstack:skill:retro
  - gstack:skill:learn
winner_mechanism: everything-claude-code:skill:continuous-learning-v2
---

# Unified Skill: Learning & Instinct Promotion

## Intent

Extract reusable patterns from a session and promote them — via quality gate — to project-scoped or global instincts, with a lifecycle (promote / prune / evolve) that keeps the knowledge base healthy over time.

## Winner's Mechanism

`continuous-learning-v2` (ECC) is the most complete end-to-end implementation: a hook-based observer captures session events automatically, creates atomic instincts with confidence scoring, then a separate `/evolve` + `/promote` + `/prune` lifecycle manages their graduation from candidate to global. The confidence-scored instinct format (`score: 0.0–1.0`) prevents knowledge bloat by making quality visible before promotion. `ck` provides the per-project persistent memory layer that instincts write into.

David already has `knowledge-capture` (capture durable patterns to memory files) and `skill-miner` (mines past JSONL transcripts for recurring patterns). These are the baseline. The gap is: no quality gate on what enters memory, no lifecycle to evolve or retire promoted items, and no hook-based automatic observation — all three are manual today.

## Existing-skill nesting (upgrading existing skills)

- **Existing mechanism (`knowledge-capture`)**: Manual, end-of-session write to `~/.claude/projects/.../MEMORY.md` or similar. One-shot capture, no quality scoring, no lifecycle. User invokes explicitly.
- **Existing mechanism (`skill-miner`)**: Mining past JSONL sessions for recurring patterns → candidate skills. Also manual, bulk-retrospective rather than per-session.
- **New mechanism's grain**: Per-session, event-driven (hook-triggered at `Stop` or explicit invocation). Atomic instinct format with `confidence` score. Scoped: project-local first, explicit promotion to global.
- **Nesting rule**: `knowledge-capture` stays as the user-facing conversational entry point ("capture this insight"). The hook-based auto-extractor (`continuous-learning-v2` mechanism) fires silently at session end as a second layer. `skill-miner` becomes a bulk retrospective pass over accumulated atomic instincts. Neither replaces the other — they operate at different grains (manual hot-path, auto end-of-session, periodic retrospective bulk).

## Non-overlapping ideas folded in

- From `compound-engineering:ce-compound`: **Dual-track schema** — separate bug track vs knowledge track, each with enforced YAML schema — `complexity: medium | optional: false | prerequisite: none`. Prevents mixed-intent entries where a bug fix gets stored as a pattern. David's memory files currently mix these indiscriminately.
- From `compound-engineering:ce-compound-refresh`: **Staleness review** — re-compare documented learnings against current codebase and deprecate/update stale entries — `complexity: low | optional: true | prerequisite: "docs/solutions/ has >20 entries"`. Without this, knowledge docs drift and become misleading.
- From `compound-engineering:ce-session-historian`: **Session-archaeology mode** — synthesis agent that distills *investigation journeys* (not just outcomes) from prior sessions, including failed attempts — `complexity: medium | optional: true | prerequisite: "multiple prior sessions on same problem exist"`. Captures negative knowledge (what didn't work) which `knowledge-capture` currently omits.
- From `compound-knowledge:kw:compound`: **Deduplication check before write** — before saving a new learning, grep knowledge base for semantically similar entries; require explicit user approval to override — `complexity: low | optional: false | prerequisite: none`. Prevents duplicate drift in knowledge base.
- From `everything-claude-code:evolve`: **Structured evolution proposals** — analyze instinct set and suggest consolidations, splits, or promotions as structured diff proposals rather than silently rewriting — `complexity: medium | optional: true | prerequisite: "instinct set has >30 entries"`. Keeps the knowledge base navigable as it grows.
- From `gstack:retro` / `gstack:learn`: **Explicit prune trigger** — after any bulk-promote session, automatically surface candidates that have aged >30 days without promotion for review/delete — `complexity: low | optional: false | prerequisite: none`. ECC's `/prune` implements this; David's stack has no equivalent.
- From `appydave-plugins:skill-miner`: **JSONL transcript mining** — retrospective bulk scan of past sessions as an initialisation pass when starting the instinct system — `complexity: medium | optional: true | prerequisite: "has >10 JSONL sessions to mine"`. Good for bootstrapping; ongoing use is lower value once hook-based capture is running.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `ecc:continuous-learning-v2` | Hook-triggered auto-extraction, atomic instinct format, confidence scoring, project-local-first scoping | The specific stop-hook wiring (hook config is env-specific) |
| `ecc:evolve` + `ecc:promote` + `ecc:prune` | Full lifecycle: candidate → project-scoped → global, with prune for aged-out candidates | `instinct-export/import` (useful for backup but not core lifecycle) |
| `ecc:ck` | Per-project persistent memory layer concept | CK's specific file format (David uses MEMORY.md convention) |
| `ce-compound` | Dual-track schema (bug vs knowledge), dedup check before write | The full parallel-subagent orchestration (overkill for David's solo use) |
| `ce-compound-refresh` | Staleness review pattern | CE's specific docs/solutions/ path convention |
| `ce-session-historian` | Investigation-journey narration (negative knowledge capture) | Multi-session synthesis dependency |
| `kw:compound` | User-approval gate before write | kw's broader plan/work/brainstorm workflow |
| `appydave:knowledge-capture` | Existing user-facing entry point — preserve as-is, nest new mechanisms under it | — |
| `appydave:skill-miner` | JSONL bootstrap pass for initialisation | Ongoing use cadence |
| `gstack:retro` / `gstack:learn` | Prune-after-promote trigger | gstack's team-specific vocabulary |

## Draft SKILL.md frontmatter

```yaml
name: knowledge-capture
description: >
  Capture durable, reusable knowledge from the current session into Claude's memory files so
  it persists across sessions. Use when user says "capture knowledge", "save this pattern",
  "add to memory", "log this learning", "this is a recurring pattern", or at session end when
  a significant bug or design decision was resolved. Writes atomic instincts with confidence
  scores and runs dedup check before save. Also supports: "prune old learnings", "evolve
  instincts", "promote to global", "what have I learned about X".
argument-hint: "[--dual-track] [--prune] [--evolve] [--promote]"
allowed-tools: Read, Edit, Write, Bash(grep:*), Bash(find:*)
```

## Open questions for David

1. **Confidence threshold**: ECC uses `0.0–1.0` float scoring. David's current memory files use prose. Should confidence scoring replace or augment prose? (A simple `high/medium/low` label may be more ergonomic than float.)

2. **Dual-track vs single-track**: CE separates bug fixes from knowledge patterns in separate YAML tracks. David's MEMORY.md is single-file, free-form. Is dual-track worth the schema overhead, or is a single `type: bug-fix | pattern | convention | decision` tag in the instinct sufficient?

3. **Hook automation**: The `continuous-learning-v2` mechanism fires on the Claude Code `Stop` hook automatically. David's `knowledge-capture` is manual. Does David want the auto-extraction layer, or is manual preferred (less noise, more intentional)?
