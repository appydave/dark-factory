---
topic: "Canonical inspection coverage"
issue: "style-check validates form, not whether a skill's description matches what its body does — an external skill-creator review caught a coherence defect ours cannot see"
created: "2026-07-11"
story_reference: "T3-02, review-dimensional"
category: "testing"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: live-capture
provenance_grain: candidate
files: ["tools/style-check.py", "canonical/skills/review-dimensional/SKILL.md", "docs/david-style-patterns.md"]
commits: ["153f42e"]
---

# Canonical inspection coverage — style-check checks form, not description↔body coherence

## Problem Signature

**Symptoms**: `verify-provenance` + `style-check` both passed `review-dimensional`, yet a background
review through the official **skill-creator** lens flagged a real defect: the description's triggers
(`'build a new review dimension'`, `'add a reviewer specialist'` — authoring) contradict the body
(`"Runs one review axis end-to-end"`, `argument-hint: [axis] [diff|pr-url]` — executing). An agent
can't tell whether to invoke it to *build* a reviewer or *run* one. This was also the exact reason
the operator couldn't tell what the skill was *for*.

**Environment**: dark-factory canonical inspection (verify-provenance + style-check) vs the generic
skill-creator methodology.

## Root Cause

Our inspectors check **form and provenance** — frontmatter shape, trigger-only description, body
length, stack-agnosticism, the source chain — but nothing checks **semantic coherence**: does the
description describe the same activity the body performs? A skill can be perfectly formed and
provenance-clean while being confused about its own identity.

## Solution

None applied to the tool yet (moratorium). Captured as a coverage gap. The two systems are
**complementary, not competing**: ours owns provenance + David's voice (skill-creator has zero
concept of provenance and *wrongly* flags legitimate Claude Code fields like `allowed-tools`/
`argument-hint`); skill-creator owns craft coherence + worked examples + token economy.

## Prevention

Add a **description↔body coherence check** to `style-check` (does the description's implied activity
— build vs run vs analyze — match the body's verbs and `argument-hint`?). More broadly: a form/
provenance validator is necessary but not sufficient; pair it with a coherence lens (or an external
skill-creator pass) before calling a canonical artifact exemplary. review-dimensional itself carries
the identity defect → a future *new version*, not an in-place edit (ratified). See [[ADR-0045]].
