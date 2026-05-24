# Run Summary — b65 Bulk Content Analysis

**Video**: b65 — Guy Monroe Marketing Plan
**Run date**: 2026-05-20
**Workflow**: `workflow-01-analysis.json` (bulk-content-analysis v1.0.0)
**Elapsed**: ~37 seconds (12 parallel subagents)

## 12 keys populated

| # | Key | Type | Status |
|---|-----|------|--------|
| 1 | `mainTopic` | string | ✓ populated |
| 2 | `keywords` | array | ✓ populated |
| 3 | `audienceInsights` | array | ✓ populated |
| 4 | `emotionalTriggers` | array | ✓ populated |
| 5 | `statistics` | string | ✓ populated |
| 6 | `catchyPhrases` | array | ✓ populated |
| 7 | `ctaPhrases` | array | ✓ populated |
| 8 | `keyTakeaways` | array | ✓ populated |
| 9 | `overallTone` | string | ✓ populated |
| 10 | `questionsPosed` | array | ✓ populated |
| 11 | `searchTerms` | array | ✓ populated |
| 12 | `usp` | array | ✓ populated |

## Store stats

- `store.jsonl`: 14 records (2 seeds + 12 analysis steps)
- `store.view.json`: 14 top-level keys
- All records valid EAV envelope (`key`, `value`, `meta.step`, `meta.ts`, `meta.by`)
- No retries needed

## Isolation verification

- Conductor-session.log: 17 lines — dispatch records, acks, project marker, done
- No transcript fragments in conductor log: ✓ verified
- No extraction payloads in conductor log: ✓ verified (write-store-directly contract held)

## Subagent pattern used

12 workers spawned in parallel via Agent tool. Each worker:
1. Ran in clean context (no parent conversation history)
2. Read transcript directly from disk
3. Wrote one EAV record to store.jsonl
4. Returned one-line ack to orchestrator

Orchestrator saw only acks — never transcript text, never extracted values.
