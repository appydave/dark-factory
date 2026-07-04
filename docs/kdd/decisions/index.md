# Decision candidates (42)

> Reformatted into the [DF-ADR template](../ADR-FORMAT-SPEC.md) on 2026-07-04 (frontmatter +
> Revision Log added; content unchanged). Ratified lazily, one at a time — 3 accepted so far
> (ADR-0009, ADR-0028, ADR-0031, 2026-07-04), the rest still `status: proposed`,
> `confidence: reconstructed`, pending a read-and-accept pass whenever each one is about to matter.
> ADR-0023 and ADR-0040 were merged into ADR-0006 and ADR-0036 respectively on 2026-07-04 (each
> pair recorded the same same-day decision from two sessions) — numbering gaps are intentional.
> **ADR-0020 is `superseded` by ADR-0021** (same-day reversal) — the first live use of the new
> `supersedes`/`superseded_by` fields.

- [ADR-0001: Re-scaffold appyradar-sentinel as a fresh repo instead of rewriting git history to purge committed node_modules](0001-re-scaffold-appyradar-sentinel-as-a-fresh-repo-instead-of-re.md)
- [ADR-0002: Archive superseded repos with a tested git-bundle backup, and gate deletion on the replacement being proven in deployment](0002-archive-superseded-repos-with-a-tested-git-bundle-backup-and.md)
- [ADR-0003: Add a rename-migration note instead of blind find/replace for historical name references in AngelEye's retrieval skill](0003-add-a-rename-migration-note-instead-of-blind-find-replace-fo.md)
- [ADR-0004: Workflow execution model: queue file + in-session polling skill, never headless or metered-credit execution](0004-workflow-execution-model-queue-file-in-session-polling-skill.md)
- [ADR-0005: Handover documents are written to backlog/ in the repo, not to ~/.claude/sessions/, despite the capture-context skill's own staleness warning](0005-handover-documents-are-written-to-backlog-in-the-repo-not-to.md)
- [ADR-0006: Move Dark Factory job-state off flat files into a Switchboard-hosted shared state plane](0006-move-dark-factory-job-state-off-flat-files-into-a-switchboar.md)
- [ADR-0007: Switchboard has CRUD authority over its own comms domain; 'never kill' applies only to the externally observed system](0007-switchboard-has-crud-authority-over-its-own-comms-domain-nev.md)
- [ADR-0008: Adopt the adversarial A-vs-B delta (run both, critique hard, recommend canonical) as a first-class Dark Factory build technique](0008-adopt-the-adversarial-a-vs-b-delta-run-both-critique-hard-re.md)
- [ADR-0009: Dark-factory apps are mapped as a 3-layer stack (data → surfaces → KBDE host), not a flat inventory](0009-dark-factory-apps-are-mapped-as-a-3-layer-stack-data-surface.md) — **accepted** (ratified 2026-07-04)
- [ADR-0010: App-build flow split into two lanes: App Pipeline (intake/PO, brain) and App Requirements (build-spec standard, Dev repo), seam at goal-ready](0010-app-build-flow-split-into-two-lanes-app-pipeline-intake-po-b.md)
- [ADR-0011: KBDE Extension SDK incompleteness is a fragility warning for builders, not a build-blocking gate](0011-kbde-extension-sdk-incompleteness-is-a-fragility-warning-for.md)
- [ADR-0012: Harness promotion decided per-mechanism (evaluation before promotion), not as a wholesale 'promote suborch's kernel'](0012-harness-promotion-decided-per-mechanism-evaluation-before-pr.md)
- [ADR-0013: Adapt HyperFrames as the shared engine for both rendered video and interactive talk-through decks, rather than adopting a presentation-native tool](0013-adapt-hyperframes-as-the-shared-engine-for-both-rendered-vid.md)
- [ADR-0014: Comprehend→Visualise split into a read-only comprehend phase and a separate render phase, provenance carried by path + commit_sha](0014-comprehend-visualise-split-into-a-read-only-comprehend-phase.md)
- [ADR-0015: Retire --dangerously-skip-permissions for Swagger spawns; use a one-time human permission grant instead](0015-retire-dangerously-skip-permissions-for-swagger-spawns-use-a.md)
- [ADR-0016: Worker session teardown must be a deliberate, gated lifecycle — never auto-kill the instant a job completes](0016-worker-session-teardown-must-be-a-deliberate-gated-lifecycle.md)
- [ADR-0017: Factory communication bus: an always-on durable broker (never runs claude) paired with in-session reactive listeners, over SSE topic-subscription rather than a filesystem](0017-factory-communication-bus-an-always-on-durable-broker-never-.md)
- [ADR-0018: Convert every named-but-unstarted build into a stored, ticketable spec instead of starting it](0018-convert-every-named-but-unstarted-build-into-a-stored-ticket.md)
- [ADR-0019: Close sessions cleanly with a handover record instead of relying on conversation compaction](0019-close-sessions-cleanly-with-a-handover-record-instead-of-rel.md)
- [ADR-0020: Doc organiser as a recurring audit-only skill, not a one-time cleanup or autofix](0020-doc-organiser-as-a-recurring-audit-only-skill-not-a-one-time.md) — **superseded by ADR-0021**
- [ADR-0021: Don't build a new doc-organiser skill — wire the existing doc-drift + doc-review skill family instead](0021-don-t-build-a-new-doc-organiser-skill-wire-the-existing-doc-.md) — supersedes ADR-0020
- [ADR-0022: Split AngelEye into AngelSentinel (always-on collector) and AngelEye Control Plane (dashboard)](0022-split-angeleye-into-angelsentinel-always-on-collector-and-an.md)
- [ADR-0024: Spawn watchtower Swaggers with interactive claude, never claude -p/headless](0024-spawn-watchtower-swaggers-with-interactive-claude-never-clau.md)
- [ADR-0025: Two-layer colour model — Colour as Brand vs Colour as Data](0025-two-layer-colour-model-colour-as-brand-vs-colour-as-data.md)
- [ADR-0026: Design-lint built as a standalone staged dark-factory tool; placement left open](0026-design-lint-built-as-a-standalone-staged-dark-factory-tool-p.md)
- [ADR-0027: Jump aliases for apps use the full project name, never an abbreviation](0027-jump-aliases-for-apps-use-the-full-project-name-never-an-abb.md)
- [ADR-0028: Close the KDD/Lisa read-gate — the write loop is built, read enforcement is not](0028-close-the-kdd-lisa-read-gate-the-write-loop-is-built-read-en.md) — **accepted** (ratified 2026-07-04; already acted on — see Revision Log)
- [ADR-0029: Spec method for DF-7: keep appydave:spec-writer as baseline, adopt Osmani structural elements rather than switching wholesale](0029-spec-method-for-df-7-keep-appydave-spec-writer-as-baseline-a.md)
- [ADR-0030: Hand-write one recipe (N=1) before building an automated recipe-builder](0030-hand-write-one-recipe-n-1-before-building-an-automated-recip.md)
- [ADR-0031: Multi-Marshall parallelism via identity, not per-file locking](0031-multi-marshall-parallelism-via-identity-not-per-file-locking.md) — **accepted** (ratified 2026-07-04)
- [ADR-0032: apps/watchtower is the durable home; experiments/watchtower-engine is a disposable proof-of-concept](0032-apps-watchtower-is-the-durable-home-experiments-watchtower-e.md)
- [ADR-0033: Close the dispatch engine's return leg (engine→Switchboard→board) before adding the talk-to-it trigger](0033-close-the-dispatch-engine-s-return-leg-engine-switchboard-bo.md)
- [ADR-0034: Collapse the Mocha Census rating scale from good/meh/shit to love/good/average + free-text label](0034-collapse-the-mocha-census-rating-scale-from-good-meh-shit-to.md)
- [ADR-0035: Design-quality lever is structure + exemplars, not DESIGN.md token expansion](0035-design-quality-lever-is-structure-exemplars-not-design-md-to.md)
- [ADR-0036: Consolidate comprehend-visualise into Mochaccino as a 4th mode; restore the shape-warrant gate](0036-consolidate-comprehend-visualise-into-mochaccino-as-a-4th-mo.md)
- [ADR-0037: Leave CLAUDE.local.md without the system-context auto-import for Dark Factory](0037-leave-claude-local-md-without-the-system-context-auto-import.md)
- [ADR-0038: Upstream-repo writeups live in a new docs/upstream-repos/ shelf; actual repo clones live only in the canonical ~/dev/upstream/repos/ registry, never inside the dark-factory app](0038-upstream-repo-writeups-live-in-a-new-docs-upstream-repos-she.md)
- [ADR-0039: The untracked-rot sweep (DF-9) will detect and report git hygiene debt only — never auto-commit or auto-write .gitignore](0039-the-untracked-rot-sweep-df-9-will-detect-and-report-git-hygi.md)
- [ADR-0041: Record factory failures as a structured, countable register instead of narrating them in prose](0041-record-factory-failures-as-a-structured-countable-register-i.md)
- [ADR-0042: Dark-Factory Swagger is the aspirational descendant of BMAD Swagger, not an unrelated namesake](0042-dark-factory-swagger-is-the-aspirational-descendant-of-bmad-.md)
- [ADR-0043: Replace per-card 'promote' with a cluster CONVERGE flow for the Floor↔Lanes bridge](0043-replace-per-card-promote-with-a-cluster-converge-flow-for-th.md)
- [ADR-0044: Adopt a canonical DF-ADR format, modeled on Cortex's native template](0044-adopt-a-canonical-df-adr-format.md) — hand-authored, not Lisa-extracted; see [TEMPLATE.md](TEMPLATE.md) and [ADR-FORMAT-SPEC.md](../ADR-FORMAT-SPEC.md)
