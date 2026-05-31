# Dark Factory — Human Communication (first-class)

**Status**: new — 2026-06-01
**Companion docs**: `architecture.md` (the factory runs dark), `intake.md` (the spoken front door), `watchtower/context.md` (events + dashboards), `mochaccino/` (visual learnings)

---

## The principle

For the Dark Factory to work, **communication with the human is a first-class citizen** — and it runs **both directions**, both first-rate.

The factory floor runs dark: lights off, no human on the floor. But the human is **never out of the loop**. They stay the *director* without standing on the floor. That only works if the comms channels are excellent. Lights-off operation and first-class human comms are not in tension — the channels are *how* the human steers and sees.

## Two channels

### 1. Audio — talk and listen

**In (human → factory):** control the direction by talking. Kick off work, steer, ask "what's in flight?". This is the spoken front door (see `intake.md`). **Talking sets a ticket; it does not spawn a Claude Code session.**

**Out (factory → human):** the factory speaks back.
- **Events** — "title-gen run finished", "promotion gate failed."
- **Summaries** — a spoken digest of what happened while you were away.
- **Feedback** — sound effects that pull your eyes to the right window; spoken narration of what's happening now.

The human should be able to tell **by ear** when something is normal vs different vs needs attention. Audio is not decoration — it's the attention router.

### 2. Visual — dashboards, education, presentation

- **Learnings** — Mochaccino builds the visualisation of learnings (the thinking/design surface).
- **Operating dashboards** — the Watchtower: glass-walled view of what ran, what won, what's stuck, what it cost. Warehouse state is part of this view.
- **Education & presentation** — the visual layer also *teaches and presents* the system, not just live ops.

## Connections

| Channel | Direction | Where it lives |
|---------|-----------|----------------|
| Audio in (steer) | human → factory | `intake.md` — Q&A bot writes tickets |
| Audio out (events/summaries/feedback) | factory → human | Watchtower projections |
| Visual learnings | factory → human | `mochaccino/designs/` |
| Visual dashboards | factory → human | Watchtower (Warehouse + run telemetry) |
| Visual education/presentation | factory → human | Mochaccino / Watchtower |

## Open decisions

- **Audio-out engine** — ElevenLabs? system TTS? (the `elevenlabs-agents` skill exists)
- **Sound-effect vocabulary** — what distinct cues mean (done / failed / needs-you)
- **Summary-on-return trigger** — Watchtower projection? scheduled? on session open?
- **Does the Q&A bot get a name?** Samantha is the reference, not yet the name.
