---
repo: poem
github: private (David Cruwys)
local_path: /Users/davidcruwys/dev/clients/supportsignal/prompt.supportsignal.com.au
context_md: /Users/davidcruwys/dev/clients/supportsignal/prompt.supportsignal.com.au/CONTEXT.md
recon_date: 2026-05-16
recon_iteration: 2
scope_note: SPECIAL SCOPE RULE — only 2 agents in scope (Penny, Alex). Other agents listed for completeness; marked out-of-scope.
---

# Recon: POEM (Prompt Orchestration & Engineering Method)

**Maintainer**: David Cruwys (private)
**Version sampled**: active development — no stable release tag observed

> **Iteration 2 note**: Iteration 1 (same date) used the wrong local path (`~/dev/ad/poem-os/poem/`) and cataloged Victor instead of Alex. Victor is a valid POEM agent but was NOT in scope. Alex (`alex.md`) exists at the correct canonical location (`/Users/davidcruwys/dev/clients/supportsignal/prompt.supportsignal.com.au/.claude/commands/poem/agents/alex.md`) and was missed entirely in iteration 1. This iteration 2 corrects both issues: correct repo path, correct agent pair (Penny + Alex).

---

## Top-level layout

```
prompt.supportsignal.com.au/
├── .claude/
│   └── commands/
│       └── poem/
│           └── agents/           ← Claude Code slash-command agent wrappers
│               ├── alex.md       ← IN SCOPE
│               ├── penny.md      ← IN SCOPE
│               ├── field-tester.md  (out of scope)
│               ├── oscar.md         (out of scope)
│               └── victor.md        (out of scope)
```

---

## Artifact types found (scoped to 2 agents)

| Type | Location | Count | Naming | Frontmatter? | Sample file |
|------|----------|-------|--------|--------------|-------------|
| Agent (slash-command wrapper) | `.claude/commands/poem/agents/` | 5 total; **2 in scope** | `{name}.md` lowercase | No YAML frontmatter — YAML embedded inside fenced code block within body | `penny.md`, `alex.md` |

### Agent body structure (both in-scope agents)

Both files follow the same BMAD-powered pattern:

```
# /poem/agents/{name} Command
<!-- Powered by BMAD™ Core -->
# {agent-id}
ACTIVATION-NOTICE: ...
## COMPLETE AGENT DEFINITION FOLLOWS - NO EXTERNAL FILES NEEDED
```yaml
IDE-FILE-RESOLUTION: ...       ← hybrid dev/prod path logic (identical in both)
REQUEST-RESOLUTION: ...        ← flexible intent → command matching
activation-instructions: [steps]
agent:
  name: {Name}
  id: {id}
  title: {Title}
  icon: {emoji}
  whenToUse: ...
  customization: null
persona:
  role: ...
  style: ...
  identity: ...
  focus: ...
core_principles: [list]
commands: [list with * prefix convention]
dependencies:
  workflows: [...]
  data: [...]
  skills: [...]
```
## Agent Behavior
[Detailed prose expansion of each command]
ARGUMENTS: {any arguments passed to the command}
```

Key structural notes:
- The YAML block is the machine-readable spec; the prose section below is human/agent documentation.
- YAML references external dependency files resolved via hybrid dev/prod path logic.
- All agents declare `ACTIVATION-NOTICE: DO NOT load any external agent files` — fully self-contained on activation, lazy-loading externals only when a command is invoked.

---

## In-Scope Agents (2)

### Penny — Prompt Engineer

- **File**: `.claude/commands/poem/agents/penny.md`
- **Agent id**: `prompt-engineer`
- **Title**: Prompt Engineer
- **Icon**: ✍️
- **whenToUse**: Use for creating, refining, testing, and validating AI prompts with systematic workflows
- **Persona**: Expert Prompt Engineer & Template Architect — methodical, quality-focused, educational; guides users through structured prompt creation using POEM principles
- **Commands** (all `*` prefixed): `*help`, `*new`, `*refine`, `*test`, `*validate`, `*exit`
- **What she does in one sentence**: Walks users through the full prompt lifecycle — create Handlebars template + JSON schema, refine iteratively, test with mock data, validate structure — using POEM-principled workflows.
- **Dependencies**: 4 workflows (`new-prompt.yaml`, `refine-prompt.yaml`, `test-prompt.yaml`, `validate-prompt.yaml`), 3 data files (`poem-principles.md`, `prompt-best-practices.md`, `schema-quality-improvements.md`), 3 skills (`check-my-prompt.md`, `preview-with-data.md`, `generate-schema.md`)

---

### Alex — Workflow Architect

- **File**: `.claude/commands/poem/agents/alex.md`
- **Agent id**: `workflow-architect`
- **Title**: Workflow Architect
- **Icon**: 🏗️
- **whenToUse**: Use for designing and creating workflow YAML definitions that orchestrate multiple prompts
- **Persona**: Workflow Architect & Orchestration Designer — conversational, analytical, design-focused; translates user goals into executable workflow definitions through interviews and analysis
- **Commands** (all `*` prefixed): `*help`, `*design`, `*analyze`, `*generate`, `*validate`, `*refine`, `*exit`
- **What he does in one sentence**: Interviews users to understand orchestration goals, scans existing prompts, maps I/O data flow, and generates clean workflow YAML with human checkpoints and a companion `.usage.md` guide.
- **Dependencies**: 5 workflows (`design-workflow.yaml`, `analyze-prompts.yaml`, `generate-workflow-yaml.yaml`, `validate-workflow.yaml`, `refine-workflow.yaml`), 3 data files (`workflow-patterns.md`, `workflow-yaml-format.md`, `io-contract-guide.md`), 3 skills (`detect-data-flow.md`, `suggest-checkpoints.md`, `validate-io-compatibility.md`)
- **Role confirmation**: `agent.title` is explicitly `"Workflow Architect"` — matches David's description. David sometimes calls Alex "Alec"; the file is `alex.md`.

---

## Out-of-Scope Agents — listed for reference only

> Do NOT include in catalog unless David explicitly expands scope.

`oscar.md`, `victor.md`, `field-tester.md`

---

## Standout patterns

1. **YAML-in-markdown double-encoding**: Agent definitions embed a YAML config block inside a fenced code block inside a markdown file. This is the BMAD activation pattern — Claude reads the prose header, then parses the YAML block as operating instructions. No standalone `.yaml` agent files at the command-wrapper level.

2. **Self-contained by design**: Every agent file declares `ACTIVATION-NOTICE: DO NOT load any external agent files`. All config is inline. External files (workflows, data, skills) are only loaded on demand when the user invokes a specific command.

3. **Hybrid dev/prod path resolution**: All agents contain identical path-detection logic (`packages/poem-core/` = dev, `.poem-core/` = prod). This is shared infrastructure boilerplate, not agent-specific content.

4. **Alex's activation includes project-context scan**: Unlike Penny's activation (load config → greet), Alex's Step 4 actively scans `poem/prompts/`, `poem/schemas/`, and `poem/workflows/` to build an inventory of available prompts and their I/O contracts before greeting the user. This is a lightweight `system-comprehension` pattern embedded in the boot sequence.

5. **Penny → Alex handoff implied**: Penny creates prompts + schemas; Alex orchestrates them into workflows. The companion `.usage.md` Alex generates is explicitly noted as the artifact that Oscar reads ("Oscar reads the usage guide to understand how to run and test the workflow") — revealing a downstream agent dependency chain.

### Prompt-pattern signals

| Pattern ID | Where observed | Signal |
|------------|---------------|--------|
| `agent-handshake` | Both `penny.md` and `alex.md` — `activation-instructions` Steps 1-5 | Structured self-introduction: identity established via persona block, state set via env detection, comm protocol set via `*help` auto-run + HALT |
| `progressive-disclosure` | Both files — ACTIVATION-NOTICE + dependency lazy-loading | Top-level YAML always loaded; workflow/data/skill files only loaded when user selects a command |
| `system-comprehension` | `alex.md` activation Step 4 | Alex builds a mental model of the project (prompts, schemas, workflows inventory) before accepting input |
| `capability-description` | Both files — `whenToUse` field in `agent:` block | Trigger-only phrasing (≤1 sentence, WHEN condition) — classic Discovery Pattern `whenToUse` field |
| `orchestration-topology` | `alex.md` overall design | Conversational Delegation topology: Alex interviews → generates YAML that orchestrates multiple prompts as pipeline steps |

---

## Inclusion candidates for unified discovery

- **Penny** (`penny.md`) — primary prompt authoring agent; clear, stable, well-documented
- **Alex** (`alex.md`) — workflow orchestration designer; interview-driven, generates multi-prompt YAML pipelines

---

## Exclusion candidates

- `oscar.md`, `victor.md`, `field-tester.md` — explicitly out of scope for this recon pass
- External dependency files (`packages/poem-core/workflows/`, `data/`, `skills/`) — source artifacts referenced by agents; not the agent wrappers themselves

---

## Open questions

1. **Oscar downstream dependency**: Alex's behavior notes explicitly state "Oscar reads the usage guide." This implies Oscar is an execution agent in the pipeline. If scope expands, Oscar should be next in-scope after Penny + Alex.

2. **Penny's `schema-quality-improvements.md`**: This data dependency appears in Penny's file but not in the iteration 1 Victor recon — worth confirming this file exists in `.poem-core/data/` and is populated.

3. **Alex's `whenToUse` vs Penny's**: Both use the `whenToUse` field as a capability trigger. The discovery routing between them (who gets invoked for what) would benefit from a routing table — flagging for Phase 2 discovery.
