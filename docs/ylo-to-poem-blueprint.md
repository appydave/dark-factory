# YLO → POEM Blueprint

**Status:** thinking captured · decision-oriented · not yet ratified
**Date:** 2026-05-22
**Audience:** David (solo)
**Origin:** synthesised from a working session comparing YLO blackboard ↔ POEM ↔ AWB (Gen 1 Ruby + Gen 3 TS), plus two deep-dive agent investigations. Source paths in §10.

---

## 0. The frame (read this first)

- **YLO will die.** It was always a testing ground. The *learnings* migrate into POEM. This doc is the migration's source of record.
- **`dark-factory` becomes the first POEM consumer.** It gets a `.poem/` folder; YLO's four workflows get **rebuilt in POEM**, not ported as-is.
- **POEM stops being a repo, becomes an Anthropic plugin** (per Nick / ALS conversation, 2026-05-21). Packaging, MCP, hooks, marketplace install all in scope.
- **Penny grows from Prompt Engineer → Agent Engineer.** Her unit expands from `input → prompt → output` to a full agent (`+ tools + model + capabilities`).
- **The Workflow Architect splits in two:** heavy **Alex** (compile-first, production) and a lightweight **QuickArchitect** (fast, dynamic, the verified v1 7-step formula) — likely a *facade* over Alex.

Everything below is the reasoning + the cross-system change punchlist (§8).

---

## 1. The three systems and the boundary

| System | Role | Status |
|--------|------|--------|
| **POEM** | Authoring surface — prompts (Penny), workflow definition (Alex/QuickArchitect), the method | becomes the home; repackage as plugin |
| **AWB Gen 3** | Compile + run — `WomPackage` contract + runtime engine | keep as the *runtime*; simplify state model (§3) |
| **YLO blackboard** | Fluid in-session testing ground | **freeze, harvest, archive** |

**The boundary, made honest:**

> **POEM owns the authoring surface** — including *"what a workflow looks like"* (the definition format) and the agents that produce it.
> **AWB owns the runtime contract** — `WomPackage` + the engine.
> **The workflow definition (YAML/DSL) is the handoff artifact.**

Today the definition shape is split awkwardly across both. Pulling the *definition format* into POEM and leaving AWB to own *compile + execute* matches what each is actually for. **AWB does not "use" Alex** — it consumes Alex's *output* (the YAML). No BMAD personas live in AWB; its equivalent roles are code (compiler, linter, runtime, SDK).

**The "workflow architect" role has had three incarnations** — the role persists, the embodiment changes:
1. v1 Ruby `agent_workflow_architect` (2024)
2. POEM's Alex (BMAD persona)
3. AWB's compiler (code, no persona)

---

## 2. The four primitives — a layer model, not a menu

Tool / prompt / subagent / skill are **layers that compose**, not alternatives:

- **Tool** — a verb Claude *uses* (Read/Write/Bash, or an MCP tool). The raw capability. *Not* an extension mechanism.
- **Prompt** — the words. A `.hbs` template is a parameterised prompt body.
- **Subagent** — *prompt + its own clean context window + a tool grant* (+ optional model/memory/isolation). Adds **context isolation + result-only return**.
- **Skill** — discoverable expertise *loaded into* context, model-invoked by its `description`, retains history.

Consequences that matter for POEM/AWB:

- **A workflow step should be a SUBAGENT, not a skill.** A skill self-triggers by description match; a workflow needs the *orchestrator* to control sequencing. The `.hbs` is the subagent's prompt body; the `.json` is its I/O contract.
- **A reusable, agent-discoverable capability should be a SKILL** (e.g. image-gen). David already proved the idiom: `appydave-thumbnail` is a skill whose body shells to a Python script hitting kie.ai, credential via env var.
- **Enforcement lives in the subagent's `tools:` allowlist** (a *real* allowlist) **+ an output schema** — **not** in a skill's `allowed-tools` (which in current Claude Code is only a *pre-approval* list, it does **not** restrict). This is the lever for AWB's "know the data is shaped appropriately."
- **Image-gen / external APIs = a skill or an MCP server, USED BY a subagent** — never a subagent themselves. (MCP when you want it as a first-class, schema-validated, shared-credential tool across many agents.)

---

## 3. State model — event sourcing + projections (delete the mutability enum)

**History (confirmed in code):**
- v1 Ruby + POEM: flat **mutable** key-value store, overwrite-by-key, no version, no log. "suggestedTitles vs titles as two keys" was **convention, not a guard rail**.
- YLO: jumped straight to **event sourcing** — append-only log, a copy of every value, no mutation — *because parallel fan-out forces it* (concurrent appends don't conflict; concurrent mutations do). Plus a **projection** (`store.view.json`, last-write-wins). That's event-sourcing-with-roll-up.
- AWB Gen 3: added a per-slot **`mutability` enum** (`mutable / immutable-after-first-write / append-only / replace-with-review / derived`).

**The insight:** AWB's mutability enum is complexity a different model dissolves. **In event sourcing, mutability is not a storage property — it's a projection (roll-up) policy.** Every fact is immutable; the *fold* decides the read semantics:

| AWB mutability mode | = projection fold over one append-only log |
|---|---|
| `mutable` | last-write-wins |
| `immutable-after-first-write` | first-write-wins |
| `append-only` | keep-all |
| `replace-with-review` | last-write-wins **gated by a review event** |
| `derived` | computed fold over other keys |

So **5 write-time mutation behaviours → 5 read-time fold strategies over one dumb substrate.** One write path, N read policies. A **relational-looking output record** (`{ titles, suggestedTitles, … }` as columns) is just a projection shape; "mutating" a value = append an event + re-project. No mutation logic in the store.

**The clean architecture — three separable layers:**
1. **Append-only log** — one write model (YLO's blackboard substrate).
2. **Projection policies** — the read-side fold (replaces the mutability *modes*).
3. **Write-time validators** — optional guard rails as *checks over the log* (`if key K folds to >1 ok-event and policy=immutable → raise`). This is where AWB's "shaped appropriately" guarantee + Penny's output schema live.

**Honest caveat:** a projection changes how you *read* — it can't *reject* a bad *write*. That's exactly why layer 3 (validators) exists. But validators are rules over the log, not storage modes — the substrate stays dumb.

---

## 4. The dual architect — heavy Alex + light QuickArchitect (facade)

**Alex = the press.** Ceremony-first, production: interview → analyze → generate → validate (I/O compatibility, schema consistency) → compile → preflight gate. Right for hardened, guaranteed workflows. Wrong for "I want a pipeline in 5 minutes."

**QuickArchitect = the sketch.** The fluid, dynamic generator David wants back — and it already existed as the **v1 Ruby `agent_workflow_architect`**. Framing: a lightweight architect in its own right, but **probably just a facade over Alex** (emits a runnable workflow immediately; "harden" = hand the same artifact to Alex for schemas + compile). Fluidity preserved as a *mode*, not a separate stack.

**Verified v1 pipeline** (David recalled "5 steps / 2 lanes / pivot → CSV"; the code says):
- **7 steps in 2 sections** (not 5).
- Section 1 *Agent Workflow Design*: (1) Workflow Idea → `goal + concept`; (2) Workflow Objective; (3) List Steps; (4) Organize Steps → **"phases"** (not "lanes"; persisted as `sections`); (5) Workflow Name Ideas *(the forgotten step)*.
- Section 2 *Create Agent as Code*: (6) **Specification** = a markdown **table** `Phase | Step | Description | Input Attributes | Output Attributes` (not CSV); (7) **Generate DSL** → **Ruby DSL** (`Agent.create(:x) do … end`) → runs to SQLite + JSON/YAML.
- Chain: `idea → goal+concept → objective → steps_list → step_list_organized(phases) → name_ideas → specification(table) → dsl`.
- v1 store was **flat mutable key-value** (confirms §3).

**The recursive insight:** the v1 architect is *itself a blackboard workflow* — each step's outputs feed later steps' inputs, accumulating in an attribute store. A 2024 prompt literally says *"attributes are collected over time, an output from one step can become an input in future steps."* So: **run QuickArchitect on the POEM/blackboard store, emitting workflows that run on the same substrate.** Meta-workflow and object-workflow share one state model.
*Caveat:* the v1 architect's prompt **source files are gone from disk**; the only surviving copy is a Feb-2025 JSON export (the source of record if resurrecting).

---

## 5. Penny — Prompt Engineer → Agent Engineer

**Now:** Penny owns `input → prompt (hbs logic) → output` + a co-located `.json` (placeholders + outputSchema).

**Proposed:** expand the unit to a full **agent**:

```
input → prompt(hbs) → output            (today)
input → prompt(hbs) → output
      + tools + model + capabilities     (proposed: an Agent unit)
```

This is **exactly the Claude Code subagent/skill frontmatter shape** (`name`, `description`, `tools`, `model` + body + I/O schema). So Penny's output artifact grows from `(.hbs + .json)` into an **agent definition that could literally BE a Claude Code subagent or skill file** — portable as a *skill* (discoverable) or a *subagent* (orchestrator-dispatched), per §2.

**Decision direction (2026-05-22): keep Penny a pure Prompt Engineer; add a NEW Agent Engineer** as a distinct persona (who *may* absorb some of Penny's responsibilities — TBD). The prompt becomes one field of the Agent Engineer's larger capability unit; Penny keeps the prompt+schema craft. Ties to §2 (the capability unit) and §6 (units ship as plugin components).

**Naming-convention snag (must resolve).** The roster uses **[R]ole = [N]ame initial** — **P**rompt→**P**enny, **A**rchitect→**A**lex, **O**rchestrator→**O**scar, **V**alidator→**V**ictor, **F**ield-tester→**F**elix. So **"Agent Engineer" wants an A-name — but A is already Alex (Architect).** Resolve by either (a) **reword the role** to free an initial — *Capability Engineer*→Cara/Carl, *Composer*→Cleo, *Integrator*→Iris/Ian, *Builder*→Bo/Bella; or (b) keep "Agent" and break the one-initial-per-role rule (not preferred).

---

## 6. POEM as an Anthropic plugin (not a repo)

Shift delivery from "clone a repo" to **install a plugin**. The brain already documents this well — `~/dev/ad/brains/anthropic-claude/claude-code/claude-code-plugins.md` (1231 lines, current to v2.1.14: marketplace, manifest, MCP, hooks, skills, agents, commands, SHA pinning). **So this is an *apply* exercise, not a *learn* one.** Freshness check only for anything past v2.1.14.

What "plugin" buys POEM:

- **Bundle as components:** Penny's Agent units → `skills/` + `agents/`; Alex / QuickArchitect → `agents/` (+ `commands/` for invocation); Oscar's role → the conductor skill. All shipped + versioned together.
- **MCP servers:** image-gen (kie), external data sources become **first-class MCP tools** — schema-validated, shared credentials, reusable across agents (the §2 idiom, productised).
- **Hooks:** lifecycle enforcement — e.g. a write-time **validator hook** (the §3 layer-3 guard rails), or a projection-on-stop hook. Hooks are where "data shaped appropriately" can be *enforced by the harness*, not by agent goodwill.
- **Packaging / install:** marketplace + SHA pinning for reproducible team installs. The **`.poem/` folder in a consuming repo** (e.g. dark-factory) = the plugin's project-level data/workspace (workflows, store, projections), analogous to `.mochaccino/`.

---

## 7. dark-factory's role in the migration

- Gets a **`.poem/` folder** — the first place YLO workflows are **rebuilt in POEM** (not ported).
- The YLO experiment folder (`ylo-experiment/`) becomes **frozen reference**; `HANDOVER.md` + Mochaccino designs 04–07 already preserve the learnings.
- This doc + those designs are the bridge: once the `.poem/` rebuild proves out, YLO can be archived.

---

## 8. Cross-system change punchlist

| # | System | Change | Why |
|---|--------|--------|-----|
| 1 | **POEM** | Adopt **append-only log + projections + validators** as the state model (§3) | Kills AWB's mutability-enum complexity; gets audit + race-safety free |
| 2 | **POEM** | Add **QuickArchitect** (v1 7-step formula) as a fluid facade over Alex (§4) | Restores "workflow on demand"; keeps Alex for hardening |
| 3 | **POEM** | Expand **Penny → Agent Engineer**; unit = prompt + I/O schema + tools + model (§5) | Capability units become portable skills/subagents |
| 4 | **POEM** | **Own the workflow-definition format** (move it back from the AWB boundary) (§1) | Authoring belongs to the authoring layer |
| 5 | **POEM** | **Repackage as an Anthropic plugin** (skills/agents/commands/MCP/hooks) (§6) | Distribution, enforcement via hooks, MCP tools, versioned install |
| 6 | **AWB G3** | **Drop the per-slot `mutability` enum**; express as projection policies + validators (§3) | Same guarantees, simpler substrate, shared with POEM |
| 7 | **AWB G3** | Keep **WomPackage** as the compiled runtime contract; consume POEM-owned definition (§1) | Clean runtime/authoring split |
| 8 | **YLO** | **Freeze + harvest + archive** once `.poem/` rebuild proves out (§7) | It was always a testing ground |
| 9 | **Brain (anthropic)** | Freshness-check `claude-code-plugins.md` past v2.1.14 only (§6) | Coverage already strong — apply, don't rewrite |

---

## 9. Open questions

1. **Agent Engineer naming:** decided to keep Penny pure + add a new Agent Engineer (§5) — but **what is it named?** [R]=[N] convention makes "Agent" (A) collide with Alex/Architect (A). Reword the role (Capability/Composer/Integrator/Builder) or break the rule? *And* which of Penny's responsibilities (if any) move to it?
2. **Projection ownership:** who declares fold policy per key — Penny (prompt/output level) or Alex (workflow level)? Likely split, mirroring schema ownership (Penny = prompt schema, Alex = workflow schema).
3. **QuickArchitect output:** does it emit POEM YAML directly, or a lighter runnable form that Alex later upgrades? (Facade boundary.)
4. **Validator placement:** write-time guard rails as a **plugin hook**, a runtime check, or a compile-time check?
5. **MCP vs skill for kie/image-gen:** ship as an MCP server (first-class tool) or keep as a Bash-shelling skill? (MCP if reused across agents.)
6. **`.poem/` layout:** mirror `.mochaccino/`'s workspace conventions (data/ + governance + manifest)?

---

## 10. Provenance / sources

- **YLO:** `ylo-experiment/HANDOVER.md`; `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md`; `.claude/skills/{conductor,store,image-gen}/SKILL.md`; the four workflows `ylo-experiment/workflow-0{1..4}-*.json`.
- **POEM:** `~/dev/ad/poem-os/poem/`; client install `~/dev/clients/supportsignal/prompt.supportsignal.com.au/` (`tools/poem-executor/{src/lib/data-store.js,runtime.js,docs/compiler-requirements.md,docs/runner-requirements.md}`, `poem/workflows/new-incident/new-incident.yaml`, agents `.claude/commands/poem/agents/{alex,penny,oscar,victor}.md`).
- **AWB Gen 3:** `~/dev/ad/apps/awb/` — `packages/state/src/types/{attribute-value,run-state}.ts` (Named-Value Model), `packages/wom/src/types/wom-package.ts` (`WomStateContract`/`WomStateSlot`), `packages/compiler/src/pipeline/`, `CONTEXT.md`, `examples/gen3/`.
- **AWB Gen 1 (Ruby):** `~/dev/ad/agent-workflow-builder/ad-agent_architecture/` — `spec/usecases/agent_engineering/agent_workflow_architect.rbx`, `lib/ad/agent_architecture/{dsl,database}/`; frozen prompt text in `gpt-agents/src/content/gpt-workflows/agent-workflow-architect.json`.
- **Anthropic primitives:** `~/dev/ad/brains/anthropic-claude/claude-code/{claude-code-subagents.md,claude-code-mechanisms.md,claude-code-plugins.md}`, `.../skills/{skill-discovery-mechanisms.md,skill-architecture.md,creating-custom-skills.md}`, `.../agent-sdk/sdk-vs-skills-workflow-choice.md`.
- **Working example (image-gen idiom):** `~/dev/ad/appydave-plugins/appydave/skills/appydave-thumbnail/` (SKILL.md + scripts/generate_thumbnails.py).
- **Visual companions:** Mochaccino designs `04` (pattern), `05` (probes), `06` (YLO vs POEM vs supportsignal), `07` (the four workflow flows) at `http://localhost:7420/designs/`.
