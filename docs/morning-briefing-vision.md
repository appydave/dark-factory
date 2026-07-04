# Morning Briefing — the full vision (and why we stopped at one project)

**Status**: 2026-07-04 — David deliberately parked the "add project #2" ticket as premature. This doc holds the real scope so it isn't lost, and names the dependencies that must exist first.

## What the briefing really is (David, 2026-07-04)
Not "a second config file." The briefing is: **anything I worked on, noted and summarized** — code projects, **brains** (change constantly, untracked), **client directories** — plus, later, external feeds: **email, calendar events** (out of scope for now), and ticket streams (**Linear, Watchtower, Switchboard**).

## Why one-project-at-a-time config doesn't scale to that
Adding projects by hand-written config presumes we know the project list. We don't, reliably:
- `~/.config/appydave/locations.json` (~100 paths incl. clients/brains) is the closest thing to "everything David touches" but conflates jump-locations/apps/repos/ports (known debt, OMI 2026-06-29) and `dev-inventory` is dead on every machine.
- `app-registry` covers only the ~40 factory-lens apps — it probes git activity for those, nothing else.
- Nothing tracks activity on brains or client dirs at all.

## Dependency chain (build order, when its time comes)
1. **Universal activity registry** — one sweep over every locations.json path (+ brains): git last-commit / file mtimes → "what changed since yesterday, everywhere." (Natural extension of app-registry's probe; the registry-conflation fix rides along.)
2. **Digest-over-activity** — the briefing iterates *what actually changed*, not a hand-list of configs. Per-project config becomes an override, not the entry ticket.
3. **Feed layer** — tickets (Linear, Watchtower/Switchboard queues) folded into NEEDS-YOU / IN-FLIGHT.
4. **External life feeds** — email/calendar (explicitly out of scope for now; life-lane privacy rules apply — see brain vision doc).

## What exists today (don't rebuild)
- This app: the §2 briefing box over ONE project (dark-factory), proven; config seam `projects/<id>.json`.
- app-registry probe + `query.py` (the pattern step 1 extends).
- omi-fetch store/events (first feed-shaped source) · engine store (ticket state).

## Related
- The parked ticket: `dark-factory/engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json` (marked deferred, points here).
- Daily operating model §2 (the briefing contract): `~/dev/ad/apps/dark-factory/docs/daily-operating-model.md`
