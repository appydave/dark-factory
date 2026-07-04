> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0002: Archive superseded repos with a tested git-bundle backup, and gate deletion on the replacement being proven in deployment

**Status:** Proposed (reconstructed)


## Context
After re-scaffolding appyradar-sentinel and renaming the framework to appysentinel, two repos (`appyradar-sentinal`, and the old bespoke `appyradar`) became superseded. The question was whether they could be removed cleanly from GitHub and local disk while still keeping a backup, or whether removal should wait.

## Decision
Archive both repos on GitHub (reversible `isArchived` flag) and rename their local folders with an `_archived--` prefix rather than delete them. Take a `git bundle --all` backup of each repo (with the backup verified by test-restoring via clone) as insurance, and gate actual deletion on `appyradar-sentinel` being deployed as the always-on daemon and running clean for a period, plus the outbound-transport-to-Switchboard build being complete.

## Alternatives Considered
Immediate delete from GitHub and local disk — rejected because the new `appyradar-sentinel` repo was only hours old, unproven in real deployment, and the outbound-transport step wasn't built yet; deleting immediately would remove both the only reference implementation and the old repos' full commit history (independent value for build-documentary/Chronicle purposes) before the replacement was proven.

## Consequences
The old repos remain reachable (read-only) at effectively zero ongoing cost. Deletion becomes a deferred, low-risk follow-up once the replacement is proven in production, and will require a one-time `gh auth refresh -s delete_repo` scope grant when that time comes since the current token can't delete repos.

## Related
- Sessions: 1b7b1ab9

## Provenance
- **Sessions** (1): 1b7b1ab9 · 2026-06-10
- **Files** (session-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/appyradar-identity-resolved.md, dev/ad/apps/angeleye/.claude/skills/angeleye-retrieve/SKILL.md, dev/ad/apps/appyradar-sentinal/sentinel.config.example.json, dev/ad/apps/appyradar-sentinal/sentinel.config.json, dev/ad/apps/appyradar-sentinal/src/collect.ts, dev/ad/apps/appyradar-sentinal/src/collectors/bash-scripts.ts, dev/ad/apps/appyradar-sentinal/src/collectors/disk-usage/collector.ts, dev/ad/apps/appyradar-sentinal/src/collectors/orchestrator.ts, dev/ad/apps/appyradar-sentinal/src/collectors/parsers.ts, dev/ad/apps/appyradar-sentinal/src/expose/mcp.ts, dev/ad/apps/appyradar-sentinal/src/main.ts, dev/ad/apps/appyradar-sentinal/src/ssh/client.ts, dev/ad/apps/appyradar-sentinal/src/types.ts, dev/ad/apps/appyradar-sentinel/README.md
- **Commits** (session-level): —
