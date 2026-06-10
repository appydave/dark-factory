# OPEN QUESTION — design-lint: standalone tool, or a Mochaccino mode?

**Raised by:** David, 2026-06-10, mid-build. *"I want to come back and think about later whether
you've done the right thing by doing a design lint here and whether it wasn't meant to be a tool built
into Mochaccino itself. We don't need to rectify anything, but at the end we do need to consider."*

**Status:** open — reconsider before the lint is promoted past staging. Do NOT auto-rectify.

## What got built (this session)

`tools/design-lint/` in dark-factory:
- `RUBRIC.md` — the judgment spec (3 reliable flags, flags-only, no count-policing).
- `shoot-one.py` — screenshot one render (reuses the mocha-census Playwright pattern).
- `README.md` — operator manual; two modes (inline gate · batch audit).
Proven: mechanical screenshot ✓, no-false-positives ✓ (lexi amber-badges + a blue/green categorical
slide correctly NOT flagged). True-positive proof (flagging the brain-cold cortex deck) still pending —
cortex source is on the M4 Mini.

## The question

Is a **free-standing dark-factory tool** the right locus, or is design-lint really a **mode of
Mochaccino** (Shelly's automated self-`review`)?

**Case for "it's a Mochaccino mode" (David's instinct, and probably right):**
- Mochaccino IS the render engine; a post-render self-check is part of the render→review loop. Mochaccino
  already has a human `review` mode — this is the *automated* sibling.
- The rules are Shelly's gate. The lint applies Shelly's own gate to Shelly's own output. Splitting that
  knowledge across two homes invites drift.
- Pattern risk: coining a separate "tool" for what is a *mode* of an existing engine is the exact mistake
  flagged in memory `its-mochaccino-not-comprehend-visualise`.

**Case for staging it in dark-factory first (why it's here now):**
- CLAUDE.md hard rule: don't write skill code directly into appydave-plugins; dark-factory `tools/` is the
  staging ground. Shelly/Mochaccino are tracked in appydave-plugins.
- The Playwright screenshot machinery already lives in dark-factory (mocha-census) — natural to reuse.
- Faster to iterate the rubric here before baking it into a tracked skill.

## Likely resolution (to confirm, not act on yet)

The **logical home is inside Mochaccino** — promote `RUBRIC.md` into Shelly as an automated
self-lint / `review` sub-mode; keep only the portable screenshot helper + staging here. The risk David
is sensing is that `tools/design-lint/` ossifies as a separate tool instead of being folded in. This is a
`capability-placement-and-reassessment` decision — locus chosen deliberately, re-judged from a distance.

**Decision owner:** David. **Trigger to revisit:** before any wiring of the lint into the live render
pipeline, or at the next design-system working session.
