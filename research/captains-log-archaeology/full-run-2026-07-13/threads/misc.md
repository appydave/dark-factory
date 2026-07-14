# Thread: misc

**Purpose**: 6-month dated narrative for the "misc" thread — 21 records that never cohered into a named project. This is the residue thread: short-lived debugging loops, session-hygiene directives, one-off questions, and ambient life/business context. Its value is not any single loop but the recurring meta-patterns it exposes.

**For Agents**:
- Read this to understand what David's *uncategorised* capture stream looks like over Jan–Jun 2026
- Two durable signals live here: the handover/context-exhaustion pattern and the verify-before-claiming / progress-visibility complaint arc
- Individual loops (Thai numpad, port 5200, test cleanup) are one-shot; do not treat them as active projects

---

## Shape of the thread

"misc" is not one thread — it is the bucket for captures that matched no project thread. Reading it chronologically, four sub-strands emerge and interleave:

1. **Session mechanics** — context exhaustion, handovers, fresh-conversation restarts (Feb 2, Feb 24, Mar 31)
2. **One-shot debugging** — Thai numpad, Postgres lazy-loading, VS Code quit, port 5200, 11MB file limit (Jan–Mar)
3. **Agent trust & visibility** — "verify it works before claiming it does" (Mar 6) escalating to the 89-minute opaque-research complaint (Jun 14)
4. **Ambient personal/business context** — coaching Brandy, client juggling, TIL captures (Mar 12 – Apr 1)

---

## Timeline

### January 2026 — STARTED with a hardware annoyance

**2026-01-11** — The thread opens mid-flow on POEM framework work (refining prompts with the Penny prompt-engineer agent) when David's Thai Magic Keyboard numpad starts emitting Unicode characters instead of digits in iTerm/Claude Code. He wants a programmatic macOS fix; numlock/fn behaviour on the Thai layout is unclear. Classic misc capture: a real blocker, orthogonal to the actual work, never mentioned again. **Status: presumed resolved or worked around — no follow-up in 6 months.**

### February 2026 — the migration cluster (peak density)

**2026-02-02** — Five captures in a single heavy session, all orbiting a large **file migration** project (~24 batches, ~13,000 test files):

- **Direction**: phase one declared complete; docs to be updated (phase two "in progress"), all migrated files sanity-checked, restart in a fresh conversation — context nearly exhausted.
- **Direction**: mid-session housekeeping — capture lessons, re-run a documentation health check after 2–3 hours of doc additions, note **190 failing tests**, verify batches ~1–24 for missed files.
- **Question**: at 10% context, background task vs written handover to paste into a fresh conversation? First explicit appearance of the handover-vs-background dilemma that later becomes a codified preference (paste-inline handovers are now a global rule).
- **Decision** ⭐: test-suite philosophy set — *keep only working tests*: fix failures or delete them with documented intent for future reimplementation; regroup the failure list (four groupings) into a new fix strategy. This is the one durable decision in the thread. No later record contradicts it.
- **Direction**: add the "mustard principles" to a document; delegate best-judgment review of question-three items to the agent.

**2026-02-12** — Fragmentary debugging note: Postgres lazy-loading of RBM (licensing/commands) not working; SQL profiling needed on a bugged-out state in an unnamed project. No next steps captured, no follow-up. **Dead end as recorded.**

**2026-02-24** — Worktree day. Two noise records (merge instruction, spin-up instruction) plus a direction: produce a simple handover so David can take over an interview conversation while worktree items are cleaned up with a "future-relevance-only" focus. The handover pattern recurs — second appearance in three weeks.

### March 2026 — scattered one-shots, first trust friction

**2026-03-01** — Two small questions: VS Code quitting the whole app on file close, and shrinking an 11MB file under a 10MB limit. One-shots, no follow-up.

**2026-03-03** — David tries to recall Ian's mention of running a Java/JavaScript program as an always-on service (not from a terminal) and *wishes his OMI device were connected to a second-brain system* so such details were retrievable. Notable: this frustration predates and motivates the OMI ingestion pipeline that later became real (the archaeology this file belongs to is downstream of exactly that wish). **The loop itself (recalling Ian's pattern) was never closed in this thread.**

**2026-03-06** — First open trust friction: the port-5200 app kept erroring on startup; David demands the exact run command and folder and tells the agent to **verify it works itself before claiming it does**. This is the seed of the verify-before-asserting rule now in global preferences.

**2026-03-12** — Personal: coaching Brandy on turning 20 photos into a slideshow video (numbered folder + FFmpeg, or a drag-and-drop tool via a Claude prompt), and articulating his *suggestive-over-prescriptive* prompting philosophy — give the AI room to be the boss.

**2026-03-13** — Noise (app reply missing).

**2026-03-31** — Business snapshot: juggling a prospective $5,000 engagement (presentation just sent) and a 77,000 THB/month client he is **behind on deliverables for**, while absorbing setup costs (new domain, new AI accounts); one AI agent now running recurring research on autopilot. Same day, a direction to another system's agent: update reports, produce a handover to carry back, **correct its self-identity (it wrongly believed it was Claude)**, explain opening a new session without the item profile. Plus a noise ABN-lookup errand. The handover pattern appears a third time — now cross-system.

### April 2026 — last flickers, then DORMANT

**2026-04-01** — Two unrelated captures: a TIL on a supply-chain attack against a ~100M-weekly-download HTTP library (maintainer account hijack, Trojan gained privileged access in ~1.1s then self-erased), and a UI decision — render the agent lifecycle chain only at top-of-message while loading, arrow marking the current agent. The UI decision belongs to some app (likely AWB-adjacent); it landed in misc for lack of a thread.

**April 2 – June 13** — **Dormant.** Ten weeks with zero misc captures. Either David's capture routing improved (fewer orphans) or the capture volume itself dipped.

### June 2026 — RE-EMERGED on the same old nerve

**2026-06-14** — The thread wakes with the strongest feedback record: an opaque long-running agent research task (89 minutes, unclear what kind of research) — "feels stuck", "shitty experience" — and a demand for a **recurring update loop showing what is going on**. This directly rhymes with 2026-03-06 (verify, don't claim) and closes the arc: the thread's most persistent signal is *agent transparency*, not any technical project.

---

## Splits, merges, superseded decisions

- **No formal splits** — misc is by definition the unsplit residue. But three strands *escaped* it into real homes over the period: the handover pattern (Feb 2 / Feb 24 / Mar 31) is now the codified `handover-pattern` skill + global paste-inline preference; the OMI second-brain wish (Mar 3) became the OMI ingestion pipeline; the progress-visibility demand (Jun 14) aligns with the AngelEye/observability work.
- **Superseded**: the Feb 2 question "background task vs handover?" is effectively superseded by the later global preference — cross-system handovers are pasted inline, never scratchpad/relative paths. The in-the-moment ambivalence resolved into a rule.
- **Not superseded**: the Feb 2 test-suite decision (keep-only-working-tests) still stands; nothing here revisits it.
- **Abandoned/unresolved**: Thai numpad fix, Postgres/RBM lazy-loading profiling, Ian's always-on-service pattern recall, port-5200 app identity — all opened, none closed in-thread.

## Current status (as of 2026-07-13)

Quiet for a month since the Jun 14 flare. The thread's live residue is a single theme — **long-running agent work must be observable and self-verifying** — which has since been absorbed into David's global preferences and observability tooling. The technical one-shots are cold; the March client-deliverables pressure has no update here (settled or moved to a client thread). Expect misc to keep collecting orphans; its main archaeological value is as an early-warning surface for preferences that later get codified.
