---
distillation_id: knowledge-capture-multi-source-researcher
stage: knowledge-capture
intent: "Research and synthesize knowledge from external sources (web, Slack, git history, GitHub issues, docs) into structured brain-ready output"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-best-practices-researcher
  - compound-engineering:skill:ce-framework-docs-researcher
  - compound-engineering:skill:ce-git-history-analyzer
  - compound-engineering:skill:ce-issue-intelligence-analyst
  - compound-engineering:skill:ce-learnings-researcher
  - compound-engineering:skill:ce-repo-research-analyst
  - compound-engineering:skill:ce-slack-research
  - compound-engineering:skill:ce-slack-researcher
  - compound-engineering:skill:ce-web-researcher
  - gbrain:skill:academic-verify
  - gbrain:skill:book-mirror
  - gbrain:skill:briefing
  - gbrain:skill:data-research
  - gbrain:skill:perplexity-research
  - gbrain:skill:query
  - gbrain:skill:strategic-reading
  - gbrain:skill:reports
  - ruflo:skill:researcher
  - ruflo:skill:deep-researcher
  - ruflo:skill:dossier-investigator
  - appydave-plugins:skill:gather
winner_mechanism: compound-engineering:skill:ce-best-practices-researcher
---

# Unified Skill: Multi-Source Researcher

## Intent

Research a topic across multiple sources (web, Context7 docs, git history, GitHub issues, Slack/Krisp), synthesize findings into a compact structured digest, and stage output for brain ingestion.

## Winner's Mechanism

CE's `ce-best-practices-researcher` is the winner: it demonstrates the correct synthesis-first posture — check curated knowledge before hitting external sources, then check Context7 for versioned docs, then web, then skills. This three-layer lookup (local → versioned docs → web) is the cleanest source-priority model in the cluster and directly addresses the failure mode where agents repeatedly fetch the same web content instead of building on prior research.

The broader CE researcher family (`ce-web-researcher`, `ce-git-history-analyzer`, `ce-issue-intelligence-analyst`, `ce-slack-researcher`) shows a clean specialization pattern: each researcher is narrowly scoped to one source, returns a structured digest, and composes with the others via the `ce-compound` orchestrator. David's `gather` skill (point-in-time DAM/ecosystem facts) is the only comparable tool in his current stack — but it's system-specific, not a generalized research layer.

## Existing-skill nesting (upgrading existing skills)

- **Existing mechanism (`gather`)**: Point-in-time fact collection from David's own systems (DAM, ecosystem, fleet). Internal sources only; not a research synthesizer.
- **No general research skill currently exists in David's stack.** The `research` command (brand-dave) is a single-purpose Brand Dave content workflow, not a generalized mechanism.
- **New mechanism's grain**: Per-task research pass before any implementation or writing task. The CE pattern is: at task-start, a research coordinator spawns 2-4 specialist researchers in parallel, each returning a structured digest; the coordinator synthesizes into a `RESEARCH-SUMMARY.md`.
- **Nesting rule**: Research runs as a pre-phase to any significant implementation or brain-update task. It's not embedded in implementation skills — it's a separate invocation David calls when context is thin. Complements `ce-compound` (which runs post-implementation) by providing the pre-implementation counterpart.

## Non-overlapping ideas folded in

- From `gbrain:strategic-reading`: **Lens-scoped reading** — read any source (book, article, transcript, case study) through an explicit strategic lens ("what does this mean for Kybernesis?"), extract only lens-relevant insights — `complexity: low | optional: false | prerequisite: none`. Prevents the "I read this but can't connect it to current work" failure mode. No equivalent in David's stack.
- From `gbrain:academic-verify`: **Citation tracing** — verify a research claim by tracing it through publications → Google Scholar → preprint servers → retractions — `complexity: medium | optional: true | prerequisite: "claim requires citation accuracy"`. Useful when David references research claims in content or brain documentation.
- From `gbrain:book-mirror`: **Personalized chapter analysis** — process a book chapter-by-chapter with a configurable analytical lens (Feynman method, Socratic dialogue, or custom persona) — `complexity: high | optional: true | prerequisite: "book as EPUB/PDF available"`. David does structured reading of technical books; this transforms them into brain-indexed material.
- From `compound-engineering:ce-git-history-analyzer`: **Archaeological git analysis** — trace file evolution via blame, identify recurring commit patterns, surface original intent from commit messages — `complexity: medium | optional: true | prerequisite: "git repo with history"`. Useful for SupportSignal onboarding and when resuming work on code David hasn't touched in months.
- From `compound-engineering:ce-issue-intelligence-analyst`: **Theme-level issue intelligence** — transform raw GitHub issues into recurring-pain themes, severity trends, and investment signals rather than per-issue summaries — `complexity: medium | optional: true | prerequisite: "GitHub repo with issues"`. Useful for Kybernesis and SupportSignal feature prioritisation.
- From `gbrain:briefing`: **Daily briefing aggregation** — compile meeting context, active deals, and recent citations into a single structured morning briefing — `complexity: medium | optional: true | prerequisite: "calendar integration or meeting list"`. David has no morning-briefing skill; this pattern from GBrain is production-tested.
- From `ruflo:dossier-investigator`: **Deep-profile investigation** — build comprehensive profile/dossier on a person, company, or technology by chaining web + academic + social sources — `complexity: high | optional: true | prerequisite: "investigation target identified"`. Useful for Kybernesis customer research.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `ce:ce-best-practices-researcher` | Three-layer lookup (local → versioned docs → web), synthesis-first posture | Context7 MCP dependency (flag as optional) |
| `ce:ce-framework-docs-researcher` | Context7 / ctx7 CLI for versioned docs | Context7 MCP dependency |
| `ce:ce-git-history-analyzer` | Archaeological git analysis pattern | CE's specific repo structure assumptions |
| `ce:ce-issue-intelligence-analyst` | Theme-level issue intelligence | CE's GitHub MCP dependency |
| `ce:ce-web-researcher` | Iterative web research with prior-art synthesis | CE's specific output format |
| `ce:ce-slack-researcher` | Organisational context from comms history | Slack MCP (not in David's stack) |
| `ce:ce-learnings-researcher` | Pre-work learnings retrieval from docs/solutions/ | CE's docs/solutions/ path convention |
| `gbrain:strategic-reading` | Lens-scoped reading pattern | GBrain's automated brain-page output |
| `gbrain:academic-verify` | Citation tracing pattern | GBrain's citation DB |
| `gbrain:book-mirror` | Chapter-by-chapter analysis with lens | GBrain's EPUB processing pipeline |
| `gbrain:briefing` | Daily briefing aggregation | GBrain's calendar integration |
| `gbrain:perplexity-research` | Brain-augmented web research | Perplexity API dependency |
| `gbrain:query` | 3-layer search + synthesis against local knowledge | GBrain's full DB model |
| `ruflo:dossier-investigator` | Deep-profile investigation pattern | Ruflo's multi-tool chaining |
| `ruflo:deep-researcher` | Iterative deep research loop | Ruflo's daemon model |
| `appydave:gather` | Point-in-time internal fact collection | Already in David's stack, keep separate |

## Draft SKILL.md frontmatter

```yaml
name: research
description: >
  Multi-source research synthesizer — check local knowledge first, then versioned docs, then
  web, then primary sources. Use when user says: "research X", "what do we know about X",
  "find best practices for X", "look into X before we build", "git history of X", "analyze
  GitHub issues for X", "strategic reading of X", "build a briefing on X", "deep-dive X",
  "verify this claim", "morning briefing". Returns a compact structured digest staged for
  brain ingestion.
argument-hint: "[topic] [--sources web|git|issues|docs|local] [--lens <strategic-question>] [--depth quick|standard|deep]"
allowed-tools: Read, Write, Bash(grep:*), Bash(git:*), Bash(gh:*), Bash(curl:*)
```

## Open questions for David

1. **Context7 MCP dependency**: CE's framework-docs researcher leans heavily on Context7 MCP (`use_mcp_tool context7`). David doesn't have Context7 in his stack. Is web fallback sufficient, or should Context7 be added as an MCP for versioned framework doc lookups?

2. **Morning briefing vs research**: GBrain's `briefing` skill is a daily ritual that aggregates meeting context, deals, and citations. Is this in scope for a research skill, or should it be a separate `briefing` skill? The mechanism overlaps (source aggregation + synthesis) but the cadence is different (daily ritual vs ad-hoc research).

3. **Slack research**: CE has two Slack researcher variants. David doesn't use Slack for internal comms (uses Krisp for meetings). Should the "comms history research" pattern point at Krisp transcripts as the equivalent source instead?
