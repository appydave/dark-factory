---
topic: "sandbox PATH stripped in piped subshells"
issue: "Sandbox PATH stripped in piped subshells"
created: "2026-06-10"
story_reference: "1b7b1ab9"
category: "debugging"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: session
files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/appyradar-identity-resolved.md", "dev/ad/apps/angeleye/.claude/skills/angeleye-retrieve/SKILL.md", "dev/ad/apps/appyradar-sentinal/sentinel.config.example.json", "dev/ad/apps/appyradar-sentinal/sentinel.config.json", "dev/ad/apps/appyradar-sentinal/src/collect.ts", "dev/ad/apps/appyradar-sentinal/src/collectors/bash-scripts.ts", "dev/ad/apps/appyradar-sentinal/src/collectors/disk-usage/collector.ts", "dev/ad/apps/appyradar-sentinal/src/collectors/orchestrator.ts", "dev/ad/apps/appyradar-sentinal/src/collectors/parsers.ts", "dev/ad/apps/appyradar-sentinal/src/expose/mcp.ts", "dev/ad/apps/appyradar-sentinal/src/main.ts", "dev/ad/apps/appyradar-sentinal/src/ssh/client.ts", "dev/ad/apps/appyradar-sentinal/src/types.ts", "dev/ad/apps/appyradar-sentinel/README.md"]
commits: []
---

# sandbox PATH stripped in piped subshells — Sandbox PATH stripped in piped subshells

## Problem Signature

**Symptoms**: Running a shell function (`check() { ... | wc -l | tr -d ' ' ... }`) and a `for entry in ...; do ... | head ...; done` loop to audit git status across multiple repos produced repeated `command not found: wc`, `command not found: tr`, `command not found: sed`, and `command not found: head`.

**Environment**: Bash tool execution during a dark-factory session, auditing git status across the appysentinel, appyradar-sentinel, angeleye, and dark-factory repos

**Triggering Conditions**: Defining a shell function or a `for`/`while` loop that pipes command output through external coreutils binaries inside the Bash tool's subshell.

## Root Cause
The sandboxed Bash tool strips PATH for piped/looped subshells, so coreutils binaries that resolve fine at the top level are unavailable inside those nested pipe/loop contexts.

## Solution
Abandoned the function/loop-with-pipes approach and ran plain `git status -sb` (and similar direct git subcommands) once per repo with no pipes, no loops, and no coreutils — git's own output already gives branch, ahead/behind, and dirty-file state without needing external filtering.

```bash
# before — fails: PATH stripped inside the piped/looped subshell
check() {
  local name="$1" path="$2"
  branch=$(git -C "$path" branch --show-current 2>&1 | head -1)   # command not found: head
  dirty=$(git -C "$path" status --porcelain | wc -l | tr -d ' ')  # command not found: wc/tr
}

# after — works: direct git subcommands, no pipes/loops/coreutils
echo "=== appysentinel ==="; git -C "$HOME/dev/ad/apps/appysentinel" status -sb
echo "=== appyradar-sentinel ==="; git -C "$HOME/dev/ad/apps/appyradar-sentinel" status -sb
echo "=== angeleye ==="; git -C "$HOME/dev/ad/apps/angeleye" status -sb
```

## Prevention
When auditing multiple repos via the Bash tool, avoid shell functions/loops that pipe through coreutils (`head`/`wc`/`tr`/`sed`) — call the underlying command's own flags directly per target (e.g. `git status -sb`, `git log --oneline -n`) instead of post-processing its output through an external filter inside a nested subshell.

## Related
- Sessions: 1b7b1ab9
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 1b7b1ab9 · 2026-06-10
- **Files** (session-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/appyradar-identity-resolved.md, dev/ad/apps/angeleye/.claude/skills/angeleye-retrieve/SKILL.md, dev/ad/apps/appyradar-sentinal/sentinel.config.example.json, dev/ad/apps/appyradar-sentinal/sentinel.config.json, dev/ad/apps/appyradar-sentinal/src/collect.ts, dev/ad/apps/appyradar-sentinal/src/collectors/bash-scripts.ts, dev/ad/apps/appyradar-sentinal/src/collectors/disk-usage/collector.ts, dev/ad/apps/appyradar-sentinal/src/collectors/orchestrator.ts, dev/ad/apps/appyradar-sentinal/src/collectors/parsers.ts, dev/ad/apps/appyradar-sentinal/src/expose/mcp.ts, dev/ad/apps/appyradar-sentinal/src/main.ts, dev/ad/apps/appyradar-sentinal/src/ssh/client.ts, dev/ad/apps/appyradar-sentinal/src/types.ts, dev/ad/apps/appyradar-sentinel/README.md
- **Commits** (session-level): —
