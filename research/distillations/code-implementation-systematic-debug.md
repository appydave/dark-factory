---
distillation_id: code-implementation-systematic-debug
stage: code-implementation
intent: "Root-cause-first debugging with causal chain gate, anti-shotgun enforcement, and smart escalation when 3+ hypotheses fail"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:systematic-debugging
  - compound-engineering:skill:ce-debug
  - agent-skills-osmani:skill:debugging-and-error-recovery
  - gsd:agent:gsd-debugger
winner_mechanism: compound-engineering:skill:ce-debug
---

# Unified Skill: Systematic Debug

## Intent

Systematically trace bugs to root cause before touching code, using a causal-chain gate (no fix until the chain is complete with no gaps), smart escalation when hypotheses are exhausted, and a test-first fix that creates a regression guard.

## Winner's Mechanism

CE's `ce-debug` is the winner over Superpowers' `systematic-debugging` because:

1. **Issue tracker integration** — fetches GitHub/Linear/Jira issues before investigating. Superpowers doesn't have this. For SupportSignal work, where bugs often arrive as GitHub issues, this is immediately practical.

2. **Causal chain gate is crisper** — "Do not proceed to Phase 3 until you can explain the full causal chain from trigger to symptom with no gaps. 'Somehow X leads to Y' is a gap." This is more precise than Superpowers' Phase 1 prerequisite.

3. **Prediction mechanism for uncertain links** — when the chain has uncertain links, form a prediction (something in a different code path that must also be true). If the prediction is wrong but the fix "works," you found a symptom, not the cause. Superpowers lacks this.

4. **Trivial-bug fast-path** — for obvious one-line fixes (missing import, clear null deref), skip the ceremony and get to the fix gate immediately. Superpowers runs the full 4-phase process regardless of bug size.

5. **Assumption audit before hypothesis formation** — list the "must be true" beliefs, mark each verified or assumed. Most stuck debugging is a wrong assumption. Superpowers' Phase 1 covers this implicitly; CE makes it explicit.

6. **Parallel sub-agent investigation** — when hypotheses are evidence-bottlenecked across independent subsystems, dispatch read-only sub-agents in parallel. Superpowers doesn't support this.

Superpowers' `systematic-debugging` is an excellent complement for the "3+ fixes failed = question the architecture" escalation pattern (Phase 4.5) and its multi-component evidence-gathering recipe — both are folded in below.

## Existing-skill nesting

David has no existing debug skill in his stack. This is a gap-fill, not an upgrade. `ce-debug` becomes the primary debug invocation.

Skip this section — from-scratch build.

## Non-overlapping ideas folded in

- From `superpowers:systematic-debugging`: **Multi-component evidence-gathering recipe** — for systems with multiple components (CI → build → signing, API → service → database), add diagnostic instrumentation at each boundary *before* forming hypotheses. Log what enters and exits each layer, then run once to observe WHERE it breaks. — `complexity: low | optional: true | prerequisite: "bug is in a multi-layer pipeline system"`. Prevents the "guess which layer is broken" failure mode that generates shotgun fixes.

- From `superpowers:systematic-debugging`: **3+ fixes = question architecture** — if 3+ hypotheses have failed, diagnose the pattern: hypotheses pointing to different subsystems = architectural problem; each fix creates symptoms elsewhere = wrong design assumption. Stop and discuss with human before attempting Fix #4. — `complexity: low | optional: false | prerequisite: "2+ fix attempts have already failed"`. Prevents the rationalization spiral that burns hours on un-rootable symptoms.

- From `superpowers:systematic-debugging`: **Human-partner signal table** — specific phrases that mean "you're doing it wrong" ("Is that not happening?" = assumed without verifying; "Stop guessing" = proposing fixes without understanding). Training the agent to recognize correction signals early prevents compounding errors. — `complexity: low | optional: false | prerequisite: none`. Directly reduces the time spent in unproductive debugging loops.

- From `agent-skills-osmani:skill:debugging-and-error-recovery`: **Triage → Evidence → Hypothesis → Fix** named phases (vs. CE's numbered phases). The named-phase vocabulary is easier to reference mid-session ("we're in the Evidence phase, not yet at Hypothesis"). — `complexity: low | optional: true | prerequisite: none`. Ergonomic improvement, not a structural change.

- From `compound-engineering:skill:ce-debug`: **Defense-in-depth trigger** — after fixing: if the root-cause pattern was found in 3+ other files, OR the bug would have been catastrophic if it reached production, apply the four-layer defense model (entry validation, invariant check, environment guard, diagnostic breadcrumb). — `complexity: medium | optional: true | prerequisite: "root cause pattern found in multiple locations OR production-severity bug"`. Turns individual bug fixes into systemic hardening.

- From `compound-engineering:skill:ce-debug`: **Learning capture offer** — after PR is open, if the bug had a non-obvious diagnostic path or the root cause reveals a wrong assumption about a shared dependency, offer to run `/ce-compound` to capture a reusable solution doc. Skip silently for mechanical fixes. — `complexity: low | optional: true | prerequisite: "non-obvious diagnostic path OR pattern appears in 3+ locations"`. Converts one-off debugging into compound knowledge.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `compound-engineering:ce-debug` | Full 4-phase structure, causal chain gate, prediction mechanism, trivial-bug fast-path, assumption audit, issue tracker integration, parallel sub-agent investigation, learning capture | Codex/Pi/Gemini platform-specific tool names (Claude Code only) |
| `superpowers:systematic-debugging` | 3+ fixes = architecture question, multi-component evidence-gathering recipe, human-partner signal table | Iron Law framing (CE's causal chain gate is sharper), 4-phase exact numbering (replaced with CE's phase names) |
| `agent-skills-osmani:debugging-and-error-recovery` | Named-phase vocabulary (Triage/Evidence/Hypothesis/Fix) | The full skill structure (CE is the richer mechanism) |
| `gsd:agent:gsd-debugger` | Nothing — domain-specific to GSD pipeline internals | All (not portable) |

## Draft SKILL.md frontmatter

```yaml
name: systematic-debug
description: "Root-cause-first debugging that traces the full causal chain before proposing any fix. Use when tests fail, builds break, behavior is unexpected, or you're stuck after failed fix attempts. Triggers on: 'debug this', 'why is this failing', 'fix this bug', 'trace this error', '#123' (issue reference), or any pasted stack trace or error message."
argument-hint: "[issue reference (#123), error message, test path, or description of broken behavior]"
allowed-tools: "Bash(git log:*), Bash(git diff:*), Bash(git bisect:*), Bash(gh issue view:*), Read, Edit, Write"
```

## Open questions for David

1. **Naming**: `systematic-debug` vs `debug` — CE uses `ce-debug`, Superpowers uses `systematic-debugging`. For David's stack, the shortest unambiguous name is `debug`. Does the `systematic-` prefix add useful signal in the description/trigger, or does it create friction?

2. **Learning capture target**: CE's `ce-debug` offers to run `/ce-compound` to capture a solution doc. David's equivalent would be appending to `data/insights.md` in the catalog, or writing to a `solutions/` folder in the affected brain. Which location fits David's knowledge-capture pattern?

3. **SupportSignal context**: CE's `ce-debug` includes explicit observability checks (Sentry, AppSignal, Datadog). SupportSignal uses which error tracker? The skill should reference the project's actual observability stack in Phase 1.3.
