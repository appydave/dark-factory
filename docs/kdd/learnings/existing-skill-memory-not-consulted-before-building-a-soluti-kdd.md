---
topic: "Memory not consulted at decision time"
issue: "Existing skill/memory not consulted before building a solution from scratch"
created: "2026-06-08"
story_reference: "215b9cee, ef961b51"
category: "tooling"
severity: "medium"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/constellation-first-placement.md"]
commits: []
---

# Memory not consulted at decision time — Existing skill/memory not consulted before building a solution from scratch

## Problem Signature

**Symptoms**: When asked whether two Claude sessions could safely write into the same repo, the assistant proposed 'put a traffic light on every shared page' (per-file locking) as the path to true multi-writer, instead of recalling that a separate stateful service should own shared state.

**Environment**: dark-factory audit session; the project's persisted-memory system (~/.claude/projects/.../memory/*.md)

**Triggering Conditions**: A live architecture question (can two sessions co-exist / write into the same repo) arose that matched an existing memory file's content almost exactly, but the memory wasn't re-consulted before answering.

## Root Cause
Memory being stored does not guarantee it is retrieved and applied at the moment a matching problem resurfaces — the trigger to consult stored notes on-topic is the weak link, not the existence of the knowledge itself.

## Solution
After being corrected, the assistant re-derived the correct answer (Switchboard as the state-owning service; identity as the real keystone) and explicitly recorded the recurrence inside the existing constellation-first-placement memory file, so a future session sees this has happened before rather than only holding the abstract principle.

```diff-after
**RECURRED 2026-06-12** — during the audit review the assistant again failed to apply this: when asked "can two sessions run?", it proposed file-level locks instead of "Switchboard owns the state." The lesson is now ratified into a concrete buildable sequence (identity→partition→worktrees→Switchboard) in [[parallelism-via-identity]].
```

## Prevention
Dev: when reasoning live about state-ownership, parallelism, or cross-session coordination questions, explicitly re-consult existing persisted notes on that exact topic before proposing a new mechanism inline, rather than reasoning from scratch and risking a worse answer than what's already stored.

## Related
- Sessions: 215b9cee, ef961b51
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 215b9cee, ef961b51 · 2026-06-08 → 2026-06-12
- **Files** (candidate-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/constellation-first-placement.md
- **Commits** (candidate-level): —
