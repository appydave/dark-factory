# Brain Improvements — Knowledge to Promote (v2 harvest)

**Purpose**: Corpus knowledge that belongs in `~/dev/ad/brains/` (or client brains), plus misfiled/cross-project insights the thread model surfaced.

**For Agents**: These are pointers for curation passes, NOT auto-writes. Per standing rule: unverified OMI/Plaud content goes to TIL + research stubs only until David verifies. Items marked ⚠️ contain sensitive/commercial facts.

---

## Promote to existing brains

### kybernesis brain (`brains/kybernesis/`)
- **Extension architecture canon** (settled 07-03, corrected twice 07-07): one GitHub repo per extension; iframe-loaded, FDE-built, never baked into codebase; package.json → Agent SDK interface contracts; extension = daemon/web server + iframe client; **iframe never routes through the host to reach its own backend** (AngelEye = reference implementation). Two agent-model corrections in 4 days means the written canon is missing — highest-value promotion in this list.
- **Extension SDK gap register**: host-mediated LLM/chat access; daemon-owned scheduling invoking extension hooks; panel-vs-mount terminology. Root-cause lesson: the failed OMI extension reinvented tagging + its own pulse instead of delegating to the host (07-05 diagnosis).
- ⚠️ **Founding/commercial facts** (07-07, David-stated): Kybernesis raising US$1.5–3M, ~$1M committed; David founding employee ~2%. Verify with David before writing anywhere.
- Two-agent feedback loop concept (extension-builder ↔ platform-extender) — design note.

### dark-factory brain (`brains/dark-factory/`)
- **Governance failure post-mortem** (07-09): factory self-approved changes to factory-running code; unapproved "war room" namespace displaced lanes/stations; no observer on main conversation; three inconsistent task-launch paths. This is a textbook staged-autonomy regression — exactly what the brain's autonomy model (0–5) exists to catalog.
- **Piecemeal-gravity lesson** (07-13): unattended, the factory gravitates to small tasks; roadmaps must be structured around big "constellation" applications sequenced one at a time.
- Smart-contracts-as-eval-rubrics concept (Tony O'Connell 07-09 + peer session 07-07): verifiable contract + rubric (security/stability/simplicity/speed) at end of a unit of work; post-hoc verification plan reading whole-repo history beats pre-set plans. Cross-file to `brains/evals/`.
- KDD read-loop gap: "the factory writes knowledge but nothing reads it" — structural insight for both dark-factory and the KDD docs.

### gling brain (`brains/gling/`)
- **Direction change** (07-11, supersedes 07-04): replace-Gling research is dead; subscription renewed; new plan is injecting an MCP/API control layer into the unobfuscated Electron app at startup so Claude Code/FliHub can drive it. Record 07-04's open-source-alternatives intent as negative knowledge (considered, dropped).

### ai-meetups brain (`brains/ai-meetups/`)
- 07-04 Saturday meetup: Anthropic data-retention nuance (subscription opt-in vs enterprise zero-retention), Sonnet 5 vs GLM 5.2 + first GLM harness, Fable cache-TTL economics, Spotify CTO×Boris (75% PRs AI-handled, intent-level prompting). Next Saturday cancelled → US-embassy Anthropic event.
- 07-11 Chiang Mai meetup (Ian Borders): Claude Tag as multiplayer Slack teammate w/ own account/memory/sandbox; certified-partner exam; multi-agent marketing orchestration demo.
- 07-10 Ishan GTM lecture: coding-agent-driven cold outreach on DeepLine; reply-rate not open-rate (1/200–300 good); effort-as-proxy emails.
- Peer report (07-10): platform v5.6 regression (queues, cost, codex integration, fights user skills) — recheck in 1–4 weeks.
- Connector-first-over-hidden-memory insight (07-10) — cross-file to `brains/agent-memory/` (fits its lossy-vs-lossless / external-memory decision layer).

### todo / client brains
- ⚠️ **Challenge DV** (no brain exists — candidate `~/dev/clients/` doc): Linda contact; competing $25k video quote; FDE retainer **$2,750/mo incl GST ($2,500+GST)**, weekly 90-min training + 1–2 tools/mo, start 15 July mid-month-to-mid-month; demo = KyberAgent + CL. 
- ⚠️ **Achieve/Angela** (candidate under supportsignal-adjacent client area): $1.2–4M funding gap, ~1,100 weekly rejected invoices, siloed CI register, no single source of truth, "daisy links" framing; North Star = FDE schema-driven read-only micro-apps w/ synthetic data; 3-week visual demo, NOT a full app; achieve-mvp repo under Supporting Potential org; Angela invoiced $1,000, on Claude Max; content engine = 100 NDIS scripts.
- **lars brain** (`brains/lars/`): demo plan — KyberAgent + brain + Extension SDK walkthrough, 2–3 min CL demo; Lars wants concrete extension examples.

### Skill/plugin docs (appydave-plugins, per skill-creation rule)
- `plaud-fetch`: token brittleness root cause (other Plaud clients invalidate refresh token) + planned Playwright re-auth — belongs in the skill's own docs.
- `omi-fetch`: naming/scope note — provider-agnostic future is the shared controller (Captain's Log); fetch skills stay thin.

## Misfiled / cross-project insights (the thread model caught these)

1. **Client decision inside a product thread**: the final Challenge DV price ($2,750) lives in the 07-13 CL UX-walkthrough capture (thread `captains-log`), not `client-challenge-dv`. Any client-facing agent reading only the client thread sends the WRONG price ($3,300). This is the single most dangerous misfile in the corpus.
2. **Affiliate triage** decision (do later with Jan+Mary) also buried in the same CL walkthrough record — belongs in todo/team context.
3. **DESIGN.md ask** targets `brand-dave` (brand system) but was captured in a CL critique — route to brand-dave, not the CL repo.
4. **Multi-topic captures are the norm**: the A330–A339 walkthrough spans CL UX + client pricing + team ops + Gling. One-record-one-thread forces a lossy choice — argument for CL's capture-splitting feature (punchlist #1).

## TIL candidates (unverified, per OMI rule)
- Fable 5-min cache TTL wake-up hacks; GLM 5.2 first harness; Claude Tag mechanics; DeepLine as Clay replacement; Loom+ffmpeg/Qwen visual-audit technique (David shared it — likely verifiable quickly).
