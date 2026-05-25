# 07 · The Four Workflows — Revisions

## 2026-05-21 — initial build
- **Brief**: David noted we visualised the pattern (04) and the probe timeline (05) but never the four workflows *as workflows*. Wanted each to read like a flowchart/diagram.
- **Peter**: created data/blackboard-workflows.json — 4 workflows transcribed verbatim from ylo-experiment/{workflow.json, workflow-titles.json, workflow-titles-human.json, workflow-thumbnails.json}. Node legend + per-workflow structure type (fan-out / linear-loop / linear-branch / linear-pipeline).
- **Mocha**: rendered designs/07-workflow-flows/index.html. Four distinct diagram grammars: (1) seed→12-chip fan-out→join; (2) linear with attempt badges + loop-back note; (3) linear→human gate→2-way branch; (4) 5-stage pipeline with fan-out ×6/×3 badges + file-output badges. Node colour-coded by type (transform/checkpoint/human/action/seed) per legend.
- **Housekeeping**: gallery card + intro line added; mockups.json updated (now 01–07 registered).
- **Faithfulness**: diagrams are 1:1 with the JSON — step ids, stores keys, inputs, fanOut counts, models, outputKeyMap, accept keywords all sourced from the specs, not invented.
