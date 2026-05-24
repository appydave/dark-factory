---
repo: matt-pocock-skills
github: https://github.com/mattpocock/skills
local_path: not cloned (remote-only recon via GitHub API)
recon_date: 2026-05-23
recon_iteration: 1
---

# Recon: Matt Pocock Skills

**Maintainer**: Matt Pocock (Total TypeScript, ai.hero.dev)
**Stars**: ~97K — highest community signal of any repo in the corpus
**Distribution**: `npx skills@latest add mattpocock/skills` via skills.sh platform
**CONTEXT.md**: Present — 40 lines, pure domain glossary (no architecture, no system snapshot). Defines Issue tracker, Issue, Triage role with _Avoid_ terms. Cleanest vocabulary-only CONTEXT.md in the corpus.
**Philosophy**: Explicitly positioned against GSD / BMAD / Spec-Kit — "they take away your control and make bugs in the process hard to resolve." Anti-process, small/composable/adaptable.

## Top-level layout

```
mattpocock/skills/
├── .claude-plugin/
│   └── plugin.json           ← Claude Code plugin manifest (14 promoted skills)
├── .out-of-scope/            ← ideas explicitly ruled out
├── docs/                     ← per-repo config docs written by setup-matt-pocock-skills
├── scripts/                  ← install / CLI scripts
├── skills/
│   ├── engineering/          ← 10 promoted skills (daily code work)
│   ├── productivity/         ← 4 promoted skills (non-code workflow)
│   ├── misc/                 ← 4 skills (kept, not promoted in README)
│   ├── personal/             ← tied to Matt's own setup, excluded from catalog
│   ├── in-progress/          ← 4 drafts (review, writing-beats, writing-fragments, writing-shape)
│   └── deprecated/           ← 4 retired (design-an-interface, qa, request-refactor-plan, ubiquitous-language)
├── CLAUDE.md                 ← bucket-membership rules + README/plugin.json invariants
├── CONTEXT.md                ← domain glossary (vocabulary-only, no architecture)
└── README.md                 ← full reference with descriptions + philosophy essays
```

## Artifact types found

| Type | Location | Count | Frontmatter? | Notes |
|------|----------|-------|--------------|-------|
| Skills (promoted) | `skills/engineering/*/SKILL.md` + `skills/productivity/*/SKILL.md` | 14 | Yes — `name`, `description` | Listed in plugin.json; must appear in README |
| Skills (misc) | `skills/misc/*/SKILL.md` | 4 | Yes — `name`, `description` | Not in plugin.json or README reference |
| Skills (in-progress) | `skills/in-progress/*/SKILL.md` | 4 | Yes | Excluded from plugin.json and README |
| Skills (deprecated) | `skills/deprecated/*/SKILL.md` | 4 | Yes | Excluded from plugin.json and README |
| Supporting files | Inside skill dirs (tdd: tests.md, mocking.md, deep-modules.md, interface-design.md, refactoring.md; grill-with-docs: CONTEXT-FORMAT.md, ADR-FORMAT.md) | ~7 | None | Reference material linked from SKILL.md body |
| CLAUDE.md | Root | 1 | None | Bucket-membership governance rules |
| CONTEXT.md | Root | 1 | None | Vocabulary-only domain glossary |

## Promoted skill list (plugin.json)

**Engineering** (10):
- `diagnose` — six-phase debugging loop (reproduce → minimise → hypothesise → instrument → fix → regression-test)
- `grill-with-docs` — alignment grilling + CONTEXT.md + ADR authoring in one session
- `triage` — issue state-machine with triage roles
- `improve-codebase-architecture` — find deepening opportunities via CONTEXT.md + ADRs
- `setup-matt-pocock-skills` — per-repo bootstrap (issue tracker, label vocab, doc layout); must run first
- `tdd` — red-green-refactor with vertical-slice tracer bullets; anti-horizontal-slice doctrine
- `to-issues` — break plan/spec/PRD into independently-grabbable GitHub issues
- `to-prd` — synthesize conversation into PRD + GitHub issue
- `zoom-out` — architecture orientation for unfamiliar code sections
- `prototype` — throwaway prototype (terminal app for logic, or multiple UI variations)

**Productivity** (4):
- `caveman` — ~75% token reduction by stripping filler; persists until explicitly disabled
- `grill-me` — alignment interview without the docs integration
- `handoff` — compact conversation into handoff doc for next agent; saves to OS temp dir
- `write-a-skill` — meta-skill for skill authoring with structure guidelines

## Standout patterns

### 1. CONTEXT.md as vocabulary-only domain glossary

Every other repo in the corpus either omits CONTEXT.md or uses it as a system snapshot / architecture overview. Pocock's CONTEXT.md is a **pure glossary** with a strict rule: "totally devoid of implementation details." It records term → definition + _Avoid_ synonyms. `grill-with-docs` creates and maintains it inline during sessions. This is the sharpest expression of the "shared language" pattern anywhere in the corpus.

### 2. Grill-first alignment as the primary entry point

`grill-me` (standalone) and `grill-with-docs` (with domain doc integration) are listed as the most-used skills. Philosophy: the primary failure mode of AI coding is misalignment before the first line of code. The grill pattern forces branch-by-branch decision resolution before implementation begins — the agent provides a recommended answer for each question it asks. Distinct from spec-kit's constitution/specify phase; no document artifact required.

### 3. Feedback-loop-first debugging doctrine

`diagnose` Phase 1 ("Build a feedback loop") is described as "the skill" — everything else is mechanical. The skill lists 10 specific loop-construction techniques in order (failing test → curl script → CLI with fixture → headless browser → replay trace → throwaway harness → property fuzz → bisection → differential → HITL bash script). Only after a passing loop exists does the skill allow Phase 2 (reproduce). No other repo in the corpus treats the feedback loop itself as the primary diagnostic artifact.

### 4. Anti-horizontal-slice TDD

`tdd` explicitly names "horizontal slicing" (write all tests first, then all code) as an anti-pattern with a label. The corpus has TDD coverage (compound-engineering, spec-kit) but none name or define this failure mode explicitly. Vertical tracer-bullet slicing (one test → one impl → repeat) is the enforced pattern. Supporting files inside the skill dir (`tests.md`, `mocking.md`, `deep-modules.md`, `interface-design.md`, `refactoring.md`) link John Ousterhout's "deep modules" concept directly into the TDD workflow.

### 5. Caveman mode — token compression as first-class skill

No other repo in the corpus treats token efficiency as a named, triggerable, persistent communication mode. `caveman` drops articles, conjunctions, filler, and hedging while preserving full technical accuracy and code blocks. Has an "Auto-Clarity Exception" for destructive operations and ambiguous multi-step sequences. ~75% token reduction claim.

### 6. skills.sh distribution platform

Install via `npx skills@latest add mattpocock/skills` — a different delivery mechanism from the corpus (which uses direct clone or plugin.json auto-install). The `skills.sh` platform lets users pick individual skills and target harnesses during install. Not catalogued elsewhere in the corpus.

### 7. Bucket-membership governance via CLAUDE.md

The root `CLAUDE.md` declares explicit invariants: every skill in `engineering/` or `productivity/` must appear in both `README.md` AND `plugin.json`; skills in `personal/`, `in-progress/`, `deprecated/` must not appear in either. This is the only repo in the corpus that encodes artifact lifecycle states (draft vs promoted vs deprecated) as CLAUDE.md rules rather than directory convention alone.

### 8. `zoom-out` — one-instruction architecture orientation

A SKILL.md whose entire body is two sentences. `disable-model-invocation: true` in frontmatter (noted — only example of this field in the corpus). Uses the project's domain glossary as the framing constraint: "Give me a map of all relevant modules and callers, using the project's domain glossary vocabulary." Lightest-weight artifact in the corpus; shows the minimum viable skill is a single injected sentence.

## Inclusion candidates

- **14 promoted skills** (plugin.json list) — primary catalog targets; all have `name` + `description` frontmatter
- **4 misc skills** — lower priority; `setup-pre-commit` and `git-guardrails-claude-code` are broadly applicable; `migrate-to-shoehorn` and `scaffold-exercises` are domain-specific to Matt's TypeScript course business
- **CONTEXT.md** — not a skill artifact but the vocabulary-only pattern it demonstrates is worth capturing as an insight

## Exclusion candidates

- `skills/personal/` — tied to Matt's personal setup; not discoverable or generalizable
- `skills/in-progress/` — drafts; may mature later but not ready for distillation
- `skills/deprecated/` — retired artifacts; catalog for historical pattern reference only
- `scripts/` + `docs/` — install tooling, not workflow artifacts
- `.out-of-scope/` — ruled-out ideas; interesting for insight capture but not catalog artifacts

## Corpus fit

**Cluster coverage** (existing Dark Factory clusters this repo enriches):

| Cluster | Skills |
|---------|--------|
| `verification-validation` | `diagnose`, `tdd` |
| `planning` | `grill-with-docs`, `grill-me`, `to-prd` |
| `workflow-architecture` | `improve-codebase-architecture`, `zoom-out`, `prototype` |
| `delivery-readiness` | `to-issues`, `triage`, `handoff` |
| `knowledge-capture` | `grill-with-docs` (CONTEXT.md/ADR authoring) |
| `code-implementation` | `tdd` |
| *(new candidate)* | `caveman` (token-compression / communication mode) |
| *(new candidate)* | `write-a-skill` (meta-skill authoring) |

**New prompt patterns** surfaced:

- `vocabulary-only-context` — CONTEXT.md restricted to glossary terms, zero implementation detail
- `grill-first-alignment` — interrogative alignment with recommended answers before implementation
- `feedback-loop-first` — loop construction as Phase 1 prerequisite, named as the primary diagnostic artifact
- `token-compression-mode` — persistent communication mode that trades verbosity for density

## Open questions

1. **`disable-model-invocation: true`** in `zoom-out` frontmatter — this field doesn't appear in any other corpus repo. Is it a skills.sh-specific frontmatter key? What does it do? Worth adding to schema-history if it becomes a pattern.

2. **skills.sh as a delivery mechanism** — the `npx skills@latest` installer lets users select individual skills across repos. Should the catalog track `distribution_platform` as a metadata field alongside `harness_type`?

3. **Supporting files inside skill dirs** — `tdd` has 5 reference files linked from SKILL.md; `grill-with-docs` has 2. The corpus schema currently treats a skill as a single SKILL.md. Should supporting files be first-class sub-artifacts or metadata on the parent skill?

4. **Deprecated skills as historical artifacts** — `ubiquitous-language` in `deprecated/` was presumably the precursor to the CONTEXT.md vocabulary pattern. Worth a targeted read to understand the evolution.

5. **`in-progress/writing-*` cluster** — three writing-focused drafts (`writing-beats`, `writing-fragments`, `writing-shape`) suggest a content-writing skill set is being developed. Matches a gap in the current Dark Factory corpus (no writing/content skills distilled yet).
