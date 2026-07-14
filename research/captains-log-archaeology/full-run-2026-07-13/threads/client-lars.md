# Thread: client-lars

**Purpose**: Six-month dated narrative of the Lars Filtenberg (Tjeks ApS, Copenhagen) client engagement, reconstructed from 24 Captain's Log captures.

**For Agents**:
- Use this to understand the lifecycle of the Lars engagement — origin, delivery arc, value crisis, dormancy, and re-emergence.
- Superseded decisions are called out explicitly; do not treat early-phase decisions (cadence, tooling, OpenClaw framing) as current.
- Current status is at the bottom.

**Thread id**: `client-lars` | **Records**: 24 | **Span**: 2026-01-31 → 2026-07-13

---

## Shape of the thread

```
Jan 31        Mar 1-11           Mar 28-31            Apr 1-2         Apr 3 ─────── Jul 12   Jul 13
DEAL     →    ONBOARDING     →   VALUE CRISIS &   →   AGENTIC     →   DORMANT (~3.5 months) → RE-EMERGED
struck        sprint             cadence reset        COMMS LIVE      (no captures)           KyberAgent demo
```

One intense 9-week burst (late Jan – early Apr), then silence, then a single re-emergence record on the day of this run.

---

## Phase 1 — The deal (2026-01-31)

**2026-01-31 (decision)** — David and Lars agree a ~3-month AI-workflow engagement starting **March 1**, ~$5k/month with **weekly check-ins**, plus a smaller month-one prepayment invoiced immediately so David can buy an M4 (personal workstation) and repurpose his M2 as a ClaudeBot/OpenClaw machine. The plan: livestream and document both setups so Lars can model them without exposing his proprietary SEO logic. Framing at this point: librarian/guardrails pattern, council-of-agents skill idea, virtual employees replacing hires, and OpenClaw's security fiasco as cautionary context.

> ⚠️ **Superseded**: the "weekly check-ins" cadence lasted about a month (see Mar 3 → Mar 31 escalation to daily). The M2-as-OpenClaw plan was overtaken by hardware events (Feb 28), and OpenClaw itself faded from the engagement framing — by July the demo subject is **KyberAgent**.

## Phase 2 — Hardware wobble on the eve of kickoff (2026-02-28)

**2026-02-28 (direction)** — The M4 Pro's screen dies days before the March 1 start. David plans an emergency migration to the M4 Mini as primary machine and a **video update email to Lars** — the first instance of the video-update communication pattern. Repair pressure: two weeks, before a Vietnam conference needing a mobile platform.

## Phase 3 — Onboarding sprint (2026-03-01 → 2026-03-11)

The engagement starts on time despite the hardware crisis. Eleven days of dense delivery:

- **2026-03-01 (meeting ×2)** — David records a **Project Theodore walkthrough** for Lars (horizontal Tailscale/Supabase mesh + vertical per-machine agent stacks: KyberBot memory, Claude Code harness, Samantha voice) and proposes a Tuesday kickoff. Same day, a week-in-review video: AppyStack pattern, Ralphie loop plugin, Lisa librarian, the four-layer agentic OS model. Side thread floated: Lars helping Joy with recipes/portion control for her shop.
- **2026-03-03 (direction)** — Client-comms infrastructure: the vOz client-communication folder is generalised into a **Lars template** (USD 5k package, **no invoice emails without approval**, North Star as primary comms doc, raw OMI inbox folder, `jLars` jump command).
- **2026-03-03 (meeting)** — **90-day kickoff proper.** David pitches the agentic-OS vision (brains before skills, flywheel intangibles); Lars counter-anchors: he wants **tangible wins within a month** and his two new machines working. First deliverable agreed: an **Ansible client-template playbook** (modeled on Mini Jan, "Joe Blow" placeholder params) plus agent-first handshake/handover docs. Cadence: weekly, **initially twice-weekly**.

  > ⚠️ Lars's "tangible wins within a month" condition is the seed of the March 28 value crisis — it was stated up front and the first month under-delivered against it.

- **2026-03-05 (direction + meeting)** — Ansible provisioning walkthrough recorded (clone repo → Claude Code reads README → audit/dry-run/provision); setup session proposed. Same day, a Loom showing a fast-built AppyStack micro app clients extend purely by prompting, plus the Mochaccino mockup skill.

  > 📌 Note the March 5 Loom: **micro-apps-by-prompting** is exactly what re-emerges as Lars's key want on July 13. The through-line of the whole thread.

- **2026-03-08 (meeting)** — Full Ansible + Claude Code setup on FliDeck Core, end to end. Two acknowledged debts: the client-template playbook **still leaks David's own defaults**, and giving Lars repo write access is **a stopgap**.
- **2026-03-11 (meeting)** — Long tutoring session: two labs bootstrapped (public jq-based jump-system repo; appydave-brain starter with three brains + distilled Lisa librarian via `npx degit`), then operations.md provenance-chain design and Mochaccino schema gap-analysis rules.

Then a **17-day capture gap** (Mar 12–27) — the first lull, and in hindsight the period where value perception eroded.

## Phase 4 — Value crisis and cadence reset (2026-03-28 → 2026-03-31)

- **2026-03-28 (direction)** — **The crisis record.** Lars is questioning his $5K/month spend after a first month with **no tangible outcome** (exactly the risk he flagged Mar 3). David responds with a delivery roadmap: AngelEye wave-based agent-workflow visualization built over the weekend, app auto-update, drip-fed education via an automated blog, and teaching Lars to build custom agent teams with the BMAD Module Builder.
- **2026-03-31 (6 records — the recovery flurry)**:
  - (meeting) Cadence reset: **daily 30-min skill-building sessions** (~14:00 David's time, starting next day) with a shared **relay-lars Dropbox folder** as shared memory. Key learning shared: *share the brain, not the account* — Claude accounts must not be shared across computers. Mythos beta access (approved, not yet granted) floated as a wow card.

    > ⚠️ **Superseded**: weekly (Jan 31) → twice-weekly (Mar 3) → **daily** (Mar 31). Each cadence decision replaced the last as value pressure mounted.

  - (direction ×3 + question) Monthly plan + onboarding presentation: infra solid first (Ansible/Tailscale/SyncThing/Dropbox), BMAD agent building for growth hacking, later AWB + AngelEye + Paperclip. An over-complex visualization is **scrapped for simple Agentic OS slides** (~8 slides: horizontal/vertical stacks + four dev sections). Open question: NotebookLM export path + prompt design for the deck. A wow-factor tease of the two-week exclusive Anthropic (Mythos) access is to be woven in — though David is puzzled the access token never appeared. Separately: full Claude removal instructions requested to reinstall under a new account (the operational tail of "share the brain, not the account").

## Phase 5 — Agentic comms go live, then dormancy (2026-04-01 → 2026-04-02)

- **2026-04-01 (meeting)** — Dropbox external relay (`relay/people/david-lars`) with prompt-injected onboarding docs; appydave-plugins installed on Lars's machine. **Two-way agentic communication loop closed** — the engagement's clearest tangible-infrastructure win.
- **2026-04-01 (feedback)** — Honest gap audit: unverified Tailscale/Ansible, no Dropbox knowledge-sharing pattern between agents, an unfinished promised document, a push dashboard showing zero despite many incidents, failures without meaningful errors. New mandate: every agent lists its future agents at least once per session.
- **2026-04-02 (meeting + idea + decision ×2)** — OMI ingestion working session: quick-brown-fox capture verified, plugin version drift found (2.3.0 vs 2.4.4), Gemini bad-JSON failures observed, live-session archiving confirmed, **first successful two-way external agent communication celebrated**. A file-based instruction loop is designed (David writes instructions; Lars's agent polls every minute; JSONL/CSV/markdown with check-off metadata). Hardening decisions: OMI script heals gracefully when `brains_index.json` is missing on Lars's machine, 1-2 Gemini retries, script lives in shared memory short-term (repo long-term), and the unneeded `claude -p` post-processing step is **kept as a commented section** rather than deleted.

**Then: silence.** No captures from 2026-04-03 to 2026-07-12 — roughly **3.5 months dormant**. Notably, the daily-session cadence agreed Mar 31 leaves no capture trail at all; either the sessions stopped being logged or stopped happening. The original 3-month engagement window (Mar–May) expires inside this gap with no recorded close-out, retro, or renewal decision.

## Phase 6 — Re-emergence (2026-07-13)

**2026-07-13 (meeting)** — Plan for a Lars call: cover **KyberAgent, the KyberAgent brain, and the Kyber Extension SDK**, with a 2-3 minute **Captain's Log demo**. Lars's key want: **on-demand micro-application tools that plug into KyberAgent for himself**.

The re-emergence rhymes with March 5: micro-apps Lars can spin up for himself was the most resonant demo then, and it's the stated want now — but the substrate has shifted from AppyStack/OpenClaw-era framing to the **Kybernesis stack** (KyberAgent + Extension SDK).

---

## Superseded decisions (rollup)

| Decision | Made | Superseded by |
|---|---|---|
| Weekly check-ins | 2026-01-31 | Twice-weekly (Mar 3), then daily 30-min sessions (Mar 31) |
| M2 repurposed as ClaudeBot/OpenClaw machine | 2026-01-31 | M4 Pro screen death forced M4 Mini-as-primary migration (Feb 28); OpenClaw framing dropped from engagement |
| OpenClaw as the reference agent runtime for Lars | 2026-01-31 | KyberAgent + Kyber Extension SDK (Jul 13) |
| Lars repo write access | 2026-03-08 | Flagged as stopgap at creation; relay-lars Dropbox shared memory became the sharing channel (Mar 31 – Apr 1) |
| Over-complex agentic-OS visualization | pre-2026-03-31 | Scrapped for simple ~8-slide deck (Mar 31) |
| `claude -p` post-processing in OMI script | pre-2026-04-02 | Deemed unneeded; retained only as commented section (Apr 2) |
| Original 3-month term (Mar–May) | 2026-01-31 | Lapsed uncelebrated inside the Apr–Jul dormancy; no recorded renewal or close-out |

## Current status (as of 2026-07-13)

**Re-emerging after ~3.5 months dormant.** The relationship survived the March value crisis and produced real infrastructure (two-way agent relay, OMI pipeline on Lars's machine, provisioned FliDeck Core), but the formal engagement's end state was never captured. Today's call reframes the relationship around the Kybernesis stack — KyberAgent, its brain, the Extension SDK, and a Captain's Log demo — anchored on Lars's persistent want: self-serve micro-apps. Open threads carried forward: the Apr 1 gap audit (unverified Tailscale/Ansible, unfinished document, broken push dashboard) was never recorded as resolved, and the commercial basis (is $5k/month still live? renewal? new scope?) is undefined in the record.

---

*Source: 24 Captain's Log records, thread `client-lars`, full-run 2026-07-13.*
