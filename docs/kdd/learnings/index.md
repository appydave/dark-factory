# Learnings (49)

> Reconstructed from session transcripts, 2026-07-04. Status: proposed.
> +4 live-captured 2026-07-11 (dark-factory-c2 session); 1 bump (job-agents skip bookkeeping → ×3, promotion-eligible).

## architecture (6)

- [medium] [Atomic queue-claim mutex for concurrent file-based polling](atomic-queue-claim-mutex-for-concurrent-file-based-polling-kdd.md)
- [medium] [Bulk structured data should move via manifest files, not through an LLM agent](bulk-structured-data-should-move-via-manifest-files-not-thro-kdd.md)
- [medium] [Constellation-first placement: shared-state fixes belong in a service, not the engine](constellation-first-placement-shared-state-fixes-belong-in-a-kdd.md)
- [high] [KBDE extension channel handlers can't be wired additively](kbde-extension-channel-handlers-can-t-be-wired-additively-kdd.md)
- [medium] [Mochaccino gallery index is hand-written HTML, not generated from a manifest](mochaccino-gallery-index-is-hand-written-html-not-generated--kdd.md)
- [medium] [Switchboard has no generic event-ingest endpoint](switchboard-has-no-generic-event-ingest-endpoint-kdd.md)

## debugging (7)

- [medium] [Backtick inside a JS comment prematurely terminated a template literal](backtick-inside-a-js-comment-prematurely-terminated-a-templa-kdd.md)
- [medium] [Drift check conflated activity status with liveness](drift-check-conflated-activity-status-with-liveness-kdd.md)
- [medium] [Flex child with explicit pixel width still shrinks and clips](flex-child-with-explicit-pixel-width-still-shrinks-and-clips-kdd.md)
- [medium] [Guard module-level server.listen() on import](guard-module-level-server-listen-on-import-kdd.md)
- [low] [JS let TDZ ordering with shared polling state](js-let-tdz-ordering-with-shared-polling-state-kdd.md)
- [medium] [Mocha Census design-id regex assumed single-level paths, corrupting nested design ids](mocha-census-design-id-regex-assumed-single-level-paths-corr-kdd.md)
- [medium] [Sandbox PATH stripped in piped subshells](sandbox-path-stripped-in-piped-subshells-kdd.md)

## documentation (2)

- [high] [Doc-drift audit found docs silently out of step with shipped code](doc-drift-audit-found-docs-silently-out-of-step-with-shipped-kdd.md)
- [low] [Durable memory retains an entity's old name after a real-world rename](durable-memory-retains-an-entity-s-old-name-after-a-real-wor-kdd.md)

## infrastructure (6)

- [high] [Engine has no HITL-park state — a designed decision-pause is read as a wedged worker](engine-has-no-hitl-park-state-designed-pause-read-as-wedged-kdd.md)


- [medium] [Dev server cache-busting gap serves stale content after re-render](dev-server-cache-busting-gap-serves-stale-content-after-re-r-kdd.md)
- [high] [Dynamic Workflow tool args parameter didn't reliably bind to the script's args global](dynamic-workflow-tool-args-parameter-didn-t-reliably-bind-to-kdd.md)
- [medium] [Engine queue directories vanished mid-run from a concurrent process reset](engine-queue-directories-vanished-mid-run-from-a-concurrent--kdd.md)
- [medium] [Parallel worker claim-binding race between spawned windows and tickets](parallel-worker-claim-binding-race-between-spawned-windows-a-kdd.md)
- [low] [Shared browser automation tool locked by a concurrent Claude Code session](shared-browser-automation-tool-locked-by-a-concurrent-claude-kdd.md)

## process (13)

- [low] [Blind git add in a dirty shared working tree risks sweeping in unrelated files](blind-git-add-in-a-dirty-shared-working-tree-risks-sweeping--kdd.md)
- [medium] [Build/dev-history claims stated without verifying against git history](build-dev-history-claims-stated-without-verifying-against-gi-kdd.md)
- [high] [Claims asserted from inference/memory without checking the actual evidence](claims-asserted-from-inference-memory-without-checking-the-a-kdd.md)
- [medium] [Design charter grounding needs direct design-origin docs, not just transcript-mining](design-charter-grounding-needs-direct-design-origin-docs-not-kdd.md)
- [medium] [Design-lint index blind spot: gallery index page skipped by scoped tickets](design-lint-index-blind-spot-gallery-index-page-skipped-by-s-kdd.md)
- [medium] [Design-lint rubric built from a small sample missed the top real failure mode](design-lint-rubric-built-from-a-small-sample-missed-the-top--kdd.md)
- [high] [Job-agents complete work but skip writing handback/run-record bookkeeping](job-agents-complete-work-but-skip-writing-handback-run-recor-kdd.md)
- [high] [Marshall cold-start dispatch: acted instead of orienting and asking](marshall-cold-start-dispatch-acted-instead-of-orienting-and--kdd.md)
- [low] [Narrow research queries need explicit exclusion clauses to avoid generic adjacent results](narrow-research-queries-need-explicit-exclusion-clauses-to-a-kdd.md)
- [medium] [Parallel/concurrent work on the same artifact drifts or duplicates without coordination](parallel-concurrent-work-on-the-same-artifact-drifts-or-dupl-kdd.md)
- [medium] [Repo identity confusion over which repo is the correct sister project](repo-identity-confusion-over-which-repo-is-the-correct-siste-kdd.md)
- [high] [Untracked-file rot accumulated from unenforced end-of-session commit discipline](untracked-file-rot-accumulated-from-unenforced-end-of-sessio-kdd.md)
- [medium] [Worker session interviewed the human instead of resolving and terminating](worker-session-interviewed-the-human-instead-of-resolving-an-kdd.md)

## testing (3)

- [medium] [style-check checks form, not description↔body coherence (skill-creator caught what ours missed)](style-check-checks-form-not-description-body-coherence-kdd.md)


- [low] [Doc-review crossref scanner flagged markdown syntax examples in prose as broken links](doc-review-crossref-scanner-flagged-markdown-syntax-examples-kdd.md)
- [high] [Indirect render signals (HTTP 200, headless screenshot, SVG count) wrongly trusted as proof of a working render](indirect-render-signals-http-200-headless-screenshot-svg-cou-kdd.md)

## tooling (12)

- [high] [Verify ran per-line against main, not the worker's worktree — worktree artifacts invisible, correct work false-failed](verify-block-ran-per-line-against-main-not-the-worker-worktree-kdd.md)
- [high] [War-game Verification blocks false-fail good work via authoring bugs (placeholder / inverted grep / cross-line $VAR)](wargame-verification-blocks-false-fail-good-work-via-authoring-bugs-kdd.md)
- [medium] [Bash cwd drift across tool calls from an earlier relative cd](bash-cwd-drift-across-tool-calls-from-an-earlier-relative-cd-kdd.md)
- [low] [Census batch field mislabeling](census-batch-field-mislabeling-kdd.md)
- [medium] [Constellation paths authored as prose, not resolvable filesystem paths](constellation-paths-authored-as-prose-not-resolvable-filesys-kdd.md)
- [low] [Cross-machine push/pull conflicts need careful reconciliation, not blind stash/rebase](cross-machine-push-pull-conflicts-need-careful-reconciliatio-kdd.md)
- [low] [Edit/Write tool guard requires an explicit Read call, not cat or prior viewing](edit-write-tool-guard-requires-an-explicit-read-call-not-cat-kdd.md)
- [medium] [Existing skill/memory not consulted before building a solution from scratch](existing-skill-memory-not-consulted-before-building-a-soluti-kdd.md)
- [low] [Naive whole-file frontmatter scan risks false positives from body text](naive-whole-file-frontmatter-scan-risks-false-positives-from-kdd.md)
- [low] [Pre-taste-spec Mochaccino designs carry anti-pattern palettes needing systematic re-render](pre-taste-spec-mochaccino-designs-carry-anti-pattern-palette-kdd.md)
- [medium] [Self-skill corpus coverage gap in census scanner](self-skill-corpus-coverage-gap-in-census-scanner-kdd.md)
- [medium] [zsh unquoted variable word-splitting](zsh-unquoted-variable-word-splitting-kdd.md)

