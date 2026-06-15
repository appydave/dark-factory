# FINDINGS — HyperFrames as an interactive talk-through presentation

**Spike date:** 2026-06-13 · **Status:** proven · **Served:** `http://localhost:7811/presenter.html`
**Artifacts:** `composition.html` (the HyperFrames-contract slide) · `presenter.html` (the keypress player) · `proof/*.png` (browser-verified hero frames)

---

## The question

David has 4 static "how a brain works" cortex slides. He wants to know whether **HyperFrames HTML
can act as an interactive talk-through presentation** — each scene animates in, **holds** on its hero
frame while he talks, then advances on a keypress (→ / space). Not a linear video. Prove or disprove.

## Verdict: YES — with one structural caveat

**HyperFrames HTML can be driven as an interactive talk-through deck, and it took very little.** The
HyperFrames Timeline Contract is *already* designed for this: every composition's GSAP timeline is
authored `{ paused: true }` and registered in `window.__timelines["<id>"]` — and, in HyperFrames' own
words, *"the player controls playback."* The shipped player is a wall-clock renderer (preview/render to
MP4). Swapping that for a player that advances on **keypress instead of a clock** is a ~120-line
standalone runtime. Nothing in the composition changes.

**What it actually took:**
1. Author `06-brain-anatomy` as a normal HyperFrames composition — 6 scenes, `gsap.from()` entrances,
   layout-before-animation, one paused timeline in `window.__timelines`. **Plus one tiny addition:**
   expose `window.__scenes = [{enter, hold}, …]` so the player knows where each scene's hero frame is.
2. Write `presenter.html`: loads the composition in an iframe, reads its timeline + scene table, and on
   each → it `tweenTo(scene.hold)` (plays the entrance) then **pauses at the hero frame** ("HOLD — talk").
   ← does an instant `pause(prev.hold)` (jump back, no replay). Scene counter + progress dots + state.

**Browser-verified (Playwright, screenshots in `proof/`):**
- Scene 1 entrance plays, then **holds at t=2.20s** with state "HOLD — talk". ✅
- → / → advances to scene 3, holding at its hero frame (t=14.20s). ✅
- ← jumps back to scene 2's hero frame (t=8.20s), instant, no replay. ✅
- Counter "N / 6" + dots track position. ✅

**The one caveat:** the composition is **not self-presenting** — it *requires* the presenter runtime
(next section). And the scene-hold-times (`window.__scenes`) are a small authoring convention the
stock HyperFrames generator doesn't emit; a deck generator would need to add it (trivial).

---

## Is the composition HTML self-contained? NO — confirmed, not refuted

**Double-clicking `composition.html` will NOT present.** Empirically verified by loading it with no
player attached:

```
timelineExists: true     timelinePaused: true     timelineTime: 0
s1 opacity: 0            s3 opacity: 0       ← every scene is invisible
```

Because the timeline is `paused` at `time=0` and the entrances are `gsap.from(... opacity:0 ...)` over
scenes that start hidden, **nothing has played → the page renders blank.** This is inherent to the
HyperFrames model, not a bug: the HTML is the *source of truth for a video*, and **the player is a
required, separate component.** For David's use case that's fine — the presenter IS the player — but it
means a talk-through deck is always *two files*: the composition + a presenter. (You could inline the
presenter into each composition to make a single double-clickable file; that trades the clean
HyperFrames contract for convenience. See recommendation.)

---

## Adversarial-delta: (A) adapt HyperFrames vs (B) presentation-native deck

### A — Adapt HyperFrames into a presenter *(what this PoC built)*

**Motion quality:** excellent and *free*. You inherit GSAP, the house-style motion grammar, eases,
stagger, and (if wanted) the shader/CSS transition library. The entrances already look like David's
aitldr videos because they ARE that engine.
**Brand gate:** clean. The composition is hand-authored HTML/CSS — the two-layer model dropped straight
in (yellow `#ffde59` anchor, ghost text, cool-as-accent-only on the four regions). Verified on screen.
**Effort:** low for the player (~120 lines, done). Medium per-slide: you author each deck as a
HyperFrames composition (which David's pipeline can already generate).
**Reusability:** **high and strategic.** The same composition file renders to **(1)** an MP4 (linear
video, stock `hyperframes render`) AND **(2)** a keypress talk-through deck (this presenter) AND **(3)**
a teleprompter/auto-advance variant — *one source, three outputs.* That is the killer property.
**Dovetail:** **best-in-class.** It IS the Mochaccino/aitldr pipeline — prose → data → composition →
{video | deck}. The talk-through deck becomes a free third render target on assets David already makes.
**Downsides:** not self-contained (needs the player); the `window.__scenes` convention is bespoke; if
HyperFrames changes its timeline contract, the presenter follows. Random-access/jump-to-slide-N needs
the scene table (already have it). No speaker-notes UI yet.

### B — Presentation-native (reveal.js, or a bespoke HTML+GSAP deck)

**reveal.js specifically:** mature, keypress/remote/touch nav, speaker-notes window, PDF export,
fragments, overview mode — all the *presentation* affordances for free.
**Motion quality:** weaker for David's house style. reveal's built-in transitions are slide-level
(fade/slide/convex); per-element choreographed entrances mean hand-writing GSAP *inside* reveal anyway
— so you end up maintaining the same animation layer as (A), minus the HyperFrames grammar, plus
reveal's opinions to fight.
**Brand gate:** doable but you re-skin reveal's defaults (themes, controls, progress bar) to escape its
look. More friction than a blank canvas.
**Effort:** low to *start*, higher to make it look like David's brand and animate per-element well.
**Reusability:** **the deck does NOT become a video.** You'd maintain a separate path for aitldr MP4s.
That fork is the real cost — it splits the pipeline David is consolidating.
**Dovetail:** poor. reveal is a parallel system with its own data model; it doesn't feed the
prose→data→composition line. A *bespoke* HTML+GSAP deck (no reveal) is closer to (A) but then you're
rebuilding the HyperFrames player you already have — (A) without the inheritance.

### Recommendation → **A: adapt HyperFrames, with the presenter promoted to a reusable runtime.**

The decisive factor is **one source, multiple renders.** David is actively consolidating a
prose → schema → Mochaccino/HyperFrames pipeline; a talk-through deck that is *the same composition file*
his videos come from is a free third output, not a second system to maintain. reveal.js wins on
out-of-the-box presentation chrome (speaker notes, PDF, remote) but loses on the two things that matter
most here: house-quality per-element motion and pipeline fit — and it can never become the MP4.
**Caveat to carry forward:** steal reveal's *good ideas* (speaker-notes view, presenter clock,
jump-to-slide) into the HyperFrames presenter over time. Build B's affordances on A's engine.

---

## What a full version (all 4 slides) would take

1. **Generalise the presenter** into a reusable runtime that takes a list of composition files (the deck
   = an ordered manifest), so slides 02/03/04 + 06 chain with → across compositions, not just scenes.
   (~half a day; the per-scene hold logic already exists.)
2. **Author 02/03/04** as HyperFrames compositions from their existing `.mochaccino/data/*.json` — same
   pattern as `composition.html` here. The data already exists; this is mechanical (structure-first → render).
3. **Add the `window.__scenes` hold-table convention** to the deck generator so any generated
   composition is presenter-ready by default (the one bespoke bit).
4. **Optional polish:** speaker-notes pane (from each scene's prose), a 5px progress bar, jump-to-slide
   (1–9 keys), and a real cross-scene transition (blur crossfade) instead of the current opacity cross-hold.
5. **Home decision:** this presenter most naturally lives **inside the Mochaccino/aitldr render line** as
   a "deck" output mode alongside "video" — not as a standalone tool. Promote it there, not here.

---

## Files

- `composition.html` — the HyperFrames-contract slide (06-brain-anatomy), 6 scenes, paused timeline,
  `window.__timelines["brain-anatomy"]` + `window.__scenes` hold-table.
- `presenter.html` — the keypress player (the proof): plays entrance → holds at hero → advances on →.
- `proof/scene-1-title.png`, `proof/scene-3-regions.png` — browser-verified hero frames (brand gate +
  two-layer colour honored; scene 3 is the cool-as-accent discipline the original cortex deck missed).

**Feasibility note:** `npx hyperframes` (v0.6.97) IS runnable locally from npm — `init` scaffolds a
project whose `index.html` is exactly the paused-timeline contract above. The presenter was built
against that contract directly (no dependency on the CLI at runtime), so the deck is plain-browser
openable with nothing but a static file server + GSAP from CDN.
