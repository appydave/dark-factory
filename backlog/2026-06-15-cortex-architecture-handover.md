# Handover — back to Cortex architecture documents (the simple Mochaccino way)

**Written:** 2026-06-15 · **Purpose:** clean close of a wide-ranging session → fresh window focused ONLY
on **Cortex architecture documents**, rendered as the simple Mochaccino presentation (NOT hyperframes).

---

## Start here next session

We are working on **Cortex architecture documents** — visual/comprehension docs of the Cortex brain,
in the **simple Mochaccino style** (static data-first HTML, served at **http://localhost:7422/designs/**).
The existing 6-design deck is the seed. **Hyperframes is parked — do not pursue it.**

**First decision to settle with David (don't assume):**
1. **Refine/extend the existing "how a brain works" deck**, or **build a new, more structural
   architecture-doc set** (the 7 `@kybernesis/brain-*` packages · contracts vs providers · the 4 DBs ·
   the 5 flows)? The current deck is *audience-positioned* ("how does a brain work?"); "architecture
   documents" may want a more *structural* framing — confirm the audience/positioning first
   (see memory: position-for-audience-not-structure).
2. **Re-comprehend Cortex at current HEAD first.** The deck data was comprehended from commit
   `a129a5d` (~v0.8.2). Cortex is now at **`7db2dce` (v0.12.0-era)** — the architecture has moved on
   (KAD/KBDE adoption, new daemon/remote-agent/watched-folders work). Accurate arch docs need a fresh
   comprehend off current HEAD, not the stale proof data.

---

## The asset (what "the simple Mochaccino presentation" is)

- **Served:** `http://localhost:7422/designs/` (python http.server, pid was 6591; restart per CLAUDE.md
  if down: `cd ~/dev/ad/apps/dark-factory/.mochaccino && nohup python3 -m http.server 7422 ...`).
- **Files:** `.mochaccino/designs/{01-session-journey, 02-brain-remembers, 03-four-memories,
  04-brain-sleeps, 05-dark-factory, 06-brain-anatomy}/index.html` + gallery `index.html`;
  data in `.mochaccino/data/*.json` (MVC: HTML fetches its JSON). **`.mochaccino/` is gitignored.**
- The 4 cortex designs are **02/03/04/06**; `01` (session journey) and `05` (dark-factory) are other topics.

## Cortex source of truth

- **Location:** M4 Mini (Tailscale `100.82.235.39`) `~/dev/kybernesis/cortex` — remote
  `KybernesisAI/cortex`. NOT local on Roamy. Currently at `7db2dce`, `main`, clean, up to date.
- 7 ESM packages `@kybernesis/brain-*` (core, contracts, storage-sqlite, storage-vec, embed-openai,
  llm-claude, testkit); 4 DBs (timeline / entity-graph / sleep / vectors); 5 flows (ingest / recall /
  fact-first recall / sleep cycle / watched-folder ingestion). Kernel depends only on contracts;
  storage/vectors/LLM are swappable providers.
- **Stale comprehension data** from old commit at `experiments/watchtower-engine/proof/cortex/data.json`
  (+ `digest.md`) — re-comprehend rather than reuse.

## Design rules that govern any render

- `docs/david-design-patterns.md` — the **two-layer colour model** (warm brand load-bearing:
  brown `#342d2d`, cream `#faf5ec`/`#f0ebe4`, yellow `#ffde59` anchor; cool semantic green/blue/purple
  ONLY on genuine structure). Diagrams **sparing**, HTML default.
- `tools/design-lint/` — the post-render gate (screenshot → critique vs `RUBRIC.md`). **Must lint the
  index + every page, not just named files** (a lesson from this session).

---

## DONE this session (do not redo)

- **Cortex deck brand-cold FIXED.** Was all-cool / 0 warm anchor (output of the bad v3 ticket that
  ordered "drop the yellow"). Re-rendered (v4) + the gallery index fixed → **5/5 design-lint PASS**
  (02/03/04/06 + index), warm anchor restored. Proof: `tools/design-lint/out/lint-v4/verdicts.json`.
- **brains** repo: committed + pushed (clean & synced).
- **cortex** (M4 Mini) + **KBDE-KyberAgent-Enterprise** (local): pulled, up to date.

## PARKED (explicitly NOT now)

- **Hyperframes presenter PoC** — feasibility proven (keypress talk-through deck works), but David is
  **not pursuing it**. Files kept at `experiments/hyperframes-presentation-poc/` (composition.html,
  presenter.html, FINDINGS.md, proof/); server **killed** (was :7811; re-serve from that dir if ever
  needed). A/B verdict ("adapt hyperframes as a Mochaccino 'deck' output mode") is in FINDINGS.md +
  memory `hyperframes-gate-discipline-vs-design-lint`. Drop unless David reopens it.
- **Repo hygiene debt** (from the machine-wide scan): 16 dirty repos. Notably `v-appydave`
  (82 mod + 61 untracked); set upstream tracking on `beauty-and-joy` (`git push -u origin main` — has a
  remote, no tracking branch) and `deckhand` (no remote at all — at risk); push the 4 clean-but-unpushed
  (`appydave-plugins`, `appyctrl`, `kiros-hq`, `vibedeck`).
- **design-lint improvements** (captured as memories, not built): crawl the whole gallery/index; add an
  objective WCAG contrast check; move the colour check to a **pre-render hard-gate** (the hyperframes
  gate-discipline lesson).

## Open micro-loops on the deck itself

- **Data prose never trimmed** — v4 fixed colour in the *view* layer only; `.mochaccino/data/*.json`
  still carries the dense prose. If the screens read wordy, trim the data (data-first).
- **Untracked session artifacts** in dark-factory: `experiments/hyperframes-presentation-poc/`,
  `experiments/watchtower-engine/{done,reports,runs}/…cortex-brain-v4…`, `tools/design-lint/out/lint-v4/`.
  Decide commit-vs-leave. (`.mochaccino/` deck HTML is gitignored, so the brand fix is NOT in git.)

---

## One-paragraph re-entry prompt (paste to resume)

> Resuming Cortex architecture-document work in dark-factory, simple Mochaccino style (served :7422,
> designs in `.mochaccino/`). Hyperframes is parked. First: decide with David whether to extend the
> existing "how a brain works" deck or build a structural architecture-doc set, and re-comprehend
> Cortex at current HEAD (`7db2dce`, v0.12.0 on M4 Mini `~/dev/kybernesis/cortex`) since the deck data
> is from old `a129a5d`. Govern every render by `docs/david-design-patterns.md` (two-layer colour) and
> lint via `tools/design-lint/` (whole gallery, not just named files).
