# CLAUDE.md — Dark Factory

You're in **`~/dev/ad/apps/dark-factory/`** — David Cruwys's canonical skill library project. The 1,100-artifact research phase is complete (see `research/`); the build phase ingests artifacts from upstream repos into `canonical/`, rewriting each in David's voice with full provenance back to source.

**Two threads live here.** (1) **Canonical ingestion** — the original charter above (`research/` → `canonical/`). (2) **The blackboard → POEM line** — a workflow-pattern experiment in `ylo-experiment/` (the YLO blackboard probes) whose learnings are being consolidated into POEM. YLO is a testing ground destined to retire; the consolidation plan is `docs/ylo-to-poem-blueprint.md`, and dark-factory will gain a `.poem/` folder where YLO's workflows get rebuilt in POEM. Most of the Mochaccino gallery (designs 04–08) visualises this second thread.

## How sessions are organized

This repo is operated PO ↔ Developer style:

- **Brain conversations** (in `~/dev/ad/brains/`) — strategic thinking, decisions, requirements drafting. The PO side.
- **This repo** — execution. The Developer side. You're here.
- **Bridge** — every brain session that needs work done here writes a `backlog/YYYY-MM-DD-<slug>.md` item. You read it and execute.

## First thing to do on activation

1. Read `README.md` for the repo charter.
2. Check `backlog/` for pending work items. Most-recent-first; pick the highest priority.
3. Read `docs/` for the specs that govern your work:
   - `canonical-form-spec.md` — what a canonical SKILL.md must contain
   - `provenance-spec.md` — provenance.json schema + verbatim source preservation rules
   - `ingestion-workflow.md` — step-by-step procedure for ingesting an artifact
   - `david-style-patterns.md` — David's voice and template patterns
   - `phase-b-next-steps.md` — **START HERE if Phase B hasn't begun** — open questions, PO decisions needed, what to build
4. Read the backlog item's referenced research sources (under `research/distillations/`, `research/evaluations/`).
5. Execute the work per the spec.

## Hard rules

- **No skill/agent/command is created in `canonical/` without a `provenance.json` and at least one verbatim copy in `_source/`.** No exceptions. The provenance chain is the value proposition.
- **Skills are stack-agnostic.** Stack-specific terminology in a canonical skill body is a defect. Stack specifics belong in the consuming project's architecture doc.
- **David's voice** — trigger-only YAML descriptions ("Use when…"), terse, no marketing prose, no workflow summaries in descriptions. See `docs/david-style-patterns.md`.
- **Assessment-mode default** — even though this is now a build repo, NEVER auto-rewrite a canonical artifact after it's ratified. Drafts can iterate; ratified artifacts get a new version, not an in-place edit.

## Don't do without asking

- Don't move or rename `research/`. It's the frozen corpus — referenced by skill paths in `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/`. Read-only from your perspective.
- Don't add data to `research/` that wasn't sourced from a recon/discover/distill/eval phase — those are append-only research outputs, not staging.
- Don't write skill code (`.claude/skills/...`) directly into David's appydave-plugins repo. This repo's `canonical/` is the staging ground; copying to plugins is a separate decision.

## Where to write

| Want to … | Write to |
|-----------|----------|
| Ingest an upstream artifact | `canonical/<type>/<name>/` |
| Add a verbatim source copy | `canonical/<type>/<name>/_source/<repo>--<file>.md` |
| Document a procedure | `docs/<topic>.md` |
| Refresh mochaccino data | `mochaccino/data/<shape>.json` |
| Re-render mochaccino HTML | `mochaccino/designs/<id>/index.html` |
| Add a work item | `backlog/<date>-<slug>.md` (usually PO writes these, but you can add findings) |
| YLO blackboard experiment runs | `experiments/ylo/blackboard/runs/<id>/` |
| YLO Workflow Tool experiment runs | `experiments/ylo/workflow-tool/runs/<id>/` |

## What lives where (compat shims)

- `~/dev/ad/brains/agentic-factory/dark-factory-catalog/` is now a **symlink** to `~/dev/ad/apps/dark-factory/research/`. Old references still resolve.
- `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/` is the **catalog SKILL** (recon/discover/distill procedure). It still exists in its original location — only the catalog DATA moved.

## Mochaccino server

A Python http.server runs on **:7420** rooted at `mochaccino/`. Pages: `/designs/` (gallery) plus eight designs — `01-pipeline-overview`, `02-mining-view`, `03-triage-console` (canonical-ingestion thread); `04-blackboard-overview`, `05-probe-progression`, `06-blackboard-vs-poem`, `07-workflow-flows`, `08-poem-consolidation` (blackboard→POEM thread). Every design carries a copy-kit (per-section checkboxes + a copy toolbar, via `designs/components/copykit.{css,js}`). If it's not running, restart with:
```bash
cd ~/dev/ad/apps/dark-factory/mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &
```

## Mocha Census (design audit + taste board)

First-class tool at **`tools/mocha-census/`** — finds every Mochaccino design across **both machines**
(M4 Pro local + M4 Mini over Tailscale), screenshots them, and serves a **rate-and-label board**
(love/good/average + free-text labels) whose verdicts distill into the design spec
**`docs/david-design-patterns.md`** + the love-tier exemplar pack. This is the self-improving design
loop: *render → rate → distill → re-render* (proven: `05-dark-factory` good→ `05-dark-factory-v2` love).

- **Operator manual:** `tools/mocha-census/README.md` (how it works, how to run, refresh, modes).
- **Run:** `bash tools/mocha-census/run-full.sh` (full both-machine refresh); board on **:7440** at
  `/out/shots/gallery.html`. The pages are static HTML — `shoot.py` spins up throwaway per-repo servers
  only during capture, nothing stays running.
- **Two modes:** *census* (audit everything, bulk-rate — built now) and *bench* (rate N specific
  variants of one idea side-by-side — planned; the right shape for 1–2 pages).

## Design-Lint (the post-render self-check / "design-loop pass")

First-class tool at **`tools/design-lint/`** — the *machine* half of the taste loop (Mocha Census is the
*human* half). After a render, it screenshots the output (`shoot-one.py`, reuses the census Playwright
pattern) and a **lint agent** critiques it against `RUBRIC.md` (operational extract of
`docs/david-design-patterns.md`), returning a `pass`/`flag` JSON verdict. Flags ONLY three reliable
failures: `cool-on-content`, `missing-warm-anchor`, `amber-orange-on-brown`. **Flags only — no
auto-fix, never policing diagram/colour counts** (avoids the round-04 Goodhart trap).

- **Operator manual / two modes (inline gate · batch audit):** `tools/design-lint/README.md`.
- **⚠️ OPEN placement question (David, 2026-06-10):** built here as the *staged* form (dark-factory
  stages skill code; Shelly/Mochaccino live in tracked appydave-plugins). The likely true home is
  **inside Mochaccino** — Shelly's automated `review`/self-lint mode — not a standalone tool. To
  reconsider before promotion: `backlog/2026-06-10-design-lint-placement-question.md`.

## End-of-session

If you completed a backlog item: mark it complete (rename to `<slug>.done.md` or move to `backlog/done/`) and write a 5-line summary at the bottom of the file.

If you didn't finish: leave the backlog item, append a `## Status` section noting where you stopped and what's blocking.
