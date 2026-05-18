---
generated: 2026-05-18
generator: system-context
status: snapshot
sources:
  - README.md
  - CLAUDE.md
  - docs/canonical-form-spec.md
  - docs/provenance-spec.md
  - docs/ingestion-workflow.md
  - research/INDEX.md
  - research/phase-2-synthesis.md
  - research/insights.md
  - research/schema-current.md
  - mochaccino/workspace.md
  - mochaccino/data/pipeline.json
  - context/context.globs.json
regenerate: "Run /system-context in the repo root"
---

# Dark Factory — System Context

## Purpose
A staging library that ingests ~1,100 skill/agent/command artifacts from 13 upstream methodology repos and re-authors the best of them in David Cruwys's voice — with a verbatim copy and JSON provenance chain attached to every canonical rewrite, so no origin is ever lost and every choice is auditable back to source.

## Core Abstractions
- **Canonical artifact** — a SKILL.md / agent.md / command.md under `canonical/<type>/<name>/`, written in David's voice (terse operator tone, trigger-only descriptions, no marketing). The build target. Every canonical has exactly one `provenance.json` and a populated `_source/` folder beside it; the three together form the durable unit.
- **Provenance chain** — `provenance.json` schema (canonical_id, version, rewrite_status, origins[], research_sources, version_history). The `origins[]` array — each entry with `kept` / `modified` / `set_aside` — is the audit surface: it records not just what fed the rewrite, but what the author deliberately discarded. The chain is what makes the library "verifiable canonical," not just "another opinionated skill set."
- **Verbatim source (`_source/`)** — a frozen byte-for-byte copy of each upstream origin, named `<repo>--<original-filename>.md`. Exists so the original is recoverable per-skill even if the upstream repo rebases, deletes, or rewrites the file. Verbatim means no whitespace cleanup, no link rewriting, no truncation.
- **Distillation** — a research-phase document under `research/distillations/<cluster>-<sub-cluster>.md` that proposes a single canonical from N origins, with a "winner mechanism + folded-in ideas + complexity annotations" structure. Distillations are not commitments; they enter the build pipeline only when a backlog item authorizes ingestion.
- **Backlog item** — a `backlog/YYYY-MM-DD-<slug>.md` file that bridges brain conversations (PO side, in `~/dev/ad/brains/`) and this repo (Dev side). It names the target canonical_id, the distillation source, the origins to harvest, the research consults, and the acceptance criteria. A developer session opens this repo, picks the highest-priority backlog item, and executes.

How they compose: a *backlog item* points to a *distillation*, which proposes folding N *origins* into one *canonical*; the developer harvests each origin to `_source/` (verbatim), writes the canonical body in David's voice, and records the kept/modified/set_aside for each origin in the *provenance chain*. The canonical without its provenance and `_source/` files is, by spec, not a canonical at all.

## Key Workflows

### Ingest one artifact (PO authors backlog → Dev produces ratified canonical)
1. PO writes `backlog/<date>-<slug>.md` naming target, distillation, origins, evals, acceptance criteria.
2. Dev session opens the repo, reads CLAUDE.md, picks the backlog item, reads the referenced distillation + evaluations + insights.md craft bits.
3. Dev locates each origin on disk at `~/dev/upstream/repos/<repo>/...`, verifies existence, copies each verbatim to `canonical/<type>/<name>/_source/<repo>--<file>.md`.
4. Dev drafts `provenance.json` with `rewrite_status: draft`, version 1, one origin entry per harvested file (initially seeded from the distillation's analysis).
5. Dev writes `SKILL.md` per `canonical-form-spec.md` — four-field frontmatter (name, description, argument-hint, allowed-tools), trigger-only description, David-pattern body (purpose → behavior → output → anti-patterns). Updates `rewrite_status` to `in-style`.
6. Dev refines each origin's `kept` / `modified` / `set_aside` arrays to reflect what the actual rewrite did.
7. Dev validates against the ratification checklist (frontmatter complete, description trigger-only with 3+ phrases, body ≤400 lines or uses references/, no orphan `_source/` files, no stack-named terminology).
8. Dev flips `rewrite_status` to `ratified`, appends a row to `canonical/INDEX.md`, renames the backlog item to `backlog/done/<slug>.md` with a `## Result` section.

### Research → distillation (already complete for the seed corpus)
1. Recon: per-repo shape report at `research/recon/<repo>.md` (13 repos done).
2. Discover: unified-contract sweep producing `research/artifacts.jsonl` (1,100 rows, 100% JSON-valid as of 2026-05-16).
3. Tag: multi-select SDLC stage mapping.
4. Evaluate: deep evals at `research/evaluations/<repo>__<type>__<name>.md` scoring quality, adoption fit, mineable phrases (88 done).
5. Distill: cluster N origins into a unified-skill draft at `research/distillations/<cluster>-<sub-cluster>.md` (76 drafts). Distillation drafts feed backlog items, not direct ingestion.

### Visual decision-support (Mochaccino)
1. Restart the local Python server if needed: `cd mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &`.
2. Open `http://localhost:7420/designs/` — gallery of pipeline-overview (`01-pipeline-overview`, SDLC-strip lens over 11 stages) and mining-view (`02-mining-view`, top-artifacts-per-cluster lens).
3. Designs render from JSON in `mochaccino/data/` (pipeline.json, mining.json) synthesised by Peter from artifacts.jsonl + pipeline-matrix + evaluations. Re-render after refreshing data; never hand-edit the HTML to reflect new data.

### Version a ratified canonical
1. Bump `provenance.json` `version` field (e.g. 1 → 2) and update `rewrite_date`.
2. Append a `version_history[]` entry with `version`, `ratified_at`, `superseded_at`, `superseded_reason`, `diff_summary`.
3. Edit `SKILL.md` per the new design. Never in-place edit a ratified artifact without bumping version — the previous version's body is recoverable via `git log`, but the WHY of the transition lives only in `version_history`.

## Design Decisions

- **Verbatim source preservation (`_source/` folder per canonical)**: every origin file is copied into the canonical's folder byte-for-byte. The rewrite drifts; upstream repos rebase or delete files; the verbatim copy is the durable record.
  - *Alternative considered*: link to upstream commit URL only.
  - *Why rejected*: upstream files disappear, get force-pushed, or move during refactors. A link is a promise; a copy is an artifact. The library's core promise — "no lost source" — collapses without per-skill durable copies.

- **Provenance as schema-validated JSON, not free-form notes**: `provenance.json` has required fields, allowed `rewrite_status` values, and validation rules in `provenance-spec.md`. `tools/verify-provenance.py` (not yet written) is the future enforcer.
  - *Alternative considered*: prose paragraphs in SKILL.md crediting sources.
  - *Why rejected*: prose can't be validated, can't be diffed mechanically, and rots silently. Schema lets the spec enforce "no orphan `_source/` files" and "every origin has a `kept[]` of ≥1" automatically.

- **`kept` / `modified` / `set_aside` trichotomy per origin**: every origin entry must record what was kept, what was changed in the rewrite, and what was deliberately not included.
  - *Alternative considered*: kept + modified only (skip set_aside as implied).
  - *Why rejected*: the discarded ideas are the highest-signal review surface. "What did the author look at and choose not to use?" is what a future reviewer needs most when re-deciding the rewrite. Silence about set-aside ideas leaves no audit trail.

- **Research phase frozen, externally referenced**: `research/` is read-only from any session opened in this repo. A symlink at `~/dev/ad/brains/agentic-factory/dark-factory-catalog/` → `apps/dark-factory/research/` keeps live skill references resolving.
  - *Alternative considered*: continuously update `research/` as new insights surface.
  - *Why rejected*: the catalog SKILL in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` has live paths into recon/ and distillations/. A moving target there breaks production skills. New craft bits append to `research/insights.md` (the one append-only exception); structural changes go in a versioned schema bump.

- **Trigger-only descriptions in canonical SKILL.md (vs workflow summaries)**: the YAML `description` is a routing condition (`"Use when..."`), never a paragraph about what the skill does.
  - *Alternative considered*: descriptive paragraph summarizing the skill's behavior.
  - *Why rejected*: agent-skills-osmani and superpowers research (logged in `insights.md` 2026-05-16) showed that only `name` + `description` enter context at session start under lazy loading. A summary lets the LLM decide it already knows the skill and skips the body; a trigger forces activation when the condition matches.

- **PO/Dev split (brain conversations vs this repo)**: strategic thinking and backlog authoring happen in `~/dev/ad/brains/`; execution happens here. The bridge is a backlog file.
  - *Alternative considered*: do everything in one repo, including conversational scratch.
  - *Why rejected*: conversation transcripts and execution code have different shapes, audiences, and lifecycles. Keeping the brain side as a thinking space and the apps side as a build space prevents thinking-noise from polluting the canonical record.

- **Stack-agnostic canonical bodies**: a canonical SKILL.md body never names a language or framework ("Run the project's test command", not "Run `npm test`"). Stack specifics belong in the consuming project's architecture doc.
  - *Alternative considered*: include stack-specific examples for clarity.
  - *Why rejected*: stack lock makes a skill un-composable across the projects David maintains. Origins are often stack-locked (BMAD examples assume one harness); the rewrite extracts the mechanism stack-free, and per-origin `modified[]` records "voice → David's terse operator tone; removed multi-harness compile target" as the audit trail of the lift.

## Non-obvious Constraints

- **`research/` is referenced by external skill paths in appydave-plugins**. Moving or renaming any file under `research/recon/`, `research/distillations/`, or `research/evaluations/` breaks the catalog SKILL at `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` and any tooling that points at it. The CLAUDE.md hard rule "Don't move or rename `research/`" is load-bearing.

- **A compat symlink masks the relocation**. `~/dev/ad/brains/agentic-factory/dark-factory-catalog/` is now a symlink to `apps/dark-factory/research/`. Old skill references and bookmarks still resolve through it. Removing or breaking that symlink will look like missing files in unrelated repos.

- **Ratified artifacts are immutable in place**. Edits to a ratified `canonical/.../SKILL.md` without bumping `version` and appending `version_history[]` silently lie — `git log` has the diff but provenance claims it didn't happen. The "assessment-mode default" in CLAUDE.md exists because the prior workflow was "iterate in place"; the build phase explicitly rejects that.

- **`origins: []` is forbidden**. A canonical that David invents from scratch must still record what he looked at and chose not to use — as origin entries with no `kept[]` and a populated `set_aside[]`. A truly origin-less canonical hides the consideration trail and violates the audit promise.

- **No orphan `_source/` files**. Every file in `_source/` must be referenced by at least one `origins[i].verbatim_copy`. A `_source/` file with no origin entry will fail validation (rule 4 in provenance-spec.md). Removing an origin from `origins[]` without also removing the verbatim copy is a common mistake.

- **`canonical/` is staging, not deployment**. Ratifying a canonical does not install it as a Claude Code skill anywhere. Migrating to `~/dev/ad/appydave-plugins/appydave/skills/` is a separate, deliberate decision (covered by another workflow, not this repo's spec). Treating canonical/ as "the live skills folder" is a category error.

- **Mochaccino server is not auto-started**. The Python `http.server` on :7420 is a manual `nohup` launch (command in CLAUDE.md). If `http://localhost:7420/designs/` returns connection refused, the server is down — restart per the snippet. Designs render statically from JSON; re-renders require Mocha (the view-renderer skill), not direct HTML edits.

- **Stack-named in body is a silent defect**. `style-check.py` doesn't exist yet, so "Run `npm test`" in a canonical body passes ratification by accident. Only manual review catches it. Treat the anti-pattern list in `canonical-form-spec.md` as a checklist, not an aspiration.

- **The schema is co-defined with an external skill**. `research/schema-current.md` (here) and `references/capability-discover.md` in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` must move together — they encode the same schema from two sides.

## Expert Mental Model

- **The provenance chain is the product**. Newcomers think this is a skill library that happens to track sources. Experts know the audit chain — "every choice is auditable back to verbatim source" — is the only thing that justifies re-authoring 1,100 existing skills instead of using them in place. The rewrite is incidental; the provenance is the moat.

- **A canonical is a folder, not a file**. SKILL.md is the visible artifact, but a canonical without `provenance.json` and `_source/` is not a canonical — it's a draft. The ratification spec treats the three together as one atomic unit. "Did you ratify the skill?" is the wrong question; "is the canonical folder complete?" is the right one.

- **`set_aside[]` carries the highest-signal review surface**. Beginners populate `kept[]` carefully and leave `set_aside[]` empty or terse. Experts pour reasoning into `set_aside[]` — that's where future maintainers learn why a tempting feature wasn't lifted. Empty `set_aside[]` across all origins usually means the rewrite is incomplete or the reviewer skipped the question "what did I deliberately not use?"

- **Description is a routing program, not a description**. The fluent practitioner writes the `description:` field last, after the body, and treats it as a 200-token program whose only job is to decide whether the body loads. Anything that doesn't help the LLM make that decision is bytes paid at every session boot for no return.

- **Distillation drafts are proposals, not commitments**. The 76 distillation drafts in `research/distillations/` look like a backlog but aren't. They're hypotheses about which clusters to canonicalize. A backlog item authorizes ingestion; absent that, a distillation is a research artifact, not a build directive.

- **Stack-agnostic means body, not provenance**. Origins legitimately name their stack ("BMAD compile-on-install for Claude Code"). The rewrite extracts the mechanism free of stack, and `modified[]` records the lift ("removed multi-harness compile target"). Confusing "the rewrite should be stack-agnostic" with "the origin record should be stack-agnostic" erases the audit trail.

- **This repo is the consumer/transformer; the catalog SKILL is the producer**. `research/` was produced by the catalog SKILL in appydave-plugins. This repo doesn't re-produce it — it transforms it into canonical artifacts. Confusing the producer/consumer relationship leads to attempts to "fix research data" here, which breaks the external reference and bloats this repo's scope.

## Scope Limits

- Does NOT install canonical skills into Claude Code — migration to `~/dev/ad/appydave-plugins/appydave/skills/` is a separate, deliberate copy step governed by other tooling, not by `canonical/INDEX.md` ratification.
- Does NOT manage upstream repos — recon, harvest, and verbatim copies treat `~/dev/upstream/repos/<repo>/` as read-only inputs. Upstream rebases, deletions, and force-pushes are handled per ingestion (see `provenance-spec.md` edge cases), not by tracking upstream activity.
- Does NOT auto-generate canonical artifacts from `artifacts.jsonl` — every canonical requires a human-authored backlog item that names target, distillation source, and acceptance criteria. The 76 distillations are inputs to that decision, not decisions themselves.
- Does NOT track upstream change over time — `origins[].harvested_at` is a one-shot snapshot. Refreshing a canonical to track upstream changes means a new harvest + version bump, not a passive sync.
- Does NOT serve as a Claude Code plugin itself — the repo's outputs (`canonical/`) are staging artifacts. There is no installable skill registered here that another Claude session would load directly.
- Does NOT track MCP tools, hooks, rules, or plugin bundles as artifacts — open questions L, M in `research/INDEX.md` flag these as out of catalog scope; recon counts them only as context.
- Does NOT replace the catalog SKILL — recon, discover, distill, evaluate are operations of the catalog skill in appydave-plugins; this repo consumes that output for build.
- Does NOT auto-restart the Mochaccino server — port 7420 is human-managed; CI does not babysit it.

## Failure Modes

- **Orphan `_source/` file**: a file exists at `canonical/<type>/<name>/_source/<file>.md` but no `origins[i].verbatim_copy` in `provenance.json` references it. Recognition: validation rule 4 fails; manually visible as files in `_source/` that don't appear in the JSON. Fix: either add a corresponding origin entry or delete the orphan.

- **Missing verbatim copy**: an origin entry references `_source/<file>.md` but the file doesn't exist on disk (often because the developer copied the path from a similar canonical without doing the harvest). Recognition: ratification is blocked by checklist item "Every origin in `provenance.json` has a corresponding `_source/<repo>--<file>.md`". Fix: harvest the file or remove the origin.

- **Description-as-summary regression**: `description:` reads like marketing or workflow summary ("Reviews code for quality, security, and style issues") instead of trigger condition. Recognition: silent — the skill loads its YAML but the body never fires because the LLM treats the description as sufficient. No tests catch this; only David's voice review does. Fix: rewrite as `"Use when..."` with 3+ explicit trigger phrases.

- **Stack-named in body**: a canonical body contains `npm test`, `rspec`, `pytest`, or framework-specific paths. Recognition: silent — passes JSON validation, fails composability across projects with different stacks. Fix: replace with project-neutral phrasing ("Run the project's test command"); record the lift in `origins[].modified[]`.

- **In-place edit on ratified artifact**: someone edits a ratified `SKILL.md` without bumping `version` or appending to `version_history[]`. Recognition: `git log` has the diff but provenance.json claims `version: 1` with empty `version_history[]`. The fix-it-later path: bump `version`, append a history entry naming the silent edit's superseded_reason, and treat going forward as v2.

- **Research path drift**: a file under `research/recon/`, `research/distillations/`, or `research/evaluations/` gets moved, renamed, or deleted. Recognition: the catalog SKILL in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` (or the brains-side compat symlink) hits a "file not found" at runtime. Fix: restore the original path; if a move is genuinely needed, do it as a coordinated change on both sides plus an `INDEX.md` schema-history entry.

- **Mochaccino server stopped**: `http://localhost:7420/designs/` returns connection refused. Recognition: browser error in the visual workspace. Fix: `cd ~/dev/ad/apps/dark-factory/mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &` (snippet in CLAUDE.md).

- **Stale upstream origin**: `origins[].source_path` points at a file that no longer exists upstream (file was deleted, renamed, or rebased away). Recognition: `source_url` 404s; `source_path` not found on disk during a re-verification pass. The verbatim copy in `_source/` still works (that's the point), but provenance trust erodes. Fix: leave the origin entry in place (it's a historical record), optionally add a note in `origins[].source_path` flagging the upstream move, and record the rediscovered path in a version bump if you re-harvest.

- **Forbidden empty origins**: a developer writes a `provenance.json` with `origins: []` because the canonical was invented from scratch. Recognition: validation rule (implied by "every origin must have non-empty `kept[]`") rejects this; the spec explicitly disallows it. Fix: log every source the developer *considered* — including ones they fully rejected — as origin entries with empty `kept[]` and populated `set_aside[]`.
