# Insights — Dark Factory Catalog Audit Log

**Purpose**: Append-only audit log of atomic craft bits surfaced while reconning and discovering across the 13-repo cluster. Smaller than a prompt pattern, sharper than a paraphrase — bits worth re-reading when writing your own skills.

**For Agents**: Append entries here whenever recon or discover surfaces something worth keeping (see "Insights Capture" in `capability-recon.md` and `capability-discover.md`). Use the entry format below. Never overwrite or reorder — append-only.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Entry format

```
## YYYY-MM-DD — <short headline>
**Type**: description-craft | table-craft | hook-craft | naming | phrase | contrast | reframing | rationale | other
**Found in**: <repo>/<relative-path> (cite the recon or discover artifact that surfaced it)
**The bit**: (verbatim quote or close paraphrase)
**Why it matters**: 1-2 lines on what this teaches — would change how you'd write your own skill
**Pattern (if any)**: <pattern-id from prompt-pattern-vocabulary.md or "none">
**Tags**: [optional, free-form]
```

---

## Seed entries (from Phase 1 recon, 2026-05-16)

## 2026-05-16 — Description-as-trigger vs description-as-summary

**Type**: contrast
**Found in**: superpowers/.claude/skills/writing-skills/ (see `recon/superpowers.md`)
**The bit**:
- Bad: *"Workflow for writing skills"*
- Good: *"Use when user is about to write code without tests"*

**Why it matters**: The `description` YAML field is what enters context at session start under lazy loading. A *summary* tells the agent "what the skill does" and lets it decide it can skip the body. A *trigger* tells the agent "fire when condition X is met" — forces activation when the situation matches, without revealing the workflow first. David surfaced this 2026-05-16 as a foundational distinction.
**Pattern**: `capability-description`, `discovery`
**Tags**: lazy-loading, yaml

---

## 2026-05-16 — Only metadata at session start, body on activation

**Type**: rationale
**Found in**: agent-skills-osmani (see `recon/agent-skills-osmani.md`)
**The bit**: *"Only `name` + `description` hit context at session start; full body loads on demand."*

**Why it matters**: This is the *engineering* reason for keeping descriptions trigger-only. Not aesthetic — every byte in the description is paid at every session boot; the body is free until activation. Optimize descriptions for routing decisions; pay nothing until the routing decides to fire. Justifies the rule against workflow summaries in descriptions.
**Pattern**: `progressive-disclosure`, `capability-description`
**Tags**: token-cost, lazy-loading

---

## 2026-05-16 — Subagents are about what is NOT in their context

**Type**: reframing
**Found in**: superpowers/.claude/skills/subagent-driven-development/ (see `recon/superpowers.md`)
**The bit**: Subagent design is usually framed as "give the agent the right tools and context." Superpowers flips this: the subagent's value comes from what's *deliberately excluded* — an implementer subagent gets the task text and nothing else (no plan file, no sibling task context), so it can't drift.

**Why it matters**: Reframes context engineering from "what do I need to include?" to "what do I need to exclude to keep the agent focused?" The exclusion list is part of the architecture — a design constraint, not an oversight.
**Pattern**: `agentic-efficiency`, `deliberate-context-exclusion`
**Tags**: subagent-design, context-engineering

---

## 2026-05-16 — Auto-trigger via phrase detection inside the body

**Type**: hook-craft
**Found in**: compound-engineering/plugins/compound-engineering/skills/ce-compound/ (see `recon/compound-engineering.md`)
**The bit**: Skill auto-invokes on phrases like *"that worked"*, *"it's fixed"*, *"fixed it"* detected inside the agent's *body* — not just from the YAML description.

**Why it matters**: Most skills declare their triggers only in YAML. ce-compound treats the body itself as a trigger surface — keyword detection happens after activation, deciding what to do *next*. Useful when triggers are *conditional on prior conversation*, not on a single user prompt. A second-tier discovery mechanism beneath the YAML.
**Pattern**: `discovery` (edge case)
**Tags**: auto-invoke, phrase-detection

---

## 2026-05-16 — Pre-emptive rebuttal is the load-bearing feature

**Type**: rationale
**Found in**: agent-skills-osmani (see `recon/agent-skills-osmani.md`)
**The bit**: Anti-rationalization tables aren't documentation — they're *prompt engineering embedded before the agent forms the excuse*. Addy Osmani calls this the load-bearing feature that makes skills constraining rather than advisory.

**Why it matters**: A skill that *describes* a discipline (TDD, verification) leaves the door open to skipping it. A skill that *names the excuses in advance* closes the door — the agent can't rationalize a path the skill has already named as wrong. The table is read BEFORE the agent reasons about whether to follow the rule.
**Pattern**: `anti-rationalization`
**Tags**: constraint-design, prompt-defense

---

## 2026-05-16 — Phase-labeled dirs are SDLC-stage metadata, not just organization

**Type**: rationale
**Found in**: bmad-method/src/bmm-skills/ (discover run, bmad-method.md recon)
**The bit**: `1-analysis/`, `2-plan-workflows/`, `3-solutioning/`, `4-implementation/` — the numeric prefix is machine-readable lifecycle sequencing baked into the file system. Every skill in `2-plan-workflows/` is unambiguously a planning-stage artifact; no per-file tag is needed.

**Why it matters**: Most repos scatter stage hints in skill descriptions or frontmatter. BMAD enforces stage as a directory-level constraint. Any downstream tool (discovery, filtering, display) can derive SDLC stage with a path substring match — no parsing, no ML. Structural metadata is cheaper and more reliable than semantic metadata. Worth copying in any SDK that has a natural phase ordering.
**Pattern**: `system-comprehension`
**Tags**: sdlc-stage, directory-structure, metadata-by-structure

---

## 2026-05-16 — customize.toml is the schema; sparse TOML is the override

**Type**: rationale
**Found in**: bmad-method/src/bmm-skills/*/customize.toml (discover run)
**The bit**: Each skill ships a `customize.toml` marked "DO NOT EDIT — this is the schema, not the target." The real overrides go in `_bmad/custom/{skill-name}.toml`. A resolver merges by shape at activation time.

**Why it matters**: This separates "what can be customized" (schema, versioned with the skill) from "what this team wants" (override, team-local). Skill upgrades never clobber team config because they touch different files. The resolver pattern is also portable — any skill framework can adopt it. Compare to monolithic SKILL.md editing: that creates a fork-on-upgrade trap.
**Pattern**: `recipe`
**Tags**: customization, upgrade-safe, schema-vs-instance

---

## 2026-05-16 — bmad-party-mode: one skill that activates all agents as a panel

**Type**: hook-craft
**Found in**: bmad-method/src/core-skills/bmad-party-mode/SKILL.md (discover run)
**The bit**: `bmad-party-mode` convenes multiple agent personas simultaneously in a single session — each agent responds in turn to the same prompt, simulating a "war room" dynamic.

**Why it matters**: Most multi-agent designs use separate processes or handoffs. Party mode is a prompt-only approximation of the same thing: one context, multiple persona voices, zero infrastructure. Useful for rapid ideation when full orchestration overhead is unjustified. Demonstrates that `orchestration` cluster artifacts don't always require runtime machinery — a crafted prompt structure can substitute.
**Pattern**: `orchestration-topology`
**Tags**: multi-agent, party-mode, prompt-only-orchestration

---

## 2026-05-16 — preamble-tier as a token-budget dial

**Type**: rationale
**Found in**: gstack — every `SKILL.md.tmpl` (discover run, gstack recon)
**The bit**: Every gstack skill declares `preamble-tier: 1-4` in frontmatter. Tier 1 is the cheapest preamble (minimal cross-cutting blocks injected); tier 4 is the most expensive (all preamble blocks, including full GBrain context load, branch detection, plan audit, review dashboard). The tier is resolved at compile time by the preamble generator scripts under `scripts/resolvers/preamble/`.

**Why it matters**: Most skill systems treat cross-cutting concerns (environment checks, safety warnings, context loading) as all-or-nothing. gstack quantizes this into an integer dial — a quick utility skill pays tier-1 cost; a full ship pipeline pays tier-4 cost. The same resolver infrastructure backs all tiers, so adding a new preamble block is one file, not 49 edits. This is a concrete implementation of `agentic-efficiency` at the compile layer rather than the runtime layer.
**Pattern**: `agentic-efficiency`, `multi-harness-compile`
**Tags**: token-budget, preamble, compile-time-optimization

---

## 2026-05-16 — Single `.tmpl` source compiles to 11 target hosts

**Type**: rationale
**Found in**: gstack — `hosts/*.ts` + `.tmpl` pipeline (discover run, gstack recon)
**The bit**: Each `SKILL.md.tmpl` is the single source of truth. Running `gen-skill-docs --host all` expands the same source through 11 host adapters (`claude.ts`, `codex.ts`, `gbrain.ts`, `cursor.ts`, `kiro.ts`, `hermes.ts`, …), each suppressing or transforming `{{PLACEHOLDER}}` tokens that don't apply to that agent. The committed `SKILL.md` starts with `<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->`.

**Why it matters**: Eliminates the fork-per-harness trap. Any improvement to the `review` skill propagates to all 11 hosts on next `gen-skill-docs` run. The auto-generated comment is an explicit merge-conflict guard — anyone who edits the `.md` directly creates a divergence signal. The pattern is structurally identical to `.js` → `.min.js` in web builds; treating the `.md` as a build artifact (not source) is the cognitive shift.
**Pattern**: `multi-harness-compile`
**Tags**: multi-host, compile-pipeline, single-source-of-truth

---

## 2026-05-16 — gbrain: block as embedded mini-DSL for memory queries

**Type**: hook-craft
**Found in**: gstack — `design-consultation/SKILL.md.tmpl`, `plan-ceo-review/SKILL.md.tmpl`, `investigate/SKILL.md.tmpl`, `retro/SKILL.md.tmpl` (discover run)
**The bit**: Six gstack skills include a `gbrain:` YAML block in frontmatter declaring structured memory queries: `id`, `kind` (list | filesystem), `filter`, `sort`, `limit`, `render_as`. At compile time the `{{GBRAIN_CONTEXT_LOAD}}` token expands these declarations into the preamble. The skill body is memory-aware without any runtime glue code.

**Why it matters**: Most memory-aware skills either hardcode retrieval calls in the body or require a separate memory agent. gstack externalizes the memory query *schema* into frontmatter — declarative, versionable, host-overridable. The `{{GBRAIN_CONTEXT_LOAD}}` / `{{GBRAIN_SAVE_RESULTS}}` token pair makes memory a compile-time concern. Worth adopting whenever memory queries are predictable and skill authors shouldn't need to know the retrieval implementation.
**Pattern**: `multi-harness-compile`, `preparation`
**Tags**: gbrain, memory-dsl, declarative-retrieval

---

## 2026-05-16 — `kw:confidence` as non-destructive interrupt with explicit re-anchor

**Type**: reframing
**Found in**: compound-knowledge/plugins/compound-knowledge/skills/kw-confidence/SKILL.md (see `recon/compound-knowledge.md`)
**The bit**: *"Non-destructive interrupt. If invoked mid-workflow, resume exactly where you left off after. Don't restart the parent workflow... Resuming `/kw:work` at Task 3."*

**Why it matters**: Most skill orchestration treats confidence checks as a sequential gate — a step you pass before continuing. kw:confidence reframes it as a callable utility with an explicit re-anchor protocol: the skill names the interrupted state, resolves the gap, then resumes by name. The re-anchor phrase is load-bearing (not UX polish) — it's how the parent workflow recovers without losing position. Any skill designed as an interrupt needs an explicit resume contract, not just an exit.
**Pattern**: `knowledge-folder-as-bus`
**Tags**: interrupt-design, workflow-reentry, non-destructive

---

## 2026-05-16 — Write-authority concentrated in one orchestrator enables safe merging

**Type**: rationale
**Found in**: compound-knowledge/plugins/compound-knowledge/skills/kw-compound/SKILL.md + agents/ (see `recon/compound-knowledge.md`)
**The bit**: All five agents end with "Return text only. Never write or delete files." Only the orchestrating skill writes. This appears as a `<critical_requirement>` block in kw:compound: *"Agents return TEXT only. They must NOT write or delete files. Only the orchestrating compound skill writes files — both new learnings and updates to stale entries."*

**Why it matters**: File-write authority concentrated in one orchestrator is not just a safety guardrail — it's what makes duplicate detection, staleness resolution, and P1/P2/P3 merging possible before anything hits disk. Agents that can write independently create race conditions and silent overwrites in the shared knowledge folder. The `<critical_requirement>` tag signals that this is architecture, not etiquette.
**Pattern**: `knowledge-folder-as-bus`, `reviewer-agent-separation`
**Tags**: write-authority, orchestration-safety, agent-separation

---

## 2026-05-16 — Pre-greeting project scan as cheap system-comprehension

**Type**: hook-craft
**Found in**: poem/agents/alex.md — activation-instructions Step 4 (discover run, poem.jsonl)
**The bit**: Alex's activation Step 4 scans `poem/prompts/`, `poem/schemas/`, and `poem/workflows/` to build an inventory of available prompts and their I/O contracts *before* greeting the user. Penny has no equivalent step — she loads principles and greets immediately.

**Why it matters**: The scan costs almost nothing (directory reads) but arms Alex with project-specific context the moment conversation starts — enabling "I see you have prompts X, Y, Z" instead of "what do you have?" Generalizes cleanly: any design/orchestration agent whose options are bounded by workspace state should scan-then-greet, not greet-then-discover. The boot scan is lightweight `system-comprehension` embedded as a named activation step, not a separate pre-command.
**Pattern**: `system-comprehension`, `agent-handshake`
**Tags**: boot-scan, activation-sequence, project-inventory

---

## 2026-05-16 — Iron Law + "violating the letter is violating the spirit"

**Type**: phrase
**Found in**: superpowers/skills/test-driven-development/, superpowers/skills/systematic-debugging/, superpowers/skills/verification-before-completion/ (Phase 2 catalog:discover)
**The bit**: Every discipline skill opens with an Iron Law in a fenced code block (`NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`) followed immediately by: *"Violating the letter of the rules is violating the spirit of the rules."* This exact phrase appears verbatim across three skills.
**Why it matters**: Pre-empts the most sophisticated agent escape route — "I'm following the spirit, just not the ritual." Naming it as a violation before the agent forms the thought closes the loophole. The code block gives visual weight signalling hard rule, not guideline.
**Pattern**: `anti-rationalization`
**Tags**: iron-law, spirit-vs-letter, discipline-skills

---

## 2026-05-16 — Description-as-trigger is empirically discovered, not a style preference

**Type**: rationale
**Found in**: superpowers/skills/writing-skills/ CSO section (Phase 2 catalog:discover)
**The bit**: *"When descriptions summarised workflow, agents performed one review instead of two because they treated the description as the skill body and skipped reading the file."* Changing from `"code review between tasks"` to `"Use when executing implementation plans with independent tasks"` (trigger only) fixed the failure.
**Why it matters**: The rule has production-test backing — documented as a real failure mode, not design intuition. Makes the `capability-description` constraint easy to defend when writing or reviewing skills: the description IS the agent's mental model; a workflow summary makes the body redundant, so the agent skips it.
**Pattern**: `capability-description`, `discovery`
**Tags**: description-field, lazy-loading, empirical, cso

---

## 2026-05-16 — `<HARD-GATE>` as a named structural primitive, not prose

**Type**: naming
**Found in**: superpowers/skills/brainstorming/, superpowers/skills/subagent-driven-development/ (Phase 2 catalog:discover)
**The bit**: `<HARD-GATE>` is an XML-style tag in the skill body declaring which successors are forbidden: *"Do NOT invoke frontend-design, mcp-builder, or any other implementation skill. The ONLY skill you invoke after brainstorming is writing-plans."* Terminal states and forbidden successors are explicit, not inferred.
**Why it matters**: Naming a constraint `<HARD-GATE>` elevates it from prose advisory to structural element — the tag format signals machine-readable boundary. Declaring all forbidden successors by name closes every lateral escape route. Contrast with "don't implement yet" (agent infers scope) vs. `<HARD-GATE>` + named exclusions (agent has no inference to do).
**Pattern**: `hard-gate-state-machine`
**Tags**: state-machine, forbidden-successors, structural-naming

---

## 2026-05-16 — Command layer as thin orchestrator, not skill (agent-skills-osmani discover)

**Type**: contrast
**Found in**: agent-skills-osmani/.claude/commands/ (Phase 2 catalog:discover)
**The bit**: Every command is ~10 lines of "invoke skill X + skill Y, then do Z." The command holds no workflow logic itself — it is purely a routing label that wires named skills together. The skill is the design artifact; the command is the activation alias.

**Why it matters**: Separating orchestration from workflow means you can evolve a skill without touching its commands, and reroute a command to a new skill without rewriting workflow. Commands document intent; skills document process. Don't put process in commands — this keeps the composition layer thin and independently replaceable.
**Pattern**: `orchestration-topology`, `capability-description`
**Tags**: command-design, separation-of-concerns, thin-orchestrator

---

## 2026-05-16 — /ship as the only endorsed multi-persona fan-out (agent-skills-osmani discover)

**Type**: rationale
**Found in**: agent-skills-osmani/.claude/commands/ship.md + CONTEXT.md (Phase 2 catalog:discover)
**The bit**: CONTEXT.md names `/ship` as "the sole endorsed multi-persona pattern" — three specialists (code-reviewer, security-auditor, test-engineer) fire in parallel, no shared state, then merge. Every other command is single-persona.

**Why it matters**: Endorsing exactly one fan-out pattern prevents ad-hoc multi-agent sprawl. Other commands are predictably single-track. Parallel is opt-in, not default, and the gate is explicit endorsement in CONTEXT.md — naming it prevents scope creep into "what if we also fan out /review?" The exception proves the rule.
**Pattern**: `orchestration-topology`
**Tags**: fan-out, multi-agent, design-constraint, endorsed-pattern

---

## 2026-05-16 — Red Flags + Verification as two-layer exit criteria (agent-skills-osmani discover)

**Type**: table-craft
**Found in**: agent-skills-osmani/skills/* (Phase 2 catalog:discover — consistent across all 23 skills)
**The bit**: Every SKILL.md ends with `## Red Flags` (observable signals that a step is being skipped or done badly) and `## Verification` (checkbox list the agent must satisfy before proceeding). Two separate sections, both at every skill boundary.

**Why it matters**: Red Flags detect drift while work is in progress; Verification confirms completion before advancing. These are different checks at different moments — collapsing them into one list loses the distinction. "Observable signals" (Red Flags) are concrete enough to fire on without human judgment. The two-layer pattern is worth copying in any skill with quality requirements where "looks done" is not sufficient evidence of done.
**Pattern**: `anti-rationalization`
**Tags**: exit-criteria, verification-gates, red-flags, two-layer

---

## 2026-05-16 — "Prompt Defense Baseline" as universal agent preamble in ECC

**Type**: hook-craft
**Found in**: everything-claude-code: all 60 `agents/*.md` files (Phase 2 catalog:discover)
**The bit**: Every one of ECC's 60 agents opens with an identical six-bullet "Prompt Defense Baseline" block before any role-specific instructions. The block covers: identity override, credential leakage, untrusted content handling, harmful output, unicode/homoglyph tricks, and session boundary preservation.
**Why it matters**: Injection resistance is treated as a *layer* (always present, always first), not as a per-agent judgment call. Putting defense before capability means the model's role-specific context can never push the safety block out of the initial attention window. The six-bullet taxonomy is also a reusable checklist — copy it verbatim into any agent you write.
**Pattern**: `injection-resistance`
**Tags**: agent-safety, defense-in-depth, universal-preamble, ecc

## 2026-05-16 — "Use PROACTIVELY" as a trigger-intensity modifier in agent descriptions

**Type**: description-craft
**Found in**: everything-claude-code: `agents/architect.md`, `agents/a11y-architect.md`, `agents/security-reviewer.md` and ~15 others (Phase 2 catalog:discover)
**The bit**: Agent descriptions routinely include "Use PROACTIVELY when X" (uppercase). This is not decoration — it overrides the default wait-for-explicit-mention routing, making the agent self-nominate when conditions match even if the user didn't name it.
**Why it matters**: The capitalized word is a routing instruction embedded in the description. It's the description-as-routing-program pattern applied to *intensity*, not just trigger conditions. If you want a specialist agent to jump in without being called, "Use PROACTIVELY when…" is the canonical phrasing from ECC's own corpus.
**Pattern**: `discovery`, `capability-description`
**Tags**: routing, trigger-intensity, proactive-activation, ecc

## 2026-05-16 — Commands as shims: catalog the deprecation intent, not just the artifact

**Type**: rationale
**Found in**: everything-claude-code: `AGENTS.md`, SKILL-PLACEMENT-POLICY, `commands/*.md` (75 files; Phase 2 catalog:discover)
**The bit**: ECC explicitly demoted `commands/` to "legacy slash-entry compatibility surface." All 75 commands exist for backward compatibility only; new work lands in `skills/`. Commands are described as "being phased out" in both AGENTS.md and the skill placement policy.
**Why it matters**: A catalog that treats commands as equal citizens misrepresents ECC's architecture. Commands are routing shims — the real capability lives in the skill. When comparing implementations across repos, the commands table overstates ECC's command surface. Tag commands `pending-deprecation` in the next `catalog:tag` pass.
**Pattern**: `discovery`
**Tags**: deprecation, architecture-intent, commands-vs-skills, ecc

---

## 2026-05-16 — "Checklists are unit tests for English" — spec quality as first-class gate

**Type**: reframing
**Found in**: spec-kit/templates/commands/checklist.md (Phase 2 catalog:discover)
**The bit**: *"Checklists are UNIT TESTS FOR REQUIREMENTS WRITING — they validate the quality, clarity, and completeness of requirements in a given domain."* The command names three explicit NOT-examples (verify button clicks, test error handling, confirm API returns 200) before stating what a checklist IS. The metaphor is the load-bearing part: if your spec is code written in English, the checklist is its unit test suite.

**Why it matters**: Most teams run checklists as pre-merge code gates. Spec-kit repositions them as pre-implementation spec gates — catching ambiguity before a line of code is written. The NOT-examples are anti-rationalization: listing what a checklist must never do means the agent can't drift toward "just verify the implementation while I'm here." Worth stealing the framing ("unit tests for requirements") for any spec-writing skill.
**Pattern**: `anti-rationalization`
**Tags**: spec-writing, checklist-design, requirements-quality, unit-test-metaphor

---

## 2026-05-16 — analyze as a read-only mandatory gate encodes "spec serves code" inversion

**Type**: rationale
**Found in**: spec-kit/templates/commands/analyze.md + recon/spec-kit.md (Phase 2 catalog:discover)
**The bit**: `analyze` is declared *non-destructive* and its template uses MUST vocabulary: "The `analyze` command is a read-only cross-artifact consistency gate that must pass before `implement` runs." From recon: *"The MUST/SHOULD vocabulary in command templates is behavioral constraint on the LLM, not documentation."*

**Why it matters**: Separating read-only-gate from implementation-phase encodes the "code serves specifications" inversion structurally — the agent cannot implement without a consistency check, and the check cannot modify anything. Most pipeline designs blur gates and transforms in the same step, allowing gate logic to quietly get skipped when the transform succeeds. Spec-kit's separation makes the gate independently auditable and independently required.
**Pattern**: `anti-rationalization`
**Tags**: pipeline-gate, read-only, mandatory, spec-as-truth

---

## 2026-05-16 — Orchestrator descriptions name all subagents, creating free bidirectional routing

**Type**: description-craft
**Found in**: appydave-plugins/appydave/skills/doc-review/SKILL.md, delivery-review/SKILL.md (discover run, appydave-plugins.jsonl)
**The bit**: `"Launches doc-review:coherence, doc-review:gaps, doc-review:completeness, doc-review:topology, doc-review:prose, and doc-review:crossref as background agents, then triages and synthesizes their findings."`

**Why it matters**: The orchestrator's YAML description doubles as a capability map — every sub-agent name is explicitly listed. A keyword match on any sub-agent name routes to the orchestrator, not just to the leaf skill. Bidirectional routing at zero extra cost: user says "run doc-review:prose" → orchestrator fires. Works across 6 fan-out skills in this repo.
**Pattern**: `orchestration-topology`, `capability-description`
**Tags**: orchestrator, fan-out, description-as-capability-map

---

## 2026-05-16 — Script-bearing skills co-deploy code and instructions as one versioned unit

**Type**: rationale
**Found in**: appydave-plugins/appydave/skills/omi-fetch/scripts/, lexi/scripts/ (discover run, appydave-plugins.jsonl)
**The bit**: 14 of 96 skills embed Python/shell/JS scripts inside the skill directory. SKILL.md invokes them via versioned cache glob: `bash "$(ls -d ~/.claude/plugins/cache/.../skills/omi-fetch/scripts | sort -V | tail -1)/omi_sync.sh"`.

**Why it matters**: The glob-to-latest pattern means version upgrades auto-resolve with no edit to the invocation string. Code and instructions version together, eliminating external-scripts-repo drift. Any skill that drives tooling should bundle its scripts — separate repos create version-lag traps.
**Pattern**: `progressive-disclosure`
**Tags**: script-bearing-skill, self-contained, versioned-cache

---

## 2026-05-16 — 18-cluster vocabulary covered all 114 active appydave-plugins artifacts with zero new proposals

**Type**: rationale
**Found in**: appydave-plugins.jsonl (discover run, 2026-05-16)
**The bit**: Cluster assignment on 96 skills + 18 commands produced zero cluster-vocabulary-additions proposals. The only friction: 11 body-only commands had no YAML description — reading first 25 lines of each resolved all assignments.

**Why it matters**: Confirms the 18-cluster vocabulary is fit-for-purpose for a personal-assistant skill corpus. Actionable heuristic: body-only commands (no YAML description) require one body read to assign clusters — not a flaw, but a shape to document. Consider adding `description` to all commands in a future pass.
**Pattern**: `discovery`
**Tags**: cluster-coverage, vocabulary-fitness, commands-without-frontmatter

---

## 2026-05-16 — Three composable knobs cover almost all real-world swarm configurations

**Type**: rationale
**Found in**: ruflo/.agents/skills/hive-mind-advanced/SKILL.md, ruflo/v3/implementation/ (Phase 2 catalog:discover, ruflo.jsonl)
**The bit**: Ruflo separates three independent swarm dimensions: topology (hierarchical, mesh, hierarchical-mesh, adaptive), consensus protocol (raft, byzantine, gossip, crdt, quorum), and transport (LocalTransport in-process vs FederationTransport cross-machine Ed25519-signed WebSocket). Anti-drift defaults are `hierarchical + max-agents 8 + raft + specialized strategy`.
**Why it matters**: Most swarm designs expose a single "swarm mode" knob, collapsing all three into one opaque choice. Three-knob decomposition means a team can switch consensus protocol (raft → byzantine for fault tolerance) without changing topology or transport — each axis is independently testable. The anti-drift default communicates the "safe baseline" — the combination with smallest attack surface for configuration drift.
**Pattern**: `orchestration-topology`
**Tags**: swarm-topology, three-knob, consensus, composable-orchestration

---

## 2026-05-16 — MCP tools as coordinator verbs only — Claude Code tools do the actual work

**Type**: reframing
**Found in**: ruflo/AGENTS.md + ruflo/plugins/ruflo-swarm/skills/swarm-init/SKILL.md (Phase 2 catalog:discover)
**The bit**: 305 MCP tools are coordinator verbs only — `swarm_init`, `agent_spawn`, `hooks_route`, `memory_store`. They never write files or execute code. Claude Code's native `Task`, `Edit`, `Write`, `Bash` tools do that. AGENTS.md enforces the "same message" rule: `swarm_init + Task×N` must appear in one Claude Code response. Violation is documented as the #1 failure mode.
**Why it matters**: Most multi-agent frameworks blur the line between orchestration and execution. Ruflo draws it sharply: MCP = coordination plane, Claude Code tools = execution plane. This keeps the orchestrator without elevated file-system privileges. The "same message" rule is a consistency guarantee — the swarm either starts atomically or not at all. Any SDK adding an orchestration layer should decide this split explicitly, not by accident.
**Pattern**: `orchestration-topology`, `reviewer-agent-separation`
**Tags**: mcp-coordination, execution-plane, same-message-rule, atomic-swarm-start

---

## 2026-05-16 — Pre-task hook fires before the user sees a response — routing before reasoning

**Type**: hook-craft
**Found in**: ruflo/plugins/ruflo-core/hooks/hooks.json — PreToolUse hook config (Phase 2 catalog:discover)
**The bit**: The `pre-task` hook fires on every new prompt and runs a semantic search of the `patterns` namespace before the agent forms any intent. If similar past work is found, the pattern is injected into the preamble. The user never sees a round-trip — routing happens in the hook, not in the first agent turn.
**Why it matters**: Most skill systems route after the user prompt is processed. Ruflo hooks the pre-task lifecycle to search memory *before* reasoning begins, pre-loading the agent's context with relevant priors. Implication: the hook layer, not the skill description, is the primary routing mechanism at runtime. Skill descriptions handle cold-start discovery; hooks handle warm-path retrieval. These are different problems requiring different solutions.
**Pattern**: `orchestration-topology`, `knowledge-folder-as-bus`
**Tags**: pre-task-hook, semantic-routing, memory-before-reasoning, hook-as-router

---

## 2026-05-16 — gbrain/gstack split: knowledge skills vs thinking skills as explicit repo boundary

**Type**: rationale
**Found in**: gbrain/skills/RESOLVER.md + gbrain/docs/ethos/THIN_HARNESS_FAT_SKILLS.md (Phase 2 catalog:discover, gbrain)
**The bit**: RESOLVER.md has a named "Thinking skills (from GStack)" section that explicitly routes brainstorm/review/debug/investigate to gstack skills: "If GStack is installed, the agent reads them directly. If not, brain-only mode still works." The boundary is not implied — it's a first-class entry in the routing table.
**Why it matters**: Most single-repo skill collections collapse knowledge-management skills and code-thinking skills together. gbrain externalizes this boundary into a two-repo composition contract: gbrain = what you know + who you know; gstack = how to think about code. The degradable fallback ("brain-only mode still works") means the boundary is a composition upgrade, not a hard dependency. Any skill ecosystem with two distinct capability families should consider declaring this split explicitly in the resolver rather than letting it emerge from naming conventions.
**Pattern**: `orchestration-topology`, `discovery`
**Tags**: two-repo-split, knowledge-vs-thinking, graceful-degradation, resolver-as-contract

---

## 2026-05-16 — Machine-readable skill frontmatter as a deployment contract, not just metadata

**Type**: rationale
**Found in**: gbrain/skills/*/SKILL.md — `triggers`, `tools`, `mutating`, `writes_to` fields (Phase 2 catalog:discover, gbrain)
**The bit**: Every gbrain SKILL.md declares: `triggers` (string list — routing signal), `tools` (MCP tools the skill is permitted to call), `mutating` (boolean — does this skill write to the brain?), and `writes_to` (directory allow-list — where it may write). The `skills/manifest.json` (`conformance_version: "1.0.0"`) mirrors this into a machine-readable registry.
**Why it matters**: Most skill frameworks put routing, permissions, and scope in prose — auditable only by humans. gbrain's frontmatter is a deployment contract: an orchestrator can read `mutating: false` and run the skill with read-only credentials; a validator can compare `writes_to` against actual file touches. The manifest makes this contract discoverable without parsing individual skill files. Any skill system that adds execution infrastructure (sandboxing, permission gating, skill-marketplace) will need exactly this structure — gbrain already has it.
**Pattern**: `capability-description`, `recipe`
**Tags**: skill-contract, mutating-flag, writes_to, manifest, machine-readable-permissions

---

## 2026-05-16 — Persona + model tier as a single dispatch unit

**Type**: rationale
**Found in**: compound-engineering/plugins/compound-engineering/agents/ (Phase 2 catalog:discover, compound-engineering)
**The bit**: The `ce-coherence-reviewer` runs on `model: haiku`; `ce-design-lens-reviewer` and `ce-scope-guardian-reviewer` run on `model: sonnet`; most reviewers use `model: inherit`. The model tier is encoded on the agent, not decided by the orchestrator at dispatch time.
**Why it matters**: Putting the model tier on the agent makes the dispatch decision self-documenting — a coherence check (pattern matching) is cheap, a design lens check (product reasoning) earns a bigger model. The orchestrator doesn't need to know which agents are cheap or expensive; each agent declares its own cost posture. This is agentic-efficiency built into the deployment unit, not into the orchestration logic.
**Pattern**: `reviewer-agent-separation`, `agentic-efficiency`
**Tags**: model-tier, agent-economics, dispatch-design

---

## 2026-05-16 — "Agent time is cheap. Tech debt is expensive." as a policy statement, not a suggestion

**Type**: phrase
**Found in**: compound-engineering/plugins/compound-engineering/skills/ce-resolve-pr-feedback/SKILL.md (Phase 2 catalog:discover, compound-engineering)
**The bit**: "Agent time is cheap. Tech debt is expensive. Fix everything valid -- including nitpicks and low-priority items."
**Why it matters**: Most code-review skills hedge: "decide based on effort vs value." This one makes the policy explicit as a one-liner that eliminates the decision entirely. The phrase is doing policy work — the agent doesn't weigh; it just fixes. The narrow exception (when implementing would actively make code *worse*) is then clearly bounded. This is a decision-rule, not guidance.
**Pattern**: `anti-rationalization`
**Tags**: policy-statement, review-posture, phrase-as-decision-rule

---

## 2026-05-16 — Overlap detection before new doc creation as a deduplication gate

**Type**: rationale
**Found in**: compound-engineering/plugins/compound-engineering/skills/ce-compound/SKILL.md (Phase 2 catalog:discover, compound-engineering)
**The bit**: Phase 2 of ce-compound scores existing docs for overlap (High / Moderate / Low) *before* creating a new one. High overlap → update in place. Moderate → note for consolidation. Low → create new. The Python validator (`scripts/validate-frontmatter.py`) runs before any write to ensure parser-safety.
**Why it matters**: Most knowledge-capture systems accumulate without pruning — they grow but never consolidate. The overlap check inverts this: creation is the fallback, update is the preference. Validated writes prevent parser-breaking frontmatter. The result is a knowledge store that stays navigable because every new session actively fights entropy before adding content.
**Pattern**: `dual-track-learning-schema`, `self-improving-agent`, `knowledge-folder-as-bus`
**Tags**: overlap-detection, knowledge-deduplication, entropy-management

---

## 2026-05-16 — Two-file command split as runtime-neutrality mechanism

**Type**: rationale
**Found in**: gsd — `commands/gsd/plan-phase.md` (entry) + `get-shit-done/workflows/plan-phase.md` (body) (Phase 2 catalog:discover, gsd.jsonl)
**The bit**: Every GSD slash command is split across two files: the thin entry in `commands/gsd/` carries YAML frontmatter (name, allowed-tools, argument-hint) and a short `<objective>` block with an `@execution_context` include pointing to the workflow body. The heavyweight procedural logic lives in `get-shit-done/workflows/`. At install time, `bin/install.js` stitches them together per target runtime.
**Why it matters**: Decouples "what is this command?" (YAML registration metadata) from "how does this command execute?" (workflow prose). The workflow body can evolve independently, be tested standalone, and reused across runtimes (Claude Code, VS Code Copilot, SDK) without duplicating frontmatter. The `@include` is not a convenience — it is the compile boundary. Any command system wanting multi-runtime support should separate registration metadata from execution logic.
**Pattern**: none established — candidate pattern ID: `two-file-command-split`
**Tags**: multi-harness, runtime-neutrality, compile-boundary, command-registration

---

## 2026-05-16 — Orchestrator stays deliberately dumb (~30-40% context) to prevent rot

**Type**: rationale
**Found in**: gsd — `commands/gsd/execute-phase.md`, `commands/gsd/plan-phase.md`, recon `gsd.md` standout patterns (Phase 2 catalog:discover, gsd.jsonl)
**The bit**: GSD orchestrators are explicitly designed to use only ~30-40% of their context window. All heavy work delegates to fresh-context subagents that each receive their own 200K (or 1M) window, pre-loaded only with the `.planning/` artifacts they need. The orchestrator's job: call `gsd-tools.cjs init` → parse JSON → spawn agents → collect results → update state. This is explicitly chosen to avoid "context rot" — degradation past 50-70% utilization.
**Why it matters**: Most orchestration patterns treat context exhaustion as a hardware limit to engineer around. GSD makes deliberate context budget a first-class design constraint at the *orchestrator level* — the orchestrator never accumulates intelligence; it manages intelligence distribution. Quantifies the `deliberate-context-exclusion` pattern as a percentage target, not just a principle.
**Pattern**: `deliberate-context-exclusion`, `orchestration-topology`
**Tags**: context-rot, context-budget, orchestrator-design, subagent-isolation

---

## 2026-05-16 — Model profile matrix: role-to-model resolved at init, not hardcoded in agent

**Type**: rationale
**Found in**: gsd — `get-shit-done/references/model-profiles.md`, recon `gsd.md` standout patterns (Phase 2 catalog:discover, gsd.jsonl)
**The bit**: GSD ships a `model-profiles.md` table mapping each agent role to a model per quality tier (quality, balanced, budget, inherit). Planners always get Opus on quality/balanced; executors get Sonnet on balanced; verifiers get Haiku on budget. `gsd-tools.cjs` resolves the profile at init time and injects the model name into each subagent spawn — no role is hardcoded to a model at rest in the agent file.
**Why it matters**: Separates model policy from agent definition. The same `gsd-planner.md` runs Opus in one team's workflow and Haiku in another's cost-optimized setup, with no fork. Cost vs. quality tradeoff becomes a configuration decision, not a codebase change. Concrete implementation of `agentic-efficiency` cost dimension at the fleet level.
**Pattern**: `agentic-efficiency`
**Tags**: model-selection, cost-profile, role-model-matrix, configuration-vs-code
