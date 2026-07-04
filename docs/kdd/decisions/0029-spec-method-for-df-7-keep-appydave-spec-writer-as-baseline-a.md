> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0029: Spec method for DF-7: keep appydave:spec-writer as baseline, adopt Osmani structural elements rather than switching wholesale

**Status:** Proposed (reconstructed)


## Context
DF-7 (Switchboard state-plane spec) already had a baseline spec written with `appydave:spec-writer`. The Osmani plugin (`agent-skills@addy-agent-skills`) had just been installed, and its `spec-driven-development` skill needed a graduation test: run the same DF-7 requirement through Osmani's method and adversarially compare the result against the appydave baseline to decide whether Osmani should become a first-class spec method here.

## Decision
Run both methods on the same DF-7 requirement (Osmani pass produced `df7-switchboard-state-plane-spec.osmani.md`) and adjudicate with an adversarial delta critique (`df7-osmani-vs-appydave-delta.md`). Verdict: the appydave:spec-writer baseline remains the stronger from-scratch spec document; Osmani did not graduate to replace it. However, specific structural elements Osmani contributed are worth folding into the baseline method going forward: a hard three-tier Boundaries block (Always / Ask-first / Never), an explicit Commands section, and checkbox Tasks each carrying Acceptance + Verify + Files.

## Alternatives Considered
(a) Fully switch to Osmani's spec-driven-development skill as the canonical spec method — rejected, produces a weaker document from scratch. (b) Discard Osmani entirely and keep appydave:spec-writer unchanged — rejected, it ignores genuine structural wins Osmani surfaced (e.g. a real gap: the baseline never stated Switchboard's build/test commands, which Osmani's template forced into visibility as an Ask-first item). (c) Hybrid — adopted: keep appydave:spec-writer as the primary method, backport Osmani's Boundaries/Commands/checkbox-Task structure into it.

## Consequences
appydave:spec-writer is a candidate for enhancement with Osmani's three-tier Boundaries block, Commands section, and per-task Acceptance+Verify+Files structure. Osmani's spec-driven-development skill is not adopted as this project's primary spec method. The adversarial-delta technique (run both, critique hard, recommend canonical) is validated as the mechanism for resolving A-vs-B forks between candidate methods/tools.

## Related
- Sessions: ca7000ef

## Provenance
- **Sessions** (1): ca7000ef · 2026-06-08
- **Files** (candidate-level): backlog/specs/df7-osmani-vs-appydave-delta.md, backlog/specs/df7-switchboard-state-plane-spec.md, backlog/specs/df7-switchboard-state-plane-spec.osmani.md
- **Commits** (candidate-level): —
