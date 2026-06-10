# DF-7 Spec Method Delta — Osmani `spec-driven-development` vs `appydave:spec-writer`

**What this is:** an adversarial critique of running the **same** DF-7 requirement through two spec methods. Inputs:
- `df7-switchboard-state-plane-spec.md` — appydave:spec-writer baseline (the original).
- `df7-switchboard-state-plane-spec.osmani.md` — Osmani pass (this batch).

Verdict up front: **the appydave baseline is the stronger DF-7 document; Osmani's method contributed a better *shape* for the build leg but would have produced a weaker spec from scratch.** Detail below. Not flattering to either.

---

## What Osmani's method ADDED (genuine wins)

1. **Boundaries as a hard three-tier (Always / Ask-first / Never).** This is Osmani's best contribution. The baseline scattered its constraints across §4 Non-Goals + the inline "never kill" notes + the five Open Decisions. Osmani forces them into one scannable block where **"Ask first" is exactly the set of open decisions** and **"Never" is exactly the constellation guardrails**. For a Ralphy build agent that will execute this autonomously, that block is more actionable than prose Non-Goals — an agent can literally gate on it.
2. **Commands as a first-class section.** The baseline never states how to build/test/restart Switchboard. Osmani's template demands it, which surfaced a real gap: *we don't actually know Switchboard's `package.json` script names* — so the Osmani version flags "confirm against package.json" as Ask-first. The baseline silently omitted this; Osmani made the unknown visible.
3. **Explicit Plan→Tasks gate with per-task Verify.** The baseline's §11 migration is good but is prose; Osmani reframes it as checkbox tasks each carrying an Acceptance + Verify + Files triple. That's directly executable as a Ralphy task list — less translation loss between spec and build.
4. **"Reframe instructions as success criteria" discipline** pushed the testing strategy to name the *load-bearing* test (the 200×8 concurrency proof) as the spec's center of gravity, rather than burying it as AC #2.

## What Osmani's method SHARPENED

- **Testing Strategy got its own home.** The baseline's test thinking lived only inside §13 Acceptance Criteria. Osmani splits "what proves it" (Testing Strategy, by level) from "what done means" (Success Criteria). The concurrency test, restart test, and read-shadow parity now read as a deliberate test pyramid, not a checklist.
- **Tech Stack table with per-row provenance** is tighter than the baseline's §5 prose-ish table — every fact carries a "read verbatim" tag, which serves DF's `ground-claims-cite-sources` rule better.

## What Osmani's method DROPPED or WEAKENED (the honest part)

1. **Problem framing got thinner.** The baseline's §2 Problem Statement is the best writing in either doc — it names the *two goals with one root cause*, quotes David ("a disaster in normal programming"), and explicitly designs *against* the repo-clone trap. Osmani's template has no "Problem Statement" slot, so this collapsed into a few Objective sentences. **A build agent that doesn't internalize *why repo-cloning is rejected* might reinvent it.** Net loss in the Osmani structure.
2. **No native "Non-Goals" section.** Osmani folds them into "Never do," which works for guardrails but loses the *negative scoping* nuance ("NOT the DF-3 telemetry layer," "NOT choosing the on-disk format beyond X"). Some Non-Goals aren't "never" — they're "out of scope for THIS spec," which the Never-tier overstates.
3. **Osmani is interview-first by design — and that's wrong for this repo's flow.** The skill's whole gated workflow assumes a live human interview (SPECIFY phase: "ask clarifying questions until concrete"). DF-7's reality is **PO-authors-here, no live interview** (`requirements-first-store-for-future-ticketing`, `surface-decisions-dont-bury`). We had to *defeat* Osmani's primary mechanism (treat the baseline as canned answers) to use it. A method whose headline feature is unusable in your actual workflow is a yellow flag for "make it canonical."
4. **Generic-template smell.** Osmani's six areas are tuned for a *greenfield app* ("Project Structure: where source lives, where tests go"). DF-7 is a *2-recipe addition to an existing app*. Half the template (Tech Stack, Project Structure, Commands) is boilerplate-shaped for a problem we don't have, so it gets padded. The baseline's bespoke sections (Recipe Inventory, Claim-by-id Contract, Migration/Coexistence, Liveness & Reaping) are **domain-shaped** and carry more signal per line.
5. **Open Decisions lost their recommendation richness.** The baseline gives each Dx a recommendation *with reasoning and a revisit trigger* ("start file-per-job; revisit only if directory scans get slow"). Osmani's "Ask first" tier compresses these — I had to re-import the reasoning manually to avoid losing it. The method didn't help here; it actively fought the nuance.

---

## Structure-by-structure scorecard

| Dimension | appydave:spec-writer | Osmani spec-driven-development | Stronger |
|---|---|---|---|
| Problem/why framing | Dedicated §2, quotes the stakeholder, designs against the anti-pattern | No slot — collapses into Objective | **appydave** |
| Domain fit (this exact task) | Bespoke sections (Recipe Inventory, Claim Contract, Migration) | Generic 6-area template, padded for greenfield | **appydave** |
| Guardrails / boundaries | Scattered across Non-Goals + inline notes | One Always/Ask-first/Never block | **Osmani** |
| Build-leg actionability | Prose migration steps | Checkbox Tasks w/ Acceptance+Verify+Files | **Osmani** |
| Commands / how-to-run | Absent | First-class (surfaced a real gap) | **Osmani** |
| Open-decision richness | Recommendation + reasoning + revisit trigger | Compressed into Ask-first bullets | **appydave** |
| Test thinking | Inside Acceptance Criteria | Own Testing-Strategy section by level | **Osmani (marginal)** |
| Fit to DF's PO-authors-no-interview flow | Native (it's a doc generator) | Fights it (interview-first by design) | **appydave** |

**Tally:** appydave 4 (and they're the heavier dimensions — framing, domain fit, decision richness, workflow fit); Osmani 4 (boundaries, tasks, commands, tests — all *packaging/rigor* wins, not *content* wins).

---

## Recommendation

1. **Canonical DF-7 = the appydave baseline, upgraded with three Osmani imports.** Don't replace it. Graft onto the baseline: (a) the **Always/Ask-first/Never** boundaries block, (b) the **checkbox Task list** with Verify steps for the migration, (c) a short **Commands** section once Switchboard's `package.json` is confirmed. These are Osmani's real value and they're additive. The baseline's Problem Statement, Recipe Inventory, Claim Contract, and Migration prose stay — Osmani has nothing better there.

2. **Both docs already bake in D4-RESOLVED and carry D1/D2/D3/D5 open** — no decision lost in translation. **4 decisions still open.**

3. **Should Osmani's `spec-driven-development` become the first-class spec method here? — Not as-is, and not as a replacement.** It is a strong *checklist/rigor overlay* (boundaries, gates, tasks, commands) but a weaker *generative spec method* for this repo, because (a) its interview-first core is unusable in the PO-authors-here flow, and (b) its template is greenfield-app-shaped while DF work is mostly *additions to existing constellation apps*. **Recommended posture:** keep `appydave:spec-writer` as the generative author; adopt Osmani's **Boundaries + gated-Tasks discipline** as a *rigor pass* applied on top. That's a "graduate the useful 30%, not the whole pack" verdict — the pack earns a place as a **lint/gate layer**, not as the spec author. Re-test on a *greenfield* DF capability (not an existing-app addition) before promoting it further; this task was structurally biased toward the bespoke baseline.

---

*Adversarial note on my own bias: this comparison used an existing-app, recipe-addition task — which inherently favors the baseline's bespoke domain sections over Osmani's generic template. A fair re-test of Osmani-as-author needs a from-scratch capability where its greenfield template fits. Flagging so the verdict isn't over-read.* **OPEN DECISION (David):** adopt Osmani as a *rigor/gate overlay* on top of appydave:spec-writer (recommended), vs. make it the primary spec method, vs. keep appydave-only.
