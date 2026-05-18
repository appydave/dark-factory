# Feedback Log

Append-only record of David's feedback on the `dark-factory-catalog` skill, used by `catalog:self-improvement`.

Entry format:

```
## YYYY-MM-DD HH:MM — <one-line summary>
**Context**: <when this came up>
**Quote**: <verbatim if useful>
**Proposed change**: <to SKILL.md / reference / schema>
**Status**: open | proposed | applied | rejected
```

---

## 2026-05-16 18:45 — Add prompt-pattern awareness to recon and discover passes

**Context**: After Phase 1 recon across all 13 repos (completed 2026-05-16). David noticed that interesting prompt-engineering moves were embedded inside skills/agents but the catalog schema and recon heuristics don't surface them — they just land as opaque fields in artifact entries.

**Quote**: "Have a look at my prompt pattern brain. Just get an understanding of what's going on there. Once you know that, that'll probably help you write an improvement to the dark-factory skill to be able to look out for cool, interesting, and useful prompt patterns."

**Proposed change**: See `proposals/2026-05-16-prompt-pattern-awareness.md` — covers (a) whether prompt-pattern becomes a first-class artifact type or a cross-cutting facet, (b) new heuristics for `capability-recon.md`, (c) schema field additions for `capability-discover.md`, and (d) whether a new `references/prompt-pattern-vocabulary.md` reference file is warranted.

**Status**: proposed
