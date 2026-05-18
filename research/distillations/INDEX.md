---
distillation_pass: orchestration
source_slice: _slice_orchestration.jsonl
source_artifact_count: 171
sub_cluster_count: 8
distillation_files: 8
created: 2026-05-16
status: draft
---

---
distillation_pass: workflow-architecture
source_slice: _slice_workflow_architecture.jsonl
source_artifact_count: 137
sub_cluster_count: 5
distillation_files: 5
created: 2026-05-17
status: draft
---

<!-- code-implementation pass appended 2026-05-17 -->

# Distillations Index

**Purpose**: Navigation index for all distillation passes. Each cluster has its own sub-cluster summary inline or in a separate INDEX section.

**For Agents**: Jump to the relevant cluster section to find distillation files. Each distillation file links back to source artifacts.

**Last Updated**: 2026-05-17

---

## Delivery-Readiness Cluster

**Pass**: Phase 5 catalog:distill — delivery-readiness cluster
**Source slice**: `artifacts/_slice_delivery_readiness.jsonl`
**Source artifact count**: 90
**Sub-cluster count**: 5 (plus excluded)
**Distillation files**: 4
**Created**: 2026-05-17

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| pre-merge-gate | [delivery-readiness-pre-merge-gate.md](delivery-readiness-pre-merge-gate.md) | ~18 | appydave:delivery-review | UPGRADE — existing skill, fold deployment verification + hard-gate state machine + threat-mitigation check |
| commit-quality-gate | [delivery-readiness-commit-quality-gate.md](delivery-readiness-commit-quality-gate.md) | ~7 | appydave:kcommit | UPGRADE — existing skill, fold value-first message framing + convention detection + adaptive PR body |
| pr-lifecycle | [delivery-readiness-pr-lifecycle.md](delivery-readiness-pr-lifecycle.md) | ~12 | compound-engineering:ce-resolve-pr-feedback | YES — resolve-pr-feedback mechanism entirely absent; `pr-lifecycle` skill exists but needs this folded in |
| post-deploy-canary | [delivery-readiness-post-deploy-canary.md](delivery-readiness-post-deploy-canary.md) | ~6 | everything-claude-code:canary-watch | YES — no post-deploy verification in David's stack |
| milestone-ship-ceremony | [delivery-readiness-milestone-ship-ceremony.md](delivery-readiness-milestone-ship-ceremony.md) | ~10 | gsd:complete-milestone | YES (conditional) — if David uses GSD; otherwise patterns still valuable |

### Artifacts excluded from sub-clusters

**Framework-specific verification loops (not David's stack)**:
`everything-claude-code:django-verification`, `laravel-verification`, `quarkus-verification`, `springboot-verification` — framework-specific pre-PR verification loops for Django/Laravel/Quarkus/Spring Boot. Not David's stack (TS/Next.js + Ruby).

**Build-fix commands (not David's primary languages)**:
`everything-claude-code:commands:build-fix`, `cpp-build`, `flutter-build`, `go-build`, `gradle-build`, `kotlin-build`, `rust-build` — language-specific build error fixers. None of these are David's primary stack. The `build-fix` pattern (detect build system → incremental fix) is worth noting as a cross-cutting idea but doesn't warrant a distillation.

**Ruflo stub skills (no mechanism)**:
`ruflo:agent-github-modes`, `ruflo:agent-github-pr-manager`, `ruflo:agent-ops-cicd-github`, `ruflo:agent-pr-manager`, `ruflo:agent-release-manager`, `ruflo:agent-release-swarm`, `ruflo:github-automation`, `ruflo:github-code-review`, `ruflo:github-multi-repo`, `ruflo:github-project-management`, `ruflo:github-release-management`, `ruflo:github-workflow-automation` — Ruflo stubs with no mechanism depth (all `description_raw` is too-short or stub). Pattern vocabulary from Ruflo covered in orchestration distill.

**Domain-specific/solo artifacts**:
- `appydave:near-compaction` — context-saving orchestrator; belongs in knowledge-capture cluster
- `appydave:system-audit` — full codebase audit; belongs in code-review cluster (already handled)
- `everything-claude-code:crosspost` — content distribution; not delivery-readiness
- `everything-claude-code:evm-token-decimals` — EVM decimal bug prevention; domain-specific
- `everything-claude-code:hermes-imports` — Hermes workflow sanitizer; solo
- `everything-claude-code:opensource-pipeline` + `opensource-sanitizer` — public release sanitization; one-of-a-kind
- `everything-claude-code:project-flow-ops` — GitHub + Linear coordination; planning/execution layer
- `everything-claude-code:unified-notifications-ops` — notification routing; infrastructure/workflow
- `ruflo:witness-curator` — cryptographic witness manifest; governance cluster (orchestration distill)
- `gsd:check-todos` + `gsd:review-backlog` — backlog management; planning cluster
- `gsd:quick` — quick task execution; code-implementation cluster
- `everything-claude-code:autonomous-loops` + `continuous-agent-loop` — loop patterns; orchestration cluster
- `spec-kit:speckit.git.remote` — helper command; utility, not standalone skill
- `agent-skills-osmani:ci-cd-and-automation` — CI/CD setup; scoped to commit-quality-gate as a folded idea

### Top 3 unified skills that close real gaps in David's stack

**1. `post-deploy-canary`** — entirely absent
David ships to Vercel regularly (SupportSignal, AppyDave tools). No post-deploy verification exists. ECC's `canary-watch` is zero-dep, Claude Code-native, and would catch the most common post-deploy failure modes (endpoint down, console errors, performance regression) without any infrastructure. The gap is real and the solution is immediately adoptable.

**2. `pr-lifecycle` (resolve-feedback mechanism)** — mechanism gap in existing skill
`ce-resolve-pr-feedback`'s mechanism (evaluate validity → parallel resolvers → reply + close via GraphQL) is absent. David likely addresses review feedback manually or ignores unresolved threads. This is especially important for SupportSignal (client code review) where reviewers expect thread closure.

**3. `pre-merge-gate` (deployment verification upgrade)** — conditional upgrade
`delivery-review` is already production-deployed but lacks the deployment-risk dimension for data-touching PRs. SupportSignal has migrations, PII, and auth surfaces — these all benefit from CE's SQL verification query generation and rollback procedure pattern before merging.

### Top 2 gaps in this distillation

**Gap 1**: No CI/CD automation skill for David's stack. The corpus has `agent-skills-osmani:ci-cd-and-automation` (general) and `everything-claude-code:deployment-patterns` (Docker/web-app focused), but nothing specifically for Vercel deployments or Ruby gem CI (GitHub Actions + rspec + rubocop). David's `kcommit` watches CI but there's no skill for setting up or modifying the CI pipeline itself.

**Gap 2**: No "build is broken, fix it" skill for David's TypeScript/Next.js stack. ECC has `build-fix` commands for 7 languages but not TypeScript/Next.js specifically. When Vercel builds break, David fixes manually. The `build-fix` pattern (detect build system → incremental fix → verify) is immediately portable to Next.js builds.

### 1 open question

**Does David use GSD?** The `milestone-ship-ceremony` distillation has the highest value if David uses GSD's `.planning/` structure. If not, the patterns still apply but the implementation is a build, not an adoption. Knowing the answer changes whether `complete-milestone` is a "fold into session-checkpoint" or a "new skill from scratch".

---

## Orchestration Cluster

# Distillations — Orchestration Cluster

**Purpose**: Unified skill drafts distilled from the 171 orchestration-tagged artifacts across 10 repos.

**For Agents**: Use this index to navigate distillation files when David asks "what unified skills came out of the orchestration distill" or is reviewing the cluster to approve/adjust unified skill candidates.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [swarm-topology](#swarm-topology) | [orchestration-swarm-topology.md](orchestration-swarm-topology.md) | ~17 (all ruflo) | ruflo:agent-hierarchical-coordinator | YES — vocabulary gap |
| [parallel-review-fan-out](#parallel-review-fan-out) | [orchestration-parallel-review-fan-out.md](orchestration-parallel-review-fan-out.md) | ~16 (appydave dominant) | appydave:delivery-review | PATTERN — already exists; this documents the canonical mechanism |
| [autonomous-pipeline-runner](#autonomous-pipeline-runner) | [orchestration-autonomous-pipeline-runner.md](orchestration-autonomous-pipeline-runner.md) | ~18 (superpowers + gsd) | superpowers:subagent-driven-development | YES — mechanism gap |
| [agent-lifecycle-coordinator](#agent-lifecycle-coordinator) | [orchestration-agent-lifecycle-coordinator.md](orchestration-agent-lifecycle-coordinator.md) | ~15 (ruflo + gbrain + ecc) | gbrain:minion-orchestrator | YES — missing layer |
| [multi-machine-coordinator](#multi-machine-coordinator) | [orchestration-multi-machine-coordinator.md](orchestration-multi-machine-coordinator.md) | ~13 (appydave + ruflo + gstack) | appydave:remote-machines | PATTERN — already exists; fleet-wide fan-out is the gap |
| [data-pipeline-orchestrator](#data-pipeline-orchestrator) | [orchestration-data-pipeline-orchestrator.md](orchestration-data-pipeline-orchestrator.md) | ~14 (appydave + gbrain) | appydave:omi | PATTERN — OMI exists; general ingest router is the gap |
| [governance-and-observability](#governance-and-observability) | [orchestration-governance-and-observability.md](orchestration-governance-and-observability.md) | ~15 (ruflo dominant) | ruflo:observe + ruflo:witness + appydave:truth-trail (3-layer) | YES — significant gap |
| [workflow-design-advisor](#workflow-design-advisor) | [orchestration-workflow-design-advisor.md](orchestration-workflow-design-advisor.md) | ~19 (appydave + gsd) | appydave:ruflo-swarm-check + appydave:agent-orchestrator | PARTIAL — two skills exist; unified entry point is the gap |
| [swarm-memory-coordinator](#swarm-memory-coordinator) | [orchestration-swarm-memory-coordinator.md](orchestration-swarm-memory-coordinator.md) | ~5 (ruflo only) | none — gap | YES — gap, no clear winner |

---

## Artifacts excluded from sub-clusters

### Ruflo domain-specific stubs (~19 artifacts)
Single-concern agent stubs from Ruflo (`agent-payments`, `agent-authentication`, `agent-trading-predictor`, `agent-data-ml-model`, `agent-dev-backend-api`, `agent-agentic-payments`, `agent-challenges`, `agent-crdt-synchronizer`, `agent-base-template-generator`, `agent-issue-tracker`, `agent-pagerank-analyzer`, `agent-production-validator`, `agent-project-board-sync`, `agent-refinement`, `agent-repo-architect`, `agent-user-tools`, `agent-v3-integration-architect`, `agent-workflow`) — domain-specific worker agents, not orchestration patterns. Not distillable into unified skills.

### True solos (~12 artifacts)
One-of-a-kind artifacts without cluster peers:
- `apps-registry`, `schedules-registry` (appydave) — config registry pattern; not orchestration
- `dark-factory-catalog` (appydave) — meta: the catalog itself
- `easy-git` (appydave) — utility
- `lexi` (appydave) — brain librarian; unique, consider a separate distillation
- `prose2models` (appydave) — conversion tool; not orchestration
- `create-plugin` (ruflo) — scaffold; not orchestration
- `bmad-party-mode` (bmad) — multi-agent conversation; edge case
- `sessions` (ecc) — session history management; utility
- `current-deck` (appydave) — context mode switcher; utility
- `mochaccino-v1` (appydave) — deprecated
- `worker-benchmarks` (ruflo) — benchmark runner; utility

---

## Top 3 unified skills that close real gaps in David's stack

### 1. `swarm-topology` — vocabulary gap
David's fan-out skills (`delivery-review`, `doc-review`) are implicitly **Parallel Panel** topology but unnamed as such. Adopting Ruflo's topology vocabulary (hierarchical / mesh / queen / raft / quorum / gossip / byzantine) gives David a design language for choosing the right structure before building. The gap is: David has instances but no taxonomy.

### 2. `autonomous-pipeline-runner` — mechanism gap
David has `ralphy` (hands-off campaign UX) but no explicit mechanism for the **deliberate-context-exclusion + hard-gate-state-machine** pattern from Superpowers. The gap: his campaigns don't currently enforce the spec-first → quality-review gate. Adopting Superpowers' mechanism into `ralphy` would make campaigns more reliable.

### 3. `governance-and-observability` — significant gap
David has no governance layer for agent swarms. As agent use scales (Kybernesis), the absence of: cost tracking, fix-verification (witness pattern), and drift detection (horizon-tracker) will become painful. `truth-trail` covers knowledge agents; the swarm governance layer is entirely missing.

---

## Top 3 sub-clusters where no clear winner emerged (need David's judgment)

### 1. `swarm-memory-coordinator`
Only 5 artifacts, all Ruflo-infrastructure-dependent. No David-stack equivalent. The gap is real but the winner mechanism requires Ruflo. Options: adopt `knowledge-folder-as-bus` pattern from compound-knowledge (markdown + grep, zero infra), or wait until first real multi-agent swarm surfaces the need.

### 2. `workflow-design-advisor`
Two existing appydave skills cover parts of this (`ruflo-swarm-check` as gate, `agent-orchestrator` as design session) but they're not unified into a single entry point. Question: is a unified skill the right answer, or is "know which tool to call when" sufficient?

### 3. `agent-lifecycle-coordinator`
`gbrain:minion-orchestrator` has the cleanest dual-mode design but depends on GBrain's infrastructure. The Ruflo implementations require the Ruflo daemon. Neither is cleanly portable to David's stack. Question: should David build a lightweight lifecycle coordinator on top of Claude Code's native subagent + worktree model?

---

## Open questions for David

1. **Ralphy vs autonomous-pipeline-runner**: Should the Superpowers `subagent-driven-development` mechanism (deliberate exclusion + hard gates) be folded INTO `ralphy`, or is it a separate skill that `ralphy` delegates to?

2. **Swarm memory**: Is the `knowledge-folder-as-bus` pattern (git markdown + grep) sufficient for swarm-internal state sharing, or is a proper agentdb needed? (This determines whether `swarm-memory-coordinator` becomes a real skill or a note.)

3. **Governance ladder**: Which governance layer does David want first? Suggested order: (a) `truth-trail` already done, (b) add cost tracking, (c) add witness/fix-verification, (d) add drift detection. Or does he want all of (b-d) bundled?

4. **Cross-platform-skill-compiler** (gstack's multi-harness-compile, ~7 artifacts): Explicitly scoped out of this distillation — not relevant for Claude Code-only stack. Confirm this is correct before closing the orchestration pass.

---

## Corpus notes

- **Ruflo**: 91 of 171 artifacts. Dominates swarm-topology, swarm-memory, and governance sub-clusters. High pattern density but infrastructure-heavy — most mechanisms require the Ruflo daemon. Adopt vocabulary and patterns; evaluate infrastructure case by case.
- **Appydave**: 39 of 171. Already in David's stack. These are baseline, not target. Fan-out pattern is strongest here.
- **Superpowers**: Only 2 artifacts in this slice but the highest mechanism density per artifact. `subagent-driven-development` is the most technically precise orchestration skill in the entire 171 — read it in full before building any autonomous pipeline.
- **GSD**: 10 artifacts. Dependency-ordered parallel waves (execute-phase) and state-aware auto-advance (gsd:next) are the two ideas worth lifting from GSD into David's stack.

---

*Distillation pass: Phase 5 catalog:distill — orchestration cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Code-Review Cluster

**Pass**: Phase 5 catalog:distill — code-review cluster
**Source slice**: `_slice_code_review.jsonl`
**Source artifact count**: 135
**Sub-cluster count**: 6
**Distillation files**: 6
**Created**: 2026-05-16

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [monolithic-quality](#monolithic-quality) | [code-review-monolithic-quality.md](code-review-monolithic-quality.md) | ~12 | agent-skills-osmani:code-review-and-quality | PARTIAL — fast path for flow-state checks; complements delivery-review |
| [dimensional-specialist](#dimensional-specialist) | [code-review-dimensional-specialist.md](code-review-dimensional-specialist.md) | ~24 | compound-engineering:ce-adversarial-reviewer | YES — depth calibration + anchored confidence rubric missing from David's 6 specialists |
| [security-specialist](#security-specialist) | [code-review-security-specialist.md](code-review-security-specialist.md) | ~14 | compound-engineering:ce-security-reviewer | YES — diff-scoped attack-path security review; gap between prompt-injection-scanner and full security-analyst |
| [pr-lifecycle](#pr-lifecycle) | [code-review-pr-lifecycle.md](code-review-pr-lifecycle.md) | ~9 | compound-engineering:ce-resolve-pr-feedback | YES — resolve-pr-feedback skill missing; GraphQL thread resolution is the mechanism gap |
| [doubt-driven](#doubt-driven) | [code-review-doubt-driven.md](code-review-doubt-driven.md) | ~6 | agent-skills-osmani:doubt-driven-development | YES — in-flight adversarial self-review entirely absent from David's stack |
| [lang-stack-specialist](#lang-stack-specialist) | [code-review-lang-stack-specialist.md](code-review-lang-stack-specialist.md) | ~23 | compound-engineering:ce-kieran-typescript-reviewer | PARTIAL — pattern documented; specific TypeScript reviewer for David's primary stack not yet built |

---

### Artifacts not sub-clustered (solos / excluded)

**Explicitly excluded — already covered by orchestration distill**:
- `appydave-plugins:skill:delivery-review` — the fan-out orchestrator; documented in `orchestration-parallel-review-fan-out.md`
- `ruflo:skill:agent-code-review-swarm` — swarm orchestration; covered in orchestration distill

**Domain-specific stubs (non-generalizable)**:
- `ruflo:skill:claims`, `ruflo:skill:"V3 Security Overhaul"`, `ruflo:skill:"V3 Swarm Coordination"` — Ruflo-infrastructure-specific, not portable
- `ruflo:agent:browser-agent`, `ruflo:agent:federation-coordinator` — infrastructure agents, not review patterns
- `everything-claude-code:skill:django-verification`, `laravel-verification`, `quarkus-verification`, `springboot-verification` — framework verification, not David's stack

**True solos (one-of-a-kind, no cluster peer)**:
- `appydave-plugins:skill:false-twins` — design analysis, not code review; unique
- `appydave-plugins:skill:lexi` — brain librarian; belongs in knowledge-management cluster
- `appydave-plugins:skill:schedules-registry`, `skills-registry` — config registries; not review
- `appydave-plugins:skill:system-audit` — system-level posture; one-of-a-kind
- `appydave-plugins:skill:ansible-fleet` — infrastructure management; not review
- `gbrain:skill:cross-modal-review` — cross-modal (image+text) review; no peers; interesting solo
- `ruflo:command:ruflo-loop`, `ruflo:command:audit` — Ruflo pipeline commands
- `compound-engineering:skill:ce-simplify-code` — simplification (not review); adjacent but separate
- `everything-claude-code:skill:council` — council-of-agents deliberation; belongs in orchestration cluster
- `everything-claude-code:skill:ecc-tools-cost-audit` — cost audit; one-of-a-kind

---

### Top 3 gaps closed in David's existing review stack

#### 1. Diff-scoped security review (`code-review-security-specialist`) — REAL GAP
David has `prompt-injection-scanner` (pipeline input gate) and `security-analyst` (project-wide audit) but nothing in between: a diff-scoped, attack-path-tracing security reviewer that runs per PR on code that touches auth, public endpoints, or user input. CE's `ce-security-reviewer` is the mechanism. This is the most immediately actionable gap — SupportSignal is an NDIS app (PII, compliance, auth requirements).

#### 2. In-flight adversarial review (`code-review-doubt-driven`) — REAL GAP
David has no mechanism for the accumulated-context problem. `delivery-review` reviews finished artifacts; nothing catches the case where the reviewer and implementer are the same session carrying the same wrong assumptions. Osmani's `doubt-driven-development` (CLAIM → EXTRACT → DOUBT → RECONCILE → STOP) is the exact mechanism, and it is entirely absent from David's stack.

#### 3. PR feedback resolution (`code-review-pr-lifecycle`) — REAL GAP
David has no skill for systematically resolving GitHub PR review threads: evaluating feedback validity, fixing in parallel, replying to threads, and closing via GraphQL. `ce-resolve-pr-feedback` is production-tested at EveryInc and directly addresses the "review comments sit unresolved" failure mode.

---

### Top 3 sub-clusters needing David's judgment

#### 1. `monolithic-quality` — is a new skill needed?
Osmani's `code-review-and-quality` is excellent for flow-state review, but David already has `delivery-review`. The question: should "quick review" invoke a new lightweight single-pass skill, or just invoke `delivery-review` with fewer dimensions? A distinct skill is more ergonomic but adds maintenance surface.

#### 2. `lang-stack-specialist` — which stack first?
The pattern is clear (CE's named-persona conditional reviewers). The question is prioritization. Candidates: `review-typescript` for Next.js (highest frequency), `review-accessibility` for SupportSignal (highest stakes), or `review-rails` for client work. All three are worth building; which goes first?

#### 3. `dimensional-specialist` — retrofit existing specialists?
CE's depth calibration (Quick/Standard/Deep) and anchored confidence rubric are clear upgrades to David's 6 existing specialists. But retrofitting 6 skills is non-trivial work. The question: retrofit all 6 in one pass, or only apply to new specialists built going forward?

---

### Open questions for David

1. **7th dimension**: Should `review-security` become an automatic 7th dimension in `delivery-review` when the diff triggers security signals (auth, public endpoints, user input)? This is how CE's `ce-security-reviewer` operates — conditional, not always-on.

2. **8th dimension**: Is a reliability/error-handling dimension (`silent-failure-hunter` territory) a gap in David's current 6? CE has `ce-reliability-reviewer`; ECC has `silent-failure-hunter`. Neither maps to a current David specialist.

3. **Resolve-PR-feedback naming**: Should `resolve-pr-feedback` use the `review-` prefix (consistent with current specialists) or a different verb (`resolve-`, `respond-`) since it's resolution, not review?

---

### Corpus notes

- **Compound-engineering**: 40+ artifacts. Most mechanism-dense source. `ce-code-review` is the most complete multi-agent review orchestrator in the corpus — 18 conditional reviewers, depth calibration, autofix modes, headless mode, GitHub thread resolution. The mechanism library for building David's next-generation review stack.
- **Appydave-plugins**: 28 artifacts. David's existing stack is the baseline. The fan-out pattern is the strongest contribution. Gaps vs CE: no depth calibration, no confidence rubric, no security dimension, no PR lifecycle tooling.
- **Agent-skills-osmani**: 7 artifacts. Highest ideas-per-artifact ratio in the cluster. `code-review-and-quality` and `doubt-driven-development` are both directly usable. `security-and-hardening` is the Three-Tier Boundary System (complement to code review).
- **Everything-claude-code**: ~20 artifacts. Strong language-specific reviewers and accessibility. `silent-failure-hunter` and `code-reviewer` (4-question pre-report gate) are the two most portable ideas.
- **Superpowers**: 2 artifacts. `receiving-code-review` is the most rigorous feedback-reception protocol in the corpus — verify before implementing, YAGNI check, no performative agreement.

---

*Distillation pass: Phase 5 catalog:distill — code-review cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Code-Implementation Cluster

**Pass**: Phase 5 catalog:distill — code-implementation cluster
**Source slice**: `_slice_code_implementation.jsonl`
**Source artifact count**: 81
**Sub-cluster count**: 4
**Distillation files**: 4
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [tdd-discipline](#tdd-discipline) | [code-implementation-tdd-discipline.md](code-implementation-tdd-discipline.md) | ~8 (superpowers dominant) | superpowers:test-driven-development | PARTIAL — BMAD sprint already has TDD; gap is non-sprint work |
| [systematic-debug](#systematic-debug) | [code-implementation-systematic-debug.md](code-implementation-systematic-debug.md) | ~4 (compound + superpowers) | compound-engineering:ce-debug | YES — no debug skill in David's stack; significant gap |
| [feature-implement](#feature-implement) | [code-implementation-feature-implement.md](code-implementation-feature-implement.md) | ~22 (compound + gsd + superpowers + spec-kit + bmad) | compound-engineering:ce-work | PARTIAL — BMAD sprint has bmad-dev-story; gap is non-sprint features |
| [worktree-isolation](#worktree-isolation) | [code-implementation-worktree-isolation.md](code-implementation-worktree-isolation.md) | ~3 (superpowers + compound) | superpowers:using-git-worktrees | YES — no explicit worktree isolation skill in David's stack |

---

### Artifacts excluded from sub-clusters

**Ruflo domain stubs (21 artifacts)**: `agent-coder`, `agent-implementer-sparc-coder`, SPARC methodology, V3 roadmap, AgentDB/ReasoningBank — Ruflo-infrastructure-specific. SPARC vocabulary noted as insight; not distilled.

**David's utility skills (4 artifacts)**: `baku`, `nano-banana`, `system-audit`, `dev` — already in David's stack.

**ECC lang-specific TDD (8 artifacts)**: `laravel-tdd`, `springboot-tdd`, `cpp-test`, `go-test`, `kotlin-test`, `rust-test` — not David's primary stack.

**GSD UI cluster (3 artifacts)** + **Compound UI/design (4 artifacts)**: GSD-pipeline-specific or Figma/DHH-specific. Not portable as-is.

---

### Top 3 gaps closed

#### 1. `systematic-debug` — REAL GAP
David has no debug skill. CE's `ce-debug` + Superpowers' architecture-escalation pattern provides a complete root-cause-first workflow with issue tracker integration — critical for SupportSignal GitHub issues. Highest-leverage improvement in this cluster.

#### 2. `feature-implement` — WORKFLOW GAP
`bmad-dev-story` covers sprint work; nothing covers non-sprint features. CE's `ce-work` complexity triage + parallel subagent + worktree isolation fills that gap.

#### 3. `worktree-isolation` — PRECONDITION GAP
No explicit worktree isolation precondition in David's stack. Closes the "accidentally implemented on main" failure mode.

---

### Top 3 sub-clusters needing David's judgment

1. **`tdd-discipline` vs. BMAD redundancy** — BMAD sprint already enforces TDD; is a standalone skill worth the maintenance surface?
2. **`feature-implement` + `lfg` topology** — should `feature-implement` be a sub-skill `lfg` calls, or standalone?
3. **Ruflo SPARC vocabulary** — worth adopting as phase annotations on existing skills?

---

### Open questions for David

1. **Assessment mode**: David does not author implementation skills directly — BMAD Amelia is the developer persona. These distillations are ideas to fold into BMAD Amelia's configuration or existing skill upgrades, not skills David would build and use directly.

2. **`dev` skill scope**: Is David's existing `dev` skill a dispatcher (routes to sub-skills) or a full implementation skill? If dispatcher, `feature-implement` and `systematic-debug` should be the routing targets.

---

### Corpus notes

- **Superpowers (6 artifacts)**: Highest mechanism-per-artifact density. `test-driven-development` and `systematic-debugging` are the two best standalone implementation discipline skills in the 81-artifact cluster. Zero-infrastructure, directly adoptable.
- **Compound-engineering (11 artifacts)**: `ce-work` is the most complete feature-execution skill; `ce-debug` is the most complete debug skill. `lfg` is the end-to-end pipeline wrapper.
- **GSD (8 artifacts)**: Wave-based dependency ordering and trivial-task fast path are the two portable ideas. The rest is GSD-specific infrastructure.
- **BMAD (3 artifacts)**: Already in David's stack via `bmad-story-lifecycle`. No new additions for sprint work; gap is non-sprint.
- **Ruflo (21 artifacts)**: Domain stubs. SPARC vocabulary is the only portable concept.

---

*Distillation pass: Phase 5 catalog:distill — code-implementation cluster. Assessment mode — David does not author implementation skills directly; these are ideas to fold into BMAD Amelia's configuration or existing skill upgrades. Regenerate after David reviews.*

---

## System-Comprehension Cluster

**Pass**: Phase 5 catalog:distill — system-comprehension cluster
**Source slice**: `_slice_system_comprehension.jsonl`
**Source artifact count**: 180 (111 ECC — 90 fallback noise, 21 genuine signal; 69 real signal from non-ECC repos)
**Sub-cluster count**: 4 kept + 1 noise bucket discarded
**Distillation files**: 4
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [repo-onboarding](#repo-onboarding) | [system-comprehension-repo-onboarding.md](system-comprehension-repo-onboarding.md) | ~12 (appydave + bmad + ce + gsd) | appydave:system-context | PATTERN — already exists; parallel-mapper + phase-scoping are the upgrade ideas |
| [pre-action-scan-boot](#pre-action-scan-boot) | [system-comprehension-pre-action-scan.md](system-comprehension-pre-action-scan.md) | ~8 (poem + gstack + ce) | poem:alex + gstack:context-save/restore (split) | YES — context-save/restore gap; scan-embedded-in-activation is a principle worth adopting |
| [brownfield-forensics](#brownfield-forensics) | [system-comprehension-brownfield-forensics.md](system-comprehension-brownfield-forensics.md) | ~7 (bmad + gstack + gsd + ce) | bmad:bmad-investigate | YES — no equivalent in David's stack; Iron Law + 4-phase structure are the mechanism |
| [intent-routing-discovery](#intent-routing-discovery) | [system-comprehension-intent-routing.md](system-comprehension-intent-routing.md) | ~8 (osmani + gbrain + appydave) | appydave:brain-query + app-query + llm-context (existing chain) | PATTERN — chain exists; dispatcher-clause compression is the upgrade; context-degradation hook is the gap |
| [domain-research](#domain-research) | [system-comprehension-domain-research.md](system-comprehension-domain-research.md) | ~9 (bmad + ce + gsd) | gsd:gsd-phase-researcher | YES — BMAD research skills are thin; planning-question-anchored research contract is the gap |

---

### ECC Noise Accounting

**111 ECC artifacts in the slice; 90 are fallback bucket noise.**

ECC's discovery algorithm assigns `system-comprehension` as the fallback cluster for unmatched artifacts. The 90 noise artifacts include domain-specific language patterns (kotlin, rust, flutter, django), infrastructure ops (homelab, netmiko), business verticals (healthcare-phi, energy-procurement, customs-trade), and ECC-internal tooling (hookify, pm2, santa-loop). None of these involve understanding a system before acting.

The 21 genuine ECC signal artifacts (codebase-onboarding, repo-scan, deep-research, learn, resume-session, workspace-surface-audit, etc.) were folded into the four sub-clusters above as secondary sources.

**Recommendation**: Re-tag the 90 noise artifacts to their actual primary clusters in a future pass.

---

### Artifacts excluded from sub-clusters (non-ECC)

**GBrain infrastructure-coupled skills** (8): `brain-ops`, `query`, `strategic-reading`, `perplexity-research`, `data-research`, `archive-crawler`, `book-mirror`, `concept-synthesis`, `daily-task-prep` — gbrain-specific agents; ideas may deserve a separate `knowledge-management` distillation

**AppyDave brand-sync + utilities** (10): `refresh-*-brain` skills, `brand`, `flihub-integration`, `paperclip`, `browse-with-me`, `frontmatter-indexer`, `knowledge-capture`, `mocha`, `mochaccino-v1`, `gather` — mistagged or adjacent utilities

**BMAD analyst persona**: `bmad-agent-analyst` — belongs in spec-writing cluster

**CE environment config**: `ce-setup`, `ce-update`, `ce-slack-research`, `ce-slack-researcher` — commodity, environment management

---

### Top 3 unified skills that close real gaps in David's stack

#### 1. `brownfield-forensics` — mechanism entirely absent
David has no systematic bug investigation or code archaeology skill. BMAD `bmad-investigate` + gstack `investigate` Iron Law combination fills a real gap. SupportSignal and client work regularly surface "why does this code behave this way?" questions.

#### 2. `pre-action-scan-boot` — context-save/restore missing
No skill for branch-aware working state persistence (decisions made, what was tried, remaining work). gstack save/restore pair fills this. POEM Alex "scan-then-greet" principle needs to be a design rule for any new agent David builds.

#### 3. `domain-research` — BMAD research skills are thin
BMAD's three research skills lack the "planning question anchor" that makes research productive. GSD's planning-question constraint ("What do I need to know to plan this well?") is a one-sentence upgrade to all three.

---

### Top 3 sub-clusters needing David's judgment

#### 1. `repo-onboarding` — parallel mode threshold
`system-context` already exists. When does serial crawl become insufficient? Threshold for switching to 4-agent parallel mode?

#### 2. `pre-action-scan-boot` — overlap with mocha
`context-save/restore` overlaps with `mocha` workspace-level context. Separate skills or new mocha mode?

#### 3. `intent-routing-discovery` — description compression
`brain-query` has 18 flat trigger phrases. gbrain dispatcher-clause compression is low-complexity. Apply now?

---

### Open questions for David

1. **ECC re-tag pass**: 90 ECC fallback noise artifacts in this cluster. Worth a re-tag pass, or leave as acknowledged noise?

2. **GBrain knowledge-management cluster**: 8 gbrain skills (strategic-reading, concept-synthesis, book-mirror, etc.) don't belong here but deserve their own distillation. New `knowledge-management` cluster?

3. **`source-driven-development` routing**: Tagged both `code-implementation` and `system-comprehension`. Which cluster owns it?

---

### Corpus notes

- **ECC (111 of 180)**: 90 fallback noise, 21 genuine signal. Real ECC signal: `codebase-onboarding`, `repo-scan`, `deep-research`, `learn`, `resume-session`, `workspace-surface-audit`.
- **GSD (9 of 69)**: Most structurally rigorous research mechanism. `gsd-phase-researcher` is the most precisely specified research contract in the cluster.
- **BMAD (9 of 69)**: Rich decomposition vocabulary (domain/market/technical) but thin specifications. Vocabulary worth keeping; implementation needs GSD planning-question anchor.
- **Compound-engineering (14 of 69)**: Strongest on anti-stale-docs (version-specific fetching) and session history synthesis.
- **Poem (1 of 69)**: Single artifact, maximum signal density. Alex's scan-then-greet boot pattern is the highest-value idea in the entire cluster.

---

*Distillation pass: Phase 5 catalog:distill — system-comprehension cluster. 90 ECC fallback noise artifacts excluded from sub-clustering; 4 sub-clusters distilled from the 69 real-signal artifacts + 21 genuine ECC. Regenerate after David reviews and approves/adjusts sub-clusters.*

*Distillation pass: Phase 5 catalog:distill — code-review cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Prompt-Engineering Cluster

**Pass**: Phase 5 catalog:distill — prompt-engineering cluster
**Source slice**: `_slice_prompt_engineering.jsonl`
**Source artifact count**: 72
**Sub-cluster count**: 5
**Distillation files**: 5
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [template-author](#template-author) | [prompt-engineering-template-author.md](prompt-engineering-template-author.md) | ~12 | appydave/penny `*new` (poem-os) | PARTIAL — schema-first + description-as-optimizable-parameter outside POEM OS workspace |
| [eval-driven-prompt](#eval-driven-prompt) | [prompt-engineering-eval-driven.md](prompt-engineering-eval-driven.md) | ~14 | superpowers:writing-skills + ecc:eval-harness | YES — no eval loop for skill descriptions in David's stack; RED-GREEN-REFACTOR for skills entirely absent |
| [injection-resistance](#injection-resistance) | [prompt-engineering-injection-resistance.md](prompt-engineering-injection-resistance.md) | ~18 | ecc injection-resistance block + superpowers anti-rationalization | YES — discipline-enforcing skills have no structural bypass defense; 3 new pattern candidates |
| [prompt-schema-design](#prompt-schema-design) | [prompt-engineering-schema-design.md](prompt-engineering-schema-design.md) | ~9 | penny `*generate-schema` + `*validate` (poem-os) | PARTIAL — schema-first discipline + additionalProperties:false + model_tier field not in current Penny outputs |
| [prompt-refine](#prompt-refine) | [prompt-engineering-iterative-refine.md](prompt-engineering-iterative-refine.md) | ~11 | ecc:prompt-optimizer + penny `*refine` | PARTIAL — render-gap-revise loop not available outside POEM OS; WHAT+WHEN+KEYWORDS+NEGATIVE not applied mechanically to existing descriptions |

**Artifacts excluded (solos / off-cluster):**

- ECC language-specific reviewers (40+ agents) — only in slice due to injection-resistance pattern annotation; primary home is code-review cluster
- ECC build-resolver agents — utility agents, not prompt-engineering patterns; stack-specific
- ECC commodity agents (`planner`, `code-architect`, `architect`, etc.) — ideas folded into relevant distillations where non-overlapping
- `ecc:hookify-rules`, `ecc:hookify-help`, `ecc:hermes-imports` — hook/workflow tooling, not prompt-engineering patterns
- `ecc:claude-devfleet`, `ecc:team-builder` — orchestration (covered in orchestration cluster)
- `ecc:cost-aware-llm-pipeline` — ideas folded into schema-design (model_tier field); full cost-routing belongs in an llm-economics distillation

---

### Top 3 gaps closed in David's prompt engineering stack

#### 1. Eval-driven skill development — REAL GAP
David writes skill descriptions and deploys them; there is no eval loop. A description that looks correct can have a trigger rate of 0% (too specific) or 80% (too broad) with no feedback mechanism. Superpowers RED-GREEN-REFACTOR + ECC eval-harness together provide the missing mechanism. The trigger contract YAML makes this engineering rather than guesswork. Directly actionable: write `eval-contract.yaml` alongside any new skill from this point forward.

#### 2. Anti-rationalization + injection resistance — REAL GAP
David's discipline-enforcing skills (TDD, code review, security) are bypassed when agents rationalize around them. ECC injection-resistance blocks and Superpowers anti-rationalization tables are structural defenses that belong in the skill definition itself. Currently absent from every skill in David's stack.

#### 3. Schema-first prompt authoring outside POEM OS — PARTIAL GAP
Penny enforces schema-alongside-template within POEM OS. Outside that context, there is no schema discipline. The `additionalProperties: false` constraint and the `model_tier` field are both missing from current Penny outputs.

---

### Top 2 sub-clusters needing David's judgment

#### 1. `eval-driven-prompt` — eval runner tool selection
Three capable runners: cc-plugin-eval (4-stage, GitHub integration), promptfoo (YAML-based, most community traction), ECC skill-comply (built into ECC harness). Question: adopt promptfoo across all skill development, or use cc-plugin-eval for catalog-specific work?

#### 2. `template-author` + `schema-design` — merge or separate?
Both are steps in Penny's `*new` workflow. Question: one unified `prompt-author` skill with schema-first as a required internal step, or two distinct skills invocable separately?

---

### 7 New prompt-pattern candidates (confirm for `prompt-pattern-vocabulary.md`)

| Pattern ID | Sub-cluster | Source |
|-----------|-------------|--------|
| `eval-driven-skill-development` | eval-driven | ECC eval-harness + mager.co |
| `pressure-scenario-testing` | eval-driven | Superpowers writing-skills |
| `tdd-for-skills` | eval-driven | Superpowers RED-GREEN-REFACTOR |
| `trigger-contract` | eval-driven | mager.co + cc-plugin-eval |
| `anti-rationalization` | injection-resistance | Osmani + Superpowers |
| `bootstrap-injection` | injection-resistance | Superpowers |
| `injection-resistance` | injection-resistance | ECC agent frontmatter baseline |

(3 additional extensions of existing patterns: `hard-gate-state-machine`, `deliberate-context-exclusion`, `cross-project-instinct-promotion` — see `proposals/2026-05-16-prompt-pattern-awareness.md`.)

---

### Evals connection (`sessions/2026-05-16-evals-research.md`)

The evals research established a two-tier eval surface: Tier 1 (trigger contract, all skills) and Tier 2 (output quality, high-stakes skills). The `eval-driven-prompt` distillation is the Tier 1 mechanism. The `injection-resistance` distillation addresses the most common failure mode Tier 1 evals surface. These two sub-clusters are the direct operational output of the evals research file.

---

### Open questions for David

1. **Eval runner**: promptfoo vs cc-plugin-eval vs skill-comply?
2. **Penny update vs new skill**: Should template-author and schema-design fold back into Penny, or become a standalone skill usable outside POEM OS?
3. **7 new pattern candidates**: Add to `prompt-patterns` brain now, or stay catalog-only vocabulary?
4. **`eval_contract_path` schema field**: Add as optional artifact schema field to make evals a catalog dimension?

---

### Corpus notes

- **Everything-claude-code**: 60+ artifacts in this slice; 6 high-signal: `eval-harness`, `skill-comply`, `prompt-optimizer`, `gan-evaluator/generator/planner`.
- **Superpowers**: 3 artifacts, highest pattern density. `writing-skills` RED phase (verbatim rationalisation capture) should be standard for any discipline-enforcing skill.
- **Appydave/POEM OS (Penny)**: Not in slice (David's own ecosystem) but canonical for this cluster. All template-author and schema-design patterns check against her first.
- **Agent-skills-osmani**: 4 artifacts. Anti-rationalization tables ("Rationalization | Reality") are the clearest articulation of the technique in the corpus.

---

*Distillation pass: Phase 5 catalog:distill — prompt-engineering cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Workflow-Architecture Cluster

**Pass**: Phase 5 catalog:distill — workflow-architecture cluster
**Source slice**: `_slice_workflow_architecture.jsonl`
**Source artifact count**: 137
**Sub-cluster count**: 5 (+ workspace-isolation as prerequisite pattern)
**Distillation files**: 6
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [multi-step-plan-writer](#multi-step-plan-writer) | [workflow-architecture-multi-step-plan-writer.md](workflow-architecture-multi-step-plan-writer.md) | ~7 | superpowers:writing-plans | YES — zero-placeholder plan discipline absent from David's stack |
| [plan-executor](#plan-executor) | [workflow-architecture-plan-executor.md](workflow-architecture-plan-executor.md) | ~8 | superpowers:executing-plans | YES — hard-blocking executor with pause/resume gap |
| [agent-team-composer](#agent-team-composer) | [workflow-architecture-agent-team-composer.md](workflow-architecture-agent-team-composer.md) | ~8 | appydave:bmad-story-lifecycle | PARTIAL — bmad-story-lifecycle covers BMAD; general team composition design missing |
| [state-machine-workflow](#state-machine-workflow) | [workflow-architecture-state-machine-workflow.md](workflow-architecture-state-machine-workflow.md) | ~19 | gsd:next | YES — auto-advance oracle entirely absent from David's stack |
| [agent-native-design](#agent-native-design) | [workflow-architecture-agent-native-design.md](workflow-architecture-agent-native-design.md) | ~6 | compound-engineering:ce-agent-native-architecture | YES — direct Kybernesis relevance; agent-native design discipline missing |
| [workspace-isolation](#workspace-isolation) | [workflow-architecture-workspace-isolation.md](workflow-architecture-workspace-isolation.md) | ~6 | superpowers:using-git-worktrees | YES — submodule guard + native-first priority order missing |

---

### Design-time vs runtime boundary

The workflow-architecture cluster is exclusively **design-time**: writing plans, composing teams, defining state machines, architecting agent-native apps, setting up workspace isolation. This is what happens *before* execution begins.

The **runtime** counterpart is the orchestration cluster (already distilled): autonomous-pipeline-runner, parallel-review-fan-out, agent-lifecycle-coordinator. These consume the designs produced by workflow-architecture skills.

The boundary is load-bearing. Mixing design and runtime concerns in one skill produces artifacts that are either too prescriptive at runtime or too passive at design time. Keep them separate.

---

### Folded / excluded artifacts

**Already covered in other cluster distillations**:
`agent-orchestrator`, `workflow-orchestrator`, `ruflo-swarm-check` → orchestration-workflow-design-advisor. `tdd-workflow` → code-implementation-tdd-discipline.

**ECC domain-specific pipelines (not David's stack)**:
`django-tdd`, `laravel-tdd`, `quarkus-tdd`, `springboot-tdd`, `*-verification` variants, `golang-testing`, `cpp-testing`, `kotlin-testing`, `perl-testing`, `rust-testing` — 13 language-specific TDD pipelines. Pattern documented; no new distillation needed.

**ECC domain-specific operations (not design-time workflow)**:
`email-ops`, `finance-billing-ops`, `google-workspace-ops`, `messages-ops`, `unified-notifications-ops`, `terminal-ops`, `lead-intelligence`, `research-ops`, `jira-integration`, `healthcare-eval-harness`, `patent-database`, `social-graph-ranker`, `gget`, `literature-review`, `network-bgp-diagnostics` — 15 operational/domain pipelines excluded.

**ECC solos flagged for future distillations**:
- `gateguard` — fact-forcing gate (blocks Edit/Write before investigation). Solo; mechanism worth lifting into discipline-enforcing skills.
- `strategic-compact` — manual context compaction advisor. Solo; relevant for long-context workflows.
- `ecc-tools-cost-audit` — evidence-first billing audit. Solo.
- `skill-scout` — search existing skills before creating new ones. Solo.

**Ruflo workflow stubs (infrastructure-bound)**:
`agent-automation-smart-agent`, `agent-workflow-automation`, `workflow-automation`, `Hooks Automation`, `V3 CLI Modernization`, `github-automation` — Ruflo-infrastructure-specific.

**gstack setup utilities (project setup, not workflow architecture)**:
`gstack-upgrade`, `plan-tune`, `setup-browser-cookies`, `setup-deploy`, `setup-gbrain`.

**POEM slides workflow (content production, not workflow architecture)**:
`poem-slides-workflow`, `poem-slides` → belongs in content-production cluster.

---

### Top 3 gaps closed in David's stack

#### 1. `state-machine-workflow` — auto-advance oracle gap
David has no mechanism for "what's next on the project?" that reads project state. Session resumption currently requires manually reconstructing context. GSD's `gsd:next` oracle reads artifacts, detects current state, and routes. Most immediately actionable gap in this cluster.

#### 2. `multi-step-plan-writer` — zero-placeholder plan discipline gap
David has `agent-orchestrator` (coordination design) but no skill enforcing "the plan is done when a fresh agent can execute it cold." Superpowers' `writing-plans` discipline (scope check, complexity assessment, bite-sized TDD tasks, zero placeholder) is the standard. Without it, plans are written at outline level and the executor fills gaps mid-execution.

#### 3. `agent-native-design` — Kybernesis architecture gap
CE's `ce-agent-native-architecture` directly addresses the design paradigm Kybernesis is built on. David has no dedicated skill for "design an application where agents are the product." Five principles (Parity, Granularity, Composability, Emergent Capability, Improvement Over Time) + 14-topic intake menu. Directly useful for Kybernesis architecture sessions.

---

### Top 3 sub-clusters needing David's judgment

#### 1. `state-machine-workflow` — GSD as system vs GSD as patterns
GSD is a full npm-installable system (81 artifacts, its own CLI). Adopt GSD directly (`npm install -g gsd`) or extract only the patterns (state detection, auto-advance, dependency analysis) into appydave-plugins? Adopting GSD gives 19 commands immediately; extracting patterns gives a lightweight owned implementation. Highest-stakes decision from this cluster.

#### 2. `agent-team-composer` — boundary with workflow-design-advisor
The orchestration distill produced `workflow-design-advisor` (sequential vs swarm topology). This cluster produces `agent-team-composer` (given a swarm, which agents and roles?). Are these genuinely two skills or one with two modes? Two is more composable; one is more ergonomic.

#### 3. `workspace-isolation` — EnterWorktree availability
The `EnterWorktree` deferred tool is listed in system-reminder. Before building `workspace-isolation`, determine whether `EnterWorktree` is the right native tool or whether manual `git worktree add` is more reliable in David's workflow.

---

### Open questions for David

1. **GSD adoption decision**: Adopt as npm package vs extract patterns? Most impactful decision from this cluster.
2. **Plan location convention**: `docs/superpowers/plans/` vs `_bmad-output/implementation-artifacts/` vs other. Auto-detect project type?
3. **`plan-executor` subagent delegation**: Auto-delegate to subagents when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set, or always run in-process?

---

### Corpus notes

- **Everything-claude-code**: 77 of 137. Low signal-to-noise in this cluster — majority are domain-specific pipelines irrelevant to David's stack. High-signal exceptions: `plan-orchestrate`, `feature-dev`, `prp-*` series, `quality-gate`, `ralphinho-rfc-pipeline`, `ce-agent-native-architecture`.
- **GSD**: 19 of 137. Most coherent system in cluster — every command is part of one state-machine model. `gsd:next` oracle is the single most useful artifact for David's daily workflow in this cluster.
- **Superpowers**: 3 of 137. Highest mechanism density. `writing-plans` + `executing-plans` form a complete plan→execute contract entirely absent from David's current stack.
- **Compound-engineering**: 2 of 137. `ce-agent-native-architecture` is the highest-quality architecture skill in the corpus for agent-native design. 14-topic intake menu is a complete architecture review checklist.
- **Appydave**: 17 of 137. Existing stack is the baseline; gaps are in design-time methodology, not coordination tooling (already covered in orchestration distill).

---

*Distillation pass: Phase 5 catalog:distill — workflow-architecture cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Documentation Cluster

**Pass**: Phase 5 catalog:distill — documentation cluster
**Source slice**: `_slice_documentation.jsonl`
**Source artifact count**: 75
**Sub-cluster count**: 5 (4 new skills + 1 upgrade)
**Distillation files**: 4 + 1 upgrade candidate
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [pr-description-gen](#pr-description-gen) | [documentation-pr-description-gen.md](documentation-pr-description-gen.md) | 4 | compound-engineering:ce-commit-push-pr | YES — PR authoring step entirely missing from David's stack |
| [changelog-author](#changelog-author) | [documentation-changelog-author.md](documentation-changelog-author.md) | 5 | gstack:document-release | YES — post-ship doc maintenance + changelog generation missing |
| [doc-review-suite](#doc-review-suite) | [documentation-doc-review-suite.md](documentation-doc-review-suite.md) | 12 | appydave:doc-review (suite) — UPGRADE | PARTIAL — suite exists; 3 optional new dimensions (editorial-structure, comment-accuracy, factual-verification) |
| [doc-write](#doc-write) | [documentation-doc-write.md](documentation-doc-write.md) | 10 | gsd:docs-update | YES — full doc generation with verification-by-default; system-context is partial coverage only |
| [adr-author](#adr-author) | [documentation-adr-author.md](documentation-adr-author.md) | 3 | agent-skills-osmani:documentation-and-adrs | YES — no dedicated ADR skill in David's stack |

---

### Artifacts not sub-clustered (solos / excluded)

**Brand-specific identity (appydave-plugins):** `brand`, `who-am-i`, `ecosystem-locations`, `context-modes`, `poem-slides-workflow`, `curate-templates`, `scene-deck`, `solo-deck`, `appydave-thumbnail` — Brand Dave-specific or content production; not portable.

**Mochaccino / design ecosystem:** `mocha`, `shelly`, `mochaccino`, `ux-writer`, `ux-review` — UX cluster. `workflow-orchestrator`, `agent-orchestrator`, `agentic-capability`, `architect` — planning cluster.

**Utilities:** `easy-git`, `screenshot-tour` (one-of-a-kind, no peers), `clipboard-intake`, `nano-banana`, `ruflo`, `review-unit-tests`.

**Specialist/infra tools:** `google-workspace-ops`, `visa-doc-translate`, `jira`, `ecc-guide`.

**Ruflo stubs / SPARC methodology:** `agent-docs-api-openapi`, `agent-pseudocode`, `ruflo-browser`, `ruflo-docs`, `ruflo-sparc`, `sparc-orchestrator`, `sparc-methodology` — planning cluster; Ruflo-infra-dependent. `AgentDB Vector Search` — implementation, not documentation.

**Publishing/output tools:** `gbrain:brain-pdf`, `gbrain:publish`, `gstack:make-pdf`, `ce-proof`, `ce-demo-reel`.

**Knowledge-management boundary (review in Stage 8):** `doc-review-crossref`, `bmad-index-docs`, `ruflo-knowledge-graph:graph-navigator` — tag both `documentation` and `knowledge-capture`; confirm in librarian distill.

---

### Top 3 gaps closed in David's existing documentation stack

#### 1. PR description authoring (`documentation-pr-description-gen`) — REAL GAP
David has `pr-lifecycle` (resolve feedback) but nothing for writing the PR description before the PR opens. CE's `ce-commit-push-pr` — adaptive depth, evidence decision tree, `--body-file` correctness — is the most complete mechanism in the corpus. Immediately actionable.

#### 2. Full doc generation with verification (`documentation-doc-write`) — REAL GAP
David has `system-context` (CONTEXT.md only). No skill generates the full documentation set with factual verification. GSD's verification-by-default is the key insight: AI-generated docs without verification routinely contain wrong commands and dead import paths.

#### 3. Post-ship doc maintenance (`documentation-changelog-author`) — REAL GAP
No existing skill handles post-ship doc update — cross-referencing what shipped against what docs claim, updating stale entries. `gstack:document-release` is the mechanism. High-frequency gap: every behavior-changing PR risks making existing docs stale.

---

### Top 2 sub-clusters needing David's judgment

#### 1. `doc-review-suite` — which new dimensions to build?
Suite exists and is the winner. Question: build D7-D9 and in what order. Distillation recommends D7 (editorial-structure) first — lowest cost. D8 (comment-accuracy) second. D9 (factual-verification) last — highest cost, niche use.

#### 2. `adr-author` — standalone vs `doc-write --type=adr`?
Small cluster. Standalone more ergonomic; bundled reduces maintenance. David's call.

---

### Open questions for David

1. **`system-context` fate**: Alias to `doc-write --type=context` or stay standalone?
2. **`ce-demo-reel` gap**: `pr-description-gen` uses `ce-demo-reel` for evidence capture. David doesn't have it. Skip (user provides URL), or build lightweight screenshot path?
3. **SPARC placement**: Confirm `sparc-methodology` variants belong in planning cluster, not documentation.
4. **Librarian boundary**: `doc-review-crossref`, `bmad-index-docs`, `knowledge-graph-navigator` — confirm Stage 8 assignment.

---

### Corpus notes

- **Appydave-plugins**: 35 of 75. Strong review coverage (doc-review suite is the winner). Weak authoring coverage — no PR description, no changelog, no full doc generation.
- **GSD**: 5 artifacts. `docs-update` + `gsd-doc-writer` + `gsd-doc-verifier` is the most complete doc-generation system. Verification-by-default is the most important architectural idea.
- **Compound-engineering**: 5 artifacts. `ce-commit-push-pr` is the PR description winner. `ce-release-notes` is a consumer tool (reads external releases), not a producer tool.
- **BMAD**: 6 artifacts. Brownfield onboarding and structural editing are the two portable ideas. Persona wrappers set aside.
- **Ruflo**: 10 artifacts. All Ruflo-infra-dependent stubs or SPARC methodology. Zero contributions to documentation distillations.
- **ECC**: 8 artifacts. `comment-analyzer` is the unique contribution (code-comment accuracy for Dimension 8).

---

*Distillation pass: Phase 5 catalog:distill — documentation cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Spec-Writing Cluster

**Pass**: Phase 5 catalog:distill — spec-writing cluster
**Source slice**: `_slice_spec_writing.jsonl`
**Source artifact count**: 157
**Sub-cluster count**: 5 (+ excluded)
**Distillation files**: 5
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [requirements-capture](#requirements-capture) | [spec-writing-requirements-capture.md](spec-writing-requirements-capture.md) | ~30 | appydave-plugins:skill:spec-writer | PARTIAL — winner already in stack; 4 non-overlapping ideas to fold in |
| [prd-lifecycle](#prd-lifecycle) | [spec-writing-prd-lifecycle.md](spec-writing-prd-lifecycle.md) | ~10 (BMAD dominant + ECC) | bmad-method:skill:bmad-prd | YES — product-level PRD lifecycle missing; spec-writer covers features, not products |
| [clarification-loop](#clarification-loop) | [spec-writing-clarification-loop.md](spec-writing-clarification-loop.md) | ~5 (osmani + BMAD + spec-kit + GSD) | agent-skills-osmani:skill:interview-me | YES — pre-spec elicitation entirely absent from David's stack |
| [constitution-style](#constitution-style) | [spec-writing-constitution-style.md](spec-writing-constitution-style.md) | ~2 (spec-kit only) | spec-kit:command:constitution | CONDITIONAL — low value for solo projects; high value for Kybernesis and SupportSignal |
| [document-review](#document-review) | [spec-writing-document-review.md](spec-writing-document-review.md) | ~10 (CE dominant + spec-kit + appydave) | compound-engineering:skill:ce-doc-review | YES — requirements/plan doc review before implementation; entirely absent (David's doc-review covers knowledge docs, not spec docs) |
| [product-strategy](#product-strategy) | [spec-writing-product-strategy.md](spec-writing-product-strategy.md) | ~7 (CE + ECC + BMAD) | compound-engineering:skill:ce-strategy | YES — STRATEGY.md as machine-readable grounding doc entirely absent |

---

### Artifacts excluded from sub-clusters

**Ruflo domain-specific agents (~22 artifacts)** — domain worker agents within the Ruflo stack; not portable spec-writing patterns.

**ECC off-cluster artifacts (~40 artifacts)** — implementation/code-review skills (accessibility, deployment-patterns, e2e-testing, etc.) co-tagged with spec-writing signals but belonging in other clusters.

**True solos / adjacent skills** — `five-personas`, `scope-analyst`, `architect`, `plan-orchestrate`, `gateguard`, `ce-proof`, `gsd-roadmapper` — each belong in other clusters or are one-of-a-kind.

---

### Heavy spec-first vs lightweight: the core tension surfaced

The 157 artifacts divide sharply into two philosophies:

**Heavy spec-first (spec-kit + BMAD)**
- Spec is the primary artifact; code serves the spec
- Pipeline: `constitution → specify → clarify → plan → tasks → implement`
- PRD as versioned, evolving source of truth; constitutional principles as immutable constraints
- spec-kit: the most architecturally complete SDD implementation in the corpus (9 phases, 30+ AI agent targets)
- BMAD: the most process-mature PRD lifecycle (versioned, intent-routed, lifecycle-managed)

**Lightweight (ECC + Osmani + CE)**
- Spec as a time-bounded artifact that answers WHAT before HOW begins
- CE brainstorm: right-size ceremony to work size; YAGNI applied to process
- ECC plan-prd: lean PRD, 4 phases, anti-fluff, no implementation detail

**David's current position**: lightweight (`spec-writer` is the only spec-writing skill in the stack). The gap is not more ceremony — it is three specific missing mechanisms (see gaps below).

---

### Top 3 gaps closed in David's spec-writing stack

#### 1. Pre-spec elicitation (`spec-writing-clarification-loop`) — REAL GAP
David has no skill for structured pre-spec elicitation. `spec-writer` immediately transforms whatever it receives — if the brainstorm is thin or wrong, the spec inherits those defects silently. Osmani's `interview-me` (one-question-at-a-time, 95% confidence threshold) fills this gap. Directly actionable: add `clarify` before `spec-writer` for any request where intent is unclear.

#### 2. Post-spec document review (`spec-writing-document-review`) — REAL GAP
David has no mechanism for reviewing a requirements document before planning begins. CE's `ce-doc-review` (7 parallel specialist agents: adversarial, coherence, feasibility, product, scope, security, spec-flow) is production-tested and directly actionable. The headless mode makes it usable in autonomous pipelines. Most immediately actionable for SupportSignal (NDIS compliance, PII, auth complexity).

#### 3. Product-level strategy anchor (`spec-writing-product-strategy`) — REAL GAP
David's spec-writing is feature-level. There is no product-level STRATEGY.md that downstream specs read as grounding. CE's `ce-strategy` produces a short, durable, machine-readable anchor. Most urgent for Kybernesis (3 founders, external capital, strategic direction needs to be explicit and shared).

---

### Top 2 sub-clusters needing David's judgment

#### 1. `constitution-style` — when does a project actually need one?
Only 2 artifacts (both spec-kit). Mechanism is sound but low-value for solo AppyDave projects. High value for Kybernesis (3 founders, multi-session, strategic constraints) and SupportSignal (compliance, PII). Does CLAUDE.md already fill this role?

#### 2. `prd-lifecycle` — new skill or `spec-writer` with scope routing?
BMAD's PRD lifecycle is the right mechanism for product-level requirements. Question: separate `prd-lifecycle` skill, or `spec-writer` detects scope and self-routes?

---

### Open questions for David

1. **`scope-analyst` placement**: Adjacent to clarification-loop; assess as upgrade or standalone.
2. **`spec-review` naming collision**: `doc-review` already exists for brain documents. `spec-review` vs upgraded `doc-review` that routes by document type?
3. **Superpowers HARD-GATE**: `<HARD-GATE>` — no code until design is approved. Should this be added to `spec-writer` or `goal-plan`?

---

### Corpus notes

- **ECC (54 of 157)**: 40+ off-cluster. Genuine signal: `prp-prd`, `plan-prd`, `product-lens`, `product-capability`. ECC's `prp-prd` (hypothesis-driven, 3 question sets + research + generate) is the most rigorous lightweight PRD process in the corpus.
- **BMAD (18 of 157)**: Most mature PRD lifecycle. Consolidation of create/edit/validate into one intent-routed `bmad-prd` is the key pattern to adopt regardless of BMAD tooling adoption.
- **spec-kit (10 of 157)**: Most architecturally complete SDD system. High ceremony; best for team/multi-agent contexts. Key portable ideas: numbered artifact IDs, post-spec `clarify` pass, immutable-principles model.
- **Compound-engineering (14 of 157)**: Highest signal-per-artifact. `ce-doc-review` (7 parallel agents) and `ce-strategy` (STRATEGY.md as grounding) are both directly actionable. CE treats the spec-writing pipeline as agent-native and headless-capable.
- **Ruflo (28 of 157)**: 22 are domain-specific agents. Not distillable into unified skills.

---

*Distillation pass: Phase 5 catalog:distill — spec-writing cluster. 157 artifacts; 5 sub-clusters distilled; ~62 artifacts excluded (Ruflo domain agents, ECC off-cluster, solos). Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Verification-Validation Cluster

**Pass**: Phase 5 catalog:distill — verification-validation cluster
**Source slice**: `artifacts/_slice_verification_validation.jsonl`
**Source artifact count**: 160
**Sub-cluster count**: 5 (+ excluded)
**Distillation files**: 5
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| pre-completion-gate | [verification-validation-pre-completion-gate.md](verification-validation-pre-completion-gate.md) | ~12 (superpowers + gsd + ecc + gstack) | superpowers:verification-before-completion | YES — evidence discipline entirely absent from David's stack |
| spec-conformance | [verification-validation-spec-conformance.md](verification-validation-spec-conformance.md) | ~18 (spec-kit + bmad + gsd + ce + appydave) | gsd:gsd-plan-checker | UPGRADE — review-acceptance-auditor exists; plan-check + flow-gap + scope-reduction-detection are the gaps |
| data-integrity-gate | [verification-validation-data-integrity-gate.md](verification-validation-data-integrity-gate.md) | ~11 (compound-engineering dominant) | compound-engineering:ce-deployment-verification-agent | YES — no Go/No-Go data deploy checklist in David's stack; SupportSignal NDIS PII makes this urgent |
| confidence-gate | [verification-validation-confidence-gate.md](verification-validation-confidence-gate.md) | ~8 (compound-knowledge + bmad + gstack + gsd) | compound-knowledge:kw-confidence | YES — epistemic gate absent; distinct from doubt-driven (self-assessment vs fresh-context reviewer) |
| test-quality | [verification-validation-test-quality.md](verification-validation-test-quality.md) | ~15 (superpowers + ruflo + spec-kit + ecc + gbrain + gsd) | superpowers:test-driven-development | UPGRADE — TDD Iron Law + Nyquist latency constraint + regression red-green-revert discipline absent |
| system-health-scan | [verification-validation-system-health-scan.md](verification-validation-system-health-scan.md) | ~14 (gstack + gbrain + gsd + ce + ruflo) | compound-engineering:ce-product-pulse | YES — no post-deploy health pulse or smoke test in David's stack |

---

### Overlap with code-review cluster

Double-tagged artifacts resolved: `ce-schema-drift-detector` and `verification-before-completion` go to verification-validation (operational gates, not quality judgments). `ce-correctness-reviewer` stays code-review. `ce-data-integrity-guardian` is dual-cluster.

---

### Top 3 gaps closed

1. `pre-completion-gate` — honesty infrastructure gap. Iron Law + Gate Function entirely absent. High priority for autonomous work.
2. `data-integrity-gate` — SupportSignal NDIS PII urgency. SQL invariants, rollback classification, schema drift detection. Directly applicable today.
3. `confidence-gate` — unique in the corpus. Only epistemic self-assessment skill across all 160 artifacts. Complements doubt-driven.

---

### Top 2 gaps NOT distilled

1. Debugging cluster: `systematic-debugging` (Superpowers Iron Law approach) — needs own pass.
2. Performance cluster: `ce-performance-oracle` + Ruflo benchmarkers — needs own pass.

---

### 1 open question

**skill or hook?** Pre-completion-gate should ideally fire as a `PostToolUse` hook on commit/push, not as an invoked skill. David decides.

---

*Distillation pass: Phase 5 catalog:distill — verification-validation cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Knowledge-Capture Cluster

**Pass**: Phase 5 catalog:distill — knowledge-capture cluster
**Source slice**: `_slice_knowledge_capture.jsonl`
**Source artifact count**: 201
**Sub-cluster count**: 6 (+ 1 ADR specialist)
**Distillation files**: 6
**Created**: 2026-05-17

---

### Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [learning-instinct-promotion](#learning-instinct-promotion) | [knowledge-capture-learning-instinct-promotion.md](knowledge-capture-learning-instinct-promotion.md) | ~20 (ECC dominant + CE + appydave) | everything-claude-code:continuous-learning-v2 | YES — quality gate + lifecycle (promote/prune/evolve) missing from David's manual knowledge-capture |
| [session-handover](#session-handover) | [knowledge-capture-session-handover.md](knowledge-capture-session-handover.md) | ~11 (appydave dominant + GSD) | appydave-plugins:capture-context | PATTERN — already exists; cross-session thread + trigger-condition seed are the gaps |
| [brain-curation](#brain-curation) | [knowledge-capture-brain-curation.md](knowledge-capture-brain-curation.md) | ~14 (appydave + gbrain + CK) | appydave-plugins:lexi | PARTIAL — tiered enrichment (T2/T3), concept dedup, staleness-on-write are missing |
| [wearable-ambient-ingest](#wearable-ambient-ingest) | [knowledge-capture-wearable-ambient-ingest.md](knowledge-capture-wearable-ambient-ingest.md) | ~13 (appydave dominant + gbrain) | appydave-plugins:omi | PARTIAL — OMI pipeline exists; Krisp/YouTube/Wistia not routed into same backlog layer |
| [multi-source-researcher](#multi-source-researcher) | [knowledge-capture-multi-source-researcher.md](knowledge-capture-multi-source-researcher.md) | ~20 (CE + gbrain + ruflo) | compound-engineering:ce-best-practices-researcher | YES — no general research synthesizer in David's stack (only system-specific `gather`) |
| [memory-store-retrieve](#memory-store-retrieve) | [knowledge-capture-memory-store-retrieve.md](knowledge-capture-memory-store-retrieve.md) | ~27 (ruflo dominant + ECC + CK) | everything-claude-code:ck | ASSESSMENT — Ruflo has most sophisticated memory architecture; zero-dep path is `ck`; infrastructure gap real but not blocking today |
| [adr-documentation](#adr-documentation) | [knowledge-capture-adr-documentation.md](knowledge-capture-adr-documentation.md) | ~5 (ECC + osmani + appydave) | everything-claude-code:architecture-decision-records | YES — no ADR skill in David's stack; session-contextual capture is the mechanism gap |

---

### Artifacts not sub-clustered (solos / excluded)

**Ruflo domain-specific stubs (~30 artifacts)**: Neural-trading/financial domain agents and infrastructure (`backtest-engineer`, `market-analyst`, `risk-analyst`, `trading-strategist`, `data-engineer`, `agent-coordination`, `coder`, `testgen`, `goal-planner`). Not portable.

**AgentDB infrastructure artifacts (~8 ruflo)**: `AgentDB *`, `ReasoningBank with AgentDB`, `agentdb`, `agentdb-specialist`, `agent-swarm-memory-manager`. Require AgentDB daemon. Vocabulary captured in memory-store-retrieve distillation.

**ECC stack-locked patterns (~10)**: `cpp-review`, `cpp-reviewer`, `cpp-testing`, `swift-reviewer`, `swiftui-patterns`, `pytorch-patterns`, `redis-patterns`, `backend-patterns`. C++/Swift/PyTorch stacks.

**True solos**: `appydave:conversation-triage` (orchestration cluster), `appydave:relay-register` (infrastructure), `appydave:truth-trail` (referenced in ADR distillation), `appydave:skill-eval-loop` (skill-authoring cluster), `ecc:santa-method` (orchestration cluster), `compound-knowledge:kw:brainstorm/plan/work` (full kw:* workflow suite; its own product).

---

### Top 2 gaps in David's stack

#### 1. No general research synthesizer (`multi-source-researcher`) — REAL GAP
David has no general research skill — only `gather` (internal systems) and individual transcript fetchers. Before any significant implementation or brain-update task, David starts cold. CE's `ce-best-practices-researcher` (three-layer: local knowledge first, then versioned docs, then web) closes this directly. `strategic-reading` and `ce-git-history-analyzer` extend it for David's specific use cases.

#### 2. No quality gate on knowledge promotion (`learning-instinct-promotion`) — REAL GAP
David's `knowledge-capture` writes directly to MEMORY.md with no confidence scoring, dedup check, or lifecycle. Memory files accumulate stale, conflicting, duplicate entries over time. ECC's `continuous-learning-v2` + `/evolve` + `/prune` is the complete mechanism. `kw:compound`'s dedup-before-write pattern is the single most immediately useful fold-in.

---

### Top 3 sub-clusters needing David's judgment

#### 1. `memory-store-retrieve` — infrastructure decision
Ruflo has the most sophisticated memory architecture in the corpus (AgentDB, ReasoningBank, vector-space, knowledge graphs). None adoption-ready for David's solo setup today. When does `ck` + grep become insufficient? This matters most for Kybernesis architecture.

#### 2. `learning-instinct-promotion` — hook automation decision
`continuous-learning-v2` fires automatically on the Claude Code `Stop` hook. David's `knowledge-capture` is fully manual. Auto-extraction adds continuous-background capture but also noise. Does David want the automatic layer?

#### 3. `wearable-ambient-ingest` — unified query layer decision
Krisp, YouTube, and Wistia transcripts are siloed from the OMI routing layer. Unify under `query_transcripts` CLI (more powerful, interface change) or keep source-specific queries (lower friction, permanent fragmentation)?

---

### Open question for David

**Kybernesis memory architecture**: Ruflo's AgentDB is the most complete agent-memory abstraction in the corpus. Evaluate it as a design reference before committing to a KyberBot memory architecture. The vocabulary (ReasoningBank reasoning traces, RJAR retrieval cycle, per-agent-scoped AgentDB) is worth a design session before the architecture crystallises.

---

### Corpus notes

- **Ruflo (59 of 201)**: Memory architecture vocabulary is the primary contribution. AgentDB and ReasoningBank are the best-documented agent-memory abstractions in the corpus. Not adoption-ready today but essential design vocabulary for Kybernesis.
- **Everything-Claude-Code (38 of 201)**: Strongest learning/instinct lifecycle. `ck` is most directly adoptable zero-dep memory tool. `continuous-learning-v2` + lifecycle is the complete learning system.
- **AppyDave (37 of 201)**: Already in David's stack. OMI pipeline and `lexi` are strongest. Session-handover family is best in corpus — no mechanism gaps, only adjacent features missing.
- **GBrain (29 of 201)**: Most sophisticated brain-curation and ambient-ingest patterns. `concept-synthesis`, tiered enrichment (T2/T3), and `strategic-reading` are the three ideas most worth lifting.
- **Compound-Engineering (13 of 201)**: `ce-best-practices-researcher` and `ce-issue-intelligence-analyst` are directly applicable. Dual-track bug/knowledge schema is the most immediately useful `knowledge-capture` fold-in.
- **Compound-Knowledge (7 of 201)**: `kw:compound`'s dedup-before-write is the single most immediately useful idea for `knowledge-capture`.

---

*Distillation pass: Phase 5 catalog:distill — knowledge-capture cluster. 201 artifacts; 6 sub-clusters + 1 ADR specialist distilled; ~65 artifacts excluded (Ruflo domain agents, ECC stack-locked, solos). Regenerate after David reviews and approves/adjusts sub-clusters.*

---

## Planning Cluster

**Source**: 132 artifacts across 12 repos. 6 distillation files written (+ a per-cluster INDEX). 1 main-INDEX-append failed mid-write 2026-05-17 — section appended retroactively here. **See [planning-INDEX.md](planning-INDEX.md) for full per-cluster synthesis** (granularity observation, overlap watch, top-3 gaps).

**Sub-clusters**:

| Sub-cluster | File | Winner | Gap |
|-------------|------|--------|-----|
| ideation-and-requirements | [planning-ideation-and-requirements.md](planning-ideation-and-requirements.md) | `compound-engineering:ce-brainstorm` | PARTIAL — new mechanism (one-question-per-turn) vs your `goal-plan` |
| roadmap-architect | [planning-roadmap-architect.md](planning-roadmap-architect.md) | `gsd:gsd-roadmapper` | YES — goal-backward roadmapping + coverage validation absent |
| sprint-planner | [planning-sprint-planner.md](planning-sprint-planner.md) | `gsd:gsd-planner` | YES — mid-horizon decomposition between epic and task is missing |
| task-breakdown | [planning-task-breakdown.md](planning-task-breakdown.md) | `compound-engineering:ce-plan` | YES — guardrails-over-choreography + no-placeholders rule absent |
| session-and-context-continuity | [planning-session-and-context-continuity.md](planning-session-and-context-continuity.md) | `appydave:session-checkpoint` | PARTIAL — machine-parseable STATE.md format is the gap |
| dependency-and-risk | [planning-dependency-and-risk.md](planning-dependency-and-risk.md) | `gsd:analyze-dependencies` | YES — dependency graph + critical path + hidden-assumption surfacing absent |

**Key structural finding**: planning artifacts span three granularities (epic / sprint / task) that different repos conflate as one thing. BMAD operates at epic-level, GSD at sprint-level, spec-kit at task-level. The mid-horizon (sprint) is the most underserved layer in David's current stack.

---

## Security-Review Cluster

**Source**: 66 artifacts. 4 distillation files written. 1 main-INDEX-append failed mid-write 2026-05-17 — section appended retroactively here. **Newly-promoted cluster** (2026-05-16 from `cluster-vocabulary-additions.md`).

**Sub-clusters**:

| Sub-cluster | File | Notes |
|-------------|------|-------|
| agent-config-scan | [security-review-agent-config-scan.md](security-review-agent-config-scan.md) | Scan agent / skill / hook configs for misconfigurations and overprivileged tool grants |
| compliance-overlay | [security-review-compliance-overlay.md](security-review-compliance-overlay.md) | Compliance-flavoured audit overlay (SOC2 / WCAG / NDIS-style frameworks) |
| prompt-injection-defense | [security-review-prompt-injection-defense.md](security-review-prompt-injection-defense.md) | Pairs with prompt-engineering's injection-resistance pattern; ECC's Prompt Defense Baseline is the seed |
| secret-detection | [security-review-secret-detection.md](security-review-secret-detection.md) | Pre-commit / pre-push secret scanning (gitleaks-style, plus prompt-aware variants) |

**Coverage observation**: your current stack has `prompt-injection-scanner` + `security-analyst` — narrow vs the 4 sub-clusters surfaced. The 3 absent capabilities (agent-config-scan, compliance-overlay, secret-detection in your harness) are all stack-agnostic gaps.

