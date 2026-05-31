---
generated: 2026-05-28
generator: system-context
status: snapshot
sources:
  - CLAUDE.md
  - context/CONTEXT.md
  - context/context.globs.json
  - canonical/INDEX.md
  - docs/architecture.md
  - docs/dark-factory-living-system-spec.md
  - docs/phase-b-next-steps.md
  - docs/ylo-to-poem-blueprint.md
  - docs/watchtower/spec.md
  - docs/canonical-form-spec.md
  - docs/provenance-spec.md
  - docs/ingestion-workflow.md
  - experiments/ylo/README.md
  - spikes/blackboard-mcp/README.md
  - research/INDEX.md
  - research/insights.md
  - research/schema-current.md
  - mochaccino/workspace.md
regenerate: "Run /system-context in the repo root"
---

# Dark Factory — System Context

## Purpose
A self-improving capability factory that continuously harvests skill/agent/command/workflow artifacts from 14 upstream methodology repos (~1,150 raw artifacts), evaluates each at five depth levels (repo scorecard → census → triage → rollout → distillation), ratifies the best version of each capability into a canonical library written in David Cruwys's voice with verbatim source preservation and full provenance, and re-runs the loop on its own outputs so the library improves while David sleeps.

**The repo hosts two intertwined threads.** Thread 1 — **canonical ingestion**: the 1,150-artifact corpus → `canonical/` staging → eventual projection to `appydave-plugins`. Thread 2 — **the blackboard → POEM line** in `experiments/ylo/`: a hybrid substrate study (blackboard vs Anthropic Workflow Tool) that produced the runtime decisions for thread 1's workflows. YLO is explicitly a testing ground destined to retire; its learnings consolidate into POEM (authoring surface) + AWB Gen 3 (runtime). Consolidation plan: `docs/ylo-to-poem-blueprint.md`. Mochaccino designs 04–08 visualise this thread.

## Core Abstractions

- **The Three Roles (Library / Warehouse / Platform)** — Dark Factory has three coexisting roles, not one. **Library** = `canonical/` (one winner per capability station, David's voice, provenance + verbatim sources). **Warehouse** = `research/` + upstream provider repos at `~/dev/upstream/repos/` (raw material, alternatives, history). **Platform** = `.claude/workflows/` + the Workflow Tool runtime (the factory that creates/runs/evaluates/promotes). Platform reads from Warehouse, produces Library, and uses Library to do production work. Choosing one role over the others is a category error — they are three layers of the same thing.

- **Canonical artifact (with variants)** — a folder at `canonical/<type>/<name>/` containing `SKILL.md` (current winner, David's voice), `provenance.json` (rewrite chain + winner_mechanism + version_history), `_source/` (verbatim copies of every origin file), and an emerging `variants/` subdir (runners-up, demoted-canonicals, alternatives). The canonical body is **stack-agnostic**; stack specifics belong in consuming projects. When a challenger beats canonical via shadow-run evidence, the swap promotes the new variant to top-level `SKILL.md` and demotes the old canonical to `variants/was-canonical-<date>.md`. **No artifact is ever destroyed** — the library is a layered cake of historical winners. `canonical_id` follows `<domain>.<lane>.<station>` (e.g. `software.dev.code-review`); variants append `.<provider>.v<n>`.

- **The 5 evaluation levels** — assessment is a pipeline, not a one-time pass. **L0 Repo Scorecard** (per upstream repo: quality_tier, freshness, priority — `research/repos.jsonl`). **L1 Census** (per artifact: cluster, quick quality_tier, verdict ∈ {adopt, evaluate, skip, defer} — `research/census.jsonl`; `level-1-census.workflow.js` already runs; batch 0 of 5 complete on 2026-05-26). **L2a Triage** (qualitative scorecard for evaluate-verdict artifacts: quality_score, adoption_fit, uniqueness, composability, mineable_phrasing, gap_analysis — `research/evals.jsonl` + markdown in `research/evaluations/`; 88 of 1,150 done, ~1,062 remaining). **L2b Rollout** (run the skill on held-out task sets, score the outputs — *infrastructure not yet built*). **L3 Distillation** (one per capability cluster, requires complete L2a+L2b coverage — `research/distillations/<cluster>.md`; the 76 existing distillations are flagged **provisional** because they were written with incomplete L2 coverage). **L4 Ratification** (HITL gate: David reviews L3 distillation, validation-gate score check, SKILL.md + provenance.json + verbatim copies written, registered in `canonical/INDEX.md`).

- **Provenance chain** — `provenance.json` schema (canonical_id, version, rewrite_status ∈ {draft, in-style, ratified}, origins[], research_sources, version_history, validation_score, validation_baseline). Each origin entry carries `kept` / `modified` / `set_aside` arrays — the trichotomy is load-bearing because `set_aside[]` records *what was deliberately not used*, which is the highest-signal audit surface. Every file in `_source/` must be referenced by at least one `origins[i].verbatim_copy`; orphans fail validation.

- **Verbatim source (`_source/`)** — frozen byte-for-byte copies of origin files, named `<repo>--<original-filename>.md`, so the original is recoverable per-skill even if the upstream repo rebases, deletes, or rewrites the file. Verbatim means no whitespace cleanup, no link rewriting, no truncation.

- **Workflow Tool + Blackboard MCP (the runtime substrate)** — Dark Factory uses Anthropic's **Workflow Tool** (deterministic JS orchestrator: `agent()`, `parallel()`, `pipeline()`, `phase()`, `schema`, `budget`) as the primary substrate. It passes state through plain JS variables (code wrapper, not model wrapper) and spawns fresh-context subagents per `agent()` call. The **Blackboard** (bash+jq+curl conductor + append-only EAV store, validated in `experiments/ylo/blackboard/`) remains useful for HITL-heavy and store-granular flows where Workflow Tool's "no filesystem access in the VM" penalty dominates (5× slower on store-heavy probes). The **MCP Blackboard pattern** (spike: `spikes/blackboard-mcp/server.mjs`, verified R11–R14 PASS) bridges them: workflow subagents call `mcp__blackboard__bb_set/get` directly via MCP, eliminating the dedicated I/O agents that account for most Workflow Tool overhead.

- **Backlog item** — `backlog/YYYY-MM-DD-<slug>.md`, the bridge between brain conversations (PO side, `~/dev/ad/brains/`) and this repo (Dev side). Names the target canonical_id, the distillation/evals/origins to consult, and acceptance criteria. A dev session opens this repo, picks the highest-priority backlog item, executes per the ingestion procedure. Currently 7 active items + a `done/` archive.

How they compose: a **backlog item** authorises ingesting from a **distillation** (proposal-only — never directly ingested without backlog authorisation), which folds N **origins** into one **canonical**. The dev harvests each origin to `_source/` (verbatim), drafts the canonical body in David's voice, records `kept/modified/set_aside` per origin in the **provenance chain**, and ratifies. The Workflow Tool **Platform** automates the mechanical 11 steps; David's HITL approval gates the creative voice-rewrite step. A canonical without provenance + `_source/` is, by spec, not a canonical at all — it is a draft.

## Key Workflows

### Ingest one artifact end-to-end (PO authors backlog → Dev produces ratified canonical)
1. PO writes `backlog/<date>-<slug>.md` naming target canonical_id, distillation source, origin list, evaluation consults, acceptance criteria.
2. Dev session opens the repo, reads `CLAUDE.md` and `docs/phase-b-next-steps.md`, picks the backlog item, reads referenced distillation + evaluations + `research/insights.md`.
3. Dev locates each origin on disk at `~/dev/upstream/repos/<repo>/...`, copies each verbatim to `canonical/<type>/<name>/_source/<repo>--<file>.md`.
4. Dev drafts `provenance.json` with `rewrite_status: draft`, version 1, one origin entry per harvested file.
5. Dev writes `SKILL.md` per `docs/canonical-form-spec.md` — four-field frontmatter, **trigger-only** description (`"Use when..."`, ≥3 trigger phrases), David-pattern body. Flips `rewrite_status: in-style`.
6. Dev refines `kept`/`modified`/`set_aside` per origin to reflect what the rewrite actually did.
7. Dev runs the ratification checklist (frontmatter complete, description trigger-only, body ≤400 lines or uses `references/`, no orphan `_source/` files, no stack-named terminology).
8. Dev flips `rewrite_status: ratified`, appends a row to `canonical/INDEX.md`, renames backlog item to `backlog/done/<slug>.md` with a `## Result` section.

**First-target status (Phase B)**: `code-review` ingestion is the next backlog item (`backlog/2026-05-18-first-ingestion-code-review.md`). Two workflows are designed to automate steps 3–8: `prepare-ingestion-brief.workflow.js` (fan-out read pattern) and `ingest.workflow.js` (transpiler). Neither is built yet. The natural HITL gate sits between draft and ratify.

### Level 1 census run (running today)
1. Read a batch of artifact IDs from `research/artifacts.jsonl` (the 1,150-row unified discovery output).
2. `level-1-census.workflow.js` fans out via `pipeline()`, 5 agents per batch, each producing a schema-validated census record (artifact_id, cluster, quality_tier, verdict ∈ {adopt, evaluate, skip, defer}, verdict_reason, source_version).
3. Append records to `research/census.jsonl`.
4. Live dashboard at `mochaccino/designs/09-census-progress/` shows progress. Batch 0 (5 records, all `agent-skills-osmani`) complete on 2026-05-26 — verdicts: 3 adopt / 2 evaluate. **1,112 records remaining.**

### Visual decision-support (Mochaccino)
1. Restart the local Python server if needed: `cd mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &`.
2. Open `http://localhost:7420/designs/` — gallery. Thread 1 (ingestion): `01-pipeline-overview`, `02-mining-view`, `03-triage-console`. Thread 2 (blackboard→POEM): `04-blackboard-overview`, `05-probe-progression`, `06-blackboard-vs-poem`, `07-workflow-flows`, `08-poem-consolidation`. Census progress: `09-census-progress`.
3. Designs render from JSON in `mochaccino/data/` (pipeline, mining, triage, blackboard-probes, blackboard-vs-poem, blackboard-workflows, poem-consolidation, census-progress) synthesised by Peter. Re-render after refreshing data via Mocha; never hand-edit HTML to reflect new data.

### Watchtower v0 — local web app for decision queue (designed, not built)
1. RVETS scaffold (React + Vite + Express + TypeScript) via `appydave:create-appystack`. Localhost-bound only, single-user (David), no auth.
2. Four screens: **Today** (highest-leverage next action at session start), **Experiments** (portfolio grouped by status: proposed/running/completed/promoted/killed), **Runs** (per-run timeline with cost rollup), **Learnings** (grouped by 9-layer taxonomy: prompt/agent/skill/workflow/harness/evaluation/data_schema/watchtower_ui/orchestration).
3. Introduces four net-new artifact types: `experiment.yml`, `run.json`, `learning.yml`, `promotion.yml`. Reads existing `research/census.jsonl` (census workflow continues to own writes — Watchtower does not re-implement the harness, it shells out to it).
4. First slice: `census-batch-1` — chosen over the ChatGPT brief's thumbnail-ideation suggestion because census already produces real records today; dogfooding requires v0 to drive a workflow that exists.

### Research pipeline (already complete for the seed corpus)
1. **Recon**: per-repo shape report at `research/recon/<repo>.md` (14 repos done — 13 in original corpus plus `ray-amjad/claude-code-workflow-creator`).
2. **Discover**: unified-contract sweep producing `research/artifacts.jsonl` (1,150 rows, 100% JSON-valid).
3. **Tag**: multi-select SDLC stage mapping.
4. **Evaluate**: deep evals at `research/evaluations/<repo>__<type>__<name>.md` (88 done; remaining tracked via L1 verdicts).
5. **Distill**: cluster N origins into a unified-skill draft at `research/distillations/<cluster>-<sub-cluster>.md` (76 drafts). **Provisional — do not ingest from these until the cluster's L2 coverage is complete.**

### Version a ratified canonical
1. Bump `provenance.json` `version` (e.g. 1 → 2), update `rewrite_date`.
2. Append a `version_history[]` entry with `version`, `ratified_at`, `superseded_at`, `superseded_reason`, `diff_summary`.
3. Edit `SKILL.md`. **Bounded add/delete/replace edits only** — SkillOpt discipline; never rewrite from scratch. Previous version is recoverable via `git log`, but the WHY of the transition lives only in `version_history`.

## Design Decisions

- **Self-improving capability factory (not a hand-rolled methodology library)**: the system runs autonomously, observes itself, harvests new capabilities from upstream sources, benchmarks them against the current production line via shadow runs, and promotes the winners. The output is a continuously improving library where each canonical is provably the current best version available, with provenance back to every alternative it beat.
  - *Alternative considered*: a static, hand-curated skill library updated when David remembers.
  - *Why rejected*: at 1,150 artifacts across 14 actively-updated upstream repos, "update when remembered" loses signal within weeks. The Library has to be a derivative of an evidence-producing pipeline, not a snapshot.

- **Verbatim source preservation (`_source/` folder per canonical)**: every origin file is copied into the canonical's folder byte-for-byte; the rewrite drifts; upstream repos rebase or delete files; the verbatim copy is the durable record.
  - *Alternative considered*: link to upstream commit URL only.
  - *Why rejected*: upstream files disappear, get force-pushed, or move during refactors. A link is a promise; a copy is an artifact. The library's core promise — "no lost source" — collapses without per-skill durable copies.

- **Provenance as schema-validated JSON, not free-form notes**: `provenance.json` has required fields, allowed `rewrite_status` values, and validation rules in `provenance-spec.md`. `tools/verify-provenance.py` (not yet written) is the future enforcer.
  - *Alternative considered*: prose paragraphs in `SKILL.md` crediting sources.
  - *Why rejected*: prose can't be validated, can't be diffed mechanically, and rots silently. Schema lets the spec enforce "no orphan `_source/` files" and "every origin has a `kept[]` of ≥1" automatically.

- **`kept` / `modified` / `set_aside` trichotomy per origin**: every origin entry must record what was kept, what was changed in the rewrite, and what was deliberately not included.
  - *Alternative considered*: `kept` + `modified` only, treating set-aside as implied.
  - *Why rejected*: the discarded ideas are the highest-signal review surface. "What did the author look at and choose not to use?" is what a future reviewer needs most when re-deciding the rewrite. Silence about set-aside ideas leaves no audit trail.

- **Workflow Tool as the runtime substrate (code wrapper, not model wrapper)**: orchestration lives in plain JS files where state flows through variables. No Claude orchestrator re-reads and re-tokenises every intermediate.
  - *Alternative considered*: a Claude conductor agent calling subagents (blackboard pattern as the primary substrate).
  - *Why rejected*: the YLO probe #2 head-to-head showed Workflow Tool is **5× slower** for store-heavy flows because the VM has no filesystem access (every store write costs a full agent round-trip), but it dominates for parallel fan-out + schema enforcement + scheduled work. Dark Factory adopts a **hybrid**: Workflow Tool for L1 census + scheduled pulses + production fan-out; Blackboard for HITL + sequential store-heavy. MCP Blackboard pattern bridges both later.

- **One winner per station + all alternatives kept (canonical + `variants/`)**: `canonical/` holds the current winner per capability station; `variants/` (per-canonical) keeps runners-up and demoted previous winners.
  - *Alternative considered*: ChatGPT-architecture's "keep all variants flat, no canonical".
  - *Why rejected*: a flat variant set produces no production line — agents can't pick a default. Naming one canonical + retaining alternatives gives a working default + reversibility + a clean history.

- **Bounded edits on already-ratified canonicals (SkillOpt discipline)**: when iterating a ratified artifact, make add/delete/replace edits only; never rewrite from scratch.
  - *Alternative considered*: free re-authoring whenever the operator's taste shifts.
  - *Why rejected*: SkillOpt (arXiv:2605.23904) shows text-space optimisation only beats baselines when edits are bounded and accepted only on strict held-out-validation improvement. Free re-authoring loses the optimisation signal. The factory's promotion gate enforces this once the rollout harness exists.

- **`research/` frozen as input, externally referenced**: read-only from any session in this repo. A symlink at `~/dev/ad/brains/agentic-factory/dark-factory-catalog/` → `apps/dark-factory/research/` keeps live skill paths in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` resolving.
  - *Alternative considered*: continuously update `research/` as new insights surface from build sessions.
  - *Why rejected*: the catalog SKILL in appydave-plugins has live paths into `recon/` and `distillations/`. A moving target breaks production skills. New craft bits append to `research/insights.md` (the one append-only exception); structural changes go in a versioned schema bump.

- **Trigger-only descriptions in canonical SKILL.md (vs workflow summaries)**: the YAML `description` is a routing condition (`"Use when..."`), never a paragraph about what the skill does.
  - *Alternative considered*: descriptive paragraph summarising the skill's behaviour.
  - *Why rejected*: research from agent-skills-osmani and superpowers (logged in `research/insights.md` 2026-05-16) showed only `name` + `description` enter context at session start under lazy loading. A summary lets the LLM decide it already knows the skill and skips the body; a trigger forces activation when the condition matches.

- **PO/Dev split (brain conversations vs this repo)**: strategic thinking happens in `~/dev/ad/brains/`; execution happens here. The bridge is a backlog file.
  - *Alternative considered*: do everything in one repo.
  - *Why rejected*: conversation transcripts and execution code have different shapes, audiences, and lifecycles. Keeping the brain side as a thinking space and the apps side as a build space prevents thinking-noise from polluting the canonical record.

- **Stack-agnostic canonical bodies**: a canonical body never names a language or framework. Stack specifics belong in the consuming project's architecture doc.
  - *Alternative considered*: include stack-specific examples for clarity.
  - *Why rejected*: stack lock makes a skill un-composable across the projects David maintains. Origins are often stack-locked (BMAD examples assume one harness); the rewrite extracts the mechanism stack-free, and per-origin `modified[]` records "voice → David's terse operator tone; removed multi-harness compile target" as the audit trail of the lift.

- **Two-machine architecture (M4 Pro = Warehouse Keeper; this machine = Factory Floor)**: warehouse-side scheduled work (upstream-pulse, framework-pulse, promote, watchtower-projection) runs continuously on the headless M4 Pro; production workflow runs on the operator's primary machine.
  - *Alternative considered*: single-machine, all jobs co-resident.
  - *Why rejected*: continuous research competes with foreground work for resources, and a primary machine that sleeps interrupts the pulse. Separating roles lets the warehouse stay fresh while you sleep. Sync via shared git over Tailscale — no new infrastructure for v1.

## Non-obvious Constraints

- **`research/` is referenced by external skill paths in appydave-plugins**. Moving or renaming any file under `research/recon/`, `research/distillations/`, or `research/evaluations/` breaks the catalog SKILL at `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` and any tooling that points at it. The CLAUDE.md hard rule "Don't move or rename `research/`" is load-bearing.

- **A compat symlink masks the relocation**. `~/dev/ad/brains/agentic-factory/dark-factory-catalog/` is now a symlink to `apps/dark-factory/research/`. Old skill references and bookmarks still resolve through it. Removing or breaking that symlink will look like missing files in unrelated repos.

- **Ratified artifacts are immutable in place**. Edits to a ratified `canonical/.../SKILL.md` without bumping `version` and appending `version_history[]` silently lie — `git log` has the diff but provenance claims it didn't happen. The assessment-mode default in CLAUDE.md exists because the prior workflow was "iterate in place"; the build phase explicitly rejects that.

- **The 76 existing distillations are provisional, not authoritative**. They were written with incomplete L2 coverage. The living-system spec rule "do not ingest from a distillation until that cluster's L2a/L2b coverage is complete" voids them as direct build inputs. Treat them as hypotheses about which clusters to canonicalise, not commitments.

- **The Workflow Tool VM has no filesystem access**. Every `remember()`/`recall()` call costs a full agent round-trip (~15–30s). This is the root cause of the 5× wall-clock gap vs Blackboard on store-heavy probes. Workflows that try to "just track state inline" without recognising this will run unbearably slowly. The MCP Blackboard pattern (spike R11–R14 PASS) is the eventual fix.

- **Workflow Tool environment-variable inheritance is fragile**. `CLAUDE_CODE_WORKFLOWS=1` must be set in the actual shell that launches Claude Code; switching surfaces (background, agent view, IDE plugin) frequently drops the env var, producing the silent "Workflow tool exists but is not enabled in this context" failure. Mitigation: set it in `.claude/settings.local.json` per-project. API keys also do not flow to subagents — agents must read from `.env` files explicitly.

- **`origins: []` is forbidden, even for from-scratch canonicals**. A canonical David invents without lifting from an existing artifact must still record what he looked at and chose not to use — as origin entries with empty `kept[]` and populated `set_aside[]`. A truly origin-less canonical hides the consideration trail and violates the audit promise.

- **No orphan `_source/` files**. Every file in `_source/` must be referenced by at least one `origins[i].verbatim_copy`. A `_source/` file with no origin entry will fail validation (rule 4 in `provenance-spec.md`). Removing an origin from `origins[]` without also removing the verbatim copy is a common mistake.

- **`canonical/` is staging, not deployment**. Ratifying a canonical does not install it as a Claude Code skill anywhere. Migrating to `~/dev/ad/appydave-plugins/appydave/skills/` is a separate, deliberate decision (covered by another workflow, not this repo's spec). Treating `canonical/` as "the live skills folder" is a category error.

- **Mochaccino server is not auto-started**. Port 7420 is a manual `nohup` launch (command in CLAUDE.md). If `http://localhost:7420/designs/` returns connection refused, the server is down — restart per the snippet. Designs render statically from JSON; re-renders require Mocha (the view-renderer skill), not direct HTML edits.

- **Stack-named terminology in a canonical body is a silent defect**. `style-check.py` doesn't exist yet, so "Run `npm test`" in a canonical body passes ratification by accident. Only manual review catches it. Treat the anti-pattern list in `canonical-form-spec.md` as a checklist, not an aspiration.

- **YLO is restructured: `experiments/ylo/`, not `ylo-experiment/`**. The directory was moved as part of the experiments/ scenario-first layout (commit `c497ed4`). External docs and brain notes that reference the old path no longer resolve. The two substrates now live at `experiments/ylo/blackboard/` and `experiments/ylo/workflow-tool/`; workflow scripts themselves live at `.claude/workflows/` (enforced by Claude Code — do not relocate).

- **The schema is co-defined with an external skill**. `research/schema-current.md` (here) and `references/capability-discover.md` in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` must move together — they encode the same schema from two sides.

- **MCP Blackboard storage is within-run state, not persistent cross-run**. The v1 server (`spikes/blackboard-mcp/server.mjs`, ~180 lines of Node) writes to `~/.claude/blackboard/store.json` and is shared across runs *only if you choose the same blackboard ID*. Cross-run persistence is opt-in, not automatic. Treating it as a database is wrong — it's a workflow-VM substitute for the missing filesystem.

## Expert Mental Model

- **The provenance chain is the product**. Newcomers think this is a skill library that happens to track sources. Experts know the audit chain — "every choice is auditable back to verbatim source" — is the only thing that justifies re-authoring 1,150 existing skills instead of using them in place. The rewrite is incidental; the provenance is the moat.

- **Canonical is the current winner, not the only winner**. The fluent practitioner reads `canonical/<type>/<name>/` and expects a layered cake — `SKILL.md` (current best) + `_source/` (what fed it) + `variants/` (runners-up, demoted previous winners). New variants arrive from upstream pulse, accumulate evidence via shadow runs, and earn promotion. "What's the canonical?" is a question with a *current* answer, not a permanent one.

- **A canonical is a folder, not a file**. `SKILL.md` is the visible artifact, but a canonical without `provenance.json` and `_source/` is not a canonical — it's a draft. The ratification spec treats the three together as one atomic unit. "Did you ratify the skill?" is the wrong question; "is the canonical folder complete?" is the right one.

- **`set_aside[]` carries the highest-signal review surface**. Beginners populate `kept[]` carefully and leave `set_aside[]` empty or terse. Experts pour reasoning into `set_aside[]` — that's where future maintainers learn why a tempting feature wasn't lifted. Empty `set_aside[]` across all origins usually means the rewrite is incomplete or the reviewer skipped the question "what did I deliberately not use?"

- **Description is a routing program, not a description**. The fluent practitioner writes the `description:` field last, after the body, and treats it as a 200-token program whose only job is to decide whether the body loads. Anything that doesn't help the LLM make that decision is bytes paid at every session boot for no return.

- **The factory eats its own dog food (and that's the point)**. Newcomers ask "when does the factory start producing real work?" Experts know the factory's *first* production work is the workflows that *maintain the factory* — `level-1-census`, `prepare-ingestion-brief`, `ingest`, `upstream-pulse`, `promote`. Running these IS the proof-of-concept; the YouTube/SDLC/marketing workflows it serves later inherit the patterns and tooling these self-runs forged.

- **Harvest, don't author**. The fluent operator does not sit down and write skills. They scan the warehouse, queue a distillation, run an ingestion workflow, review the draft, ratify. New capabilities enter as variants; promotion is evidence-driven. "I should write a skill for X" is a beginner's reflex; the expert's reflex is "what's already in the warehouse for X, and what's the L2 coverage?"

- **Distillation drafts are proposals, not commitments**. The 76 drafts in `research/distillations/` look like a backlog but aren't. They are hypotheses about which clusters to canonicalise, written before the L2 coverage was complete. A backlog item authorises ingestion; absent that, a distillation is a research artifact, not a build directive — and per the living-system rule, ingestion requires complete L2 coverage first.

- **Stack-agnostic means body, not provenance**. Origins legitimately name their stack ("BMAD compile-on-install for Claude Code"). The rewrite extracts the mechanism free of stack, and `modified[]` records the lift ("removed multi-harness compile target"). Confusing "the rewrite should be stack-agnostic" with "the origin record should be stack-agnostic" erases the audit trail.

- **The Workflow Tool is a code wrapper; the blackboard is a model wrapper — pick by I/O shape, not preference**. The fluent operator picks substrate per workflow: parallel fan-out + schema enforcement + scheduled work → Workflow Tool; sequential store-heavy + native HITL + per-run granularity → Blackboard; cross-machine state or > 10 store ops → adopt MCP Blackboard pattern. Trying to standardise on one for ideological reasons leaves perf or ergonomics on the floor.

- **This repo is the consumer/transformer; the catalog SKILL is the producer**. `research/` was produced by the catalog SKILL in appydave-plugins. This repo doesn't re-produce it — it transforms it into canonical artifacts. Confusing the producer/consumer relationship leads to attempts to "fix research data" here, which breaks the external reference and bloats this repo's scope.

## Scope Limits

- Does NOT install canonical skills into Claude Code — migration to `~/dev/ad/appydave-plugins/appydave/skills/` is a separate, deliberate copy step governed by other tooling, not by `canonical/INDEX.md` ratification.

- Does NOT manage upstream repos — recon, harvest, and verbatim copies treat `~/dev/upstream/repos/<repo>/` as read-only inputs. Upstream rebases, deletions, and force-pushes are handled per ingestion (see `provenance-spec.md` edge cases). `upstream-pulse.workflow.js` (planned, M4 Pro) will detect upstream changes but not modify upstream.

- Does NOT auto-generate canonical artifacts from `artifacts.jsonl` — every canonical requires a human-authored backlog item that names target, distillation source, and acceptance criteria. The 76 distillations are inputs to that decision, not decisions themselves. Even with L4-ratification automated, the validation-gate held-out score is the auto-promote condition, not "the workflow ran clean."

- Does NOT track MCP tools, hooks, rules, or plugin bundles as cataloguable artifacts — open questions L, M in `research/INDEX.md` flag these as out of catalog scope; recon counts them only as context.

- Does NOT replace the catalog SKILL — recon, discover, distill, evaluate are operations of the catalog skill in appydave-plugins; this repo consumes that output for build.

- Does NOT replace POEM or AWB — POEM (Penny/Alex/Oscar authoring surface) and AWB Gen 3 (compile + run) are upstream of Dark Factory's workflows. The YLO→POEM blueprint specifies dark-factory becomes a `.poem/` *consumer*, not a POEM reimplementation. The conversational layer (Penny/Alex/Oscar in `.claude/agents/` here) is a thin local interface, not a fork.

- Does NOT own the census write path from Watchtower — Watchtower v0 reads `research/census.jsonl` but never writes to it. The census workflow continues to own writes; Watchtower shells out to the existing Workflow Tool harness and surfaces results. The four Watchtower record types (`experiment.yml`, `run.json`, `learning.yml`, `promotion.yml`) are net-new and live alongside census records, not within them.

- Does NOT auto-restart the Mochaccino server — port 7420 is human-managed; CI does not babysit it.

- Does NOT support multi-user, mobile, or shared sessions in Watchtower v0 — single-user (David), localhost-only, desktop browser only. No auth, no RBAC, no agents reading the UI (agents read underlying files). These are *hard cuts*, not deferred features.

- Does NOT persist Blackboard MCP state across runs by default — within-run only unless the workflow explicitly chooses a stable blackboard ID. Treating it as a queryable cross-run store is a category error; future "persistent queryable store" is an explicit open decision in the living-system spec.

## Failure Modes

- **Orphan `_source/` file**: a file exists at `canonical/<type>/<name>/_source/<file>.md` but no `origins[i].verbatim_copy` in `provenance.json` references it. Recognition: validation rule 4 fails; manually visible as files in `_source/` that don't appear in the JSON. Fix: either add a corresponding origin entry or delete the orphan.

- **Missing verbatim copy**: an origin entry references `_source/<file>.md` but the file doesn't exist on disk (often because the dev copied the path from a similar canonical without doing the harvest). Recognition: ratification is blocked by checklist item "Every origin in `provenance.json` has a corresponding `_source/<repo>--<file>.md`". Fix: harvest the file or remove the origin.

- **Description-as-summary regression**: `description:` reads like marketing or workflow summary ("Reviews code for quality, security, and style issues") instead of trigger condition. Recognition: silent — the skill loads its YAML but the body never fires because the LLM treats the description as sufficient. No tests catch this; only David's voice review does. Fix: rewrite as `"Use when..."` with ≥3 explicit trigger phrases.

- **Stack-named in body**: a canonical body contains `npm test`, `rspec`, `pytest`, or framework-specific paths. Recognition: silent — passes JSON validation, fails composability across projects with different stacks. Fix: replace with project-neutral phrasing ("Run the project's test command"); record the lift in `origins[].modified[]`.

- **In-place edit on ratified artifact**: someone edits a ratified `SKILL.md` without bumping `version` or appending to `version_history[]`. Recognition: `git log` has the diff but `provenance.json` claims `version: 1` with empty `version_history[]`. Fix: bump `version`, append a history entry naming the silent edit's `superseded_reason`, treat going forward as v2.

- **Workflow Tool env-var drop**: a workflow that ran fine in one shell stops working in another with "Workflow tool exists but is not enabled in this context." Recognition: the agent view, background process, or IDE plugin didn't inherit `CLAUDE_CODE_WORKFLOWS=1`. Fix: persist the env in `.claude/settings.local.json`. Restart Claude Code from a shell where `echo $CLAUDE_CODE_WORKFLOWS` prints `1`.

- **`parallel()` runs nothing visible**: a workflow calls `parallel([agent(...), agent(...)])` and the agents seem to run but produce no logged output. Recognition: silent — the workflow appears to complete but `meta.phases` lacks the expected entries. Cause: `parallel()` requires thunks `() => agent()`, not bare `agent()` calls. Fix: wrap each in an arrow function.

- **Workflow phase agents run invisibly**: an `agent({phase: "labelA"})` call exists but no records appear under that phase in the projection. Recognition: phase labels in `agent({phase})` must exactly match the corresponding entry in `meta.phases.titles`; mismatches silently route the agent to nowhere. Fix: align the strings.

- **Workflow Tool snapshots scripts at launch**: editing the source `.workflow.js` mid-run has no effect on the running workflow. Recognition: behaviour matches the pre-edit version even after save. Fix: edit the generated copy in the session dir, not the source — or restart the run with the updated source.

- **`resumeFromRunId` drops args**: resuming a workflow run loses the original arguments. Recognition: a resumed run errors on missing inputs. Fix: re-pass args explicitly on resume.

- **API agent silent stalls**: a workflow agent that hits an external API hangs without failing. Recognition: no error, no progress, agent burns through its budget. Cause: agent prompt didn't include explicit non-2xx bail or poll cap. Fix: every API-calling agent prompt must say "abort on non-2xx" and "cap polls at N".

- **Research path drift**: a file under `research/recon/`, `research/distillations/`, or `research/evaluations/` gets moved, renamed, or deleted. Recognition: the catalog SKILL in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` (or the brains-side compat symlink) hits a "file not found" at runtime. Fix: restore the original path; if a move is genuinely needed, do it as a coordinated change on both sides plus an `INDEX.md` schema-history entry.

- **Mochaccino server stopped**: `http://localhost:7420/designs/` returns connection refused. Recognition: browser error in the visual workspace. Fix: `cd ~/dev/ad/apps/dark-factory/mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &`.

- **Stale upstream origin**: `origins[].source_path` points at a file that no longer exists upstream (deleted, renamed, or rebased away). Recognition: `source_url` 404s; `source_path` not found during a re-verification pass. The verbatim copy in `_source/` still works (that's the point), but provenance trust erodes. Fix: leave the origin entry in place (it's a historical record), optionally flag the upstream move in `origins[].source_path`, record the rediscovered path in a version bump if you re-harvest.

- **Forbidden empty origins**: a dev writes a `provenance.json` with `origins: []` because the canonical was invented from scratch. Recognition: validation rejects this; the spec explicitly disallows it. Fix: log every source the dev *considered* — including ones fully rejected — as origin entries with empty `kept[]` and populated `set_aside[]`.

- **Ingesting from a provisional distillation**: a dev opens a 76-batch distillation file, sees the proposed structure, and starts ingestion without confirming the cluster's L2 coverage. Recognition: the resulting canonical is built from an unreliable proposal that predates the evaluation pipeline. Fix: gate ingestion on L2 completeness per the living-system spec; treat the 76 distillations as provisional sketches until rebuilt under complete L2 coverage.

- **Blackboard MCP treated as a database**: a workflow stores cross-run state in MCP Blackboard and expects to query it weeks later. Recognition: a later run gets stale or absent data; the v1 storage is a single file at `~/.claude/blackboard/store.json` with no querying, indexing, retention policy, or cross-machine sync. Fix: use the JSONL store (`store.jsonl`) for persistent telemetry, or wait for the "persistent queryable store" decision (open in the living-system spec).
