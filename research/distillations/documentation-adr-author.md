---
distillation_id: documentation-adr-author
stage: system-comprehension
intent: "Capture architectural decisions as ADRs — context, decision, alternatives considered, consequences — with lifecycle management (supersede, not delete)"
created: 2026-05-17
status: draft
source_artifacts:
  - agent-skills-osmani:skill:documentation-and-adrs
  - compound-engineering:agent:ce-ankane-readme-writer
  - gsd:command:milestone-summary
winner_mechanism: agent-skills-osmani:skill:documentation-and-adrs
---

# Unified Skill: adr-author

**Purpose**: Write an ADR (Architecture Decision Record) capturing the context, decision, alternatives considered, and consequences for a significant technical choice. Includes lifecycle management (supersede, not delete).

**For Agents**: Use when user says "write an ADR", "document this decision", "record why we chose X over Y", "create a decision record", "we decided to use X, document it". Distinct from `changelog-author` (post-ship doc update) and `doc-write` (full project documentation sweep).

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Write a decision record that captures the *why* behind a significant technical choice — the context that led to the decision, the alternatives that were considered and rejected, and what the consequences are. Store in `docs/decisions/` with sequential numbering. Lifecycle-safe: new ADRs supersede old ones via reference, never by deletion.

## Winner's Mechanism

`agent-skills-osmani:skill:documentation-and-adrs` provides the most complete ADR authoring system in the corpus:

- **ADR template** with all four required sections: Context, Decision, Alternatives Considered, Consequences
- **Sequential numbering** in `docs/decisions/`
- **Lifecycle states**: PROPOSED → ACCEPTED → SUPERSEDED | DEPRECATED
- **Non-deletion rule**: supersede via reference, never delete. Dead ADRs are archaeologically valuable.
- **"Why, not what" principle**: the central voice discipline — comments on intent, not code restatement
- **Anti-rationalization table**: common excuses vs reality (e.g., "the code is self-documenting" → "code shows what, not why")

The Osmani skill also covers README structure, API documentation, inline comments, and changelog format — a broader "documentation" skill. For the purposes of this distillation, the ADR-specific mechanism is the target. The README structure and inline comment guidelines are better served by `doc-write` (README generation) and `doc-review-comment-accuracy` (comment review).

## Non-overlapping ideas to fold in

- From `compound-engineering:agent:ce-ankane-readme-writer`: **named-style constraint** — when generating a README, explicitly reference a style exemplar (Andrew Kane's style: imperative voice, 1-3 lines of description, minimal prose, heavy code examples). This model — "write in the style of X" — can apply to ADRs too: "write this ADR the way a senior engineer would explain it to a new team member" — `complexity: low | optional: false | prerequisite: none`.

- From `gsd:command:milestone-summary`: **decision framing for non-engineers** — when the ADR captures a decision with stakeholder impact, generate an additional plain-English summary paragraph (1-3 sentences, no jargon) suitable for a milestone summary or client communication — `complexity: low | optional: true | prerequisite: "ADR has stakeholder impact (user-facing, cost, timeline)"`.

- From `agent-skills-osmani` verification checklist: **post-write checklist** — after writing the ADR: confirm ADR exists for all significant architectural decisions, confirm superseded ADRs reference the new one, confirm no dead TODOs in consequences section — `complexity: low | optional: false | prerequisite: none`.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `agent-skills-osmani:documentation-and-adrs` | ADR template + lifecycle + non-deletion rule + anti-rationalization table + verification checklist | README structure (→ doc-write), inline comment guidelines (→ doc-review-comment-accuracy), changelog format (→ changelog-author) |
| `ce-ankane-readme-writer` | Named-style constraint model | Ruby-gem-specific README formatting details |
| `gsd:milestone-summary` | Plain-English stakeholder summary fold-in | GSD planning artifact dependency |

## Draft SKILL.md frontmatter

```yaml
name: adr-author
description: "Write an Architecture Decision Record capturing context, decision, alternatives, and consequences. Use when: 'write an ADR', 'document this decision', 'record why we chose X', 'create a decision record', 'we decided to use X document it', 'architectural decision'."
argument-hint: "[decision title or blank to prompt for details]"
allowed-tools: Bash(ls *), Read, Write
```

## Open questions for David

1. **Scope overlap with `doc-write`**: `doc-write --type=architecture` and `adr-author` both touch architectural documentation. Should `adr-author` be invoked as a sub-step inside `doc-write` (when architecture mode detects a decision-worthy change), or remain fully standalone?

2. **ADR template rigidity**: Osmani's template is four-section. Some teams use a simpler "MADR" (Markdown Any Decision Record) format with a shorter structure. David's existing ADR format (if any) should win — does David have any existing ADRs in his repos that define the current template?

3. **Cluster status**: This is a small cluster (1 clear winner + 2 contributing ideas). It could be folded into `doc-write` as a `--type=adr` mode rather than a standalone skill. Standalone is more ergonomic for on-demand use. Recommend standalone.
