---
distillation_id: documentation-doc-review-suite
stage: audit
intent: "Multi-angle parallel documentation quality review — 6-9 dimensions covering coherence, completeness, gaps, topology, prose, crossref, and optionally editorial structure and comment accuracy"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:doc-review
  - appydave-plugins:skill:doc-review-coherence
  - appydave-plugins:skill:doc-review-completeness
  - appydave-plugins:skill:doc-review-crossref
  - appydave-plugins:skill:doc-review-gaps
  - appydave-plugins:skill:doc-review-prose
  - appydave-plugins:skill:doc-review-topology
  - bmad-method:skill:bmad-editorial-review-prose
  - bmad-method:skill:bmad-editorial-review-structure
  - everything-claude-code:agent:comment-analyzer
  - everything-claude-code:agent:doc-updater
  - gsd:agent:gsd-doc-verifier
winner_mechanism: appydave-plugins:skill:doc-review (suite)
---

# Unified Skill: doc-review-suite (upgrade candidate)

**Purpose**: Upgrade David's existing 7-piece doc-review suite by folding in three additional angles: editorial structure (restructuring/cutting), comment accuracy (code-comment drift), and factual verification (claims vs codebase). The orchestrator stays unchanged; add optional 7th, 8th, and 9th dimension sub-skills.

**For Agents**: This distillation is an UPGRADE to existing skills, not a from-scratch build. David already has `doc-review` + 6 dimension skills. The question is which new dimensions are worth adding.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Extend the existing 6-dimension parallel doc-review suite with up to 3 additional reviewers — editorial structure, code-comment accuracy, and factual verification — while keeping the orchestrator's fan-out model unchanged.

## Winner's Mechanism

David's existing suite (`doc-review` + 6 dimension skills) is already the winner mechanism. The orchestrator is clean: one entry point, 6 parallel background agents, normalized `DR-{CODE}-NNN` finding IDs, three-verdict synthesis (HEALTHY / NEEDS_ATTENTION / UNHEALTHY).

The key architecture decisions that make the suite work:
- **Dimension isolation**: each sub-skill is independently invokable AND composable via the orchestrator
- **Normalized finding format**: deduplication across dimensions works because the format is consistent
- **Verdict rollup**: worst-dimension verdict propagates to the overall verdict

No other source in the corpus has a comparable multi-angle doc-review architecture. The competitors are point tools (bmad editorial reviewers = single-angle), supporting agents (gsd-doc-verifier = fact-checker with no synthesis layer), or code-comment specialists (ecc:comment-analyzer).

## Existing-skill nesting

- **Existing mechanism**: `doc-review` orchestrates 6 parallel dimension agents. Each dimension has its own SKILL.md and review checklist. Findings use `DR-{CODE}-NNN` IDs. Three-verdict synthesis.
- **New mechanism's grain**: per-dimension (each new angle is one more background agent launched by the orchestrator)
- **Existing mechanism's grain**: per-corpus (orchestrator fires all dimensions against a path)
- **Nesting rule**: new dimensions plug in as additional sub-skills. The orchestrator's Step 2 gains optional `--dimensions=all|default|<list>` routing. Default set remains the current 6; opting into 7/8/9 requires explicit invocation or flag.

## Non-overlapping ideas to fold in

**Dimension 7 — Editorial Structure** (from `bmad-method:skill:bmad-editorial-review-structure`)

A structural editor that proposes cuts, reorganization, and simplification while preserving the author's voice and intent. Different from `doc-review-topology` (which checks file organization and nav) — editorial structure reviews *within-document* organization: section order, information hierarchy, eliminating redundancy, identifying what should be cut entirely.

`complexity: medium | optional: true | prerequisite: none`

Code: `ES` | Finding prefix: `DR-ES-NNN`

Key behaviors:
- Proposes concrete restructuring (not vague "this section is weak")
- Tracks voice — edit suggestions must match the author's existing style
- Cuts before adds — bias toward deletion, not padding

**Dimension 8 — Comment Accuracy** (from `everything-claude-code:agent:comment-analyzer`)

Analyzes code comments for accuracy, completeness, and maintainability. Finds: wrong comments (code diverged), misleading TODO comments, over-commented obvious code, under-commented non-obvious patterns, and stale annotations.

`complexity: medium | optional: true | prerequisite: "scope includes source code files, not just .md"`

Code: `CA` | Finding prefix: `DR-CA-NNN`

This extends `doc-review` into code-comment territory. Currently the suite only reviews `.md` files. Dimension 8 would fire only when the scope includes source files.

**Dimension 9 — Factual Verification** (from `gsd:agent:gsd-doc-verifier`)

Verifies factual claims in documentation against the live codebase — returns a confidence score per claim. Catches: incorrect command examples, wrong import paths, outdated API shapes, nonexistent file references.

`complexity: high | optional: true | prerequisite: "runnable codebase at scope path (not just docs)"`

Code: `FV` | Finding prefix: `DR-FV-NNN`

Highest complexity: requires actually running/reading code to verify claims. Most valuable for how-to guides and CLAUDE.md files. Lowest frequency of use.

## Additional fold-ins (orchestrator level)

- From `bmad-method:skill:bmad-editorial-review-prose`: **voice consistency** as a distinct sub-check within `doc-review-prose` — flag when sections shift from David's voice (direct, imperative) to passive/academic — `complexity: low | optional: false | prerequisite: none`. A checklist addition to the existing `prose` dimension, not a new dimension.

- From `everything-claude-code:agent:doc-updater`: **codemap maintenance** concept — after reviewing a corpus, flag any `INDEX.md` or `CLAUDE.md` that references files which no longer exist — `complexity: low | optional: false | prerequisite: none`. This is already partly covered by `doc-review-crossref`; explicit dead-file-in-index check should be a crossref checklist addition.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave:doc-review` (suite) | Entire orchestrator + 6 dimensions = the winner mechanism | Nothing set aside — this is the base |
| `bmad:editorial-review-structure` | Structural editing as Dimension 7 (ES) | BMAD persona wrapper, BMAD-specific output format |
| `bmad:editorial-review-prose` | Voice consistency checklist addition to `doc-review-prose` | Duplicate of existing `prose` dimension's core function |
| `ecc:comment-analyzer` | Code-comment accuracy as Dimension 8 (CA) | ECC-specific 4-question gate (too prescriptive for a sub-dimension) |
| `gsd:gsd-doc-verifier` | Factual verification concept as Dimension 9 (FV) | GSD parallel-agent invocation machinery (orchestrator handles this) |
| `ecc:doc-updater` | Dead-file-in-index check (crossref addition) | Full doc-update workflow (different skill: doc-write) |

## Draft SKILL.md frontmatter updates

The orchestrator skill already exists. If adding optional dimensions:

```yaml
name: doc-review
description: "Orchestrate parallel documentation review across 6-9 quality dimensions. Launches dimension sub-skills as background agents, then triages and synthesizes findings. Use when: 'review docs', 'doc review', 'review this brain', 'documentation quality', 'full doc audit', 'review all dimensions', 'run doc review'. Optional: --dimensions=all (adds editorial-structure, comment-accuracy, factual-verification)."
argument-hint: "[path or brain name] [--dimensions=default|all|coherence,gaps,...]"
allowed-tools: Bash(find *), Bash(grep *), Read
```

New dimension sub-skills (each gets its own SKILL.md):
- `doc-review-editorial-structure` — `allowed-tools: Read`
- `doc-review-comment-accuracy` — `allowed-tools: Read, Bash(grep *)`
- `doc-review-factual-verification` — `allowed-tools: Read, Bash(grep *), Bash(find *)`

## Open questions for David

1. **Dimension 8 scope boundary**: Does `doc-review` stay markdown-only, or should the orchestrator detect source files in scope and auto-enable Dimension 8? Mixed-scope directories (e.g., a `docs/` dir next to `src/`) make this ambiguous.

2. **Dimension 9 cost**: Factual verification requires reading source code to verify every claim. On a large brain (100+ files), this is expensive. Should it be an always-explicit `--dimensions=factual-verification` only, never part of `--dimensions=all`?

3. **Build priority**: Dimensions 7 and 8 are clear wins. Dimension 9 is high value but high cost to build. Suggested order: (a) add editorial-structure checklist to existing `doc-review-prose` (free), (b) build `doc-review-editorial-structure` as Dimension 7, (c) add dead-file check to `doc-review-crossref` (free), (d) build Dimension 8, (e) revisit Dimension 9 later.
