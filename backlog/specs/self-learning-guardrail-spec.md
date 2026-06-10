# Self-Learning Guardrail — Requirements Spec

> **Status:** Draft spec — no build. Build-technique-agnostic.
> **Ticket:** DF-4 · `q-20260608-selflearning-spec` · experiment `exp-20260608-selflearning`
> **Authored:** 2026-06-08 (Swagger, via `appydave:spec-writer`)
> **Working name:** "the learning-sweep guardrail"

---

## 1. Purpose

Make self-learning **active machinery** rather than a passive directive. The Dark Factory's North Star is "the factory that improves itself" — but that promise is hollow if the learning a session produces **evaporates when the session ends**. This spec defines a mechanism (a skill and/or a Claude Code hook — no cron, Max plan) that **forces a learning sweep** at the moments that matter, so a cold restart loses nothing material.

## 2. Problem Statement

**The trigger is the weak link, not the storage.** The persistence buckets already exist and work well — auto-memory (`MEMORY.md` + per-fact files, loaded every session), `backlog/`, and the brains. What fails is the **act of remembering to persist** at the right moment.

**Evidence (concrete, not hypothetical):** In a single session on **2026-06-08**, recorded rules were violated **3–4 times despite being written down**:
- The "lead with my-take, not question-menus" rule (`lead-with-my-take-not-question-menus.md`) — David has rejected the AskUserQuestion-style menu ~3–4× and it recurred.
- The "don't manage AngelEye / don't hand-perform" class of rule.

This mirrors the **Millwright lesson** (`build-reusable-systems-not-one-offs.md`): a *passive memory* (`use-the-loop-dont-just-talk`) already existed and **did not hold** — so the fix is not another memory file, it is **active machinery** (a skill, e.g. `millwright`) that runs at the decision point. The same logic applies here: passive "remember to persist" guidance has already failed; we need a mechanism that **fires**.

**The litmus test the mechanism must satisfy:** *If David shut the session down right now and restarted, would the next session have everything material it needs?* If no, the sweep must persist before the session is allowed to end.

## 3. Goals

- **G1 — Force the sweep at the right triggers**, not only at the very end of a session.
- **G2 — Close the trigger gap** so that a *correction from David* reliably results in a *persisted artifact* within the same session.
- **G3 — Verify against the litmus** ("would a cold restart lose anything material?") as the sweep's exit condition.
- **G4 — Avoid nagging.** The mechanism must not interrupt flow with low-value prompts; silence when there is nothing material to persist.
- **G5 — Build-technique-agnostic.** This spec defines triggers, procedure, persistence targets, and acceptance — not the implementation. Build comes later.

## 4. Non-Goals

- **NG1 — Not a new persistence store.** Reuse the existing buckets (auto-memory, `MEMORY.md`, `backlog/`, brains). No new database.
- **NG2 — Not cron / scheduled API runs.** Max plan; the only "timer" is event-driven hooks firing in-session ([[no-cron-automation-runs-in-session]]).
- **NG3 — Not a replacement for `millwright` or `marshall`.** This composes with them; it is the *self-learning* guardrail, not the build-side or routing guardrail.
- **NG4 — Not retroactive corpus mining.** It governs the *current* session's learning, not a sweep of historical transcripts.
- **NG5 — Does not pick the build technique.** Hook-vs-skill is an open PO decision (§19).

## 5. Users and Roles

| Role | Relationship to the mechanism |
|------|-------------------------------|
| **David (PO / conductor)** | The source of corrections and the beneficiary of continuity. Must NOT be nagged. Approves persistence with one word when prompted; usually the sweep is silent/automatic. |
| **Marshall (Conductor agent)** | Primary host. Runs the sweep as a sub-routine; surfaces "here's what I persisted" tersely. |
| **Swagger (job-agent)** | Secondary host — a dispatched job can also produce learnings worth persisting (e.g. this ticket). |
| **The next session (cold restart)** | The true consumer. Its completeness is the acceptance bar. |
| **Hook runtime (Claude Code)** | The deterministic enforcer if the mechanism is hook-backed (PreCompact/Stop/SessionEnd/SessionStart). |

## 6. Product Scope

**In scope**
- Detect the four trigger classes and run a sweep.
- A defined sweep procedure (capture → classify → persist → verify).
- Routing each learning to the correct bucket.
- A "nothing material" fast-exit (anti-nag).
- A verification gate using the litmus question.
- Acceptance criteria that are testable in a single session.

**Out of scope (this iteration)**
- The chosen build form (hook vs skill vs combo) — recommended but PO-decided.
- Cross-session deduplication tooling (a `lexi`-style audit) beyond "update don't duplicate."
- Automatic editing of brains content (brains stay a deliberate write).

## 7. Key Concepts / Entities

- **Learning** — a durable, reusable fact/decision/correction/proof produced in-session. Has: *content*, *type* (user | feedback | project | reference, per auto-memory schema), *trigger that surfaced it*, *target bucket*.
- **Trigger** — an event that should cause a sweep (§9).
- **Sweep** — the bounded procedure (§10) that turns candidate learnings into persisted artifacts.
- **Bucket** — a persistence destination (§11).
- **Litmus** — the binary verification: "cold-restart-loses-nothing?" (§10, step 5).
- **Correction** — a special, high-priority learning: David tells the agent it did the wrong thing. The headline failure mode this spec exists to fix.

## 8. Functional Requirements

- **FR1** — The mechanism MUST recognize the four trigger classes in §9 and initiate a sweep on each.
- **FR2** — On a **correction trigger**, the mechanism MUST ensure a corresponding persisted artifact (auto-memory update or new file, or backlog note) exists **before session-end**. A correction that ends the session unpersisted is a defect.
- **FR3** — The sweep MUST classify each candidate learning by type and route it to the correct bucket (§11).
- **FR4** — The sweep MUST prefer **updating an existing** memory/file over creating a duplicate (check by `name`/topic first).
- **FR5** — The sweep MUST run the **litmus verification** and, if it fails, persist the missing items before allowing the session to end / compaction to proceed.
- **FR6** — The mechanism MUST support **silent success**: when there is nothing material, it completes without prompting David (anti-nag, FR-driven by NFR1).
- **FR7** — When persistence requires a judgment David should own, the mechanism MUST surface it as a **terse "my take + go"** prompt (per `lead-with-my-take-not-question-menus`), never an AskUserQuestion menu.
- **FR8** — The mechanism MUST be invokable **on-demand** (e.g. "run the learning sweep") in addition to firing on triggers.
- **FR9** — Each sweep MUST leave a trace (what was persisted + where) so Marshall can surface it in one line and so the action is auditable.
- **FR10** — The mechanism MUST be idempotent across the lifecycle: a Stop-triggered sweep followed by a PreCompact-triggered sweep in the same session MUST NOT double-write the same learning.

## 9. Trigger Requirements

Four trigger classes. The mechanism must cover all four; the *build form* per trigger is an open decision (§19).

| # | Trigger | When | Candidate hook event | Notes |
|---|---------|------|----------------------|-------|
| **T1** | **Milestone** | A decision ratified, a probe proven, a job completed | (in-session, agent-detected; or `TaskCompleted` / `SubagentStop`) | Lightweight checkpoint sweep — "what did this milestone teach?" |
| **T2** | **Correction from David** | David says the agent did the wrong thing / repeats a rule | `UserPromptSubmit` (detect correction language) or agent-detected | **Highest priority.** This is the headline failure mode. Must result in a persisted artifact same-session (FR2). |
| **T3** | **Pre-compaction** | Before context is compacted | `PreCompact` (matcher `manual`/`auto`) | Last chance before context is summarized/lost. `PreCompact` can `block` (exit 2) — so the sweep can run before compaction proceeds. |
| **T4** | **Session-end** | Session terminates | `SessionEnd` (reasons: `clear`/`logout`/`prompt_input_exit`/…) | **Caveat:** `SessionEnd` output is **not processed** (stderr-to-user only) and **cannot block** — so it is a *best-effort flush / reminder*, NOT a hard gate. The hard gate must come earlier (`Stop`/`PreCompact`). |

**Hook capability notes (from the canonical hooks spec, v2.1.167):**
- **`Stop`** fires once per turn-end, **can block** (`decision:"block"` + reason; exit 2) and now supports non-blocking `additionalContext` feedback (v2.1.163). It has an **8-consecutive-block safety cap** (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`). This makes `Stop` the natural place to enforce "don't finish the turn with an unpersisted correction" — but the cap and nag-risk must be respected.
- **`PreCompact`** can block compaction — the right place to force a flush before context loss.
- **`SessionStart`** (matcher `compact`/`resume`/`startup`) can inject `additionalContext` — useful to **re-load** what was persisted and to confirm continuity on the next session (closes the loop / proves the litmus).
- **`SessionEnd`** is observe-only — useful as a final reminder, not a gate.

## 10. Workflow Requirements — The Sweep Procedure

The sweep is a bounded, 5-step procedure:

1. **Capture** — enumerate candidate learnings since the last sweep: corrections received, decisions ratified, probes proven, gotchas discovered. (Scope to the delta, not the whole session — supports FR10 idempotency.)
2. **Filter (anti-nag gate)** — drop anything not *durable + reusable + material*. If nothing survives → **silent exit** (NFR1). This step is what prevents nagging.
3. **Classify & route** — for each survivor, assign type (user/feedback/project/reference) and bucket (§11); prefer updating an existing artifact (FR4).
4. **Persist** — write it. For corrections (T2), this is mandatory before session-end (FR2). Surface a terse "my take + go" only where David must own the call (FR7).
5. **Verify (litmus gate)** — ask: *"If David restarted now, would the next session lose anything material?"* If yes → loop back to step 4 for the missing items. If no → done; record the trace (FR9).

**Marshall sub-routine framing:** Marshall's skill already has a "Self-learning" step; this spec formalizes it into the above 5-step procedure and binds it to the four triggers.

## 11. Data / Persistence Requirements

| Bucket | What goes here | Schema |
|--------|----------------|--------|
| **Auto-memory** (`~/.claude/projects/.../memory/<slug>.md` + `MEMORY.md` pointer) | Cross-session facts/decisions/**feedback/corrections** — the **primary** target for T2 corrections | Frontmatter (`name`, `description`, `metadata.type` ∈ user/feedback/project/reference); body with **Why** + **How to apply**; `[[links]]`; one fact per file. **`MEMORY.md` index updated** with a one-line pointer. |
| **`backlog/`** (+ `build-state.md` if present) | Open work, project state, in-flight decisions | Existing backlog item format. |
| **Brains** (`~/dev/ad/brains/`) | Reusable cross-project knowledge | Deliberate write — brains are not auto-edited; the sweep may *propose* a brain write but flags it for David. |

**Routing rule of thumb:** correction/feedback/decision about *how to work* → auto-memory (feedback type). Project state / open work → backlog. Cross-project reusable knowledge → brains (proposed, not auto-written).

## 12. Business Rules

- **BR1** — A **correction (T2) is never allowed to die unpersisted.** This is the one hard invariant.
- **BR2** — **Update before duplicate.** Check for an existing artifact by `name`/topic before creating a new one (avoids memory-file rot).
- **BR3** — **Don't persist the ephemeral.** Conversation-only details, one-off task mechanics, and anything the repo/git already records are NOT persisted (per the auto-memory contract). If asked to remember such a thing, persist *what was non-obvious about it* instead.
- **BR4** — **No menus.** Any David-facing prompt is "my take + go" prose, never AskUserQuestion (the rule this whole mechanism is partly built to enforce — it must not violate it).
- **BR5** — **Silence is valid.** A sweep that persists nothing is a success, not a skipped step — provided the litmus passes.
- **BR6** — **The litmus is the exit gate**, not "did we write something." Writing zero is fine if nothing material was lost.

## 13. Reporting / Observability Requirements

- **OB1** — Each sweep emits a **one-line trace**: trigger that fired, count + destinations of what was persisted (or "nothing material"). Marshall surfaces this.
- **OB2** — Persistence actions are **auditable** — the artifact itself (memory file / backlog edit) is the record; the trace points to it.
- **OB3** — (Stretch) a running count of *corrections-this-session* vs *corrections-persisted* makes FR2 compliance visible and feeds the tool-usage / self-evolution telemetry line.

## 14. Non-Functional Requirements

- **NFR1 — No nagging.** The dominant failure mode to avoid. Silent on empty sweeps; prompt David only when a judgment is genuinely his (FR7). A mechanism that interrupts flow will be disabled and is worse than nothing.
- **NFR2 — Low latency / non-blocking by default.** Milestone (T1) sweeps run inline and fast; only the correction (T2) and pre-compaction (T3) gates may block, and only when there is a real unpersisted item.
- **NFR3 — Respect the Stop-hook block cap** (8 consecutive blocks). The mechanism must converge — never wedge a session by repeatedly refusing to stop.
- **NFR4 — Deterministic where it matters.** The correction invariant (BR1) should be enforced structurally (hook fails-closed) if hook-backed, not left to model discretion — that is the whole "active machinery" point.
- **NFR5 — Composable** with `marshall` and `millwright`; shares their "my take + go" voice and self-learning framing.
- **NFR6 — Survives compaction correctly.** If any background/monitor element is used, it must follow `monitors-survive-compaction` (don't blind re-arm; track ids) — though a pure hook-based design sidesteps this.
- **NFR7 — Cheap.** Runs on the Max subscription in-session; no API/cron spend.

## 15. Assumptions

- The existing auto-memory + `MEMORY.md` mechanism continues to load every session (the persistence half is healthy).
- Claude Code hooks at v2.1.167+ behave per the canonical spec (`Stop`/`PreCompact` can block; `SessionEnd` cannot; `SessionStart` can inject context).
- Corrections from David are detectable — either by language pattern at `UserPromptSubmit` or by the agent recognizing the moment.
- Marshall is the usual host session; Swaggers are secondary hosts.

## 16. Constraints

- **No cron, no headless API.** In-session, event-driven only (Max plan).
- **`SessionEnd` is observe-only** — cannot be the hard gate; the gate must be `Stop`/`PreCompact`.
- **Stop-hook 8-block cap** bounds how aggressively the turn-end gate can insist.
- **Brains are deliberate writes** — the sweep proposes, does not auto-commit, brain content.
- Must not regress the "no menus" rule it is partly designed to enforce.

## 17. Risks

- **R1 — Nag-induced disablement.** If the mechanism interrupts too often, David turns it off → net negative. Mitigated by NFR1 + the anti-nag filter (step 2).
- **R2 — Block-loop / wedged session.** A Stop/PreCompact gate that always finds "something" could fight the user. Mitigated by NFR3 + a strict materiality filter.
- **R3 — Detection misses.** A correction phrased gently may not trip a language-pattern trigger → the very failure mode persists. Mitigated by combining T2 (live) with T3/T4 (end-of-life backstop sweeps).
- **R4 — Memory-file rot / duplication.** More persistence → more files → more rot. Mitigated by BR2 (update-don't-duplicate) and periodic `lexi`-style audit (out of scope here).
- **R5 — Model-discretion leakage.** If built as skill-discipline only (not a fails-closed hook), it is "yet another passive directive" — exactly what already failed. This is the core PO decision (§19, D1).

## 18. Recommended MVP

**My take (for PO approval):** a **hybrid** — skill for the procedure, one hook for the hard gate.

1. **A `learning-sweep` skill** encoding the 5-step procedure (§10), invokable on-demand and called by Marshall at milestones (T1) and on detected corrections (T2). This is the *judgment* layer.
2. **One `Stop` (and/or `PreCompact`) hook** that fails-closed on the single hard invariant **BR1**: *if a correction was received this turn/session and no corresponding persisted artifact exists, block the stop with a terse reason and run the sweep.* This is the *deterministic* layer that makes the failure mode **impossible**, not merely discouraged — the Millwright principle applied.
3. `SessionStart` (matcher `resume`/`compact`) injects a one-line "continuity confirmed: last session persisted X" to close the loop and prove the litmus on the next boot.

Rationale: the skill alone repeats the passive-memory failure (R5); a hook alone lacks the judgment to classify/route. The hook enforces the one invariant that has empirically broken; the skill does the nuanced rest. Keep the hook's blocking scope **narrow** (corrections only) to respect NFR1/NFR3.

## 19. Open PO Decisions

1. **D1 — Hook-enforced vs skill-discipline (the central call).** Pure skill = composable, no fails-closed guarantee (risks repeating the failure). Pure hook = deterministic but blunt/naggy. **My take: hybrid (§18).** Press go, or pick skill-only / hook-only.
2. **D2 — Which event hosts the hard gate** — `Stop` (per-turn, finer-grained, has block cap) vs `PreCompact` (per-compaction, coarser, no cap) vs both. **My take: `Stop` for the correction invariant + `PreCompact` for the full pre-loss flush.**
3. **D3 — Correction-detection method** — language-pattern at `UserPromptSubmit` (deterministic, brittle) vs agent-recognition (flexible, leaky) vs both. **My take: both — pattern as a backstop, agent as primary.**
4. **D4 — Anti-nag tuning** — how material must a learning be to trigger a David-facing prompt vs silent persist? Define the materiality bar. **My take: silent-persist by default; prompt only for brain-writes and genuine forks.**
5. **D5 — Where the `learning-sweep` skill lives** — standalone skill, a sub-routine inside `marshall`, or a sibling to `millwright`. **My take: a standalone `learning-sweep` skill that `marshall` calls, mirroring how `marshall` calls `millwright`.**

## 20. Acceptance Criteria Summary

Testable, single-session-verifiable:

- **AC1 (the headline)** — Given a session in which David issues a correction, when the session reaches Stop/end, then a corresponding persisted artifact (auto-memory file/update or backlog note) **exists before the session ends**. *(Directly tests FR2/BR1 — the 3–4×-violation failure.)*
- **AC2** — Given a sweep with no material learnings, when it runs, then it **completes silently** with no David-facing prompt and the litmus passes. *(Tests NFR1/BR5.)*
- **AC3** — Given a learning that duplicates an existing memory, when the sweep persists it, then the **existing artifact is updated, not duplicated**. *(Tests BR2/FR4.)*
- **AC4** — Given a `PreCompact` trigger with an unpersisted material learning, when compaction is attempted, then the sweep **runs (and may block) before context is lost**. *(Tests T3/FR5.)*
- **AC5** — Given any David-facing decision the sweep raises, then it is presented as **"my take + go" prose, never an AskUserQuestion menu**. *(Tests BR4/FR7 — the mechanism doesn't violate the rule it enforces.)*
- **AC6** — Given a completed sweep, then a **one-line trace** of trigger + what-persisted-where is available to Marshall. *(Tests OB1/FR9.)*
- **AC7** — Given two triggers fire in one session (e.g. Stop then PreCompact), then the same learning is **not double-written**. *(Tests FR10/idempotency.)*
- **AC8 (litmus)** — Given the sweep reports "done," then a simulated cold restart loses **nothing material** that was learned this session. *(Tests G3/FR5 — the master acceptance bar.)*

---

### Key assumptions made
- Persistence buckets are healthy; only the trigger is broken.
- Hooks behave per the v2.1.167 canonical spec (`Stop`/`PreCompact` block; `SessionEnd` cannot).
- Corrections are detectable in-session by pattern and/or agent recognition.
- Marshall is the primary host and already has a self-learning step to formalize.

### What appears to be missing from the brainstorm
- A concrete **materiality threshold** distinguishing "persist" from "drop" (left as D4).
- A definition of **how a correction is detected** programmatically (left as D3).
- Any **dedup/audit** strategy for the growing memory corpus beyond "update don't duplicate" (deferred to a `lexi`-style tool).
- **Metrics/telemetry** for whether the guardrail actually works over time (touched as OB3, not fully specced).

### The 5 most important decisions the PO still needs to make
1. **Hook-enforced vs skill-discipline vs hybrid** (D1) — the decision that determines whether this repeats the failure it's fixing.
2. **Which hook event hosts the hard gate** — `Stop`, `PreCompact`, or both (D2).
3. **How corrections are detected** — pattern, agent, or both (D3).
4. **The anti-nag materiality bar** — when does the sweep speak vs persist silently (D4).
5. **Where the `learning-sweep` skill lives** and how Marshall invokes it (D5).
