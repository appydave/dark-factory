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
