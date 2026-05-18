# Proposal: Prompt-Pattern Awareness in Dark-Factory Catalog

**Purpose**: Add prompt-pattern detection as a first-class concern to the `catalog:recon` and `catalog:discover` capabilities, grounded in David's prompt-patterns brain and what Phase 1 recon actually found.

**For Agents**: This is a proposal document — do NOT apply any changes to SKILL.md or reference files without David's approval. This exists to capture the analysis and specific proposed edits.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16
**Status**: proposed — awaiting David review

---

## 1. Prompt-Patterns Brain Synthesis

David's brain at `~/dev/ad/brains/prompt-patterns/` covers the **architectural layer** of prompt engineering — not prompt craft (few-shot, CoT, elicitation) but how prompts, skills, agents, and tools are *designed as systems*.

### David's working definition

> **Declarative capability signaling** — prompts, agents, tools, and skills that carry metadata about their own purpose, context, and composability, so that LLMs and orchestrators can discover when and how to invoke them.

The core metaphor is **the resume**: every artifact in a well-designed AI system should describe what it can do, when to use it, when NOT to use it, how it composes, and what it needs to operate.

### Taxonomy — the 10 pattern families

| Pattern | One-line definition |
|---------|---------------------|
| **Discovery** | Self-describing capabilities — description IS the routing program. No separate classifier. |
| **Recipe** | Prompts that build application capability, stack-aware, applied to a known tech context. |
| **Compound Recipe** | Multiple recipes with declared dependencies, ordering, idempotency, ownership boundaries. |
| **Capability Description** | WHAT + WHEN + KEYWORDS + NEGATIVE TRIGGERS formula — the "resume" formula. |
| **Progressive Disclosure** | 3-tier load: metadata always, instructions on activation, resources on demand. 98% token reduction. |
| **Migration vs Seed** | Seed = one-time bootstrap; Migration = incremental, idempotent application. |
| **System Comprehension** | Structured prompts that give an agent a working *mental model* of an unfamiliar system before it acts. |
| **Preparation** | Extract + synthesise knowledge from one source; deliver in the form another system can act on immediately. |
| **Agent Handshake** | Structured self-introduction between collaborating agents — identity, role, state, communication protocol. |
| **Self-Improving Agent** | Agents that capture mistakes, accumulate learnings, and promote observations → notes → rules across invocations. |
| **Orchestration Topology** | Parallel Panel / Autonomous Pipeline / Conversational Delegation — plus Coordinator Loop as compound. |
| **Agentic Efficiency** | Three coupled cost dimensions: model tier, context volume, prompt precision. |

### Key architecture insight — two dimensions

The brain distinguishes two layers that practitioners often collapse:

```
Craft Layer (HOW to write a better prompt)
└── Few-shot, CoT, temperature, elicitation, system prompt writing

Architecture Layer (HOW to design prompts as a system — this brain)
└── Self-describing, composable, stack-aware, progressively disclosed building blocks
```

The catalog has been treating artifacts (skills, agents, commands) as the unit. Prompt patterns are a **cross-cutting layer** — they describe HOW those artifacts are architected internally.

### What is well-populated vs. underdeveloped

**Well-populated in the brain:**
- Discovery Pattern — extensively documented with the 3-tier architecture, WHAT+WHEN+KEYWORDS formula, negative capability signaling
- Capability Description — the formula is concrete and battle-tested across David's ecosystem
- Self-Improving Agent — deep treatment including academic grounding (Reflexion, Voyager), promotion ladder, file layouts, failure modes
- Composability — vocabulary/sentence/paragraph metaphor, dependency ordering, conflict resolution, idempotency contract

**Underdeveloped or missing in the brain:**
- **Anti-rationalization patterns** — Osmani and Superpowers both implement them as empirically-derived tables, but the brain has no pattern for this technique
- **Pressure-scenario testing** — Superpowers' test prompts (`.txt` files encoding edge-case bypass attempts) encode a distinct technique: test skill *not-triggering* as well as triggering. No named pattern in the brain.
- **Context-isolation-as-design** — Superpowers' "subagents are about what is NOT in their context" framing is a distinct prompt architecture. Related to Agentic Efficiency (context volume dimension) but not fully captured.
- **Knowledge-folder-as-bus** — compound-knowledge's "folder is the bus" pattern (no daemon, no vector store, just git-tracked markdown + grep) is a composability/persistence architecture not named in the brain.
- **Hard-gate / state-machine composition** — Superpowers' `<HARD-GATE>` + terminal state machine for skill composition is more constrained than what the Compound Recipe pattern covers.

---

## 2. Phase 1 Recon Cross-Reference

Observed prompt-pattern moves mapped to the brain's taxonomy:

| Repo | Observed move | Brain pattern | Classification |
|------|--------------|---------------|----------------|
| **agent-skills-osmani** | Anti-Rationalization tables — "Rationalization \| Reality" two-column table, LLM reads rebuttals *before* forming the excuse | — | **New category candidate: Anti-Rationalization** |
| **agent-skills-osmani** | Description-only startup (lazy load) — only `name` + `description` enter context; full body loads on activation | **Discovery / Progressive Disclosure** | Existing — confirmed in brain |
| **agent-skills-osmani** | Three-layer composition: Command → Persona → Skill with explicit "personas do not invoke personas" rules | **Compound Recipe** | Existing — partial match; the type-exclusion rule is novel |
| **agent-skills-osmani** | Red Flags + Verification checklists as exit-criteria enforcement | — | **New category candidate: Exit-Criteria Enforcement** |
| **superpowers** | Trigger-only descriptions (empirically: summaries caused agents to skip reading the body) | **Capability Description** | Existing — strongest real-world evidence yet seen |
| **superpowers** | Iron Laws + Rationalizations tables — same structure as Osmani but labelled differently | — | **New category candidate: Anti-Rationalization** |
| **superpowers** | Session-start hook injects full skill body as `<EXTREMELY_IMPORTANT>` — bootstrap forces awareness | — | **New category candidate: Bootstrap Injection** |
| **superpowers** | State machine composition with `<HARD-GATE>` and terminal states | **Compound Recipe** | Existing — edge of the pattern; terminal states not covered |
| **superpowers** | TDD applied to skill authoring: RED (baseline rationalisations) → GREEN (minimal SKILL.md) → REFACTOR (re-run, find new rationalisations) | — | **New category candidate: TDD-for-Skills** |
| **superpowers** | Subagents dispatched via context-isolation: implementer never reads plan file intentionally | **Agentic Efficiency (context volume)** | Existing — special case: *deliberate exclusion* not just minimization |
| **superpowers** | Test prompts encoding bypass-attempt scenarios (`skip-formalities.txt`) | — | **New category candidate: Pressure-Scenario Testing** |
| **everything-claude-code** | Instinct-with-confidence-scoring — YAML-fronted learnings with `confidence: 0.3→0.9`, `trigger`, `domain`, `scope` | **Self-Improving Agent** | Existing — most structured implementation seen |
| **everything-claude-code** | `/evolve` + `/promote` as cross-project instinct escalation — promote only when same ID in 2+ projects | **Self-Improving Agent** | Existing — extends the promotion ladder concept |
| **everything-claude-code** | "Prompt Defense Baseline" block at top of every agent — structured injection-resistance rules embedded in frontmatter body | — | **New category candidate: Injection Resistance** |
| **compound-engineering** | Reviewer-agent separation with tiered dispatch and JSON findings schema | **Agent Handshake / Orchestration Topology** | Existing — the output schema contract is novel |
| **compound-engineering** | Learning dual-track schema: bug track vs knowledge track, enforced by YAML schema + Python validator | **Self-Improving Agent** | Existing — adds schema-enforced dual-track output |
| **compound-engineering** | Auto-invoke trigger on phrase detection ("that worked", "it's fixed") inside skill body | **Discovery** | Existing — interesting: trigger embedded in body, not description |
| **compound-knowledge** | Folder-as-bus: `docs/knowledge/` accumulates learnings; no DB, no daemon; plain markdown + grep retrieval | — | **New category candidate: Knowledge-Folder-as-Bus** |
| **compound-knowledge** | `kw:confidence` as non-destructive interrupt that re-anchors after resolution | **Compound Recipe** | Existing — closest is idempotency; the "interrupt + resume" is novel |
| **compound-knowledge** | Work-type auto-detection (5 types × 3 tiers) that shapes output template without asking user | **System Comprehension** | Existing — edge case: self-classification, not system reading |

### New category candidates summary

From the recon cross-reference, 6 distinct patterns appear that have NO named home in the brain:

1. **Anti-Rationalization** — embedding rebuttals before the agent forms the excuse (Osmani + Superpowers)
2. **TDD-for-Skills** — RED/GREEN/REFACTOR applied to skill authoring rather than code (Superpowers)
3. **Pressure-Scenario Testing** — test files encoding bypass-attempt phrases to verify skill-not-triggering (Superpowers)
4. **Bootstrap Injection** — session-start hook force-loads a skill body as EXTREMELY_IMPORTANT context (Superpowers)
5. **Knowledge-Folder-as-Bus** — git-tracked markdown folder as persistence substrate; no daemon, no vector store (compound-knowledge)
6. **Injection Resistance** — structured prompt-defense baseline blocks embedded in agent frontmatter body (ECC)

Plus 3 extensions of existing patterns:
- **Hard-gate state machine** (extends Compound Recipe)
- **Deliberate context exclusion** (extends Agentic Efficiency)
- **Cross-project instinct promotion** (extends Self-Improving Agent)

---

## 3. Specific Edits Proposed

### 3a. SKILL.md — artifact type vs. cross-cutting facet?

**The question**: Should "prompt pattern" become a *first-class artifact type* (alongside skill/agent/command) or a *cross-cutting facet* on existing artifacts (a field that says "this artifact implements these patterns")?

**Analysis:**

| Option | Pros | Cons |
|--------|------|------|
| **First-class artifact type** (`artifact_type: "prompt-pattern"`) | Discoverable in the same sweep; shows up in SDLC tagging; clean schema evolution | Prompt patterns aren't discrete files — they're techniques embedded *inside* skill files. Would require creating synthetic entries that don't correspond to real files. |
| **Cross-cutting facet** (`prompt_patterns_used: ["anti-rationalization", "progressive-disclosure"]`) | Accurately describes reality — a single SKILL.md can implement 3 patterns simultaneously. No synthetic entries. Composable with SDLC tags. | Not surfaced by `artifact_type` filtering alone; requires a separate query path. |

**Recommendation: Cross-cutting facet.**

Prompt patterns are architectural techniques embedded inside artifacts, not separate artifacts themselves. Making them a first-class type would require synthetic entries with no corresponding file, which violates the catalog's principle of artifacts mapping to real files. A `prompt_patterns_used` facet on the artifact schema is the right model — it enriches existing entries rather than creating phantom ones.

The skill decision tree in SKILL.md does NOT need to change. The existing flow handles the catalog operations correctly. Prompt-pattern detection is a *field enrichment* that happens during discover (or as a new `catalog:tag-patterns` micro-capability).

**Proposed SKILL.md text addition** (in the `## Core Capabilities` table, as a note, NOT a new row):

```
> **Note on prompt patterns**: Prompt patterns (anti-rationalization tables, progressive disclosure, 
> self-improving loops, etc.) are cross-cutting techniques found *inside* artifacts, not standalone 
> artifacts. They are captured as a `prompt_patterns_used` facet field during discovery, referencing 
> the vocabulary in `references/prompt-pattern-vocabulary.md`.
```

---

### 3b. `references/capability-recon.md` — new heuristics to add

Add a new section **"Prompt-Pattern Heuristics"** to the existing `## Heuristics` section:

**Proposed addition (append after existing heuristics block):**

```markdown
## Prompt-Pattern Heuristics

When scanning a repo, actively look for these structural signals — they indicate prompt patterns worth noting in the recon report under a new `## Prompt-pattern signals` section:

**Anti-Rationalization tables**
- Look for two-column markdown tables with headers like `Rationalization | Reality`, `Excuse | Truth`, or `Bad pattern | Why it fails`
- Signal: the skill embeds pre-emptive rebuttals before the agent forms excuses
- File locations: anywhere in SKILL.md body, especially in skills with discipline names (TDD, debugging, verification)

**Trigger-only vs. summary descriptions**
- Read the YAML `description` field: is it trigger phrases + WHEN conditions (≤2 sentences), or a workflow summary (3+ sentences)?
- Signal: trigger-only = Discovery Pattern intentionally implemented; summary = may have routing problems

**Progressive disclosure implementation**
- Look for tiered file structure: `SKILL.md` + `references/*.md` + optional `scripts/`
- Look for statements like "only load on demand" or "read only if triggered" in SKILL.md
- Signal: Progressive Disclosure pattern in use

**Session-start hook injection**
- Check `hooks/` for scripts that read skill bodies and inject them as `additionalContext` or `EXTREMELY_IMPORTANT` context
- Signal: Bootstrap Injection pattern — skills can't be ignored even if the agent would normally skip them

**Self-improving loops**
- Look for files named `instincts/`, `learnings.md`, `observations.jsonl`, or YAML-fronted files with `confidence`, `trigger`, `promotion_count` fields
- Look for `/evolve` or `/promote` commands, or skill bodies describing an observation → rule promotion mechanism
- Signal: Self-Improving Agent pattern in use

**Pressure-scenario test files**
- Look in `tests/` for `.txt` files containing natural-language user requests designed to bypass skill invocation
- Look for test scripts that assert skill-NOT-triggering as well as skill-triggering
- Signal: Pressure-Scenario Testing pattern — rare but high-value

**Knowledge-folder-as-bus**
- Look for `docs/knowledge/` or `docs/solutions/` directories with YAML-frontmatter markdown files accumulating across sessions
- Look for agents whose sole job is grepping that folder (not a vector store, just grep)
- Signal: Knowledge-Folder-as-Bus persistence pattern

**Hard-gate state machine composition**
- Look for `<HARD-GATE>` or similar labels in skill bodies that explicitly block transition to certain other skills
- Look for skill descriptions that define terminal states or forbidden successor skill names
- Signal: Hard-gate state machine variant of Compound Recipe

**Injection resistance blocks**
- Look for "Prompt Defense Baseline", "Prompt Injection", or structured blocks early in agent frontmatter body listing rules for resisting instruction overrides
- Signal: Injection Resistance pattern embedded in agent definitions

**Note on reporting**: Under the recon report's `## Standout patterns` section, add a sub-section `### Prompt-pattern signals` listing which patterns were observed and where. Do NOT try to evaluate them during recon — just flag their presence for the discover phase.
```

---

### 3c. `references/capability-discover.md` — schema field proposal

Add `prompt_patterns_used` as an **optional** field to the unified contract, plus documentation on how to populate it.

**Proposed addition to the `## The unified contract` table:**

```markdown
| `prompt_patterns_used` | no | Array of pattern IDs from `references/prompt-pattern-vocabulary.md`. Empty array if none detected. Only populated after recon flagged signals. |
```

**Proposed new section in `capability-discover.md`:**

```markdown
## Prompt-Pattern Detection Pass

When extracting fields for an artifact that recon flagged as having prompt-pattern signals, also populate `prompt_patterns_used`:

1. Read the artifact file fully (not just description)
2. Check against the vocabulary in `references/prompt-pattern-vocabulary.md`
3. For each pattern present, add its `id` to `prompt_patterns_used`
4. If uncertain, leave the array empty — false positives here are worse than misses

This is a best-effort pass, not exhaustive. If no prompt-pattern signals were flagged during recon for this repo, skip this field entirely (leave as empty array or omit).

The field cross-references the brain's taxonomy by stable IDs defined in the vocabulary file. Example:

```json
{"id":"superpowers:skill:test-driven-development", ..., "prompt_patterns_used":["anti-rationalization","progressive-disclosure","tdd-for-skills","pressure-scenario-testing"]}
```
```

---

### 3d. New reference file — `references/prompt-pattern-vocabulary.md`

**Recommendation: YES, create this file.**

Rationale: The catalog needs a stable ID vocabulary to populate `prompt_patterns_used` consistently across discover passes and across the 13 repos. Without it, one agent writes `"anti-rationalization-table"` and another writes `"rationalization-rebuttal"` for the same pattern. The vocabulary file is the single source of truth — and it can be kept thin (ID + one-line definition) since the brain itself holds the full treatment.

**Proposed content:**

```markdown
# Prompt Pattern Vocabulary

**Purpose**: Stable ID list for `prompt_patterns_used` field in the artifact catalog. One-line definitions only — full treatment in the prompt-patterns brain at `~/dev/ad/brains/prompt-patterns/`.

**For Agents**: When populating `prompt_patterns_used` during catalog:discover, use ONLY IDs from this file. If you observe a pattern not listed here, propose a new entry rather than inventing an ID.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## From the Prompt-Patterns Brain (established patterns)

| ID | One-line definition | Brain file |
|----|--------------------|-----------:|
| `discovery` | Description IS the routing program — no separate classifier | `discovery-pattern.md` |
| `capability-description` | WHAT + WHEN + KEYWORDS + NEGATIVE TRIGGERS formula | `capability-description-patterns.md` |
| `progressive-disclosure` | 3-tier load: metadata always, instructions on activation, resources on demand | `discovery-pattern.md` |
| `recipe` | Stack-aware prompt that builds application capability when applied | `recipe-pattern.md` |
| `compound-recipe` | Multiple recipes with declared dependencies, ordering, and idempotency | `composability-patterns.md` |
| `migration-vs-seed` | Seed = one-time bootstrap; Migration = incremental, idempotent | `recipe-pattern.md` |
| `system-comprehension` | Structured prompt building agent mental model of an unfamiliar system | `system-comprehension-pattern.md` |
| `preparation` | Extract + synthesise knowledge from source; deliver in actionable form for another system | `preparation-pattern.md` |
| `agent-handshake` | Structured self-introduction: identity, role, state, communication protocol | `agent-handshake-pattern.md` |
| `self-improving-agent` | Observation → note → rule promotion across invocations; file-based, no vector DB | `self-improving-agent-pattern.md` |
| `orchestration-topology` | Parallel Panel / Autonomous Pipeline / Conversational Delegation structure choice | `orchestration-topology-patterns.md` |
| `agentic-efficiency` | Three coupled cost dimensions: model tier, context volume, prompt precision | `agentic-efficiency-pattern.md` |

---

## Observed in Phase 1 Recon — Candidate New Patterns

These were found in the corpus but don't yet have a home in the prompt-patterns brain. They are valid IDs for the catalog. David may choose to formalize them into the brain or leave them as catalog-only vocabulary.

| ID | One-line definition | First seen |
|----|--------------------|-----------:|
| `anti-rationalization` | Two-column table embedding pre-emptive rebuttals before the agent forms its own excuses | agent-skills-osmani, superpowers |
| `tdd-for-skills` | RED (baseline rationalisations verbatim) → GREEN (minimal skill body) → REFACTOR (re-run, expand) applied to skill authoring | superpowers |
| `pressure-scenario-testing` | Test files encoding natural-language bypass attempts to verify skill-not-triggering as well as triggering | superpowers |
| `bootstrap-injection` | Session-start hook force-loads a skill body as EXTREMELY_IMPORTANT context before agent forms intent | superpowers |
| `knowledge-folder-as-bus` | Git-tracked markdown folder accumulates learnings across sessions; retrieval via grep, no daemon or vector store | compound-knowledge |
| `injection-resistance` | Structured "Prompt Defense Baseline" block embedded early in agent body, resisting instruction overrides | everything-claude-code |
| `hard-gate-state-machine` | Skill composition enforced with terminal states and explicit forbidden successors | superpowers |
| `deliberate-context-exclusion` | Subagents receive only task text, intentionally NOT given plan file or sibling task context | superpowers |
| `cross-project-instinct-promotion` | Instincts promote from project-local to global only when same ID appears in 2+ distinct projects | everything-claude-code |
| `dual-track-learning-schema` | Learning output separated into bug track vs knowledge track, each with different schema enforcement | compound-engineering |
| `reviewer-agent-separation` | Orchestrating skill dispatches specialist reviewer agents; orchestrator merges findings; agents never write files | compound-engineering |

---

*Cross-reference: `~/dev/ad/brains/prompt-patterns/INDEX.md` — full brain with pattern files, decision tree, and worked examples*
```

---

## 4. Open Questions for David

These are the 4 most blocking questions before any changes land:

**Q1 — Cross-cutting facet or artifact type?**
The proposal recommends `prompt_patterns_used` as a facet field on existing artifacts rather than a separate `artifact_type: "prompt-pattern"`. Does David agree? If he wants prompt patterns as first-class entries (so they show up in `catalog:distill` as things to *adopt*, not just *observe*), the approach changes substantially.

**Q2 — Should the 6 new pattern candidates go into the prompt-patterns brain, or stay catalog-only vocabulary?**
`anti-rationalization`, `tdd-for-skills`, `pressure-scenario-testing`, `bootstrap-injection`, `knowledge-folder-as-bus`, `injection-resistance` are all real patterns found in the corpus. They belong in the brain eventually. But should the catalog proposal *drive* that brain update (write them to the brain now) or leave them as catalog-only IDs until David decides to formalize? This affects scope.

**Q3 — Is `catalog:discover` the right place for pattern detection, or should it be a new `catalog:tag-patterns` micro-capability?**
The current discover pass is already complex. Adding prompt-pattern detection as a third responsibility (alongside field extraction and normalize) may bloat it. A thin `catalog:tag-patterns` capability (reads artifacts.jsonl, enriches with `prompt_patterns_used`, writes back) would keep concerns separated. Trade-off: one more capability to invoke.

**Q4 — How deep should pattern detection go during recon?**
The heuristics proposed above are structural signals (look for two-column tables, check description length, look for `<HARD-GATE>` strings). This is shallow but fast. Deeper detection (actually reading skill bodies and classifying against pattern definitions) is more accurate but expensive. David's call: should recon flag signals only (surface-scan), or should it go deep on standout files?

---

*Proposal authored: 2026-05-16 | For: David Cruwys | Awaiting approval before any skill edits*
