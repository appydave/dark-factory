---
distillation_id: security-review-agent-config-scan
stage: security-review
intent: "Scan Claude Code configuration surfaces (.claude/ dir, CLAUDE.md, settings.json, MCP servers, hooks, agent prompts) for misconfigs, injection risks, and secret leakage using AgentShield"
created: 2026-05-17
status: draft
source_artifacts:
  - everything-claude-code:skill:security-scan
  - everything-claude-code:command:security-scan
  - everything-claude-code:agent:security-reviewer
  - everything-claude-code:skill:enterprise-agent-ops
winner_mechanism: everything-claude-code:skill:security-scan + everything-claude-code:command:security-scan
---

# Unified Skill: security-review-agent-config-scan

**Purpose**: Scan the Claude Code configuration surfaces of a project for security misconfigurations, injection risks, overly-permissive allow lists, and accidentally committed secrets — using the AgentShield scanner as the deterministic engine.

**For Agents**: Use when David says "scan my claude config", "check for security issues in the harness", "audit my hooks", "review my MCP setup", "AgentShield scan", or before committing changes to `.claude/` directories.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Detect exploitable security issues in the Claude Code harness config itself — not application code. The attack surface is: CLAUDE.md (prompt injection), settings.json (overly-permissive allow lists, dangerous bypass flags), MCP servers (hardcoded secrets, npx supply chain risks), hooks (command injection via interpolation, data exfiltration), and agent prompts (unrestricted tool access, missing model specs). Uses AgentShield as the scanner; the skill provides judgment on top of raw findings.

## Winner's Mechanism

`everything-claude-code:skill:security-scan` + `everything-claude-code:command:security-scan` form a two-layer winner:

- **Skill layer**: Defines the five surfaces to scan, what "bad" looks like per surface (table), AgentShield install/run mechanics, and a precedence rule: "Do not invent findings — use AgentShield output as source of truth and separate scanner facts from follow-up judgment."
- **Command layer**: Adds a structured output contract (security grade + score, counts by severity, critical/high findings with paths, auto-fix protocol), CI pattern (GitHub Actions with `fail-on-findings: true`), and argument hints (`[path] [--format] [--min-severity] [--fix]`).

The combination is directly actionable. David has no equivalent — no skill currently audits `.claude/` config surfaces. This is a clean gap.

## Non-overlapping ideas folded in

- From `everything-claude-code:agent:security-reviewer`: The **Prompt Defense Baseline block** — six lines that should appear in every agent prompt handling untrusted content. The config scan should flag agent prompts that are missing this block as a medium-severity finding. — `complexity: low | optional: false | prerequisite: none`. Missing in the skill, present in the agent file.
- From `everything-claude-code:skill:enterprise-agent-ops`: **Security boundary checklist for long-lived agents** (auth scoping, data access minimization, lifecycle controls). When the scan surfaces an agent prompt without role/tool constraints, use this checklist to frame the remediation. — `complexity: medium | optional: true | prerequisite: "project has long-running or daemon agents"`. Elevates the skill from scanner to advisor.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| security-scan (skill) | Five-surface scan table, AgentShield install/run mechanics, "no invented findings" rule, min-severity filter | Community-install instructions for repo-scan (different skill) |
| security-scan (command) | Output contract, CI pattern, argument hints, auto-fix protocol | ECC-specific preamble framing |
| security-reviewer (agent) | Prompt Defense Baseline block as a finding criterion | Full OWASP Top 10 application review (covered by code-review-security-specialist) |
| enterprise-agent-ops | Security boundary checklist for long-lived agents | Observability and lifecycle sections (separate distillation) |

## Draft SKILL.md frontmatter

```yaml
name: security-scan-agent-config
description: >
  Scan the Claude Code configuration (.claude/ dir, CLAUDE.md, settings.json, MCP servers,
  hooks, agent prompts) for security misconfigs, injection risks, overly-permissive allow lists,
  hardcoded secrets, and missing Prompt Defense Baselines.
  Uses AgentShield as the deterministic engine; adds judgment on top of findings.
  Use when: "scan my claude config", "audit my hooks", "check my MCP setup",
  "AgentShield scan", "security check before committing to .claude", "is my harness safe".
argument-hint: "[path] [--min-severity low|medium|high|critical] [--fix]"
allowed-tools: "Bash(npx ecc-agentshield:*), Bash(npm:*), Read, Write"
```

## Open questions for David

- AgentShield is an ECC-community npm package (`npx ecc-agentshield`). Is this acceptable as a hard dependency, or should the skill fall back gracefully to a manual checklist when AgentShield isn't installed?
- Should the Prompt Defense Baseline check be part of this skill (config-level) or stay in `review-security` (code-level)? The current split is: this skill checks if agent prompts have the block; `review-security` checks if application code sanitizes untrusted content properly.
- CI gate: Is adding `fail-on-findings: true` to GitHub Actions something David wants for SupportSignal's `.claude/` directory?
