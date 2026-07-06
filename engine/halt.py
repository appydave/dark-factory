#!/usr/bin/env python3
"""halt.py — the factory kill switch.

One flag file, one convention, factory-wide: engine/store/HALT. Its mere
EXISTENCE means "stop starting new work"; its absence means "run normally."
No daemon, no lock server, no IPC — just a file any process can `stat()` in
a syscall, per dark-factory's own file-contract convention (docs/comms-flow.md
§4: state under a trusted repo path, never /tmp).

See docs/kill-switch-spec.md for the full convention (who may write it, what
it deliberately does NOT do — no process kills, graceful only — and the
cross-machine note).

Usage:
  python3 halt.py halt ["reason"] [--by <name>]   # write the flag, stop new work
  python3 halt.py resume                          # remove the flag, resume
  python3 halt.py status [--json]                 # print current state

Also importable — is_halted()/halt_info() are the two functions every other
factory process (orchestrator.py, warm_pool.py, the pulses) calls to check
state. Both are deliberately defensive: a missing, unreadable, or corrupt
HALT file is treated as "not halted" — this switch must never itself become
a crash vector for the processes it's meant to protect.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(ENGINE, "store")
HALT_PATH = os.path.join(STORE, "HALT")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_halted():
    """True iff the flag file exists. Never raises — a stat() failure for any
    reason other than "not found" (permissions, weird filesystem state) is
    still treated as not-halted, per the additive/backward-compatible rule."""
    try:
        return os.path.exists(HALT_PATH)
    except Exception:
        return False


def halt_info():
    """Returns the HALT file's {ts, by, reason} payload, or None if not
    halted. A halted-but-corrupt file still reads as halted (with '?' fields)
    rather than silently reporting "running" — existence is the ground truth,
    the payload is just detail."""
    if not is_halted():
        return None
    try:
        with open(HALT_PATH) as f:
            return json.load(f)
    except Exception:
        return {"ts": None, "by": None, "reason": None}


def write_halt(reason, by):
    os.makedirs(STORE, exist_ok=True)
    payload = {"ts": now_iso(), "by": by, "reason": reason}
    with open(HALT_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    return payload


def clear_halt():
    existed = os.path.exists(HALT_PATH)
    if existed:
        os.remove(HALT_PATH)
    return existed


def cmd_halt(args):
    payload = write_halt(args.reason, args.by)
    print(f"HALTED -> {HALT_PATH}")
    print(json.dumps(payload, indent=2))


def cmd_resume(args):
    existed = clear_halt()
    if existed:
        print(f"RESUMED -> removed {HALT_PATH}")
    else:
        print("Already running -- no HALT file present.")


def cmd_status(args):
    info = halt_info()
    if args.json:
        print(json.dumps({"halted": info is not None, "info": info, "path": HALT_PATH}, indent=2))
        return
    if info is None:
        print("RUNNING -- no HALT file present.")
        return
    print("=" * 50)
    print("   FACTORY HALTED")
    print("=" * 50)
    print(f"  since:  {info.get('ts', '?')}")
    print(f"  by:     {info.get('by', '?')}")
    print(f"  reason: {info.get('reason', '?')}")
    print(f"  flag:   {HALT_PATH}")
    print("=" * 50)


def main():
    ap = argparse.ArgumentParser(
        description="dark-factory kill switch -- engine/store/HALT flag-file convention "
                    "(see docs/kill-switch-spec.md)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_halt = sub.add_parser("halt", help="write the HALT flag-file, stopping new claim/dispatch")
    p_halt.add_argument("reason", nargs="?", default="no reason given")
    p_halt.add_argument("--by", default=os.environ.get("USER", "unknown"))
    p_halt.set_defaults(func=cmd_halt)

    p_resume = sub.add_parser("resume", help="remove the HALT flag-file, resuming claim/dispatch")
    p_resume.set_defaults(func=cmd_resume)

    p_status = sub.add_parser("status", help="print current halt state")
    p_status.add_argument("--json", action="store_true")
    p_status.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
