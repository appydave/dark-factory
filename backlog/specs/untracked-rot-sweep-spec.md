# Spec — Untracked-Rot Sweep (detect-and-tell git-hygiene sentinel)

**Ticket:** DF-9 · **Project:** constellation (AppyRadar) · **Lane:** B (Observability) + hygiene
**Status:** SPEC ONLY — no build. Building is a later, separately-dispatched job.
**Author:** Marshall · **Requested by:** David · **Date:** 2026-06-11
**Memory:** [[untracked-file-rot]], [[cleanup-is-harness-driven-not-remembered]], [[observability-and-balanced-growth]], [[dark-factory-is-a-constellation-of-apps]]

---

## 1. Purpose

Make git-hygiene debt **visible automatically** so deliverables stop rotting uncommitted across repos. A standing **detect-and-tell** sweep that reports — never acts. The motivating incident: 2026-06-11, the dark-factory repo had **72 untracked + 8 modified + 1 deleted** files — multiple prior sessions' real tools/skills/docs left uncommitted because nobody surfaced the pile. A human had to notice and trigger a manual cleanup.

## 2. Problem Statement

End-of-session discipline ("mark complete, commit") is **remembered, not enforced** — so it fails session after session. The cost is invisible until someone runs `git status` and finds hundreds of files. This is the same class of failure as the reaper solved for windows: **relying on an agent to remember to clean up doesn't work.** The fix is the same shape: a harness-driven sentinel that **observes externally and tells**, so the human (or Marshall) can decide.

This is **AppyRadar-natural** — AppyRadar's charter is resource-health / already-built detection across the workspace; uncommitted-deliverable debt is a resource-health signal.

## 3. Goals

- **G1.** Detect git-hygiene debt across a configured set of repos: untracked files, modified-but-uncommitted, staged-not-committed, deleted-uncommitted, and stale/abandoned worktrees.
- **G2.** Classify each untracked item as **likely-deliverable** vs **likely-ignorable** (so the report leads with what matters, not screenshot noise).
- **G3.** Report age — oldest debt per repo (how long has this been rotting?).
- **G4.** **Tell, never act.** Emit a structured record + a one-line surfacing for Marshall. No auto-commit, no auto-gitignore, no auto-anything.
- **G5.** Cover **both machines** (M4 Pro local + M4 Mini over Tailscale), reusing the mocha-census both-machine pattern.

## 4. Non-Goals

- **NOT** auto-committing, auto-staging, or writing `.gitignore` (this spec's whole point is detect-and-tell; acting is the human's/Marshall's call — see [[cleanup-is-harness-driven-not-remembered]]).
- **NOT** a git wrapper / merge-conflict resolver (that's `appydave:easy-git`).
- **NOT** policing commit *messages* or *content quality*.
- **NOT** scanning inside ignored paths (respect each repo's `.gitignore`).

## 5. Users and Roles

- **Marshall** — consumes the one-line surfacing at session open (BOLDLY, if a threshold is crossed — same posture as the constellation preflight).
- **David** — sees the report, decides what to commit / ignore / discard.
- **AppyRadar** — owns the sweep as one of its resource-health probes; emits to Switchboard; Watchtower renders.

## 6. Product Scope

### In scope
- A repo-set config (which repos to watch; default: the dark-factory cluster + brains + active app repos).
- Per-repo scan producing counts + classified file lists + oldest-debt age.
- A structured output record (jsonl) + a human one-liner.
- Both-machine execution.

### Out of scope (later)
- A rich Watchtower panel (MVP emits the record; viz is a follow-on).
- Auto-remediation of any kind.
- Cross-repo "this file looks like it belongs in repo X" intelligence.

### MVP vs later
- **MVP:** one machine, one configured repo-list, `git status --porcelain` parse → classified record + Marshall one-liner.
- **Later:** both-machine fan-out, age tracking, Watchtower panel, threshold-based BOLD surfacing.

## 7. Key Concepts / Entities

- **Debt item** — one path in a non-clean git state, with `{repo, path, state, classification, age_days}`.
- **State** — `untracked | modified | staged | deleted | stale-worktree`.
- **Classification** — `likely-deliverable | likely-ignorable | unknown` (heuristic, see §11).
- **Repo report** — `{repo, machine, counts_by_state, oldest_debt_days, items[]}`.
- **Sweep record** — the full multi-repo, multi-machine roll-up (one jsonl line per sweep).

## 8. Functional Requirements

### 8.1 Detect (the core)
- For each configured repo, run `git status --porcelain=v1 -z` (ignored paths excluded by default) + detect worktrees (`git worktree list`) with no commits/branch ahead and old mtime.
- Compute `oldest_debt_days` from filesystem mtime of the oldest untracked/modified path (git has no untracked-age; mtime is the proxy — state the limitation in output).

### 8.2 Classify (lead with what matters)
- Apply heuristics (§11) to tag each item `likely-deliverable | likely-ignorable | unknown`.
- The report **sorts deliverables first**; ignorable noise (screenshots, caches, logs) is collapsed to a count.
- A **gitignore-gap hint**: if ≥N ignorable items share a pattern (e.g. `*.png` at root), suggest the human add a `.gitignore` rule (suggest only — never write it).

### 8.3 Tell (never act)
- Emit the sweep record to Switchboard (the comms bus) + persist jsonl.
- Produce a one-line Marshall surfacing: `⚠️ git-hygiene: <N> uncommitted deliverables across <M> repos (oldest <D>d — <repo>). Run the sweep report for detail.`
- **Threshold:** if any repo has ≥ `bold_threshold` likely-deliverable items OR oldest-debt ≥ `age_threshold_days`, Marshall surfaces it **BOLDLY at the top** of a session open (same rule as a DOWN required-app in the preflight).

### 8.4 First-step slice (smallest shippable)
- Single-machine, parse `git status --porcelain` for a hardcoded repo-list, classify untracked-only by file-type/location, print the one-liner + a grouped list. No Switchboard/Watchtower yet.

## 9. Data / Information — Sweep Record Schema

```json
{
  "sweep_id": "sweep-20260611-1",
  "ts": "2026-06-11T...",
  "machines": ["roamy", "m4-mini"],
  "totals": { "repos_scanned": 7, "deliverables": 12, "ignorable": 31, "stale_worktrees": 1 },
  "repos": [
    {
      "repo": "dark-factory", "machine": "roamy",
      "counts": { "untracked": 0, "modified": 0, "staged": 0, "deleted": 0 },
      "oldest_debt_days": 0,
      "items": [ { "path": "...", "state": "untracked", "classification": "likely-deliverable", "age_days": 4 } ]
    }
  ]
}
```

**Placement:** record persisted under AppyRadar's data dir (TBD on app scaffold); emitted to Switchboard; Watchtower reads.

## 10. Business Rules

- **R1. Detect-and-tell only.** The sweep MUST NOT mutate any repo (no add/commit/gitignore/rm). Acting is out of band.
- **R2. Respect `.gitignore`.** Never report ignored paths as debt; their existence is correct.
- **R3. Flags must be reliable** (design-lint precedent): classification heuristics err toward `unknown` rather than mislabel a deliverable as ignorable. Better to surface noise than hide a real deliverable.
- **R4. Read-only on both machines.** Remote scan over Tailscale is read-only (ssh + `git status`), no remote mutation.

## 11. Classification Heuristics (initial, tunable)

| Signal | → classification |
|--------|------------------|
| Under `tools/`, `docs/`, `.claude/skills/`, `backlog/`, `*.md`, `*.json` spec/ticket | `likely-deliverable` |
| Root-level `*.png`/`*.jpg`, `*.log`, `.serve.log`, tool-cache dirs (`.playwright-mcp/`, `.mochaccino/`) | `likely-ignorable` (+ gitignore-gap hint) |
| Inside an experiments `runs/`/`reports/`/`done/` output dir | `likely-deliverable` (engine state) |
| Binary, > size-threshold, or no recognized signal | `unknown` |

## 12. Metrics

- **deliverable-debt count** per repo (the number that matters).
- **oldest-debt age** per repo (mtime proxy).
- **sweep coverage** (repos reached / repos configured; remote failures noted, never silently dropped — [[parallel-and-distributed-execution]]).

## 13. Non-Functional

- Fast (read-only git ops); both-machine fan-out parallel.
- Remote-failure-tolerant: a machine unreachable over Tailscale → report partial + flag the gap, don't fail the sweep.
- Idempotent: running it changes nothing.

## 14. Assumptions

- AppyRadar exists (or will) as the constellation's resource-health app and can host this probe. If not yet scaffolded, the MVP can ship as a standalone script under AppyRadar's intended home and fold in later.
- Tailscale both-machine access works (proven by mocha-census).

## 15. Constraints

- No cron ([[no-cron-automation-runs-in-session]]) — the sweep runs **in-session**, triggered at Marshall's session-open preflight and on demand, not on a timer.
- Read-only remote.

## 16. Risks

- **Misclassification** hides a deliverable → R3 (err toward `unknown`/deliverable).
- **Alert fatigue** — if every session screams about old debt, it gets ignored. Mitigate: collapse ignorable to a count; BOLD only past threshold; let the human snooze a repo.
- **mtime ≠ git-age** — filesystem mtime is a proxy; state it, don't claim git knows.

## 17. Recommended MVP (smallest first step)

**A read-only `git status --porcelain` parse over a configured repo-list on the local machine, classifying untracked items by location/type, printing a one-line summary + deliverables-first grouped list.** Wire into Marshall's session-open preflight as a non-blocking advisory. Everything else (both-machine, age, Switchboard/Watchtower, thresholds) is a follow-on.

## 18. Future Enhancements

- Both-machine fan-out + brains-collection coverage (memory notes brains are the worst offender).
- Watchtower hygiene panel (debt over time; a "rot trend" line).
- Per-repo snooze / acknowledged-debt list.
- A companion **stale-worktree** reaper recommendation (detect → tell → human prunes).

## 19. Open Questions / OPEN PO DECISIONS

1. **Home:** AppyRadar probe (in-app, built via Ralphy) vs a standalone `tools/` script promoted later? (Lean: AppyRadar — it's the resource-health app — but MVP can start as a script.)
2. **Repo-set source of truth:** hardcoded list, a config file, or derived from `brains/source-repos.md` + an apps registry?
3. **Trigger point:** Marshall session-open preflight only, or also a manual `/radar`-style invocation?
4. **Threshold values:** what `bold_threshold` (deliverable count) and `age_threshold_days` cross into BOLD surfacing?
5. **Does the brains repo count as one watched repo, or do we sweep each brain sub-dir?** (brains is the known worst offender.)

## 20. Acceptance Criteria Summary (testable)

- [ ] Given a repo with N untracked deliverables + M ignorable files, the sweep reports N deliverables (listed) and M ignorable (collapsed count), and mutates nothing.
- [ ] Ignored paths never appear as debt.
- [ ] Oldest-debt age is reported per repo (mtime proxy, labeled as such).
- [ ] A one-line Marshall surfacing is produced; past threshold it is marked for BOLD top-of-session surfacing.
- [ ] An unreachable remote machine yields a partial report + an explicit coverage-gap note (never a silent drop).
- [ ] Re-running the sweep produces no repo changes (idempotent / read-only).
