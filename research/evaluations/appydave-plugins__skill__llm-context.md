---
artifact_id: appydave-plugins:skill:llm-context
repo: appydave-plugins
artifact_type: skill
cluster_facet: [context-assembly, file-pipeline, token-management]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: llm-context

**Intent**: Assembles file contents into LLM-ready payloads via glob patterns or stdin file paths, with smart routing (clipboard if ≤100k tokens, temp file if larger) and multiple output formats.

## Scores

- **quality_score**: 4. The stdin pipe pattern, --smart routing, and token estimation flag are excellent. Well-structured, concise, with real workflow examples. Docked one point for being CLI-tool-specific (appydave-tools dependency).
- **adoption_fit_final**: `mid`. The assembly-with-smart-routing concept is universally applicable; the specific CLI is not. The pattern (query → paths → assemble → clipboard/file) is mineable.
- **inspiration_value**: `mid`. The --smart flag (auto-route by token count) and -t token estimate (dry run) are practical patterns worth capturing.
- **uniqueness_refined**: `uncommon`. Token-aware smart routing as a first-class assembly behavior is not common in skill-based systems.
- **composability**: `called-by-others`. Positioned explicitly as the assembler — downstream of brain-query, app-query, omi-query. The pipeline diagram makes this unambiguous.
- **description_craft_refined**: `trigger`. Description has role-clarity embedded ("This is the ASSEMBLER — downstream of query tools").

## Mineable phrasing

> "This is the ASSEMBLER — downstream of query tools (brain-query, app-query, omi-query). NOT a search/discovery tool."

## Notes

The pipeline diagram (query_brain / query_apps / query_omi → llm_context → LLM payload) is the clearest single-responsibility decomposition diagram in the stage-0 batch. The role label in the description ("ASSEMBLER") and the explicit "NOT a search/discovery tool" negative are strong discovery-design patterns worth replicating in any skill that is easily confused with adjacent skills.
