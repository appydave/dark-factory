# C1 — First end-to-end Watchtower consumer run

This is the **first** time the Watchtower consumer ran a job end-to-end:
**claim → execute → record → done**, by hand, with no loop, no mutex, no monitor.

- **queue_id**: `q-20260605-c1-proof`
- **experiment_id**: `exp-20260605-watchtower-c1`
- **path through the engine**: `queue/` → `running/` → `done/` ✅
- **kind**: `instruction` (the simplest job type)
- **run record**: `runs/run-watchtower-c1-001.json`

The spine carries work. C1 proven.
