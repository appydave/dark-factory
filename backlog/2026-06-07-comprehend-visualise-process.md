# Comprehend → Visualise — the factory's prose/code→visualisation PROCESS

**Date:** 2026-06-07 (afternoon reframe). **Status:** problem framed + process drafted; NOT built. Ready for next sessions.
**Lineage:** the noon "deeper documentation system" #1 → narrowed through the afternoon to this concrete shape.

## The problem (David's words, 2026-06-07 ~3pm)
> "The Dark Factory should be able to go off and build things for us at any time. You should be able to **point it towards prose [or code] and create rendered visualisations and put them in specific locations.**"

Archetype job ("a normal day"): *"Go read `~/dev/kybernesis/cortex` on the M4 Mini. Look at the code + the GitHub commits over the last two weeks, figure out the exact system we built — ~8 packages, 4+ databases, components, flowcharts — and come up with a bunch of visualisations."*

**Why it matters:** David is a YouTuber. When he writes code, *being able to visualise it* is a first-class need (teaching/content), not a nice-to-have.

**Honest current state (David):** "we're not there, because we don't even have a *process* for you to work with." → This doc designs that process.

## Decisions locked this afternoon
- **Engine = Mochaccino (latest).** Most advanced; the evolutionary fix to FliDeck's schema/data-separation flaw; proven provenance + refresh + reuse at scale (SupportSignal). See `docs/watchtower/deeper-doc-system-findings.md`.
- **FliDeck hosting/navigation-at-scale = OUT OF SCOPE today** but important — *capture the learnings, don't build it now.* (tabs/groups/manifest, harness contract, 343-slide viewer, `sync-from-index`.)
- **Why Mochaccino has three sub-skills** (David asked): **Peter = data** (source → `data/*.json`, with `meta.source` provenance), **Shelly = shapes** (the shape librarian/catalog — what structures the data can take: list/kanban/timeline/matrix/card-grid/layer-stack/lifecycle-flow…), **Mocha = render** (JSON → branded HTML + gallery). It's **MVC**: the split exists so the **data layer is a durable, independent asset** (the exact thing FliDeck lacked), shapes are reusable/catalogued, and rendering is mechanical. Each is independently improvable.

## The proposed PROCESS — "Comprehend → Visualise"
```
0  POINT (Marshall)      target {repo/folder/prose} + intent + OUTPUT LOCATION + audience  → a job ticket
        │
1  COMPREHEND (Swagger,  read code + git log (last N) + structure; fan out parallel readers
   parallel readers)     over packages / DBs / components / flows  → grounded, cited digest
        │
2  STRUCTURE (Peter+     digest → structured DATA. Shelly picks shapes
   Shelly)               (layer-stack=architecture · matrix=pkg×concern · card-grid=packages/components
                         · timeline=git history · lifecycle-flow=workflows). meta.source cites code+commits.
        │
3  RENDER (Mocha)        data → branded HTML visualisations → written to the OUTPUT LOCATION; gallery; serve.
        │
4  PLACE & RETURN        outputs land at the specified location; Marshall reports links; done/.
        │
5  REFRESH (the payoff)  on new commits, re-run 1–3 from the SAME provenance chain → visuals stay live.
```

## The key insight (what makes it buildable)
Mochaccino today is **interview-driven** (conversational, one design at a time — built for a human in the loop). The factory's missing piece is an **autonomous driver** for the Peter→Shelly→Mocha pipeline — invoked by a ticket `{target, intent, location}`, no human interview.
**The Marshall→Swagger→engine loop IS that autonomous driver.** A Swagger can run Peter→Shelly→Mocha headlessly. So the build is small: codify the pipeline as the recipe a Swagger runs + an autonomous (non-interview) Mochaccino invocation + the comprehension front-end (recon over a codebase). We are NOT building a new engine — we're marrying the proven engine to the proven dispatch loop.

## Acceptance test (first proving run)
The **Kybernesis/cortex** job above. Done = factory, pointed at `~/dev/kybernesis/cortex` (M4) with intent "visualise the system," autonomously produces a provenanced set of visualisations (architecture, packages, DBs, flows, 2-week change story) into a specified location, served, with `meta.source` back to code+commits so it can be refreshed.

## Open questions for next session
1. **Autonomous Mochaccino:** does a Swagger invoke the Peter/Shelly/Mocha skills directly, or do we need a thin non-interview workflow wrapper? (Probably a workflow/recipe.)
2. **Comprehension front-end:** how deep does STAGE 1 go for a big repo (8 packages, 4 DBs)? Parallel readers per package → merged digest (the pattern we used today).
3. **Output location convention:** in-repo `.mochaccino/` (Mochaccino's default, kept in VC) vs a factory-owned location? Cross-machine (cortex is on M4).
4. **Shape selection for code:** is the current Shelly catalog enough for codebases, or do we need code-specific shapes (dependency graph, ER diagram, package map)?
5. **Refresh trigger:** manual re-dispatch now; later tie to commit/staleness (observability thread).

## Is it a workflow? — YES for the core, NO for the gates (David's intuition, grounded)
Grounded in the vendored Workflow spec (`brains/anthropic-claude/claude-code/workflows/`, verified 2026-06-07). A Claude Code workflow = a deterministic JS script orchestrating subagents; **2 hard limits: no mid-run human gate, no cross-session memory.** The process splits exactly along that grain:
```
   WITHIN-JOB  =  a Workflow script            BETWEEN-JOB  =  the engine queue
   ───────────────────────────────             ──────────────────────────────────
   Comprehend → Structure → Render             human review · refresh-on-commit
   pipeline/parallel; agents =                 = job boundaries:
   Peter / Shelly / Mocha;                     render lands in done/ → David reviews →
   handoff = JS vars + files (the baton)        enqueue "revise" or "refresh" job
```
- The **mechanical core** (read→structure→render) is a workflow's sweet spot: serial phases + fan-out over packages; handoff is "plain JS variable passing… agents never talk; state flows through return values + files" (patterns.md).
- The **human-in-the-loop** is what a workflow CAN'T hold mid-run. The spec's own answer names us: *"Both [limits] disappear when a durable job queue wraps the workflow (the Dark Factory 'Watchtower' pattern)… the gate is a job boundary: stage lands in done/, a human approves, the next job is enqueued."* So the Marshall→Swagger→engine loop IS the half the workflow needs. **Complementary halves, not competitors.**
- **Caveats to design around:** (1) workflow orchestrator can't touch fs/shell — only `agent()` can, so Peter/Shelly/Mocha each become `agent()` calls; (2) no durable store — YLO blackboard is still the inspectable-persistence differentiator; (3) research-preview, opt-in (`ultracode`). Strategic fork (native vs bespoke) = its own session.
- **Reliability:** a code-controlled `pipeline()` stage runs at 100% sequencing consistency vs probabilistic chained handoffs — right for a repeatable factory job.

→ Open question #1 (autonomous Mochaccino) is now answered in shape: **author the within-job core as a Workflow script; the engine owns the gates + refresh.** We author against the verified `workflow.schema.json` (8 globals), not memory.

## Scope boundary (so next sessions don't sprawl)
IN: the Comprehend→Visualise process via Mochaccino, autonomous, dispatchable, provenanced.
PARKED (documented, not built): FliDeck hosting/nav-at-scale; the full "hundreds of slides / N categories" deck generation; cross-machine dispatch hardening.
