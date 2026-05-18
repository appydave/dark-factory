---
distillation_id: system-comprehension-intent-routing
stage: system-comprehension
intent: "Route an agent's query to the right context source — brain, app, or assembled file payload — based on what the user actually needs"
created: 2026-05-17
status: draft
source_artifacts:
  - agent-skills-osmani:skill:context-engineering
  - gbrain:skill:functional-area-resolver
  - appydave-plugins:skill:brain-query
  - appydave-plugins:skill:app-query
  - appydave-plugins:skill:llm-context
winner_mechanism: appydave-plugins:skill:brain-query + app-query + llm-context (David's existing 3-skill chain)
---

# Unified Skill: Intent-Routing Discovery (context-engineering upgrade)

**Purpose**: Three-skill chain that routes any "I need to understand X" request to the right context source: brain files (curated knowledge), app files (codebase), or assembled LLM payload (packaged context). Osmani's context-engineering provides the framing; gbrain's functional-area-resolver provides the compression mechanism for large routing tables.

## Intent

Given "find brain about X" / "get files from Y app" / "assemble context for Z" — route to the correct tool in David's discovery chain without the user knowing the underlying mechanics. The meta-skill: curate what context an agent receives, when it receives it, and how it's structured.

## Winner's Mechanism

David's existing 3-skill chain (`brain-query → app-query → llm-context`) is the winner. Each skill is already installed and has a clear job:

- `brain-query` — **find** brain files by topic (discovery)
- `app-query` — **fetch** app codebase files by category using `context.globs.json` (structured retrieval)
- `llm-context` — **assemble** found file paths into an LLM-ready payload (packaging)

The chain is: find → fetch → assemble. Each step is independent and composable.

Osmani's `context-engineering` provides the **framing** for why this chain matters: only `name` + `description` hit context at session start under lazy loading. Every byte in the description is paid at every boot. The chain's job is to route efficiently — invoke only the skill that matches the exact grain of "need context."

## Existing-skill nesting

All three skills exist. This distillation documents the canonical routing chain and proposes one upgrade: gbrain's `functional-area-resolver` mechanism as a compression technique for David's routing tables.

- **Existing mechanism**: Three separate skills, each with trigger phrases. User (or orchestrating agent) invokes the right one manually.
- **functional-area-resolver grain**: Compresses per-skill routing tables by grouping into functional areas with dispatcher clauses. A/B-tested: dispatcher outperforms naive pipe-table compression.
- **Nesting rule**: `functional-area-resolver` is a skill-authoring technique, not a runtime skill. Apply it when writing the `description` field of any routing skill — groups related trigger phrases into functional areas ("For brain discovery: [...]. For app file retrieval: [...]. For context assembly: [...]") rather than listing every phrase individually. This reduces description token cost while improving routing accuracy.

## Non-overlapping ideas folded in

- From `agent-skills-osmani:skill:context-engineering`: **session-start vs activation distinction** — `complexity: low | optional: false | prerequisite: none`. Osmani explicitly documents the two-tier loading model: description fires at session start (always), body fires on activation (only if routed). The routing chain should exploit this — descriptions are the routing program, bodies are the execution program. Currently David's three skill descriptions are detailed but could be tighter.

- From `gbrain:skill:functional-area-resolver`: **dispatcher-clause compression** — `complexity: low | optional: true | prerequisite: routing description has 8+ trigger phrases`. gbrain's resolver converts granular skill-per-row tables into functional-area dispatchers: each area lists sub-skills in a `(dispatcher for: ...)` clause. A/B evaluated at gbrain — dispatcher outperforms naive compression. Apply to `brain-query` description (currently 18 trigger phrases in a flat list) to reduce token cost while preserving routing accuracy. `complexity: low | optional: true | prerequisite: "brain-query description has grown beyond 15 trigger phrases"`.

- From `agent-skills-osmani:skill:context-engineering`: **context degradation detection** — `complexity: medium | optional: true | prerequisite: session is long-running`. Osmani's skill also fires "when agent output quality degrades." This implies a mechanism for detecting context window pollution. Currently David has no explicit mechanism for this. Consider: a lightweight hook that triggers `brain-query` re-orientation when a session reaches a certain depth without a knowledge-anchor.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave-plugins:skill:brain-query` | Canonical brain-discovery tool; find-then-pipe pattern | No changes — upgrade only |
| `appydave-plugins:skill:app-query` | Canonical app-file-retrieval tool; depends on context.globs.json | No changes — upgrade only |
| `appydave-plugins:skill:llm-context` | Canonical assembler; ASSEMBLER not SEARCH framing | No changes — upgrade only |
| `agent-skills-osmani:skill:context-engineering` | Two-tier loading model framing; context degradation trigger | Full skill body (David's 3-skill chain supersedes it) |
| `gbrain:skill:functional-area-resolver` | Dispatcher-clause compression technique for description authoring | gbrain infrastructure tools (search, get_page, etc.) — David uses CLI tools instead |

## Draft SKILL.md frontmatter

No new skill needed — the 3-skill chain is already installed. The upgrade is to the descriptions:

```yaml
# Suggested upgrade to brain-query description (functional-area-resolver applied):
name: brain-query
description: >
  Search and discover brain files using the query_brain CLI.
  For brain discovery: "search brains for X", "find brain about X", "which brains cover X",
  "brain files for X", "what's in the X brain", "active brains", "brains tagged X",
  "brains in category X", "load brain X", "what brains do we have", "find knowledge about X".
  (dispatcher for brain-query → llm-context assembly pipeline)
  Different from focus (orientation) and brain-librarian (curation).
allowed-tools: "Bash(query_brain:*)"
```

```yaml
# context-engineering as a meta-description-quality skill (Osmani framing)
name: context-engineering
description: >
  Curate what context an agent receives, when it receives it, and how it's structured to
  maximize output quality. Use when starting a new project session, when agent output quality
  degrades mid-session, when switching between tasks, or when optimizing skill descriptions
  for routing accuracy. Meta-skill — governs how other skills describe themselves.
allowed-tools: "Read, Edit"
```

## Open questions for David

1. **Description upgrade priority**: `brain-query` has 18 trigger phrases in a flat list (high token cost at session start). Should gbrain's dispatcher-clause compression be applied to `brain-query` now as a quick win?

2. **Context degradation hook**: Osmani fires `context-engineering` on output quality degradation. Is there a session-depth trigger in `settings.json` hooks that could surface `brain-query` re-orientation automatically, or is this a conversation-pattern the user manually recognizes?

3. **`source-driven-development` routing**: Osmani's `source-driven-development` skill also landed in this slice (grounds implementation in official docs). Is it part of this cluster (routing to external docs as context source) or belongs in the code-implementation cluster? Currently tagged as both `code-implementation` and `system-comprehension`.
