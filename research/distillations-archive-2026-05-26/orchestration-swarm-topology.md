---
distillation_id: orchestration-swarm-topology
stage: orchestration
intent: "Name and invoke the right coordination topology for a multi-agent task — hierarchical, mesh, byzantine, raft, gossip, quorum, queen"
created: 2026-05-16
status: draft
source_artifacts:
  - ruflo:skill:agent-hierarchical-coordinator
  - ruflo:skill:agent-mesh-coordinator
  - ruflo:skill:agent-byzantine-coordinator
  - ruflo:skill:agent-raft-manager
  - ruflo:skill:agent-queen-coordinator
  - ruflo:skill:agent-gossip-coordinator
  - ruflo:skill:agent-quorum-manager
  - ruflo:skill:agent-consensus-coordinator
  - ruflo:skill:agent-adaptive-coordinator
  - ruflo:skill:agent-sync-coordinator
  - ruflo:skill:agent-collective-intelligence-coordinator
  - ruflo:skill:hive-mind
  - ruflo:skill:hive-mind-advanced
  - ruflo:agent:coordinator
  - ruflo:skill:agent-coordinator-swarm-init
  - ruflo:skill:agent-sparc-coordinator
  - ruflo:skill:agent-v3-queen-coordinator
winner_mechanism: ruflo:skill:agent-hierarchical-coordinator
---

# Unified Skill: swarm-topology

**Purpose**: Name and invoke a named coordination topology for a multi-agent task. Topology is the architectural decision — one coordinator selects and initialises the right structure based on task shape.

**For Agents**: Use when David says "which topology", "hierarchical swarm", "mesh agents", "use quorum", "what coordinator do I need", or is designing a new multi-agent workflow and needs the coordination model picked before implementation.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Select and initialise the right named coordination topology for a multi-agent task — a single skill that describes each topology, when to use it, and boots the coordinator.

## Winner's Mechanism

`ruflo:skill:agent-hierarchical-coordinator` wins because Ruflo is the only repo that names topologies explicitly AND ships separate coordinator skills per topology. The naming is the mechanism — giving topologies stable vocabulary (hierarchical / mesh / byzantine / raft / gossip / quorum / queen) makes coordination choices legible and discussable. David's existing fan-out skills (`doc-review`, `delivery-review`) are implicitly Parallel Panel topology — this cluster supplies the vocabulary to name that explicitly and extend it.

## Non-overlapping ideas folded in

- From `ruflo:skill:hive-mind-advanced`: Byzantine fault-tolerant consensus + queen-led collective — queen topology adds a persistent coordinator role that survives agent churn, different from pure hierarchy.
- From `ruflo:skill:agent-adaptive-coordinator`: Dynamic topology switching at runtime based on observed failure/load — adds a meta-layer: don't just pick once, let the coordinator evolve the structure.
- From `ruflo:skill:agent-sparc-coordinator`: SPARC methodology phases (Specification, Pseudocode, Architecture, Refinement, Completion) mapped to coordinator handoffs — a named sequenced topology for SDLC workflows.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ruflo:agent-hierarchical-coordinator | Topology vocabulary: orchestrator → specialists → workers | Ruflo-specific `$agent-*` invocation syntax |
| ruflo:agent-mesh-coordinator | Peer-to-peer coordination with no single orchestrator — good for resilience | Ruflo daemon dependency |
| ruflo:agent-byzantine-coordinator | Fault tolerance model — minority can fail, consensus still holds | Crypto-signing machinery |
| ruflo:agent-raft-manager | Leader election + log replication mental model | Raft protocol specifics |
| ruflo:agent-queen-coordinator | Queen = persistent long-horizon coordinator; workers are ephemeral | Flow Nexus platform dep |
| ruflo:agent-gossip-coordinator | Gossip = eventual consistency, no central broker | Network topology assumptions |
| ruflo:agent-quorum-manager | Quorum = decisions require N-of-M agreement | Voting mechanism implementation |
| ruflo:hive-mind | Byzantine fault-tolerant + consensus in one skill | Over-engineering for small swarms |
| ruflo:agent-adaptive-coordinator | Runtime topology evolution | Complexity overhead |

## Draft SKILL.md frontmatter

```yaml
name: swarm-topology
description: >
  Name and initialise the right multi-agent coordination topology for a task.
  Covers hierarchical (orchestrator→specialists→workers), mesh (peer-to-peer resilient),
  queen (persistent long-horizon coordinator), raft (leader-election), quorum (N-of-M consensus),
  gossip (eventual consistency), and byzantine (fault-tolerant with minority failures).
  Use when: "which topology", "hierarchical swarm", "mesh agents", "set up quorum",
  "what coordinator do I need", "design the coordination", "how should agents coordinate".
```

## Topology quick-reference (for skill body)

| Topology | Shape | Best for |
|----------|-------|----------|
| **Hierarchical** | Orchestrator → Specialists → Workers | Review fan-outs, SDLC pipelines, known task decomposition |
| **Mesh** | Peers coordinate directly | Resilient exploration, no single point of failure |
| **Queen** | Persistent queen + ephemeral workers | Long-horizon campaigns, multi-session continuity |
| **Raft** | Leader election + followers | Distributed state with one authoritative writer |
| **Quorum** | N-of-M agreement before proceeding | High-stakes decisions requiring consensus |
| **Gossip** | Broadcast + propagation, no broker | Eventual-consistency memory sync across agents |
| **Byzantine** | Tolerates up to f faulty agents (N≥3f+1) | Untrusted or unreliable worker pool |

## Open questions for David

- Should this be a **design advisor** (recommends topology) or a **launcher** (boots the coordinator)? Ruflo conflates both — David might prefer them separate.
- Is "queen" topology useful for his solo/small-team context, or is it over-engineered for now?
- Does he want the topology vocabulary promoted to the `prompt-patterns` brain as a formal entry under `orchestration-topology`?
