---
artifact_id: agent-skills-osmani:skill:git-workflow-and-versioning
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [delivery-readiness, code-implementation]
phase_fit: [3, 4, 6]
evaluated_at: 2026-05-17
---

# Eval: git-workflow-and-versioning

**Intent**: Enforce disciplined git workflow (trunk-based development, atomic commits, descriptive messages, scope separation, worktrees for parallel agents) as the safety net for AI-accelerated code generation.

## Scores
- **quality_score**: 5 — Trunk-based development with DORA research citation, atomic commit discipline, worktrees for parallel AI agent work, "DIDN'T TOUCH" change summary pattern, pre-commit hygiene steps, and a dedicated "Using Git for Debugging" section (bisect, blame, log --grep) are all production-grade. The "change summaries" section is the single most agent-specific addition in any git skill.
- **adoption_fit_final**: strong — Language/stack agnostic. The worktrees-for-parallel-agents section directly aligns with Ralphy's campaign model. The "DIDN'T TOUCH (intentionally)" change summary pattern is directly adoptable.
- **inspiration_value**: high — The change summary format with "THINGS I DIDN'T TOUCH (intentionally)" and "POTENTIAL CONCERNS" sections is a novel addition to standard git guidance — specifically designed for AI agent output review. The "Dev branches are costs" framing is direct and quotable.
- **uniqueness_refined**: uncommon — The agent-specific worktrees section and the structured change summary format (with deliberate non-touch declaration) are not found in other git skills. Core git principles are commodity; these additions are rare.
- **composability**: called-by-others — Referenced by incremental-implementation (Step 4: Commit) and the build command.
- **description_craft_refined**: trigger — Description uses "Always. Every code change flows through git." — a bold, unconditional trigger statement that is unusual but effective.

## Mineable phrasing
> "THINGS I DIDN'T TOUCH (intentionally): ... This shows you exercised scope discipline and didn't go on an unsolicited renovation."

## Notes
The "DIDN'T TOUCH" section in the change summary template is the most practically useful agent-specific addition to standard git guidance in the corpus — it turns implicit scope discipline into an explicit artefact that reviewers can verify. The trunk-based development framing with the explicit "Dev branches are costs" statement (not the standard "use short-lived branches") is sharper and more memorable. The combination of worktrees + Ralphy campaign model creates a natural alignment: Ralphy's Mode 3 Build already uses worktrees; this skill provides the disciplined commit practices that make those worktrees clean and reversible.
