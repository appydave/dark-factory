# Requirement — Consolidate comprehend-visualise INTO Mochaccino (restore Shelly's judgment)

**Status:** requirement / merge-point for two divergent conversations · **Date:** 2026-06-09
**Author:** David Cruwys (PO) · **Owner of execution:** ONE window only (see §7 — coordination)
**One line:** Fold the useful parts of `comprehend-visualise` into Mochaccino as a 4th *mode* + restore
**Shelly** as the graphics-warrant gate; demote `comprehend-visualise` to a thin caller + provenance +
run-state recorder; strip all design/render rules out of it.

> **Self-contained.** Build from this doc alone — it has the context, root cause, target architecture,
> exact file moves, paths, and the coordination rules. It exists because two conversations (windows)
> are both touching the same untracked skill files; **this doc is the single source of truth both align
> to. Do not improvise the refactor from a chat — execute this.**

---

## 1. Why this exists (context + the failure)

A taste spec (`docs/david-design-patterns.md`, distilled from 156 of David's rated designs) was wired
into `comprehend-visualise/SKILL.md` as render conditioning. Its lever #1 read **"Draw it as a
DIAGRAM — the #1 love-trigger … not a card-grid; an actual drawn diagram."** A downstream render loop
took that literally and **re-skinned everything into JS-built SVG node-graphs** — abandoning the
varied, reliably-good HTML that is Mochaccino's actual house style, and (reportedly) creating a real
verification/cache/test cost. David never asked for a shape engine. He praised shapes **used sparingly,
where they genuinely made sense** — the *eye for where a shape earns its place*.

**Root cause (precise):** the taste-lever **bypassed Shelly**. Mochaccino's three specialists are
Peter (data), **Shelly (Shape Librarian)**, Mocha (renderer). Deciding *whether* a shape is warranted
and *which* is literally Shelly's job. Hardcoding "always diagram" in render-conditioning **neutered
the one specialist whose purpose is that situated judgment.** The class of error: reading a *feature
correlation* (loved designs happened to contain more SVG, because that content was flow-shaped) as a
*mandate* (Goodhart — don't make a rated feature a maximisation target). Same class of error also
produced the "orient strip on every design" over-stamp (already demoted).

**Corrected understanding (already written into `docs/david-design-patterns.md`):** HTML is the default
and the strength; diagrams are situational and sparing; never maximise `svg`; ~half the love-tier
exemplars use no diagram at all (lexi-profile, layout-28/29, the homepages). The spec is **guidance
Shelly consults, never a rule that replaces her judgment.**

---

## 2. Target architecture

| piece | role after this change |
|---|---|
| **Mochaccino** (`appydave-plugins/appydave/skills/mochaccino`) | the engine **and** the design judgment. Gains a 4th mode (comprehend) and a strengthened Shelly gate. |
| **Peter** | data (unchanged) — target → `.mochaccino/data/NN-*.json` |
| **Shelly** (Shape Librarian) | **the graphics-warrant gate.** Default: NO shape. Add a diagram/shape ONLY where the content is a flow/topology/relationship and it clarifies — sparingly, situated. Consults the taste spec as *guidance*, decides per-design. This is the restored "eye for where". |
| **Mocha** | renderer (unchanged) — renders what Shelly decided; HTML by default, a shape only where Shelly called for one. |
| **comprehend-visualise** (`dark-factory/.claude/skills/comprehend-visualise`) | **demoted to a thin mechanism:** comprehend-a-target → Mochaccino-ready data, **provenance** (`meta.source` = path + commit), and **run-state recording** (success/failure → the register). Holds **NO** design/render rules. |

## 3. The specific changes

### 3.1 Mochaccino — add a 4th mode
- Add **"comprehend → visualise"** to Mochaccino's existing *Use Cases / Modes* section (it already has
  3: UI-mockup, documentation, documentation-validation). Intent = "explain a system/codebase/prose to
  an audience." The comprehend fan-out (codebase → cited model → data) becomes this mode's front of the
  data pipeline. Reuse `comprehend-visualise/comprehend-fanout.workflow.js` (move/own it under
  Mochaccino, or have Mochaccino call it).

### 3.2 Mochaccino/Shelly — restore the graphics-warrant gate
- Shelly's gate must explicitly decide **shape-or-not** first, then which, **sparingly**. Default to
  none. A shape is warranted only when the content is inherently a flow/topology/relationship and a
  drawn diagram clarifies it. **Never convert a working HTML layout wholesale to SVG.**
- The taste spec (`docs/david-design-patterns.md`) is an input Shelly *consults* for judgment, NOT a
  mandate. Carry forward the form-agnostic rules that ARE reliable: disciplined semantic block colour;
  ghost text; **kill orange/amber on brown/beige** (David's #1 documented colour gripe); ease density.

### 3.3 comprehend-visualise — strip design rules, keep mechanism + state
- **Remove** the entire "Render conditioning" section and the diagram levers from
  `comprehend-visualise/SKILL.md`. It must not tell the renderer how to look.
- **Keep:** comprehend-a-target → data; provenance (`meta.source` = target path + commit); dispatch;
  and **recording run success/failure/state** (the `experiments/watchtower-engine/failures/register.jsonl`
  aspect, plus run logs). Its honest job = "call Mochaccino and record what happened."

## 4. Non-negotiables (carry over from Mochaccino)
data-first (no view before real data) · `designs/NN-name/index.html` subfolders · gallery regenerated
each turn (and **make the gallery manifest-driven**, not hand-written — separate papercut, note it) ·
served over http, never `file://` · light-mode primary · provenance on every design · **HTML is the
medium; shapes are sparing annotation placed by Shelly's judgment, never a default or a mandate.**

## 5. Definition of done
- Mochaccino has a working **comprehend** mode (codebase/prose → data → render).
- **Shelly decides shape-or-not per design**, defaulting to none; output is HTML unless a shape is
  genuinely warranted; no wholesale SVG.
- `comprehend-visualise` contains **zero** render/design rules — only call + provenance + run-state.
- The taste spec is referenced as *guidance*, not a maximisation target.
- A re-render of a previously SVG-over-rotated design comes back as proportionate HTML-with-sparing-shape.

## 6. Where things live / reuse
- Mochaccino skill + specialists: `~/dev/ad/appydave-plugins/appydave/skills/{mochaccino,peter,shelly,mocha}/SKILL.md`
- comprehend-visualise: `~/dev/ad/apps/dark-factory/.claude/skills/comprehend-visualise/` (SKILL.md +
  `comprehend-fanout.workflow.js`) — **untracked in git**.
- Taste spec (already corrected): `~/dev/ad/apps/dark-factory/docs/david-design-patterns.md`
- Run-state register: `~/dev/ad/apps/dark-factory/experiments/watchtower-engine/failures/register.jsonl`
- Mochaccino usage patterns: `appydave-plugins/appydave/skills/mochaccino/references/usage-patterns.md`

## 7. ⚠️ Coordination — two divergent windows (read FIRST)
Two conversations are live and both can edit the same **untracked** files (no git safety net):
`comprehend-visualise/SKILL.md`, the Mochaccino skill, `docs/david-design-patterns.md`.
- **FREEZE edits** to those three files in both windows until one executor owns this refactor.
- **This doc is the merge point.** Whoever executes works from it, not from chat improvisation.
- **One executor**, ideally working where Mochaccino lives (`appydave-plugins`). The other window's
  scope shrinks to the comprehend-visualise caller + run-state recorder (§3.3) and must NOT re-add
  design rules or edit the Mochaccino skill / taste spec.
- The taste spec was corrected in *this* (dark-factory) window — treat that file as authoritative; do
  not revert it.

## 8. Open decisions for PO (David)
- comprehend as a **4th mode** vs a small dedicated **graphics-assessor sub-skill** — recommendation:
  4th mode for the front-door + strengthen **Shelly** for the graphics judgment (don't add a new skill;
  Shelly already is that role).
- Retire the standalone `comprehend-visualise` skill entirely, or keep it as the thin caller? —
  recommendation: keep it thin (caller + provenance + state), don't delete; it owns the codebase-
  comprehend + run-state that Mochaccino shouldn't.
- Which window executes.

---

### Paste-ready kickoff (for the executing window)
> Execute `~/dev/ad/apps/dark-factory/backlog/2026-06-09-mochaccino-consolidation-requirement.md`.
> Fold comprehend-visualise into Mochaccino: add a "comprehend" 4th mode, and restore **Shelly** as the
> graphics-warrant gate (default no shape; add one only where content is a flow and it clarifies —
> sparingly; never wholesale SVG). Strip ALL render/design rules out of comprehend-visualise, leaving it
> a thin caller + provenance + run-state recorder. The taste spec
> (`docs/david-design-patterns.md`, already corrected) is guidance Shelly consults, NOT a mandate.
> Work in `appydave-plugins` where Mochaccino lives. Freeze edits to the shared untracked files until
> you own them.

---

## Execution log — Marshall window (2026-06-09)

Executed §3 against the four files. Edits (appydave-plugins tracked = recoverable via git; comprehend-visualise untracked = rewritten clean):

- **`comprehend-visualise/SKILL.md`** — full rewrite to a thin caller: (1) comprehend-a-target → Mochaccino-ready data, (2) provenance `meta.source` = path + commit, (3) run-state recording (register on failure). Removed the entire "Render conditioning" section + diagram levers + render hard-expectations. Holds ZERO design/render rules; hands off to Mochaccino. (§3.3 ✅)
- **`mochaccino/SKILL.md`** — added the **"Comprehend → visualise"** 4th mode to Use Cases/Modes; shape brief now states Shelly runs the shape-or-not gate first, default HTML. (§3.1 ✅)
- **`shelly/SKILL.md`** — added **"Graphics-Warrant Gate (decide shape-or-not FIRST)"** as her lead principle + `get-shape` step 0; default no drawn shape, diagram only for warranted flow/topology, sparingly; taste spec = guidance not mandate; carries the form-agnostic rules (semantic block colour, ghost text, kill orange-on-brown, ease density). (§3.2 ✅)

DoD status: §5 items 1–4 ✅. **Item 5 (proof: re-render a previously SVG-over-rotated design → proportionate HTML-with-sparing-shape) NOT yet run** — pending, so as not to repeat false-verification.

Noted-not-done papercut (§4): the gallery is still hand-written, not manifest-driven. Logged, deferred.

The `comprehend-fanout.workflow.js` was left in place (comprehend-visualise owns the comprehend mechanism); Mochaccino's comprehend mode calls it. Not moved.

**Awaiting:** assessment by the other window; then the proof re-render. Nothing committed.

### Proof result — DoD §5 ✅ (2026-06-09)

Re-rendered cortex through the refactored pipeline (Swagger `q-20260609-cortex-proof`). Shelly's gate made four distinct per-design calls (verified via post-JS DOM + screenshots, not just counts):
- `03-four-memories` (taxonomy) → **HTML, no diagram** ← the key proof signal
- `06-brain-anatomy` (mostly relational) → **HTML-primary + one small organ-swap diagram**
- `02-brain-remembers` (flow) → HTML + sparing flow diagram
- `04-brain-sleeps` (cycle) → HTML + sparing cycle diagram
- orange/yellow-on-brown: 0 refs across all four; ghost text + semantic block colour present.

**appydave-plugins committed:** `7d9eb29` (Mochaccino 4th mode + Shelly gate) on main, pre-commit validation green.
Remaining: comprehend-visualise stays untracked in dark-factory (where it ultimately lives is the open call); gallery-manifest papercut deferred; bookkeeping-skip recurred a 4th time (DF-3).
