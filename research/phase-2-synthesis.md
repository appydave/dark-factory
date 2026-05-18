# Phase 2 Synthesis — What the Numbers Mean

**Purpose**: Enriched commentary on the Phase 2 corpus. Raw cluster + pattern counts (in `INDEX.md`) tell you HOW MUCH; this file tells you WHY each one matters, WHERE it concentrates, and an EXAMPLE worth studying.

**For Agents**: Read this when picking which cluster to distill, or when explaining the corpus to David. The counts are interpretation-free; this file is the interpretation.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Headline observation: "densest pattern coverage"

The vocabulary holds **23 named prompt patterns** (12 established + 11 candidates). For each repo, count how many DISTINCT patterns its skills use:

| Repo | Skills | Distinct patterns used | Density (patterns per skill) |
|------|-------:|------------------------:|-----------------------------:|
| **superpowers** | 14 | 11 | **0.79** ⭐ |
| compound-engineering | 86 | ~8 | 0.09 |
| everything-claude-code | 365 | ~8 | 0.02 |
| ruflo | 219 | ~6 | 0.03 |

ECC has many more *total* pattern instances (because it has 26× more skills), but per skill it uses a narrow set. **Superpowers concentrates more techniques per file than anywhere else** — every candidate pattern in the vocabulary appears in at least one of its 14 skills. If you want to LEARN patterns by reading skills, superpowers is the densest mine.

---

## Top clusters — what each means and what to mine

### `knowledge-capture` (201) — accumulating learnings/memory across sessions

- **Strongest**: ruflo (59), appydave-plugins (37), gbrain (29), compound-engineering (13)
- **Signature examples**: ruflo's `memory-*` skills (HNSW vector + agentdb namespaces); compound-engineering's `ce-compound` (auto-fires on "that worked" / "it's fixed"); gbrain's brain-ops; your `omi-extract` / `capture-context`
- **Why mine this**: every serious harness invents its own memory mechanism — vector store (ruflo) vs grep + frontmatter (compound-knowledge) vs confidence-scored instincts (ECC) vs hand-curated brains (yours). Comparing them tells you what "memory" actually means in agent systems.

### `system-comprehension` (180 — partly inflated)

- **Strongest**: ECC (111 — but **flagged as fallback bucket** for unmatched artifacts), gbrain (12), Ruflo
- **Signature examples**: gbrain's briefing skill; POEM Alex's pre-greeting scan ("scan-then-greet, not greet-then-discover"); your `system-context`
- **Why mine this**: real signal lives in the smaller repos (gbrain, POEM Alex). The ECC contribution is fallback noise and needs a re-tag pass before distill.

### `orchestration` (171) — coordinating multiple agents/skills at runtime

- **Strongest**: ruflo (91 — swarm coordinator suite), appydave-plugins (39 — your fan-out skills), gbrain (16)
- **Signature examples**: ruflo's `hierarchical-coordinator` / `mesh-coordinator` / `byzantine-coordinator` / `raft-manager` / `queen-coordinator` / `gossip-coordinator`; your `doc-review` / `delivery-review` / `omi` / `system-audit`
- **Why mine this**: David's stated interest. Ruflo dominates 2:1 and names topologies explicitly — rare. This is where multi-agent coordination craft lives. Distilling here yields a unified set of "David-style orchestration skills" mining the best of Ruflo's named topologies.

### `verification-validation` (160) — verify work meets spec; gates, not implementation

- **Strongest**: distributed across repos
- **Signature examples**: spec-kit's `analyze` (read-only mandatory gate); superpowers' `verification-before-completion`; compound-engineering's reviewer agents; your `delivery-review`
- **Why mine this**: every workflow needs gates. This is where "Iron Law" anti-rationalization patterns concentrate — read superpowers here for the sharpest phrasings.

### `spec-writing` (157) — formalize requirements before implementation

- **Strongest**: ECC (54), bmad-method (18), spec-kit (10), gsd
- **Signature examples**: spec-kit's `constitution → specify → clarify` chain; BMAD's PRD lifecycle (`bmad-prd` → `bmad-create-prd` → `bmad-edit-prd` → `bmad-validate-prd`); ECC's spec authoring
- **Why mine this**: contrasts two philosophies — heavy spec-first (spec-kit, BMAD epic-level) vs lightweight (ECC inline). A distill would surface "when is each warranted?"

### `workflow-architecture` (137) — design multi-step / multi-agent workflows

- **Strongest**: ECC (77), gsd (19), bmad
- **Signature examples**: POEM Alex (Workflow Architect — interviews user, scans project, emits workflow YAML + `.usage.md` guide); gsd workflow design; BMAD workflow authoring
- **Why mine this**: this is what David is doing RIGHT NOW with the dark-factory catalog itself. Alex's "scan-then-greet" boot pattern is worth borrowing.

### `code-review` (132) — review code quality against criteria

- **Strongest**: compound-engineering (40 — reviewer suite), appydave-plugins (27 — your review skills), agent-skills-osmani (6)
- **Signature examples**: `ce-code-review` (15-20 parallel reviewers + structured JSON findings); your `delivery-review` orchestrator (6 specialists); Osmani's review skills
- **Why mine this**: **best-mined cluster.** Multiple repos all solve the same problem differently — converging here gives you the canonical David-style code review.

*Skipping `planning` (132), `delivery-readiness` (90), `code-implementation` (81), `documentation` (75), `prompt-engineering` (72), `security-review` (66 — newly promoted), `discovery-routing` (56), `test-authoring` (43), `refactor` (39), `performance` (34 — newly promoted), `dependency-management` (21 — newly promoted), `skill-authoring` (16), `self-improvement` (16), `field-feedback` (4) — for brevity. Same treatment available on request.*

---

## Top patterns — what each means and what to mine

### `capability-description` (311) — table stakes

- **What**: WHAT + WHEN + KEYWORDS + NEGATIVE TRIGGERS in the description field — the "resume" formula
- **Where**: universal — every well-written skill carries it
- **Why it matters**: 28% of corpus carries it. Pattern is table stakes, not a differentiator. Its ABSENCE is the useful signal — skills without it have routing problems. (Recall: 11 of your own brand-dave/flivideo commands have no description — quality flag.)

### `discovery` (184) — description IS the routing program

- **What**: lazy load until trigger fires; no separate classifier
- **Where**: ECC dominates with 175 of 184 — ECC bets its architecture on this
- **Signature**: ECC's 230 skills all designed around description-as-trigger
- **Why it matters**: confirms the "Use when user is about to write code without tests" framing is industry-standard among serious skill authors. Your insights.md already canonizes this contrast.

### `reviewer-agent-separation` (92)

- **What**: orchestrator dispatches specialist reviewer agents in parallel; reviewers return structured JSON; reviewers never write files (David's invariant)
- **Where**: compound-engineering (~49 reviewer agents), ECC
- **Signature**: `ce-code-review` dispatches 15-20 reviewers across tiers; orchestrator dedupes by confidence
- **Why it matters**: architectural answer to "how do you scale code review?" Worker and reviewer are SEPARATE concerns — a constraint that produces clean fan-out.

### `orchestration-topology` (87)

- **What**: Parallel Panel / Autonomous Pipeline / Conversational Delegation — explicit structure choice for coordinating agents
- **Where**: ruflo (40+ — the named coordinator suite), appydave-plugins
- **Signature**: ruflo's `hierarchical-coordinator` / `mesh-coordinator` / `byzantine-coordinator` / `raft-manager` / `gossip-coordinator` / `quorum-manager`; your `doc-review` (Parallel Panel)
- **Why it matters**: Ruflo names them explicitly — most other tools don't. This naming alone teaches you the design space.

### `multi-harness-compile` (72) — newly promoted

- **What**: one source → N target-host outputs via compile pipeline; compiled outputs are build artifacts, not source
- **Where**: gstack (49), spec-kit (23)
- **Signature**: gstack's `.tmpl` → 11 hosts via 21 resolver modules; spec-kit's 30 harness adapter classes
- **Why it matters**: answer to "how do I ship one skill to Claude AND Codex AND Cursor." NOT relevant for you (Claude Code only) — but the compilation MECHANISM (token grammar, resolver, preamble-tier dial) is interesting design.

### `injection-resistance` (60)

- **What**: "Prompt Defense Baseline" structured block embedded early in agent body
- **Where**: ECC (universal — all 60 agents carry it)
- **Signature**: ECC's `agents/*.md` files all carry the same defense baseline block
- **Why it matters**: ECC is the only repo treating prompt injection as a first-class concern for every agent. Worth borrowing the *block* directly for any agent that ingests external input.

### `knowledge-folder-as-bus` (50)

- **What**: git-tracked markdown folder as persistence substrate; grep retrieval; no DB / daemon / vector store
- **Where**: compound-knowledge (universal — 11/11 artifacts), gbrain
- **Signature**: compound-knowledge's `docs/knowledge/` folder + `kw:compound` writer + grep-based researcher agents
- **Why it matters**: shows you don't need vector embeddings for agent memory — markdown + grep + good frontmatter gets you 80% of the way.

---

## Standout phrases (atomic gold)

The 39 entries in `insights.md` capture craft-sized bits. Re-reading favorites:

- **"Use when user is about to write code without tests"** (Superpowers) — the canonical example of description-as-trigger
- **"Iron Law + violating the letter is violating the spirit"** (Superpowers) — verbatim phrase that pre-empts spirit-vs-ritual rationalizations across TDD, debugging, verification
- **"Agent time is cheap. Tech debt is expensive."** (Compound-engineering) — phrase doing policy work, eliminating the weighing decision entirely
- **"Checklists are unit tests for English"** (Spec-kit) — reframes requirements validation as a quality gate on the spec, not on the code
- **"Subagents are about what is NOT in their context"** (Superpowers) — flips context engineering from inclusion to deliberate exclusion
- **"Scan-then-greet, not greet-then-discover"** (POEM Alex) — boot-time `system-comprehension` embedded in activation rather than a separate command

---

## Recommended next move

**Distill on the `orchestration` cluster** (171 artifacts).

Why this single cluster first:
1. **Smallest "real test"** — 171 is small enough to walk by hand, big enough to surface real variation
2. **You named it as the interest area** — Ruflo's swarm topologies are your stated target
3. **Ruflo names topologies explicitly** (hierarchical / mesh / byzantine / raft / gossip / quorum) — gives the distill a built-in skeleton
4. **You already have 39 of your own orchestrators** in `appydave-plugins` (your fan-out style) — the distill becomes "merge Ruflo's topology vocabulary with your fan-out patterns"
5. **Proves the distill flow** before bigger clusters (knowledge-capture at 201, system-comprehension at 180)

Output of the distill pass: 5-10 unified "David-style orchestration skills" with phrasings mined from across the 171, following SRP, composable, consistent — exactly your stated goal.
