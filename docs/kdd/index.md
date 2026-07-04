# KDD (reconstructed from sessions)

2 patterns · 45 learnings · 41 decisions

> **Status: proposed.** Reconstructed from 63 Claude Code session transcripts (52 Roamy + 11 M4
> Mini, union of both machines — sessions are machine-local and disjoint) via the Lisa
> `reconstruct-kdd` pipeline. Provenance: reconstructed from session transcripts — review before
> trusting; conform decisions to this repo's own ADR format before ratifying any of them.

Reconciled against the existing binding decision record at
[`docs/watchtower/DECISIONS.md`](../watchtower/DECISIONS.md) (D1–D4, Watchtower v0). That record
is canonical and untouched by this reconstruction — nothing here supersedes it. One reconstructed
decision candidate (the session that produced D1–D4 itself) was recognized as a duplicate and
dropped; three tactical/draft items were dropped as noise (one rescued on adversarial re-check —
see the run's `RECONCILE-TRIAGE.md`); zero conflicts were found.

- [Decisions](decisions/index.md) — 41 proposed ADR candidates, numbered ADR-0001 onward (fresh
  sequence; D1–D4 predate this sequence and use their own naming — no collision, but note the
  gap when this repo eventually adopts one ADR numbering scheme)
- [Learnings](learnings/index.md) — 45 problem-and-fix write-ups across 7 categories
- [Patterns](patterns/index.md) — 2 lessons that recurred across 3+ sessions

Two near-duplicate pairs flagged at reconstruction time were merged by hand on 2026-07-04 (both
recorded the same same-day decision from two sessions): ADR-0023 folded into
[ADR-0006](decisions/0006-move-dark-factory-job-state-off-flat-files-into-a-switchboar.md)
("move job-state to Switchboard"), and ADR-0040 folded into
[ADR-0036](decisions/0036-consolidate-comprehend-visualise-into-mochaccino-as-a-4th-mo.md)
(comprehend-visualise consolidation proposal + its later execution). Numbering gaps at 0023/0040
are intentional — see `_runs/2026-07-04-david-roamy/RECONCILE-TRIAGE.md` for the original flag.

Full run audit (session list, verdicts, classifier output, triage report):
[`_runs/2026-07-04-david-roamy/`](_runs/2026-07-04-david-roamy/).
