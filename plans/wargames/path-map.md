# Path Map — the strategic tracks for the war-game portfolio

**Date:** 2026-07-06 · Phase 0 output of `backlog/2026-07-06-fable-wargame-portfolio.md`
Synthesized from 4 parallel reader passes: strategy docs (12), backlog (34 items + stockpiles),
YLO/canonical threads, engine + constellation + done-ticket history.

## Critical reconciliation: docs lag code

The strategy layer (docs/) says the harness-evaluation promotion plan is unbuilt. The code says
otherwise: warm pool, CAP=3 governor + BACKOFF, HITL gate (wired, unexercised), audit.jsonl,
status.py, kind-filter, auto-wake (disarmed) ALL shipped into `engine/` 2026-07-04→06. Most of
six-app-evaluation's High items are likewise done (status.py, VERIFIERS registry, omi-fetch
search + claude-cli enrichment, name-collision pointer fix). **Consequence for every war game:
recon moves verify current state on disk; never trust a doc's status line.** A dedicated
truth-reconciliation ticket also belongs in the portfolio (Track T8).

## The ten tracks

### T1 — Engine & dispatch spine (finish C3→C5)
The kernel works; its safety systems are built but unproven. Seeds: exercise HITL gate live
end-to-end · prove CAP/BACKOFF against a real 429 · arm auto-wake dispatch leg (WAKE-ARMED
protocol + first live run) · Switchboard SSE trigger v2 (job.queued + Last-Event-ID, the specced
C3 end-state) · warm pool N>1 (2–3 workers under CAP) · C4 return leg ("what ran" surfaced to
David) · C5 one real kind:workflow job end-to-end via talking · golden-job regression suite
(eval-architecture Gap A, needs stability-1 traces) · reaper stuck-case (needs T6 AppyRadar
decision) · kill-on-done fold into dispatch (C3d).

### T2 — Producer / BA agent / morning-briefing chain (C2, the converged frontier)
Three independent docs (06-23 → 07-04) converge here. Seeds: build the BA agent itself
(contract pinned: in=state, process=deep 1-project conversation, out=tickets/specs; internals
open) · universal activity registry (sweep locations.json + brains + client dirs; fixes
locations.json conflation debt) · digest-over-activity (project list from what changed, not
hand-config) · digest.py --list + project #2 onboarding (unblocks the deferred queue ticket) ·
feed layer (engine tickets + Watchtower + Linear into NEEDS-YOU/IN-FLIGHT) · Step-0 briefing →
BA → ticket pipeline proven daily for a week.

### T3 — Canonical ingestion & the eval ladder (Path 2 cargo — ZERO shipped in 7 weeks)
The original charter has produced 0 ratified artifacts from the 1,100 corpus. Seeds: execute
first ingestion (code-review → review-dimensional, open since 05-18; 3 PO decisions have stated
defaults) · build tools/verify-provenance.py (8 rules) + tools/style-check.py · validate
david-style-patterns.md against a real produced artifact · resolve the 14 corpus questions A–N
(or ticket each as a decision war-game) · distill remaining top clusters (knowledge-capture 201,
system-comprehension 180, spec-writing 157…) · L2b rollout harness design (biggest infra gap) ·
LLM-judge calibration against mocha-census human labels (Gap B — cheap, high-leverage, the
calibration set already exists) · DF-8 comparison registry build · L0 scorecard + L2a eval
workflows · ingest.workflow.js transpiler.

### T4 — YLO→POEM consolidation
Probes proven, blueprint unratified (9-item punchlist, 6 open questions). Seeds: ratify
blueprint · build .poem/ in dark-factory, rebuild the 4 YLO workflows in POEM · then freeze +
archive YLO · MCP-store blackboard spike (does it kill the Workflow-Tool I/O tax? gates v2
architecture) · haiku-for-I/O quick win · the 7 cheap open loops (flux-schnell fix, EAV
corrective records, aspect-ratio brief language, /goal-vs-conductor doc, run renames, stray
gallery delete) · POEM-as-Anthropic-plugin repackage · QuickArchitect facade · Agent Engineer
persona.

### T5 — Watchtower & decision surfaces
The glass wall is still a design doc + 1-commit stub. Seeds: decide UI ambition (real app vs
Mochaccino boards + status.py) · curation queue (promote/reject → promotion.yml) · reconcile the
two "decision queue" concepts (curation-at-rest vs mid-task HITL) · kanban/live-agent/live-bus
views · governance visualization (drift/idle/lineage) · Board v6 Map view · Cardputer front desk
stages 1–2 (cheap hardware spike, ready today).

### T6 — Constellation health & discoverability
Six-app-eval's root-cause finding: new tools invisible behind identically-named old skills.
Seeds: finish collision sweep (registry pointers landed; audit remaining pairs) · migrate
running appyradar-sentinal ('a') → appyradar-sentinel ('e') · fix sentinel blind-to-Roamy
cross-machine liveness · AngelEye revival (hook compat, daemonize, MCP wrapper, roll-ups, port
drift) · AppyRadar owns tmux/process state (reaper's stuck-case home — decision needed) ·
capture service (new app vs fold into AppyRadar — decision) · retire-or-fix failing
com.appydave.omi-sync launchd · kdd-viewer query CLI polish · mount omi-fetch KBDE extension
(blocked on external D2) · every-app-exposes-API+MCP doctrine sweep.

### T7 — Self-learning & reflective loops
The "living system" promise. Seeds: inward-pointing SOP pulse (drift detection over the
factory's own workflows) · extend canonical/variants promotion semantics to workflows/SOPs ·
lightweight decision-lineage log (one-liners, not ADR ritual) · daily "what did the workers do"
review digest · tool-usage telemetry (DF-5, AngelEye hooks) · usage-driven skill evolution
(heavily-used→optimize, unused→deprecate) · idea-lifecycle machinery over concepts.md
(staleness + recategorization — the ONE reflective-review pattern, build once apply 4×) ·
Chronicle build-documentary first cut (transcript mining) · KDD structural SDLC gates (David's
stated real direction) · mocha-census bench mode verification + design-lint→Shelly fold.

### T8 — Knowledge & doc truth reconciliation
The docs-lag-code problem, plus hygiene. Seeds: truth-reconciliation pass (update
harness-evaluation/runtime-model/six-app-eval status lines to match shipped engine/) · fix
CLAUDE.md's stale "START HERE: phase-b" activation pointer · retire Penny/Alex/Oscar from
architecture.md (superseded by Marshall/Swagger, never formally killed) · resolve M4-Pro
"Warehouse Keeper" role (real or abandoned?) · DF-ADR nested-provenance flattening (Lisa
uniformity) · KDD Cortex reconcile() unification (needs Cortex host access) · Cortex
re-comprehension at HEAD · repo hygiene: 16 dirty repos, missing remotes/pushes · doc-health
sweep wiring (doc-drift + doc-review report-mode, parked side-quest).

### T9 — Human-comms & physical surfaces
Seeds: audio-out engine decision (ElevenLabs vs system TTS; elevenlabs-agents skill exists,
unwired) · sound-effect vocabulary (done/failed/needs-you) · summary-on-return trigger · Q&A
bot / spoken front door ("Samantha" — intake rule: captures idea → writes ticket, never spawns
a session) · intake physical home decision (backlog/ vs dedicated intake/) · learning.yml
9-layer taxonomy emission (designed, never built, central to intake.md).

### T10 — Fleet & distribution
Seeds: M4 Mini ↔ Roamy worker delegation over Tailscale (SSH+tmux Swagger workers) ·
per-machine Switchboard daemons · cross-machine HALT broadcast (kill switch is per-machine
today) · other minis (m2, jan, mary) as workers · fleet-aware status aggregation ·
dev-inventory revival decision (dead on every machine).

## Portfolio-shaping observations

- T2 is the most-converged near-term thread; T3 is the largest unserved charter; T1 is
  cheapest-to-close (mostly "prove what's built").
- The 4 idle-time governors (T7's reflective loops) are one pattern built once.
- Roughly 30 candidates already exist pre-written across backlog inventory + DF-1..10
  tickets.json + the six-app-eval improvement tables; the remaining ~70 come from track seeds
  above.
