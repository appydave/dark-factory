# PROOF — comprehend-visualise (Phase 1)

- **What it does:** points the factory at a repo/folder (local or remote-over-SSH), enumerates packages/DBs/components + 14-day git log, fans out cited parallel readers, merges a grounded `digest.md`, selects Mochaccino/Shelly shapes, and emits a provenanced render-`brief.json`. Comprehends only — never renders (that's Phase 2).
- **Where it lives:** `.claude/skills/comprehend-visualise/SKILL.md` (trigger-only desc, stack-agnostic, read-only on target, provenance = path + commit_sha).
- **Self-test target:** `experiments/watchtower-board` @ `ce9bad9` (small, local, real).
- **Result:** `digest.md` = 29 lines (file-cited, ✅/⚠️/❓ tagged); `brief.json` = valid JSON, **4 visualisations** (layer-stack, card-grid, lifecycle-flow, timeline), each with shape+title+source_files+shows. Artifacts under `experiments/watchtower-engine/proof/cv-selftest/`.
- **The ONE thing Phase 2 (Mochaccino render) needs from the brief:** `target.path` + `target.commit_sha` — the provenance Peter stamps as `meta.source` on every `data/*.json` so renders cite back to source and stay refreshable.
