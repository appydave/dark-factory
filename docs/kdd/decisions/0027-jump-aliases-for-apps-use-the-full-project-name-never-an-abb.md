---
id: ADR-0027
title: "Jump aliases for apps use the full project name, never an abbreviation"
status: proposed
scope: internal
date_decided: 2026-06-10
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["a76dc657"]
  files: [".config/appydave/locations.json", "~/.oh-my-zsh/custom/aliases-jump.zsh"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0027: Jump aliases for apps use the full project name, never an abbreviation

**Status:** Proposed (reconstructed)

## Context

Adding a `jump` skill entry for dark-factory to `~/.config/appydave/locations.json`. The user's own suggestion was a short form (`japp-df` or `japp-darkfactory`). No entry existed yet for this app, so the convention had to be inferred from sibling app entries already in the file (`watchtower`, `angeleye`, `thumbrack`).

## Decision

Named the new entry `japp-darkfactory` — the full app name — matching the pattern already used by every other `type: product`/app entry (`japp-watchtower`, `japp-angeleye`, `japp-thumbrack`).

## Alternatives Considered

`japp-df` (short form, closer to the user's original suggestion) was considered but rejected: it would be the only abbreviated jump alias among app entries, breaking visual/behavioral consistency with the existing sibling apps.

## Consequences

Establishes the standing rule for `type: product` entries in locations.json: jump aliases are always `japp-<full-name>`, not abbreviations. Abbreviated aliases remain fine at the brand level (e.g. `ad`, `v`, `ss`) but not for individual app/product keys. Future app entries should follow this without re-deriving it from scratch.

## Related

- Sessions: `a76dc657`

## Provenance

- **Sessions** (1): `a76dc657` · 2026-06-10
- **Files** (candidate-level): `.config/appydave/locations.json`, `~/.oh-my-zsh/custom/aliases-jump.zsh`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
