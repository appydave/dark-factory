---
artifact_id: appydave-plugins:skill:prompt-injection-scanner
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, orchestration, verification-validation]
phase_fit: [5, 6, 9]
evaluated_at: 2026-05-17
---

# Eval: prompt-injection-scanner

**Intent**: Scan untrusted content for prompt injection attacks before it enters any pipeline, wrapping content in an isolated Opus agent for model-pinned auditable sanitization.

## Scores
- **quality_score**: 4 — Source-based risk mode defaults (omi=standard, email=strict, web=strict), five-step process, logging to a brain security log, HUMAN REVIEW REQUIRED flag for HIGH findings, verbatim-prompt pattern (references/scanner-agent-prompt.md). Compact and operationally clear.
- **adoption_fit_final**: strong — David's pipelines ingest OMI transcripts, emails, web content, and client documents — exactly the attack surface this guards. Already installed and active.
- **inspiration_value**: mid
- **uniqueness_refined**: rare — The model-pinned Opus sub-agent for scanning (prevents the currently-running model from being the scanner) is a distinct security architecture choice not common in agent literature.
- **composability**: called-by-others — Designed as a gate at the front of any untrusted-content pipeline; composable with OMI, email relay, and web-fetch workflows.
- **description_craft_refined**: trigger — Rich trigger list including pipeline-entry scenarios.

## Mineable phrasing
> "Wraps content in an isolated Opus agent for model-pinned, auditable sanitization."

## Notes
The model-pinning pattern (spawn a specific model version for the scan regardless of session model) provides auditability and prevents model-drift from weakening scan quality over time. Logging to `~/dev/ad/brains/security/scan-log.md` creates a persistent audit trail. The `browser-testing-with-devtools` skill's security section and this skill form a complementary pair: one guards incoming content, the other guards browser-sourced data.
