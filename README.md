# Dark Factory

A canonical skill library being mined from 13 upstream methodology frameworks (BMAD, gstack, GSD, Spec Kit, Compound Engineering, Agent Skills, Superpowers, Everything Claude Code, Ruflo, gbrain, AppyDave Plugins, POEM, Compound Knowledge), distilled into **David's likeness** — David's patterns, templates, and voice — with **full provenance** back to every origin file.

## Why this exists

The 13-repo cluster ships ~1,100 skills/agents/commands. Most overlap. Many are stack-locked or methodology-locked. None are written in David's voice or compose into David's factory pipeline.

The Dark Factory takes the best mechanisms from those 1,100, **preserves the originals verbatim** (so nothing is lost), and produces a unified canonical set re-authored in David's style. Every canonical artifact carries a provenance chain back to the source files it was mined from.

## Layout

```
.
├── README.md                — this file
├── CLAUDE.md                — orientation for any Claude session opening this repo
│
├── research/                — frozen corpus from the assessment phase
│   ├── artifacts.jsonl       (1,100 source records)
│   ├── distillations/        (76 unified-skill drafts)
│   ├── evaluations/          (88 deep evals)
│   ├── recon/                (13 per-repo shape reports)
│   ├── insights.md           (39+ atomic craft bits)
│   ├── pipeline-matrix/      (11 SDLC stages walked)
│   └── …
│
├── canonical/               — David's library (the build target)
│   ├── INDEX.md              registry of ratified artifacts
│   ├── skills/<name>/
│   │   ├── SKILL.md          David's rewrite
│   │   ├── provenance.json   origin trace
│   │   └── _source/          verbatim origin copies
│   ├── agents/<name>/
│   └── commands/<name>/
│
├── mochaccino/              — visual decision-support workspace
│   └── designs/01-pipeline-overview, 02-mining-view (served on :7420)
│
├── backlog/                 — discrete work items (PO ↔ Dev handover)
│   └── YYYY-MM-DD-<slug>.md
│
├── docs/
│   ├── canonical-form-spec.md     what canonical SKILL.md must contain
│   ├── provenance-spec.md         provenance.json schema + rules
│   ├── ingestion-workflow.md      step-by-step ingest procedure
│   └── david-style-patterns.md    voice and template guide
│
└── tools/                   — scripts for ingest, verify, style-check
```

## The tie to brains

- **Brain** (`~/dev/ad/brains/`) — where conversations happen, where strategic thinking lives. The `agentic-factory/` folder there holds the factory-build-plan, the pipeline matrix as narrative, session handovers, and the cluster maps.
- **This repo** (`~/dev/ad/apps/dark-factory/`) — where the actual work lives. Research data, canonical skills, the visual decision tool.
- **Bridge** — the brain conversations end with a *handover message* + a `backlog/` item in this repo. A Claude session opened in this repo reads the backlog and executes.

A compat symlink at `~/dev/ad/brains/agentic-factory/dark-factory-catalog` → `apps/dark-factory/research` keeps existing skill references working during transition.

## Status

- **Research phase**: complete (1,100 artifacts, 76 distill drafts, 88 deep evals, 11 stage walks).
- **Canonical phase**: not started. Backlog has the first ingestion task.
- **Mochaccino**: live at `http://localhost:7420/designs/`.

---

*Created: 2026-05-18. Moved out of `brains/agentic-factory/dark-factory-catalog/` and `brains/.mochaccino/dark-factory/` on the same day.*
