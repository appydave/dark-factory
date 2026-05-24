# Dark Factory Catalog

**Purpose**: Cross-repo catalog of skills/agents/workflows/commands across the 14-repo agentic-factory cluster. End goal — a **composable set of single-responsibility skills** that solve legitimate dark-factory problems, follow a consistent pattern, and can compose into workflows / topologies. Number emerges from the work, not as a target.

**Phase**: recon ✓ → discover ✓ (1,100 artifacts) → distill `orchestration` ✓ (9) → distill `code-review` ✓ (6) → **2 skills built** (`pr-lifecycle` new, `ralphy` upgraded) → **template improvements applied** (schema 0.0.6) → distill `workflow-architecture` ✓ (6, 2026-05-17) → **repo #14 added** (`matt-pocock-skills`, recon 2026-05-23, ~18 artifacts). **Next**: discover run for repo #14 OR continue distilling remaining clusters.
**Maintainer**: David Cruwys
**Skill logic**: `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/`

## Structure

| Path | What |
|------|------|
| `schema-current.md` | Live schema (versioned) |
| `schema-history.md` | Schema change log (append-only) |
| `recon/` | Per-repo shape reports (Phase 1) |
| `artifacts.jsonl` | Unified corpus (Phase 2) |
| `evaluations/` | Scoring notes (Phase 4) |
| `distillations/` | Unified-skill drafts (Phase 5) |
| `insights.md` | **Append-only audit log** of atomic craft bits (phrases, contrasts, reframings) surfaced during recon/discover. Smaller than a pattern. |
| `feedback-log.md` | David's feedback for self-improvement |

## Phases

1. **Recon** — per-repo shape discovery → `recon/<slug>.md`
2. **Discover** — unified-contract sweep → `artifacts.jsonl`
3. **Tag** — multi-select SDLC stage mapping → `tags.jsonl`
4. **Evaluate** — score artifacts on quality/uniqueness/mechanism
5. **Distill** — cluster + draft ~50 unified skills

## Current status

- **2026-05-16** — Bootstrap → Phase 1 recon 13/13 → schema 0.0.2 → 0.0.3 → Phase 2 discover 13/13 ✓ → schema 0.0.4. **Corpus: 1,100 artifacts (691 skills / 224 commands / 185 agents), 100% JSON-valid.** Awaiting David's review of cluster-vocabulary additions before tag/evaluate/distill.
- **2026-05-23** — Repo #14 added: `matt-pocock-skills` (mattpocock/skills, ~97K stars). Remote-only recon complete. ~18 discoverable artifacts (14 promoted + 4 misc). New prompt patterns surfaced: `vocabulary-only-context`, `grill-first-alignment`, `feedback-loop-first`, `token-compression-mode`. Discover run pending.

**→ For *meaning* — what each cluster/pattern is, where it concentrates, signature examples, and why each one is worth mining — read [phase-2-synthesis.md](./phase-2-synthesis.md).**

## Corpus statistics (2026-05-16)

**By repo** (largest → smallest):
| Repo | Count | Notes |
|------|------:|-------|
| everything-claude-code | 365 | 230 skills + 60 agents + 75 commands |
| ruflo | 219 | 134 skills + 45 agents + 40 commands (+ 104 plugin-bundled skills deferred to Phase 2.5) |
| appydave-plugins | 122 | 114 active + 8 retired across appydave/brand-dave/flivideo |
| compound-engineering | 86 | 37 skills + 49 agents (incl. 2 beta) |
| gsd | 81 | 60 commands (51 with paired workflow body) + 21 agents |
| gbrain | 51 | 42 active + 1 retired + 8 recipes |
| gstack | 49 | `.tmpl` source files; compiled `.md` outputs excluded |
| bmad-method | 44 | all SKILL.md (no separate agent/command/workflow types in v6) |
| agent-skills-osmani | 33 | 23 skills + 3 personas + 7 Claude commands (Gemini variants excluded) |
| spec-kit | 23 | 9 core SDD + 7 extension + 7 preset commands |
| superpowers | 14 | densest prompt-pattern coverage in corpus |
| compound-knowledge | 11 | 6 skills + 5 agents |
| poem | 2 | Penny + Alex only |
| matt-pocock-skills | ~18 | 14 promoted skills + 4 misc; discover run pending |

**By cluster** (top 10):
| Cluster | Count |
|---------|------:|
| knowledge-capture | 201 |
| system-comprehension | 180 (inflated — ECC fallback) |
| orchestration | 171 |
| verification-validation | 160 |
| spec-writing | 157 |
| workflow-architecture | 137 |
| code-review | 132 |
| planning | 132 |
| delivery-readiness | 90 |
| code-implementation | 81 |

**By prompt pattern** (top 10):
| Pattern | Count |
|---------|------:|
| capability-description | 311 |
| discovery | 184 |
| reviewer-agent-separation | 92 |
| orchestration-topology | 87 |
| multi-harness-compile | 72 |
| injection-resistance | 60 |
| knowledge-folder-as-bus | 50 |
| progressive-disclosure | 44 |
| deliberate-context-exclusion | 41 |
| anti-rationalization | 39 |

**Vocabulary additions surfaced** (awaiting David's review):
- Pattern: `multi-harness-compile` (added to candidate section — 2 repos, 72 artifacts)
- Clusters (in `cluster-vocabulary-additions.md`): `security-review` (66), `performance` (34), `dependency-management` (21), `accessibility` (3)

## Cross-repo synthesis — Phase 1

### Aggregate counts (rough, repo-reported)

| Repo | Skills | Agents | Commands/Workflows | Other |
|------|--------|--------|--------------------|-------|
| appydave-plugins | 96 | — | 18 | 14 script-bearing skills |
| bmad-method (v6) | 44 SKILL.md | ~5 | 78 step files | 6 templates, 32 customize.toml |
| gstack | 49 .tmpl / 48 .md | — | 60 CLI scripts | 11 host adapters, 21 resolvers |
| superpowers | 14 | — | — | 23 companion files, 5 specs, 5 plans, 4 hooks |
| agent-skills-osmani | 23 | 3 personas | 14 (7 Claude + 7 Gemini) | 3 hooks |
| compound-engineering | 37 | 49 | — | ~25 learning docs |
| compound-knowledge | 6 | 5 | — | (11 total) |
| everything-claude-code | 230 | 60 | 75 | 110 rules, 28 hooks, 33 adapter skills |
| ruflo | 134 | 44 | 49 | 305 MCP tools, 33 plugin bundles |
| gbrain | 43 | — | — | 8 recipes, 4 identity templates, 9 conventions |
| spec-kit | — | — | 9 command templates | 30 harness adapters, 5 doc templates |
| gsd | — (60 installed) | 21 | 60 workflows | 43 templates, 9 hooks |
| poem | — | **1 confirmed (Penny)**, Alec **missing** | — | Victor + Felix surfaced |

### Recurring cross-cutting patterns

1. **Multi-harness compile-on-install** — gstack (.tmpl→.md, 11 hosts via 21 resolvers), spec-kit (one Markdown source → Claude/Gemini/Codex/Copilot/Cursor/Windsurf/Goose/Roo/Kimi/Qwen + 20 more), gsd (two-file split installs for 12 runtimes), ECC (33 `.agents/skills/` adapters). Becoming the dominant cross-harness pattern.
2. **Worker/reviewer separation** — compound-engineering (49 agents in tiered parallel review against `findings-schema.json`), ECC (60 agents w/ Prompt Defense Baseline), gsd (fresh-context subagent architecture with `.planning/STATE.md` as bus).
3. **Anti-rationalization tables** — agent-skills-osmani (load-bearing in every SKILL.md), superpowers (TDD-applied: RED = capture rationalisations, GREEN = counter-text).
4. **Description-as-trigger-API** — superpowers explicitly bans workflow summaries in `description`; agent-skills-osmani lazy-loads only `name` + `description` at session start.
5. **Knowledge capture as first-class loop step** — compound-engineering `ce-compound` (543 lines, auto-trigger on "that worked"/"it's fixed"), compound-knowledge (folder-as-bus, no DB/daemon), ECC (Observer agent → Instincts YAML → `/evolve` gate).
6. **Phase-labelled SDLC encoding** — bmad-method (`1-analysis/`, `2-plan-workflows/`, `3-solutioning/`, `4-implementation/`), spec-kit (`constitution → specify → clarify → plan → tasks → analyze → implement` as artifact graph), gsd (`.planning/STATE.md` as state machine).
7. **Orchestrator + sub-agent decomposition** — appydave-plugins (doc-review, omi, delivery-review fan-outs), ruflo (swarm_init + Task×N in one message), bmad agent skills that menu sub-skills.

### Open questions across repos (require David's call before Phase 2)

| # | Question | Affects |
|---|----------|---------|
| A | Source vs compiled — track `.tmpl` source, compiled `.md`, or both? | gstack, spec-kit, gsd, ECC, compound-engineering |
| B | Sub-artifact granularity — are bmad step files (78), superpowers companion files (23), and agent-skills sub-files first-class entries or skill metadata? | bmad, superpowers, agent-skills-osmani |
| C | Multi-harness variants — one catalog entry with variant flags, or N entries? | spec-kit (30), agent-skills (Claude+Gemini), ECC (33), gsd (12) |
| D | Adapter vs canonical — ECC's 33 adapter skills, Ruflo's 33 plugin bundles vs `.agents/skills/` — separate type? | ECC, ruflo |
| E | **POEM Alec missing** — Alec doesn't exist in the repo. Was it planned, or is Victor the intended second agent? Also `felix.md` vs `field-tester.md` are duplicates. | poem |
| F | Rules with no frontmatter — separate catalog schema or "always-on context"? | ECC (110 rules) |
| G | Beta vs stable — `ce-work-beta`, `ce-polish-beta` — separate artifact type? | compound-engineering |
| H | Cross-repo dependency edges — compound-knowledge reads `docs/solutions/` (compound-engineering writes it); gbrain delegates code-thinking to gstack. Catalog these edges? | compound-engineering ↔ compound-knowledge, gbrain ↔ gstack |
| I | Recipes as distinct type from skills? | gbrain (8 recipes w/ own schema: `secrets`, `health_checks`, `setup_time`) |
| J | Personas as distinct type from skills/agents? | agent-skills-osmani (3 personas) |
| K | Versioning — track `version` field per artifact? | agent-skills-osmani, ruflo, ECC |
| L | MCP tools in scope? Ruflo has 305 coordination tools — are these artifacts? | ruflo |
| M | AgentShield (separate npm package) in scope? | ECC |
| N | Out-of-scope-but-related — appydave root-level `.skill` zips, archived consultants plugin | appydave-plugins |

## Recon coverage

| # | Repo | Slug | Report |
|---|------|------|--------|
| 1 | AppyDave Plugins | `appydave-plugins` | `recon/appydave-plugins.md` |
| 2 | BMAD-METHOD | `bmad-method` | `recon/bmad-method.md` |
| 3 | gstack | `gstack` | `recon/gstack.md` |
| 4 | Superpowers | `superpowers` | `recon/superpowers.md` |
| 5 | Agent Skills (Osmani) | `agent-skills-osmani` | `recon/agent-skills-osmani.md` |
| 6 | Compound Engineering | `compound-engineering` | `recon/compound-engineering.md` |
| 7 | Compound Knowledge | `compound-knowledge` | `recon/compound-knowledge.md` |
| 8 | Everything Claude Code | `everything-claude-code` | `recon/everything-claude-code.md` |
| 9 | Ruflo | `ruflo` | `recon/ruflo.md` |
| 10 | gbrain | `gbrain` | `recon/gbrain.md` |
| 11 | Spec Kit | `spec-kit` | `recon/spec-kit.md` |
| 12 | GSD | `gsd` | `recon/gsd.md` |
| 13 | POEM (Penny + Alec only) | `poem` | `recon/poem.md` |
| 14 | Matt Pocock Skills | `matt-pocock-skills` | `recon/matt-pocock-skills.md` |
