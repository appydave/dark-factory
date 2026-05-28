---
distillation_id: code-review-monolithic-quality
stage: audit
intent: "Single-skill, multi-axis code review — correctness, readability, architecture, security, performance — no fan-out required"
created: 2026-05-16
status: draft
source_artifacts:
  - agent-skills-osmani:skill:code-review-and-quality
  - agent-skills-osmani:agent:code-reviewer
  - agent-skills-osmani:command:review
  - bmad-method:skill:bmad-code-review
  - superpowers:skill:requesting-code-review
  - everything-claude-code:agent:code-reviewer
  - everything-claude-code:command:code-review
  - everything-claude-code:command:review-pr
  - gsd:command:gsd:review
  - gstack:skill:review
  - ruflo:skill:github-code-review
  - compound-knowledge:skill:kw:review
winner_mechanism: agent-skills-osmani:skill:code-review-and-quality
---

# Unified Skill: code-review-monolithic-quality

**Purpose**: Single-pass, multi-axis code review for everyday changes — no fan-out machinery required. Covers the five essential axes (correctness, readability, architecture, security, performance) and returns a clear verdict. Use when a diff is small-to-medium and the full `delivery-review` fan-out is overkill.

**For Agents**: Use this when David says "quick review", "check this", "review my changes" on a focused diff (under ~300 LOC). This is the lightweight single-reviewer path. David's `delivery-review` is the full 6-dimension fan-out path for pre-merge gates. These two are **complementary**: monolithic-quality for flow-state checks, delivery-review for merge gates.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Conduct a confident five-axis review as a single agent, filtering noise via >80% confidence threshold, and return a Clear / Fix Required / Block verdict — fast enough to run during implementation without interrupting flow.

## Winner's Mechanism

`agent-skills-osmani:skill:code-review-and-quality` wins. It is the most complete single-skill implementation across the corpus: explicit five-axis framework (correctness, readability/simplicity, architecture, security, performance), approval standard that avoids perfectionism ("approve when it definitely improves overall code health"), change sizing guidance (~100 lines = good, ~1000 = split it), and clear split-strategy table. It avoids the trap of rewarding complexity while punishing small diffs.

The `everything-claude-code:agent:code-reviewer` adds one critical mechanism: a **pre-report gate** with four forced questions before writing any finding (exact line? concrete failure mode? surrounding context read? severity defensible?). This prevents the noise flood that kills trust in automated reviews.

## Non-overlapping ideas folded in

- From `everything-claude-code:agent:code-reviewer`: Four-question pre-report gate before any finding is written — prevents low-confidence noise and severity inflation. Combine with Osmani's axes.
- From `everything-claude-code:command:review-pr`: Prompt Defence Baseline header (injection resistance block) — relevant when the reviewed code itself processes untrusted input; embed as a standard check in the security axis.
- From `gstack:skill:review`: Verdict phrasing — "Ready to ship? YES / NO / WITH CONDITIONS" is cleaner than PASS/FAIL for monolithic reviews (cleaner binary than delivery-review's three-tier, appropriate for a faster path).
- From `superpowers:skill:requesting-code-review`: SHA-range anchoring pattern (BASE_SHA + HEAD_SHA) — forces the reviewer to work on a deterministic diff rather than inference, eliminating scope ambiguity.
- From `bmad-method:skill:bmad-code-review`: "Acknowledge what was done well before listing issues" calibration note — accurate praise helps the implementer trust the rest of the feedback.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| agent-skills-osmani:code-review-and-quality | Five-axis framework, approval standard, change sizing table | The split-strategy section (execution detail, out of scope for a review skill) |
| everything-claude-code:code-reviewer | Pre-report gate (4 questions), confidence threshold (>80%), consolidate similar issues | Prompt Defense Baseline in full (folded as a security axis check) |
| gstack:review | YES/NO/WITH CONDITIONS verdict | Stack-specific triggers |
| superpowers:requesting-code-review | SHA-range scope anchoring | Task-tool dispatch mechanism (delivery-review owns fan-out) |
| bmad-method:bmad-code-review | Strengths-first calibration note | BMAD-specific persona framing |
| gsd:review | General review pattern | GSD pipeline coupling |
| compound-knowledge:kw:review | Applies same pattern to knowledge artifacts | Knowledge-specific checks |
| ruflo:github-code-review | GitHub PR integration pattern | Ruflo infrastructure dependency |

## Draft SKILL.md frontmatter

```yaml
name: review-code
description: >
  Single-pass five-axis code review (correctness, readability, architecture, security, performance).
  Confidence-gated: only reports findings where >80% sure it is a real problem.
  Returns a clear YES / NO / WITH CONDITIONS verdict.
  Use when: "quick review", "check this change", "review before I commit", "review my diff",
  "review this file", "fast code review", "lightweight review".
  For pre-merge gate with 6 specialist dimensions use delivery-review instead.
```

## Canonical skill body (for SKILL.md)

```
Run a five-axis code review against a diff or file set. Filter noise — only report when >80% confident.

## Inputs

- **scope** — diff, file list, PR number, "current changes", or BASE_SHA..HEAD_SHA
- **also_consider** (optional) — project-specific conventions, architecture doc, spec

## Steps

### 1. Anchor Scope
Load the diff. If scope is "current changes": run git diff + git diff --cached.
If scope is a PR number: fetch via gh pr diff {number}.
State the scope clearly before reviewing.

### 2. Five-Axis Review

For each axis, apply the pre-report gate before writing any finding:
- Can I cite the exact file:line?
- Can I describe the concrete failure mode (input → bad outcome)?
- Have I read surrounding context (callers, imports, tests)?
- Is the severity defensible?

If any answer is No — drop or downgrade.

**Axis 1 — Correctness**: Edge cases, null/empty/boundary handling, error paths, race conditions, off-by-one.
**Axis 2 — Readability**: Names (no `temp`/`data`/`result`), control flow clarity, module organization, dead code.
**Axis 3 — Architecture**: Pattern consistency, dependency direction, abstraction debt, duplication.
**Axis 4 — Security**: Untrusted input validation, parameterized queries, secrets hygiene, auth/authz checks, encoding.
**Axis 5 — Performance**: N+1 queries, unbounded loops/fetches, missing pagination, blocking I/O in async paths.

Consolidate similar findings (e.g., "3 functions missing error handling" not 3 separate entries).

### 3. Acknowledge Strengths
List 1-3 specific things done well. Accurate praise builds trust in the rest of the feedback.

### 4. Verdict
- **YES** — ready to merge/commit, improvements only
- **WITH CONDITIONS** — specific issues to fix first (list them)
- **NO** — significant rework needed (explain what)
```

## Open questions for David

- Is this skill worth creating as a standalone, or should "quick review" just invoke `delivery-review` with fewer dimensions? The argument for a separate skill: it is genuinely faster (no fan-out overhead) and fits the flow-state use case. The argument against: maintaining two review paths for what is essentially the same job.
- Should the confidence threshold (>80%) be made explicit in the description so users know findings are pre-filtered?
- Where does this sit relative to `codebase-audit` (project-wide, deep) and `delivery-review` (diff-scoped, fan-out)? Suggest: monolithic-quality = flow-state check; delivery-review = merge gate; codebase-audit = campaign completion.
