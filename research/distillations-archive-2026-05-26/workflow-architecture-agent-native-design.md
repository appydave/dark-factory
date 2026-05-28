---
distillation_id: workflow-architecture-agent-native-design
stage: workflow-architecture
intent: "Design an agent-native application — where features are prompt-defined outcomes, not functions in code — applying the five agent-native principles from spec through architecture"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-agent-native-architecture
  - everything-claude-code:skill:agentic-os
  - everything-claude-code:skill:mcp-server-patterns
  - bmad-method:skill:bmad-create-architecture
  - bmad-method:skill:bmad-agent-architect
  - appydave-plugins:skill:agentic-capability
  - ruflo:skill:flow-nexus-swarm
winner_mechanism: compound-engineering:skill:ce-agent-native-architecture
---

# Unified Skill: agent-native-design

**Purpose**: Architecture design skill for applications where agents are first-class citizens — features are outcomes achieved by agents with tools, not functions written in code. Covers: tool design, action parity, system prompt architecture, context injection, self-modification.

**For Agents**: Use when David is designing a new product or feature where agents drive the primary behavior — not when adding AI to an existing code-first app. Trigger phrases: "agent-native app", "build this around agents", "design for agents", "features as prompts", "AI-first architecture", "MCP server for X", "agents as the product", "kybernesis architecture", "this should be autonomous".

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Agent-native design is a distinct architectural paradigm: the application's features are *prompt-defined outcomes*, not code paths. To change behavior, you edit prose, not functions. The architectural decisions are different from traditional software: tool granularity (atomic primitives → domain tools), action parity (agents can do everything the UI can), context injection (runtime state → agent prompt), and emergent capability (the agent does things you didn't design for).

This is the design-time skill. `bmad-story-lifecycle` and `plan-executor` handle the build-time execution.

## Winner's Mechanism

`compound-engineering:ce-agent-native-architecture` wins for **the most comprehensive articulation of agent-native principles in the corpus**. Five principles (Parity, Granularity, Composability, Emergent Capability, Improvement Over Time) + 14 detailed reference files covering tool design, action parity, context injection, self-modification, product implications, and mobile patterns. It is organized as a progressive disclosure skill: intake menu → routing → reference files. The intake menu alone (14 numbered design topics) is a complete checklist for an agent-native architecture review.

No other artifact in the corpus comes close for this specific design mode. Most architecture skills in the corpus assume code-first architecture and add AI as a layer. CE's skill assumes agents are the product, not the tooling.

`agentic-os` (ECC) contributes the **persistent multi-agent operating system** extension — when the agent-native app itself needs to be always-on, multi-agent, with session persistence and cross-session memory. This is the `agentic-os` territory: not just "agents do features" but "the system is an OS where agents are processes."

`mcp-server-patterns` (ECC) contributes the **MCP tool design patterns** specifically — Node/TypeScript SDK, Zod validation, stdio vs Streamable HTTP transport. When the agent-native app needs to expose its capabilities as MCP tools (which is the recommended primitive layer).

## Non-overlapping ideas folded in

- From `agentic-os` (ECC): **Persistent agent OS design** — session persistence, cross-session memory, multi-agent coordination as OS-level primitives — `complexity: high | optional: true | prerequisite: "system needs always-on, multi-agent coordination with persistent state"`. For Kybernesis (where the product is an agent coordination layer) this is directly relevant.
- From `mcp-server-patterns` (ECC): **MCP as the tool primitive layer** — Zod-validated tools, proper transport selection, resource + prompt patterns — `complexity: medium | optional: true | prerequisite: "agent-native app exposes tools to other agents or external clients"`. The canonical tool layer for agent-native apps in the Claude ecosystem.
- From `bmad-create-architecture` (bmad): **Architecture document as a living artifact** — produces a structured Architecture Decision Document that governs all subsequent implementation decisions — `complexity: medium | optional: false | prerequisite: none"`. The output of the design session isn't just notes; it's a governed document that feeds the BMAD story lifecycle.
- From `appydave-plugins:agentic-capability`: **Capability description as the discovery contract** — `complexity: low | optional: false | prerequisite: none`. Each agent-native feature must have a capability description (what it can do, when to use it) before the implementation. This is the description-as-trigger-API principle applied to agent-native design.
- From `ruflo:flow-nexus-swarm`: **Cloud-native event-driven architecture layer** — `complexity: high | optional: true | prerequisite: "app needs cloud deployment + event-driven triggers beyond local Claude Code"`. Ruflo's Flow Nexus pattern (webhook triggers, cloud swarm deployment) is the production-grade extension of local agent-native design. Relevant when Kybernesis moves to multi-tenant.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ce-agent-native-architecture (CE) | Five principles, 14-topic intake menu, tool design patterns, action parity, self-modification, progressive disclosure structure | CE-specific install paths and references |
| agentic-os (ECC) | Persistent multi-agent OS design patterns | ECC-specific agent catalogue |
| mcp-server-patterns (ECC) | MCP tool design primitives, transport selection | ECC-specific SDK version pinning |
| bmad-create-architecture (bmad) | Architecture document as living governed artifact | BMAD ceremony and persona system |
| agentic-capability (appydave) | Capability description as discovery contract | AppyDave-specific output format |
| flow-nexus-swarm (ruflo) | Cloud-native event-driven extension | Ruflo daemon dependency |

## Draft SKILL.md frontmatter

```yaml
name: agent-native-design
description: >
  Design applications where agents are first-class citizens and features are
  prompt-defined outcomes, not code functions. Covers: tool granularity,
  action parity, context injection, self-modification, emergent capability.
  Use when: "agent-native app", "design for agents", "features as prompts",
  "AI-first architecture", "MCP server for X", "agents as the product",
  "this should be autonomous", or designing Kybernesis components.
argument-hint: "[product-description | existing-codebase-path]"
allowed-tools: "Read, Bash(cat:*), Bash(find:*), Write"
```

## Open questions for David

1. **Kybernesis alignment**: CE's `ce-agent-native-architecture` describes exactly what Kybernesis is building. Should this skill be adopted as-is for Kybernesis design sessions, or adapted into a Kybernesis-specific architecture skill with the five principles baked in as context?

2. **MCP-first vs skill-first**: CE's architecture uses MCP tools as the primitive layer. David's current stack uses Claude Code skills. For new agent-native apps, should the default be MCP tools (portable, standard) or Claude Code skills (already in place, lower overhead)? Or detect and route based on whether the app needs multi-harness or Claude-only?

3. **Architecture document location**: BMAD produces architecture docs to `_bmad-output/`. For non-BMAD agent-native design sessions, where should the architecture document live? `docs/architecture/` is the common default but may conflict with BMAD projects.
