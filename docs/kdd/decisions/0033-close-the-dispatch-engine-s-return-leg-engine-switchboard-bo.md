> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0033: Close the dispatch engine's return leg (engine→Switchboard→board) before adding the talk-to-it trigger

**Status:** Proposed (reconstructed)


## Context
The audit found the factory's work is really two loop families: the 'doing' loop (talk→ticket→dispatch→run→result) is already ~80% closed — claim→run→done→reaper ran 35 jobs unattended — while the 'watching' loop (sensors→bus→glass wall) is 0% closed; every sentinel collects telemetry but nothing delivers or renders it. The initial instinct was to finish the doing loop next (the talk-and-it-runs trigger), which is the North Star and nearly done.

## Decision
Close the doing loop's return leg first: have the dispatch engine emit lifecycle events (claimed/running/done/failed) to Switchboard's existing SSE transport, and render them on a live board. Defer the auto-wake trigger to second, and appyradar-sentinel (the fleet telemetry daemon, not the archived visual appyradar) to Switchboard telemetry as the third step, reusing the same rail.

## Alternatives Considered
Close the trigger first ('talk and it runs') — rejected because it adds more autonomous action to a system that still can't be observed, which was named as the actual underlying complaint ('I don't get the visibility I need... I don't trust it'); the philosophy brain states observability is a prerequisite for autonomy, not a nice-to-have.

## Consequences
Reuses existing infrastructure (Switchboard's 399-line SSE transport with replay, an existing :7430 board) so new code is small. Forces and proves the identity work from the parallelism decision, since lifecycle events must be stamped with which Marshall/Swagger/job. Corrects an earlier looser plan of 'appyradar → Switchboard' to specifically 'appyradar-sentinel (the daemon) → Switchboard', since the visual appyradar rewrite is a separate later consumer of Switchboard alongside Watchtower.

## Related
- Sessions: ef961b51

## Provenance
- **Sessions** (1): ef961b51 · 2026-06-12
- **Files** (session-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/constellation-first-placement.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/parallelism-via-identity.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/watchtower-app-vs-engine.md, dev/ad/apps/dark-factory/AUDIT-2026-06-12.md, dev/ad/apps/dark-factory/docs/north-star.md, dev/ad/apps/dark-factory/experiments/watchtower-engine/bin/claim-next.sh, dev/ad/brains/dark-factory/INDEX.md, dev/ad/brains/dark-factory/dark-factory-model.md, dev/raw-intake/omi/2026-06-12-1500-dart-factory-strategy-breakdown.md
- **Commits** (session-level): —
