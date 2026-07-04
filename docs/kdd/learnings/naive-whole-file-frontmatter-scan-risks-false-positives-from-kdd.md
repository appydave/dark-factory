---
topic: "Frontmatter status scan must not read the whole file body"
issue: "Naive whole-file frontmatter scan risks false positives from body text"
created: "2026-06-23"
story_reference: "2fdc2412"
category: "tooling"
severity: "low"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["apps/kdd-viewer/lib/frontmatter.py"]
commits: []
---

# Frontmatter status scan must not read the whole file body — Naive whole-file frontmatter scan risks false positives from body text

## Problem Signature

**Symptoms**: Risk of incorrect/inflated field-coverage counts (e.g. 'X of 578 learnings carry status') if a naive whole-file text search were used across a large, uncontrolled real-world markdown corpus.

**Environment**: KDD Viewer v1 build (build #6 of the 2026-07-03 cut), scanning SupportSignal's 578-learning KDD corpus.

**Triggering Conditions**: Computing frontmatter field coverage across hundreds of real markdown files, some of which embed example code or prose in their bodies that can resemble frontmatter syntax.

## Root Cause
A whole-file regex/grep approach cannot distinguish an actual frontmatter field from a matching string that merely appears somewhere in the document body.

## Solution
The hand-rolled frontmatter parser only reads between the first two `---` delimiter lines of each file, so field-coverage numbers are computed strictly from the real frontmatter block.

## Prevention
When parsing frontmatter across a large, uncontrolled document corpus, always bound the parse to the delimited frontmatter block — never grep/regex the whole file body for field-like strings.

## Related
- Sessions: 2fdc2412
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 2fdc2412 · 2026-06-23
- **Files** (candidate-level): apps/kdd-viewer/lib/frontmatter.py
- **Commits** (candidate-level): —
