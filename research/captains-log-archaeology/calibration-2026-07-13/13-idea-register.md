# 13 — Idea Register

**Purpose**: Genuinely novel ideas from the slice worth keeping, organized by theme.

**For Agents**:
- "Novel" = not already a routed ticket in `10-tickets.md`, not already brain-canon, or an idea whose VALUE exceeds its ticket (the ticket builds a thing; the idea is a reusable pattern).
- Dispositions: **keep** (register here), **app-pipeline** (route to `dark-factory/app-pipeline/`, the single app-idea intake), **brain** (see 12-brain-improvements), **park**.

---

## Theme: Capture intelligence (the Captain's Log conceptual family)

| Idea | Statement | Source(s) | Disposition |
|------|-----------|-----------|-------------|
| Unified "transcript" abstraction | OMI, Plaud, emailed links, YouTube, scraped articles are all one normalized type — transcripts — flowing through one analyze/summarize/tag pipeline. Providers differ only at fetch. | plaud 07-05-1831, 07-11-0733 | keep — this is Captain's Log's core thesis |
| Quest / side-quest threading | Captures link temporally (2nd/3rd mention same day) AND thematically (one capture splits into ideas joining different chains) — Dark Factory's quest framing applied to personal capture | plaud 07-13-0714, omi 07-06-0903 | keep — ticketed (CL-11) but the framing generalizes to any knowledge stream |
| Sequential human ID scheme | A00-style short codes ("go get A001") as the reference currency between human, agent, and UI — IDs as conversation handles, not DB keys | omi 07-04-0810 | keep |
| Deliberate dual-device bake-off | Record the same speech on two devices specifically to score transcription quality — cheap self-run eval methodology | plaud 07-06-0904 | keep — reusable eval pattern |
| Vernacular normalization without context change | Entity-dictionary pass that fixes product names in transcripts while provably not altering meaning | plaud 07-12-0642 | keep — pipeline + product dual-use |

## Theme: Agent architecture

| Idea | Statement | Source(s) | Disposition |
|------|-----------|-----------|-------------|
| Connector-first memory | If connectors to your own specialized brains are solid, you may not need the vendor's opaque in-app memory at all — sovereignty by architecture | plaud 07-10-1721 | brain (`agent-memory`) |
| Two-agent builder↔platform loop | Extension-builder agent runs SDLC on extensions; every platform gap it hits becomes a prioritized roadmap ticket for a second agent that extends the platform — demand-driven platform development | plaud 07-13-0712 | keep — ticketed (KYB-07) but pattern generalizes to any SDK+consumer pair |
| Doc-watcher brain agent | A dedicated agent whose ONLY job is reading a system's docs+commits and reporting what teammates added — brain-as-searchable-memory over repos | omi 07-06-0904, plaud 07-13-0657 | keep — pattern for any multi-contributor system |
| Contracts + rubrics per unit of work | Close each unit of work with security/stability/simplicity/speed rubric verification; optionally staked (smart-contract flavored); happiness-score A/B across agents | omi 07-07-1641, plaud 07-09-1533 | keep — feeds `evals` brain + KDD-05 |
| Broad north stars over prescriptive plans | For agents, an over-specified plan underperforms a strong north star + freedom (Anthropic unknown-unknowns pattern applied to planning) | omi 07-07-1626 | keep |
| Ideas-not-just-lessons extraction | KDD librarians should mine IDEAS (not only lessons/patterns/ADRs) into provenance-chained speculative PRs agents work while idle — the factory generates its own side quests | omi 07-02-0633 | keep — ticketed (KDD-06), doctrine-grade |

## Theme: Business & monetization

| Idea | Statement | Source(s) | Disposition |
|------|-----------|-----------|-------------|
| Recipes as sellable products | App core logic + visualization surface packaged as a "recipe" sold via paywall/community — the ~100 micro-app backlog becomes inventory, not debt | omi 06-29-1137 | keep — strategic |
| FDE retainer template | ~$2,750/mo inc GST: weekly 90-min training + 1-2 bespoke micro-tools; sell the teaching AND the tooling; demo with your own live system (Captain's Log) | plaud 07-13-0633/0851, omi 07-07-0959/1516 | brain (`creator-os`) — three clients converged on it independently |
| Session→marketing-assets mining | Every coding session post-processed by a router skill into tweets / YouTube material / lead magnets / Skool posts — marketing as an SDLC byproduct | plaud 07-09-0821 | app-pipeline (via TOOL-09) |
| Extensions as bespoke small-business micro-apps | Configurable till/POS with per-business line-item shapes; pricing data feeds websites, videos, and agents — Joy's shops as the prototype | omi 07-11-1539 | keep |
| "Agent Burst" | Coworking concept of agents chatting in a shared room; business name unresolved | omi 07-03-1503 | park |

## Theme: Media & workflow tooling

| Idea | Statement | Source(s) | Disposition |
|------|-----------|-----------|-------------|
| Inject MCP into closed Electron apps | Unobfuscated Electron app + startup injection = free API/MCP over any desktop tool you already pay for; enhance, don't rebuild | plaud 07-11-1627 | keep — generalizes way beyond Gling |
| Prompt-pacing TUI | Cron-paced batch prompt execution ("run 20 image prompts while at lunch") — resurrect the old Ruby tool as an extension | omi 06-30-0814 | park (thumbnail arc paused) |
| Combinatorial shortlisting | The thumbnail problem is not generation but reduction: 100+ variant matrix → 10-20 candidates → 3 used; shortlisting is the product | omi 06-30-0814 | keep — applies to any generative fan-out |
| UAT from a Loom walkthrough | Record a Loom, ffmpeg frame-match against Playwright runs to build an audit trail agents can fix from (Taylor agent) | plaud 07-09-1533 | keep |
| B-roll auto-tagging | Qwen vision + Whisper over raw footage replaces human tagging of a 1000-video catalog | omi 07-11-1539 | app-pipeline (via TOOL-04) |

## Theme: Knowledge-factory doctrine

| Idea | Statement | Source(s) | Disposition |
|------|-----------|-----------|-------------|
| Knowledge must be READ structurally | Writing KDDs is worthless unless reads are wired into SDLC checkpoints (PR validation etc.) — consumption points, not storage, define a knowledge system | omi 07-04-1257 | brain (`dark-factory`) — the fortnight's deepest insight |
| Self-modification firewall | An autonomous factory must treat changes to its own orchestration code as a distinct, human-gated class of work | plaud 07-09-0642 | brain (`dark-factory`) |
| Skill registry with staleness | Investigated-vs-used split (~1100 vs ~100) + last-accessed decay — skills as inventory with shelf life, not a pile | omi 07-04-0800 | keep — ticketed (DF-12) |
| Extensions must serve humans AND agents | Minimum-viable data isn't viable: every surface needs inferred metadata, summaries, usage docs, and search for both consumer types | omi 07-04-0806 | keep — design principle |

---

## Cross-check ledger

- Checked against `10-tickets.md`: ideas that are ALSO tickets are marked; register keeps the generalizable pattern, ticket keeps the build.
- App-shaped ideas routed to `dark-factory/app-pipeline/` per the single-intake rule (session-mining skill, B-roll tagger).
- Thumbnail/prompt-TUI items parked per memory: recipe→thumbnail arc PAUSED until ~late July.

---

*Calibration run 2026-07-13 (real corpus). Replaces the zero-record stub.*
