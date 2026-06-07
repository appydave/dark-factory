# board v4 — Floor↔Lanes bridge

- Endpoint: `POST /api/promote` accepts `{concept, lane}` → writes a valid queue ticket to `engine/queue/<queue_id>.json`, returns `{accepted:true, queue_id}`.
- Ticket: `kind:instruction`, `experiment_id:exp-promoted`, `args:{from:'lanes-board',lane}`, `requested_at` ISO from OS clock; `queue_id = 'q-'+Date.now()+'-promoted-'+slug` (slug sanitized: `[a-z0-9-]` only, no `/` or `..`).
- UI: each Lanes concept card gets a `promote ▶` button (delegated handler) → POST → shows `promoted → <queue_id>`.
- Tested: `node selfcheck-promote.mjs` asserts ticket shape + JSON round-trip via temp dir; `node --check` clean; `listen` guarded so import never touches :7430. No servers started/killed.
- Untouched: Floor view, `/api/state`, `/api/concepts`, staleness logic — additive only, pure Node + vanilla JS, no deps.
