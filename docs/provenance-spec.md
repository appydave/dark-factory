# Provenance Spec

**Purpose**: Defines the `provenance.json` schema that every canonical artifact MUST carry. This is the chain back from David's rewrite to every origin file it was mined from — the "verifiable canonical" promise.

**For Agents**: Read before writing `provenance.json` for any new canonical artifact. Validate with `tools/verify-provenance.py` (run `python3 tools/verify-provenance.py <artifact-dir>`, or `--all` for the whole library; `--self-test` proves the rules) or manually against the checklist below.

**Created**: 2026-05-18
**Last Updated**: 2026-05-18

---

## Why provenance matters

Three claims the chain must support:

1. **No mystery skills.** Every canonical artifact's origins are known and locatable. No "where did this come from" five months later.
2. **No lost source.** The verbatim original is preserved in `_source/` even after rewrite. If David's rewrite drifts or breaks, the original is recoverable per-skill (not just from upstream repos that may go stale).
3. **Audit the rewrite.** What was kept, what was modified, what was set aside — each documented per-origin so future reviewers can re-derive the decisions.

## Schema

```json
{
  "canonical_id": "dark-factory:skill:code-review",
  "canonical_type": "skill",
  "canonical_name": "code-review",
  "version": 1,
  "rewrite_status": "draft | in-style | ratified",
  "rewrite_date": "2026-05-18",
  "rewrite_author": "David Cruwys",

  "origins": [
    {
      "source_repo": "compound-engineering-plugin",
      "source_path": "/Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/skills/ce-code-review/SKILL.md",
      "source_commit": "main@abc1234",
      "source_url": "https://github.com/EveryInc/compound-engineering-plugin/blob/main/...",
      "harvested_at": "2026-05-18",
      "verbatim_copy": "_source/compound-engineering--ce-code-review.md",
      "kept": [
        "fan-out mechanism (15-20 reviewers in parallel)",
        "structured JSON findings schema",
        "confidence-based dedup"
      ],
      "modified": [
        "voice → David's terse operator tone",
        "description → trigger-only (was a workflow summary)",
        "removed multi-harness compile target"
      ],
      "set_aside": [
        "cluster analysis dispatch (too complex; can re-add later as optional)"
      ]
    },
    {
      "source_repo": "agent-skills-osmani",
      "source_path": "/Users/davidcruwys/dev/upstream/repos/agent-skills/skills/code-review-and-quality/SKILL.md",
      "source_commit": "main@def5678",
      "harvested_at": "2026-05-18",
      "verbatim_copy": "_source/agent-skills-osmani--code-review-and-quality.md",
      "kept": [
        "5-axis severity-labeled review framework",
        "4-question pre-report gate (cite line, name failure, read context, defend severity)",
        "anti-rationalization table"
      ],
      "modified": [],
      "set_aside": [
        "multi-model review pattern (out of David's current runtime budget)"
      ]
    }
  ],

  "research_sources": {
    "distillation": "research/distillations/code-review-dimensional-specialist.md",
    "evaluations": [
      "research/evaluations/agent-skills-osmani__skill__code-review-and-quality.md",
      "research/evaluations/compound-engineering__skill__ce-correctness-reviewer.md"
    ],
    "cluster_distill_index": "research/distillations/INDEX.md#code-review-cluster"
  },

  "version_history": []
}
```

## Field rules

| Field | Required | Notes |
|-------|----------|-------|
| `canonical_id` | yes | `dark-factory:<type>:<name>` |
| `canonical_type` | yes | `skill` \| `agent` \| `command` |
| `canonical_name` | yes | kebab-case |
| `version` | yes | integer, starts at 1 |
| `rewrite_status` | yes | `draft` (initial) → `in-style` (David's voice applied) → `ratified` (passes all checklists) |
| `rewrite_date` | yes | ISO date |
| `rewrite_author` | yes | usually "David Cruwys" or "Claude (under direction)" |
| `origins[]` | yes | minimum 1; usually 2-5 |
| `origins[].source_repo` | yes | matches a repo in `research/recon/<repo>.md` |
| `origins[].source_path` | yes | absolute path that existed on disk at harvest time |
| `origins[].source_commit` | recommended | git commit SHA at harvest time |
| `origins[].source_url` | recommended | GitHub URL for the file at that commit |
| `origins[].harvested_at` | yes | ISO date |
| `origins[].verbatim_copy` | yes | relative path to `_source/<repo>--<file>.md` — must exist on disk |
| `origins[].kept` | yes | array, minimum 1 — what was kept from this origin |
| `origins[].modified` | yes | array, possibly empty |
| `origins[].set_aside` | yes | array, possibly empty — what was deliberately NOT kept |
| `research_sources.distillation` | recommended | the distill draft this canonical came from |
| `research_sources.evaluations[]` | recommended | the deep evals consulted |
| `version_history[]` | yes | empty for v1, populated on version bump |

## Verbatim copy rules

Every entry in `origins[]` MUST have a corresponding file in `_source/`:

- **Path convention**: `_source/<source_repo>--<original-filename>.md`
  - Example: `_source/compound-engineering--ce-code-review.md`
  - Use double-hyphen `--` to separate repo name from filename
- **Content**: complete verbatim copy of the origin file. No editing. No truncation.
- **If origin is multiple files** (skill body + references + scripts): copy each into `_source/` with the same naming, OR put them in a subfolder: `_source/compound-engineering--ce-code-review/SKILL.md`, `references/...`
- **Never substitute a link for the verbatim copy.** Upstream files can disappear, change, or get rebased — the verbatim copy is the durable record.

## Validation rules (for `tools/verify-provenance.py`)

The validator must enforce:

1. `provenance.json` parses as valid JSON
2. All `required` fields present
3. Every `origins[i].verbatim_copy` path exists relative to the artifact's folder
4. Every file in `_source/` is referenced by at least one origin (no orphans)
5. `rewrite_status` is one of the three allowed values
6. `version` is a positive integer
7. `version_history[]` has `version - 1` entries (e.g. v3 has 2 history entries)
8. No `origins[i].kept` is empty (you must have kept SOMETHING from each origin — if you kept nothing, drop that origin from the list)

## Version bumps

When ratified canonical needs change:

```json
{
  "version": 2,
  "rewrite_status": "ratified",
  "rewrite_date": "2026-09-01",
  "version_history": [
    {
      "version": 1,
      "ratified_at": "2026-05-25",
      "superseded_at": "2026-09-01",
      "superseded_reason": "Added 7th conditional dimension (security) per compound-engineering pattern",
      "diff_summary": "+1 specialist agent (security-reviewer), +3 lines in behavior block, no breaking changes to invocation signature"
    }
  ]
}
```

The previous version's SKILL.md can be retrieved from `git log` if needed. The `version_history[]` records the WHY of each version transition.

## Cross-referencing

If a canonical artifact references another canonical artifact (e.g. an orchestrator that calls specialists), record the dependency in SKILL.md, not in provenance.json. Provenance is about *upstream origins*, not about *internal dependencies*. The two graphs are different.
