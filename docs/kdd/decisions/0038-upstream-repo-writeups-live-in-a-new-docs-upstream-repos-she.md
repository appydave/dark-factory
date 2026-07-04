---
id: ADR-0038
title: "Upstream-repo writeups live in a new docs/upstream-repos/ shelf; actual repo clones live only in the canonical ~/dev/upstream/repos/ registry, never inside the dark-factory app"
status: proposed
scope: internal
date_decided: 2026-06-10
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["f68c5f1c"]
  files: ["docs/INDEX.md", "docs/upstream-repos/2026-06-10-fleet-orchestrator-research.md", "docs/upstream-repos/README.md", "docs/upstream-repos/cao-cli-agent-orchestrator.md", "docs/upstream-repos/ccswarm.md", "docs/upstream-repos/composio-agent-orchestrator.md", "docs/upstream-repos/research-prompt.md"]
  commits: ["6ee755b"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0038: Upstream-repo writeups live in a new docs/upstream-repos/ shelf; actual repo clones live only in the canonical ~/dev/upstream/repos/ registry, never inside the dark-factory app

**Status:** Proposed (reconstructed)

## Context

Needed to persist a deep-research finding (CAO, Composio agent-orchestrator, ccswarm as the closest OSS analogues to Dark Factory's architecture) as durable documentation, and the user asked to also put the 3 repos themselves somewhere reviewable. Two existing candidate locations existed for the docs: research/recon/ (the distillation-catalog corpus for the 1,100-artifact skill census) or a new folder — and for the code, either clone directly into dark-factory or use an existing brain-registered upstream location.

## Decision

Created docs/upstream-repos/ inside dark-factory for writeups only (method + verbatim prompt + per-repo findings + README index). The actual repo clones were placed at the canonical ~/dev/upstream/repos/{cli-agent-orchestrator,agent-orchestrator,ccswarm}/ location and registered in ~/dev/ad/brains/source-repos.md under a new 'Dark Factory — Fleet-Orchestrator Reference Sources' section paired to the dark-factory brain.

## Alternatives Considered

(a) File the writeups in research/recon/ — rejected because that folder is the distillation-catalog cluster for THE 1100 skill-distillation corpus, is governed by a hard 'no non-recon data' rule, and is crawled by the dark-factory-catalog skill; mixing in architectural-exemplar writeups would pollute the crawler's corpus. (b) Clone the 3 repos directly into the dark-factory app (what was initially proposed and done in the assistant's first answer) — rejected/corrected once the user pointed at the existing brain registry: repo clones belong in the canonical ~/dev/upstream/repos/ location, not inside any single consuming app.

## Consequences

dark-factory stays markdown-only for this material (no vendored 3rd-party code in the app repo); the actual source is available locally for review at ~/dev/upstream/repos/ and discoverable via the brain registry like every other upstream source; each per-repo doc in docs/upstream-repos/ was subsequently edited to point at its local clone path so the two locations stay linked.

## Related

- Sessions: `f68c5f1c`

## Provenance

- **Sessions** (1): `f68c5f1c` · 2026-06-10
- **Files** (candidate-level): `docs/INDEX.md`, `docs/upstream-repos/2026-06-10-fleet-orchestrator-research.md`, `docs/upstream-repos/README.md`, `docs/upstream-repos/cao-cli-agent-orchestrator.md`, `docs/upstream-repos/ccswarm.md`, `docs/upstream-repos/composio-agent-orchestrator.md`, `docs/upstream-repos/research-prompt.md`
- **Commits** (candidate-level): `6ee755b`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
