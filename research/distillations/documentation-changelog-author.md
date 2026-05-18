---
distillation_id: documentation-changelog-author
stage: delivery-readiness
intent: "Maintain release-time documentation — changelogs, release notes, milestone summaries, post-ship doc updates"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-release-notes
  - gstack:skill:document-release
  - gsd:command:milestone-summary
  - agent-skills-osmani:skill:documentation-and-adrs
  - bmad-method:skill:bmad-agent-tech-writer
winner_mechanism: gstack:skill:document-release
---

# Unified Skill: changelog-author

**Purpose**: Update project documentation at ship time — cross-reference the diff against existing docs, update stale entries, flag gaps, and generate the changelog block for the release.

**For Agents**: Use when user says "update the docs after shipping", "write the changelog", "update release notes", "document this milestone", "docs are out of date after this PR". Not for pre-ship doc generation (that's `doc-write`).

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Maintain the living documentation layer at ship time: cross-reference what shipped against what docs claim, update stale entries, and output a changelog block in the project's existing format.

## Winner's Mechanism

`gstack:skill:document-release` is the winner because it operates at the correct grain: **post-ship, cross-reference-first**. The mechanism reads all project docs, compares against the changes just shipped, and updates any doc that is now stale — rather than generating docs from scratch or querying an external API.

This is the highest-leverage moment for doc maintenance. Docs written before a feature ships are predictions; docs updated after a ship are facts.

`ce-release-notes` is a strong alternative but it solves a different sub-problem: it queries the upstream changelog API for a known plugin and renders a readable summary. Valuable for consumers of a plugin (including David's team learning what's in compound-engineering). Not the mechanism for maintaining David's own project docs.

`gsd:command:milestone-summary` adds a valuable idea: generating a **stakeholder-facing summary** (plain English, no technical jargon, shareable with non-engineers) from planning artifacts. That's a distinct output that belongs alongside the technical changelog, not instead of it.

## Non-overlapping ideas folded in

- From `gsd:command:milestone-summary`: stakeholder-facing milestone summary — generate a plain-English summary from planning artifacts (wave files, task items) for sharing with clients or non-engineers — `complexity: low | optional: true | prerequisite: "GSD planning artifacts exist (wave files, milestone.md)"`. Most valuable on client projects (SupportSignal) where delivery summaries go to stakeholders.

- From `compound-engineering:skill:ce-release-notes`: phase-based fetch + soft-cap rendering — useful model for how to present changelog content with a 25-line soft-cap and markdown-fence-awareness when rendering — `complexity: low | optional: false | prerequisite: none`. Applies to David's own `CHANGELOG.md` rendering for any release summary output.

- From `agent-skills-osmani:skill:documentation-and-adrs`: explicit rule "don't delete old decisions" — new ADRs supersede via reference, never by deletion — `complexity: low | optional: false | prerequisite: none`. ADR lifecycle management belongs in any documentation-maintenance skill.

- From `bmad-method:skill:bmad-agent-tech-writer`: voice discipline — write in a consistent editorial tone (imperative voice, active sentences) rather than letting LLM drift into passive-heavy documentation prose — `complexity: low | optional: false | prerequisite: none`.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `gstack:document-release` | Post-ship cross-reference + stale-doc update mechanism | gstack-specific binary dependencies (make-pdf etc.) |
| `ce-release-notes` | Soft-cap rendering + phase-based API fetch model | CE-specific GitHub API + Python helper dependency |
| `gsd:milestone-summary` | Stakeholder-facing summary from planning artifacts | GSD wave-file dependency (optional fold-in, not core) |
| `agent-skills-osmani:documentation-and-adrs` | ADR non-deletion rule + `CHANGELOG.md` format example | Full ADR authoring workflow (different concern, see `adr-author`) |
| `bmad-agent-tech-writer` | Imperative voice + editorial tone discipline | BMAD persona wrapper (not needed in David's system) |

## Draft SKILL.md frontmatter

```yaml
name: changelog-author
description: "Update project documentation at ship time — cross-reference what shipped against existing docs, update stale entries, generate changelog block in project format. Use when: 'update the docs', 'write the changelog', 'document this milestone', 'release notes', 'docs are stale', 'what changed in this release'."
argument-hint: "[version tag, milestone name, or blank to use HEAD vs previous tag]"
allowed-tools: Bash(git *), Bash(gh *), Read, Edit, Write
```

## Open questions for David

1. **Scope**: Should `changelog-author` also handle ADR creation at ship time (when the ship constitutes a significant architectural decision), or is ADR authoring a separate skill? ADRs are low-frequency; bundling might cause scope creep.

2. **`CHANGELOG.md` format**: David's repos don't have a consistent changelog format yet. Should this skill enforce Keep-a-Changelog (the Osmani example), Conventional Commits-derived, or infer from the existing file?

3. **Stakeholder summary**: The GSD milestone-summary idea is most valuable on client projects. Should it be an `--stakeholder` flag on this skill, or a separate `milestone-summary` skill?
