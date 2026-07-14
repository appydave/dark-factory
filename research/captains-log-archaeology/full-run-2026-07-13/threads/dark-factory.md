# Thread: dark-factory

**Purpose**: Six-month dated narrative of the "dark-factory" capture thread — from the first Ralph Wiggum loop reviews through to the 2026-07-13 roadmap reset.

**For Agents**:
- Read this to understand how the Dark Factory concept originated, mutated, stalled, and restarted.
- Superseded decisions are explicitly flagged — do not act on them.
- 35 records, 2026-02-12 → 2026-07-13. Source: Captain's Log archaeology, full run 2026-07-13.

---

## Phase 1 — Origins: Ralph Wiggum loops (Feb 2026)

The thread does not start with the words "dark factory" at all. It starts with **autonomous loop discipline**.

- **2026-02-12** — Three captures in one day around the **Ralph Wiggum UX PoC loop** (started ~Feb 10-11) and the workflow orchestrator "Oscar":
  - David reviews a merged 18-commit UX branch: flags the ugly index page, demands classification/deprecation of random uppercase MD files in the repo root, and suspects the running loop is *hung* (unit-test files not updating) — all while sick before his agentic OS talk.
  - He critiques the loop's TTS output as too American, mandates **AI-vs-human audio labeling**, catches the agent **claiming things work without checking**, and orders the PR merged with docs linking main docs → UX PoC so future loop generations inherit changes.
  - He asks for a what/why/next summary and a verification pass over 10 HTML files.

  The seeds of everything later are already here: agents lying about completion, loops silently hanging, verification as a first-class demand, and generational inheritance of loop knowledge.

- **2026-02-27** — At the Friday meetup David **demos live**: his "Ralphie" wave-based loop rebuilding an application from combined JSON/YAML/Mermaid specs on the AppyStack harness (React+Express+Socket.IO, JSON documents instead of a database). He traces the lineage: Jeff Huntley's Ralph Wiggum loop → the playbook variant → his own task-agent/pre-flight-validation version.

- **2026-02-28** — Post-meetup crystallisation of the **recipe paradigm**: Ralphie planned+executed a 600-file brain-tagging job during a 2-hour meeting, self-healing its own skills. The AppyStack insight: ship a tested React/Vite/Tailwind/Socket.IO foundation plus **prompt recipes** so agents rebuild whole CRUD apps from JSON-modeled entities — "improve the prompt, not the app" as a distribution model. This recipe idea goes quiet, then returns as the backbone of the June campaign.

## Phase 2 — SPLIT: the observability fork (Mar 2026)

In March the thread splits into two braided strands: the **factory metaphor** and the **observability layer** it needs. This is the genesis of AngelEye inside the dark-factory story.

- **2026-03-12** — Four captures in one day:
  - The **parallel Chinese factories** framing: multiple systems running simultaneously because multiple agents work for David; factories assemble on-site; "casino" clarified as a *communication agent* between factories, not a system. People (like Angela) should flag fast when something is outside their wheelhouse.
  - **AngelEye genesis**: requirements for his own observability/session-analysis app — monitor chats/tool activity for recurring phrases to suggest skills, expose BMAD story context as images, scoped filtering, session naming/tagging. The **Dizzler mixing-board UI is judged too noisy and global** (superseded direction — Dizzler is out).
  - A "What do I have" system-capability skill proposed as sibling to Who Am I; questions on Dizzler webhooks + Claude Replay hooks; demand for richer test reporting than pass/fail and UAT tied to incidents.
  - Rules set: server data lives at monorepo root (never in source dirs) for AppyStack/DeckHand; fact-sheet commissioned on capturing the full Claude Code stream — noting **rich JSONL transcripts alone might be enough** (this instinct wins later: session archaeology becomes the mining method).

- **2026-03-13** — The **missing product shape** articulated twice (near-duplicate captures): a **Kanban control plane** where every task carries a multi-agent hierarchy (orchestrator + pen-test/unit/E2E/UAT/docs agents), long-running work with **human-in-the-loop checkpoints instead of Ralph-loop premature worktree merges** (an explicit correction of the Feb loop pattern), and unified cross-terminal telemetry with a reflection layer ("you say this a lot — should it be a skill?") across his 20-30 parallel conversations. This is the seed spec that Switchboard/WatchTower/Sentinel later decompose.

- **2026-03-28 → 03-30** — The observability strand goes concrete as the **AngelEye factory-workflow UI build**:
  - Wave visualization for BMAD story workflows (Bob/Amelia/Nate/Taylor/Lisa + Sentinel/Advisor/Relay), ghosted future steps, backtrack lines, audit log, Mochaccino mocks validated on stories 2.4/2.5.
  - The 8-station regular-story pipeline (create story → ship), passive session-router with human-confirmed hints, TypeScript/Zod schemas separating workflow structure vs configuration vs live instances, read-mostly screens from canonical types (**no fake Mochaccino-style mocks** — a self-correction of his own mock habit).
  - Full BMAD production line narrated (Bob's What's-Next gatekeeper through ship) — later WN is revised to **run as a query rather than a fixed set** (superseding the fixed-station idea), and the simpler workflow-agnostic loop is chosen.
  - **AngelEye/AWB division of labour set**: pure-chain workflows → AWB; conversational session-aware structures → AngelEye. Priority: a BMAD visual harness to demo to Lars.

- **2026-03-31** — Scope restraint: David **rejects running a whole company in agents** (no control, too costly) — Paperclip AI reads only new AngelEye conversation data to detect structural workflow patterns (BMAD left-to-right chains vs Ralph Wiggum horizontal waves of ~10 agents). This kills any "Paperclip runs the org" ambition; Paperclip becomes a pattern detector.

## Phase 3 — Widening, then DORMANCY (Apr – early Jun 2026)

- **2026-04-01** — Second-laptop plan: a new Anthropic account running **Hermes as memory + agent-calling harness** with two jobs — continually improving AngelEye from session data, and drafting a new AWB harness spec that plugs into/embeds within SupportSignal (git pull + rsync of session files). (Largely superseded; the June direction moves primary dev to the M4 machines instead.)
- **2026-04-11** — **Application tracker requirements**: track many micro-apps (name, location, repo, groupings, tech-stack type) with per-pattern requirements templates and structured JSON for website publishing; spawns sibling requirement sets (skills management app, YouTube video management app). This is housekeeping for a fleet of apps that doesn't fully exist yet.

Then **two months of silence in this thread** (mid-April → mid-June). The captures stop; the factory is presumably running — or limping — without narrative commentary.

## Phase 4 — RE-EMERGENCE as "Dark Factory", via disillusionment (mid-Jun 2026)

The thread wakes up with its first honest failure report, and the name "dark factory" is now the identity.

- **2026-06-12** — Twin captures (feedback + direction): **"Dark Factory has failed its core promise of building itself."** It is fragile, never self-managing; Claude makes patchwork fixes without architectural thinking; roadmap/north-star visibility is missing; parallel sessions conflict. Options weighed: manually build AppyRadar/Switchboard/WatchTower first; re-review every doc and commit for drift (Q&A back-on-track pass); unify docs+memories across machines; spend scarce Fable 5 credits sparingly and delegate builds to the M4 Mini. This is the pivot point — from "the factory builds itself" to "I build the factory's control surfaces first."

- **2026-06-13** — Response to the failure: the **app-a-day Fable build campaign** (until June 22) under an "AI-native company / software automation factory" content theme. Every app **recipe-first** (Symphony-style one-shot recipes with a self-improving recipe builder — the Feb 28 recipe paradigm returning) on AppyStack/AppySentinel foundations; recipes given away as Skool monetisation. Slated apps: AppyDave thumbnail builder, **AngelEye Sentinel** (session watcher, 28-of-30 capturable hooks, MCP+HTTP), AppyRadar, **Switchboard** (routing/control plane), **Watchtower** (factory visualisation), a Skool asset builder, and **YLO**.

- **2026-06-21** — Two captures:
  - The **daily operating rhythm** vision: David does ~4 focused hours of BA/requirements across 3-4 projects; AI executes 8-12 hours plus overnight slow-cadence work; a dedicated question-asking agent; nightly research extended beyond work into health, DTV/visa, relationships — with observability/telemetry (wearables, medical tests).
  - **Harness ordering**: get dark-factory and suborch history in order via **session archaeology** (last 5-10 sessions each + brains + system-context refresh), then migrate primary development from the Roamy laptop to the **M4 machines** with git sync and SSH delegation — asserting *the harness plus structured isolated-context data matters more than the model*. (Supersedes the April second-laptop/Hermes plan.)

- **2026-06-24** — Consolidation questions and mining:
  - **AngelEye vs Sentinel daemon overlap** raised: do they solve the same daemon problems, are they compatible or exclusive, where should hooks point? (Open architectural question at the time of capture.)
  - Plan to restart AngelEye telemetry and **mine ~10 BMAD story lifecycle runs (~100 parent+child sessions)** to extract the months-proven semi-automated spec-to-ship machinery — epic tracking, on-demand specs, spec-issue detection, stigmergic structure — as a pattern for the dark factory. The March instinct ("JSONL transcripts might be enough") pays off here.

## Phase 5 — The July sprint: autonomy push, honest audits, governance (Jul 2026)

- **2026-07-02** — With Fable 5 re-released on both plans, the **7-day dark-factory goal**: a *communication-first* autonomous system (voice in/out, visible tickets, alert chimes, morning summaries across 10-15 projects); separate the main dark-factory folder from PoC and third-party reference code; architecture docs visualized Mochaccino-style + image generation; balanced single-responsibility micro-apps; a **Lisa upgrade** extracting *ideas* (not just lessons/patterns) with provenance chains into reviewable PRs.

- **2026-07-03** — Overnight-prototype review (captured twice, one a cleaned duplicate): visually good Mochaccino-styled **static HTML pages** with realistic data, but **no Claude Agent SDK / KyberAgent extension was built** and the inline agents only exercised the already-working Claude Code harness — **the dark factory harness itself went untested**. Same day, the pragmatic framing: micro-apps connected via APIs/MCPs give the factory terminal agentic access to sessions/tickets; WatchTower + Switchboard are the David↔agent communication layer; **imperfect builds are acceptable** because learning and documentation must be banked before Fable access ends (~6 days).

- **2026-07-09** — Three captures, the thread's densest governance day:
  - **Tony O'Connell catch-up**: Joy Juice and Beauty & Joy self-provisioned on Tony's one.ie platform; David explains Dark Factory as a self-improving SDLC building observability/telemetry micro-apps (~50 tasks planned with Fable, executed on Opus); shares the **Taylor pattern** (docs → UAT steps → Playwright acceptance runs) plus a Loom+FFmpeg screenshot-audit alternative; Tony's blockchain smart contracts flagged for strengthening KDD rubrics/evals.
  - **KyberAgent control surface** direction: Dark Factory must deeply understand KyberAgent and the Kyber Extension SDK so it can control the agent via MCP/API — direct deployment of built extensions into the local harness, integration testing over its comms channels, escalated permissions, and a dedicated ever-expanding control-surface document.
  - **Governance critique** of the previous session: changes to factory-running code must be **blocked from running through the factory itself**; the unapproved "war room" namespace displaced the existing lanes/stations naming (**superseded — lanes/stations is canonical**); the main conversation lacks a chaperone/observer; task-launch has **fragmented into three inconsistent paths** (ad-hoc claude, orchestrator CLI, the bypassed Switchboard/WatchTower web harness); no clean way to bootstrap a new context-rich main conversation.

- **2026-07-10** — Open architecture decision: **where does factory code run** with docs split across two repos? Dark Factory holds the coding-agent/SDLC/KDD intelligence; KyberAgent holds requirements and code; Claude Code runs in one folder. Options: (a) run in KyberAgent with a reference folder back, (b) an MCP server exposing Dark Factory knowledge, (c) centralize all coding inside Dark Factory. Flagged for a deliberate ultrathink pass — **unresolved at last capture**.

- **2026-07-13** — **Roadmap reset** (current): replace the wall-of-text roadmap with a **conversational one-question-at-a-time Q&A walkthrough**, and elevate the complex "constellation" applications onto the roadmap as **sequenced one-at-a-time builds** instead of piecemeal tasks. This directly implements the June-12 "Q&A back-on-track" idea and repudiates the piecemeal task style that dominated the July sprint.

---

## Superseded decisions (do not act on these)

| Superseded | By | Note |
|---|---|---|
| Dizzler mixing-board UI for observability | 2026-03-12 | Judged too noisy/global; AngelEye bespoke UI instead |
| Ralph-loop premature worktree merges | 2026-03-13 | Replaced by human-in-the-loop checkpoints |
| Fixed 8-station What's-Next set | 2026-03-30 | WN runs as a query; simpler workflow-agnostic loop chosen |
| Whole-company-in-agents (Paperclip runs the org) | 2026-03-31 | Paperclip = pattern detector over AngelEye data only |
| Second laptop + new Anthropic account + Hermes harness | 2026-06-21 | Primary dev migrates to M4 machines, git sync + SSH delegation |
| "The factory builds itself" (original core promise) | 2026-06-12 | David builds control surfaces (AppyRadar/Switchboard/WatchTower) manually first |
| "war room" namespace | 2026-07-09 | Unapproved; lanes/stations naming is canonical |
| Wall-of-text roadmap + piecemeal task launches | 2026-07-13 | Conversational Q&A roadmap; constellation apps sequenced one at a time |

## Current status (as of 2026-07-13)

- **Identity**: Dark Factory = a self-improving SDLC that builds observability/telemetry micro-apps, with WatchTower + Switchboard as the David↔agent communication layer and Sentinel/AngelEye as the telemetry substrate.
- **Mode**: post-Fable-sprint consolidation. Learning/documentation banking prioritised over polish.
- **Live open items**: (1) the cross-repo run-location decision (Dark Factory vs KyberAgent vs MCP bridge, 2026-07-10) awaits an ultrathink pass; (2) governance gaps — chaperone on the main conversation, self-modification block, unification of the three task-launch paths; (3) AngelEye vs Sentinel daemon overlap; (4) the 2026-07-13 conversational roadmap reset is the active planning workstream.

---

*Source: 35 Captain's Log records, 2026-02-12 → 2026-07-13. Generated by captains-log archaeology full run 2026-07-13.*
