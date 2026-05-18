---
repo: bmad-method
github: https://github.com/bmad-code-org/BMAD-METHOD
local_path: /Users/davidcruwys/dev/upstream/repos/BMAD-METHOD
context_md: /Users/davidcruwys/dev/upstream/repos/BMAD-METHOD/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: BMAD-METHOD

**Maintainer**: bmad-code-org (Brian "BMad" Madison)
**Version sampled**: v6.6.0 (current HEAD, 2026-04-28 release)
**Note on v4**: v4 is fully deprecated. The CONTEXT.md and CHANGELOG confirm that v6.1+ replaced the v4 YAML/XML execution engine with SKILL.md files. No v4 artifact directories exist in this checkout — the `removals.txt` file at root documents what was pruned. v4 is a reference point in docs only.

---

## Top-level layout

```
BMAD-METHOD/
├── src/
│   ├── bmm-skills/          # BMad Method Agile-AI module: 30 skills across 4 phases
│   │   ├── 1-analysis/      # Phase 1: 6 skills (agents + analysis workflows)
│   │   ├── 2-plan-workflows/ # Phase 2: 7 skills (PM agent + PRD workflows)
│   │   ├── 3-solutioning/   # Phase 3: 5 skills (architect agent + architecture)
│   │   ├── 4-implementation/ # Phase 4: 12 skills (dev agent + story/sprint/review)
│   │   └── module.yaml      # BMM module manifest (agents, dirs, config prompts)
│   └── core-skills/         # Shared cross-module: 12 skills
│       └── module.yaml      # Core module manifest
├── tools/
│   ├── installer/           # Node.js npx installer (bmad-method install)
│   │   └── modules/         # Module registry, channel resolution, marketplace
│   └── docs/
├── evals/                   # Automated eval harness (triggers.json + evals.json per skill)
├── docs/                    # Docusaurus site, 5 languages (EN, CN, FR, VI, CS)
├── .context/CONTEXT.md      # Rich condensed system snapshot (~6KB, 190 lines)
├── .claude-plugin/          # marketplace.json — Claude Code plugin descriptor
├── .augment/                # Augment AI code review guidelines
├── test/                    # Skill validation tests
└── website/                 # Docusaurus site source (Astro-like)
```

---

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Agent skills | `src/bmm-skills/*/bmad-agent-*` | 6 | `bmad-agent-{role}` | Yes — `name`, `description` | `bmad-agent-analyst/SKILL.md` |
| Workflow skills | `src/bmm-skills/*/bmad-{verb}-{noun}` | 24 | `bmad-{verb}-{noun}` | Yes — `name`, `description` | `bmad-prd/SKILL.md`, `bmad-dev-story/SKILL.md` |
| Core skills | `src/core-skills/bmad-*` | 12 | `bmad-{function}` | Yes — minimal (name+description only, some 1-line body) | `bmad-brainstorming/SKILL.md` |
| customize.toml | One per skill dir | 32 | `customize.toml` | N/A (TOML, not markdown) | `bmad-agent-analyst/customize.toml` |
| Step files | `*/steps/step-NN-*.md` | 78 | `step-NN-{phase}.md` | No — plain markdown prose instructions | `bmad-create-architecture/steps/step-01-init.md` |
| Templates | `*/assets/*.md` or `*/templates/*.md` | 6 | `{artifact}-template.md` | No | `prd-template.md`, `brief-template.md` |
| Research sub-skills | `src/bmm-skills/1-analysis/research/bmad-*-research` | 3 | `bmad-{domain}-research` | Yes (each has SKILL.md) | `bmad-market-research`, `bmad-domain-research`, `bmad-technical-research` |
| Sub-agents | `*/agents/*.md` | ~5 | `{role}.md` | No — plain prose persona + instructions | `distillate/agents/bmad-domain-research.md` |
| References | `*/references/*.md` | ~10 | `{topic}.md` | No | `facilitation-guide.md`, `validation-render.md` |
| Assets / checklists | `*/assets/*.md` (non-template) | ~8 | `{name}-checklist.md`, `{name}.html` | No | `prd-validation-checklist.md` |
| Module manifests | `src/*/module.yaml` | 2 | `module.yaml` | No (YAML) | `bmm-skills/module.yaml` — agent roster, config prompts, directories |
| Evals | `evals/bmm-skills/*/` | 1 covered | `triggers.json` + `evals.json` | No (JSON) | `bmad-product-brief/evals.json` |
| External modules (registry) | `tools/installer/modules/registry-fallback.yaml` | 5 listed | by module slug | No (YAML) | `bmad-builder`, `bmad-automator`, `cis`, `gds`, `tea` |

---

## Skills breakdown by phase

| Phase | Skills |
|-------|--------|
| Phase 1 — Analysis | bmad-agent-analyst, bmad-agent-tech-writer, bmad-document-project, bmad-prfaq, bmad-product-brief, research/* (3 sub-skills) |
| Phase 2 — Planning | bmad-agent-pm, bmad-agent-ux-designer, bmad-create-prd, bmad-create-ux-design, bmad-edit-prd, bmad-prd, bmad-validate-prd |
| Phase 3 — Solutioning | bmad-agent-architect, bmad-check-implementation-readiness, bmad-create-architecture, bmad-create-epics-and-stories, bmad-generate-project-context |
| Phase 4 — Implementation | bmad-agent-dev, bmad-checkpoint-preview, bmad-code-review, bmad-correct-course, bmad-create-story, bmad-dev-story, bmad-investigate, bmad-qa-generate-e2e-tests, bmad-quick-dev, bmad-retrospective, bmad-sprint-planning, bmad-sprint-status |
| Core (cross-cutting) | bmad-advanced-elicitation, bmad-brainstorming, bmad-customize, bmad-distillator, bmad-editorial-review-prose, bmad-editorial-review-structure, bmad-help, bmad-index-docs, bmad-party-mode, bmad-review-adversarial-general, bmad-review-edge-case-hunter, bmad-shard-doc |

**Total SKILL.md count**: 44 (across all of `src/`)

---

## Standout patterns

### 1. Skill = directory with SKILL.md + customize.toml (universal install surface)
Every skill is a folder containing `SKILL.md` (YAML frontmatter + prose instructions) and optionally `customize.toml` (TOML override schema). The SKILL.md frontmatter is minimal — just `name` and `description`. The meat is in the markdown body. This is the IDE-portable format: Claude Code, Cursor, Windsurf, Cline, and 38 other platforms install these via the npm installer into their own `.{ide}/skills/` directory.

### 2. Three-tier customization via customize.toml + sparse TOML overrides
Every skill ships a `customize.toml` that documents all configurable fields (marked DO NOT EDIT — it's the schema, not the target). Actual overrides go in `_bmad/custom/{skill-name}.toml` (team) and `.user.toml` (personal). The Python resolver (`_bmad/scripts/resolve_customization.py`) merges by shape at activation time. This is the load-bearing pattern that lets the framework be upgraded without forking.

### 3. Phase-labeled directory structure encodes SDLC sequencing
`src/bmm-skills/1-analysis/`, `2-plan-workflows/`, `3-solutioning/`, `4-implementation/` — the numbers are the phase order. Skills know their phase. This is the most explicit SDLC-stage labeling of any repo in scope so far.

### 4. Agent skills vs workflow skills: two distinct shapes
- **Agent skills** (`bmad-agent-*`): load a named persona (Mary, John, Winston, Sally, Amelia, Paige) with a TOML-driven menu of sub-skills. Stateful sessions. Identity is hardcoded; behavior is customizable.
- **Workflow skills** (`bmad-prd`, `bmad-dev-story`, etc.): single-purpose multi-step processes. Often delegate to step files and sub-agents. Stateless (fresh chat per invocation).

### 5. Step files (78 total) are the granular workflow implementation
Workflows like `bmad-create-architecture` use 8 step files (`step-01-init.md` through `step-08-complete.md`). Each step is a standalone prose instruction block, loaded sequentially. The SKILL.md orchestrates; steps contain the logic. This decomposition keeps SKILL.md readable while allowing deep per-step complexity.

### 6. External module ecosystem (5 official modules, marketplace-hosted)
The repo ships two bundled modules (`core`, `bmm`) and coordinates 5 external modules via a registry:
- `bmad-builder` (bmb) — Agent + Builder
- `bmad-automator` (baut) — Story automation (experimental/next channel)
- `bmad-creative-intelligence-suite` (cis) — Creative tools
- `bmad-game-dev-studio` (gds) — Game development agents/workflows
- `bmad-method-test-architecture-enterprise` (tea) — Master Test Architect

### 7. Eval harness per skill (emerging pattern)
`evals/bmm-skills/bmad-product-brief/` contains `triggers.json` (positive/negative activation examples) and `evals.json` (structured test cases with prompts, file fixtures, and per-expectation assertions). This is the only skill with evals currently — signals intent to expand.

### 8. `.claude-plugin/marketplace.json` — Claude Code plugin descriptor
BMAD ships a Claude Code plugin manifest listing two plugin bundles: `bmad-pro-skills` (core cross-cutting skills) and `bmad-method-lifecycle` (full phase 1-4 skills). This is the Claude Code marketplace integration surface — separate from the npx installer flow.

---

## Inclusion candidates for unified discovery

- All 44 SKILL.md files — primary artifact type, universally installable
- `customize.toml` files — configure agent/workflow behavior, part of artifact identity
- `module.yaml` files (2) — define agent roster, config prompts, directory structure per module
- Step files (78) — workflow implementation detail; include as "referenced-by" not standalone
- Templates (`*/assets/*-template.md`, `*/templates/*.md`) — output document scaffolds
- Research sub-skills (3 SKILL.md) — within `src/bmm-skills/1-analysis/research/`
- External module registry (`registry-fallback.yaml`) — enumerates 5 installable modules with their repos

---

## Exclusion candidates

- `docs/` tree — Docusaurus documentation site (EN + 4 translations); reference content, not artifacts
- `tools/installer/` — Node.js build and install tooling; not AI skills
- `website/` — Astro/Docusaurus site source
- `test/` — skill validation tests and fixtures
- `evals/` — eval harness JSON (test infrastructure, not skills); note as metadata only
- `README*.md`, `CHANGELOG.md`, `CONTRIBUTING.md` — repo governance docs
- `.github/` — CI/CD workflows
- `.augment/`, `.coderabbit.yaml` — third-party code review config

---

## Open questions

1. **Research sub-skills: are they first-class or subordinate?** `src/bmm-skills/1-analysis/research/` contains 3 skills (`bmad-market-research`, `bmad-domain-research`, `bmad-technical-research`), each with their own SKILL.md and step files. They're invocable directly but also appear as menu items in `bmad-agent-analyst`. Should they be cataloged as independent skills or as components of the analyst agent?

2. **Step files: standalone or bound artifacts?** 78 step files implement workflow logic but are never invoked directly — only via their parent SKILL.md. Do they get their own catalog entries, or are they metadata on the parent skill?

3. **Sub-agents (`*/agents/*.md`): same question.** The distillator ships `bmad-domain-research.md` and `bmad-market-research.md` as sub-agent definitions inside `src/core-skills/bmad-distillator/agents/`. These are invoked as subagents by the orchestrating skill, not directly by users. Catalog separately or as skill metadata?

4. **External modules (cis, gds, tea, bmb, baut): in scope?** They are separately maintained repos. The registry points to them; they are installable via bmad-method. Should recon cover them? Their local clones (if present) would need separate recon runs.

5. **Evals format: is this a discoverable artifact type?** Only `bmad-product-brief` has evals today but it looks like an intended pattern. Treat as infrastructure now, watch for expansion.

6. **No v4 content in this checkout — confirmed.** The `removals.txt` documents the cleanup. No yaml-agent definitions, no template files from the old execution engine exist here. The "v4 vs v6" framing from the task brief is historical — this repo is v6-only now.
