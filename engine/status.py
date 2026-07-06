#!/usr/bin/env python3
"""
status.py — read-only aggregation over engine/store/. Answers, without hand-`ls`ing
and hand-`cat`ing JSON, the questions docs/six-app-evaluation-2026-07-04.md #5 named
as missing: what's queued right now / how old is the oldest ticket / did ticket X
succeed / who (which tmux worker) is running right now / what did the last few
dispatches actually do.

No new state. Every number here is derived fresh from store/queue/, store/running/,
store/done/, store/results/, and store/audit.jsonl on each run — same ledger
orchestrator.py already writes, just aggregated instead of read by hand.

Two output modes:
  python3 status.py            human-readable report
  python3 status.py --json     the same data as machine-readable JSON (for agents)

The ticket schema has drifted across the store's lifetime (queue_id/kind/verify_kind
vs ticket/title/source/priority vs ad-hoc done-in-place fields) — every field lookup
below degrades gracefully across all the shapes actually observed in the real store,
rather than assuming one canonical shape.
"""
import os, sys, json, re, argparse, subprocess
from datetime import datetime, timezone

from orchestrator import Q, RUN, DONE, RES, AUDIT, REPO  # single source of truth for paths
from orchestrator import is_backoff, backoff_info, BACKOFF_PATH  # CAP/429-wall governor (cap-governor ticket)
from halt import halt_info, HALT_PATH

TS_RE = re.compile(r'^(\d{8})T(\d{4,6})Z-')


def _list_json(d):
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.endswith(".json"))


def _load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def parse_fname_ts(fname):
    """Every ticket filename in this store is timestamp-prefixed, but the precision
    varies: some carry seconds (20260703T125625Z-...), some don't
    (20260704T0629Z-...). Handle both."""
    m = TS_RE.match(fname)
    if not m:
        return None
    date_s, time_s = m.groups()
    fmt = "%Y%m%d%H%M%S" if len(time_s) == 6 else "%Y%m%d%H%M"
    try:
        return datetime.strptime(date_s + time_s, fmt).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def parse_iso(s):
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def ticket_title(data, fallback):
    return (data.get("title") or data.get("question") or data.get("ticket")
            or data.get("queue_id") or (data.get("prompt", "")[:70] + "…" if data.get("prompt") else None)
            or fallback)


def ticket_created_at(data, fname):
    """Prefer the ticket's own requested_at (authoritative intent); fall back to the
    timestamp encoded in its filename (always present, by convention)."""
    return parse_iso(data.get("requested_at")) or parse_fname_ts(fname)


def human_age(seconds):
    if seconds is None:
        return "?"
    if seconds < 60:
        return f"{int(seconds)}s"
    if seconds < 3600:
        return f"{seconds / 60:.1f}m"
    if seconds < 86400:
        return f"{seconds / 3600:.1f}h"
    return f"{seconds / 86400:.1f}d"


def tmux_workers():
    """Current df-worker-* tmux sessions, or None if tmux itself isn't on PATH."""
    try:
        r = subprocess.run(["tmux", "list-sessions"], capture_output=True, text=True, timeout=5)
    except FileNotFoundError:
        return None
    if r.returncode != 0:
        return []  # tmux present, no server running -> no sessions
    return [line.strip() for line in r.stdout.splitlines()
            if line.split(":", 1)[0].strip().startswith("df-worker-")]


def done_outcome(fname):
    """A done ticket's outcome lives in one of two places in the real store
    (schema drift, not a bug): the results/<fname>.json worker self-report (the
    normal path), or fields written directly into the ticket JSON itself
    (result/verified — observed on at least one hand-closed ticket). Self-report
    wins when both exist."""
    ticket = _load(os.path.join(DONE, fname))
    title = ticket_title(ticket, fname)
    result, notes = None, None
    res = _load(os.path.join(RES, fname))
    if res:
        result = res.get("status")
        notes = res.get("notes")
    if result is None:
        result = ticket.get("result")
        notes = notes or ticket.get("verified") or ticket.get("note")
        if isinstance(result, dict):  # dict-shaped ticket-embedded result (e.g. halt-switch ticket) -> unwrap
            notes = notes or result.get("notes")
            result = result.get("status")
    return title, result or "unknown", notes


def audit_tail(n):
    if not os.path.exists(AUDIT):
        return []
    out = []
    with open(AUDIT) as f:
        lines = f.read().splitlines()
    for line in lines[-n:]:
        try:
            out.append(json.loads(line))
        except Exception:
            pass
    return out


def build_report(n_done=5, n_audit=5):
    now = datetime.now(timezone.utc)

    queue_files = _list_json(Q)
    queue_items, oldest = [], None
    for f in queue_files:
        data = _load(os.path.join(Q, f))
        ts = ticket_created_at(data, f)
        age = (now - ts).total_seconds() if ts else None
        queue_items.append(dict(file=f, title=ticket_title(data, f), age_s=age))
        if ts and (oldest is None or ts < oldest[0]):
            oldest = (ts, f)

    running_files = _list_json(RUN)
    running_items = []
    for f in running_files:
        data = _load(os.path.join(RUN, f))
        running_items.append(dict(
            file=f, title=ticket_title(data, f),
            claimed_by=data.get("claimed_by"), claimed_at=data.get("claimed_at"),
        ))

    done_files = _list_json(DONE)
    done_recent = []
    for f in done_files[-n_done:]:
        title, result, notes = done_outcome(f)
        done_recent.append(dict(file=f, title=title, result=result, notes=notes))

    # is_backoff() has the auto-clear side effect (removes an expired flag before we
    # report on it) — call it first, then read backoff_info() only if still active.
    backoff_active = is_backoff()
    backoff = backoff_info() if backoff_active else None

    return dict(
        generated_at=now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        halt=halt_info(),  # None if running; {ts, by, reason} if HALT flag-file present
        backoff=backoff,   # None if running; {ts, until, reason, worker} if BACKOFF flag-file present+unexpired
        queue=dict(
            depth=len(queue_files),
            oldest_ticket=oldest[1] if oldest else None,
            oldest_age_s=(now - oldest[0]).total_seconds() if oldest else None,
            items=queue_items,
        ),
        running=dict(count=len(running_files), items=running_items),
        done=dict(total=len(done_files), recent=done_recent),
        workers=tmux_workers(),
        audit_tail=audit_tail(n_audit),
    )


def print_halt_banner(h):
    """Big, impossible-to-miss banner — the kill switch (docs/kill-switch-spec.md)
    is only worth building if its state is visible, not just queryable."""
    print()
    print("#" * 60)
    print("##" + "  FACTORY HALTED".center(56) + "##")
    print("#" * 60)
    print(f"  since:  {h.get('ts', '?')}")
    print(f"  by:     {h.get('by', '?')}")
    print(f"  reason: {h.get('reason', '?')}")
    print(f"  flag:   {HALT_PATH}")
    print("#" * 60)


def print_backoff_banner(b):
    """Mirrors print_halt_banner — the BACKOFF governor (cap-governor ticket) is only
    worth building if its state is as visible as HALT's."""
    print()
    print("#" * 60)
    print("##" + "  FACTORY IN BACKOFF (429 wall)".center(56) + "##")
    print("#" * 60)
    print(f"  since:  {b.get('ts', '?')}")
    print(f"  until:  {b.get('until', '?')}")
    print(f"  reason: {b.get('reason', '?')}")
    print(f"  worker: {b.get('worker', '?')}")
    print(f"  flag:   {BACKOFF_PATH}")
    print("#" * 60)


def print_human(r):
    def banner(s):
        print(f"\n=== {s} ===")

    if r.get("halt"):
        print_halt_banner(r["halt"])
    if r.get("backoff"):
        print_backoff_banner(r["backoff"])

    print(f"dark-factory engine status — {r['generated_at']}")

    banner("QUEUE")
    q = r["queue"]
    print(f"  depth: {q['depth']}")
    if q["oldest_ticket"]:
        print(f"  oldest: {q['oldest_ticket']}  (age {human_age(q['oldest_age_s'])})")
    for item in q["items"]:
        print(f"    - [{human_age(item['age_s']):>7}]  {item['file']}  — {item['title']}")

    banner(f"RUNNING ({r['running']['count']})")
    for item in r["running"]["items"]:
        print(f"    - {item['file']}")
        print(f"        claimed_by={item['claimed_by']}  claimed_at={item['claimed_at']}")
        print(f"        {item['title']}")

    banner(f"DONE — last {len(r['done']['recent'])} of {r['done']['total']}")
    for item in r["done"]["recent"]:
        print(f"    - [{item['result']:>8}]  {item['file']}  — {item['title']}")
        if item["notes"]:
            print(f"        {item['notes']}")

    banner("WORKERS (tmux)")
    w = r["workers"]
    if w is None:
        print("  tmux not found on PATH")
    elif not w:
        print("  no df-worker-* tmux sessions running")
    else:
        for line in w:
            print(f"  {line}")

    banner(f"AUDIT — last {len(r['audit_tail'])} dispatch(es)")
    for e in r["audit_tail"]:
        sid = (e.get("session_id") or "?")[:8]
        print(f"    {e.get('ticket')}  worker={e.get('worker')}  session={sid}  "
              f"claimed_by={e.get('claimed_by')}  claimed_at={e.get('claimed_at')}")


def main():
    ap = argparse.ArgumentParser(description="dark-factory engine status — read-only ledger aggregation")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON instead of the human report")
    ap.add_argument("--n-done", type=int, default=5, help="how many recent done/ tickets to show (default 5)")
    ap.add_argument("--n-audit", type=int, default=5, help="how many recent audit.jsonl lines to show (default 5)")
    args = ap.parse_args()

    report = build_report(args.n_done, args.n_audit)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
