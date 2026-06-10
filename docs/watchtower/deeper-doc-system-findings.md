# Findings — Deeper Documentation System (2026-06-07)

Research dispatched by Marshall across three reader Swaggers. Brief: `deeper-doc-system-research-brief.md`. All claims tagged ✅verified (cite) / ⚠️inference / ❓unknown.

**One-line conclusion:** every stage of "prose → structured model → rendered slides/docs" already exists as a David skill — but the stages are **not chained**. The factory's job is the *glue*, not new engines.

---

## A. What each cluster IS

### A1. Mochaccino render family — `appydave-plugins/appydave/skills/{peter,mocha,shelly,mochaccino,mochaccino-v1}`
A 4-persona MVC pipeline: **Mochaccino** (orchestrator/interview) → **Shelly** (recommends a data *shape*) → **Peter** (source → `data/NN-slug.json`) → **Mocha** (JSON → `designs/NN-slug/index.html`) → Python `http.server :7420` gallery. ✅verified (mochaccino/SKILL.md:38-46, workflow.md:1-17). Strict MVC; provenance baked in: Peter's `meta.source` cites the canonical source, Mocha stamps an HTML citation comment. ✅verified (mocha/SKILL.md:44-46). Three modes — UI-mockup, **text-to-documentation**, **documentation-validation** (if Peter can't build a clean shape, the spec has a gap). ✅verified (mochaccino/SKILL.md:52-58).
**Shelly's 6 shapes** (✅verified shelly/references/shape-catalog.md:12-132): `list`, `kanban`, `timeline`, `matrix`, `card-grid`, `layer-stack` — all share a mandatory `meta{id,version,extracted,prompt,source}`. **No `slide-deck` shape exists.** ⚠️inference: that's the gap for presentations.
**Why v2 exists:** mochaccino-v1 had no data layer → FliDeck once produced **343 bespoke HTML files** for bmad-poem, nothing derivable. ✅verified (mochaccino/references/canonical-sources.md:36-43). *This is the exact anti-pattern the factory must not repeat.*

### A2. Structure + slide-generation skills
- **prose2models** (KEYSTONE) — `appydave-plugins/appydave/skills/prose2models`. Prose → structured model. Commands: extract / extract-as / update-model / version-model / list-shapes / summarize-changes / recommend-next. ✅verified (SKILL.md:48-96). 5 shape families incl. **Presentation = sections, key messages, themes, slide structure, headline-evidence pairs.** ✅verified (SKILL.md:20-26). Writes `.prose-models/current/` + `versions/`. **But: no canonical Presentation JSON example — only a UX example exists.** ❓unknown (SKILL.md:145-160).
- **poem-slides-workflow** — `appydave-plugins/brand-dave/skills/poem-slides-workflow`. Session-router that runs a workflow doc. Takes a BMAD transcript → **hand-authors** 4-5 HTML slides per story phase (intake/complete/sat/sat-cheatsheet/qa-review) → syncs to FliDeck. ✅verified (SKILL.md:56-65; brains/brand-dave/docs/bmad-story-slide-workflow.md:219-235). **Does NOT call prose2models or Mochaccino** — agent judgment writes the HTML. ⚠️inference.
- **flideck** — `~/.claude/skills/flideck`. Presentation **hosting/query** service (preview :5200, API :5201). Not a generator. ✅verified (flideck/SKILL.md; reference/presentations-command.md:17-42).
- **bmad-story-lifecycle** — produces **no slides**; its run transcript is the *input* to poem-slides-workflow. ✅verified (SKILL.md).

### A3. brand-dave deck systems — `brains/brand-dave/{deck-systems-docs,presentation-templates/solo}`
The design system + template/component library, extracted from **70-73 real bmad-poem slides across 8 content categories**. ✅verified (01-pattern-library-extraction-handover.md:173-220). **NB: the corpus evidence is 8 categories, not the "30-40" from memory** — flagged for David.
- **40 HTML components** (self-contained CSS snippets) ✅verified (components/INDEX.md).
- **8 templates**, each with a **`.meta.yaml` data-shape contract** (e.g. `comparison`, `scorecard`, `timeline`) ✅verified. `timeline.meta.yaml` even references a formal `data-systems/schemas/presentation-outline-schema.json`.
- **7 recipes** (composition guides) + **`index.yaml`** machine-readable discovery index with `use_when` matching ✅verified.
- **Design tokens**: 8 brand vars + 5 semantic colors + 4 fonts; **Card Shell** macro (brown header / white body / yellow footer); **QUALITY-CHECKLIST** 50-pt rubric + `spacing-checker.js`. ✅verified (README.md:163-200, QUALITY-CHECKLIST.md).
- **Deck types**: Solo (standalone assets → FliDeck), Scene (live-recording slideshow), Arcade (retro/TTY demo, discovery-only). ✅verified.
- **Lineage**: brain = source of truth → syncs to `appydave-plugins/brand-dave`. ✅verified (PLUGIN-SYNC-NOTES.md).

---

## B. The common pattern — structure-first → render, in three layers

```
        PROSE                    SCHEMA / MODEL                 RENDER
  (specs, tickets,     →    (structured data, the         →   (HTML slides/docs,
   transcripts,             leverage point)                    on-brand, provenanced)
   concepts.md)
  ───────────────         ─────────────────────           ──────────────────────
  prose2models  ........>  .prose-models/*.json   ..X..>   [NO RENDERER reads it]
  Mochaccino interview ..> Peter data/*.json (6 shapes) .> Mocha HTML + gallery ✅
  (none / agent)          .meta.yaml data contracts ..X.> agent hand-authors HTML
                          + 40 components + tokens          → FliDeck hosts ✅
```

Same philosophy throughout ([[structure-first-then-render]]): the schema is the leverage point, the view is mechanical. **Three nearly-complete chains, none joined end-to-end:**
1. prose2models extracts a model → **nothing renders it.**
2. Mochaccino renders cleanly → **but has no slide-deck shape and is interview-driven (one design at a time, not batch).**
3. The solo library has data contracts + components + design system → **but rendering is hand-authored HTML, not schema-driven.**

**The missing glue is one thing: a schema-driven slide renderer** — read a structured slide/Presentation model, emit Card-Shell-compliant HTML from the 40-component library, citation-stamped. Replace "agent hand-authors HTML" with "model → render."

---

## C. PROPOSAL — deeper-doc-system as a first-class Dark Factory subsystem

**Thesis:** don't build engines — **chain the ones we own** and add the single missing renderer + a batch path.

- **Ingest** — factory prose: `backlog/concepts.md`, tickets/stories (engine queue), architecture docs, agent specs, phase notes, the Chronicle. Each is a prose source.
- **Schema** — adopt prose2models' **Presentation** family as the intermediate model, but *define the canonical schema it lacks*: a `slide-deck` shape = `{ meta, deck:{title,category}, slides:[{ id, layout_hint, headline, evidence, body, speaker_notes }] }`. `layout_hint` maps to a solo template / Shelly shape. (Reuses `presentation-outline-schema.json` if it fits.)
- **Render** — the **one new build**: a renderer that reads the slide-deck model and emits HTML from the **solo 40-component library** with brand tokens + Card Shell, citation-stamped à la Mocha. Either (a) add a `slide-deck` shape to Shelly + teach Mocha the components, or (b) a standalone renderer keyed off `index.yaml`/`.meta.yaml`. **Recommend (a)** — stays inside the proven MVC + provenance + gallery infra.
- **Batch** — wrap prose2models so the factory feeds it programmatically (no per-design human interview) across many prose sources → many models → many decks. This is what turns "one mockup" into "hundreds of slides / N categories."
- **Where it lives** — a constellation subsystem (working name **"Pressroom"** / or fold into Mochaccino). Dispatched as an **engine ticket** (`kind: skill` or `workflow`): prose source → model → render → gallery/FliDeck. Fits the existing Marshall→Swagger loop.
- **Reuse vs build:** Reuse = prose2models, Mochaccino MVC + provenance + gallery, the 40 components + 8 `.meta.yaml` contracts + recipes + `index.yaml` + design tokens + QUALITY-CHECKLIST. **Build new = (1) the canonical slide-deck schema, (2) the schema-driven renderer, (3) the batch/factory-intake wrapper, (4) component↔shape bridge (already named as future work in mochaccino/references/canonical-sources.md:100-114).**

---

## D. Open questions / decisions for David

1. **The "30-40 categories" gap.** Documented corpus = **8 categories / 70-73 slides** (bmad-poem). Where do the other ~30 live — another project, your head, or to-be-generated? This sets the subsystem's real scope.
2. **Render path:** extend Mochaccino (add `slide-deck` shape — stays in the proven MVC/provenance/gallery) vs a standalone renderer off the solo `index.yaml`? (Recommend: extend Mochaccino.)
3. **Slides vs docs:** is the first target presentation *decks* (Card Shell slides → FliDeck) or *documentation pages* (Mochaccino text-to-documentation)? Same engine, different shape — which first?
4. **Home:** new constellation app ("Pressroom") vs folding into Mochaccino? (Constellation = consistent with the suite; Mochaccino = less new surface.)
5. **Build locus:** app-owns-its-features says build the renderer *in* the skill/app via Ralphy — or is this the factory's first self-built subsystem? ([[capability-placement-and-reassessment]])

---

## UPDATE (2026-06-07) — corpus corrected to FliDeck; the creation pattern found

**Naming:** "Deckhand" was wrong. The app is **FliDeck** (`~/dev/ad/flivideo/flideck`, React+Express, :5200 preview / :5201 API). `apps/deckhand` is an unrelated Stream Deck config tool — coincidental name collision. ✅verified (apps/deckhand/CLAUDE.md:1).

**Corpus:** the "30-40 categories / hundreds of slides" is REAL. FliDeck's gallery = **20 presentations** in `brand-artifacts/presentation-assets/` — appystack(35), ansible(19), arcade-deck(22), bmad-agents(16), **bmad-poem(343)**, claudemas-12-days(10)… ✅verified. The earlier "8 categories/70 slides" was only the brand-dave *extraction subset*. **bmad-poem = 343 bespoke HTML files, no data layer** ✅verified — simultaneously the proven-at-scale corpus AND the mochaccino-v1 anti-pattern.

### THE CREATION PATTERN (David: "a really powerful pattern")
```
source prose/transcript
   ↓  /solo-deck agent  ← loads design system + 40-component library + brand tokens
   ↓                      + harness-authoring-standard.md (a STABLE AUTHORING CONTRACT)
   ↓  generates self-contained "harness-fragment" HTML per slide
   ↓  files land in  brand-artifacts/presentation-assets/{name}/   (a WATCHED folder)
   ↓  FliDeck Chokidar auto-discovers
   ↓  ONE call:  PUT /api/presentations/:id/manifest/sync-from-index
   ↓             (cheerio parses card links → builds tabs/groups/slides manifest)
   → served at :5200, branded, navigable
```
✅verified (flideck/docs/harness-authoring-standard.md, agent-guide.md, CLAUDE.md, prd/fr-26-index-html-sync.md; appydave-plugins/brand-dave/commands/solo-deck.md).

**Why it's powerful = `design-system-as-agent-context` + `stable-authoring-contract` + `watched-folder` + `one-sync-call`.** Any agent that loads the contract produces slides that work in the viewer with zero viewer-side changes — creation and viewer decoupled by convention. **Mechanical (automatable):** load library → generate to contract → drop in folder → sync. **Human-judgment:** which slide types, what the content means, quality review, tab/group labeling.

**FliDeck manifest schema** ✅verified (flideck/CLAUDE.md):
```json
{ "tabs":[{"id","label","file":"index-{id}.html","order"}],
  "groups":{ "id":{"label","order","tabId"|"parent","tab":true} },
  "slides":[{"file","group","title","viewportLock"}],
  "meta":{"updated","notes"} }
```

### Revised proposal — center on the creation pattern, not a forced data layer
The factory doc/slide subsystem = **a Swagger-dispatched creation job** that: (a) takes a factory prose source, (b) runs a slide-generation agent bound to `harness-authoring-standard.md` + brand tokens, (c) writes HTML to `presentation-assets/{name}/`, (d) fires one `sync-from-index`. **FliDeck is the hosting/manifest layer — already built, proven at 343 slides.** The factory builds only the *creation glue + intake*.

### THE central decision (supersedes earlier "extend Mochaccino")
Two proven-vs-clean render philosophies collide:
- **(P) FliDeck/solo-deck bespoke-HTML** — PROVEN at scale, branded, David calls it powerful. Cost: no data layer → 343 unreusable files; regeneration = re-author.
- **(M) Mochaccino MVC data-layer** — clean, reusable, provenanced, but no slide-deck shape and unproven at deck scale.
The factory could (P) automate the proven pattern as-is, (M) push slides through a data layer, or **(H) hybrid** — prose2models extracts the *model*, then a renderer emits harness-fragment HTML to the FliDeck contract (data layer feeding the proven viewer). H gets reuse + the proven hosting. **This is David's call** — it sets whether we optimize for "ship decks now" (P) or "structure-first reusable" (H).
