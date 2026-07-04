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
