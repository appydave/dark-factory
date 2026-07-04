---
domain: "infrastructure"
name: "Dispatched worker/Swagger tmux windows don't auto-close without an active reaper"
status: "proposed"
created: "2026-06-05"
story_references: ["2df0e613", "307792ae", "627e86a2", "98af2b78"]
last_updated: "2026-06-11"
recurrence_count: 4
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["backlog/2026-06-06-swagger-lifecycle.md", "experiments/watchtower-engine/bin/dispatch-swagger.sh", "experiments/watchtower-engine/bin/reaper.sh", "experiments/watchtower-engine/registry/", "experiments/watchtower-engine/running/"]
commits: ["2d09641"]
---

# infrastructure — Dispatched worker/Swagger tmux windows don't auto-close without an active reaper Pattern

## Context
Dozens of `claude` processes were found running, including one spawned to process a queue ticket that had been idle for 22 hours after completing its job, plus several stray bypass-mode sessions left over from earlier test runs.

Interactive `claude` sessions never exit on their own; they persist at the REPL indefinitely. The only designed cleanup path (closing the window once the job lands in the done folder) requires the window to exist in the Orchestrator's own tmux server AND requires the Orchestrator to actually observe the handback — anything spawned out-of-band or missed by the watcher becomes an invisible, indefinitely-running process.

## Implementation
Diagnosed by cross-referencing every claude-shaped OS process (pid, elapsed time, full command) against the live tmux window list, isolated the genuinely stray process by its multi-hour elapsed time and job-specific command line, and killed it after confirming it was not a live working session.

## Examples
```bash
# find every claude/tmux-shaped process with elapsed time, cross-check against live windows
ps -eo pid,ppid,tty,etime,command | grep "[c]laude" | grep -v "Claude.app|Claude Helper"

# identified stray: PID 93734, up 22h, cmd contains "Process the next ticket in experiments/watchtower-engine/queue/"
kill 93734 2>/dev/null && echo "killed 93734" || echo "(already gone)"
```

## Rationale
Interactive `claude` sessions never exit on their own; they persist at the REPL indefinitely. The only designed cleanup path (closing the window once the job lands in the done folder) requires the window to exist in the Orchestrator's own tmux server AND requires the Orchestrator to actually observe the handback — anything spawned out-of-band or missed by the watcher becomes an invisible, indefinitely-running process.

## Anti-Patterns
Give every spawned Worker a visible registry entry at spawn time ({queue_id, window, pid, tty, purpose, started_at} written to a known directory, deleted on clean close) so a simple directory listing answers 'what is each open worker and why' even before any auto-reaping exists. A periodic sweep can then reap registry entries whose job has completed and are older than a grace window.

## Related
- Originated from learnings:
  - A Swagger job was dispatched without arming the reaper monitor loop, so even though the Swagger completed and bookkept correctly (run record + handback + moved to done/), its tmux window never auto-closed.
  - A dispatched Swagger's tmux window and registry entry remained after its job completed, because no reaper loop was running to auto-close it.
  - Interactive Swagger spawns in tmux never self-close because the Claude process stays alive at the REPL after finishing.
  - Spawned worker sessions (interactive `claude` in a tmux window) idle at the REPL forever once their job finishes, and closing the tmux window alone does not guarantee the underlying process is cleaned up — it only helps when the window is still tracked by the same tmux server the Orchestrator controls.
- Related patterns: []
- ADRs: []

## Provenance
- **Sessions** (4): 2df0e613, 307792ae, 627e86a2, 98af2b78 · 2026-06-05 → 2026-06-11
- **Files** (candidate-level): backlog/2026-06-06-swagger-lifecycle.md, experiments/watchtower-engine/bin/dispatch-swagger.sh, experiments/watchtower-engine/bin/reaper.sh, experiments/watchtower-engine/registry/, experiments/watchtower-engine/running/
- **Commits** (candidate-level): 2d09641
