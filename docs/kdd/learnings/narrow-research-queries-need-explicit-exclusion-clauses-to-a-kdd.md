---
topic: "research prompt exclusion clauses"
issue: "Narrow research queries need explicit exclusion clauses to avoid generic adjacent results"
created: "2026-06-10"
story_reference: "f68c5f1c"
category: "process"
severity: "low"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["docs/upstream-repos/research-prompt.md"]
commits: ["6ee755b"]
---

# research prompt exclusion clauses — Narrow research queries need explicit exclusion clauses to avoid generic adjacent results

## Problem Signature

**Symptoms**: Without guardrails, a research prompt about 'agent orchestration' would be dominated by generic in-process agent libraries (CrewAI/AutoGen/LangGraph) rather than the target class of fleet-of-CLI-session control planes.

**Environment**: deep-research skill prompt design, dark-factory session, researching OSS analogues to the Dark Factory architecture

**Triggering Conditions**: researching a specific, narrowly-defined class of software (agent-fleet CLI orchestrators) that shares vocabulary with a much more commonly discussed, differently-shaped class (in-process multi-agent libraries)

## Root Cause
search and retrieval naturally surface the most common/well-indexed matches for shared terminology; without explicit exclusion of the adjacent-but-different class, results collapse into that more common class instead of the target one.

## Solution
The research prompt explicitly pinned the target class definition and added hard 'NOT' clauses (NOT single-agent chat wrappers, NOT IDE plugins, NOT in-process agent libraries) plus a named verify-by-name checklist, forcing the search to contrast the library class rather than list it as a match.

## Prevention
When writing a research prompt for a narrow architectural class of software, name the class precisely and add explicit NOT-exclusion clauses naming the closest generic/adjacent class, so results contrast against it instead of being absorbed into it.

## Related
- Sessions: f68c5f1c
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f68c5f1c · 2026-06-10
- **Files** (candidate-level): docs/upstream-repos/research-prompt.md
- **Commits** (candidate-level): 6ee755b
