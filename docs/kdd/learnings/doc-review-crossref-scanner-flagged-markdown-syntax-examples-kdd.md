---
topic: "doc-review crossref false positives"
issue: "Doc-review crossref scanner flagged markdown syntax examples in prose as broken links"
created: "2026-06-16"
story_reference: "7a973797"
category: "testing"
severity: "low"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["docs/doc-organiser-proposal.md"]
commits: []
---

# doc-review crossref false positives — Doc-review crossref scanner flagged markdown syntax examples in prose as broken links

## Problem Signature

**Symptoms**: A python crossref scanner run over docs/ reported 2 broken links in docs/doc-organiser-proposal.md (lines 36 and 60) pointing at `path` and `...`.

**Environment**: docs/ doc-review sweep on the dark-factory repo, ad-hoc python regex-based link scanner run inline via Bash.

**Triggering Conditions**: The target doc contained literal example markdown link syntax like `[...](path)` used to illustrate the link format itself, not actual hyperlinks.

## Root Cause
Regex-based link extraction can't distinguish a genuine markdown link from a literal code/prose example that happens to match link syntax.

## Solution
Manually inspect each flagged link in its surrounding context before reporting it as broken. Both flags here were literal regex/format examples inside doc-organiser-proposal.md, not real links, so the verdict was corrected to 'zero real broken cross-refs'.

## Prevention
Treat automated crossref-scanner flags as candidates requiring manual verification, not final verdicts; a link checker should special-case fenced/inline code spans and literal-syntax examples to cut false-positive noise.

## Related
- Sessions: 7a973797
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 7a973797 · 2026-06-16
- **Files** (candidate-level): docs/doc-organiser-proposal.md
- **Commits** (candidate-level): —
