# War-Game Authoring Spec — portfolio 2026-07-06

Every war game in `backlog/wargames/` follows this template exactly. A war game is NOT a plan:
a plan assumes the happy path; a war game pre-simulates the fight. The executor is a
**sonnet-class Swagger** dispatched by `engine/orchestrator.py` — write for that reader:
concrete, literal, no implied context, no taste calls left open.

## Binding context (read before authoring)

- `plans/wargames/decisions.md` — locked decisions. No war game may contradict them.
- `engine/store/queue/.CONVENTION.md` — ticket JSON idiom.
- **Docs lag code in this repo.** Never assert current state from a strategy doc; every claim
  about what exists must be verified on disk by your recon or delegated to the executor's
  recon moves.

## File pair per candidate

1. `backlog/wargames/<id>-<slug>.md` — the war game (template below).
2. `backlog/wargames/tickets/<id>.json` — engine-idiom ticket (Family A), **staged, not
   queued** — Phase 5's promotion script drains them progressively. Shape:

```json
{
  "ticket": "wg-<id-lowercase>-<slug>",
  "kind": "instruction",
  "title": "<track-prefix>: <title>",
  "source": "backlog/wargames/<id>-<slug>.md (war-game portfolio 2026-07-06)",
  "executor": "swagger",
  "priority": "high | normal",            // NOW=high, NEXT=normal
  "requested_at": "<real UTC now — stamp via `date -u +%Y-%m-%dT%H:%M:%SZ`>",
  "requested_by": "david (war-game portfolio triage, 2026-07-06)",
  "depends_on": ["wg-..."],               // [] if none
  "prompt": "<self-contained: one-para mission + 'Read and execute the war game at <repo-relative path>. Follow its moves in order; on any failure signal apply the counter-move; on any abort condition stop and write needs-decision/.'>",
  "verify": "<prose acceptance bar, checkable by re-running a command>"
}
```

## War-game markdown template

```markdown
# <ID> — <Title>

| field | value |
|---|---|
| ticket | wg-<id>-<slug> |
| track / size / priority | ... |
| executor | sonnet Swagger via engine |
| depends_on | ... or none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission
What + why + what done looks like, one tight paragraph.

## Locked context
The specific decisions.md rulings that bind THIS ticket, restated in one line each.

## Recon (verify before any work)
Numbered checks of current disk/system state. Each: `command or file to check` → what you
expect → what it means if you don't find it. Docs lag code — these replace doc-trust.

## Moves
Numbered. EVERY move has all four lines:
- **Do:** the action, concrete enough to execute without judgment.
- **Expect:** the observation if it worked (exact file, output line, exit code, screen state).
- **Failure signal:** what you'd see instead if it didn't.
- **Counter-move:** the recovery action, or "→ Fork F<n>" or "→ Abort A<n>".

## Forks
F1, F2… Each: **Trigger** (the observation that forces the choice) → **Route A** (when/what)
/ **Route B** (when/what). Only real forks — no decorative branching.

## Assumptions ledger
What authoring-time recon could not resolve. Each: the assumption, why it's plausible, and
what the executor should do if it proves false (usually → needs-decision/).

## Abort conditions
A1, A2… Hard stops: the condition, and the exact park action (write
`engine/store/needs-decision/<ticket>.json` with the question; leave the ticket in running/;
never guess past an abort).

## Verification
The acceptance bar as executable checks (commands + expected output, files that must exist,
behaviours to demonstrate). Mirrors the JSON `verify` field. Include negative checks where
cheap (what must NOT have changed).

## Executor notes (sonnet)
Scope fence (what NOT to touch), style constraints, when to prefer HITL over guessing,
and the one most-likely rabbit hole with the instruction to skip it.
```

## Authoring rules

- **Grounded moves only.** If you haven't verified a path/flag/command exists (or put it in
  Recon), it can't appear in a Do line.
- **Second-order thinking.** For each move ask "and if the counter-move also fails?" — the
  second failure routes to a fork or abort, never to improvisation.
- **Assumptions are flagged, not resolved silently.** David's skipped interview items and
  anything genuinely undecidable go in the ledger with a false-branch action.
- **Right-size.** S ≈ 4–7 moves, M ≈ 6–10, L ≈ design-first (the war game's mission is then
  producing a design/spec + follow-on tickets, not the full build).
- **Cross-ticket honesty.** If another war game must land first, say so in depends_on and
  make Recon check for its artifacts.
- **No YLO/POEM work** (parked), **no `-p`/headless/SDK ever** (metered billing),
  **interactive `claude` only**, HALT/BACKOFF flags respected implicitly by the engine.
