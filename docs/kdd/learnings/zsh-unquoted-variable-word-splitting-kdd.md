---
topic: "zsh unquoted variable word-splitting"
issue: "zsh unquoted variable word-splitting"
created: "2026-06-10"
story_reference: "1b7b1ab9"
category: "tooling"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["apps/appysentinel/DEVELOPMENT.md", "apps/appysentinel/docs/architecture-refactor-v2.md", "apps/appysentinel/docs/design-synthesis.md", "apps/appysentinel/docs/mochaccino-forensic.md", "apps/appysentinel/package.json", "apps/appysentinel/packages/cli/README.md", "apps/appysentinel/packages/cli/package.json", "apps/appysentinel/packages/config/package.json", "apps/appysentinel/packages/core/package.json", "apps/appysentinel/packages/template/README.md"]
commits: ["b54bc30"]
---

# zsh unquoted variable word-splitting — zsh unquoted variable word-splitting

## Problem Signature

**Symptoms**: A multi-file find/replace sweep (renaming `appysentinal` to `appysentinel` across package.json/README/docs files) produced no `fixed:` output at all — the loop ran once against a single bogus combined filename instead of iterating the intended file list.

**Environment**: zsh shell on macOS, shell commands issued through the Bash tool against the appysentinel repo (`~/dev/ad/apps/appysentinel`)

**Triggering Conditions**: Assigning a list of file paths to a shell variable (e.g. `$FILES`) and then looping over it with `for f in $FILES` without quoting or using a true array — works in bash's default word-splitting behavior but not in zsh.

## Root Cause
zsh does not word-split unquoted variable expansions by default (unlike bash), so `$FILES` was treated as one literal token rather than a list of filenames.

## Solution
Re-ran the sweep using an explicit, literal space-separated file list in the `for` loop instead of expanding a variable, which sidesteps zsh's word-splitting difference entirely.

```bash
# before — silently does nothing on zsh (FILES never gets split into words)
for f in $FILES; do ...; done

# after — zsh-safe: explicit literal list, no variable expansion to split
for f in package.json packages/core/package.json packages/config/package.json \
  packages/cli/package.json packages/template/README.md packages/cli/README.md \
  docs/design-synthesis.md DEVELOPMENT.md docs/architecture-refactor-v2.md \
  docs/mochaccino-forensic.md; do
  # sed/perl replace appysentinal -> appysentinel in $f
  echo "fixed: $f"
done
```

## Prevention
When looping over a dynamically-built file list in a script that may run under zsh, don't rely on bash's default unquoted word-splitting — use an explicit literal list, a real zsh/bash array (`"${FILES[@]}"`), or `xargs`/`while read` from a newline-delimited source instead.

## Related
- Sessions: 1b7b1ab9
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 1b7b1ab9 · 2026-06-10
- **Files** (candidate-level): apps/appysentinel/DEVELOPMENT.md, apps/appysentinel/docs/architecture-refactor-v2.md, apps/appysentinel/docs/design-synthesis.md, apps/appysentinel/docs/mochaccino-forensic.md, apps/appysentinel/package.json, apps/appysentinel/packages/cli/README.md, apps/appysentinel/packages/cli/package.json, apps/appysentinel/packages/config/package.json, apps/appysentinel/packages/core/package.json, apps/appysentinel/packages/template/README.md
- **Commits** (candidate-level): b54bc30
