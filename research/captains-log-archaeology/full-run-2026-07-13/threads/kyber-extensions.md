# Thread: kyber-extensions

**Purpose**: Six-month dated narrative of the "kyber-extensions" capture thread — 40 records, 2026-06-05 → 2026-07-13.

**For Agents**:
- Use this to understand how the Kyber Extension SDK went from a coupling complaint to a settled iframe/daemon architecture with a micro-app product framing.
- Check the "Superseded decisions" section before acting on any older capture from this thread.
- Current status is at the bottom; anything dated before 2026-07-07 on architecture is likely stale.

---

## Shape of the thread at a glance

```
Jun 05  SEED        — decoupling complaint against Martin's KBDE Extension SDK
Jun 12  SPLIT-IN    — massive portable-brain / cortex spec day (memory strand, 12 records in one day)
Jun 13–19 DORMANT   — one-week gap
Jun 20  RE-EMERGE   — SDK landscape mapped after Martin conversation; SDK strand becomes dominant
Jun 23–25 AUDIT     — Scene Probe parity, channel-architecture audits, Mochaccino off real data
Jun 29  STRATEGY    — hosting, third-party hosts, monetization (recipes)
Jul 03–07 CONVERGE  — iframe + repo-per-extension decided; canonical AngelEye daemon model locked
Jul 11  MERGE-OUT   — memory strand declared DONE; extensions framed publicly as micro-apps
Jul 13  CURRENT     — two-agent feedback loop (extension-builder → platform-ticket agent)
```

The thread is really **two strands sharing one spine**: (A) the **brain/memory/portable-brain** work that dominated 2026-06-12, and (B) the **Extension SDK** work that took over from 2026-06-20. Strand A effectively closed by 2026-07-11 ("David has finished the memory layer"); strand B is the live thread.

---

## 1. How it started — 2026-06-05

In a meeting with Ian, two seeds were planted in one sitting:

- **Retrieval benchmark harness** for the brain/memory work — score quality, measure query/response time, write failure notes, find common failure modes, then a phased spec. Explicitly *no quick hacks*.
- **The founding complaint of this thread**: Martin's **KBDE Kyber Extension SDK tightly couples extensions to the Electron chat app**. David wanted a decoupled plugin/API with a **stable, backward-compatible contract**.

Everything that follows is those two seeds playing out — the benchmark seed drove the June 12 blitz; the decoupling seed drove everything from June 20 onward.

## 2. The June 12 blitz — portable brain / cortex spec day (strand A)

Twelve records in a single day. This was a spec-and-probe marathon on the memory layer, not the SDK:

- **Provenance discipline**: David directed that a **provenance chain** be kept for the cortex/brain work so the whole exercise could be reproduced when revisited "in roughly two weeks" (it was — June 20+). He also set a working rule: research first, then clarity + decision framing, *then* suggestions.
- **Spec pipeline**: Spec A (prerequisite work) was completed and closed with a handover doc + completion notes; **Spec B** (the actual database column upgrade) was to be written in a fresh conversation. **Spec C** was readied for coding handoff (Osmani-skill write-up, Linear update, paste-ready handover). **Spec D**'s scope (Arcana KAD/KBDE only?) was queried. Cross-machine repo/brain sync (M4 Pro ↔ M4 Mini, incl. Roamy's pushes) was demanded as a precondition.
- **Scoping calls**: Bedrock/Australia data residency for NDIS data flagged for independent research; a background agent tasked to explain why **KAD uses a brain provider while KBDE calls directly** ("one is wrong") — an early echo of the coupling complaint; KAD→KyberBot confirmed as *rename only, not a technology shift*.
- **Probe trouble**: missing-file count ballooned **42 → 375** between tests; David suspected data existed only in files, not in memory, and judged the release "not yet useful as delivered". Suspicious look-alike "analysis dots" in AngelEye raised the possibility of generated noise instead of real brain data.
- **Boundary violation spotted**: the file-system reconcile living *inside* the portable brain while talking to a database — David called for a background architecture deep-think and a **shared diff tool** usable by KAD, KBDE and iKANA, possibly centralized in KyberAgent core / Cortex core. Reconciliation would need a button exposed in KDB/KBDE before Portable Brain integrates (lazy-reconcile approved pending clarity).
- **Test datasets**: sub-brains swapped to agentic-os / kybernesis / agentic-factory / angeleye / prompt-patterns; David clarified his brain folder was already KBDE-ingested (embeddings exist), unlike LoCoMo/LongMem.
- **Close-out decision**: rather than choose between committing milestone C, scaling, or going deeper, David decided to **save audit data and document current metrics every run** — accumulate problem understanding even without code changes. Folder-fix work was routed to a **Cortex agent**, not a Kybernesis enterprise agent.
- Ongoing irritant: the **KBDE watch-folders regression** reappeared (possibly an undone fix).

## 3. Dormancy — Jun 13–19

One silent week. Exactly the "revisit in roughly two weeks" window the June 12 provenance decision anticipated.

## 4. Re-emergence — 2026-06-20: the SDK strand takes over

After a conversation with Martin, David mapped the **KyberAgent Extension SDK landscape** end-to-end: composer surface (dynamic slash commands, model-aware buttons) and contextual-menu surface each needing 3–4 worked use cases; a **demo surface showing real data, not schemas**; loosely-coupled **bidirectional harness/brain communication**; per-extension custom data APIs; foundational architecture (security, retries, logging, tests); and manifest-based delivery/marketplace questions. From here on, the SDK strand carries the thread.

## 5. The audit-and-mockup push — Jun 23–25

- **Jun 23** — Scene Probe declared not-done until **every SDK capability is personally checked off with iframe/in-proc parity**: rich JSON capability graph, Playwright screenshots, **Mochaccino mockups before coding**, embedded how-to docs as reference implementations, and first a preliminary spike returning questions.
- **Jun 24** (five records — the heaviest SDK day):
  - Frustration that the prior system audit **wasn't thorough** — issues only surfaced on re-work; David unsure whether two or three overlapping channel mechanisms still coexisted.
  - Direction to **consolidate sprawling audit skills** (code-quality audit, system audit, delivery review — the latter used by app.supportsignal.com.au) into a routed system-audit; split the **SDK/host boundary into packages with a real fake host (not mocks)** for proper unit tests; check whether the "David Extension SDK overhaul" branch name was still relevant. All in **long-horizon mode, not smallest-step**.
  - Finding that **channel/endpoint naming is arbitrary configuration, not deterministic convention** — demanded Rails-style convention-over-configuration and a full architecture audit of channels + data shapes across agent / extension SDK / brain / chat / host. Political boundary noted: **Agent SDK is David's purview; the host risks colliding with Ian and Martin**.
  - Two capability ideas born: **host-managed scheduled tasks** (extensions declare cron-like schedules; the host owns execution — motivated by OMI-fetch) and an **OMI watch-and-poll extension** (10-min/hourly folder monitoring replacing manual hunting).
  - **Mochaccino promotion idea**: evolve from generated HTML mockups to schema-driven data-first documentation, potentially a first-class documentation extension teaching FDEs. And a key source-of-truth ruling: Scene Probe mockups render as one usable Mochaccino extension with **the Extension SDK — not Mochaccino JSON — as the canonical capabilities source of truth**. Day plan: move Scene Probe test extensions (iframe + in-proc) from data-packed debug surface toward an almost-usable UX; remove obsolete extensions.
- **Jun 25** — work the API surface (ASP) and build Mochaccino screens around it, **every screen a direct reflection of real working code**; designs must bind to tangible programmable assets (agent pushes back when data is missing → feature spec/ticket or schema-generated mocks); the channels/hosts/extensions/permissions list reorganized (**v4 layout read better than v9**).

## 6. Strategy interlude — 2026-06-29

David thought through the wider ecosystem: pub/sub host-extension communication; an **app/port registry currently conflated with locations.json**; turning existing apps (**AngelEye, AppyRadar, FliVideo, Storyline**) into extensions; **optional third-party hosts (AionUI, Theo's T3) as decoupling insurance** — the June 5 complaint now a strategy; and a **monetization model of selling "recipes"** (core app logic + visualization surface) via community or paywall, plus an Airtable-style relational-data extension idea.

## 7. Convergence — Jul 03–07: the architecture locks

- **Jul 03** — passing thought: bake test coverage in from the start of every extension. Then the structural decision: **iframe technique for third-party extensions; one GitHub repo per extension** (future org like kyber-extensions/kybernesis); package.json pointing at the agent SDK for host interface contracts; dynamically loadable; authorization deferred.
- **Jul 04** — reality check: the **five extensions built in the batch were all too thin** — minimum viable data, no search guidance, inferred metadata, summaries, usage docs or discovery UX. Each to be re-evaluated from how **a human AND an agent** would actually use it.
- **Jul 05** — the diagnostic that validated the June 24 scheduled-tasks idea: the **Kybernesis OMI extension went wrong because it reinvented the OMI-ingest skill's tagging and rolled its own 10-minute pulse** instead of delegating to the host. Verdict: the SDK must gain **scheduled-task/cron support** and give extensions access to a **host chat conversation** so tagging runs via the host. Capability ticket to be written in KyberAgent docs or Dark Factory.
- **Jul 07** (three records — the canonical model day):
  - David articulated the **correct extension architecture using AngelEye as the model**: a separately-running web server/daemon reads the file system and serves the client page; the client renders in an iframe inside the host with socket communication; **the iframe must never talk to the backend through the host**. This was an explicit push-back on a muddled model being presented to him.
  - Doc-review on the extension repo: refresh-context/system-context docs don't suit repos that already have good docs and KDDs; three recommended changes approved; test-only screenshots removed; **panel-vs-mount terminology questioned** given extensions are deliberately host-disconnected iframes.
  - Execution: merge frame-extension changes to David's branch, run option-2 fully-closed **end-to-end tests alongside UAT**; the "~10 failing tests" claim queried (suspected integration, not unit).

## 8. Merge-out and public framing — 2026-07-11

At a meetup David articulated the settled product framing: **extensions are pre-baked micro-apps (agent + skills) living inside the KyberAgent desktop**. The archetype is **Joy's juice/nail/eyebrow-tattoo configurable POS-and-pricing catalog**, feeding websites, AI-generated promo videos (Whisper transcript + Qwen visual tagging of B-roll, auto-assembly, Thai/English), and agents. Division of labour: **Martin builds the agent communication bus; David has finished the memory layer** — strand A of this thread formally closed.

## 9. Current status — 2026-07-13

Latest idea: a **two-agent feedback loop** for the SDK — an **extension-builder agent** (fed by the KyberAgent brain agent) develops extensions through the standard SDLC, and when it hits missing host/harness/daemon capabilities it **prioritizes and files roadmap tickets for a second agent that extends the Kybernesis platform itself**. The thread has moved from complaint → audit → architecture → product framing → self-improving factory loop.

**State**: ACTIVE, converged. Architecture is settled (iframe + daemon + socket, repo-per-extension, host-owned scheduling, SDK as capabilities source of truth). Open work: SDK cron/host-chat capability ticket, extension depth re-evaluation (the five thin ones), panel-vs-mount terminology, authorization model, marketplace/manifest delivery, app/port registry vs locations.json separation, monetization (recipes) execution.

---

## Superseded decisions — do not act on these

| Superseded | By | Replacement |
|---|---|---|
| Extensions rolling their own schedulers/pulses (e.g. OMI extension's 10-min pulse) | 2026-06-24 idea, confirmed 2026-07-05 | Host-owned scheduled tasks; extensions only declare cron-like schedules |
| Mochaccino JSON as the capabilities source of truth | 2026-06-24 | **Extension SDK** is the canonical capabilities source of truth |
| Iframe extensions talking to the backend *through the host* (muddled model) | 2026-07-07 | AngelEye model: standalone daemon + socket; iframe never routes through host |
| Extensions tightly coupled to the Electron chat app (Martin's original KBDE SDK shape) | 2026-06-05 complaint → 2026-07-03/07 decisions | Decoupled iframe + repo-per-extension + stable SDK contract; third-party hosts as insurance |
| KAD→KyberBot treated as a technology shift | 2026-06-12 | Rename only |
| v9 layout of channels/hosts/extensions/permissions list | 2026-06-25 | Reorganize toward the v4 logical ordering |
| Original probe test sub-brain set | 2026-06-12 | agentic-os / kybernesis / agentic-factory / angeleye / prompt-patterns |
| Smallest-step working mode on SDK audits | 2026-06-24 | Long-horizon mode explicitly demanded |
| "Release useful as delivered" (portable brain, 375 missing files) | 2026-06-12 | Not useful then; memory layer later completed (declared done 2026-07-11) |

## Recurring failure modes worth noting

- **Shallow audits** that pass and then leak issues on re-work (2026-06-24 frustration; echoed by the "five thin extensions" on 2026-07-04).
- **Reinvention instead of delegation** — extensions duplicating skills/host capabilities (OMI extension, 2026-07-05).
- **Configuration where convention should rule** — arbitrary channel/endpoint naming (2026-06-24).
- **Boundary violations** — reconcile logic inside the portable brain (2026-06-12); iframe-through-host (2026-07-07). David consistently catches these himself and pushes back.
