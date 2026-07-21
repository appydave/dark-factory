# RESUME POINT — Dark Factory roadmap Q&A (+ 3 truth cleanups)

**For:** session `dark-factory-b0` (`616e641c-0890-47a5-8500-a206be40595a`).
**Written:** 2026-07-21 by the predecessor session (`eacae19c`, now acting as Chaperone).
**Read this whole file before your first action.** You are cold; everything you need is here.

---

## 0. Your FIRST work — three truth cleanups (do these before resuming the Q&A)

> ✅ **DONE 2026-07-21 — commit `100276b`.** (1) T3 → `progressing` (not `partial`; no such legend key)
> in BOTH `factory-map.json` and `index.html`, which embeds its own copy of the data rather than
> fetching it. (2) playwright installed to `tools/design-lint/.venv`; gate run for real — **verdict
> `flag`, not pass**: `amber-orange-on-brown`, `#c8841a` as text-on-cream ×14 + fill ×5, where
> `docs/david-design-patterns.md:42-55` allows it only in 01/02/03 sequences. Record corrected
> forward, not rewritten. Verdict at `tools/design-lint/out/lint/11-factory-map.verdict.json`.
> (3) No on-disk handover instance found beyond (1). **Amber defect left unfixed** — design change,
> not a truth correction; map is the live Q&A backdrop.

The predecessor session closed with three uncorrected findings raised by the Chaperone
(advisories 0019/0020, `docs/_chaperone-feed.md`). All three are **verified true as of now**.
They are small, concrete, and they make the record honest. Do them first.

1. **The Factory Map's T3 card oversells.** `mochaccino/data/factory-map.json` → track `T3` has
   `status: "proven"` and a note saying the artifact was *"harvested, drafted, inspected, and
   RATIFIED."* But artifact #1 was **hand-ratified by the PO seat as one-time recovery** — the
   HITL/ratification pipeline is unbuilt (ADR-0045). The map's own gaps board says this honestly;
   the status card contradicts it.
   **Fix:** `status → "partial"` and rewrite the note to
   *"drafted + hand-ratified as recovery; the ratification pipeline itself is unbuilt (see gap)."*
   Re-render `mochaccino/designs/11-factory-map/` so the page matches the data.

2. **`design-lint` cannot run — and a commit claims it passed.** `python3 -c "import playwright"`
   fails; `tools/design-lint/shoot-one.py` crashes on it. Commit **`76e2512`** states *"passes the
   design-lint taste check"* — **the gate never ran** (a screenshot was eyeballed manually instead).
   **Fix:** install/repair playwright so `shoot-one.py` runs, actually run the gate on
   `11-factory-map`, and correct the record (a follow-up commit stating plainly that the earlier
   claim was wrong and what the real verdict is). Do **not** silently rewrite history.

3. **Handover wording.** Anywhere the record says the factory "ratified its first artifact",
   qualify it: **hand-ratified as recovery**. The factory can currently **draft**, not **ratify**.

Report what you changed. Then continue below.

---

## 1. What this Q&A is

**Goal (David, verbatim intent):** a **sequenced build order for the 7 unbuilt pipelines**, each
tagged by **who steers it — David, an agent, or the factory autonomously.**

**How to run it — this is a hard constraint:**
- **One question at a time.** Never dump a roadmap.
- **Do NOT use the AskUserQuestion tool.** David wants to riff and debate in open text.
- Offer **multiple choice + your own recommendation + the counter-argument you'd accept.** He
  explicitly likes options *and* likes to argue with them.
- Backdrop is the **Factory Map**: `http://localhost:7420/designs/11-factory-map/`
  (data: `mochaccino/data/factory-map.json`). Server: `cd mochaccino && python3 -m http.server 7420`.

## 2. Decisions already locked — do not re-ask these

| # | Question | Answer |
|---|---|---|
| Q1 | What's the factory's job first? | **B — Watchtower first.** Observability is the precondition for delegating anything as "autonomous". |
| Q1b | David's correction | **Watchtower IS a constellation app.** Any micro-app is part of the constellation. T5 ⊂ T6 — they are not siblings. |
| Q2 | How wide is Watchtower v1? | **C — engine-only v1, widen as feeds land.** Ship against data that exists (`status.py --json`); don't block on broken sentinel/AngelEye. |
| Q2b | David's architectural rule | **Federation, not monolith.** Every constellation app exposes its own **API/MCP** surface; Watchtower *taps* them. "Watchtower is where I can go to see everything." Widening Watchtower = each app growing a surface. (`T6-05` already specs AngelEye's MCP wrapper — the pattern exists.) |
| Q3 | After Watchtower v1, which feed next? | **C — Inventory / registry.** The only candidate whose data already exists and is authoritative (`locations.json`, `apps.json`, `app-registry/query.py`); A and B both require reviving a dark app or repairing a broken one before yielding a single row. Also unblocks T2 (its gap is "11 off-registry repos are invisible to the inventory"). Answered 2026-07-21. |
| Q4 | Who steers each pipeline? | **B — split by reversibility.** Factory runs unattended where output is a **draft or read-only** artifact; David gates anything **irreversible** (lands in `canonical/`, writes a registry, touches another repo). A rule, not a list — new pipelines inherit it. **Consequence David accepted:** the gate is unbuilt (ADR-0045), so today "gated" means the run parks and gets misread as wedged. HITL is therefore the **unlock for autonomy**, not a nice-to-have. Answered 2026-07-21. |
| Q5 | Where does HITL sit? | **B — third, after Watchtower v1 + Inventory.** Both are read-only so under Q4 they need no gate. Rationale: T3-02's park on 07-11 was *correct* and sat invisible ~16min while the reaper killed it — that was a blindness failure, not a HITL design failure. Eyes before hands. Answered 2026-07-21. |
| — | Ingestion name collision | **Rename dark-factory T3 → "Harvest".** Captain's Log owns "ingestion" (it's in the app title, `server/src/ingest/`, `POST /api/ingest`, 100+ doc hits). "Harvest" is 0 hits there and is already T3's own internal word. Instance of ticket `T6-01`. |

**Map defect to fix while you're at it:** the status board lists T5 and T6 as sibling tracks, but the
architecture layer correctly nests Watchtower under SURFACES. The track list is a **mixed taxonomy**
(T1 = an engine capability; T2/T7 = process faculties; T5/T6 = apps; T8/T9/T10 = cross-cutting).
Per Q1b, **the constellation is the container and micro-apps are the build unit.**

## 3. The open question — Q3 (ask this, once cleanups are done)

**After Watchtower v1, which data feed comes next?** (This IS the constellation build order, given Q2b.)
- **A) AngelEye** — agent/session telemetry. Dark, needs revival (`T6-04`), MCP wrapper already specced (`T6-05`). *Predecessor's recommendation.*
- **B) Sentinel / AppyRadar** — fleet + machine state. Known-broken (blind-to-Roamy `T6-03`, a→e migration `T6-02`). Broken things rot; T10 needs it.
- **C) Inventory / registry** — `docs/constellation-map.md` calls this *"the first data source in the bottom layer"* and says the briefing idea was built backwards without it. Currently stale.
- *(D — Captain's Log — was dropped: it targets KBDE, not Watchtower. Different lane.)*

## 4. The challenge sitting beside Q3 — do not bury it

David's own archaeology (`research/captains-log-archaeology/`) concluded:

> *"Captain's Log / Dark Factory dominated only the LAST FORTNIGHT — the 6-month centre of gravity
> is client + infra + content. The recent obsession is recency bias."*

So the honest alternative to answering Q3 is **testing the premise**: not "which factory pipeline"
but "how much factory at all, versus the work that actually pays." David has been asked to choose
between answering Q3 and testing this. **He has not answered yet.**

## 5. Context you should load (in this order)

1. This file.
2. `mochaccino/data/factory-map.json` — the 9 tracks, real counts, gaps board.
3. `docs/kdd/decisions/0045-stabilise-before-drain-engine-moratorium-after-t1-21.md` — the moratorium (now **exited**, David said "out of the moratorium").
4. `docs/_chaperone-feed.md` — the outside-eye record, incl. the 3 cleanups above.
5. `backlog/2026-07-11-factory-map-spec.md` — how the map was specced.

## 6. Standing rules for this seat

- **David runs dispatch commands in his own terminal**; you emit the command, never run
  `./run.sh` or `promote-wargame go` yourself. (`feedback_engine_run_command`.)
- **Verify before asserting.** The #1 recurring defect on this project — and it recurred *into a
  commit message* on 07-11. If a gate didn't run, say it didn't run.
- **Three zones:** driver tooling = this seat's job · a ticket's impl = dispatch to a worker ·
  the live engine mid-run = do not touch. (`feedback_po_seat_never_builds`.)
- A **Chaperone** (session `eacae19c`) is watching this session and posts advisories to the
  blackboard channel `dark-factory-coherence` + `docs/_chaperone-feed.md`. Read them at boundaries
  with `bb_list({channel:"dark-factory-coherence", prefix:"advisory."})`. They are **advisory,
  non-blocking** unless tagged `force:"ruling-blocking"`.
