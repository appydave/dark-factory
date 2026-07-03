#!/usr/bin/env python3
"""
consumer.py — the missing brick named in docs/comms-flow.md §5: "events have no
consumer." omi-fetch (and now this engine) write events to store/events/*.json and
nothing ever reads them. This is that reader.

Polls TWO event sources:
  - engine/store/events/                         (this engine's own job.completed etc.)
  - ~/dev/ad/apps/omi-fetch/store/events/         (the first real external event producer)

For each event file not already recorded in engine/store/events-consumed.jsonl, this
appends a consumption record (source, path, ts_consumed) and — on macOS — plays
`afplay /System/Library/Sounds/Glass.aiff` once per batch, so a human doesn't have to
poll a terminal to know something landed. This is the first "charm": proof that an
event can travel from write to a human-audible signal without anyone tailing a log.

Usage:
  python3 consumer.py            # loop forever, poll every 5s (Ctrl-C to stop)
  python3 consumer.py --once     # single pass, exit (good for scripted verification)
  python3 consumer.py --interval 10
"""
import os, sys, json, time, glob, subprocess
from datetime import datetime, timezone

ENGINE = os.path.dirname(os.path.abspath(__file__))
ENGINE_EVENTS = os.path.join(ENGINE, "store", "events")
CONSUMED_LOG = os.path.join(ENGINE, "store", "events-consumed.jsonl")
OMI_FETCH_EVENTS = os.path.expanduser("~/dev/ad/apps/omi-fetch/store/events")

SOURCES = [
    ("engine", ENGINE_EVENTS),
    ("omi-fetch", OMI_FETCH_EVENTS),
]


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_seen():
    """Rebuild the seen-set from the durable consumed-log, so restarting the
    consumer never re-plays/re-records events already consumed in a prior run."""
    seen = set()
    if os.path.exists(CONSUMED_LOG):
        with open(CONSUMED_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    seen.add((rec.get("source"), rec.get("path")))
                except Exception:
                    pass
    return seen


def chime():
    """Best-effort macOS sound cue; silently no-ops elsewhere."""
    try:
        subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"],
                        capture_output=True, timeout=5)
    except Exception:
        pass


def poll_once(seen):
    consumed_this_pass = []
    for source, path in SOURCES:
        if not os.path.isdir(path):
            continue
        for f in sorted(glob.glob(os.path.join(path, "*.json"))):
            key = (source, f)
            if key in seen:
                continue
            try:
                event = json.load(open(f))
            except Exception as e:
                event = {"parse_error": str(e)}
            record = dict(source=source, path=f, ts_consumed=now_iso(), event=event)
            with open(CONSUMED_LOG, "a") as out:
                out.write(json.dumps(record) + "\n")
            seen.add(key)
            consumed_this_pass.append(record)
            print(f"[consumed] {source}: {os.path.basename(f)}", flush=True)
    if consumed_this_pass:
        chime()
    return consumed_this_pass


def main():
    once = "--once" in sys.argv
    interval = 5
    if "--interval" in sys.argv:
        interval = int(sys.argv[sys.argv.index("--interval") + 1])

    os.makedirs(ENGINE_EVENTS, exist_ok=True)
    seen = load_seen()
    print(f"[consumer] watching: {ENGINE_EVENTS}", flush=True)
    print(f"[consumer] watching: {OMI_FETCH_EVENTS}"
          + ("" if os.path.isdir(OMI_FETCH_EVENTS) else "  (not present on this machine)"), flush=True)

    if once:
        n = len(poll_once(seen))
        print(f"[consumer] single pass done: {n} event(s) consumed", flush=True)
        return

    print(f"[consumer] looping every {interval}s (Ctrl-C to stop)", flush=True)
    try:
        while True:
            poll_once(seen)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[consumer] stopped", flush=True)


if __name__ == "__main__":
    main()
