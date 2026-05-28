---
distillation_id: orchestration-data-pipeline-orchestrator
stage: orchestration
intent: "Fetch, transform, classify, and route data from external sources into David's knowledge system — repeatable, quota-aware, resumable"
created: 2026-05-16
status: draft
source_artifacts:
  - appydave-plugins:skill:omi
  - appydave-plugins:skill:omi-schedule
  - appydave-plugins:skill:grab-downloads
  - gbrain:skill:ingest
  - gbrain:skill:webhook-transforms
  - gbrain:skill:email-to-brain
  - gbrain:skill:calendar-to-brain
  - gbrain:skill:meeting-sync
  - gbrain:skill:x-to-brain
  - gbrain:skill:restart-sweep
  - gbrain:skill:twilio-voice-brain
  - ruflo:skill:stream-chain
  - gbrain:skill:cron-scheduler
  - appydave-plugins:skill:clauding-lab-events
winner_mechanism: appydave-plugins:skill:omi
---

# Unified Skill: data-pipeline-orchestrator

**Purpose**: Fetch data from external sources, transform/classify it, route it into David's knowledge system — quota-aware, resumable, with progress monitoring built in.

**For Agents**: Use when David says "sync OMI", "pull new data", "ingest X into brain", "run the pipeline", "what's in my inbox", or needs to route external signals (email, calendar, webhook, API) into his second-brain system.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Chain: fetch (external API/source) → transform/classify (LLM or deterministic) → write (brain frontmatter / git commit) — with quota tracking, resumability, and progress polling built in. Claude monitors and reports; user does not run monitoring commands themselves.

## Winner's Mechanism

`appydave-plugins:skill:omi` wins because it is the most complete implementation of the data pipeline pattern in David's actual stack. It demonstrates:

1. **Two-stage pipeline**: sync (fetch → git commit) then extract (classify with Gemini → write frontmatter)
2. **Quota awareness**: Flash-Lite 1,000 RPD limit; clean stop on quota hit; resumes exactly where it left off next day
3. **Claude-does-monitoring**: Claude polls the log every 30 seconds and reports — user never runs monitoring commands
4. **Backlog surfacing**: after extract, surface what needs actioning (which brains need updates)
5. **Discovery query refresh**: periodic step to keep random-queries.yml fresh based on what surfaced

This is a production pattern David runs daily. The mechanism is directly reusable for any external-source → brain pipeline.

## Non-overlapping ideas folded in

- From `gbrain:skill:ingest`: **Intent-routing to specialized ingest skills** — a single `ingest` command dispatches to the right specialist based on source type. David could add this as a router layer above `omi` for multi-source intake.
- From `gbrain:skill:webhook-transforms`: **Generic event → brain-ingestible signal** transform — any external event (SMS, meeting, social mention) converted via the same transform pipeline. Extensible to new sources without changing the router.
- From `gbrain:skill:meeting-sync`: **Meeting transcript ingestion** (Circleback) with attendee detection + entity enrichment — a concrete instance of the webhook-transform pattern for a high-value source David uses.
- From `ruflo:skill:stream-chain`: **Stream-JSON chaining** for multi-agent pipeline steps — a composable approach to chaining transform steps where each step's output is the next step's input, with structured JSON as the bus.
- From `gbrain:skill:cron-scheduler`: **Scheduled ingestion with staggering and quiet hours** — prevents all pipelines from firing simultaneously; respects Do Not Disturb windows. David already has `omi-schedule` for this but the staggering logic is worth adding.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| omi | Full mechanism: sync→extract→backlog→refresh cycle, quota awareness, Claude-polls-log | OMI-specific API key |
| omi-schedule | launchd schedule management for macOS | OMI-specific |
| gbrain:ingest | Intent-routing to specialized ingestors | GBrain Supabase dep |
| gbrain:webhook-transforms | Generic event→signal transform framework | GBrain-specific schema |
| gbrain:meeting-sync | Meeting transcript → brain with attendee detection | Circleback dep |
| ruflo:stream-chain | Stream-JSON chaining between pipeline steps | Ruflo stream format |
| gbrain:cron-scheduler | Staggered scheduling with quiet hours | GBrain cron infrastructure |
| grab-downloads | File-mover as ingest entry point (~/Downloads → project) | Downloads-specific UX |

## Draft SKILL.md frontmatter

```yaml
name: data-pipeline-orchestrator
description: >
  Fetch data from an external source, transform/classify it, and route it into
  David's knowledge system — quota-aware, resumable, Claude-monitors-not-user.
  Existing instances: omi (OMI API → raw-intake → brain frontmatter).
  Pattern: fetch → classify → write → surface backlog → refresh discovery.
  Use when: "sync OMI", "ingest X into brain", "pull new data", "run the pipeline",
  "process new transcripts", "what's in my intake queue", "set up ingest for X".
```

## Open questions for David

- Should `grab-downloads` be considered part of this cluster or is it a pure utility (not a pipeline)?
- Is there a missing general-purpose `ingest` orchestrator that routes ANY source (OMI, email, calendar, Krisp, downloads) to the right pipeline? That would close the "add a new data source" gap.
- `meeting-sync` (Circleback → brain) — is this worth adding now? David is using Krisp, not Circleback — but the mechanism is the same. Should `krisp-fetch` → `omi-extract` become a unified `krisp-pipeline` instance?
