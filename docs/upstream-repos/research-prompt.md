# Research Prompt (verbatim) — Fleet-of-CLI-Sessions Orchestrators

**Used:** 2026-06-10 · **Skill:** `deep-research` · **Run ID:** `wf_cab05fdc-97e`

Preserved verbatim so the research is reproducible. See [`2026-06-10-fleet-orchestrator-research.md`](./2026-06-10-fleet-orchestrator-research.md) for the method writeup and findings.

---

> Find open-source projects that orchestrate **FLEETS of coding-agent CLI sessions** — a control plane that spawns, dispatches work to, monitors, and tears down multiple **Claude Code** or **OpenAI Codex CLI** sessions as isolated workers, with a conductor/orchestrator layer on top. This is the "agent-fleet manager" / "multi-agent orchestration OS" class — **NOT** single-agent chat wrappers, **NOT** IDE plugins, **NOT** in-process agent libraries.
>
> **HARD REQUIREMENTS per result:**
> - Open source with publicly readable code (link the GitHub repo).
> - Report star count + activity (last commit, open issues) to gauge traction. Prefer 500+ stars, but include 2-3 promising sub-500 repos if the architecture is strong.
> - Must drive Claude Code, Codex CLI, or comparable agentic CLIs as the execution unit — or be model/CLI-agnostic orchestrators that explicitly support them.
>
> **FOR EACH PROJECT REPORT:**
> 1. One-line "what it is" + GitHub URL + stars + last-commit date.
> 2. Architecture: how it dispatches jobs, where shared state lives (central service vs per-worker vs files), how it monitors liveness, how it reaps/cleans up finished workers.
> 3. Human-in-the-loop model: human gating between jobs, or fully autonomous?
> 4. Observability: what dashboard / status / telemetry it ships (or lacks).
> 5. Closest overlap with this reference design — a "talk-to-it agent factory" with a STATELESS floor plus separate state-plane services (a comms bus, session telemetry, resource-health, and a visual control plane) — and where it differs.
>
> **SPECIFIC THINGS TO HUNT FOR / VERIFY BY NAME** (confirm each actually exists and is real, don't assume; report real current star counts): claude-flow / ruflo, Claude Squad, Conductor (the Claude Code orchestrator app), Crystal, OpenAI Swarm / OpenAI Agents SDK, Codex-based orchestrators, git-worktree-based parallel-agent runners, tmux-based multi-Claude session managers, Anthropic's multi-agent research harness, and the library-class tools AutoGen / CrewAI / LangGraph (note these as the in-process LIBRARY class and CONTRAST them against the fleet-of-CLIs class rather than listing them as matches).
>
> **DELIVERABLE:** a ranked table (ranked by relevance to the fleet-of-CLI-sessions class, NOT by stars), then a short "closest 3 to study" section with what to steal from each and what they get wrong. Flag anything that's vaporware or abandoned.

---

## Why it's shaped this way

- **The `NOT` clauses do the heavy lifting** — without them every search drowns in CrewAI/AutoGen/LangGraph (the *library* class). Naming them explicitly forces contrast, not listing.
- **"Verify by name, report current stars"** — guards against trusting model memory for fast-drifting facts.
- **Fixed per-result report shape** — turns "who else does this" into a structured, comparable, fact-checkable table.
- **Ranked by relevance, not stars** — the architecturally-closest match (CAO, ~694★) is more useful than the most popular (Claude Squad, ~7.8k★).
