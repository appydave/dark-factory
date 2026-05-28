# Watchtower v0 — Session Context

**Date**: 2026-05-28
**Purpose**: Orientation for the three parallel agents drafting Watchtower requirements

---

## Who David is

Sole author / PO / ratifier of the Dark Factory project. Builds the system *for himself*, by himself. Hands-on technical operator. Time and attention are the scarce resources, not money or compute.

## What just happened (the trigger)

Ran Level 1 Census batch 0 (5 artifacts assessed). Built Mochaccino design 09 to visualize progress. At only 5 records, the dashboard already feels cluttered. David's articulated signal:

> *"I look at a screenshot like this, and in its small we've only done five things. From a point of view, it's okay, but this is going to get to overwhelm within two or three iterations. I want to have a series of experiments that we keep testing but probably also promote experiments to proper workflows."*

This is the prototype-to-product wall. Mochaccino was the thinking tool; the Watchtower is the operating surface.

## Key decisions already made

These are **fixed inputs**, not open questions:

1. **Watchtower lives inside `dark-factory/` repo at `apps/watchtower/`** — not a separate repo yet. Data model is still moving; colocation reduces friction.
2. **Scaffold with `appydave:create-appystack`** (David's own skill for spinning up RVETS apps). Don't design the stack — just use it.
3. **Four machine-readable records**: `experiment.yml`, `run.json`, `learning.yml`, `promotion.yml`. See chatgpt-brief.md for shape.
4. **9-layer learning taxonomy**: prompt, agent, skill, workflow, harness, evaluation, data_schema, watchtower_ui, orchestration.
5. **Swagger orchestration model** (BMAD-style conductor): one ticket, one delegated worker at a time, returns with a take, Swagger decides next move, asks David only at judgement points. Specialist roles underneath: Architect / Builder / Runner / Evaluator / Learning Miner / Promoter.
6. **First vertical slice is census-batch-1**, NOT a new domain like thumbnail ideation. Dogfood what's already running.

## Key open questions (your output should help answer or surface these)

- What is the minimum data contract between Watchtower and the workflow harness in `.claude/workflows/`?
- How does Watchtower trigger a workflow run? (file-write, exec, MCP?)
- Where does ratified vs experimental separation live in the filesystem?
- What's the storage backend? Plain JSON/YAML files vs SQLite vs both?
- Should the diagram view be auto-generated from workflow scripts or hand-authored?

## Parent architecture references

Read these for grounding (in order of priority):

1. `docs/dark-factory-living-system-spec.md` — the canonical vision spec (SkillOpt grounding, 5 eval levels, 3 trigger types). Section 1, 2, 3, 4 are essential.
2. `docs/architecture.md` — the parent architecture doc. Library / Warehouse / Watchtower / Transpiler / Provider model.
3. `mochaccino/designs/09-census-progress/index.html` — current state of the censusing work this Watchtower is being built around.
4. `.claude/workflows/level-1-census.workflow.js` — the first real workflow. Watchtower must be able to drive THIS specifically.
5. `research/artifacts.jsonl` — 1,150 artifacts, 15 providers (skim first 5 lines for data shape).
6. `research/census.jsonl` — 5 records so far, what census output looks like.

## The dogfooding loop

You — the agent reading this — are part of the proof. The Dark Factory censused `agent-skills:api-and-interface-design` / `agent-skills:spec-driven-development` / `plan-hunter` as tier-4 or tier-5 skills. By invoking those skills to design the Watchtower, we're testing whether the census verdicts are real. Your output's quality is the first validation signal.

## Boundaries on your output

- **Don't ask David clarifying questions** — he's stepped back and asked for parallel drafts. Surface ambiguities as `Open Questions` sections in your output.
- **Be opinionated** — the brief is opinionated input. Push back where you think it's wrong. Mark your dissent clearly.
- **Stay v0-scoped** — anything that smells like "v0.1 or later" goes in an explicit `Out of Scope` section.
- **Local-only, single-user** — no auth, no multi-tenancy, no deployment story.
- **Keep your output under 600 lines unless your skill specifically requires more.**

## What the parent will do with your output

After all three agents return:
1. David reads all three (schemas.md, spec.md, plan.md)
2. `agent-skills:code-review-and-quality` is invoked as a critique pass on the three docs
3. David decides what to keep / merge / reject
4. `appydave:create-appystack` scaffolds `apps/watchtower/`
5. First vertical slice (census batch 1 through Watchtower) is built

Your output is consumed by humans + one more LLM review pass. Optimize for both.
