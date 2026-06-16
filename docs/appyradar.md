# AppyRadar — the machine & fleet sensor

**Status**: 2026-06-10 — the corrected, durable definition. Supersedes every "AppyCtrl" reference in the older docs (that was a wrong application name; see the correction below). Pairs with `dark-factory-constellation.md`.

> **⚠️ Read this first — the AppyCtrl correction.** Across the older backlog/spec docs, the process/resource/liveness observer is called **AppyCtrl**, and is described as "the thing that kills dead processes." **That was wrong on both counts.** There is no app called AppyCtrl in this role. The real application — the one that *understands the nature of this machine and the other machines on the network, and exposes their memory/process data through a Sentinel + MCP* — is **AppyRadar**, and it is **read-only** (it never kills). Wherever an older doc says "AppyCtrl," read "AppyRadar," and discard any "it reaps/kills" role (killing belongs to Marshall — see §4).

---

## 1. What AppyRadar is

**A read-only fleet intelligence sensor** — a single-screen view of health, resource pressure, AI activity, and maintenance debt across the 5-Mac network, so you don't have to SSH into each machine to triage the morning.

Its job is to **observe machines and make what it sees queryable** — nothing more. It reads; it never mutates the systems it observes.

---

## 2. What it observes (and exposes)

- **Machine health** — up/down/reachable per host.
- **Resource pressure** — RAM, CPU, process tables (`ps`-level), disk.
- **AI activity** — what's running on each box.
- **Maintenance debt** — the accumulating-cruft signals (e.g. untracked/uncommitted git state, stale worktrees) you'd otherwise only find by SSHing in.
- **Process / tmux observation** — the read side of "what's actually running where."

It exposes this via a **read-only MCP surface** (one summary tool, one detail tool, domain-specific aggregated tools; `trigger_collect` is acceptable because it only spawns a collection subprocess and returns — it does not mutate the observed system; data-age is first-class on every response).

---

## 3. Substrate, status, and where the real code lives

- **Substrate:** AppySentinel (it is **Pilot 1** of the AppySentinel scaffold). Same family as Switchboard — a headless, always-on, observer-only per-machine Sentinel. Collect → snapshot-store → Access(MCP/HTTP/CLI).
- **PoC-validated:** 2026-04-27. Working `orchestrator-ssh` recipe (SSH from one machine to a fleet of remote hosts, no remote agent install; compound bash scripts per connection; emits `machine.snapshot` state + `machine.offline` event per machine) and a working read-only MCP server.
- **The real AppyRadar today:** the AppySentinel-substrate rebuild **`appyradar-sentinel`** is **live** (`~/dev/ad/apps/appyradar-sentinel/`, proven 2026-06-11). The original Bun/TypeScript SSH fleet collector (`scripts/audit.ts`) now lives only in the archived bespoke `_archived--appyradar/`; the earlier typo'd `appyradar-sentinal` PoC is archived as `_archived--appyradar-sentinal`. PoC sources (`ssh/client.ts`, `collectors/*`, `expose/mcp.ts`) were referenced by Switchboard's `configure-sentinel` skill.
- **⚠️ Not a Baku app.** `~/dev/baku/b-appy-radar` is **only a UI mock** built from an AppyRadar snapshot. None of the real AppyRadar belongs to Baku.

---

## 4. The boundary rule — sensors read, control acts elsewhere

This is the principle that keeps AppyRadar's identity clean (David, 2026-06-10):

- **AngelEye** owns reading Claude Code sessions + absorbing Claude Code hooks, and making that data **queryable**.
- **AppyRadar** owns reading machine / process / tmux / machine observations, and making that data **queryable**.
- **Communication and control** generally live in **Switchboard**, **Watchtower**, or **the agents on the factory floor** — *not* in the sensors.
- A sensor *may* host an action if it genuinely belongs there — but anything that **does** something (e.g. kills a process, deletes a file) should go **through a proper control program** (Switchboard / Watchtower / a floor agent), which may *call* AppyRadar or AngelEye if it makes sense for the action to live near the data.

So: **AppyRadar emits observations and answers queries (including detection events like `machine.offline` or an `orphan_detected` signal). It does not act on them.** The reaper's actual kill is Marshall's; the routing/coordination is Switchboard's; the human surface is Watchtower's.

---

## 5. Place in the constellation

AppyRadar is the **machine/process/fleet sensor** in the constellation — the read-only counterpart to AngelEye (the session sensor). Together they are the two queryable sources of truth about "what's alive / under pressure / stuck"; Switchboard carries the messages and state; Watchtower shows it; Marshall (on the floor) is the only thing that acts/kills.

Two consequences for the rest of the system:
1. **Switchboard's accreted process-polling belongs here.** Switchboard's `poll-command`/`process.snapshot`/`snapshot-store` slice (it polls `ps -Ao …pcpu,pmem,etime`, tmux, `pgrep claude`) is AppyRadar's domain, sitting in Switchboard by accretion. It should migrate to AppyRadar — or Switchboard hosts it only until AppyRadar's Sentinel rebuild lands.
2. **The reaper's stuck-case signal is AppyRadar/AngelEye territory — ownership TBD.** Whether the stuck-Swagger liveness signal comes from AngelEye (session last-active), AppyRadar (process/tmux state), or both, is an **open design decision** (deferred). What's settled: the *signal* is a sensor's; the *kill* is Marshall's. (Process-tree detection was already proven a dead end — claude reparents to its daemon.)

---

## 6. Open questions

- **Reaper stuck-case ownership** — AngelEye vs AppyRadar vs both (see §5.2). Deferred.
- **Migration of Switchboard's process-polling** — when and how the `poll-command` slice moves to AppyRadar.
- **Per-machine vs orchestrator topology** — the PoC is orchestrator-SSH (one box reaches the fleet). Does each machine also run a local AppyRadar, or is the SSH-orchestrator model the whole story?
- **Maintenance-debt scope** — how far the "untracked-file / stale-worktree rot" detection goes (it was one of the capabilities the old "AppyCtrl" notes gestured at).
