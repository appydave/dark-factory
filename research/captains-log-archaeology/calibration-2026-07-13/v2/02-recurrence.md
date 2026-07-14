# Recurrence Analysis — Calibration v2

**Purpose**: Cluster near-duplicate fingerprints within each thread to surface what David keeps saying — "said X times over N days", ranked loudest-first.

**For Agents**:
- High recurrence = high felt importance OR a stuck loop. Check `04-loop-registry.md` for which.
- Dual-capture pairs (same conversation on OMI + Plaud) are flagged — they are device redundancy, not independent repetition, but still count as emphasis (David wore both devices and the idea survived both transcriptions).

**Method**: fingerprints are unique per record; recurrence clusters are semantic near-duplicates of the *statement*, scoped within thread.

---

## Ranked recurrence clusters

### R1. "Build Captain's Log as the unified OMI+Plaud viewer/extension" — said **8× over 9 days** (07-04 → 07-13) · captains-log
Fingerprints: `2026-07-04-omi-list-metadata-tagging-ids` → `plaud-2026-07-05-unify-omi-plaud-controller-decision` → `plaud-2026-07-06-captains-log-extension-ticket` → `2026-07-06-captains-log-extension-telemetry-dark-factory-ticket` → `plaud-2026-07-09-captains-log-viewer-kyberagent-hosting` → `plaud-20260712-0642-captains-log-kybernesis-extension-architecture` → `plaud-fd16f65c-captains-log-ingestion-filtering-sdk` → `plaud-eac21d32-captains-log-ux-overhaul`.
The single loudest idea in the corpus. Each restatement ADDS spec (metadata → controller → telemetry → hosting → architecture → durability → UX), so this is productive recurrence, not a stuck loop. 07-06 pair (omi 0907 / plaud 0908) is a dual-capture.

### R2. "Challenge DV retainer proposal must go out" — said **4× over 7 days** (07-07 → 07-13) · client-challenge-dv
`2026-07-07-linda-challenge-dv-coaching-retainer-pitch` + `plaud-2026-07-07-linda-challenge-dv-consultation` (dual-capture) → `plaud-1ea12ad5-challenge-dv-fde-retainer` → price revision in `plaud-eac21d32-captains-log-ux-overhaul`.
STUCK recurrence: the action ("send Linda the proposal") has been restated since 07-07 without evidence of sending; the price changed twice on 07-13 alone ($3,300 → $2,750 incl GST). Start date 15 July makes this urgent.

### R3. "Stand up a KyberAgent on Roamy to watch/learn Kybernesis" — said **3× over 8 days** (07-06 → 07-13) · kyberagent-pilot
`2026-07-06-kyberagent-doc-watcher-roamy-setup` + `plaud-2026-07-06-doc-watcher-kyberagent-roamy` (dual-capture) → `plaud-3278d754-kyberagent-learning-agent-roamy`.
STUCK recurrence: "this weekend" (07-06) came and went; 07-13 restates the same intent, scope-inflated (doc-watcher → whole-system learning agent + Ian/Martin change reports). Companion sub-theme said 2×: "work out how to talk to KyberAgent from Claude Code."

### R4. "The Extension SDK must provide host-mediated LLM access + scheduling" — said **3× over 8 days** (07-05 → 07-13) · kyber-extensions/captains-log
`plaud-2026-07-05-extension-sdk-tagging-scheduling-gaps` → `plaud-20260712-0642-...` (ticket missing host capabilities, daemon-managed cron) → `plaud-fd16f65c-...` (align with SDK "once publishable").
Structural dependency recurrence — Captain's Log keeps hitting the same platform wall.

### R5. "Control Gling programmatically instead of living with its UI" — said **3× over 8 days** (07-04 → 07-11) · gling-automation
`2026-07-04-gling-opensource-video-editing-research` → `omi-2026-07-11-gling-programmatic-control` → `plaud-20260711-1627-gling-electron-mcp-injection`.
Recurrence with a pivot: replace-it (07-04) → inject-into-it (07-11). The 07-11 pair is a same-day double-statement — renewal charge triggered renewed intent.

### R6. "Smart contracts as verifiable end-of-work rubrics" — said **3× over 3 days** (07-07 → 07-09) · agent-verification/ai-meetups
`2026-07-07-smart-contracts-dual-loop-north-stars` → `2026-07-07-kdd-smart-contract-rubric-verification-peer` → `plaud-20260709-1533-tony-coworking-smart-contracts-joy-sites`.
Idea gaining conviction across three different peers; converged on "contract + rubric at end of a unit of work" for Dark Factory evals.

### R7. "Lisa is misbehaving / must be scoped" — said **3× over 4 days** (07-04 → 07-07) · kdd-lisa
`2026-07-04-kdd-bridge-clarity-tickets-gemini-deprecation` (partially) → `2026-07-04-lisa-branch-instead-of-learning-doc` → `2026-07-07-lisa-not-customized-per-repo-kdd-scope`.
Corrective recurrence — same class of failure (Lisa exceeding scope) restated; no confirmed fix. Dormant since 07-07.

### R8. "Unify OMI and Plaud processing (one controller, not per-provider)" — said **3× over 7 days** (07-05 → 07-11) · captains-log
`2026-07-05-unify-omi-plaud-local-whisper-groq` → `plaud-2026-07-05-unify-omi-plaud-controller-decision` (same-day refinement) → `plaud-20260711-0733-captains-log-email-youtube-ingestion` (generalizes to N providers).
Feeder of R1; the morning/evening 07-05 pair shows intra-day belief refinement (see 03-decision-drift).

### R9. "The factory writes knowledge but nothing reads it" / KDD read-side gap — said **2× over 1 day** (07-04) · kdd-lisa
`2026-07-04-kdd-bridge-clarity-tickets-gemini-deprecation` (explicit) + echoed in `2026-07-02` Lisa/KDD idea-extraction framing. Unresolved, high-leverage.

### R10. "Dark Factory must control/understand KyberAgent" — said **2–3× over 4 days** (07-09 → 07-13) · dark-factory/kyber-extensions
`plaud-20260709-0728-dark-factory-kyberagent-control-surface` → `plaud-20260710-0721-dark-factory-where-does-code-run` (adjacent) → `plaud-a93414d0-extension-builder-feedback-loop` (agentified version).

### R11. "Plaud refresh-token brittleness needs automating" — said **2× over 2 days** (07-12 → 07-13) · captains-log
`plaud-20260712-0714-plaud-refresh-token-workaround` → automate-via-Playwright action in `plaud-eac21d32`. Escalating from "easy re-fetch flow" to "fully automated".

### R12. "Thumbnail generator micro-app + prompt TUI" — said **2× over 1 day** (06-30) · recipe-thumbnail
`omi-2026-06-30-0801` → `omi-2026-06-30-0814`. Burst then silence — 13 days dormant. Oldest un-progressed build intent in the corpus.

### R13. "Extensions are too thin / must serve real usage" — said **2× over 3 days** (07-04 → 07-07) · kyber-extensions
`2026-07-04-thin-extensions-usability-critique` → `2026-07-07-extension-doc-review-panel-mount` (enrichment continues). Quality-bar recurrence.

### R14. "Affiliate inbox triage" — said **2× over 2 days** (07-12 → 07-13) · misc
`plaud-e160ba80-affiliate-inbox-triage` → deferred-to-Jan/Mary in `plaud-eac21d32`. Deliberately parked, not stuck.

---

## Dual-capture pairs (device redundancy, flagged not double-counted)

| Date | Topic | OMI record | Plaud record |
|------|-------|-----------|--------------|
| 07-06 | doc-watcher on Roamy | `...-0904-setting-up-a-chiber-agent-brain` | `...-0904-designing-a-kubernetes-documentation-watcher` |
| 07-06 | Captain's Log extension | `...-0907-captains-log-extension-and-telemetry` | `...-0908-meeting-captains-log-extension-build` |
| 07-07 | Linda / Challenge DV | `...-0953-ai-video-content-coaching` | `...-0959-consultation-linda` |

## Reading

- **Productive recurrence** (spec accretes each time): R1, R4, R6, R8, R11.
- **Stuck recurrence** (same ask, no movement): R2 (Challenge DV proposal), R3 (Roamy agent), R7 (Lisa guardrails), R12 (thumbnail generator).
- Stuck items are precisely what Captain's Log's missing "temporal chain / quest linkage" (07-13, `plaud-7336f864`) would surface automatically — this document is the manual proof of that feature's value.
