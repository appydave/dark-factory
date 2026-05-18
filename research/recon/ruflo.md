---
repo: ruflo
github: https://github.com/ruvnet/claude-flow
local_path: /Users/davidcruwys/dev/upstream/repos/ruflo
context_md: /Users/davidcruwys/dev/upstream/repos/ruflo/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Ruflo (upstream: claude-flow)

**Purpose**: Phase 1 reconnaissance — shape discovery only. No scoring, tagging, or catalog entries.

**For Agents**: Use this file before running `catalog:discover` on the ruflo repo. Answers what artifact types exist, where they live, naming conventions, and frontmatter shapes.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

**Maintainer**: ruvnet (Reuven Cohen)
**Version sampled**: 3.7.0-alpha.38
**AppyDave alias**: "Ruflo" (rebranded from claude-flow; three packages publish in lockstep: `@claude-flow/cli` + `claude-flow` + `ruflo`)

## Top-level layout

```
ruflo/
├── .agents/           # 134 agent skills (hidden — primary artifact store for Claude Code)
│   └── skills/        # one dir per skill (SKILL.md inside each)
├── plugins/           # 33 installable plugin bundles (marketplace-distributed)
│   ├── ruflo-core/    # agents/, commands/, skills/, hooks/, scripts/
│   ├── ruflo-agentdb/ # agents/, commands/, skills/
│   ├── ruflo-swarm/   # agents/, skills/ (monitor-stream, swarm-init)
│   ├── ruflo-federation/
│   └── ... (29 more)
├── v3/                # Actual monorepo source (pnpm workspace lives here)
│   ├── @claude-flow/  # Package family: cli, swarm, memory, hooks, codex, security, guidance, embeddings, testing
│   ├── agents/        # 5 core agent yamls (coder, architect, tester, reviewer, security-architect)
│   ├── mcp/tools/     # 13 TypeScript MCP tool modules (agent, config, federation, hooks, memory, session, sona, swarm, system, task, worker, v2-compat)
│   ├── plugins/       # 16 v3 plugin packages (agentic-qe, cognitive-kernel, gastown-bridge, prime-radiant, etc.)
│   ├── src/           # DDD-structured source (agent-lifecycle, coordination, infrastructure, memory, task-execution)
│   ├── implementation/# ADRs, architecture docs, hook plans, swarm-plans
│   └── docs/          # ADRs, benchmarks, DDD domain docs
├── ruflo/             # 100 KB stub wrapper — execs into @claude-flow/cli
├── verification/      # Signed witness manifest + history (macOS/linux/windows)
│   └── inventory.json # Canonical artifact counts: 305 MCP tools, 49 CLI commands, 32 plugins, 44 agents
├── .context/          # CONTEXT.md (~37 KB synthesised snapshot, generated 2026-05-12)
│   └── CONTEXT.md
├── bin/               # cli.js, npx-repair.js, npx-safe-launch.js
├── scripts/           # 18 audit/fix scripts (audit-cli-mcp-tools.mjs, regen-witness.mjs, etc.)
├── tests/             # Test suite
├── .claude-plugin/    # plugin.json + marketplace.json (Claude Code plugin manifest)
├── agentdb.rvf        # AgentDB binary (SQLite/HNSW vector store — runtime artifact)
├── CLAUDE.md          # Claude Code harness identity + usage contract
├── AGENTS.md          # Cross-harness agent contract (100 lines on "MCP + Task in same message")
└── README.md
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Agent Skills (.agents) | `.agents/skills/` | 134 | `kebab-case` dir, `SKILL.md` inside | Yes — YAML (`name`, `description`, optional `version`/`tags`/`category`) | `hive-mind/SKILL.md`, `memory-management/SKILL.md` |
| Plugin Skills | `plugins/*/skills/` | ~8 per plugin | `kebab-case` dir, `SKILL.md` inside | Yes — minimal YAML (`name`, `description`, `argument-hint`, `allowed-tools`) | `ruflo-core/skills/init-project/SKILL.md` |
| Plugin Commands | `plugins/*/commands/` | ~2-5 per plugin | `kebab-case.md` flat files | Yes — YAML front matter (`name`, `description`) | `ruflo-core/commands/ruflo-status.md` |
| Plugin Agent Definitions | `plugins/*/agents/` | ~4 per plugin | `kebab-case.md` flat files | No — plain markdown persona descriptions | `ruflo-core/agents/coder.md`, `researcher.md` |
| Core Agent Yamls | `v3/agents/` | 5 | `type-name.yaml` | No frontmatter — bare YAML (`type`, `version`, `capabilities`, `optimizations`) | `coder.yaml`, `architect.yaml` |
| MCP Tool Modules | `v3/mcp/tools/` | 13 `.ts` source files → 305 tools total | `domain-tools.ts` | No — TypeScript exports | `memory-tools.ts`, `swarm-tools.ts`, `agent-tools.ts` |
| Plugin Packages | `plugins/` | 33 dirs | `ruflo-<domain>` | `README.md` as descriptor; `plugin.json` in some | `ruflo-swarm/`, `ruflo-agentdb/` |
| v3 Plugins | `v3/plugins/` | 16 | `domain-name/` | `plugin.yaml` | `agentic-qe/plugin.yaml`, `prime-radiant/plugin.yaml` |
| Hook Configs | `plugins/ruflo-core/hooks/hooks.json` | 1 file, 27 lifecycle events | JSON | n/a | `hooks.json` (27 hooks: PreToolUse, PostToolUse, PreCompact + sub-matchers) |
| Audit/Build Scripts | `scripts/` | 18 | `audit-*.mjs`, `regen-*.mjs` | No | `audit-cli-mcp-tools.mjs`, `inventory-capabilities.mjs` |
| Verification Artifacts | `verification/` | Ed25519-signed manifest + JSONL history | `manifest.md.json`, `history.jsonl` | JSON | `verification/inventory.json` (canonical counts) |

## Agent skill frontmatter shape

**Minimal** (most `.agents/skills/`):
```yaml
---
name: agent-swarm
description: Agent skill for swarm - invoke with $agent-swarm
---
```

**Rich** (coordination skills like `hive-mind-advanced`):
```yaml
---
name: hive-mind-advanced
description: >
  Byzantine fault-tolerant consensus...
  Use when: distributed coordination...
  Skip when: single-agent tasks...
version: 1.0.0
category: coordination
tags: [hive-mind, swarm, queen-worker, consensus, collective-intelligence, multi-agent, coordination]
author: Claude Flow Team
---
```

**Plugin skill** (more structured, prescriptive):
```yaml
---
name: swarm-init
description: Initialize a multi-agent swarm with anti-drift configuration
argument-hint: "[--topology hierarchical|mesh|ring]"
allowed-tools: Bash(npx *) mcp__claude-flow__swarm_init mcp__claude-flow__swarm_status Agent
---
```

## Core agent YAML shape (`v3/agents/*.yaml`)
```yaml
# coder agent configuration
type: coder
version: "3.0.0"
capabilities:
  - code-generation
  - refactoring
  - debugging
optimizations:
  - flash-attention
  - token-reduction
createdAt: "2026-01-13T00:03:03.440Z"
```
These are **not** prompt files — they're capability declarations. The actual agent prompt lives in `plugins/*/agents/*.md` or is injected by the MCP server.

## Standout patterns

### 1. MCP-first, Claude Code as executor
Ruflo's 305 MCP tools are **coordinator verbs** only — no file writes, no code execution. Claude Code's `Task`, `Edit`, `Write`, `Bash` tools do the actual work. This is the most load-bearing architectural decision: swarm orchestration without usurping the editor. The "same message" rule (swarm_init + Task×N in one Claude Code response) is enforced via AGENTS.md and hooks — violation is the #1 failure mode.

### 2. Memory namespace hygiene as first-class primitive
Five namespaces with distinct semantics: `patterns` (reusable success stories), `tasks` (in-progress state), `solutions` (bug fixes), `feedback` (user corrections), `collaboration` (cross-agent shared state). HNSW vector index (384-dim ONNX embeddings, RaBitQ 1-bit quantization option) over SQLite/libsql. 29 controllers across 6 init levels. `pre-task` hook fires on every prompt and searches `patterns` namespace for similar past work — routing happens **before** the user sees a response.

### 3. Pluggable consensus transport (ADR-095 G2)
Swarm topology (hierarchical, mesh, hierarchical-mesh, adaptive) is separate from consensus protocol (raft, byzantine, gossip, crdt, quorum). Both are separate from transport (`LocalTransport` for in-process, `FederationTransport` for cross-machine Ed25519-signed WebSocket). Anti-drift defaults: `hierarchical + max-agents 8 + raft + specialized strategy`. These three composable knobs cover most real-world swarm configurations.

### 4. Plugin marketplace as distribution unit
33 plugins under `plugins/`, each bundling agents + skills + commands + hooks for a capability slice. The canonical install surface: `/plugin install ruflo-swarm@ruflo` from the Claude Code marketplace. `ruflo-agentdb` is the substrate plugin that all others compose. `verification/inventory.json` (Ed25519-signed) is the canonical artifact count — docs saying "300 tools" vs manifest saying 305 → manifest wins.

### 5. Dual-mode Codex worker (as of #1909)
`@claude-flow/codex` spawns real `codex exec` processes alongside `claude -p` workers, enabling genuinely cross-platform swarms. Prior to #1909, "dual mode" was a lie — both workers were Claude. The `codex-integration-audit` CI workflow now blocks regressions on spawn invariants.

### 6. Hook lifecycle is the hot path, not CLI commands
27 lifecycle hooks fire automatically (`pre-task`, `post-edit`, `pre-command`, `post-task`, `session-start`, etc.) via `.claude/settings.json`. 12 background workers (`audit`, `optimize`, `testgaps`, `consolidate`, ...) run silently. Expert use pattern: configure hooks once, never type `ruflo` again. The `ruflo-hook.sh` shim (ruflo-core@0.2.1+) is resilient — prefers local binary, falls back to `npx --prefer-offline`, always exits 0 so Claude Code never sees a hook crash.

## Inclusion candidates for unified discovery

- **`.agents/skills/` — 134 skills**: Primary consumable artifact. SKILL.md files have YAML frontmatter with `name`, `description`, `tags`. High signal for catalog. Includes: swarm topology skills (hierarchical-coordinator, mesh-coordinator, queen-coordinator, gossip-coordinator, byzantine-coordinator, raft-manager, crdt-synchronizer, quorum-manager), memory skills (agentdb-vector-search, agentdb-advanced, memory-management, reasoningbank-agentdb), hive-mind skills (hive-mind, hive-mind-advanced), hooks-automation, github-* skills (~6), pair-programming, performance-analysis, security-audit, neural-training.
- **`plugins/*/skills/` — ~8 per plugin, ~264 total across 33 plugins**: Structured skill SKILL.md with `allowed-tools` field — very useful for capability discovery. Each plugin is an independently installable unit.
- **`plugins/*/agents/*.md` — persona definitions**: Plain markdown agent personas (coder, researcher, reviewer, witness-curator). Inclusion candidate with lower confidence — no frontmatter.
- **`v3/agents/*.yaml` — 5 core capability declarations**: Minimal YAML, capability-only. Include as agent role definitions.
- **`verification/inventory.json`**: Authoritative counts (305 MCP tools, 49 CLI commands, 32 plugins, 44 agents). Read this first for any catalog validation.

## Exclusion candidates

- **`v3/mcp/tools/*.ts`**: TypeScript MCP tool source — these are implementation, not artifacts. The tool surface is exposed via the running MCP server, not file-by-file.
- **`v3/src/`**: DDD-structured TypeScript source (domain, application, infrastructure layers). Not artifacts.
- **`v3/plugins/`**: 16 v3 package-level plugins — these are build artifacts / WIP packages, not the installable marketplace plugins in root `plugins/`.
- **`scripts/*.mjs`**: Audit and build tooling — 18 Node.js scripts for regen, verify, and bulk-fix. Not artifacts.
- **`verification/`**: Signed manifests and history. Infrastructure, not consumable artifacts (except `inventory.json` as a count oracle).
- **`bin/`**: 3 npx launch shims. Not artifacts.
- **`agentdb.rvf` / `agentdb.rvf.lock`**: Runtime database files. Not artifacts.
- **`v3/docs/adr/`**: 100+ Architecture Decision Records. Documentation, not artifacts — though they explain why the catalog should surface certain skills over others.
- **`tests/`**: Test suite. Not artifacts.

## Open questions

1. **`.agents/skills/` vs `plugins/*/skills/` — are they the same artifact type?** Both use SKILL.md + YAML frontmatter, but `.agents/skills/` has 134 entries while each plugin's `skills/` dir has ~4-8. The `.agents/` form looks like a flattened "all skills from all installed plugins" aggregate. Need to confirm: does installing `ruflo-swarm` write its skills into `.agents/skills/swarm-init/` automatically, or are they separate namespaces?

2. **Plugin count discrepancy**: `verification/inventory.json` says 32 plugins; `plugins/` dir has 33 subdirs (excluding README.md). One of the 33 dirs may be a meta-dir or not yet published. Which one is extra?

3. **`agentdb-*` skills in `.agents/skills/`**: `agentdb-advanced`, `agentdb-learning`, `agentdb-memory-patterns`, `agentdb-optimization`, `agentdb-vector-search` — are these user-facing skills or internal substrate skills that shouldn't be in the catalog surface?

4. **`flow-nexus-*` skills**: `flow-nexus-neural`, `flow-nexus-platform`, `flow-nexus-swarm` in `.agents/skills/` — these reference `mcp__flow-nexus__*` tools. Is Flow Nexus a Ruflo upstream dependency, a third-party MCP server, or a deprecated component? The `agent-swarm/SKILL.md` references `mcp__flow-nexus__swarm_init` rather than `mcp__claude-flow__swarm_init`.

5. **v3 plugins vs root plugins**: `v3/plugins/` has 16 packages (agentic-qe, cognitive-kernel, gastown-bridge, etc.) that don't appear in the root `plugins/` marketplace list. Are these experimental / domain-specific extensions not yet promoted to the marketplace, or internal packages?

6. **`ruflo/` subdirectory**: Contains `src/mcp-bridge/index.js`, `src/ruvocal/` (with Helm charts and cloudbuild.yaml). The `ruvocal` subfolder has Kubernetes deployment config — is Ruflo intended for cloud deployment and is this the production serving infrastructure?
