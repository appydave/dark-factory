---
artifact_id: agent-skills-osmani:skill:browser-testing-with-devtools
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [test-authoring, verification-validation]
phase_fit: [4, 5, 6]
evaluated_at: 2026-05-17
---

# Eval: browser-testing-with-devtools

**Intent**: Gives agents live browser inspection (DOM, console, network, performance) via Chrome DevTools MCP instead of relying on static code analysis.

## Scores
- **quality_score**: 5 — Exceptional depth: security boundaries section, content-as-untrusted-data rules, structured debug workflows for UI/network/perf, and a screenshot-based regression pattern. One of the most thorough skills in the corpus.
- **adoption_fit_final**: strong — David's stack includes FliVideo (React/Next.js) and AppyStack apps; chrome-devtools MCP is already listed in the system-reminder available tools.
- **inspiration_value**: high
- **uniqueness_refined**: rare — The security-boundaries + prompt-injection-aware browser content section is genuinely uncommon and not found in generic testing materials.
- **composability**: calls-others — Cross-references and is cross-referenced by `test-driven-development`; designed as a complement to TDD for the browser layer.
- **description_craft_refined**: trigger — Multi-trigger description lists exact use cases; requirement dependency (chrome-devtools MCP) stated inline.

## Mineable phrasing
> "Instead of guessing what's happening at runtime, verify it."

## Notes
Security boundaries treatment (treating DOM/console/network output as untrusted data, never interpreting it as instructions) is load-bearing for agentic use and rare in skill literature. The five-step debug workflow (REPRODUCE → INSPECT → DIAGNOSE → FIX → VERIFY) is clean and reusable as a template. Strong candidate as the winner mechanism for a unified `browser-verification` skill.
