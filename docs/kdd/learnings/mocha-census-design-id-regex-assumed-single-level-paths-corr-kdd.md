---
topic: "Mocha Census nested design-id parsing"
issue: "Mocha Census design-id regex assumed single-level paths, corrupting nested design ids"
created: "2026-06-08"
story_reference: "f2df9480"
category: "debugging"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["tools/mocha-census/scan.sh", "tools/mocha-census/shoot.py"]
commits: []
---

# Mocha Census nested design-id parsing — Mocha Census design-id regex assumed single-level paths, corrupting nested design ids

## Problem Signature

**Symptoms**: shots.json logged 203 entries but only 183 PNG files existed on disk; `os.path.exists()` returned True for all 203 yet `ls` only found 183. Investigation initially chased a red herring (APFS case-insensitive filename collision, ruled out by direct check) before finding the real cause.

**Environment**: tools/mocha-census (Dark Factory) scanning SupportSignal's `.mochaccino/designs/components/<name>/index.html` nested design tree, plus a duplicated `designs/designs/` artifact present on the Mini machine.

**Triggering Conditions**: Running scan.sh + shoot.py against a repo (SupportSignal) whose Mochaccino designs are nested one level deeper than the flat `designs/<id>/index.html` convention every other scanned repo used.

## Root Cause
scan.sh derived `design_id` with a single-segment regex capture (`s#.*/designs/([^/]+)/index\.html#\1#`). For nested paths this failed to match cleanly, so `design_id` became the entire absolute path; shoot.py then wrote screenshots into malformed nested directories and hit broken URLs.

## Solution
Fixed the regex in scan.sh to capture the full sub-path after `designs/` (handles nesting) and excluded the doubled `designs/designs/` artifact. Updated shoot.py to replace `/` with `--` when building the PNG filename so a nested id can't create a subdirectory. Purged the 20 junk shots.json entries, re-scanned, reshot — result verified as 193 unique designs = 193 shot, 0 missing, 0 extra.

```diff-before
    \( -path '*/.mochaccino/designs/*/index.html' -o -path '*/mochaccino/designs/*/index.html' \) \
    -not -path '*/node_modules/*' -not -path '*/.claude/skills/*' -not -path '*/worktrees/*' 2>/dev/null |
while IFS= read -r f; do
  root="$(printf '%s' "$f" | sed -E 's#/(\.?mochaccino)/designs/.*#/\1#')"
  did="$(printf '%s' "$f" | sed -E 's#.*/designs/([^/]+)/index\.html#\1#')"
```
```diff-after
    \( -path '*/.mochaccino/designs/*/index.html' -o -path '*/mochaccino/designs/*/index.html' \) \
    -not -path '*/node_modules/*' -not -path '*/.claude/skills/*' -not -path '*/worktrees/*' \
    -not -path '*/designs/designs/*' 2>/dev/null |
while IFS= read -r f; do
  root="$(printf '%s' "$f" | sed -E 's#/(\.?mochaccino)/designs/.*#/\1#')"
  # design_id = full sub-path between designs/ and /index.html (handles nested e.g. components/foo)
  did="$(printf '%s' "$f" | sed -E 's#.*/designs/(.+)/index\.html#\1#')"
```

```diff-before
                url = f"http://127.0.0.1:{port}/designs/{r['design_id']}/index.html"
                img = f"{r['repo']}__{r['design_id']}.png"
```
```diff-after
                url = f"http://127.0.0.1:{port}/designs/{r['design_id']}/index.html"
                img = f"{r['repo']}__{r['design_id'].replace('/', '--')}.png"
```

## Prevention
When a scanner/parser assumes a fixed path depth, verify against every real source tree before trusting counts — assert `manifest count == files actually on disk` explicitly rather than eyeballing a total.

## Related
- Sessions: f2df9480
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f2df9480 · 2026-06-08
- **Files** (candidate-level): tools/mocha-census/scan.sh, tools/mocha-census/shoot.py
- **Commits** (candidate-level): —
