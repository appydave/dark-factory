---
topic: "KBDE extension channel handlers can't be wired additively"
issue: "KBDE extension channel handlers can't be wired additively"
created: "2026-06-23"
story_reference: "2fdc2412"
category: "architecture"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["apps/omi-fetch/extension/FRICTION.md", "apps/omi-fetch/extension/kbde.extension.ts"]
commits: ["89084aa"]
---

# KBDE extension channel handlers can't be wired additively — KBDE extension channel handlers can't be wired additively

## Problem Signature

**Symptoms**: The extension passed `validateExtensionDefinition` with zero errors and was discoverable via the host's directory-scan manifest discovery, but could not be rendered by the real host — manifest announcement did not translate into a mounted, working extension.

**Environment**: First real KyberAgent (KBDE) extension build, `apps/omi-fetch/extension/`, built against the live `@kyberagent/extension-sdk` source in the `KBDE-KyberAgent-Enterprise` repo, under placement rules that forbade modifying anything in that host repo.

**Triggering Conditions**: Wiring the ③ Data (`data.omi-fetch.captures`) and ④ Events channels for an extension that must be staged entirely outside the KBDE host repo ('build outside, promote later').

## Root Cause
Channel handler registration in KBDE lives in one hardcoded function in an existing file (`seam/handlers.ts`) rather than through a pluggable/additive registration mechanism; separately, the ④ Events channel has no SDK builder or type at all — it exists only via hand-wiring and prose convention, invisible to `validateExtensionDefinition`, the capabilities generator, and the id-convention checker.

## Solution
Did not work around the gap (placement rules forbade editing the host's `seam/handlers.ts`) — shipped the extension in a validated-but-unmounted state, with a ranked `FRICTION.md` documenting this as the precise wall between 'staged' and 'mounted', for the SDK's author to close in the host itself.

## Prevention
Before promising an extension 'will mount', verify the host actually has an additive registration path for every channel kind used — schema validation (`validateExtensionDefinition` passing) and runtime mountability are two separate claims; don't conflate them.

## Related
- Sessions: 2fdc2412
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 2fdc2412 · 2026-06-23
- **Files** (candidate-level): apps/omi-fetch/extension/FRICTION.md, apps/omi-fetch/extension/kbde.extension.ts
- **Commits** (candidate-level): 89084aa
