# KDD Uniformity Findings — for Roamy / Lisa standardization (2026-07-04, from m4)

The kdd-viewer now scans all four KDD instances as a uniformity probe. David's hypothesis
("if you can't read one, we've got systemic problems") CONFIRMED — 3 of 4 structurally divergent:

| Instance | Verdict | Top divergence |
|---|---|---|
| SupportSignal | clean | — (the reference shape) |
| dark-factory | divergent | decision `provenance:` is NESTED yaml — flat parsers silently lose files/commits |
| Cortex | divergent | decisions have ZERO frontmatter — title/status/supersedes only in body prose |
| KBDE | divergent | same profile as Cortex |

Since Cortex/KBDE decisions are Lisa-EMITTED, the divergence is in Lisa's emit path, not human
sloppiness → fix once in Lisa, re-emit. Also: only ONE real supersede link exists in the whole
corpus (dark-factory ADR-0020↔0021). Cortex's proposed-adrs/ staging split no longer exists
(merged flat). Full detail: ~/dev/ad/apps/kdd-viewer/docs/extension-notes.md + view/index.html.

## STATUS — emit path FIXED (2026-07-04, Roamy; Lisa v5.12.1, commit `b416ccb`)

Root cause confirmed and narrower than "the emit path": `emit`'s decision candidates always
carried full flat frontmatter — it was **`reconcile-existing`** (the stage that writes the final
staged ADRs) that took body-from-heading and dropped the YAML. Fixed: staged decisions now carry
`adr_number/title/status + created/story_reference/provenance/files/commits (carried flat) +
supersedes/superseded_by`. Verified on the cached DF run — full frontmatter, identical triage
counts. `/plugin` update to **5.12.1** on any machine that runs reconstructions.

Two corrections to this note's framing, grounded:
- **"Cortex is Lisa-emitted" is only half true.** Cortex's native ADR format (its own ADR-0001,
  hand-authored 2026-05-27, pre-dating the reconstruction) has no YAML frontmatter *by design*
  (`**Status:**` inline), and its Lisa batch was normalized INTO that house format at
  ratification. Cortex's shape is a ratified host choice, not Lisa damage. KBDE (100% Lisa-raw,
  no prior format) is the true emit-path casualty.
- **"Re-emit" is not the fix for existing corpora.** Reconstruct is one-shot per project, and
  KBDE's 48 ADRs went through human triage (25-item noise purge, adversarial drop-review) —
  re-emitting would trample that. Retrofitting frontmatter onto KBDE's existing 48 is a
  one-time doc migration on the KBDE machine (mechanical: title/status already sit in each
  body), not a Lisa re-run. Dark Factory already has full DF-ADR frontmatter from its reformat.

Open question for David (not acted on): dark-factory's **nested** `provenance:` block in DF-ADR
frontmatter — flat parsers lose files/commits. Options: (a) consumers use real YAML parsing
(kdd-viewer's normalize-first adapter can), or (b) DF-ADR flattens to `files:`/`commits:` at top
level like Lisa's emit now does. Lean (b) for uniformity, but it's a DF-ADR format decision
(ADR-0044 territory), not a silent fix.
