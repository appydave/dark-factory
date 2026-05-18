---
distillation_id: knowledge-capture-memory-store-retrieve
stage: knowledge-capture
intent: "Persistent structured memory for agents — store, retrieve, and reason over cross-session facts via vector search, knowledge graphs, or key-value stores"
created: 2026-05-17
status: draft
source_artifacts:
  - ruflo:skill:agent-memory-coordinator
  - ruflo:skill:agent-v3-memory-specialist
  - ruflo:skill:memory-management
  - ruflo:skill:memory-specialist
  - ruflo:skill:agentdb
  - ruflo:skill:agentdb-specialist
  - ruflo:skill:AgentDB Advanced Features
  - ruflo:skill:AgentDB Learning Plugins
  - ruflo:skill:AgentDB Memory Patterns
  - ruflo:skill:AgentDB Performance Optimization
  - ruflo:skill:ReasoningBank Intelligence
  - ruflo:skill:ReasoningBank with AgentDB
  - ruflo:skill:recall
  - ruflo:skill:ruflo-memory
  - ruflo:skill:vector
  - ruflo:skill:vector-engineer
  - ruflo:skill:embeddings
  - ruflo:skill:kg
  - ruflo:skill:neural
  - ruflo:skill:hive-mind-advanced
  - ruflo:skill:V3 Memory Unification
  - ruflo:skill:flow-nexus-neural
  - ruflo:skill:session-specialist
  - ruflo:skill:agent-swarm-memory-manager
  - everything-claude-code:skill:knowledge-ops
  - everything-claude-code:skill:ck
  - compound-knowledge:skill:knowledge-base-researcher
  - compound-knowledge:skill:past-work-researcher
winner_mechanism: everything-claude-code:skill:ck
---

# Unified Skill: Memory Store & Retrieve

## Intent

Provide agents with persistent per-project memory — store structured facts across sessions and retrieve them efficiently — without requiring infrastructure beyond the filesystem.

## Winner's Mechanism

ECC's `ck` (Context Knowledge) is the winner for David's stack: persistent per-project memory for Claude Code, zero-dep (filesystem only), already compatible with the Claude Code harness. It implements the right abstraction — structured memory that survives session boundaries — without requiring AgentDB, vector infrastructure, or a running daemon.

Ruflo dominates this sub-cluster (23 of 27 artifacts) but nearly all its implementations depend on AgentDB, neural training loops, HNSW vector indexing, or the ReasoningBank daemon — infrastructure David doesn't have and doesn't need for current work. The Ruflo vocabulary (ReasoningBank, AgentDB, vector-space memory, knowledge graphs) is worth understanding as a design language for future Kybernesis work, but is not adoption-ready for David's solo Claude Code setup.

**Assessment note**: This sub-cluster is the clearest infrastructure-gap cluster in the entire knowledge-capture pass. Ruflo has the most sophisticated memory architecture in the corpus. The right question isn't "adopt Ruflo's memory" — it's "what memory patterns can be implemented on top of markdown + grep + `ck` today, and which require infrastructure investment?"

## No infrastructure-compatible winner for full capability

There is no single winner for advanced memory operations. The honest assessment:

| Memory capability | Best pattern (zero-dep) | Ruflo equivalent (infra-required) |
|------------------|------------------------|---------------------------------|
| Per-project persistent memory | `ck` (ECC) — markdown + MEMORY.md | AgentDB with SQLite/vector |
| Cross-project retrieval | `knowledge-base-researcher` grep pattern | ReasoningBank cross-session retrieval |
| Knowledge graph | `kg` heuristic (markdown relations) | Full graph-navigator with entity extraction |
| Semantic search | None (not possible zero-dep) | HNSW vector index via `vector-engineer` |
| Swarm shared memory | `knowledge-folder-as-bus` pattern | `agent-swarm-memory-manager` |

## Non-overlapping ideas folded in

- From `ruflo:recall` + `ruflo:ruflo-memory`: **Structured retrieval protocol** — RETRIEVE → JUDGE → APPLY → REINFORCE cycle for memory access (not just grep) — `complexity: medium | optional: true | prerequisite: "memory base has >50 entries"`. Grep finds; the RJAR cycle evaluates relevance and applies confidence weighting before use. David's current retrieve is unstructured grep.
- From `compound-knowledge:knowledge-base-researcher`: **Tag-first retrieval** — grep by YAML tag before content search; group results as Directly Relevant / Tangentially Relevant / Background — `complexity: low | optional: false | prerequisite: none`. Low complexity, high signal-to-noise improvement. David's brain-query uses tag filtering but not the Directly/Tangential/Background result grouping.
- From `ruflo:V3 Memory Unification`: **Single-interface memory model** — unify multiple memory backends (file, key-value, vector, graph) behind a single `memory:store/retrieve/search` interface — `complexity: high | optional: true | prerequisite: "multiple memory backends in use"`. Future-proof design for when David adds vector or graph storage without breaking existing callers.
- From `everything-claude-code:knowledge-ops`: **Sync and retrieval across storage layers** — explicit multi-layer storage model: local files → project memory → global memory → external knowledge base — `complexity: medium | optional: true | prerequisite: "multiple storage layers active"`. Formalizes the storage hierarchy David implicitly uses (MEMORY.md → brain files → raw-intake) into an explicit model.
- From `ruflo:hive-mind-advanced`: **Consensus memory** — when multiple agents contribute to shared memory, require quorum agreement before writing a fact — `complexity: high | optional: true | prerequisite: "multi-agent swarm with shared memory"`. Not needed now; relevant for Kybernesis multi-agent deployments.

## Ruflo patterns worth preserving as vocabulary

The Ruflo memory architecture introduces vocabulary David should know even without adopting the infrastructure:

- **ReasoningBank**: Persistent reasoning traces — not just facts, but *why* a fact was established. Enables agents to explain their confidence.
- **AgentDB**: Structured agent-scoped key-value + vector store. The abstraction separates agent memory from shared project memory.
- **Neural context** (`neural-training`, `flow-nexus-neural`): Reinforcement-learning-style memory where retrieval frequency affects storage weight. The insight: not all facts decay at the same rate.
- **Knowledge graph** (`kg`, `graph-navigator`): Entities + relations as first-class nodes, not just bag-of-words. Enables "what connects X to Y?" queries that grep can't answer.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `ecc:ck` | Per-project persistent memory, zero-dep — the winner | CK's specific file format |
| `ce:knowledge-base-researcher` | Tag-first retrieval, result grouping | CE's docs/solutions/ path |
| `ce:past-work-researcher` | Past-work retrieval pattern | CE's plans/ path structure |
| `ruflo:recall` | RJAR retrieval cycle concept | AgentDB dependency |
| `ruflo:memory-management` | Memory lifecycle vocabulary | Ruflo daemon dependency |
| `ruflo:agentdb` / `agentdb-specialist` | AgentDB abstraction model (design vocabulary) | Full AgentDB implementation |
| `ruflo:kg` | Knowledge-graph concept (future design) | Graph infrastructure |
| `ruflo:vector` + `vector-engineer` | Vector search concept | HNSW/embedding infrastructure |
| `ruflo:hive-mind-advanced` | Consensus memory concept | Swarm infrastructure |
| `ruflo:ReasoningBank*` | Reasoning-trace persistence concept | ReasoningBank daemon |
| `ecc:knowledge-ops` | Multi-layer storage model | ECC's specific layer configuration |

## Draft SKILL.md frontmatter

```yaml
name: ck
description: >
  Persistent per-project memory for Claude Code. Use when user says: "remember this for
  this project", "store this fact", "what do we know about X in this project", "recall
  project context", "project memory", "what's stored in project memory", "save this
  to project context", "retrieve from memory". Zero-dep — reads/writes markdown in project
  memory directory.
argument-hint: "[store|retrieve|search|list] [<key>] [<value>]"
allowed-tools: Read, Write, Bash(grep:*)
```

## Open questions for David

1. **Vector search threshold**: Ruflo's memory architecture shows that tag+keyword retrieval misses ~30% of relevant entries (semantic overlap without lexical match). At what memory-base size does the absence of semantic search become a real problem for David? (Current estimate: >200 entries across all brains.)

2. **Graph vs flat memory**: `kg` and `graph-navigator` enable relationship queries ("what connects Kybernesis to Paperclip?") that grep can't answer. Is this a near-term need, or something to evaluate once Kybernesis has more architecture decisions captured?

3. **AgentDB evaluation**: Ruflo's AgentDB is the most complete agent-memory abstraction in the corpus. If Kybernesis is building an agent platform, should David evaluate AgentDB as a design reference before committing to a memory architecture for KyberBot agents?
