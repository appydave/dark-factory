---
distillation_id: security-review-secret-detection
stage: security-review
intent: "Pre-commit and pre-push gate that detects secrets (API keys, tokens, passwords, credentials) hardcoded in source, logs, or commit history before they leave the machine"
created: 2026-05-17
status: draft
source_artifacts:
  - everything-claude-code:skill:security-review
  - everything-claude-code:skill:security-bounty-hunter
  - everything-claude-code:command:security-scan
  - everything-claude-code:agent:security-reviewer
winner_mechanism: everything-claude-code:skill:security-review (secrets section) + everything-claude-code:agent:security-reviewer
---

# Unified Skill: security-review-secret-detection

**Purpose**: Lightweight pre-commit/pre-push gate that sweeps staged changes and commit history for hardcoded secrets — API keys, tokens, passwords, credentials — before they leave the machine. Operates at lower cost than a full security review; designed to run on every commit.

**For Agents**: Use when David says "check for secrets before committing", "scan for hardcoded credentials", "is there an API key in this diff", "git history secrets scan", "pre-commit secret check". Can also auto-trigger from kcommit hooks.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Surface hardcoded secrets in staged changes, working tree, or git history before they hit remote. Secrets in source are the single highest-frequency, easiest-to-prevent security failure mode in solo/small-team dev. The goal is speed: this must run in seconds, not minutes, so it stays on the commit path.

## Winner's Mechanism

The ECC `security-review` skill has the clearest secret-detection section in the corpus — it provides:

1. **FAIL/PASS code examples** (TypeScript) — exact bad vs. good patterns with verification steps
2. **Five concrete checks**: no hardcoded keys/tokens/passwords, all secrets in env vars, `.env.local` in `.gitignore`, no secrets in git history, production secrets in hosting platform
3. **Regex patterns** for common secret formats (from `security-reviewer` agent): `sk-proj-`, `gh_`, bearer tokens, private keys

The `security-reviewer` agent adds the **runtime scan command**: `grep -rE "(api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]{8,}" --include="*.ts,*.js,*.py,*.rb,*.env*"` — a zero-dependency shell one-liner that works before any CI tooling is installed.

`security-bounty-hunter` confirms the attack surface: "Hardcoded API keys or secrets in source" is the first entry in the in-scope bounty pattern table, confirming this is real-world impact territory.

## Non-overlapping ideas folded in

- From `everything-claude-code:skill:security-bounty-hunter`: **Git history scan** — secrets committed then "deleted" remain in git history. Add `git log -p --all --grep="key\|secret\|password\|token" -- | grep "+" | grep -iE "key|secret|password|token"` as a second sweep. — `complexity: low | optional: false | prerequisite: none`. ECC security-review only checks staged/working files; history is the escape hatch attackers use.
- From `everything-claude-code:command:security-scan`: **Output contract** — even a lightweight scan should return (a) finding count, (b) exact file:line per finding, (c) severity (CRITICAL for clearly exposed keys, HIGH for probable keys). — `complexity: low | optional: false | prerequisite: none`. Formats findings for quick triage.
- From `everything-claude-code:skill:security-review`: **`.env` file guard** — verify `.env`, `.env.local`, `.env.*.local` are in `.gitignore` before every commit, not just at project setup time. — `complexity: low | optional: false | prerequisite: none`. Projects drift; gitignore entries get removed.

## Existing-skill nesting

David has `kcommit` (commit quality gate). Secret detection is a natural pre-commit hook running **inside** kcommit's staged-changes check, before the commit message is drafted.

- **Existing mechanism**: `kcommit` checks commit message quality, conventional commit format, and staged file list.
- **New mechanism's grain**: per-commit, runs on staged diff + `git log -p` for history sweep (on first run or after gap).
- **Existing mechanism's grain**: per-commit, runs after staging, before commit message.
- **Nesting rule**: secret-detection runs as a **blocking gate** before kcommit proceeds. If secrets found: surface findings, halt commit, wait for David to confirm intentional (test fixture) or fix. If clean: kcommit continues normally. This matches how CE's commit gates compose — each gate is a distinct concern that chains.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| security-review (skill) | FAIL/PASS patterns, 5-check list, `.gitignore` verification step | Full OWASP checklist (belongs in security-specialist) |
| security-reviewer (agent) | Grep one-liner, secret format regex patterns | OWASP review workflow (separate scope) |
| security-bounty-hunter | Git history scan command, "hardcoded secrets = real bounty impact" framing | Full bounty submission workflow |
| security-scan (command) | Output contract format (count + file:line + severity) | AgentShield dependency (too heavy for pre-commit) |

## Draft SKILL.md frontmatter

```yaml
name: security-scan-secrets
description: >
  Pre-commit and pre-push gate that sweeps staged changes and git history for hardcoded secrets:
  API keys, tokens, passwords, credentials. Zero external dependencies — runs grep patterns
  against staged diff and git log. Designed for the commit path: fast, blocking, low noise.
  Use when: "check for secrets before committing", "scan for hardcoded credentials",
  "is there an API key in this diff", "git history secrets scan", "pre-commit secret check".
  Auto-trigger from kcommit hooks.
argument-hint: "[--staged-only] [--include-history]"
allowed-tools: "Bash(git:*), Bash(grep:*), Read"
```

## Open questions for David

- Should `security-scan-secrets` be a standalone invocable skill AND a kcommit hook, or only a hook (never called directly)?
- Should `.env` file validation (checking gitignore) be part of this skill or part of kcommit's existing checks?
- False-positive handling: test fixtures often contain fake-looking API keys. Should the skill check for a `# test-fixture` comment to suppress the finding, or always flag and let David confirm?
