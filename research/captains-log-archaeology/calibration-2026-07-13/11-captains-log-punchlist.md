# 11 — Captain's Log Product Punchlist

**Purpose**: Product improvements for Captain's Log — David's explicit critiques merged with what the corpus structurally demands, ranked by leverage.

**For Agents**:
- Two evidence streams merged: (a) David's own captains-log feedback found in the records (15 captures across 6 of 9 active days — he critiques this product more than any other), (b) structural demands proven by processing this very corpus.
- "Leverage" = how much downstream value unlocks per unit of build effort, not how loudly it was asked for.

---

## The one-line thesis

Captain's Log currently *stores* captures; the corpus proves the value is in *connecting and closing* them. Every high-leverage item below moves it from a viewer to an intelligence loop.

## Ranked punchlist

### 1. Temporal + thematic threading (quest/side-quest view) — STRUCTURAL, David-stated
The 07-13 capture "no temporal/thematic linkage between captures" describes exactly what this manual archaeology run had to do by hand: 15 Captain's Log captures, 12 Dark Factory captures, 3 doc-watcher plans were only visible as arcs after human weaving. Chain same-day captures on one topic; let one capture split into multiple ideas that link into different chains. This is the single feature that makes the tool worth more than its raw transcripts. *(plaud 07-13-0714, omi 07-06-0903; proven by 01-thread-atlas.md existing at all)*

### 2. Open-loop tracking with closure — STRUCTURAL
58 of 102 records carry open loops (~70 items); the tool has no concept of a loop, so nothing surfaces "doc-watcher planned 3× never started" or "app/port registry untouched 15 days." David asked for notes/done-marking/audit-log against transcripts (07-13-0725) — generalize it: loops get stable IDs, first-seen/last-seen, closure events, staleness alerts. Recurrence-without-progress is the most valuable signal this corpus contains and nothing currently computes it. *(plaud 07-13-0725, 04-open-loops.md)*

### 3. Plaud token-refresh automation — David's explicit ⭐ highest priority
Operational prerequisite: until the daily manual paste-console-script dance is automated (Playwright), nothing above can run unattended. Low glamour, absolute blocker. *(plaud 07-13-0851, 07-12-0714)*

### 4. Noise gate, upstream and cheap — STRUCTURAL + David-stated
29% of the corpus is noise, and it all consumed full LLM extraction. David asked to hide empty/noise by default (07-13-0851); go further: classify pre-LLM (word count < ~15, single-char bodies, hallucination-loop detection) so noise never costs tokens, then default-hide with a reveal toggle. Also fixes threading pollution — filter before linking or every thread accretes ambient chatter. *(plaud 07-13-0851; corpus stat)*

### 5. Recurrence + duplicate triage — STRUCTURAL
Three distinct phenomena currently look identical: (a) same file twice (.clean/raw), (b) same conversation on two devices (bake-off pairs), (c) same IDEA restated across days. (a) should be file-level deduped, (b) merged by timestamp-proximity across sources, (c) NEVER deduped — it's the recurrence signal ("you've raised this 6×") that drives promotion to tickets/brains. The tool must distinguish them or counts are meaningless. *(plaud 07-06-0904 bake-off; omi 07-03-1137 pair)*

### 6. Tag governance + vocabulary normalization (one system, two faces)
David: missing tags are a config gap, not per-item fixes; wants a centralized tag store (07-13-0851). Same capture demands vernacular correction (Kybernesis mis-transcribed). These share one entity dictionary — the identical dictionary this pipeline needs for entity normalization (Dart/Dark Factory, Romy/Roamy). Build once, serve both product and pipeline. *(plaud 07-13-0851, 07-12-0642)*

### 7. Slice-and-dice filtering + search
Tags, timeframe, noise toggle, keyword over summaries — David's stated UX baseline for a growing corpus. Cheap, do with #4. *(plaud 07-13-0625, 07-13-0851)*

### 8. Chat-with-document / converse-with-corpus
Ask "what have I said about the extension SDK?" instead of re-reading. Depends on Extension SDK host-chat access (KYB-01) — sequence after SDK gap lands. *(plaud 07-13-0851)*

### 9. Durable ingestion (launchd) + manual trigger
Machine-lifetime background job, 30-min cadence 7am–10pm, restart-proof, plus an on-demand button. Pairs with #3 for full unattended operation. *(plaud 07-13-0625)*

### 10. Readability basics (batch)
Inline show-markdown, light mode (via Kybernesis DESIGN.md), semantic source colors (OMI green / Plaud blue), sequential ID scheme visible and stable. All from one 07-13 walkthrough; one UI sprint. *(plaud 07-13-0851, omi 07-04-0810)*

### 11. Data-destination config + new providers
Where each provider's output lands (raw-intake / brain / TIL) as config; email-to-self provider (YouTube transcripts, article scrape). Expansion, not core — do after the loop-closing features. *(plaud 07-12-0702, 07-11-0733)*

### 12. Cross-machine availability
Captures visible fleet-wide (Roamy vs M4 Mini), with machine-routing suggestions in the UI. Real but least urgent while David works primarily on one machine. *(omi 07-06-0904, plaud 07-06-0908)*

---

## What the ranking says

Items 1-2 are the product's actual reason to exist (nobody else is building "argue with your own last fortnight"). Items 3-4 are the cost/operations floor. Items 5-6 are the data-quality substrate the first two depend on. Everything from 7 down is good UX on top of a sound core — David's 07-13 punch-list items are real but mostly rank BELOW the structural demands he hasn't asked for by name yet (he gestured at #1 and #2 as open questions, `kind: question`, unresolved).

---

*Calibration run 2026-07-13 (real corpus). Replaces the zero-record stub.*
