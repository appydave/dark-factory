---
name: review-dimensional
description: "Single-axis specialist review pattern — one concern, one finding format, depth-calibrated by diff size, composable into any fan-out orchestrator. Use when: 'build a new review dimension', 'add a reviewer specialist', 'dimensional review', 'single-axis review', 'depth-calibrated review'."
argument-hint: "[axis] [diff | pr-url | file-list]"
allowed-tools: Read, Grep, Glob, Bash
---

# Review Dimensional

Runs one review axis end-to-end — scope, hunt, validate, report — at a depth calibrated to how big and how risky the change is.

## Behavior

1. **Resolve scope.** Diff (staged + unstaged), a PR reference, or an explicit file list. HALT if empty or unreadable.
2. **Estimate size and risk.** Count changed lines (additions + deletions, excluding generated files, lockfiles, and test fixtures). Scan the change for domain risk signals — auth, payment, data mutation, external API, session handling, anything compliance-adjacent.
3. **Select depth** per the calibration table below, then run the axis-specific hunt at that depth.
4. **Validate completeness.** Revisit every hunt category once more. Add anything newly spotted; drop anything you now confirm is actually handled elsewhere.
5. **Report.** Emit normalized findings (see Output) and a verdict line. If a non-trivial diff yields fewer than 3 findings, re-examine before concluding — a clean small diff can legitimately still be a PASS, but don't let scope-blindness masquerade as cleanliness.

## Depth calibration

| Tier | Trigger | What runs |
|------|---------|-----------|
| Quick | Under 50 changed lines, no risk signals | The axis's core hunt only. Cap findings to what's clearly evidenced — don't manufacture volume. |
| Standard | 50–199 changed lines, or a minor risk signal | Core hunt plus cross-boundary checks (how this change interacts with what calls it or what it calls). |
| Deep | 200+ changed lines, or a strong risk signal | Full hunt, including multi-step failure chains where an early condition cascades into a later one. Worth a second pass over the highest-risk interaction points. |

## Axis territory

State the axis's precise boundary before hunting — what this run catches that no sibling reviewer does. Name the adjacent axes explicitly and what each of them owns instead, so findings don't drift into a sibling's lane. A specialist that can't state what it *won't* flag hasn't scoped itself yet.

## Confidence rubric

Anchor every finding before it ships:

| Confidence | When it holds | How to surface |
|------------|---------------|----------------|
| **100** | Mechanically verifiable from the diff and surrounding code alone; no assumed runtime condition. | Report normally. |
| **75** | A complete, concrete scenario: given this input or state, execution reaches this line and produces this specific wrong outcome. | Report normally. |
| **50** | The scenario holds but one step rests on a condition you can see but can't confirm (an external response shape, a timing window). | Soft/low-confidence bucket only — never the headline severity. |
| **≤25** | Pure speculation about runtime state, or a chain that needs several unlikely conditions at once. | Suppress — don't report. |

## Output

Normalized findings, one per issue, dimension-coded (`{AXIS}-NNN`, severity-sorted):

- **ID** — `{AXIS}-NNN`
- **Severity** — critical | high | medium | low
- **Location** — `file:line` (or a named scope boundary if the finding isn't line-scoped)
- **Summary** — one line, naming the concrete failure, not the pattern matched
- **Evidence** — the scenario or trace that makes the finding true, cited against real lines

Before the report ships, run the pre-report gate on every finding: does it cite a real line, name a concrete failure (not "consider..." or "might want to..."), show you read the surrounding context (not just the diff hunk in isolation), and does the severity survive being defended out loud? Drop or downgrade anything that doesn't clear all four.

Close with a verdict line: **FAIL** (any critical) · **CONDITIONAL** (any high, no critical) · **PASS** (otherwise — an empty findings list is a legitimate PASS on a genuinely clean change).

## Anti-patterns

- Flagging territory a sibling axis owns instead of naming it and moving on — lane drift defeats the whole point of splitting review into axes.
- Writing files or applying fixes. A reviewer reports; it never edits. Fixing is a separate step owned by whatever consumes the findings.
- Padding a report to look thorough — a suppressed (≤25 confidence) finding doesn't get a lower severity, it gets dropped entirely.
- Running Deep-tier techniques on a Quick-tier diff "just in case" — depth is calibrated for a reason; over-running it wastes the reason someone chose specialists over one giant reviewer.

## Halt conditions

- HALT if scope is empty or unreadable — don't guess at what changed.
