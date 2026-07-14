# Tickets — Deduped, Routed, Build-Ready (v2 harvest)

**Purpose**: Actionable tickets extracted from 101 capture records (2026-06-29 → 2026-07-13), deduped across restatements and routed to target app/system.

**For Agents**: Each ticket cites its source dates. "Supersedes" notes where a later capture overrode an earlier one — always take the latest value. Priority: P0 = time-critical, P1 = gates other work, P2 = build queue, P3 = parked/verify-first.

---

## Captain's Log (app — `~/dev/ad/apps/captains-log` lineage)

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| CL-01 | P1 | **Durable ingestion**: launchd-managed cron, 30-min cadence 07:00–22:00, verify it survives restart; add in-app manual "Ingest now" button | 07-13 |
| CL-02 | P1 | **Plaud token resilience**: automated refresh-token re-acquisition (Playwright-style, replaces daily manual console paste); persist token against the Plaud provider record. Root cause: any other Plaud client (Android/web) invalidates the token | 07-12, 07-13 |
| CL-03 | P2 | **Show transcript inline**: "Show" button reveals full markdown/transcript (currently copy-only) | 07-13 |
| CL-04 | P2 | **Light mode + DESIGN.md**: analyze kybernesis.ai design system, write DESIGN.md under `brand-dave`, implement light theme (dark-only is unreadable) | 07-13 |
| CL-05 | P2 | **Vocabulary-correction layer**: normalization prompt fixing personal terms without altering meaning ("Happy Dave"→AppyDave, "cyber/chiber/Kubernetes agent"→KyberAgent, "DV") applied to transcripts + synopses at ingestion | 07-12, 07-13 |
| CL-06 | P2 | **Hide noise by default** behind a toggle (corpus shows ~32% noise rate — this is a third of the list) | 07-13 |
| CL-07 | P2 | **Filter toggles**: tags/summaries, timeframe recency, noise on/off, keyword/topic search | 07-13 |
| CL-08 | P2 | **Tag governance**: config-level (not per-item) tag rules + centralized tag store/manager; seed missing tags (captains-log, kybernesis, lars) | 07-13 |
| CL-09 | P3 | **Semantic source colors** (OMI green, Plaud blue) instead of text labels | 07-13 |
| CL-10 | P1 | **Timeline grouping / temporal linkage**: chain a capture to earlier same-topic captures; allow one capture to split into multiple ideas linking to other chains (quest/side-quest model). Design-first — see punchlist #1 | 07-13 (2 records) |
| CL-11 | P2 | **Output-destination config** per provider: where raw transcripts land (folder vs second brain), and whether Plaud gets a TIL-style process like OMI | 07-12 |
| CL-12 | P2 | **Intelligence-hub ingestion providers**: self-sent emails carrying article/YouTube links → transcript extraction or scrape → common transcript form → summarize + ontology-tag | 07-11 |
| CL-13 | P3 | **OMI vs Plaud transcription bake-off**: same micro-conversations on both devices, compare quality | 07-06 |
| CL-14 | P2 | **Unified controller consolidation**: fetch skills stay separate (omi-fetch, plaud-fetch) but ALL processing (Whisper-local/Groq transcription, tagging/ontology, source pinning) moves to the shared controller; salvage good ideas from the abandoned Kybernesis OMI extension; document OMI vs Plaud format quirks | 07-05 (decision), 06-05→07-13 (8 restatements) |
| CL-15 | P2 | **Action tracking on transcripts**: notes + mark-as-done; candidate mechanism = browsing audit-log of wants/ideas consolidated in one pass. Mechanism undecided — spike first | 07-13 |
| CL-16 | P3 | **Chat-with-document** via Extension SDK LLM integration — blocked on SDK-01 | 07-13 |
| CL-17 | P3 | **Extension SDK alignment**: check CL architecture fits KyberAgent Extension SDK; import SDK once publishable | 07-13 |

Shipped already (close as done): sequential IDs asked 07-04, live as A330–A339 by 07-13. The 07-04 OMI-list metadata/synopsis/card-panel spec is subsumed into CL-03/05/07.

## Extension SDK / Kybernesis platform (raise as Kybernesis tickets)

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| SDK-01 | P1 | **Host-mediated chat/LLM access** for extensions (extensions must never reinvent their own LLM calls — root cause of the failed OMI extension) | 07-05, 07-13 |
| SDK-02 | P1 | **Daemon-owned scheduling**: host daemon runs cron/pulse and invokes extension hooks; extension owns config only | 07-05, 07-09, 07-12 |
| SDK-03 | P2 | **Feature roadmap** for Extension SDK / host / harness / daemon (prerequisite for the two-agent feedback loop) | 07-13 |
| SDK-04 | P2 | **Document canonical extension architecture**: extension = daemon/web server (fs access, sockets) + iframe client in host; iframe never routes through host to reach its backend (AngelEye is the reference). Twice corrected — write it down | 07-03 (packaging decision), 07-07 (2 corrections) |
| SDK-05 | P2 | **Panel vs mount terminology** decision + docs (product exists in-product AND as iframe extension) | 07-07 |
| SDK-06 | P2 | **Enrich the five thin extensions**: search guidance, inferred metadata, summaries, usages, docs — evaluated from real-user (human AND agent) perspective | 07-04 |
| SDK-07 | P3 | **Frame extension verification** (verify-first, may be stale): merge to David's branch, run option-2 fully-closed E2E, clarify whether the ~10 failing tests were integration or unit | 07-07 |
| SDK-08 | P3 | **GitHub org naming** for extensions (appydave-kyber / kybernesis / kyber-extensions) — open decision | 07-03 |

## Dark Factory

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| DF-01 | P1 | **Roadmap reset**: guided one-question-at-a-time Q&A walkthrough; restructure around constellation applications built one at a time. GATES everything below | 07-13 |
| DF-02 | P1 | **Governance rule**: tickets that change factory-running code must NOT run through the factory (self-approval observed 07-09) | 07-09 |
| DF-03 | P2 | **Namespace repair**: review/rename unapproved "war room" back toward lanes/stations | 07-09 |
| DF-04 | P2 | **Chaperone/observer** for the factory's main conversation (note: `appydave:chaperone` skill already exists — evaluate before building) | 07-09 |
| DF-05 | P2 | **Consolidate task launch** onto one path; restore Switchboard/WatchTower as the web harness (currently 3 inconsistent paths) | 07-09 |
| DF-06 | P2 | **Cross-repo execution decision** (ultra-think): run in target repo w/ reference folder vs MCP server exposing DF knowledge vs centralize coding in DF | 07-10 |
| DF-07 | P2 | **Control-surface doc over KyberAgent**: ever-expanding doc — MCP/API control, deploy-into-local-harness, integration-test channels, permission escalation | 07-09 |
| DF-08 | P2 | **Architecture docs**: events, hooks, pipelines, communication channels; + doc the WatchTower/Switchboard ack flow | 07-02, 07-03 |
| DF-09 | P3 | **Mochaccino visualization system** for apps/tickets/side-quests (schema+data → image models) | 07-02 |
| DF-10 | P3 | **Folder separation**: main DF folder vs proof-of-concept vs third-party reference library | 07-02 |
| DF-11 | P3 | **Smart-contract-style rubrics/evals**: verifiable contract + rubric (security/stability/simplicity/speed) at end of each unit of work; post-hoc verification plans over pre-set plans | 07-07 (2), 07-09 |
| DF-12 | P3 | **Exercise the DF harness itself**: at least one real server-backed Claude Agent SDK extension, agents spinning up/communicating — not static HTML on the Claude Code harness | 07-03 |

## KDD / Lisa

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| KDD-01 | P2 | **Lisa guardrails**: deterministic menuing/routing or ask-human step; one-off vs pattern counting on every learning; learnings = single doc on the working ticket, never a KDD branch | 07-04 |
| KDD-02 | P2 | **Lisa scope**: KDD folder only — never customized per-repo, never the docs folder or application | 07-07 |
| KDD-03 | P1 | **Close the read loop**: wire KDD document READS into structural workflow points (PR validation, knowledge-update moments). "The factory writes knowledge but nothing reads it" | 07-04 |
| KDD-04 | P2 | **KDD bridge MCP**: register in app registry, document what/why/config (it appeared unannounced) | 07-04 |
| KDD-05 | P3 | Verify-first (likely stale): validate/close ticket 176; open 192 in fresh session with handover; defer 191 until loose ends cleared | 07-04 |
| KDD-06 | P2 | **Deprecate broken Gemini integration** out of the system | 07-04 |
| KDD-07 | P3 | KDD shareable synopsis in-repo; `.kdd` folder convention until dedicated KDD home lands | 07-03 |

## KyberAgent pilot (Roamy)

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| KA-01 | P0 | **Learning agent on Roamy** ($100 credits): brain scoped purely to understanding Kybernesis (SDK, daemon, harness); reads KDD docs + commits; regular reports on what Ian/Martin add (incl. website, Arcana). OVERDUE — "this weekend" (07-06) lapsed; prerequisite for Lars + Challenge DV demos and the two-agent loop | 07-06 (2), 07-13 |
| KA-02 | P1 | **Claude Code ↔ KyberAgent comms**: work out + document how to talk to / control a KyberAgent (and search its brain) from Claude Code; note injected conversations don't reliably land on the same machine | 07-06 |
| KA-03 | P2 | **Two-agent feedback loop**: extension-builder agent (fed by the Kybernesis-brain agent) writes prioritized platform tickets for a platform-extender agent. Depends on SDK-03 + KA-01 | 07-13 |

## Clients

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| CDV-01 | P0 | **Reply to Linda's email** (Canva workflow question) — unanswered | 07-13 |
| CDV-02 | P0 | **Send revised Challenge DV FDE retainer proposal**: **$2,750/mo incl GST ($2,500+GST)** — SUPERSEDES $3,300 from earlier same day — weekly 90-min Claude-centric training + 1–2 custom tools/mo, starting **15 July**, mid-month-to-mid-month. Start date is 2 days out | 07-07 (2), 07-13 (2) |
| CDV-03 | P1 | **Challenge DV demo prep**: KyberAgent multi-agent orchestration, second brain, extensions, Captain's Log | 07-13 |
| LARS-01 | P1 | **Lars call demo**: 2–3 min Captain's Log demo showing on-demand micro-apps plugging into KyberAgent + where Extension SDK/brain/agents fit | 07-13 |
| ACH-01 | P1 | **Achieve MVP setup**: Angela write access to achieve-mvp repo (Supporting Potential org); load her mapping/workflow outputs, organized; context-load with Claude | 07-07 |
| ACH-02 | P2 | **Schema mining**: AI deep-analysis of legacy SupportSignal, app.supportsignal.com.au, V2, and DSP app (moments-that-matter docs) → JSON structures for workflows/data shapes | 07-09 |
| ACH-03 | P2 | **Read-only micro-apps** off those schemas, agent-generated synthetic data (durable JSON in repo), Mochaccino visuals → participant/staff/site dashboards | 07-09 |
| ACH-04 | P2 | **30,000-ft process view**: red-circle major problem areas, order by dependency chain into a project list | 07-09 |
| ACH-05 | P2 | **100 one-minute NDIS scripts** (Angela executes via shared scripting skill; David enables) | 07-07 |
| ACH-06 | P3 | **SupportSignal revival** on fresh Vercel + Supabase as demo/screenshot source | 07-07 |
| ACH-07 | P3 | Angela + Stravan onboarding coordination; confirm Angela's project docs were emailed (07-04 action, likely done via 07-07 session) | 07-04 |

## Gling

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| GL-01 | P2 | **Electron injection spike**: inject startup code layer into Gling's unobfuscated Electron app exposing MCP/API (load videos, keywords, editing) so Claude Code/FliHub can drive it. SUPERSEDES the 07-04 open-source-replacement research (subscription renewed 07-11; direction is now enhance-not-replace). Read `brains/gling` first | 07-04, 07-11 (2) |

## Skills / tooling / misc

| ID | P | Ticket | Sources |
|----|---|--------|---------|
| SK-01 | P2 | **Skill registry**: investigating (~1,100) vs in-use (~100), last-accessed/staleness, per-skill learnings+metadata alongside the skill, taxonomy search/filter, detail viewer, quality UX | 07-04 |
| SK-02 | P3 | Clarify review vs delivery-review skill distinction; can a background agent evaluate skill-creator output? Plugins discussion → Thursday catch-up | 07-11 |
| MISC-01 | P2 | **Affiliate inbox triage** (ideasmen, mostly AITLDR): classify scam/real/follow-up/forgotten-outreach, pre-draft replies — do WITH Jan and Mary (07-13 deferral) | 07-12, 07-13 |
| MISC-02 | P3 | Install/run latest AionUI + T3 locally as third-party extension-host tests (decoupling insurance) | 06-29 |

## Parked — recipe/thumbnail arc (paused 2026-07-10 per memory, resume ~late July)

| ID | Ticket | Sources |
|----|--------|---------|
| RT-01 | Generalized self-improving recipe skill (create/read/structure/modify recipes, multi-stack, guided Q&A) | 06-30 |
| RT-02 | Thumbnail-generator micro-app as KyberAgent extension (AppyDave brand config first; per-brand rules; regenerable via extension recipe) | 06-30 (2) |
| RT-03 | Locate old prompt-batch TUI (appydave-tools / Ruby gems) as thumbnail batch runner; design 100→10-20 shortlisting | 06-30 |
| RT-04 | Session→marketing asset router (coding sessions → tweets/YouTube/lead magnets → staged human refinement → channel delivery) | 07-09 |
