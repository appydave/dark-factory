# Proposal — Dark Factory Documentation Organiser

**Status**: proposal — 2026-06-05 · **decided** (defaults locked, §5) · build parked in `backlog/2026-06-05-doc-organiser.md`
**Origin**: queue ticket `q-20260605-propose-doc-organiser` (Watchtower instruction job)
**DONE**: a proposal to decide from. This does **not** build anything.

---

## TL;DR (the decision in one line)

The doc-organisation *discipline* already exists (`docs/INDEX.md`, Problem #1 ✅) — but nothing **checks** it, so it drifts. Proposal: a **recurring audit skill** (`doc-organiser`) that reports drift and never edits, dispatched as a Watchtower **instruction job** when David wants a sweep. Pick the recommendation in §2 or override.

---

## 1. What "organised" means for dark-factory docs

The standard already exists — `docs/INDEX.md` line 4: *"when a new design doc lands, it gets a line here or it doesn't exist."* "Organised" = that promise holds. Concretely, six checks:

| Check | "Organised" means |
|-------|-------------------|
| **Index coverage** | Every `docs/**.md` has a line in `docs/INDEX.md`. No orphans. |
| **Read-order integrity** | The numbered read-order in INDEX still points at files that exist and matters-first. |
| **Stale dates** | `Status:` / `Last updated:` lines aren't lying — flag docs whose stamp predates their last `git` touch, or that are N+ days cold. |
| **Overlap / duplication** | Two docs claiming the same job get flagged for a "parent/child or merge" decision (the `architecture.md` ↔ `spec.md` pattern, already adjudicated in INDEX). |
| **Orphans** | A `.md` under `docs/` that no INDEX line and no other doc references. |
| **Broken cross-refs** | `[...](path)` and `` `file.md` `` mentions that resolve to nothing (renames, moves). |

**Live proof it's needed**: `docs/watchtower/symphony-spec.md` and `docs/watchtower/watchtower-from-symphony.md` exist on disk today and are **not** in `docs/INDEX.md`. The discipline is already drifting — by exactly the amount nobody is checking it.

Scope note: "organised" is **`docs/` only** for v1. `research/` is the frozen Warehouse (read-only, its own `INDEX.md`); `backlog/` and `experiments/` have their own registers. Don't let the organiser sprawl into them.

## 2. Shape: one-time pass vs recurring skill vs Marshall job

| Option | What it is | Verdict |
|--------|-----------|---------|
| **A. One-time organise pass** | A single session that audits + fixes today, then we're done. | ✗ Rejected. Drift is continuous (the orphans above accrued in days). A one-shot is stale the moment a doc lands. |
| **B. Recurring skill** `doc-organiser` | A skill that runs the six checks and emits a **drift report** (markdown table + suggested INDEX lines). **Audit-only — never edits.** | ✓ **Recommended.** Matches the repo's "report, human decides" grain and the assessment-mode default. |
| **C. Marshall job** | The same skill, but *dispatched by* Marshall/Watchtower on a trigger instead of run by hand. | ✓ **Recommended as the trigger**, layered on B — not an alternative to it. |

**Recommendation: B + C.** Build the skill (B); invoke it as a Watchtower **instruction/skill job** (C) — this very ticket is the dispatch pattern. No cron (Max-plan rule: automation runs in-session, never headless). The "recurring" cadence is "whenever David queues a sweep or a /loop drains one," not a clock.

**Hard line — audit, not autofix.** The organiser **proposes**: a drift report + ready-to-paste INDEX lines. It does **not** rewrite docs, move files, or edit INDEX. Same reasons ratified canonical artifacts don't get auto-rewritten: the index is a human-curated read-order, and "this doc duplicates that one" is a *hypothesis to validate, not an order to obey* (`systemic-fixes.md`). Fixing is a separate, human-approved move.

## 3. What it checks (the six, as a runnable spec)

1. **Sprawl / index coverage** — `find docs -name '*.md'` minus the set of files referenced in `INDEX.md` → orphan list.
2. **Stale dates** — parse `Status:` / `Last updated:` / date stamps; compare to `git log -1 --format=%cs <file>`; flag stamp-older-than-content and cold-for-N-days (suggest N=30).
3. **Overlap / duplication** — heuristic: docs with high title/heading overlap or cross-claiming scope → flag for parent/child-or-merge decision. Low-confidence; report as "review", never auto-act.
4. **Orphans** — in `INDEX.md`? referenced by any other doc? If neither → orphan.
5. **Broken cross-references** — extract `[...](...)` links and `` `*.md` `` mentions; resolve relative to the doc; report unresolved.
6. **Read-order integrity** — every numbered/bulleted INDEX entry resolves to a real file; flag dead entries and newly-landed files missing from read-order.

Output = one markdown **drift report** (`docs/_reports/doc-organiser-YYYY-MM-DD.md` or inline in chat), severity-ranked, with a copy-paste block of suggested INDEX lines. Decisions surfaced in-chat, not buried (per `surface-decisions-dont-bury`).

## 4. Where it should live

- **The skill** → `.claude/skills/doc-organiser/SKILL.md` (a real, invocable skill, peer to `marshall` / `swagger` / `store`). It's repo machinery, not a canonical artifact, so it does **not** need provenance.
- **The dispatch** → a Watchtower queue ticket (`kind: skill`, `skill: doc-organiser`), exactly like this ticket. That's the "recurring" surface.
- **This proposal** → `docs/doc-organiser-proposal.md` (here) + a line in `docs/INDEX.md` (dogfooding the rule it audits).
- **Reports** → `docs/_reports/` (git-ignored or kept — David's call), so audits don't themselves become sprawl.

## 5. Decisions (locked 2026-06-05 by David, via Marshall)

1. **Approve B + C** ✅ — build the recurring audit skill, Watchtower-dispatched. **Its first run *is* the cleanup** — no separate manual pass; today's orphans (the two `watchtower/symphony-*` docs) get caught on run 1.
2. **Cold-doc age threshold** → **no age flag.** Flag only broken / orphan / stale-stamp (exact signals). "Old" ≠ "wrong".
3. **Report location** → **in-chat, write nothing.** No `docs/_reports/` — so the audit can't itself become sprawl.
4. **Duplication check** → **defer.** v1 ships the deterministic checks only (index coverage, orphans, broken cross-refs, stale-stamp, read-order integrity); add the fuzzy overlap heuristic later.

> **Status**: decision-ready. **Build is parked** in `backlog/2026-06-05-doc-organiser.md` — a side-quest, *not* on the C1→C5 spine. Resurface after the spine, or when a doc-drift sweep is wanted.

---

*Next move if approved: a backlog item + a `doc-organiser` SKILL.md. Not started — this is propose-only per the ticket.*
