# suborch → dark-factory — Conformance & Gap Analysis

**Purpose**: Measure dark-factory's **current execution code** against the patterns, laws, dead-ends, operational learnings, and capabilities proven in the sibling kernel **suborch** (`~/dev/ad/apps/suborch-demo`, 2 days of live testing, June 2026). This is a *conformance map*, not a build plan — it surfaces where DF already complies, where it gaps, and what each gap would take to close. **It deliberately does NOT decide adopt-vs-rebuild** — the gaps are the input to that decision.

**For Agents**: Read this to know exactly which suborch-proven behaviours DF satisfies today and which it doesn't, with current-state evidence (file:line) and a concrete delta per gap. Pair with suborch's build-spec (`~/dev/ad/apps/suborch-demo/CONTEXT.md`) for the canonical definition of each pattern, and `darkfactory-reconciliation.md` (in the anthropic-claude brain research-briefs) for the prior primitive-level comparison (note: that doc is 2026-06-16 and pre-dates suborch's warm pool / HITL / audit work — this doc supersedes its currency).

**Created**: 2026-06-18
**Last Updated**: 2026-06-18
**Status**: measure-only (adopt-vs-rebuild decision deferred — see §6)
**Evidence basis**: live code read of `dark-factory/` + `switchboard/` on 2026-06-18; suborch state from its current `CONTEXT.md`.

---

## 1. TL;DR — the shape of the gap

**dark-factory is conformant on the foundations.** It independently follows almost every operating law and avoids every dead-end suborch identified — the same architecture, built twice. The gaps are **concentrated in four areas, all of which suborch built and DF designed-but-didn't-build:**

1. **Warm pool** (C3) — DF cold-spawns a fresh `claude` per ticket; suborch reuses a warm pool (kills the latency floor + 429-churn).
2. **Concurrency governor** (C4 · L2 · O5) — design intent only ("~4 Swaggers max"), no enforcement code; suborch has a CAP gate.
3. **Three net-new capabilities** — native HITL gate (K1), block notification (K2), audit trail ticket→session→transcript (K3) — all MISSING; suborch proved all three.
4. **Two latent issues** — blackboard MCP registered project-level not user-level (L7), and reboot-wedged-worker self-heal deferred (O4).

Everything else (artifact-is-truth, external teardown, bounded retry, trusted-dir, all 5 dead-ends) — **DF already complies.**

**Scorecard:** MEETS 11 · PARTIAL 3 · MISSING 4 · N-A 3.

---

## 2. Conformance matrix

Verdict legend: **MEETS** (code proves it) · **PARTIAL** (some, with a named hole) · **MISSING** (not present) · **N-A** (doesn't apply given current architecture). The **Delta** column is the concrete transfer action if/when DF closes the gap.

### Layer 1 — Code / primitives

| # | Pattern | Verdict | DF current state (evidence) | Delta to close |
|---|---------|---------|------------------------------|----------------|
| C1 | Atomic CAS lease (`rename`), no double-claim | **MEETS** | `claim-next.sh:5-32` — `mv queue→running` mutex; stress-proven 200×8 | — (convergent) |
| C2 | Thin router / pointer-not-payload | **MEETS** | Marshall holds 1-line handbacks only (`marshall/SKILL.md:50-53`; `reports/*.json` = 4 fields) | — (convergent) |
| C3 | Persistent warm workers (boot-once, reuse) | **MISSING** | Cold-spawn per ticket: `tmux new-window … "claude '<instr>'"` (`dispatch-swagger.sh:19`); "one invocation = one job then returns" | Adopt suborch's `WarmPool` (`warm_pool.py`): boot-once REPL + send-keys reuse + idle-gate + reboot-on-wedge. **The biggest single gap.** |
| C4 | Concurrency governor (CAP under 429 wall) | **PARTIAL** | "~4 Swaggers" is design intent (`runtime-model.md:33`); **no enforcement code** (`marshall/SKILL.md`: "cap … not here yet, C3c/C3d") | Adopt suborch's router admission control (CAP=N gate before dispatch) |

### Layer 2 — Operating laws

| # | Law | Verdict | DF current state (evidence) | Delta |
|---|-----|---------|------------------------------|-------|
| L1 | Artifact-is-truth (never trust self-report) | **MEETS** | Reaper keys on `done/*.json` mtime (`reaper.sh:29-45`); "verify the artifact, never trust 'done'" (`marshall/SKILL.md:37`) | — |
| L2 | Gate ACTIVE work, not session count | **N-A** | Intent documented; no cap code to evaluate (see C4) | Falls out of C4 |
| L3 | External-signal teardown | **MEETS** | `reaper.sh` kills the window; "do NOT rely on self-close" | — |
| L4 | Surface failures, don't auto-reassign past a bound | **MEETS** | `retry.sh` bounded (RETRY_MAX=3, backoff); past bound → terminal `failed/`, window left open | — |
| L5 | Idle-gate reuse on the `…` ellipsis | **N-A** | No warm workers to gate (see C3) | Falls out of C3 |
| L6 | Workers under a trusted repo path, never `/tmp` | **MEETS** | Scoped to `experiments/watchtower-engine/` (`settings.local.json:8-14`); spawned in repo root | — |
| L7 | Blackboard MCP user-level (`~/.claude.json`) | **MISSING** | Registered **project-level** `.mcp.json` → `spikes/blackboard-mcp/server.mjs`; absent from `~/.claude.json` | Move the MCP registration to user-level per machine, or workers won't see it cross-session/cross-machine. **Latent bug** when DF goes multi-machine. |

### Layer 3 — Dead-ends (DF should AVOID; MEETS = correctly avoided)

| # | Dead-end | Verdict | DF current state (evidence) |
|---|----------|---------|------------------------------|
| D1 | Gating completion on a `state` string | **MEETS** (avoided) | Completion = handback file appearing (`run-next-workflow/SKILL.md:56`), not status |
| D2 | `respawn`/`--resume`/`--continue` for reuse | **MEETS** (avoided) | None found; fresh spawn each ticket |
| D3 | Network-monitor "proof" of billing | **MEETS** (avoided) | No monitoring code; billing is a documented rule (`runtime-model.md:76`) |
| D4 | Pane/process-tree liveness detection | **MEETS** (avoided) | Proven dead (`reaper-livefire-finding.md`); reaper uses engine artifacts. ⚠️ switchboard's `staleness-detector.ts:130-156` still carries the known-broken BFS (observer-only, never kills) |
| D5 | Any metered path (`-p`/SDK/key set) | **MEETS** (avoided) | Interactive spawn only; "NEVER `claude -p`" (`marshall/SKILL.md:15`); no `ANTHROPIC_API_KEY` |

### Layer 4 — Operational learnings (non-functional)

| # | Learning | Verdict | DF current state (evidence) | Delta |
|---|----------|---------|------------------------------|-------|
| O1 | HITL runs are HUMAN-paced | **PARTIAL** | Only HITL is `titles-human.workflow.js` (two-pass re-invocation); no engine-level pause primitive; no timing instrumentation | Comes with K1; add wall-clock awareness (don't gate many tickets per batch) |
| O3 | A parked worker is invisible without a notification | **PARTIAL** | Risk named (`reaper-brief.md` "stuck case"); switchboard emits `session.stale`; but AngelEye "NOT running", no alert wired | Wire a notification channel (see K2) |
| O4 | Self-heal (reboot wedged + re-queue) is load-bearing | **PARTIAL** | `retry.sh` re-queues from `failed/`; step-0 sweeps stranded `running/` (>10min); but **reboot of a live-but-hung worker is deferred** (stuck-case reaper) | Adopt suborch's reboot-on-wedge (timeout → fresh process → re-queue) |
| O5 | 429 budget shared box-wide across ALL claude procs | **N-A** | Understood (`runtime-model.md:33`); no enforcement (see C4) | Falls out of C4 |

### Layer 5 — Net-new capabilities

| # | Capability | Verdict | DF current state (evidence) | Delta |
|---|-----------|---------|------------------------------|-------|
| K1 | Native HITL gate (propose → pause → human approve/decline/redirect via file-drop → resume) | **MISSING** | `titles-human.workflow.js` is two-pass re-invocation, **not** worker pause/resume; human gate at job boundary, not mid-worker; no file-drop mechanism | Adopt suborch's gate: `needs-decision/<id>.json` (worker parks) + `decisions/<id>.json` (human) + send-keys resume. Proven in `suborch-demo/orchestrator.py --hitl` + `experiments/hitl_probe.py` |
| K2 | Block notification (alert when a decision is pending) | **MISSING** | Design intent only (`human-comms.md` — "ElevenLabs? system TTS?" open); SSE exists, no subscriber/alert; no `osascript`/`terminal-notifier`/TTS anywhere | Adopt suborch's `notify()` (terminal bell + `osascript` desktop notification on block); or wire switchboard SSE → an alert client |
| K3 | Audit trail ticket → session id → transcript path | **MISSING** | Run records have `queue_id`/`experiment_id`/timestamps but **no `session_id`, no transcript path**; `registry/` maps window↔queue_id only | Adopt suborch's `find_session`-by-content → `store/audit.jsonl` (ticket → session UUID → `.jsonl` path) |

---

## 3. The concentrated gaps (what actually matters)

The matrix has 21 rows but the gap is really **one cluster + three capabilities**:

- **The warm-pool cluster (C3 → C4/L2/L5/O5).** DF cold-spawns per ticket and has no concurrency governor. These are linked: without a warm pool, concurrency was never pushed, so the 429 governor was never needed/built. suborch's warm pool + CAP is a single coherent unit that fills all of C3, C4, L2, L5, O5 at once.
- **HITL gate (K1) + its two companions (K2 notification, K3 audit).** suborch built all three in the last 2 days; DF has none as a worker-level primitive. K1 is the centrepiece; K2/K3 make it usable and observable.
- **Two latent fixes:** L7 (MCP user-level) and O4 (reboot-wedged-worker).

Everything else is already conformant — **DF does not need to change its foundations.**

---

## 4. What dark-factory HAS that suborch lacks (do not disturb)

Any future transfer must NOT bulldoze these — they are DF's product surface, which suborch deliberately lacks:

1. **Observer constellation** — switchboard (launchd :5099/:5100, SSE fan-out, MCP registry, staleness-detector) + AngelEye + AppyRadar. (`switchboard/src/main.ts`)
2. **Marshall conductor** — a full skills-based orchestrator persona (preflight → take → dispatch → surface → self-learn). (`marshall/SKILL.md`)
3. **Millwright** — the build-side sibling ("build the machine, not perform the task") with a machinery-form decision matrix.
4. **Failure register** — structured JSONL ledger + `audit.sh` with category-threshold root-cause rule.
5. **Mochaccino design tooling** — visualisation/mockup pipeline.
6. **Canonical / ingestion warehouse** — three-layer self-improving capability extraction from upstream repos.
7. **Constellation preflight + blackboard MCP** — `constellation-status.sh` hard-stop; file-backed cross-agent KV.

---

## 5. The reverse direction (DF → suborch), briefly

The biggest thing suborch *should* take from DF is the **observer** (it has none): name workers `swagger-*` so switchboard sees them. suborch's `CONTEXT.md` already records this as its planned cockpit (Track A). Out of scope for this doc, noted for completeness.

---

## 6. The deferred decision this informs

This doc is "measure first." The gaps above are now concrete enough to choose **adopt-vs-rebuild** per cluster:

- **Warm-pool cluster + audit (C3/C4/K3):** these are mechanical, well-isolated, and suborch's code (`warm_pool.py`, `orchestrator.py`, `find_session`) is proven — the strongest **adopt-the-code** candidates (vendor behind Marshall's dispatch, replacing `dispatch-swagger.sh`'s cold spawn).
- **HITL gate + notification (K1/K2):** small file-drop protocol; could be **re-implemented** natively in DF's idiom (queue dirs + a notify call) or adopted. DF's `blackboard` MCP + switchboard SSE could host the surfacing.
- **Latent fixes (L7/O4):** trivial, do regardless of the bigger decision.

**Recommended next step (not taken here):** decide adopt-vs-rebuild for the warm-pool cluster first — it's the highest-value, most-isolated gap, and it's what DF's "the loop never completes" audit actually needs.

---

## Provenance

- DF current state: live code read 2026-06-18 (`dark-factory/experiments/watchtower-engine/`, `dark-factory/.claude/skills/`, `dark-factory/docs/`, `switchboard/src/`).
- suborch reference: `~/dev/ad/apps/suborch-demo/CONTEXT.md` (the build-spec) + `experiments/`.
- Checklist derived from suborch's 5 learning layers (code/laws/dead-ends/operational/capabilities).
- Supersedes the *currency* of `darkfactory-reconciliation.md` (2026-06-16) for execution-loop conformance; that doc remains the prior primitive-level narrative.
