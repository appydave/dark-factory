# YLO Experiment — Blackboard Workflow Probes

Bash + jq + curl implementation of the **blackboard workflow pattern** (per `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md`). Four probes have run against the b65 Guy Monroe transcript, each testing one dimension of the pattern.

**For full context, recipes, file map, and open loops — read [`HANDOVER.md`](HANDOVER.md).**

## The four probes at a glance

| # | Workflow file | Tested |
|---|---------------|--------|
| 1 | `workflow-01-analysis.json` | Parallel fan-out — 12 subagents extract content-analysis fields |
| 2 | `workflow-02-titles.json` | Scripted refinement + `outputKeyMap` key rename |
| 3 | `workflow-03-titles-human.json` | Real human-in-the-loop gate (typed critique) |
| 4 | `workflow-04-thumbnails.json` | Async kie.ai API + binary artifacts + title-thumbnail pairing |

All four passed acceptance criteria. Isolation discipline held in every run — orchestrator never ingested step payloads.

## Skills (project-local)

```
.claude/skills/
├── conductor/SKILL.md      ← orchestrator role
├── store/SKILL.md          ← bash+jq EAV operations
└── image-gen/SKILL.md      ← kie.ai async wrapper
```

## Visualisations

Mochaccino designs at `../mochaccino/designs/`:

- `04-blackboard-overview` — architecture diagram (orchestrator / store / subagents / contracts)
- `05-probe-progression` — the four probes as a timeline, what each tested, key learnings

Run server: `cd mochaccino && python3 -m http.server 7420` → http://localhost:7420/designs/

## Start here

If you want to:
- **Understand the pattern** → read [`HANDOVER.md`](HANDOVER.md) §1–§7
- **Build a new workflow** → read [`HANDOVER.md`](HANDOVER.md) §2 (quickstart) and §8 (recipe)
- **Resume from another machine** → read [`HANDOVER.md`](HANDOVER.md) end-to-end
- **Browse outputs** → `runs/b65/` and `runs/b65-2-5/`
- **See visual mockups** → start the mochaccino server (above)
