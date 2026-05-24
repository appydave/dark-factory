# Restructure experiment directories — group by scenario, then substrate

**Date**: 2026-05-24
**Status**: ready
**Priority**: medium
**Estimated effort**: 30 minutes (mostly `git mv` + path-reference fixups)

---

## 🎯 Goal

Move the two experiment directories currently sitting at the repo root into a single `experiments/` parent, grouped by **scenario** first and **substrate** second. The current flat layout conflates "what we're testing" (YLO title generation, thumbnails, etc.) with "how we're testing it" (blackboard, Anthropic Workflow Tool).

---

## Current layout

```
dark-factory/
├── experiments/ylo/blackboard/                       ← blackboard substrate, 4 probes
│   ├── workflow.json                     (probe #1: bulk content analysis)
│   ├── workflow-titles.json              (probe #2: scripted critique)
│   ├── workflow-titles-human.json        (probe #3: real HITL)
│   ├── workflow-thumbnails.json          (probe #4: kie.ai thumbnails)
│   ├── prompts/
│   └── runs/b65/, runs/b65-2-5/
└── experiments/ylo/workflow-tool/        ← Workflow Tool substrate
    └── runs/b65/                         (probe #2 done; probe #1 staged at runs/b65-p1/)
```

## Target layout

```
dark-factory/
└── experiments/
    └── ylo/
        ├── README.md                     ← summary + cross-substrate findings
        ├── blackboard/                   ← was experiments/ylo/blackboard/
        │   ├── workflow.json
        │   ├── workflow-titles.json
        │   ├── workflow-titles-human.json
        │   ├── workflow-thumbnails.json
        │   ├── prompts/
        │   ├── HANDOVER.md
        │   └── runs/b65/, runs/b65-2-5/
        └── workflow-tool/                ← was experiments/ylo/workflow-tool/
            ├── comparison.md             ← side-by-side write-up
            └── runs/b65/, runs/b65-p1/
```

The workflow scripts themselves (`.claude/workflows/*.workflow.js`) stay where they are — that path is enforced by Claude Code.

---

## Why scenario-first, not substrate-first

- A third substrate (say, AWB or Inngest) just becomes `experiments/ylo/awb/` — no rename
- A second scenario (e.g. thumbnail-gen as its own experiment) becomes `experiments/thumbnail-gen/` — clear separation
- Side-by-side comparisons live under the same parent (`experiments/ylo/`) — easier to diff `b65/store.jsonl` across substrates
- The README at `experiments/ylo/` becomes the canonical entry-point for "what did we learn about YLO"

---

## Steps

1. `mkdir -p experiments/ylo`
2. `git mv experiments/ylo/blackboard experiments/ylo/blackboard`
3. `git mv experiments/ylo/workflow-tool experiments/ylo/workflow-tool`
4. **Path fixups** — grep + update references:
   - `grep -rln "experiments/ylo/blackboard" .` (excluding `.git`, `research/`) → update to `experiments/ylo/blackboard`
   - `grep -rln "experiments/ylo/workflow-tool" .` → update to `experiments/ylo/workflow-tool`
   - Known callers to check:
     - `backlog/done/2026-05-25-workflow-tool-run-and-compare.done.md`
     - `experiments/ylo/workflow-tool/runs/b65/comparison.md`
     - `~/dev/ad/brains/ylo/recommendations.md` (uses `apps/dark-factory/experiments/ylo/workflow-tool/...`)
     - `~/dev/ad/brains/anthropic-claude/claude-code/workflow-tool.md`
     - The `dark-factory-catalog` skill paths (check `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/`)
5. **Workflow script args** — update default `transcriptPath`/`storePath` examples in `.claude/workflows/*.workflow.js` if any are hard-coded
6. Update `CLAUDE.md` (the project one) — change the "Where to write" table and any other path references
7. Write `experiments/ylo/README.md` — pull the cross-substrate findings (the table from `comparison.md`) up to this level
8. Commit with one focused message
9. Verify nothing breaks by running `grep -rln "experiments/ylo/blackboard\|experiments/ylo/workflow-tool" .` — should return nothing outside `.git/`

---

## ⚠️ Don't break

- `research/` references — the dark-factory-catalog SKILL depends on `research/` paths being stable. The catalog symlink at `~/dev/ad/brains/agentic-factory/dark-factory-catalog/ → research/` must still resolve.
- The mochaccino designs reference experiment paths in their narrative — check `mochaccino/designs/04-blackboard-overview/` and `05-probe-progression/` for hardcoded paths.
- `.claude/workflows/` — Claude Code looks here at session boot. Do NOT move workflow scripts under `experiments/`.

---

## Open question (for the person doing this)

Should `experiments/ylo/README.md` consolidate the recommendation (Hybrid: Workflow Tool for #1/#4, blackboard for #2/#3), or keep that in `workflow-tool/comparison.md` and have the README just link? Lean toward consolidate — the comparison file's purpose was to write up one substrate's run, not host the cross-cutting decision.
