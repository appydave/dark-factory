---
topic: "Stale memory name AppyCtrl vs AppyRadar"
issue: "Durable memory retains an entity's old name after a real-world rename"
created: "2026-06-09"
story_reference: "a69afeb2, c89d3d81"
category: "documentation"
severity: "low"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["memory/MEMORY.md", "memory/project_fleet_machine_identities.md"]
commits: []
---

# Stale memory name AppyCtrl vs AppyRadar — Durable memory retains an entity's old name after a real-world rename

## Problem Signature

**Symptoms**: A background agent's capture-service brief referred to the app as 'AppyRadar', while the assistant's own durable memory (dark-factory-is-a-constellation-of-apps.md) and the session-loaded MEMORY.md index still said 'AppyCtrl' — a name the primary constellation doc had already flagged as wrong in a dated correction.

**Environment**: Project memory files under ~/.claude/projects/<project>/memory/, checked against docs/dark-factory-constellation.md in the dark-factory repo

**Triggering Conditions**: An independent background agent's summary used a different name for the same app than the assistant's own loaded memory, prompting a verification check instead of trusting either source blindly.

## Root Cause
The memory file was a point-in-time snapshot (flagged by the harness as several days old) that had not been refreshed after the primary constellation doc recorded a dated correction: the app previously called 'AppyCtrl' (and wrongly believed to kill dead processes) is actually 'AppyRadar', a read-only fleet sensor that never kills.

## Solution
Read the primary constellation doc to confirm the correction was real, then edited memory/dark-factory-is-a-constellation-of-apps.md and memory/MEMORY.md to replace every 'AppyCtrl' occurrence with 'AppyRadar', adding a note that the old name was wrong.

```diff-before
- AppyCtrl — system/resource health: understand memory + resources on this machine AND across the
  whole Tailscale network. David already built it months ago (a couple hours, proof-of-concept) and
  we just aren't using it. ⚠️ a quick peek at ~/dev/ad/apps/appyctrl/README.md says "T3 Code — minimal
  web GUI for coding agents (Codex/Claude)" — POSSIBLE repurpose/mismatch; needs proper investigation
  in its own fresh window. Don't assume what it is.
```
```diff-after
- AppyRadar (⚠️ was mis-named "AppyCtrl" in older docs — corrected 2026-06-10 in the authoritative
  map docs/dark-factory-constellation.md) — read-only machine + fleet intelligence: memory/resource/
  process/AI-activity/maintenance-debt on this machine AND across the 5-Mac Tailscale network, exposed
  via Sentinel + MCP. It NEVER kills (reaping is Marshall's job alone — there is no killer-sentinel).
  PoC-validated 2026-04-27, on the AppySentinel substrate (appyradar-sentinal), live SSH collector
  scripts/audit.ts on the M4 Mini. NOT a Baku app. The old "AppyCtrl kills dead processes" role was
  wrong on both the name and the killing.
```

## Prevention
When a memory file's system-reminder flags it as several days old, or an independent agent's output disagrees with what memory says, verify the disputed fact against the primary/authoritative doc before asserting or continuing to propagate it — treat memory as a point-in-time observation, not live state.

## Related
- Sessions: a69afeb2, c89d3d81
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): a69afeb2, c89d3d81 · 2026-06-09 → 2026-07-03
- **Files** (candidate-level): memory/MEMORY.md, memory/project_fleet_machine_identities.md
- **Commits** (candidate-level): —
