---
repo: spec-kit
github: https://github.com/github/spec-kit
local_path: /Users/davidcruwys/dev/upstream/repos/spec-kit
context_md: /Users/davidcruwys/dev/upstream/repos/spec-kit/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Spec Kit

**Maintainer**: GitHub (Den Delimarsky lead; moved to Anthropic late 2025 — project now on smaller GitHub team)
**Version sampled**: 0.8.11 (released 2026-05-15)

## Top-level layout

```
spec-kit/
├── .context/               # CONTEXT.md (30 KB system context, auto-generated via /system-context)
├── .github/                # CI, issue templates, GitHub Actions skills
├── docs/                   # MkDocs documentation site
├── extensions/             # Bundled + community extension definitions (git, selftest, template)
├── integrations/           # Integration catalog JSON (community catalog)
├── media/                  # Images/logos
├── newsletters/            # Release newsletters
├── presets/                # Bundled presets (lean, scaffold, self-test)
├── scripts/
│   ├── bash/               # 5 shell helper scripts
│   └── powershell/         # 5 PowerShell equivalents
├── src/specify_cli/        # Python CLI source
│   ├── integrations/       # 30 harness integration classes (Python)
│   └── workflows/          # Workflow runtime engine
├── templates/
│   ├── commands/           # 9 core command prompt templates (Markdown)
│   └── *.md                # 5 artifact document templates (spec, plan, tasks, constitution, checklist)
├── tests/                  # pytest suite
└── workflows/speckit/      # 1 bundled workflow definition (YAML)
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Command templates (core) | `templates/commands/` | 9 | `<phase>.md` (e.g., `specify.md`, `plan.md`) | YAML — `description`, `handoffs`, `scripts` keys | `specify.md` |
| Document templates | `templates/*.md` | 5 | `<artifact>-template.md` | None (plain Markdown with placeholder comments) | `spec-template.md` |
| Integration classes | `src/specify_cli/integrations/<key>/` | 30 | one dir per harness, `__init__.py` inside | N/A (Python class) | `claude/__init__.py` |
| Extension definitions | `extensions/<name>/extension.yml` | 3 bundled | `extension.yml` per extension | YAML — `schema_version`, `extension`, `requires`, `provides`, `hooks` | `git/extension.yml` |
| Extension commands | `extensions/<name>/commands/` | 7 total | `speckit.<ext>.<cmd>.md` | YAML `description` | `speckit.git.feature.md` |
| Preset definitions | `presets/<name>/preset.yml` | 3 bundled | `preset.yml` per preset | YAML — `schema_version`, `preset`, `requires`, `provides`, `tags` | `lean/preset.yml` |
| Preset commands | `presets/<name>/commands/` | 9 total | `speckit.<phase>.md` | Inherits command format | `lean/commands/speckit.specify.md` |
| Preset templates | `presets/<name>/templates/` | 2 (scaffold) | `<artifact>.md` | None | scaffold templates |
| Workflow definitions | `workflows/<name>/workflow.yml` | 1 bundled | `workflow.yml` | YAML — `schema_version`, `workflow`, `requires`, `inputs`, `steps` | `speckit/workflow.yml` |
| Scripts (Bash) | `scripts/bash/` | 5 | `<action>.sh` | None (shell) | `create-new-feature.sh` |
| Scripts (PowerShell) | `scripts/powershell/` | 5 | `<action>.ps1` | None (PS) | `create-new-feature.ps1` |
| Community catalogs | `integrations/catalog.community.json`, `extensions/catalog.community.json`, `presets/catalog.community.json` | 3 files | JSON arrays | N/A | `extensions/catalog.community.json` |

## Standout patterns

### 1. Compile-on-install multi-harness adapter (the key architectural move)

Spec Kit does NOT ship 30 harness-specific copies of each command. Instead it ships one canonical Markdown source per command in `templates/commands/` and compiles it at `specify init` time into the target harness's format. Each harness has a Python integration class in `src/specify_cli/integrations/<key>/` declaring its `folder`, `commands_subdir`, command format (`markdown` | `toml` | `yaml`), argument placeholder (`$ARGUMENTS` vs `{{args}}`), and context file (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`). The compile step rewrites `__SPECKIT_COMMAND_*__` and `{SCRIPT}` placeholders, injects harness-specific frontmatter flags (e.g., `user-invocable`, `disable-model-invocation` for Claude; `mode:` for Copilot), and drops files into the right subdirectory. This one-source-many-targets pattern means 30+ harnesses × 9 commands share a single canonical template, not 270 divergent files.

### 2. Pinned phase pipeline with human-approval gates and lifecycle hooks

The methodology is embodied as a fixed command chain: `constitution → specify → clarify → plan → tasks → analyze → implement → taskstoissues`. These are not suggestions; the artifact chain is a directed graph where each command's inputs are the previous command's outputs (`spec.md → plan.md → tasks.md`). The bundled `workflow.yml` automates the chain with explicit `gate` steps (human approval before proceeding). The `git` extension injects `before_*` / `after_*` lifecycle hooks at every phase boundary — branch creation before `specify`, auto-commit after each phase — without modifying the core templates. Hooks use an `optional: true/false` flag; mandatory hooks block execution until resolved.

### 3. Resolution stack (overrides > presets > extensions > core)

Template resolution at install time follows an explicit priority order. Presets replace/prepend/append/wrap core templates using a `strategy` field. Extensions add new commands and hooks without touching existing ones. The `lean` preset ships stripped-down versions of all 9 core commands (no clarify, checklist, or analyze) that replace the core templates at install. Teams can stack multiple presets and extensions; the CLI manages precedence without requiring any forking of the repo.

### 4. Dual-script strategy (Bash + PowerShell parity)

Every helper script ships in both `scripts/bash/` and `scripts/powershell/` with matching semantics. Command templates reference the correct variant via the `scripts: sh: / ps:` frontmatter keys, resolved by the integration layer at install based on the host OS. The templates expose the script path via the `{SCRIPT}` placeholder, which gets rewritten to the agent-correct invocation during compile.

### 5. Specs-as-source-of-truth inversion

Generated specs (`spec.md`, `plan.md`, `tasks.md`) live inside the repo under `specs/<NNN-feature-name>/` alongside the code they govern. The spec is the durable artifact; the implementation is regenerated from it. The `analyze` command is a read-only cross-artifact consistency gate that must pass before `implement` runs. This "code serves specifications" inversion is load-bearing — the MUST/SHOULD vocabulary in command templates is behavioral constraint on the LLM, not documentation.

## Inclusion candidates for unified discovery

- **Command templates** (`templates/commands/`) — the 9 core SDD phase commands; these are the primary artifacts that agents invoke
- **Document templates** (`templates/*.md`) — output artifact shapes (spec, plan, tasks, constitution, checklist); define the SDD output contract
- **Extension definitions** (`extensions/*/extension.yml`) — bundled extensions that wrap the phase pipeline with hooks and additional commands
- **Extension commands** (`extensions/*/commands/*.md`) — additional commands contributed by extensions (e.g., `speckit.git.feature`, `speckit.git.commit`)
- **Preset definitions** (`presets/*/preset.yml`) — bundled preset manifests describing what they override
- **Preset commands** (`presets/*/commands/*.md`) — lean/stripped variants of core commands
- **Workflow definitions** (`workflows/*/workflow.yml`) — automated multi-step orchestration with gate steps
- **Scripts** (`scripts/bash/`, `scripts/powershell/`) — shell helpers invoked by command templates during pipeline execution

## Exclusion candidates

- `src/specify_cli/` Python source — this is the CLI bootstrap tool, not the methodology artifacts; it installs files, it doesn't run the workflow
- `tests/` — pytest suite, not SDD artifacts
- `docs/` — MkDocs documentation site (HTML/Markdown for humans, not for agents)
- `media/`, `newsletters/` — brand/marketing assets
- `integrations/catalog*.json`, `extensions/catalog*.json`, `presets/catalog*.json` — community catalog registries (metadata about external things, not the things themselves)
- `.github/workflows/` — CI pipeline, not Spec Kit artifacts
- `pyproject.toml`, `CHANGELOG.md`, `DEVELOPMENT.md` — project maintenance files

## Open questions

1. **Community extensions/presets**: The `catalog.community.json` files point to external repos (e.g., "Time Machine extension", "Architecture Workflow extension", "Agent Governance extension"). These community artifacts are not in this repo — are they in scope for the catalog? If yes, this recon covers only the bundled set.

2. **Integration classes vs. installed artifacts**: The 30 Python integration classes in `src/specify_cli/integrations/` define how templates compile per harness but are not themselves SDD artifacts. However, each installed result (e.g., `.claude/skills/speckit-plan/SKILL.md`) IS the per-harness artifact. Should the catalog track the source template, the compiled output, or both?

3. **`AGENTS.md` at repo root**: Root-level `AGENTS.md` provides project-wide agent context for Codex/OpenAI harnesses — similar to `CLAUDE.md` for Claude Code. Is this a catalogable "persona/context file" artifact type or excluded as a README-equivalent?

4. **Workflow runtime engine** (`src/specify_cli/workflows/`): The `specify workflow run` CLI command can drive the full pipeline headlessly. Is this relevant for dark-factory agentic-loop classification (it is the closest thing to autonomous orchestration in this repo)?

5. **Preset compose strategies**: The `strategy: replace/prepend/append/wrap` field on preset `provides` items creates a layering system at install time. Should this be modeled in the catalog schema as a composition axis, or treated as implementation detail of the preset artifact?
