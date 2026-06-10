# Capture Service — design brief (a proposed 5th constellation tool)

**Status**: 2026-06-10 — DRAFT for decision. A *brief*, not a build. Slots alongside
`docs/dark-factory-constellation.md` (read that first for the constellation shape and the
read-vs-control rule). Cross-links: `tools/design-lint/README.md`, `tools/mocha-census/`.

> **The one-sentence frame.** Screenshotting a rendered HTML page has become a *recurring*
> floor primitive (mocha-census, slide decks, design-lint, future render loops), and it is
> re-implemented four times with drift. This brief proposes an always-on **Capture** service
> with a warm browser and one MCP contract — so every caller TALKS to it instead of
> re-vendoring Playwright. Whether it's a new app or folds into an existing tool is **David's
> call**; this brief recommends but does not decide.

---

## 1. Problem — four scripts, one cold-start dance, copy-paste drift

Today four scripts each carry the *same* boilerplate to take a screenshot. Verbatim, they all:

- launch Chromium via Playwright (`pw.chromium.launch()`),
- spin up a **throwaway HTTP server** so relative `fetch()`es resolve
  (`ThreadingHTTPServer(("127.0.0.1", 0), …)` rooted at the page's directory),
- set a viewport + `device_scale_factor=1`,
- decide full-page vs fixed,
- write a PNG with its own ad-hoc naming,
- tear it all down.

The `serve()` helper is **copy-pasted nearly identically** in all four files
(`shoot.py:40-44`, `shoot-slides.py:85-89`, `check-health.py:23-27`,
`shoot-one.py:19-23`). That's the tell: it's a shared primitive masquerading as four
private helpers.

**The drift is already real:**

| Concern | shoot.py | shoot-slides.py | shoot-one.py | check-health.py |
|---|---|---|---|---|
| full-page decision | always `full_page=True` (`:84`) | **heuristic** — `full = doc_h > height*1.6` (`:153-154`) | `--full` flag, default fixed (`:36,57`) | n/a (reads body text) |
| naming | `{repo}__{id}.png` (`:80`) | `{corpus}__{slug}.png` (`:145`) | `stem_for()` last-80-char slug (`:25-28,45`) | n/a |
| settle wait | `350ms` (`:83`) | `400ms` (`:149`) | `350ms` (`:56`) | `300ms` (`check-health.py:47`) |
| dedup | by `(repo,id)` in `shots.json` (`:66,77`) | by `(corpus,slug)` (`:114,143`) | **none** (re-shoots every call) | n/a |
| broken-render detection | none | none | none | **its own** regex + console-error logic (`:29,51-52`) |

Concrete drift to name out loud:

- **shoot-slides.py grew a full-page-fallback heuristic** (`doc_h > args.height * 1.6` →
  `full_page`) that **shoot-one.py lacks** — the design-lint shooter has no equivalent, so a
  page that overflows the viewport is silently clipped there but captured whole in the slide
  shooter. Same job, two behaviours.
- **Each invents its own `out/<…>__<slug>.png` naming** — `repo__id`, `corpus__slug`,
  `stem_for()`'s `[-80:]` truncation. No shared convention; sidecars (`shots.json`) are
  per-tool and incompatible.
- **check-health.py re-implements broken-render detection from scratch** —
  `BAD = re.compile(r"failed to load|unexpected token|…")` over `inner_text("body")` plus a
  console-error listener (`pg.on("console", …)`), and a `stuck` "Loading…" heuristic. None of
  the *shooters* know whether the PNG they just wrote is a broken render; that knowledge lives
  only in a fourth, separate script that re-loads everything.

**The per-call tax.** Every invocation pays a fresh `pw.chromium.launch()` — Chromium cold
start is **hundreds of ms to a couple of seconds** before a single pixel is captured. For
one-shots that's tolerable; for the design-lint **batch audit** (mode B, fan-out over a whole
deck) and a hoped-for **inline per-render lint gate** that "should feel instant"
(`tools/design-lint/README.md`), it's the dominant cost and the thing that makes the loop feel
sluggish.

---

## 2. Proposal — an always-on Capture service with a warm browser

One small service that:

- holds a **warm Chromium** (launched once, reused per call — no cold start),
- owns the **serve-dir-so-fetch-resolves** trick as a first-class option,
- exposes **one MCP contract** any caller reaches: a Claude session, a Swagger, the
  design-lint agent, Mochaccino/Shelly's render step.

The four `shoot*` scripts become **thin clients** of this contract instead of re-vendoring
Playwright. This is the constellation's "talk-to tool" shape (§2 of the constellation doc) —
single-responsibility, MCP-talkable — not a library everyone re-imports.

---

## 3. What it buys

**(a) Warm browser — no cold start. The biggest win.** The batch audit fans out over N pages;
today each spawn (or each `shoot-one` call) re-launches Chromium. A warm browser turns
per-page capture into a `goto` + `screenshot`, making the inline lint gate feel instant and the
batch run drop the launch tax to *once, ever*.

**(b) One contract reachable everywhere via MCP.** Not a re-vendored Playwright snippet in
every tool. Any session/Swagger/agent calls the same `capture(...)`. The drift table above
collapses to one implementation with one set of defaults.

**(c) The concepts built in are the real value — not the screenshot itself.** A PNG is trivial;
what's valuable is the accumulated know-how currently scattered across four files, made
first-class and shared:

- **regions / clipping** — capture a CSS-selector or pixel region, not just full-page/fixed.
- **named save destinations + conventions** — one naming scheme the service owns, replacing
  three ad-hoc ones.
- **serve-dir-so-fetch-resolves** as a *first-class option* — the throwaway-server trick every
  script needs, provided once.
- **viewport / device-scale presets** — `1280×900`, `1600×900` (16:9 slide), retina `2×`, etc.,
  named instead of magic numbers re-typed per call.
- **dedup-by-mtime** — a known census gap. Today dedup is "have I seen this `(repo,id)` key";
  it never re-shoots a *changed* page. mtime-aware dedup ("source newer than PNG → re-shoot")
  is the correct rule and belongs in the service.
- **broken-render detection** — absorb what `check-health.py` does separately (console errors,
  `Failed to load`, stuck `Loading…`) so a capture can return *"PNG written **and** it rendered
  clean / it's broken"* in one call, instead of a fourth script re-loading everything.

---

## 4. Where it fits in the constellation

The existing constellation is four single-responsibility, MCP-talkable tools other tools talk
to (per `docs/dark-factory-constellation.md`): **Watchtower** (visual control plane),
**AngelEye** (Claude Code session telemetry, read-only), **Switchboard** (comms + state bus),
**AppyRadar** (read-only machine/fleet resource intelligence — *the corrected name for what the
older docs called "AppyCtrl"*). Capture is the natural **5th**: a small, read-only-ish
mechanical service that *produces an artifact on request*.

**It pairs cleanly with design-lint — and the split is already drawn.**
`tools/design-lint/README.md` already names the two halves:

- **Capture = the mechanical half** — serve the page, warm-shoot the PNG. (Today: `shoot-one.py`.)
- **Lint = the judgment half** — a vision agent applies `RUBRIC.md` to the PNG. (Stays an agent;
  vision/judgment, never the service's job.)

A capture service makes that separation crisp: design-lint stops carrying its own shooter and
just *calls* Capture, then runs the lint agent on the returned path. Same for the others:

- `shoot.py` → calls Capture per design (`full_page`, `serve_dir`, census naming).
- `shoot-slides.py` → calls Capture per slide (16:9 preset, the overflow heuristic becomes a
  service default everyone shares, not a private fork).
- `shoot-one.py` → essentially *is* a 1-line client of `capture(...)`.
- `check-health.py` → its broken-render logic becomes Capture's optional health return; the
  script shrinks to "ask Capture, with health on."

---

## 5. The decision — KEEP OPEN (recommendation below)

**New standalone Capture app** vs **fold into an existing tool** (most plausibly **AppyRadar**,
since it's the closest existing single-responsibility service, or a tiny capability inside
design-lint/mocha-census). This is **David's call** — the brief lays it out, doesn't pre-pick.

| Dimension | New standalone "Capture" | Fold into AppyRadar | Fold into design-lint / mocha-census |
|---|---|---|---|
| **Ownership** | clean SRP — "capture a rendered page" | muddies AppyRadar's *read-only fleet intelligence* identity (already fighting identity drift per constellation §6) | re-creates the drift we're removing — one tool owns it, others re-vendor again |
| **Liveness burden** | +1 always-on service to keep alive **and observe** (same class as Switchboard/AngelEye) | reuses an already-always-on host; no *new* daemon | none new, but no warm-browser win either (back to per-call launch) |
| **Discoverability** | a named MCP tool everyone finds | hidden under a fleet-intel tool — surprising place to look for "screenshot" | hidden in a lint/census tool — not obviously shared |
| **Blast radius** | a crash kills *only* capture | a capture crash could take down fleet monitoring — bad coupling | a crash is local, but no shared warm browser to crash anyway |
| **Naming coherence** | "Capture" reads exactly as what it does; clean constellation slot | AppyRadar = *sense the machines*; screenshotting a localhost page is not that | "design-lint owns screenshots for slides too" reads wrong |

**Recommendation (David's to ratify): a NEW, deliberately tiny standalone Capture service.**
Reasons: (1) the warm-browser win — the single biggest payoff — *requires* a long-lived owner,
which the fold-into-a-script option can't give; (2) AppyRadar is explicitly the *read-only
sensor* plane and is already battling identity drift (constellation §6.2) — bolting an
artifact-producing browser onto it repeats exactly the mistake of accreting process-polling into
Switchboard; (3) "Capture" is the most honest name and the cleanest SRP slot. The cost is one
more thing to keep alive — accept it *only* because screenshotting is now genuinely recurring
(see §7).

If David would rather not add a 5th always-on service yet, the honest fallback is **a shared
`capture` library + thin warm-browser daemon co-located on whichever host already runs the
render loop**, promoted to a full constellation tool once it earns its keep — but note that a
mere library does **not** buy the warm browser, which is the whole point.

---

## 6. MVP scope

Reusable core only: **warm browser + serve-dir + viewport/region + named save.** Defer the rest.

**v1 — the minimal MCP contract**

```
capture(
  target,                 # html file path OR http(s) URL
  viewport?  = "1280x900" | "1600x900" | preset-name,
  region?    = null,      # CSS selector or {x,y,w,h}; null = whole page
  full_page? = "auto",    # true | false | "auto" (the shared overflow heuristic)
  serve_dir? = "auto",    # serve the file's dir so relative fetches resolve; "auto" for file paths
  save_as?   = null,      # explicit path; else service's naming convention
) -> { path, width, height, full_page, served }

health() -> { alive, browser_up, uptime, last_capture_at }   # liveness probe
```

`health()` is the liveness/staleness probe Marshall/Watchtower can poll — table stakes for any
always-on service (per the read-vs-control rule: it *reports*, it doesn't act).

**v2 — earn-its-keep layer (explicitly deferred):**
- **regions / fine clipping** beyond simple selector.
- **broken-render / health-of-the-render detection** (absorb `check-health.py`) returned inline
  with the capture.
- **dedup-by-mtime** as a service-owned default.
- device-scale/retina presets, batch endpoint for fan-out.

Build v1, let the design-lint loop and mocha-census refresh actually use it, *then* add v2.

---

## 7. Honest cautions

- **It's a new always-on service to keep alive AND observe.** Same liveness/staleness class as
  Switchboard and AngelEye — it needs a `health()` probe, and Marshall/Watchtower need to notice
  when it's dead or stale (constellation §4, the read-vs-control rule). Adding a 5th daemon is
  not free.
- **Justified ONLY because screenshotting is now genuinely recurring** — across mocha-census,
  slide capture, design-lint (inline gate + batch audit), and future render loops. If it were
  one caller, a shared function would do. Four callers with live drift is the threshold.
- **Don't over-build v1.** Resist shipping regions, health-detection, dedup, and presets on day
  one. Warm browser + serve-dir + viewport + named save is the whole MVP. Everything else waits
  for a real second caller to ask for it (the round-04 Goodhart lesson: build to need, not to a
  feature checklist).
- **Keep judgment out of it.** Capture is mechanical only. The *lint verdict* stays a vision
  agent (design-lint). The service must never grow a "is this on-brand?" opinion.

---

## 8. Migration sketch

Concrete collapse, once v1 exists:

| Script | Becomes |
|---|---|
| `tools/design-lint/shoot-one.py` | a ~1-line client: `capture(target, full_page=…, save_as=out/lint/…)` |
| `tools/mocha-census/shoot.py` | per-design `capture(...)` with census naming + `serve_dir`; keeps its `shots.json` rollup |
| `tools/mocha-census/shoot-slides.py` | per-slide `capture(viewport="1600x900", full_page="auto")`; the overflow heuristic moves *into* the service so all callers share it |
| `tools/mocha-census/check-health.py` | shrinks to "call `capture(..., health=true)`" once v2 lands; until then unchanged |

**Conventions the service should own (replacing three ad-hoc ones):**
- **Naming**: one scheme, e.g. `<namespace>__<slug>.png`, where the caller supplies the
  namespace (`census`, `slides`, `lint`) and the service slugs the target consistently
  (consolidating `repo__id`, `corpus__slug`, `stem_for()[-80:]`).
- **Dedup**: by **source mtime vs PNG mtime** (re-shoot when source is newer) — fixing the
  census "seen-key never re-shoots a changed page" gap, not just "have I seen this key."
- **Settle wait**: one shared default (the four scripts use 300/350/350/400ms — pick one,
  expose an override).
- **full-page**: one shared `"auto"` heuristic (shoot-slides' `doc_h > height*1.6`) so no caller
  forks its own.

---

## 9. Open questions for David (resolve before building)

- **New app vs integrate?** (Brief recommends a *new, tiny* standalone Capture; fold-into-AppyRadar
  rejected for identity-drift reasons. Your call.)
- **Name?** "Capture" / "AppyShot" / something brand-coherent with AppyRadar/AngelEye?
- **Where does it live — Roamy or the M4 Mini?** It must be reachable by whoever runs the render
  loop; mocha-census already shoots across *both* machines.
- **MCP vs local HTTP?** True MCP tool (discoverable, constellation-shaped) vs a thin local
  `:PORT` daemon the scripts curl. MCP is the constellation idiom; local-http is faster to stand up.
- **Does it absorb `check-health.py` in v1 or v2?** (Brief says v2 — confirm.)
- **Who owns liveness of *this* service?** AngelEye/AppyRadar observe; Marshall reaps — does
  Capture's `health()` feed the same reaper path?

---

**Status: DRAFT for decision — not yet ticketed.**
