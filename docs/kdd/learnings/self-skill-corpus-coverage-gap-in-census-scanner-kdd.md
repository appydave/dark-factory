---
topic: "self-skill corpus coverage gap"
issue: "Self-skill corpus coverage gap in census scanner"
created: "2026-05-27"
story_reference: "1f8758f3"
category: "tooling"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["research/artifacts.jsonl", "research/scripts/reconcile-self-skills.py"]
commits: ["2642737"]
---

# self-skill corpus coverage gap — Self-skill corpus coverage gap in census scanner

## Problem Signature

**Symptoms**: A manual disk-vs-jsonl diff found `k-fleet` and `pr-lifecycle` on disk in appydave-plugins but absent from artifacts.jsonl, plus ~25-30 skills living as real directories directly under ~/.claude/skills/ (never formalized into the appydave-plugins repo) with zero coverage in the census corpus.

**Environment**: research/artifacts.jsonl — Dark Factory's frozen artifact corpus, dark-factory repo

**Triggering Conditions**: The original recon/scan only enumerated the formal appydave-plugins repo path; it never scanned ~/.claude/skills/ for real user-installed skill directories, and hadn't been re-run since two new skills were added after the last recon pass.

## Root Cause
The recon scanner's scope was limited to one provider repo path; skills built directly into the global Claude Code skills directory bypass the formal plugin pipeline entirely and were structurally invisible to the census.

## Solution
Wrote research/scripts/reconcile-self-skills.py, an idempotent script that (1) adds appydave-plugins skills created after the last recon, (2) marks moved/archived skills with status: archived rather than deleting their records, and (3) adds ~/.claude/skills/ real (non-symlink) directories as a new provider, david-local. It backs up artifacts.jsonl before writing.

```python
APPYDAVE_PLUGINS = Path.home() / 'dev/ad/appydave-plugins'
GLOBAL_SKILLS = Path.home() / '.claude/skills'

def make_record(repo: str, artifact_type: str, name: str,
                file_path: Path, fm: dict) -> dict:
    ...
```

Run output:
```
Existing records: 1118
Backup written: artifacts.jsonl.bak-20260528-081859

Added: 32
  + appydave-plugins:skill:k-fleet
  + appydave-plugins:skill:pr-lifecycle
  + david-local:skill:algorithmic-art
  + david-local:skill:angela
  ...
```

## Prevention
When auditing a corpus for completeness, diff disk against the index across every real source path (not just the formal plugin repo) — and label symlinked/Anthropic-bundled directories as a separate, clearly-tagged provider so they aren't silently missed or double-counted in future scans.

## Related
- Sessions: 1f8758f3
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 1f8758f3 · 2026-05-27
- **Files** (candidate-level): research/artifacts.jsonl, research/scripts/reconcile-self-skills.py
- **Commits** (candidate-level): 2642737
