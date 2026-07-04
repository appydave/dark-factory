> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0039: The untracked-rot sweep (DF-9) will detect and report git hygiene debt only — never auto-commit or auto-write .gitignore

**Status:** Proposed (reconstructed)


## Context
After manually cleaning the 72-file untracked pile, needed to decide the shape of a standing fix so the same rot doesn't silently recur. The spec had to choose between a sentinel that only surfaces the problem versus one that also resolves it automatically.

## Decision
Wrote DF-9 (backlog/specs/untracked-rot-sweep-spec.md, registered spec-written priority 3 in backlog/specs/tickets.json): a detect-and-tell sweep that scans configured repos for untracked/modified/deleted state, classifies untracked items as deliverable/ignorable/unknown, reports the oldest debt per repo, and only *suggests* .gitignore rules — it never commits or writes files itself. It's meant to surface boldly at Marshall's session-open preflight, the same posture as the existing reaper (window teardown) and design-lint (flag-only render check).

## Alternatives Considered
An auto-acting sweep that commits obviously-safe deliverables and writes .gitignore rules itself was considered implicitly (that's effectively what the manual cleanup this session did) but rejected as the standing design — keeping the human/Marshall in the loop for what gets committed was chosen to avoid the sentinel making a wrong commit/ignore call unsupervised.

## Consequences
Rot is not eliminated automatically — a human or Marshall still has to act on the report — but the risk of an automated tool misclassifying or wrongly committing/ignoring files is avoided. The home for the sweep (an AppyRadar in-app probe vs a standalone tools/ script promoted later) was left as an open decision in the spec, with the MVP able to start as a simple script.

## Related
- Sessions: f68c5f1c

## Provenance
- **Sessions** (1): f68c5f1c · 2026-06-10
- **Files** (candidate-level): backlog/specs/tickets.json, backlog/specs/untracked-rot-sweep-spec.md
- **Commits** (candidate-level): —
