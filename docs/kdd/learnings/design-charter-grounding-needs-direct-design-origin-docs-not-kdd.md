---
topic: "Design docs beat transcript-mining"
issue: "Design charter grounding needs direct design-origin docs, not just transcript-mining"
created: "2026-06-09"
story_reference: "fe4204be"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["backlog/2026-06-09-switchboard-charter-grounding.md"]
commits: []
---

# Design docs beat transcript-mining — Design charter grounding needs direct design-origin docs, not just transcript-mining

## Problem Signature

**Symptoms**: The seed document framed 7 of the charter's open questions as fully unresolved. Mining all 7 switchboard build-cluster session transcripts in parallel (via `abridge` agents) returned findings that were rich on architecture-decided-while-building but nearly silent on 'what Switchboard should BE'.

**Environment**: dark-factory backlog grounding task — Switchboard greenfield charter, phase 1 (grounding), writing backlog/2026-06-09-switchboard-charter-grounding.md

**Triggering Conditions**: Running the grounding phase using only the 7 switchboard build-cluster session transcripts (mined in parallel) before reading the design-origin docs (memories, the sentinel proposal doc) directly.

## Root Cause
Build-session transcripts capture architecture discovered incidentally while shipping code, not the deliberate identity/design conversation. The actual identity-defining discussion lived in separate memory files and a backlog proposal doc that were outside the transcript-mining scope.

## Solution
After the 7-transcript mine returned, read the design-origin sources directly — backlog/2026-06-06-dark-factory-sentinel.md and the memories watchtower-sentinel-bus-direction, dark-factory-is-a-constellation-of-apps, constellation-first-placement — which resolved most of the seed's 'open questions' as already-ruled, correcting the grounding doc from a blank-slate framing to a confirm/challenge framing.

## Prevention
When grounding a design/charter task, read canonical design-origin docs (memories, prior proposal docs) directly as a first-class source alongside transcript mining — don't rely on transcript-mining of build sessions alone to judge what's already decided vs genuinely open.

## Related
- Sessions: fe4204be
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): fe4204be · 2026-06-09
- **Files** (candidate-level): backlog/2026-06-09-switchboard-charter-grounding.md
- **Commits** (candidate-level): —
