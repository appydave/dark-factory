# Canonical Form Spec

**Purpose**: Defines what a canonical skill, agent, or command in `canonical/` MUST look like. This is the contract that makes the library coherent, scannable, and Claude-Code-installable as-is.

**For Agents**: Read before authoring any artifact in `canonical/`. Validate after authoring with `tools/style-check.py` or by manual review against the checklist at the bottom.

**Created**: 2026-05-18
**Last Updated**: 2026-05-18

---

## File layout per canonical artifact

```
canonical/skills/<skill-name>/
├── SKILL.md             ← the rewrite in David's voice + style
├── provenance.json      ← origin trace (see provenance-spec.md)
├── _source/             ← verbatim copies of every origin file
│   └── <repo>--<file>.md
├── references/          ← David's reference docs (optional, only if SKILL.md > ~400 lines)
│   └── <topic>.md
└── scripts/             ← scripts referenced by SKILL.md (optional)
    └── <name>.sh
```

Same shape for `canonical/agents/<name>/` and `canonical/commands/<name>/`.

## SKILL.md frontmatter

ALL applicable fields. Copy from origin source — do not invent.

```yaml
---
name: <kebab-case-slug>
description: <trigger-only, ≤2 sentences. "Use when..." phrasing. NOT a workflow summary.>
argument-hint: <CLI-style hint if the skill takes args, e.g. "[pr-url]". Omit if none.>
allowed-tools: <comma-separated bash commands the skill needs without runtime prompting>
---
```

**Why all four**: missing `allowed-tools` makes the skill prompt on every bash command at runtime. Missing `argument-hint` makes the user think it takes no args. These came up as gaps when we built `pr-lifecycle` in the research phase.

## Description discipline

**Bad** (workflow summary — the LLM decides it can skip the body):
> "Workflow for writing skills"
> "Reviews code for quality, security, and style issues"

**Good** (trigger condition — the LLM fires when condition matches):
> "Use when user is about to write code without tests"
> "Use when: 'review this PR', 'check for bugs', 'is this ready to merge'"

Include 3-6 explicit trigger phrases in the description. The description IS the routing program — there is no separate classifier.

## Body structure

David's pattern (from his existing review/orchestration skills):

```markdown
# <Title>

One-line purpose statement — what this fires to accomplish.

## Behavior

(What the skill does, in operator voice. Imperatives. No marketing.)

## Sub-agents / Specialists (only if it's an orchestrator)

| Specialist | Concern | Output |
|------------|---------|--------|
| ... | ... | ... |

## Output

(What the skill produces. Format, location, structure.)

## Anti-patterns

(2-4 bullets — what NOT to do. Concrete examples beat abstract rules.)
```

Optional sections after the core:
- `## References` — links to `references/<topic>.md` files (only if the body is getting heavy)
- `## Scripts` — index of scripts in `scripts/`
- `## Provenance` — pointer to `provenance.json` (the actual data lives there; the body just references it)

## Voice rules

1. **Terse > polished.** Operator tone. Single-sentence purpose statements beat paragraphs.
2. **No marketing.** Skills don't sell themselves; the description triggers; the body executes.
3. **Imperatives.** "Do X. Then Y." Not "This skill will help you do X."
4. **Tables for structure.** Specialists, anti-patterns, criteria — tabular wherever the data is comparable.
5. **Stack-agnostic.** Never name a language/framework in the body unless the skill is genuinely stack-specific (which it shouldn't be — see anti-patterns).

## Anti-patterns in canonical form

- **Workflow summary in description** (forces lazy-load to bypass the body)
- **Stack-named in body** ("Run `npm test`" — should be "Run the project's test command")
- **Inline source content** without a corresponding `_source/` verbatim copy (breaks provenance)
- **Missing `allowed-tools`** when the skill calls bash (breaks autonomous runs)
- **In-place edits to a ratified canonical** (use a versioned rewrite instead)
- **Forking the SKILL.md and discarding the original** (the verbatim source MUST be preserved in `_source/`, even if the rewrite is total)

## Ratification checklist

Before marking a canonical artifact as `ratified` (in provenance.json `rewrite_status`):

- [ ] Frontmatter has `name`, `description`, `argument-hint` (or noted N/A), `allowed-tools`
- [ ] Description is trigger-only, ≤2 sentences, contains 3+ trigger phrases
- [ ] Body is ≤400 lines OR reference files are used for overflow
- [ ] Every origin in `provenance.json` has a corresponding `_source/<repo>--<file>.md`
- [ ] `provenance.json` validates per `provenance-spec.md`
- [ ] No stack-specific terminology in the body (or noted intentional exception)
- [ ] No anti-patterns from the list above

## Versioning a ratified artifact

When a ratified canonical needs change:

1. Bump version field in provenance.json: `version: 2`
2. Append to `provenance.json` `version_history[]` with what changed and why
3. Optionally: keep `SKILL.md.v1` for diff reference (rare — usually `git log` is enough)

Never edit a ratified artifact in place without bumping version.
