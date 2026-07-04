# Loose-Ends Ledger — 2026-07-04

**Purpose**: every open item from the 2026-07-02→04 orchestration session (constellation → pipeline → extension cut → engine), one line each, owner-tagged — so the session itself is disposable. In backlog/ deliberately: the project-digest's NEEDS-YOU scan can see it.

**For Agents**: work items owned by `me/engine` are claimable; `David` items surface in the briefing, don't nag.

## Needs David (decisions / one-clicks)

| # | Item | Weight |
|---|------|--------|
| D1 | Create GitHub org **`kyberagent-extensions`** (web UI, one click) → then I split `omi-fetch/extension/` into its own repo there | 1 min |
| D2 | **SDK mount gap** (the real one): additive handler wiring past the `seam/handlers.ts` wall · an ④ Events SDK builder · publish the SDK as a package. Input: `omi-fetch/extension/FRICTION.md` | David's KBDE work |
| D3 | Retire failing `com.appydave.omi-sync` launchd job (superseded by omi-fetch pulse) — say the word, I execute | 1 line |
| D4 | Design-lint placement: standalone tool or Mochaccino mode? (oldest open decision; digest NEEDS-YOU #1) | decision |
| D5 | DF-7 greenlight + first-ingestion code-review — pre-existing backlog opens the digest surfaces | decision |
| D6 | Poster taste-check (design 10 alternates) — optional | optional |
| D7 | The **pending big project brief** you said you'd attach as a separate file | when ready |
| D8 | Coffee-shop capture cut off mid-thought ("…you take the omi—") — re-speak if it mattered | optional |

## Mine / engine (claimable work)

| # | Item | Where specced |
|---|------|---------------|
| M1 | Engine hardening before pool>1: CAP/429 governor · auto-wake (C3/DF-10) · per-ticket-kind VERIFIERS · live-exercise HITL gate · switchboard `swagger-*` naming | `engine/docs/ENGINE-NOTES.md` |
| M2 | AngelEye-sentinel extension (#5 of the cut, unbuilt) | `app-pipeline/angeleye-sentinel.md` |
| M3 | Cortex KDD scan — needs Roamy + staging-vs-ratified schema fix | `kdd-viewer/docs/extension-notes.md` |
| M4 | Project-digest #2: wire `needs_you.markers` config, add second project | `project-digest/docs/extension-notes.md` |
| M5 | appyradar-sentinel blind to Roamy (collector Mini-only) | `backlog/problems.md` 2026-07-02 note |
| M6 | DF-7 state plane rebuild (flat files → service) — future, post-hardening | `backlog/specs/df7-*.md` + `docs/harness-evaluation.md` |

## Standing context (not work, don't lose)
Engine proven 2026-07-03 (`96fe799` = first worker-made commit) · orchestrator-delegation pattern is standing practice · extension model = iframe/repo-per-ext/package.json→SDK · three-folder rule pinned in constellation-map · "M4 Pro" = Roamy = the MacBook Pro.
