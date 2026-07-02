# Dark Factory — Constellation Map (the data + observability architecture)

**Status**: 2026-06-25 — canonical. The single map of every app in the dark factory's orbit, sorted into the layer it belongs to and tagged with David's verdict. Supersedes the surface-only [`observability-surface-audit.md`](~/dev/ad/brains/dark-factory/observability-surface-audit.md) (that was a live-state snapshot of 7 *surfaces*; this is the whole stack — sources, data-plane, surfaces, host).

**Why this exists**: The morning-briefing idea (see [`daily-operating-model.md`](./daily-operating-model.md)) was backwards — it sits at the *top* of a stack whose lower layers don't exist yet. David's objection, unpacked: *"I can't trust a briefing when I can't SEE anything and don't know what apps/data exist."* The real question was never "build a briefing" — it was **"what is the data-and-observability architecture around the dark factory, and what must I build so I can actually SEE and TRUST it — landing in KyberAgent (KBDE) as the harness?"** This doc answers the first half (what exists, sorted); the build order follows from it.

**Provenance**: app-inventory audit (2026-06-25, both-registries + filesystem sweep, M4-local only) → David's live pruning pass (session, 2026-06-25). Verdicts below are David's words, not inferred.

---

## The model: it's a stack, not a list

```
┌─ HOST / HARNESS ─────────────────────────────────────────────┐
│  KBDE / KyberAgent  ← where every surface mounts as an        │
│  extension (typed channels: Data / Brain / Composer / Chat /  │
│  Events / Host-context / Host-command / planned Write).       │
│  This is the answer to "where do I SEE it."                   │
└──────────────────────────────────────────────────────────────┘
        ▲ surfaces mount as extensions across the seam
┌─ SURFACES  (a slice of data + a way to see it) ──────────────┐
│  → candidates to (re)build as KBDE extensions                 │
└──────────────────────────────────────────────────────────────┘
        ▲ surfaces visualize a slice of data
┌─ DATA LAYER  (the "great data cluster" around dark-factory) ─┐
│  SOURCES → DATA-PLANE (sentinels/MCP/feeds) → made available  │
│  as data artifacts that surfaces + agents consume             │
└──────────────────────────────────────────────────────────────┘
```

**The realization that anchors the whole map** (David, 2026-06-25): the registry/inventory files themselves — *what apps exist, do they run, what data do they host* — "are actually something that need to be made available as **data artefacts** to different applications." The inventory is not an app; **it is the first data source in the bottom layer.** The briefing's "where's the latest project / what's its state" feed is a *consumer* of that source. That's why building the briefing first felt wrong.

---

## Layer 1 — DATA (sources · data-plane · boilerplate)

### Sources — produce data the factory needs
| App / artifact | Path | What it produces | Status |
|---|---|---|---|
| **The inventory / registries** | `~/.config/appydave/{locations,apps}.json` · `brains/.../dev-inventory/` | "What apps exist, do they run, what data they host" — the first feed | exists, **stale & incomplete** (Kybernesis + several off-registry) |
| **OMI Ingester** | apps/omi | Wearable transcript pipeline → great data for brains | dark (pipeline) · **also a surface, see L2** |
| **Cortex** | kybernesis/Cortex | Knowledge-graph / second-brain store *for agents* — where brain-related stuff lives | active (06-23) · *not* a build target; keep listed as the brain store |
| Per-project git / mission state | each repo | "Where are we up to" — commits, tickets, `mission.md` | durable, read-on-demand |

### Data-plane — make data available / queryable (sentinels · MCP · feeds)
| Component | Path | Role | Status / verdict |
|---|---|---|---|
| **Blackboard MCP** | (spike) | Shared K/V so **dynamic workflows share data** with each other | **RUNNING** · important data pattern for dark-factory |
| **appyradar-sentinel** (NEW 'e') | apps/appyradar-sentinel | Fleet collector — forward path | dark, 2 commits · **the keep** |
| appyradar-sentinal (OLD 'a') | (off-registry) | Same role, the version *currently running* (9 MCP tools) | RUNNING · legacy; migrate to 'e' |
| **Switchboard** | (off-registry) | Headless data plane (SSE + MCP) — process/session snapshots | dark · data-plane candidate |
| supportsignal-sentinal | (off-registry) | SS per-machine sentinel | dark · SS world |

### Boilerplate — how we scaffold more of the above (NOT build targets)
| Boilerplate | Path | Used for |
|---|---|---|
| **AppySentinel** | apps/appysentinel | Observer-only sentinel scaffold — used a lot |
| **AppyStack** | apps/appystack | RVETS app scaffold — used a lot |

---

## Layer 2 — SURFACES (→ KBDE extension candidates)

A surface = a slice of data + a way to visualise it (list / search / detail-card / graphic / dashboard). Which one you reach for is chosen by *data type*. All of these are candidates to (re)build as KBDE extensions.

### Core data surfaces — the cluster that delivers data into the dark factory
| Surface | Path | Visualizes | Status | KBDE |
|---|---|---|---|---|
| **AngelEye** | apps/angeleye | Session / agent observability | **UP :5050** | ★ strong |
| **AppyRadar** | apps/appyradar | Fleet telemetry (machines / disk / processes) | dark | ★ strong |
| **Watchtower** (app) | apps/watchtower | "Glass wall" — HOTL decision queue | **stub (1 commit)** | ★ strong (greenfield) |
| **Watchtower-engine / -board** | (exp) | DF job queue + board (:7430) | dark | app we should use |

### Utility micro-apps — "beautiful utilities," not the data cluster, but all convertible to KBDE extensions
| App | Path | What | Verdict |
|---|---|---|---|
| **DeckHand** | apps/deckhand | Stream Deck / workspace control | keep · extension candidate |
| **ScreenTour** | apps/screentour | Screenshot / TUI capture walkthroughs | keep · extension candidate |
| **ThumbRack** | apps/thumbrack | Thumbnail tooling | interesting, keep |
| **Media Studio** | tools/media-studio | AI image/video workspace gallery | potential extension |
| **OMI Ingester** | apps/omi | (also L1 source) — cool app idea, definite extension | **definite KBDE extension** |

### Prototyping surface — where surfaces get mocked before they're built
| Tool | Path | Role |
|---|---|---|
| **Mochaccino / Mocha-Census** | apps/dark-factory/mochaccino · tools/mocha-census | UI/UX mockups (:7420) + rate-and-label board (:7440). **Where POCs + visual documentation live** — prototype a KBDE extension surface here first. |

---

## Layer 3 — HOST / HARNESS

| App | Path | Role | Status |
|---|---|---|---|
| **KBDE / KyberAgent-Enterprise** | kybernesis/KBDE-KyberAgent-Enterprise | **The host.** Electron app + daemon + Extension SDK seam; surfaces mount as sandboxed extensions across typed channels. The answer to "where do I see it." | **active (06-24)** |

> **Extension SDK seam** (host ↔ extension): typed channels — ③ Data, ② Brain (`brain.read`-gated), ① Composer (slash-commands), ② Chat, ④ Events, A1 Host-context, A1 Host-command, planned ✎ Write. Principles: host ≠ extension; brain is host-owned core; gates track ownership; `contributionIds` = `<channel>.<owner>.<name>`. Authoritative rules: `kybernesis/KBDE-KyberAgent-Enterprise/.claude/skills/extension-sdk/references/capability-model.md` (committed). Plain-language: `.../context/extension-sdk-semantic-meaning.md` (⚠ gitignored, this-machine-only). Taxonomy is **under active review** — working model, not gospel.

---

## Engine (existing machinery — feeds/uses the layers)
AWB **Gen 3** ⭐ (apps/awb, `jawb`) — primary interest · **Gen 2** (clients/supportsignal/prompt.supportsignal.com.au) · **Gen 1** (/agent-workflow-builder, `jwb`, archived) — all three listed deliberately · **POEM OS** (keep) · **appydave-tools** (keep).

## Business tools — own world, NOT the data cluster (maybe-someday extensions)
FliVideo suite (FliHub, FliDeck, Storyline, FliGen, FliBrief, FliVoice, FliLaunch) — "just tools for my business, nothing more." · SupportSignal suite (signal-studio, app, prompt=AWB Gen2, brain, v2-planning, email, www, **DSP**).

## Its own world (not a constellation component)
**ARP** (kybernesis/arp) = **Agent Relationship Protocol** — the agent-to-agent trust/identity/permissioning *protocol* + runtime (sovereign DIDs, per-purpose Connection Tokens, Cedar policy + consent, DIDComm transport, tamper-evident audit). Large monorepo (8 apps / 22 pkgs), hosted at arp.run. **Active/mature but paused** (159 commits, last May 3 2026). **ARP-mobile** = iOS/Android owner/consent control app (Expo RN, early spike, 3 commits). **Classification: NEITHER** — ARP is the *rails agents run on*, not a surface or a data-plane feed. It's the Kybernesis agent-trust layer (KyberBot/KyberAgent consume it). *One thread to keep:* ARP's tamper-evident audit log is a plausible future **data source** a constellation could consume — unverified whether it exposes an MCP/queryable feed.

## Parked / not yet scoped
Arcana · Atlas · Mythos — unknown, parked. · KyberBot / KyberBot-desktop / KyberAgent-desktop / Cortex-AppyDave / Kybernesis-brain / Kybernesis-CLI — Kybernesis satellites, not yet scoped.

## Dropped / dead
**AppyCtrl** (apps/appyctrl) — DEAD. Was the old "GUI to hold coding-agent surfaces"; **superseded by KBDE.** · **Digital Stage Summit** (apps/digital-stage-summit-2026) — not needed.

---

## Build constraints (how the bricks get built — David, 2026-06-25)

Two gates that govern *any* build off this map:

1. **Dogfood — build it through the factory, not by hand.** Bricks are built via the dark factory's own loop (daily operating model: BA agent → Marshall → Swagger → build-to-spec/SPAT), not ad-hoc hand-coding. The factory builds the factory. The first data feed doubles as the **first real run of the operating loop**.
2. **The KBDE Extension SDK is a pending handover, not researchable.** How we build extensions + the SDK's design decisions don't exist in finished form yet — David delivers that knowledge; research is no substitute (the SDK isn't finished). Therefore: **any Layer-2 surface / KBDE extension is BLOCKED until that handover lands. Layer-1 work (a data source / MCP feed) is NOT blocked** — it needs no SDK. The inventory feed splits exactly on this line: the queryable data-artifact half can proceed now; its visualization/extension half waits.

## The two views of the orbit (cross-link)

This map is the **exists/structure** view. The **build-order** view is the brain roadmap:
`~/dev/ad/brains/dark-factory/app-pipeline/build-sequence-roadmap.md` (2026-06-30) — sequences the *product arc* (Day 0: map the KBDE SDK → thumbnail-builder → recipe-builder-skill → batch-prompt-runner → community-asset-builder). Its Day-0 SDK gate is the same gate as §Build constraints #2. The full candidate backlog: `~/dev/ad/brains/dark-factory/app-pipeline/README.md`.

**2026-07-02 additions** (OMI `2026-07-02-0633-david-plans-dark-factory-automation.md`): `architecture-visualizer` (UNBLOCKED — visualize THIS map via schema→data→kie.ai drawn diagrams), `idea-extraction` (Lexi upgrade), watchtower's communication triad. Also: dedicate Fable 5 to factory work; single-responsibility-but-not-tiny as the micro-app sizing rule ("10 apps in harmony beats 1000").

## The three folders (RESOLVED — David, 2026-07-02)

Sessions must distinguish these three and **build ONLY in the first**:

| # | Folder | Role | Rule |
|---|--------|------|------|
| 1 | `~/dev/ad/apps/dark-factory/` | **The main dark-factory** | The only build target |
| 2 | `~/dev/ad/apps/suborch-demo/` | **The POC** — "Subscription-Safe Multi-Session Claude Orchestration": working execution kernel (queue → isolated Claude sessions → artifact-verified reap), 100% Max-subscription (no SDK/metered), warm tmux pool, atomic CAS lease, blackboard `store/`, 10/10 tasks in 51s. Built in dark-factory sessions; synced to both machines | Reference/testing only — concepts proven here get rebuilt properly in #1 |
| 3 | `~/dev/upstream/repos/omnigent/` | **The third-party library** — Omnigent, Databricks' open-source agent harness (new, active). Used to verify the POC's concepts (suborch `experiments/` includes an Omnigent validation spike) | Read-only reference; upgrade via `git pull` upstream |

The POC's `CONTEXT.md` + `PHASE-5-PLAN.md` (switchboard cockpit + Linear bridge) carry design law that feeds back into #1 — notably the warm-pool/CAS/artifact-is-truth mechanics, which are prior art for Switchboard/Marshall.

## Fleet ground-truth (2026-07-02 cross-machine probe — closes the blind spot)

**Machine identities (observed via hostname/chip/tailscale — ends the "M4 Pro" ambiguity):**
| David-speak | Actual machine | Tailscale | Role |
|---|---|---|---|
| "M4 Mini" | Mac mini, Apple **M4** (`mac-mini-m4.local`) | `mac-mini-m4` | **The machine this repo's sessions run on.** Runs the appyradar-sentinel collector (launchd). |
| "M4 Pro" | **MacBook Pro**, Apple M4 (`MacBook-Pro-4.local`) — *Pro = form factor, no M4-Pro chip exists in the fleet* | `macbook-pro-2` | The other dev machine (Lisa/KDD work lives here). Currently runs **Switchboard :5099 UP** + Storyline :5300. |
| — | Mac mini M2 | `mac-mini-m2` | Offline at probe time; unknown state. |

**Corrections to this map's earlier claims (statuses rot — see the lesson):**
- **Switchboard is NOT dark** — it runs on the MacBook Pro (:5099/:5100). Earlier "dark" verdict was local-only vision.
- AngelEye :5050 down on both machines at probe time (was UP on 06-25). Mochaccino :7420 was down, restarted 07-02.
- **`dev-inventory/current.json` doesn't exist on EITHER reachable machine** — the registry `~/dev/ad/CLAUDE.md` points to is gone or on the offline M2. The inventory-as-data-artifact case is stronger than we knew.
- **AppyRadar Sentinel has its own blind spot**: collector runs only on the Mini and reports the MacBook Pro "offline" while it's alive and serving — the fleet dashboard can't be trusted for cross-machine liveness yet.
- Repo drift between machines is real (kybernesis core local-only; `kyberbrain` remote-only; remote has `_archived--appyradar*` while local runs them).

**The lesson (feeds architecture-visualizer):** run/dark status in a *document* is stale within days — twice now. Liveness belongs in **live data** (the constellation.json → registry/sentinel seam), with docs carrying only the structural facts.

## Open questions / next

1. **Which first data feed do we make real?** The map says start at the bottom: a real, queryable **data source** (the lean candidate is the *inventory itself* — make "what apps exist + state" a live data artifact, since it's stale, incomplete, and everything else needs it).
2. **Is "the inventory as a data artifact" an extension, a data-plane feed, or its own thing?** (David's open question — likely a data-plane source surfaced via MCP, consumed by a surface.)
3. **Cross-machine blind spot.** This map = M4-local only. The fleet is 5 Tailscale machines; `dev-inventory/current.json` and most live observability state are M4-Mini-side. The other machine needs its own scan before the map is trustworthy.
4. **Migrate the running sentinel** from `appyradar-sentinal` (old 'a') to `appyradar-sentinel` (new 'e').

## References
- Daily operating model (the briefing this map re-grounds): [`daily-operating-model.md`](./daily-operating-model.md)
- Why + life-OS + absorption law: `~/dev/ad/brains/dark-factory/using-dark-factory-vision.md`
- Prior surface-only snapshot (superseded): `~/dev/ad/brains/dark-factory/observability-surface-audit.md`
- Four sister projects: Switchboard · Watchtower · AngelEye · AppyRadar Sentinel — `~/dev/ad/brains/dark-factory/` orbit.
- Full raw audit: `scratchpad/app-inventory-audit.md` (this session).
