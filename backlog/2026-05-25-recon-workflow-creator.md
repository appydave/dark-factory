# Backlog: Discover/Distill/Evaluate workflow-creator skill

**Created**: 2026-05-25
**Priority**: Medium-High — feeds workflow authoring quality
**Estimated effort**: 1 session (~30 min for discover+distill, separate session for evaluate+canonical decision)
**Prerequisites**: Recon complete (see `research/recon/claude-code-workflow-creator.md`)

## Context

Ray Amjad's `claude-code-workflow-creator` skill was added as upstream provider #14 on 2026-05-25. Recon is complete. The artifact is a single high-quality skill with comprehensive references, templates, and examples — exactly what dark-factory's process is designed to consume.

This is also the highest-leverage authoring resource for the Workflow Tool, which is now central to dark-factory's Platform layer (see `docs/architecture.md`). The faster we surface its mechanisms into our own authoring guidance, the sooner Phase B (first dog-food workflow) can proceed with confidence.

## Tasks

### 1. Discover

For each artifact in the repo, catalog:
- Purpose (one line)
- Mechanism (what specific technique it embodies)
- Mineable phrases (David-voice-compatible language)
- Cross-references (which other artifacts in dark-factory's corpus does this connect to?)

Artifacts to catalog:
- `SKILL.md` — the procedure (Steps 0–N)
- `references/api-reference.md` — primitives catalog
- `references/patterns.md` — orchestration patterns
- 3 templates in `assets/templates/`
- 6 example workflows in `assets/examples/`
- `scripts/validate-workflow.mjs` — linter

Output: `research/distillations/workflow-creator-mechanisms.md` (one entry per mechanism, with verbatim quotes and provenance).

### 2. Cross-pollination check

Compare against:
- `docs/ingestion-workflow.md` (our 11-step procedure) — any steps we should adopt?
- `docs/workflow-tool-authoring-notes.md` Parts 4 & 5 (already partially synthesized)
- `experiments/ylo/README.md` (Hybrid recommendation) — does the skill's "when is a workflow right" criterion validate or refine our Hybrid call?

Output: notes added to `research/insights.md` for any cross-cutting findings.

### 3. Linter test

Run `scripts/validate-workflow.mjs` against our 5 existing workflows in `.claude/workflows/`. Does it catch any of our C1–C5 issues retroactively? Does it surface issues we missed?

```bash
cd /Users/davidcruwys/dev/upstream/repos/claude-code-workflow-creator
for wf in /Users/davidcruwys/dev/ad/apps/dark-factory/.claude/workflows/*.workflow.js; do
  node scripts/validate-workflow.mjs "$wf"
done
```

Output: results logged here as Status section.

### 4. Evaluate

Score the skill against our standard evaluation dimensions:
- Quality (writing, completeness, mechanism density)
- Adoption fit (how well does it map to dark-factory's needs?)
- Reusability (stack-agnostic? David-voice-compatible?)
- Unique mechanisms (what does it have that nothing else does?)

Output: `research/evaluations/workflow-creator.md`

### 5. Canonical decision

Two ratification questions for David (PO):
- Should this become `canonical/skills/workflow-creator/`? (Likely yes — we have nothing else this strong on this topic.)
- If yes, what's the canonical name? Options: `workflow-creator`, `workflow-author`, `workflow-design` — TBD by PO.

If yes, queue an ingestion backlog item using the standard ingestion procedure (or — ideally — the new `ingest.workflow.js` from Phase B once it exists).

## Acceptance criteria

- [ ] `research/distillations/workflow-creator-mechanisms.md` exists with at least one entry per artifact in the repo
- [ ] Linter has been run against our 5 workflows; results logged
- [ ] Cross-pollination notes added to `research/insights.md`
- [ ] `research/evaluations/workflow-creator.md` exists with scorecard
- [ ] PO decision recorded: ingest as canonical? If yes, name confirmed.

## Status

Pending. Ready for the next session.
