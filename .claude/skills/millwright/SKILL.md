---
name: millwright
description: "Use when about to build a Dark Factory capability — or when you catch yourself about to hand-perform a task instead of building reusable machinery. Decides the FORM of machinery (skill / workflow.js / agent-job / improve-existing / combo) and how to build it well. Invoke BEFORE building, and the moment you're tempted to 'just do it' inline. Triggers: 'build machinery', 'what form / should this be a workflow or a skill', 'build a reusable system', 'millwright', 'how do we build this'."
---

# Millwright — the machine-builder

Marshall's build-side sibling. **Marshall routes the work; Millwright builds the machines that do the work.** The Dark Factory's product is **reusable machinery you direct by talking** — not bespoke outputs. Millwright exists to stop the #1 failure: dropping from *factory-builder* to *worker* and hand-performing the task. (Memory: `build-reusable-systems-not-one-offs`.)

## The one rule
**Build the machine, don't perform the task.** Whatever is in front of you (a viz, a doc, an analysis) is the **test payload** — not the deliverable. The deliverable is the **reusable machine** that produces it, and every payload after it.

## Step 1 — Mode guard (always first)
Ask, plainly:
- "Am I about to **build a machine**, or **hand-perform a task**?"
- "What **reusable machine** produces this output repeatably?"
- "Is the spec / usage-pattern I was handed the **blueprint for the machine** — or am I misreading it as a manual checklist to follow once?"
- "Does the machine **already exist**? Then improve or use it — don't rebuild or short-circuit it."

If the honest answer is "I'm about to do the task by hand" → **STOP.** Build or use the machine instead.

## Step 2 — Pick the form (decision matrix)
| If the capability is… | Build it as… |
|---|---|
| a repeatable procedure needing **human judgment / HITL** each run | a **SKILL** (Mochaccino, Marshall) |
| a **deterministic, parallel, mechanical burst** (fan-out, batch, N-vote verify) | a **WORKFLOW.js** |
| a one-shot **dispatched unit** of work, isolated | an **AGENT / Swagger job** via the engine |
| **already exists** but is weak or missing a piece | **IMPROVE existing machinery** — mine real usage → distil → bake in (don't fork) |
| **human-led overall, with mechanical bursts inside** | a **SKILL that wraps WORKFLOW.js** and/or uses an existing engine |

Grounding — *who holds the plan* (vendored workflows spec): Claude turn-by-turn → skill/subagent · the script → workflow · a lead over peers → team. **HITL:** a `workflow.js` run has **no mid-run human gate** — human gates live at **run/job boundaries**, so human-led exploration belongs in the **skill**, never inside the workflow.

## Step 2½ — SPEC first, then pick the builder (Millwright is the gatekeeper)
For any non-trivial capability: **write the requirements/spec BEFORE building, and decouple the spec from the build technique** (David, 2026-06-08). Millwright routes to the right machinery for *each*:

**Pick the SPEC tool** (turn a messy requirement → a clear, testable spec):
| Input | Tool |
|---|---|
| long messy brainstorm → structured PRD | `appydave:spec-writer` |
| need a structured interview → plan + a `/goal` condition | `appydave:goal-plan` |
| autonomous batch project, requirements phase | `ralphy` (Requirements mode) |
| (David's liked external set) | **Osmani Agent Skills** (⚠️ source unverified — `osmani-agent-skills`) |

**Pick the BUILD technique** (Ralphy is ONE of several — don't default to it):
| Target | Build via |
|---|---|
| change to a constellation app (AngelEye/Switchboard/…) | **Ralphy**, in-app (app owns its features) |
| dark-factory's own tool / capability | a **Swagger** through the loop (factory builds its own tools) |
| deterministic parallel/mechanical burst | a **workflow.js** |
| small, design-central | **author directly** (Marshall/Millwright) |

So: requirements-writing is its own machinery, independent of who builds. The gatekeeper picks spec-tool → writes/dispatches the spec → THEN picks the build technique. (A "what machinery exists" registry — skills/workflows/techniques — feeds this; ties to `tool-usage-telemetry-for-self-evolution` + skills-registry.)

## Step 3 — Build it well (per form)
- **Skill** — frontmatter contract: trigger-only `Use when…` description, David's voice, terse. Use `skill-creator`; put depth in `references/`. Mine real usage into `references/usage-patterns.md` (how Mochaccino 4.3.0 was sharpened).
- **Workflow.js** — author per `~/dev/ad/brains/anthropic-claude/claude-code/workflows/` (8 globals; `pipeline` is the default; the orchestrator does NO fs/shell — only `agent()` does I/O; no mid-run human gate).
- **Improve-existing** — mine many real runs → distil the repeatable pattern → **bake into the skill** + version-bump. Don't build new when improving wins.
- **Agent-job** — write a tight queue ticket → `dispatch-swagger.sh` → verify the **artifact** (never trust a "done").
- **Build ON existing engines** — for prose/code → visuals the engine is **Mochaccino** (Peter=data · Shelly=shapes · Mocha=render), and it is **data-first**: prose → schema + JSON BEFORE any view. Feed it data; never hand it a hand-drawn "shape brief."

## Step 4 — Prove + register
- Run the machine once on a real **test payload** → the output is **proof the machine works**, not the deliverable.
- **Register** it (skills index / engine / gallery) so it's discoverable and reusable. A machine nobody can find isn't reusable.

## Anti-patterns (the mistakes Millwright is here to stop)
- Hand-performing the task inline instead of building the machine.
- Reading a spec / usage-pattern as a to-do list instead of the machine's blueprint.
- Reinventing or **short-circuiting an existing engine** (a "shape brief" instead of feeding Mochaccino real data).
- Storing the fix as a passive **memory** when it should be active **machinery** (a skill).
- For visuals: skipping the **data-first gate**.
- Handing David a **question-menu** instead of leading with "my take → go". (Memory: `lead-with-my-take-not-question-menus`.)
