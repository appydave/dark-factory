export const meta = {
  name: 'daily-review',
  description: 'End-of-day digest: what the factory did today, what needs David, what looks idle/stale',
  phases: [{ title: 'Review' }],
}

// Workflow = SOP-in-data (docs/sop-lifecycle.md). The cheapest facet of the
// self-watching loop: "what did the smart-but-non-communicative workers do today?"
// Script body has no filesystem/Bash — gathering happens inside the agent.

phase('Review')

const DIGEST_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['date', 'headline', 'activity', 'needs_review', 'idle_or_stale'],
  properties: {
    date: { type: 'string', description: 'the review date / window' },
    headline: { type: 'string', description: 'one terse line summarising the day' },
    activity: {
      type: 'array', items: { type: 'string' },
      description: 'what actually happened — terse bullets, grounded in command output only',
    },
    needs_review: {
      type: 'array', items: { type: 'string' },
      description: "things only David can decide or should look at — decisions, open questions, divergences",
    },
    idle_or_stale: {
      type: 'array', items: { type: 'string' },
      description: 'workflows/docs/state that look abandoned, unused, or two approaches that diverged without reconciliation (the "two workers" drift problem)',
    },
  },
}

const since = (args && args.since) || '1 day ago'

const digest = await agent(
  `You are the Dark Factory's daily reviewer. Produce a TERSE end-of-day review. Short phrases, no prose walls (David's style).

Work from the repo root. Gather real activity by running these shell commands and reading the output — do NOT invent anything:
- git log --since="${since}" --oneline --stat
- git status --short                         (uncommitted work in flight = today's unsaved activity)
- ls -t experiments/watchtower-engine/runs/ experiments/watchtower-engine/done/ experiments/watchtower-engine/failed/ 2>/dev/null
- ls backlog/*.md backlog/*.done.md 2>/dev/null   (open vs closed tickets)
- tail -n 40 backlog/problems.md             (the problem register)

Then synthesise into the schema:
- activity: what actually happened today.
- needs_review: decisions/open questions for David, and any DIVERGENCE between two approaches (the "two workers" problem — someone went a different direction and dropped earlier ideas).
- idle_or_stale: a workflow/doc/state file that was active and now isn't, or work left mid-flight.

If a source is empty, say so rather than padding. Ground every bullet in command output.`,
  { label: 'daily-review', schema: DIGEST_SCHEMA }
)

return digest
