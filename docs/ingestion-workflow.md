# Ingestion Workflow

**Purpose**: Step-by-step procedure for taking an upstream artifact (or a cluster of related artifacts) from `research/` and producing a canonical version in `canonical/<type>/<name>/`.

**For Agents**: This is the recipe. Read once. Apply per backlog item.

**Created**: 2026-05-18
**Last Updated**: 2026-05-18

---

## The flow

```
backlog item → identify origins → harvest verbatim → write provenance →
rewrite SKILL.md in David's voice → validate → ratify → register
```

## Step 1 — Read the backlog item

`backlog/<date>-<slug>.md` should tell you:
- **Target**: `dark-factory:<type>:<name>` — what to produce
- **Distillation source**: which `research/distillations/<cluster>-<sub-cluster>.md` to start from
- **Origins to harvest**: which upstream files to pull from
- **Research consults**: which `research/evaluations/*.md` files inform decisions
- **Acceptance criteria**: what "done" means for this item

If any of those are missing or unclear, ask the PO (write a question into the backlog item under `## Questions`) before executing.

## Step 2 — Read the research context

Before touching anything:

1. Read the distillation draft. It already names the winner mechanism + folded-in ideas + complexity annotations (per the v0.0.6 template).
2. Read each consulted evaluation file. They carry quality scores, adoption fit, mineable phrases, and craft notes.
3. Skim `research/insights.md` for any captured craft bits relevant to this artifact type.

## Step 3 — Locate the origin files on disk

For each origin in the distillation's source list:

1. Find the actual file path at `~/dev/upstream/repos/<repo>/...`
2. Verify it still exists (the upstream may have moved files since recon).
3. If moved: update the path; record the move in your backlog notes.
4. If missing: flag in `backlog` and ask PO whether to proceed without that origin.

## Step 4 — Harvest verbatim copies

Create the canonical folder structure:

```bash
mkdir -p canonical/<type>/<name>/{_source,references,scripts}
```

For each origin, copy the source file verbatim:

```bash
cp <source_path> canonical/<type>/<name>/_source/<source_repo>--<original-filename>.md
```

If the source has companion files (references, scripts) that you'll lift ideas from:

```bash
cp -r <source_dir>/references canonical/<type>/<name>/_source/<source_repo>--<name>--references/
```

**Verbatim means verbatim.** No edits, no whitespace normalization, no link rewriting. The `_source/` files are evidence, not artifacts you'll iterate on.

## Step 5 — Write provenance.json (draft)

Use the schema in `provenance-spec.md`. At this stage:

- `rewrite_status`: `"draft"` (you haven't rewritten yet)
- `version`: `1`
- `origins[]`: one entry per harvested file, with `kept` / `modified` / `set_aside` initially populated from the distillation draft. You'll refine `modified` after you actually write the SKILL.md.

Validate the schema with the checklist at the bottom of `provenance-spec.md`.

## Step 6 — Write SKILL.md in David's voice

Follow `canonical-form-spec.md`. The high-leverage moves:

1. **Frontmatter first.** Copy `argument-hint` and `allowed-tools` from the strongest origin source (usually the winner mechanism). Don't invent.
2. **Description as trigger.** Write the description LAST after the body is written — or write a placeholder up front and refine after. The description fires the skill; getting it wrong means the skill never loads.
3. **Body in David's pattern.** One-line purpose → behavior → (optional) sub-agents table → output → anti-patterns. Operator voice. Tables for comparable data.
4. **Reference David's existing similar skills** at `~/dev/ad/appydave-plugins/appydave/skills/` for tone. Don't copy-paste; mimic the rhythm.

Update `rewrite_status` to `"in-style"` when you're done writing.

## Step 7 — Refine provenance entries

Now that the rewrite is done:
- For each origin, update `modified[]` with what you actually changed
- For each origin, update `set_aside[]` with what you deliberately did NOT include
- Refine `kept[]` if your rewrite ended up using different elements than the distillation suggested

## Step 8 — Validate

Run `python3 tools/style-check.py canonical/<type>/<name>/` — it covers the style/layout items below. Provenance-content items stay manual until `tools/verify-provenance.py` exists:

- [ ] `provenance.json` parses + all required fields present
- [ ] Every origin's `verbatim_copy` file exists
- [ ] No orphan files in `_source/` (every file referenced by some origin)
- [ ] SKILL.md frontmatter has all 4 fields (name, description, argument-hint, allowed-tools)
- [ ] Description is trigger-only, ≤2 sentences, 3+ trigger phrases
- [ ] Body has the David-style sections (purpose, behavior, output, anti-patterns)
- [ ] No stack-specific terminology in body
- [ ] Body ≤400 lines OR uses references/ for overflow

If anything fails: fix before marking ratified.

## Step 9 — Ratify

Update `provenance.json`:

```json
{
  "rewrite_status": "ratified",
  "rewrite_date": "<today>"
}
```

## Step 10 — Register in canonical/INDEX.md

Append a row to the registry:

```markdown
| <name> | <type> | <one-line description> | <n> origins | ratified <date> |
```

## Step 11 — Close the backlog item

Rename `backlog/<date>-<slug>.md` → `backlog/done/<date>-<slug>.md` and add a `## Result` section at the bottom:

```markdown
## Result

Ratified `canonical/<type>/<name>/` on <date>. 
- Origins harvested: <n>
- Source files: <list>
- Notable decision: <one-line>
```

## Edge cases

**Multiple winners (no single winner emerged in distill)**: produce TWO canonicals if they're genuinely doing different jobs; or pick one and document the other's mechanism in `set_aside[]` with reasoning. Don't merge two into a Frankenstein.

**Origin file doesn't exist anymore**: still record the origin in provenance.json with `source_path` and the date harvested, but mark `verbatim_copy: "[origin removed before harvest]"`. Flag in backlog item — PO may want to re-run recon on that repo.

**The canonical ends up being entirely David's invention**: that's fine, but the provenance must still record what you considered and chose NOT to use. A canonical with `origins: []` is forbidden — if you literally invented something, log it as a "from scratch" entry with no kept/modified, all set_aside (= you looked at this but used nothing from it).

**Style-check disagrees with you**: the spec wins. If the rule itself is wrong, propose an amendment to `canonical-form-spec.md` as a separate backlog item; don't violate the spec to ship.
