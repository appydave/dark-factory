---
id: ADR-0032
title: "apps/watchtower is the durable home; experiments/watchtower-engine is a disposable proof-of-concept"
status: proposed
scope: internal
date_decided: 2026-06-12
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["ef961b51"]
  files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/watchtower-app-vs-engine.md", "AUDIT-2026-06-12.md"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0032: apps/watchtower is the durable home; experiments/watchtower-engine is a disposable proof-of-concept

**Status:** Proposed (reconstructed)

## Context

The name 'Watchtower' referred to three different things: the brain's 'control surface' concept, the empty one-commit apps/watchtower scaffold, and the working dispatch engine buried in dark-factory/experiments/watchtower-engine/ (real rename(2) atomic claim, reaper proven unattended, 35 jobs through done/, live board on :7430). Docs described the working engine but filed it under the name pointing at the empty scaffold, so readers looking for 'Watchtower' found nothing.

## Decision

apps/watchtower is the canonical, durable home for Watchtower; it will be rebuilt there on the AppySentinel (or AppyStack) template once the current experiment has de-risked the design. experiments/watchtower-engine remains the disposable proving ground until then, not the permanent home.

## Alternatives Considered

The assistant's original recommendation was the opposite: promote experiments/watchtower-engine in place and let it own the 'Watchtower' name, archiving the empty apps/watchtower shell. This was rejected — it would enshrine a spike as production. The repo owner's call (experiment=disposable PoC, app=durable artifact) was adopted instead.

## Consequences

The dispatch engine mechanics stay in experiments/ as a PoC; a future rebuild effort is needed to port proven mechanics into apps/watchtower on a proper template. Resolves the 3-way name collision going forward.

## Related

- Sessions: `ef961b51`

## Provenance

- **Sessions** (1): `ef961b51` · 2026-06-12
- **Files** (candidate-level): `.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md`, `.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/watchtower-app-vs-engine.md`, `AUDIT-2026-06-12.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
