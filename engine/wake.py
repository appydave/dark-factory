#!/usr/bin/env python3
"""
wake.py — the factory's auto-wake + queue-notification watcher.

C3 spirit (backlog/specs/c3-marshall-auto-wake-spec.md), v1 retargeted to today's
engine: Switchboard's SSE leg is down, so this is a launchd WatchPaths trigger on
engine/store/queue/ instead of an SSE subscribe. See docs/auto-wake.md for the
full wire diagram and the explicit divergence-from-spec note.

Two legs, always separate:

  (a) NOTIFY — always. If the set of dispatchable tickets sitting in queue/ has
      changed since the last run (engine/store/.wake-state.json), fire a macOS
      notification (osascript, copied from orchestrator.py's notify()) and append
      one line to engine/store/wake.log. Debounced: an unchanged set logs "quiet"
      and does not re-notify.

  (b) DISPATCH — only if ARMED. wake.py NEVER calls claude itself (the
      interactive-claude-only law lives in orchestrator.py — this script only ever
      shells out to `python3 orchestrator.py`, detached, as a supervisor would).
      Dispatch fires only when ALL of: engine/store/WAKE-ARMED exists, HALT
      absent, BACKOFF absent, and no other engine run is live (engine/store/.wake.lock
      holds a pid; a dead pid is stale and gets taken over, a live pid means skip).

Ships DISARMED — no WAKE-ARMED file is created by this module. bin/factory-wake
{arm|disarm|status} is the muscle-memory wrapper (mirrors bin/factory-halt), and
also delegates here (`exec python3 engine/wake.py "$@"`).

Invoked with no args (or by launchd's WatchPaths trigger): runs one scan+notify(+
maybe dispatch) pass, then exits. Invoked with arm/disarm/status: manages the
WAKE-ARMED flag-file directly, mirroring engine/halt.py's HALT convention
(docs/kill-switch-spec.md) so the two gates read identically.

stdlib only.
"""
import os
import sys
import json
import subprocess
from datetime import datetime, timezone

ENGINE   = os.path.dirname(os.path.abspath(__file__))
REPO     = os.path.dirname(ENGINE)
STORE    = os.path.join(ENGINE, "store")
Q        = os.path.join(STORE, "queue")

WAKE_ARMED_PATH = os.path.join(STORE, "WAKE-ARMED")
HALT_PATH       = os.path.join(STORE, "HALT")
BACKOFF_PATH    = os.path.join(STORE, "BACKOFF")
LOCK_PATH       = os.path.join(STORE, ".wake.lock")
STATE_PATH      = os.path.join(STORE, ".wake-state.json")
WAKE_LOG_PATH   = os.path.join(STORE, "wake.log")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def notify(title, msg):
    """Copied from orchestrator.py's notify() (not imported — orchestrator.py is
    being actively edited by a sibling ticket this session; this small function
    is stable and cheap to duplicate rather than risk a cross-module import into
    a possibly-changing file)."""
    sys.stdout.write("\a")
    sys.stdout.flush()
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification {json.dumps(msg)} with title {json.dumps(title)} sound name "Glass"'],
            capture_output=True, timeout=5)
    except Exception:
        pass


def log(msg):
    """Appends one line to wake.log. Deliberately does NOT also print() — when
    launchd invokes this script its own StandardOutPath/StandardErrorPath also
    point at wake.log, so printing here would double every line under launchd
    while looking fine when run by hand. Tail wake.log to see output either way."""
    line = f"{now_iso()} {msg}\n"
    try:
        with open(WAKE_LOG_PATH, "a") as f:
            f.write(line)
    except Exception:
        pass


_skip_logged = set()


def dispatchable(fname):
    """DUPLICATED from engine/orchestrator.py's dispatchable() (~line 101) — same
    skip rules, on purpose not imported (orchestrator.py is under active edit by a
    sibling ticket this session; a small filter is cheap to keep in sync by hand,
    an import is not). Skip: (a) external-research tickets (self-contained payload
    for a non-Claude consumer), (b) tickets David explicitly deferred
    (status/priority == deferred), (c) unparseable JSON."""
    try:
        t = json.load(open(os.path.join(Q, fname)))
    except Exception as e:
        reason = f"unparseable JSON ({e})"
        t = None
    else:
        if t.get("kind") == "external-research" or t.get("executor") == "external-research-agent":
            reason = "external-research ticket (not for a Claude worker)"
        elif "deferred" in (str(t.get("status", "")), str(t.get("priority", ""))):
            reason = "deferred by David"
        else:
            return True
    if fname not in _skip_logged:
        _skip_logged.add(fname)
        log(f"[skip] ticket {fname}: {reason}")
    return False


def pending_tickets():
    if not os.path.isdir(Q):
        return []
    return sorted(f for f in os.listdir(Q) if f.endswith(".json") and dispatchable(f))


def ticket_title(fname):
    try:
        t = json.load(open(os.path.join(Q, fname)))
        return t.get("title") or (t.get("prompt", "") or "")[:80] or fname
    except Exception:
        return fname


def load_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"last_seen": []}


def save_state(tickets):
    payload = {"last_seen": sorted(tickets), "updated_at": now_iso()}
    with open(STATE_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def pid_alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, just not owned by us -- still alive
    except Exception:
        return False
    return True


def lock_status():
    """Returns (is_live, pid_or_none). is_live True only if the lock file exists
    AND its pid is still alive. A missing file, unreadable file, or dead pid all
    read as not-live (stale) -- takeover is safe."""
    if not os.path.exists(LOCK_PATH):
        return False, None
    try:
        with open(LOCK_PATH) as f:
            pid = int(f.read().strip())
    except Exception:
        return False, None
    return pid_alive(pid), pid


def write_lock(pid):
    with open(LOCK_PATH, "w") as f:
        f.write(str(pid))


def dispatch_orchestrator():
    """Launches `python3 orchestrator.py --teardown --max-wall 900` fully detached
    (own session, so it survives wake.py exiting). wake.py itself never calls
    claude -- it only ever supervises the one process that does."""
    logf = open(WAKE_LOG_PATH, "a")
    proc = subprocess.Popen(
        ["python3", os.path.join(ENGINE, "orchestrator.py"), "--teardown", "--max-wall", "900"],
        cwd=REPO,
        stdout=logf, stderr=logf,
        start_new_session=True,
    )
    write_lock(proc.pid)
    return proc.pid


def run_pass():
    tickets = pending_tickets()
    state = load_state()
    last_seen = set(state.get("last_seen", []))
    current = set(tickets)
    new_tickets = sorted(current - last_seen)

    if not new_tickets:
        log(f"quiet: no new dispatchable tickets (n={len(current)} pending, unchanged)")
        save_state(tickets)
        return

    n = len(new_tickets)
    first_title = ticket_title(new_tickets[0])
    msg = f"{n} ticket(s) queued: {first_title[:80]}"
    notify("dark-factory", msg)

    armed = os.path.exists(WAKE_ARMED_PATH)
    halted = os.path.exists(HALT_PATH)
    backoff = os.path.exists(BACKOFF_PATH)

    if armed and not halted and not backoff:
        live, existing_pid = lock_status()
        if live:
            action = f"skip-dispatch (live lock pid={existing_pid})"
        else:
            note = f" (stale lock pid={existing_pid} taken over)" if existing_pid else ""
            pid = dispatch_orchestrator()
            action = f"dispatched (pid={pid}){note}"
    else:
        reasons = []
        if not armed:
            reasons.append("disarmed")
        if halted:
            reasons.append("HALT present")
        if backoff:
            reasons.append("BACKOFF present")
        action = "skip-dispatch (" + ", ".join(reasons) + ")"

    log(f"wake: {n} new ticket(s) [{', '.join(new_tickets)}] armed={armed} action={action}")
    save_state(tickets)


def cmd_arm():
    os.makedirs(STORE, exist_ok=True)
    payload = {"ts": now_iso(), "by": os.environ.get("USER", "unknown")}
    with open(WAKE_ARMED_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(f"ARMED -> {WAKE_ARMED_PATH}")
    print(json.dumps(payload, indent=2))


def cmd_disarm():
    existed = os.path.exists(WAKE_ARMED_PATH)
    if existed:
        os.remove(WAKE_ARMED_PATH)
        print(f"DISARMED -> removed {WAKE_ARMED_PATH}")
    else:
        print("Already disarmed -- no WAKE-ARMED file present.")


def cmd_status():
    armed = os.path.exists(WAKE_ARMED_PATH)
    info = None
    if armed:
        try:
            with open(WAKE_ARMED_PATH) as f:
                info = json.load(f)
        except Exception:
            info = {}

    loaded = False
    try:
        out = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=5)
        loaded = "com.appydave.dark-factory-wake" in out.stdout
    except Exception:
        pass

    print("ARMED" if armed else "DISARMED")
    if info:
        print(f"  since: {info.get('ts', '?')}  by: {info.get('by', '?')}")
    print(f"  launchd loaded: {'yes' if loaded else 'no'}")
    print(f"  flag: {WAKE_ARMED_PATH}")
    print("  last wake.log lines:")
    lines = []
    if os.path.exists(WAKE_LOG_PATH):
        with open(WAKE_LOG_PATH) as f:
            lines = f.readlines()
    if not lines:
        print("   (no wake.log entries yet)")
    for line in lines[-3:]:
        print("   " + line.rstrip())


def main():
    os.makedirs(STORE, exist_ok=True)
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == "arm":
        cmd_arm()
    elif cmd == "disarm":
        cmd_disarm()
    elif cmd == "status":
        cmd_status()
    else:
        run_pass()


if __name__ == "__main__":
    main()
