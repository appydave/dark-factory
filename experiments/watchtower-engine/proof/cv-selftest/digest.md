# Comprehension Digest — `experiments/watchtower-board`

**Target:** `experiments/watchtower-board` · **commit_sha:** `ce9bad99de9c94e4c0dab577b0e6d07ed6247336`
**Intent:** self-test — prove the comprehend→digest→brief path end-to-end on a small local target.
**Method:** single-pass read (target is 3 source files + 2 record files). Claims tagged ✅verified(file) · ⚠️inference · ❓unknown.

## What it is
A **read-only live VIEW** of the Dark Factory floor — the v1 "Watchtower" board ✅(`server.mjs:3-14`). It owns no state: it reads the engine dirs + tmux and renders them over HTTP on **:7430** ✅(`server.mjs:17,28`). Deliberately *not* inside Switchboard — respecting capability-placement; eventual home is the AppyStack "Watchtower" instance ✅(`server.mjs:6-9`). Every timestamp is OS-sourced (fs mtime / git), never a language model ✅(`server.mjs:11-12`).

## Architecture (layers)
- **View / HTTP server** — `server.mjs` (330 lines), an `node:http` server; renders Floor + Concept Lanes ✅(`server.mjs:16,28`).
- **Parse / staleness helpers** — `parse-concepts.mjs` (107 lines) turns `backlog/concepts.md` into structured lanes `[{lane, items:[{concept,status,pri}]}]` ✅(`parse-concepts.mjs:5-13`); `attachStaleness` flags ideas by git-blame committer-time ✅(imported `server.mjs:21`, `gitLineDates` `server.mjs:25-46`).
- **Data sources (read-only)** — the engine dirs (`../watchtower-engine`) and the repo's `backlog/concepts.md`, plus `git blame`/`git log` and tmux ✅(`server.mjs:23-25`).

No database or schema layer exists — the board is stateless and derives everything from the filesystem + git at request time ✅(`server.mjs:5-6`). (So no `matrix`/ER shape is warranted here.)

## Components
- `server.mjs` — the view + HTTP server + `gitLineDates` runtime helper (git-blame line→epoch map) ✅(`server.mjs:25-46`).
- `parse-concepts.mjs` — pure-Node markdown-table → lanes parser; runs standalone as its own self-test (`node parse-concepts.mjs` prints `<N> lanes, <M> items`) ✅(`parse-concepts.mjs:18`).
- `selfcheck-converge.mjs` (50 lines) — converge self-check harness (v5 fix) ⚠️inference(name + size; not line-read this pass).

## Key flow — concepts → board
`backlog/concepts.md` → `parseConcepts()` → `attachStaleness()` (git-blame committer-time vs `STALE_DAYS=14`) → rendered Concept Lanes view ✅(`parse-concepts.mjs:5-13`, `server.mjs:21,24`).

## 14-day change story (git, board path)
`9c408e9` v1 minimal live board → `323d02c` v2 Concept Lanes → `c9e7c8d` v3 idea-staleness (git-sourced last-touched) → `d400962` v4 Floor↔Lanes bridge + standing reaper → `070d687` v5 converge bridge + reaper keys off `done/` ✅(`git log --since='14 days ago'`).

## Provenance
All citations resolve against `experiments/watchtower-board` at commit `ce9bad99de9c94e4c0dab577b0e6d07ed6247336`. Phase 2 (Mochaccino/Peter) stamps this path+sha as `meta.source`.
