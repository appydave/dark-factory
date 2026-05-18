---
artifact_id: appydave-plugins:skill:mocha
repo: appydave-plugins
artifact_type: skill
cluster_facet: [ui-design, mockup-rendering, mvc-separation]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: mocha

**Intent**: View-rendering persona within the Mochaccino quartet — reads JSON data files (from Peter) and renders self-contained HTML designs into the designs/ directory, never modifying data.

## Scores

- **quality_score**: 4. Excellent MVC enforcement, clear render/re-render/gallery/serve commands, local server handling with port conflict detection. Docked one point: ecosystem-specific (quartet dependency, brand-dave brand tokens).
- **adoption_fit_final**: `weak`. The persona-based MVC decomposition pattern is interesting, but the skill is deeply embedded in the Mochaccino ecosystem. The mechanism is difficult to lift without the surrounding quartet.
- **inspiration_value**: `mid`. The MVC rule (reads data, writes HTML, never reverses) enforced as a hard constraint is clean. The citation comment pattern inside HTML is a nice provenance approach.
- **uniqueness_refined**: `uncommon`. A rendering persona with a strict MVC constraint codified inside a skill is unusual — most mockup skills blend data and view.
- **composability**: `called-by-others`. Invoked by Mochaccino orchestrator; calls frontend-design skill as a sub-dependency. Part of a chain.
- **description_craft_refined**: `trigger`. Description names all four quartet members and lists both delegation and direct triggers.

## Mineable phrasing

> "Mocha reads data. Mocha writes HTML. Never the other way around."

## Notes

The local server pre-flight (check for running server before open, detect port conflicts, surface URL to user so they can reload independently) is a mature operational detail rarely seen in design skills. The workspace-aware gallery regeneration (regenerate root index when any workspace gallery changes) shows systematic thinking about stale state. However, the deep ecosystem coupling makes adoption without the full quartet unrealistic.
