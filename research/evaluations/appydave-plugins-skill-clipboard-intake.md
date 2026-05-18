---
artifact_id: appydave-plugins:skill:clipboard-intake
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation, knowledge-capture]
phase_fit: [6, 7, 8]
evaluated_at: 2026-05-17
---

# Eval: clipboard-intake

**Intent**: Bidirectional clipboard bridge — safe classified ingestion from clipboard to filesystem (Mode A) and packaging of files onto clipboard for external tools (Mode B).

## Scores
- **quality_score**: 4 — The security architecture (raw content never enters orchestrator context; background agent handles all reading) is sophisticated and correct. SHA-256 duplicate detection is production-grade. The 50KB size threshold for Mode B with automatic temp-file fallback is a practical design decision. Loses one point because the known-buckets.md reference architecture means the skill is incomplete without that file, and the trigger phrases for Mode A vs Mode B overlap enough to cause selection ambiguity.
- **adoption_fit_final**: strong — David's own tool, wired to his raw-intake pipeline and Lexi ontology. No adoption friction.
- **inspiration_value**: mid — The "raw content never enters orchestrator context" security pattern is the most portable idea. The Mode A/B bidirectional framing is clean.
- **uniqueness_refined**: uncommon — The security gate (prompt-injection-scanner before web/email sources) combined with deduplication is a distinctive pattern. Most clipboard skills are write-only.
- **composability**: calls-others — Calls prompt-injection-scanner, enrich-metadata, and lexi. Background agent spawning for raw content isolation is orchestration pattern.
- **description_craft_refined**: trigger — Long but well-organized trigger list covering both modes distinctly.

## Mineable phrasing
> "Raw content NEVER enters the main orchestrator context — A background agent does all reading, classifying, and writing"

## Notes
The security-gate architecture (ask source → decide risk mode → run scanner for untrusted sources → spawn isolated agent) is the most complete input-safety pattern in the corpus. This is the right model for any skill that ingests user-supplied content. The SHA-256[:8] hash for deduplication is a clean, low-overhead mechanism. Mode B's size-aware output format (text on clipboard vs path on clipboard) shows practical production thinking.
