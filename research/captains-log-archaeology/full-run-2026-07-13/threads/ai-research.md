# Thread: ai-research

**Purpose**: 6-month dated narrative of David's "ai-research" capture thread (40 records, 2026-01-09 → 2026-07-10) — how it started, evolved, split, went dormant, and re-emerged.

**For Agents**:
- Use this to understand the arc of David's AI-tooling research before proposing new research loops
- Check the "Superseded decisions" section before citing any decision from this thread
- Current status is at the bottom; everything above is history

---

## The arc at a glance

```
Jan ─ BMAD ecosystem contributions (b-integrator, BVibe, Autoclawed)
Feb ─ Broad scanning: second brains (Cole Medin), image gen (kie.ai), ADEs (Kintsugi)
Mar ─ CRYSTALLIZATION: $5k/mo client funds the research → "agentic OS" becomes the spine
      Mar 6 burst: AionUI, MOTUS, gap-analysis backlog
Apr ─ Cost crisis + harness shootout (Hermes, Archon, unified-harness question, ghosty)
Apr 6 → Jun 13 ─ DORMANT (~9 weeks)
Jun–Jul ─ RE-EMERGENCE: Fable access shutdown, platform 5.6 regression,
      connector-first memory architecture (current framing)
```

---

## Phase 1 — Origin: the BMAD contribution burst (2026-01-09 → 2026-01-11)

The thread **starts** on **2026-01-09** with David having just joined the BMAD Method Corp core group and writing his contribution message to Brian and the team. Three records land the same day:

- **Idea**: a thin Zapier-style integration layer (**"b-integrator" / "b-connect"**, modelled on Ian's 3-hour vibe-coded Claudiaire) connecting enterprise Kanban tools (Jira/Asana/Linear/Notion) to agent harnesses — plus **"BVibe"**, a vibe-coding front end to BMAD that silently accrues epics/stories/PRDs for a one-button brownfield upgrade.
- **Feedback**: his two-cents message covering the flow system, QuickFlow/Kanban/Autoclawed positioning, and turning BMAD conversation knowledge into visuals.
- **Research loop opened**: a multi-agent architectural teardown of **Autoclawed** (Electron Kanban + multi-Claude spawning + RAG memory) — "looks good but heavy and buggy".

**2026-01-11** adds a second seed that will become its own sub-thread: with Kevin, exploring **Nano Banana contextual data visualizations** via structured JSON prompts, aimed at parsing large wearable-recording volumes.

So the thread is born as *two* strands: (a) BMAD/agent-harness ecosystem, (b) AI image/visualization economics.

## Phase 2 — Broad scanning (2026-02-02 → 2026-02-28)

February is wide-aperture reconnaissance, no spine yet:

- **02-02** — a peer floats collaborating on **vMAD-method** side projects (BMAD wrappers for visualization/action). Loop opened; never re-appears in this thread — effectively **abandoned**.
- **02-10** — prompt-crafting session; and a **superseded-on-the-spot decision**: David rejects an outdated voice-agent model comparison (GPT-4o near deprecation, Qwen/Kimi viable) and sets a standing rule — **model selection must be OpenRouter-based and web-searched, never from LLM memory**.
- **02-12** — the image strand continues: reviews Steve's (Dreaming Computers) ComfyUI + kie.ai video; feedback that Steve should ship the JSON + blog into his Skool community.
- **02-20** — the pivotal input of the month: **Cole Medin's Dynamous workshop** on his Claude Code + Agent SDK second brain (soul/user/memory.md, hooks, hybrid RAG, heartbeat on a locked-down VPS, "PydanticAI for production / Agent SDK for personal"). This becomes the reference architecture David keeps returning to.
- **02-21** — infrastructure literacy (tmux vs PM2 dashboards) and first ADE sighting: **Kintsugi** (Sonar's macOS agentic dev environment layered on Claude Code).
- **02-28** — image strand again: one-shot spec/UI/Mermaid generation from a single JSON spec, plus the Gemini-prompt → kie.ai-playground pattern (~6c per infographic).

## Phase 3 — Crystallization: the agentic OS spine (2026-03-01 → 2026-03-16)

- **03-01** — the image strand peaks and is **split off**: kie.ai NanoBanana 2 study routed into a **kie-ai brain refresh** loop. After this, image-gen research largely leaves the thread (it now lives in the `kie-ai` brain).
- **03-02** — a strategic watch-note: track sub-$10k clients and enterprise AI deployment (Amazon, BMW, Fox).
- **03-04** — **the hinge of the whole thread**: David lands a **$5k USD/month SEO client explicitly to fund his Claude Code / agentic-OS research**. Same day he articulates the vertical stack (second brain, memories, chat, voice) vs horizontal stack (multi-agent coordination), decides **paid community beats courses**, and briefs his agent on ingestion/routing/morning-briefing/heartbeat design. The "agentic OS architecture build-out" loop opens; everything after this is in its gravity. A **Krisp** exploration question opens the same day (relation to OMI).
- **03-06** — the single busiest day: five records.
  - **AionUI evaluation** loop opens with three records — research brief (compare vs KyberBot, verify ACP vs A2A from the repo), then upgraded to a deep dive as a possible "harness-on-top-of-harnesses" layer inside the agentic OS.
  - Directive to clone the meetup's high-star agent frameworks (NanoBot, NanoClaw, Pocket Hermes, PicoClaw) into upstream as research areas.
  - **MOTUS vs Paperclip** comparison loop opens (Ian's agent org-chart system).
  - A background research backlog: gap analyses of **Paperclip, KyberBot, and Tom's Valor Agent** against his own Agentic OS "to borrow ideas".
  - Plus one stray: scroll-driven web animation as a Remotion alternative.
  - Note the implicit **supersession**: the January Autoclawed teardown is never revisited — AionUI takes its slot as the multi-agent-front-end candidate.
- **03-09 / 03-10 / 03-16** — the BMAD strand quietly continues alongside: Claude API + `/loop` research with a BMAD epics/stories build-order question; an **A2A** (agent-to-agent communication) question; and a basic "how do I kick off BMAD" question. Notably, the ambitious January BVibe/b-integrator ideas have **gone silent** — by mid-March David is asking operator-level BMAD questions, not building BMAD products. Treat BVibe/b-integrator as **dormant-superseded** by the agentic-OS focus.

## Phase 4 — Cost crisis and the harness shootout (2026-03-28 → 2026-04-06)

- **03-28** — the model-economics strand returns as a designed experiment: **multi-model brain tagging** (local Qwen/Mistral via Ollama + free OpenRouter models) benchmarked against Haiku/Gemini/Codex with cost/speed metrics — a direct descendant of the 02-10 "never trust from-memory model advice" rule.
- **04-01** — five records in one day, the thread's stress peak:
  - **Subscription cost crisis**: the $200 Claude plan is exhausting within its 7-day window because background agents and swarms are exploding token costs. Standing up secondary $20 Codex/Anthropic accounts; reluctantly weighing **two $200 plans** (OpenAI + Claude); probing AUD annual cost and self-hosting economics ("AI subscription cost strategy" loop).
  - **Hermes ("Herbie") install** committed to — manual install, submodules step missed.
  - **Unified harness comparison** loop: model-agnostic harnesses (Claude Code, Hermes, Paperclip-like) driving Codex/Gemini — including weighing **building off the leaked Claude Code source (v2.10.88)** vs adopting something polished. No later record resolves this; the July connector-first idea suggests the build-your-own-harness impulse was **not pursued** — treat as superseded.
  - Minor: ChatGPT-remote-control question (truncated, unanswered) and a ChatGPT-vs-Claude voice comparison.
- **04-02 → 04-04** — **Archon** enters: Dynamous livestream preview, then hands-on with the prerelease (YAML workflows, prompt vs batch-command nodes) and figuring out **Archon + BMAD** integration — the BMAD strand and the agentic-OS strand **merge** here.
- **04-06** — last record before dormancy: a note-to-self to prove **ghosty** (tmux multi-agent swarm) with a BMAD 6.7 run and a Haiku swarm.

## Dormancy (2026-04-06 → 2026-06-13, ~9 weeks)

The thread goes completely quiet for over two months — the longest gap in its life. Plausibly the April cost crisis plus the funded client work absorbed the bandwidth; the open loops (ghosty testing, Hermes install, unified-harness question, MOTUS comparison, Krisp) all freeze in place with no recorded closure.

## Re-emergence — sovereignty and skepticism (2026-06-13 → 2026-07-10)

The thread returns with a distinctly different mood: less "evaluate everything", more **risk, cost, and data sovereignty**.

- **06-13** — over pre-meetup lunch: the sudden **US-government shutdown of Fable model access** (VPN blocks, possible KYC/citizenship gating), directly hitting David's own work — he'd been using it to build a **visual explorer for his brain** (node/graph views of ingestion/retrieval) on a $20 plan, with a long run possibly cut off mid-flight. Vendor-access fragility becomes a live concern, not a hypothetical.
- **07-07** — Anthropic's **"unknown unknowns" agent pattern** (broad north stars beat prescriptive plans) + an unresolved question about smart contracts in dual-loop planning.
- **07-10** — two records that define the **current** stance:
  - Peer report that **platform 5.6 regressed vs 5.5** (hour-long thread queues, costlier, broken codex integration, skills effectively unsupported); vendor seen as pivoting to consumers over developers — "watch over the next few weeks".
  - **The connector-first memory architecture idea**: if chat has connectors to your *own* specialized storage (a brain here, two brains there), you may not need the vendor's repos or hidden memory at all — avoiding lock-in, keeping data sovereignty. This is the thread's newest organizing idea and arguably **supersedes** the earlier instinct to adopt/build a single unifying harness: the value moves from the harness to the owned storage it connects to.

---

## Splits and merges (summary)

| Event | When | What happened |
|---|---|---|
| Split: image-gen strand → kie-ai brain | 2026-03-01 | Nano Banana / kie.ai research (Jan 11, Feb 12, Feb 28, Mar 1) routed into the `kie-ai` brain; leaves this thread |
| Merge: BMAD strand + agentic-OS strand | 2026-04-04 | Archon evaluated explicitly as the engine to run BMAD inside the agentic OS |
| Crystallization | 2026-03-04 | Scattered scanning reorganizes around the funded "agentic OS architecture build-out" |

## Superseded decisions / dead branches

- **BVibe + b-integrator/b-connect** (2026-01-09) — never mentioned again after January; displaced by the agentic-OS focus. Dormant, likely dead.
- **vMAD side-project collaboration** (2026-02-02) — loop opened, no follow-up. Abandoned.
- **From-memory model comparisons** (2026-02-10) — explicitly rejected; superseded by the OpenRouter/web-searched rule, later operationalized in the 03-28 multi-model tagging experiment. (Note 04-01: Chinese models flagged as omitted from a prior comparison — same rule reasserting itself.)
- **Autoclawed as the multi-agent front end** (2026-01-09) — teardown requested, never revisited; AionUI (2026-03-06) took its evaluation slot.
- **Building a unified harness off leaked Claude Code v2.10.88** (2026-04-01) — weighed, never acted on; the 2026-07-10 connector-first idea points the architecture away from harness-building entirely.
- **Single $200 Claude plan as sufficient** (implicit pre-April) — broken by swarm token costs; superseded by the multi-account strategy (2026-04-01).

## Open loops never closed on record

ghosty swarm testing (04-06) · Hermes install (04-01) · unified harness comparison (04-01) · MOTUS vs Paperclip (03-06) · Krisp exploration (03-04) · A2A question (03-10) · Fable access suspension (06-13).

## Current status (as of 2026-07-13)

**Active but repositioned.** After the 9-week dormancy, the thread has re-emerged around three live concerns: vendor-access fragility (Fable shutdown), vendor-quality regression (platform 5.6, watch for a few weeks), and the **connector-first memory architecture** — own the brains, connect the chat, skip the vendor's memory. That last idea is the thread's current center of gravity and the most likely seed of its next research burst; the April-era harness-evaluation loops remain open but stale.
