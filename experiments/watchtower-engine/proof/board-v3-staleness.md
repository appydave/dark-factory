# board-v3 · idea-staleness (exp-20260606-board-v3)

- parse-concepts.mjs: each item now carries `line` (1-based source line in concepts.md); self-test still prints `<N> lanes, <M> items`.
- Added EXPORTED PURE `attachStaleness(lanes, lineDateMap, nowMs, staleDays)` — no git/IO; sets per-item `lastTouched/ageDays/stale` and per-lane `lastTouched(max)/ageDays/stale`.
- server.mjs only: runtime `gitLineDates()` (execFile `git blame --line-porcelain backlog/concepts.md`, cwd=repo root) → {line:epochMs}; /api/concepts now parse→blame→attachStaleness(…,Date.now(),14). git failure → empty map (all fresh), endpoint never crashes.
- Lanes UI additive: per-card age badge (`new`/`Nd`), `.stale` class (opacity .5 + muted border), `cold · Nd` hint in stale lane headers. Floor view + /api/state untouched.
- Mock-test (inline lineDateMap, no git): `staleness ok: 8 stale of 51`. Both files pass `node --check`.
