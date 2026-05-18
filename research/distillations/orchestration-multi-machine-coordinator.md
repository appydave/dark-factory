---
distillation_id: orchestration-multi-machine-coordinator
stage: orchestration
intent: "Run commands, copy files, or execute workflows across David's Mac fleet or external platforms via SSH, Ansible, or API"
created: 2026-05-16
status: draft
source_artifacts:
  - appydave-plugins:skill:remote-machines
  - appydave-plugins:skill:ansible-fleet
  - ruflo:agent:device-coordinator
  - ruflo:agent:fleet-manager
  - ruflo:agent:federation-coordinator
  - ruflo:command:federation
  - ruflo:command:iot
  - gstack:skill:pair-agent
  - appydave-plugins:skill:paperclip
  - ruflo:skill:github-multi-repo
winner_mechanism: appydave-plugins:skill:remote-machines
---

# Unified Skill: multi-machine-coordinator

**Purpose**: Dispatch work to remote machines (SSH), manage fleet-wide provisioning (Ansible), or coordinate across external platforms — the cross-boundary orchestration layer.

**For Agents**: Use when David says "run this on the M4", "SSH to M2 and do X", "deploy across the fleet", "manage all my machines", "cross-machine", or needs to coordinate work that spans physical or cloud boundaries.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Coordinate work across multiple machines (SSH + Ansible) or external platforms (Paperclip API, federation) — dispatch commands, monitor results, handle cross-boundary state.

## Winner's Mechanism

`appydave-plugins:skill:remote-machines` wins because it is already in David's stack, knows his fleet (M4 Mini, M2 Mini, Roamy, Jan, Mary via Tailscale IPs), and handles the three most common operations: run commands, copy files, execute workflows. It is the correct entry point for David's 5-Mac environment.

`appydave-plugins:skill:ansible-fleet` is the companion for fleet-wide provisioning (Ansible playbooks across the AppyDave + client machine groups) — different concern (configuration management vs ad-hoc commands), different tool.

## Non-overlapping ideas folded in

- From `ruflo:agent:device-coordinator`: **5-tier trust scoring** for device fleet members — trust is a property of the device, not just the user. Useful when David adds new machines or agents to the fleet.
- From `ruflo:agent:federation-coordinator`: **Zero-trust cross-installation federation** — agents on different Claude installations coordinate via signed claims. Relevant if the Kybernesis multi-tenant model requires cross-installation coordination.
- From `gstack:skill:pair-agent`: **Pair a remote AI agent with a browser session** — extends multi-machine to include browser-based workflows running remotely.
- From `ruflo:command:iot`: **IoT device fleet** (Cognitum Seed) — generalizes fleet management beyond Macs to embedded devices. Not currently relevant but the mental model (fleet = any connected node) is worth keeping.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| remote-machines | Fleet awareness, SSH commands, file copy, workflow dispatch | None — this is the winner |
| ansible-fleet | Fleet-wide Ansible playbook execution (config management layer) | Client machine scoping (separate concern) |
| ruflo:device-coordinator | Trust-scoring for fleet members | Cognitum Seed hardware dep |
| ruflo:federation-coordinator | Cross-installation zero-trust coordination | Federation infrastructure dep |
| gstack:pair-agent | Browser-paired remote agent | GStack browser extension dep |
| ruflo:github-multi-repo | Multi-repo coordination as cross-machine pattern | GitHub-specific |
| paperclip | External platform API coordination | Paperclip-specific REST endpoints |

## Draft SKILL.md frontmatter

```yaml
name: multi-machine-coordinator
description: >
  Dispatch commands, copy files, or run workflows across David's Mac fleet
  (M4 Mini, M2 Mini, Roamy, Jan, Mary) via SSH + Tailscale, or coordinate
  fleet-wide provisioning via Ansible playbooks.
  Existing instances: remote-machines (ad-hoc SSH), ansible-fleet (config management).
  Use when: "run on M4", "SSH to M2", "across the fleet", "deploy all machines",
  "cross-machine", "sync files between machines", "provision new machine".
```

## Open questions for David

- `remote-machines` and `ansible-fleet` are already separate skills — is this distillation better as **documentation of the two-skill pattern** rather than a unified skill?
- Should federation (cross-Claude-installation coordination) be added to `remote-machines` now that Kybernesis is underway, or kept separate?
- Is there a "fan-out to all machines" orchestrator missing? (Run the same task on M4 + M2 + Roamy in parallel, collect results.)
