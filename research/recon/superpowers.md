---
repo: superpowers
github: https://github.com/obra/superpowers
local_path: /Users/davidcruwys/dev/upstream/repos/superpowers
context_md: /Users/davidcruwys/dev/upstream/repos/superpowers/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Superpowers

**Maintainer**: Jesse Vincent (jesse@fsck.com, GitHub: obra)
**Version sampled**: 5.1.0

## Top-level layout

```
superpowers/
├── AGENTS.md              (symlink → CLAUDE.md)
├── CLAUDE.md              (primary agent instructions + contribution policy)
├── CLAUDE.local.md        (local overrides, not committed)
├── GEMINI.md              (Gemini CLI tool mapping)
├── README.md
├── RELEASE-NOTES.md       (single source; CHANGELOG.md deleted in v5.1.0)
├── CODE_OF_CONDUCT.md
├── gemini-extension.json
├── package.json
├── assets/                (images, logos)
├── docs/
│   ├── plans/
│   ├── superpowers/
│   │   ├── plans/         (5 plan docs — dated, topic-named)
│   │   └── specs/         (5 spec docs — dated, topic-named)
│   ├── testing.md
│   └── windows/
├── hooks/
│   ├── hooks.json
│   ├── hooks-cursor.json
│   ├── run-hook.cmd
│   └── session-start      (shell script — the bootstrap injector)
├── scripts/
│   ├── bump-version.sh
│   └── sync-to-codex-plugin.sh
├── skills/                (14 skill directories, each with SKILL.md)
├── tests/                 (7 test suites, 52 files total)
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── .cursor-plugin/
│   └── plugin.json
├── .opencode/
│   ├── INSTALL.md
│   └── plugins/superpowers.js
└── .context/
    └── CONTEXT.md         (~28 KB, comprehensive system context)
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skills | `skills/<skill-name>/SKILL.md` | 14 SKILL.md files | verb-gerund (`subagent-driven-development`, `writing-plans`) | YAML: `name`, `description` | `skills/test-driven-development/SKILL.md` |
| Skill reference files | within skill dirs (alongside SKILL.md) | 23 companion .md files | descriptive (`implementer-prompt.md`, `root-cause-tracing.md`) | None — plain markdown | `skills/subagent-driven-development/implementer-prompt.md` |
| Spec docs | `docs/superpowers/specs/` | 5 | `YYYY-MM-DD-<topic>-design.md` | None | `2026-04-06-worktree-rototill-design.md` |
| Plan docs | `docs/superpowers/plans/` | 5 | `YYYY-MM-DD-<feature>.md` | None | `2026-04-06-worktree-rototill.md` |
| Hooks | `hooks/` | 4 files | `hooks.json`, `run-hook.cmd`, `session-start` (shell), `hooks-cursor.json` | None — JSON/shell | `hooks/session-start` |
| Test suites | `tests/` | 7 subdirs, 52 files | by harness + scenario; `.sh` + `.mjs` + `.js` + `.jsonl` prompts | None | `tests/claude-code/test-subagent-driven-development.sh` |
| Skill test prompts | `tests/explicit-skill-requests/prompts/`, `tests/skill-triggering/prompts/` | 14 `.txt` files | scenario-named (`skip-formalities.txt`, `i-know-what-sdd-means.txt`) | None | `tests/explicit-skill-requests/prompts/skip-formalities.txt` |
| Plugin manifests | `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.opencode/` | 5 files | `plugin.json`, `marketplace.json`, `superpowers.js` | None — JSON/JS | `.claude-plugin/plugin.json` |
| Scripts | `scripts/` | 2 | `bump-version.sh`, `sync-to-codex-plugin.sh` | None — shell | `scripts/bump-version.sh` |

## Standout patterns

### 1. Description field as a behaviour-shaping API, not documentation

The `description` field in YAML frontmatter is deliberately minimal and states ONLY trigger conditions — never workflow summaries. This is documented as an empirical discovery: when descriptions summarised workflow, agents performed one review instead of two because they treated the description as the skill body and skipped reading the file. Examples:

- `using-superpowers`: "Use when starting any conversation — establishes how to find and use skills..."
- `test-driven-development`: "Use when implementing any feature or bugfix, before writing implementation code"
- `subagent-driven-development`: "Use when executing implementation plans with independent tasks in the current session"

This is a concrete, tested, anti-rationalization technique — not a stylistic preference.

### 2. Skills compose by named reference with `superpowers:` namespace prefix, not @-imports

Cross-referencing between skills uses `superpowers:test-driven-development` and `REQUIRED SUB-SKILL:` markers. `@`-imports were explicitly rejected because force-loading files consumes context before the agent decides whether the skill is relevant. The `superpowers:` prefix disambiguates from other installed plugins.

The composition chain is declared as a **state machine with terminal states**:
- `brainstorming` → only legal successor is `writing-plans` (`<HARD-GATE>` blocks all implementation skills)
- `writing-plans` → only successors are `subagent-driven-development` or `executing-plans`
- `subagent-driven-development` → ends with `finishing-a-development-branch`

Cross-cutting guards (`test-driven-development`, `systematic-debugging`, `verification-before-completion`) are invoked inside subagents at any stage, not as workflow phases.

### 3. Session bootstrap via hook injection of full skill body

`hooks/session-start` reads the entire body of `skills/using-superpowers/SKILL.md` and injects it as `additionalContext` inside `<EXTREMELY_IMPORTANT>` tags on every `startup|clear|compact` event. The skill body explicitly tells the agent: "If you think there is even a 1% chance a skill might apply, you ABSOLUTELY MUST invoke the skill." This fires before the agent forms intent for the first message. New harness support is gated on the acceptance test: "Let's make a react todo list" in a clean session must auto-trigger `brainstorming` without user explicit invocation.

### 4. Iron Laws + Rationalizations tables as empirically-derived anti-patterns

Each discipline skill (`test-driven-development`, `systematic-debugging`, `verification-before-completion`) declares one Iron Law and a Rationalizations table of verbatim phrases observed from real agent sessions — not hypothetical examples. These are treated as production code, not documentation: the CREATION-LOG.md in `systematic-debugging/` tracks what was extracted, what was left out, and why.

### 5. Subagents as context-isolation devices, not collaborators

`subagent-driven-development` dispatches three fresh subagents per task: implementer (gets full task text pasted, never reads the plan file), spec-compliance reviewer (explicitly distrusts the implementer's report), code-quality reviewer. The pattern note: subagents are about *what is NOT in their context*, not what is. The implementer never reads the plan file because that would pollute context with unrelated tasks.

### 6. TDD applied to skill authoring itself

`writing-skills/SKILL.md` defines skill creation as RED-GREEN-REFACTOR applied to documentation: RED = run a subagent through a pressure scenario without the skill and document baseline rationalisations verbatim; GREEN = write minimal SKILL.md addressing those specific rationalisations; REFACTOR = re-run, find new rationalisations, add counters, expand Red Flags table.

### 7. Multi-harness plugin architecture

One skill library, 5 harness adapters: Claude Code (`.claude-plugin/`), Codex CLI/App (`.codex-plugin/`), Cursor (`.cursor-plugin/`), Gemini CLI (`gemini-extension.json` + `GEMINI.md`), OpenCode (`.opencode/plugins/superpowers.js`). Each harness has its own `hooks.json` or equivalent. `AGENTS.md` is a symlink to `CLAUDE.md`; `GEMINI.md` is separate due to tool mapping differences. `scripts/bump-version.sh` keeps all manifests in sync.

### 8. Live spec + plan artefacts as part of the repo

`docs/superpowers/specs/` and `docs/superpowers/plans/` contain the superpowers repo's own design artefacts — eating its own dog food. Five dated specs and five dated plans document the evolution of the tool's own features.

### 9. Zero-dependency philosophy

No `node_modules` in production. v5.0.2 ripped out Express/Chokidar/WebSocket (~1200 LOC). CLAUDE.md's `What We Will Not Accept` section auto-rejects PRs that add third-party deps unless they add a new harness. This is a hard design constraint, not a preference.

### 10. Test harness parses session transcripts (.jsonl), not user-facing output

`tests/claude-code/` scripts run sessions and assert against the `.jsonl` transcript — checking for skill-tool invocations, subagent dispatches, TodoWrite usage, files created, commits made. This is the only way to verify whether the skill actually triggered vs. the agent happening to produce correct output.

## Sample artifacts

### Skill (SKILL.md with YAML frontmatter)
`skills/subagent-driven-development/SKILL.md`:
- YAML: `name: subagent-driven-development`, `description: Use when executing implementation plans...`
- Body: graphviz `digraph` flowcharts for when-to-use and the per-task loop, model selection guide, four implementer status codes (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED), Red Flags table, Integration section cross-referencing 4 other skills

### Skill reference prompt
`skills/subagent-driven-development/implementer-prompt.md`:
- Plain markdown, no frontmatter
- Provides the copy-paste template for dispatching an implementer subagent — includes exactly what context to inject and what not to (don't include plan file path, paste full task text)

### Spec doc (live artefact)
`docs/superpowers/specs/2026-04-06-worktree-rototill-design.md`:
- No frontmatter; markdown with problem statement, goals, failure modes, design decisions
- Date-prefixed, topic-named, version-tracked via git commits

### Plan doc
`docs/superpowers/plans/2026-04-06-worktree-rototill.md`:
- No frontmatter; implementation steps as checkboxes, each 2-5 minutes, TDD steps explicit
- Header includes `REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development` note

### Test prompt (skill trigger test)
`tests/explicit-skill-requests/prompts/skip-formalities.txt`:
- Plain text prompt simulating a user trying to bypass the skill workflow
- Used by shell test runners to verify the agent refuses to skip and invokes the correct skill

### Hook
`hooks/session-start`:
- Shell script (POSIX-safe; `printf` not heredoc, due to bash 5.3+ regression)
- Reads `skills/using-superpowers/SKILL.md`, strips frontmatter, wraps in `<EXTREMELY_IMPORTANT>` tags, outputs as `additionalContext` JSON

## Inclusion candidates for unified discovery

- **Skills** (`skills/*/SKILL.md`) — 14 files, YAML frontmatter, named with verb-gerunds, clear trigger descriptions. Primary artifact type; these are what the methodology IS.
- **Skill reference prompts** (companion files alongside SKILL.md) — 23 files, plain markdown. High value because they contain the actual dispatch templates and reference guides used inside skills. Discoverable via parent skill's cross-references.
- **Session-start hook** (`hooks/session-start`) — the mechanism that makes skills auto-trigger. Single file. Critical for understanding how the bootstrap works.
- **Spec docs** (`docs/superpowers/specs/`) and **plan docs** (`docs/superpowers/plans/`) — 10 files total. Demonstrate what brainstorming + writing-plans produce in practice. Useful as output-format examples.

## Exclusion candidates

- `scripts/` — operational tooling (version bumping, plugin sync), not methodology artifacts
- `assets/` — images/logos
- `tests/` — test harness for the plugin itself, not reusable methodology content (though test prompts in `tests/explicit-skill-requests/prompts/` and `tests/skill-triggering/prompts/` are interesting as anti-rationalization examples)
- Plugin manifests (`.claude-plugin/`, `.codex-plugin/`, etc.) — harness configuration, not methodology
- `RELEASE-NOTES.md` — changelog
- `CLAUDE.md` / `AGENTS.md` — contribution policy and PR rejection criteria, not methodology artifacts for the catalog
- `docs/testing.md` — test harness documentation for contributors

## Open questions

1. **Are skill reference prompts (`implementer-prompt.md`, `spec-reviewer-prompt.md`, etc.) first-class catalog entries or subordinate to their parent SKILL.md?** They have no frontmatter and no independent discovery mechanism — they're only reached via SKILL.md cross-references. Likely: catalog SKILL.md as primary, note companion files in its entry.

2. **CREATION-LOG.md in `systematic-debugging/`** — is this a pattern other skills should follow? Only one skill has it. It documents why content was included/excluded during the TDD-for-skills process. Useful metadata for catalog; probably not a separate artifact type.

3. **The test prompts (`tests/explicit-skill-requests/prompts/*.txt`, `tests/skill-triggering/prompts/*.txt`)** are effectively named anti-rationalization scenarios — "skip-formalities.txt", "i-know-what-sdd-means.txt". They encode edge cases where agents try to bypass skills. Should these be surfaced in the catalog as a distinct artifact type ("pressure scenarios") or treated as test infrastructure?

4. **`docs/superpowers/specs/` and `docs/superpowers/plans/`** — these are the repo's own design artefacts, not reusable templates. They demonstrate what the methodology produces but aren't methodology artifacts themselves. Recommend: include as output examples only, not as catalog entries.

5. **No agents/ directory** — superpowers does not define named agents. Subagents are dispatched via dispatch-template prompts embedded in skill reference files, not as standalone agent definitions. The catalog schema may need a "dispatch template" artifact type to distinguish these from skills.

6. **Multi-harness plugin files** — `.cursor-plugin/`, `.codex-plugin/`, `.opencode/plugins/superpowers.js` contain harness-specific wiring, not methodology. But they're interesting for understanding how the bootstrap adapts across harnesses. Out of scope for methodology catalog, but relevant to the multi-harness pattern study.
