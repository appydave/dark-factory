# David Style Patterns

**Purpose**: Concrete examples of David's voice + structural patterns for canonical artifacts. The canon to mimic when rewriting.

**For Agents**: Read before writing any canonical SKILL.md. Pair with `canonical-form-spec.md` (rules) — this file is the *embodiment* of the rules.

**Created**: 2026-05-18
**Last Updated**: 2026-05-18 *(seed version — refine as canonical artifacts get ratified)*

---

## David's existing skills as the reference corpus

Read these for voice + structure before rewriting any canonical:

| Pattern | Read | What to mimic |
|---------|------|---------------|
| **Fan-out orchestrator** | `~/dev/ad/appydave-plugins/appydave/skills/delivery-review/SKILL.md` | Single-sentence purpose; sub-agent table; "Output" section spec |
| **Single-axis specialist** | `~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md` | Tight purpose; concrete trigger phrases; "Don't" anti-patterns |
| **Data-pipeline orchestrator** | `~/dev/ad/appydave-plugins/appydave/skills/omi/SKILL.md` | Phase sequence; cross-skill handoffs; idempotency notes |
| **Cross-machine command** | `~/dev/ad/appydave-plugins/appydave/skills/remote-machines/SKILL.md` | Operator instructions; SSH/Tailscale conventions; safety rails |
| **Knowledge-capture** | `~/dev/ad/appydave-plugins/appydave/skills/capture-context/SKILL.md` | Session handover format; what to write where |
| **Multi-mode skill** | `~/dev/ad/appydave-plugins/appydave/skills/ralphy/SKILL.md` | Mode table; per-mode behavior block; hard-gate (post-2026-05-17 upgrade) |

## Voice — the rules in 8 lines

1. **Operator, not assistant.** "Do X. Then Y." Not "This skill will help you do X."
2. **Terse.** One sentence beats two. Two beat three.
3. **Tables for comparable structure.** Specialists, modes, criteria — all tabular.
4. **No marketing.** No "powerful", "comprehensive", "robust", "seamlessly". Just what the thing does.
5. **Triggers in the description, workflow in the body.** Never reverse.
6. **Stack-agnostic.** "Run the project's test command." Never "Run `npm test`."
7. **One CTA per section.** Don't ask the agent to do three things at once.
8. **Don't repeat content.** If something's in `behavior`, don't restate it in `output`.

## Structural templates

### Template A — Single-purpose skill (most common)

```markdown
# <Title>

<One-sentence purpose statement. What it accomplishes when fired.>

## Behavior

<3-7 lines of imperatives. What the agent does in sequence. No verbose explanation.>

## Output

<Where the result lands. Format. Structure. What the user will see.>

## Anti-patterns

- <Concrete don't #1>
- <Concrete don't #2>
- <Concrete don't #3>
```

### Template B — Orchestrator skill (fan-out)

```markdown
# <Title>

<One-sentence purpose: fans out to N specialists and merges findings.>

## Behavior

<How the orchestrator decides what specialists to dispatch.>

## Specialists

| Specialist | Concern | Output JSON |
|------------|---------|-------------|
| `<name-1>` | <one-line concern> | `{findings: [...]}` |
| `<name-2>` | <one-line concern> | `{findings: [...]}` |

## Output

<How findings are merged. Where the synthesized report lands.>

## Anti-patterns

- Sequential dispatch instead of parallel (defeats the orchestrator)
- Specialists writing files directly (reviewers never write)
- <one more>
```

### Template C — Multi-mode skill (like ralphy)

```markdown
# <Title>

<One-sentence purpose covering all modes.>

## Modes

| Mode | Fires when | Output |
|------|-----------|--------|
| `<mode-1>` | <trigger condition> | <result> |
| `<mode-2>` | <trigger condition> | <result> |

## Mode <mode-1> behavior

<3-7 lines>

## Mode <mode-2> behavior

<3-7 lines>

## Anti-patterns

- <one>
- <two>
```

## Frontmatter exemplars

### Trigger-only description (good)

```yaml
description: >
  Resolve PR review feedback — evaluate validity, fix valid issues in parallel,
  reply to threads, close them via GraphQL. Use when: 'resolve PR feedback',
  'address review comments', 'fix the review comments', 'reply to PR threads',
  'close review threads', 'the reviewer said X, should I fix it?'.
```

### Workflow summary (BAD — do not write this)

```yaml
description: >
  This skill helps you handle PR feedback. It will read all the review comments,
  decide which are valid, fix them one at a time, then reply to each thread
  and mark them resolved on GitHub.
```

(The bad one tells the LLM what the skill does. The LLM then decides it can skip the body. The trigger-only version tells the LLM *when to fire* without revealing the workflow — so the LLM must load the body to know how to execute.)

## Common rewrites (origin pattern → David pattern)

| Origin pattern | David's rewrite |
|----------------|-----------------|
| "This skill provides comprehensive code review across multiple dimensions..." | One sentence: what it does. |
| "By following this workflow, you'll be able to..." | Cut entirely. Use imperatives. |
| "It is important to note that..." | Cut. State the rule directly. |
| Multi-paragraph behavior section | Numbered list, ≤7 items. |
| "Tools used: Bash, Read, Edit, Write" buried in prose | Move to `allowed-tools` frontmatter. |
| Marketing adjectives ("powerful", "advanced", "intelligent") | Delete. Adjectives don't trigger skills. |

## Stack-locked → stack-agnostic rewrites

| Origin (stack-locked) | David's rewrite (agnostic) |
|------------------------|------------------------------|
| "Run `npm test` to check tests pass" | "Run the project's test command. Determine it from the project's package manifest or architecture doc." |
| "Use `gh pr create` to open a PR" | (Acceptable — `gh` is harness-agnostic, not language-specific. Keep.) |
| "Format with `prettier --write .`" | "Run the project's formatter. Determine from the project's architecture doc." |
| "Lint with `eslint --fix`" | Same as above. |
| "The TypeScript types should..." | (Either cut or generalize to "The project's type system should..." — depends on context.) |

## To be expanded

This file is a seed. As canonical artifacts get ratified, append new patterns + new anti-patterns + new exemplars seen in the rewrites. The pattern: when you find yourself making the same rewrite decision twice, document it here so the next agent doesn't have to re-derive it.
