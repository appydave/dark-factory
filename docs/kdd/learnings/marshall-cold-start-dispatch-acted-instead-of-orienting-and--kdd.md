---
topic: "Marshall cold-start dispatch"
issue: "Marshall cold-start dispatch: acted instead of orienting and asking"
created: "2026-06-08"
story_reference: "215b9cee"
category: "process"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".claude/skills/marshall/SKILL.md"]
commits: []
---

# Marshall cold-start dispatch — Marshall cold-start dispatch: acted instead of orienting and asking

## Problem Signature

**Symptoms**: On a bare `/marshall` with no task given, the assistant read the handover, immediately formed an opinionated recommendation, invoked millwright, and authored engine code (DF-3 telemetry) inline — without asking the user what to work on and without dispatching the work through a Swagger job-agent as the protocol requires.

**Environment**: Dark Factory repo, `.claude/skills/marshall/SKILL.md` (the Marshall Conductor skill), session start (cold open, no compaction).

**Triggering Conditions**: A fresh session opened with just `/marshall` and no specific instruction — which the skill's existing 'keep momentum, don't ask' and 'never hand back a bare menu, pick one and start' rules were misread as license to act, even though those rules are meant for mid-session use once a direction is already set.

## Root Cause
The skill had no explicit distinction between cold-start behavior (orient + surface + ask) and mid-session behavior (take + act). The 'don't ask, keep momentum' rules applied globally, so they overrode the intended orientation step at session start.

## Solution
Reverted the inline DF-3 build completely (engine scripts restored to HEAD, new files deleted, the overstated memory removed), then made three bounded edits to `.claude/skills/marshall/SKILL.md`: added a new 'Cold start — orient, surface, ASK (do NOT dispatch)' section right after Preflight, and scoped both the 'Take' loop step and the 'never hand back a bare menu' hard rule to explicitly say they are mid-session-only and do not license acting on a cold open.

```diff-before
It reports each Dark Factory app UP/DOWN. **Required: Switchboard (comms bus) + AngelEye (session telemetry — load-bearing for the reaper).** If a required app is DOWN (exit 1): **say so BOLDLY at the very top of your response** — never bury it — and start the missing app before dispatching. The apps are meant to be turned on; a down dependency silently loses data (we lost a whole session's AngelEye telemetry because nothing told us). Watchtower board + AppyCtrl are advisory, not blocking. See memory `constellation-preflight-marshall-not-blind`.

## The loop
```
```diff-after
It reports each Dark Factory app UP/DOWN. **Required: Switchboard (comms bus) + AngelEye (session telemetry — load-bearing for the reaper).** If a required app is DOWN (exit 1): **say so BOLDLY at the very top of your response** — never bury it — and start the missing app before dispatching. The apps are meant to be turned on; a down dependency silently loses data (we lost a whole session's AngelEye telemetry because nothing told us). Watchtower board + AppyCtrl are advisory, not blocking. See memory `constellation-preflight-marshall-not-blind`.

## Cold start — orient, surface, **ASK** (do NOT dispatch)

**When Marshall is activated with no specific instruction** — David opens a window and types `/marshall` / "be Marshall" / "evaluate the system" — the session is a **handover pickup, not a work order.** A handover doc (and `backlog/`) records **David's *parked* decisions**; it is NOT a mandate to execute them. **Stop at orientation and hand David the wheel.** (Session content truncated in digest beyond this point.)
```

```diff-before
2. **Take** — form an opinionated recommendation. Don't ask "what next?" — say what you'd do.
```
```diff-after
2. **Take** — form an opinionated recommendation. Don't ask "what next?" — say what you'd do. *(Mid-session only. At a cold open you DO ask — see **Cold start** above.)*
```

```diff-before
**Hard rule — never hand back a bare menu.** Options *with reasoning*, then **pick one and start.** **"go" = proceed** (David's default move-forward signal): on "go", execute the recommendation immediately, no re-confirmation.
```
```diff-after
**Hard rule — never hand back a bare menu.** Options *with reasoning*, then **pick one and start.** **"go" = proceed** (David's default move-forward signal): on "go", execute the recommendation immediately, no re-confirmation. *(This is the **mid-session** rule, once David has set a direction. It does **not** apply at a cold open — there, **Cold start** wins: surface threads and ask. "Don't hand back a bare menu" never means "so go act instead of asking" when David hasn't chosen a thread yet.)*
```

## Prevention
At session cold-start (no task given), the operator role must run preflight → load state → surface outstanding threads as a grouped board → ask what to do next, and STOP. 'Keep momentum / don't ask / pick one and start' rules apply only once a human has already set a direction mid-session; they must be explicitly scoped in the skill doc so they can't be misread as license to act unprompted.

## Related
- Sessions: 215b9cee
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 215b9cee · 2026-06-08
- **Files** (candidate-level): .claude/skills/marshall/SKILL.md
- **Commits** (candidate-level): —
