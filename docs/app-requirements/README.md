# App Requirements — Lane 2 (the build-spec you build FROM)

**Status**: 2026-06-25 — charter pinned. The structure is set; the per-target templates firm up as concepts and the KBDE handover arrive.

**What this is**: the **second lane** of the app-build flow. Where a decided app idea becomes a *formal, ratified build-spec* — structured enough to hand to a builder. This is the **Developer side** of the PO→Developer bridge.

```
┌─ APP PIPELINE (brain, PO) ────┐   seam    ┌─ APP REQUIREMENTS (here, Dev) ┐
│ loose intake / backlog        │  ──────▶  │ formal build-spec you build   │
│ idea → scoped → "yes, build"  │  goal-    │ FROM                          │
│ output: a DECISION            │  ready    │ output: a buildable CONTRACT  │
└───────────────────────────────┘           └───────────────────────────────┘
  ~/dev/ad/brains/dark-factory/                ~/dev/ad/apps/dark-factory/
  app-pipeline/                                docs/app-requirements/
```

## The seam

A candidate crosses from Lane 1 to Lane 2 at **`status: goal-ready`** in its pipeline file. Lane 1 is conversational drafting; Lane 2 is the ratified spec. Do not start a build-spec for a candidate that hasn't reached `goal-ready`.

⚠️ **Naming trap:** a pipeline file's `## Initial Requirements` are *draft* bullets. The doc here is *the* spec. Same word, two maturities.

## The seam mechanic — a spec skill, not a conversation

Lane 2 is entered by **running a skill**, not by more chat. The skill is what turns a decision into structure:
- `agent-skills:spec-driven-development` / `agent-skills:spec`
- `appydave:spec-writer`
- the **Osmani pattern** (see `../../backlog/specs/df7-osmani-vs-appydave-delta.md`)

## Build target selects the template

Every candidate carries a `build_target` (set in its pipeline file). It decides which template applies and where the built thing lands in the [constellation map](../constellation-map.md):

| `build_target` | Lane-2 template | Lands in constellation as | Template status |
|---|---|---|---|
| `sentinel` | headless data-plane app on the **AppySentinel** boilerplate | Data-plane (Layer 1) | draftable now |
| `appystack` | standalone **RVETS** app (AppyStack boilerplate) | Standalone app | draftable now |
| `kbde-extension` | surface mounting in the **KBDE** host across the SDK seam | Surface (Layer 2) | **⛔ GATED on the KBDE Extension SDK handover** — needs the channel/archetype/capability fields David delivers |

## What every build-spec carries (target-agnostic skeleton)

1. **Goal / Definition of Done** — what "built" means.
2. **Scope — in / out** — explicit boundaries.
3. **Architecture decisions** — stack, boilerplate, data sources it reads, where its state lives.
4. **Acceptance criteria** — testable; for surfaces, score against the absorption law (uptake over output — see the brain vision doc).
5. **Key references** — pipeline file, prior art, canonical design docs (absolute paths).
6. **(target-specific)** — sentinel: what it collects + exposes (MCP tools). appystack: routes/screens. **kbde-extension: which channels, which archetype, what capabilities** ← the gated part.

## Status / next

- Structure pinned; `sentinel` and `appystack` templates can be authored as David delivers pipeline concepts.
- The **`kbde-extension` template is blocked** on the KBDE Extension SDK handover (the contract fields don't exist in finished form yet — not researchable). See `../constellation-map.md` §Build constraints.

## References
- Lane 1 intake: `~/dev/ad/brains/dark-factory/app-pipeline/README.md`
- Constellation map (layers + build targets): [`../constellation-map.md`](../constellation-map.md)
- Daily operating model (where specs flow: BA → Marshall → Swagger): [`../daily-operating-model.md`](../daily-operating-model.md)
