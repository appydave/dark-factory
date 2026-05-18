---
artifact_id: appydave-plugins:skill:relay-register
repo: appydave-plugins
artifact_type: skill
cluster_facet: [discovery-routing, knowledge-capture, planning]
phase_fit: [1, 2, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: relay-register

**Intent**: Manage typed shared-folder channels (relay folders) between agent harnesses, apps, and people via Syncthing (internal) or Dropbox (external), using a Python script for all operations.

## Scores
- **quality_score**: 3 — Clear command reference with idempotency guarantee and migrate-safety checklist. The intent-inference table (what the user says → flags to pass) is a well-designed disambiguation layer. Limited to David's specific infrastructure topology.
- **adoption_fit_final**: mid — Tightly coupled to David's Tailscale/Syncthing/Dropbox setup and specific device names. The concept (typed relay folder as agent communication channel) is generalisable but the implementation is not portable without significant rework.
- **inspiration_value**: mid — The three-type (app/people/project) × two-transport (Syncthing/Dropbox) matrix is a clean taxonomy for inter-agent communication channels. The idempotency guarantee ("will NEVER rename or delete an existing folder") is a safety pattern worth noting.
- **uniqueness_refined**: uncommon — Relay-folder management as an agent skill (rather than manual setup) is not common in the corpus. The typed-channel taxonomy (app vs people vs project) is a distinct architectural concept.
- **composability**: standalone — Script-driven; no agent sub-invocations.
- **description_craft_refined**: trigger — Description lists ~20 trigger phrases covering all relay operations; the intent-inference table inside the skill body reinforces disambiguation.

## Mineable phrasing
> "typed shared-folder channels between agent harnesses and apps, or between people"

## Notes
The explicit idempotency rule (check before create, never overwrite) is a defensive infrastructure pattern that prevents Syncthing propagation failures. The Folder ID vs path distinction note ("The Folder ID shown in Syncthing UI is a separate identifier — treat them as distinct fields") is the kind of non-obvious operational detail that saves debugging time. The "open Syncthing" quick action (immediately run `open http://localhost:8384` rather than just show the URL) is a good ergonomic pattern: action over explanation.
