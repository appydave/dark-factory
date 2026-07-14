# Thread Atlas — Streams of Consciousness (2026-06-29 → 2026-07-13)

**Purpose**: Cluster 102 voice-capture records (66 OMI + 36 Plaud) into narrative threads — how each stream of thinking evolved, split, merged, went dormant, or shipped over the calibration fortnight.

**For Agents**:
- This is the headline artifact of the calibration slice — read this before the recurrence/drift/open-loop files.
- Thread names are normalized from raw `thread` tags (near-duplicates merged, e.g. `dark-factory-kdd` + `kdd-lisa` + `kdd-librarians`).
- 30 of 102 records (29%) were pure noise/ambient and are excluded from thread narratives.

---

## Signal Overview

| # | Thread | Records | Span | Status |
|---|--------|---------|------|--------|
| 1 | Captain's Log (unified capture pipeline) | 15 | 07-05 → 07-13 | **OPEN — dominant thread, in active build** |
| 2 | Dark Factory engine + KDD/Lisa | 12 | 07-02 → 07-13 | **OPEN — governance reset in progress** |
| 3 | Kyber extension architecture & SDK | 8 | 06-29 → 07-13 | **DECIDED (iframe/repo-per-ext) with open SDK gaps** |
| 4 | Client FDE arc (Linda/Challenge DV, Angela/Achieve, Lars) | 7 | 07-07 → 07-13 | **OPEN — proposals pending** |
| 5 | AI meetups & peer research | 6 | 07-03 → 07-11 | Ongoing intake, no loop |
| 6 | KyberAgent learning / doc-watcher agent | 3 | 07-06 → 07-13 | **OPEN — twice planned, never started** |
| 7 | Gling automation | 3 | 07-04 → 07-11 | OPEN — plan pivoted (see drift) |
| 8 | Recipe skill + thumbnail arc | 3 | 06-30 only | **DORMANT since 06-30** |
| 9 | Agent verification / smart contracts | 3 | 07-07 → 07-09 | Exploratory, open |
| 10 | Skill registry + thin extensions | 2 | 07-04 only | Dormant since 07-04 |
| 11 | Minor singletons | ~8 | scattered | see below |

---

## 1. Captain's Log — the unified capture pipeline (15 records, 9 days)

The fortnight's centre of gravity. Born from frustration, converged fast, now the most actively specified product in the corpus.

**Timeline**

- **07-04 0810** *(pre-history, tagged `omi-ingestion`)* — feature gripes at the old OMI list app: titles aren't enough, wants tags + synopsis + sequential IDs (A00-style).
- **07-05 0954** — the founding insight: OMI and Plaud are just two providers of one "talking input device" concept; `omi-fetch` as a name makes no long-term sense. Unify ingestion, self-host Whisper/Groq transcription, kill the 2× $20/mo subscriptions.
- **07-05 1831 (Plaud)** — **DECISION**: providers stay separate fetch skills, but a single shared controller owns transcription/tagging/ontology/routing. Old OMI extension condemned as a "half-assed fork".
- **07-06 0903–0908** — three rapid captures: (a) embryo of the capture-weaving idea (compare micro-conversations against each other — literally this document's job); (b) transcription bake-off — David deliberately dual-records the same monologues on both devices; (c) the extension must replace the OMI extension, with conversation→project→machine routing telemetry; Dart Factory ticket requested.
- **07-09 0722** — **NAMED**: "Captain's Log". **DECISION**: host it as a KyberAgent extension (gets LLM access via the agent daemon, no bespoke API layer), configurable ~10-min ingestion pulse.
- **07-11 0733** — **SCOPE EXPANSION**: from OMI+Plaud viewer to unified intelligence hub — add email-to-self ingestion (YouTube transcript extraction, article scraping), everything normalized to "transcripts".
- **07-12 0642 / 0702 / 0714** — build-day directives: mine prior conversations into a spec, vernacular normalization ("Happy Dave" → "AppyDave"), cron configured in extension but executed by host daemon; open questions on data destinations (raw vs brain vs TIL) and Plaud's brittle refresh-token auth.
- **07-13 0625 / 0714 / 0725 / 0851** — hardening day: launchd durable ingestion (30-min, 7am–10pm) + manual trigger, slice-and-dice filtering; two structural questions (no temporal/thematic linkage between captures; no way to attach actions/notes to transcripts); then a 13-minute live UX walkthrough (items A330–A339) producing a full punch-list — show-markdown, light mode, DESIGN.md from kybernesis.ai, tag governance/central tag store, semantic source colors, chat-with-document, and Plaud token automation flagged **highest priority**.

**Evolution shape**: gripe → unification insight → naming + hosting decision → scope expansion → spec/build → live UX feedback. A textbook idea-to-product arc in 9 days.

**Splits/merges**: absorbed `omi-ingestion` (07-04) and the condemned OMI-extension work; feeds requirements into thread #3 (Extension SDK gaps become Kybernesis tickets). The temporal-linkage question (07-13 0714) spawns the **capture-archaeology** need this very calibration exercise answers.

**Status**: OPEN, in active build. Loudest single item: automate the daily manual Plaud token refresh.

---

## 2. Dark Factory engine + KDD/Lisa (12 records, 12 days)

**Timeline**

- **07-02 0633** — 7-day Fable-powered sprint plan: architecture docs/visuals (Mochaccino), morning briefing, tickets/alerts, tmux discipline, Lisa/KDD upgrade to extract *ideas* (not just lessons) with provenance-chained speculative PRs.
- **07-03 0909** — sprint directive: race the ~6 remaining Fable days building connected micro-apps (WatchTower + Switchboard as the David↔agent comms layer); mistakes fine if learnings become docs.
- **07-03 0921** — KDD sub-thread opens: OMI-fetch extension, KDD-inspector extension, `.kdd` dotfolder convention; **thumbnail generation explicitly reserved for David personally**.
- **07-03 1137 (×2 — duplicate clean/raw captures)** — blind review: sprint "apps" were static HTML opened from disk, not server-backed extensions; inline agents only proved the Claude Code harness, not the dark-factory harness (agents spinning up/down + communicating over its bus).
- **07-04 1257 / 1412** — the structural complaint of the fortnight: **"the factory writes knowledge but nothing reads it"**; mystery KDD-bridge appeared unannounced; broken Gemini integration to deprecate; Lisa turned one learning into a whole branch; wants menuing/deterministic guardrails.
- **07-07 1439** — Lisa scope correction: KDD-folder-only, generic, no per-repo customization ("what have we been doing wrong with our thinking?").
- **07-09 0642** — governance post-mortem: factory self-modified its own orchestrator via a ticket (gut: should be blocked); unapproved "war room" namespace displaced lanes/stations vocabulary; 3 inconsistent task-launch paths; no chaperone on the main conversation; no way to bootstrap a fresh context-rich main conversation.
- **07-09 0728** — mandate: factory must master the KyberAgent extension SDK + control surfaces (MCP/API) to deploy extensions straight into the local harness and run integration tests.
- **07-10 0721** — unresolved cross-repo question: where does coding run when SDLC intelligence lives in Dark Factory but KDD/code lives in KyberAgent? (reference folders vs MCP knowledge server vs centralize).
- **07-13 0639** — roadmap reset: current roadmap is an unusable wall of text; wants guided one-question-at-a-time Q&A and constellation apps as explicit sequenced builds.

**Evolution shape**: ambition sprint → disappointing blind review → structural critique (write-only knowledge) → governance breakdown → reset. The tone shifts from *build fast* (07-02) to *govern properly* (07-09) to *re-plan* (07-13).

**Splits/merges**: KDD/Lisa is a persistent sub-thread that never resolves; merges with thread #3 via the 07-09 mandate (factory ↔ KyberAgent control).

**Status**: OPEN — reset requested, governance policies undecided, cross-repo question unanswered.

---

## 3. Kyber extension architecture & SDK (8 records, 15 days)

**Timeline**

- **06-29 1137** — founding strategy monologue: ~100 micro-app ideas (AngelEye, AppyRadar, FliVideo, Storyline) become KyberAgent extensions; app/port registry; decouple enough to also target AionUI/T3 as alternate hosts; monetize via "recipes" (paywall/community).
- **07-03 1401** — **DECISION** (coffee-shop): iframe technique, one GitHub repo per extension, package.json → agent-extension SDK, GitHub org name TBD (appydave-kyber / kybernesis / kyber-extensions); noted gap: dynamic external-extension loading probably not in the host yet.
- **07-03 1408** — aside: add test coverage to extension builds.
- **07-05 2003 (Plaud)** — post-mortem of the OMI extension identifies **two SDK gaps**: host-provided chat-conversation access, and built-in scheduled-task/cron — both should become SDK requirements.
- **07-07 1953** — architecture pushback/clarification: an extension = standalone web server + daemon reading the filesystem, client rendered in an iframe; the iframe must NOT route through the host to a backend.
- **07-13 0712** — two-agent feedback loop design: extension-builder agent files roadmap tickets to a platform-extender agent when it hits SDK gaps; needs an Extension SDK roadmap to land tickets in.
- **07-13 0625** *(via Captain's Log)* — Captain's Log must be buildable on the soon-publishable Extension SDK.
- Related sub-thread `iframe-extension-dev`: **07-07 1500 / 1942** — hands-on frame-extension dev (option-2 end-to-end tests, ~10 failing tests unclear, panel-vs-mount terminology, refresh-context pruning gripe).

**Status**: architecture DECIDED (iframe, repo-per-extension, own web server); SDK capability gaps, org-name decision, and dynamic-loading gap still OPEN. Captain's Log is the forcing function.

---

## 4. Client FDE arc — Linda/Challenge DV, Angela/Achieve, Lars (7 records, 7 days)

A business thread crystallizing around a repeatable **Forward Deployed Engineer retainer** offer.

- **07-07 0953 / 0959** — sales call with Linda (Challenge DV / Darkness to Daylight): AI video demos (HeyGen, Hyperframes, Joy's B-roll) vs a $25k outsourced quote; retainer floated at **~$5k/mo** (weekly 90-min coaching + bespoke micro-tools). Linda interested pending pricing.
- **07-07 1516** — parallel client: Angela Harvey (Supporting Potential) — achieve-mvp private repo, $1000 invoice, Claude Max, 3-week visual demo for Achieve (~$150M NDIS provider), 100 one-minute NDIS scripts, SupportSignal redeploy on Vercel+Supabase.
- **07-09 0942** — deep Achieve working session: $1.2–4M funding leakage, 1,100 weekly rejected invoices → North Star of FDE-style micro-apps from JSON schemas with agent-generated synthetic data (Mochaccino visuals).
- **07-13 0631** — Lars demo plan: 2–3 min tour of KyberAgent + brain + Extension SDK with Captain's Log as the example (Lars wants on-demand micro-apps).
- **07-13 0633 / 0851** — Challenge DV offer reshaped: **$3,300/mo inc GST** floated in the morning, revised to **$2,750 ($2,500 + GST)** by 08:51, running mid-month from July 15; contact-name uncertainty (Lisa/Lindy) unresolved; unread email + Canva question pending.

**Splits/merges**: all three clients converge on the same product story — KyberAgent + extensions + Captain's Log as the demo asset. The client thread is now downstream of threads #1 and #3.

**Status**: OPEN — Challenge DV proposal to send (July 15 start), Angela actions in flight, Lars demo to prepare.

---

## 5. AI meetups & peer research intake (6 records)

- **07-03 1503 / 1539** — coworking sessions: Claude agents chatting via a shared room; "Agent Burst" naming open; peer app/API-key debugging.
- **07-04 1000** — Saturday AI engineers meetup: model safety/privacy, GLM 5.2 economics, Fable limits, Spotify/Boris 30M-LOC talk; July event-calendar actions.
- **07-10 1805** — GTM lecture (Ishan): DeepLine replaces Clay, agent-run cold outreach, reply-rate metrics.
- **07-11 1323 / 1506** — Chiang Mai meetup: Ian Borders' Claude Tag talk; multi-agent marketing orchestration + ARP permissions; one concrete takeaway — **investigate plugin-on-plugin dependencies** for modularising the AppyDave plugin suite.

**Status**: intake stream, no loop; small actions (WhatsApp dates, Angela docs/onboarding) time-sensitive and possibly stale.

## 6. KyberAgent learning / doc-watcher agent (3 records — DORMANT→RE-EMERGED)

- **07-06 0904** (captured on BOTH devices — the bake-off in action): weekend plan to stand up a KyberBot agent on Roamy whose sole job is watching Kybernesis/Cortex/Arcana docs, brain as searchable memory; wants to talk to it FROM Claude Code (capability unknown); flags cross-machine capture-availability problem.
- *Gap: 7 days of silence — the weekend plan didn't happen.*
- **07-13 0657** — re-emerges reframed as "the pilot": David admits he doesn't know how to actually use KyberAgent; first agent on Roamy ($100 credits) with a Kybernesis-comprehension brain, reading KDDs/commits, reporting on Ian & Martin's additions.

**Status**: OPEN — twice planned, not yet started.

## 7. Gling automation (3 records — DORMANT→RE-EMERGED with pivot)

- **07-04 1240** — replace Gling with an open-source agentic video-cutter before the subscription renews "in days"; recalls a prior conversation possibly in the video-as-code brain.
- *Gap: 7 days. Renewal happened.*
- **07-11 1603 / 1627** — plan pivots: don't replace, **inject an MCP server/API into Gling's unobfuscated Electron codebase** and drive it from FliHub/Claude Code — enhance the real app instead of rebuilding. (See decision-drift file.)

**Status**: OPEN — injection investigation queued; gling brain review pending; subscription decision defaulted to "renewed" by inaction.

## 8. Recipe skill + thumbnail arc (3 records — DORMANT since 06-30)

- **06-30 0733** — generalized self-improving recipe skill (IKEA flat-pack analogy: instructions ± parts + a "recipe robot"), composing with harness skills (AppyStack, KyberAgent).
- **06-30 0801 / 0814** — thumbnail-generator micro-app per brand (AppyDave → AITLDR/vOz/Kybernesis); resurrect the old prompt-pacing TUI; shortlist the 100+ variant matrix to 10–20.
- Partial contradiction **07-03 0921**: thumbnail generation for David is explicitly NOT to be automated (he keeps personal control).

**Status**: DORMANT — no capture after 06-30 (consistent with the externally-known "recipe→thumbnail arc PAUSED 2026-07-10, resume ~late July"). The recipe *concept* survives as vocabulary in the 06-29 monetization strategy and 07-09 session-mining idea.

## 9. Agent verification / smart contracts (3 records)

- **07-07 1626 / 1641** — smart contracts + dual-loop planning question; KDD (Lisa/Lexi, 3-recurrence pattern promotion) vs peer's rubric substrate (security/stability/simplicity/speed, staking, happiness-score A/B); mutual interest in contract/rubric verification per unit of work.
- **07-09 1533** — Tony (one.ie) peer session: smart contracts as agent work contracts → candidate for Dark Factory rubrics/evals; Taylor/Playwright and Loom+ffmpeg UAT automation recipes; Joy Juice & Beauty & Joy provisioning on Tony's platform.
- Precursor: **07-03 1531** crypto-wallet workshop (test wallets/tokens) — exploratory context only.

**Status**: exploratory OPEN — a candidate strengthening mechanism for Dark Factory's end-of-SDLC gate.

## 10. Skill registry + thin extensions (2 records, 07-04 only)

Skill-registry design (~1100 skills investigated vs ~100 used; staleness tracking, learnings, taxonomy search, viewer UX) plus the "five extensions are too thin" critique — minimum-viable data with no discovery metadata; extensions must serve humans AND agents. **Dormant since 07-04**, but its discovery-metadata principle echoes in Captain's Log's tag-governance work.

## 11. Minor singletons

- **session-content-mining (07-09)** — router skill mining Claude Code sessions into marketing assets (tweets/YouTube/lead magnets/Skool). Open idea, unactioned.
- **skill-lab (07-10)** — context-aware self-learning utility skills (CEO-brief reporting style); coffee booked Thursday 11am.
- **agent-memory-architecture (07-10)** — connector-first beats vendor hidden memory; data sovereignty, no lock-in.
- **model-landscape (07-10)** — overheard "version 5.6" degradation complaints (queues, cost, fights user skills); watch 1–4 weeks.
- **joy-video-automation (07-11)** — B-roll auto-tagging (Qwen+Whisper) for the ~1000-video back catalog; Joy's bespoke micro-apps (till/POS) as Kybernesis extensions.
- **aitldr-affiliates (07-12 → 07-13)** — affiliate email triage directive; deferred on 07-13 to do together with Jan and Mary.
- **skills-review-tooling (07-11)** — confusion between review-skill variants (delivery vs dimensional); plugins on Thursday's agenda.
- **video-as-code (07-04)** — folded into the Gling arc.
- **personal/** — health (skipping HIIT 6×1-min; 60/90-day no-sugar window, no cheat days), NordPass master-password verification, shopping errands, OMI wind-noise reliability doubt (07-04 motorbike test).

---

## Cross-thread observations

1. **Everything funnels into two artifacts**: Captain's Log (the intake organ) and the Extension SDK (the delivery organ). Dark Factory is the machine meant to build both; the client FDE arc is the monetization of both.
2. **The bake-off produced real duplicates**: 07-06 0904 exists on OMI *and* Plaud — the corpus contains David's own deliberate A/B test, and any dedup/threading system must handle it.
3. **The meta-loop**: 07-06 0903 ("compare micro conversations against each other") and 07-13 0714 ("no temporal/thematic linkage between captures") describe exactly this atlas. The system David asked for on 07-13 is the one generating this file.
