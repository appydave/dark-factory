---
distillation_id: delivery-readiness-milestone-ship-ceremony
stage: delivery-readiness
intent: "Close out a completed milestone — verify all work landed, update version artifacts, archive planning state, and record what shipped"
created: 2026-05-17
status: draft
source_artifacts:
  - gsd:command:complete-milestone
  - gsd:command:cleanup
  - gsd:command:stats
  - gsd:command:progress
  - gsd:command:audit-milestone
  - gsd:command:audit-uat
  - gsd:command:plan-milestone-gaps
  - agent-skills-osmani:skill:deprecation-and-migration
  - agent-skills-osmani:skill:ci-cd-and-automation
  - appydave-plugins:command:flivideo:progress
winner_mechanism: gsd:command:complete-milestone
---

# Unified Skill: Milestone Ship Ceremony

**Purpose**: For Agents: Use when David says "complete milestone", "close this milestone", "archive the milestone", "what shipped in v1.0", "prepare for next version", "milestone complete".

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

## Intent

Run the end-of-milestone ceremony: verify all planned work is complete (audit-milestone), surface any outstanding UAT gaps (audit-uat), archive the milestone phases, update ROADMAP.md, git-tag the historical record, and produce a stats summary of what shipped.

## Winner's Mechanism

`gsd:complete-milestone` wins because it is the only artifact in this cluster that actually executes the ceremony as a structured workflow: mark milestone complete → archive phases to `milestones/v{X.Y}-phases/` → update planning files → git-tag the record. It is production-tested in GSD's own development. The verification sub-commands (`audit-milestone`, `audit-uat`) compose naturally as pre-conditions.

No David-stack equivalent exists. This is a net-new capability if David adopts GSD's planning structure. If not, the patterns are still worth distilling for any project with milestones.

## Existing-skill nesting

David has no milestone ceremony skill. Net-new build.

Skip this section — from-scratch build.

## Non-overlapping ideas folded in

- From `gsd:audit-milestone`: Pre-archive audit — verify milestone achieved definition of done before archiving, spawn integration checker for cross-phase wiring — `complexity: medium | optional: false | prerequisite: milestone has VERIFICATION.md files`. Prevents archiving an incomplete milestone as "done".
- From `gsd:audit-uat`: UAT gap surface before closing — scan all phases for pending/skipped/blocked UAT items, cross-reference against live codebase for stale documentation — `complexity: low | optional: true | prerequisite: phases have UAT sections in PLAN.md`. Catches "code shipped but UAT doc not updated" before it becomes invisible technical debt.
- From `gsd:plan-milestone-gaps`: Gap-to-phase promotion — converts gaps found in audit into new ROADMAP phases rather than losing them — `complexity: low | optional: true | prerequisite: audit found gaps`. Ensures gaps from the ceremony become first-class backlog items, not forgotten notes.
- From `gsd:stats`: Shipped metrics — phases, plans, requirements completion, git history stats, timeline — `complexity: low | optional: false | prerequisite: none`. The ceremony should produce a record of what was built, not just that it was archived.
- From `gsd:cleanup`: Phase directory cleanup — archive accumulated phase directories after milestone complete — `complexity: low | optional: false | prerequisite: .planning/phases/ has accumulated directories`. Standard hygiene step; pairs with complete-milestone.
- From `agent-skills-osmani:deprecation-and-migration`: Safe removal checklist when a milestone includes sunset work — verify removal is complete, users notified, no orphan references — `complexity: medium | optional: true | prerequisite: milestone includes deprecation work`. Relevant when a milestone retires a feature or API.
- From `agent-skills-osmani:ci-cd-and-automation`: Quality gate verification as part of ceremony — confirm that the CI pipeline configuration matches what was promised in the milestone's definition of done — `complexity: medium | optional: true | prerequisite: milestone changes CI configuration`. Prevents "we said we'd add a linter check but forgot".
- From `gsd:progress` + `appydave:flivideo-progress`: Progress check as ceremony opener — before running the audit, show current state so David can see where things stand — `complexity: low | optional: false | prerequisite: none`. Situational awareness before deciding whether to proceed with ceremony or continue work.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `gsd:complete-milestone` | Full workflow: mark done, archive, update planning files, git-tag | GSD's `.planning/phases/` file naming convention (adaptable) |
| `gsd:audit-milestone` | Pre-archive verification + integration checker pattern | `gsd-security-auditor` agent spawn (already in pre-merge-gate distillation) |
| `gsd:audit-uat` | UAT gap cross-reference against live codebase | GSD's UAT section format in PLAN.md |
| `gsd:plan-milestone-gaps` | Gap-to-phase promotion after audit | GSD's 999.x backlog numbering |
| `gsd:stats` | Shipped metrics output format | GSD's specific git metric queries |
| `gsd:cleanup` | Phase directory archival pattern | GSD's archive path convention |
| `gsd:progress` | Progress-first opener pattern | GSD's STATE.md routing |
| `agent-skills-osmani:deprecation-and-migration` | Removal checklist for sunset work | Anti-rationalization table format |
| `agent-skills-osmani:ci-cd-and-automation` | CI gate verification step | Full CI/CD setup scope (separate concern) |
| `appydave:flivideo-progress` | Progress tracking concept | FliVideo-specific implementation |

## Draft SKILL.md frontmatter

```yaml
name: session-checkpoint
description: "Close out a completed milestone — audit completion, surface UAT gaps, archive planning phases, update version artifacts, git-tag the historical record, and produce shipped metrics. Use when: 'complete milestone', 'close this milestone', 'archive the milestone', 'milestone complete', 'prepare for next version', 'what shipped in v1.x'."
argument-hint: "[version, e.g. v1.0]"
allowed-tools: "Read, Write, Bash(git:*), Bash(gh:*), Glob, Grep"
```

**Note**: `session-checkpoint` already exists in David's stack. Before building this as a new skill, check whether this ceremony should be folded into `session-checkpoint` as a "milestone mode", or whether it merits a distinct `milestone-ceremony` skill.

## Open questions for David

1. **GSD dependency**: This distillation assumes GSD's `.planning/` structure. Does David use GSD on any active projects (SupportSignal, FliVideo, AppyStack)? If not, the ceremony pattern is still valuable but needs a lighter file convention (could be just a CHANGELOG.md + git tag).

2. **session-checkpoint vs milestone-ceremony**: David already has `session-checkpoint` for per-session knowledge capture. A milestone ceremony is a different grain (per-version, not per-session). Are these two separate skills, or should `session-checkpoint` have a `--milestone` mode?

3. **Stats persistence**: `gsd:stats` produces metrics but doesn't persist them. Should the ceremony write a `SHIPPED.md` (or CHANGELOG entry) with the metrics, so future David can see what was built in each version?
