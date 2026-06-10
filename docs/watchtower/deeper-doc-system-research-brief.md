# Research brief — Deeper Documentation System (2026-06-07)

**Goal:** produce a grounded findings doc that lets Marshall design a **deeper documentation system** as a first-class Dark Factory subsystem — David's #1. The system turns the factory's own prose (tickets, stories, concepts, architecture, agents, phases) into structured data and then into rendered slide/doc sets ("hundreds of slides across ~30-40 categories", BMAD-style).

**Premise correction (2026-06-07):** the source corpus is NOT `brains/llm-structured-data`. It is David's **presentation/slide-building skills** (which originally lived in the brains folder) + the **brand-dave deck systems**. All LOCAL on Roamy — not M4-exclusive.

## The real corpus (all local)

**Render family (appydave-plugins/appydave/skills/):** `peter` (data→JSON), `mocha` (JSON→HTML), `shelly` (shape librarian), `mochaccino` (+ `mochaccino-v1`).

**Structure + slide-generation skills:**
- `appydave-plugins/appydave/skills/prose2models/` — **keystone**: prose → structured models; shape families incl. **Presentation** (sections, key messages, slide structure). Writes `.prose-models/`.
- `appydave-plugins/brand-dave/skills/poem-slides-workflow/`
- `~/.claude/skills/flideck/`
- `appydave-plugins/appydave/skills/bmad-story-lifecycle/`

**Brand-dave deck systems (brains/brand-dave/):**
- `deck-systems-docs/` — `solo-deck.md`, `scene-deck.md`, `generation-methods.md`, `index-grid-patterns.md`, `arcade-deck/{README,discovery,skills-identified}.md`, `scenes/`.
- `presentation-templates/solo/` — component/template library: `comparison|scorecard|timeline|diagram|cards|decision-tree|knowledge-graph|markdown-viewer` each with `.meta.yaml` + `.html`, plus `recipes/`, `components/`, `design-principles.md`, `semantic-colors.md`, `QUALITY-CHECKLIST.md`, `css-variable-patterns.md`.

## Output — findings doc (`docs/watchtower/deeper-doc-system-findings.md`)

- **A. What each cluster IS** — render family / structure+slide skills / brand-dave deck systems. 1 para each + key data shape, quoted with file:line.
- **B. THE COMMON PATTERN** — how it's all "structure-first → render" (prose → model/schema → rendered slides/docs). Where prose2models, peter/mocha/shelly, and the templates each sit.
- **C. PROPOSAL — deeper-doc-system as a first-class Dark Factory subsystem:**
  - Ingest: which factory prose (tickets, stories, `backlog/concepts.md`, architecture, agents, phases).
  - Schema: the intermediate structured form (sketch JSON/DSL; reuse prose2models' Presentation family?).
  - Render: via what (mocha/mochaccino? the solo template library? flideck?).
  - Where it lives + how it's dispatched (engine ticket? workflow? skill?).
  - Reuse vs build-new (we already own most of the pieces — what's the glue?).
- **D. Open questions / decisions for David.**

**Grounding:** cite file:line; quote real shapes; tag ✅verified / ⚠️inference / ❓unknown.
