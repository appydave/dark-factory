# Backlog — Build Triage Console (`03-triage-console`)

**Target**: `mochaccino/designs/03-triage-console/index.html` — an interactive menu / filter / drill / analyze interface for the 1,100-artifact corpus.

**Priority**: High in eventual scope, but **DEFERRED** as of 2026-05-18 evening.

**Created**: 2026-05-18
**Status**: deferred — blocked on broader skill-workshop spec
**Block reason**: David called a strategic shift mid-session. The triage console isn't the destination — it's one feature of a broader **skill workshop app** (control plane for browse / refresh / assess / create / upgrade skills from upstream + own). We pause this backlog item and properly spec the broader app using Osmani's `spec-driven-development` methodology FIRST. Once the broader spec is ratified and decomposed into tasks, this triage console becomes one of those tasks — re-prioritized in context.
**See**: `backlog/2026-05-18-elicit-skill-workshop-spec.md`
**PO**: David (via brain session 2026-05-18)

---

## Why this exists

David's framing (verbatim):

> "If I'm going to understand 1,100 artefacts. And keep in mind I'm stealing everything I can or reframing everything I can. I steal like an artist. I'm not sure if I'm meant to go through everything... I don't have what I would call a high-level menu system that makes sense to me, not something visual. The stuff I see is full of prose. I got no way of drilling into anything. I got no way of filtering anything. I got no way of analysing any sort of prompt skill that I'm not interested in."

The existing two designs are scannable cards but they're still static reports. David needs **interactive triage**:

- **Filter** → narrow 1,100 to a tractable subset
- **Drill** → click into a specific artifact and see all its detail
- **Analyze** → mineable phrase, eval notes, file path, full description, all facets in one view
- **Cull** (eventually, v2): keep / skip / steal / reframe state per artifact

This is a **menu system**, not a gallery. Density beats polish.

## Data source (already prepared)

`mochaccino/data/triage.json` — single 836 KB file containing:

- `meta` — count, evaluated_count, generated_at
- `filters` — pre-computed counts per stage / cluster / repo / type for fast chip rendering
- `artifacts[]` — all 1,100 rows. Each has:
  - `id`, `name`, `repo`, `type`
  - `description_raw`, `description_normalized`
  - `cluster_facet[]`, `phase_fit[]` (stage numbers)
  - `file_path`, `retired`
  - `tier1{}` — token_weight, description_craft, stack_fit, maturity_signal_prelim, uniqueness_prelim, harness_compat, infra_dep, adoption_fit_prelim
  - `has_eval` — bool flag for the 88 with deep eval data
  - **If `has_eval`**: also `quality_score`, `adoption_fit_final`, `inspiration_value`, `uniqueness_refined`, `composability`, `description_craft_refined`, `mineable_phrase`, `eval_notes`, `intent`

Don't re-parse research/ files at runtime. Use this bundle.

## Required functionality

### Filter bar (top)

Three rows of chip filters + a search box. Multi-select within a group (OR); AND across groups.

| Group | Chips | Notes |
|-------|-------|-------|
| Stage | 11 chips, labelled "00 research" through "10 observability", with `(N)` counts | Use `meta.filters.stages` from the data |
| Cluster | 21 chips, labelled with cluster name + count | `meta.filters.clusters`; wrap to multiple lines |
| Repo | 13 chips, labelled with repo name + count | `meta.filters.repos` |
| Type | 3 chips: `skill`, `agent`, `command` | `meta.filters.types` |
| Quality | 5 chips: `★5`, `★4`, `★3`, `★≤2`, `unevaluated` | Quality scores from eval; unevaluated = no `has_eval` |
| Adoption | 4 chips: `strong`, `mid`, `weak`, `skip` | From `adoption_fit_final` |
| Has phrase | 1 toggle: "has mineable phrase" | Filters to artifacts where `mineable_phrase` is non-null |
| Has eval | 1 toggle: "evaluated only" | Filters to `has_eval == true` (88 artifacts) |

Plus:
- **Search box** — free text over `name` + `description_raw` + `mineable_phrase`
- **Clear all filters** button (visible when any filter is active)
- **Active filter summary** — "Showing 87 of 1,100" indicator

### Main list (left pane, ~60% width)

A dense scannable table — one row per artifact:

| Column | Content |
|--------|---------|
| Name | mono, bold |
| Repo | small, muted |
| Type | small chip |
| Stages | small pill list (numeric badges 0-10) |
| Quality | ★★★★★ if eval, "—" otherwise |
| Adopt | colored badge if eval, blank otherwise |
| 💎 | indicator if `mineable_phrase` exists |

Click row → drawer opens with full detail. Selected row highlighted.

**Sortable columns** by clicking header: name, repo, quality (desc default), stage.

**Default sort**: evaluated artifacts first (by quality desc), then unevaluated (by name).

**Performance**: 1,100 rows is fine to render all at once in the DOM. No virtualization needed. Filter just toggles CSS visibility or re-renders.

### Detail drawer (right pane, ~40% width)

Hidden when no selection. Slides in when a row is clicked.

Contents (in order):

1. **Header**: name (large), repo + type (small line below), close button (×)
2. **Open button**: if `file_path` exists, a "Copy file path" button that copies it to clipboard
3. **Description**: raw description in a quote-style block
4. **Facets section**: table of all facets
   - Stages: pills 0-10
   - Clusters: pills
   - Tier 1 facets (token_weight, maturity, uniqueness_prelim, adoption_fit_prelim, description_craft, harness_compat, infra_dep)
5. **Evaluation section** (only if `has_eval`):
   - Intent (single line)
   - Quality score (stars)
   - Adoption fit (badge)
   - Inspiration value (badge)
   - Uniqueness refined (badge)
   - Composability (label)
   - Description craft refined (label)
6. **Mineable phrase** (only if non-null): quoted callout in AppyDave amber border style (mirror the existing `02-mining-view` pattern)
7. **Eval notes** (only if non-null): muted block

No triage action buttons in v1. Those come in v2 (separate backlog item).

### Brand + style

AppyDave (`brand-dave:brand`) — light-mode-primary. Reuse the CSS variables and typography from the existing two designs:

- Cream canvas `#faf5ec`, white surfaces, warm borders
- Oswald uppercase for section labels
- Roboto for body
- Roboto Mono for data + filenames + chip labels
- Brand yellow `#ffde59` for the dark-factory label chip + active filter chips
- Brand amber `#c8841a` for quote brackets, hover accents, sequences
- Status colors: `#3d8a5a` (strong), `#5b6f86` (covered/mid), `#c8841a` (partial/weak-adopt), `#a94a36` (weak/skip)

Don't reinvent — copy the CSS variable block from `01-pipeline-overview/index.html` or `02-mining-view/index.html`.

### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ [DARK-FACTORY] Triage Console — Filter, drill, analyze         │
│ ← gallery · pipeline overview · mining view                     │
├─────────────────────────────────────────────────────────────────┤
│ STAGE  [00] [01] [02] [03] [04] [05] [06] [07] [08] [09] [10]   │
│ CLUSTER  [orchestration] [code-review] [knowledge-capture] …    │
│ REPO  [appydave] [ecc] [ruflo] [bmad-method] [superpowers] …    │
│ TYPE [skill] [agent] [command]  QUALITY [★5][★4]…  [evaluated] │
│ 🔍 Search…                              [Clear filters]         │
│ Showing 87 of 1,100                                Sort: quality│
├──────────────────────────────────────┬──────────────────────────┤
│ Name          Repo  Type Stages Q A 💎│  ┌─ Detail ──────────┐  │
│ ──────────────────────────────────────│  │                    │  │
│ doubt-driven  osmani skill 4,5 ★★★★★ s 💎│  │ name             │  │
│ false-twins   appy   skill 5,6 ★★★★★ s 💎│  │ description      │  │
│ ce-code-review ce    skill 6   ★★★★★ s 💎│  │ facets table     │  │
│ ...                                   │  │ eval section     │  │
│                                       │  │ mineable phrase  │  │
│                                       │  │ file path        │  │
│                                       │  └────────────────────┘  │
└──────────────────────────────────────┴──────────────────────────┘
```

## Acceptance criteria

- [ ] File at `mochaccino/designs/03-triage-console/index.html` (self-contained — embedded CSS + JS, fetches `../../data/triage.json`)
- [ ] All 1,100 artifacts present in the table (default sort = evaluated first by quality, then alphabetical)
- [ ] Each of the 8 filter groups works independently
- [ ] AND-across-groups, OR-within-group filter logic
- [ ] Search filters across name + description + mineable phrase
- [ ] Clicking a row opens the drawer with full detail
- [ ] Sortable columns (click header)
- [ ] "Showing N of 1,100" updates correctly
- [ ] AppyDave brand applied (same variables as existing designs)
- [ ] Update `mochaccino/mockups.json` to register the new design
- [ ] Update `mochaccino/designs/index.html` (gallery) to add the third tile linking to it
- [ ] Page loads in <500ms on localhost; filter response feels instant (<100ms re-render)

## What this skill does NOT include (defer to v2)

- Triage action buttons (keep / skip / steal / reframe per artifact) — needs persistence design first (LocalStorage vs file-write vs lightweight Python backend)
- Side-by-side comparison (pick 2-3 artifacts and diff them) — separate use case
- Origin file viewer (read the actual upstream SKILL.md inline) — needs server-side serving research/ which is outside mochaccino root; defer
- Bulk operations on filtered set — needs triage state first

## Open questions for PO

1. **Drawer vs inline expansion** — does David want a side drawer (always-visible right pane, current proposal) or click-to-expand-inline (each row expands beneath itself)? Drawer is more menu-like; inline is more compact. Default: drawer.
2. **Default visible rows** — show all 1,100 unfiltered, or default-filter to `has_eval == true` (88) and toggle "show all"? Default: show all unfiltered — let David's first action be filtering.
3. **Search behavior** — substring match on name + description (recommended) or fuzzy? Default: substring, case-insensitive.

If PO doesn't answer before execution: take the defaults above.

## Voice anchor for AppyDave brand

Open `mochaccino/designs/01-pipeline-overview/index.html` and copy the `<style>` block's CSS variable definitions verbatim. Reuse them in the new design. Don't reinvent the brand layer.

## Execution hint

Build sequence that minimizes rework:

1. Page skeleton + header + brand CSS variables
2. Fetch + parse triage.json on load
3. Render the table (all 1,100, no filter) with sort
4. Add filter chips (one group at a time; test after each: stage → cluster → repo → type)
5. Add search box
6. Add the drawer + click-to-open behavior
7. Add sort toggles
8. Wire up "Clear filters" + active filter summary
9. Update mockups.json + gallery
10. Test load time + filter response

A reasonable single session can do this in 60-90 min if vanilla JS (no framework). Use embedded `<script>` — no build step.
