# DF-ADR: the canonical Dark Factory ADR format — design doc

**Status:** proposed (companion to [ADR-0044](decisions/0044-adopt-a-canonical-df-adr-format.md), which is
the decision this doc justifies). This file carries the research grounding; the ADR carries the decision
itself, kept short per its own template.

## Why this needed a real decision, not a guess

Dark Factory isn't just documenting its own architecture — it's the one place expected to (a) hold the
factory's own build decisions, (b) issue guidance/machine-readable structure that steers *other* microapps
(skill selection, agent-team conventions, ticket shape), while (c) respecting that each app can run its own
SDLC. And per the "self-learning" ask: decisions shouldn't be write-once — they should accumulate
corroborating (or contradicting) evidence over time as Lisa keeps mining new sessions, the same way a
*learning* earns promotion to a *pattern* at recurrence ≥3.

Four of David's own repos already have a live answer to "what does an ADR look like here," and industry has
~15 years of ADR practice to draw on. Rather than invent a fifth shape, this surveys both and reconciles.

## What already exists (own projects)

| Repo | Convention | Shape |
|---|---|---|
| **Dark Factory** | two, unreconciled | `docs/watchtower/DECISIONS.md` (terse D1-D4, hand-authored) + `docs/kdd/decisions/*` (Lisa-reconstructed: Context/Decision/Alternatives Considered/Consequences/Related/Provenance) |
| **SupportSignal** | most production-tested — 3 months, 631 commits (2026-03-22 → 2026-06-22) | `docs/kdd/decisions/adr-NNN-*.md` (14 ADRs) with real machine-readable frontmatter: `adr_number, status, created, decision_date, story_reference, supersedes, superseded_by`; body keeps `## Status` visible even though it's also in frontmatter. Separate `docs/scribe/decision-log.md` (D001–D023, dense triage-to-ticket traceability log tied to a specific review sprint) ties findings → decision → ticket/commit — a distinct, lighter append-only log, not a substitute for ADRs. |
| **Cortex** | native, supersession-aware, but younger — ~5 weeks, 211 commits (2026-05-26 → 2026-07-02) | `ADR-NNNN`, `**Status:**` inline under the title, `Context/Decision/Rationale/Consequences/See also`. 48 ADRs. **Its own Lisa reconstruction batch (2026-07-02) was normalized INTO this native template at ratification, not left raw.** Explicit rule: "Never delete a superseded ADR." Supersession is recorded in prose, not a frontmatter field. |
| **KBDE** | 100% Lisa-raw | same shape as Dark Factory's reconstructed batch (no prior native format to reconcile into) |
| **poem-os** | heaviest, most narrative | own `docs/architecture-decisions/` + `docs/kdd/decisions/adr-NNN-*` + a BMAD template; adds Implementation + References sections |
| **storyline-app** | lightest, free-form | per-story `decisions.md`, not sequential/numbered — fine for a single story's scope, wrong shape for anything that needs to be found later |

**Read on this:** SupportSignal is the strongest precedent by actual production mileage — 3 months of
near-daily ticket creation is a real stress test a 5-week rebuild hasn't had. Its frontmatter
(`supersedes`/`superseded_by`/`story_reference` as real YAML fields, not prose) is what this design borrows
directly. Cortex adds one thing SupportSignal doesn't have to draw on: a lived example of folding a *Lisa
reconstruction batch* into a native format at ratification — exactly the situation Dark Factory is in right
now — plus its explicit "never delete a superseded ADR" rule. Both matter; neither alone was sufficient.

## What industry practice adds (cited)

- **Nygard (2011)**, the origin of ADRs: five sections — Title/Status/Context/Decision/Consequences.
  Consequences records *all* outcomes, not just the positive ones.
  [cognitect.com/blog/2011/11/15/documenting-architecture-decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- **MADR** (current spec): structured `status` frontmatter that *encodes supersession in the field itself*
  (`superseded by ADR-000X`), `decision-makers`/`consulted`/`informed` (RACI-derived), explicit
  **Considered Options** with pros/cons per option (makes rejected alternatives first-class, not narrative
  aside), and a **Confirmation** section for how compliance is verified.
  [adr.github.io/madr](https://adr.github.io/madr/)
- **Y-statements**: a one-paragraph form ("In the context of X, facing Y, we decided Z over W, to achieve Q,
  accepting R") for high-volume small decisions where full-template ceremony would suppress recording them
  at all. [ozimmer.ch / Y-Statements](https://medium.com/olzzio/y-statements-10eb07b5a177)
- **Supersession convention**: edit the *old* ADR's status in place to forward-link
  (`Superseded by ADR-00XX`); never delete. Decentraland's process goes further, requiring a Deprecation
  Reason section distinguishing "once valid, now outdated" from "never accepted."
  [adr.decentraland.org/adr/ADR-277](https://adr.decentraland.org/adr/ADR-277)
- **Cross-repo / organizational ADRs**: orgs distinguish "you must comply" from "you were told" via the same
  RACI-style frontmatter used for supersession (`decision-makers` vs `consulted` vs `informed`), or park
  cross-cutting decisions in a separate shared collection that downstream repos cross-link to rather than
  duplicate.
  [hidekazu-konishi.com — ADR templates and operational patterns](https://hidekazu-konishi.com/entry/architecture_decision_records_templates_and_operations.html)
- **Machine-mined / retrospective decision records**: Lore encodes decision context into git-commit
  trailers for AI coding agents — `Constraint`, `Rejected`, `Directive`, `Confidence: low/medium/high`,
  `Scope-risk`, `Reversibility` — explicitly because reconstruction can't recover reasoning that was "never
  written down." Its `Confidence` field is an *author's self-assessment*, not a derived score — the honest
  limit of any after-the-fact record. [arXiv:2603.15566](https://arxiv.org/html/2603.15566v1)

## The design

### Frontmatter (new — borrows SupportSignal's machine-readable fields + MADR's status discipline)

```yaml
---
id: ADR-NNNN
title: <imperative or noun phrase>
status: proposed | accepted | deprecated | superseded
supersedes: ADR-XXXX        # present only when this decision reverses an earlier one
superseded_by: ADR-YYYY     # present only once status becomes `superseded` — filled on the OLD file
scope: internal | cross-app-guidance | delegated
applies_to: [app-slug, ...]  # only when scope: cross-app-guidance
date_decided: YYYY-MM-DD
deciders: [David Cruwys]
confidence: reconstructed | proposed | confirmed
recurrence_count: N          # corroborating sessions, same mechanic Lisa already uses for pattern promotion
provenance:
  sessions: [...]
  files: [...]
  commits: [...]
tags: [...]
---
```

### Body (Cortex's proven shape, kept, plus two DF-specific sections)

```markdown
# ADR-NNNN: Title

## Context
## Decision
## Alternatives Considered      <- explicit, MADR-style: rejected options are first-class, not an aside
## Consequences
## Applies To                   <- ONLY for scope: cross-app-guidance — which apps, how it's enforced
## Related
## Provenance                   <- human-readable mirror of the frontmatter citation
## Revision Log                 <- append-only: date · event (reaffirmed/corroborated/challenged) · note
```

### The three fields that are actually new (everything else is borrowed, not invented)

**`scope`** — the field that answers "DF writes tickets for other apps but apps own their own SDLC."
Three values, deliberately simple rather than a full RACI matrix:
- `internal` — how Dark Factory itself is built (most of what the reconstruction just produced)
- `cross-app-guidance` — DF is setting a standard other microapps are expected to follow (skill
  selection, machine-readable schemas, agent-team conventions). Gets an `Applies To` section.
- `delegated` — explicitly NOT a DF decision. A pointer used when DF notices an app made its own local
  call and cross-references it, without DF's KDD silently absorbing it as if DF owned it.

**`confidence` + `recurrence_count` + Revision Log** — the self-learning hook. Not new infrastructure:
Lisa's clustering already computes `recurrence_count` for *learnings* promoted to *patterns* — this
proposes the same mechanic for *decisions*. Every subsequent Lisa run (steady-state, per-ticket capture,
not a batch reconstruction) that finds a session reaffirming, depending on, or citing an existing decision
appends a line to its Revision Log and bumps `recurrence_count`, rather than spawning a duplicate ADR or
silently doing nothing. A session that *contradicts* an existing decision is Lisa's existing `conflict`
verdict — which should now also downgrade `confidence` and flag the ADR for a supersession review, instead
of just sitting in a reconcile-triage report. `confidence` itself borrows Lore's honesty: it's a
self/measured assessment (`reconstructed` = mined after the fact, `proposed` = decided but unconfirmed by
practice, `confirmed` = corroborated by ≥1 later session), not a derived precision score — reconstruction
genuinely can't recover reasoning nobody wrote down.

### Supersession vs. merge — these are different situations, don't conflate them

The two pairs merged by hand on 2026-07-04 (ADR-0006/0023, ADR-0036/0040) were **duplicate recordings of
the same moment** — two sessions on the same day describing one decision. Merging into one file was
correct there.

**ADR-0020/0021 in this repo right now is a different case** — a genuine same-day *reversal*
("build a doc-organiser skill" → "don't; wire the existing doc-drift/doc-review family instead"). Per
Cortex's rule and MADR's status field, this should NOT be merged — it should be linked: 0020 gets
`status: superseded`, `superseded_by: ADR-0021`; 0021 gets `supersedes: ADR-0020`. This is the first real
candidate for the new field, and worth fixing during ratification as a concrete demonstration.

## Rollout (no automation changes required to start)

1. **Adopt now** for every new decision going forward, hand-authored or Lisa-extracted.
2. **Reformatted (done, 2026-07-04)**: all 41 proposed candidates now use this template — frontmatter +
   Revision Log added, content unchanged, mirroring what Cortex did with its own reconstruction batch.
3. **Fixed (done, 2026-07-04)**: ADR-0020/0021's supersession link — the first live use of the field.
4. **Full content ratification: deliberately deferred, not batched.** David's call, 2026-07-04 — don't
   spend judgment ratifying all 41 up front. They already passed extraction, clustering, human review, and
   adversarial drop-review, so `status: proposed` / `confidence: reconstructed` is a legitimate resting
   state, not neglect. Ratify **lazily, one at a time, only when a specific decision is about to matter**
   (a build touches it, or a later Lisa run corroborates/contradicts it) — this is the actual point of the
   `confidence`/`recurrence_count`/Revision Log design: recurrence does the prioritizing, not a sweep.
5. **Leave `docs/watchtower/DECISIONS.md` (D1-D4) untouched** — historical, binding, predates this format;
   reference it, don't retrofit.
6. **Leave Cortex and KBDE alone** — no retroactive changes to sibling projects. Dark Factory's format is
   now explicitly modeled on Cortex's, so cross-project harmonization stays easy later if wanted.
7. **Later, separate follow-up (not part of this decision):** extend Lisa's `extractor-schema.md` and
   `reconcile-classifier-schema.md` so future *reconstructions* natively emit `scope`/`confidence`/
   `recurrence_count`, instead of needing a manual reformat pass each time. Flagged, not built — this
   proposal is the format; teaching Lisa to emit it natively is a follow-on ticket.

## Closing three gaps from the reconstruction (decided 2026-07-04, after the fact)

This format proposal only reformatted the 41 *decisions*. Three loose ends from the reconstruction
itself surfaced afterward — closing each explicitly rather than leaving them silently unaddressed:

- **Learnings and patterns (45 + 2) ratification: same rule as decisions.** No reason for a different
  standard — they passed the same extraction/cluster/review gate. `status: proposed` on the learning
  and pattern docs is an equally legitimate resting state; ratify lazily, one at a time, only when a
  specific one is about to matter. Not reformatted into DF-ADR frontmatter (that format is
  decisions-specific — learnings/patterns already carry their own frontmatter from `emit`), just the
  same deferral philosophy.
- **The "search wider" sign-off duty: adequate as done, not a gap.** Lisa collected ~250
  `prior_art_hints` across candidates; nearly all were self-referential to Dark Factory's own `docs/`
  and memory. That's expected, not under-searching — these are Dark Factory's *own* architecture
  decisions, not ported from another system the way Cortex reconciled against its v1. There is no
  plausible external repo holding undiscovered prior art on how Dark Factory decided to build its own
  queue or engine. Closing this without further search.
- **`improve-eval`/`improve-gate`: explicitly skipped, not silently omitted.** This stage measures the
  extractor/classifier against real human disagreement (accept vs. reject) and only keeps a prompt
  revision if it measurably improves agreement. This run produced **14 accepts, 0 rejects** at the
  review gate — no disagreement signal exists yet to learn from. Running it now would only confirm
  trivial 100% agreement. Revisit if a future ratification pass actually finds the classifier wrong
  about something — that's the point at which there'd be a real label to measure against.
