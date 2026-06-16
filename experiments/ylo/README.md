# YLO Experiment — Cross-Substrate Summary

**Scenario**: YouTube Launch Optimizer (YLO) — Guy Monroe b65 run (Marketing Plan video)  
**Substrates tested**: Blackboard (`blackboard/`) · Workflow Tool (`workflow-tool/`)  
**Probes**: #1 bulk content analysis · #2 scripted title critique · #3 human-gated titles · #4 kie.ai thumbnails  
**Status**: All 4 probes complete on both substrates ✅

---

## Recommendation — Hybrid

**Use Workflow Tool for #1 and #4. Use Blackboard for #2 and #3.**

| Probe | Recommended substrate | Reason |
|-------|----------------------|--------|
| #1 — bulk content analysis (70 videos) | **Workflow Tool** | Native `pipeline()` fan-out, schema per-item, no HITL needed |
| #2 — title gen + scripted critique | **Blackboard** | Sequential + store-heavy; Workflow Tool is 5× slower |
| #3 — human-gated title refinement | **Blackboard** | Native HITL step type; DIY two-pass in Workflow Tool is awkward |
| #4 — thumbnail gen (kie.ai parallel) | **Workflow Tool** | Parallel image jobs, schema-validated, no HITL |

Do not migrate probes #2 and #3 to Workflow Tool. The performance gap is structural (see below).

---

## Empirical comparison (probe #2 — same task, both substrates)

| Dimension | Blackboard | Workflow Tool | Winner |
|-----------|------------|---------------|--------|
| Wall-clock time | ~56s | ~284s (4.7×) | Blackboard |
| Agent calls | 2 | 9 | Blackboard |
| Store records written | 33 | 5 | Blackboard (more granular) |
| Lines of orchestration code | ~240 (3 files) | 144 (1 JS file) | Workflow Tool |
| Schema enforcement | DIY | Native per-agent retry | Workflow Tool |
| Parallel fan-out | Awkward | Native `parallel()`/`pipeline()` | Workflow Tool |
| HITL support | Native step type | DIY two-pass | Blackboard |
| Resumability | Via store projection | `scriptPath` + `resumeFromRunId` | Tie |

**Root cause of 5× gap**: The Workflow VM has no filesystem access. Every `remember()` call (store write) costs one full agent round-trip (~15–30s). Blackboard writes directly via bash — store writes are free.

---

## Run directories

```
experiments/ylo/
├── blackboard/          ← was ylo-experiment/
│   ├── workflow-01-analysis.json       (probe #1)
│   ├── workflow-02-titles.json         (probe #2)
│   ├── workflow-03-titles-human.json   (probe #3)
│   ├── workflow-04-thumbnails.json     (probe #4)
│   ├── prompts/
│   ├── HANDOVER.md
│   └── runs/
│       ├── b65/                       (probes #1–#4 blackboard runs)
│       └── b65-2-5/                   (probe #3 HITL run)
└── workflow-tool/       ← was anthropic-workflow-experiment/
    ├── comparison.md                  (probe #2 detailed write-up)
    └── runs/
        ├── b65/                       (probe #2 Workflow Tool run)
        └── b65-p1/                    (probes #1–#4 Workflow Tool runs)
            ├── store.jsonl            (30 records — all 4 probes)
            ├── transcript.txt
            ├── thumbnails-manifest.md
            └── thumbs/               (6 exp + 3 final images)
```

Workflow scripts live in `.claude/workflows/` (enforced by Claude Code — do not move):
- `content-analysis.workflow.js` — probe #1
- `title-gen.workflow.js` — probe #2
- `titles-human.workflow.js` — probe #3
- `thumbnails.workflow.js` — probe #4

---

## Authoring notes and gotchas

See `docs/workflow-tool-authoring-notes.md` for the full list. Key issues from session 2:

- `parallel()` requires thunks `() => agent()`, not bare `agent()` calls — every script had this wrong
- Phase labels in `agent({phase})` must exactly match `meta.phases` titles or the agent runs invisibly
- The Workflow tool snapshots scripts at launch — edit the generated copy in the session dir to fix a live run
- `resumeFromRunId` loses args — always re-pass them
- API agent prompts must include explicit non-2xx bail and poll cap — agents don't fail fast otherwise
- API keys don't flow to subagents via shell env — read from `.env` file explicitly in the prompt

---

## Open questions

- Can the Workflow VM call MCP tools directly? If yes, a `store` MCP eliminates the I/O overhead
- Does `env` in `.claude/settings.json` reach workflow subagents? Would clean up the API key pattern
- Is `model: "haiku"` viable for `remember()`/`recall()` agents? Expected ~5× speedup on I/O
- Is double-nesting of recall values consistent and characterisable?
