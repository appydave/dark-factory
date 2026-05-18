---
repo: compound-knowledge
github: https://github.com/EveryInc/compound-knowledge-plugin
local_path: /Users/davidcruwys/dev/upstream/repos/compound-knowledge-plugin
context_md: /Users/davidcruwys/dev/upstream/repos/compound-knowledge-plugin/.context/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 1
---

# Recon: Compound Knowledge Plugin

**Maintainer**: Austin Tedesco (austin@every.to), Every Inc.
**Version sampled**: 1.0.0 (released 2026-03-22)

## Top-level layout

```
compound-knowledge-plugin/
├── .claude-plugin/
│   └── marketplace.json
├── .context/
│   ├── CONTEXT.md          (~21KB, comprehensive system context)
│   └── context.globs.json
├── plugins/
│   └── compound-knowledge/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── AGENTS.md       (authoring conventions — the real dev guide)
│       ├── CLAUDE.md       (shim → @AGENTS.md)
│       ├── CHANGELOG.md
│       ├── README.md
│       ├── PRIVACY.md
│       ├── SECURITY.md
│       ├── LICENSE
│       ├── skills/
│       │   ├── kw-brainstorm/SKILL.md
│       │   ├── kw-plan/SKILL.md
│       │   ├── kw-confidence/SKILL.md
│       │   ├── kw-review/SKILL.md
│       │   ├── kw-work/SKILL.md
│       │   └── kw-compound/SKILL.md
│       └── agents/
│           ├── review/
│           │   ├── strategic-alignment-reviewer.md
│           │   └── data-accuracy-reviewer.md
│           └── research/
│               ├── knowledge-base-researcher.md
│               ├── past-work-researcher.md
│               └── stale-knowledge-checker.md
└── PRIVACY.md / README.md / SECURITY.md  (repo-level stubs)
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skills | `plugins/compound-knowledge/skills/kw-*/SKILL.md` | 6 | `kw-{verb}/SKILL.md` — one dir per skill | Yes — `name`, `description`, `argument-hint` | `kw-brainstorm/SKILL.md` |
| Agents (research) | `plugins/compound-knowledge/agents/research/*.md` | 3 | kebab-case noun phrase | Yes — `name`, `description`, `model: inherit` + `<examples>` blocks | `knowledge-base-researcher.md` |
| Agents (review) | `plugins/compound-knowledge/agents/review/*.md` | 2 | kebab-case noun phrase | Yes — `name`, `description`, `model: inherit` | `strategic-alignment-reviewer.md` |
| Plugin manifest | `.claude-plugin/plugin.json` | 1 | fixed | JSON (not markdown FM) | `plugin.json` |
| Dev conventions | `AGENTS.md` | 1 | fixed | None (plain markdown) | `AGENTS.md` |
| System context | `.context/CONTEXT.md` | 1 | fixed | YAML header (`generated`, `sources`, `status`) | `CONTEXT.md` |

**Total addressable artifacts**: 11 (6 skills + 5 agents)

## Skill frontmatter shape

```yaml
---
name: kw:brainstorm
description: "Brain dump and compile knowledge before structuring a plan. Use when..."
argument-hint: "[topic, brain dump, or meeting notes]"
---
```

Argument capture uses XML tag immediately after frontmatter:
```
<brain_dump> #$ARGUMENTS </brain_dump>
```

`kw:compound` and `kw:confidence` omit `argument-hint` (they operate on session context, not direct arguments).

## Agent frontmatter shape

```yaml
---
name: knowledge-base-researcher
description: "Search docs/knowledge/ for saved learnings... <example>...</example>"
model: inherit
---
```

Research agents embed `<examples>` blocks directly in the description field. Review agents embed examples inline in the YAML description string with escaped newlines. All five agents share the constraint `model: inherit` and end with "Return text only. Never write files."

## Standout patterns

### 1. Knowledge substrate is the differentiator vs compound-engineering

compound-engineering manages code artifacts (PRs, tests, specs, implementation tasks). compound-knowledge manages two *knowledge artifact types* that accumulate across sessions:

- **`plans/`** — in-flight work documents (brainstorms, type-tagged plans, execution logs). Written by skills; read by research agents.
- **`docs/knowledge/`** — durable learnings with YAML frontmatter (`type`, `tags`, `confidence`, `created`, `source`). Written only by `kw:compound` after user approval; retrieved by grep+tag in `knowledge-base-researcher`.

The folder *is* the bus. No database, no vector store, no daemon. This design is intentional — knowledge survives plugin removal and is git-tracked, plain markdown, and greppable by hand. The tradeoff is no semantic/fuzzy retrieval.

### 2. `kw:confidence` as non-destructive interrupt (no analog in compound-engineering)

compound-knowledge introduces an epistemic gate (`kw:confidence`) that can fire mid-`kw:work`, mid-`kw:plan`, or anywhere, then re-anchors ("Resuming `/kw:work` at Task 3.") after resolution. This is not a pipeline step — it's a callable utility. No equivalent exists in compound-engineering, which has a more linear plan→implement→validate→PR flow.

### 3. Work-type taxonomy auto-detection

`kw:plan` auto-classifies the request into one of five work types (Strategy / Campaign / Brief / Research / Operations) and one of three detail tiers (Quick / Standard / Deep) — without asking the user. Each type has its own "lead with" template rule: Strategy leads with recommendation (Pyramid Principle), Campaign leads with timeline, Research leads with findings, Operations leads with trigger+steps. compound-engineering has no equivalent — it's all code delivery.

### 4. Pipeline mode baked into every skill

Every SKILL.md ends with a "Pipeline Mode" block specifying behaviour when invoked with `disable-model-invocation` context: skip `AskUserQuestion`, use sensible defaults, write without confirmation, proceed automatically. This is the same convention as compound-engineering — the two plugins are designed to compose.

### 5. CLAUDE.md as shim → AGENTS.md (shared convention)

Both compound-knowledge and compound-engineering use `CLAUDE.md` as a one-line `@AGENTS.md` redirect. The authoring rules live in `AGENTS.md`, making the plugin's conventions available to Cursor, Codex, OpenCode, and other tools that read `AGENTS.md` as a standard. The CHANGELOG explicitly calls this out as a design decision matching the sibling plugin.

### 6. Agent authority split: text-only research/review, write-only orchestrating skill

All five agents end with "Return text only. Never write or delete files." Only the orchestrating skill writes. This appears as a `<critical_requirement>` block in `kw:compound`. The split is intentional: file-write authority in one place, prevents agents from clobbering each other, and allows the orchestrator to merge findings with explicit semantics (P1/P2/P3 grouping, duplicate detection before save).

## Sample artifacts

### Skill — `kw:compound/SKILL.md` (paraphrased)
Closes the loop. Scans session for 1-3 compoundable learnings (types: insight/playbook/correction/pattern), requires user approval before saving, greps `docs/knowledge/` for duplicates, launches `stale-knowledge-checker` Task agent to find contradictions, then writes approved learnings as YAML-frontmatter markdown. Pipeline Mode block present.

### Agent — `knowledge-base-researcher.md` (paraphrased)
Searches `docs/knowledge/` by keyword grep and YAML tag grep. Returns structured text with "Directly Relevant" / "Tangentially Relevant" / "No Learnings Found" sections. Flags learnings older than 90 days or marked `confidence: low`. Never writes files.

### Agent — `stale-knowledge-checker.md` (paraphrased)
Triggered by `kw:compound` after a new learning is extracted. Checks for contradicted / superseded / complementary existing entries in `docs/knowledge/`. Returns structured text only; the orchestrating skill handles all writes. Conservative bias toward "update/merge" over deletion.

## Inclusion candidates for unified discovery

- **Skills** (6): `kw:brainstorm`, `kw:plan`, `kw:confidence`, `kw:review`, `kw:work`, `kw:compound` — all primary catalog targets. YAML frontmatter present, `argument-hint` on 4/6.
- **Agents — research** (3): `knowledge-base-researcher`, `past-work-researcher`, `stale-knowledge-checker` — task agents with YAML frontmatter, distinct roles.
- **Agents — review** (2): `strategic-alignment-reviewer`, `data-accuracy-reviewer` — task agents with YAML frontmatter, P1/P2/P3 severity model.

## Exclusion candidates

- `CLAUDE.md` — shim only, one line: `@AGENTS.md`
- `AGENTS.md` — dev conventions, not an artifact; useful as recon context but not a discoverable skill/agent
- `plugin.json` — manifest metadata
- `CHANGELOG.md`, `README.md`, `PRIVACY.md`, `SECURITY.md`, `LICENSE` — standard repo hygiene
- `.context/CONTEXT.md` — system context snapshot (not shipped as a skill)
- `context.globs.json` — context generator config

## Open questions

1. **`docs/solutions/` read-only co-tenant** — The plugin reads `docs/solutions/` for engineering patterns but never writes there. Is this directory expected to be supplied by compound-engineering, or by the user? Needs clarification before modeling cross-plugin data flow.

2. **Proof integration** — "Push to Proof" is offered at every handoff point across all 6 skills. Proof is Every Inc.'s internal collaboration product. This is a hard-coded external dependency with no configuration hook. Should this be flagged as a vendor lock-in constraint in the catalog schema?

3. **No `commands/` dir (migrated away in v1.0.0)** — The CHANGELOG notes migration from `commands/kw/` to `skills/kw-*/SKILL.md`. No `commands/` directory exists in the sampled version. If David's system encounters an older install of this plugin (pre-v1.0.0), the discovery contract will find zero skills. Worth flagging for version-sensitive discovery.

4. **`docs/knowledge/` taxonomy gap** — The plugin explicitly acknowledges "no controlled vocabulary, no domain field, no SKOS broader/related — tag freedom is total." This is the inverse of David's `enrich-metadata` schema. Should the catalog note this as a structured-metadata gap that David's skills could address as an overlay?

5. **Agent naming convention is fully qualified** — Skills reference agents as `compound-knowledge:research:stale-knowledge-checker`. If the plugin is installed under a different alias or renamed, every fan-out fails silently. Worth capturing as a deployment fragility in the catalog.
