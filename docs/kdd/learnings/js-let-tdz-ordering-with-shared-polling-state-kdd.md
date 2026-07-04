---
topic: "JS let TDZ ordering, shared polling state"
issue: "JS let TDZ ordering with shared polling state"
created: "2026-06-06"
story_reference: "5a5b5de5"
category: "debugging"
severity: "low"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-board/server.mjs"]
commits: []
---

# JS let TDZ ordering, shared polling state — JS let TDZ ordering with shared polling state

## Problem Signature

**Symptoms**: Adding a second view (Lanes) to a dependency-free Node HTTP server's single-page client script, which shares a `#counts` DOM element with the existing Floor view's `tick()`/`setInterval` poller. A naive first attempt declared the new `let view='floor';` state variable near the bottom of the script (after the Lanes-specific functions, right before `show()`), but `tick();setInterval(tick,2000);` is invoked earlier in the same script, before that declaration point would execute.

**Environment**: experiments/watchtower-board/server.mjs — inline client-side `<script>` block in a template string served by the board's Node http server (:7430)

**Triggering Conditions**: Adding a shared gate variable (`view`) that a pre-existing, already-invoked polling function (`tick()`) needs to read, when the new variable is declared later in top-to-bottom script order than the point where the poller already runs.

## Root Cause
`let`/`const` bindings are hoisted to the top of their scope but stay in the temporal dead zone (TDZ) until the declaration statement actually executes. `tick()` runs at `tick();setInterval(tick,2000);`, which executes before a `let view=...` declared further down in the script would have run — so reading `view` inside `tick()` would throw a ReferenceError the first time the interval fires, well before the later `let view` line is ever reached.

## Solution
Move the `let view='floor';` declaration to the top of the script (right after the `esc()` helper, before `function ticket()` and before `tick();setInterval(tick,2000);` is called), then add `if(view!=='floor')return;` as the first line of `tick()` to pause Floor polling while Lanes is shown, and delete the now-duplicate `let view='floor';` that had been placed later near `show()`.

```diff-before
const el=(id)=>document.getElementById(id);
const esc=(s)=>(s||'').replace(/[<&]/g,(c)=>({'<':'&lt;','&':'&amp;'}[c]));
function ticket(t,cls){return '<div class="card '+cls+'">'+
```
```diff-after
const el=(id)=>document.getElementById(id);
const esc=(s)=>(s||'').replace(/[<&]/g,(c)=>({'<':'&lt;','&':'&amp;'}[c]));
let view='floor';
function ticket(t,cls){return '<div class="card '+cls+'">'+
```

```diff-before
async function tick(){
 try{const s=await (await fetch('/api/state')).json();
```
```diff-after
async function tick(){
 if(view!=='floor')return;            // pause floor polling while Lanes is shown
 try{const s=await (await fetch('/api/state')).json();
```

```diff-before
}
let view='floor';
function show(v){view=v;
```
```diff-after
}
function show(v){view=v;
```

## Prevention
Dev: when a new shared-state variable must be read by an existing, already-invoked function, declare it above that invocation point in script order, not appended at the point of the new feature's code — `let`/`const` have no forward-reference safety net the way hoisted `function` declarations do.

## Related
- Sessions: 5a5b5de5
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 5a5b5de5 · 2026-06-06
- **Files** (candidate-level): experiments/watchtower-board/server.mjs
- **Commits** (candidate-level): —
