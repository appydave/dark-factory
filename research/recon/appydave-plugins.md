---
repo: appydave-plugins
github: https://github.com/appydave/appydave-plugins
local_path: /Users/davidcruwys/dev/ad/appydave-plugins
context_md: /Users/davidcruwys/dev/ad/appydave-plugins/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: AppyDave Plugins

**Maintainer**: David Cruwys (david@appydave.com)
**Version sampled**: appydave v3.46.0 / brand-dave v1.10.1 / flivideo v1.1.0

## Top-level layout

```
appydave-plugins/
├── appydave/                   # Primary plugin (60+ skills, 2 commands)
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/                 # 80 skill directories
├── brand-dave/                 # Brand-specific plugin (15 skills, 10 commands)
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
├── flivideo/                   # FliVideo plugin (1 skill, 6 commands)
│   ├── .claude-plugin/
│   ├── commands/
│   └── skills/
├── _archived/                  # consultants plugin (7 skills, 1 command) — archived 2026-04-19
├── .claude-plugin/             # marketplace.json (root-level registry)
├── .claude/                    # Project-level Claude settings + rules
├── .mochaccino/                # Mochaccino UI design workspace
├── docs/                       # Dev docs, plans, handovers
├── scripts/                    # Repo-level: create-skill.sh, validate-skills.sh
├── apps-registry.skill         # Root-level zip artifact (non-standard)
├── omi-schedule.skill          # Root-level zip artifact (non-standard)
├── relay-register.skill        # Root-level zip artifact (non-standard)
├── CONTEXT.md                  # Comprehensive system context
├── INDEX.md                    # Master skills index + orchestrator group registry
├── validate-plugin.sh          # Plugin structure validator
└── reload-plugins.sh           # Deploy source → versioned cache
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skill (directory form) | `{plugin}/skills/{name}/SKILL.md` | 96 total (80 appydave + 15 brand-dave + 1 flivideo) | `kebab-case` dir name | Yes — `name:` + `description:` only | `appydave/skills/doc-review/SKILL.md` |
| Command | `{plugin}/commands/{name}.md` | 18 total (2 appydave + 10 brand-dave + 6 flivideo) | `kebab-case.md` | Yes — `name:` + `description:` (inline, no dashes block) | `brand-dave/commands/curate-templates.md` |
| Reference files | `{plugin}/skills/{name}/references/*.md` | ~143 files across 61 reference dirs | descriptive `kebab-case.md` | No (plain markdown) | `appydave/skills/dark-factory-catalog/references/capability-recon.md` |
| Skill scripts | `{plugin}/skills/{name}/scripts/*` | ~49 files across 14 script dirs | Python (`.py`), shell (`.sh`), JS (`.js`), YAML (`.yml`) | No | `appydave/skills/lexi/scripts/run_audit.py` |
| Skill assets | `{plugin}/skills/{name}/assets/` | 1 dir found | freeform | No | `appydave/skills/screenshot-tour/assets/tour-starter.yml` |
| Skill templates | `{plugin}/skills/{name}/templates/` | 1 dir found | `kebab-case.md` | No | `flivideo/skills/po-templates/templates/*.md` |
| Plugin manifest | `{plugin}/.claude-plugin/plugin.json` | 3 active (+ 1 archived) | `plugin.json` | n/a (JSON) | `appydave/.claude-plugin/plugin.json` |
| Marketplace registry | `.claude-plugin/marketplace.json` | 1 (root) | fixed name | n/a (JSON) | `.claude-plugin/marketplace.json` |
| Root-level .skill zips | `/*.skill` | 3 | `{name}.skill` | Embedded in zip | `apps-registry.skill`, `omi-schedule.skill`, `relay-register.skill` |
| Archived skills | `_archived/consultants/skills/` | 7 | same as active | Yes | `_archived/consultants/skills/architect/` |
| Archived commands | `_archived/consultants/commands/` | 1 | same as active | Yes | `_archived/consultants/commands/` |
| Repo tooling scripts | `scripts/` | 2 | `kebab-case.sh` | No | `scripts/create-skill.sh`, `scripts/validate-skills.sh` |
| Deployment scripts | `reload-plugins.sh`, `validate-plugin.sh` | 2 | root-level bash | No | — |
| Docs / planning | `docs/*.md` | ~14 + handovers subdir | `kebab-case.md` | No | `docs/plugin-development-hell.md` |

## Standout patterns

**Orchestrator + sub-agent decomposition** is the dominant structural pattern in `appydave`. Complex review workflows (`doc-review`, `delivery-review`, `ux-review`, `codebase-audit`, `system-audit`, `near-compaction`, `omi`) are split into one orchestrator skill (fan-out coordinator) and 4–7 sub-agent skills (single-concern, independently invocable). The orchestrator's `description:` explicitly names all sub-agents; `INDEX.md` maintains a gap-detection baseline to catch drift. This is the primary architecture for any multi-dimensional analysis workflow.

**Description-as-trigger-phrase-catalogue** is enforced practice. Skills like `omi-schedule`, `dark-factory-catalog`, and `brand:brand` pack 10–20+ explicit trigger phrases and synonyms into their `description:` field. The CONTEXT.md treats the description as the only routing surface — body content is post-activation. This produces unusually verbose description fields compared to external repos.

**Script-bearing skills** (14 of 96) embed operational Python/shell/JS automation directly inside the skill directory. Scripts are invoked via instructions like "run `scripts/omi_schedule.py`" — they deploy alongside SKILL.md into the versioned cache. This makes skills that drive external tooling (OMI sync, Krisp fetch, screenshot tour, lexi audits) self-contained without depending on a separate scripts repo.

**Root-level `.skill` zip artifacts** (`apps-registry.skill`, `omi-schedule.skill`, `relay-register.skill`) are a non-standard packaging form — binary zips of a skill directory. They appear to be distribution snapshots for install-without-git-clone scenarios. These are distinct from the normal directory-form skills under `{plugin}/skills/`.

**Two-tier command frontmatter**: Commands have a short inline frontmatter (`name:` + `description:`) and then open with `# /command-name — Description` as the first heading. Skills use only `name:` + `description:` and open with `# Skill Title`. Both types enforce YAML frontmatter, but commands additionally carry the `/namespace:command-name` routing signal in the heading.

## Inclusion candidates for unified discovery

- `appydave/skills/` — 80 skill directories; primary artifact corpus; all have YAML frontmatter
- `brand-dave/skills/` — 15 skill directories; brand-workflow layer; all have YAML frontmatter
- `flivideo/skills/` — 1 skill directory (`po-templates`); small but in-scope
- `appydave/commands/` — 2 commands; both have frontmatter
- `brand-dave/commands/` — 10 commands; all have frontmatter
- `flivideo/commands/` — 6 commands; all have frontmatter
- `*/skills/*/references/*.md` — reference files attached to skills (not independently addressable, but count toward skill richness)
- `*/skills/*/scripts/*` — operational automation embedded in skills (note: `.py`, `.sh`, `.js` mixed)
- `dark-factory-catalog` skill itself — the driving artifact; should be noted as catalog infrastructure

## Exclusion candidates

- `_archived/` — intentionally decommissioned; flag as archived in catalog but don't surface as active
- `*/backup/` — original files pre-migration; not curated artifacts
- `docs/` — dev planning docs and handovers; not skills/agents/commands
- `scripts/` (root-level) — repo tooling, not plugin artifacts
- `validate-plugin.sh`, `reload-plugins.sh` — deployment infrastructure
- `.mochaccino/` — UI design workspace for the Mochaccino tool; not plugin artifacts
- `.claude/` — project Claude settings and rules; not artifacts in the dark-factory sense
- Root-level `.skill` zips — binary packaging artifacts; active skills already covered under `appydave/skills/`

## Open questions

- **Root-level `.skill` files**: Are these kept in sync with their source counterparts under `appydave/skills/`? If they diverge (version lag), discovery could surface stale content. Should recon treat them as aliases of the live directory form, or track them independently?

- **`_archived/consultants` skills**: 7 skills with intact frontmatter (`architect`, `code-reviewer`, `delegation-router`, etc.). Should these be cataloged with `status: archived` or fully excluded? The `dark-factory-catalog` procedure says note it; guidance on whether to surface archived artifacts in later phases would help.

- **Command frontmatter schema**: Commands have `name:` + `description:` frontmatter like skills, but the heading carries the invocation path (`/brand-dave:poem-slides`). Is the `name:` field the short label or the full `namespace:command` form? Sampling shows mixed — `plugin-index` uses `name: plugin-index` without namespace; `brand-dave/commands/poem-slides.md` uses `name: poem-slides`. Worth confirming for the discovery schema.

- **`flivideo/skills/po-templates/templates/`**: The templates subdir inside a skill contains 5 markdown files (`backlog.md`, `brainstorming-notes.md`, `changelog.md`, `prd-template.md`, `readme.md`). These are scaffold templates invoked by the skill at runtime, not independently addressable artifacts — but they are substantive content. Should `templates/` under a skill be counted in reference/content totals?

- **Skill count discrepancy**: `ls appydave/skills/ | wc -l` returns 80, but CONTEXT.md (generated 2026-04-24) says "60 skills". The 20-skill gap suggests significant additions since the CONTEXT.md was last regenerated. Discovery count should use live filesystem, not CONTEXT.md numbers.
