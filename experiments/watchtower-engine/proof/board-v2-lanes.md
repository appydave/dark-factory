# board-v2-lanes — proof

- Added `experiments/watchtower-board/parse-concepts.mjs` exporting `parseConcepts(md)` → `[{lane, items:[{concept,status,pri}]}]` (strips bold, skips header+separator, keeps status/pri emoji verbatim).
- server.mjs: imports parseConcepts; new endpoint `GET /api/concepts` reads `backlog/concepts.md` → JSON lanes + counts.
- HTML: added Floor/Lanes header toggle; Lanes view renders each lane as a card-group of concept cards with status+pri emoji badges (reuses --vars + .card).
- Self-test `node parse-concepts.mjs` printed: **8 lanes, 48 items**.
- Floor view UNTOUCHED — only additive (toggle span, hidden lanes container, `if(view!=='floor')return` poll-pause); existing markup/CSS/state logic unchanged. `node --check` passes both files.
