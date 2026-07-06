#!/usr/bin/env python3
"""
warm_pool.py — PERSISTENT REUSABLE WORKER pool for the dark-factory production engine.

Adapted, not rewritten, from suborch-demo's proven warm_pool.py
(~/dev/ad/apps/suborch-demo/warm_pool.py — see docs/harness-evaluation.md, promotion
plan Phase 2: "Vendor suborch-demo/warm_pool.py behind Marshall's dispatch"). The
mechanics (boot-once REPL + send-keys reuse, artifact-is-truth idle detection,
content-based session resolution) are suborch's; the only changes here are dark-factory
naming/visibility conventions:

  - tmux sessions are named `df-worker-<n>` (not `warm-<name>`) so they are
    immediately recognizable via `tmux ls` and attach-able via
    `tmux attach -t df-worker-1` — VISIBILITY IS A REQUIREMENT per the harness
    evaluation's per-mechanism verdict (dispatch row).
  - default pool size is 1 (dark-factory runs real, expensive jobs — not 3 cheap
    haiku trivia workers).

Invariant unchanged: interactive `claude` only. No -p, no SDK, ANTHROPIC_API_KEY unset.
Reaping stays artifact-is-truth: the caller verifies a real file, never the REPL text.
"""
import os, sys, time, subprocess, glob
from halt import is_halted

HOME = os.path.expanduser("~")


def _tmux(*a):
    return subprocess.run(["tmux", *a], capture_output=True, text=True)


def project_dir(cwd):
    """Where Claude Code persists a cwd's session transcripts: it slugs the absolute
    path, replacing '/' and '_' with '-'."""
    slug = os.path.abspath(cwd).replace("/", "-").replace("_", "-")
    return os.path.join(HOME, ".claude", "projects", slug)


def find_session(cwd, needle, timeout=8):
    """Resolve a worker's session UUID + transcript path by CONTENT — the .jsonl that
    contains a unique marker from its first turn."""
    pd = project_dir(cwd)
    t0 = time.time()
    while time.time() - t0 < timeout:
        for f in glob.glob(os.path.join(pd, "*.jsonl")):
            try:
                if needle in open(f, errors="ignore").read():
                    return os.path.basename(f)[:-6], f
            except OSError:
                pass
        time.sleep(0.4)
    return None, None


def safety_check():
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        sys.exit("ABORT: ANTHROPIC_API_KEY/AUTH_TOKEN set -> metered billing. Unset first.")


class WarmWorker:
    """One persistent interactive REPL in a detached, NAMED, attach-able tmux session."""

    def __init__(self, index, model, cwd, extra_flags=()):
        self.name = f"df-worker-{index}"
        self.model = model
        self.cwd = cwd
        self.extra_flags = list(extra_flags)
        self.session = self.name           # tmux session name == worker name (visibility)
        self.busy = None                   # ticket id when assigned, else None
        self.booted = False
        self.session_id = None             # this boot's Claude session UUID (its transcript file)
        self.transcript = None             # absolute path to the .jsonl — the audit trail

    def capture(self):
        return _tmux("capture-pane", "-t", self.session, "-p").stdout

    def boot(self, timeout=90):
        self.session_id = None
        self.transcript = None
        _tmux("kill-session", "-t", self.session)
        _tmux("new-session", "-d", "-s", self.session, "-x", "220", "-y", "50")
        flags = " ".join(self.extra_flags)
        cmd = (f"cd {self.cwd} && claude --model {self.model} "
               f"--dangerously-skip-permissions --strict-mcp-config {flags}".rstrip())
        _tmux("send-keys", "-t", self.session, "-l", cmd)
        _tmux("send-keys", "-t", self.session, "Enter")
        t0 = time.time()
        while time.time() - t0 < timeout:
            pane = self.capture()
            if "bypass permissions on" in pane or "for shortcuts" in pane:
                self.booted = True
                return time.time() - t0
            time.sleep(1)
        raise TimeoutError(f"worker {self.name} REPL never became ready")

    def send(self, prompt):
        """Inject a turn into the live REPL (no re-boot). Keep prompts single-line —
        tmux send-keys -l does not simulate real newline keypresses reliably; the
        worker is handed a POINTER to a file for anything multi-line (SPK-D1)."""
        _tmux("send-keys", "-t", self.session, "-l", prompt)
        time.sleep(0.4)
        _tmux("send-keys", "-t", self.session, "Enter")

    def idle(self):
        """True iff the REPL is at rest. The TUI's spinner verb is random (Working…,
        Crafting…, Cogitating…) so key on the trailing ellipsis, checked in the
        footer region only."""
        region = "\n".join(l for l in self.capture().splitlines() if l.strip())[-400:]
        return ("…" not in region) and ("esc to interrupt" not in region)

    def reboot(self):
        """Recover a wedged worker (never idles) with a fresh process."""
        self.stop()
        return self.boot()

    def clear(self):
        """Reset conversation context, keep the process warm."""
        _tmux("send-keys", "-t", self.session, "-l", "/clear")
        time.sleep(0.4)
        _tmux("send-keys", "-t", self.session, "Enter")
        time.sleep(0.8)

    def stop(self):
        _tmux("kill-session", "-t", self.session)
        self.booted = False


class WarmPool:
    def __init__(self, size, model, cwd, extra_flags=()):
        self.workers = [WarmWorker(i + 1, model, cwd, extra_flags) for i in range(size)]

    def boot_all(self):
        times = []
        for w in self.workers:                 # sequential boots: gentle on the 429 wall
            times.append(w.boot())
        return times

    def free_worker(self):
        """Defense-in-depth for the kill switch (docs/kill-switch-spec.md):
        while HALT is set, no free worker is ever handed out, so orchestrator.py's
        dispatch loop cannot send a NEW ticket to any worker even if some future
        caller forgets its own is_halted() check. Workers already mid-task are
        untouched here — this only gates handing out a worker for NEW work."""
        if is_halted():
            return None
        for w in self.workers:
            if w.busy is None:
                return w
        return None

    def teardown_all(self):
        for w in self.workers:
            w.stop()

    def leftover_check(self):
        ls = _tmux("ls").stdout
        return [w.session for w in self.workers if w.session in ls]
