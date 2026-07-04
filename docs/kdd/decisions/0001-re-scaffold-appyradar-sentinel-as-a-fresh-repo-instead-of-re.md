> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0001: Re-scaffold appyradar-sentinel as a fresh repo instead of rewriting git history to purge committed node_modules

**Status:** Proposed (reconstructed)


## Context
appyradar-sentinal's git history had `node_modules/` committed wholesale in its initial scaffold commit and later untracked, leaving ~19MB of dead TypeScript/esbuild/vite/rollup blobs permanently baked into `.git` history even though the working tree was clean. The repo also carried a misspelled identity (`sentinal`) in its folder name, GitHub URL, and published package name from commit 1.

## Decision
Instead of running history-rewriting surgery (e.g. `git filter-repo`) on the existing repo, make a clean working-tree copy excluding `.git` and `node_modules`, fix the misspelled name references in place, `git init` a brand-new single-commit history, verify the 214-test suite still passes identically, then push as a new GitHub repo (`appyradar-sentinel`, correct spelling) and archive the old one.

## Alternatives Considered
History rewrite (`git filter-repo` or similar) on the existing repo — rejected because there was nothing in the polluted 5-commit history worth preserving via surgery (the misspelling was baked in from the very first commit), and because the repo was still at the skeleton/PoC stage with zero external consumers, so a fresh start had zero migration cost.

## Consequences
The old commit-by-commit history (initial scaffold → untrack node_modules → merge PoC domain logic → tiered pulses) is not carried into the new repo, only the final working-tree state is — which was flagged as losing independent build-documentary/Chronicle value, leading to a follow-up decision to archive (not delete) the old repo and take a `git bundle` backup before any future deletion.

## Related
- Sessions: 1b7b1ab9

## Provenance
- **Sessions** (1): 1b7b1ab9 · 2026-06-10
- **Files** (candidate-level): apps/appyradar-sentinel/README.md, apps/appyradar-sentinel/package.json, apps/appyradar-sentinel/src/
- **Commits** (candidate-level): 104c191
