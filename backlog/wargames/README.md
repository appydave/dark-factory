# War-Game Portfolio — 57 executor-ready tickets (2026-07-06)

Authored by 57 parallel Fable agents against `plans/wargames/wargame-spec.md`, from the
triaged NOW+NEXT survivors of the 110-candidate pool (`plans/wargames/candidates.js` —
the 52 LATER briefs stay there). Each ticket = a war game (`<ID>-<slug>.md`) + a staged
engine ticket (`tickets/<ID>.json`).

**Run:** `bin/promote-wargame.py --list` · promote ready tickets one-by-one or `--next N`;
then boot the engine with a raised wall: `cd engine && python3 orchestrator.py --pool 1
--model sonnet --max-wall 3600`. Progressive drain — never bulk-promote.

## Systemic flags from the authoring run (read before first promotion)

1. **Self-hosting hazard** — five tickets (T1-01/02/03/05/06) run or kill the engine
   itself; an engine-dispatched executor would murder its own tmux session. The promote
   script refuses them; run those attended in a manually-opened worker.
2. **WORKER_TIMEOUT=240s** — orchestrator reaps quiet workers at 4 minutes; most war
   games run longer. Always dispatch war-game tickets with `--max-wall 3600`; a real fix
   (per-ticket wall override) is a good first engine tweak.
3. **T1-02 blocks your own usage** — the 429 saturation run exhausts the 5-hour window
   for ALL interactive Claude use; it parks on a pre-seeded go-decision so the timing is
   David's call.
4. **`.CONVENTION.md` is stale** (says orchestrator doesn't kind-filter; it does since
   07-06) — T8-01's truth pass covers it.
5. **Latent engine defects found during recon** (recorded in T1-01): declined HITL
   tickets strand in `running/`; a corrupt `decisions/*.json` silently defaults to
   APPROVE.

## Index

| ID | pri | title | deps | headline |
|---|---|---|---|---|
| T1-01 | high | T1 Engine: Exercise HITL gate live end-to-end | — | Live 3-leg HITL proof (approve/redirect/decline via --hitl); recon found two latent engine defects to record — declined tickets strand in running/ (commit never called), and a corrupt/partial decisions/<tid>.json sile… |
| T1-02 | high | T1 Engine: Prove CAP/BACKOFF against a real 429 | — | War game to hit a genuine usage-limit wall and prove the shipped CAP/BACKOFF governor (fixture capture, signature match, flag lifecycle, live reap path); recon confirmed the governor is fully built but ENGINE-NOTES st… |
| T1-03 | high | T1 Engine: Arm auto-wake dispatch leg — first live run | — | Arms the auto-wake dispatch leg (protocol doc + arm/disarm logging + live canary fire); recon found the 07-06 anomaly leaves no transcript trace AND a session-killing hazard: a wake-dispatched second orchestrator tmux… |
| T1-04 | high | T1 Engine: C4 return leg — 'what ran' surfaced to David | — | C4 return leg: done-watcher leg in wake.py (launchd WatchPaths widened to store/done) + engine done-tickets as a third SHIPPED source in project-digest — recon confirmed orchestrator never notifies on completion and m… |
| T1-11 | high | T1: DECISION war-game — Switchboard state-authority fork | — | Q3 state-authority fork mapped as a decision artifact (filesystem-truth vs DF-7 plane); recon found Switchboard down on both machines, DF-7 recipes never built, its spec targeting the retired floor (11 stale refs), an… |
| T10-01 | high | T10 Fleet: Roamy as Swagger worker | — | Cross-machine Swagger delegation Mini->Roamy over Tailscale, live-proven during authoring (ssh+tmux+interactive claude boots in ~5s, answers a turn in ~5s, torn down clean) — war game re-runs the proof against a real … |
| T2-01 | high | T2 Producer/BA: build the BA agent (Producer / C2) — internals spec + v1 producer skill | — | BA agent (Producer/C2) war game — design-first: internals spec + v1 producer skill + stdlib ticket emitter with scratch-dir dry-run; recon confirmed digest.py works for dark-factory (15 JSON keys verified), no produce… |
| T2-02 | high | T2 Producer/BA: Universal activity registry — staged sweep + design spec | — | Universal activity registry war game (L, design-first: staged sweep+query tool, ratification-gated spec, deferred promotion ticket) — recon found 11 off-registry git repos invisible to locations.json, including switch… |
| T2-03 | high | T2 Producer/BA: digest.py --list + onboard project #2 (omi-fetch) | — | digest.py --list + onboard omi-fetch as project #2 (wiring the ignored needs_you.markers config key) and close the superseded deferred queue ticket — recon confirmed list_project_ids() exists unused, only dark-factory… |
| T3-01 | high | T3 Ingestion: First ingestion — review-dimensional (Session 1: harvest + draft) | — | First-ever canonical ingestion (Session 1: harvest+draft of review-dimensional) — recon confirmed all 3 upstream origins on disk with SHAs, but found David's review-* voice anchors refactored into aliases over lenses.… |
| T3-02 | high | T3 Ingestion: Voice-review + ratify first ingestion | wg-t3-01-first-ingestion-review-dimensional | Voice-review + ratify the first canonical artifact (review-dimensional) via a designed engine HITL pause; recon confirmed canonical/ is still empty (registry 0), the 05-18 backlog item is still open, validators T3-03/… |
| T3-03 | high | T3 Ingestion: build tools/verify-provenance.py (8-rule provenance validator) | — | War-gamed the 8-rule provenance validator (tools/verify-provenance.py) — recon confirmed the tool is unbuilt and canonical/ holds zero artifacts, so the tool ships with an 11-case --self-test as its own proof, plus su… |
| T3-04 | high | T3 Ingestion: Build tools/style-check.py — automated ratification checklist | — | tools/style-check.py war game (SC1-SC14 checks, fixture self-test) — recon confirmed canonical/ is EMPTY (only INDEX.md), so verification is fixture-based, not real-artifact-based |
| T3-05 | high | T3: DECISION batch — the 14 corpus questions A–N | — | Decision batch for corpus questions A-N — recon found most are already settled: A David-ruled (schema-history 0.0.3 source-only), B/D/F/L David-deferred to Phase 2.5, C/G/I/J settled de-facto by discover practice, E r… |
| T3-17 | high | T3 Ingestion: LLM-judge calibration (Gap B) — score the design judge against David's mocha-census labels | — | Gap B judge calibration: blind 60-shot stratified pass over round-02 (47 love / 54 good / 55 average, 100% PNG coverage verified) scored via stdlib weighted-kappa tool; recon found the calibration set fully intact and… |
| T5-01 | high | T5 Watchtower: app charter + scaffold — first deploy serving status.py --json | — | Watchtower charter + finish-the-scaffold + first deploy of the status.py --json seam — recon found the AppyStack scaffold ALREADY exists (1 commit, 2026-06-11) but was never installed, sits on Chrome-unsafe ports 5060… |
| T5-07 | high | T5 Watchtower: Reconcile the two decision-queue concepts | — | T5-07 locks the HITL-gate vs curation-queue vocabulary in one design note (docs/decision-queues.md) before the Watchtower UI bakes the name collision in — recon confirmed the split is already documented (comms-flow.md… |
| T6-01 | high | T6 Constellation: name-collision sweep, all apps | — | T6-01 sweeps all 40 constellation apps vs ~145 David-owned skills for NL-resolution collisions — recon found the two landed 07-04 pointer fixes (commit 0754317, plugin v6.1.0) are NOT live because the plugin cache sti… |
| T6-02 | high | T6 Constellation: Migrate sentinel 'a'→'e' — cut launchd + MCP to the re-scaffold, retire the typo'd repo | — | Sentinel 'a'→'e' migration war-gamed end-to-end (install → smoke → MCP+launchd cutover with rollback → retire-in-place → register); recon confirmed the live mismatch — the MCP server NAMED appyradar-sentinel serves fr… |
| T6-03 | high | T6 Constellation: Fix sentinel blind-to-Roamy | — | Fix sentinel blind-to-Roamy — root cause pre-verified live: config host 'macbook-pro' stopped resolving after the 2026-07-03 Roamy rename (ssh 'Could not resolve hostname' confirmed today, while ssh davidcruwys@roamy … |
| T6-10 | high | T6 Constellation: Retire-or-fix com.appydave.omi-sync — verify retirement, restore the orphaned sync leg | — | T6-10 covers the omi-sync retire-or-fix — recon found the retirement already executed today (loose-ends D3, plist archived 15:02), so the war game pivots to verifying it and closing the orphaned sync gap: raw-intake i… |
| T7-05 | high | T7: Daily workers' review digest — day-windowed end-of-day rollup over engine/store | — | War-games engine/workers_digest.py — a read-only, local-day-windowed end-of-day rollup over engine/store/ (settled tickets + audit attribution + blocked-on-you + running/queue), with the candidate-mandated project-dig… |
| T7-10 | high | T7 Self-learning: design-lint → Shelly fold + census bench verify | — | Folds design-lint's rubric into Shelly as a lint-render self-review command (Q9 locked) and verifies the three census claims — recon confirms none of bench-mode / export-to-file / generator-seam ever landed (bench is … |
| T8-01 | high | T8 Doc truth: Truth-reconciliation pass — strategy-doc status lines match shipped engine/ reality | — | Truth-reconciliation of 4 strategy docs + ENGINE-NOTES via additive dated addenda; recon confirmed docs-lag-code on all five (C2/C3 shipped, HITL wired-unexercised, auto-wake built-disarmed, omi-fetch search + kdd que… |
| T8-02 | high | T8 Doc truth: Fix CLAUDE.md's stale activation pointer | — | Surgical three-file fix of the phase-b activation misroute — recon found it lives at THREE ends (CLAUDE.md:24 'START HERE', docs/INDEX.md:41 'the next build move', and un-bannered phase-b-next-steps.md itself, frozen … |
| T8-03 | high | T8: Retire Penny/Alex/Oscar from architecture.md — note the Marshall/Swagger supersession | — | Retire Penny/Alex/Oscar from architecture.md with a dated supersession note — recon confirmed 5 exact reference sites, that the doc's Last-updated (2026-06-01) is literally one day before the Marshall/Swagger naming c… |
| T8-08 | high | T8: Repo hygiene sweep — fleet verdicts + safe pushes | — | Fleet repo-hygiene sweep (both machines, verdicts + safe pushes only) — recon shows the June-15 picture moved: mac-mini-m4 now has 48 dirty repos / 4 no-remote / 5 unpushed, and deckhand on Roamy STILL has no remote w… |
| T9-02 | high | T9 Voice: Sound-effect vocabulary — done/failed/needs-you chimes | — | T9-02 sound vocabulary (needs-you=Sosumi, failed=Basso, done=Glass, other=Pop in consumer.py) — recon found orchestrator.py emits ONLY job.completed today, so the ticket also adds 5 one-line emit_event inserts (job.fa… |
| T1-05 | normal | T1: C5 proof — one real workflow job via talking | — | C5 north-star proof staged as a de-risked 10-minute drill; recon found the one real gap — Marshall's SKILL.md predates the engine and never mentions engine/store/queue/, so the talk-to-ticket leg would misfire today |
| T1-06 | normal | T1 Engine: Warm pool N>1 under CAP | — | Warm pool N=3 under CAP: 200x8 lease-race harness + live --pool 5 clamp run — recon found a self-hosting hazard (worker names hardcoded df-worker-<n>; boot() kill-sessions its own name, so the live leg cannot run from… |
| T1-07 | normal | T1 Engine: Golden-job regression suite (Gap A) — design, frozen jobs, runner ticket | — | Golden-job regression suite (Gap A) war-gamed design-first: 5 frozen machinery-leg jobs + envelope schema + replay-runner follow-on ticket; recon found audit.jsonl has only 1 real dispatch entry (17 done tickets are m… |
| T1-10 | normal | T1: Engine store retention policy — archive-only keep-window tool | — | Store retention war game: archive-only keep-window tool (engine/retention.py, 30d/keep-20 defaults) — recon found the consumer's seen-set keys on absolute event paths, making unconsumed-event and consumed-log ordering… |
| T10-02 | normal | T10 Fleet: Cross-machine HALT broadcast | — | Cross-machine HALT broadcast via halt.py --fleet + engine/fleet.json (SSH file-write, no Switchboard) — recon proved Roamy reachable with a clean dark-factory clone whose engine PREDATES halt.py entirely, so the ticke… |
| T2-04 | normal | T2 Producer/BA: Digest-over-activity | wg-t2-02-activity-registry | Digest-over-activity: digest.py --active iterates registry-detected change (full boxes for configured projects, compact lines otherwise) — recon confirmed project-digest v1 is green and no activity registry exists any… |
| T2-05 | normal | T2 Producer/BA: Feed layer into the briefing — engine tickets + needs-decision + Linear into NEEDS-YOU/IN-FLIGHT | wg-t1-04-c4-return-leg | Feed layer: engine queue/running/needs-decision + Linear folded into the briefing's NEEDS-YOU/IN-FLIGHT — recon found NO Linear API key anywhere on disk (Linear is claude.ai-MCP OAuth only), so the expected route buil… |
| T2-06 | normal | T2 Producer/BA: Five-day briefing→BA→tickets proof — arm the Step-0 acceptance test | wg-t2-01-ba-agent | Arms the operating model's 5-day Step-0 acceptance test as a staged harness (protocol + day-log templates + 5 per-day auditor tickets + day-0 rehearsal), since one Swagger dispatch can't span a week or speak for David… |
| T3-06 | normal | T3 Ingestion: Distill knowledge-capture — eval gap-fill + winner verification (201-artifact cluster) | — | T3-06 re-scoped from disk truth: knowledge-capture is ALREADY distilled (7 drafts, 2026-05-18) — the war game closes the real gap: 92 missing per-artifact evals across the distillations' 111 cited sources, winner-pick… |
| T3-07 | normal | T3 Ingestion: Distill: system-comprehension (180) — refresh + overlap map | — | T3-07 reframed by recon: system-comprehension was ALREADY distilled 2026-05-17 (5 draft files on disk) — war game now delivers the genuinely missing piece, an overlap map re-verifying all 5 sub-cluster winner/gap clai… |
| T3-08 | normal | T3 Ingestion: Spec-writing cluster (157) — L2a validation + distillation refresh | — | Spec-writing cluster L2a validation + distillation refresh — recon found the candidate premise stale: the cluster was ALREADY distilled 2026-05-17 (6 draft files), so the ticket was re-scoped to close the L2a eval gap… |
| T3-15 | normal | T3 Ingestion: L2b rollout harness DESIGN | — | L2b rollout harness DESIGN — spec-only ticket producing backlog/specs/l2b-rollout-harness-spec.md (task sets + rubric + execution env, 5-task seeded-defect code-review pilot, T3-16 build plan); recon found the eval pi… |
| T3-19 | normal | T3 Ingestion: Second ingestion wave — orchestration cluster ×3 (Session 1: harvest + draft) | wg-t3-01-first-ingestion-review-dimensional, wg-t3-02-ratify-first-ingestion | Second ingestion wave locks the orchestration cluster's own Top-3 (swarm-topology, autonomous-pipeline-runner, governance-and-observability) with all 9 origin paths pre-verified + SHAs recorded; recon found truth-trai… |
| T3-26 | normal | T3 Ingestion: Promotion mechanics proof | wg-t3-02-ratify-first-ingestion | One HITL-gated promote+demote cycle on the first ratified artifact (challenger variants/self.v2.md -> SKILL.md v2, v1 -> variants/was-canonical-<date> hash-verified), codified into docs/promotion-procedure.md — recon … |
| T5-02 | normal | T5 Watchtower: Kanban board over the engine store (read-only v1) | wg-t5-01-watchtower-charter-scaffold | Read-only kanban (queue/running/done lanes) in the real Watchtower app via a status.py --json seam — recon confirmed the scaffold is 1-commit bare, status.py works but lacks card fields (fixed additively), and the sca… |
| T5-03 | normal | T5 Watchtower: Live agent view — df-worker liveness + pane tails + AngelEye probe | wg-t5-01-watchtower-charter-scaffold | Live agent view for Watchtower — /api/agents composing status.py --json + tmux pane tails + AngelEye probe, with a working/idle/stale state machine; recon found the Watchtower repo already exists as a 1-commit virgin … |
| T5-06 | normal | T5 Watchtower: HITL inbox UI — approve/decline/redirect surface over the engine's mid-task gate | wg-t5-01-watchtower-charter-scaffold, wg-t5-07-decision-queue-reconcile | HITL inbox UI in the Watchtower app (GET/POST /api/hitl + approve/decline/redirect page over engine needs-decision/->decisions/); recon confirmed the gate contract in orchestrator.py (~599-632, corrupt decision silent… |
| T5-12 | normal | T5 Watchtower: Engine API layer — status.py --json promoted to HTTP API :7430 + df-engine MCP wrapper (API+MCP doctrine) | — | Engine API layer: status.py --json promoted to read-only HTTP :7430 + zero-dep df-engine MCP wrapper (MCP-over-API, kdd-bridge house pattern) — recon confirmed status.py works today, no HTTP server exists in engine/, … |
| T6-04 | normal | T6 Constellation: AngelEye revival — launchd daemon + hook re-install against current Claude Code | — | AngelEye revival (daemonize + hook re-install): recon found the app fully dark — no listener on :5051, ZERO AngelEye hooks in ~/.claude/settings.json, builds 3+ months stale — and the machine's angeleye-install skill … |
| T6-05 | normal | T6: AngelEye MCP wrapper — read-only stdio surface over the existing API | — | AngelEye MCP wrapper (first API+MCP doctrine retrofit): thin read-only stdio proxy over the verified :5051 API — recon confirmed zero MCP code exists, real port is 5051 not the documented 5501, server is currently DOW… |
| T6-07 | normal | T6 Constellation: AppyRadar owns tmux/process state | — | T6-07 builds the tmux/process collector + process_state CLI/MCP surface in appyradar-sentinel ('e' repo — verified a never-installed 2-commit scaffold, while the live MCP and launchd still run the old 'a' repo appyrad… |
| T6-12 | normal | T6 Constellation: omi-fetch enrichment backlog | — | omi-fetch enrichment residuals + steady-state proof — recon found the candidate's premise already OBE: commit dc6d96b (2026-07-06 morning) cleared the whole 291-row backlog on sonnet, leaving only 2 stub rows (A122, A… |
| T7-01 | normal | T7 Self-learning: the ONE reflective-review engine (staleness scan + review briefs, 4 targets) | — | T7-01 builds the ONE staleness+recategorization engine (scan/brief CLI, 4 targets) — recon found David already ruled the architecture inside concepts.md itself (JSON=truth, date-math staleness, LLM=judge), and all 4 t… |
| T7-04 | normal | T7: Lightweight decision-lineage log — one-line ledger tied to workflows | — | One-line decided/over/because ledger at docs/kdd/lineage.md — recon found docs/sop-lifecycle.md literally mandates this exact artifact ("lineage, not ceremony"), so the war game builds the skim layer under the existin… |
| T7-09 | normal | T7 Self-learning: KDD structural SDLC gates | — | KDD structural SDLC gates: Gate A (pre-work decisions checkpoint injected into the engine dispatch prompt) + Gate B (done-ticket absorption through Lisa via a ledger-diff script emitting deferred absorption tickets) —… |
| T8-05 | normal | T8 Doc truth: DF-ADR provenance flattening + KDD uniformity | — | Flatten 42 DF-ADR nested provenance blocks to Lisa's flat convention + re-census all 4 KDD instances — recon found Cortex AND KBDE are already flat (48/48 each, the 07-04 findings note is stale), so dark-factory is th… |
| T8-09 | normal | T8 Doc truth: Switchboard greenfield charter recon | — | Switchboard charter recon: authoring recon already resolved both disputes — charter NEVER authored (KICKOFF/seed/grounding exist, step-4 David interview never ran) and Switchboard is UP on Roamy right now (launchd, bo… |
| T9-01 | normal | T9 Voice: audio-out engine decision + build | wg-t1-04-c4-return-leg | Audio-out engine decided in-game (kokoro-tts primary / macOS say fallback / ElevenLabs rejected) + build of engine/speak.py wired into both notify() seams — recon found the elevenlabs-agents skill cited by human-comms… |
| T9-04 | normal | T9 Voice: Samantha Q&A front door v1 — intake spec + samantha skill + OMI capture drain | wg-t2-01-ba-agent | Samantha front door v1 = the consumer comms-flow §3a says is missing — recon found the voice channel fully live (omi-fetch pulsing, 291/291 captures signal-enriched) and a David-ratified Voice Law (§8, 2026-07-06) tha… |

## Per-ticket flags (from authoring recon)

**T1-01**
- Self-hosting hazard for the whole T1 portfolio: this ticket runs orchestrator.py, but WarmWorker.boot() kills df-worker-1 — if the executor is itself dispatched into df-worker-1 by a live engine, the proof run kills its own session. War game aborts (A1) to needs-decision/ in that case; T1-01 likely needs a standalone/manually-supervised dispatch.
- WORKER_TIMEOUT=240s reboots+requeues any worker with no artifact — most multi-move war-game tickets exceed that budget under engine dispatch; portfolio-wide execution-model question for Phase 5.
- engine/store/queue/.CONVENTION.md is stale: it warns orchestrator.py does not filter by kind, but dispatchable() now skips external-research and deferred tickets (verified on disk 2026-07-06) — the war game has the executor record this docs-lag-code instance in its report.
- Phase 5 queue contention handled as Fork F1: if other promoted war-game tickets sit dispatchable in queue/ at run time, the proof parks them to engine/store/queue-parked-t1-01/ for the duration and restores them byte-identical — an invented, documented convention.
- --hitl gates exactly ONE ticket filename per run, so the proof is three sequential orchestrator runs, and the decline run exits 1 by design (all-done-only exits 0).

**T1-02**
- Deliberately HITL: the ticket parks on first dispatch unless David pre-seeds engine/store/decisions/wg-t1-02-go.json — saturation exhausts the 5-hour window and blocks ALL interactive Claude use (including David's own sessions) until reset, so timing is his call.
- Structural trap verified in code: WarmWorker.boot() kills any existing df-worker-<n> tmux session, so an engine-dispatched executor (itself df-worker-1) cannot run the nested end-to-end orchestrator leg — Fork F3 Route B parks that one leg for an attended run; consider a --worker-offset flag someday.
- Portfolio-wide risk: WORKER_TIMEOUT=240s will reap any war-game worker long before a multi-hour war game finishes — Phase 5 promotion needs attended runs or a lengthened-timeout dispatch mode for ALL war-game tickets, not just this one.
- Likely real finding awaiting the run: the actual TUI wall phrasing (e.g. '5-hour limit reached ∙ resets ...') may contain none of the four shipped USAGE_LIMIT_SIGNATURES substrings — F2 covers the one-line fix; this gap is the ticket's main value.
- backlog/wargames/ did not exist before this task — created it (plus tickets/); other war games authored in parallel will land alongside.

**T1-03**
- Anomaly likely unresolvable: authoring-time sweep of all dark-factory transcripts found zero WAKE-ARMED arm executions at 08:19Z — war game plans for UNRESOLVED verdict + logging mitigation, not a guaranteed root cause
- Systemic gap beyond this ticket: warm_pool.py boot() kill-sessions df-worker-N, and wake.py's .wake.lock is blind to manually-started orchestrators — any concurrent second engine boot murders a live worker; relevant to T1-06 (warm pool N>1) too
- End-state ARMED is inferred from the ticket title; David never separately ratified permanent arming — all abort paths deliberately end DISARMED + needs-decision
- Scope includes a 2-line code edit to engine/wake.py (arm/disarm wake.log logging) — slightly beyond pure doc+proof, but it is the direct mitigation for the anomaly's untraceability
- cmd_arm records by=$USER which cannot distinguish human from agent shells — the new logging adds pid/ppid but attribution remains weak by design

**T1-04**
- Cross-repo ticket: leg (b) edits ~/dev/ad/apps/project-digest (separate git repo, currently clean except generated view/dark-factory.html) — executor commits/pushes two repos
- consumer.py overlaps conceptually (reads job.completed events + chimes) but only covers orchestrator-path tickets and needs a run-forever loop; war game explicitly fences it off as the rabbit hole rather than unifying
- Notification channel bar is macOS osascript (call-path-verified), per the accepted 0932 auto-wake precedent — if David wants a richer channel (T9 audio-out/Samantha) this parks to needs-decision instead
- done-ticket outcome schema is duplicated in three places by deliberate engine convention (orchestrator/status/wake) — the new summariser adds a fourth copy of the results-vs-embedded-result duality; a future refactor ticket could consolidate
- War game includes a one-line docs truth fix (north-star C4 spine annotation) — tiny overlap with T8 truth-reconciliation, fenced to a suffix-only edit

**T1-11**
- Contradictions confirmed on disk: comms-flow.md says Switchboard 'live on MacBook Pro :5099/:5100' but localhost:5099 refuses, launchctl has no job, and roamy:5099 times out (Roamy Tailscale-active, so recorded as unverifiable, not down); constellation doc calls it 'substantially built'; auto-wake.md cites a 'Switchboard is DOWN' line in CLAUDE.md that no longer exists there.
- DF-7's client contract is stale: all 6 Switchboard commits are 2026-06-06, job-state-store/job-coordinator were never built, and the spec's claim-next.sh/run-next-workflow/WT_STATE_PLANE targets were superseded by engine/ on 2026-07-04 — the war game makes re-baselining the spec (Move 3) part of Branch B's honest cost.
- candidates.js says T8-09 (charter recon) 'feeds T1-11', but T8-09 is bucket 'next' while T1-11 is 'now' — a hard depends_on would invert priority, so it's a soft input: T1-11 carries its own recon and reads T8-09's output only if present.
- Ownership gap already half-closed: orchestrator.py records claimed_by/claimed_at on claim (line ~227), so DF-7's 'anonymous claim' problem statement is partially outdated — recorded in the war game so Branch B isn't oversold.
- One trigger class needs watching at execution time: if any forcing trigger (second-machine claims, store-sync proposal, double-claim) has already fired, Fork F3 parks a needs-decision asking David to actually rule — the 'defer' premise would be stale.

**T10-01**
- Seed IP contradiction: candidates.js T10-01 says 100.82.235.39, but tailscale status shows that IP is mac-mini-m4 ITSELF; Roamy is roamy/100.89.32.35. War game treats it as a typo (direction 'claimed on Mini, executed on Roamy' is unambiguous) and corrects it explicitly.
- Authoring recon included a live probe on Roamy: booted an interactive claude in a throwaway tmux session (wg-recon-probe), ran one trivial no-tool turn, killed the session. Subscription-authed (david@appydave.com), zero ANTHROPIC env vars — subscription-safe, and fully cleaned up.
- claude is NOT on Roamy's non-interactive SSH PATH — it lives at ~/.local/bin/claude (zsh -lc only). Every remote command in the war game uses absolute binary paths; any future automation (T10-06) must too.
- orchestrator.py's dispatchable() does not filter by executor tag, so a concurrently running local engine could steal the payload ticket from queue/ — handled as Fork F2 (direct-to-running re-author), and noted as a design input for T10-06.
- Roamy's dark-factory repo is 13 commits behind the Mini (clean fast-forward ancestor). War game syncs ff-only and hard-forbids merge/rebase/reset on Roamy (KDD-stream commits live there).

**T2-01**
- This ticket's DoD deliberately excludes C2 closure: the live morning conversation is HITL (David-attended) and beyond a Swagger's verify — a backlog pilot note hands David the first live run; T2-06 (5-day proof) should depend_on this ticket.
- Skill working name is 'producer' (north-star's own C2 role name; no collision found in dark-factory or appydave-plugins) — David may want a persona name (Marshall/Swagger/Samantha pattern); listed as an open question in the spec, rename is cheap.
- v1 is single-project (dark-factory) by David's own 2026-07-04 parking of project #2 (morning-briefing-vision.md); multi-project waits on T2-02/T2-03/T2-04 — executors are fenced off building it.
- Emitted-ticket safety: dry-run tests must never write to engine/store/queue/ (live wake watcher notifies + a running pool would dispatch); the war game snapshots the queue and runs a grep-dryrun guard, since Phase-5 promotion makes the queue non-static during execution.
- Mild contract tension noted: daily-operating-model §2 names mission.md as a briefing source, but no mission.md exists at dark-factory root and digest.py ships without it — the spec is grounded on digest's real 15-key JSON, not the doc's aspirational source list.

**T2-02**
- switchboard and watchtower (plus appyradar-sentinel/-sentinal, suborch-demo, 6 client repos) are absent from locations.json — the register-every-new-app standing rule is being violated by the factory's own apps; worth a David-visible note beyond this ticket
- T2-07 (locations.json conflation fix), T2-04 (digest-over-activity), and T2-10 (brains mtime sweep) all border this ticket — war game hard-fences all three out; T2-10's premise is partially stale since brains IS one git repo (verified), so git-log + dirty-count already covers it coarsely
- docs/morning-briefing-vision.md exists in TWO copies (dark-factory/docs + project-digest/docs) with no declared canonical — this war game annotates only the dark-factory copy and defers the twin to T2-04
- the deferred-ticket idiom (status:deferred sitting in queue/) is used for the follow-on promotion ticket, mirroring the 20260704T0630Z precedent; if the engine's kind-filter/queue semantics change, that ticket could be dispatched pre-ratification (its prompt self-parks as a guard)
- ~/.config/appydave/ contains ~200 locations.json/bank-reconciliation backup files — unrelated config hygiene debt observed during recon

**T2-03**
- Contradiction handled, David should sanity-check: the deferred queue ticket carries his 2026-07-04 ruling 'premature — needs universal activity registry first'; this war game closes it as superseded on the strength of the 07-06 portfolio ratification (path-map T2 seed explicitly says it unblocks that ticket). Move 6 preserves the deferred_reason and re-points the registry vision at its own T2 ticket; assumption ledger item 1 parks the closure if a post-07-06 re-deferral is found.
- Project #2 defaulted to omi-fetch per the original ticket's own 'next most actively-worked repo' rule (14 commits since 06-20, in app-registry, clean README first-paragraph goal) — David never picked one; Fork F1 Route B falls back to app-registry and any triage-time pick by David overrides both.
- Mild overlap with T1-04 (C4 return leg): both tickets edit project-digest, but on disjoint files (T2-03: digest.py + needs_you.py + configs; T1-04: shipped.py + renderers) — dark-factory.json is touched by both (different keys, additive). Safe in either order; both war games carry race-detection recon and abort-on-half-landed-edits.
- Scope note: needs_you.markers wiring is included because the original queue ticket explicitly mandates following extension-notes' ranked list ('wire that first when adding project #2') — but omi-fetch has no backlog, so the wiring is verified against dark-factory's config (synced to built-ins to preserve recall), not against project #2.

**T3-01**
- Backlog item 2026-05-18 names stale eval files: agent-skills-osmani__skill__code-review-and-quality.md and both compound-engineering code-review evals don't exist on disk — war game routes the executor to the two real files (hyphen-named osmani evals) and records the rest as a finding
- David's review-blind-hunter/edge-case-hunter/review-code-quality are now thin aliases single-sourced in code-quality/references/lenses.md (post-dates the May-18 brief and the distillation); lenses.md added to the voice-anchor set — if lenses.md already carries depth calibration + confidence rubric, the canonical is partially redundant as cargo (assumption 4, report finding)
- provenance-spec.md self-contradicts: its example uses source_repo 'compound-engineering-plugin' but its field rule requires matching research/recon/<repo>.md (= 'compound-engineering'); war game follows the field rule and reports the spec bug
- Session split honored: T3-01 ends at rewrite_status 'in-style' with an HITL handoff — T3-02 (voice-review+ratify, in candidates.js, not yet authored) is the required follow-on; if T3-02 never gets promoted the REPORT.md Session-2 checklist is the manual fallback
- tools/verify-provenance.py and tools/style-check.py (T3-03/T3-04) don't exist yet — validation is the manual checklist; war game auto-upgrades to the validators if they land first (no hard dependency)

**T3-02**
- depends_on id for T3-01 is INFERRED (parallel authoring) — the war game gates on T3-01's disk artifacts instead, but reconcile the ticket id at Phase 5 promotion
- Contradiction found: the 2026-05-18 backlog item's execution hint puts SKILL.md-writing in session 2, while decisions.md Q9 locks drafting into session 1 (T3-01); this war game follows Q9 and aborts (A1) rather than absorbing T3-01 scope if the draft is missing
- This ticket only works with a human in the loop: if the Phase 5 promotion script dispatches it ungated, the run intentionally ends parked in running/ as failed(timeout) with the needs-decision file alive — drain-order doc should either dispatch it with --hitl or expect the two-pass lifecycle
- Backlog-item close (Step 11) may be claimed by T3-01's war game too — T3-02 handles both locations conditionally, but check for double-close at promotion
- Engine hazard inherited by design: a corrupt decisions/ file silently defaults to approve in orchestrator.py (~617-619); the war game forbids the executor from defaulting and aborts A3 instead, but David's manual echo answers remain exposed to the engine-side default on gated runs

**T3-03**
- canonical/ is empty (INDEX.md only, verified 2026-07-06) — the validator can only be proven via self-test fixtures in temp dirs; a fork (F1) handles the race where T3-01's first ingestion lands artifacts before this executes, including an informational park if a *ratified* artifact fails its own spec.
- Spec ambiguity pinned as a default: provenance-spec.md allows multi-file origins in _source/ subfolders but never says what verbatim_copy holds then — the war game pins directory-tolerant R3/R4 semantics (flagged in the assumptions ledger with a cheap false-branch).
- Scope split made explicit: ingestion-workflow.md Step 8 mixes provenance checks (items 1-3, this tool) with SKILL.md style checks (items 4-8, the unbuilt tools/style-check.py) — style-check is fenced out as its own T3 ticket; later tickets citing 'Step 8 automation' should not assume style checks are covered.
- Exit-code contract (0 pass / 1 fail / 2 usage) is nowhere specified in docs — this ticket pins it; T3-01 and later ingestion tickets should gate on it and grep the machine-readable 'FAIL <artifact> R<n>:' line format.

**T3-04**
- Contradiction found INSIDE canonical-form-spec.md: frontmatter template says argument-hint 'Omit if none' but the ratification checklist says 'argument-hint (or noted N/A)' — resolved as WARN-not-FAIL in Assumption 2; David can flip a constant if he disagrees
- Scope boundary with sibling T3-03 drawn explicitly: style-check does existence-only for provenance.json/_source; the 8 provenance content rules belong to verify-provenance.py — if David wants one merged tool, the split is additive and mergeable
- No depends_on despite T3-01/T3-02/T3-03 being neighbours: the tool builds and proves itself against tempdir fixtures; Fork F1 handles T3-01 racing ahead (report-only run), Fork F2 handles T3-03 landing first (docs wording)
- Docs promise the tool in two places since 2026-05-18 ('when written' in canonical-form-spec.md line 5, 'until ... exist' in ingestion-workflow.md step 8) — both get surgically updated as part of the ticket

**T3-05**
- Contradiction: research/INDEX.md says the 14 questions 'require David's call before Phase 2', but Phase 2 ran and ~30 distillations shipped on implicit defaults — this ticket codifies them retroactively
- Question E's premise is false: 'Alec' is alex.md (Workflow Architect) per recon/poem.md role confirmation — nothing is missing from POEM
- Corpus drift inside research/ itself: artifacts.jsonl holds 1,150 rows vs INDEX.md's 1,100/13-repo stats; 'david-local' (30 rows) and 'matt-pocock-skills' (18) are absent from its repo tables — logged as T8 material, not fixed here
- Because research/ is read-only (CLAUDE.md hard rule), the questions table will STILL point nowhere after this ticket ships; the answers doc lands in docs/ and the gap is handed to T8 truth-reconciliation
- OPEN-class defaults (H, K, M, N) are Fable-proposed and unratified — the doc is PROVISIONAL until David bulk-ratifies at triage, though provisional defaults already unblock T3-06+ distillation tickets

**T3-17**
- Scope nuance vs the brief: David's design labels can only calibrate the DESIGN judge (design-lint / taste class). L1 census and L2a triage judge TEXT artifacts and have no human-labeled set — the war game ships the reusable protocol/scorer but explicitly does NOT claim those judges calibrated (Assumption 5, residual gap noted in CALIBRATION.md).
- 'Pin judge model+version' collides with the no-API/no-headless rule: the strongest available pin is the interactive session's model string + JUDGE-PROMPT.md sha256, not an API snapshot id. A true API-pinned judge is a metered-billing decision, offered as option (c) in the Fork F1 Route B park.
- David's own tier bar drifts between rating sessions (round-03-result.json: 47 loves -> 1) — exact-tier agreement has a hard ceiling, so weighted kappa + adjacent agreement are the primary metrics per round-03's own recalibration note.
- Truth-set vocabulary caveat: round-01 uses good/meh/shit, round-02 uses love/good/average with 74 free-text labels — round-02 is pinned as truth (Fork F2 handles any newer full round appearing before execution).

**T5-01**
- Contradiction: scaffold defaults 5060/5061 (Chrome ERR_UNSAFE_PORT) vs apps.json's registered allocation 5080/5081 — war game aligns everything to 5080/5081
- apps.json watchtower record is stale: path points inside dark-factory (~/dev/ad/apps/dark-factory/apps/watchtower) and url says :5060 — Move 7 fixes both
- Scope reframe: 'scaffold RVETS/AppyStack' became verify+finish, NOT re-scaffold — apps/watchtower repo already exists on github (appydave/watchtower); re-running create-appystack would be destructive (Assumption 1 parks if David wanted fresh)
- Tension recorded, not resolved: constellation marks watchtower build_target=kbde-extension while Q6 says real web app — charter treats it as standalone-now/KBDE-mount-later (Assumption 3)
- Watchtower missing from locations.json and ad/CLAUDE.md despite the register-at-birth standing rule — registration folded into this ticket (jump alias japp-watchtower proposed, David's naming wins)
- Charter home docs/watchtower/ carries 16 mostly-superseded v0 files and a pending RE-BUCKETING move plan — executor is fenced off from executing those moves and from implementing the census-era spec.md

**T5-07**
- Contradiction found and folded in: docs/comms-flow.md and docs/harness-evaluation.md still say the HITL gate 'lives only in the POC / not yet in dark-factory's real Swaggers' — false since 2026-07-04; the gate is in engine/orchestrator.py (~L57/70/526/599-633) with empty needs-decision/ + decisions/ dirs on disk. The note records this in a docs-lag ledger for T8 rather than fixing those docs.
- Sequencing risk: T5-01 (Watchtower charter+scaffold) is also NOW-bucket; if it drains before T5-07 the charter may coin vocabulary first. Recommend promoting T5-07 ahead of T5-01 in the Phase-5 drain order — Fork F2 handles the race if it happens anyway.
- Cross-repo write: Move 5 makes a fork-guarded one-line README edit + commit in the separate apps/watchtower repo (only if still the clean 1-commit stub 1f4d5e9; remote unverified, local commit suffices). Skippable without failing the ticket.
- Curation verb drift discovered: docs/watchtower/plan.md says discard/rerun/improve/promote, spec.md AC-1 says Accept/Rerun/Promote/Kill. Deliberately recorded-not-resolved — T5-05 owns the verb-set decision.
- Bonus finding: engine/status.py has zero awareness of blocked HITL tickets (grep 0 hits) — captured as a follow-on one-liner in the note, not built here.

**T6-01**
- Contradiction found: the empirical collision fixes six-app-eval/path-map call 'landed' exist only in the appydave-plugins dev repo (v6.1.0); the live cache serves v5.9.1 without them — the fixes are currently invisible, the exact class this ticket targets. The war game closes this gap as Move 4.
- The 0754317 precedent put its 'Known name collisions' ledger note in skills-registry/SKILL.md, which has since been archived to _archived/appydave-skills/ — the sweep report becomes the collision ledger; war game forbids resurrecting the archived skill.
- Scope governor added (Fork F2): if >5 new collisions are confirmed, only the 5 with running/active apps get fixed and the rest are marked collision-deferred in the report — an S ticket should not spree-edit 12 live skill descriptions before David sees the matrix.
- ~/.claude/skills is not a git repo — any pointer fix applied there has no commit trail; the war game requires quoting such diffs verbatim in the report.
- App-universe assumption flagged: constellation.json (40 apps) is taken as the universe per the brief; ~/dev/ad/apps/ contains dirs absent from it (kdd-bridge, yt-mirror, suborch-demo) — report notes uncovered ids rather than silently expanding scope.

**T6-02**
- MCP surface shrinks at cutover: 'a' exposes 13 tools, 'e' only 9 — pause/resume/trigger_collection, investigate_machine, add/remove_machine disappear (gains disk_archaeology + refresh). Recon found zero runtime consumers (only a cowork spec doc mentions them), so the war game defaults to accepting the reduced surface with an abort-to-needs-decision if the executor's re-grep finds a real consumer.
- 'e' is functionally behind 'a' in the command layer by design (new lineage, not a port) — if David expected feature parity, that's a scope decision before this ticket runs.
- Legacy repo is 113 files dirty since 2026-04-28; the war game commits the whole tree as an archive snapshot after a secrets scan (abort A3 on any hit). Folder deletion and the non-git appyradar-sentinal-safe backup are explicitly deferred to David.
- T6-03 (blind-to-Roamy) should list this ticket as a dependency — fixing fleet hostnames against the retiring 'a' repo would be wasted work; this war game deliberately carries the stale 5-machine config across verbatim.
- constellation-map.md and app-registry already describe 'e' as 'the keep' — docs agree with this migration; app-registry needs no hand-edit (its probe self-refreshes live status).

**T6-03**
- mac-mini-m2 is likely a SECOND false-offline of the same class — Tailscale shows it up but its ssh alias resolves via mac-mini-m2.local (mDNS); not covered by any T6 candidate I saw — follow-up ticket candidate
- The 'appyradar-sentinel' MCP server in ~/.claude.json is backed by the OLD 'a'-spelled repo (appyradar-sentinal/src/access/bindings/mcp.ts) — known name trap, fenced out of scope in the war game
- app-registry names this same machine a THIRD way ('macbook-pro-2', Switchboard entries) — naming debt flagged in executor notes, out of scope
- No a-to-e migration war game existed in backlog/wargames/ at authoring; T6-03 deliberately carries no depends_on and fixes the running deployment either way — if a sibling agent authored the migration ticket in parallel, sequencing is safe because T6-03's recon forks (F2/F3) detect a migrated world and park to needs-decision
- sentinel.config.json is gitignored per-deployment, so the live fix is uncommittable by design — evidence trail lives in dark-factory engine/store/results/ instead

**T6-10**
- Contradiction with the candidate brief: the 'decide' half is already done — omi-sync was retired 2026-07-06 ~15:02 by the loose-ends run (D3 marked DONE); launchctl confirms unloaded. The war game is reframed as verify-retirement + drain-the-debris + restore-the-sync-leg.
- Real damage found: cross-machine OMI sync has been dead the whole time omi-sync was failing — raw-intake ahead 41/behind 3 (Roamy IS pushing), 30 stranded untracked omi/*.md transcripts (06-14 to 07-03) never committed, 11 modified June-14 files (the original rot cause) left for David to adjudicate via the report.
- Scope call needing David's eye at triage: the war game patches omi-fetch pulse.py with a guarded push-with-catchup git_sync leg, which amends that app's DELIBERATE documented 'never pushes' design law. Justified in Assumptions #3 (the push owner is retired; David's global auto-push rule) and revertible in one commit — but it is a design-law override.
- Mild seam overlap with T6-01 (name-collision sweep): both touch omi-fetch's README, different sections; T6-10 explicitly fences appydave-plugins (T6-01's seam) out of scope. No hard dependency either way.

**T7-05**
- Cross-ticket interaction with T1-10 (store retention): that war game hard-aborts on unknown engine/store/ dirs, so written digests are locked to engine/digests/ OUTSIDE the store — if David ever wants them inside store/, T1-10's policy table needs a matching edit.
- Adjacent seams deliberately fenced off: T1-04 owns project-digest's lib/shipped.py done-feed and wake.py done-watcher; T2-05 owns the needs-you feed — if either lands first it does NOT trigger the overlap abort (per-project briefing enrichment vs factory-wide day rollup), and the war game says so explicitly.
- Settle-time basis is file stats (results mtime, else max mtime/ctime of the done file) — verified sound on the real store today, but a fresh git clone resets file times and would dump all history into 'today'; Fork F1 downgrades to ticket-field timestamps with a visible header note.
- Local-calendar-day window (David is UTC+10) and the tool/flag names were never put to David — both flagged as assumptions with one-line-change false branches, not parking matters.

**T7-10**
- This ticket edits David's tracked appydave-plugins repo (shelly + mochaccino SKILL.md, plugin.json bump 6.1.0→6.2.0) — dark-factory CLAUDE.md calls promotion-to-plugins 'a separate decision'; the war game treats decisions.md Q9 (2026-07-06) as that decision and includes an abort if a later reversal note is found.
- design-lint README claims an out/lint-v5/ correctness pass (2026-06-15) that does not exist on this machine — only out/lint and out/lint-v4 are on disk; logged as a do-not-chase assumption (likely Roamy or never committed).
- The 2026-06-10 placement-question backlog item still says 'decision owner: David, do NOT auto-rectify' — superseded by Q9; the war game closes it as resolved-by-Q9 rather than reopening the question.

**T8-01**
- Scope grew by one file, deliberately: engine/docs/ENGINE-NOTES.md (harness-evaluation's own as-built companion) itself lags — its auto-wake row says 'Not built' but engine/wake.py + launchd plist + bin/factory-wake exist (disarmed). Fixing it is Move 4b; flagged as Assumption 3 with a one-hunk revert path if David rules it out.
- Contradiction found during recon, reported not fixed: omi-fetch's enrichment engine (lib/enrich.py) shells out via `claude -p` — the no-`-p`/metered-billing law was written for engine dispatch, but David may want this reviewed; the war game records it as an observation only (Assumption 4).
- engine/store/queue/.CONVENTION.md is also stale (says orchestrator.py does NOT filter by kind; orchestrator.py:195 now skips external-research tickets) — left out of T8-01's scope, listed for the executor to note in REPORT.md as a finding; may deserve its own micro-fix or folding into another T8 ticket.
- Recon confirmed six-app-eval items are a mixed bag — status.py, VERIFIERS (3 entries), omi-fetch --search/--since/--signal + claude-cli enrichment + skill collision pointer, kdd-viewer query.py all SHIPPED; project-digest --list (ticket still sitting in engine/store/queue/) and engine/find.py genuinely STILL OPEN — so the addenda must be honest deltas, not a blanket 'all done'.

**T8-02**
- CLAUDE.md's opening charter paragraphs are ALSO stale (still frames the repo as pure canonical-ingestion + active YLO thread, contradicting README's Path-1 banner and Q5's YLO park) — deliberately fenced OUT of T8-02; make sure the T8 truth-reconciliation ticket owns it or it falls through the cracks
- docs/INDEX.md line 41 and docs/dark-factory-living-system-spec.md (lines 6, 323) also reference phase-b-next-steps: INDEX's stale descriptor is fixed in-scope here; living-system-spec's contextual mentions are verified-and-left-alone (documented in Move 4)
- No other T8 war games existed on disk at authoring — if a sibling T8 ticket also claims CLAUDE.md or the phase-b banner, the race is handled via Recon 3 + Fork F1/Abort A2, but avoid scoping two T8 tickets onto CLAUDE.md at promotion time

**T8-03**
- Personas are still LIVE concepts inside POEM (ylo-to-poem-blueprint.md discusses Penny extensively) — the war game fences the retirement to architecture.md only; touching POEM docs would violate Q5 (parked).
- Persona mentions also exist in workflow-tool-authoring-notes.md (R14 row), spikes/blackboard-mcp/, a 2026-05-18 backlog spec, and a mochaccino brief — left untouched as historical/POEM records; results JSON will flag any that actively mislead as follow-up candidates.
- Potential same-file collision with a future T8 truth-reconciliation ticket: architecture.md section 7 (M4 Pro Warehouse Keeper) is also stale but explicitly OUT of this ticket's scope — if both tickets run concurrently they edit the same doc; sequence them at promotion time.
- chatgpt-brief.md:99 already states the supersession ('Swagger is the daily interface. Not Penny, Alec, or Oscar directly') — architecture.md is the only doc still making the stale claim.

**T8-08**
- June-15 claim partially stale: beauty-and-joy, appydave-plugins, kiros-hq, and deckhand (local) are all resolved on mac-mini-m4 — but deckhand on Roamy still has NO remote + 28 dirty files (verified live over ssh 2026-07-06); that's genuinely at-risk work.
- Scope grew truthfully: '16 dirty repos' is now 48 on mac-mini-m4 (incl. v-appydave at 306 dirty entries, prompt.supportsignal at 158). The war game keeps size S by making the deliverable a verdicts report + safe pushes only — the actual cleanup is David's decision list, not this ticket.
- 4 repos have no remote at all today (digital-stage-summit-2026, screentour, bank-reconciliation, brain-cowork-upgrade) — remote creation is fenced as a David-go setup action per his standing preferences; the ticket parks it as needs-David verdicts, never runs gh repo create.
- 5 locations.json paths point at nothing (registry drift) — reported under registry-drift verdict; registering them is a separate ticket per the register-every-app standing rule.
- Assumption: the June-15 machine-wide scan ran on Roamy (inferred from handover context, unproven); the war game makes this immaterial by superseding it with a fresh two-machine sweep.

**T9-02**
- Scope note: brief said 'wired into consumer.py' but the failed/needs-you event kinds don't exist yet — orchestrator.py (verified line 638) emits only job.completed; the war game adds 5 anchored one-line emissions there, deliberately skipping the non-terminal retry re-queue path
- Contradiction found: docs/comms-flow.md line 139 claims attention alerts have 'zero implementation' — false since consumer.py's Glass chime shipped; left alone (T8-01 truth-reconciliation seam), noted in the war game's Locked context
- Seam adjacency, not dependency: T1-01 (HITL live proof) runs the orchestrator live — Fork F2 handles collision with any live pool run; conversely T1-01's run will emit the first REAL job.needs_decision after this lands (live-fire proof deliberately delegated there)
- Taste calls made by Fable, flagged in the Assumptions ledger: the four sound picks (one-dict-line to change), 'declined' classified as failed chime, and omi-fetch new-capture events reclassified Glass->Pop (behaviour change for the only current 'other' producer)

**T1-05**
- Marshall SKILL.md (72 lines) still points at experiments/watchtower-engine/ + a Switchboard/AngelEye preflight that would hard-block or rabbit-hole the drill — the war game patches it additively (sanctioned by decisions.md Q4) with Abort A3 if the file has been rewritten; David may want eyes on that patch
- David's speaking leg cannot be automated: the ticket's done-bar is staging + rehearsal + drill card, and the C5 proof doc flips to PROVEN only when David runs the drill — so C5 closure needs ~10 min of David-present time after this ticket lands
- Nested-engine hazard confirmed in warm_pool.py: workers are tmux df-worker-1..N, so an engine-dispatched executor must never run orchestrator.py — the war game hard-fences this and routes the live engine pass to David/armed-wake
- orchestrator.py sends NO notification on job completion (only HITL/BACKOFF) — C5's told-leg is honestly scoped to wake queue-notify + consumer.py chime + status.py + Marshall surfacing; the always-on return leg remains the separate C4 ticket
- If Phase 5 promotes many war-game tickets into queue/ before David runs the drill, the drill's engine pass drains them too — handled as drill-fork D-F3 (run anyway, evidence keyed to ticket id) but worth sequencing awareness

**T1-06**
- Self-hosting hazard: if Phase 5's promotion drains this ticket through the engine pool, the executor lands inside df-worker-1 and the live N=3 leg ALWAYS parks (Fork F1 Route B) — the race-harness leg completes but the live-pool leg needs a plain-terminal or solo-run dispatch; consider draining T1-06 outside the pool
- Two simultaneous orchestrator.py processes are unsafe today (worker-name collision: second boot() kills the first's df-worker sessions); the war game records this as a ledger finding, and a future worker-name-namespacing ticket is implied but not in the portfolio
- The live run co-drains any dispatchable tickets sitting in queue/ at execution time (queue scan is global, no test isolation); war game forks on this (F2) but a busy queue at promotion time turns the plumbing test into real work — sequence T1-06 against a near-empty queue
- 6 no-op probe tickets remain permanently in engine/store/done/ per the growing-ledger convention (prefixed wg-t1-06-noop for T1-10's future retention pass)

**T1-07**
- eval-architecture.md's 'Gap A waits on stability-1 traces' is softer than documented: the orchestrator-written audit.jsonl->transcript chain already yields usage + tool_use data (verified on the 2026-07-03 constellation transcript), so T1-07 runs now with T1-08 (stability-1) as a fidelity upgrade fork, not a blocker — depends_on left empty deliberately
- eval-architecture.md's '35+ runs in done/' is stale: engine/store/done/ has 17 tickets and experiments/watchtower-engine/runs/ has 34 — historical done/ tickets are NOT reusable as golden jobs (mostly builder-agent-closed, already-applied one-shot fixes), so the suite uses purpose-built sandboxed jobs instead
- War game asserts a mechanism-derived rule not yet David-ratified: golden replays are top-level-only (never inside a df-worker — tmux name + store collisions); if any future doctrine wants engine-dispatched replays it parks to needs-decision/
- The war game's Move 6 queues a real follow-on build ticket (replay.py runner) into engine/store/queue/ at execution time per ticket-first — if auto-wake is armed by then it will dispatch unattended
- engine/golden/ chosen as the suite's home over tools/ — flagged as an assumption with a clean git-mv escape if David objects at triage

**T1-10**
- keep-days=30 / keep-min=20 defaults are Fable's numbers, not David-ratified — flagged in the assumptions ledger with a false-branch (flags-only change; archive-vs-delete objection parks to needs-decision/)
- consumer.py rebuilds its seen-set from events-consumed.jsonl keyed on (source, absolute path): pruning a consumed-log line while its event file still exists causes re-consumption, and archiving an unconsumed event loses the signal — the policy table hard-codes both invariants plus a crash-safe ordering (file moves before its log line)
- engine/store/ is fully git-tracked, so archiving is live-dir hygiene only (git history keeps everything regardless); gitignoring archive/ would drop files from the index and is deferred to David
- scheduling deliberately out of scope per unknowns-map §B (a live cron is a standing commitment needing explicit go) — retention is manual-invocation only in this ticket

**T10-02**
- Contradiction resolved in-ticket: docs/kill-switch-spec.md §6 says cross-machine halt is 'a natural extension of the Switchboard state plane' but decisions.md Q3 DEFERS that fork (T1-11) — the war game deliberately uses plain SSH file-write and rewrites §6 to match; if David wants fleet control to wait for Switchboard instead, pull this ticket
- Roamy's engine lags origin badly (HEAD 2eae942, no halt.py/wake.py/bin) — its orchestrator today would NOT respect any HALT flag; Move 1's ff-only pull fixes that, but any Roamy-side agent mid-session would hit Fork F1-B and park
- Scope deliberately Roamy-only per Q8: m2/jan/mary and a Roamy-initiated reverse halt are excluded (Assumptions 3+5) — each is a one-line follow-up if wanted
- Broadcast also lands prophylactically: nothing engine-shaped runs on Roamy today (verified), so the round-trip proves flag reach, not a live engine stopping

**T2-04**
- depends_on slug is a guess: T2-02's war game did not exist at authoring time, so I derived wg-t2-02-universal-activity-registry from its candidate title — if the T2-02 author picks a different slug, the engine dependency gate never satisfies; reconcile the string in tickets/T2-04.json during Phase 5 promotion.
- T2-02 is L-size and the spec says L = design-first, so wg-t2-02 may reach done/ having produced only a design, not a runnable registry — T2-04's Recon 1-2 + Abort A1 handle this (park to needs-decision, never build the registry itself), but expect that park unless T2-02 spawns and lands a build follow-on first.
- Scope overlap watch: the deferred engine queue ticket 20260704T0630Z-project-digest-list-and-project-2 (= T2-03's work) also edits digest.py's argparse; T2-04 is written to coexist with or without --list landed, but if both run concurrently on project-digest they will collide on digest.py — sequence them.
- project-digest is its own git repo (appydave/project-digest), so this ticket commits to TWO repos; it also carries a pre-existing modified view/dark-factory.html (regenerates on every run, even --no-write) which the war game whitelists as expected.

**T2-05**
- No LINEAR_API_KEY exists on this machine (verified: env, ~/.config/appydave/, dark-factory/.env, project-digest tree) — plain-Python digest cannot use the claude.ai Linear MCP; ticket ships Linear degraded-pending-key with a parked provisioning question unless David drops a key first
- depends_on wg-t1-04-c4-return-leg is file-collision serialization, not functional: both tickets edit projects/dark-factory.json + all three project-digest renderers; concurrent dispatch would conflict (Fork F3 covers out-of-order dispatch)
- Ranking call made without David: engine needs-decision candidates score 110 (above the 100 title-marker ceiling) so a blocked worker deterministically tops NEEDS-YOU, urgent Linear issues 85 — flagged in the assumptions ledger as one-line constants if he objects
- Verified free-standing question files in engine/store/needs-decision/ are inert (orchestrator only watches its own live-agent tids; status.py/wake.py never read the dir) — safe for both the abort protocol and the park-and-proceed Linear question

**T2-06**
- depends_on slug 'wg-t2-01-ba-agent-build' is a GUESS — T2-01 is authored by a parallel subagent and its exact ticket name is unknowable from here; reconcile the slug at Phase-5 promotion. The war game hedges by gating on the BA-agent ARTIFACT (Recon 2 globs wg-t2-01* in done/ + .claude/skills/) rather than the ticket id.
- engine dispatchable() does NOT enforce depends_on (verified, orchestrator.py ~line 183) — if the promotion script queues T2-06 before T2-01 lands, it will dispatch and immediately park via Abort A1; harmless but wasteful. Promotion script should sequence.
- T2-03's project-#2 ticket (20260704T0630Z-project-digest-list-and-project-2.json) sits in the queue marked status:deferred with David's explicit 'premature — needs activity registry first' note, yet candidates.js lists T2-03 as bucket-now. Contradiction: promoting T2-03 un-defers something David deferred 2 days ago. T2-06 handles either outcome via Fork F2 (multi- vs single-project protocol) but the T2-03 author/promoter should surface this to David.
- The proof week itself is David-driven and cannot be guaranteed by any ticket — the war game converts absence into data (stall rule parks a needs-decision after 2 consecutive missed days; ≥4-of-5 PASS bar tolerates 1 miss).
- A subtle live-data trap is encoded as a hard rule: any real (non --no-write) digest run bumps briefing_n and resets the since-window, eating Day 1's SINCE delta — the harness rehearsal must be read-only throughout, and mid-week stray runs are detectable via day-log briefing_n jumps.

**T3-06**
- CANDIDATE PREMISE STALE — and it propagates: T3-07..T3-12 all say 'distill <cluster>' but EVERY named cluster already has distillation files on disk (system-comprehension 5, spec-writing 6, verification-validation 6, planning 7, delivery-readiness 5, code-implementation 4). David should re-scope those siblings to the same eval-gap-fill + winner-verification shape before running them.
- dark-factory CLAUDE.md points to a dead path for the catalog skill: ~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/ does not exist; the skill was archived to ~/dev/ad/appydave-plugins/_archived/appydave-skills/dark-factory-catalog/ (procedure refs capability-evaluate.md / capability-distill.md live there). T8 truth-reconciliation material.
- Distillation frontmatter ids drift from corpus ids (e.g. compound-engineering:skill:ce-best-practices-researcher vs corpus :agent:; gsd:command:gsd:pause-work vs :command:pause-work; quoted ruflo ids with spaces) — war game handles it via normalized matching, but any tooling that joins distillations to artifacts.jsonl will hit this.
- research/evaluations/ has a split filename convention (16 __-form vs 72 hyphen-form, same mtime) — war game standardizes new files on __-form; a rename/normalize decision is open.
- Ticket deliberately does NOT depend on T3-05 (14 corpus questions): kc slice membership and primary-artifacts-only scope were locked 2026-05-16, and the distillations already exist; Recon 7 makes the executor pick up any T3-05 rulings that land first, with an abort if one re-scopes the cluster.
- Scope honesty: worklist covers the 111 distillation-cited sources, not all 203 slice members — the ~90 artifacts the 05-18 pass deliberately excluded stay un-evaluated unless David orders full-slice coverage (called out in the report move).

**T3-07**
- Candidate premise was stale: the 180-artifact cluster already has a full distillation pass (research/distillations/system-comprehension-*.md, 2026-05-17, status draft). The same is true of knowledge-capture (T3-06) and spec-writing (T3-08) — whoever authors those should reframe the same way rather than redistilling.
- understand-anything plugin (installed v2.7.5, 8 skills; upstream at ~/dev/upstream/repos/understand-anything, SHA 470cc01) entered David's stack WITHOUT ever being reconned into the corpus — no research/recon/understand-anything.md exists. The war game surfaces this as a finding and suggests a follow-up recon ticket; David may want that ticket added to the portfolio directly.
- Living-system spec (docs/dark-factory-living-system-spec.md ~line 132) marks all 76 existing distillations provisional — 'Do not ingest until the cluster's Level 2 is complete'. T3-07 is therefore scoped analysis-only; any ingestion from this cluster must wait on T3-14 (L2a coverage) and T3-21 (provisional sweep policy).
- L2 eval coverage of this cluster is ~3 of 88 evaluation files — thin; quantified as a mandatory report finding.
- Minor contradictions found and handled in-game: distillations INDEX header says 'Distillation files: 4' but 5 exist on disk (cosmetic, recorded not fixed); root CLAUDE.md claims query_brain is an installed CLI but it is not on PATH in this shell.
- Assumption flagged: appending a new distill-phase file to research/distillations/ is treated as a sanctioned append (per CLAUDE.md's append-only rule and candidates.js T3-06's stated target); if David prefers docs/, it is a 2-command undo flagged in the executor's report.

**T3-08**
- Candidate premise contradiction: path-map/candidates.js call spec-writing 'undistilled', but 6 distillation files exist on disk since 2026-05-17 (status: draft). The sibling 'Distill:' candidates T3-06, T3-07, T3-09..12 almost certainly share this stale premise — their distillation files are also on disk; those war games should be re-scoped the same way (validate + eval-cover, not re-distill).
- Stack drift baked into the distillation: requirements-capture winner appydave-plugins:skill:spec-writer is now ARCHIVED (_archived/appydave-skills/spec-writer), while the osmani agent-skills plugin (interview-me, spec-driven-development) is now INSTALLED — the cluster's gap analysis is stale in both directions. The resurrect-vs-replace call on spec-writer is left as an explicit contested fork for David, not decided by the executor.
- Rule tension flagged and resolved in the war game: CLAUDE.md calls research/ read-only, but the campaign (Q2 + T3-06's own brief) routes eval/distill outputs into research/evaluations|distillations/. War game treats phase-sourced writes as sanctioned, with an abort (A3) if an execution-time guard rejects them.
- research/evals.jsonl from the living-system spec was never built — markdown files in research/evaluations/ (88, with a 72/16 filename-convention split) are the real store. New evals follow the hyphen majority convention.
- Strict living-system reading requires L2a AND L2b before de-provisionalizing, but no L2b rollout harness exists (T3-15/16) — ticket ships 'l2a-validated' status only and defers the provisional-sweep policy to T3-21; scope risk if David expects full unprovisionalization from this ticket.

**T3-15**
- Contradiction: living-system spec Phase 5 plans the L2b runner as level-2b-rollout-eval.workflow.js (Workflow Tool), but decisions.md Q4 locks everything-through-the-engine — war game pins engine ticket-chain as default with substrate-agnostic task-set/rubric design and routes the final call to David's ratification (Assumption 3)
- Contradiction: living-system spec says L3 distillation REQUIRES L2b complete, yet all 76 existing distillations were written with zero L2b coverage — routed as spec Open Question Q-c with default no-retro-gate (policy belongs to T3-21)
- research/evals.jsonl (living-system spec §7's L2a home) never materialized — only census.jsonl (10 rows) exists; mandated as a REPORT finding for the T8 truth-reconciliation pass
- Scope risk: war game authorizes a 2-line status edit to docs/eval-architecture.md (gap register row L2b unbuilt→spec-written) — sanctioned as the doc's self-described purpose, but flagged since other wargames treat docs/ as report-findings-only (Assumption 4 carries the skip branch)
- New storage home proposed (top-level evals/ dir for task sets + rollouts.jsonl, NOT research/ which is frozen) — proposal only, nothing created; David decides at ratification (spec Open Question Q-a)
- Soft coupling, not hard deps: T3-16 (build) consumes this spec; T3-17 (judge calibration, Gap B) is consumed-by-reference — build plan slice 5 is the only slice blocked on it; F2 fork handles whether T3-01's review-dimensional exists at execution time

**T3-19**
- No wave-2 ratify ticket exists in the candidate list — T3-19 ends at in-style ×3 and hands David a per-artifact Session-2 checklist telling him to clone the wg-t3-02 pattern; David may want to spawn a batch-ratify ticket for the wave.
- truth-trail (a governance origin) has been archived to appydave-plugins/_archived/ since the 2026-05-16 distillation — the war game harvests from the archive path read-only and flags the drift as a mandatory report finding.
- research/distillations/INDEX.md frontmatter says 8 orchestration sub-clusters/files but 9 files exist on disk and the table has 9 rows — frozen corpus, so it's a report finding, not an edit.
- Zero orchestration-cluster evaluations exist in research/evaluations/ (88 files, none match) — this wave ingests on distillation evidence alone; research_sources.evaluations will be empty.
- Governance-and-observability is the riskiest pick (composite 'no single winner', ~200 lines of thin ruflo infra text) — Fork F3 lets the executor ship the wave as 2 artifacts and defer governance with a documented recommendation, which the brief's '2-3 winners' scoping makes a success, not a failure.
- Distillation names are used as canonical names without formal sub-cluster approval from David (assumption ledger 2) — rename at Session 2 is a one-line git mv, mirroring the code-review→review-dimensional precedent.

**T3-26**
- Doc contradiction: docs/architecture.md §3 mandates variants/was-canonical-<date>.md on demotion while docs/canonical-form-spec.md §Versioning says 'optionally keep SKILL.md.v1' and never mentions variants/ — the war game follows architecture.md (per the candidate brief) and has David pre-approve a one-line pointer amendment to canonical-form-spec via the PLAN pack
- provenance-spec.md requires version_history[] but defines no event shape; this proof pins a schema (David pre-reads it in PLAN.md §3) — later promotion/rollback tickets and T7's extend-to-SOPs seed inherit it
- Rubric-based promotion evidence (L2b harness, T3-15/16) doesn't exist yet — David sign-off substitutes for this one mechanics proof, explicitly caveated as NOT the standing trigger; if he objects to the substitution itself that is a decline path, not a redirect
- If T3-02 ends DECLINED (its valid alternate outcome) there is no ratified artifact and T3-26 aborts at Recon 1 — scheduling should keep it behind T3-02's actual ratification, not just its ticket completion
- Variant naming (self.v2.md) and mv-on-promotion are unspecced anywhere; the proof pins both as precedent via the procedure doc, overridable by David's verdict

**T5-02**
- T5-01's war game landed in parallel during authoring with exactly the predicted slug — depends_on id verified against its header table; my war game reuses its planned /api/engine/status + DARK_FACTORY_ROOT seam via Fork F1 rather than duplicating it
- Docs-lag-code instance found: watchtower's CLAUDE.md/README name the shared package @appystack-template/shared but the real package is @appydave/shared — war game instructs trusting code
- status.py --json is not perfectly side-effect-free: build_report() calls is_backoff(), which deletes an EXPIRED BACKOFF flag — a 5s poll performs that housekeeping unlink; flagged as Assumption 3 with a needs-decision park if David wants zero write side effects
- dark-factory/apps/watchtower/ (inside the dark-factory repo) is untracked junk (.env/.vscode/node_modules, only .gitignore tracked) that shadows the real ~/dev/ad/apps/watchtower — fenced as a trap in the war game; candidate for a hygiene cleanup ticket
- Store counts are live: T2-03 explicitly moves the one queued ticket to done/ this same cycle, so all verification compares board-vs-ls at the same moment, never fixed numbers

**T5-03**
- depends_on ticket id 'wg-t5-01-watchtower-charter-scaffold' is a GUESS — T5-01 was authored in parallel and its exact slug was unverifiable; reconcile the string at promotion time (the war game's Recon 1 gates on T5-01's on-disk artifacts, not the id, so execution is safe either way)
- ~/dev/ad/apps/watchtower already exists on disk (1 commit, 2026-06-11, 'Initial commit: Watchtower — human control surface over Dark Factory') — T5-01's 'scaffold' move is partially pre-done; its author should treat the repo as existing, not greenfield
- candidates.js names T6-04 (AngelEye revival) as a prerequisite for T5-03, but the brief's 'when revived' wording was honored instead: the war game builds probe-and-degrade with availability-only integration, so T6-04 is intentionally NOT in depends_on
- Watchtower is not registered in locations.json/app-registry — the war game fences registration off as T5-01's charter obligation per the standing register-every-new-app rule; verify T5-01 actually covers it

**T5-06**
- depends_on ticket ids are best-guess slugs — T5-01/T5-07 were authored in parallel; Phase-5 promotion should resolve by T-id against backlog/wargames/tickets/ (existing cross-refs already show slug drift, e.g. wg-t2-01-ba-agent vs wg-t2-01-ba-agent-build)
- needs-decision/ is double-purposed: mid-task gate items AND free-standing parked questions from war-game aborts (T1-01/T2-05 idiom) — the UI renders both as kind gate|parked; T5-07's vocabulary note should ratify this split
- corrupt/partial decisions/<tid>.json silently defaults to APPROVE (orchestrator.py ~617-619) — UI mitigates via atomic rename, but CLI echo writers remain exposed; engine-side fix is a follow-on ticket candidate
- T5-06 writes to the engine store from an app (decisions/ only) — sanctioned by the candidate brief and the engine's own [HITL] log instruction, but if any Watchtower read-only doctrine exists it aborts to needs-decision (A4)
- status.py --json has no HITL section today (verified by running it) — T5-12's API layer will want to absorb the /api/hitl seam later; this build reads the store directly by same-machine path

**T5-12**
- Ordering tension with T5-01 (Watchtower charter/scaffold, bucket NOW): T5-01's brief says 'first deploy serving status.py --json' — if it lands before T5-12 it may grow its own store-reading path; the war game handles this as Fork F2 (converge, or abort if Watchtower ships a competing HTTP API), but at triage David may prefer to promote T5-12 to land first so Watchtower reads the API from day one
- Standing-service commitment: the API ships as a launchd KeepAlive agent (precedent: the wake watcher uses the same pattern), flagged in the assumptions ledger with uninstall-api.sh as the one-command escape — unknowns-map treats standing crons as needing explicit go
- Bind address assumed 0.0.0.0 (Cardputer on LAN + Roamy over Tailscale are named consumers; data is read-only status) — one-line flip to 127.0.0.1 if David objects
- Constellation-map's :7430 earmark ('Watchtower-engine/-board, dark') is interpreted as this API's predecessor row; F1 falls back to :7431 if occupied
- Known quirk documented rather than fixed: build_report()'s is_backoff() auto-clears an expired BACKOFF flag, so the 'read-only' API inherits that one indirect write — identical to running status.py by hand, by design

**T6-04**
- Contradiction: the backlog framing 'hook HTTP transport broke at v2.1.89' is misleading — HTTP transport was tested and REJECTED (curl transport works and is ratified per angeleye docs/architecture/hook-transport.md); the real revival work is re-install + daemon, with version-drift (CC 2.1.201 vs EVENT_MAP reconciled at 2.1.167) as a check-and-report move, not a code fix
- Stale skill hazard: ~/.claude/skills/angeleye-install/SKILL.md (Mar 25) hardcodes 24 events INCLUDING WorktreeCreate — if anyone runs it before this ticket lands, worktree creation breaks machine-wide; the war game rewrites it to consume GET /api/hooks/supported
- Scope call: ticket covers items 1+2 of backlog/2026-06-06-angeleye-refresh.md only; overlay/pruning/MCP/Watchtower-feed (items 3-6) fenced out — the 980MB data dir (registry.json alone is 24MB) makes pruning a real future ticket
- Design decision baked in: daemon runs NODE_ENV=production (UI+API on one port :5051) via removing NODE_ENV from the untracked .env (dotenv override:true blocks launchd env vars); fallback code seam is Fork F1-B — David can flip to dev-mode daemon with a one-line plist change if he objects
- Live-proof mechanism: hooks only bind to sessions started after install, so the war game spawns ONE short-lived interactive claude in tmux (angeleye-wg-probe) as proof — flagged in the assumptions ledger in case even that is considered engine-only privilege
- Evidence of manual runs: data was written 2026-06-29 despite no hooks installed — someone ran the server manually since hooks were removed; harmless but recorded so the executor isn't confused

**T6-05**
- Soft dependency, not hard: AngelEye's server is not running today and the wrapper proxies HTTP — if it won't boot at execution time the war game parks to needs-decision pointing at T6-04 (revival). If David wants certainty, sequence T6-04 before T6-05 at triage.
- ~/.claude.json's appyradar-sentinel entry points at the LEGACY 'sentinal' repo (src/access/bindings/mcp.ts), not the new re-scaffold's src/expose/mcp.ts — confirms T6-02's premise; T6-05 fences it off read-only.
- The new appyradar-sentinel repo's mcp.ts header cites docs/mcp-surface.md which does not exist in that repo — another docs-lag-code instance; T6-05 creates the AngelEye equivalent properly.
- Shape-setting precedent: whatever surface shape this ticket ships (read-only, proxy-over-HTTP, user-scope tsx registration) becomes the template T6-14's constellation-wide sweep copies — assumptions #1-#4 in the ledger flag the calls made.

**T6-07**
- Live-vs-canonical split verified on disk: ~/.claude.json's 'appyradar-sentinel' MCP server and launchd (com.appydave.appyradar-sentinal) both point at the OLD 'a' repo; the 'e' repo has no node_modules, no sentinel.config.json, no snapshots. Handled as Fork F1 rather than hard depends_on because the sibling sentinal→sentinel migration ticket's id was unknown at authoring — if that ticket exists, the promotion script may want to sequence it before/alongside T6-07 (either order works; F1 covers both states).
- Scope nuance vs decisions.md: the assumptions ledger there says reaper stuck-case ownership is 'war-gamed as fork inside T6-08', while this candidate's brief says T6-07 'resolves the ownership question toward AppyRadar'. Reconciled as: T6-07 builds AppyRadar's queryable source (its own charter per docs/appyradar.md §4) and updates the doc, but explicitly leaves the reaper-consumption fork (AngelEye vs AppyRadar vs both) to T6-08. T6-08 should list wg-t6-07-appyradar-process-state in its depends_on.
- This war game commits to a second repo (appyradar-sentinel, remote git@github.com:appydave/appyradar-sentinel.git) plus a dark-factory docs edit — first portfolio ticket I've seen that pushes outside dark-factory; worker needs SSH-agent/push access to that remote.
- 'e' repo README claims '214 tests' and references docs/mcp-surface.md / docs/ssh-batching.md that don't exist in the repo — doc-lag inside the sentinel repo itself; not fixed here (T8 territory), war game relies only on verified files.

**T6-12**
- Candidate brief is stale: '~244/274 remaining' vs disk reality 291/291 enriched (289 claude-cli, 2 stub) as of omi-fetch commit dc6d96b, same day as portfolio authoring — the war game's mission was rescoped to residuals + steady state, not the bulk backlog.
- Rule tension: enrich.py's engine is literally `claude -p` per record, while wargame-spec says no -p/headless ever. Resolved in-game via commit 3d49f66's own rationale ('session auth, not the metered API') + the candidate brief naming this engine; flagged in the Assumptions ledger with a needs-decision false branch if David rules the ban absolute.
- Brief says 'haiku engine' but CLAUDE_CLI_MODEL = 'sonnet' — deliberate switch in commit 3d49f66 (2026-07-06) for signal/synopsis quality; war game locks the model as-is and forbids 'fixing' it back. The _call_claude_cli docstring still says haiku (stale comment, report-only).
- omi-fetch's pulse launchd (com.appydave.omi-fetch, 600s) keeps adding un-enriched rows, so pending count at execution time is unknowable — recon recounts live, with pending>100 as a hard abort (state anomaly).
- Did not verify omi-fetch has a pushable git remote — Move 5's counter-move degrades to commit-only with a note if push fails.

**T7-01**
- Resolved concepts.md's open Q 'code or skills?' as deterministic CODE for the detection half only, grounded in David's own design-resolution row — flagged as Assumption 4 with an additive false-branch (skill wrapper later), and the war game explicitly forbids creating a SKILL.md now (skill-flood + T6 name-collision class: 'daily-review' and 'review' skills already exist)
- Soft overlap with T8 truth-reconciliation: the docs-target briefs will surface exactly the docs-lag-code items T8's campaign fixes — complementary (detector vs fixer), no dependency either way, and the executor is fenced from fixing what the briefs surface
- Memory target's root is a per-machine absolute path outside the repo and not git-tracked — mtime is the only date basis; Fork F2 ships the target with honest-error degradation if the harness relocates auto-memory
- Recurring cadence/trigger wiring is explicitly OUT of scope — tool-registry.md's 'Open decisions' says a live schedule needs David's explicit go; if triage expects a running weekly loop, that is a follow-on ticket
- Demonstration judgment pass is proposals-only and capped at 25 items; it never edits backlog/concepts.md beyond flipping the two status cells that this build makes factually true

**T7-04**
- Placement (docs/kdd/lineage.md, inside Lisa's KDD domain) was never asked in the interview — pinned as Fable's call with a cheap false-branch (git mv + 3 pointer edits); Roamy's cross-machine Lisa commits touch the same dir, mitigated by a merge=union .gitattributes line
- The ticket includes a one-paragraph append to dark-factory CLAUDE.md's End-of-session section (the capture wiring that makes the log get written) — precedent exists (commit f7153d0 added a CLAUDE.md section as routine work) but it's flagged as an assumption with a skip route (Fork F3-B) if David objects
- Soft overlap with T8 truth-reconciliation: Move 3 appends a built-status note to sop-lifecycle.md; if a T8 ticket later rewrites that doc's status lines, the two edits are compatible but whoever lands second should keep both
- engine/store/decisions/ is the mid-task HITL gate, NOT a decision log — the war game explicitly disambiguates so no executor ever conflates the two

**T7-09**
- Advisory-gap honesty: the reap loop polls needs-decision/ ONLY for HITL-gated tickets, so an ungated worker parking BLOCKED_BY_DECISION reads as failed(timeout) in the run report; v1 accepts this (the parked file is the durable question), v2 hardening is deferred to avoid colliding with T1 engine tickets
- Only ~3 of 42 DF-ADRs are 'accepted' — Gate A validates against a mostly-proposed corpus; the war game turns this into a feature (Gate A = the lazy-ratification trigger the decisions index itself prescribes)
- First absorption ticket ships status:'deferred' — David must un-defer it to trigger the first live Lisa run over the ~17 done tickets (wait-for-go on a real spend)
- Shared-surface risk: T7-09 edits engine/orchestrator.py task_prompt() while T1-track tickets exercise the same file — Fork F3 handles drift, but sequencing T7-09 after T1 engine work reduces merge friction
- Lisa-owned checkpoint generalization for PR-based repos (SupportSignal) deliberately NOT built — appydave-plugins is out of scope from this repo; documented as future scope in the design doc
- done/results asymmetry verified (17 done tickets, only 4 results files) — Gate B absorbs from done JSON always, results as optional enrichment

**T8-05**
- CONTRADICTION: decisions.md Q9 (2026-07-06, 'flatten to Lisa format') directly reverses David's own 2026-07-04 ruling recorded in ADR-0044's Revision Log and ADR-FORMAT-SPEC.md ('nesting stays, parsers must speak YAML, flatten rejected'). The war game executes Q9 as the newer ruling and records the reversal append-only, with an abort (A1) if a third, even-newer ruling is found — but David ruled both ways within 48h and may want to confirm the flip was deliberate.
- Stale docs corrected by this ticket: backlog/2026-07-04-kdd-uniformity-findings.md ('3 of 4 divergent') and kdd-viewer's cortex/kbde instance notes ('NO YAML frontmatter') no longer match disk — both siblings now carry flat frontmatter 48/48, likely landed via the Roamy KDD stream.
- One invented value flagged in the ledger: ADR-0044 (the only hand-written, non-reconstructed decision) gets 'provenance: hand-authored' since 'reconstructed-from-sessions' would be false — one-line veto if David wants a different scalar.
- Scope note: the ticket writes to a second repo (kdd-viewer instances/store/view — the uniformity instrument) with its own commit; T8-01's 'don't touch kdd-viewer' fence is read as T8-01-scoped, not global (ledger assumption 3 with a park-if-false branch).

**T8-09**
- Contradiction root-caused: Switchboard binds host-local (src/main.ts:45), so remote curl roamy:5099 always times out — T1-11's authoring recon (EXIT:28) read this as unverifiable/down; when T8-09 runs, T1-11's Fork F1 should take Route A (up on Roamy) and its Branch B resurrection bill shrinks
- docs/comms-flow.md:39 'live on MacBook Pro :5099/:5100' is actually TRUE (verified via ssh 2026-07-06) — it was catalogued as a contradiction in T1-11's ledger; the real defect is the doc omitting the host-local binding
- docs/auto-wake.md:131 cites CLAUDE.md 'Switchboard is DOWN' but dark-factory CLAUDE.md no longer mentions Switchboard at all — dangling citation, left for T8 reconciliation
- Roamy /health showed subscribers:0 lastEventId:0 — the bus runs but nothing consumes it; war game forbids inferring usage history from this
- Both machines at identical HEAD d1506ba with no state-plane recipes — T1-11's premise holds today; T8-09 aborts to needs-decision if that changes

**T9-01**
- Contradiction: docs/human-comms.md (2026-06-01) claims 'the elevenlabs-agents skill exists' — exhaustive search of appydave-plugins, ~/.claude/skills, and plugin caches/repos found no such skill; the candidate brief inherited the phantom. The war game rejects ElevenLabs on structural grounds (metered cost for ambient always-on events, network dependency, API key lives in fligen/server/.env not dark-factory) and bakes kokoro-tts primary / say fallback as the pre-made decision, aligned with the newer canonical docs/comms-flow.md (2026-07-03) which already names kokoro-tts as the voice-out piece.
- Scope call: ticket authorizes the one-time kokoro-tts venv install (~330MB to ~/.kokoro-tts via the skill's own idempotent setup.sh, no sudo — verified against its source) under Q7's voice-IN ruling; if David considers installs out of engine-ticket scope, that assumption is ledgered with a Fork F1 say-only fallback rather than a park.
- depends_on wg-t1-04-c4-return-leg is a soft ordering made hard: T1-04 (high/NOW) edits wake.py and lands the done-watcher this ticket's live test rides; sequencing avoids a same-file race and Fork F2 covers the case where T1-04 landed differently or was parked.
- T9-02 (chime vocabulary, consumer.py) is bucket-NOW and may drain before this ticket — no file overlap (this ticket fences consumer.py off explicitly), but David should expect two separate audio landings, chimes then speech.

**T9-04**
- Real dependency: the war game reuses .claude/skills/producer/emit-ticket.py, which T2-01 builds but has NOT yet executed (only staged) — promotion order must land wg-t2-01-ba-agent first; executor aborts to needs-decision/ if the emitter is absent.
- Naming tension flagged, not resolved: human-comms.md says 'Samantha is the reference, not yet the name' while the candidate title uses Samantha — shipped as working name with christening as open question #1 for David.
- Voice Law tension resolved conservatively: comms-flow §8 makes voice surfaces read-only, so v1 files tickets ONLY via read-back approval in a David-attended session; the always-on auto-consumer (event → ticket, no human) is explicitly deferred as the named upgrade path — if David expected full automation from 'front door v1', that is a scope call to revisit at triage.
- engine/consumer.py already polls omi-fetch events (chime-only) — the war game fences it off as T9-01/T9-02 territory to avoid a seam collision.
- T9-05 (intake home) is a later-bucket candidate, so v1 deliberately creates no intake/ dir; the seen-ledger lives in the skill dir and migrates in one move if T9-05 decides otherwise.

