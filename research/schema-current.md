---
schema_version: 0.0.4
created: 2026-05-16
last_updated: 2026-05-16
phase: post-discover
---

# Schema (current)

Schema is co-defined by `~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/references/capability-discover.md` (in the skill) and this file. Required + optional fields below.

## Required fields (every artifact must have)

| Field | Description |
|-------|-------------|
| `id` | `<repo>:<artifact-type>:<name>` |
| `repo` | Repo slug (from `references/repos.md` in the skill) |
| `file_path` | Absolute path on disk (canonical source if compile-on-install) |
| `artifact_type` | skill \| agent \| command \| workflow (primary only in Phase 2) |
| `name` | Filename without extension OR YAML frontmatter `name` |
| `description_raw` | Source description (paragraph) |
| `description_normalized` | Normalized one-sentence "what this does" |
| `discovered_at` | ISO date |
| `discovered_by_version` | Schema version at discovery time |

## Optional facet fields

| Field | Description |
|-------|-------------|
| `prompt_patterns_used` | Array of pattern IDs from `prompt-pattern-vocabulary.md`. Cross-cutting *architectural* facet. |
| `cluster_facet` | Array of cluster IDs from `cluster-vocabulary.md`. *Problem-family* facet — drives the distill walk. |
| `sdlc_stage` | Array of stage IDs from `sdlc-stages.md`. *When-in-lifecycle* facet. |
| `frontmatter_yaml` | Parsed YAML frontmatter (for skills/agents/commands) |
| `retired` | Boolean — true means soft-deleted; never remove the line itself |
| `body_path` | Path to a paired workflow body file (used by gsd's two-file split — entry file is `file_path`, executable prose is `body_path`). Added 0.0.4. |
| `notes` | Free-form per-artifact annotation (e.g. "beta variant", "no description in source"). Added 0.0.4. |

Each facet is a separate axis. A single artifact carries values on multiple axes.

## Phase 2 scope (decided 2026-05-16)

- **Primary artifacts only**: `skill`, `agent`, `command`, `workflow`.
- **Source-only for compile-on-install repos**: catalog the canonical `.tmpl` or master markdown; skip compiled per-harness outputs.
- **Deferred to Phase 2.5**: templates, hooks, rules, step files, MCP tools, plugin bundles. Counts already in recon reports.

## Sister artifacts

These coordinate with the JSONL corpus but live separately:

- `insights.md` (this directory) — append-only audit log of atomic craft bits surfaced during recon/discover.
- `prompt-pattern-vocabulary.md` (in skill) — stable IDs referenced by `prompt_patterns_used`.
- `cluster-vocabulary.md` (in skill) — stable IDs referenced by `cluster_facet`.
- `cluster-vocabulary-additions.md` (in skill) — holding pen for proposed new cluster IDs awaiting David's review.
- `sdlc-stages.md` (in skill) — stable IDs referenced by `sdlc_stage`.

## Change log

See [schema-history.md](./schema-history.md).
