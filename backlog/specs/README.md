# Dark Factory — spec registry (the future-ticket store)

The home for **written-but-not-yet-built specs** = future development tickets. David's rule (2026-06-08): *write the requirements, store them for future ticketing, build later.* A spec landing here as `spec-written` is the "happy" bar — building is a separate, later decision.

**Modeled on Symphony** (`docs/watchtower/symphony-spec.md`): each ticket has a **key**, a **project**, a **priority** (integer, lower = higher, 1–4), and a **state**. Dispatch sorts by priority. At *build* time, Symphony's §7.1 run-states (Unclaimed → Claimed → Running → …) take over. This `tickets.json` is the **interim tracker**; the eventual home is a real Symphony work-management layer (its own future spec).

- `tickets.json` — the machine-readable registry (structure-first; the index/board renders from this).
- Spec docs live next to their domain (`backlog/specs/*.md`, `angeleye/docs/requirements/*.md`) — the ticket carries the `spec_path`.

**States:** `spec-todo` → `spec-written` → `ticketed` → `building` → `done`.
