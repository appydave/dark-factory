---
distillation_id: verification-validation-data-integrity-gate
stage: verification
intent: "Go/No-Go gate for production data changes — SQL verification, rollback plan, migration safety, schema drift detection"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:agent:ce-deployment-verification-agent
  - compound-engineering:agent:ce-schema-drift-detector
  - compound-engineering:agent:ce-data-integrity-guardian
  - compound-engineering:agent:ce-data-migrations-reviewer
  - compound-engineering:agent:ce-data-migration-expert
  - gsd:command:audit-uat
  - gsd:agent:gsd-nyquist-auditor
  - appydave-plugins:skill:truth-trail
winner_mechanism: compound-engineering:agent:ce-deployment-verification-agent
---

# Unified Skill: verification-validation-data-integrity-gate

**Purpose**: Pre-deploy safety gate for changes touching production data. Generates concrete, executable Go/No-Go checklists: invariant definition, SQL verification queries, rollback plan, and post-deploy monitoring. Distinct from code review — this is data safety, not code quality.

**For Agents**: Use when a PR or migration touches database tables, data models, backfills, or data transformations. Also use when David says "is this migration safe?", "what's the rollback plan?", "check data integrity", "schema drift", "deploy checklist". NOT a substitute for code review — it focuses on data safety invariants.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Prevent data loss, corruption, and silent integrity failures in production deployments. The core failure modes being prevented:

1. **Irreversible schema changes** deployed without a rollback path
2. **Schema drift** — unrelated schema.rb changes from other branches included in a PR
3. **Migration without invariants** — no pre/post verification queries to confirm correctness
4. **Silent data corruption** — backfills that succeed structurally but produce wrong values

## Winner's Mechanism

`compound-engineering:agent:ce-deployment-verification-agent` wins. It is the only artifact in the corpus that produces a **complete, executable Go/No-Go checklist** rather than a review report. Key mechanism:

1. **Define invariants first** — "What must remain true before/after deploy?" Named constraints, not vague checks. Forces the deployer to think about correctness before running anything.
2. **Pre-deploy SQL audit queries** (read-only) — baseline counts, null checks, mapping verification. "Save these values" — creates a measurable baseline for post-deploy comparison.
3. **Migration/backfill steps table** — each step gets: command, estimated runtime, batching approach, rollback procedure. This prevents ad-hoc "let me just run it and see."
4. **Post-deploy verification within 5 minutes** — concrete SQL queries proving the migration completed correctly, not error rates. Compares against pre-deploy baseline.
5. **Explicit rollback classification** — four states: Yes (dual-write), Yes (backup), Partial (code revert + manual fix), No (document why acceptable). The "No" case being explicit and documented is the key discipline.
6. **24-hour monitoring plan** — metrics, alert conditions, dashboard links. Not just "watch the logs" — specific thresholds.

The `ce-deployment-verification-agent` is production-tested at EveryInc against real Rails migrations. The SQL patterns and invariant templates are concrete enough to use immediately.

## Overlap with code-review cluster

There is **explicit overlap** with `ce-data-integrity-guardian` and `ce-data-migrations-reviewer` from the code-review cluster. The distinction:

- **Code-review cluster**: Reviews the migration code for ACID properties, constraint correctness, transaction boundaries, PII handling. Asks: "Is the migration code correct?"
- **This cluster**: Generates the deployment operational checklist. Asks: "How do we safely deploy this migration and verify it succeeded?"

These are complementary. The code reviewer catches logic errors before merge; the deployment gate generates the execution plan for deploy day. David likely needs both — the code-review pass first, then this gate before `git push --production`.

## Non-overlapping ideas folded in

- From `compound-engineering:agent:ce-schema-drift-detector`: **Schema drift detection** — cross-reference schema.rb changes against migrations actually in the PR. Detects the failure mode where developers pull base branch, run all migrations, then commit schema.rb — polluting the PR with unrelated schema changes. Specific git commands provided (`git diff <base> --name-only -- db/migrate/`). — `complexity: low | optional: false | prerequisite: "Rails project with schema.rb"`. This is a quick pre-check that should run BEFORE any deployment verification.

- From `compound-engineering:agent:ce-data-integrity-guardian`: **Privacy compliance layer** — identify PII fields, check encryption for sensitive data, verify data retention policies, GDPR right-to-deletion compliance. Particularly relevant for SupportSignal (NDIS app with personal health data). — `complexity: medium | optional: true | prerequisite: "PR involves fields that may contain PII or health data"`. SupportSignal clients have NDIS participants whose data is highly regulated.

- From `compound-engineering:agent:ce-data-migration-expert`: **Long-running operation risk assessment** — estimates table-lock risk, recommends batching strategies, identifies whether the migration needs a maintenance window vs can run live. — `complexity: medium | optional: false | prerequisite: "migration touches large tables or adds NOT NULL columns"`

- From `appydave-plugins:skill:truth-trail`: **Audit trail for agent claims about data** — verifies that agent-reported success on data operations is actually backed by evidence (not just "said it succeeded"). Analogous to the pre-completion gate but for data operations specifically. — `complexity: low | optional: true | prerequisite: "autonomous agent ran the migration"`

## Staging order (important)

The three CE data agents have a declared ordering:

1. `ce-schema-drift-detector` — first, ensures clean schema. Wasted review time if drift is present.
2. `ce-data-integrity-guardian` / `ce-data-migrations-reviewer` — migration code review (this belongs in code-review cluster, not here)
3. `ce-deployment-verification-agent` — deployment checklist generation (this distillation)

The unified skill covers step 1 + step 3. Step 2 belongs to the code-review cluster.

## Why this matters for David's stack

SupportSignal is an NDIS app. Data migrations touching participant records, support budgets, or incident reports carry compliance risk. David currently has no skill for generating Go/No-Go checklists for data deploys. The gap is: `delivery-review` catches code quality issues; nothing generates the "how to safely deploy this to production and verify it worked" artifact.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ce-deployment-verification-agent | Invariant definition framework, SQL audit query patterns, migration steps table, post-deploy verification queries, rollback classification (4 states), 24-hour monitoring plan, Go/No-Go checklist format | Ruby/Rails-specific console verification examples (keep the concept, not the syntax) |
| ce-schema-drift-detector | Schema drift detection process, git diff commands, drift indicator taxonomy, fix commands | Rails-only framing (concept applies to any ORM with a schema file) |
| ce-data-integrity-guardian | PII identification layer, GDPR compliance framing, transaction boundary analysis | Already covered by code-review cluster for migration code review |
| truth-trail (appydave) | Audit trail for agent-claimed data successes | Already in David's stack; reference pattern only |

## Draft SKILL.md frontmatter

```yaml
name: data-deploy-gate
description: >
  Pre-deploy safety gate for changes touching production data — schema migrations, backfills, data transformations.
  Generates a concrete Go/No-Go checklist: define invariants → SQL pre-deploy audit queries →
  migration steps with rollback → post-deploy verification → 24-hour monitoring plan.
  Use when: "is this migration safe?", "what's the rollback plan?", "check data integrity",
  "schema drift check", "deploy checklist", "pre-deploy verification", any PR with db/migrate/ changes.
  For SupportSignal: always run on PRs touching participant, support_budget, or incident tables.
allowed-tools: Read, Bash(git diff:*), Bash(grep:*), Bash(find:*), Bash(git log:*)
```

## Open questions for David

- Should `data-deploy-gate` be a **conditional reviewer in `delivery-review`**, auto-triggered when the diff contains `db/migrate/` changes? Or a standalone pre-push skill invoked explicitly? Auto-trigger is safer but adds overhead to every PR with migrations.
- For SupportSignal: should `data-deploy-gate` have SupportSignal-specific invariant templates? The NDIS domain has specific data integrity requirements (participant consent records, budget ceiling enforcement) that warrant named invariants.
- The schema drift detection sub-step: should this be a separate lightweight hook that runs on every PR rather than part of the deployment gate? It's cheap enough to run always.
