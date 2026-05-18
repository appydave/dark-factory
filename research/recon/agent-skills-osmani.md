---
repo: agent-skills-osmani
github: https://github.com/addyosmani/agent-skills
local_path: /Users/davidcruwys/dev/upstream/repos/agent-skills
context_md: /Users/davidcruwys/dev/upstream/repos/agent-skills/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Agent Skills (Addy Osmani)

**Maintainer**: Addy Osmani (Google Chrome team)
**Version sampled**: 1.0.0 (plugin.json)
**CONTEXT.md**: Present — 170 lines, extremely high-density. Covers purpose, abstractions, key workflows, design decisions, non-obvious constraints, expert mental model, scope limits, failure modes. Best CONTEXT.md encountered in the dark-factory catalog to date.

## Top-level layout

```
agent-skills/
├── .claude/
│   └── commands/       ← 7 slash commands (spec, plan, build, test, review, code-simplify, ship)
├── .claude-plugin/
│   └── plugin.json     ← Claude Code plugin manifest
├── .context/
│   └── CONTEXT.md      ← ~170-line condensed system overview
├── .gemini/
│   └── commands/       ← 7 Gemini equivalents (.toml format)
├── .opencode/
│   └── skills          ← symlink or adapter for OpenCode harness
├── agents/             ← 3 persona files + README.md
├── docs/               ← 7 harness-setup guides
├── hooks/              ← 6 bash hook scripts + 2 docs + hooks.json
├── references/         ← 5 reference checklists/patterns
├── skills/             ← 23 skill dirs, each with SKILL.md
├── AGENTS.md           ← Top-level harness-agnostic persona manifest
├── CLAUDE.md           ← Claude Code rules file
├── CLAUDE.local.md     ← Local overrides (not tracked)
├── CONTRIBUTING.md
└── README.md
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skills | `skills/<name>/SKILL.md` | 23 | `kebab-case` dir + `SKILL.md` | Yes — `name`, `description` only | `spec-driven-development/SKILL.md` |
| Personas (Agents) | `agents/<name>.md` | 3 | `kebab-case.md` flat file | Yes — `name`, `description` | `code-reviewer.md` |
| Slash Commands (Claude) | `.claude/commands/<name>.md` | 7 | `kebab-case.md` | Yes — `description` only | `ship.md` |
| Slash Commands (Gemini) | `.gemini/commands/<name>.toml` | 7 | `kebab-case.toml` | TOML, not YAML | `ship.toml` |
| Hooks | `hooks/*.sh` + `hooks/hooks.json` | 3 hook scripts (+ 2 tests + 2 docs) | `purpose-name.sh` | None — bash scripts | `session-start.sh` |
| Reference docs | `references/*.md` | 5 | `topic-name.md` | None | `orchestration-patterns.md` |
| Harness setup docs | `docs/*.md` | 7 | `harness-setup.md` | None | `cursor-setup.md` |
| Supporting files | Inside skill dirs (idea-refine) | varies | `topic.md`, `scripts/` | None | `frameworks.md`, `refinement-criteria.md` |

## Standout patterns

### 1. Anti-Rationalization Tables — the load-bearing component

Every SKILL.md contains a `## Common Rationalizations` section with a two-column Markdown table:

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need long specs, but they still need acceptance criteria. |

This is described in CONTEXT.md as "prompt engineering, not documentation" — the table embeds the rebuttal *before* the agent forms the excuse, exploiting the token-by-token generation model. Addy treats this as the single load-bearing feature that differentiates skills from ignorable best-practice docs.

### 2. Lazy-loading via description-only startup

At session startup, only `name` + `description` fields enter context. The full SKILL.md body loads only when the agent determines the skill applies. 23 skills × ~250 lines = ~5750 lines if eager-loaded; lazy loading keeps startup cost near zero. The `description` field is explicitly the discovery mechanism and must contain both what + when ("Use when…" triggers).

### 3. Three-layer composition: Command → Persona → Skill

Slash commands are the orchestration layer. Personas are roles with output formats. Skills are numbered workflows with exit criteria. The composition rules are explicit: personas do not invoke personas; commands invoke personas; personas follow skills. `/ship` is the sole endorsed multi-persona pattern (parallel fan-out with merge in one assistant turn).

### 4. Hook-driven session enforcement

`session-start.sh` injects the `using-agent-skills` meta-skill into every new session automatically (discovery flowchart the agent cannot opt out of). Two further hooks handle `WebFetch` response caching with ETag revalidation (`sdd-cache`) and code-block protection during simplification (`simplify-ignore`). Each hook fails closed gracefully.

### 5. Harness-agnostic design

The same workflow content ships adapters for Claude Code, Cursor, Gemini CLI, Windsurf, OpenCode, GitHub Copilot, Kiro. Gemini commands use `.toml` format; everything else is Markdown. Plugin manifest (`plugin.json`) declares skills/agents/commands for the Claude plugin marketplace.

### 6. Red Flags sections + Verification checklists

Every skill ends with:
- `## Red Flags` — observable signals that a step is being skipped or performed badly
- `## Verification` — checkbox list the agent must satisfy before proceeding

These make exit criteria concrete and checkable, not qualitative.

## Inclusion candidates for unified discovery

- **23 Skills** (`skills/*/SKILL.md`) — primary artifact type; YAML-frontmattered, workflow-shaped, anti-rationalization tables, verification gates
- **3 Personas** (`agents/*.md`) — YAML-frontmattered, role-with-output-format shaped
- **7 Slash Commands** (`/.claude/commands/*.md`) — orchestration entry points; YAML `description` only, body is workflow invocation prose
- **5 Reference docs** (`references/*.md`) — supporting reference material (checklists, orchestration patterns); no frontmatter but high-value structured content

## Exclusion candidates

- `hooks/` bash scripts — harness enforcement layer, not addressable artifacts for the catalog
- `docs/` harness setup guides — installation instructions, not workflow artifacts
- `.gemini/commands/*.toml` — harness-specific adapter, content mirrors `.claude/commands/`
- `CLAUDE.md`, `AGENTS.md`, `CLAUDE.local.md` — project config files, not skills/agents
- `.claude-plugin/plugin.json` — distribution metadata
- `skills/idea-refine/scripts/` — bash helper script inside a skill dir; the SKILL.md is the artifact

## Open questions

1. **Persona frontmatter shape differs from skills**: personas use `name` + `description` but the body is a system-prompt persona, not a workflow-with-exit-criteria. Should the catalog treat personas as a distinct artifact type from skills? Or subtype of skill?

2. **Gemini `.toml` commands**: same 7 commands as `.claude/commands/` but in TOML format. Does the catalog want harness-specific variants, or should it record one logical command with multiple harness representations?

3. **`idea-refine` has supporting sub-files** (`examples.md`, `frameworks.md`, `refinement-criteria.md`, `scripts/`) inside its skill dir — the only skill structured this way. Signals multi-file skills may emerge as the collection grows. Is the catalog schema ready for `SKILL.md` + optional reference files as a unit?

4. **Version pinning**: plugin.json shows `1.0.0` but git tags are the only versioning mechanism (per CONTEXT.md). The catalog has no version field in its current schema — worth adding before discovery run?

5. **`using-agent-skills`** (`skills/using-agent-skills/SKILL.md`) is a meta-skill about how to use the other skills. It's injected at session start by the hook. Catalog-worthy as an artifact? Or infrastructure like the hooks?
