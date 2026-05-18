---
artifact_id: appydave-plugins:skill:browse-with-me
repo: appydave-plugins
artifact_type: skill
cluster_facet: [browser-automation, hitl, tool-selection]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: browse-with-me

**Intent**: Routes browser automation tasks to the right tool (Playwright MCP, agent-browser, Chrome DevTools, Chrome Extension) based on session length and context, with a HITL pause protocol.

## Scores

- **quality_score**: 4. Strong routing table, excellent HITL pause protocol with exact output format, clear headed/headless rule. Docked one point: some references marked "(not yet tested)" — signals incomplete maturity.
- **adoption_fit_final**: `mid`. The tool-selection decision table and HITL protocol are stack-agnostic and highly adoptable; specific MCP tool names are environment-locked.
- **inspiration_value**: `high`. The HITL pause block format (URL / What I see / screenshot / "How would you like to proceed?") is immediately reusable in any agentic flow involving human checkpoints.
- **uniqueness_refined**: `uncommon`. Tool-routing skill combining five browser approaches in one decision framework is unusual.
- **composability**: `calls-others`. Delegates to reference files per tool; designed as a dispatcher.
- **description_craft_refined**: `trigger`. Description is an exhaustive list of trigger phrases — possibly over-specified but very discoverable.

## Mineable phrasing

> "David watches. You drive. Pick the right tool, then operate it."

## Notes

The "Snapshot before screenshot" rule (use accessibility tree first, screenshots only when visual confirmation needed) encodes a cost-aware practice that goes beyond most browser-automation skills. The HITL pause format is mineable verbatim. The headed-always rule is a strong example of encoding operator preferences as a non-negotiable constraint inside the skill body.
