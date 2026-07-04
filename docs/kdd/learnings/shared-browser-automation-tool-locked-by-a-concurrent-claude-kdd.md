---
topic: "Browser tool contention across sessions"
issue: "Shared browser automation tool locked by a concurrent Claude Code session"
created: "2026-06-08"
story_reference: "372250f1, 5eae009f"
category: "infrastructure"
severity: "low"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-engine/runs/run-cortex-render-004.json"]
commits: []
---

# Browser tool contention across sessions — Shared browser automation tool locked by a concurrent Claude Code session

## Problem Signature

**Symptoms**: mcp__playwright__browser_navigate failed with a browser-already-in-use error naming the shared Chrome profile path; falling back to mcp__chrome-devtools__navigate_page then failed with a Chrome-not-running / missing DevToolsActivePort error.

**Environment**: Swagger session verifying Mochaccino HTML renders via the shared local Chrome browser (dark-factory dev machine), while another process/session held the same Chrome profile.

**Triggering Conditions**: Two agent sessions (or a session plus a leftover process) both attempted to drive the same local Chrome browser instance via MCP browser tools at the same time.

## Root Cause
The Playwright MCP server and the chrome-devtools MCP fallback both target a single shared Chrome instance/profile by default; a concurrent session already had it locked, and no DevTools port was available for the fallback tool to attach to.

## Solution
Did not retry-loop on the browser lock. Treated the screenshot as optional confirmation and substituted non-visual verification: curl HTTP 200 checks on every rendered design and data JSON endpoint, plus the grep-based shape audit (svg/foreignObject/html_cards counts) already run for the render-quality check, then proceeded to complete the ticket.

Failures encountered:
```
Error: Browser is already in use for /Users/davidcruwys/Library/Caches/ms-playwright/mcp-chrome-12c231d, use --isolated to run multiple instances of the same browser
```
```
Could not connect to Chrome. Check if Chrome is running.
Cause: Could not find DevToolsActivePort for chrome at /Users/davidcruwys/Library/Application Support/Google/Chrome/DevToolsActivePort
```
Fallback verification used instead of a screenshot:
```
200  designs/index.html
200  designs/06-brain-anatomy/index.html
200  designs/03-four-memories/index.html
200  designs/04-brain-sleeps/index.html
200  designs/02-brain-remembers/index.html
200  data/06-brain-anatomy.json
```

## Prevention
When a browser-automation MCP tool (Playwright or chrome-devtools) reports a lock or a missing DevToolsActivePort, don't retry or fight it — substitute an equivalent non-visual proof (HTTP status checks plus a structural/text audit of the rendered output) and note in the run record that visual confirmation was skipped due to contention, rather than blocking the job on shared-browser availability.

## Related
- Sessions: 372250f1, 5eae009f
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 372250f1, 5eae009f · 2026-06-08 → 2026-06-09
- **Files** (candidate-level): experiments/watchtower-engine/runs/run-cortex-render-004.json
- **Commits** (candidate-level): —
