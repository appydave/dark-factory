# Harness Evaluation — dark-factory's engine vs suborch-demo

**Purpose**: David's question — dark-factory already went down the orchestration-harness path once; suborch-demo is a from-scratch experiment that referenced it. Which mechanisms actually deserve promotion into the production harness, from which side? Not a re-run of the existing docs below — a verdict built on top of them, checked against the raw code and run artifacts myself.

**Prior art this doc stands on** (read fully, not re-derived): `~/dev/ad/brains/anthropic-claude/claude-code/research-briefs/darkfactory-reconciliation.md` (2026-06-16, first comparison, recommends HYBRID) and `docs/suborch-conformance.md` (2026-06-18, the current conformance map, MEETS 11 · PARTIAL 3 · MISSING 4 · N-A 3). Both already point the same direction. This doc's job: confirm that direction against fresh evidence, answer the Omnigent lineage question directly, and turn "hybrid" into a promotion plan with file-level actions.

**Status**: evaluation only. No code changed.

---

## Verdict up front

**Confirm the hybrid, don't re-litigate it.** Two independent prior docs (2026-06-16, 2026-06-18) already reached "adopt suborch's execution kernel, keep dark-factory's product surface" — and re-reading the actual code agrees. The two systems are the **same architecture, independently derived twice** from the same constraint (subscription-only, `rename(2)` CAS, artifact-is-truth). Where they differ is exactly where one side did work the other hasn't: suborch pushed concurrency (warm pool, 429 governor, HITL gate) that dark-factory only designed; dark-factory pushed real usage and observability (35 jobs, switchboard) that suborch never built.

**Biggest surprise**: there's nothing left to referee. The "which wins" framing dissolves on contact with the evidence — every dimension below resolves to either "same primitive, keep dark-factory's" or "dark-factory hasn't built this yet, suborch has, promote it." Zero dimensions are genuinely contested.

---

## The two lineages at a glance

```
dark-factory (experiments/watchtower-engine/)          suborch-demo (apps/suborch-demo/)
──────────────────────────────────────────────         ──────────────────────────────────
queue/ ──rename(2)──▶ running/                          queue/ ──os.rename──▶ running/
   │                                                        │
tmux new-window "claude '<instr>'"   (COLD, per ticket)  WarmPool: tmux send-keys into a
   │                                                      reused REPL (BOOT ONCE, reuse N×)
Swagger runs workflow                                       │
   │                                                     artifact_ok(results/<tid>.txt)
done/*.json  ◀── artifact-is-truth                          │
   │                                                     running/ ──rename──▶ done/
Marshall reaper: tmux kill-window                            │
   (keys off done/ mtime + registry)                     needs-decision/<tid>.json  ──▶
                                                           decisions/<tid>.json ──▶ send-keys
switchboard: passive SSE+MCP observer                     resume (HITL, PROVEN: approve/
   (ps/tmux/pgrep polling, never spawns)                  decline/redirect all demonstrated)

35 real jobs, Mode A = human types              10/10 toy tasks, 51s, 3 boots (vs 10 cold);
"process the queue" each time (serial/manual)   store wiped every run, no persistent ledger
```

---

## Comparison table

| # | Dimension | dark-factory | suborch-demo | Verdict |
|---|---|---|---|---|
| 1 | **Dispatch** | Cold `tmux new-window "claude '<instr>'"` per ticket (`dispatch-swagger.sh:19`). No reuse — "one invocation = one job then returns." | `WarmPool` (`warm_pool.py`): boot once, `tmux send-keys` reuse. Solves both the ~15-30s cold-boot latency AND the 429-churn from repeated spawns. Proven: 3 session boots total vs 10 cold spawns for 10 tasks. | **Promote suborch.** This is the single biggest gap (conformance doc: "the biggest single gap"). DF never needed it because it never ran concurrent. |
| 2 | **Claim/lease** | `claim-next.sh:24-31` — `mv queue/$f running/$f`; loser gets ENOENT, tries next. Anonymous claim (no `claimed_by`). Stress-proven 200×8×5, zero double-claims. | `orchestrator.py` `lease()` — `os.rename(Q/tid, RUN/tid)`, catches `FileNotFoundError`. Same anonymous-claim gap. | **Same primitive, independently derived.** Nothing to promote either way — but both share the same gap (no recorded ownership), which is exactly what DF-7 proposes to fix. Rebuild fresh at DF-7. |
| 3 | **Reaping/verification** | `reaper.sh` keys off `done/*.json` mtime + a window↔queue_id registry; kills the tmux window on grace. Explicitly abandoned process-tree detection as a dead end (`reaper-livefire-finding.md` — "Claude Code reparents to its daemon"). Proven live unattended once (2026-06-07). | `artifact_ok()` — checks `results/<tid>.txt` exists + non-empty. Discovered and fixed a real bug DF hasn't hit yet: gating on `state==done` instead of artifact-landed caused slot-starvation (546s/9-of-10 → 52s/10-of-10 once fixed). | **Same principle (artifact-is-truth), suborch found the concurrency-specific failure mode first.** Promote the "commit the instant the artifact lands" rule into DF's reaper *before* DF goes concurrent — it hasn't hit this bug only because it's never run concurrently. |
| 4 | **State model** | `queue/ running/ done/ failed/ runs/ registry/ reports/ failures/ deferred/ proof/` — richer, accumulated, has bounded retry w/ backoff (`retry.sh`, RETRY_MAX=3) and a structured failure ledger. | `queue/ running/ done/ results/ needs-decision/ decisions/ audit.jsonl` — leaner. No `failed/` on disk (failures live only in an in-memory dict); `reset()` wipes the whole store every run — **not a growing ledger**. | **Neither maps directly to the future.** DF-7 wants a *service-backed* plane (Switchboard `job-state-store` + `job-coordinator` recipes, ownership + liveness-keyed reaping) — a third design, not either's flat files. **Rebuild fresh per DF-7**, but borrow suborch's per-job `audit.jsonl` (ticket→session→transcript) as the schema seed for DF-7's per-job durable record. |
| 5 | **HITL** | Two different systems, confirmed NOT the same thing (per `comms-flow.md` §7c, independently re-verified): Watchtower's **curation queue** (promote/reject a canonical skill; design doc + 1-commit stub; never mutates `canonical/`) is a human-in-the-loop over *artifacts*, at rest. | `needs-decision/<tid>.json` → `decisions/<tid>.json` → live `send-keys` resume — a mid-task pause/resume of a **running worker**. Proven end-to-end: approve (10/10 with ticket 07 gated), decline (B2), redirect (standalone `hitl_probe.py`, confirmed the human's value was actually used, not the worker's default). | **Confirmed different mechanisms, both needed, neither replaces the other.** The harness genuinely needs suborch's mid-task gate — DF has literally nothing at this layer (`titles-human.workflow.js` is a two-pass re-invocation at a job *boundary*, not a pause inside one). **Promote suborch's K1/K2** (gate + `notify()`); leave Watchtower's curation queue exactly where it is. |
| 6 | **Observability** | `switchboard` — real launchd daemon, SSE+MCP, `ps`/`tmux`/`pgrep` polling, staleness-detector. Verdict from the prior reconciliation doc stands: "production-ready." Never spawns Claude — genuinely zero-coupling. | None of its own. `audit.jsonl` (dispatch ledger) + a Stop-hook push-callback experiment (liveness signal, explicitly "not completion proof"). suborch's own roadmap (Track A, still unbuilt) already plans to *adopt* switchboard rather than build a rival, by naming `--bg` workers `swagger-*` so switchboard's existing collector sees them for free. | **switchboard survives, unchanged.** Promote suborch's `audit.jsonl` (ticket→session_id→transcript) into DF as **net-new** (K3) — DF's `registry/` only maps window↔queue_id today, no session/transcript trail. |
| 7 | **Production evidence** | **35 real jobs**, verified directly (file count matches, timestamps span 2026-05-30→2026-06-12, real elapsed dev time). But Mode A: a human types "process the queue" every time — serial/manual, never autonomous, never concurrent. | **10/10 in 51s** — real, but 10 hardcoded toy one-liners (haiku, primes, capital cities), and the store is wiped (`reset()`) every run, so there's no persistent job history to compare against DF's 35. CONTEXT.md itself is candid: other runs took 380s/961s, and "workers wedged and self-healed in nearly every run" — the self-heal is load-bearing, not a rare backstop. | **Weigh honestly, don't average.** These prove *different things*: DF proves sustained real usage under a human-serial loop; suborch proves the concurrent-autonomous-dispatch *mechanism* works cleanly, once, on toys. Neither is production-hardened-concurrent. **The proof run below is designed to close exactly this gap** — one real ticket, not a toy, through the adopted mechanism. |
| 8 | **Provenance/lineage** | — | See dedicated section below. | Independently convergent architecture; one explicit concept borrowed from Omnigent (not code, not the core mechanism). |

---

## Per-mechanism verdict

| Mechanism | Verdict | Action |
|---|---|---|
| Dispatch (cold-spawn vs warm pool) | **Promote suborch's `warm_pool.py`** | Vendor behind Marshall's dispatch, replacing `dispatch-swagger.sh`'s cold spawn. Biggest single value item. |
| Claim/lease (`rename`/CAS) | **Keep dark-factory's, extend it** | Already convergent — no replacement needed. Add `claimed_by`/`claimed_at` recording (DF-7 D-item), closing the one gap both sides share. |
| Reaping (artifact-is-truth) | **Keep dark-factory's mechanism, import suborch's fix** | Same principle. Pre-empt the starvation bug suborch already found: commit on artifact-landed, never on a `state==done` string, before DF goes concurrent. |
| State model (flat files) | **Rebuild fresh, per DF-7** | Neither's flat-file shape is the target — DF-7 is a service-backed plane. Use suborch's `audit.jsonl` shape as input to `job-state-store`'s per-job schema. |
| HITL | **Promote suborch's gate wholesale, additively** | `needs-decision/`+`decisions/`+`send-keys resume`+`notify()`, native shell/skill port. Leave Watchtower's curation queue untouched — different job. |
| Observability | **Keep switchboard, add suborch's audit trail** | switchboard stays the observer of record. Add `audit.jsonl` (ticket→session→transcript) to DF as net-new capability (K3). If/when DF adopts `--bg` workers alongside tmux windows, add a `--bg`/`agents --json` collector to switchboard so it sees both. |
| Concurrency governor (429 wall) | **Promote suborch's CAP gate** | DF has design intent ("~4 Swaggers max") with zero enforcement code. suborch's CAP=N admission-control gate is a direct, proven import — needed the moment warm pool ships (concurrency without a governor just moves the 429 wall, doesn't remove it). |
| Auto-wake (DF-10/C3) | **Orthogonal — build as already specced** | Not a suborch-vs-DF question at all. C3 wires *who* triggers dispatch (Switchboard `job.queued` SSE → Marshall's Monitor) — independent of *how* dispatch executes once triggered. Do both; they compose. |

---

## What suborch owes to dark-factory / Omnigent (lineage note)

- **From dark-factory**: nothing lifted at the code level — suborch-demo is Python, dark-factory's engine is shell+skills, built independently. What it owes is *architectural*: both were built from the same documented constraints (`runtime-model.md`'s subscription-only rule, the same 2026-06-15 metered-billing cutover) and landed on the identical `rename(2)` CAS + artifact-is-truth pattern with no cross-pollination of code. suborch's own CONTEXT.md calls this out directly: **"one architecture built twice."** This is convergent evolution off a shared constraint, not borrowing.
- **From Omnigent**: **one explicit borrow, not the core mechanism.** `PHASE-5-PLAN.md`'s own provenance note: *"The HITL gate pattern is borrowed from Omnigent's policy-ASK/elicitation model... the implementation is entirely suborch's own primitives."* That's the only credited transfer. Everything else that sounds Omnigent-adjacent (warm pool, CAS lease) is independently derived — confirmed by grepping Omnigent's source: no `rename`/CAS lease mechanism exists there at all, and its `mcp_pool.py` is an MCP-connection proxy pool, unrelated in concept to suborch's tmux worker pool (naming coincidence, not shared design).
- **Omnigent-as-runtime was tried once and reverted** (2026-06-17 spike, `experiments/omnigent_validation_spike.py`, kept explicitly labeled "NOT a dependency"). Reason: Omnigent can only observe sessions it spawns itself — adopting it as suborch's cockpit would mean Omnigent runs the Claude session and suborch's own engine (warm pool/lease/reaper) gets bypassed, inverting suborch's whole identity. Correctly rejected.
- **Independent third-party validation, not a source**: a Databricks team is noted as having converged on the same core mechanism (interactive `claude` + tmux + `send-keys` + no `-p`) — used only as evidence suborch's design is "correct, not a workaround."

**Answer to the lineage question: partial.** Omnigent contributed exactly one concept (the HITL gate idea), reimplemented from scratch; it contributed zero code and zero of the concurrency/claim/warm-pool mechanics, and one adoption attempt was explicitly reverted.

---

## Promotion plan

**Phase 1 — trivial, do regardless of the bigger decision** (both named as "latent fixes" in the conformance doc):
- Move dark-factory's blackboard MCP registration from project-level `.mcp.json` to user-level `~/.claude.json` (L7 — breaks cross-machine/cross-session otherwise).
- Add the explicit `ANTHROPIC_API_KEY`-unset guard to `dispatch-swagger.sh` at spawn time (documented as a rule today, not enforced in code).

**Phase 2 — the warm-pool cluster (highest value, most isolated)**:
- Vendor `suborch-demo/warm_pool.py` behind Marshall's dispatch, replacing `dispatch-swagger.sh`'s cold spawn. Define the import seam as a thin contract (queue dir + claim protocol + worker spawn/teardown commands) so the Python kernel is callable from a shell/skill conductor without a language rewrite — the file-drop store is already the natural seam.
- Add suborch's CAP=N admission-control gate to Marshall before any concurrent dispatch ships (C4/L2/O5 — currently zero enforcement code).
- Import the "commit-on-artifact-landed, not `state==done`" rule into `reaper.sh` now, pre-emptively — cheap, and closes a bug DF hasn't hit only because it's never gone concurrent.

**Phase 3 — HITL gate (K1/K2)**:
- Port `needs-decision/<id>.json` → `decisions/<id>.json` → resume protocol natively into watchtower-engine's idiom (queue-style dirs + a `notify()` call — terminal bell + `osascript`). Wire the notification through switchboard's SSE if a client exists, otherwise the local bell/desktop-notification is sufficient day one.
- Leave Watchtower's curation queue (promote/reject `canonical/` candidates) completely untouched — confirmed orthogonal, not a duplicate.

**Phase 4 — DF-7 state plane (rebuild fresh)**:
- Build the two new Switchboard recipes DF-7 specs: `job-state-store` (per-job durable record, `pool→claimed→running→done|failed`, `claimed_by`/`claimed_at`) and `job-coordinator` (claim-by-id over the network, liveness-keyed reaping via AngelEye, modeled on `staleness-detector.ts`). Seed its per-job schema from suborch's `audit.jsonl` shape (ticket→session→transcript) rather than either side's current ad hoc registry files.
- DF-10 (auto-wake) is a separate, already-specced, independent wire — build it in parallel; it composes with Phase 2's warm pool rather than depending on it.

**The one-ticket end-to-end proof run** (closes the "production evidence" gap honestly):
Take one real, currently-open dark-factory backlog item (not a toy) and run it through the Phase 2+3 stack once Phase 2/3 land: warm-pool dispatch (not cold-spawn), with the HITL gate wired and deliberately exercised on at least one judgment call inside the run, landing as a genuine `done/36` (job #36, continuing the real ledger — not a wiped demo store). That single run proves concurrency-capable dispatch + native HITL on real stakes, the exact thing neither side has today (DF: real work, never concurrent; suborch: concurrent, never real work). Write the proof to `experiments/watchtower-engine/proof/warm-pool-hitl-first-real-run.md`.

---

## Related

- `~/dev/ad/brains/anthropic-claude/claude-code/research-briefs/darkfactory-reconciliation.md` — first comparison (2026-06-16), reached HYBRID independently
- `docs/suborch-conformance.md` — current conformance matrix (2026-06-18), MEETS/PARTIAL/MISSING scorecard this doc's table 1-8 is checked against
- `docs/comms-flow.md` §7 — names the HITL-mechanism split this doc confirms at row 5
- `backlog/specs/c3-marshall-auto-wake-spec.md` (DF-10), `backlog/specs/df7-switchboard-state-plane-spec.md` (+ `.osmani.md` variant) — the specced future Phase 4 targets
- `docs/runtime-model.md`, `~/dev/ad/brains/dark-factory/watchtower-control-surface.md` — the shared constraint (subscription-only, files-as-truth) both lineages independently derived from
- `~/dev/ad/apps/suborch-demo/CONTEXT.md`, `PHASE-5-PLAN.md`, `orchestrator.py`, `warm_pool.py` — suborch's build-spec and code
