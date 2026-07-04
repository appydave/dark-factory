# Six-App Evaluation — 2026-07-04

**Source**: OMI capture A266, "Evaluating Thin Extensions and Usability" (2026-07-04 08:06) —
David's verdict on the six things built 2026-07-03/04: *"they're all very thin… no search, no
inferred metadata, no summaries/usages/documentation, no find. Look at each from the point of
view of how someone would ACTUALLY use it — and they're meant to be used by both HUMANS and
AGENTS."* Also grounded in `backlog/2026-07-04-loose-ends-ledger.md` item M7 (the enrichment
round this doc executes) and each app's own `docs/extension-notes.md` / `FRICTION.md`, which
already name several of these gaps honestly.

**Method**: for each app, two personas walked 2-3 realistic tasks — human David and a fresh
Claude agent with no memory of the app — via the actual README, code, and CLI, not assumption.
Every finding below is a real file, line, or command, checked live (not inferred from names).

---

## Verdict table

| App | Search/find | Inferred metadata | Usage docs | Human UX | Agent affordance | Discoverability |
|---|---|---|---|---|---|---|
| omi-fetch (v2) | 2/5 | 3/5 | 4/5 | 3/5 | 3/5 | 1/5 |
| app-registry | 4/5 | 3/5 | 4/5 | 3/5 | 4/5 | 2/5 |
| project-digest | 1/5 | 2/5 | 4/5 | 3/5 | 3/5 | 2/5 |
| kdd-viewer | 1/5 | 2/5 | 4/5 | 2/5 | 1/5 | 2/5 |
| engine (orchestrator+store) | 1/5 | 1/5 | 4/5 | 2/5 | 2/5 | 3/5 |
| omi-fetch/extension (KBDE) | 1/5 | 2/5 | 5/5 | 1/5 | 1/5 | 1/5 |

Scale: 1 = absent/blocking, 5 = genuinely solves the problem today.

**A pattern across all six, worth naming once instead of six times**: documentation quality is
uniformly high (David's own `docs/extension-notes.md` convention is working — every app names
its own gaps honestly, nothing here is hidden). The consistent weak points are *runtime* find
capability and *cold-start* discoverability — a stranger (human or agent) landing on any of
these six with zero prior context has no single path in.

---

## 1. omi-fetch (v2)

**Verdict**: v2 made real, honest progress on the "thin" complaint — sequential capture codes
(`A000`…) give every conversation a permanent, referenceable handle, and `enrich.py` adds a real
`tags`/`synopsis`/`signal` schema per record. But **search still doesn't exist**: `lookup.py`
resolves an *exact known code* to a record (`lookup.py A013`) or dumps the *entire* index
unfiltered (`lookup.py --list`, 274 lines) — there is no keyword, tag, date-range, or signal
filter. Worse, only **30 of 274 records (11%)** carry any tags/synopsis at all, because both real
enrichment engines (Gemini API, Gemini CLI) are confirmed broken and every enriched row so far
used the `--stub` heuristic fallback (`enrichment_engine` field proves this, honestly tracked).
The single most damaging finding isn't in the app's code at all: an **existing, unrelated**
appydave-plugins skill is also literally named `omi-fetch`
(`appydave-plugins/appydave/skills/omi-fetch/SKILL.md`) and triggers on the exact same natural
language ("what did I record", "what's in omi", "omi conversations") that a human or agent would
use to reach the *new* app's richer store. `skills-registry/SKILL.md` (line 134) still only
lists the old skill. Both humans and agents will reach for the dumber, older tool first and never
discover codes/tags/synopsis/cards-view exist.

| Task (human/agent) | Outcome today |
|---|---|
| "Find the OMI conversation about thumbnails from last week" | No search command. Must open `view/index.html` (200-row cap) and scroll, or `grep -i thumbnail store/index.jsonl` by hand. |
| "What did I capture yesterday morning, with context?" | `lookup.py --list` dumps everything unfiltered; no date filter flag. |
| Agent: "does an omi-fetch tool exist?" | Says "yes" — to the *wrong* one (the old sync-job skill), because it shares the trigger vocabulary and is the only one registered anywhere discoverable. |

**Top 3 improvements**
1. **High** — Add real find to `lookup.py`: `--search <substring>` over title/tags/synopsis, `--since <date>`, `--signal <kind>` — the fields already exist (v2 schema), just nothing queries them.
2. **High** — Fix or replace the enrichment engine so more than 11% of the corpus carries real tags/synopsis (Gemini paths are both confirmed broken; either fix `~/.secrets`/CLI auth or swap to a working engine) — `--stub` is a permanent fallback, not a plan.
3. **High** (shared with app-registry, see cross-cutting) — Resolve the `omi-fetch` skill/app name collision so natural-language requests reach the new store, not the old one.

---

## 2. app-registry

**Verdict**: the strongest **find** surface of the six, by a clear margin. `query.py` ships six
real verbs — `running`, `dark`, `layer <name>`, `app <id>`, `stale --days N`, `drift`, `all` —
each printing clean JSON, each doing exactly what a human or agent would actually ask for
("which apps are dark right now", "what drifted from the constellation map"). The three-opinion
model (`verdict_status` from constellation.json, `apps_json_status` from apps.json, `live.status`
from a fresh probe) is genuinely good design: it surfaces disagreement instead of silently
picking a winner. The gap is entirely **discoverability**, not the tool itself: no skill file
exists anywhere for the new `app-registry` (checked `skills-registry/SKILL.md` and the full
`appydave-plugins/appydave/skills/` tree — nothing), and it collides in *concept* (not quite
name) with the pre-existing `appydave:apps-registry` skill, which governs a completely different,
older file (`~/.config/appydave/apps.json`) and triggers on "list apps" / "find app" / "what apps
do I have" — exactly the phrasing someone would use to reach the new, richer tool.

| Task | Outcome today |
|---|---|
| "Which apps are dark right now and why" | `python3 query.py dark` — works well, today, one command. |
| "Has anything drifted from the constellation map" | `python3 query.py drift` — works well, today. |
| Agent: "is there a registry tool in this ecosystem?" | Finds `appydave:apps-registry` (the old one) first — no skill points at this one. |

**Top 3 improvements**
1. **Med** — Register a thin skill (or a `CLAUDE.md` pointer) for `app-registry`'s `query.py`, distinct enough from `appydave:apps-registry` that both are individually reachable.
2. **Med** — Add a one-line disambiguation note in each skill's description ("this is the OLD/per-machine apps.json editor" vs "this is the fresh liveness+drift registry") so an agent that finds either one knows the other exists.
3. **Low** — The stage-2 MCP wrapper named in `docs/extension-notes.md` (deferred, not built) would remove the "shell out to python3" step for agents — worth doing once discoverability is fixed, not before.

---

## 3. project-digest

**Verdict**: the best-designed **field shape** of the six — the five-field morning-briefing box
(GOAL / NEEDS-YOU / SINCE / IN-FLIGHT / SHIPPED / LIVE-NOW) is exactly the right compression for
"where are we." But it is functionally a single-project demo today: **only one project is
configured** (`projects/dark-factory.json`) against a fleet of ~40 constellation apps, and there
is no way to discover *what's configured* short of `ls projects/` — `lib/config.py`'s
`list_project_ids()` already exists and is used only inside an error message
(`config.py:73`), never exposed as a real command. `digest.py --list` does not exist.

| Task | Outcome today |
|---|---|
| "What needs me this morning, across projects" | Impossible — no multi-project loop, no list of what's configured, exactly one project wired up. |
| "Give me a digest of dark-factory" | `python3 digest.py dark-factory` — works well, today. |
| Agent: "what project ids can I even ask for?" | Must guess or `ls projects/*.json`; the answer function exists but isn't callable directly. |

**Top 3 improvements**
1. **Med** — Expose `digest.py --list` (thin wrapper over the already-built `list_project_ids()`) — this is a one-line fix for a real discoverability gap.
2. **Med** — Onboard project #2 for real (per the app's own README "Adding a project" section) — the generalization seam is designed but genuinely unexercised; `docs/extension-notes.md` names three real risks (marker vocabulary, goal-extraction mode, done-convention) that won't surface until it's tried.
3. **Low** — Wire `needs_you.markers` from config (schema field exists, `lib/needs_you.py` doesn't read it yet) — named as the #1 item for project #2 in the app's own extension-notes.md.

---

## 4. kdd-viewer

**Verdict**: the weakest **find** of the six, by explicit design choice, not oversight — the
README's own Non-goals section states "No search" outright for v1. The normalize-first
architecture (one adapter config per KDD instance, real per-instance messiness absorbed cleanly —
title precedence, category-as-directory-path, fragile `promoted_to_pattern` resolution) is
genuinely well-built and honestly documented (`docs/extension-notes.md`'s normalization mapping
table is excellent). But the only way to answer "what do we know about decision X" is opening
`view/<id>.html` in a browser and reading every card in the right tab by eye — there is no
keyword match, and an agent (which can't meaningfully browse a tabbed HTML page) has no better
path than reading `store/instances/<id>.json` directly, a path the README never actually points
an agent toward as a *first-class* interface (it's framed as an internal artifact, not a query
surface).

| Task | Outcome today |
|---|---|
| "What do we know about decision X in project Y" | Open the HTML, click the Decisions tab, scan by eye. No search. |
| "Show me all learnings tagged Z across projects" | No cross-instance query exists at all (explicit Non-goal). |
| Agent: same task | `store/instances/<id>.json` is machine-readable and well-shaped, but nothing tells the agent to read it instead of trying to "view" the HTML. |

**Top 3 improvements**
1. **Med** — Add a minimal `query.py` (or `scan.py --grep <term>`) doing title/category substring match over `store/instances/<id>.json` — doesn't need full-text search, just breaks "must eyeball every card."
2. **Med** — Add one README line pointing agents at `store/instances/<id>.json` as the machine-readable interface, explicitly, alongside the HTML view.
3. **Low** — Scan Cortex for real (it's configured but `"unscanned": true`, wrong machine) — proves the normalize-first bet against a second, structurally different instance (staging/ratified split named as the expected break point).

---

## 5. dark-factory engine (orchestrator/warm_pool/consumer + store)

**Verdict**: the best-built *bones* of the six — the ticket JSON schema (`queue_id`,
`requested_by`, `verify_kind`, `claimed_by`/`claimed_at`, `audit.jsonl`'s ticket→worker→session
chain) is genuinely rich and consistent, and `docs/ENGINE-NOTES.md` is an exemplary as-built
record (it names every known limitation, including its own gaps, without hiding any). But there
is **zero aggregation**: no status script exists anywhere in `engine/` — answering "what's queued
right now, how old is the oldest ticket, did ticket X succeed" today means `ls store/queue/
store/done/` and opening each JSON by hand. And `orchestrator.py`'s `VERIFIERS` dict
(`orchestrator.py:217`) has **exactly one entry** (`verify_constellation_4_apps`) — every other
ticket kind, including the 8 this evaluation is about to file, has no automated verification path
at all; the orchestrator can only trust the worker's own self-report for anything outside that
one hardcoded case.

| Task | Outcome today |
|---|---|
| "Is the engine currently running or dead" | `tmux ls` — works, if you know to look. |
| "What's in the queue right now and how old is the oldest item" | Manual `ls` + read each JSON's `requested_at`; no computed age/depth anywhere. |
| "Did ticket X succeed and what did it produce" | Check `store/done/` vs `store/queue/` by hand, then read the ticket's own `verified` field if it made it to `done/`. Works, but entirely manual. |
| Agent: "find all tickets related to omi-fetch" | `grep -l omi-fetch store/*/*.json` — works, but nothing surfaces it as a supported query. |

**Top 3 improvements**
1. **High** — Build `engine/status.py`: queue depth, oldest ticket age, last N done tickets with title+outcome, sourced from `store/queue/`, `store/done/`, `audit.jsonl` — the exact aggregation gap named above.
2. **High** — Generalize `VERIFIERS` beyond the single `constellation-4-apps` entry — at minimum a generic "named file(s) changed + parses + contains expected keys" declarative verifier, so new ticket kinds (like this evaluation's own tickets) are machine-verifiable, not self-report-only.
3. **Med** — A `find`/`grep` convenience wrapper (`engine/find.py <term>`) over `store/*/*.json` — small, but turns a known manual habit into a supported command.

---

## 6. omi-fetch/extension (the KBDE extension attempt, validated-unmounted)

**Verdict**: technically the most sophisticated artifact of the six (real `@kyberagent/
extension-sdk` builders, `validateExtensionDefinition` passes with zero errors, both ③ Data and
④ Events channels have real, SDK-shaped handler code) and by far the **best-documented** —
`FRICTION.md` (197 lines, ranked, with exact file/line citations) is a first-consumer bug report
of publishable quality, turning "this doesn't work" into five specific, ranked SDK gaps. But it
is, today, **a feature nobody can reach**: `status: validated-unmounted` means zero human or agent
usability — the surface has never rendered in a real KBDE host, the data endpoint has never
answered a live query, nothing scans `omi-fetch/extension/` for a manifest. Mounting is blocked
on a *named, external* gap (`packages/daemon/src/seam/handlers.ts` must be hand-edited — outside
this build's placement rules, tracked as ledger item D2, David's own KBDE work). Even once
mounted, `search(query)` is explicitly still "not built" per both `FRICTION.md` and
`docs/extension-notes.md`.

| Task | Outcome today |
|---|---|
| "Glance at today's OMI captures from the KBDE dashboard" | Impossible — unmounted, no live surface. |
| "Search OMI transcripts from within KBDE" | Would still be impossible even mounted — `search()` isn't built at the SDK layer this extension targets either. |
| Agent: "is there a KBDE surface for OMI data?" | No — nothing scans this folder; it's orphaned from any manifest discovery today. |

**Top 3 improvements**
1. **Low** (blocked externally, tracked as ledger D2 — not dark-factory's to fix) — Mounting itself needs KBDE's `seam/handlers.ts` wiring or the SDK's own additive-handler milestone; this is David's call on the KBDE side, already queued.
2. **Med** — Add a one-line pointer in `omi-fetch/README.md` ("an extension attempt exists at `extension/`, status: validated-unmounted, see `extension/FRICTION.md`") — today a reader of the main app's README has no idea this exists at all.
3. **Low** — Once mounted, revisit `search(query)` as the first real gap (both docs already name it) — no new discovery needed, just sequencing.

---

## Cross-cutting findings (worth fixing once, not six times)

- **Name collisions actively hide the new tools.** `appydave:omi-fetch` (old sync-job skill) and
  `appydave:apps-registry` (old `apps.json` editor skill) both share trigger vocabulary with the
  new dark-factory apps of nearly the same name. Any natural-language ask — human or agent — will
  resolve to the *older, dumber* tool first, because that's the only one registered in
  `skills-registry/SKILL.md`. This is worse than "thin": the new tools' real capability (capture
  codes, tags, drift detection) is functionally invisible, not just underdeveloped.
- **Constellation.json IS the discoverability floor, but it's circular.** All four apps
  (omi-fetch, app-registry, project-digest, kdd-viewer) are correctly listed in
  `mochaccino/data/constellation.json` — so `app-registry`'s own `query.py all` would surface
  them. But you have to already know `app-registry` exists to reach that list. Nothing outside
  dark-factory (a skill, a CLAUDE.md line, an MCP tool) points a cold agent at the constellation
  map or at `app-registry` as the entry point.
- **Documentation is not the gap.** Every one of the six has an honest, detailed
  `docs/extension-notes.md` (or `FRICTION.md`) that already names most of the findings above.
  The gap is exclusively *runtime* — find, aggregate, and be found — not *written* documentation.

---

## Single best / single worst (across all six)

- **Best**: `app-registry`'s `query.py` — six real, well-chosen find verbs
  (`running`/`dark`/`layer`/`app`/`stale`/`drift`/`all`) that answer the actual questions David
  asks, working today, no caveats.
- **Worst**: the `omi-fetch` and `apps-registry` **skill/app name collisions** — two of the four
  new query tools are functionally invisible to natural-language use (by David or an agent)
  because an older, less capable tool with the same trigger words answers first. This is a single
  root cause hurting two of the six items simultaneously.
