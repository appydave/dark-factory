> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0003: Add a rename-migration note instead of blind find/replace for historical name references in AngelEye's retrieval skill

**Status:** Proposed (reconstructed)


## Context
After renaming the `appysentinal` repo to `appysentinel`, AngelEye's `angeleye-retrieve/SKILL.md` contained several `appysentinal` references. Some looked like a stale path reference, but a real Claude Code session (`8f2325dd`, dated 2026-04-28) was genuinely tagged `appysentinal` in the AngelEye telemetry registry, and another line quoted a verbatim excerpt of a past handover prompt.

## Decision
Instead of a blanket find/replace of `appysentinal` → `appysentinel` in the skill doc, added an explicit note documenting the rename date and instructing future retrieval to search both the old and new project names, while leaving the historical example text (the genuinely-tagged session data and quoted prompt excerpt) unchanged.

## Alternatives Considered
Blind find/replace of every `appysentinal` occurrence in the skill doc — rejected because it would silently corrupt genuine historical telemetry data and quoted examples, breaking future retrieval searches for sessions legitimately tagged with the pre-rename project name.

## Consequences
Retrieval workflows against AngelEye must now search both `appysentinal` and `appysentinel` to get a project's full history across the rename boundary; the skill doc explicitly teaches this instead of silently losing the distinction between pre- and post-rename sessions.

## Related
- Sessions: 1b7b1ab9

## Provenance
- **Sessions** (1): 1b7b1ab9 · 2026-06-10
- **Files** (candidate-level): apps/angeleye/.claude/skills/angeleye-retrieve/SKILL.md
- **Commits** (candidate-level): cca1fc6
