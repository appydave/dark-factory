---
topic: "Flex child pixel-width clipping"
issue: "Flex child with explicit pixel width still shrinks and clips"
created: "2026-06-11"
story_reference: "307792ae"
category: "debugging"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/hyperframes-presentation-poc/presenter.html"]
commits: []
---

# Flex child pixel-width clipping — Flex child with explicit pixel width still shrinks and clips

## Problem Signature

**Symptoms**: Scene 6 of the HyperFrames presenter PoC showed text and a ghost word cut off on the right edge of the browser window, with the canvas visibly anchored right-of-centre instead of letterboxed symmetrically.

**Environment**: experiments/hyperframes-presentation-poc/presenter.html (dark-factory), a 1920x1080 iframe canvas scaled to fit an arbitrary browser viewport

**Triggering Conditions**: Browser viewport narrower than 1920px (e.g. 1800px wide) while the composition canvas was defined with a fixed width:1920px.

## Root Cause
The `#scaler` div (the 1920x1080 box holding the composition iframe) was a flex child of `#stage` with the default `flex-shrink:1`. An explicit CSS `width:1920px` is only a preferred size for a flex item — with shrink enabled, flex quietly shrank the layout box down to the viewport's actual width (~1800px). `overflow:hidden` on the scaler then silently clipped the right ~120px of the 1920px canvas instead of visibly overflowing, and `transform-origin:center` computed its centre from the shrunk box, not the intended 1920px box, offsetting the whole scaled canvas.

## Solution
Set `flex: 0 0 auto` on `#scaler` so its layout box is always a true 1920x1080 regardless of the flex container's available space. Also moved `#stage` to end above a bottom control bar, rewrote `fit()` to measure the stage's real client box instead of `window - magic numbers`, capped scale at 1x to avoid upscaling blur, and added re-fit calls on `window.load`, the iframe's `load` event, plus a `requestAnimationFrame` re-fit to catch first-paint metric shifts.

```css
#scaler {
  width: 1920px; height: 1080px; transform-origin: center center;
  box-shadow: 0 30px 120px rgba(0,0,0,.55); background: var(--paper);
  border-radius: 6px; overflow: hidden;
}
```
Fix (reported by the agent that applied it, not captured as a verbatim diff in this transcript): add `flex: 0 0 auto;` to `#scaler` so flex no longer shrinks its declared 1920x1080 box.

## Prevention
When sizing a flex child to an exact pixel box (e.g. a fixed-aspect canvas inside a centering flex container), always pair the explicit width/height with `flex: 0 0 auto` — an explicit pixel size alone is only a preference under flex's default shrink behaviour, and `overflow:hidden` will hide the resulting clip rather than surface it.

## Related
- Sessions: 307792ae
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 307792ae · 2026-06-11
- **Files** (candidate-level): experiments/hyperframes-presentation-poc/presenter.html
- **Commits** (candidate-level): —
