# ccswarm — nwiizo/ccswarm

**Repo:** https://github.com/nwiizo/ccswarm
**Local clone:** `~/dev/upstream/repos/ccswarm/` (cloned 2026-06-10; registered in `brains/source-repos.md`)
**Stars:** 139 (included for **architecture, not traction**) · **Latest:** v0.9.1 (2026-06-10) · **Lang:** Rust · **Status:** actively maintained
**Relevance rank:** #5 · **Strongest declarative-workflow model in the class**
**Review status:** ☐ not yet reviewed

> ⚠️ Star count / release date captured 2026-06-10 — re-verify before citing.

## What it is

A Rust **FlowEngine** that drives **Claude Code (full support) + Codex** running specialist personas — planner / coder / reviewer / qa / researcher — via **declarative YAML workflows**, with git-worktree isolation, producing PR-ready diffs. Self-described: "Multi-agent orchestration system using Claude Code with Git worktree isolation and specialized AI agents."

## Architecture

- **Isolation:** git-worktree per parallel agent — implemented in `crates/ccswarm/src/agent/isolation.rs`.
- **CLI support:** Claude provider = **full** (flags: `--allowed-tools`, `--agent`, `--resume`, `--system-prompt`, `--max-budget-usd`, `--worktree`); Codex via `codex exec`; `gh copilot` probed but unsupported (returns shell strings).
- **Dispatch:** **FlowEngine** orchestrates personas via YAML in `.ccswarm/flows/` — **sequential** (plan → sangha consensus → implement → review → fix → PR) or **parallel** (frontend + backend → supervisor).
- **State:** per-worktree (no central state-plane service).

## HITL model

Workflow-defined; includes a "sangha consensus" gate step. Largely autonomous within a declared flow.

## Observability

Minimal — no dedicated dashboard/telemetry surfaced; flows + worktree diffs are the artifact.

## Overlap with Dark Factory — and where it differs

**Closest anyone gets to Symphony + Marshall/Swagger roles expressed as data.** The YAML FlowEngine + typed personas is the structure-first/recipe→app pattern we favour (structure-first-then-render): the workflow is *declared*, the execution is mechanical.

**Differs:** no state-plane services, no visual control plane, low traction.

## What to steal

- The **declarative-workflow + persona model** — YAML-declared flows (plan → consensus → implement → review → fix → PR) as data, not code. Directly relevant to expressing Marshall's job-routing and Symphony stories as a schema.
- The **per-provider capability flags** (budget cap, allowed-tools, resume, worktree) as a clean CLI-adapter contract.

## What it gets wrong (for our purposes)

- No external observability — can't observe the loop without reading worktrees.
- No plane separation; single-machine, single-process orchestration.

## Next-action if we review

Read the FlowEngine + YAML schema (`.ccswarm/flows/`) as a candidate shape for declaring Symphony workflows-as-data; compare the persona model against our Swagger job-agent + sub-agent decomposition.
