---
topic: "HITL/ratification pipeline"
issue: "Engine has no HITL-park state — a designed decision-pause is misread as a wedged worker and rebooted; the multi-step apply never completes"
created: "2026-07-11"
story_reference: "wg-t3-02"
category: "infrastructure"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: live-capture
provenance_grain: candidate
files: ["engine/orchestrator.py", "canonical/skills/review-dimensional/provenance.json"]
commits: ["153f42e"]
---

# HITL/ratification pipeline — designed decision-pause read as "wedged"

## Problem Signature

**Symptoms**: T3-02 (ratify the first canonical artifact) failed **three times**. First run: the
worker built the review pack and did the *designed* HITL pause (wrote `needs-decision/`, parked for
David) — the engine's inactivity-timeout misread the idle wait as **wedged** and rebooted it. Resume
runs (decision recorded): the multi-step ratification apply (status flip + `_source` restructure +
rubric table + INDEX + backlog-done + learnings) **never completed in a worker window** →
false-failed → exhausted retries.

**Environment**: dark-factory engine reaping a HITL/ratification war game.

## Root Cause

The engine models only *active* vs *wedged* — it has **no "parked for a human decision" state**. A
worker that correctly stops to wait for David is indistinguishable from a hung one. And the reap gate
demands a single all-checks-pass artifact, but a ratification is a long chain of small edits the
worker can't reliably finish before the timeout — so a genuinely-in-progress apply reads as a fail.

## Solution

None built (engine moratorium — [[ADR-0045]]). Recovery this session: the **PO seat applied the
ratification by hand** (David's recorded decision → `_source` restructure, rubric table, status→
ratified, INDEX, backlog→done, learnings; both inspectors green) and shipped artifact #1. The
HITL/ratification-pipeline gap is recorded as a post-moratorium rebuild target.

## Prevention

A human-in-the-loop step needs first-class engine support: a **park state** the reaper respects (not
inactivity-rebooted), and a **resumable multi-step apply** that isn't gated as one atomic
pass/fail. Until then, HITL/ratification tickets cannot be engine-completed — do them attended or as
seat recovery. Related recurrence: [[job-agents-complete-work-but-skip-writing-handback-run-record]]
(worker skips the final bookkeeping steps of its procedure).
