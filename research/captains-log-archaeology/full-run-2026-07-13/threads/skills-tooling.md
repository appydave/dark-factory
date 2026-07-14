# Thread Timeline — skills-tooling

**Purpose**: 6-month dated narrative of the "skills-tooling" capture thread (77 records, 2026-01-11 → 2026-07-11) — how David's skill/tooling ecosystem thinking started, evolved, split, went dormant, and re-emerged as fleet-level governance.

**For Agents**:
- Use this to understand the lineage of David's skill-building conventions (skill-creator canonical, plugin-hosted skills, descriptive naming).
- Check "Superseded decisions" before acting on any early-2026 capture from this thread.
- Current front of the thread is meta-tooling: skill registry, review-skill evaluation, self-adaptive skills.

---

## Phase 1 — Origin: "I can't remember how to start my own projects" (2026-01-11)

The thread starts on a single day with a single pain: per-project startup commands (npm/bun/docker across FliGen, FliDeck, FliHub, Storyline, SupportSignal) were unmemorable. In one burst David:

- **Scoped the problem** explicitly as plan-first, not implementation — a consistent `start.sh`/"go" command that *echoes* commands while running them, without disturbing his jump system, and wary of heavy third-party tools.
- **Sketched the design**: a single `s` alias delegating to a per-project `start.sh` generated from a standard template (simple → complex), numbered `s1`/`s2` (`t1`/`t2` for test harnesses), run-plus-help behaviour, checked against the jump-folder namespace — and flagged it must be documented centrally in the second brain.
- **Built and validated it** the same day across the voice-agent and SupportSignal multi-service projects (with a note of frustration: Claude wrote files *before* the design was finalized — an early instance of the "don't act before the design is set" theme that recurs all thread).
- **Framed it for teaching**: a universal project starter guide for the Skool community, demoed via Loom (four FliVideo apps on separate ports with PO/dev Claude conversations each), using SupportSignal (BMAD v4) as the complex example. Same capture notes David joining Brian's BMAD team in an ideas/feedback capacity.

The DNA of the whole thread is visible here: small standardized utilities + strict design-before-build + everything documented into the brain + eventually shareable as teaching content.

## Phase 2 — Early forks: voice input and hygiene (2026-01-16 → 2026-02-02)

- **2026-01-16 — ITO voice-input fork.** David scoped a two-app voice-input system modeled on the open-source ITO project (Rust Fn-key mic capture + JS app hitting his Groq Whisper endpoint), insisting on requirements documents first, and questioned whether Rust was even necessary versus pure JavaScript. He issued agent tasks for a technology-validation report and — characteristically — asked the agent to *report, not fix* where the research docs were muddied. This fork does not reappear in the thread; it was effectively parked (voice work later resurfaces via other threads, e.g. OMI/transcription tooling).
- **2026-01-22 — first hygiene capture.** POEM "external consultants" plugin must be renamed to "consultants" with no remnants; `npx poem start` errors; port registry inconsistencies plus a mystery "installation 17689". This is the first appearance of a strand that never leaves the thread: *tooling drift and registry cleanliness*.
- **2026-02-02 — process meta-layer.** Three captures in a day: handover docs must **name the next action** (multiple-options-only handovers leave the next context window paralyzed); decision to start async multi-context orchestration with **Telegram as the only first channel** (option A over strategic-pause-plus-handover); and a question about resuming Claude Code sessions by session code. Skills work is now inseparable from session/handover discipline.

## Phase 3 — Plugin plumbing and Ralphie/ralphy identity (2026-02-21 → 2026-02-28)

- **2026-02-21** — appydave-plugin namespace and alias-wiring failures (OMI skill reload included). David pushed two principles: unit tests belong inside tight code-iteration loops (the IR compiler already had 200+ tests on the other machine), and **project memory alone is enough** — don't duplicate data in both project memory and Claude.
- **2026-02-24** — Ralphie confusion peak: after a "disastrous" conversation in another window, David demanded a check of both the second brain and the plugin for Ralphie's *actual* capabilities. Same day, at 50% context, he directed a clean ralphy campaign handover (open items, exact absolute paths, brain→plugin propagation via the renderer) so a new campaign could launch fresh. Plus an archaeology side-task: recover the cluelessjs gem/NPM package and account details.
- **2026-02-28** — multi-repo automation: confirmed the 00x-numbered subfolders are individual GitHub repos (not a monorepo) and wanted a one-pass commit-and-push script with remote-existence checks. Also griped about Claude Code re-asking folder trust.

## Phase 4 — The March explosion: skills as an ecosystem (2026-03-01 → 2026-03-16)

The busiest stretch of the thread (~30 records). Several sub-threads spin up in parallel and start cross-linking:

**DeckHand / workspace automation (Mar 1–3).** Requirements for a virtual Stream Deck replacement (32-button, 15-button, 3-button pedal, Ajazz, Ecamm scenes) without Elgato software. **Mar 2 decision: the tool is named DeckHand**, covering both Ajazz and Elgato; layout-engine + automation work folded into one workspace-automation brain. Hammerspoon reframed as a general window-layout/automation engine with commissioned deep research. Mar 3 extends it to button-deck automations that launch and position apps per monitor, folded into the agentic OS.

**RADAR + personal-org skills (Mar 3).** The personal-organization skill is **named RADAR** (rejecting "morning brief" and "daily ops" as names while keeping the phrase as an invocation). Same day: cross-machine SSH failures prompt a dedicated skill so Claude reliably remembers it can reach other machines; the todo-brain overview format is designed (core-eight primary view), with the insight that *defining what belongs in the list is itself knowledge to preserve*.

**Ecamm integration skill (Mar 4, + Mar 9).** A self-evolving skill scoped around the ~14 HTTP API endpoints, plist read/write with automatic backup/rewind, and a **UAT log correlating David's manual UI actions with config changes** — he narrated building "web" and "code" scenes specifically as training input. Mar 9 adds pre-commit wrap-up discipline on the virtual-camera work.

**AppyStack as skill substrate (Mar 5, 9, 11).** Signal Studio scaffolded in ~1 hour via AppyStack recipes becomes the flagship demo — but the recipes' invocation mechanism is flagged as undocumented (the README names "recipe" without explaining use). Mar 9 plans existing-folder installs + an ElevenLabs voice recipe. **Mar 11 decision: the globally-installed Mochaccino skill should be deleted and generalized into AppyStack** (superseded later — see below).

**Agent-transparency friction (Mar 5–11).** Ansible playbook SSH'ing into the *local* M4 Mini and stalling 30+ minutes on MLX Whisper; screenshot hotkey binding failing opaquely; and the sharpest one (Mar 11): an agent updated 25 files after asking permission to update one skill — **agents must disclose the scope of their writes**.

**ralphy maturation (Mar 7, 16).** **Decision: abstract Mode 1/2/3 labels are replaced with descriptive workflow names** (requirements, plan, build, extend) — this stuck, and is how ralphy is documented today. Mar 16 asks whether ralphy's autonomous loop should routinely run code-quality/test-quality/architecture audits as a standard, not a local memory quirk — the seed of the later review-skill family.

**Image-renaming skill (Mar 7).** Full scoping (NotebookLM PNG workflow: filter → zero-padded prefix + kebab-case description → move to project folder), with two decisions: the prefix is a **runtime question at invocation, not static config**, and the split two-skill implementation gets consolidated into one. Built with skill-creator — foreshadowing the Mar 30 canonicalization.

**/loop and observability (Mar 12–13).** /loop and /btw demoed to Angela and Ronnie (185 pass / 4 fail / 11 skip e2e run); next day the loop is producing no useful feedback and David asks how to design /loop so it doesn't "do stupid things like emit the same message every iteration."

**Unified app startup (Mar 13).** David requests a researched plan for **one skill/command launching all everyday apps** (FliHub, FliDeck, DeckHand, ThumbRack…) with port-conflict handling, single-instance enforcement, and auto browser open. This is the January `start.sh` idea re-emerging at a higher altitude — per-project shell scripts superseded by an ecosystem-level launcher.

**AngelEye enters the thread (Mar 12, 16).** Skill creation ordered for the AngelEye app; then two "detrimental" reliability failures (650+ sessions vanished after restart; stop-hooks dying when the port is down → **startup scripts must be self-healing**), plus a planned refactoring pass (pagination for 671 sessions, dislikes become small backlog items not ADRs, review agents join the loop periodically). Mar 16 also flags the three new consultant skills as possibly wrongly Codex-oriented — David doesn't want external agents in the loop.

## Phase 5 — Consolidation before the pause (2026-03-30 → 2026-04-06)

- **2026-03-30 — decision: skill-creator is the canonical scaffolding path.** Python scripts live inside the skill, extraction schema moves into skill references, orchestrator-calls-skills noted as a possible future pattern. This closes the "how do skills get made" question opened in March.
- **2026-03-31** — NotebookLM presentation workflow planned (conversation data + brain research → NotebookLM-consumable form → styled presentation).
- **2026-04-01** — housekeeping: the stray `.mochaccino` folder questioned, Mochaccino folder deletion directed, commit/push discipline restated (plugin changes and second-brain knowledge *always* committed and pushed), Hermes added to the technologies list.
- **2026-04-02** — two forward-looking captures: an architecture question on whether omi-fetch/art-fetch are deterministic (shell-invocation of nondeterministic skills is fragile — review before building the next epic), and an **app idea: an agent/skill viewer** visualizing all agents/skills, their arguments, discovery mechanisms, and file dependencies. Dormant seed — germinates in July.
- **2026-04-06 — decision closing the phase:** the jump skill had been quietly modified to *work around* the jump CLI instead of using it, leaving the tool stale. David decided **appydave-tools needs a proper spec with full unit-test coverage before the skill is refactored** onto standardized tooling — and directed Claude to be proactive with exact copy-pasteable commands, paths, and model/agent-team choices.

## DORMANT — 2026-04-06 → 2026-06-13 (~10 weeks)

No captures. (The gap coincides with other threads dominating — travel/DTV, Kybernesis, brand work — the skills ecosystem was in *use* rather than under active redesign.)

## Phase 6 — Re-emergence: evaluating and governing the fleet (2026-06-13 → 2026-07-11)

The thread returns changed in character — less "build me a skill", more "how do I judge, compare, and manage the skills I have":

- **2026-06-13** — quality comparison requested: Anthropic's built-in code review vs David's delivery-review skill — redundant, complementary, or something else?
- **2026-06-14** — two design captures: a **voice-forge skill** producing `voice.md` stored with the brand alongside `design.md`, possibly generalized into per-format skills with voice-drift reflection against newer transcripts; and a directive (agent addressed as Angela) to reverse-engineer the ~2-weeks-earlier README research in Kybernesis Cortex into a repeatable **README skill** (this became `craft-readme`).
- **2026-06-20** — after a video on six agentic loops: a **loop selector/orchestrator skill** that lists, invokes, interviews (grilling-style), critiques the six loops from David's own architecture's perspective, copies them into AppyDave plugins as his own, and documents prompt/identity patterns in the second brain.
- **2026-07-04** — **skill registry design**: track ~1,100 investigated + ~100 in-use skills with last-accessed/staleness, per-skill learnings metadata, rich search, and a detail viewer with high-quality browsing UX. This is the April 2 agent/skill-viewer idea reborn at scale.
- **2026-07-10** — a **self-learning, context-aware formatting skill** for ad-hoc executive-style reporting ("I need this as a table" with no design details), adaptive to conversation context and even time-of-day fatigue — explicitly extending the small-utility-skill pattern (RN rename, BTW prompt builder).
- **2026-07-11** — the delivery-review question returns: how does it differ from the other review skills, and how do you evaluate a skill-creator-built review skill run by a background agent? Plus a plugins catch-up flagged for Thursday.

## Superseded decisions

| Superseded | By | Notes |
|---|---|---|
| Per-project `start.sh` + `s`/`s1`/`s2` alias system (2026-01-11) | Unified app-startup launcher plan (2026-03-13) | Same pain, higher altitude: one skill/command with port-conflict handling, single-instance enforcement, auto browser open. |
| Ralph/ralphy abstract "Mode 1/2/3" labels (pre-2026-03-07) | Descriptive workflow names: requirements, plan, build, extend (2026-03-07) | Stuck — this is ralphy's documented mode set today. |
| Image functionality split across two skills (2026-03-07) | Consolidated single skill with runtime prefix question (2026-03-07) | Same-day correction. |
| Globally-installed Mochaccino skill (pre-2026-03-11) | "Delete and generalize into AppyStack" (2026-03-11) | Itself later superseded in practice — Mochaccino re-emerged as a plugin-hosted design-system orchestrator quartet, not an AppyStack recipe. |
| Ad-hoc / manual skill scaffolding (Jan–Mar) | skill-creator as canonical path (2026-03-30) | Also codified later as "new skills → AppyDave plugin source, not ~/.claude/skills/". |
| Jump skill working around the jump CLI (discovered 2026-04-06) | Spec + full unit tests for appydave-tools first, then refactor skill onto it (2026-04-06) | Anti-drift decision: tooling is source of truth, skills wrap it. |
| Agent/skill viewer app idea (2026-04-02) | Skill registry design (2026-07-04) | Not contradicted — absorbed and expanded (~1,100 skills, staleness, learnings metadata). |
| ITO voice-input two-app plan, Rust + JS (2026-01-16) | Effectively parked | Rust-necessity question never resolved in this thread; voice capture later served by other tooling (OMI/Plaud/transcription threads). |

## Current status (as of 2026-07-13)

**Active — meta-governance phase.** The thread has climbed three altitudes over six months: (1) *per-project convenience scripts* (Jan), (2) *an ecosystem of purpose-built skills with conventions* — skill-creator canonical, plugin-hosted, descriptive naming, disclosed write scope, self-healing startup (Feb–Apr), (3) *fleet governance* — a registry for ~1,100 investigated skills, systematic comparison of overlapping review skills, and self-adaptive skills that learn the user's context (Jun–Jul). Open fronts: skill registry design, delivery-review vs built-in review evaluation, loop selector skill, voice-forge, context-aware formatting skill, and the Thursday plugins catch-up flagged 2026-07-11.
