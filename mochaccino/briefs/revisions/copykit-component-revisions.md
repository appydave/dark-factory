# Copy Kit — shared component · Revisions

## 2026-05-22 — initial build
- **Brief**: David wants every render to have a copy button + per-section checkboxes, so he can select how many sections to copy to the clipboard and feed them back as context.
- **Shelly/component**: created designs/components/copykit.css + copykit.js (reusable, brand-styled).
  - Per-block checkbox chip (top-right, dims until hover/checked; lighter variant on dark blocks).
  - Floating toolbar (bottom-right): "all" master toggle · "N / total selected" count · "Copy selected" · "Copy all".
  - Copies as markdown: `# {page title}` then `## {section label}` + section innerText. Toast confirms + shows ~KB.
  - navigator.clipboard with execCommand fallback (localhost is a secure context, so clipboard API works).
  - MutationObserver re-scan (debounced, busy-guarded) so JS-rendered pages (01/02/03, which fetch JSON then build DOM) get chips after async render.
- **Per-page wiring** (head <link> + pre-</body> config + script):
  - 01 .stage · 02 .card · 03 .summary-row,.table-wrap · 04 .arch,.contracts,.oscar,.eav,.skills
  - 05 .probe · 06 .hero,.lens,.lineage,.converge,.xpoll,.verdict · 07 .legend,.wf · gallery .design
- **Verified**: node --check passes; css/js serve 200; all 8 pages carry the includes. Browser-level (chip render / copy) left for David — Chrome had no DevTools debug port for MCP attach.
- **Skill note**: this is a cross-cutting component, not a single design. Lives in designs/components/ (Shelly's territory). Future designs should include it by default — candidate for a workspace Rule.
