---
repo: everything-claude-code
github: https://github.com/affaan-m/everything-claude-code
local_path: /Users/davidcruwys/dev/upstream/repos/everything-claude-code
context_md: /Users/davidcruwys/dev/upstream/repos/everything-claude-code/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Everything Claude Code (ECC)

**Maintainer**: Affaan M (affaan-m)
**Version sampled**: 2.0.0-rc.1
**Anthropic Hackathon Winner**

## Top-level layout

```
everything-claude-code/
├── skills/           # 230 canonical workflow surfaces (primary artifact store)
├── agents/           # 60 specialist subagents
├── commands/         # 75 legacy slash-command shims (being phased out)
├── hooks/            # hooks.json + scripts/hooks/ (deterministic event interceptors)
├── rules/            # 110 rule files across 20 language/framework dirs
├── contexts/         # 3 context files (dev.md, research.md, review.md)
├── scripts/          # 35+ Node.js CLI scripts (ecc.js, install-apply.js, observe-runner.js, etc.)
├── manifests/        # install-modules.json (21 modules) + install-profiles.json (6 profiles)
├── mcp-configs/      # mcp-servers.json reference config
├── legacy-command-shims/ # 2 backward-compat shims
├── ecc2/             # Alpha Rust rewrite (dashboard + daemon; not production)
├── .agents/          # Cross-harness adapter: 33 skill directories for non-Claude harnesses
├── .claude-plugin/   # Claude plugin manifest (plugin.json)
├── .codex-plugin/    # Codex plugin manifest
├── examples/         # Example CLAUDE.md files per framework (django, rust, go, etc.)
├── docs/             # Architecture + spec docs (cross-harness, PLAN-PRD-PATTERN, etc.)
├── research/         # Research notes
├── plugins/          # plugins/skills/ directory (adapter layer)
├── src/              # Source (TypeScript/JS)
├── tests/            # Test suite
├── CLAUDE.md         # Harness identity file
├── AGENTS.md         # Cross-harness agent contract
├── SOUL.md           # Core identity/principles
├── EVALUATION.md     # Eval rubric
├── the-longform-guide.md / the-shortform-guide.md / the-security-guide.md
└── ecc_dashboard.py  # Python dashboard
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skills | `skills/<name>/SKILL.md` | 230 | kebab-case dir + `SKILL.md` | Yes: `name`, `description`, `origin`, optional `version` | `skills/continuous-learning-v2/SKILL.md` |
| Agents | `agents/<name>.md` | 60 | kebab-case `.md` | Yes: `name`, `description`, `tools[]`, `model` | `agents/planner.md` |
| Commands (legacy shims) | `commands/<name>.md` | 75 | kebab-case `.md` | Yes: `name`, `description`, `command: true` | `commands/evolve.md` |
| Hooks | `hooks/hooks.json` | 28 hook entries across 7 events | JSON entries with `id`, `matcher`, `description`, `command` | N/A (JSON) | `pre:observe:continuous-learning` (async, 10ms) |
| Rules | `rules/<lang>/<name>.md` | 110 | language subdir + kebab-case `.md` | None observed | `rules/common/agents.md` |
| Install Modules | `manifests/install-modules.json` | 21 | JSON objects with `targets`, `dependencies`, `cost`, `stability` | N/A (JSON) | `security`, `hooks-runtime`, `orchestration` |
| Install Profiles | `manifests/install-profiles.json` | 6 profiles | `minimal`, `core`, `developer`, `security`, `research`, `full` | N/A (JSON) | — |
| Cross-harness Skills | `.agents/skills/<name>/agents/` | 33 | Mirrors `skills/` — adapter copies for non-Claude harnesses | Varies | `.agents/skills/tdd-workflow/agents/` |
| Contexts | `contexts/<name>.md` | 3 | `dev.md`, `research.md`, `review.md` | Not observed | `contexts/dev.md` |
| Examples | `examples/<framework>-CLAUDE.md` | ~8 | Framework-specific `CLAUDE.md` templates | None | `examples/saas-nextjs-CLAUDE.md` |
| Scripts (CLI) | `scripts/*.js` | ~35 | Verb-noun pattern: `install-apply.js`, `observe-runner.js`, `doctor.js` | None | `scripts/ecc.js` (main CLI entry) |

## Standout patterns

### 1. Closed feedback loop: Hooks → Instincts → Skills

This is ECC's core differentiator. Every `PreToolUse`/`PostToolUse` event fires `observe-runner.js` (async, 10ms, 100% capture rate). A background Observer agent (Haiku) reads the resulting `observations.jsonl` and writes Instinct files — YAML-fronted markdown with `id`, `trigger`, `confidence` (0.3 → 0.9), `domain`, `scope` (project|global), and `evidence`. The `/evolve` command clusters instincts into new Skills/Agents/Commands under a per-project `evolved/` tree. The `/promote` command escalates cross-project instincts (same ID in 2+ projects, avg confidence ≥ 0.8) to the global namespace. This is a self-improving harness, not a static config bundle.

**Key constraint**: Instincts are user-local (`${XDG_DATA_HOME}/ecc-homunculus/projects/<git-remote-hash>/`), never shipped in the repo. The repo contains the mechanism; users generate the data.

### 2. Skills-first, commands-as-shims architecture

ECC explicitly demoted `commands/` to a "legacy slash-entry compatibility surface." All 75 commands exist for backward compatibility and slash-command discoverability; new work lands in `skills/`. Skills are portable across 7 harnesses (Claude Code, Codex, Cursor, OpenCode, Gemini, Copilot, Qwen) via adapter translation in `.agents/skills/`. Commands require per-harness rewriting. This is the key architectural decision: the canonical artifact is `skills/<name>/SKILL.md` with `name`/`description`/`origin` frontmatter.

### 3. AgentShield — `.claude/` as an attack surface

`skills/security-scan/SKILL.md` shells out to `npx ecc-agentshield scan`. AgentShield audits `CLAUDE.md` (hardcoded secrets, prompt injection), `settings.json` (permissive allowlists), `.mcp.json` (risky servers, npx supply chain), `hooks/` (command injection via interpolation), and `agents/*.md` (unrestricted tool access). References CVE-2025-59536 (pre-trust execution) and CVE-2026-21852 (`ANTHROPIC_BASE_URL` token exfiltration). ECC audits its own install surface — the repo ships the tool that scans itself.

### 4. Selective install via 21 modules × 6 profiles × per-harness targets

`manifests/install-modules.json` declares 21 named modules, each with `targets` (which harnesses), `dependencies`, `cost`, and `stability`. `manifests/install-profiles.json` composes them into 6 profiles. A Node-based `scripts/ecc.js` CLI orchestrates `plan → apply → doctor → repair → auto-update` against an SQLite state store at `~/.claude/.ecc-state.db`. The `ecc consult` subcommand recommends profiles from natural language queries.

### 5. Agent specialisation: role + language matrix

60 agents follow a clear matrix: role specialists (planner, architect, tdd-guide, code-reviewer, security-reviewer, harness-optimizer, loop-operator, chief-of-staff) × language reviewers/build-resolvers (TypeScript, Python, Go, Rust, Java, Kotlin, C++, C#, F#, Flutter/Dart, Django, FastAPI, Swift, HarmonyOS). Agent frontmatter includes `tools[]` (restricted list) and `model` (usually `opus` for planners/architects, implicit for others). All agents include a "Prompt Defense Baseline" block at the top — structured injection-resistance rules.

### 6. Multi-model parallel planning with Code Sovereignty

`/multi-plan` spawns Codex and/or Gemini as background workers returning text-only. Claude is the sole filesystem writer. The `architect` agent reconciles competing plans before any code is touched. Enforced by `run_in_background: true` on all external model calls and the constraint that external models have zero write access.

### 7. Three identity documents for three audiences

- `CLAUDE.md` — harness-loaded session identity for Claude Code
- `AGENTS.md` — cross-harness agent contract (Codex, OpenCode, Cursor all read this)
- `SOUL.md` — core principles statement (human-facing)

## Inclusion candidates for unified discovery

- **Skills** (`skills/*/SKILL.md`) — primary artifact; YAML frontmatter makes them machine-readable. 230 items.
- **Agents** (`agents/*.md`) — specialist subagents with `tools[]`/`model` metadata. 60 items.
- **Commands** (`commands/*.md`) — legacy but still active as slash-command entry points. 75 items.
- **Rules** (`rules/**/*.md`) — always-on guidance; grouped by language. 110 items. Worth including as a distinct artifact type.
- **Install Modules** (`manifests/install-modules.json`) — capability packaging units. 21 items.
- **Instinct mechanism** (described in `skills/continuous-learning-v2/SKILL.md`) — not a file artifact but a runtime pattern worth cataloging as a capability.

## Exclusion candidates

- `scripts/*.js` — internal CLI/tooling, not workflow artifacts
- `ecc2/` — alpha Rust rewrite, not production artifacts
- `tests/` — test suite
- `docs/` — architecture documentation (useful reference but not workflow artifacts)
- `examples/` — framework-specific CLAUDE.md templates; borderline (could be "personas" but are really examples)
- `research/` — exploratory notes
- `contexts/` — 3 files only; thin layer, probably not worth separate catalog entry
- `hooks/hooks.json` — hook *wiring* (not individually addressable artifacts); the hook scripts in `scripts/hooks/` are implementation details

## Open questions

1. **Instinct files are user-local only** — there are no example instinct files in the repo. For catalog purposes, should we document the instinct *schema* rather than trying to enumerate instinct files? The schema is in `docs/continuous-learning-v2-spec.md`.

2. **`.agents/skills/` vs `skills/`** — the `.agents/skills/` directory has only 33 of the 230 skills (adapter copies for non-Claude harnesses). Are these worth cataloging separately, or should they be noted as "adapter variants of canonical skills"? They appear to be a subset, not 1:1.

3. **`commands/` deprecation timeline** — the AGENTS.md and SKILL-PLACEMENT-POLICY are explicit that commands are being phased out. Should the catalog flag all 75 commands as "pending deprecation" during the discover phase, or wait for ECC to remove them?

4. **Rules are not YAML-fronted** — `rules/` files don't have frontmatter, just markdown. This breaks the "YAML frontmatter = addressable artifact" heuristic. Do rules get their own schema in the unified catalog, or are they treated as "always-on context" rather than invocable artifacts?

5. **AgentShield is a separate npm package** (`ecc-agentshield`) referenced from the skill — is the security scanner itself in-scope for the dark-factory catalog, or just the `security-scan` skill that invokes it?

6. **228 vs 230 skill count** — CONTEXT.md says "230 curated skills"; the actual `skills/` dir count is 230. Some marketing copy says 228. The 230 count from `find` is the authoritative number as of 2026-05-16.

7. **`examples/` CLAUDE.md files** — these are framework-specific identity templates (Django, Rust, Go, Next.js, etc.). Could be treated as "persona templates" — worth a separate artifact type or fold into skills?
