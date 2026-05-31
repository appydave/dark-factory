# Dark Factory — Intake

**Status**: new — 2026-06-01
**Companion docs**: `architecture.md` (the three roles), `dark-factory-living-system-spec.md` (eval levels + validation gate), `watchtower/context.md` (the ticket-driven conductor)

---

## What Intake is

The **front door** of the factory. Where ideas land before they're factory-worthy.

The three roles — Library (`canonical/`), Warehouse (`research/`), Platform (`.claude/workflows/`) — all assume the material already exists. Intake is the area *before* that. The inbox.

## Three forms an idea arrives in

- **David's head** — "I had an idea, let's investigate."
- **A paper** — external research to absorb (e.g. SkillOpt).
- **Someone else's work** — a skill, a pattern, a repo worth a look.

## The rule: anything can enter, nothing is trusted

Intake is open. The Warehouse is **not** — hard rule: `research/` only takes recon/discover/distill/eval output. So ideas need their own room; they can't be dumped into the Warehouse.

But entering Intake ≠ being good. **The validation gate is the gate, not the door.** Only validated learning crosses into Warehouse/Library.

## The flow

```
Idea (you)   ─┐
Paper         ├─→  INTAKE  →  EXPERIMENT  →  LEARNING  →  [validation gate]  →  Warehouse / Library
Other's work ─┘    (capture)   (test it)     (good/bad)
```

- **Capture** — idea becomes a ticket (`backlog/<date>-<slug>.md` or an `experiment.yml`).
- **Experiment** — spin it up any time of day; it adds learning, good or bad. Lives in `experiments/`.
- **Learning** — every run emits a `learning.yml` (the 9-layer taxonomy). Negative results count.
- **Gate** — SkillOpt discipline: cross into the Library only on strict held-out improvement.

## The Q&A bot — the spoken front door

You should be able to *talk* to an agent — think Samantha — and have it start work.

**Key rule: kicking off a task writes a ticket; it does not spawn a Claude Code session.** The bot captures the idea, files the ticket, and the Platform picks it up.

(This is the ticket-driven conductor model — light reference: see `watchtower/context.md`.)

Audio is one of two first-class human-comms channels (the other is visual dashboards/presentation). The full principle lives in `human-comms.md`.

## Open decisions

- **Where the inbox physically lives** — reuse `backlog/` + `experiments/`, or a dedicated `intake/`?
- **Capture surface** — the Q&A bot, a CLI, a watched file?
- **Triage** — who turns a raw idea into a well-formed experiment ticket?
