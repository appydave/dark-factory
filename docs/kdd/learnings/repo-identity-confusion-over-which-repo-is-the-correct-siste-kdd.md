---
topic: "Repo identity verification"
issue: "Repo identity confusion over which repo is the correct sister project"
created: "2026-06-10"
story_reference: "903d8c01, d9b55fdb"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/project_four_sister_projects.md", ".config/appydave/locations.json", "apps/appyradar-sentinel (new clone)", "apps/appysentinal (renamed to apps/appysentinel)"]
commits: []
---

# Repo identity verification — Repo identity confusion over which repo is the correct sister project

## Problem Signature

**Symptoms**: Repeatedly misidentified the correct repo to sync — first cloned `appydave/appyradar` (wrong), then treated `appysentinal`/`appysentinel` as the fourth project (wrong), before the user corrected it to `appyradar-sentinel`. Also believed the old `appysentinal` spelling was a separately archived repo when GitHub showed it was actually the same repo via rename/redirect.

**Environment**: Local git clones under ~/dev/ad/apps/ across five similarly-named candidate repos (appysentinal, appysentinel, appyradar, appyradar-sentinal, appyradar-sentinel).

**Triggering Conditions**: One repo had been renamed (misspelling fixed) at the same time a similarly-named sibling repo was freshly re-scaffolded under a new name, and the secondhand account of which repos were 'archived' didn't match GitHub's actual state.

## Root Cause
Treated repo-name similarity and secondhand descriptions ('the old one has been archived') as ground truth instead of querying GitHub directly for canonical identity (repo id, archived flag, last push) before cloning, renaming, or repointing remotes.

## Solution
Query GitHub for every candidate name up front and compare the returned repo id across name variants — an identical id across two names means rename/redirect (same repo, just `git remote set-url` + pull); different ids mean genuinely separate repos (clone fresh). Only decide sync strategy after that identity check.

```bash
# query canonical identity for every candidate spelling before acting
for r in appysentinel appysentinal appyradar-sentinel appyradar-sentinal appyradar; do
  printf "queried %-20s -> " "$r"
  # resolve name -> canonical owner/repo + id + archived flag (gh api / gh repo view)
done
```
Result (verbatim from session):
```
queried appysentinel         -> appydave/appysentinel   id=R_kgDOSL8Ycg
queried appysentinal         -> appydave/appysentinel   id=R_kgDOSL8Ycg
queried appyradar-sentinel   -> appydave/appyradar-sentinel   id=R_kgDOS28dxA
queried appyradar-sentinal   -> appydave/appyradar-sentinal   id=R_kgDOSNg7Nw   [ARCHIVED]
queried appyradar            -> appydave/appyradar   id=R_kgDOS2c4sg   [ARCHIVED]
```
The identical id (`R_kgDOSL8Ycg`) for `appysentinel`/`appysentinal` proved it was one renamed repo, not two separate ones; the different ids for the two `appyradar-sentinel`/`appyradar-sentinal` spellings proved those were genuinely separate repos (new re-scaffold vs. an archived original).

## Prevention
Before syncing/renaming/cloning any repo whose name might have changed, run the id-comparison check first — never rely on a name string or a verbal/doc description of archived-vs-renamed. After renaming a local clone folder to match a corrected repo name, grep dependent path registries (e.g. a project-locations config) for the old path and fix them in the same pass, since the rename will otherwise silently break them.

## Related
- Sessions: 903d8c01, d9b55fdb
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 903d8c01, d9b55fdb · 2026-06-10
- **Files** (candidate-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/project_four_sister_projects.md, .config/appydave/locations.json, apps/appyradar-sentinel (new clone), apps/appysentinal (renamed to apps/appysentinel)
- **Commits** (candidate-level): —
