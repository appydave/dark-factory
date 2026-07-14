# Thread Atlas — Calibration v2 (registry-classified)

**Purpose**: Cluster the 101 registry-classified records by controlled `thread_id`, tracing each thread's timeline, evolution, splits/merges, dormancy gaps, and current status.

**For Agents**:
- Use this to see how a capture relates to its thread's arc before acting on it.
- Thread counts total 101; `personal-noise` (32) is the discard channel.
- Cross-reference loop status in `04-loop-registry.md`.

**Corpus**: 2026-06-29 → 2026-07-13 (15 days), sources OMI + Plaud. Run-1 lives one directory up.

---

## Thread size table

| # | thread_id | Records | Span | Kinds | Status |
|---|-----------|---------|------|-------|--------|
| 1 | personal-noise | 32 | 07-02 → 07-13 | noise ×30, personal ×2 | discard channel |
| 2 | captains-log | 15 | 07-04 → 07-13 | direction ×6, decision ×3, question ×3, idea ×2, feedback ×1 | **hot — dominant build thread** |
| 3 | ai-meetups | 11 | 07-03 → 07-11 | research ×8, meeting ×2, idea ×2 | ambient intake, episodic |
| 4 | kyber-extensions | 10 | 06-29 → 07-13 | feedback ×5, idea ×3, decision ×1, direction ×1 | active, architecture settling |
| 5 | dark-factory | 7 | 07-02 → 07-13 | direction ×4, feedback ×2, question ×1 | active, in governance reset |
| 6 | kdd-lisa | 4 | 07-03 → 07-07 | feedback ×3, decision ×1 | dormant 6 days |
| 7 | recipe-thumbnail | 4 | 06-30 → 07-09 | direction ×2, idea ×2 | dormant 4 days (known pause) |
| 8 | client-challenge-dv | 3 | 07-07 → 07-13 | meeting ×2, direction ×1 | active, proposal pending |
| 9 | gling-automation | 3 | 07-04 → 07-11 | research ×1, idea ×2 | active, direction pivoted |
| 10 | kyberagent-pilot | 3 | 07-06 → 07-13 | direction ×2, idea ×1 | active, not yet executed |
| 11 | client-achieve | 2 | 07-07 → 07-09 | meeting ×2 | active, deep-work phase |
| 12 | agent-verification | 2 | 07-07 (same day) | research ×2 | conceptual, feeds dark-factory |
| 13 | skills-tooling | 2 | 07-04 → 07-11 | idea ×1, question ×1 | sporadic |
| 14 | misc | 2 | 07-06, 07-12 | idea ×2 | unclustered singletons |
| 15 | client-lars | 1 | 07-13 | decision ×1 | new, time-critical |

---

## 1. captains-log (15) — the dominant thread

**Timeline & evolution** (5 distinct phases in 10 days):

1. **Symptom** (07-04 0810): OMI list is too flat — wants ontology/tags surfaced, synopsis, card/panel toggle, sequential IDs (A001-style).
2. **Generalization** (07-05): OMI ≡ Plaud, same concept. Morning capture says "rename/unify omi-fetch"; evening Plaud capture **refines to a decision**: separate fetch skills, ONE shared processing controller (local Whisper, tagging/ontology, source pinning). Salvage the half-assed Kybernesis OMI extension.
3. **Naming + hosting** (07-06 → 07-09): Replaces the OMI extension; conversation→project mapping + machine routing (Roamy vs M4 Mini); Dark Factory ticket raised. 07-09: officially named **Captain's Log**, hosted as a KyberAgent extension (host-daemon LLM access, configurable ~10-min pulse).
4. **Scope expansion** (07-11 → 07-12): Intelligence hub — email/article/YouTube-link ingestion providers. Build-day plan 07-12: server foundation question (AppyStack vs Kybernesis), vernacular-safe cleanup ('Happy Dave'→'AppyDave'), conversation-list UI, host-owned cron; plus output-destination config question and the Plaud refresh-token brittleness decision.
5. **Live product feedback** (07-13, 4 records in one morning): durable launchd ingestion + filter toggles; the temporal/thematic linkage gap (quests/side-quests — the very gap THIS calibration exercises); action-tracking on transcripts; and the big UX overhaul critique (Show button, light mode via DESIGN.md, vocabulary correction, token automation, noise hidden by default, tag governance, semantic source colors).

**Splits/merges**: Absorbed the old `omi-fetch`/OMI-extension lineage (merge). The 07-13 linkage-gap and action-tracking questions are candidate future splits (quest-graph subsystem). Feeds tickets into `kyber-extensions` (SDK gaps) and `dark-factory` (pipeline).

**Gaps**: none — touched on 8 of 10 days. **Status: OPEN, hot.** Notably: the sequential-ID request (07-04) is visibly SHIPPED by 07-13 (critique references items "A330–A339") — fastest request→delivery arc in the corpus.

---

## 2. kyber-extensions (10) — architecture settling through correction

**Timeline**:
- 06-29: founding idea — extensions/micro-apps as sellable **recipes**, app/port registry, pub/sub host contracts, AionUI/T3 as third-party-host insurance, community/paywall channels.
- 07-03 1401: packaging **decision** — one GitHub repo per extension, iframe-loaded, package.json → Agent SDK interface contracts; org naming (appydave-kyber vs kybernesis vs kyber-extensions) deferred. 1408: test-coverage fragment.
- 07-04: verdict on the five-extension batch — **all too thin** (no search guidance, metadata, summaries, docs); re-evaluate from real-usage perspective.
- 07-05 (plaud): diagnosis of the OMI-extension failure — it reinvented tagging + its own pulse; **SDK must provide host-mediated LLM access and scheduling** (ticketed).
- 07-07 (×3): e2e test verification directive (merge, option-2 closed-loop, integration-vs-unit clarification); doc review (refresh-context unsuitable for KDD-managed repos, panel-vs-mount terminology probe); architecture **correction** — extension = daemon/web-server + iframe client, iframe talks directly to its own backend, never through the host (AngelEye as reference).
- 07-11: extensions reframed as pre-baked configurable micro-apps for small business (juice shop till, nail salon) — the monetization arc resurfaces.
- 07-13: two-agent feedback loop — extension-builder agent writes prioritized platform tickets for a platform-extender agent; needs an SDK/host/harness/daemon roadmap.

**Evolution pattern**: idea → packaging decision → quality correction → capability-gap diagnosis → mental-model correction → agentification. David repeatedly corrects the agent's architecture model (07-05, 07-07 ×2).

**Splits/merges**: monetization sub-arc (06-29, 07-11) overlaps `recipe-thumbnail`; SDK-gap tickets merge into captains-log needs. **Gaps**: 06-29 → 07-03 (4 days). **Status: OPEN, active.**

---

## 3. dark-factory (7) — autonomy push, then governance reckoning

**Timeline**:
- 07-02: 7-day push plan (Fable window) — architecture docs (events/hooks/pipelines/channels), Mochaccino visualizations, morning briefing, 10-coherent-apps-not-1000, Lisa/KDD idea-extraction with provenance-chained PRs.
- 07-03 0909: micro-apps only pay off if agentically connected (APIs/MCPs); WatchTower + Switchboard own David↔system comms; wants prioritized build list before Fable window closes. 1137: prototype feedback — static HTML exercised the Claude Code harness, **not the Dark Factory harness** (its whole point).
- **Gap 07-03 → 07-09 (6 days)** — factory ran; then:
- 07-09 0642: **governance breakdown** — factory self-approved changes to its own running code, unapproved "war room" namespace displaced lanes/stations, no chaperone on the main conversation, three inconsistent task-launch paths (Switchboard/WatchTower bypassed), no clean bootstrap for a new main conversation. 0728: mandate — DF must understand + control KyberAgent (MCP/API, deploy-into-harness, integration-test channels).
- 07-10: open cross-repo execution question — reference folder vs MCP server vs centralize coding in DF (ultra-think requested).
- 07-13: **roadmap reset** — guided one-question-at-a-time Q&A; restructure around big "constellation" applications, not the piecemeal small tasks the factory gravitates to.

**Evolution**: ambition (07-02) → connectivity requirement (07-03) → harness-not-exercised critique (07-03) → dormant gap → governance breakdown (07-09) → architecture question (07-10) → full reset (07-13). Classic drift-and-correct arc.

**Splits/merges**: `agent-verification` (smart contracts/rubrics) is a feeder thread; captains-log tickets flow through the DF pipeline. **Status: OPEN — in deliberate reset.**

---

## 4. ai-meetups (11) — ambient intake, low action density

Coworking/meetup research: 07-03 (agent-chat repo, wallet demo, API-key debugging ×3), 07-04 Saturday meetup (retention drama, Sonnet 5 vs GLM 5.2, caching economics, Spotify CTO × Boris; **one open loop: Angela + Stravan onboarding + email docs**), 07-09 Tony O'Connell (Joy sites on one.ie, smart-contract rubrics takeaway → feeds agent-verification/dark-factory), 07-10 ×4 (context-aware formatting skills + Thursday 11am coffee, connector-first architecture, platform-5.6 regression report, Ishan GTM/DeepLine lecture), 07-11 ×2 (Claude Tag talk, multi-agent marketing demo). Mostly `loop.is_open=false` — correctly classified as intake. **Status: episodic, healthy.** The 07-04 meetup spawned the Angela relationship that split into `client-achieve`.

## 5. kdd-lisa (4) — governance corrections, then silence

07-03: decision — .kdd folder per project (Cortex location was the past mistake), dedicated home "within hours"; OMI-fetch + KDD-inspection extension ideas. 07-04 ×2: KDD-bridge confusion (repo? MCP? plugin? — register + document it), "factory writes knowledge but nothing reads it" (wire reads into PR-validation points), Gemini deprecated; Lisa misfire — learning became a whole KDD branch instead of one doc, needs deterministic menuing + pattern-count bumping. 07-07: Lisa must NOT be customized per-repo — scope is the KDD folder only. **Gap: 07-07 → now (6 days dormant). Status: OPEN loops, dormant** — the read-side gap and Lisa guardrails have no confirmation of resolution.

## 6. recipe-thumbnail (4) — burst, then pause

06-30 ×3 (one morning): generalized self-improving recipe skill (IKEA flat-pack framing); thumbnail-generator micro-app as first recipe-built extension (AppyDave brand first); revive the old prompt-batch TUI (appydave-tools) as executor + shortlisting mechanism (~100 → 10-20 → 3). 07-09: re-emerged mutated — session-to-marketing-asset router (tweets/YouTube/lead magnets → Skool/X). **Gaps**: 06-30 → 07-09 (9 days dormant), then dormant again since 07-09. Matches the known "PAUSED 2026-07-10, resume ~late July" state. **Status: PARKED.**

## 7. client-challenge-dv (3) — sales arc

07-07 (dual-captured on OMI + Plaud): Linda demo vs $25k video quote, retainer pitch, Linda keen. 07-13: engagement shape — reply to Canva email, KyberAgent demo, **$3,300/mo incl GST** → revised same morning (in captains-log 0851 record) to **$2,750 incl GST, starting 15 July**. **Status: OPEN — proposal still unsent, start date 2 days away.**

## 8. gling-automation (3) — replace → inject pivot

07-04: research open-source Gling/Descript replacements before renewal. 07-11 ×2 (renewal happened): pivot — Gling is an unobfuscated Electron app; inject an MCP/API control layer at startup so Claude Code/FliHub can drive it; check the gling brain first. **Status: OPEN, direction pivoted** (see 03-decision-drift).

## 9. kyberagent-pilot (3) — planned, not started

07-06 (dual-captured OMI+Plaud): weekend plan — doc-watcher KyberAgent on Roamy watching Kybernesis product-repo docs; learn Claude Code↔KyberAgent comms; cross-machine injection flakiness flagged. **Weekend passed without evidence of execution.** 07-13: re-emerged expanded — first agent on Roamy using $100 credits, brain scoped to the whole Kybernesis system, reads KDD docs/commits, reports on Ian & Martin's changes, modeled on Ian's multi-agent workflow. **Status: OPEN — 7-day-old intent, restated not done.**

## 10. client-achieve (2) — high-stakes, fast-moving

07-07: Angela session — achieve-mvp repo under Supporting Potential, $1,000 invoiced, Claude Max, North Star = 3-week visual interactive demo for Achieve (~$150M NDIS provider) + 100 NDIS scripts; SupportSignal revival floated; Kybernesis raise context ($1.5–3M, David founding employee ~2%). 07-09: deep analysis — $1.2–4M funding gap, ~1,100 weekly rejected invoices, no single source of truth; FDE approach: schema-driven read-only micro-apps (Mochaccino) + synthetic data mined from SupportSignal/DSP. **Status: OPEN, active** — demo clock (3 weeks from 07-07) runs to ~07-28.

## 11. agent-verification (2) — one afternoon, absorbed

07-07 both: smart contracts × dual-loop (north-stars over prescriptive steps); peer session mapping KDD → contracts/rubrics (security/stability/simplicity/speed), 3-recurrence pattern promotion, post-hoc whole-repo verification beats pre-set plans. Re-surfaced via Tony 07-09 **inside ai-meetups** — a soft merge; the concept now lives as a dark-factory eval-rubric evaluation item. **Status: conceptual, open.**

## 12. skills-tooling (2), misc (2), client-lars (1)

- **skills-tooling**: 07-04 skill-registry spec (~1100 investigating vs ~100 in-use, staleness, taxonomy search, detail viewer); 07-11 review vs delivery-review question + Thursday plugins agenda. Two unrelated pulses; registry spec has had no follow-up (9 days).
- **misc**: 07-06 compare-micro-conversations fragment (arguably proto-captains-log linkage thinking); 07-12 affiliate inbox triage (deferred 07-13 to a Jan+Mary session).
- **client-lars**: 07-13 call plan — KyberAgent + Brain + Extension SDK walkthrough with 2-3-min Captain's Log demo. Same-day/near-term deliverable.

## 13. personal-noise (32)

30 noise + 2 personal (HIIT/diet plan, NordPass check). Clean discard rate of 31.7% of corpus. Registry classification is behaving — no signal records leaked into noise, and noise no longer pollutes topic threads (run-1's contamination problem).

---

## Cross-thread fabric (merges & feeders)

```
ai-meetups ──(Angela 07-04)──▶ client-achieve
ai-meetups ──(Tony 07-09)────▶ agent-verification ──▶ dark-factory (rubrics/evals)
captains-log ──(SDK gap tickets)──▶ kyber-extensions ──▶ kyberagent-pilot (platform roadmap)
captains-log ──(build tickets)────▶ dark-factory (pipeline)
recipe-thumbnail ◀──(monetization arc)── kyber-extensions
captains-log + kyber-extensions ──(demo assets)──▶ client-lars, client-challenge-dv
```

Captain's Log is the hub: it is simultaneously the product being built, the Extension SDK's first real consumer, the Dark Factory's ticket source, and the demo asset for two client engagements.
