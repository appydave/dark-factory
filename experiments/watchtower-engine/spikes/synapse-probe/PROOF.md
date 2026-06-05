# Synapse probe — PROOF (2026-06-06)

Proves the keystone of the Watchtower comms-bus direction: **a Sentinel can push topic-filtered events over SSE, and a Claude Code `Monitor` consumes that stream directly to wake an in-session agent — no filesystem in the hot path.**

`server.py` — ~70-line stdlib SSE pub/sub broker. `GET /sse?subscribe=a,b` (server-side topic filter), `GET /pub?topic=X&msg=Y` (monotonic event id = basis for `Last-Event-ID` replay).

## Part (a) — deterministic (`run-probe.sh`)
A `marshall`-only subscriber received `id:1` and `id:3`; the `swagger-7` event (`id:2`) was **filtered out**. The id gap `1,3` is the proof event 2 existed but never reached this subscriber.
**RESULT: ✅ PASS** — SSE push + server-side topic subscription + monotonic ids.

## Part (b) — live Monitor (the synapse)
Broker running; armed a `Monitor` on `curl -sN ".../sse?subscribe=marshall" | grep --line-buffered '^data:'`. Published one `marshall` event and one `swagger-7` event.
- `marshall` event → **Monitor woke the in-session agent**: `data: SYNAPSE-LIVE-marshall-woke`.
- `swagger-7` event → **no wake** (filtered before reaching this subscriber).
- Monitor then timed out and auto-cleaned. Broker killed; port free; zero stray processes.
**RESULT: ✅ PASS** — external event → SSE (topic-filtered) → Monitor → agent woken, filesystem-free.

## What this licenses
The production bus = Sentinel (SSE/socket push, topic-filtered, durable event log) + Monitor (per-agent synapse subscribed to its topics). Files/`fswatch` are testing scaffold only. Durability gap (ephemeral SSE) is closed later by an event log + `Last-Event-ID` replay — not probed here, not an unknown. See `backlog/2026-06-06-dark-factory-sentinel.md`.
