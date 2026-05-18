---
artifact_id: appydave-plugins:skill:ansible-fleet
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, knowledge-capture, orchestration]
phase_fit: [6, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: ansible-fleet

**Intent**: Provides a workflow layer over David's Ansible-provisioned Mac fleet — three capabilities: fleet audit (drift report), capability lifecycle (add/deprecate with automation-compatibility gate), and config variation management (explaining where a setting lives).

## Scores

- **quality_score**: 4 — The skill is tightly scoped and practical. The Ansible-compatible/NOT-compatible classification gate is excellent — it prevents the most common mistake (auto-generating a playbook for a GUI-install-only app). The output shapes (Markdown + JSON dual output for fleet audit) show real operational thinking. The "Never auto-run playbooks" rule is load-bearing. Minor deduction: the skill is narrow to David's specific fleet topology and hard-wires machine names, making it less reusable as a pattern example.
- **adoption_fit_final**: strong — This skill already exists in David's stack (it is his). The evaluation purpose here is to assess whether it should inspire patterns elsewhere or be upgraded. The Ansible-compatible classifier and the three-capability structure are the reusable design ideas. Deeply integrated with `~/dev/ad/agent-os/ansible/` — not Ruflo-dependent.
- **inspiration_value**: mid — The classifier gate pattern (hard no before generating anything) is the mineworthy idea. The dual-output (human Markdown + machine JSON) is also worth noting as a pattern for operational skills.
- **uniqueness_refined**: uncommon — Fleet audit skills that operate over declarative config (not live SSH checks) are not common. The automation-compatibility gate before generation is distinctive.
- **composability**: standalone — Calls no other skills; is called by users directly. References ansible brain but not as a dependency.
- **description_craft_refined**: trigger — Description contains rich trigger phrases ("audit fleet", "check drift", "provision machine") and capability summary. Well-formed for a complex skill.

## Mineable phrasing

> "Never auto-run playbooks. Always generate the diff and wait for approval."

## Notes

The skill's Ansible-compatible classification gate is a portable dark-factory pattern: before generating any infrastructure artifact, classify whether automation is actually feasible, and if not, produce manual instructions and stop. This prevents both wasted effort and false confidence. The fleet topology section is David-specific but the three-capability structure (audit, lifecycle, config-variation) is a reusable shape for any declarative-config-managed system (Ansible, Terraform, etc.). No Ruflo dependency.
