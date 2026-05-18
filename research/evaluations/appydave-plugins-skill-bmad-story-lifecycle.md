---
artifact_id: appydave-plugins:skill:bmad-story-lifecycle
repo: appydave-plugins
artifact_type: skill
cluster_facet: [orchestration, planning]
phase_fit: [1, 2, 9]
evaluated_at: 2026-05-17
---

# Eval: bmad-story-lifecycle

**Intent**: Launches and manages the full BMAD story lifecycle via Claude Code multi-agent teammate orchestration — environment detection, agent chain spawning, gate protocol, and persistent Swagger log.

## Scores

- **quality_score**: 5 — This is one of the highest-quality orchestration skills in the catalog. The environment detection (mode 1/2/3 via env vars, not invocation method) is a sophisticated runtime disambiguation pattern. The Swagger gate protocol (full diagnostic → Swagger's Take → "→ say 'go'" prompt) preserves human agency at every gate while minimizing friction. The constraint that "Mode 2 is BROKEN in 2.1.212" is brutally honest production documentation — not aspirational. The Swagger log (written after every gate to story file) is the persistence mechanism that survives context resets. The distinction between Mode 1 (Agent Teams) and Mode 3 (sequential Skill calls) with clear fallback logic is genuinely production-quality harness design.
- **adoption_fit_final**: mid — The skill is tightly coupled to BMAD agent names (Bob, Amelia, Nate, Taylor, Lisa, Swagger) and the BMAD project structure (`_bmad-output/`, `sprint-status.yaml`). The harness orchestration patterns (env-detection, gate protocol, agent-log persistence) are broadly applicable. The BMAD-specific routing cannot be adopted without also adopting BMAD methodology, but the structural patterns can be extracted.
- **inspiration_value**: high — The gate protocol design (synthesized recommendation, not a neutral menu; "→ say 'go'" prompt; full diagnostic before judgment) is the most sophisticated human-gate design in the catalog. The env-var-based mode detection ("invocation method is NOT a reliable signal — ignore it") is a hard-won production insight. The Swagger log persistence pattern (append after every gate, survive context reset) is portable to any multi-session orchestrator.
- **uniqueness_refined**: rare — Multi-agent orchestration with per-gate synthesis + persistence + env-based mode detection in a single skill is uncommon. Most orchestration skills either lack the gate synthesis or the persistence mechanism.
- **composability**: calls-others — Swagger orchestrates Bob/Amelia/Nate/Taylor/Lisa via TeamCreate + Agent tool. It is the root of a multi-agent tree.
- **description_craft_refined**: trigger — Excellent trigger phrase coverage; also communicates the output deliverables (infrastructure start block, orchestrator prompt, paste-ready command sequence).

## Mineable phrasing

> "The invocation method (Skill tool vs tmux pane) is NOT a reliable signal — ignore it. Check the env vars."

## Notes

The Swagger gate protocol is the design pattern worth extracting: at every human gate, present full unfiltered agent output followed by a distinct "Swagger's Take" synthesis section with a concrete recommendation and a "→ say 'go'" prompt. This prevents the most common multi-agent failure mode — routing raw agent output to the user without synthesis, leaving them to interpret competing signals. The story-file log (written after every gate) is the observability mechanism that makes multi-session orchestration tractable. Both patterns are portable without BMAD methodology. Ruflo-independent.
