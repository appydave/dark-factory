# Resume handover — 2026-06-07 (paste the block below to resume at this point)

This file backs up the copy-paste resume block. Resume point = **just after the Symphony re-look, at the "how do we build the AngelEye change?" fork.**

---

RESUME POINT — Dark Factory / Marshall, 2026-06-07 (~morning).

WHERE WE ARE (today, all committed + in memory):
- Engine-state REAPER proven live (bin/reaper.sh + dispatch registry; auto-closes finished Swaggers, no Marshall memory). Standing reaper Monitor may be armed.
- Constellation PREFLIGHT built + in Marshall doctrine (bin/constellation-status.sh; required = Switchboard + AngelEye).
- AngelEye STARTED (server :5051, client :5050, backfilling transcripts) — NOT daemonized (don't daemonize until the Sentinel/control-plane split), live-hook NOT wired.
- Canonical HOOKS spec adopted as grounding (~/dev/ad/brains/anthropic-claude/claude-code/hooks/, 30 events; ignore deprecated hooks-reference.md).
- SYMPHONY RE-LOOK done (docs/watchtower/symphony-relook-2026-06-07.md): our dispatch registry = Symphony OrchestratorState.claimed + claim state machine (§4.1.8/§7.1); the reaper's deferred STUCK case = Symphony §8.5 stall detection, keyed off the agent EVENT STREAM (last_event_timestamp + stall_timeout), NOT the process tree — i.e. exactly the AngelEye live-hook direction, validated.

THE ACTIVE DECISION (where we paused):
Next move was "handoff note vs dispatch a real backlog item" (continuing G = run real work through the loop, reaper armed).

THE FORK INTRODUCED IN THIS DISCUSSION (the reason for this handover):
How should we BUILD the AngelEye live-hook change?
- AngelEye + several apps were built with David's RALPHY plugin (advanced Ralph-Wiggum loop). Build knowledge is baked into AngelEye's agent.md.
- Native path (NOW): requirement-note → run Ralphy IN the AngelEye folder.
- Tempting future path: author the spec with an Osmani agent-skill; or dispatch a code-build to a Swagger using 2-3 Osmani skills ("factory builds the constellation"). But that needs the Ralphy/agent.md context first.
- North Star reflection: the 1,100-prompt SDLC-automation census is more SIDE QUEST than the full North Star; the machinery (Path 1) is the truth — and we've been doing SDLC automation this weekend already (dispatched code builds).

RECOMMENDATION (Marshall's):
- For NOW: AngelEye change = requirement-note → Ralphy, built IN AngelEye (app-ownership, low-risk). The live-hook's purpose per the Symphony re-look: expose per-session last-active so the reaper's stuck-case can do stall detection.
- The "factory builds AngelEye via Osmani skills + Swagger" exploration is a SEPARATE focused session, done IN the AngelEye/Ralphy folder where agent.md lives — not from dark-factory.
- Don't fully tangent from dark-factory; this handover makes the tangent safe.

RESUME OPTIONS:
(a) Continue today's path: write the AngelEye live-hook HANDOFF NOTE (requirement, to run via Ralphy in AngelEye), grounded in the canonical hooks spec (30 events, :5051) + Symphony §8.5 stall-detection purpose.
(b) Continue G: dispatch a real buildy backlog item through the loop (reaper armed).
(c) Pivot to the AngelEye/Ralphy exploration as its own session (understand Ralphy + agent.md; evaluate Osmani skills; decide factory-builds-the-app) — do it IN the AngelEye folder.

POINTERS: memories ralphy-plugin-builds-apps, osmani-agent-skills, canonical-hooks-spec, cleanup-is-harness-driven-not-remembered (stuck-case mechanism), capability-placement-and-reassessment. Docs: docs/watchtower/symphony-relook-2026-06-07.md, reaper-brief.md, build-state.md. Plan: backlog/2026-06-07-day-possibilities.md.
