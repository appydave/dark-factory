# YLO Experiment — Blackboard Workflow Handover

**Purpose**: Single canonical document for anyone (or future-you on another machine) who needs to understand, resume, or extend the blackboard workflow probes in this folder. Reads top-to-bottom. The quickstart section at the top gets you running in 5 minutes; deeper sections explain how and why.

**Last updated**: 2026-05-21
**Sessions in scope**: blackboard pattern probes #1 through #4 (May 2026)

---

## 1. The 30-second orientation

We've built a **bash + jq + curl** implementation of the **blackboard workflow pattern** (per `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md`). It runs stateful, multi-step workflows inside a single Claude Code session by:

- treating the main session as a **conductor** (orchestrator role) that never accumulates step payloads
- delegating each step to an isolated **subagent** with its own clean context window
- coordinating via a **durable EAV store** (JSONL append-only) — the single source of truth
- supporting **human-in-the-loop gates** without poisoning the orchestrator's context

Four probes have run. Each tested a different dimension. The pattern works. All four probes' outputs live in `experiments/ylo/blackboard/runs/`.

---

## 2. Quickstart — "I want to build a new workflow today"

Five steps. Assumes you've `git pull`ed this repo onto a fresh machine.

### 2.1 — Confirm preconditions

```bash
cd ~/dev/ad/apps/dark-factory

# Skills installed?
ls .claude/skills/conductor/SKILL.md .claude/skills/store/SKILL.md .claude/skills/image-gen/SKILL.md

# Required tools
jq --version && curl --version | head -1

# If you'll use kie.ai:
test -n "$KIE_AI_API_KEY" && echo "kie key set" || echo "source ~/.secrets"
```

### 2.2 — Pick a video / run id

Convention: `runs/<video-id>/` (e.g. `runs/b65`, `runs/b71`). Per-run isolation. Most workflows seed `videoId` + `transcriptPath` and append to that run's `store.jsonl`.

### 2.3 — Author `workflow-<name>.json`

Minimal shape (full schema in `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md` §11.1):

```json
{
  "id": "my-workflow",
  "name": "My Workflow",
  "version": "1.0.0",
  "store": { "backend": "jsonl", "path": "{workflowDir}/runs/{videoId}/store.jsonl",
             "projection": "{workflowDir}/runs/{videoId}/store.view.json",
             "writeCadence": "step" },
  "seed": [ { "key": "videoId", "from": "input" } ],
  "steps": [
    {
      "id": "extract-something",
      "name": "...",
      "type": "transform",
      "model": "analysis",
      "promptFile": "prompts/extract-something.hbs",
      "inputs": [ { "key": "transcriptPath", "required": true } ],
      "stores": "myOutputKey",
      "workerContract": "write-store-directly",
      "humanGate": false
    }
  ]
}
```

Step types: `transform` (LLM step), `checkpoint` (human-gated), `action` (side effect like writing a file), `gate` (predicate / branch), `elicit` (gather input from human).

### 2.4 — Write the prompt template(s)

`experiments/ylo/blackboard/prompts/<name>.hbs` — plain text with `{{placeholder}}` markers for store keys the worker needs. Example:

```
Analyse this transcript and extract X.

Transcript path: {{transcriptPath}}
Topic: {{mainTopic}}

Return ONLY JSON: { "myField": "..." }
```

### 2.5 — Run via the conductor

You ARE the conductor. Open this folder in Claude Code. The conductor skill activates when you load a workflow. You'll:

1. **Seed** the store with input keys (videoId, paths, etc.)
2. **Dispatch** each step as a subagent via the Agent tool, passing the rendered prompt + store path + write key
3. **Receive** one-line acks (never payloads) and log them to `runs/<videoId>/conductor-session-<workflow>.log`
4. **For human gates**: render the relevant key's value(s), prompt user, end your turn, parse the next user message
5. **Project + manifest** at end: `jq -s 'reduce .[] as $r ({}; . + {($r.key): $r.value})' store.jsonl > store.view.json`

That's the loop. The conductor and store skills document the contracts precisely.

---

## 3. What's been built — the four probes

Each probe added one new dimension to the pattern.

| # | Workflow file | Tested | Outputs | Result |
|---|---------------|--------|---------|--------|
| 1 | `workflow-01-analysis.json` | **Parallel fan-out** — 12 subagents extracting content-analysis fields | `runs/b65/store.jsonl` (12 keys) | 16/16 ACs |
| 2 | `workflow-02-titles.json` | **Scripted refinement loop** — generate → fixture critique → refine, plus `outputKeyMap` key rename | adds generatedTitles attempt:1+2, titleCritiqueLog, selectedTitles | 21/21 ACs |
| 3 | `workflow-03-titles-human.json` | **Real human-in-the-loop gate** — generate → render to user → parse typed critique → refine; both accept-path and refine-path | `runs/b65-2-5/store.jsonl` (separate store to keep isolated) | 21/21 ACs |
| 4 | `workflow-04-thumbnails.json` | **Async external API + binary artifacts + title-thumbnail pairing** — kie.ai polling, JPGs to disk, paths in store | `runs/b65/thumbs/` (6 exp + 3 final), 15 new store records | 20/22 ACs (2 annotated) |

**The load-bearing claim — proven 4 times**: the orchestrator never ingests step payloads (transcript text, extracted values, titles, critique text, image bytes, kie.ai response bodies). The conductor logs are clean; the store holds the truth.

---

## 4. Architecture — how the pieces fit

```
                              ┌─────────────────────────────────┐
                              │  workflow-<name>.json           │
                              │  (the spec — DAG of steps)      │
                              └──────────────┬──────────────────┘
                                             │ loads
                                             ▼
  user types       ┌──────────────────────────────────────────┐
  ──────────────►  │  CONDUCTOR (this Claude Code session)    │
                   │  - reads store keys/status (NOT payloads)│
                   │  - resolves step inputs from store       │ ◄────┐
                   │  - spawns one subagent per step          │      │ writes
                   │  - logs dispatches/acks only             │      │
                   └─────┬────────────────────────┬───────────┘      │
                         │ Agent.spawn            │ writes log       │
                         ▼                        ▼                  │
            ┌──────────────────┐         ┌─────────────────────┐    │
            │   SUBAGENT       │         │  conductor-session  │    │
            │  (clean context, │         │  -<workflow>.log    │    │
            │   write-store    │         │  (acks only)        │    │
            │   -directly)     │         └─────────────────────┘    │
            └────────┬─────────┘                                    │
                     │ jq -nc >> store.jsonl                        │
                     ▼                                              │
            ┌──────────────────────────────────────────────┐        │
            │  runs/<videoId>/store.jsonl                  │ ───────┘
            │  EAV append-only log                         │
            │  {key, group, index, value, meta{step,by,ts}}│
            └──────────────────────────────────────────────┘
```

### Hard contracts

- **Write-store-directly**: worker writes the store, returns a 1-line ack. Orchestrator sees only the ack.
- **Return-summary** (rarely used): worker returns the payload; orchestrator writes the store. Used when the orchestrator must reason about the value (e.g. to host a human gate).
- **Conductor-writes**: conductor itself writes (no subagent). For checkpoints reading fixture files, for the assemble-output step, for seeds.

### Two coordination modes

- **Parallel fan-out** (probe 1, 4 exploration phase): N steps with shared inputs and distinct output keys. Spawn N subagents concurrently.
- **Sequential dependency** (probes 2, 3, 4 refine/finals): later steps consume earlier outputs. Dispatch in order.

---

## 5. The skills — three files, all project-local

`/Users/davidcruwys/dev/ad/apps/dark-factory/.claude/skills/`

### 5.1 `conductor/SKILL.md`
The orchestrator role. Documents:
- The §5 execution loop
- Hard isolation constraints (5 rules)
- Subagent task templates (transform, refine)
- Conductor log format (7 line types: DISPATCH, ACK, CRITIQUE-LOGGED, REFINE, HUMAN-GATE-OPENED, HUMAN-GATE-CLOSED, PROJECT, DONE)
- Human gate behaviour (`humanGate: true` + `gateMode: "human-stdin"`)
- `outputKeyMap` rename support
- Resumability (re-read store, skip done steps)

Built across probes 1, 2, 3. Untouched by probe 4.

### 5.2 `store/SKILL.md`
The EAV bash+jq operations. Three primitives:
- `remember STORE_PATH KEY VALUE_JSON STEP_ID` — append one EAV record
- `recall STORE_PATH KEY` — project last-write-wins
- `project STORE_PATH VIEW_PATH` — fold log into `{key: value, ...}` JSON view

Untouched since probe 1.

### 5.3 `image-gen/SKILL.md`
The kie.ai async wrapper. Documents:
- POST createTask → poll recordInfo → curl download pattern
- Two model lanes: flux-schnell (cheap, exploration) and nano-banana-2 (premium, finals)
- 5-stage worker template (create / poll / download / store / ack)
- Hard rules (no bytes echoed, no response bodies in ack, localPath only in store)
- Worker invocation contract

**Known spec drift**: this skill references `flux-schnell` which does not exist on kie.ai. See open loop #2.

Built in probe 4.

---

## 6. The store — EAV semantics

Every record has the same envelope:

```json
{
  "key": "<string>",
  "group": null | "<string>",
  "index": null | <int>,
  "value": <any JSON>,
  "meta": {
    "step": "<step-id>",
    "by": "subagent:<step-id>" | "conductor",
    "ts": "<ISO-8601>",
    "attempt": <int>,
    "status": "ok" | "error" | "candidate",
    "source": "<optional>",
    "note": "<optional>"
  }
}
```

### Projection rules
- **Scalar keys**: last-write-wins. `jq -s 'reduce .[] as $r ({}; . + {($r.key): $r.value})'` gives the projection.
- **Collection keys** (with `group` + `index`): accumulate per index. Use `select(.key=="X" and .group=="..." and .index==N)` then `tail -1` for last-write-wins per slot.

### Append-only — hard rule
Never edit existing lines. Always append new ones. The append-only chain IS the audit trail. Refinement attempts, accept-then-refine, error states — all preserved as history.

### Examples seen in this repo

- Probe 2's `selectedTitles` was first written as a string. Probe 4 appended a new array-typed `selectedTitles`. Last-write-wins gives the array; the original string is preserved as audit.
- Probe 3's `ok` accept-path wrote `selectedTitles` with `meta.skippedRefinement:true`. The subsequent real critique appended `titleCritiqueLog`, then refined `generatedTitles` to attempt:2, then a new `selectedTitles` (via outputKeyMap). All preserved.
- Probe 4's exploration index 3 first wrote an error record (model unsupported), then a second record after re-dispatch with `meta.attempt:2`.

---

## 7. The isolation discipline (the Oscar fix)

This is the single most important rule. The pattern's value collapses without it.

**The orchestrator NEVER ingests step payloads.** This is enforced by:

1. **Workers are subagents** — they get a clean context, do their work, write the store, return only a one-line ack. The orchestrator never sees the payload.
2. **The conductor log captures only**: dispatches, acks, gate transitions, errors, timing. Never the data itself.
3. **The transcript is on disk, not in conductor context** — workers read it via their own bash, the orchestrator holds only the path.
4. **Image bytes never leave disk** — workers `curl -o` them to local files, the store record carries only `localPath`. No base64. No `data:image/...`.
5. **Critique text lives in the store, not the log** — even the conductor's CRITIQUE-LOGGED line records only the byte length.

**Verification commands** that prove isolation held:

```bash
# No payload content in conductor log
grep -Ff <(head -c 200 runs/<id>/transcript.txt) runs/<id>/conductor-session-*.log | wc -l   # → 0
grep -E "base64,|iVBOR|data:image|\"resultJson\"" runs/<id>/conductor-session-*.log         # → empty

# No image bytes anywhere in store
grep -E "base64,|iVBOR|data:image" runs/<id>/store.jsonl                                    # → empty
```

These verifications were run against every probe.

---

## 8. Writing a new workflow — recipe

You have the skills, the pattern, and the example workflows. The recipe:

### 8.1 — Decide what dimension you're testing
What does this workflow need that the four probes haven't already proven? (Or are you just using the pattern, not testing it?)

### 8.2 — Sketch the DAG
- What's seeded (`seed[]`)?
- What inputs does each step need (`inputs[]`)?
- What does each step write (`stores`)?
- Where are the parallel fan-out points?
- Where (if anywhere) are the human gates?

### 8.3 — Author `workflow-<name>.json`
Use the existing files as templates:
- `workflow-01-analysis.json` — pure parallel fan-out
- `workflow-02-titles.json` — sequential with scripted refinement + `outputKeyMap`
- `workflow-03-titles-human.json` — sequential with real human gate
- `workflow-04-thumbnails.json` — multi-phase (LLM → image → fixture select → image) with title pairing invariant

### 8.4 — Author `.hbs` prompts
One per transform step. Use `{{placeholder}}` for store keys. Spell out exactly what JSON shape the worker should return — workers are LLMs and won't guess.

### 8.5 — Run
Open this folder in Claude Code. Tell the conductor to run your workflow. Watch the acks come back. Project the store. Write a run summary.

### 8.6 — Verify isolation
Always run the grep verifications from §7 before declaring done. If anything leaked, fix the worker's prompt before re-running.

---

## 9. Open loops — known issues

Listed by priority. None are blockers; all are visible.

### High — needs decision

1. **`flux-schnell` is a phantom model.** Plan and `image-gen/SKILL.md` reference it. kie.ai's API rejects it. Probe #4 fell back to `flux-2/pro-text-to-image`. Action: update `image-gen/SKILL.md` and `workflow-04-thumbnails.json` to a verified model slug. See `runs/b65/kie-models-research.md` for alternatives.

2. **First-pass exploration records in probe #4 carry inaccurate `model:"flux-schnell"`** when they actually used different models. The records exist in `runs/b65/store.jsonl` at indices 2, 5. Honesty issue, not functional. Could be corrected by appending new EAV records with the truth.

3. **Aspect-ratio drift on nano-banana-2 finals**. 2 of 3 came back square instead of 16:9. Diagnosed as: nano-banana-2 treats `aspect_ratio` as a hint; visual cues in the prompt body override it. Fix: add explicit horizontal language ("wide horizontal YouTube banner, 16:9 composition") to `prompts/generate-design-brief.hbs`. See `runs/b65/thumbnails-manifest.md` for details.

### Medium

4. **`/goal` vs human-gate interaction**. Probe #3's human gate fires intentional turn-yielding; `/goal`'s stop hook treats this as "incomplete condition" and keeps nudging. Decided in conversation: `/goal` is a **build-time** tool, the conductor is the **runtime** — they're orthogonal. Direct conductor invocation is the default; don't wrap in `/goal` for runtime. This rule needs explicit documentation in `conductor/SKILL.md` (currently implicit).

5. **`b65-2-5/` naming inconsistency**. Probe #3's run dir. When we settled on ordinal numbering (no decimals), this never got renamed. Should be `b65-humangate/` or similar. Cosmetic.

### Low

6. **`kie-models-research.md`** (~210 lines at `runs/b65/kie-models-research.md`) has concrete recommendations not yet applied. Headlines: kie.ai catalog includes ~21 text-to-image models across 8 providers; cheap recommendation is `flux-2/pro-text-to-image`; typography tier suggestion is `ideogram-v3-text-to-image`; `nano-banana-pro` was deprecated 2026-03-09 and may have been remapped.

7. **`runs/b65/thumbnails-gallery.html`** is a stray dark-mode file in the run dir. Canonical viewer is `runs/b65/thumbs/review.html` (built from `manifest.json` via `appydave-thumbnail/scripts/viewer.py`). The stray file can be deleted.

---

## 10. File map — where everything lives

### The blackboard skills
```
.claude/skills/
├── conductor/SKILL.md      ← orchestrator role + §5 loop + human gate + outputKeyMap
├── store/SKILL.md          ← bash+jq EAV operations (remember/recall/project)
└── image-gen/SKILL.md      ← kie.ai async pattern (POST/poll/download/store/ack)
```

### The workflows
```
experiments/ylo/blackboard/
├── workflow-01-analysis.json      ← probe #1: bulk content analysis
├── workflow-02-titles.json        ← probe #2: scripted refinement
├── workflow-03-titles-human.json  ← probe #3: real human gate
└── workflow-04-thumbnails.json    ← probe #4: kie.ai thumbnails
```

### The prompts (15 .hbs + 1 .json)
```
experiments/ylo/blackboard/prompts/
├── analyze-*.hbs                  ← 12 files, probe #1, verbatim AWB Gen 3
├── generate-title.hbs             ← probe #2, verbatim AWB Gen 3
├── generate-title.json            ← schema for above
└── generate-design-brief.hbs      ← probe #4, written fresh (brand-aware)
```

### The runs
```
experiments/ylo/blackboard/runs/
├── b65/                           ← probes #1, #2, #4 share this store
│   ├── transcript.txt
│   ├── store.jsonl                ← 33 records (all probes combined, audit history preserved)
│   ├── store.view.json            ← last-write-wins projection
│   ├── conductor-session.log              (probe #1)
│   ├── conductor-session-titles.log       (probe #2)
│   ├── conductor-session-thumbnails.log   (probe #4)
│   ├── run-summary.md                     (probe #1)
│   ├── run-summary-titles.md              (probe #2)
│   ├── thumbnails-manifest.md             (probe #4)
│   ├── critique-fixture.txt               (probe #2)
│   ├── selection-fixture.json             (probe #4)
│   ├── kie-models-research.md             (probe #4 research)
│   └── thumbs/                            (probe #4 binary outputs)
│       ├── exp-1.jpg ... exp-6.jpg
│       ├── final-1.jpg, final-2.jpg, final-3.jpg
│       ├── manifest.json                  (for viewer.py)
│       └── review.html                    (viewer.py output)
│
└── b65-2-5/                       ← probe #3 only (separate to keep human-gate isolated)
    ├── transcript.txt
    ├── store.jsonl                ← 20 records (12 analysis seeds + 8 probe-3-specific)
    ├── conductor-session-titles-human.log
    └── run-summary-titles-human.md
```

### Documentation
```
experiments/ylo/blackboard/
├── README.md                      ← brief intro, points to HANDOVER
└── HANDOVER.md                    ← this document (canonical)

docs/                              ← dark-factory project docs (research/canonical pipeline)
├── canonical-form-spec.md
├── david-style-patterns.md
├── ingestion-workflow.md
└── provenance-spec.md
```

### Visualisations (mochaccino)
```
mochaccino/
├── data/
│   ├── pipeline.json              ← dark-factory research pipeline data
│   ├── mining.json
│   ├── triage.json
│   └── blackboard-probes.json     ← the 4 probes as structured data
└── designs/
    ├── index.html                 ← gallery
    ├── 01-pipeline-overview/      ← dark-factory research pipeline
    ├── 02-mining-view/            ← skill mining
    ├── 03-triage-console/         ← triage console
    ├── 04-blackboard-overview/    ← pattern architecture diagram
    └── 05-probe-progression/      ← four probes as timeline
```

Run the mochaccino server: `cd mochaccino && python3 -m http.server 7420` then open `http://localhost:7420/designs/`.

---

## 11. Cross-references

### Brain canonical docs (read-only, source of truth)
- **Substrate spec**: `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md` — the original 348-line design doc. Sections §3 (components), §5 (execution loop), §6 (refinement), §7 (parallel), §11 (JSON contracts) are load-bearing.
- **Probe plans** (one per probe, committed to brain):
  - `~/dev/ad/brains/plans/plan-ylo-blackboard-bulk-analysis.md` (probe #1)
  - `~/dev/ad/brains/plans/plan-ylo-blackboard-title-refinement.md` (probe #2)
  - `~/dev/ad/brains/plans/plan-ylo-blackboard-titles-human-gate.md` (probe #3)
  - `~/dev/ad/brains/plans/plan-ylo-blackboard-thumbnails.md` (probe #4)

### Upstream prompt sources (DO NOT lift again — already lifted verbatim)
- `~/dev/ad/apps/awb/examples/gen3/youtube/prompts/content-analysis/` — 12 analyse prompts (probe #1)
- `~/dev/ad/apps/awb/examples/gen3/youtube/prompts/title-thumbnail/generate-title.hbs` (probe #2)

### Production references (for inspiration / comparison, not import)
- `~/dev/ad/appydave-plugins/appydave/skills/appydave-thumbnail/SKILL.md` — brand-aware composition patterns
- `~/dev/ad/appydave-plugins/appydave/skills/appydave-thumbnail/scripts/generate_thumbnails.py` — Python kie.ai integration we deliberately did NOT use (bash+curl+jq only constraint)
- `~/dev/ad/apps/awb/examples/gen3/` — AWB Gen 3 reference implementation

### External
- kie.ai API: `https://api.kie.ai/api/v1/jobs/createTask` + `recordInfo` (Bearer `$KIE_AI_API_KEY` from `~/.secrets`)
- kie.ai brain docs: `~/dev/ad/brains/kie-ai/` (fundamentals, image-generation, nano-banana)

---

## 12. What "done" looks like for any new workflow

Adapted from each probe's AC pattern. For a new workflow, verify:

- [ ] `workflow-<name>.json` parses, has required top-level keys (`id`, `name`, `version`, `store`, `seed`, `steps`)
- [ ] Each step has unique `stores` key, declared `inputs[]`, valid `type`
- [ ] Prompts exist for each transform step
- [ ] Store has expected records after run (count per step type)
- [ ] All records carry valid EAV envelope (`key`, `value`, `meta.step`, `meta.ts`, `meta.by`)
- [ ] **Isolation held**: grep verifies no payload content in `conductor-session-*.log` and no image bytes in `store.jsonl`
- [ ] Run summary written documenting attempt count, elapsed time, costs (if any)
- [ ] If you reused an existing run dir: pre-existing records untouched (only appends)

---

## 13. One-paragraph elevator pitch

We solved the AWB-replacement problem inside Claude Code. AWB's three problems were: (1) it ran outside the session and ate API credits, (2) the stateful workflow document couldn't live in-session, (3) the naive "just run it in main context" attempt (POEM Oscar) failed due to context poisoning. The blackboard pattern fixes all three: workflows run in a Claude Code session as a "conductor" role that orchestrates isolated subagents through an external JSONL store. Subagents have clean contexts (so no global poisoning) and write the store directly (so the orchestrator never accumulates payloads). The store is the source of truth — workflows are resumable, all state is auditable, and human-in-the-loop critiques only forward the *distilled* feedback to the next worker, never the raw chat. Four probes proved the pattern across parallel fan-out, scripted refinement, real human gates, and async external API calls with binary outputs. Total bash+jq+curl implementation, ~3 skills, ~4 workflows. Project-local in `dark-factory/.claude/skills/`. The pattern is ready for production YLO use.
