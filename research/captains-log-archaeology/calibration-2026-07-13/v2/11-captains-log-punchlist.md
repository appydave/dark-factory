# Captain's Log — Product Punchlist (ranked by leverage)

**Purpose**: What Captain's Log must become, ranked by leverage. Two evidence streams: (a) David's explicit critiques from the corpus, (b) what the corpus itself structurally proves the product needs — this archaeology run IS the requirements document.

**For Agents**: Leverage = how much downstream value unlocks per unit of build. Items 1–4 are structural (the corpus demands them); 5+ are David's direct UX asks.

---

## The meta-finding

This calibration run manually did what Captain's Log should do automatically: threading, recurrence detection, loop tracking, noise suppression, entity normalization, decision supersession. Every pain in this run is a CL feature spec. The strongest single proof: the unified-viewer idea was restated **8 times in 9 days** because no system showed David it was already captured.

## Ranked punchlist

### 1. Temporal/thematic linkage — the quest chain (highest leverage)
David flagged it himself (07-13, twice: "no connective tissue", "quest/side-quest structure"). The corpus proves it: 15 captains-log records form one obvious thread that no tooling connects. Without chains, every restatement looks like a new idea; with chains, restatement #2 becomes "add detail to CL-thread" instead of a fresh capture.
- Chain a capture to earlier same-topic captures (temporal link)
- Split one capture into multiple ideas that link to different chains
- UI: timeline grouping of related captures (his 07-13 ask)
- This is also the substrate for #2 and #3.

### 2. Recurrence + supersession detection
The Challenge DV price moved $3,300 → $2,750 incl GST within ONE day, and the final figure lives in a captains-log UX-walkthrough record, not the client thread. Nothing marks the earlier value as superseded. CL needs a "current value" notion: when a capture restates a decision in an existing chain, flag it as revision and surface the latest. Same mechanism kills the said-8-times problem — show "you've raised this N times, here's the accreted spec."

### 3. Action/loop extraction with lifecycle
47 raw loop labels → 35 real loops; 20 open, 10 stale. Loops age silently (KyberAgent-on-Roamy blew its "this weekend" deadline invisibly; the Linda proposal sat 6 days restated-but-unsent). CL should extract open loops per capture, dedupe against the chain, and show age × importance. David's 07-13 "attach actions / mark-as-done / audit-log consolidation" idea is the manual half of this — build it, then automate the extraction half.

### 4. Noise default-hide with confident classification
31.7% of the corpus is noise (32/101), and it classifies cleanly — zero signal leaked in v2. This is a solved-ish LLM problem with a full third of the list as payoff. David asked for exactly this (07-13). Ship the toggle, default hidden, with the classifier confidence surfaced so borderline items (personal-but-signal like health plans) stay findable.

### 5. Vocabulary/entity normalization at ingestion
The raw filenames tell the story: "cyber agent", "chiber agent", "kubernetes extension", "homey viewer", "ome", "Happy Dave". David asked for a vernacular-safe correction layer (07-12, 07-13). Needs a personal dictionary (Kybernesis, KyberAgent, AppyDave, Challenge DV, Plaud, OMI, names) applied to transcripts AND titles/synopses without altering meaning. Also the precondition for reliable threading (#1) — you can't chain what you can't name.

### 6. Read-the-thing basics: Show button + light mode
Can't view the transcript (copy-only) and dark-mode-only is unreadable. Trivial builds, daily friction. DESIGN.md from kybernesis.ai under brand-dave (07-13). Do these first even though leverage is lower — they're hours, not days.

### 7. Plaud token automation
Daily manual console-paste to keep Plaud ingestion alive is the single most fragile operational point (07-12 decision + 07-13 automation ask). If ingestion silently dies, everything above starves. Pair with CL-01 durable launchd cron + "last pulled" visibility (the 07-04 complaint: "new omis not showing through" with no way to know).

### 8. Tag governance + central tag store
Tags today are per-item and drift (missing captains-log/kybernesis/lars tags). Config-level governance + one tag manager (07-13). Medium leverage alone, but it's the controlled vocabulary that #1/#2 depend on — same lesson as this run's controlled thread_ids fixing run-1's fragmentation.

### 9. Filters (tags, timeframe, noise, keyword) + semantic source colors
Straight UX asks (07-13). Filters matter more as volume grows; colors are polish.

### 10. Intelligence-hub ingestion (email/article/YouTube providers)
Strategically right (07-11) — CL as THE capture funnel, not an OMI/Plaud viewer — but expanding intake before #1–#5 exist just makes the pile bigger. Sequence after the processing spine works.

### 11. Chat-with-document
Blocked on Extension SDK host-mediated LLM (SDK-01). Queue behind the SDK ticket rather than building a bypass — the failed OMI extension already proved what bypassing the host costs.

## Architecture decisions already made (don't relitigate)
- Fetch skills stay separate; ONE shared processing controller (07-05)
- Hosted as KyberAgent extension; LLM via host daemon; scheduling owned by host, config in extension (07-09, 07-12)
- Replaces the OMI-only extension; conversation→project mapping + machine-routing suggestion are core telemetry (07-06)
- Sequential IDs — shipped (A330–A339 confirmed 07-13)
