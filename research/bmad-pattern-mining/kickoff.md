# BMAD Machinery Mining — Kickoff

**Purpose**: Self-contained brief to mine the SupportSignal BMAD story-lifecycle session
corpus and extract the *machinery* — how the semi-automated pattern actually fits together —
as a reusable **operating-model** pattern spec for the **Dark Factory**.

**For Agents**: This doc is runnable from a clean window opened in the dark-factory app
(`/Users/davidcruwys/dev/ad/apps/dark-factory`). Read it top-to-bottom, then execute the
Workflow in §6. Do **not** re-derive the corpus location or the schema — they are fixed below.

**Created**: 2026-06-24
**Lives here because**: per the dark-factory split, the *brain* owns why+life-OS+law and the
*app* owns the operating model. The BMAD machinery spec is operating-model material → app.
**Origin**: OMI conversation 8633017a (2026-06-24 "Dark Factory Workflow and Ticket Tracking"),
saved at `/Users/davidcruwys/dev/raw-intake/omi/2026-06-24-0645-dark-factory-workflow-and-ticket-tracking-discussion.md`

---

## 1. The goal (in David's words)

> "Find a pattern in the way I've done the BMAD team sessions… run a BMAD story lifecycle by
> ticket number → Swagger orchestrator reads the requirements → delegates → Bob creates then
> validates the spec → development → testing → delivery review → UAT → librarian → ship.
> Running semi-autopilot for months. It's certainly a pattern I'd love to run in the Dark
> Factory. **Careful not to lose the nature of the mechanism and the machinery, how it all fits
> together** — there's structure below it, it's not just prompt engineering, it's that stigmergy."

Deliverable: a canonical **BMAD machinery pattern spec** that a Dark Factory operating model can
reuse — the *structure and orchestration*, not a summary of what got built.

**Token posture**: David explicitly does not care about token burn. Exhaust the corpus.
The constraint is *fidelity of the mechanism*, not cost. Summarisation that loses machinery is
the failure mode — avoid it.

---

## 2. The corpus (verified 2026-06-24)

| Fact | Value |
|------|-------|
| Session dir | `/Users/davidcruwys/.claude/projects/-Users-davidcruwys-dev-clients-supportsignal-app-supportsignal-com-au/` |
| Repo it maps to | `/Users/davidcruwys/dev/clients/supportsignal/app.supportsignal.com.au/` |
| Total `.jsonl` sessions | 653 |
| Sessions with BMAD markers | 649 |
| On-disk span (mtime) | 2026-05-25 → 2026-06-24 (~30 days) |
| Sidecar project | `…-app-supportsignal-com-au-skills-bmad-oversight-references` (the BMAD oversight skill refs) |

**⚠️ Naming gap (flagged):** David called this "Signal Studio", but the
`…-signal-studio` session dir holds **0** transcripts. The real BMAD corpus is
**app.supportsignal.com.au** (649 BMAD sessions). The lifecycle machinery (Swagger orchestrator,
Bob, story-context, delivery review) lives there. Confirm this is the intended corpus before a
full run if anyone doubts it.

---

## 3. Why per-*story* clustering, not per-raw-session

A single BMAD story run is **not** one session — it's a parent orchestrator session ("Swagger")
plus **child team sessions** (Bob, dev, test, delivery-review, UAT, librarian). The machinery
*is the relationship between parent and children*. Reading 649 raw sessions blind would shred
that structure.

So Phase 0 must **cluster sessions into story-runs** before any deep read:
- group by ticket/story id (grep for `story`, `6.6`, ticket numbers, epic refs)
- group by `cwd` + time-adjacency (child teams spawn within minutes of the parent)
- follow explicit session links / `isSidechain` / parent-uuid references inside the JSONL
- bucket each run as: **full lifecycle**, **partial**, or **fragment/noise**

Phase 1 then reads **one cluster (story-run) per reader**, reconstructing parent↔child machinery.

---

## 4. Extraction schema (the anti-summarisation guardrail)

Every reader returns this fixed structure. Mechanism is captured as *concrete steps and
artifacts*, never as a prose summary.

```json
{
  "story_id": "string (ticket/story ref, or 'unknown-<short-hash>')",
  "run_type": "full-lifecycle | partial | fragment",
  "sessions_in_cluster": ["session-uuid", "..."],
  "orchestrator": {
    "name": "Swagger or actual",
    "what_it_reads_in": "requirements/spec inputs it loaded",
    "how_it_delegates": "the actual delegation mechanism — teammate spawn? task? sub-agent?"
  },
  "lifecycle_stages": [
    {"stage":"spec-create","agent":"Bob","inputs":"...","outputs":"...","decision_logic":"how pass/fail was decided","artifacts":["file paths / doc names"]},
    {"stage":"spec-validate","...":"..."},
    {"stage":"development","...":"..."},
    {"stage":"testing","...":"..."},
    {"stage":"delivery-review","...":"..."},
    {"stage":"uat","...":"..."},
    {"stage":"librarian","...":"..."},
    {"stage":"ship","...":"..."}
  ],
  "handoffs": "exact mechanism of how one stage hands to the next (file? message? state doc?)",
  "structural_layer": "the docs/state/files BELOW the prompts that make it work (the 'stigmergy') — name them with paths",
  "spec_issue_detection": "concrete examples where a bad spec was caught and how",
  "token_efficiency_notes": "anything observed about cost/speed",
  "verbatim_mechanism_quotes": ["1-3 short quotes that capture machinery that must NOT be lost"],
  "uncertainty": "what this cluster could not determine"
}
```

Rule for readers: **if forced to choose between brevity and preserving the mechanism, preserve
the mechanism.** Use `verbatim_mechanism_quotes` rather than paraphrasing structural detail away.

---

## 5. Synthesis target

Phase 2 assembles all cluster extracts into:
`/Users/davidcruwys/dev/ad/apps/dark-factory/research/bmad-pattern-mining/bmad-machinery-pattern.md`

Must contain:
1. **The lifecycle as a state machine** — stages, transitions, gate conditions (mermaid).
2. **The orchestration structure** — Swagger ↔ child teams, who spawns whom, how delegation works.
3. **The structural layer** — the on-disk docs/state that carry context between stages (the part
   that is "not just prompt engineering"). Name real files in the SS repo.
4. **What's reusable for Dark Factory** vs what's SupportSignal-specific (agents/skills can change;
   the machinery is the point).
5. **Variance map** — where runs differed (high-effort vs effort-zero stories), failure modes.
6. **Open questions / unverified** from the completeness critic (Phase 3).

Each claim cites the cluster(s)/session id(s) it came from. Verify structural claims against the
live repo `…/app.supportsignal.com.au/` (the orchestrator skill, agent defs, story docs) before
asserting. If the distilled pattern proves canonical, promote it from `research/` to the app's
`canonical/` operating-model area in a follow-up.

---

## 6. How to run it (you are in a CLEAN window in the dark-factory app)

This is a heavy multi-agent job — run it as a **dynamic Workflow** so the 649-session reading
happens in isolated subagents and only a compact digest returns to your window.

Opt into orchestration explicitly, then author the Workflow with this shape:
```
Phase 0  Scout      inline: enumerate 649 sessions, cluster into story-runs (§3), emit work-list
Phase 1  Fan-out    one reader per story-cluster, extract to schema (§4), mechanism preserved
Phase 2  Synthesise assemble bmad-machinery-pattern.md (§5), cite session ids
Phase 3  Critic     completeness pass — what modality/run/claim is missing or unverified
```
Notes for the author:
- pipeline() by default; barrier only before the §5 synthesis (needs all clusters together).
- Phase 0 clustering is plain code over the JSONL index (cheap), not an agent per session.
- The Workflow must **write the full pattern doc to disk (§5 path) and `return` only a short
  digest** — keep the launching window light.
- Cap is min(16, cores-2) concurrent; 649 clusters is fine but expect many waves — `log()` progress.
- If clustering yields more than a few hundred full-lifecycle runs, sample by story diversity
  (high-effort vs effort-zero, early vs late in the May-25→Jun-24 span) and **`log()` what was dropped**.

---

## 7. Status

- [x] Corpus located + verified (649 BMAD sessions, app.supportsignal.com.au)
- [x] Technique + schema fixed (this doc)
- [x] Relocated brain → app (operating-model ownership)
- [x] Workflow executed (2026-06-24 — dynamic Workflow, 71/71 story-run clusters + 4/4 queue sessions mined)
- [x] `bmad-machinery-pattern.md` produced (research/bmad-pattern-mining/, 454 lines, 7 sections + completeness-critic pass)
- [ ] Reviewed by David, fed into Dark Factory operating model
