# HANDOVER — close the KDD read-gate (ADR-0028)

**Written:** 2026-07-04 (Roamy). **For:** a Dark Factory session on **mac-mini-m4** — this is real
build work, it belongs where actual DF building happens, not on Roamy (the orchestrator machine).
**Status:** not started. Source decision fully specified — read it, don't re-derive the plan.

---

## 0. Read this first

The full decision, context, and rationale already exist:
`~/dev/ad/apps/dark-factory/docs/kdd/decisions/0028-close-the-kdd-lisa-read-gate-the-write-loop-is-built-read-en.md`

Short version: Dark Factory's KDD *write* loop is built and proven (Cortex, KBDE, and — as of
2026-07-04 — Dark Factory itself all have a `docs/kdd/` tree). Nothing *reads* it. A session on this
repo re-derived already-settled facts multiple times in one sitting because there was no gate
forcing a check of existing knowledge before starting new research. That's the gap this closes.

## 1. The recommended sequence (from ADR-0028, don't replan this)

1. **Verify/sync the Lisa plugin on this machine.** ADR-0028 (written 2026-07-03) said mac-mini-m4
   was on `appydave-plugins` v5.4.1, missing Lisa entirely (Roamy had v5.9.0 then, now v5.9.1).
   **Could not verify this remotely from Roamy** (Tailscale SSH timed out, 2026-07-04 — machine may be
   asleep/offline). Check for real: `cat ~/.claude/plugins/installed_plugins.json` and look for
   `appydave@appydave-plugins` version + whether `lisa/SKILL.md` contains "Hard-won doctrine". If
   stale, `/plugin` update it.
2. **KDD bootstrap — done, skip this step.** Dark Factory's own `docs/kdd/` was reconstructed
   2026-07-04 (63 sessions, 41 decisions + ADR-0044 + 45 learnings + 2 patterns). Current HEAD at
   time of writing: `ff446635437f2fe3bf6bceafb02d647556a470bd`. Pull latest before starting.
3. **Build the KBDE brain-MCP read bridge** — an MCP server exposing `k-darkfactory` (this project's
   brain) and `k-brain` (David's broader second-brain) as queryable tools, plus three companion-skill
   gates:
   - **G1 no-query** — don't ask the brain what a local file already answers; check disk first.
   - **G2 citation** — any brain-sourced answer must cite its `source_path`.
   - **G3 negative-result** — search ≥2 phrasings before asserting "nothing is known."
   **Correction, confirmed from the ADR's own text:** this is NOT gated on the KBDE Extension SDK
   handover — "the read channel is an MCP server + hook, not a KBDE extension, so it is buildable
   now." Don't wait on Extension SDK work to start this.
4. **Wire it as an enforced hook** (SessionStart / goal-plan / BA-briefing), not an optional habit.
   ADR-0028 itself leans toward trying **advisory-injection first** (surface the gate's existence,
   don't hard-block) and only hardening to a hard-block if it's still skipped in practice — don't
   jump straight to a hard gate.
5. **Unify the two knowledge stores** — point Cortex's file-as-truth `reconcile()` at `docs/kdd/` as
   a watched folder, so markdown stays the ledger and Cortex indexes it, rather than maintaining two
   separate stores.

## 2. What NOT to do

- Don't re-derive this plan from scratch — ADR-0028's Context/Decision/Alternatives/Consequences
  sections already have the full reasoning, read them.
- Don't treat this as gated on David's KBDE Extension SDK work (see step 3's correction).
- Don't build a hard-block gate first — try advisory-injection, per the ADR's own stated preference.
- Don't batch-ratify the other 41 decisions while you're in `docs/kdd/decisions/` for this — that was
  a deliberate call (see `docs/kdd/ADR-FORMAT-SPEC.md` rollout section): ratify lazily, one at a time,
  only when a specific decision is about to matter. This ticket doesn't change that.

## 3. When picked up

Report back (or leave a status note in this file / a fresh backlog item) on: whether the Lisa plugin
was actually stale on m4, what the MCP bridge ended up looking like, and whether advisory-injection
alone was enough or it needed hardening to a hard-block.

## Key paths

| What | Path |
|---|---|
| Source decision | `~/dev/ad/apps/dark-factory/docs/kdd/decisions/0028-close-the-kdd-lisa-read-gate-the-write-loop-is-built-read-en.md` |
| Dark Factory's own KDD (now exists) | `~/dev/ad/apps/dark-factory/docs/kdd/` |
| DF-ADR format spec (context for the format these decisions are in) | `~/dev/ad/apps/dark-factory/docs/kdd/ADR-FORMAT-SPEC.md` |
| Lisa plugin (source, for version/doctrine check) | `~/dev/ad/appydave-plugins/appydave/skills/lisa/` |
