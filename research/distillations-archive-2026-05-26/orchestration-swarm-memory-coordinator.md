---
distillation_id: orchestration-swarm-memory-coordinator
stage: orchestration
intent: "Share state and learnings across agents in a running swarm — the memory bus layer distinct from David's personal brain knowledge system"
created: 2026-05-16
status: draft
source_artifacts:
  - ruflo:skill:agent-swarm-memory-manager
  - ruflo:skill:agent-memory-coordinator
  - ruflo:skill:AgentDB Advanced Features
  - ruflo:skill:agent-coordination
  - ruflo:skill:agentic-jujutsu
winner_mechanism: ruflo:skill:agent-swarm-memory-manager
---

# Unified Skill: swarm-memory-coordinator

**Purpose**: Share state, findings, and learnings between agents running in the same swarm — distinct from David's personal second-brain knowledge system and distinct from long-term instinct promotion.

**For Agents**: Use when designing a multi-agent system where agents need to share intermediate results without full context merging — swarm-internal state bus, not knowledge archival.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Provide a shared state bus for a running agent swarm: writers post structured findings, readers query without re-running work, coordinator deduplicates and routes — all without each agent needing the full swarm context.

## Winner's Mechanism

`ruflo:skill:agent-swarm-memory-manager` wins as the most complete Ruflo implementation of swarm-internal memory — manages shared state across swarm members using agentdb namespaces, with QUIC sync between nodes.

However, this is the **weakest cluster** in the orchestration slice — only 5 artifacts, all from Ruflo, all Ruflo-infrastructure-dependent. There is no David-stack equivalent. The closest is `compound-knowledge`'s `knowledge-folder-as-bus` pattern (git-tracked markdown + grep) — but that's a different cluster (knowledge-capture, not orchestration).

The honest assessment: David doesn't currently have a swarm-memory layer. This cluster surfaces the gap rather than providing a clear winner to adopt.

## Non-overlapping ideas folded in

- From `ruflo:skill:agent-coordination`: **Spawn + lifecycle + memory** in one skill — coordination and memory are coupled in Ruflo's design. Worth noting that David might want to couple them too (the lifecycle coordinator in `agent-lifecycle-coordinator` could carry the memory bus).
- From `ruflo:skill:agentic-jujutsu`: **Quantum-resistant, self-learning version control** for agent state — ReasoningBank as the state store. Interesting as a pattern (version-controlled agent memory), even if the implementation is Ruflo-specific.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| agent-swarm-memory-manager | Shared state bus concept, agentdb namespaces | Ruflo/QUIC infrastructure |
| agent-memory-coordinator | Memory as a coordinator role (separate concern) | Ruflo daemon |
| AgentDB Advanced Features | HNSW vector + multi-db + QUIC sync model | Heavy infrastructure |
| agent-coordination | Memory + lifecycle coupling | Ruflo-specific |
| agentic-jujutsu | Version-controlled agent state (ReasoningBank) | Quantum-resistant overhead |

## Draft SKILL.md frontmatter

```yaml
name: swarm-memory-coordinator
description: >
  Shared state bus for a running agent swarm — writers post findings, readers query
  without re-running work, coordinator deduplicates. Swarm-internal only; not
  David's second-brain knowledge system.
  Use when: "agents need to share results", "swarm state", "agent found X and next agent needs it",
  "avoid re-running work", "shared memory across agents".
```

## Open questions for David

- Is there a **simple implementation** of swarm memory that doesn't require Ruflo infrastructure? (E.g., a scratch markdown file per swarm run, each agent appends its findings, next agent reads it.) The `knowledge-folder-as-bus` pattern from compound-knowledge may be the right model.
- Should swarm memory be part of `agent-lifecycle-coordinator` (the coordinator owns the state bus) or always a separate skill?
- Is this cluster worth a real unified skill now, or is it better flagged as a **gap** for David to fill when he builds his first multi-agent swarm that needs shared state?
