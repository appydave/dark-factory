---
distillation_id: documentation-doc-write
stage: system-comprehension
intent: "Generate or update project documentation from scratch — README, CLAUDE.md, architecture docs, API docs, across up to 10 doc types"
created: 2026-05-17
status: draft
source_artifacts:
  - gsd:command:docs-update
  - gsd:agent:gsd-doc-writer
  - gstack:skill:document-generate
  - everything-claude-code:agent:doc-updater
  - ruflo:agent:ruflo-docs:docs-writer
  - bmad-method:skill:bmad-agent-tech-writer
  - bmad-method:skill:bmad-document-project
  - bmad-method:skill:bmad-index-docs
  - bmad-method:skill:bmad-shard-doc
  - appydave-plugins:skill:system-context
winner_mechanism: gsd:command:docs-update
---

# Unified Skill: doc-write

**Purpose**: Generate or update project documentation files — parallel sub-agents per doc type, with factual verification pass before accepting output. Handles create, update, and brownfield (legacy project onboarding) modes.

**For Agents**: Use when user says "write the README", "generate docs for this project", "our docs are missing", "document this module", "create a CONTEXT.md", "onboard this legacy project for AI agents". Not for post-ship doc maintenance (that's `changelog-author`) or doc quality review (that's `doc-review`).

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Generate or update the full documentation set for a project — README, CLAUDE.md, CONTEXT.md, architecture docs, API docs, and indexes — using parallel agents per doc type with a verification pass to prevent hallucinated claims.

## Winner's Mechanism

`gsd:command:docs-update` is the winner because it has the most complete documentation generation architecture in the corpus:

- **Up to 9 doc types in parallel** — spawns `gsd-doc-writer` agents per type (README, CLAUDE.md, architecture, API, database, deployment, testing, changelogs, PRD)
- **Factual verification by default** — every generated doc passes through `gsd-doc-verifier` before acceptance, catching hallucinated commands and wrong import paths
- **Create + update modes** — `gsd-doc-writer` handles both from-scratch and update-in-place
- **Type routing** — not all doc types apply to all projects; the orchestrator routes to applicable types

The verification-by-default principle is the most important architectural decision. Without it, AI-generated docs routinely contain plausible-but-wrong command examples and dead import paths that are worse than having no docs at all.

`gstack:skill:document-generate` covers the same space with a simpler mechanism (single-agent, no verification). Useful as a fallback for one-off generation; not the right architecture for a full-project doc sweep.

`appydave-plugins:skill:system-context` is already in David's stack but narrowly scoped to CONTEXT.md generation. `doc-write` should subsume it — CONTEXT.md becomes one of the doc types.

## Existing-skill nesting

David has `system-context` (CONTEXT.md only). `doc-write` is a superset:

- **`system-context` grain**: per-repo CONTEXT.md, auto-regenerated when architecture changes
- **`doc-write` grain**: per-repo full documentation sweep, all applicable doc types
- **Nesting rule**: `doc-write --type=context` subsumes `system-context`. Keep `system-context` as a convenience alias for `doc-write --type=context` if the existing trigger phrases need to keep working. Don't break existing users of `system-context`.

## Non-overlapping ideas to fold in

- From `bmad-method:skill:bmad-document-project`: **brownfield onboarding mode** — document a legacy project that has no existing docs and where the code is the primary source of truth. Key: read the codebase first, infer architecture from structure, then generate — don't generate and verify, generate FROM the code — `complexity: medium | optional: true | prerequisite: "project has no existing documentation"`. Valuable for SupportSignal legacy analysis, client onboarding.

- From `bmad-method:skill:bmad-index-docs`: **index generation** — after writing docs, regenerate any `INDEX.md` files in the scope — `complexity: low | optional: false | prerequisite: none`. A natural post-generation step that maintains navigation.

- From `bmad-method:skill:bmad-shard-doc`: **large-doc splitting** — when a generated doc exceeds a token threshold, auto-split at level-2 headings into separate files with a parent index — `complexity: low | optional: true | prerequisite: "generated doc exceeds ~2000 lines"`. Prevents documentation monoliths.

- From `everything-claude-code:agent:doc-updater`: **codemap maintenance** — maintain a `CODEMAP.md` (file-by-file purpose summary) alongside the documentation — `complexity: medium | optional: true | prerequisite: none`. Especially valuable for AI agents navigating the codebase. Different from CONTEXT.md (architecture overview) — codemap is per-file, CONTEXT.md is per-system.

- From `agent-skills-osmani:skill:documentation-and-adrs` (folded from the `readme-adr-author` overlap): **"write why, not what"** as the core voice principle for generated docs — generated doc content must prefer rationale over code restatement — `complexity: low | optional: false | prerequisite: none`.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `gsd:docs-update` | Parallel-per-type orchestration, verification-by-default, create+update modes, 9 doc types | GSD-specific wave/state machinery |
| `gsd:gsd-doc-writer` | Per-type content generation model | GSD task-file dependencies |
| `gsd:gsd-doc-verifier` | Factual verification step | GSD-specific output format |
| `gstack:document-generate` | Single-agent fallback mode | No verification step (set aside — verification is non-negotiable) |
| `ecc:doc-updater` | Codemap maintenance concept | ECC-specific prompt-engineering-heavy approach |
| `bmad:bmad-document-project` | Brownfield onboarding mode | BMAD persona wrapper |
| `bmad:bmad-index-docs` | Post-generation index regeneration | BMAD-specific index format |
| `bmad:bmad-shard-doc` | Large-doc splitting | BMAD H2 splitting is overly prescriptive; adopt the concept, not the implementation |
| `ruflo:docs-writer` | Nothing unique — generic doc writer with no verification | Full artifact set aside |
| `appydave:system-context` | CONTEXT.md as one doc type | Narrow single-type scope (subsumed) |
| `bmad:bmad-agent-tech-writer` | Imperative voice + active-sentence discipline | BMAD persona/persona-wrapper |

## Draft SKILL.md frontmatter

```yaml
name: doc-write
description: "Generate or update project documentation — README, CLAUDE.md, CONTEXT.md, architecture, API docs, index files. Parallel agents per doc type with factual verification. Use when: 'write the docs', 'generate docs', 'our README is missing', 'document this module', 'create a CONTEXT.md', 'onboard this project for AI agents', 'docs are missing'."
argument-hint: "[path] [--type=readme|context|architecture|api|all] [--mode=create|update|brownfield]"
allowed-tools: Bash(find *), Bash(grep *), Read, Write, Edit
```

## Open questions for David

1. **`system-context` fate**: Should `system-context` become a thin alias for `doc-write --type=context`, or remain a standalone skill (since it has its own specific CONTEXT.md format)? Keeping it standalone avoids breaking existing trigger phrases but creates slight duplication.

2. **Verification cost**: Factual verification per doc type adds significant time to a full sweep. For brownfield onboarding (where docs don't exist yet), verification is harder (less codebase to cross-reference). Should verification be `--verify=on|off|brownfield-skip`?

3. **Doc type list**: GSD has 9. BMAD covers different angles. What's the right canonical list for David's projects? Suggestion: README, CLAUDE.md, CONTEXT.md, CODEMAP.md, architecture.md, api.md, testing.md, deployment.md, changelog.md. Nine types, aligned to what David actually maintains.
