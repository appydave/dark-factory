# KDD reconstruction run — 2026-07-04, David, Roamy

Immutable record of the one-shot KDD backfill for Dark Factory. Reconstruct is one-shot per
project (not re-run on this repo going forward) — steady state is per-ticket capture instead.

## Corpus

- 63 session transcripts, union of both machines (sessions are machine-local and disjoint):
  52 from Roamy (`~/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/`), 11 from the
  M4 Mini over Tailscale.
- Handover / runbook: `~/.kdd-cache/dark-factory/HANDOVER.md` (not committed — private cache).
- Pipeline: Lisa `reconstruct-kdd`, `appydave-plugins` v5.9.1 (commit `8e54143`).

## Pipeline stages run

| Stage | Result |
|---|---|
| init | 63 sessions manifested |
| digest | 63/63 digested |
| extract (63 sonnet agents, one per session) | 114 candidates (67 learning, 47 decision); 5 agents hit a transient API disconnect mid-batch and were retried cleanly |
| cluster (1 sonnet agent, semantic pass) | 67 learning candidates → 47 clusters; 2 promotion-eligible patterns (≥3 sessions), 12 recurring (2 sessions) |
| provenance | 63 sessions → 691 file refs, 14 commit refs |
| emit + human review | 2 patterns + 45 learnings + 47 decisions emitted; review queue → 14 accept verdicts (all 2 patterns + 12 recurring learnings), 0 merges needed |
| apply + re-emit | 0 merges to fold (none proposed) — idempotent no-op, final tree unchanged |
| reconcile-prep | ⚠️ auto-discovery reported "greenfield" (only checks `docs/kdd/decisions`, `docs/decisions`, `docs/adr(s)` dirs) — this is a **known tool blind spot**, not true greenfield: the repo's real binding decision record is the single file `docs/watchtower/DECISIONS.md` (D1–D4). The classifier agent was hand-briefed with that file's content to compensate. |
| reconcile-classify (1 sonnet agent) | 94 items classified: 1 duplicate, 4 noise, 89 new, 0 conflict |
| adversarial drop-review (1 sonnet agent, mandatory per Lisa doctrine) | Re-checked all 5 drops. 4 confirmed. **1 rescued**: the jump-alias naming-convention decision, originally dropped as "trivial" — the drop-review gate exists precisely to catch this under-drop failure mode. |
| reconcile-existing | 90 staged (43 decisions, 45 learnings, 2 patterns), 1 duplicate + 3 noise dropped, 0 conflicts. Canonical `docs/watchtower/DECISIONS.md` untouched. |

Final: **90 items promoted** to `docs/kdd/` at `status: proposed`.

## Human gates exercised

- **Review gate** (`REVIEW.md` / `verdicts.jsonl`, this dir): David accepted all 2 promotion-eligible
  patterns and all 12 recurring learnings, no merges.
- **Sign-off / search-wider prompt**: ~250 `prior_art_hints` were collected across candidates
  (mostly self-referential to this repo's own `docs/`/memory — expected for a self-hosted factory).
  No additional external search scope was needed beyond the existing `docs/watchtower/DECISIONS.md`
  anchor.
- **Drop-review gate**: mandatory adversarial re-check of every duplicate/noise verdict — see above,
  rescued 1 of 5.

## Known issues found and fixed during this run

- Lisa's `reconstruct_kdd.py` had "Cortex" (a prior project) hardcoded into the emitted KDD title
  (`emit`/`review` stage headers). Fixed at the source
  (`~/dev/ad/appydave-plugins/appydave/skills/lisa/scripts/reconstruct_kdd.py`) — cosmetic only,
  did not affect candidate data, but would have mis-branded every future project's run.
- `reconcile-prep`'s existing-KDD discovery only recognizes directory-based decision logs
  (`docs/kdd/decisions`, `docs/decisions`, `docs/adr(s)`); it does not recognize a single-file
  binding record like `docs/watchtower/DECISIONS.md`. Worked around by hand-briefing the classifier
  agent this run; the tool itself was not changed (would need a `--existing-decisions-file` option
  or similar to generalize).

## Not yet done (flagged, not blocking)

- Two near-duplicate decision pairs surfaced separately (safe-bias) and would benefit from a human
  merge pass: `0006`/`0023` (job-state → Switchboard, two sessions) and `0036`/`0040`
  (comprehend-visualise consolidation, proposal + execution). See `RECONCILE-TRIAGE.md`.
- All 43 decisions are `status: proposed` reconstructed candidates, not ratified ADRs — each still
  needs to be conformed to this repo's actual ADR format (`Deciders`, etc.) before ratifying, per
  Lisa's own banner on every file.

## Files in this run record

- `REVIEW.md` — the human review queue as presented (patterns/recurring learnings)
- `verdicts.jsonl` — the 14 accept verdicts appended at the review gate
- `reconcile_classify.json` — the classifier's 94-item verdicts (post drop-review rescue applied)
- `RECONCILE-TRIAGE.md` — the final reconcile-existing triage report (what was staged, why)
