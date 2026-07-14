# Decision Drift — Calibration v2

**Purpose**: Track beliefs/plans that changed across the 101 records, and flag superseded decisions that still LOOK current if you only read the earlier capture.

**For Agents**:
- Never act on a record below without checking its "current belief" column — the earlier capture is a trap.
- Drift here is normal thinking-out-loud; the failure mode is a downstream system ingesting the stale version.

---

## D1. omi-fetch unification: "one skill" → "separate skills, one controller" (SAME DAY reversal)
- **07-05 morning** (`2026-07-05-unify-omi-plaud-local-whisper-groq`, omi): "Rename/unify omi-fetch into a provider-agnostic voice-capture skill covering both OMI and Plaud."
- **07-05 evening** (`plaud-2026-07-05-unify-omi-plaud-controller-decision`, kind=decision): OMI and Plaud **stay separate fetch skills**; a single shared controller owns transcription/tagging/ontology.
- **Trap**: the morning record reads as a directive and is only 9 hours stale. Current belief: separate fetchers + shared controller (= Captain's Log).

## D2. Captain's Log platform: standalone controller → KyberAgent extension → "align with SDK later"
- 07-05: unified controller tool (names to be suggested; no host mentioned).
- 07-09 (`plaud-...-captains-log-viewer-kyberagent-hosting`, decision): host as a **KyberAgent extension** — host-daemon LLM access means "no API/SDK build needed".
- 07-12 (`plaud-20260712-0642`): server foundation re-opened (AppyStack vs what Kybernesis provides); ticket missing host capabilities, refactor later.
- 07-13 (`plaud-fd16f65c`): build now, **check architecture fits the Extension SDK and import it once publishable**.
- **Net drift**: "extension from day one" softened into "standalone-ish build that must remain SDK-alignable". The 07-09 "no build needed" claim is superseded — the SDK gaps (LLM chat, daemon cron) proved real and are ticketed.

## D3. Gling: replace → enhance/inject
- 07-04 (`2026-07-04-gling-opensource-video-editing-research`): find open-source replacements **before the subscription renews**; Hyperframes takes over enhancement.
- 07-11 (`omi-...-gling-programmatic-control` + `plaud-...-gling-electron-mcp-injection`): renewal already happened; explicit reversal of "the earlier reverse-engineer-and-recreate plan" — inject an MCP/API layer into Gling's unobfuscated Electron app and drive the real product.
- **Trap**: the 07-04 research task looks like an open todo; it is dead. Current belief: keep Gling, control it programmatically.

## D4. Challenge DV price: $3,300 → $2,750 incl GST (same morning)
- 07-13 0633 (`plaud-1ea12ad5`): FDE retainer **$3,300/month incl GST**, weekly 90-min training + ~2 tools/month.
- 07-13 0851 (`plaud-eac21d32`, buried in the captains-log UX record): revised to **$2,750 incl GST ($2,500+GST)**, 90-min training + 1–2 tools, starting 15 July, mid-month to mid-month.
- **Trap severity: high** — the superseding decision lives in a DIFFERENT thread's record (captains-log), so a thread-scoped reader of client-challenge-dv would draft the proposal at the wrong price.

## D5. Extension architecture mental model: corrected twice
- 07-03 (`...-extension-architecture-decision`): iframe-loaded extensions declaring **host communication** via package.json contracts.
- 07-07 (`...-extension-webserver-iframe-architecture-correction`): David corrects the agent — an extension packages its own daemon/web server; **the iframe talks directly to its own backend, never through the host** (AngelEye reference). Related probe: panel-vs-mount terminology (unresolved).
- Also 07-05 (`plaud-...-extension-sdk-tagging-scheduling-gaps`): extensions must **delegate LLM work to the host**, not reinvent tagging/pulse.
- **Net current belief**: host mediates LLM + scheduling; data plane is extension-owned (iframe ↔ own daemon). Early "everything through host contracts" reading is superseded.

## D6. Dark Factory task shape: many micro-tasks → few constellations
- 07-02: "balanced single-responsibility micro-apps — 10 coherent apps not 1000" (already anti-fragmentation).
- 07-09: governance breakdown shows the factory drifted anyway (war-room namespace, self-approval, 3 launch paths).
- 07-13 (`plaud-a08f0bee`): roadmap **reset** around "complex constellation applications built one at a time — not the piecemeal small tasks the factory gravitates to".
- **Trap**: any factory backlog generated pre-07-13 reflects the piecemeal model; treat as unranked until the roadmap walkthrough happens. Also superseded: "war room" naming (must revert toward lanes/stations) and Gemini integration (deprecated 07-04).

## D7. KDD home: Cortex (mistake) → per-project .kdd (interim) → dedicated home ("within hours" — unconfirmed)
- 07-03 (`...-kdd-repository-structure`): .kdd folder inside each project NOW; dedicated KDD home expected within hours.
- No later record confirms the dedicated home landed; 07-04 and 07-07 records still argue about bridge identity and Lisa scope.
- **Trap**: the "within hours" framing makes .kdd look temporary; as of 07-13 it is effectively the standing convention until proven otherwise.

## D8. Recipe/thumbnail ownership and scope
- 06-30: agent commissioned to build generalized recipe skill + thumbnail generator.
- 07-03 (`...-kdd-repository-structure`): David **reserves thumbnail generation for himself** (agent fans out on Arcana instead).
- 07-09 (`plaud-...-session-marketing-asset-router`): recipe concept mutates from "rebuild apps" toward "post-process coding sessions into marketing assets".
- Thread dormant since. **Trap**: the 06-30 commission reads as an active agent task; ownership moved to David and the whole arc is paused.

## D9. Fable window arithmetic
- 07-02: "7-day Dark Factory push" (window ends ~07-09).
- 07-03: "learnings become documentation usable **after Fable access ends in ~6 days**" (consistent).
- 07-09 (`plaud-...-tony-coworking`): still "specced on Fable, executed on Opus".
- **Note**: not a reversal, but any plan record inside 07-02→07-09 that assumes Fable availability is now conditionally stale.

## D10. Superseded-but-current-looking — quick reference

| Stale record (looks actionable) | Superseded by | Current belief |
|---|---|---|
| 07-05 am "unify omi-fetch into one skill" | 07-05 pm decision | Separate fetchers + shared controller |
| 07-04 "research Gling replacements" | 07-11 injection plan | Keep Gling, inject MCP control |
| 07-13 0633 "$3,300/mo" Challenge DV | 07-13 0851 | $2,750 incl GST, start 15 Jul |
| 07-09 "extension hosting = no API/SDK build needed" | 07-12/07-13 SDK-gap tickets | Build standalone-ish, align to SDK when publishable |
| 07-03 "iframe talks via host contracts" (as data plane) | 07-07 correction | Iframe ↔ own daemon; host = LLM + cron only |
| 06-30 "agent builds thumbnail generator" | 07-03 reservation + pause | David-owned, parked ~late July |
| Pre-07-13 factory micro-task backlog | 07-13 roadmap reset | Constellation apps, sequenced, one at a time |
| 07-02→07-09 Fable-assumed plans | window expiry | Re-check model availability per plan |
