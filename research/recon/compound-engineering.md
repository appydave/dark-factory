---
repo: compound-engineering
github: https://github.com/EveryInc/compound-engineering-plugin
local_path: /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin
context_md: /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Compound Engineering Plugin

**Maintainer**: Kieran Klaassen (kieran@every.to / EveryInc)
**Version sampled**: marketplace v1.0.2 (CLI + plugin on linked-versions; latest as of 2026-05-11 CONTEXT.md snapshot)

## Top-level layout

```
compound-engineering-plugin/
├── .agents/plugins/          ← Codex marketplace catalog
├── .claude/commands/         ← legacy (empty after v2.39.0 collapse)
├── .claude-plugin/           ← Claude marketplace.json
├── .compound-engineering/    ← config.local.example.yaml (gitignored at runtime)
├── .context/                 ← CONTEXT.md (21 KB system snapshot)
├── .cursor-plugin/           ← Cursor marketplace catalog
├── docs/
│   ├── brainstorms/          ← requirements docs (ce-brainstorm outputs)
│   ├── plans/                ← plan docs (ce-plan outputs)
│   ├── solutions/            ← learning docs (ce-compound outputs, subdirs by category)
│   └── specs/
├── plugins/
│   ├── coding-tutor/         ← second plugin (skills + commands only)
│   └── compound-engineering/ ← primary plugin
│       ├── agents/           ← 49 .agent.md files
│       └── skills/           ← 37 skill dirs, each with SKILL.md
├── scripts/release/
├── src/                      ← Bun/TypeScript CLI (converter + installer)
│   ├── commands/
│   ├── converters/           ← claude-to-<target>.ts (8 targets)
│   ├── parsers/claude.ts
│   └── targets/
└── tests/
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skills | `plugins/compound-engineering/skills/<name>/SKILL.md` | 37 | `ce-<name>/SKILL.md` — every dir gets own SKILL.md | Yes — `name:`, `description:`, `argument-hint:` | `ce-compound/SKILL.md` (543 lines, multi-phase orchestrator) |
| Agents | `plugins/compound-engineering/agents/` | 49 | `ce-<name>.agent.md` flat, `ce-` prefix mandatory | Yes — `name:`, `description:`, `model:`, `tools:`, optional `color:` | `ce-adversarial-reviewer.agent.md`, `ce-learnings-researcher.agent.md` |
| Skill references | `plugins/*/skills/<name>/references/` | ~60 files across skills | kebab-case `.md`, sometimes `.yaml`, `.json` | No — plain markdown or schema files | `ce-compound/references/schema.yaml`, `ce-plan/references/plan-template.md` |
| Skill scripts | `plugins/*/skills/<name>/scripts/` | sparse (e.g., `ce-compound/scripts/validate-frontmatter.py`) | language-appropriate | No | Python validator run inline from SKILL.md |
| Skill assets | `plugins/*/skills/<name>/assets/` | sparse (e.g., `ce-compound/assets/resolution-template.md`) | kebab-case | No | Markdown template for solution doc assembly |
| Learning docs | `docs/solutions/<category>/<slug>-<date>.md` | ~25 live (self-documenting repo) | `<slug>-YYYY-MM-DD.md` or plain | Yes — YAML frontmatter (`title`, `problem_type`, `tags`, `module`, `severity`, `date`) | `pass-paths-not-content-to-subagents-2026-03-26.md` |
| CLI source | `src/` | ~20 TS files | `<target>.ts`, `claude-to-<target>.ts` | No — TypeScript | `src/converters/claude-to-codex.ts` |
| Marketplace catalogs | `.claude-plugin/marketplace.json`, `.cursor-plugin/`, `.agents/plugins/` | 3 JSON files | fixed names per platform | No | Declares plugins + source paths |

## Standout patterns

### 1. The compound loop is the product — skills are the wiring

The conceptual loop is: `strategy → ideate? → brainstorm → plan → work → debug → code-review → compound → product-pulse`. Each skill is one step. They are explicitly designed to hand off to each other — `ce-plan` calls `ce-work` via `Skill` primitive, `ce-compound` is auto-triggered by phrases like "that worked" / "it's fixed". The loop is not a separate workflow file; it is implicit in skill descriptions, argument-hints, and the `Auto-Invoke` block embedded in `ce-compound/SKILL.md`.

### 2. Reviewer-agent separation with tiered persona dispatch

`ce-code-review` does not review code itself. It dispatches reviewer agents in parallel tiers:
- **Always-on** (4 persona agents + 2 CE agents): `ce-correctness-reviewer`, `ce-testing-reviewer`, `ce-maintainability-reviewer`, `ce-project-standards-reviewer`, `ce-agent-native-reviewer`, `ce-learnings-researcher`
- **Cross-cutting conditional** (7 agents): `ce-adversarial-reviewer`, `ce-reliability-reviewer`, `ce-security-reviewer`, `ce-performance-reviewer`, `ce-scope-guardian-reviewer`, `ce-previous-comments-reviewer`, `ce-api-contract-reviewer`
- **Stack-specific conditional** (8 agents): per-language Kieran reviewers + Swift/iOS + Rails/data migration/design
- **CE-plugin-specific** (2 agents): `ce-agent-native-reviewer` + `ce-adversarial-document-reviewer`

Each persona agent returns **JSON matching `findings-schema.json`** — the orchestrator deduplicates, gates by confidence, and assembles the review. The orchestrator is a skill; the reviewers are pure agents — user never invokes agents directly.

### 3. Learning capture is a first-class citizen, not a post-hoc note

`ce-compound/SKILL.md` is 543 lines of detailed multi-phase orchestration:
- **Phase 0.5**: scans MEMORY.md auto-memory block for relevant prior context before research
- **Phase 1**: parallel research subagents (Context Analyzer, Solution Extractor, Related Docs Finder)
- **Phase 2**: overlap detection — if existing doc scores High overlap, update it; Moderate, note consolidation; Low, create new. Runs `scripts/validate-frontmatter.py` for parser-safety
- **Phase 2.5**: Selective Refresh Check — decides whether to invoke `ce-compound-refresh` on stale related docs
- **Discoverability Check**: inspects AGENTS.md/CLAUDE.md to ensure future agents can find `docs/solutions/`
- **Phase 3**: optional specialized reviewer agents (performance-oracle, security-sentinel, data-integrity-guardian)
- **Auto-invoke trigger**: fires on "that worked", "it's fixed", "working now", "problem solved"

The learning output format is dual-track: **bug track** (problem/symptoms/what-didn't-work/solution/why/prevention) vs **knowledge track** (context/guidance/why-it-matters/when-to-apply/examples). Schema enforced by `references/schema.yaml` + Python validator.

### 4. Claude as authoring source of truth; cross-platform via converter pipeline

Skills are authored once in Claude's YAML-frontmatter + Markdown format, then `bun run src/index.ts install --to <target>` converts to Codex, OpenCode, Pi, Gemini, Kiro, Copilot, Droid, Qwen. Each target has a `src/converters/claude-to-<target>.ts` module. This is a publish-once multi-harness deployment pattern with the converter as the adapter layer.

### 5. Scratch space discipline and skill hermeticity

Two-tier temp strategy: `mktemp -d` for per-run throwaway, `/tmp/compound-engineering/<skill>/<run-id>/` for cross-invocation reuse, `.context/` only for user-curated artifacts. Each skill dir is hermetic — no cross-skill file references (installed plugins live at versioned cache paths, cross-skill paths would break). Shared support must be duplicated inline or in each skill's own `references/`.

### 6. Caching gotcha shapes authoring workflow

Skill and agent definitions cache at Claude Code session start. Edits to `SKILL.md` or `.agent.md` don't take effect until next session. `skill-creator` is the proper iteration loop (injects content into a generic subagent at dispatch time). This constraint is explicitly called out in CONTEXT.md non-obvious constraints and failure modes.

## Inclusion candidates for unified discovery

- **Skills** (`plugins/*/skills/*/SKILL.md`) — 37 files, YAML-frontmatter addressable, user-invokable workflows. Primary product artifact.
- **Agents** (`plugins/*/agents/*.agent.md`) — 49 files, YAML-frontmatter addressable, subagent specialists. The reviewer separation pattern is the most distinctive contribution.
- **Learning docs** (`docs/solutions/**/*.md`) — 25+ files, rich YAML frontmatter (problem_type, tags, module, severity, date). The live output of the compound loop running on itself.
- **Skill references** (`plugins/*/skills/*/references/`) — schema contracts, templates, workflow references. Not user-facing but load-bearing for skill runtime.

## Exclusion candidates

- `src/` — TypeScript converter CLI, build infrastructure, not agent artifacts
- `tests/` — test fixtures and skill test harness, not runtime artifacts
- `scripts/release/` — release automation scripts
- `.github/workflows/` — CI config
- `CHANGELOG.md`, `PRIVACY.md`, `SECURITY.md` — housekeeping docs
- `plugins/coding-tutor/` — secondary plugin, minimal (3-4 skills), not the primary product

## Open questions

1. **`docs/solutions/` in the user's repo vs this repo**: The learning store at `docs/solutions/` is a convention skills write to in whatever repo the user installs the plugin in. This repo has its own self-referential `docs/solutions/` (the plugin eating its own dog food). Which matters for the dark-factory catalog — the schema/structure or the live instance?

2. **Agent count vs "51+ agents" in CONTEXT.md**: The directory shows 49 `.agent.md` files. CONTEXT.md says "51+ of them." Small discrepancy — may be stale CONTEXT.md or some agents have been removed since 2026-05-11.

3. **`skills/lfg/SKILL.md`**: The `lfg` (let's fucking go) skill is listed under `skills/` but doesn't follow the `ce-` prefix convention. Is it a meta-entry-point skill (pipeline mode) or an exception to the prefix rule? Needs sampling.

4. **`ce-work-beta` and `ce-polish-beta`**: Beta skills appear alongside stable versions. Is the beta promotion pattern (separate dir → graduation via promotion checklist) an artifact type worth cataloging separately?

5. **Headless vs interactive mode**: Many skills have explicit `mode:headless` paths for automation. Does the dark-factory catalog care about this execution posture distinction — does it signal "automation-ready" vs "human-in-the-loop-required"?

6. **Cross-platform converter targets**: The `src/converters/` pipeline means skills exist in multiple target forms (Claude native, Codex, Pi, etc.). Does the catalog track the canonical Claude-authored form, or does it need to be aware of converted forms?
