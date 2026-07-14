# Thread: client-supportsignal

**Records**: 121 captures, 2026-01-13 → 2026-06-22
**Arc**: Angela onboarding → test-migration marathon → the Convex abandonment pivot → Signal Studio MVP sprint → v2 BMAD/Supabase planning → 10-week dormancy → re-emergence as a business crisis and commercial reset.

---

## Phase 1 — How it started: Angela onboarding + doc-architecture cleanup (Jan 2026)

**2026-01-13.** The thread opens not with code but with a person: David onboards **Angela** onto Claude Code and the POEM system on her Windows/WSL machine — restructuring her dev folder into `supportsignal/angela_poc`, cloning the private `prompt.supportsignal.com.au` repo, explaining Penny/workflows/Handlebars. They agree on recurring daily 1-hour training sessions. This is the seed of everything that follows: Angela as a trainable domain expert is the thread's constant.

**2026-01-19** is a dense working day with two strands:

- **Incident-workflow quality.** Pairing with Angela, David hits the background-agents-can't-write-without-dangerous-permissions wall (declines to enable it), and — after seeing her weekend AMS incident dashboard — **reframes incident enhancement around atomic predicate/classification signals confirmed by a human before any enhanced narrative is written**. This "predicate prompts for Penny" idea becomes the product's conceptual spine. Same day: a regression bug (regenerate-questions kept stale answers) starts the "incident workflow regressions" loop, and David asks the archaeology question — *when did incident create/edit actually break?*
- **Doc architecture.** David declares the existing data grouping and naming "a complete mess" (data fine, structure not), refuses to route the restructure through the architect agent (it would go via ChatGPT), and orders a software-architect audit of all project documents — planning docs, KDD, PRDs, epics, stories. Decisions logged at 11% context: E4 KDD retrospective stays separate from Epic 4, E3 KDD folds into Epic 3, systematic fix over quick-fix, and the durable rule that **handovers are written inline with absolute paths, never as new files**. An Epic 4 retrospective slide deck (consolidated semantic JSON first, deck second) closes the day.

## Phase 2 — The Vitest migration marathon (2026-02-02)

A single brutal day of captures (10 records) around migrating the Convex system tests from Jest to Vitest — ~120-130 commits over 2-3 days, handover number 19, batches 20-24.

The recurring pain was **tracking integrity, not the tests themselves**: failing counts blew out from ~70 to 168/169 ("what's the point of migrating with failure?"), the migration queue's target kept growing (34 files → 50, percentages sliding), metrics shifted between answers (373 passes / 47 failures vs 31/50 vs 32 files done), and the agent referenced a "group five" David never defined. David set hard standards — failing tests unacceptable, never change production code to satisfy tests without discussion — and ordered audits, a librarian check that tests were genuinely migrated rather than invented, and Lisa health-check commands. He also asked the meta-question that echoes through the whole log: *where do recurring systemic problems get written down, and how do they re-enter the workflow?*

The migration eventually landed at **717 passing Convex tests** (noted 2026-02-10) and was held up as the disciplined template to repeat on the web app and Cloudflare Worker suites. **In hindsight this entire effort was superseded three weeks later when Convex itself was abandoned (2026-02-24)** — the learnings transferred; the migrated suite largely did not.

## Phase 3 — Predicates become the product (2026-02-10 → 2026-02-13)

- **2026-02-10.** David and Angela review her 21 new incident-analysis prompts (8 predicates + 8 observations), establish the **three-part predicate / observation / classification structure**, and rule that observations are signals, never questions. **Superseded decision: the old enhancement prompts are deprecated.** Human-in-the-loop confirmation is conceded as mandatory for market (incident reports are legal documents). Same day: **Epic 12 declared blocked** — story 12.5 production cutover moves to end of epic pending POEM prompt upload/validation testing; and the planned **shadow-mode prompt-comparison table is ruled overengineered**, replaced by an immediate JSON discrepancy report on upload.
- **2026-02-12.** Alignment meeting (David sick but present): shift from linear prompt flows to **signal-based predicates/classifications powering dashboards and BI**. David takes ~1 week to finish the predicate observation area; Angela to be trained via Looms then train Ronnie, and to pitch AMS on a trial site. Testing knowledge gets siloed from the main KDD until ratified.
- **2026-02-13.** Housekeeping: plan of action on 156 lint issues and TypeScript errors.

## Phase 4 — THE PIVOT: Convex abandoned, two-week rebuild (2026-02-21 → 2026-02-24)

- **2026-02-21.** David scopes the **AWB workflow POC (WUI)** — an isolated throwaway client-server app on the new engine, wizard-style flow execution, parallel agents, conditional steps. This SupportSignal-motivated POC is where the thread **splits**: AWB grows into its own product line while remaining SupportSignal's workflow engine.
- **2026-02-23.** Troubleshooting factsheet with absolute paths prepared as evidence of work done on David's side — a defensive artifact hinting at partnership friction to come.
- **2026-02-24 — the biggest single day of the thread.** The major PO handover: **SupportSignal can no longer use Convex after six months of building and must rebuild in two weeks.** Ordered planning: sign-in, basic roles, data management first, possibly syncing from Convex as a migration bridge; database export becomes business-critical (feeds POEM for Angela's workflows). Around this, a requirements-doc review locks a batch of decisions: auth/SSO/impersonation must use **off-the-shelf libraries for Postgres/Supabase/React** (never rolled-own again); authorization stays role-based with multi-role composition, tenant filters, **no role inheritance**; **API-first company onboarding** restricted to internal staff (Ronnie, David, Angela), view-only screens first, CRUD deferred; config model settled as **YAML workflow + Handlebars prompt + JSON schemas** merged into an n8n-like inferred DOM; severity stays prompt-engineered, and "notification of high severity" is reframed as in-system highlighting. Moments That Matter UI out of scope; incident runtime is a document object model, not POEM itself. Angela gets a simplified run experience, and an evening remote session gets her running the WUI with real Claude token auth.

**Superseded: the two-week rebuild framing itself.** What actually happened was not a two-week port but a two-track strategy — Signal Studio MVP now, BMAD v2 greenfield later.

## Phase 5 — Signal Studio sprint (2026-03-02 → 2026-03-05)

The rebuild materializes as **Signal Studio**, a local JSON-backed onboarding console generated with AppyStack.

- **2026-03-02.** David demos the console (companies/sites/users/participants/incidents/moments) to Angela, live-dictates fixes, designs admin-only publishing mode + git-dirty sync indicator, and sets the workflow: **Angela tests and writes Angela_feedback.md, never touches code**; Anawah is the first onboarding target. Micro-app polish: "configure" renamed "Project Info", dark-mode Playwright review, reset-database behind a confirm modal, validation framework.
- **2026-03-03.** Pairing with Angela (Supporting Potential): ports 6040/6041, git identity, studio helper commands for WSL; Sync-to-Git button bug logged.
- **2026-03-04.** **Directors meeting (David, Angela, Ronnie)**: demo of the prototype with git sync + publish; Angela drives a 40-field hierarchical participant model; Ronnie pushes signal-vs-noise on cloud-migration risk. Agreed: finish MVP this week, start automated cloud build (schema + REST API via BMAD) the following Monday.
- **2026-03-05.** Autonomy demos: the Ralph Wiggum loop turns Angela's plain-language requirements into a self-tested build (ABN validation, tiers, CSV import); David's Raffy RAFT-loop plugin executes ~11 work units in parallel waves for the participant-system overhaul. The **Mochaccino mockup skill** is specced so Angela can iterate HTML UX mockups herself. SupportSignal v2 planning gap analysis commissioned — Signal Studio named the agile JSON/Git MVP source of truth.

## Phase 6 — Architecture hardening + integration (2026-03-09 → 2026-03-13)

- **2026-03-09.** David reframes Signal Studio as a **data reflection engine** — JSON entities pushed one-way into the main app via the publish bar; DB schema must be schema-compatible but not a mirror; epics reordered so foundation/security/API land before incidents/moments. Studio is explicitly **transitional** — permanent only if made bidirectional. Wave 12 (incident data model) stood up in parallel with UAT/Playwright acceptance work.
- **2026-03-10.** Scoping bugs: company admins can see other companies' data — must tighten to own-company only. Data-seeding decisions: no system admin without a company ID, copy Angela's current data, three-tier data setup.
- **2026-03-11.** **Crisis day**: Playwright MCP e2e tests broken and flooding prod/staging/dev data directories with hundreds (~10k at peak) of junk JSON files; a "UAT run" ground for 2+ hours showing no screens. David orders nuke-and-reseed, flood.md documentation, git-history recovery, and a genuine human-walkthrough UAT plan. Same day, constructive threads: Mochaccino must be **schema-constrained** (emit gap analyses, not invent structures) — the crux of the Angela (UX-first) vs David/Ronnie (data-first) tension; Angela shifts from participants (~80% done) to moments/incidents; domain settled as **app.supportsignal.com.au**; BMAD learnings get a public-ish repo; strategy call with Rodi sets build order (schema+auth → incidents/moments for field use) and frames the MVP as a **reference implementation AI rebuilds the real app from**.
- **2026-03-12.** Three-tier environments locked with **"staging" deliberately chosen over "UAT"** so AI agents parse it (superseding earlier UAT naming); the CLI reaffirmed as core MVP capability; early client feedback on participant onboarding chosen over polish. Retrospective note: the handover-document pattern turned Angela into an effective domain-expert prompt engineer in two weeks.
- **2026-03-13.** AWB–Signal Studio integration slog: lost registry JSON re-implemented per-user (git-ignored per-machine registry.json), hard-coded Moments That Matter exposed, API examples corrected to infer from YAML source of truth. Port cleanup: SupportSignal 6000/6001, Signal Studio 6040/6041, new AWB gets its own registered ports. **Superseded/rejected: field-to-field mapping between systems** — replaced by domain-specific translation at the call boundary. **De-scoped: Angela's eight-step shift-management design** (future one-month sellable feature); Moments That Matter locked to a simple signal-only model.

## Phase 7 — v2 BMAD planning, then handbrake (2026-03-16 → 2026-04-02)

- **2026-03-16.** **SupportSignal v2 framed as a greenfield Supabase relational build driven by BMAD**: Signal Studio is the UX/feature reference but its JSON-database, Git-sync and weak-validation foundations **must never carry over** (transform types, don't copy); epics 1–4 strictly sequential, epic 5 CRUD in parallel after epic 1; Mary/John/Winston as setup agents. FR review (~40 items), FR14 rewrite, SaaS B2B tier pricing marked TBA. David flags a **visa border run pauses him 1-2 weeks** — the first deceleration.
- **2026-03-30 → 03-31.** Epic 5 execution: schemas must align with Signal Studio before all future stories (~60% done, runner/wiring/enrichment missing). **Signal Studio confirmed as source of truth until SupportSignal is actually deployed.** Sync-verification doubts dominate: participant data marked "synced" doesn't match production; an Epic 0 deep entity-retrieval API is framed for send-vs-received debugging. Story 5.3 reframed as an upgrade informed by the 0.7 "cluster fuck"; a token/permission exposure risk is documented with revocation deferred.
- **2026-04-01 → 04-02.** Tapering: verification-flow bugs (incidents invisible to David's account), the incident-data ingestion point not yet implemented, a stopgap CRUD incident endpoint proposed, epic triage parking remaining AWB work. Then the captures stop.

## DORMANT: 2026-04-02 → 2026-06-12 (~10 weeks)

No captures. Context from the wider log: David's visa border run, then attention on Kybernesis, Media Studio, AWB Gen 3, and other product work. When the thread returns, it is not about code at all.

## Phase 8 — Re-emergence: business crisis and commercial reset (2026-06-12 → 2026-06-22)

- **2026-06-12.** The thread re-enters as a **partnership crisis**: Ronnie has run out of money and become hard to work with. David explains to Joy that he and Angela will push the near-ready product to market themselves — one client install next week, two more in ~6 weeks, scale late year. Same day, David and Angela debrief a hostile Ronnie meeting, reconcile true burn (~AUD 4k/month, Ronnie keeps paying core tooling for now), and agree the **FDE (forward-deployed expert) play**: Angela consults into large NDIS-adjacent orgs with David's tooling, new capabilities feature-flagged inside SupportSignal as the exit hedge, **targeting a sale exit — superseding Ronnie's 7-year vision**. Kybernesis per-client brains are Angela's first FDE step; standing Monday 1pm meetings; David possibly paying Angela's org ~$1k US/month.
- **2026-06-13.** The **Daily Support Plan (DSP) app** is greenlit — behaviour-support-plan ingestion → sharded extraction with provenance → human review → one-page PDF guide — built one-shot on AppyStack **under Supporting Potential** (Angela's org, not SupportSignal) as a $400-1000-per-plan cashflow tool and bridge into SupportSignal subscriptions. A sibling thread is born.
- **2026-06-22.** The last capture: David drafts an email to Rony and Angela **resetting his SupportSignal commitment to ~5 direct hours/week** (daily 40-min Angela sessions + weekly directors' session, generating 10-15 build hours), naming wall-of-text fatigue, and framing KyberAgent/Arcana, the extension SDK, FDE focus, and Media Studio as aligned outside work.

---

## Superseded decisions (roll-up)

| Decision | Made | Superseded by |
|---|---|---|
| Convex as the app platform (6 months of build) | pre-thread | 2026-02-24 — Convex abandoned, rebuild ordered |
| Jest→Vitest Convex migration as template for web app | 2026-02-02/10 | Convex abandonment made the migrated suite moot; learnings carried |
| Enhancement prompts for incident narratives | pre-2026-02-10 | Predicate/observation/classification structure (2026-02-10) |
| Shadow-mode prompt comparison table | early Feb | Overengineered — JSON discrepancy report on upload (2026-02-10) |
| Story 12.5 cutover mid-epic | Epic 12 plan | Blocked, moved to end of epic (2026-02-10) |
| "Two-week rebuild" framing | 2026-02-24 | Two-track: Signal Studio MVP + BMAD v2 greenfield (Mar) |
| "UAT" environment naming | early Mar | "staging" — AI agents parse it correctly (2026-03-12) |
| Field-to-field mapping between AWB and Studio | proposed | Rejected — domain translation at call boundary (2026-03-13) |
| Angela's eight-step shift management | 2026-03 design | De-scoped to future one-month sellable feature (2026-03-13) |
| Signal Studio JSON/Git/weak-validation foundations | Mar MVP | Must never carry into v2 — transform, don't copy (2026-03-16) |
| Ronnie's 7-year hold vision | founding assumption | Sale-exit target + FDE hedge (2026-06-12) |
| David full-bore on SupportSignal | Jan–Apr | ~5 direct hours/week reset (2026-06-22) |

## CURRENT status (as of 2026-07-13)

Quiet since the 2026-06-22 commitment-reset email — three weeks, consistent with the new deliberately-reduced cadence rather than abandonment. The thread has transformed from an engineering log into a commercial one: product near-ready, go-to-market driven by David + Angela (first client install was slated for ~mid-June, follow-ups at ~6 weeks), Ronnie relationship strained and formally de-risked via the FDE/feature-flag/sale-exit structure, and the DSP app running as the Supporting Potential cashflow bridge. Open engineering threads left dangling at dormancy: Signal Studio↔SupportSignal sync verification, the incident-data ingestion point, epic 5 completion (~60%), and the deferred token revocation.
