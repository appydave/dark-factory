> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0026: Design-lint built as a standalone staged dark-factory tool; placement left open

**Status:** Proposed (reconstructed)


## Context
Millwright's form-decision step required picking where a new post-render design-QA capability ('design-loop pass') should live. Dark-factory's CLAUDE.md rule requires skill code to be staged in dark-factory's tools/ before touching the tracked appydave-plugins repo where the render engine (Mochaccino/Shelly/Mocha) actually lives, but David's own instinct was that a post-render self-check is really a mode of Mochaccino/Shelly (Shelly's own gate applied to Shelly's own output), not a separate tool.

## Decision
Build tools/design-lint/ (RUBRIC.md + shoot-one.py + README.md) as a free-standing staged tool in dark-factory now, explicitly not wired into Shelly/Mochaccino in appydave-plugins, and record the placement question as an open, dated backlog item for David to resolve later rather than resolving it unilaterally.

## Alternatives Considered
Building design-lint directly as a mode inside Mochaccino/Shelly in appydave-plugins was the other option — Shelly's own gate checking Shelly's own output, avoiding the pattern of coining a separate tool for what is really a mode of an existing engine. Not taken because it would touch David's tracked plugins repo without his go-ahead, and dark-factory's CLAUDE.md hard rule is to stage skill code here first.

## Consequences
The Playwright screenshot logic and rubric are proven for the mechanical half (clean PNG output) and for no-false-positives (correctly did not flag known-good controls), but live in a location David flagged as possibly wrong. A dated backlog item (backlog/2026-06-10-design-lint-placement-question.md) parks the reconsideration so it is not lost to memory alone. True-positive proof (correctly flagging a real brand-cold render) is still pending because the source deck lives on a different machine.

## Related
- Sessions: a69afeb2

## Provenance
- **Sessions** (1): a69afeb2 · 2026-06-09
- **Files** (candidate-level): CLAUDE.md, backlog/2026-06-10-design-lint-placement-question.md, tools/design-lint/README.md, tools/design-lint/RUBRIC.md, tools/design-lint/shoot-one.py
- **Commits** (candidate-level): —
