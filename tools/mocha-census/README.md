# Mocha Census — design audit + taste board

A reusable Dark Factory tool that **finds every design page across machines, screenshots them, and
gives you a rate-and-label board** whose verdicts feed back into the design spec. It is the machine
behind the self-improving design loop: *render → rate → distill → re-render*.

## What it actually is (how it works)

The pages are **plain HTML files already on disk** — Mochaccino designs at
`<repo>/.mochaccino/designs/<id>/index.html`, each fetching its own `data/<id>.json` client-side.
There is **no app to run** and **no persistent server per page**. Instead:

- **Screenshotting** (`shoot.py`): because each page does `fetch(...json)`, `file://` won't work — so
  the tool spins up **one throwaway `http.server` per repo on an ephemeral port**, screenshots every
  design under it with headless Chromium (Playwright), then **tears the server down**. Short-lived,
  reused across all of that repo's designs. Nothing is left running.
- **The board** (`out/shots/gallery.html`): a static page served by one `python -m http.server 7440`.
  It reads `out/shots/shots.json`, shows the contact sheet, stores your ratings in the browser
  (localStorage), and exports them as JSON.

So the only "servers" are (a) ephemeral per-repo ones inside `shoot.py` that exist only during
capture, and (b) the gallery viewer on :7440.

## The pieces

| file | role |
|---|---|
| `scan.sh` | `find` every real design on a machine (skips skill-templates/worktrees/node_modules). Runs locally **or** over SSH: `ssh host 'bash -s' < scan.sh -- <label>` |
| `combine.py` | dedupe build-copies + cross-machine dupes → `out/manifest.json` (run **manually**; not invoked by `run-full.sh`) |
| `shoot.py` | serve each repo, full-page PNG per design, dedupe by `(repo,design_id)` → `out/shots/` + `shots.json` |
| `shoot-slides.py` | sibling of `shoot.py` for **slide decks** — 1600×900 16:9 PNG of every standalone HTML slide → `out/slides/` |
| `check-health.py` | flag broken renders (console errors / stuck "Loading…") so a data-wiring bug isn't mistaken for a design verdict |
| `extract.py` | structural feature-extraction over rated designs (composition signals) |
| `run-full.sh` | the whole thing: local shoot → rsync Mini-only roots → shoot the rest |
| `out/shots/gallery.html` | the **taste board** (love/good/average + free-text label, keyboard A/S/D, ←/→, export JSON) |
| `out/ratings/round-NN.json` | each rating round David exports |
| `out/ratings/exemplars.json` | the love-tier exemplar pack the design spec references |

Findings flow to **`docs/david-design-patterns.md`** (the design spec) and the exemplar pack.

## How to run it

```bash
cd ~/dev/ad/apps/dark-factory/tools/mocha-census

# 1. full refresh across BOTH machines (M4 Pro local + M4 Mini over Tailscale)
bash run-full.sh

# 2. or just this machine
bash scan.sh m4pro > out/census-m4pro.tsv
python3 shoot.py --tsv out/census-m4pro.tsv

# 3. scope to one project / a few variants (the "rate these N" case)
python3 shoot.py --tsv out/census-m4pro.tsv --filter dark-factory

# serve the board (if not already on :7440)
nohup python3 -m http.server 7440 > .serve.log 2>&1 &
# open http://localhost:7440/out/shots/gallery.html → rate → "copy ratings JSON" → paste back
```

## Refreshing (re-run any time)

Yes — re-running is the design. `shoot.py` dedupes by `(repo,design_id)` and **only shoots designs
not already captured**, so a re-run is cheap.

**Known gap:** it does not yet detect a *changed* page (same id, new content) — to re-capture an edited
design you must delete its `out/shots/<repo>__<id>.png` first (and its `shots.json` entry). A future
improvement: compare file mtime vs the shot and auto-re-shoot stale ones.

## Cross-machine

`scan.sh` runs over SSH to the M4 Mini (`davidcruwys@100.82.235.39`, Tailscale). `run-full.sh` `rsync`s
the Mini-only design folders into a local mirror so a single Chromium captures everything. ~122 designs
exist on both machines with **diverged mtimes** — the board shoots the freshest and labels each card's
source machine.

> **Prerequisite:** `run-full.sh` itself does **not** SSH-scan the Mini — it consumes an existing
> `out/census-m4mini.tsv`. Produce/refresh it first with the manual scan step:
> `ssh davidcruwys@100.82.235.39 'bash -s' < scan.sh -- m4mini > out/census-m4mini.tsv`.
> Without that TSV, `run-full.sh` rsyncs nothing from the Mini.

## Modes (current + planned)

- **Census mode (now):** discover *everything*, contact-sheet, bulk rate. Built for breadth (~200 pages).
- **Bench mode (planned):** point at *N specific* designs/variants → side-by-side compare → rate/label →
  return JSON. This is the "generate 5 variants of one idea, rate, regenerate" loop and the right shape
  for 1–2 pages. Same engine (`shoot.py` + a viewer), different front door.

## The self-improvement loop this serves

`render → rate+label → distill to spec (docs/david-design-patterns.md) → re-render → re-rate`. Proven
once: `05-dark-factory` (good/"busy") → re-rendered to spec as `05-dark-factory-v2` → rated **love**.
The open step to make it fully self-learning: wire the spec + exemplar pack into the generator
(`frontend-design` / Mochaccino render) and tighten rating-ingest (export-to-file instead of paste).
