# Session Order — dark-factory

**Purpose**: Ordered, deduped record of what was actually built across recent Claude Code sessions, triangulated against git. The clean sequential audit ("ordering the dark factory") — latest-wins, with the tried→abandoned trail kept.

**For Agents**: Read this to understand *what happened and in what order*, including claims that did NOT survive triangulation. Where this disagrees with code/git, code wins — flag the drift.

**Generated**: 2026-06-21 via session-archaeology workflow (8/8 session readers)
**Source sessions**: 2026-06-10 → 2026-06-16
**Method**: fan-out one reader per session → triangulate every evidence anchor vs git+disk → latest-wins synthesis

> **Triangulation summary**: Very clean set: 100+ anchors checked, ~88 confirmed against the repo (commits, files, symbols, content), ~17 unverifiable (Linear-style IDs, GitHub/npm-UI/remote-machine/session-JSONL/Playwright-render claims not checkable from local git), and 3 effectively missing/misstated (queue/ job file moved to done/, a bare appyradar-sentinel git SHA 23639a4 that doesn't resolve, and the "apps/switchboard 399-line SSE" claim — switchboard exists only as backlog specs/job records, not committed app source).

---

> **⚠️ Correction (2026-06-21): the "Switchboard doesn't exist on disk / design-only"
> finding below (triangulation summary above, Thread G, and contradiction #4) is WRONG —
> a `repoPath` scoping artifact. The archaeology searched for `apps/switchboard` *inside*
> the dark-factory repo (where `apps/` holds only `watchtower/`) and missed that Switchboard
> is a real sibling app at `~/dev/ad/apps/switchboard` (git repo, 17 source files,
> `src/deliver/sse-deliver.ts`, commits: SSE deliver channel `a3dd0d8`, `POST /jobs`
> ingest `c81b219`, durable claimable job tickets `489117c`, topic-selective replay
> `d1506ba`). SSE + replay + queue persister + job ingest are all real, exactly as
> CONTEXT.md describes. The earlier `AUDIT-2026-06-12.md` "Switchboard README under-claims
> by an entire build" drift was therefore CORRECT, not overstated. Verified on disk
> 2026-06-21. Everything else in this record stands.**

---

# Dark Factory — Cross-Session Synthesis (8 sessions, 2026-06-10 → 2026-06-16)

## 1. Verified arc (one line per session)

1. **S1 (06-10)** — Framed Dark Factory as "agentic MES / agent-fleet control plane"; ran fleet-orchestrator deep-research (7 OSS projects, stateless-floor split is green-field); created `docs/upstream-repos/` shelf; cleaned 72-file untracked rot in 7 commits; wrote DF-9 git-hygiene sentinel spec. ✓
2. **S2 (06-10→11)** — AppyRadar/AppySentinel naming audit; fixed `appysentinal→appysentinel` misspelling + GitHub rename; clean re-scaffold of `appyradar-sentinel` (node_modules history pollution fix); archived two old repos; live fleet collection test from Roamy. ✓
3. **S3 (06-12)** — Autonomous Swagger session: claimed/executed ticket `q-20260612-cortex-brain-v4` (brand-cold colour fix across 4 cortex HTML designs), moved to `done/`. ✓
4. **S4 (06-15→16)** — `system-context` skill refresh of `CONTEXT.md` + `context.globs.json` (constellation-aware); **written but never committed**. ✓ (files on disk, uncommitted)
5. **S5 (06-16)** — doc-drift audit over 11 code-anchored docs (21 findings, 1 critical); doc-organiser proposal superseded; committed `6b91d46`; aborted Cortex re-comprehend after multi-window collision. ✓
6. **S6 (06-11→16)** — Re-comprehended Cortex at v0.12.0 (`7db2dce`); correctness pass on cortex deck; built design `07-memory-fades`; full-gallery design-lint 8/8 PASS; proposed architecture-doc set. ✓
7. **S7 (06-16)** — doc-architect Gate-4 fired on dark-factory; doc-review 4-dimension sweep; supersession banners + INDEX coverage on `watchtower/` cluster; committed `ef4d618`. ✓
8. **S8 (06-12)** — Grounding/drift audit (5 Haiku crawlers + Opus synthesis); `AUDIT-2026-06-12.md`; three architectural decisions ratified with David; zero builds. ✓

> **Chronology note:** session digests are *labelled* oldest-first but the timestamps interleave. S8 (06-12) and S3 (06-12) predate S4–S7 (06-15/16). The audit (S8) is the analytical spine; S5/S6/S7 are the doc-hygiene aftermath.

---

## 2. Cross-session threads (grouped, latest-wins)

### Thread A — What Dark Factory *is* (class identity)
- **S1**: Defined as agentic MES / agent-fleet control plane. Core moat: **stateless floor + separate state-plane services**. Ruflo flagged as architectural *opposite* (Queen-led shared central state). ✓ `dark-factory-class-is-agentic-mes.md`
- **S1**: Deep-research confirmed the stateless-floor split is **green-field** — no surveyed OSS project ships it. ✓ commit `6ee755b`, `docs/upstream-repos/2026-06-10-fleet-orchestrator-research.md`
- **S4**: `CONTEXT.md` crystallised 8 architectural dimensions: North Star "talk-to-it factory", 3 planes (floor/Switchboard/Watchtower) + 2 read-only sensors (AngelEye/AppyRadar), Marshall→Swagger→workflow runtime, billing = in-session/Max-plan never cron/API. ✓ (file on disk, **uncommitted**)
- **Current truth**: agentic MES; identity + observability are the two missing structural pieces (S8), *not* AI capability.

### Thread B — Constellation app naming (the long-running confusion)
- **S2**: Established AppyRadar (sensor app) vs AppySentinel (substrate/framework). Fixed misspelling, re-scaffolded clean repo, archived olds. ✓
- **S5**: Rename propagated through docs (`appyradar-sentinal` → `appyradar-sentinel`). ✓ `6b91d46`
- **S7**: doc-review confirmed rename landed. ✓
- **S8**: Logged Drift #5 (local `appyradar-sentinel` correct vs archived GitHub `appyradar-sentinal` missing the *e*). ✓
- **Current truth (verified on disk today):** under `~/dev/ad/apps/` the live dirs are `appyradar-sentinel` and `appysentinel`; archived as `_archived--appyradar` and `_archived--appyradar-sentinal`. ✓
- ⚠️ **DOWNGRADE:** S2's anchor `~/dev/ad/apps/ — 4 repos: appyradar, appysentinal, appyradar-sentinal, appystack` is **✗ missing** — those exact names/spellings don't exist on disk. There is **no `appystack`** under `apps/`. Treat that line as session-narrative, not ground truth.

### Thread C — appyradar-sentinel: what was actually built
- **S2**: Claimed real working sensor — SSH transport, 7 collectors, tiered-pulse engine, disk archaeology, 9-tool MCP, "214 tests / 462 assertions". ?
- **S8**: Logged Drift #4 — "proven live 2026-06-11" vs the only commit being a clean re-scaffold the same date; "215 tests". ✓ (drift confirmed)
- ⚠️ **DOWNGRADE / contradiction:** the rich feat-branch history (SHA `23639a4` etc.) is **✗ missing** — the re-scaffolded repo has a *single* commit `104c191`; historical SHAs are gone. Test counts (214 vs 215) are **? unverifiable** (no committed run log) and the two sessions disagree. The "live fleet collection" results are **? unverifiable** (runtime). **Net: the working code may be real, but the only repo-checkable artifact is one clean-scaffold commit. Do not cite "proven live" or a specific test count as fact.**

### Thread D — Cortex Mochaccino deck (the worked example for design rules)
- **S3** (06-12): Autonomous Swagger fixed v4 brand-cold colour failure across 4 designs; `#ffde59` restored (02=1,03=1,04=2,06=1, was 0). ✓ (grep-confirmed)
- **S6**: Re-comprehended Cortex at v0.12.0; correctness pass (provenance → `7db2dce`); built `07-memory-fades`; gallery 8/8 PASS. ✓
- **S5**: Attempted re-comprehend at `88aa6bf`, **reverted** on multi-window collision (read-only SSH, zero writes to remote). ✓ (proof dir `cortex-7db2dce/` confirmed)
- **Current truth**: cortex audience deck = 7 screens (01-07); data provenance pinned to `7db2dce` (v0.12.0); two-layer colour model is canonical (warm `#ffde59` load-bearing, cool semantic structure-only).
- **Design rule provenance**: `docs/david-design-patterns.md` (canonical style) + `tools/design-lint/RUBRIC.md` (operational). design-lint **must cover the gallery index**, not just individual designs (S6 lesson, `memory/design-lint-must-cover-the-index.md`). ✓

### Thread E — Watchtower three-way name collision (resolved)
- **S4/S5**: Flagged "Watchtower" = 3 meanings. ✓
- **S8**: **Resolved by David**: `apps/watchtower` = durable production home (rebuild on AppySentinel/AppyStack template when de-risked); `experiments/watchtower-engine` = **disposable** spike (do NOT promote in-place); brain's "control surface" concept describes the engine but was mis-filed at the app. ✓ `memory/watchtower-app-vs-engine.md`
- **Current truth**: `apps/watchtower` is a single-commit RVETS scaffold (Socket.io stubs, no persistence) — confirmed on disk today (only `watchtower` exists under `apps/`). The `rename(2)` atomic-claim mutex in `experiments/watchtower-engine/bin/claim-next.sh:28` is real and will be *graduated*, not the directory. ✓

### Thread F — Doc-hygiene programme (drift → review → architect)
- **S5**: doc-drift sweep, 15 files, `6b91d46`. ✓ (subject: "docs: doc-drift sweep — refresh code-anchored docs vs current code")
- **S5**: doc-organiser proposal superseded — doc-drift covers vertical (code↔doc), doc-review covers horizontal (doc↔doc-set). Only gap = dispatch wiring. ✓
- **S7**: doc-architect Gate-4 (defer-to-governance) fired; doc-review 4-dim sweep; supersession banners on `watchtower/` cluster + INDEX coverage, `ef4d618` (6 files, 26 insertions). ✓
- **Current truth**: code↔doc drift cleared; superseded watchtower docs *banner-stamped* but **physically un-rehomed** (deferred per `RE-BUCKETING.md` — touches CLAUDE.md paths).

### Thread G — Loop closure / parallelism architecture (S8 decisions)
- **Parallelism-via-identity**: "two sessions conflict" reframed as an **identity** problem, not a locking problem. Sequence: safety-latch → stable IDs → state-partition-by-ID → worktrees-per-job → Switchboard-as-registry-LAST. ✓ `memory/parallelism-via-identity.md`
- **Loop families**: Watching loop (sensors→bus→glass) = 0% closed; Doing loop (claim→run→done→reaper) = ~80% closed (35 jobs proven; auto-wake C3c is the one missing wire). Recommendation **accepted, not built**: close doing-loop return-leg first. (state: discussed)
- ⚠️ **DOWNGRADE:** the audit's evidence for Switchboard ("399-line SSE transport + POST /jobs + MCP server", "real working SSE daemon") is **✗ missing** — there is **no `apps/switchboard` or `experiments/switchboard` on disk** (confirmed today). Switchboard exists only as backlog charters/specs + one `done/` job record. **The "Switchboard under-claimed by an entire build" drift is itself overstated — there is no committed Switchboard app to under-claim.** Treat Switchboard as design-only.

---

## 3. Contradictions resolved across sessions

| # | Contradiction | Resolution |
|---|---|---|
| 1 | **S2** "appyradar-sentinal has rich feat-branch history (214 tests, SHA 23639a4)" vs **S8/repo** "single clean-scaffold commit 104c191" | Re-scaffold (S2 itself) deliberately discarded history to drop committed node_modules. The rich history is **gone from the repo**; only `104c191` survives. Test count unverifiable. |
| 2 | **S6** "v3 ticket said drop yellow #ffde59" vs **S3** "v4 restores yellow" | Correct sequence: v3 (06-09) issued a *buggy* instruction (drop warm, use cool as fill); `docs/david-design-patterns.md` landed next day overruling it; v4 (06-12) reverses v3. v3 ticket is now **historically incorrect**, v4 is canonical. |
| 3 | **S8 audit** "promote watchtower-engine in place (the engine IS Watchtower)" vs **David's call** "experiments stay disposable" | David overrode the audit. Engine = disposable spike; `apps/watchtower` = durable rebuild target. The audit recommendation was wrong and explicitly corrected. |
| 4 | **S8** "Switchboard README under-claims a real 399-line SSE daemon" vs **repo (today)** "no switchboard app exists" | **Unresolved in David's favour — the drift claim is unverifiable/overstated.** No Switchboard source is committed anywhere. The "walking skeleton vs real daemon" drift cannot stand. |
| 5 | Claude (S8) framed parallelism as multi-machine, Switchboard-first | David corrected twice: on-machine worktrees suffice for easy parallelism; build Switchboard registry **last**. The locking metaphor was scrapped. |

---

## 4. Negative knowledge (don't-repeat list)

- **Don't blind find-replace `sentinal→sentinel`** — the radar repo legitimately used the old spelling in cross-refs; AngelEye SKILL.md historical session tags (`appysentinal`, session `8f2325dd`) must stay to preserve telemetry retrieval. (S2)
- **Don't re-run the scaffold CLI to "clean" a repo** — risks diverging from tested code. Clean working-tree copy + fresh `git init` is the chosen method. (S2)
- **Don't put architectural-exemplar repos in `research/recon/`** — that's the skill-distillation crawler corpus. Use `docs/upstream-repos/`. (S1)
- **Don't drop the warm `#ffde59` anchor for cool semantic fill** (the v3 bug); don't force HTML-primary designs into SVG. Cool is structure-only; SVG only where content genuinely IS a flow/cycle. (S3/S6)
- **Don't lint only individual designs** — always screenshot the gallery index too. (S6)
- **Don't promote `experiments/watchtower-engine` in place** — experiments stay disposable; rebuild proven mechanics on a template in `apps/`. (S8)
- **Don't build Switchboard / file-locking first** for parallelism — identity → partition → worktrees → Switchboard-last. (S8)
- **Don't start comprehend work on a shared remote repo without checking for an active concurrent window** — S5 collided with another window on Cortex. AngelEye/Switchboard are the real fix. (S5)
- **Don't spend Fable 5 on mechanical work** — crawl/count/grep audits suit Haiku+Opus; reserve Fable for architectural reconciliation. (S8)
- **Don't trust READMEs as ground truth** — recurring pattern: `watchtower-engine` README over-claimed "not yet run" (35 jobs done); appyradar-sentinel README called working code a "walking skeleton". Verify against code. (S1/S2/S5/S8)

---

## 5. Architecture-doc update map (which doc/section each change touches)

| Change | Doc / section | Status |
|---|---|---|
| MES class label + stateless-floor moat front-loaded | `docs/architecture.md`, `docs/dark-factory-constellation.md` overview; `context/CONTEXT.md` purpose | partial — CONTEXT.md done but **uncommitted** |
| Fleet-orchestrator landscape (green-field finding) | `docs/upstream-repos/` shelf (✓ committed `6ee755b`); brains `source-repos.md` (✓ `392a222`) | done |
| DF-9 git-hygiene sentinel | `backlog/specs/untracked-rot-sweep-spec.md` + `tickets.json` (✓ `f50bab1`) — **home decision still open** (AppyRadar probe vs `tools/` script) | spec done, build TBD |
| AppyRadar/Sentinel rename | `docs/dark-factory-constellation.md`, `docs/appyradar.md` (✓ `6b91d46`); AngelEye SKILL.md (✓ `cca1fc6`) | done |
| Watchtower 3-way naming | `memory/watchtower-app-vs-engine.md` (✓); needs landing in `docs/architecture.md` + `CLAUDE.md` | memory only — **doc not yet updated** |
| Parallelism-via-identity sequence | `memory/parallelism-via-identity.md` (✓); needs an ADR/section in `docs/architecture.md` | memory only — **doc gap** |
| Loop-closure sequence (doing-loop return-leg first) | `docs/north-star.md` C1-C5 spine (C4 = return-leg) ✓ present; `AUDIT-2026-06-12.md` §1 | documented, build not started |
| Watchtower superseded docs | `docs/watchtower/{spec,context,chatgpt-brief,HANDOVER,REVIEW}.md` banners + `RE-BUCKETING.md` + INDEX (✓ `ef4d618`) | banner-stamped; **physical re-home deferred** |
| CONTEXT.md + context.globs.json constellation refresh | `context/CONTEXT.md`, `context/context.globs.json` | written **uncommitted** across S4/S5/S7 |
| AUDIT canonical state map | `AUDIT-2026-06-12.md` (✓ on disk) | **untracked/uncommitted** |

**Missing / surfaced doc gaps:**
- No committed `docs/architecture.md` section yet captures the **Watchtower naming resolution** or the **identity-first parallelism** decision — both live only in `~/.claude/.../memory/`. Promote to a tracked ADR.
- **Switchboard has no design doc backed by code** — it's referenced as a plane but exists only as backlog/specs. Any "Switchboard daemon" claim needs grounding or removal.
- `context/` files (`CONTEXT.md`, `context.globs.json`) are the single on-demand orientation doc yet have been uncommitted for 3+ sessions.

---

## 6. Open questions / handoffs

**Uncommitted working tree (highest-priority handoff — pin these into atomic commits):**
- `context/CONTEXT.md` + `context/context.globs.json` (S4 regen, untouched since)
- `AUDIT-2026-06-12.md`, `backlog/2026-06-12-cardputer-frontdesk.md`, `plans/`, experiment proof dirs (S7)

**Decided but not built:**
- Loop-closure: close doing-loop return-leg first (Switchboard queue→consumer→board) — **but Switchboard doesn't exist yet as code**, so this is a build-from-scratch, not a wiring job.
- Parallelism sequence ratified; step 0 (safety latch) not yet built.
- DF-9 spec written; home (AppyRadar probe vs `tools/` script) undecided.

**Still open (need David's go):**
- **Q4**: Build all 4 SRP apps now (greenfield-all) vs JIT (build when a closed loop demands it)?
- **Q5**: Authorise a docs-truth-only follow-up to reconcile remaining stale READMEs + duplicate Marshall skill (`experiments/.../skills/marshall/` and `.claude/skills/marshall/` — both confirmed on disk) into one living status surface?
- **Q6**: Spend Fable 5 credits on architectural reconciliation pass (on M4 Mini, credit-conservation)?
- Physical re-home of `docs/watchtower/` per `RE-BUCKETING.md` (touches CLAUDE.md paths — needs its own ratification thread).
- Fold appyradar naming + stripped visual layer (the old `appyradar` `hotel-live.html` dashboard was NOT carried forward to the sentinel substrate — a *planned gap*, not a loss) into the audit + a memory file (offered S8, not done).

**Verification debts to flag to David:**
- "appyradar-sentinel proven live / 214–215 tests" — **unverifiable from repo** (single scaffold commit, no run log, conflicting counts). Don't repeat as fact.
- "Switchboard 399-line SSE daemon" — **no such code on disk**; the audit's Drift #2 is overstated.
