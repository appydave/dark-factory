> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0005: Handover documents are written to backlog/ in the repo, not to ~/.claude/sessions/, despite the capture-context skill's own staleness warning

**Status:** Proposed (reconstructed)


## Context
The `capture-context` skill's own output rules explicitly state: 'Never write into the project directory. Handover documents in repos go stale and poison future sessions... suggest `~/.claude/sessions/` instead.' But Marshall's cold-start protocol in this repo reads its 'what's available' state from `backlog/*.md` files inside the repo, not from `~/.claude/sessions/`.

## Decision
Write the session-correction handover to `backlog/2026-06-08-session2-correction-handover.md` (a repo path), following the existing convention Marshall already reads from, rather than the skill's default recommendation.

## Alternatives Considered
Follow the skill's built-in default and write to `~/.claude/sessions/[topic]-[date].md` instead — rejected for this session because Marshall's cold-start read path does not look there, and doing so would silently break the existing handover-pickup mechanism without a separate migration.

## Consequences
The repo now carries a second handover-shaped file (alongside the main work-state handover) that is exactly the kind of artifact the skill warns can 'go stale and poison future sessions.' The tension between 'keep it where Marshall already reads it' and 'don't let repo-committed handovers rot' was explicitly flagged as an open input for the future DF-6 handover-mechanism spec, rather than resolved here.

## Related
- Sessions: 215b9cee

## Provenance
- **Sessions** (1): 215b9cee · 2026-06-08
- **Files** (candidate-level): backlog/2026-06-08-session-handover.md, backlog/2026-06-08-session2-correction-handover.md
- **Commits** (candidate-level): —
