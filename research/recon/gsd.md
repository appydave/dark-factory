---
repo: gsd
github: https://github.com/glittercowboy/get-shit-done
local_path: /Users/davidcruwys/dev/upstream/repos/GSD
context_md: /Users/davidcruwys/dev/upstream/repos/GSD/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: GSD (Get Shit Done)

**Purpose**: Phase reconnaissance report for the GSD repo — artifact types, structure, and standout patterns.

**For Agents**: Use when preparing for `catalog:discover` on GSD, or when understanding GSD's mechanism for agentic-factory cluster comparisons.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

**Maintainer**: glittercowboy (TÂCHES) — GitHub handle; no personal name in the repo. Community Discord referenced.
**Version sampled**: 1.32.0 (package.json)

---

## Top-level layout

```
GSD/
├── agents/              ← 21 specialised subagent definitions
├── bin/                 ← installer CLI (install.js ~3000 lines, 223 KB)
├── commands/
│   └── gsd/            ← 60 slash commands (orchestrator entry points)
├── docs/                ← multi-language translations (ja-JP, ko-KR, pt-BR, zh-CN)
├── get-shit-done/
│   ├── bin/
│   │   └── lib/        ← 19 CommonJS domain modules (state, config, phase, etc.)
│   ├── references/     ← 25 shared reference docs loaded by agents/workflows
│   ├── templates/      ← 43 .planning/ file templates
│   └── workflows/      ← 60 workflow orchestrator files (workflow body for commands)
├── hooks/              ← 9 JS/SH hook scripts (prompt-guard, session-state, etc.)
├── sdk/
│   ├── prompts/
│   │   ├── agents/     ← 8 agent defs mirroring core (SDK subset)
│   │   └── workflows/  ← 5 workflow files for programmatic SDK use
│   └── src/            ← TypeScript ESM SDK (wraps Anthropic Claude Agent SDK)
├── scripts/            ← build/release helpers
└── tests/              ← vitest test suite
```

---

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Agents | `agents/` | 21 | `gsd-{role}.md` | Yes — YAML with `name`, `description`, `tools`, `color` | `gsd-planner.md` |
| Commands (orchestrators) | `commands/gsd/` | 60 | `{verb}-{noun}.md` | Yes — YAML with `name`, `description`, `argument-hint`, `agent`, `allowed-tools` | `plan-phase.md` |
| Workflow bodies | `get-shit-done/workflows/` | 60 | `{verb}-{noun}.md` | No — plain XML-structured prose, `<purpose>`, `<process>` blocks | `plan-phase.md` |
| Reference docs | `get-shit-done/references/` | 25 | `{topic}.md` | No — plain prose/tables; loaded via `@~/.claude/get-shit-done/references/` includes | `universal-anti-patterns.md` |
| Templates | `get-shit-done/templates/` | 43 | `{artifact}.md` | No — template Markdown for `.planning/` files (state, plan, summary, etc.) | `state.md` |
| Hooks | `hooks/` | 9 | `gsd-{purpose}.js/.sh` | No — standalone Node.js/Bash scripts; token `{{GSD_VERSION}}` rewritten at install | `gsd-prompt-guard.js` |
| Core CJS modules | `get-shit-done/bin/lib/` | 19 | `{domain}.cjs` | N/A — CommonJS modules (Node built-ins only, no external deps) | `state.cjs`, `phase.cjs` |
| SDK agents | `sdk/prompts/agents/` | 8 | `gsd-{role}.md` | Yes — mirrors core agents, subset for programmatic use | `gsd-planner.md` |
| SDK workflows | `sdk/prompts/workflows/` | 5 | `{verb}-{noun}.md` | No — streamlined for API-driven headless execution | `plan-phase.md` |

---

## The GSD Loop Shape

The canonical GSD pipeline for a single phase:

```
/gsd-new-project
  └─ questioning (dream extraction) → PROJECT.md, config.json, REQUIREMENTS.md, ROADMAP.md, STATE.md

/gsd-discuss-phase N
  └─ interactive gray-area resolution → .planning/phases/NN-name/NN-CONTEXT.md

/gsd-plan-phase N
  └─ orchestrator spawns:
       4× gsd-phase-researcher (parallel) → RESEARCH.md
       gsd-research-synthesizer           → RESEARCH-SUMMARY.md
       gsd-planner                        → NN-01-PLAN.md ... NN-M-PLAN.md
       gsd-plan-checker (loop ≤3)         → pass/fail
  └─ state update via gsd-tools.cjs

/gsd-execute-phase N
  └─ wave analysis → dependency groups
  └─ per-wave: gsd-executor per plan (parallel, fresh 200K context each)
               → atomic commits per task (--no-verify within wave)
               → NN-01-SUMMARY.md per plan
  └─ post-wave: git hook run pre-commit

/gsd-verify-work N
  └─ gsd-verifier (goal-backward, not task-backward) → VERIFICATION.md
  └─ human UAT walkthrough → UAT.md
  └─ failures spawn gsd-debugger → fix plans

/gsd-ship N
  └─ /gsd-pr-branch filters .planning/ commits → PR
```

**State spine** (`STATE.md` + `PROJECT.md` + `ROADMAP.md` + `REQUIREMENTS.md`) is loaded into every spawned agent as permanent shared memory. `.planning/` directory is the entire shared bus.

---

## Standout patterns

### 1. Two-file command split: command vs workflow

Every slash command is split across two files. The file in `commands/gsd/` is the thin entry point — it has YAML frontmatter (name, argument-hint, allowed-tools) and a short `<objective>` block with `@execution_context` includes. The heavyweight procedural body lives in `get-shit-done/workflows/`. The install process stitches them together per runtime. This means:

- The YAML frontmatter drives Claude Code's command registration
- The workflow body can be updated independently and is reused across runtimes
- The `@~/.claude/get-shit-done/workflows/plan-phase.md` include is the actual logic

This is GSD's runtime-neutrality mechanism: one payload, N adapter transforms by `bin/install.js`.

### 2. Fresh-context subagent as first-class pattern

GSD's defining architecture choice: orchestrators stay deliberately dumb (~30-40% context used). All intelligence is delegated to fresh-context subagents that each receive their own 200K (or 1M) context window, pre-loaded with only the `.planning/` artifacts they need. The orchestrator's job is to: call `gsd-tools.cjs init <workflow>` → parse JSON → spawn agents → collect results → call `gsd-tools.cjs state update`. This is explicitly chosen to avoid "context rot" — the degradation of output quality past 50-70% context utilisation.

### 3. Absent = enabled (inverse feature flags)

`config.json` uses the reverse convention: absent keys default to `true`. Users explicitly set `research: false` to disable; removing the key re-enables it. This protects quality at the cost of token spend. It's a deliberate UX decision that frequently trips users and is one of GSD's most distinctive non-obvious constraints.

### 4. Model profile matrix

A `references/model-profiles.md` table maps each agent role to a model per quality tier (`quality`, `balanced`, `budget`, `inherit`). Planners always get Opus on `quality`/`balanced`; executors get Sonnet on `balanced`; haiku for verifiers on `budget`. The orchestrator resolves the profile at init time via `gsd-tools.cjs` and injects the model name into each subagent spawn.

### 5. Vertical slice planning as the quality lever

GSD explicitly teaches "vertical slices parallelise, horizontal slices serialise." The planner is instructed toward feature-complete vertical slices (data → API → UI in one plan) rather than layer-based plans. This is the single biggest lever on wall-clock execution time and is documented as expert mental model, not just a tip.

---

## Inclusion candidates for unified discovery

- **Agents** (`agents/`) — 21 files with YAML frontmatter; clear role descriptions; the core intelligence units. Direct discovery candidates.
- **Commands** (`commands/gsd/`) — 60 files with YAML frontmatter; each describes a user-invokable workflow entry point with argument hints. Strong discovery candidates.
- **Reference docs** (`get-shit-done/references/`) — 25 files; no frontmatter but named descriptively. Include as a second-class artifact type (guidance, not invokable).
- **Hooks** (`hooks/`) — 9 files; invokable lifecycle artifacts. Include as hook-type artifacts with the `gsd-` prefix convention.

---

## Exclusion candidates

- `get-shit-done/workflows/` — workflow bodies loaded by commands; not independently invokable. Discovery should point to the command, not the workflow body.
- `get-shit-done/templates/` — `.planning/` file templates; build-time artefacts used by `gsd-tools.cjs`, not agent artifacts.
- `get-shit-done/bin/lib/*.cjs` — CommonJS runtime modules; source code, not artifacts.
- `sdk/prompts/` — mirrors the core agent/workflow set; redundant with `agents/` + `commands/gsd/` for discovery purposes. Worth a note in catalog that SDK versions exist.
- `docs/` — multi-language translations of README/guides; no artifact content.
- `scripts/`, `tests/`, `.github/` — build/CI infra.

---

## Open questions

1. **Skills vs commands**: CONTEXT.md notes that Claude Code 2.1.88+ installs into a `skills/gsd-*/SKILL.md` structure, not `commands/gsd/`. No `skills/` directory exists in the source repo — it's generated by `bin/install.js` at install time. Does the catalog want to document the *installed* artifact shape or the *source* shape? These differ structurally.

2. **Workflow body inclusion**: The `get-shit-done/workflows/` files are where the actual procedural logic lives, but they're not independently addressable — they're always loaded via `@execution_context` include from the command file. Recommend tracking as a "workflow body" sub-type under commands, not as a separate artifact type.

3. **Crypto/token branding signal**: The $GSD Solana token badge (dexscreener link, contract `dwudwjvan7bzkw9zwlbyv6kspdlvhwzrqy6ebk8xzxkv`) appears in all five language READMEs. Zero code integration confirmed by grep. Catalog evaluation should explicitly note this is community/marketing noise with no architectural implication.

4. **Maintainer identity**: The GitHub account is `glittercowboy`; the npm package author is `TÂCHES`. No personal name in the repo. Community Discord exists (linked in README). Is the maintainer identity important for the catalog schema?

5. **SDK agent overlap**: `sdk/prompts/agents/` contains 8 of the 21 core agents (the most-used ones). Worth confirming whether the SDK is considered a separate deployment target or just an API-layer copy. If separate, it may need its own catalog entry.
