---
repo: gstack
github: https://github.com/garrytan/gstack
local_path: /Users/davidcruwys/dev/upstream/repos/gstack
context_md: /Users/davidcruwys/dev/upstream/repos/gstack/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: gstack

**Maintainer**: Garry Tan (YC president)
**Version sampled**: 1.39.1.0

## Top-level layout

```
gstack/
├── .context/CONTEXT.md          # System context (~27 KB, very detailed)
├── SKILL.md / SKILL.md.tmpl     # Root meta-skill (router/dispatcher)
├── CLAUDE.md / AGENTS.md        # Host config
├── agents/                      # OpenAI agent definition (openai.yaml)
├── browser-skills/              # Domain-scoped browser automation skills
├── bin/                         # 60 CLI utility scripts (gstack-* prefixed)
├── hosts/                       # 11 host adapter TypeScript files
├── lib/                         # 4 TypeScript library modules
├── model-overlays/              # 6 per-model instruction overlays
├── openclaw/skills/             # 4 OpenClaw-flavoured skills
├── qa/references/ qa/templates/ # QA reference docs + report template
├── review/specialists/          # 7 specialist review checklists
├── scripts/                     # gen-skill-docs.ts + 21 resolver modules
├── <skill-name>/                # 40+ skill directories, each with SKILL.md.tmpl + SKILL.md
└── browse/, design/, make-pdf/  # Compiled binary sources (Bun)
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skill templates | `<skill-name>/SKILL.md.tmpl` | 49 | `kebab-case/SKILL.md.tmpl` | Yes (YAML) | `office-hours/SKILL.md.tmpl` |
| Compiled skills | `<skill-name>/SKILL.md` | 48 | `kebab-case/SKILL.md` | Yes (same as tmpl) | `office-hours/SKILL.md` |
| CLI bin scripts | `bin/gstack-*` | 60 | `gstack-<verb>[-noun]` (shell/TS) | No | `bin/gstack-next-version` |
| Host adapters | `hosts/<name>.ts` | 11 | `<agent-name>.ts` | No | `hosts/claude.ts`, `hosts/codex.ts` |
| Resolver modules | `scripts/resolvers/` | 21 | `<concern>.ts` or `<concern>/generate-*.ts` | No | `preamble/generate-preamble-bash.ts` |
| Model overlays | `model-overlays/<model>.md` | 6 | `<model>.md` | No (pure prose) | `model-overlays/opus-4-7.md` |
| OpenClaw skills | `openclaw/skills/<name>/SKILL.md` | 4 | `gstack-openclaw-<skill>` | Yes (YAML) | `gstack-openclaw-investigate/SKILL.md` |
| Browser skills | `browser-skills/<name>/SKILL.md` | 1 | `<domain-slug>/SKILL.md` | Yes (YAML, extra: `host`, `trusted`, `source`) | `hackernews-frontpage/SKILL.md` |
| Review specialists | `review/specialists/<concern>.md` | 7 | `<concern>.md` | No | `review/specialists/security.md` |
| QA references | `qa/references/`, `qa/templates/` | 2 | `issue-taxonomy.md`, `qa-report-template.md` | No | `qa/references/qa-report-template.md` |
| Agent definition | `agents/openai.yaml` | 1 | `<provider>.yaml` | No (YAML body) | `agents/openai.yaml` |

## Standout patterns

### 1. Template-compiled skills — the `.tmpl` → `.md` pipeline

The single most important pattern in gstack. Every skill is defined in `SKILL.md.tmpl`, NOT in `SKILL.md`. The `.tmpl` file:
- Contains the same YAML frontmatter (`name`, `preamble-tier`, `version`, `description`, `allowed-tools`, `triggers`, `gbrain`)
- Contains `{{PLACEHOLDER}}` tokens in the body: `{{PREAMBLE}}`, `{{BASE_BRANCH_DETECT}}`, `{{GBRAIN_CONTEXT_LOAD}}`, `{{GBRAIN_SAVE_RESULTS}}`, `{{SCOPE_DRIFT}}`, `{{PLAN_COMPLETION_AUDIT_REVIEW}}`, `{{REVIEW_DASHBOARD}}`, `{{TEST_BOOTSTRAP}}`

`scripts/gen-skill-docs.ts` reads each `.tmpl`, calls the corresponding resolver in `scripts/resolvers/` to expand each token, and writes the committed `SKILL.md`. The committed `.md` starts with:
```
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->
```

**Implication for cataloging**: The `.tmpl` is the source of truth; the `.md` is a build artifact. Both are committed. Merge conflicts must always be resolved on `.tmpl` + resolver, then regenerated. The template/resolver split means shared cross-cutting blocks (preamble bash, GBrain context load, branch detection) can evolve independently of the skill-specific workflow bodies.

The preamble resolver itself is split into 20+ fine-grained generators under `scripts/resolvers/preamble/` — one file per concern (`generate-upgrade-check.ts`, `generate-telemetry-prompt.ts`, `generate-ask-user-format.ts`, etc.). `preamble-tier: 1-4` in frontmatter controls which generators fire.

### 2. Multi-host compilation from single source

The same `.tmpl` produces different `SKILL.md` outputs for different target agents:
- `hosts/claude.ts` — primary, full feature surface
- `hosts/codex.ts` — strips denylist items, removes `voice-triggers`, adds OpenAI-format metadata
- `hosts/gbrain.ts`, `hosts/openclaw.ts`, `hosts/cursor.ts`, `hosts/kiro.ts`, `hosts/hermes.ts`, etc.

Each host declares which resolver placeholders to suppress (e.g., `GBRAIN_*` resolvers are suppressed on hosts that don't have GBrain). Setup runs `gen-skill-docs --host all` and installs host-flavoured files into each agent's skills directory.

**Pattern name**: "Host abstraction" — single source, multi-target compilation.

### 3. Skill pipeline as directed graph

Skills are not independent tools. They form an explicit pipeline where each step's output is the next step's input:

```
office-hours → plan-ceo-review → plan-eng-review → plan-design-review → [implement]
             → autoplan (runs all three plan-* reviews in sequence)
→ review → qa → codex/cso (cross-model second opinion)
→ ship → land-and-deploy → canary → retro
```

The root `SKILL.md` (in `gstack/`) is a dispatcher/router that reads the user's intent and invokes the correct specialist skill via the Skill tool.

### 4. GBrain frontmatter block

Skills that query persistent memory include a `gbrain:` YAML block defining structured queries against the GBrain memory store (a separate repo). Each query has `id`, `kind` (`list` | `filesystem`), `filter`, `sort`, `limit`, and `render_as` — effectively a mini-DSL for memory-aware context injection.

### 5. Browser-skills are a separate artifact class

`browser-skills/` contains site-scoped automation skills with extra frontmatter fields: `host: <domain>`, `trusted: true|false`, `source: human|generated`. These are not AI-agent skills — they are browser automation scripts for specific websites, invoked via `$B skill run <name>`. The reference implementation is `hackernews-frontpage`.

### 6. Model overlays support inheritance

`model-overlays/opus-4-7.md` opens with `{{INHERIT:claude}}` — a template token that expands the `claude.md` overlay first, then adds model-specific instructions on top. This is a lightweight inheritance system for model-specific behavioral tuning.

## Inclusion candidates for unified discovery

- **SKILL.md.tmpl files** (49) — primary artifact; these are the source of truth for skills
- **SKILL.md files** (48) — generated from tmpl; useful for installed-form frontmatter (same structure as tmpl)
- **Browser-skills SKILL.md** (1, expandable) — distinct artifact class with richer frontmatter schema
- **OpenClaw skills SKILL.md** (4) — host-specific skill flavouring, already installed format
- **Model overlays** (6) — behavioral modifier layer; distinct from skills but still "addressable artifacts"
- **Review specialists** (7) — reference checklists consumed by `review` skill; scoped instruction sets

## Exclusion candidates

- `bin/gstack-*` scripts (60) — infrastructure/tooling, not agent-facing artifacts
- `scripts/resolvers/` (21 modules) — build-time pipeline, not addressable at runtime
- `hosts/*.ts` (11) — compilation targets, not artifacts
- `lib/` (4 TS modules) — library code
- `browse/`, `design/`, `make-pdf/` source trees — compiled binary code
- `supabase/` — backend infra
- `test/`, `.github/` — CI and test fixtures
- `docs/` — human-facing documentation, not skills
- `gstack-upgrade/migrations/` — schema migration files

## Open questions

1. **tmpl vs md for cataloging**: Should the catalog index `.tmpl` files (source of truth) or `.md` files (installed artifact shape)? Or both with a `compiled_from` link? The tmpl has the authoritative `gbrain:` queries; the md has the expanded preamble — they contain different information.

2. **Browser-skills schema**: `browser-skills/` has a richer frontmatter schema (`host`, `trusted`, `source`) than standard skills. Does the unified discovery contract need a `browser-skill` subtype, or is `skill` with extra optional fields enough?

3. **Model overlays as artifact type**: Are model overlays (6 files) worth cataloging separately, or are they too infrastructural? They're behavioral modifiers — closer to "config" than "skill" but they do shape agent behavior in a discoverable way.

4. **Review specialists**: These 7 markdown files are consumed by the `review` skill as sub-checklists. Are they standalone artifacts (each addresses a distinct concern: security, performance, API contract, etc.) or just `review` skill internals?

5. **Pipeline ordering**: The skill pipeline is a directed graph with clear step ordering. Should recon capture pipeline position (`step: 1-of-7`) or is that a `catalog:tag` concern?

6. **GBrain queries in frontmatter**: The `gbrain:` block is a mini-DSL for memory queries. Does the discovery contract need to surface gbrain query schemas, or is that too deep for Phase 1?
