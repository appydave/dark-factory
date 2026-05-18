---
distillation_id: knowledge-capture-session-handover
stage: knowledge-capture
intent: "Preserve session state so a new Claude session can resume without re-reading the conversation"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:capture-context
  - appydave-plugins:skill:session-checkpoint
  - appydave-plugins:skill:near-compaction
  - appydave-plugins:skill:handover-pattern
  - everything-claude-code:skill:save-session
  - gsd:command:gsd:pause-work
  - gsd:command:gsd:resume-work
  - gsd:command:gsd:session-report
  - gsd:command:gsd:thread
  - gsd:command:gsd:note
  - bmad-method:skill:bmad-retrospective
winner_mechanism: appydave-plugins:skill:capture-context
---

# Unified Skill: Session Handover

## Intent

Produce a compact, structured handover document from the current session so a new Claude session can resume work immediately — without re-reading the conversation or rediscovering context.

## Winner's Mechanism

David's `capture-context` is the winner: it already has the right grammar (STOP directive, Working On, Current State, Key Decisions with rationale, Active Files, What We Ruled Out, Gotchas, Options, How to Resume) and the right philosophy — gotchas and ruled-out approaches are more valuable than what-was-done. The output is paste-in text by default (not a written file), which keeps handovers ephemeral and prevents stale documents from poisoning future sessions. `session-checkpoint` and `near-compaction` already exist as complementary narrow tools.

The cluster confirms David's three-skill family is the strongest in the corpus for this problem. The gap is not the mechanism — it's two missing components: (1) a cross-session thread model for work that spans many sessions (GSD's `gsd:thread`), and (2) a forward-looking idea capture with trigger conditions (GSD's `gsd:plant-seed`).

## Existing-skill nesting (upgrading existing skills)

- **Existing mechanism (`capture-context`)**: Full session handover — decisions + rationale + ruled-out + gotchas + active files. Manual invocation. Ephemeral paste-in output.
- **Existing mechanism (`session-checkpoint`)**: Narrow task-progress marker — which step to start on. Complementary, not overlapping.
- **Existing mechanism (`near-compaction`)**: Orchestrator that fires `capture-context` + `session-checkpoint` + `knowledge-capture` together when context window fills. Compaction trigger, not handover.
- **New mechanisms' grain**: Thread (cross-session, project-lived) and seed (forward-looking idea with trigger condition). Both are persistent — they write files that outlive a session.
- **Nesting rule**: `capture-context` remains the per-session handover. `near-compaction` remains the compaction orchestrator. A new `session-thread` pattern adds the persistent cross-session layer that `capture-context` currently can't provide (ephemeral by design). These compose — `near-compaction` can call `session-thread` to persist threads that shouldn't go in the ephemeral handover.

## Non-overlapping ideas folded in

- From `gsd:gsd:thread`: **Cross-session context threads** — named, file-backed threads for work that spans many sessions but doesn't belong to a specific task (e.g., "architecture decisions for v2", "open questions about Kybernesis") — `complexity: low | optional: true | prerequisite: "project spans >3 sessions"`. Fills the gap between ephemeral handovers and durable memory: threads persist, but they're manually curated, not auto-accumulated.
- From `gsd:gsd:plant-seed`: **Trigger-condition idea capture** — capture a forward-looking idea with a condition that surfaces it automatically at the right milestone ("when we hit auth, revisit this security decision") — `complexity: medium | optional: true | prerequisite: "multi-milestone project"`. Currently David has no mechanism to tie deferred ideas to future project states.
- From `gsd:gsd:session-report`: **Token-usage estimate in handover** — include estimated token spend alongside work summary — `complexity: low | optional: true | prerequisite: "none"`. Low signal most days, but useful for flagging runaway sessions to avoid.
- From `everything-claude-code:save-session`: **Dated file output** — `~/.claude/session-data/[topic]-[date].md` as the save convention — `complexity: low | optional: false | prerequisite: none`. ECC's path convention is cleaner than ad-hoc filenames; David's `capture-context` already suggests `~/.claude/sessions/` but doesn't enforce the naming pattern.
- From `bmad-method:bmad-retrospective`: **What-worked / what-didn't split** — explicit two-column retrospective as an optional closing section — `complexity: low | optional: true | prerequisite: "multi-day project or sprint boundary"`. Useful at sprint close; not needed for daily handovers.
- From `gsd:gsd:note`: **Zero-friction timestamped note** — quick `gsd:note <text>` capture for observations that don't warrant a full handover, with `promote-to-todo` subcommand — `complexity: low | optional: true | prerequisite: none"`. Fills the gap between "full handover" and "throw it away".

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave:capture-context` | Full handover grammar, ephemeral-by-default output, gotchas-first philosophy | — (it's the winner) |
| `appydave:session-checkpoint` | Narrow task-progress marker — keep separate | — |
| `appydave:near-compaction` | Compaction orchestrator — keep separate | — |
| `appydave:handover-pattern` | PO↔Developer handover format | Too domain-specific for general handover |
| `gsd:pause-work` | `.continue-here.md` file convention for in-project state | Writing into project dir (anti-pattern per David's rules) |
| `gsd:resume-work` | Context-restore + route-to-next-workflow pattern | GSD's full project-state coupling |
| `gsd:thread` | Named persistent cross-session threads | GSD's project-phase coupling |
| `gsd:plant-seed` | Trigger-condition idea capture | GSD's milestone-linked surfacing automation |
| `gsd:session-report` | Token-usage estimate | SESSION_REPORT.md written to project (anti-pattern) |
| `ecc:save-session` | Dated file naming convention | Specific file path (`~/.claude/session-data/`) |
| `bmad:bmad-retrospective` | What-worked/what-didn't retrospective section | BMAD's sprint ritual framing |

## Draft SKILL.md frontmatter

```yaml
name: capture-context
description: >
  Capture and summarize session context for continuity across Claude sessions. Use when user
  says "capture context", "save session context", "summarize this session", "create a context
  handover", "what should I tell the next session", "session summary", "capture what we've done",
  or "I'm starting a new session". Produces a compact, structured summary: decisions with rationale,
  active files, ruled-out approaches, and gotchas. Also handles: "save as thread", "plant a seed for
  later", "quick note", "token usage".
argument-hint: "[--quick] [--full] [--save] [--thread <name>] [--seed]"
allowed-tools: Read, Write
```

## Open questions for David

1. **Thread persistence location**: GSD writes `.continue-here.md` into the project directory (anti-pattern per your rules). ECC uses `~/.claude/session-data/`. Should threads live in `~/.claude/threads/[project-slug]/[thread-name].md` instead? Needs decision before building.

2. **Plant-seed surfacing**: GSD's `gsd:plant-seed` surfaces ideas at the "right milestone" by scanning seeds at session start. Is that automatic scan desired, or should seeds be manually queried? The auto-scan approach requires a session-start hook.

3. **Token reporting**: Is token-usage estimate in the handover useful to David? It adds noise to daily handovers but could be valuable for cost awareness across Kybernesis/SupportSignal work.
