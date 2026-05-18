---
repo: gbrain
github: https://github.com/garrytan/gbrain
local_path: /Users/davidcruwys/dev/upstream/repos/gbrain
context_md: /Users/davidcruwys/dev/upstream/repos/gbrain/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: GBrain

**Purpose**: Phase 1 reconnaissance — artifact types, counts, and structure for gbrain. Pre-discovery.

**For Agents**: Read before running `catalog:discover` on this repo. Describes what kinds of artifacts exist and where.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

**Maintainer**: Garry Tan
**Version sampled**: 0.32.3.0 (per `skills/manifest.json`)

## Top-level layout

```
gbrain/
├── .context/CONTEXT.md          ← rich auto-generated snapshot
├── admin/                       ← React SPA for OAuth admin dashboard (not artifacts)
├── bin/                         ← CLI entry point
├── docs/                        ← architecture, guides, ethos, MCP docs (71 .md files)
│   ├── architecture/
│   ├── designs/
│   ├── ethos/
│   ├── eval/
│   ├── guides/
│   ├── integrations/
│   └── mcp/
├── evals/                       ← retrieval benchmarks + functional-area-resolver eval harness
├── recipes/                     ← integration playbooks (8 files, YAML frontmatter)
├── skills/                      ← 43 SKILL.md files + conventions + migrations + manifest
│   ├── conventions/             ← 9 shared convention files (no SKILL.md, just prose)
│   ├── migrations/              ← 28 versioned migration notes (v0.5.0 → v0.35.0.0)
│   └── manifest.json            ← machine-readable skill registry
├── src/                         ← TypeScript source (CLI + MCP server + engine)
├── templates/                   ← 4 identity templates (.template extension)
├── test/                        ← extensive test suite + e2e fixtures
├── AGENTS.md                    ← multi-harness install + operating protocol
├── CLAUDE.md                    ← Claude Code architecture reference
├── RESOLVER.md  (in skills/)    ← skill dispatcher table
├── gbrain.yml                   ← storage topology config (db_tracked vs db_only dirs)
└── openclaw.plugin.json         ← OpenClaw plugin manifest
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skills | `skills/*/SKILL.md` | 43 | one dir per skill, `SKILL.md` inside | YAML (`name`, `version`, `description`, `triggers`, `tools`, `mutating`, `writes_to`) | `skills/brain-ops/SKILL.md` |
| Convention files | `skills/conventions/` | 9 | kebab-case `.md`, one `.yaml` | None — prose only | `skills/conventions/brain-first.md` |
| Recipes | `recipes/*.md` | 8 | kebab-case `.md` | YAML (`id`, `name`, `version`, `category`, `requires`, `secrets`, `health_checks`, `setup_time`, `cost_estimate`) | `recipes/calendar-to-brain.md` |
| Identity templates | `templates/*.template` | 4 | `NAME.md.template` | None — markdown body only | `templates/SOUL.md.template` |
| Migration notes | `skills/migrations/*.md` | 28 | `v0.X.Y.md` | None | `skills/migrations/v0.32.2.md` |
| Architecture/guide docs | `docs/**/*.md` | 71 | kebab-case or ALLCAPS | Mixed — some YAML frontmatter (ethos essays) | `docs/ethos/THIN_HARNESS_FAT_SKILLS.md` |
| Skill manifest | `skills/manifest.json` | 1 | `manifest.json` | N/A — JSON | `skills/manifest.json` |
| OpenClaw plugin | `openclaw.plugin.json` | 1 | root-level JSON | N/A — JSON | `openclaw.plugin.json` |
| Eval harness | `evals/` | 5 | mixed (`.jsonl`, `.mjs`, `.ts`) | None | `evals/functional-area-resolver/` |
| Skill resolver | `skills/RESOLVER.md` | 1 | `RESOLVER.md` | None — dispatcher table | `skills/RESOLVER.md` |
| Agent entry point | `AGENTS.md` | 1 | `AGENTS.md` | None | root |

## Standout patterns

### 1. Thin harness, fat skills — the defining ethos

GBrain's foundational design decision (articulated in `docs/ethos/THIN_HARNESS_FAT_SKILLS.md`) is that agent capability lives in markdown skills, not code. Skills carry judgment ("if the person is a YC founder, check portfolio connections before writing the page"), survive model swaps, and accumulate domain knowledge independently of the harness. The harness stays small: a CLI + MCP server, both generated from a single `operations.ts` contract file. This is the same architecture gbrain teaches agents to use — the repo is itself an example of what it advocates.

### 2. Two-repo separation: gbrain (knowledge) vs gstack (code)

GBrain is explicitly scoped to non-code knowledge. `docs/ethos/THIN_HARNESS_FAT_SKILLS.md` and CONTEXT.md both state that engineering-specific workflows (investigate, review, plan-eng-review) belong to GStack (`github.com/garrytan/gstack`). GBrain indexes code files via tree-sitter for cross-reference, but it defers thinking skills to GStack. `RESOLVER.md` reflects this: "Thinking skills (from GStack)" section explicitly routes brainstorm/review/debug to GStack skills, with a fallback note: "If GStack is installed, the agent reads them directly. If not, brain-only mode still works." The repos are designed to run independently or together.

### 3. Machine-readable skill manifest + conformance versioning

`skills/manifest.json` declares `conformance_version: "1.0.0"` alongside a per-skill registry (name, path, description). This signals that gbrain skills are meant to be consumed programmatically — by an orchestrator or plugin manager, not just read by agents. Each skill's YAML frontmatter goes further: `triggers`, `tools`, `writes_to`, and `mutating` fields give a machine-parseable contract, not just human prose.

### 4. Recipes as versioned integration playbooks

`recipes/` files are a distinct artifact type from skills. They describe external integrations (Google Calendar, email, X/Twitter, Twilio voice) with structured YAML (`secrets`, `health_checks`, `setup_time`, `cost_estimate`, `requires`). These are not agent behaviors — they are operator deployment guides for wiring data sources into the brain. No equivalent exists in gstack (based on prior gstack brain docs).

### 5. Named storage topology via gbrain.yml

`gbrain.yml` specifies which brain content directories are `db_tracked` (version-controlled, human-curated: `people/`, `companies/`, `deals/`, `concepts/`, etc.) versus `db_only` (machine-generated, gitignored, restorable from DB: `media/x/`, `media/articles/`, `meetings/transcripts/`). This explicit separation of curated vs bulk-generated content is a design decision that affects how the dark factory catalog should treat gbrain page types.

### 6. Identity templates bootstrapped by soul-audit skill

The 4 files in `templates/` (`SOUL.md`, `HEARTBEAT.md`, `USER.md`, `ACCESS_POLICY.md`) are populated by the `soul-audit` skill, not written by hand. HEARTBEAT.md includes cron-style schedules pointing to specific skills (signal-detector every message, daily-task-prep each morning, brain sync every 15 minutes). This is gbrain's operational rhythm declaration.

## Sample artifacts (paraphrased)

**`skills/brain-ops/SKILL.md`** — the core always-on skill. Declares `mutating: true`, `writes_pages: true`, lists 8 MCP tools. Body defines the Iron Law (every mention of a person/company creates a back-link), the READ → ENRICH → WRITE loop, and four operational phases. Cross-references `conventions/brain-first.md` and `conventions/quality.md` for the detailed protocols.

**`skills/signal-detector/SKILL.md`** — ambient sub-agent. Fires on every inbound message. Spawned in parallel, never blocks main response. Captures original thinking (exact phrasing preserved) AND entity mentions with equal priority. Logs a one-line summary of what was captured.

**`recipes/calendar-to-brain.md`** — integration recipe. YAML frontmatter declares two auth options (ClawVisor gateway vs direct Google OAuth), health checks for each, 20-minute setup time, $0 cost. Body describes the full calendar sync flow.

**`templates/HEARTBEAT.md.template`** — operational cadence declaration. Lists five time windows (every message, morning, every 15 minutes, daily, weekly) and which skills run in each. Comments instruct the `soul-audit` skill to fill in custom schedules.

**`skills/conventions/brain-first.md`** — shared convention. No frontmatter. Prose-only. Describes the 5-step lookup protocol all skills must follow before any external API call. Referenced from multiple SKILL.md files as a shared sub-procedure.

## Inclusion candidates for unified discovery

- **Skills** (`skills/*/SKILL.md`) — primary artifact type; YAML frontmatter is fully machine-parseable; triggers and tools fields give scope and tool-use contract
- **Recipes** (`recipes/*.md`) — distinct artifact class; structured YAML; high signal for integration coverage
- **Identity templates** (`templates/*.template`) — agent identity layer; worth cataloging as a pattern even if not "skills"
- **Skill manifest** (`skills/manifest.json`) — ready-made discovery index; should be read first during `catalog:discover`
- **RESOLVER.md** (`skills/RESOLVER.md`) — dispatcher table; represents the routing layer, not just individual skills; worth cataloging as a meta-artifact

## Exclusion candidates

- `src/` — TypeScript implementation; not agent artifacts
- `test/` — test suite and fixtures (though e2e fixtures contain interesting brain page examples)
- `admin/` — React SPA; build artifact
- `skills/migrations/` — versioned change notes; historical, not active skills
- `skills/conventions/` — shared sub-procedures; referenced by skills but not independently invokable; borderline
- `docs/` — architecture documentation; not skills; some ethos docs (like THIN_HARNESS_FAT_SKILLS.md) are high-signal philosophy but not catalog artifacts
- `evals/` — retrieval benchmark harness; engineering tooling

## Open questions

1. **GStack relationship**: How much of gbrain's value is contingent on gstack being installed alongside? RESOLVER.md suggests gbrain degrades gracefully without it, but the thinking-skills routing table points entirely at gstack. Should the catalog treat gbrain-alone vs gbrain+gstack as separate capability profiles?

2. **Recipes vs skills boundary**: Recipes are versioned, have frontmatter, and describe agent-accessible integrations. Are they a distinct catalog type or a sub-type of skills? The `category: sense` field in recipe frontmatter suggests Garry treats them differently.

3. **Conformance versioning**: `skills/manifest.json` declares `conformance_version: "1.0.0"`. Is this version tracked across repos (gstack uses the same)? If so, it could be a compatibility signal for the unified catalog.

4. **gbrain.yml storage topology**: The `db_tracked` / `db_only` split directly affects what counts as curated knowledge vs ephemeral cache. Should the catalog schema include a field for this storage class?

5. **Minions as an artifact type**: GBrain's Minion system (Postgres-native background jobs) is code infrastructure, not a skill. But the `minion-orchestrator` skill teaches agents how to spawn and coordinate minions. Is the minion taxonomy (job types, handlers) worth cataloging separately?
