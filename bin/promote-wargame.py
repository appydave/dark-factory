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
  bin/promote-wargame.py go T3-03           # promote AND print the run command (closes the two-step gap)
  bin/promote-wargame.py go --next 3        # promote next N AND print the run command
                                            #   go prints NO run command if nothing was promoted (empty-run guard)

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

# the ONE run-path, absolute so the cwd trap can't recur (see docs/factory-console-skill-spec.md)
RUN_COMMAND = (
    "cd /Users/davidcruwys/dev/ad/apps/dark-factory/engine && \\\n"
    "  python3 orchestrator.py --pool 1 --model sonnet --max-wall 3600 --worker-timeout 1800"
)

def promote(sid, staged, force=False):
    """Promote one staged ticket into the queue. Returns True on success, else prints
    the reason and returns False (callers decide whether to hard-exit)."""
    if sid not in staged:
        print(f"no staged ticket {sid}"); return False
    p, j = staged[sid]
    if sid in SELF_HOSTING and not force:
        print(f"{sid} is SELF-HOSTING (runs/kills the engine) — run attended, not engine-dispatched. --force to override."); return False
    _, _, done = state_sets()
    unmet = [d for d in j.get("depends_on", []) if d not in done]
    if unmet and not force:
        print(f"{sid} blocked by unmet deps: {unmet}. --force to override."); return False
    if j["ticket"] in done and not force:
        print(f"{sid} ({j['ticket']}) is already in done/ — use --force to deliberately re-run."); return False
    dest = QUEUE / f"{j['ticket']}.json"
    if dest.exists():
        print(f"{dest} already queued"); return False
    shutil.copy2(p, dest)
    print(f"promoted {sid} -> {dest.relative_to(ROOT)}")
    return True

def next_ready(staged, n):
    ready = [r for r in status(staged) if r[2] == "ready" and not r[3]]
    ready.sort(key=lambda r: (r[1] != "high", r[0]))
    return [r[0] for r in ready[:n]]

def reminder():
    print("REMINDER: run the orchestrator with a raised wall for war games, e.g.")
    print(f"  {RUN_COMMAND}")

def go(sids, staged, force=False):
    """Promote sids AND print the run command — but ONLY if at least one was promoted
    (the empty-run guard, in code: no silent run of an empty queue)."""
    promoted = sum(1 for sid in sids if promote(sid, staged, force=force))
    if promoted:
        print("\nRUN — paste this into another terminal (this seat dispatches, it does not run):")
        print(f"  {RUN_COMMAND}")
    else:
        print("\nnothing promoted — NO run command (empty-run guard). Nothing to run.")
    return promoted

def main():
    args = sys.argv[1:]
    staged = load()
    if not args or args[0] == "--list":
        for sid, pri, st, host, title in status(staged):
            print(f"{sid:7} {pri:6} {st:10} {host:9} {title}")
        return
    force = "--force" in args
    if args[0] == "go":
        rest = [a for a in args[1:] if a != "--force"]
        if rest and rest[0] == "--next":
            n = int(rest[1]) if len(rest) > 1 else 1
            sids = next_ready(staged, n)
            if not sids:
                print("no ready tickets to promote — NO run command (empty-run guard).")
                return
        elif rest:
            sids = [rest[0]]
        else:
            sys.exit("go needs a ticket id or --next N")
        go(sids, staged, force=force)
        return
    if args[0] == "--next":
        n = int(args[1]) if len(args) > 1 else 1
        for sid in next_ready(staged, n):
            promote(sid, staged)
        reminder()
        return
    if promote(args[0], staged, force=force):
        reminder()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
