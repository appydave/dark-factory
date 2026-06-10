# Requirement — "Mocha Lab": a Watchtower design-quality & improvement tool

**Working name:** Mocha Lab (rename freely) · **Status:** requirement, ready to build in a fresh session
**Author:** David Cruwys (PO) · **Date:** 2026-06-08
**One line:** Promote the throwaway "Mocha Census" prototype into a first-class, durable visual tool —
part of **Watchtower** — that screenshots any set of Mochaccino designs, lets David rate + label them,
and feeds those verdicts back into the design spec so the factory's design quality keeps improving.

> **This file is self-contained.** You can build the whole thing from this document alone — it includes
> what the prototype does, how it works, every path/IP/port, the validated design findings, and the new
> requirements. You do **not** need the conversation that produced it.

---

## 1. Why this exists (context)

It started as a design critique ("this Mochaccino page looks ugly") and became a realisation: to teach
the factory David's taste, you can't critique one page — you need to **see his whole body of design
work, rate it, and distill the rating into rules**. We built a prototype ("Mocha Census") that did
exactly that across ~200 designs on two machines, then proved the loop end-to-end: a page David rated
*good / "busy"* was re-rendered to the distilled spec and re-rated **love**.

The prototype is real and working but is a pile of scripts in `dark-factory/tools/mocha-census/`. David
wants it promoted to a **first-class tool he keeps using** — every time the factory renders a
Mochaccino, we can check its quality and keep improving the design ideas. It belongs in **Watchtower**
(the constellation's visual control plane).

**Dark Factory is a self-learning / self-improving system.** This tool is one of its learning organs:
it converts David's tacit taste into an explicit, versioned spec that conditions future design output.
Building it must close the two manual seams that stop the loop from running itself (see §7).

---

## 2. What the prototype already does (reuse, don't reinvent)

Location: `~/dev/ad/apps/dark-factory/tools/mocha-census/` (operator manual: `README.md` there).

**The pages are static HTML already on disk** — Mochaccino designs at
`<repo>/.mochaccino/designs/<id>/index.html`, each `fetch()`-ing its own `data/<id>.json`. There is no
app and no persistent per-page server.

- `scan.sh` — `find`s every real design on a machine (excludes `.claude/skills`, worktrees,
  node_modules, and doubled `designs/designs/`). Runs locally **and over SSH** to the second machine.
- `combine.py` — dedupes build-copies (`dist/`,`public/`,`client/dist/`) and cross-machine dupes →
  `out/manifest.json`.
- `shoot.py` — for each repo, spins up a **throwaway `http.server` on an ephemeral port** (needed
  because the pages `fetch` JSON, which `file://` blocks), screenshots every design with **headless
  Chromium via Playwright (Python)**, then **tears the server down**. Dedupes by `(repo,design_id)`.
  Output: `out/shots/<repo>__<design_id>.png` + `out/shots/shots.json`.
- `check-health.py` — loads each design and flags **broken renders** (console errors / stuck on
  "Loading…") so a data-wiring bug is never mistaken for a bad design.
- `extract.py` — structural feature-extraction (grid/flex/cards/svg/table/colour-count/lines) over
  rated designs, to find what separates the tiers.
- `run-full.sh` — the whole flow: local shoot → `rsync` the Mini-only design folders to a local mirror
  → shoot the rest.
- `out/shots/gallery.html` — the **taste board**: contact sheet of all shots, rate **love / good /
  average** per design (keyboard **A/S/D**), **←/→** to step in a zoom/lightbox, a **free-text label**
  per design, live tally, repo/rating filters, **"copy ratings JSON"** export. Ratings persist in the
  browser (localStorage) and seed the next round from the previous export.
- `out/ratings/round-NN.json` — each exported rating round. `out/ratings/exemplars.json` — the
  love-tier exemplar pack. `docs/david-design-patterns.md` — the **distilled design spec** (the rules).

**Run it today:** `cd tools/mocha-census && bash run-full.sh`; board served by
`python3 -m http.server 7440` at `http://localhost:7440/out/shots/gallery.html`.

**Stats from the proven run:** 193 unique designs, 14 repos, both machines. Pipeline validated:
`05-dark-factory` (good) → `05-dark-factory-v2` (love).

---

## 3. The new tool — required capabilities (the deltas)

Everything the prototype does, **plus**:

### 3.1 Two modes, one engine
- **Census mode** — discover *everything* across both machines → contact-sheet → bulk rate. (Exists.)
- **Bench mode (NEW, the priority)** — point at **N specific designs / variants of one idea** (e.g.
  "these 5 layouts I just generated") → **side-by-side compare view** → rate + label → return verdicts.
  This is the everyday use: generate a handful, rate them, regenerate. Right shape for **1–2 pages**,
  where census machinery (scan both machines, manifest, gallery of hundreds) is overkill.

### 3.2 Quality check on any Mochaccino run
- Whenever the factory renders a Mochaccino design, we can **check its quality on demand** against the
  spec — a single-design "score this against `david-design-patterns.md`" view, not just bulk rating.
- Surface the render-health check (broken vs clean) as a first-class signal, not a hidden script.

### 3.3 Close the ingest seam (NO copy-paste)
- The board must **export ratings to a file** (e.g. `out/ratings/round-NN.json`) the tool/agent reads
  directly — not a clipboard paste back into chat. The rating round should land somewhere an agent
  picks up automatically. (Today the only manual seam is David pasting JSON; remove it.)

### 3.4 Wire the self-improving loop
- Rating rounds + labels should **feed the spec** (`docs/david-design-patterns.md`) and the **exemplar
  pack**, and the spec + exemplars should **condition the generator** (`frontend-design` / Mochaccino
  render). Target loop, fully closed: `render → rate+label → distill to spec → re-render → re-rate`.

### 3.5 Watchtower integration
- Live as a **visual tool/panel in Watchtower** (`~/dev/ad/apps/watchtower/`), the constellation's
  visual control plane — not a one-off script folder. Use **AppyDave brand design** for its own UI
  (warm browns/cream/yellow; see §6/§8). It can keep the Python+Playwright capture engine behind it.

### 3.6 Refresh / re-runnable (with change detection)
- Re-running is the model: dedupe and only shoot new designs. **Add the missing bit:** detect a
  *changed* page (file mtime newer than its screenshot) and **auto re-shoot** it. (Today you must delete
  the old PNG by hand to refresh an edited design.)

### 3.7 Cross-machine (keep)
- Scan + capture across **both Macs** (M4 Pro local + M4 Mini over Tailscale). ~122 designs exist on
  both with diverged mtimes — shoot the freshest, label the source machine, and ideally surface the
  divergence (it's real untracked-file drift worth seeing).

### 3.8 Rating model (keep + persist properly)
- Tiers: **love › good › average** (the broken-render "shit" tier was dropped — broken ≠ bad design).
- **Free-text label** per design (the *why* — this is the strongest signal; see §5).
- Keyboard: **A** love · **S** good · **D** average · **←/→** step · type a label. Toggle to clear.
- Persist locally, **seed each round from the previous**, export to file.
- **Methodology rule (important):** David's tiers **drift between sessions** (round-02 had 47 "love"s;
  round-03 had 1 — he rates "love" comparatively). **Anchor learning on the labels and the relative
  ordering, NOT on absolute tier counts.**

---

## 4. Functional requirements (testable)

1. **FR-1** Capture: given a target (all-machines, one repo, or an explicit list of design paths),
   produce a full-page PNG per design, serving each via a throwaway local server, nothing left running.
2. **FR-2** Health: flag each captured design as clean / broken (console error or stuck loading).
3. **FR-3** Census view: contact sheet of all captures with per-design rating + label + filters.
4. **FR-4** Bench view: side-by-side comparison of N chosen designs/variants with the same rating+label.
5. **FR-5** Single-design quality view: score one design against the spec rules and show pass/flags.
6. **FR-6** Ratings persist locally, seed from the prior round, and **export to a file** (no paste).
7. **FR-7** Re-run only shoots new **or changed** (mtime-newer) designs.
8. **FR-8** Cross-machine scan + capture (local + SSH/rsync to the Mini), source-machine labelled.
9. **FR-9** A distillation step turns a rating round into updates to `david-design-patterns.md` +
   `exemplars.json` (assisted by an agent is fine; the round file is the input).
10. **FR-10** Runs under the Max plan with **no cron / no API scheduling** (in-session only — see §6).

## 5. The validated design findings (embed — this is the spec the tool maintains)

From rounds 01–03 (full version: `dark-factory/docs/david-design-patterns.md`). The tool exists to
apply and keep refining these:

- **Tier is composition; the recurring flaw is colour.** What makes a design *love* vs *good* is
  structure (diagram-ness, colour-discipline) — but the single most repeated complaint, even on loved
  designs, is a colour failure.
- **#1 fix — NO orange/amber on brown/beige** (13 gripes across all tiers). Orange only as a small
  highlight; never text-on-brown or filled boxes on beige. Lead with green/blue/purple semantic blocks.
- **LOVE triggers:** (1) **diagram/flow** — SVG connectors, a **legend** strip, an input/output header
  (love svg≈3.5 vs good 0.6); (2) **disciplined semantic block colour** — **fewer** colours used
  meaningfully (love ≈13 distinct vs 19), alternating cream/dark-brown section **bands** + per-block
  accent; (3) **ghost text** — oversized tone-on-tone background lettering (his signature; loved even on
  broken shells); (4) **uniqueness / asymmetry / randomness**.
- **Connectors: colour belongs in the blocks, not the lines.** (round-03) Keep lanes/tiles coloured;
  make connector lines **thin and neutral** with small colour-dots at endpoints. Bold coloured curves
  are one step too much.
- **Caps at good (never love):** off-brand palette ("not my brand color"); competent-but-flat (no
  diagram, no colour-blocking). **Average:** thin card-sprawl, no diagram.
- **Soft dings:** busy/dense; too much dark brown; childish icons.
- **Always separate broken renders from design verdicts.**

## 6. Non-functional requirements

- **No persistent servers per page** — ephemeral capture servers only; one viewer server is fine.
- **Max plan, in-session automation only** — never cron or paid API scheduling; if recurring, use the
  in-session loop pattern.
- **AppyDave brand** for the tool's own UI (the prototype board already uses a dark warm theme — keep
  the brand: browns/cream, yellow as highlight, Bebas/Oswald/Roboto stack; obey the tool's own §5 rules).
- **Self-contained capture engine** (Python 3 + Playwright + Chromium already installed on the M4 Pro;
  `~/Library/Caches/ms-playwright` has chromium). Watchtower UI may wrap it.
- Cheap to re-run; safe to run repeatedly.

## 7. The two seams to close (what makes it self-learning)

1. **Ingest seam** — replace "David pastes ratings JSON into chat" with "board writes a round file the
   agent reads." (FR-6)
2. **Generator seam** — the spec + exemplar pack are not yet wired into the renderer, so the rules are
   applied by hand. Wire `david-design-patterns.md` + `exemplars.json` into the `frontend-design` /
   Mochaccino render step so new designs start on-spec.
   Close both → the loop runs itself: rate → spec updates → next render is auto-on-spec → re-rate.

## 8. Environment / facts the builder needs

- **Machines:** M4 Pro "Roamy" (this/local) + M4 Mini (`davidcruwys@100.82.235.39`, **Tailscale** —
  always use the Tailscale IP, not `.local`). Designs live under `~/dev` on both.
- **Design location pattern:** `<repo>/.mochaccino/designs/<id>/index.html` (+ `…/data/<id>.json`);
  some repos use `mochaccino/` (no dot); designs can nest (`designs/components/<name>/index.html`).
- **Ports in use:** prototype board on **7440**; the dark-factory `.mochaccino` server on **7422**;
  the canonical mochaccino gallery on **7420**. Pick a free port for the new tool.
- **Prototype to lift from:** `~/dev/ad/apps/dark-factory/tools/mocha-census/` (scan/shoot/health/
  combine + `gallery.html` + `README.md`).
- **Spec + data to carry forward:** `dark-factory/docs/david-design-patterns.md`,
  `tools/mocha-census/out/ratings/{round-01,round-02,round-03-result,exemplars}.json`.
- **Watchtower repo:** `~/dev/ad/apps/watchtower/` (built via David's Ralphy plugin; change it in-app
  via Ralphy + a requirement spec — this file can be that spec).

## 9. Open decisions for PO (David)

- **Name** — "Mocha Lab"? "Design Bench"? "Taste Lab"?
- **Home** — a panel inside Watchtower, or a standalone Watchtower-adjacent app sharing its shell?
- **Build approach** — keep the Python+Playwright engine and add a Watchtower UI over it, or rebuild
  capture in Watchtower's own stack? (Recommend: keep the proven Python engine; new UI on top.)
- **How "bench" is fired** — a Watchtower button ("rate these N"), a CLI, or a skill (`/bench`,
  `/census`) Marshall can invoke?

## 10. Definition of done

- Census **and** bench modes work; bench does side-by-side rating of an explicit N.
- Single-design quality check against the spec works.
- Ratings export to a **file** (no copy-paste); a round file can be ingested by an agent.
- Re-run auto-re-shoots **changed** designs (mtime).
- Cross-machine capture works (both Macs).
- Lives in/with Watchtower, brand-styled, no persistent per-page servers, no cron.
- A documented path exists from a rating round → spec/exemplar update → next render on-spec.

## 11. Suggested first steps (for the building session)

1. Read `dark-factory/tools/mocha-census/README.md` + `scan.sh`/`shoot.py`/`gallery.html` — lift the
   engine.
2. Stand up **bench mode** first (highest daily value): take a list of design paths → shoot → a
   side-by-side compare+rate view → write a round file. Prove it on 5 variants of one idea.
3. Add **export-to-file** + **mtime re-shoot**.
4. Fold in census mode (the existing flow) and the single-design quality check.
5. Wrap in Watchtower (panel + brand) and expose a fire-off (skill/button).
6. Wire spec+exemplars into the generator to close the self-learning loop.

---

### Paste-ready kickoff (for the new window)

> Build "Mocha Lab" — a Watchtower visual tool that screenshots Mochaccino designs, lets me rate them
> (love/good/average + a free-text label, keyboard A/S/D + arrows), and feeds the verdicts back into the
> design spec so our design quality keeps improving. Full requirement (self-contained, with paths/IPs/
> the validated taste rules):
> `~/dev/ad/apps/dark-factory/backlog/2026-06-08-mocha-lab-requirement.md`.
> Reuse the working prototype at `~/dev/ad/apps/dark-factory/tools/mocha-census/`. Priority is **bench
> mode** (rate N variants of one idea side-by-side) and **export-to-file** (kill the copy-paste seam).
