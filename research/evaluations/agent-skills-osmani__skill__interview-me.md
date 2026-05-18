---
artifact_id: agent-skills-osmani:skill:interview-me
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [requirements-discovery, intent-extraction, spec-requirements]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: interview-me

**Intent**: Closes the gap between what users ask for and what they actually want through one-question-at-a-time interviewing, each question paired with an explicit hypothesis, until 95% confidence is reached and a structured intent restate is confirmed.

## Scores

- **quality_score**: 5. Exceptional. Hypothesis + confidence number mechanism, single-question discipline with reasoning, "want vs. should want" detection, concrete restate format, explicit non-yes enumeration. Everything is structural, not advisory.
- **adoption_fit_final**: `strong`. Process-only, fully stack-agnostic, applicable to any underspecified requirement regardless of domain.
- **inspiration_value**: `high`. The "can I predict the user's reaction to the next three questions?" stop condition is checkable and honest — a genuinely better gate than "I feel confident."
- **uniqueness_refined**: `rare`. The hypothesis-attached-to-every-question discipline and the "want vs. should want" detection (sophistication-signaling answers) are not found in this form elsewhere in the corpus.
- **composability**: `calls-others`. Explicitly positions itself before idea-refine and spec-driven-development in a defined handoff chain.
- **description_craft_refined**: `trigger`. Description enumerates four distinct trigger scenarios including one meta-trigger ("you catch yourself silently filling in ambiguous requirements").

## Mineable phrasing

> "If you didn't have to justify this to anyone, what would you actually want?"

## Notes

The non-yes enumeration ("Whatever you think is best" / "Sounds good" / "Sure, let's go" are NOT confirmations) is one of the most practically useful anti-patterns in the entire batch. The before/after example showing how two questions revealed the actual ask was "a list" not "a dashboard" is a model for how to write a concrete example in any skill. The "Out of scope" line in the restate as non-negotiable is a strong design principle.
