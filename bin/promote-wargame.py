#!/usr/bin/env python3
"""Promote staged war-game tickets into the engine queue, dependency-aware.

Staged tickets live in backlog/wargames/tickets/<ID>.json (never auto-queued).
Promotion copies one into engine/store/queue/ so the orchestrator (or auto-wake,
if armed) picks it up. Progressive drain by design — promote a few, watch, repeat.

Usage:
  bin/promote-wargame.py --list             # portfolio status: ready / blocked / queued / done
  bin/promote-wargame.py T3-03              # promote one ticket (deps must be done)
  bin/promote-wargame.py T3-03 --force      # promote even with unmet deps
  bin/promote-wargame.py --next 3           # promote the next N ready tickets (high priority first)

Caveats baked in (from the authoring run's systemic flags):
  * SELF-HOSTING tickets (their war game runs orchestrator.py / kills df-worker
    sessions) refuse engine promotion — run those attended. Marked in the list.
  * WORKER_TIMEOUT is 240s in orchestrator.py; multi-move war games usually need
    longer. Promote expects you to run the orchestrator with --max-wall raised
    (e.g. 3600) for war-game tickets; a warning prints on every promotion.
"""
import json, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGED = ROOT / "backlog" / "wargames" / "tickets"
QUEUE = ROOT / "engine" / "store" / "queue"
DONE = ROOT / "engine" / "store" / "done"
RUNNING = ROOT / "engine" / "store" / "running"

# war games that boot/kill the engine or saturate usage: never engine-dispatched
# tickets that must NOT be engine-dispatched: their war game RUNS or KILLS the engine (spins up a
# nested orchestrator / reboots the worker pool), so an engine-dispatched worker would murder its
# own session. Editing engine code is NOT self-hosting (Python doesn't hot-reload — a worker can
# edit orchestrator.py while the orchestrator runs; the change lands on the next launch).
SELF_HOSTING = {"T1-01", "T1-02", "T1-03", "T1-05", "T1-06"}

def load():
    staged = {}
    for p in sorted(STAGED.glob("T*.json")):
        j = json.loads(p.read_text())
        staged[p.stem] = (p, j)
    return staged

def state_sets():
    def names(d):
        out = set()
        for p in d.glob("*.json"):
            try:
                out.add(json.loads(p.read_text()).get("ticket", p.stem))
            except Exception:
                out.add(p.stem)
        return out
    return names(QUEUE), names(RUNNING), names(DONE)

def status(staged):
    queued, running, done = state_sets()
    rows = []
    by_ticket = {j["ticket"]: sid for sid, (_, j) in staged.items()}
    for sid, (p, j) in staged.items():
        t = j["ticket"]
        if t in done: st = "done"
        elif t in running: st = "running"
        elif t in queued: st = "queued"
        else:
            unmet = [d for d in j.get("depends_on", []) if d not in done]
            st = f"blocked({len(unmet)})" if unmet else "ready"
        rows.append((sid, j["priority"], st, "SELF-HOST" if sid in SELF_HOSTING else "", j["title"][:70]))
    return rows

def promote(sid, staged, force=False):
    if sid not in staged:
        sys.exit(f"no staged ticket {sid}")
    p, j = staged[sid]
    if sid in SELF_HOSTING and not force:
        sys.exit(f"{sid} is SELF-HOSTING (runs/kills the engine) — run attended, not engine-dispatched. --force to override.")
    _, _, done = state_sets()
    unmet = [d for d in j.get("depends_on", []) if d not in done]
    if unmet and not force:
        sys.exit(f"{sid} blocked by unmet deps: {unmet}. --force to override.")
    if j["ticket"] in done and not force:
        sys.exit(f"{sid} ({j['ticket']}) is already in done/ — use --force to deliberately re-run.")
    dest = QUEUE / f"{j['ticket']}.json"
    if dest.exists():
        sys.exit(f"{dest} already queued")
    shutil.copy2(p, dest)
    print(f"promoted {sid} -> {dest.relative_to(ROOT)}")
    print("REMINDER: run the orchestrator with a raised wall for war games, e.g.")
    print("  cd engine && python3 orchestrator.py --pool 1 --model sonnet --max-wall 3600 --worker-timeout 1800")

def main():
    args = sys.argv[1:]
    staged = load()
    if not args or args[0] == "--list":
        for sid, pri, st, host, title in status(staged):
            print(f"{sid:7} {pri:6} {st:10} {host:9} {title}")
        return
    if args[0] == "--next":
        n = int(args[1]) if len(args) > 1 else 1
        ready = [r for r in status(staged) if r[2] == "ready" and not r[3]]
        ready.sort(key=lambda r: (r[1] != "high", r[0]))
        for sid, *_ in ready[:n]:
            promote(sid, staged)
        return
    promote(args[0], staged, force="--force" in args)

if __name__ == "__main__":
    main()
