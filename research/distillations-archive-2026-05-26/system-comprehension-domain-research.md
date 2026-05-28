---
distillation_id: system-comprehension-domain-research
stage: system-comprehension
intent: "Research a domain, technology stack, or market ecosystem before committing to a technical or strategic direction"
created: 2026-05-17
status: draft
source_artifacts:
  - bmad-method:skill:bmad-domain-research
  - bmad-method:skill:bmad-market-research
  - bmad-method:skill:bmad-technical-research
  - compound-engineering:agent:ce-best-practices-researcher
  - compound-engineering:agent:ce-framework-docs-researcher
  - compound-engineering:agent:ce-web-researcher
  - gsd:command:gsd:research-phase
  - gsd:agent:gsd-phase-researcher
  - gsd:agent:gsd-project-researcher
winner_mechanism: gsd:agent:gsd-phase-researcher (most precisely defined research contract)
---

# Unified Skill: Domain Research (pre-implementation research)

**Purpose**: Before planning or implementing in an unfamiliar domain or with an unfamiliar technology, conduct structured research that answers a specific question: "What do I need to know to plan this well?" Produces a RESEARCH.md consumed downstream by planning.

## Intent

Research a domain, technology, framework, or market ecosystem to produce structured findings that unblock downstream planning or implementation. The key question is always: "What do I need to know to plan this phase/project well?" — not open-ended exploration.

## Winner's Mechanism

`gsd:agent:gsd-phase-researcher` wins on precision. It answers a specific question ("What do I need to know to PLAN this phase well?") rather than conducting open-ended domain exploration. Its output is RESEARCH.md — a typed artifact consumed by `gsd-planner`. This "research to answer a planning question" framing is sharper than BMAD's triplet (domain/market/technical are separate skills) or CE's open-ended researchers.

BMAD's three research skills (domain/market/technical) are the right **decomposition vocabulary** but they're under-specified. They trigger on broad phrases and produce unstructured output. Adopting GSD's "answer the planning question" constraint would make them more useful.

CE's `ce-framework-docs-researcher` is the best of CE's three: it fetches version-specific documentation via Context7 MCP, which prevents stale training-data patterns. The anti-stale-docs concern is real and absent from both GSD and BMAD.

## Existing-skill nesting

No direct David equivalent. BMAD's three research skills are available but thin. This is primarily a documentation of the sub-cluster and an upgrade proposal for BMAD research skills.

Skip nesting section — from-scratch addition or BMAD upgrade.

## Non-overlapping ideas folded in

- From `gsd:agent:gsd-phase-researcher`: **planning-question-anchored research contract** — `complexity: low | optional: false | prerequisite: none`. Every research session should start with an explicit question: "What do I need to know to plan X well?" This constraint prevents research drift (open-ended exploration that never lands). The contract: research produces RESEARCH.md answering EXACTLY this question, nothing else.

- From `compound-engineering:agent:ce-framework-docs-researcher`: **version-specific doc fetching over training data** — `complexity: medium | optional: false | prerequisite: research involves a framework/library with active releases`. CE explicitly fetches current official docs (via Context7 MCP or web) rather than relying on training data. Training data for any framework may be 1-2 major versions stale. For implementation research, version-specificity is a correctness requirement, not an optimization.

- From `gsd:agent:gsd-project-researcher`: **ecosystem-first before roadmap** — `complexity: low | optional: true | prerequisite: new project or milestone`. Before creating a roadmap, research "what does this domain ecosystem look like?" — not the implementation details, the landscape. Understanding competing tools, community conventions, and integration patterns before roadmapping prevents fundamental direction errors.

- From `bmad-method:skill:bmad-technical-research`: **produce a technical research report** — `complexity: low | optional: true | prerequisite: research will be reviewed by stakeholders`. BMAD's output is a structured report that can be presented. GSD's RESEARCH.md is internal planning input. When research needs to be shareable (stakeholder review, architecture decision record), the BMAD output format is more appropriate.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `gsd:agent:gsd-phase-researcher` | "Planning question" research contract; RESEARCH.md typed output | GSD planning pipeline dependency (make output standalone) |
| `gsd:agent:gsd-project-researcher` | Ecosystem-first framing before roadmap | GSD milestone lifecycle dependency |
| `compound-engineering:agent:ce-framework-docs-researcher` | Version-specific doc fetching anti-pattern (don't use training data for framework docs) | Context7 MCP dependency (use web fallback instead) |
| `compound-engineering:agent:ce-best-practices-researcher` | Curated-knowledge-first lookup before web | Community-forum sourcing heuristic |
| `compound-engineering:agent:ce-web-researcher` | Iterative web research pattern; prior art scan | Iterative search loop (not necessary for single-question research) |
| `bmad-method:skill:bmad-domain-research` | Domain decomposition vocabulary | Open-ended trigger without planning anchor |
| `bmad-method:skill:bmad-market-research` | Market/competitor research framing | Same |
| `bmad-method:skill:bmad-technical-research` | Shareable report output format | Same |
| `gsd:command:gsd:research-phase` | Standalone invocation (orchestrator-independent) | GSD internal invocation path |
| `gsd:agent:gsd-phase-researcher` | Winner mechanism | See above |

## Draft SKILL.md frontmatter

```yaml
name: research
description: >
  Conduct structured pre-planning research on a domain, technology, framework, or market.
  Answers one question: "What do I need to know to plan this well?"
  Use when the user says "research X before we start", "what do I need to know about X",
  "domain research for X", "technical research on X", "market research for X",
  "investigate options for X", "what's the ecosystem for X", "framework research",
  "best practices for X", "how should we approach X technology".
  Distinct from investigate (debugging/forensics) and system-context (codebase comprehension).
  Produces RESEARCH.md or a structured findings report.
argument-hint: "[domain|technical|market|ecosystem] <topic>"
allowed-tools: "Bash(curl:*), Read, Write, WebFetch, WebSearch"
```

## Open questions for David

1. **Three BMAD skills vs one unified**: BMAD has three research skills (domain/market/technical). Should David have three separate skills (matching BMAD's decomposition) or one unified `/research` skill with a topic-type parameter? The three-skill design is more ergonomic but adds routing surface; the unified design is simpler.

2. **Context7 dependency**: CE's `ce-framework-docs-researcher` uses Context7 MCP for version-specific docs. David doesn't have Context7 installed. Is WebFetch to official docs sufficient as a fallback, or is Context7 worth adding to the stack?

3. **Research output format**: GSD writes RESEARCH.md (internal planning input). BMAD writes a technical research report (shareable). Should David default to RESEARCH.md (planning-anchored, internal) with an `--report` flag for the shareable format, or vice versa?
