# Upstream Repos — 3rd-Party Architectural Reference Shelf

This folder holds writeups of **3rd-party open-source repos worth studying as architectural exemplars** for building the Dark Factory constellation. Park them here, review later.

> **Not to be confused with `research/recon/`.** That folder is the **distillation-catalog cluster** (BMAD, gstack, Superpowers, … — the ~15 repos feeding THE 1100 skill-distillation, crawled by the `dark-factory-catalog` skill). **This** folder is for repos we study to learn *how to build the factory itself* — different purpose, kept separate so neither pollutes the other.
>
> **Docs only — no code here.** The actual repo *clones* live in the canonical upstream location `~/dev/upstream/repos/` (registered in `~/dev/ad/brains/source-repos.md`, paired to the `dark-factory/` brain). Only the docs about what they mean for Dark Factory live in this folder. Closest-3 clone paths: `cli-agent-orchestrator/`, `agent-orchestrator/`, `ccswarm/` under `~/dev/upstream/repos/`.

## What's here

| File | What |
|------|------|
| [`2026-06-10-fleet-orchestrator-research.md`](./2026-06-10-fleet-orchestrator-research.md) | **Method + findings** — who else builds our class (fleet-of-CLI-sessions orchestrators), the green-field finding, full ranked table |
| [`research-prompt.md`](./research-prompt.md) | The verbatim `deep-research` prompt (reproducible) |
| [`cao-cli-agent-orchestrator.md`](./cao-cli-agent-orchestrator.md) | **CAO** (awslabs) — closest architectural match; central dispatch + liveness + reap-with-scrollback |
| [`composio-agent-orchestrator.md`](./composio-agent-orchestrator.md) | **agent-orchestrator** (Composio) — highest traction; liveness-via-GitHub-signals |
| [`ccswarm.md`](./ccswarm.md) | **ccswarm** (nwiizo) — declarative YAML workflow + persona model |

## The headline finding (2026-06-10)

The fleet-of-CLI-sessions class is **real, active, and crowded** — but **no surveyed project ships our architecture**: a stateless floor + separate state-plane services (comms bus + session telemetry + resource-health + visual control plane). Everyone folds state into **per-worktree files** or **GitHub**. The constellation split is a **genuine green-field gap** — a defensible thesis, not a reinvention.

The **closest 3 to study** (filed above): CAO (#1, dispatch/liveness/reap), Composio agent-orchestrator (#3, external-signal liveness), ccswarm (#5, workflows-as-data).

## Convention for adding a repo

One `.md` per repo, kebab-case. Suggested sections: what it is · stars/activity (with a "captured on" date — counts drift fast) · architecture (dispatch / state / liveness / reaping) · HITL · observability · overlap-with-Dark-Factory · what-to-steal · what-it-gets-wrong · review-status checkbox.
