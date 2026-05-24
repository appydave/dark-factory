---
repo: claude-code-workflow-creator
github: https://github.com/ray-amjad/claude-code-workflow-creator
local_path: /Users/davidcruwys/dev/upstream/repos/claude-code-workflow-creator
context_md: none (uses README.md instead)
recon_date: 2026-05-25
recon_iteration: 1
status: recon-only — discover/distill/evaluate pending
---

# Recon: Claude Code Workflow Creator (Ray Amjad)

**Maintainer**: Ray Amjad (independent — produces Claude Code educational content)
**Version sampled**: HEAD as of 2026-05-25
**Source**: companion to Ray Amjad's introduction video "Anthropic Just Dropped the Update Claude Code Always Needed" (transcript at `x.txt` in repo root)

## Why this repo matters

The Workflow Tool was added to Claude Code in May 2026 as a deterministic multi-agent orchestrator. It is **unannounced and undocumented officially** as of recon date. This skill is the single most complete authoring resource we've found for the new tool. It carries:

- The file format (with the otherwise-undocumented globals like `budget`, the `meta` block shape, agent options)
- The judgement calls (when to use a workflow vs a skill vs a single agent)
- A tested authoring procedure (steps from goal → shape → script → validation)
- Six complete runnable example workflows
- A linter for the parser's hard rules
- Pattern library: fan-out, pipeline, loop-until-budget, judge panel, nested workflow, adversarial verify

For Dark Factory specifically: this skill is directly applicable. It maps cleanly to our `Alex` (Prompt Architect) persona — Alex would use this skill internally when designing new workflows.

## Top-level layout

```
claude-code-workflow-creator/
├── SKILL.md                              ← the skill entry point (detailed procedure)
├── README.md                             ← install + usage
├── references/
│   ├── api-reference.md                  ← every global, option, cap, constant
│   └── patterns.md                       ← copy-paste orchestration patterns
├── assets/
│   ├── templates/                        ← 3 starter shapes
│   │   ├── fan-out.template.js
│   │   ├── pipeline.template.js
│   │   └── loop.template.js
│   └── examples/                         ← 6 complete runnable workflows
│       ├── README.md                     ← maps each example to a technique
│       ├── triage-sentry.js              ← MCP + filter + per-issue pipeline
│       ├── dead-code-sweep.js            ← loop-until-dry with safety cap
│       ├── personalize-outreach.js       ← model-per-phase (haiku/opus), pipeline streaming
│       ├── api-contract-drift-detector.js
│       ├── implement-and-review.js       ← adversarial verify pattern
│       ├── review-branch.js
│       └── customer-feedback-theme-extractor.js
└── scripts/
    └── validate-workflow.mjs             ← linter against parser hard rules
```

## Artifact types found

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Skill | `SKILL.md` (root) | 1 | `kebab-case` (the repo itself is the skill folder) | Yes — `name`, `description` | `SKILL.md` |
| References | `references/*.md` | 2 | `kebab-case.md` | None | `api-reference.md` |
| Templates | `assets/templates/*.template.js` | 3 | `<shape>.template.js` | JS doc-comment | `fan-out.template.js` |
| Example workflows | `assets/examples/*.js` | 6 | `kebab-case.js` | JS `meta` block | `triage-sentry.js` |
| Validation script | `scripts/*.mjs` | 1 | `validate-<thing>.mjs` | Shebang + comment | `validate-workflow.mjs` |

## Skill anatomy

The `SKILL.md` follows a steps-based procedure pattern:

- **Step 0** — Confirm the Workflow tool is available (env var check)
- **Step 1** — Decide whether a workflow is even the right tool (avoid over-reach)
- **Step 2** — Find the shape of the job (fan-out / pipeline / loop / hybrid)
- (Additional steps continue — script structure, schema design, validation)

The skill explicitly refers to reference files using "read the file when the step says so" pattern — not loaded upfront, loaded on demand. This is a clean separation that minimizes context cost when the skill is invoked but the deep material isn't needed.

## Mineable phrases / craft notes (initial pass)

- *"The workflow file IS the orchestrator"* — frames the architectural shift from model-wrapper to code-wrapper
- *"Only the leaf agent() calls spend model tokens"* — sharp framing of where cost lives
- *"A workflow earns its cost when all of these are true: parallel or multi-stage, deterministic and resumable, isolated fresh-context advantage"* — gating criterion before authoring
- *"Many subagents in a fixed shape (fan-out / pipeline / loop), same every run, worth resuming"* — the workflow's job description in one line
- The Step 1 table (Job → Right tool) — directly liftable into our `david-style-patterns.md` as a triage pattern

## Adoption recommendation

**Strong recommend**: formal adoption as upstream provider #14. The artifact is exactly what dark-factory's research process is designed to consume: a high-quality, well-documented, mechanism-rich skill from a known author.

**Suggested use within dark-factory**:

1. **As a research source** (immediate): inform our `workflow-tool-authoring-notes.md` with patterns and primitives discovered here. Already partially done — see `docs/workflow-tool-authoring-notes.md` Part 4 (primitives) and Part 5 (patterns).

2. **As a canonical skill candidate** (after distill phase): may become `canonical/skills/workflow-creator/` — David's voice version, with provenance back to this source plus any other workflow-authoring guidance found in research.

3. **As the Alex (Prompt Architect) persona's primary tool** (Phase E): Alex calls into this skill when the user asks to design a workflow.

4. **As a v1 of the workflow linter** (immediate): `scripts/validate-workflow.mjs` may already cover our C1–C5 checklist items. Worth running against our existing workflows to test (R10 in research agenda).

## Open questions for discover/distill phase

1. Does the skill's procedure differ from our `docs/ingestion-workflow.md` 11-step procedure in interesting ways? (Cross-pollination opportunity.)
2. How does this skill's "Step 1 — when is a workflow right" compare to our `experiments/ylo/README.md` Hybrid recommendation? (Reinforces or contradicts?)
3. Are there primitives in `references/api-reference.md` we haven't surfaced yet?
4. Are there patterns in `references/patterns.md` (judge panel, nested workflow) that solve open problems we've articulated?
5. Does the linter catch the 5 checklist items from our authoring notes?

## Discover/distill backlog

See `backlog/2026-05-25-recon-workflow-creator.md` (to create) for the follow-up work. Estimated 1 session for discover + distill (~30 min if everything is well-documented like the recon suggests).

## Next steps

- ✅ Recon complete (this file)
- ☐ Discover (catalog each artifact's purpose, list mineable mechanisms) — backlog item
- ☐ Distill (merge with other workflow-authoring guidance into a unified write-up) — backlog item
- ☐ Evaluate (rate vs other sources) — likely top scorer; backlog item
- ☐ Consider for canonical ingestion as `canonical/skills/workflow-creator/`
