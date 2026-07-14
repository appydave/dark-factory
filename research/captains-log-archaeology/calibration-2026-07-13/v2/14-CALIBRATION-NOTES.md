# Calibration Notes — v2 vs Run-1, Honest Assessment

**Purpose**: Did the v2 design changes (thread registry, loop registry, noise short-circuit, entity normalization) actually fix run-1's failures — and what still breaks at 1,250-record / 6-month scale?

**For Agents**: This is the go/no-go gate for the full-corpus run. Read the "cross-slice merge" section before designing that run.

---

## Scorecard

| v2 mechanism | Verdict | Evidence |
|---|---|---|
| Thread registry (controlled thread_ids) | **Worked, with a known lossy edge** | 15 threads, 101 records, zero run-1-style fragmentation; captains-log held 15 records coherently across 10 days |
| Loop registry (identity + lifecycle) | **Worked within-slice; identity is NOT yet durable** | 47 raw labels → 35 loops, statuses assigned (20 open / 10 stale / 3 parked / 2 likely-resolved); one loop closed on hard evidence (sequential IDs → A330 sighting) |
| Noise short-circuit | **Clean win** | 32/101 (31.7%) discarded with tiny essences, no extraction effort wasted, no signal leaked (spot-check: HIIT/NordPass correctly kept as `personal`, not dropped) |
| Entity normalization | **Good at extraction; no enforced canon yet** | "cyber agent"/"chiber"/"kubernetes extension"/"homey viewer" all resolved to KyberAgent/Captain's Log; "Ian (Kybernesis)" vs "Ian Borders" correctly kept distinct |

## What genuinely improved over run-1

1. **Fragmentation is gone.** Run-1's failure mode — the same initiative shattered across ad-hoc labels — did not recur. The controlled vocabulary meant the 8 restatements of the unified-viewer idea all landed in `captains-log`, which is what made the recurrence analysis (02-recurrence.md R1) possible at all. Recurrence detection is a *product* of thread discipline; run-1 couldn't have produced R1.
2. **Loops now have lifecycle, not just existence.** Stale-detection (10 loops) and evidence-based closure (sequential IDs) are qualitatively new. The age×importance ranking surfaced real operational risk (Challenge DV proposal unsent 6 days, price drifting; Roamy agent deadline lapsed) rather than a flat list.
3. **Noise handling is now free.** A third of the corpus cost near-zero processing. At 1,250 records that's ~400 records that won't burn extraction budget.
4. **Supersession got caught once** — the $3,300→$2,750 price drift was detected *because* both records shared a loop. Run-1 would have reported two prices with no ordering.

## What's still weak (within-slice)

- **One record = one thread_id is lossy.** The A330–A339 walkthrough record spans CL UX + the Challenge DV price decision + affiliate-triage deferral + Gling. It was filed under `captains-log`, so the corpus's most important client fact (final price) is invisible to anyone reading `client-challenge-dv`. This is the single most dangerous residual defect. Fix: allow secondary thread refs (`thread_id` + `also_touches[]`), or split multi-topic records at extraction.
- **Thread boundary judgment calls remain.** The thumbnail micro-app sits in `recipe-thumbnail` but is architecturally a `kyber-extensions` build; 07-05's controller *decision* went to `captains-log` while its SDK-gap *diagnosis* went to `kyber-extensions`. Defensible, but a different extractor could choose differently — the registry needs one-line inclusion rules per thread, not just names.
- **Loop labels are still free-text at extraction.** "Captain's Log controller build" / "Captain's Log extension build" / "Captain's Log Kybernesis extension build" were three labels merged into one loop only at weave time by judgment. Within one slice that's fine; across slices it's roulette.
- **"Likely-resolved" is inference, not evidence.** Only 1 of the 2 closures had a hard sighting. Fine at 101 records; at 1,250, unverified closures will accumulate into false confidence.

## The scale question: what breaks at 1,250 / 6 months

The full run will be ~12 slices of this size. Everything above survives EXCEPT the piece that was explicitly left undesigned: **cross-slice identity.**

- **Thread ids drift without a seed.** Each slice run re-derives threads from its own records. `captains-log` didn't exist as a concept before 07-04; six months of slices will see threads born, renamed (omi-list → captains-log), merged, and dormant-then-revived (recipe-thumbnail paused 07-10, resuming late July — a naive slice 3 weeks later would mint a fresh thread for its revival).
- **Loop ids are per-run artifacts.** LOOP-019 means "Challenge DV proposal" only inside this run's registry. Re-run the same slice tomorrow and numbering reshuffles. Cross-slice references (03-decision-drift pointing at loop ids) are therefore not durable.
- **Supersession needs a ledger, not luck.** Price-drift detection worked because both records fell in one slice. The $25k-quote → $3,300 → $2,750 chain spanning slices would NOT be caught without carried state.

**Required design (blocking for the full run): a persistent registry protocol.**
1. `registry/threads.yaml` — append-only thread records: stable id, one-line inclusion rule, aliases, status (active/dormant/merged-into). Each slice run READS it as controlled vocabulary, may propose additions/merges, never renumbers.
2. `registry/loops.yaml` — append-only loop ledger: stable `LOOP-NNN` issued once, label aliases, status transitions with evidence, last-seen date. Slice output = transitions + new loops, not a fresh registry.
3. `registry/decisions.yaml` — current-value ledger for superseding facts (prices, dates, chosen names): key, current value, history. Cheap, and it's what makes the drift analysis compound instead of reset.
4. Slices must run **chronologically** (registry-in → registry-out); parallel slice execution is off the table unless slices are made registry-independent and merged in a serial reconciliation pass (viable, but that pass is then the new risk).

Secondary scale risks: multi-topic records (fix above), entity canon (ship the vocabulary dictionary from punchlist #5 as extractor input), and weave-context size (15 threads/35 loops fit in one weave; ~60 threads/200+ loops at full scale will need per-thread weaves + a final atlas pass).

## Verdict

**GO — conditional.** The v2 extraction layer is calibrated: threading, loop lifecycle, noise, and entities all held at slice scale, and the outputs (tickets/punchlist/recurrence) are decision-grade. Do NOT launch the full run until the persistent registry protocol (threads + loops + decisions ledgers, chronological slice order) is written and tested on a 2-slice dry run — that's roughly a half-day of design, and without it the 12 slices will produce 12 incompatible registries and re-import run-1's fragmentation at a higher level.

**Single biggest remaining risk**: cross-slice identity drift — thread/loop ids re-derived per slice instead of carried, silently splitting six-month arcs into per-slice fragments.
