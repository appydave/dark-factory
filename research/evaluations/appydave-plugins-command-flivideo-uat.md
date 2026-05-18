---
artifact_id: appydave-plugins:command:flivideo:uat
repo: appydave-plugins
artifact_type: command
cluster_facet: [verification-validation]
phase_fit: [5, 6]
evaluated_at: 2026-05-17
---

# Eval: uat (flivideo command)

**Intent**: User acceptance testing command for FliVideo that runs as a subagent, loading backlog context, executing acceptance criteria tests, and producing a structured pass/fail verdict.

## Scores
- **quality_score**: 4 — Context-loading protocol (backlog + changelog + CLAUDE.md on every session start), subagent invocation pattern, structured UAT file template (FR-number based), smoke vs full UAT modes, auto vs manual test classification, and session summary output format. Well-designed for autonomous UAT runs.
- **adoption_fit_final**: strong — This is David's own FliVideo tool; it's already in use. The subagent-for-UAT pattern and the FR-number-linked file convention are reusable patterns for any product.
- **inspiration_value**: mid
- **uniqueness_refined**: uncommon — The "First Steps (Every Session)" context-loading protocol before any test action is a clean discipline. Smoke vs Full UAT mode branching, and the explicit auto (Claude executes) vs manual (human verifies) classification per test step, are thoughtful distinctions.
- **composability**: calls-others — Invokes as subagent; output feeds `/po` (backlog updates) and `/dev` (failure details for fixes).
- **description_craft_refined**: summary — Single summary sentence without trigger phrase list.

## Mineable phrasing
> "Test like a user — focus on what users see and do. Stick to acceptance criteria — don't invent requirements."

## Notes
The auto/manual test classification within a single UAT file (some steps Claude can execute via curl/CLI, others require human UI interaction) is a practical hybrid model for agentic UAT. The related agents section (`/po` and `/dev`) sketches a three-agent loop (UAT → backlog owner → dev) that models a lightweight product delivery chain. Strong pattern for a unified `uat` skill across David's product suite.
