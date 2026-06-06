# Observability & telemetry — measure, don't trust hearsay

**Raised**: 2026-06-06 (David). **Status**: open — on the queue.
**North Star**: observability/telemetry is a standing investment area (see `docs/north-star.md`).

## The trigger

A meetup claim — "Claude Code leaks to ~60GB RAM and crashes the box, so only 1 Claude Code instance per machine" — is shaping our parallelization model (distribute Swaggers across machines vs pile locally). But it's **⚠️ unverified hearsay**. We should **measure it ourselves**, not take a text model's or anyone's word for it.

## The class-level fix

Stand up real observability for the factory's own runtime so claims like this are answered with data, and system health is always visible — not discovered after a crash.

## Smallest move (and it's nearly free — the substrate exists)

Switchboard's `poll-command` recipe already runs `ps -Ao pid,ppid,user,pcpu,pmem,etime,comm` and writes a Signal snapshot. So:
1. **Verify the 60GB claim:** have Switchboard archive periodic snapshots and chart Claude Code / Swagger **RSS over time** — does a long-running Claude Code instance actually balloon? Confirm or kill the "1 per machine" constraint with our own numbers.
2. **Surface it:** Watchtower (control plane) visualises per-process RAM/CPU + open-Swagger count — the always-visible system-health view.
3. Feed it back into the parallelization model: if the leak is real, the distribute-don't-pile rule stands on evidence; if not, we can pile more locally.

## Done when

- We have our own RAM-over-time data on Claude Code instances (claim confirmed or refuted with numbers).
- System health (per-process resource use, open Swaggers) is visible without guessing.
