---
distillation_id: knowledge-capture-brain-curation
stage: knowledge-capture
intent: "Maintain second-brain health — enrich, validate, deduplicate, and navigate curated knowledge bases"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:lexi
  - appydave-plugins:skill:frontmatter-indexer
  - appydave-plugins:skill:enrich-metadata
  - appydave-plugins:skill:brain-query
  - gbrain:skill:maintain
  - gbrain:skill:enrich
  - gbrain:skill:cold-start
  - gbrain:skill:migrate
  - gbrain:skill:citation-fixer
  - gbrain:skill:concept-synthesis
  - gbrain:skill:article-enrichment
  - gbrain:skill:brain-ops
  - compound-knowledge:skill:stale-knowledge-checker
  - gstack:skill:sync-gbrain
winner_mechanism: appydave-plugins:skill:lexi
---

# Unified Skill: Brain Curation

## Intent

Keep a second-brain knowledge collection healthy: enrich files with structured metadata, validate cross-references and links, detect staleness, deduplicate, and surface navigation gaps — without touching source documents' prose.

## Winner's Mechanism

David's `lexi` is the winner: it's already a portable multi-brain health suite running against this exact corpus. Lexi covers: health audits, link validation, frontmatter schema checks, tag/ontology validation, SRP detection, isolation audits, negative-knowledge audits, and brains-index generation. It's production-tested against 60+ brains and the widest-coverage curation tool in the cluster.

`frontmatter-indexer` is lexi's narrower sibling (schema detection + validation, lower footprint for targeted passes) and stays as a complementary tool for index-regeneration. `enrich-metadata` handles the write side (cheap LLM enrichment pass to add missing tags, topics, entities). `brain-query` is the discovery/navigation tool — separate concern from curation.

GBrain's tools are the richest external reference: `maintain` runs back-link enforcement, citation audit, filing validation, and SRP checks; `enrich` does tiered enrichment with API calls; `concept-synthesis` deduplicates raw concept stubs into a tiered map. The gap in David's stack vs GBrain is: no tiered enrichment protocol and no concept-deduplication pass.

## Existing-skill nesting (upgrading existing skills)

- **Existing mechanism (`lexi`)**: Health audit suite — broken links, frontmatter validation, tag checks, brains-index regeneration. Multi-brain or single-brain scope. Manual invocation.
- **Existing mechanism (`frontmatter-indexer`)**: Schema detection + validation + index rebuild. Narrower than lexi; used when only the index needs regenerating.
- **Existing mechanism (`enrich-metadata`)**: Cheap LLM enrichment pass — adds `tags`, `topics`, `relationships`, `summaries`, `entities` to markdown files. Write-focused, not audit-focused.
- **New mechanisms' grain**: (1) Tiered enrichment (T1 basic metadata / T2 deep analysis / T3 external citations), (2) concept deduplication across files, (3) staleness scoring against codebase/external sources.
- **Nesting rule**: Lexi is the audit + health pass (read-only findings). Enrich-metadata is the enrichment write pass. They compose sequentially: run lexi → review findings → run enrich-metadata on flagged files. Concept-synthesis sits above both as a periodic dedup sweep. Staleness checker fires as a post-commit hook or periodic cron.

## Non-overlapping ideas folded in

- From `gbrain:concept-synthesis`: **Tiered concept map** — deduplicate raw concept stubs across brain files into T1/T2/T3 tiers (load-bearing concepts / supporting concepts / peripheral mentions) — `complexity: high | optional: true | prerequisite: "brain has >50 files with concept overlap"`. David's brains accumulate the same concept across multiple files; this turns chaos into a navigable hierarchy.
- From `gbrain:enrich`: **Tiered enrichment protocol** — T1 (basic metadata via cheap LLM), T2 (full analysis via better model), T3 (external citation enrichment via web search) — `complexity: medium | optional: true | prerequisite: none"`. David's `enrich-metadata` is effectively T1 only. T2 and T3 are missing.
- From `compound-knowledge:stale-knowledge-checker`: **Post-write staleness scan** — after any new learning is captured, scan knowledge base for contradicted or superseded entries and flag them — `complexity: low | optional: false | prerequisite: none"`. Prevents the "I fixed this but the old pattern is still in the brain" failure mode. Currently nothing triggers this in David's stack.
- From `gbrain:cold-start`: **Day-one bootstrap template** — structured question sequence for initialising a new brain with zero existing content — `complexity: low | optional: true | prerequisite: "new brain with <5 files"`. David already has `brain-creation-guide.md` but it's prose-only; a structured prompt sequence would be faster.
- From `gbrain:migrate`: **Universal import** — migrate from Obsidian, Notion, Logseq, Roam, CSV, JSON into brain format — `complexity: high | optional: true | prerequisite: "external knowledge source exists"`. Useful for when team members (Jan, Mary) contribute from other tools.
- From `gbrain:maintain`: **Back-link enforcement** — verify every `@file-reference` or wikilink resolves to an existing file — `complexity: low | optional: false | prerequisite: none`. Lexi checks broken links but not back-link completeness (unlinking when source file is renamed/deleted).
- From `gbrain:citation-fixer`: **Citation format normalisation** — audit citation formatting across brain pages and normalise to a consistent citation style — `complexity: low | optional: true | prerequisite: "brain mixes citation formats"`. Low friction but high polish for the `academic-verify` + `strategic-reading` workflows.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave:lexi` | Full health audit suite — the winner | — |
| `appydave:frontmatter-indexer` | Index rebuild — complementary narrow tool | — |
| `appydave:enrich-metadata` | LLM enrichment write pass | — |
| `appydave:brain-query` | Discovery/navigation — separate concern | — |
| `gbrain:maintain` | Back-link enforcement, SRP checks | GBrain's DB-backed storage model |
| `gbrain:enrich` | T2/T3 tiered enrichment levels | GBrain's Notion-linked metadata store |
| `gbrain:concept-synthesis` | Tiered concept map (dedup sweep) | GBrain's automated relationship graph |
| `gbrain:cold-start` | Bootstrap question sequence | GBrain's brain-as-DB pattern |
| `gbrain:migrate` | Universal import patterns | GBrain's platform-specific connectors |
| `gbrain:citation-fixer` | Citation normalisation | GBrain's citation DB |
| `gbrain:brain-ops` | Concept (brain as queryable KB) | Requires tool installation (`brain-ops`) |
| `ce:stale-knowledge-checker` | Post-write staleness scan trigger | CE's docs/solutions/ specific paths |
| `gstack:sync-gbrain` | Sync-to-external-brain concept | gstack's specific GBrain integration |

## Draft SKILL.md frontmatter

```yaml
name: lexi
description: >
  Portable brain librarian — curate, onboard, maintain, and analyse second-brain knowledge
  collections (single brain or multi-brain sweep). Use when user says: "audit brain",
  "check brain health", "find broken links", "validate frontmatter", "regenerate index",
  "check tags", "stale knowledge check", "find duplicate concepts", "enrich brain files",
  "lexi sweep", "brain health", "add metadata to brain files", "check cross-references".
argument-hint: "[brain-name | --all] [--audit] [--enrich] [--stale] [--dedup] [--links]"
allowed-tools: Read, Edit, Write, Bash(grep:*), Bash(find:*), Bash(query_brain:*)
```

## Open questions for David

1. **Tiered enrichment model cost**: GBrain's T2 enrichment uses a better (more expensive) model. Should lexi's `--enrich` flag default to T1-only (cheap, fast) and require `--deep` to invoke T2? Or is a single quality level sufficient for David's brains?

2. **Concept-synthesis scope**: The concept-deduplication pass across 60+ brains is expensive. Should this be brain-local only (find duplicates within one brain) or truly cross-brain? Cross-brain is more powerful but requires loading a lot of context.

3. **Back-link enforcement**: Should broken-back-link warnings in lexi be errors (block commit via hook) or advisory warnings (surfaced in report only)? The pre-commit hook currently doesn't run lexi.
