# 10 — Ticket Drafts (Routed by Target)

**Purpose**: Deduped, build-ready ticket drafts extracted from capture `actions` (102 records, 2026-06-29 → 07-13), routed to their target app/system.

**For Agents**:
- This is the deduped intake surface for this fortnight's slice — read before opening tickets anywhere.
- Every ticket cites its source capture(s). No citation, no ticket.
- Cross-device duplicates (OMI+Plaud bake-off pairs, .clean/raw pairs) have been merged into single tickets.
- Priority markers: 🔴 urgent/date-bound, ⭐ David-flagged highest priority.

**Totals**: 66 tickets — Captain's Log 18, Dark Factory 16, KDD/Lisa 6, Kybernesis/KyberAgent 8, Clients/Business 8, Brains/Tools 10.

---

## Captain's Log (18)

| # | Title | Intent | Source(s) |
|---|-------|--------|-----------|
| CL-01 ⭐ | Automate daily Plaud token refresh | Replace the manual paste-console-script flow with Playwright automation + token storage against the ingestion-provider record; blocks unattended operation | plaud 07-12-0714, plaud 07-13-0851 |
| CL-02 | Durable launchd ingestion job | Move OMI+Plaud polling off the web server onto launchd; ~30-min cadence 7am–10pm; verify restart survival; add manual trigger button | plaud 07-13-0625 |
| CL-03 | Slice-and-dice filtering + search | Filter by tag, timeframe (recent-first), noise on/off; keyword search over summaries/descriptions | plaud 07-13-0625, 07-13-0851 |
| CL-04 | Hide noise/empty captures by default | 29% of corpus is noise; default-hide with reveal toggle; never render single-period Plaud bodies | plaud 07-13-0851 |
| CL-05 | Inline "show markdown" button | Render full transcript/markdown inline, not just copy-to-clipboard | plaud 07-13-0851 |
| CL-06 | Light-mode theme | David can't read current dark mode; derive from the Kybernesis DESIGN.md (see TOOL-01) | plaud 07-13-0851 |
| CL-07 | Semantic source colors + ID recode | OMI green, Plaud blue (later email/YouTube) instead of text labels; recode item IDs (A330-style) to match | plaud 07-13-0851 |
| CL-08 | Vocabulary/vernacular normalization | Route transcripts/synopses through a vocabulary system so product names transcribe correctly ("Happy Dave"→AppyDave, "Dart Factory"→Dark Factory, "Kubernetes"→Kybernesis) without altering context | plaud 07-12-0642, 07-13-0851 |
| CL-09 | Tag governance + centralized tag store | Missing captains-log/kybernesis/lars tags are a config gap, not per-item fixes; consider a dedicated tag-management surface | plaud 07-13-0851 |
| CL-10 | Notes/decisions/done-marking on documents | Attach actions, notes, done-state, or a multi-conversation audit log to transcripts; later chat-with-document via Extension SDK | plaud 07-13-0725, 07-13-0851 |
| CL-11 | Temporal + thematic threading | Link the 2nd/3rd capture on a topic in a day; split one conversation into multiple ideas that link to other chains (quest/side-quest framing) — the corpus's loudest structural gap | plaud 07-13-0714, omi 07-06-0903 |
| CL-12 | Data-destination configuration | Map where ingested Plaud/OMI data lands (raw-intake vs brain vs TIL) and expose as a per-provider config setting | plaud 07-12-0702 |
| CL-13 | Email-to-self ingestion provider | Extract YouTube transcripts + scrape linked articles into the same transcript pipeline; analyze/summarize/ontology-tag | plaud 07-11-0733 |
| CL-14 | OMI vs Plaud structure comparison + quality bake-off | Diff transcript data structures for Plaud-specific handling; score the deliberate dual-recorded 07-06/07-07 pairs for transcription quality | plaud 07-05-1831, plaud 07-06-0904 |
| CL-15 | Extension SDK compatibility check | Confirm the build can import/run on the KyberAgent Extension SDK once publishable | plaud 07-13-0625 |
| CL-16 | Spec + build the Kybernesis extension | Mine prior CL/OMI/Plaud conversations into requirements + spec; decide AppyStack vs native Kybernesis foundation; per-provider cron configured in extension, executed by host daemon; mine old OMI extension for its good ideas; ticket missing SDK capabilities back to Kybernesis | plaud 07-12-0642, omi 07-06-0907 + plaud 07-06-0908 (dupe pair), plaud 07-09-0722, plaud 07-05-1831 |
| CL-17 | Cross-machine capture availability | Injected conversations land on one machine only; captures must be available fleet-wide (Roamy vs M4 Mini routing surfaced in UI) | omi 07-06-0904 + plaud 07-06-0904 (dupe pair), plaud 07-06-0908 |
| CL-18 | Self-hosted transcription (Whisper/Groq) | Pull raw audio locally and transcribe via local Whisper or Groq (Ian's tip: faster/free) to kill the 2× $20/mo provider subscriptions | omi 07-05-0954 |

## Dark Factory constellation (16)

| # | Title | Intent | Source(s) |
|---|-------|--------|-----------|
| DF-01 | Self-modification policy | Flag and block tickets that change the factory's own running code/systems from executing as normal tickets (policy open to debate, default = block) | plaud 07-09-0642 |
| DF-02 | Revert "war room" namespace | Unapproved namespace from a throwaway brainstorm displaced lanes/stations/workflow vocabulary; review and likely revert | plaud 07-09-0642 |
| DF-03 | Chaperone for the main factory conversation | Add an observer role (in-conversation vs external trade-off) with its own name/skill/agent — note `appydave:chaperone` skill already exists as a starting point | plaud 07-09-0642 |
| DF-04 | Consolidate task launching onto one path | 3 inconsistent launch methods (ad-hoc claude runs, orchestrator CLI, bypassed switchboard/watchtower); evaluate reviving switchboard + watchtower as the sanctioned web harness | plaud 07-09-0642 |
| DF-05 | Repeatable main-conversation bootstrap | Clean way to start a fresh context-rich main conversation stream (current one is unresettable context spaghetti) | plaud 07-09-0642 |
| DF-06 | Roadmap reset via guided Q&A | One-question-at-a-time walkthrough (plain conversation, not ask-tool); restructure roadmap so constellation apps are explicit sequenced builds, not piecemeal tasks | plaud 07-13-0639 |
| DF-07 | Cross-repo coding context decision | Ultra-think: reference-folder context vs MCP knowledge server vs centralizing coding in Dark Factory (SDLC intelligence and KDD/code live in different repos) | plaud 07-10-0721 |
| DF-08 | Master KyberAgent control surfaces | Deep-study Extension SDK + KyberAgent MCP/API so the factory can deploy extensions straight to the local harness and run integration tests; start the ever-expanding "what must be exposed" doc | plaud 07-09-0728 |
| DF-09 | Architecture docs + generated visuals | Events/hooks/pipelines/channels documented mermaid-first; Mochaccino schema→data→generated diagrams over time | omi 07-02-0633 |
| DF-10 | Morning briefing surface (WatchTower) | Which of ~10-15 projects ran overnight, status summaries, side quests per project | omi 07-02-0633 |
| DF-11 | Separate + label the three codebases | Canonical dark-factory vs PoC test code vs third-party reference in upstream | omi 07-02-0633 |
| DF-12 | Skill registry | ~1100 investigated vs ~100 used skills: last-accessed/staleness, per-skill learnings/metadata, taxonomy search, detail viewer | omi 07-04-0800 |
| DF-13 | Re-evaluate the five thin extensions | Each rebuilt from real-consumer perspective (human AND agent): inferred metadata, summaries, usages, docs, search support | omi 07-04-0806 |
| DF-14 | Document KDD bridge + deprecate Gemini | Explain what KDD bridge is (repo with MCP), why it exists, register it in the app registry; remove the broken Gemini integration | omi 07-04-1257 |
| DF-15 | Ticket triage 176/191/192 (+ model ops) | Validate 176's tests and close; hand 192 to a fresh session; 191 waits for a full-focus session; consider Haiku→Sonnet 4.5 workload move | omi 07-04-1257 |
| DF-16 | Harness-testing builds, not inline agents | Answer whether server-backed extensions are planned; next builds must exercise the dark-factory harness (agents spin up/down + bus comms), not the Claude Code harness | omi 07-03-1137 (.clean + raw dupe pair) |

## KDD / Lisa (6)

| # | Title | Intent | Source(s) |
|---|-------|--------|-----------|
| KDD-01 | Wire KDD reads into SDLC checkpoints | "The factory writes knowledge but nothing reads it" — KDD docs must be READ at PR validation and knowledge-update points, structurally, not just via an MCP. Root of every Lisa loop | omi 07-04-1257 |
| KDD-02 | Lisa guardrails + branch post-mortem | Add menuing/smart-determinism so Lisa routes correctly or asks the human; investigate why one learning became a whole branch instead of one KDD doc on the ticket | omi 07-04-1412 |
| KDD-03 | Lisa scope: KDD folder only | Strip per-repo customization; her job is the KDD folder, not general docs or the application | omi 07-07-1439 |
| KDD-04 | .kdd dotfolder convention + locate Lisa's JSON | KDD working files go in a `.kdd/` dotfolder per project until a dedicated home exists; find where Lisa's machine-readable JSON files are currently landing (unknown) | omi 07-03-0921 |
| KDD-05 | Contract + rubric verification per unit of work | Explore security/stability/simplicity/speed rubric verification at end of each unit of work; capture inter-agent comm problems in structured form inside tickets so librarians can promote them | omi 07-07-1641, plaud 07-09-1533 |
| KDD-06 | Lisa idea-extraction upgrade | Extract ideas (not just lessons/patterns/ADRs) with provenance-chained speculative PRs agents work while idle | omi 07-02-0633 |

## Kybernesis / KyberAgent / Extension SDK (8)

| # | Title | Intent | Source(s) |
|---|-------|--------|-----------|
| KYB-01 | File SDK gap requirements: host chat access + daemon cron | The two missing capabilities that forced the OMI extension to reinvent ingestion; write the ticket in KyberAgent docs or as a dark-factory plan and report back where it was filed | plaud 07-05-2003, plaud 07-12-0642 |
| KYB-02 | Dynamic external-extension loading gap | Host probably can't dynamically load external extensions yet; write up problem + proposed solution | omi 07-03-1401 |
| KYB-03 | Decide the extensions GitHub org name | appydave-kyber vs kybernesis vs kyber-extensions | omi 07-03-1401 |
| KYB-04 | Canonical extension architecture doc | Confirm: extension = standalone web server + daemon on own ports, client in iframe, repo-per-extension, package.json → agent-extension SDK contracts; iframe must NOT route through host to backend | omi 07-07-1953, omi 07-03-1401 |
| KYB-05 🔴 | Kybernesis-brain / doc-watcher agent on Roamy | Stand up the first KyberAgent ($100 credits) with a brain scoped to KyberAgent/Kybernesis/Cortex/Arcana docs; read KDDs + commits; regular reports on Ian/Martin additions. Planned 3× (07-06 ×2, 07-13), never started — oldest repeated-plan loop | omi 07-06-0904 + plaud 07-06-0904 (dupe pair), plaud 07-13-0657 |
| KYB-06 | Claude Code ↔ KyberAgent communication | Determine how (or whether) a running KyberAgent can be talked to/controlled from Claude Code | omi 07-06-0904, plaud 07-06-0904 |
| KYB-07 | Extension SDK roadmap + two-agent loop | Establish a roadmap for SDK/host/harness/daemon features so extension-blocking gaps have somewhere to land; extension-builder agent files tickets a platform agent consumes | plaud 07-13-0712 |
| KYB-08 | iframe-extension dev cleanup | Merge to David's branch + option-2 closed E2E tests; clarify the ~10 failing tests (integration vs unit); prune refresh-context output + stale screenshots; define panel vs mount terminology; tickets ~160/174 queued | omi 07-07-1500, omi 07-07-1942 |

## Clients / Business (8)

| # | Title | Intent | Source(s) |
|---|-------|--------|-----------|
| BIZ-01 🔴 | Challenge DV proposal — due before July 15 | Reply to her unread email, CONFIRM name (Lisa or Lindy), answer Canva question; send $2,750 inc GST ($2,500+GST) proposal: weekly 90-min training + 1-2 custom tools/mo, mid-month to mid-month from July 15 | plaud 07-13-0633, plaud 07-13-0851, plaud 07-07-0959 |
| BIZ-02 | Achieve MVP build plan | AI analysis over legacy SupportSignal + v2 planning + DSP app ("moments that matter"); JSON workflow schemas → read-only micro-apps; synthetic-data agents; 30,000-ft process view with gaps circled, dependency-ordered | plaud 07-09-0942, omi 07-07-1516 |
| BIZ-03 | Angela onboarding admin | achieve-mvp repo access instructions; invoice $1,000; Claude Max on her card; she loads Achieve outputs for context review; 100 one-minute NDIS scripts via Claude Code | omi 07-07-1516 |
| BIZ-04 | SupportSignal redeploy as demo asset | Stand the SS app up on fresh Vercel + Supabase for screenshots/live demo | omi 07-07-1516 |
| BIZ-05 | Lars demo prep | 2-3 min tour: Captain's Log, Extension SDK, brain, agents — framed as on-demand micro-apps for him | plaud 07-13-0631 |
| BIZ-06 | Affiliate inquiry triage (with Jan + Mary) | Gather ~2 weeks of AITLDR affiliate emails on david@ideasmen; classify scammy vs real, check prior outreach, draft responses — deferred to a joint session | plaud 07-12-0922, plaud 07-13-0851 |
| BIZ-07 | Meetup follow-ups | July dates into WhatsApp group (10th GTN, 11th US-embassy Anthropic event, 17th Claude event, 24th tech talk); email Angela's project docs; coordinate Angela+Stravan onboarding session | omi 07-04-1000 |
| BIZ-08 | Tony platform provisioning follow-up | Joy Juice + Beauty & Joy client provisioning on one.ie (schemas now visualisable) | plaud 07-09-1533 |

## Brains / Tools / Other apps (10)

| # | Title | Intent | Source(s) |
|---|-------|--------|-----------|
| TOOL-01 | Kybernesis DESIGN.md under brand-dave | Analyze kybernesis.ai's design system → DESIGN.md (AppyDave-adjacent colors + monotype style); unblocks CL-06 | plaud 07-13-0851 |
| TOOL-02 | Gling MCP injection | Gling is unobfuscated Electron: inject startup code exposing an MCP server/API over internal functions (load videos, set keywords); wire FliHub to open Gling pre-loaded; check gling brain for prior reverse-engineering notes first | plaud 07-11-1627, omi 07-11-1603 |
| TOOL-03 | Open-source video-cutting research | Find the recent (~5 days prior to 07-04) conversation about 3 agentic open-source Gling/Descript alternatives; check video-as-code brain + upstream; vet candidates for injection/exfiltration safety. NOTE: Gling renewal already hit (07-11) — decision now = cancel-next-cycle vs TOOL-02 automation | omi 07-04-1240 |
| TOOL-04 | B-roll auto-tagging pipeline | Qwen vision + Whisper to tag the ~1000-video back catalog currently hand-tagged by assistant | omi 07-11-1539 |
| TOOL-05 | Plugin-on-plugin dependencies | Investigate plugin dependency declarations for modularising the AppyDave suite instead of one mega-plugin (verify against official Anthropic docs) | omi 07-11-1506 |
| TOOL-06 | App/port registry untangle | Micro-app registry (location + assigned port) vs locations.json — possibly a KyberAgent extension; the corpus's OLDEST untouched loop (15 days); relates to existing port-registry work in brains repo | omi 06-29-1137 |
| TOOL-07 | Generalized recipe skill | Deep-research ~3 months of recipe conversations + reference recipes (OpenAI Symphony, Karpathy LLM-brain); build create/read/structure/modify/customize with guided Q&A, composing with harness skills (AppyStack, extension SDK) | omi 06-30-0733 |
| TOOL-08 | Thumbnail generator extension + prompt-pacing TUI | Per-brand field configs from thumbnail brain; locate the old Ruby prompt-pacing TUI; matrix-shortlisting (100+ variants → 10-20). NOTE: memory says recipe→thumbnail arc PAUSED to ~late July — hold, don't build | omi 06-30-0801, omi 06-30-0814 |
| TOOL-09 | Session→marketing-assets mining skill | Router skill that post-processes Claude Code sessions into tweets/YouTube material/lead magnets/Skool posts for review-then-deliver → skill-lab | plaud 07-09-0821 |
| TOOL-10 | OMI list app fixes vs Captain's Log supersession | Requested: tags+synopsis in list view, detail toggle, sequential ID scheme, "last pulled" visibility. Decide which land in apps/omi vs are absorbed by Captain's Log (which supersedes the viewer role) | omi 07-04-0810, omi 07-04-1257 |

---

## Not ticketed (personal / already-scheduled)

- HIIT skipping plan + 60/90-day no-sugar window (omi 07-05-1345) — personal/health, David-owned.
- Steak knife + food containers (omi 07-04-1720); NordPass master-password check (omi 07-07-1428) — personal.
- Steve catch-up (omi 07-04-1257), Thursday 11am coffee — calendar event already created by peer (plaud 07-10-1714), Thursday plugins topic (omi 07-11-1644).
- "Agent Burst" business naming (omi 07-03-1503) — parked idea, see 13-idea-register.

## Dedup ledger

~70 raw open-loop actions in → 66 tickets after merging: 3 cross-device OMI/Plaud pairs (doc-watcher, CL extension directive, .clean/raw prototype feedback), Captain's Log spec/build directives collapsed (4→1 into CL-16), Challenge DV pricing walk collapsed (3 captures → BIZ-01 at final $2,750), Linda/Challenge DV recognized as ONE client arc despite 3 thread names.

---

*Calibration run 2026-07-13 (real corpus, 102 records). Replaces the zero-record stub from the prior failed hand-off.*
