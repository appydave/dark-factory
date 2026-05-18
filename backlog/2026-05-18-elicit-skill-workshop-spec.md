# Backlog — Elicit Spec for the Skill Workshop App

**Target**: Produce a ratified spec document for the **dark-factory skill workshop app** — David's control plane for browsing, refreshing, assessing, creating, and upgrading skills mined from upstream methodology frameworks (and his own).

**Priority**: First. Blocks all other build work on the app, including the previously-queued `2026-05-18-build-triage-console.md` backlog item.

**Methodology**: **Osmani `spec-driven-development`** with `interview-me` for Phase 1 elicitation.

**Created**: 2026-05-18
**Status**: open
**PO**: David (via brain session 2026-05-18)

---

## Why this exists

The triage console started as a "fix the prose problem" view but David's framing has grown:

> "I feel like I'm starting to build this concept of an app just so I can understand how to build the workflow. What I need to be able to do is teach any part of the software development life cycle. Add a new skill into it. The skill needs to show a pattern, its own template design that we are going to build based on a combination of the skill, the creator skill, and probably the best of the best from what we have seen so far... we need to be able to bring over a skill, analyse it, see how it fits into our template, and compare how it fits into our template... we can build a control plane for building out our agents based off other people's great work."

This is a real app. Building features (like the triage console) before the broader spec exists invites scope drift and pattern inconsistency. Spec first; build second.

## Methodology choice (PO has already picked)

**Osmani `spec-driven-development`** — read at:
- Plugin: `~/dev/upstream/repos/agent-skills/skills/spec-driven-development/SKILL.md`
- Verbatim copy will live at `canonical/skills/spec-driven-development/_source/` after that skill is ingested (TBD — separate backlog)

Why this and not Spec Kit or GSD: see `backlog/2026-05-18-elicit-skill-workshop-spec.md` opening message + PO's notes in the brain session 2026-05-18. Short version: lightweight, solo-friendly, assumption-surfacing before spec content, pairs with `interview-me`. We rated it 5/5 in the eval pass.

Phase 1 (elicitation) uses **Osmani `interview-me`** discipline:
- One question at a time, conversationally
- After each answer: state your hypothesis of David's intent + a confidence number (0-100)
- Watch for "want vs should want" — when David's answer sounds like he's justifying to an imagined audience, ask the rephrase: *"If you didn't have to justify this to anyone, what would you actually want?"*
- Stop questioning a topic when you reach 95% confidence
- Move topics in the order below; don't jump ahead

## Topics to cover in the interview (order matters)

Cover these in this order. Don't move on from one until you have 95% confidence + David has confirmed the captured hypothesis.

1. **Primary use case** — what's the single most valuable thing the app does on day one? What scenario is David thinking of when he uses it next week?
2. **Source of truth model** — where do skills "live" canonically? (Upstream repos? Local clones? Both?) How does the app refer to them?
3. **Refresh detection** — three types David named: (a) prompt I've seen has changed, (b) new prompt appeared, (c) prompt deprecated. How does the app detect each? How does it surface them? *Hint*: probably a "Refresh Inbox" feature, but let David shape it.
4. **Browse / filter / drill** — the triage-console use case. Triggers: name, cluster, stage, repo, quality, mineable-phrase presence. What other axes matter? What happens after drill?
5. **Assessment metrics** — David said "I'm not sure of the different metrics that do that." Walk him through the dimensions we already have (quality_score, adoption_fit, uniqueness, composability, description_craft, inspiration_value) — confirm which he cares about, add any missing.
6. **Template fit comparison** — David's canonical template lives at `docs/canonical-form-spec.md`. How does the app SHOW a candidate skill's distance from / alignment to that template? (Side-by-side diff? Score per facet? Visual overlap?)
7. **Create capability** — how does David author a new skill in his own style from inside the app? Does he write it directly, or does the app dispatch to **POEM Penny** (`~/dev/clients/supportsignal/prompt.supportsignal.com.au/.claude/commands/poem/agents/penny.md`) for the prompt-craft work? PO's lean: dispatch to Penny; the workshop handles bookkeeping. Confirm with David.
8. **Upgrade capability** — same question but for David's existing skills. Pick one of his (e.g. `delivery-review` or `review-blind-hunter`) and walk through what "upgrade in the workshop" would do step by step.
9. **Control plane scope** — what does David NOT want this app to do? (Examples that probably qualify: shipping the app as a product, multi-user mode, web UI for non-David audience). Establish explicit out-of-scope.
10. **Persistence + state** — where do user decisions live? Browser LocalStorage, on-disk JSON in the repo, a SQLite file? What's the simplest thing that survives a restart?
11. **POEM integration depth** — workshop calls Penny as specialist (PO lean) vs absorb POEM concepts into workshop vs leave POEM external and link to it. Confirm.
12. **Refresh-as-event** — when refresh detects a new/changed/deprecated skill, should it be a passive list David visits, an active notification, a separate workspace? *Hint*: the metaphor "Refresh Inbox" suggests an inbox-shaped UX with a counter.

## Deliverables

By end of the elicitation session, three files exist in the apps repo:

### `docs/spec/skill-workshop/spec.md`

Per Osmani's spec-driven Phase 2 template:
- Frontmatter with `name`, `status: draft`, `created`, `phase: 2`
- One-paragraph problem statement (in David's words where possible)
- Primary use case (Topic 1 result)
- Capability list (Topics 4-8) — what the app does
- Architecture sketch (Topic 2-3, 10, 12)
- Out of scope (Topic 9)
- Open questions for ratification

### `docs/spec/skill-workshop/assumptions.md`

Every assumption the interviewer surfaced + how it was either (a) verified with David, or (b) flagged as unresolved. Per Osmani's pattern: assumptions get surfaced BEFORE they become hidden defects in the spec.

### `docs/spec/skill-workshop/clarifications.md`

The clarification log — every "wait, let me ask again" moment from the interview. What was originally said, what the rephrase revealed, what the final captured intent is. This is the trail that lets a future reviewer audit the spec's derivation.

## Acceptance criteria

- [ ] `docs/spec/skill-workshop/` folder exists with the three files
- [ ] All 12 topics covered with hypothesis + confidence ≥95% (or explicitly flagged as "PO postponed, see clarifications.md")
- [ ] `spec.md` has a complete capability list — every item David named in the brain session 2026-05-18 is reflected
- [ ] `assumptions.md` has at least one entry per topic (zero hidden assumptions)
- [ ] `clarifications.md` records every want-vs-should-want rephrase moment
- [ ] PO (David) explicitly ratifies the spec by responding "/approve spec" or naming what to change
- [ ] Spec status moves from `draft` to `ratified` only after PO approval

## Out of scope for this backlog item

- Writing any HTML / CSS / JS
- Building the triage console (its existing backlog item is deferred, not deleted)
- Implementing refresh detection logic
- Calling Penny / POEM integration (that's an implementation task — the spec just records the decision)
- Producing Phase 3 (clarify) or Phase 4 (tasks) artifacts — those are follow-on backlog items after spec ratification

## Open questions for PO before interview starts

If David hasn't answered these in the brain session, the interviewer should ask them as a 0th round before Topic 1:

1. **Session length** — David willing to do 60-90 min interview now, or break into multiple shorter sessions?
2. **Decision proxy** — if David doesn't have a strong opinion on a topic, what's the default? Lean fast-and-iterative (Osmani-style minimal viable), or lean rigorous (heavier spec, fewer rewrites)?

If David doesn't answer either, default: 60 min target session, lean fast-and-iterative.

## Voice anchor

Before opening the interview, read 2-3 of David's existing review skills to get his terse + operator tone:
- `~/dev/ad/appydave-plugins/appydave/skills/delivery-review/SKILL.md`
- `~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md`
- `~/dev/ad/appydave-plugins/appydave/skills/ralphy/SKILL.md` (especially the post-2026-05-17 hard-gate upgrade — shows his Mode-table format)

When drafting the spec, mimic that voice. Imperatives, terse, no marketing. No "this skill will..." constructions.
