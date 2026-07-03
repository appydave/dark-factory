#!/usr/bin/env python3
"""
orchestrator.py — dark-factory's production engine kernel.

Adapted from suborch-demo's orchestrator.py (~/dev/ad/apps/suborch-demo/orchestrator.py),
per docs/harness-evaluation.md's promotion plan. This is NOT a from-scratch rewrite —
most of the mechanics below are suborch's, ported into dark-factory's real (not toy)
queue-file idiom:

  KEPT FROM DARK-FACTORY (per the evaluation's verdict table):
    - rename(2) claim/lease as the CAS mutex (queue/ -> running/) — same primitive
      dark-factory's claim-next.sh already proved (200x8 stress test). EXTENDED here
      with ownership recording (claimed_by/claimed_at written into the ticket the
      instant the rename wins) — closing the one gap both dark-factory and suborch
      shared (row 2 of the evaluation table).
    - artifact-is-truth reaping (never trust a worker's chat reply) — dark-factory's
      own principle (reaper.sh), reinforced by suborch's fix below.
    - flat-file store under a trusted repo path (never /tmp) — dark-factory convention,
      confirmed in docs/comms-flow.md §4.

  PROMOTED FROM SUBORCH (per the evaluation's per-mechanism verdict):
    - WarmPool dispatch (warm_pool.py) replacing dark-factory's cold
      `tmux new-window` spawn-per-ticket (dispatch-swagger.sh) — the single biggest
      value item named in the evaluation.
    - The "commit on artifact-landed, not on a state==done flag" starvation fix
      suborch found the hard way (546s/9-of-10 -> 52s/10-of-10). Implemented here as:
      reap gates purely on `artifact_ok()` + ticket-specific `verify()`, never on the
      worker's own claimed status.
    - The mid-task HITL gate (needs-decision/<tid>.json -> decisions/<tid>.json ->
      send-keys resume) — ported natively, present but NOT exercised on the real
      proof ticket (per the day's build instructions; use --hitl for a --test demo).

  NOT suborch's shape (deliberate divergence, because this is a REAL engine, not a demo):
    - No reset()/wipe-the-store-every-run. The store is a growing ledger (done/,
      audit.jsonl, events/ all accumulate) — dark-factory's actual convention
      (comms-flow.md §4), not suborch's disposable 10-toy-task harness.
    - No hardcoded TASKS dict. Tickets are real files dropped into store/queue/ by
      anything (a human, omi-fetch's consumer, a future Switchboard SSE wake) — the
      queue directory is scanned fresh each pass, not a fixed list.
    - Workers' cwd is the dark-factory REPO ROOT (not the engine store), so a
      ticket's prompt can reference ordinary repo-relative paths
      (e.g. "mochaccino/data/constellation.json") the way a human would.

Invariant unchanged: interactive `claude` only. No -p, no Agent SDK, no API key —
subscription-safe (docs/runtime-model.md).
"""
import os, sys, time, json, socket, subprocess, re, uuid
from datetime import datetime, timezone
from warm_pool import WarmPool, safety_check, find_session

ENGINE   = os.path.dirname(os.path.abspath(__file__))
REPO     = os.path.dirname(ENGINE)                 # dark-factory repo root — worker cwd
STORE    = os.path.join(ENGINE, "store")
Q, RUN, DONE, RES = (os.path.join(STORE, d) for d in ("queue", "running", "done", "results"))
EVENTS   = os.path.join(STORE, "events")
NEEDS, DEC = (os.path.join(STORE, d) for d in ("needs-decision", "decisions"))
AUDIT    = os.path.join(STORE, "audit.jsonl")

MODEL          = "sonnet"   # real work, not toy trivia -> not haiku
POOL           = 1          # default; dark-factory's real jobs are few and expensive
WORKER_TIMEOUT = 240        # seconds: a real edit+commit turn budget (generous vs suborch's 45s trivia)
COOL_CAP       = 30
MAX_WALL       = 900        # seconds: hard guard for a --serve-less (drain) run
POLL           = 3
MAX_RETRY      = 2
HITL_TIMEOUT   = 1800

CLAIMANT = f"{socket.gethostname()}-pid{os.getpid()}"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def banner(msg):
    print(f"\n=== {msg} ===", flush=True)


def notify(title, msg):
    """Ported verbatim from suborch: terminal bell + macOS notification so a blocked
    HITL ticket (or, here, also completion) isn't invisible."""
    sys.stdout.write("\a"); sys.stdout.flush()
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification {json.dumps(msg)} with title {json.dumps(title)} sound name "Glass"'],
            capture_output=True, timeout=5)
    except Exception:
        pass


def ensure_dirs():
    for d in (Q, RUN, DONE, RES, EVENTS, NEEDS, DEC):
        os.makedirs(d, exist_ok=True)


def pending_tickets():
    """Real queue scan (not a fixed list) — oldest-first by filename, matching
    claim-next.sh's convention (timestamp-prefixed names sort in time order)."""
    return sorted(f for f in os.listdir(Q) if f.endswith(".json"))


def lease(fname):
    """rename(2) CAS claim, THEN record ownership into the ticket (DF-gap closed):
    who claimed it and when. The rename is still the sole mutex — the ownership
    write happens only after we already exclusively own the file."""
    src, dst = os.path.join(Q, fname), os.path.join(RUN, fname)
    try:
        os.rename(src, dst)
    except FileNotFoundError:
        return False
    try:
        with open(dst) as f:
            ticket = json.load(f)
        ticket["claimed_by"] = CLAIMANT
        ticket["claimed_at"] = now_iso()
        with open(dst, "w") as f:
            json.dump(ticket, f, indent=2)
            f.write("\n")
    except Exception as e:
        print(f"[warn] {fname}: claimed but could not record ownership ({e})", flush=True)
    return True


def load_ticket(tid):
    with open(os.path.join(RUN, tid)) as f:
        return json.load(f)


def task_prompt(tid, gated=False):
    """SPK-D1 (suborch): hand the worker a POINTER, not the payload. Kept single-line
    for tmux send-keys -l safety; the ticket's full multi-line instructions live in
    the JSON file the worker reads with its own Read tool."""
    ticket_path = os.path.join(RUN, tid)
    res_path = os.path.join(RES, tid)
    if gated:
        nd = os.path.join(NEEDS, tid)
        return (f"Your ticket id is {tid}. Read the full instructions from the JSON file at {ticket_path} "
                f"(its \"prompt\" field). This ticket requires a human decision before finalizing. Work out your "
                f"proposed approach, then use the Write tool to create {nd} containing EXACTLY this JSON (valid "
                f'JSON, no prose): {{"ticket":"{tid}","question":"Approve this approach?","proposed":"<your plan in one line>",'
                f'"note":"<why / alternative>"}} . Then STOP — do not make any edits yet, do not write {res_path}. '
                f"Reply with exactly the single token AWAITING_DECISION and wait for my next message.")
    return (f"Your ticket id is {tid}. Read the full instructions from the JSON file at {ticket_path} (its "
            f"\"prompt\" field) and execute them exactly, in this repo. When completely finished, use the Write "
            f'tool to save a JSON status report to {res_path} in EXACTLY this form (valid JSON, no prose): '
            f'{{"ticket":"{tid}","status":"done","files_changed":["<paths>"],"commit_sha":"<sha or null>",'
            f'"notes":"<one short line>"}} . Then reply with exactly: ACK {tid}')


def resume_prompt(tid, decision):
    res_path = os.path.join(RES, tid)
    act = (decision.get("action") or "approve").lower()
    if act == "decline":
        return (f"Decision: DECLINED for ticket {tid}. Do not make any edits and do not write any file. "
                f"Reply with exactly the single token ABORTED.")
    note = f" Human note: {decision['note']}." if decision.get("note") else ""
    choice = f" Use this specific direction: {decision['choice']}." if decision.get("choice") else ""
    return (f"Decision: {act.upper()} for ticket {tid}.{choice}{note} Proceed with the full ticket instructions "
            f'now, then use the Write tool to save a JSON status report to {res_path} in EXACTLY this form: '
            f'{{"ticket":"{tid}","status":"done","files_changed":["<paths>"],"commit_sha":"<sha or null>",'
            f'"notes":"<one short line>"}} . Then reply with exactly: ACK {tid}')


def artifact_ok(tid):
    res = os.path.join(RES, tid)
    return os.path.exists(res) and os.path.getsize(res) > 0


# --- ticket-specific verification (artifact-is-truth: the orchestrator checks the
#     REAL deliverable itself, never just the worker's self-report) --------------

def verify_constellation_4_apps(_ticket):
    checks = []
    cpath = os.path.join(REPO, "mochaccino/data/constellation.json")
    hpath = os.path.join(REPO, "mochaccino/designs/10-constellation/index.html")
    new_ids = {"omi-fetch", "app-registry", "project-digest", "kdd-viewer"}

    try:
        data = json.load(open(cpath))
    except Exception as e:
        return False, [f"constellation.json failed to parse: {e}"]

    ids_present = {a.get("id") for a in data.get("apps", [])}
    missing = new_ids - ids_present
    if missing:
        checks.append(f"missing app ids in constellation.json apps[]: {sorted(missing)}")

    flow_ids = set()
    for fl in data.get("flows", []):
        flow_ids.add(fl.get("from")); flow_ids.add(fl.get("to"))
    flow_missing = new_ids - flow_ids
    if flow_missing:
        checks.append(f"no flows[] entry references these new ids: {sorted(flow_missing)}")

    try:
        html = open(hpath, encoding="utf-8").read()
    except Exception as e:
        return False, checks + [f"index.html unreadable: {e}"]

    m = re.search(r'<script type="application/json" id="constellation-data">(.*?)</script>', html, re.S)
    if not m:
        checks.append("could not find <script id=\"constellation-data\"> block in index.html")
    else:
        try:
            embedded = json.loads(m.group(1))
            embedded_ids = {a.get("id") for a in embedded.get("apps", [])}
            missing_embedded = new_ids - embedded_ids
            if missing_embedded:
                checks.append(f"embedded HTML JSON missing ids: {sorted(missing_embedded)}")
        except Exception as e:
            checks.append(f"embedded HTML JSON failed to parse: {e}")

    return (len(checks) == 0), checks


VERIFIERS = {
    "constellation-4-apps": verify_constellation_4_apps,
}


def verify(ticket):
    """Returns (ok: bool, findings: list[str]). No verify_kind -> pass (generic
    tickets rely on artifact_ok() alone, same as suborch's results/<tid>.txt check)."""
    vk = ticket.get("verify_kind")
    if not vk:
        return True, []
    fn = VERIFIERS.get(vk)
    if not fn:
        return False, [f"unknown verify_kind: {vk}"]
    return fn(ticket)


def commit(tid):
    os.rename(os.path.join(RUN, tid), os.path.join(DONE, tid))


def emit_event(kind, payload):
    fname = f"{now_iso().replace(':', '').replace('-', '')}-{kind}-{uuid.uuid4().hex[:8]}.json"
    path = os.path.join(EVENTS, fname)
    body = dict(event=kind, ts=now_iso(), **payload)
    with open(path, "w") as f:
        json.dump(body, f, indent=2)
        f.write("\n")
    return path


def audit(entry):
    with open(AUDIT, "a") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    safety_check()
    ensure_dirs()

    argv = sys.argv
    model = argv[argv.index("--model") + 1] if "--model" in argv else MODEL
    pool_size = int(argv[argv.index("--pool") + 1]) if "--pool" in argv else POOL
    max_wall = int(argv[argv.index("--max-wall") + 1]) if "--max-wall" in argv else MAX_WALL
    teardown = "--teardown" in argv
    gated_tid = argv[argv.index("--hitl") + 1] if "--hitl" in argv else None

    banner(f"dark-factory engine kernel — pool={pool_size} model={model} "
           f"repo={REPO} subscription-only" + (f" (--hitl {gated_tid})" if gated_tid else ""))

    pool = WarmPool(pool_size, model, REPO)
    boots = pool.boot_all()
    print(f"[pool] {pool_size} warm worker(s) booted in {sum(boots):.0f}s total "
          f"({', '.join(f'{b:.0f}s' for b in boots)}) — named df-worker-1.."
          f"{pool_size} (tmux ls / tmux attach -t df-worker-1)", flush=True)

    active = {}     # tid -> dict(worker, started, gated, state, blocked_since, ticket)
    cooling = []
    results = {}
    retries = {}
    peak = 0
    t0 = time.time()

    def settle(tid, a):
        del active[tid]
        cooling.append(dict(worker=a["worker"], since=time.time()))

    while True:
        for c in list(cooling):
            w = c["worker"]
            if w.idle():
                w.busy = None; cooling.remove(c)
            elif time.time() - c["since"] > COOL_CAP:
                w.reboot(); w.busy = None; cooling.remove(c)
                print(f"[reboot]   {w.name}: would not idle -> fresh process", flush=True)

        pending = [f for f in pending_tickets() if f not in active]
        while pending:
            w = pool.free_worker()
            if not w:
                break
            fname = pending.pop(0)
            if not lease(fname):
                continue
            ticket = load_ticket(fname)
            tid = fname
            gated = (tid == gated_tid)
            w.busy = tid
            w.send(task_prompt(tid, gated))
            active[tid] = dict(worker=w, started=time.time(), gated=gated,
                                state="running", blocked_since=None, ticket=ticket)
            peak = max(peak, len(active))
            if not w.session_id:
                w.session_id, w.transcript = find_session(REPO, f"ticket id is {tid}.")
            audit(dict(ticket=tid, attempt=retries.get(tid, 0) + 1, worker=w.name,
                       session_id=w.session_id, transcript=w.transcript,
                       claimed_by=ticket.get("claimed_by"), claimed_at=ticket.get("claimed_at")))
            print(f"[dispatch] ticket {tid} -> {w.name}  (session {(w.session_id or '?')[:8]})", flush=True)

        for tid, a in list(active.items()):
            if a["gated"] and not artifact_ok(tid):
                nd = os.path.join(NEEDS, tid)
                dfile = os.path.join(DEC, tid)
                if a["state"] == "running" and os.path.exists(nd) and os.path.getsize(nd) > 0:
                    a["state"] = "blocked"; a["blocked_since"] = time.time()
                    try:
                        req = json.load(open(nd))
                    except Exception:
                        req = {}
                    print(f"[HITL] locked ticket {tid} — {req.get('question', 'awaiting decision')} "
                          f"proposed={req.get('proposed', '?')!r}", flush=True)
                    print(f"[HITL]    decide:  echo '{{\"action\":\"approve\"}}' > {dfile}", flush=True)
                    notify(f"engine: ticket {tid} needs you", req.get("question", "A worker is waiting."))
                    continue
                if a["state"] == "blocked":
                    if os.path.exists(dfile) and os.path.getsize(dfile) > 0:
                        try:
                            decision = json.load(open(dfile))
                        except Exception:
                            decision = {"action": "approve"}
                        act = (decision.get("action") or "approve").lower()
                        a["worker"].send(resume_prompt(tid, decision))
                        a["state"] = "resumed"; a["started"] = time.time()
                        print(f"[HITL] resumed ticket {tid} decision={act.upper()}", flush=True)
                        if act == "decline":
                            results[tid] = "declined"; settle(tid, a)
                        continue
                    if time.time() - a["blocked_since"] > HITL_TIMEOUT:
                        w = a["worker"]; del active[tid]; w.reboot(); w.busy = None
                        results[tid] = "failed(no-decision)"
                        print(f"[HITL] ticket {tid}: no decision in {HITL_TIMEOUT}s -> surfaced unanswered", flush=True)
                        continue
                    continue

            if artifact_ok(tid):
                ok, findings = verify(a["ticket"])
                if ok:
                    commit(tid); results[tid] = "done"; settle(tid, a)
                    ev = emit_event("job.completed", dict(ticket=tid, result="done"))
                    print(f"[reap]     ticket {tid}: done, verified -> event {os.path.basename(ev)}", flush=True)
                else:
                    print(f"[verify]   ticket {tid}: artifact present but verification FAILED: {findings}", flush=True)
                    if time.time() - a["started"] > WORKER_TIMEOUT:
                        results[tid] = "failed(verify)"; a["verify_findings"] = findings; settle(tid, a)
                        print(f"[reap]     ticket {tid}: giving up after verify timeout", flush=True)
            elif time.time() - a["started"] > WORKER_TIMEOUT:
                w = a["worker"]; del active[tid]
                w.reboot(); w.busy = None
                print(f"[reboot]   {w.name}: wedged on ticket {tid} -> fresh process", flush=True)
                if retries.get(tid, 0) < MAX_RETRY:
                    retries[tid] = retries.get(tid, 0) + 1
                    os.rename(os.path.join(RUN, tid), os.path.join(Q, tid))
                    print(f"[reap]     ticket {tid}: no response -> re-queue (retry {retries[tid]})", flush=True)
                else:
                    results[tid] = "failed(timeout)"
                    print(f"[reap]     ticket {tid}: failed (worker timeout, retries exhausted)", flush=True)

        still_pending = bool(pending_tickets())
        if not active and not still_pending:
            break
        if time.time() - t0 > max_wall and not any(a["gated"] for a in active.values()):
            print(f"[wall]     max-wall {max_wall}s reached with work outstanding", flush=True)
            break
        time.sleep(POLL)

    elapsed = time.time() - t0
    banner("REPORT")
    for tid, status in results.items():
        print(f"  {tid}: {status}")
    print(f"\n  {elapsed:.0f}s wall | peak concurrency {peak}/{pool_size}")
    def _jsons(d):
        return len([f for f in os.listdir(d) if f.endswith(".json")])
    print(f"  store: queue={len(pending_tickets())} running={_jsons(RUN)} done={_jsons(DONE)}")

    if teardown:
        pool.teardown_all()
        print("  pool torn down (--teardown given)", flush=True)
    else:
        print("  pool LEFT ALIVE — tmux ls / tmux attach -t df-worker-1", flush=True)

    sys.exit(0 if all(v == "done" for v in results.values()) else (0 if not results else 1))


if __name__ == "__main__":
    main()
