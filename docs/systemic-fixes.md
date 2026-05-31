# Dark Factory — Problems & Systemic Fixes

**Status**: new — 2026-06-01
**Companion docs**: `intake.md` (signals enter here), `human-comms.md`, `architecture.md` §13 (principles), `dark-factory-living-system-spec.md` (the validation gate)

---

## Two things, one doc

1. A place to **note every suspected problem** in the system.
2. A **first principle** for how we respond to them.

## The problem register

We must be able to log anything that feels wrong — a defect, friction, a missing capability, "I can't see X." Capture is cheap; let nothing fall through.

**But a register is not a graveyard.** Logging a problem isn't progress. The value is triage + the response discipline below. (Where it physically lives — `backlog/`, a `problems.jsonl`, or its own area — is an open decision.)

## First principle: fix the class, not the instance

When we fix something, we **consider the bigger picture as we do it.** The question is never just "how do I fix this one thing" — it's:

> *What system, workflow, or skill would fix this properly — and the next ten like it?*

- "I can't visualise X" → maybe we need a **presentation system**, not one chart.
- "Work on the docs" → maybe the move is a **doc-organisation capability** (cf. Lexi in the brains), not one more file.
- A bug in one workflow → maybe a **lint/validator** that catches the whole class.

The output of a fix is often a **workflow, agent, or skill** — not a patch.

### The guard rail (don't go overboard)

Systemic ≠ build-an-app-because-David-had-an-idea. The discipline is to *consider* the higher altitude and then pick the **smallest move that fixes the class.** Sometimes that's still a one-line patch. **Name the altitude you chose and why.**

## Anti-sycophancy: good/bad is a hypothesis, not gospel

David reports **feelings**, not verdicts. "This is good" / "this is bad" is a signal to investigate — not an instruction to obey.

- A sycophant ships the human's suggestion and creates ten new problems. **Don't.**
- Challenge is required, not optional. Push back when the evidence or the system view disagrees.
- Treat every good/bad as a claim to validate — this is the same discipline as the validation gate (`dark-factory-living-system-spec.md`): nothing is trusted until it earns it.
