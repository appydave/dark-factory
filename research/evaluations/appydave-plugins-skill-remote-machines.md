---
artifact_id: appydave-plugins:skill:remote-machines
repo: appydave-plugins
artifact_type: skill
cluster_facet: [orchestration, spec-writing, workflow-architecture]
phase_fit: [1, 2, 9]
evaluated_at: 2026-05-17
---

# Eval: remote-machines

**Intent**: Run commands, copy files, or execute workflows on David's other four Macs via SSH using Tailscale IPs as the canonical addressing scheme.

## Scores
- **quality_score**: 3 — Accurate and complete reference card for the five-machine fleet. The Tailscale-preferred / .local-fallback hierarchy is clearly documented. Mostly static lookup table; low generative value.
- **adoption_fit_final**: mid — Machine-specific IPs and role descriptions are David's fleet only. The Tailscale-preferred pattern and the "proactive use" trigger ("Also use proactively when a task would clearly benefit from running on a specific machine") are the portable elements.
- **inspiration_value**: low — SSH command reference with machine roster is well-understood infrastructure knowledge. The "proactive invocation" trigger in the description (Claude should suggest this skill without being asked) is the only notable craft element.
- **uniqueness_refined**: commodity — Multi-machine SSH reference is standard ops knowledge.
- **composability**: standalone — Reference card; no agent orchestration hooks.
- **description_craft_refined**: trigger — Description includes both explicit trigger phrases and a proactive-invocation rule ("Also use proactively when a task would clearly benefit from running on a specific machine").

## Mineable phrasing
> "Also use proactively when a task would clearly benefit from running on a specific machine (e.g. a background job on the headless agent machine)."

## Notes
The proactive-invocation trigger ("Also use proactively...") is a description-craft pattern worth mining: it moves the skill from reactive (user must ask) to ambient (Claude recognises applicable situations). The machine role descriptions (Primary workstation / Headless bot / Jan's work / Mary's AITLDR) are a functional routing table for distributed task dispatch. The note about Jan and Mary possibly being offline with a date stamp ("last seen 7d ago as of 2026-04-04") shows good operational honesty.
