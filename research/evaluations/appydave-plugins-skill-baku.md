---
artifact_id: appydave-plugins:skill:baku
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-implementation, knowledge-capture, test-authoring]
phase_fit: [3, 4, 7, 8]
evaluated_at: 2026-05-17
---

# Eval: baku

**Intent**: Sync and manage Baku app zips from claude.ai (claude-ship exports) to a local versioned folder, grouping by app identity via component fingerprints.

## Scores
- **quality_score**: 3 — Functional, well-structured for its niche purpose. The fingerprinting approach (discriminating component filenames since `package.json` name is always `"my-app"`) is clever. Limited scope — this is a personal workflow tool, not a reusable mechanism.
- **adoption_fit_final**: mid — Directly relevant to David's Baku/claude-ship workflow. No external applicability; this is a first-party tool for managing a very specific artifact type.
- **inspiration_value**: low
- **uniqueness_refined**: rare — The component-fingerprint-based app identification approach is genuinely novel for the problem of undifferentiated claude.ai exports.
- **composability**: standalone — Self-contained sync workflow; no required dependencies.
- **description_craft_refined**: trigger — Rich trigger phrase list ("sync baku", "baku sync", "baku status", etc.).

## Mineable phrasing
> "All project-*.zip files have package.json name 'my-app' — useless. The script fingerprints each zip by its unique non-boilerplate component filenames."

## Notes
The fingerprinting problem (all exports look identical at the manifest level) is a real artifact management challenge that generalizes to any system producing undifferentiated bundles. In distillation, this clusters as a personal workflow tool rather than a unified skill candidate. The `--identify` flag using Claude CLI for LLM-based app naming is a neat composition pattern worth noting.
