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
from datetime import datetime, timezone, timedelta
from warm_pool import WarmPool, safety_check, find_session
from halt import is_halted, halt_info

ENGINE   = os.path.dirname(os.path.abspath(__file__))
REPO     = os.path.dirname(ENGINE)                 # dark-factory repo root — worker cwd
STORE    = os.path.join(ENGINE, "store")
Q, RUN, DONE, RES = (os.path.join(STORE, d) for d in ("queue", "running", "done", "results"))
EVENTS   = os.path.join(STORE, "events")
NEEDS, DEC = (os.path.join(STORE, d) for d in ("needs-decision", "decisions"))
AUDIT    = os.path.join(STORE, "audit.jsonl")
# LEDGER (wg-t1-16) is the outcome/result ledger, sibling to AUDIT's dispatch/input
# ledger: audit.jsonl records "who got dispatched, when" (one line per lease);
# ledger.jsonl records "what happened to it" (one line per reap decision — a
# terminal verdict OR a requeue-with-a-next-action), chained via a 'prior' pointer
# to the ticket's previous ledger line so a crashed session's whole story is on
# disk. Never rewritten — corrections are new lines, same append-only idiom as
# audit.jsonl (engine/store/queue/.CONVENTION.md).
LEDGER   = os.path.join(STORE, "ledger.jsonl")
BACKOFF_PATH = os.path.join(STORE, "BACKOFF")   # 429/usage-limit governor flag-file (mirrors halt.py's HALT)

MODEL          = "sonnet"   # real work, not toy trivia -> not haiku
POOL           = 1          # default; dark-factory's real jobs are few and expensive
CAP            = 3          # HARD CAP: per suborch's proven "well under the ~5-7 per-account 429 wall" —
                             # --pool is clamped to this at startup, loudly, regardless of what's requested
WORKER_TIMEOUT = 240        # seconds: a real edit+commit turn budget (generous vs suborch's 45s trivia)
COOL_CAP       = 30
MAX_WALL       = 900        # seconds: hard guard for a --serve-less (drain) run
POLL           = 3
MAX_RETRY      = 2
HITL_TIMEOUT   = 1800
BACKOFF_COOLDOWN = 900      # seconds (15 min): default cooldown once a usage-limit signature is detected

USAGE_LIMIT_SIGNATURES = ("usage limit", "rate limit", "429", "out of extended usage")

CLAIMANT = f"{socket.gethostname()}-pid{os.getpid()}"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s):
    """Defensive ISO-8601 'Z' parse — never raises; unparseable/missing -> None."""
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def looks_like_usage_limit(pane_text):
    """Pure detector: case-insensitive substring match of a captured tmux pane
    against known 429/usage-limit signatures. Never raises — empty/None input
    just reads as False, same defensive contract as halt.py's is_halted()."""
    if not pane_text:
        return False
    lowered = pane_text.lower()
    return any(sig in lowered for sig in USAGE_LIMIT_SIGNATURES)


# --- BACKOFF flag-file — mirrors halt.py's HALT idiom exactly (docs/kill-switch-spec.md),
#     the one difference being BACKOFF has a built-in expiry: is_backoff() auto-removes
#     the flag once "until" has passed and logs the resume, rather than waiting for a
#     human to explicitly clear it. -----------------------------------------------------

def backoff_info():
    """Returns the BACKOFF file's {ts, until, reason, worker} payload regardless of
    expiry, or None if the flag-file doesn't exist. A corrupt-but-present file still
    reads as "in backoff" (with '?' fields) — existence is the ground truth, same as
    halt_info()."""
    try:
        if not os.path.exists(BACKOFF_PATH):
            return None
    except Exception:
        return None
    try:
        with open(BACKOFF_PATH) as f:
            return json.load(f)
    except Exception:
        return {"ts": None, "until": None, "reason": None, "worker": None}


def is_backoff():
    """True iff the BACKOFF flag exists AND is unexpired. Unlike HALT (no expiry,
    only a human clears it), BACKOFF self-clears: once 'until' has passed, this
    removes the flag, logs the resume, and returns False. Never raises."""
    info = backoff_info()
    if info is None:
        return False
    until = _parse_iso(info.get("until"))
    if until is not None and datetime.now(timezone.utc) >= until:
        clear_backoff()
        print(f"[backoff]  cooldown expired (was until {info.get('until')}) "
              f"-- auto-resuming claim/dispatch", flush=True)
        return False
    return True


def write_backoff(reason, worker, cooldown=BACKOFF_COOLDOWN):
    os.makedirs(STORE, exist_ok=True)
    until_dt = datetime.now(timezone.utc) + timedelta(seconds=cooldown)
    payload = {"ts": now_iso(), "until": until_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
               "reason": reason, "worker": worker}
    with open(BACKOFF_PATH, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    return payload


def clear_backoff():
    existed = os.path.exists(BACKOFF_PATH)
    if existed:
        os.remove(BACKOFF_PATH)
    return existed


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


_skip_logged = set()   # tickets already warned about — log each skip once, not every pass


def dispatchable(fname):
    """Filter for pending_tickets() (queue/.CONVENTION.md warning made real):
    NOT every queue .json is for a tmux Claude worker. Skip (a) external-research
    tickets — self-contained payloads for a non-Claude consumer, (b) tickets David
    has explicitly deferred, (c) unparseable JSON (skip-and-warn beats crash or
    blind dispatch)."""
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
        print(f"[skip]     ticket {fname}: {reason}", flush=True)
    return False


def pending_tickets():
    """Real queue scan (not a fixed list) — oldest-first by filename, matching
    claim-next.sh's convention (timestamp-prefixed names sort in time order).
    Filtered through dispatchable() — external-research/deferred tickets stay
    in queue/ untouched."""
    return sorted(f for f in os.listdir(Q) if f.endswith(".json") and dispatchable(f))


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



# --- generalized VERIFIERS: a pluggable check registry -------------------------
#
# The one bespoke function above (verify_constellation_4_apps) doesn't scale — every
# new ticket kind previously needed a hand-written Python function added here. This
# adds a small declarative check DSL instead: a ticket sets verify_kind="generic" and
# carries a verify_spec.checks[] list, each check naming one of the pluggable types
# below (file_exists / json_parses / must_contain / git_commit_present / script).
# New ticket kinds compose these; only a genuinely novel check TYPE (rare) needs new
# Python. verify_constellation_4_apps is untouched — this is purely additive.

def check_file_exists(check, _ticket):
    rel = check["path"]
    ok = os.path.exists(os.path.join(REPO, rel))
    return ok, (None if ok else f"missing file: {rel}")


def check_json_parses(check, _ticket):
    rel = check["path"]
    try:
        json.load(open(os.path.join(REPO, rel)))
        return True, None
    except Exception as e:
        return False, f"{rel} failed to parse as JSON: {e}"


def check_must_contain(check, _ticket):
    rel = check["path"]
    wanted = check.get("text") or check.get("contains") or []
    wanted = wanted if isinstance(wanted, list) else [wanted]
    try:
        body = open(os.path.join(REPO, rel), encoding="utf-8").read()
    except Exception as e:
        return False, f"{rel} unreadable: {e}"
    missing = [w for w in wanted if w not in body]
    return (not missing), (None if not missing else f"{rel} missing expected text: {missing}")


def check_git_commit_present(check, _ticket):
    """Confirm real work landed as a commit — either a specific sha (check['sha']),
    or a recent commit whose message contains check['message_contains']. Read-only:
    never creates a commit itself."""
    sha = check.get("sha")
    if sha:
        r = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                            cwd=REPO, capture_output=True)
        return r.returncode == 0, (None if r.returncode == 0 else f"commit sha not found in repo: {sha}")
    needle = check.get("message_contains")
    if needle:
        r = subprocess.run(["git", "log", "--oneline", "-n", "50", f"--grep={needle}"],
                            cwd=REPO, capture_output=True, text=True)
        found = bool(r.stdout.strip())
        return found, (None if found else f"no recent commit message contains: {needle!r}")
    return False, "git_commit_present check needs 'sha' or 'message_contains'"


def check_script(check, _ticket):
    """Custom script path — a ticket can name its OWN verifier script instead of
    composing the built-in check types. Run as `python3 <path> [args...]` if the
    path ends in .py, else executed directly. Exit 0 = pass."""
    rel = check.get("path")
    if not rel:
        return False, "script check missing 'path'"
    full = rel if os.path.isabs(rel) else os.path.join(REPO, rel)
    if not os.path.exists(full):
        return False, f"verifier script not found: {rel}"
    cmd = (["python3", full] if full.endswith(".py") else [full]) + list(check.get("args", []))
    try:
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, timeout=check.get("timeout", 60))
        ok = r.returncode == 0
        return ok, (None if ok else f"script {rel} exited {r.returncode}: {r.stderr.decode(errors='replace')[:300]}")
    except Exception as e:
        return False, f"script {rel} failed to run: {e}"


def check_command(check, _ticket):
    """Raw shell command, exit 0 = pass. Lower-ceremony than check_script when a
    ticket just needs an ad-hoc one-liner, not a standalone verifier file."""
    cmd = check.get("cmd")
    if not cmd:
        return False, "command check missing 'cmd'"
    try:
        r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, timeout=check.get("timeout", 60))
        ok = r.returncode == 0
        return ok, (None if ok else f"command exited {r.returncode}: {cmd!r} stderr={r.stderr.decode(errors='replace')[:300]}")
    except Exception as e:
        return False, f"command failed to run: {e}"


CHECK_REGISTRY = {
    "file_exists": check_file_exists,
    "json_parses": check_json_parses,
    "must_contain": check_must_contain,
    "git_commit_present": check_git_commit_present,
    "script": check_script,
    "command": check_command,
}


def verify_generic_declarative(ticket):
    """verify_kind="generic": walk ticket["verify_spec"]["checks"], each a
    {"type": <CHECK_REGISTRY key>, ...params}. ALL checks must pass. A ticket kind
    that needs a check type not in CHECK_REGISTRY still needs Python — everything
    else needs zero orchestrator.py edits."""
    spec = ticket.get("verify_spec") or {}
    checks = spec.get("checks", [])
    if not checks:
        return False, ["verify_kind=generic but verify_spec.checks is empty/missing"]
    findings = []
    for c in checks:
        ctype = c.get("type")
        fn = CHECK_REGISTRY.get(ctype)
        if not fn:
            findings.append(f"unknown check type: {ctype!r} (known: {sorted(CHECK_REGISTRY)})")
            continue
        ok, msg = fn(c, ticket)
        if not ok:
            findings.append(msg)
    return (len(findings) == 0), findings


def verify_artifacts_fallback(ticket):
    """Generic fallback for tickets with no verify_kind at all: if the ticket itself
    names artifact paths and/or a verify_command directly (no verify_spec.checks[]
    ceremony needed), check those. Lighter-weight than the full 'generic' DSL for a
    ticket that just wants 'these paths exist, and this command exits 0'."""
    findings = []
    for rel in ticket.get("artifacts") or []:
        if not os.path.exists(os.path.join(REPO, rel)):
            findings.append(f"missing artifact: {rel}")
    cmd = ticket.get("verify_command")
    if cmd:
        try:
            r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, timeout=60)
            if r.returncode != 0:
                findings.append(f"verify_command exited {r.returncode}: {cmd!r}")
        except Exception as e:
            findings.append(f"verify_command failed to run: {e}")
    return (len(findings) == 0), findings


# --- wargame verifier: independent re-verification at reap (wg-t1-15) ----------
#
# BMAD Swagger's discipline (research/bmad-pattern-mining/bmad-machinery-pattern.md):
# never trust the worker's self-report -- re-derive the verdict from primary
# evidence. The war games (backlog/wargames/<ID>.md) already carry a machine-
# readable spec for this: a fenced ```bash block under '## Verification' with
# runnable positive + negative checks. This verifier extracts and runs that block
# directly, instead of trusting results/<tid>.json's claimed status.

WARGAME_PATH_RE = re.compile(r'backlog/wargames/[\w.\-]+\.md')


def resolve_wargame_path(ticket):
    """A ticket names its war game in 'source' and/or 'prompt' (free text). Find
    the first backlog/wargames/<ID>.md reference; None if there isn't one."""
    for field in ("source", "prompt"):
        m = WARGAME_PATH_RE.search(ticket.get(field) or "")
        if m:
            return os.path.join(REPO, m.group(0))
    return None


def extract_wargame_checks(md_path):
    """Strict contract (war game Move 1): checks live in a fenced ```bash block
    under the '## Verification' heading. Returns (checks: list[str], error: None)
    on success, or (None, error) if the heading/fence is missing or yields nothing
    runnable -- callers must fall back to today's behaviour + a logged warning,
    never silently pass. Full-comment and blank lines are skipped; a `<<DELIM`
    heredoc is kept as a single multi-line check."""
    try:
        text = open(md_path, encoding="utf-8").read()
    except Exception as e:
        return None, f"war game file unreadable: {md_path}: {e}"

    heading = re.search(r'^## Verification\s*$', text, re.M)
    if not heading:
        return None, f"no '## Verification' heading in {md_path}"

    fence = re.search(r'```bash\s*\n(.*?)```', text[heading.end():], re.S)
    if not fence:
        return None, f"no fenced ```bash block under '## Verification' in {md_path}"

    lines = fence.group(1).splitlines()
    checks, i = [], 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        heredoc = re.search(r'<<-?\s*[\'"]?(\w+)[\'"]?', line)
        if heredoc:
            delim = heredoc.group(1)
            block = [line]
            i += 1
            while i < len(lines) and lines[i].strip() != delim:
                block.append(lines[i]); i += 1
            if i < len(lines):
                block.append(lines[i]); i += 1
            checks.append("\n".join(block))
            continue
        checks.append(line)
        i += 1

    if not checks:
        return None, f"'## Verification' block in {md_path} parsed but yielded no runnable lines"
    return checks, None


def git_status_snapshot():
    r = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True)
    return r.stdout


def run_wargame_checks(checks):
    """Run each extracted check read-only against the repo (a bare `cd <dir>` line
    changes cwd for subsequent checks, matching how the war games write multi-step
    blocks; it is not itself executed as a command). A non-zero exit = a failed
    check, exactly like a failed negative check."""
    findings = []
    cwd = REPO
    for cmd in checks:
        stripped = cmd.strip()
        cd_only = re.match(r'^cd\s+(\S+)\s*$', stripped) if "\n" not in cmd else None
        if cd_only:
            target = cd_only.group(1)
            target = target if os.path.isabs(target) else os.path.join(REPO, target)
            if os.path.isdir(target):
                cwd = target
            else:
                findings.append(f"cd target not found: {target}")
            continue
        try:
            r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                                timeout=60, executable="/bin/bash")
            if r.returncode != 0:
                findings.append(f"check failed (exit {r.returncode}): {cmd.splitlines()[0][:120]} "
                                 f"stderr={r.stderr.decode(errors='replace')[:300]}")
        except Exception as e:
            findings.append(f"check errored: {cmd.splitlines()[0][:120]}: {e}")
    return (len(findings) == 0), findings


def find_results_file(ticket, tid=None):
    """Locate the worker's results/<tid>.json for self-report cross-checking.
    Prefers the caller-supplied tid (the queue filename); falls back to matching
    the ticket's own 'ticket' field, since it doesn't always equal the filename
    stem (e.g. timestamp-prefixed filenames)."""
    if tid:
        p = os.path.join(RES, tid)
        if os.path.exists(p):
            return p
    want = ticket.get("ticket")
    if not want:
        return None
    p = os.path.join(RES, f"{want}.json")
    if os.path.exists(p):
        return p
    try:
        for f in os.listdir(RES):
            try:
                if json.load(open(os.path.join(RES, f))).get("ticket") == want:
                    return os.path.join(RES, f)
            except Exception:
                continue
    except FileNotFoundError:
        pass
    return None


def verify_wargame(ticket, tid=None):
    """verify_kind="wargame" (also auto-applied by verify() when no verify_kind is
    set but the ticket names a backlog/wargames/<ID>.md source): re-derive the
    verdict from the war game's own '## Verification' block instead of trusting
    the worker's results/<tid>.json self-report. Read-only -- never edits a worker
    artifact to force a pass. Falls back to an artifact-only pass (+ a logged
    warning) whenever the war game can't be resolved or its block can't be parsed,
    so tickets without a clean machine-readable spec keep working exactly as
    before this verifier existed."""
    md_path = resolve_wargame_path(ticket)
    if not md_path or not os.path.exists(md_path):
        print(f"[verify]   wargame: no resolvable backlog/wargames/*.md for "
              f"{ticket.get('ticket', tid)} -- falling back to artifact-only pass", flush=True)
        return True, []

    checks, err = extract_wargame_checks(md_path)
    if err:
        print(f"[verify]   wargame: {err} -- falling back to artifact-only pass", flush=True)
        return True, []

    before = git_status_snapshot()
    ok, findings = run_wargame_checks(checks)
    after = git_status_snapshot()
    if before != after:
        ok = False
        findings.append("war-game verification commands modified the repo (should be read-only) "
                         "-- war-game authoring defect, flag for the T8 truth pass")

    res_path = find_results_file(ticket, tid)
    claimed = None
    if res_path:
        try:
            claimed = json.load(open(res_path)).get("status")
        except Exception:
            claimed = None
    print(f"[verify]   wargame {ticket.get('ticket', tid)}: worker claimed={claimed!r} "
          f"engine_verdict={'done' if ok else 'fail'}", flush=True)
    if claimed == "done" and not ok:
        findings.append("worker self-report contradicted by independent evidence "
                         "(claimed done, war-game checks disagree) -- verdict_source: engine")

    return ok, findings


VERIFIERS = {
    "constellation-4-apps": verify_constellation_4_apps,   # unchanged, kept working
    "generic": verify_generic_declarative,                  # new: declarative checks[] DSL
    "artifacts": verify_artifacts_fallback,                 # new: explicit opt-in to the fallback shape
    "wargame": verify_wargame,                               # wg-t1-15: independent re-verify at reap
}


def verify(ticket, tid=None):
    """Returns (ok: bool, findings: list[str]).

    - verify_kind set + known -> that VERIFIERS entry (bespoke or generic-DSL).
    - verify_kind set + unknown -> fail loudly (unchanged behavior).
    - no verify_kind, but the ticket names a backlog/wargames/<ID>.md source ->
      the wargame verifier (new, wg-t1-15): reap re-derives the verdict from the
      war game's own checks instead of trusting the worker's self-report.
    - no verify_kind, no war game, but the ticket names artifacts/verify_command
      directly -> the lightweight fallback checker.
    - none of the above -> pass, same as before this change (generic tickets that
      only ever relied on artifact_ok() + self-report keep working exactly as they
      did)."""
    vk = ticket.get("verify_kind")
    if not vk:
        if resolve_wargame_path(ticket):
            return verify_wargame(ticket, tid)
        if ticket.get("artifacts") or ticket.get("verify_command"):
            return verify_artifacts_fallback(ticket)
        return True, []
    fn = VERIFIERS.get(vk)
    if not fn:
        return False, [f"unknown verify_kind: {vk}"]
    return fn(ticket)


def commit(tid):
    src = os.path.join(RUN, tid); dst = os.path.join(DONE, tid)
    if not os.path.exists(src):
        if os.path.exists(dst):
            return  # already committed — idempotent, not an error
        print(f"[reap]     WARN commit({tid}): neither running/ nor done/ present — skipping", flush=True)
        return
    os.rename(src, dst)


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


# --- verdict ledger (wg-t1-16): durable, prior-chained reap outcomes -----------

def _read_jsonl(path):
    """Defensive JSONL reader — a malformed line is skipped, never raises. Shared
    by the ledger and (via status.py) the audit trail."""
    if not os.path.exists(path):
        return []
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def _short_evidence(x, limit=400):
    if isinstance(x, (list, tuple)):
        x = "; ".join(str(i) for i in x)
    x = str(x)
    return x if len(x) <= limit else x[:limit] + "…"


def prior_ledger_id(tid):
    """The ticket's most recent ledger line id, or None if this is its first —
    the chain a re-attempted ticket (T1-11 hit attempt 3) reconstructs from disk."""
    last = None
    for e in _read_jsonl(LEDGER):
        if e.get("ticket") == tid:
            last = e
    return last.get("id") if last else None


def record_verdict(tid, attempt, verdict, verdict_source, evidence, next_action, embed=True):
    """Append one line to ledger.jsonl for this reap outcome, chained to the
    ticket's previous attempt via 'prior'. When embed=True (a real settle, not an
    interim requeue) also writes the same block as ticket["verdict"] at the
    ticket's CURRENT on-disk location (running/ — called before commit() renames
    it to done/, so the embed lands wherever the file ends up). audit.jsonl
    (dispatch/input) is never touched here — this is the outcome/result ledger."""
    entry = dict(
        id=f"{tid}#{attempt}",
        ticket=tid,
        attempt=attempt,
        verdict=verdict,
        verdict_source=verdict_source,
        evidence=_short_evidence(evidence),
        ts=now_iso(),
        prior=prior_ledger_id(tid),
        next=next_action,
    )
    with open(LEDGER, "a") as f:
        f.write(json.dumps(entry) + "\n")
    if embed:
        for d in (RUN, DONE):
            p = os.path.join(d, tid)
            if os.path.exists(p):
                try:
                    t = json.load(open(p))
                    t["verdict"] = entry
                    with open(p, "w") as tf:
                        json.dump(t, tf, indent=2)
                        tf.write("\n")
                except Exception as e:
                    print(f"[ledger]   WARN could not embed verdict into {p}: {e}", flush=True)
                break
    return entry


def main():
    safety_check()
    ensure_dirs()

    argv = sys.argv
    model = argv[argv.index("--model") + 1] if "--model" in argv else MODEL
    pool_size = int(argv[argv.index("--pool") + 1]) if "--pool" in argv else POOL
    max_wall = int(argv[argv.index("--max-wall") + 1]) if "--max-wall" in argv else MAX_WALL
    # Inactivity window before rebooting a silent worker (wg-t1-14): resets on any pane-output
    # change (a["last_active"], set in the poll loop below), so a worker that keeps producing
    # output -- war-game tickets spend all their recon/evidence moves writing NOTHING to an
    # artifact until a late authoring move -- is never rebooted just for taking a long time.
    # A genuinely wedged (silent) worker still reboots once this window elapses.
    # --max-wall remains the separate, absolute hard ceiling on total run time (untouched).
    worker_timeout = int(argv[argv.index("--worker-timeout") + 1]) if "--worker-timeout" in argv else WORKER_TIMEOUT
    teardown = "--teardown" in argv
    gated_tid = argv[argv.index("--hitl") + 1] if "--hitl" in argv else None

    if pool_size > CAP:
        print(f"[cap]      *** requested --pool {pool_size} exceeds hard CAP={CAP} "
              f"(429-wall admission control, docs/kill-switch-spec.md idiom) -- "
              f"clamping to {CAP} ***", flush=True)
        pool_size = CAP

    banner(f"dark-factory engine kernel — pool={pool_size} model={model} "
           f"worker-timeout={worker_timeout}s "
           f"repo={REPO} subscription-only" + (f" (--hitl {gated_tid})" if gated_tid else ""))

    pool = WarmPool(pool_size, model, REPO)
    boots = pool.boot_all()
    print(f"[pool] {pool_size} warm worker(s) booted in {sum(boots):.0f}s total "
          f"({', '.join(f'{b:.0f}s' for b in boots)}) — named df-worker-1.."
          f"{pool_size} (tmux ls / tmux attach -t df-worker-1)", flush=True)

    active = {}     # tid -> dict(worker, started, gated, state, blocked_since, ticket, last_active, last_pane)
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

        # Kill switch (docs/kill-switch-spec.md): checked before EVERY claim/
        # dispatch pass. Halted -> skip leasing/dispatching new tickets this
        # pass, but fall through to the reap loop below unchanged (already-
        # running tickets are never killed mid-task; graceful only).
        if is_halted():
            info = halt_info() or {}
            print(f"[halt]     factory halted since {info.get('ts', '?')} by {info.get('by', '?')} "
                  f"({info.get('reason', '?')}) -- skipping claim/dispatch this pass", flush=True)
        elif is_backoff():
            info = backoff_info() or {}
            print(f"[backoff]  factory in backoff since {info.get('ts', '?')} until {info.get('until', '?')} "
                  f"({info.get('reason', '?')}) -- skipping claim/dispatch this pass", flush=True)
        else:
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
                                    state="running", blocked_since=None, ticket=ticket,
                                    last_active=time.time(), last_pane="")
                peak = max(peak, len(active))
                if not w.session_id:
                    w.session_id, w.transcript = find_session(REPO, f"ticket id is {tid}.")
                audit(dict(ticket=tid, attempt=retries.get(tid, 0) + 1, worker=w.name,
                           session_id=w.session_id, transcript=w.transcript,
                           claimed_by=ticket.get("claimed_by"), claimed_at=ticket.get("claimed_at")))
                print(f"[dispatch] ticket {tid} -> {w.name}  (session {(w.session_id or '?')[:8]})", flush=True)

        for tid, a in list(active.items()):
            # Activity fingerprint (wg-t1-14): pane text changed since last poll -> worker is
            # doing something, even if it hasn't landed an artifact yet. Bumps last_active,
            # which is what the reboot branch below keys on instead of raw elapsed time.
            pane = a["worker"].capture()
            if pane != a["last_pane"]:
                a["last_pane"] = pane
                a["last_active"] = time.time()

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
                        # HITL wait can outlast worker_timeout with zero pane activity (human
                        # thinking, not the worker) -- reset the inactivity clock on resume too,
                        # or the reboot branch below would trip on its very next poll.
                        a["last_active"] = time.time()
                        print(f"[HITL] resumed ticket {tid} decision={act.upper()}", flush=True)
                        if act == "decline":
                            record_verdict(tid, retries.get(tid, 0) + 1, "declined", "hitl",
                                           f"human declined via {dfile}", None)
                            results[tid] = "declined"; settle(tid, a)
                        continue
                    if time.time() - a["blocked_since"] > HITL_TIMEOUT:
                        record_verdict(tid, retries.get(tid, 0) + 1, "failed(no-decision)", "hitl",
                                       f"no HITL decision within {HITL_TIMEOUT}s ({nd})", None)
                        w = a["worker"]; del active[tid]; w.reboot(); w.busy = None
                        results[tid] = "failed(no-decision)"
                        print(f"[HITL] ticket {tid}: no decision in {HITL_TIMEOUT}s -> surfaced unanswered", flush=True)
                        continue
                    continue

            if artifact_ok(tid):
                ok, findings = verify(a["ticket"], tid)
                if ok:
                    record_verdict(tid, retries.get(tid, 0) + 1, "done", "engine",
                                   "artifact present, verify() passed", "done")
                    commit(tid); results[tid] = "done"; settle(tid, a)
                    ev = emit_event("job.completed", dict(ticket=tid, result="done"))
                    print(f"[reap]     ticket {tid}: done, verified -> event {os.path.basename(ev)}", flush=True)
                else:
                    print(f"[verify]   ticket {tid}: artifact present but verification FAILED: {findings}", flush=True)
                    # Decided on FIRST detection (wg-t1-20), not after 30min of re-running the
                    # SAME deterministic verify() every poll (T1-16 live wedge): verify() is a
                    # pure read of static state, so the verdict can't change between polls --
                    # caching/acting on the first result is safe. Mirrors the inactivity-timeout
                    # retry idiom below (reboot immediately, re-queue with retries[tid] bumped up
                    # to MAX_RETRY, else settle) so there's ONE retry idiom, not two.
                    w = a["worker"]
                    del active[tid]
                    w.reboot(); w.busy = None
                    print(f"[reboot]   {w.name}: verify FAILED on ticket {tid} -> fresh process", flush=True)
                    if retries.get(tid, 0) < MAX_RETRY:
                        retries[tid] = retries.get(tid, 0) + 1
                        record_verdict(tid, retries[tid], "failed(verify)", "engine", findings, "queue", embed=False)
                        # Hand the retried worker the engine's independent findings (the whole
                        # point of retrying, vs the worker blindly resubmitting the same result):
                        # append them to the ticket's own prompt field, which is what the worker
                        # re-reads fresh via task_prompt's pointer indirection.
                        run_path = os.path.join(RUN, tid)
                        try:
                            t = json.load(open(run_path))
                            t["prompt"] = t.get("prompt", "") + (
                                f"\n\nRETRY {retries[tid]}/{MAX_RETRY}: the previous attempt's artifact FAILED "
                                f"the engine's independent verification. Engine findings: {findings}. Re-read "
                                f"this ticket fresh and fix the actual defects -- do not just resubmit the same "
                                f"result."
                            )
                            with open(run_path, "w") as f:
                                json.dump(t, f, indent=2)
                                f.write("\n")
                        except Exception as e:
                            print(f"[verify]   WARN could not embed retry findings into {run_path}: {e}", flush=True)
                        os.rename(run_path, os.path.join(Q, tid))
                        print(f"[reap]     ticket {tid}: verify FAILED -> re-queue with findings (retry {retries[tid]})", flush=True)
                    else:
                        record_verdict(tid, retries.get(tid, 0) + 1, "failed(verify)", "engine", findings, None)
                        results[tid] = "failed(verify)"
                        ev = emit_event("job.completed", dict(ticket=tid, result="failed(verify)"))
                        print(f"[reap]     ticket {tid}: verify FAILED, retries exhausted -> settled "
                              f"failed(verify) -> event {os.path.basename(ev)}", flush=True)
            # Reboot on INACTIVITY, not raw elapsed time (wg-t1-14): a worker that keeps
            # producing pane output is never rebooted here no matter how long it runs --
            # --max-wall (checked below, outside this loop) is the separate hard ceiling that
            # still bounds total run time regardless of activity.
            elif time.time() - a["last_active"] > worker_timeout:
                w = a["worker"]
                # LIMIT DETECTION: before rebooting a wedged worker, sniff its pane for a
                # 429/usage-limit signature -- a reboot would otherwise mask exactly the
                # symptom we need to see (docs/kill-switch-spec.md idiom, mirrored here).
                pane_text = w.capture()
                if looks_like_usage_limit(pane_text):
                    lowered = pane_text.lower()
                    matched = next((s for s in USAGE_LIMIT_SIGNATURES if s in lowered), "?")
                    reason = f"usage-limit signature '{matched}' on {w.name} (ticket {tid})"
                    write_backoff(reason, w.name)
                    print(f"[backoff]  ticket {tid}: {w.name} pane shows '{matched}' -> BACKOFF written "
                          f"(cooldown {BACKOFF_COOLDOWN}s)", flush=True)
                    notify("engine: entering BACKOFF",
                           f"{w.name} hit a usage limit ({matched}) -- pausing claim/dispatch "
                           f"~{BACKOFF_COOLDOWN // 60}min")
                del active[tid]
                w.reboot(); w.busy = None
                print(f"[reboot]   {w.name}: wedged on ticket {tid} -> fresh process", flush=True)
                if retries.get(tid, 0) < MAX_RETRY:
                    retries[tid] = retries.get(tid, 0) + 1
                    record_verdict(tid, retries[tid], "failed(timeout)", "engine",
                                   f"worker unresponsive > {worker_timeout}s (inactivity)", "queue", embed=False)
                    os.rename(os.path.join(RUN, tid), os.path.join(Q, tid))
                    print(f"[reap]     ticket {tid}: no response -> re-queue (retry {retries[tid]})", flush=True)
                else:
                    record_verdict(tid, retries.get(tid, 0) + 1, "failed(timeout)", "engine",
                                   f"worker unresponsive > {worker_timeout}s (inactivity), retries exhausted", None)
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
