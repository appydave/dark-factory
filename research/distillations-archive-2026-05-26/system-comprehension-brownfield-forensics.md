---
distillation_id: system-comprehension-brownfield-forensics
stage: system-comprehension
intent: "Investigate an unknown or broken codebase — trace root causes, reconstruct decision history, and produce evidence-graded findings"
created: 2026-05-17
status: draft
source_artifacts:
  - bmad-method:skill:bmad-investigate
  - gstack:skill:investigate
  - gsd:command:gsd:forensics
  - compound-engineering:agent:ce-git-history-analyzer
winner_mechanism: bmad-method:skill:bmad-investigate
---

# Unified Skill: Brownfield Forensics (investigate + archaeology)

**Purpose**: Systematic investigation of an unknown, broken, or historically complex codebase. Combines root-cause tracing for bugs with archaeological git history analysis to understand why the code is the way it is. Produces evidence-graded findings, not guesses.

## Intent

Given a bug, incident, unfamiliar codebase, or "why does this code look this way?" question — systematically gather evidence, form calibrated hypotheses, trace root causes, and produce findings with confidence levels. The Iron Law: no fixes without root cause.

## Winner's Mechanism

`bmad-method:skill:bmad-investigate` is the winner. It is:

- **Evidence-graded**: findings include calibrated confidence scores, not just "here's what I found"
- **Calibrated to input**: scales from bug report → incident trace → unfamiliar code walkthrough → full archaeological dig. Not one-size-fits-all.
- **Zero infrastructure dependency**: no external tools beyond standard file access and git
- **Rare uniqueness signal**: unlike the commodity-scored CE and GSD members, BMAD investigate is scored `rare` — fewer than 5% of the corpus offers the same evidence-grading + input-calibration combination

`gstack:skill:investigate` contributes the **Iron Law** phrasings and the 4-phase structure (investigate → analyze → hypothesize → implement). It is scored `rare` on uniqueness and its Iron Law formulation ("no fixes without root cause") is verbatim worth preserving.

## Existing-skill nesting

No direct equivalent exists in David's stack. This is a from-scratch addition. The closest is `delivery-review` (reviews finished work) — but forensics covers in-progress bugs and historical archaeology, not post-implementation review.

Skip this section — from-scratch build.

## Non-overlapping ideas folded in

- From `gstack:skill:investigate`: **Iron Law + four-phase structure** — `complexity: low | optional: false | prerequisite: none`. The four phases (investigate / analyze / hypothesize / implement) map cleanly onto BMAD's evidence-graded approach. Iron Law phrase is verbatim-worthy: "no fixes without root cause." This is the canonical anti-rationalization formulation for debugging — equivalent to Superpowers' "Iron Law" for TDD.

- From `compound-engineering:agent:ce-git-history-analyzer`: **archaeological git history analysis** — `complexity: medium | optional: true | prerequisite: non-trivial git history exists`. CE's analyzer traces file evolution via `git log --follow`, code origins via `git blame`, and recurring commit patterns to surface why code exists. This is the "understanding the past" leg of forensics — BMAD investigate covers "understanding the present"; CE covers "understanding the history." They compose.

- From `gsd:command:gsd:forensics`: **post-mortem artifact writing** — `complexity: low | optional: true | prerequisite: a GSD workflow failed or a structured incident needs documentation`. GSD writes findings to `.planning/forensics/` as a structured forensic report. The artifact-writing convention (structured output to a known location) is worth adopting for David's version — findings should land in a predictable place for future sessions to find.

- From `bmad-method:skill:bmad-advanced-elicitation` (adjacent signal): **adversarial self-review of findings** — `complexity: medium | optional: true | prerequisite: initial investigation is complete`. After forming a root-cause hypothesis, apply socratic/pre-mortem/red-team elicitation to stress-test it. Prevents the most common forensics failure mode: confirmation bias in hypothesis selection.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `bmad-method:skill:bmad-investigate` | Evidence grading, calibrated-to-input scaling, confidence levels | BMAD persona framing (neutral investigation, not role-play) |
| `gstack:skill:investigate` | Iron Law phrase, 4-phase structure (investigate/analyze/hypothesize/implement) | gstack compile pipeline (needs-compile) |
| `gsd:command:gsd:forensics` | Post-mortem artifact writing convention (.planning/forensics/ or equivalent) | GSD workflow dependency (forensics triggers on GSD workflow failure — make it standalone) |
| `compound-engineering:agent:ce-git-history-analyzer` | Archaeological git analysis (blame, log --follow, commit pattern mining) | Agent-dispatch model (stand-alone tool calls sufficient) |

## Draft SKILL.md frontmatter

```yaml
name: investigate
description: >
  Systematic investigation of bugs, incidents, and unfamiliar code — evidence-graded findings,
  root-cause traced, confidence-scored. Iron Law: no fixes without root cause.
  Use when the user says "investigate this bug", "trace this error", "why does this code do X",
  "what caused this incident", "walk me through this code", "archaeological dig on this file",
  "git history for X", "what broke this", "root cause analysis", "forensics on this failure",
  "understand why this was built this way", "help me understand this codebase section".
  Distinct from system-context (full-repo comprehension) and delivery-review (finished work review).
argument-hint: "[--depth=quick|standard|deep] [--output=findings|report]"
allowed-tools: "Bash(git:*), Bash(grep:*), Bash(find:*), Read, Write"
```

## Open questions for David

1. **Naming conflict**: `gstack:skill:investigate` already uses the name `investigate`. If David adopts this, should it be `/investigate` (replacing nothing, since no David skill currently owns that name) or `/forensics` (to match GSD's naming)?

2. **Artifact output convention**: GSD writes to `.planning/forensics/`. Should David's version write findings to a predictable location (e.g., `.claude/investigations/<date>-<slug>.md`) or stay ephemeral (output in the conversation)? AngELEye session archive makes ephemeral findings persistent anyway.

3. **Git archaeology as separate sub-skill**: CE's `ce-git-history-analyzer` is rich enough to be standalone. Should "git archaeology" be a separate `/git-archaeology` skill that `investigate` calls as a sub-step, or should it be embedded inline?
