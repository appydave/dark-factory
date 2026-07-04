# External research-agent queue — capture only, not scoped

**Raised:** 2026-07-04, mid-conversation while designing the DF-ADR format (see `docs/kdd/decisions/0044-adopt-a-canonical-df-adr-format.md`). Not built, not fully spec'd — this is a capture so the idea isn't lost, per "requirements-first, store for future ticketing."

## Status update 2026-07-04 (same day)

David asked to build the queue skeleton + hand it off, so this moved from "capture only" to "built,
awaiting execution": `kind: external-research` tickets now live in `engine/store/queue/` (3 seeded), and
`backlog/2026-07-04-research-agent-queue-handover.md` is the execution handover for whichever conversation
has access to the friend's agent. **The open questions below are still open** — the handover explicitly
defers to whatever that conversation discovers about the friend's agent's real capabilities, rather than
guessing here.

## The idea

David has a friend-operated online agent (not a Claude Code session, no file access, less capable than
Sonnet/Opus). Right now the pattern for using it is: a DF session curates a self-contained research packet
(narrow question + inlined context, since the external agent can't read files) and hands it over manually.

The ask: let a DF session **push new research tasks to a queue** the external agent can pull from, so
research happens **asynchronously, on the side**, while DF work continues — instead of a synchronous
hand-off each time.

## Why this isn't a generic "swarm fan-out"

Earlier framing in this conversation assumed N parallel agents (a swarm) that could be dispatched
concurrently and reconciled via majority vote. **Corrected: it's one (or a small, unknown number of)
external agent(s) run by a friend** — concurrency model unknown, likely sequential or friend-managed, not
something DF controls. So the "reconcile N divergent answers" half of the earlier fan-out-packet design
doesn't apply as-is; what's actually needed is closer to a **single-consumer work queue**, not a fan-out.

## How this maps onto Dark Factory's existing architecture

DF already has this exact shape internally — Switchboard/Watchtower's queue+claim model dispatches work to
Marshall/Swagger sessions. What's new here is an **external, non-Claude, no-file-access consumer type**:

- Today's queue items assume the consumer can run `claude` and read the repo. An external-agent task
  can't — it needs the packet-curation step (narrow question + context inlined as literal text) done
  *before* the task lands in the queue, not left for the consumer to figure out.
- **Open question: how does the external agent get notified/pull work?** Polling an endpoint? A shared doc
  the friend's setup watches? Unknown — depends on what access the friend's agent actually has (this needs
  asking the friend, not guessing).
- **Open question: how do results come back?** Given no file access outbound either (presumably), results
  need some return channel DF can read — could be the same shared surface, could be something else.
- **Open question: task schema.** If/when this gets built, the per-task shape from the earlier fan-out-packet
  draft (id/question/context/output_schema/depends_on) is probably still the right unit of work — just
  queued one at a time rather than fanned out N-wide.

## Not decided

- Whether this is worth building at all vs. keeping the manual hand-off.
- Where it would live if built (Switchboard extension? a standalone lightweight queue file? something else).
- Whether "research task" is the only task type worth queuing this way, or a broader pattern.

## Next step, if picked up

Ask David what the friend's agent setup can actually do (read a shared doc? call a webhook? poll an API?)
before designing anything — the mechanism is entirely constrained by that, not by DF's side.
