# Spec — Mocha Lab (Watchtower design-quality & improvement tool)

**Status:** specification (transformed from requirement) · **Author of spec:** Swagger (spec-writer)
**Source requirement:** `backlog/2026-06-08-mocha-lab-requirement.md` (self-contained, 236 lines)
**Working prototype (read-only reference):** `tools/mocha-census/`
**Build:** NOT this job. This document is build-technique-agnostic — Ralphy *or* a Swagger could build it
later. Nothing here recommends, assumes, or starts a build.

> **Legend for tags:** ✅ stated in the requirement · ⚠️ inference (extrapolated beyond the requirement) ·
> ❓ open PO decision (must be answered before/at build time).

---

## 1. Purpose

Promote the throwaway **Mocha Census** prototype into **Mocha Lab** — a first-class, durable visual tool
inside **Watchtower** (the constellation's visual control plane) that:

1. **Screenshots** any set of Mochaccino designs (one machine or both),
2. lets David **rate + label** them (love / good / average + free-text *why*),
3. **exports** those verdicts to a file an agent can read directly, and
4. **feeds** the verdicts back into the design spec (`docs/david-design-patterns.md`) + exemplar pack so
   the factory's design quality keeps improving on its own.

It is one of Dark Factory's **self-learning organs**: it converts David's tacit taste into an explicit,
versioned spec that conditions future design output. ✅

## 2. Problem Statement

The capability already exists but only as a pile of scripts (`tools/mocha-census/`). Two manual seams
stop the learning loop from running itself (✅ §7 of requirement):

- **Ingest seam** — today David copy-pastes a ratings JSON blob from the board back into chat. Brittle,
  manual, and breaks the "agent picks it up" automation.
- **Generator seam** — the distilled spec + exemplar pack are *not* wired into the renderer, so the rules
  are applied by hand instead of conditioning new output automatically.

Secondary problems: census machinery (scan both machines, build a manifest, render a gallery of hundreds)
is **overkill for the everyday case** — "I just generated 5 variants of one idea, rate them." And a
*changed* page is not re-shot automatically (you must hand-delete the old PNG). ✅

## 3. Goals

- **G1** — Make the rate→distill→re-render loop **run itself** by closing both manual seams. ✅
- **G2** — Make **bench mode** (rate N variants of one idea side-by-side) the everyday front door. ✅ priority
- **G3** — Promote the prototype to a **durable, brand-styled tool in Watchtower**, reusing the proven
  Python+Playwright capture engine. ✅
- **G4** — Keep the tool **cheap and safe to re-run repeatedly**, with change-detection so edits re-shoot. ✅
- **G5** — Preserve cross-machine reach (M4 Pro local + M4 Mini over Tailscale) and the validated taste
  rules the tool maintains. ✅

## 4. Non-Goals

- **NG1** — NOT a Mochaccino renderer. Mocha Lab *rates* designs; it does not generate them. (The generator
  seam is *wiring* the spec into the existing renderer, not building a renderer.) ✅
- **NG2** — NOT a build task. No framework/stack is mandated here; build approach is ❓ PO decision (§16). ✅
- **NG3** — NO cron / no paid-API scheduling. In-session loop pattern only (Max plan). ✅
- **NG4** — NOT a replacement for `docs/david-design-patterns.md`; it *maintains* that spec, doesn't supersede it. ✅
- **NG5** — The dropped "shit" tier is **not** reintroduced — broken renders are a separate health signal,
  not a design verdict. ✅

## 5. Users and Roles

| Role | Who | Interaction |
|---|---|---|
| **Rater (primary)** | David | Opens the board, rates love/good/average, types labels, exports a round. ✅ |
| **Distiller (agent)** | A Swagger / Marshall-dispatched agent | Reads the exported round file, updates the spec + exemplars. ✅ |
| **Generator (downstream)** | `frontend-design` / Mochaccino render step | Consumes spec + exemplars to start new designs on-spec. ✅ |
| **Operator** | David or Marshall | Fires a census / bench run (button, CLI, or skill — ❓ §16). ✅ |

## 6. Product Scope

**In scope** ✅
- Two modes on one capture engine: **Census** (discover everything → bulk rate) and **Bench** (N explicit
  designs → side-by-side rate).
- Single-design **quality check** against the spec rules.
- **Export ratings to a file** (no clipboard paste).
- **Re-run with change detection** (mtime-newer → auto re-shoot).
- **Cross-machine** scan + capture (local + SSH/rsync to the Mini), source-machine labelled.
- A documented **distillation step**: rating round → `david-design-patterns.md` + `exemplars.json`.
- Lives **in/with Watchtower**, AppyDave-brand-styled.

**Out of scope (this spec)** — building it; choosing the final home/stack; auto-running on a schedule.

**MVP vs later** ⚠️ (recommended, see §17–18): MVP = bench mode + export-to-file + mtime re-shoot.
Later = census fold-in, single-design quality view, full Watchtower panel, generator wiring.

## 7. Key Concepts / Entities

- **Design** — a Mochaccino page on disk: `<repo>/.mochaccino/designs/<id>/index.html` (+ `data/<id>.json`).
  Some repos use `mochaccino/` (no dot); designs can nest (`designs/components/<name>/index.html`). ✅
- **Shot** — a full-page PNG capture of a design + metadata (`repo`, `design_id`, source machine, mtime). ✅
- **Rating** — `{ design_key, tier: love|good|average, label: <free text>, machine }`. ✅
- **Round** — an exported set of ratings (`out/ratings/round-NN.json`); seeds the next round. ✅
- **Exemplar pack** — `out/ratings/exemplars.json`, the love-tier reference set the spec cites. ✅
- **Design spec** — `docs/david-design-patterns.md`, the distilled, versioned rules (§9 below). ✅
- **Health flag** — clean vs broken render (console error / stuck "Loading…"), kept separate from tier. ✅
- **Bench set** — an explicit list of N design paths (variants of one idea) targeted for side-by-side rating. ✅

## 8. Prototype Reuse Map (exists → reused vs net-new)

Grounded in a read-only inspection of `tools/mocha-census/`. ✅ for "exists"; ⚠️ on reuse/new verdicts.

| Capability | Prototype artifact (exists) | Verdict | Delta needed |
|---|---|---|---|
| Discover designs (local + SSH) | `scan.sh` (25 LOC) | **REUSE** | none functional |
| Dedupe build-copies + cross-machine dupes | `combine.py` (62 LOC) → `out/manifest.json` | **REUSE** | none |
| Screenshot via throwaway per-repo server | `shoot.py` (103 LOC, Playwright+Chromium) | **REUSE + EXTEND** | add **mtime change-detection** (FR-7) |
| Render-health flagging | `check-health.py` (65 LOC) → `health.json` | **REUSE + PROMOTE** | surface as first-class signal in views (FR-2, 3.2) |
| Structural feature extraction | `extract.py` (83 LOC) → `features.json` | **REUSE (distillation aid)** | feeds FR-9, optional |
| Full both-machine flow | `run-full.sh` (29 LOC) | **REUSE** | none |
| Taste board (love/good/average, A/S/D, ←/→, label, filters, copy-JSON) | `out/shots/gallery.html` (237 LOC) | **REUSE UI patterns, REPLACE export** | swap **copy-to-clipboard → write-to-file** (FR-6); add bench/single-design views |
| Rating rounds + exemplar pack | `out/ratings/round-0{1,2,3-result}.json`, `exemplars.json` | **CARRY FORWARD (data)** | seed the new tool from these |
| Distilled spec | `docs/david-design-patterns.md` | **CARRY FORWARD** | the artifact the loop maintains |

**Net-new (not in prototype):** ⚠️
- **Bench mode** side-by-side compare-and-rate view over an explicit N (FR-4). *(planned in prototype, not built.)*
- **Export-to-file** ingest path replacing clipboard (FR-6).
- **mtime-based auto re-shoot** (FR-7). *(known gap, README §Refreshing.)*
- **Single-design quality view** scoring one design against the spec rules (FR-5).
- **Watchtower panel + AppyDave brand chrome** as a durable home (3.5).
- **Generator wiring** of spec+exemplars into the render step (§13, the generator seam).

## 9. Embedded Design Findings (the spec this tool maintains — requirement §5) ✅

These are the *content* Mocha Lab applies and keeps refining; full version in `docs/david-design-patterns.md`.

- **Tier is composition; the recurring flaw is colour.** Structure (diagram-ness, colour-discipline)
  separates *love* from *good*; the single most-repeated complaint, even on loved designs, is a colour failure.
- **#1 fix — NO orange/amber on brown/beige** (13 gripes across all tiers). Orange only as a small
  highlight; never text-on-brown or filled boxes on beige. Lead with green/blue/purple semantic blocks.
- **LOVE triggers:** (1) diagram/flow — SVG connectors, a **legend** strip, input/output header
  (love svg≈3.5 vs good 0.6); (2) disciplined semantic block colour — **fewer** colours used meaningfully
  (love ≈13 distinct vs 19), alternating cream/dark-brown section bands + per-block accent; (3) **ghost
  text** — oversized tone-on-tone background lettering (his signature); (4) uniqueness / asymmetry / randomness.
- **Connectors: colour belongs in the blocks, not the lines.** Keep lanes/tiles coloured; connector lines
  thin and neutral with small colour-dots at endpoints. Bold coloured curves are one step too much.
- **Caps at good (never love):** off-brand palette; competent-but-flat (no diagram, no colour-blocking).
  **Average:** thin card-sprawl, no diagram.
- **Soft dings:** busy/dense; too much dark brown; childish icons.
- **Always separate broken renders from design verdicts.**

**Methodology rule (load-bearing):** David's tiers **drift between sessions** (round-02 had 47 "love"s;
round-03 had 1 — he rates "love" comparatively). **Anchor learning on the labels and relative ordering,
NOT on absolute tier counts.** ✅

## 10. Functional Requirements (testable)

Carried verbatim-in-intent from requirement §4, with acceptance criteria added. ✅

| ID | Requirement | Acceptance criterion (testable) |
|---|---|---|
| **FR-1** | **Capture** — given a target (all-machines, one repo, or an explicit list of design paths), produce a full-page PNG per design via a throwaway local server. | A run against each target type yields one PNG per discovered design; `ps`/port-scan after the run shows **no leftover capture server**. |
| **FR-2** | **Health** — flag each captured design clean / broken (console error or stuck loading). | Each shot carries a `health: clean\|broken` field; a deliberately broken page is flagged `broken` and is **not** ratable as a design tier. |
| **FR-3** | **Census view** — contact sheet of all captures with per-design rating + label + filters. | Board renders all shots; repo + rating filters narrow the set; rating/label persist locally. |
| **FR-4** | **Bench view** — side-by-side comparison of N chosen designs/variants with the same rate+label controls. | Given an explicit list of N paths, the view shows them **adjacent** for direct comparison; each can be rated/labelled; a round file is written. *(priority — §2 G2)* |
| **FR-5** | **Single-design quality view** — score one design against the spec rules; show pass/flags. | For one design, the view lists which §9 rules pass/flag (at minimum the colour and diagram checks). ⚠️ scoring method is inference. |
| **FR-6** | **Ratings persist locally, seed from the prior round, and EXPORT TO A FILE** (no paste). | After rating, an action writes `out/ratings/round-NN.json` to disk (not clipboard); a fresh board session pre-loads the latest round; an agent can read the file with **no human paste step**. *(priority — §2 G1)* |
| **FR-7** | **Re-run only shoots new OR changed (mtime-newer) designs.** | Editing a design's source so its mtime > its PNG's mtime causes the next run to **auto re-shoot** that design only; unchanged designs are skipped. |
| **FR-8** | **Cross-machine** scan + capture (local + SSH/rsync to the Mini), source-machine labelled. | A both-machine run captures Mini-only designs; each shot records its **source machine**; ~122 dual-resident designs shoot the **freshest** mtime. |
| **FR-9** | **Distillation step** turns a rating round into updates to `david-design-patterns.md` + `exemplars.json` (agent-assisted OK; the round file is the input). | Given a round file, a documented procedure (agent or script) produces a diff to the spec + exemplar pack traceable to specific labels. |
| **FR-10** | Runs under Max plan with **no cron / no API scheduling** (in-session only). | No cron entry, no `claude -p`, no paid-API scheduler is introduced; any recurrence uses the in-session loop pattern. |

## 11. Workflow Requirements

- **Bench loop (everyday, priority):** operator names N design paths → capture (FR-1) → side-by-side view
  (FR-4) → David rates A/S/D + labels → export round (FR-6) → regenerate variants → repeat. ✅
- **Census loop (breadth):** scan both machines (FR-8) → manifest/dedupe → contact sheet (FR-3) → bulk rate
  → export round (FR-6) → distill (FR-9). ✅
- **Quality-gate on a render:** factory renders a Mochaccino → single-design quality view (FR-5) shows
  pass/flags against §9 → accept or re-render. ✅
- **Self-learning loop (target, fully closed):** `render → rate+label → distill to spec (FR-9) → spec +
  exemplars condition the generator (§13) → re-render on-spec → re-rate`. ✅

## 12. Data / Information Requirements

- **Round file** (`out/ratings/round-NN.json`) — array of `{design_key, tier, label, machine, health}`;
  written by the board, read by the distiller. The **canonical ingest artifact** (FR-6). ✅
- **Exemplar pack** (`out/ratings/exemplars.json`) — love-tier references the spec cites. ✅
- **Shot index** (`shots.json`) — `{repo, design_id, png_path, machine, src_mtime, shot_mtime, health}`;
  `src_mtime` vs `shot_mtime` drives FR-7. ⚠️ field names inferred from prototype shape.
- **Manifest** (`out/manifest.json`) — deduped design inventory across machines. ✅
- **Design spec** (`docs/david-design-patterns.md`) — versioned; rounds append rules, never silently overwrite. ⚠️

## 13. Generator-Seam Requirement (the second seam — requirement §7.2) ✅

The spec + exemplar pack must be **wired into the render step** (`frontend-design` / Mochaccino) so new
designs **start on-spec** rather than having rules applied by hand. Acceptance: a fresh render references
`david-design-patterns.md` + `exemplars.json` as conditioning input, and a re-render of a known-good case
reproduces the proven uplift (`05-dark-factory` good → `05-dark-factory-v2` love) without manual rule
application. ⚠️ exact wiring mechanism is a build-time decision; this spec only states the requirement.

## 14. Non-Functional Requirements ✅

- **NFR-1** No persistent per-page servers — ephemeral capture servers only; **one** viewer server is fine.
- **NFR-2** Max plan, **in-session automation only** — never cron or paid-API scheduling.
- **NFR-3** **AppyDave brand** for the tool's own UI (warm browns/cream, yellow highlight, Bebas/Oswald/Roboto)
  — and the UI must **obey its own §9 rules** (no orange-on-brown, etc.).
- **NFR-4** Self-contained capture engine — Python 3 + Playwright + Chromium (already installed on M4 Pro;
  `~/Library/Caches/ms-playwright`). Watchtower UI may wrap it.
- **NFR-5** Cheap to re-run; **safe to run repeatedly** (idempotent capture, no destructive overwrite of rounds).
- **NFR-6** **Pick a free port** — 7440 (prototype board), 7422 (dark-factory `.mochaccino`), 7420
  (canonical gallery) are taken.
- **NFR-7** Cross-machine via **Tailscale IP** `davidcruwys@100.82.235.39` — never `.local`.

## 15. Assumptions ✅⚠️

- ✅ The proven Python+Playwright engine is kept; the new UI sits on top (requirement §9 recommendation).
- ✅ Pages remain static HTML on disk that `fetch` their own JSON (hence the throwaway-server requirement).
- ⚠️ "Single-design quality view" scoring is at least partly automated (feature-extraction + rule checks);
  full automation of taste judgement is **not** assumed — David still rates.
- ⚠️ The distillation step (FR-9) may stay agent-assisted (a Swagger reads the round and edits the spec)
  rather than fully scripted, at least at MVP.
- ⚠️ Watchtower can host/wrap a Python engine (it's Ralphy-built; mechanism is a build concern).

## 16. Open PO Decisions (surfaced, not buried — requirement §9) ❓

1. **Name** ❓ — "Mocha Lab"? "Design Bench"? "Taste Lab"?
2. **Home** ❓ — a panel *inside* Watchtower, or a standalone Watchtower-adjacent app sharing its shell?
3. **Build approach** ❓ — keep the Python+Playwright engine + add a Watchtower UI over it, *or* rebuild
   capture in Watchtower's own stack? (Requirement *recommends* keeping the proven engine.)
4. **How "bench" is fired** ❓ — a Watchtower button ("rate these N"), a CLI, or a skill (`/bench`,
   `/census`) Marshall can invoke?
5. **Build technique** ❓ ⚠️ — Ralphy campaign vs a dispatched Swagger job (explicitly deferred — not this job).

## 17. Recommended MVP ⚠️

Smallest slice that closes the highest-value seam and proves the everyday loop:

1. **Bench mode** (FR-4) over an explicit list of N paths — highest daily value.
2. **Export-to-file** (FR-6) — kills the copy-paste seam.
3. **mtime auto re-shoot** (FR-7) — makes iteration painless.

Prove it on 5 variants of one idea, end-to-end (capture → side-by-side rate → round file on disk → agent reads it).

## 18. Future Enhancements ⚠️

- Fold in **census mode** (the existing breadth flow) and **cross-machine** capture polish (FR-3, FR-8).
- **Single-design quality view** (FR-5) as a render gate.
- **Watchtower panel + brand chrome** (3.5) as the durable home.
- **Generator wiring** (§13) to fully close the self-learning loop.
- Surface **cross-machine mtime divergence** as a visible drift signal (requirement §3.7).

## 19. Risks ⚠️

- **R1 — Taste drift mistaken for signal.** Absolute tier counts swing between sessions; anchoring the
  distiller on counts (not labels/ordering) would corrupt the spec. *Mitigation:* FR-9 keys on labels +
  relative order (the §9 methodology rule).
- **R2 — Broken renders polluting verdicts.** A data-wiring bug read as "bad design." *Mitigation:* FR-2
  health flag, kept strictly separate from tier.
- **R3 — Server leaks.** Throwaway capture servers not torn down → port/process leak (a standing Dark
  Factory quality bar). *Mitigation:* FR-1 acceptance asserts clean teardown.
- **R4 — Cross-machine staleness.** Shooting the stale copy of a dual-resident design. *Mitigation:* FR-8
  shoots freshest mtime + labels source machine.
- **R5 — Generator seam left open.** If §13 is skipped, the loop still needs manual rule application and
  isn't truly self-learning. *Mitigation:* tracked as an explicit FR/requirement, not an afterthought.

## 20. Acceptance Criteria Summary (Definition of Done — requirement §10) ✅

- [ ] **Census AND bench** modes work; bench does side-by-side rating of an explicit N. (FR-3, FR-4)
- [ ] **Single-design quality check** against the spec works. (FR-5)
- [ ] Ratings **export to a file** (no copy-paste); a round file can be ingested by an agent. (FR-6)
- [ ] Re-run **auto re-shoots changed** designs (mtime). (FR-7)
- [ ] **Cross-machine** capture works (both Macs). (FR-8)
- [ ] Lives **in/with Watchtower**, brand-styled, **no persistent per-page servers, no cron**. (NFR-1/2/3)
- [ ] A documented path exists **rating round → spec/exemplar update → next render on-spec**. (FR-9, §13)

---

### Key assumptions made

- The proven Python+Playwright capture engine is retained; the new tool is UI-on-top, not a rewrite. ⚠️
- David remains the human rater; automation handles capture, persistence, ingest, and distillation aids — not taste itself. ⚠️
- Distillation (FR-9) can be agent-assisted at MVP rather than fully scripted. ⚠️
- Watchtower can host or wrap a Python engine. ⚠️

### What appears to be missing from the requirement (gaps to resolve at build time)

- **Exact scoring method for the single-design quality view** (FR-5) — rule-by-rule automated check vs
  human-assisted checklist is unspecified. ⚠️
- **Round-file schema is not formally defined** — fields inferred from prototype shape; should be pinned before build. ⚠️
- **Spec-update governance** — how rule edits are versioned/approved in `david-design-patterns.md` (append
  vs overwrite, who ratifies) is unstated. ⚠️
- **Generator-wiring mechanism** (§13) — *that* it must happen is clear; *how* it hooks into `frontend-design`/Mochaccino is not. ⚠️

### The 5 most important decisions the PO still needs to make

1. **Name** the tool (Mocha Lab / Design Bench / Taste Lab). ❓
2. **Home** — Watchtower panel vs standalone Watchtower-adjacent app. ❓
3. **Build approach** — keep Python engine + UI-on-top vs rebuild capture in Watchtower's stack. ❓
4. **Bench trigger** — Watchtower button vs CLI vs Marshall-invokable skill (`/bench`, `/census`). ❓
5. **Build technique** — Ralphy campaign vs dispatched Swagger (deferred; not this job). ❓ ⚠️

---

**Headline:** 10 functional requirements (FR-1…FR-10) + generator-seam requirement (§13); 5 open PO
decisions (§16). MVP = bench mode + export-to-file + mtime re-shoot. Build is a separate later decision.
