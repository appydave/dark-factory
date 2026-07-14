# Thread: kdd-lisa — KDD (Knowledge-Driven Development) & Lisa the Librarian

**Purpose**: Six-month dated narrative of David's captures on the KDD system and its lifecycle librarian, Lisa — from migration cleanup, through a quality-campaign burst, a 4.5-month dormancy, to the July re-emergence around governance and scope.

**For Agents**:
- Use to understand how KDD/Lisa thinking evolved and which early decisions were later superseded
- Check the "Superseded decisions" section before acting on any pre-July KDD convention
- Current status is at the bottom — July 2026 framing is authoritative

**Records**: 28 | **Span**: 2026-02-02 → 2026-07-07 | **Shape**: burst → burst → burst → dormant (~4.5 months) → re-emergence

---

## Phase 1 — Started: migration cleanup and batch refactoring (2026-02-02)

The thread opens not as "Lisa" but as **KDD housekeeping during a Convex/Cloudflare migration**. Nine records land on a single day:

- **Handover philosophy**: nearing context exhaustion, David decided the handover should carry only the **durable philosophical lessons** taught to the agent — not low-level detail about services being deleted post-migration. Write the handover, don't curate everything.
- **Quick cleanup approved**: move two legacy KDD files, remove the legacy folder; archive/index taxonomy explicitly out of scope (handled elsewhere).
- **Mid-flight audit**: David restricted the KDD migration to converts-related files (not web/CloudWorkers), ordered broken-link fixes, and demanded clarity on archive-vs-historical topology, what indexes are, real completion percentage (85% vs the claimed 100%), and missing content. The "is it really done?" scepticism becomes a thread-long motif.
- **Working method locked in**: option A — **rolling-task management at ~6 hours/day**, batches of ~10 tasks, each ending with a handover (ChatGist docs) into the next session. Two routine end-of-session checks appear here for the first time: "does anything warrant a KDD update?" and "any patterns/learnings to carry forward?" — the ritual that later becomes Lisa's capture job.
- **Compression rule**: documentation answers to open questions get officially recorded with links; replicated data-mesh parts can be compressed to summaries **as long as historical rationale is preserved**, with verification before summarizing.

At this point KDD is a documentation refactor; there is no named librarian.

## Phase 2 — Evolved: librarian gating, broken links, quality campaign (2026-02-10)

Eight days later the thread hardens into **governance + measurable quality**, and "Lisa" appears by name:

- **Librarian gate established**: migration project memory lives with the migration docs themselves; **nothing enters the KDD unless it goes through the librarian**. This supersedes the looser Feb-02 "just write the handover" posture — KDD entry is now gated.
- **First Lisa friction**: a directive-misrecognizing script, confusing task ordering, inconsistent non-descriptive file naming ("memory" files). David's key line: KDD learnings exist precisely so a from-scratch rebuild avoids "this run's clusterfuck."
- **Hard health standard**: 15% or even 5% broken links is unacceptable — target is effectively **100%**, with a background-agent review giving every remaining file an explicit disposition (small review / needs human input / delete / comment out).
- **Lisa reliability problem**: Lisa kept miscounting broken links (~150–155 vs a conflicting 340) and ignored the dedicated system defining which links count — even after a context reload. David wanted to know *why the system failed*, not just corrected numbers.
- **s9 test migration sub-loop**: a 1–3 day quality campaign — old-suite→Jest rewrite with both suites running in parallel (mirroring the prior convex s5/s8 setup), easy-wins audit log, cross-component consistency checks, and a baseline commit whose state survives context-window resets. Frustration followed fast: the S9 suite didn't even start — David expected a runnable baseline he could watch grow, "not endless analysis."
- **Workflow tightening**: delete intermediate broken-links files, print results in-conversation, admit uncertainty instead of guessing, don't patch inherently broken setups; capture session learnings (haiku-vs-open-source comparison, **librarian QC-bot concept**) before the 7%-context handover.
- **Archive classification decision**: archive files can't be blindly excluded from link validation (they document *how* to archive, not archived data) — adopt a **RuboCop-style standardized ignore-comment** the Python tool auto-skips. This supersedes the implicit "skip archives" behavior.
- **Pattern export**: broken-link remediation extended to FliHub, with the pattern documented **so librarians can reuse it** — first sign of KDD methods generalizing across projects.

## Phase 3 — Split toward audit: web-testing migration + full doc audit (2026-02-13)

- **Web-testing knowledge migrated into KDD** with careful hygiene: redirects only in David's planning/learnings directory, originals kept to avoid "context poisoning," the new link-checker script placed in the existing scripts directory, **and the librarian updated to know about it**.
- Background tasks commissioned to find all Ralph Wiggum loop refactor learnings, verify each is genuinely Vitest web-layer (not Convex/Cloudflare), and plan a possible web-layer test folder parallel to the Convex one.
- **Scope discipline against shiny research**: David rejected premature integration of n8n/ComfyUI/Kybernesis research into core architecture ("nine layers" means nothing to him, no system overview exists) — file as standalone research docs, and run a **full documentation audit** first (topology validation, index regeneration, health dashboard).

## Dormancy (2026-02-14 → 2026-07-02, ~4.5 months)

No captures. The February machinery (batches, link campaigns, librarian gating) went quiet — attention moved elsewhere in the ecosystem. When the thread returns, the question is no longer "clean the docs" but "**where does KDD live and who is allowed to write to it**."

## Phase 4 — Re-emerged: home, guardrails, and the bridge problem (2026-07-03 → 2026-07-07)

- **2026-07-03 — KDD home decision**: KDD working/archive files live in a **`.kdd`-style dotfolder inside each project** — explicitly superseding the previously reused Cortex-style location — as an interim until the dedicated KDD home exists. David stressed **Lisa/KDD matters more than Lexi**, asked for a pasteable high-level synopsis, and floated two extensions: OMI-fetch and a KDD at-a-glance inspector (projects, decisions, documents, patterns).
- **2026-07-04 — Lisa guardrails (feedback, angry)**: a single Lisa/KDD learning ballooned into its own branch instead of one learning doc on the working ticket. David demanded a **menuing/deterministic clarification step** — ask the human, check one-off vs pattern, bump learning counts — so the mistake class can't recur.
- **2026-07-04 — KDD bridge triage**: David pinned down what the KDD bridge actually is (a repo/MCP thrown out without visibility), **decided Gemini is broken and must be deprecated out of the system**, set ticket flow (validate-then-close 176, open 192 fresh, defer painful 191), and named the core problem: **"the factory writes knowledge but nothing reads it"** — KDD docs should be read at PR-validation and knowledge-update time. This reframes the whole thread: February optimized writing/cleanliness; July says consumption is the missing half.
- **2026-07-07 — The two-librarian model articulated** (in-person): **Lisa = lifecycle learnings, Lexi = reference**, with a promotion ladder — issues logged per unit of work, promoted to a pattern with real code examples after **three recurrences**, feeding a post-plan verification step against repo history. (The other party mapped it to smart-contract rubrics and agent staking marketplaces — noted, not adopted.)
- **2026-07-07 — Scope boundary set**: David pushed back on customizing Lisa for one repository's quirks — **Lisa's scope is the KDD folder only**, not a repo's general documentation folder or application — and asked what went wrong in the thinking before merging documentation-only work.

## Superseded decisions

| Earlier position | Superseded by |
|---|---|
| Feb-02: capture learnings via ad-hoc end-of-session handover checks | Feb-10: nothing enters KDD except through the librarian (gate) |
| Feb-10: archive folders implicitly excluded from link validation | Feb-10 (same day): archives are how-to docs — RuboCop-style ignore-comments instead of blanket exclusion |
| Pre-Jul: KDD working/archive files in reused Cortex-style location | Jul-03: `.kdd` dotfolder per project (interim until dedicated home) |
| Pre-Jul: Gemini as part of the KDD tooling | Jul-04: Gemini broken — deprecate out of the system |
| Feb framing: KDD success = clean, complete, 100%-linked docs | Jul-04 framing: writing is solved-ish; the gap is **reading** — KDD must be consumed at PR-validation/knowledge-update time |
| Implicit: Lisa adapts to each repo's documentation needs | Jul-07: Lisa's scope is the KDD folder only; per-repo customization rejected |

## Current status (as of 2026-07-13)

Active and strategically elevated ("Lisa/KDD matters more than Lexi"). The conceptual model is now settled — two librarians (Lisa lifecycle / Lexi reference), three-recurrence promotion ladder, `.kdd` per-project dotfolder, KDD-folder-only scope for Lisa — but the operational gaps are open: the deterministic clarification/menuing guardrail for Lisa is demanded but not confirmed built, the dedicated KDD home is still pending, the KDD bridge (repo/MCP) lacks visibility, tickets 176/191/192 are mid-flow, and the "nothing reads the knowledge" consumption loop (KDD read at PR-validation time) is designed but not implemented.
