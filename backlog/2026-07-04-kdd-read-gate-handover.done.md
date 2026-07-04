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

## Status (executed 2026-07-04, mac-mini-m4)

**Step 1 (Lisa plugin):** confirmed stale as suspected at the start of this session —
`~/.claude/plugins/installed_plugins.json` showed `appydave@appydave-plugins` installed at
**v5.1.0**, while `~/dev/ad/appydave-plugins` (the repo) was at HEAD `05b2292` dated 2026-07-04
(v5.9.1). Not fixed by this session directly — but a **concurrent session on this same machine**
ran `/plugin` update + `/reload-plugins` partway through this work (see
`backlog/2026-07-04-loose-ends-ledger.md`, D10 closed, and its own commit `2e49fdb`, landed at the
same wall-clock minute as this work). Reconfirmed just now: `installed_plugins.json` shows
`appydave@appydave-plugins` at **5.9.1**. So by the time this ticket closes, Lisa's doctrine IS what
this machine loads — resolved, just not by this session's own action.

**Step 3 (MCP read bridge) — BUILT.** New app: `~/dev/ad/apps/kdd-bridge/` (git-init'd, local commits
only, not pushed). Stdio MCP server, zero deps, same house pattern as
`spikes/blackboard-mcp/server.mjs`. Four tools: `k_darkfactory_search` / `k_darkfactory_list`
(dark-factory's `docs/kdd/` + `~/dev/ad/brains/dark-factory/`) and `k_brain_search` / `k_brain_list`
(`~/dev/ad/brains/`, excluding restricted `brains/davidcruwys/`). The three gates are baked into the
tool contracts: **G2 (citation)** is structural — every result object carries `source_path`, no code
path can omit it. **G3 (negative-result)** is structural-and-checkable — `queries` takes an array of
phrasings, and the response's `g3` block reports `phrasing_count`/`sufficient`/a note on whether a
"nothing is known" claim is currently justified. **G1 (no-query)** is honestly advisory only — a tool
can't verify what a caller checked before calling it; surfaced via tool descriptions, the `_list`
primitives, and the SessionStart hook (step 4). Smoke-tested via stdio (see below).

**Step 4 (advisory-injection hook) — BUILT, in dark-factory (local commit, not pushed).** Registered
`kdd-bridge` in both `.mcp.json` and `.claude/settings.json` `mcpServers`. Added a `SessionStart` hook
to `.claude/settings.json`, same `echo '{"systemMessage":...}'` style as the existing `PreCompact`
self-learning-sweep hook already in that file — advisory only, matches ADR-0028's own stated
preference ("try advisory-injection first ... only harden to a hard-block if still skipped in
practice"). No hard-block built.

**Step 5 (Cortex unification) — PREPARED, NEEDS ROAMY, not wired.** Investigated
`~/dev/kybernesis/cortex/`: it's a pnpm library, not a running daemon on this machine (no
launchd/pm2 process found). Its own `reconcile()` (`packages/brain-core/src/reconcile.ts`, Spec C) is
explicitly folder-agnostic by design — "the watched-folders manifest is never consulted; the
diskList is the truth." Watching/walking is a HOST concern (a KBDE/KAD daemon or Arcana job) living
outside Cortex; no such live host process or watched-roots config was found on this machine, and
`~/dev/kybernesis/KBDE-KyberAgent-Enterprise/` (a live sibling project with its own SDLC) was
deliberately NOT edited to avoid faking an integration that may not connect to anything real. Full
wiring spec (exact `diskList` builder, where to add the watched-root, the `reconcile()` call) written
to `~/dev/ad/apps/kdd-bridge/docs/cortex-reconcile-wiring.md` for whichever session has confirmed
host-runtime access.

**Smoke-test evidence** (stdio, no Claude needed — full transcript in
`~/dev/ad/apps/kdd-bridge/README.md`):
- `tools/list` → all 4 tools returned with schemas.
- `k_darkfactory_search({queries:["read-gate","Lisa"]})` → `found:true`, 20 results (capped), 57
  files matched, every result with a real absolute `source_path` — **G2 confirmed**.
- `k_brain_search({queries:["xyzzy-nonexistent-term-12345","plugh-also-nonexistent-999"]})` →
  `found:false`, `g3:{phrasing_count:2, sufficient:true, note:"...safe to assert \"nothing is
  known\"..."}` — **G3 confirmed**.
- `k_darkfactory_list({prefix:"kdd/decisions"})` → all 44 decision files listed with `source_path` —
  **G1 primitive confirmed**.

**Commits:**
- `kdd-bridge` (new repo): `bf95539` — "feat: kdd-bridge v0.1 — MCP read gate for ADR-0028" (local
  only, no remote configured/pushed).
- `dark-factory`: `f2bb98b` — "feat(kdd): register kdd-bridge MCP + SessionStart advisory hook
  (ADR-0028 step 4)" (local only — branch is `ahead 1` of `origin/main`, not pushed).

**Honest gaps:** G1 has no real enforcement mechanism, only advisory text in three places — named
plainly in `kdd-bridge/docs/extension-notes.md` rather than glossed over. G3 is checkable but not
enforceable — a calling agent can still ignore a `sufficient:false` note. Step 5 is genuinely
undone, not partially done — no watched-root config was added anywhere, by design, because no live
host to receive it was confirmed. No automated test suite for kdd-bridge, only the manual stdio
smoke test above. Did not batch-ratify any of the other 41 decisions while in `docs/kdd/decisions/`,
per the DON'Ts.

## For Roamy — getting the bridge (2026-07-04, from m4)
The bridge is a SEPARATE repo (github.com/appydave/kdd-bridge, private, pushed at bf95539).
dark-factory's .mcp.json + SessionStart hook reference ~/dev/ad/apps/kdd-bridge/server.mjs —
that path dangles on any machine until cloned:

    gh repo clone appydave/kdd-bridge ~/dev/ad/apps/kdd-bridge

Same convention as the other 2026-07-03/04 micro-apps (omi-fetch, app-registry, project-digest,
kdd-viewer) — each its own private repo under appydave/, cloned to ~/dev/ad/apps/<name>.
Roamy likely wants ALL of them for full parity. No build steps; zero-dependency node/python.
