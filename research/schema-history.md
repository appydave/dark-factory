# Schema History

Append-only log of schema changes for the dark-factory-catalog.

## 0.0.1 — 2026-05-16

Initial bootstrap. No artifact fields defined yet. Schema will be drafted after Phase 1 recon confirms what fields each repo's artifacts actually carry.

**Migration**: none required (no prior artifacts).

## 0.0.2 — 2026-05-16

**Added** `prompt_patterns_used` as an OPTIONAL facet field — array of stable IDs from `prompt-pattern-vocabulary.md`. Populated during discover when recon flagged prompt-pattern signals.

**Decision (David, 2026-05-16)**: facet over artifact-type. Prompt patterns are techniques embedded inside artifact files, not standalone files. The facet model keeps catalog rows aligned with real files. See `proposals/2026-05-16-prompt-pattern-awareness.md` for full analysis.

**Also documented**: `frontmatter_yaml`, `retired` as optional fields.

**Sister artifacts** added (not in JSONL, but coordinated):
- `insights.md` (catalog data dir) — append-only audit log for atomic craft bits smaller than a pattern (phrases, contrasts, reframings).
- `prompt-pattern-vocabulary.md` (in skill) — 12 established + 11 candidate IDs.

**Migration**: no existing artifacts; future discover passes populate the new field as appropriate.

## 0.0.6 — 2026-05-16 (capability-distill.md template improvements — closed-loop feedback from first builds)

After building 2 skills from distill drafts (`pr-lifecycle` new + `ralphy` upgrade), three concrete gaps surfaced in the distillation template. All three are now patched.

**Gap 1 — frontmatter fields incomplete** (surfaced by pr-lifecycle build):
- Draft template only had `name` + `description`.
- Missing `argument-hint` and `allowed-tools` — both load-bearing for Claude Code. Without `allowed-tools`, a built skill prompts on every bash command at runtime, near-unusable for autonomous work.
- Fix: template now includes both fields with a "load-bearing" callout instructing the builder to copy from the winner source, not invent.

**Gap 2 — no nesting guidance for upgrade-path builds** (surfaced by ralphy upgrade):
- When the target skill already exists (ralphy), the draft needs to spell out how new mechanisms nest with existing ones at different grains (per-task vs per-wave, etc.).
- Fix: new "Existing-skill nesting" section added to template, conditional on upgrade-path. Explicitly names new/existing grains + composition rule.

**Gap 3 — folded ideas listed flat without complexity weight** (surfaced by pr-lifecycle build):
- Distill agents listed every folded idea as a bullet of equal weight, but some (like compound-engineering's cluster-analysis dispatch) are 5× more complex than the others.
- Fix: template now requires `complexity / optional / prerequisite` annotations on every folded idea.

**Migration**: existing 15 distillation drafts NOT retroactively updated. Future distill runs carry the improved template — meaning the 13 remaining clusters (knowledge-capture, etc.) will benefit when distilled.

**Validation signal**: this entry IS the closed-loop feedback we wanted from building. The catalog is now genuinely improved by use, not just by design.

## 0.0.5 — 2026-05-16 (cluster vocabulary update — no schema field change)

**Cluster vocabulary additions** (David approved 2026-05-16):
- `security-review`, `performance`, `dependency-management` — PROMOTED from `cluster-vocabulary-additions.md` to `cluster-vocabulary.md` main table.
- `accessibility` — REJECTED; folded into `code-review`. 3 ECC artifacts re-tagged inline in `artifacts.jsonl` and `artifacts/everything-claude-code.jsonl`. Each row carries a `notes` annotation recording the merge.

**Migration**: applied inline; no manual fix needed.

## 0.0.4 — 2026-05-16

**Added** optional fields that emerged during Phase 2 discover:
- `body_path` — paired workflow body file path (gsd's two-file split: YAML registration in `commands/gsd/` + executable prose in `get-shit-done/workflows/`).
- `notes` — free-form per-artifact annotation (e.g. "beta variant" used by compound-engineering for `ce-work-beta` / `ce-polish-beta`; "no description in source" used by appydave-plugins for body-only commands).

**Vocabulary additions**:
- `prompt-pattern-vocabulary.md` candidate section gained `multi-harness-compile` — independently proposed by gstack and spec-kit discover agents. Confirmed across 2 repos, 72 artifacts.
- `cluster-vocabulary-additions.md` created with 4 proposed cluster IDs surfaced (and used) during ECC discover: `security-review`, `performance`, `dependency-management`, `accessibility`. Pending David's review for promotion.

**Phase 2 discover statistics**:
- 1,100 total artifacts in `artifacts.jsonl` (100% JSON-valid).
- Per-repo: ECC 365 / ruflo 219 / appydave-plugins 122 / compound-engineering 86 / gsd 81 / gbrain 51 / gstack 49 / bmad-method 44 / agent-skills-osmani 33 / spec-kit 23 / superpowers 14 / compound-knowledge 11 / poem 2.
- Type split: 691 skills / 224 commands / 185 agents.
- 28 insights total in `insights.md` (5 seed + 23 from discover agents).

**Migration**: no migration needed — `body_path` and `notes` are optional and already populated where applicable by the discover agents.

## 0.0.3 — 2026-05-16

**Added** `cluster_facet` as an OPTIONAL facet field — array of stable cluster IDs from new `cluster-vocabulary.md`. Identifies the problem family the artifact belongs to (`code-review`, `planning`, `knowledge-capture`, etc.). Drives the distill walk: walk one cluster, compare implementations, mine best phrasings.

**Decision (David, 2026-05-16)**: cluster is a separate facet from SDLC stage and prompt-patterns. Three orthogonal axes:
- `cluster_facet` — WHAT problem family (this file)
- `sdlc_stage` — WHEN in lifecycle
- `prompt_patterns_used` — HOW it's architected

**Scope decisions (David, 2026-05-16)** — applied to Phase 2 discover:
- Primary artifacts only (skill / agent / command / workflow). Templates / hooks / rules / step files / MCP tools deferred to Phase 2.5.
- Source-only for compile-on-install repos (gstack, spec-kit, gsd, ECC adapters, compound-engineering converters). Compiled outputs are build artifacts, not separate skills.

**Goal-frame revision (David, 2026-05-16)**: replaced "~50 unified skills" target with "composable set of single-responsibility skills that solve legitimate problems and can compose into workflows / topologies — number emerges from the work."

**New reference file**: `cluster-vocabulary.md` with 18 starter cluster IDs (refines during discover).

**Migration**: no existing artifacts; future discover passes populate the new field as appropriate.
