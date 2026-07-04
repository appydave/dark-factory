---
id: ADR-0028
title: "Close the KDD/Lisa read-gate — the write loop is built, read enforcement is not"
status: accepted
scope: internal
date_decided: 2026-07-03
deciders: [David Cruwys]
confidence: confirmed
recurrence_count: 1
provenance:
  sessions: ["c89d3d81"]
  files: ["docs/app-requirements-spec.md", "docs/build-a-kyberagent-extension.md", "docs/constellation-map.md", "docs/daily-operating-model.md"]
  commits: []
tags: []
---

> 🤖 Reconstructed via Lisa KDD pipeline, 2026-07-04. Ratified by David 2026-07-04.

# ADR-0028: Close the KDD/Lisa read-gate — the write loop is built, read enforcement is not

**Status:** Accepted

## Context

Lisa's reconstruct-kdd pipeline (the KDD write loop) already runs on two real projects (Cortex → 69-doc KDD, KBDE → 58 sessions staged) and produces curated learnings/patterns/decisions with human sign-off. But nothing in dark-factory's own pipeline (daily briefing, BA-agent, goal-plan) consults docs/kdd/ or a brain before starting new work. A five-agent cross-repo research pass (brainiac, cortex, KBDE, dark-factory surface, plus the sibling case-study session) converged on the same finding independently: the sibling session on this repo re-derived facts already sitting on disk multiple times within one sitting — the same three-folder disambiguation question was asked four separate times, machine identity was resolved by two separate multi-minute agent runs, and a 107k-token harness-lineage research pass only reconfirmed a verdict two existing repo docs (darkfactory-reconciliation.md, suborch-conformance.md) already stated.

## Decision

Treat the missing read gate as the priority integration point rather than investing in more KDD-write tooling. Recommended sequence: (1) sync the lisa plugin skill onto mac-mini-m4, the machine dark-factory sessions actually run on (it exists only on Roamy as v5.9.0; mac-mini-m4 has v5.4.1 without it), (2) bootstrap dark-factory's own KDD by running reconstruct-kdd against its own session archive so this session and the sibling session become the first captured knowledge, (3) build the spec'd-but-unbuilt KBDE brain-mcp bridge (exposing a local k-darkfactory brain plus the k-brain second-brain as MCP tools) together with its companion-skill gates — G1 no-query (don't ask the brain what a local file already answers), G2 citation (cite source_path), G3 negative-result (search 2+ phrasings before asserting 'nothing known') — since those three gates are exactly the discipline the sibling session lacked, (4) wire that read as an enforced hook (SessionStart / goal-plan / BA-briefing) rather than an optional habit, then (5) unify the two knowledge stores by pointing cortex's file-as-truth reconcile() at docs/kdd/ as a watched folder so markdown stays the ledger and cortex indexes it.

## Alternatives Considered

Continue investing in more KDD-write capability alone (more reconstruct-kdd runs, kdd-viewer polish, the idea-extraction 5th artifact type) without adding a read gate — rejected as treating the symptom, since the brain's own prior measurement already shows advisory-only reads get skipped ('Bob's create-time KDD reads were 1,0,0,0,1 across the heaviest creation sessions; nothing enforces the scan'). Within the read gate itself, hard-block hook vs. advisory-injection was also weighed and left open, leaning advisory-injection first and hardening only if it's still skipped in practice.

## Consequences

If unaddressed, every new dark-factory session risks re-paying the rediscovery cost the sibling session paid — repeated agent-minutes and tokens spent re-deriving already-settled facts (machine identity, folder disambiguation, harness-lineage verdicts) instead of consulting a librarian once. The KBDE-extension host-mount for a librarian surface is gated on an unrelated Extension SDK handover, so this sequence is deliberately scoped to not depend on it — the read channel is an MCP server + hook, not a KBDE extension, so it is buildable now.

## Related

- Sessions: `c89d3d81`

## Provenance

- **Sessions** (1): `c89d3d81` · 2026-07-03
- **Files** (candidate-level): `docs/app-requirements-spec.md`, `docs/build-a-kyberagent-extension.md`, `docs/constellation-map.md`, `docs/daily-operating-model.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
- 2026-07-04 — ratified — the strongest possible confirmation: this decision was independently acted on the same day (mac-mini-m4 built `kdd-bridge`, an MCP read-bridge, directly from this ADR — smoke-tested, G2/G3 gates structurally confirmed working; see `backlog/2026-07-04-kdd-read-gate-handover.done.md`). Note: the Context section's cited counts ("Cortex → 69-doc KDD, KBDE → 58 sessions staged") are now stale — Cortex has 112 docs, KBDE 208, as of this ratification — not an error, both grew since 2026-07-03; doesn't affect the decision's validity. Status → accepted, confidence → confirmed.
- 2026-07-04 — superseded (partially) — David's PO direction (same day, appended to the handover doc) reshapes this decision's remaining scope: the read-gate's real home is structural SDLC checkpoints (PR-created → validate against KDD; worker-output-absorbed → write back through Lisa), not a session-start advisory alone. The MCP built above serves those checkpoints, it doesn't replace them. That follow-on design/build is out of this ratification's scope.
