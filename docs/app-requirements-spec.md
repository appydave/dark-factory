# App Requirements — the build-spec standard (Lane 2)

**Status**: 2026-06-25 — the *standard*, not a home for instances. Sits beside `canonical-form-spec.md` / `provenance-spec.md` as a `docs/*-spec.md`.

**What this is**: the standard for turning a decided app into a *formal build-spec you build FROM*. It owns the **"how"** (the shape of a build-spec, per build target). It does **not** hold the specs themselves.

## The rule that fixes the smell: factory owns the standard, the target app owns the instance

```
FACTORY OWNS                          TARGET APP OWNS
────────────                          ───────────────
• Lane 1 intake backlog               • its own build-spec (the instance)
  (brain app-pipeline/, folder of     • lives in the app's own repo
   candidate files — factory knowledge)
• THIS standard (the "how")           
```

A build-spec is a **per-app artifact**, so it lives **with the target app**, never permanently in the factory. This matches the app-pipeline rule (*"built apps keep their docs in their own repos"*) and the dark-factory ethos (*staging, not a permanent home; don't absorb*).

**Where an instance lives, by case:**
- **Enhance an existing app** → its build-spec lives in **that app's repo** from the start. The factory never holds it.
- **New app, repo exists** → authored into the **new app's repo** at scaffold time.
- **New app, no repo yet** → staged *transiently* in the factory (the repo's staging-ground identity), with an explicit `migrates_to: <target>` marker. It leaves the factory the moment the app has a home.

> This is why Lane 1 and Lane 2 are **not** symmetric folders: Lane 1 is a factory-owned instance store; Lane 2 is a standard whose instances live in target apps.

## The seam

A candidate crosses from Lane 1 (intake) to Lane 2 (build-spec) at **`status: goal-ready`** in its pipeline file — the PO→Developer bridge. Don't write a build-spec for a candidate that hasn't reached `goal-ready`. Lane 2 is entered by **running a spec skill** (spec-driven / spec-writer / the Osmani pattern — `../backlog/specs/df7-osmani-vs-appydave-delta.md`), not more conversation.

⚠️ **Naming trap:** a pipeline file's `## Initial Requirements` are *draft* bullets. A build-spec is the *ratified* contract. Same word, two maturities.

## Build target selects the template

The candidate's `build_target` (set in its pipeline file) decides the template and where the built thing lands in the [constellation map](./constellation-map.md):

| `build_target` | Build-spec template | Lands in constellation as | Template status |
|---|---|---|---|
| `sentinel` | headless data-plane app on **AppySentinel** boilerplate | Data-plane (Layer 1) | draftable now |
| `appystack` | standalone **RVETS** app (AppyStack boilerplate) | Standalone app | draftable now |
| `kbde-extension` | surface mounting in the **KBDE** host across the SDK seam | Surface (Layer 2) | **⛔ GATED on the KBDE Extension SDK handover** |

## Build-spec skeleton (target-agnostic)

Whatever the target, the spec the target app receives carries:

1. **Goal / Definition of Done** — what "built" means.
2. **Scope — in / out** — explicit boundaries.
3. **Architecture decisions** — stack, boilerplate, data sources it reads, where its state lives.
4. **Acceptance criteria** — testable; for surfaces, score against the absorption law (uptake over output — brain vision doc).
5. **Key references** — pipeline file, prior art, canonical design docs (absolute paths).
6. **(target-specific)** — sentinel: what it collects + exposes (MCP tools) · appystack: routes/screens · **kbde-extension: which channels, which archetype, what capabilities** ← the gated part.

## Status / next
- `sentinel` and `appystack` templates can firm up as David delivers pipeline concepts.
- The `kbde-extension` template is **blocked** on the KBDE Extension SDK handover (contract fields not finished, not researchable). See `./constellation-map.md` §Build constraints.

## References
- Lane 1 intake: `~/dev/ad/brains/dark-factory/app-pipeline/README.md`
- Constellation map: [`./constellation-map.md`](./constellation-map.md)
- Daily operating model (BA → Marshall → Swagger): [`./daily-operating-model.md`](./daily-operating-model.md)
