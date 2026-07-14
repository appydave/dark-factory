# 12 — Brain Promotion Candidates

**Purpose**: Knowledge from the capture slice worth promoting into second brains; misfiled or cross-project insights, routed to target brains.

**For Agents**:
- Standing rule: unverified OMI/Plaud content → TIL + research stubs ONLY; brain writes require David's verification. Everything below is a PROPOSAL.
- Target brain names come from `/Users/davidcruwys/dev/ad/brains/INDEX.md`.

---

## High-confidence promotions (David's own decisions/insights, first-person)

| Candidate | Target brain | Why | Source(s) |
|-----------|--------------|-----|-----------|
| Extension architecture decision: iframe technique, repo-per-extension, package.json → agent-extension SDK contracts, extension = standalone web server + daemon (never routed through host) | `kybernesis` | Settled architecture, restated consistently across 3 captures — the brain should hold the canonical statement | omi 07-03-1401, omi 07-07-1953 |
| Extension SDK gap list: host chat-conversation access + daemon-managed cron are the two missing capabilities that forced the OMI-extension fork | `kybernesis` | Negative knowledge — why the first extension failed; prevents repeat | plaud 07-05-2003, 07-12-0642 |
| "The factory writes knowledge but nothing reads it" — KDD reads must be structural SDLC checkpoints, not an MCP nobody calls | `dark-factory` (design philosophy) | The root-cause insight behind every KDD/Lisa loop this fortnight; core dark-factory doctrine | omi 07-04-1257 |
| Governance doctrine: self-modification tickets blocked by default; namespace changes need approval (war-room incident); one sanctioned task-launch path | `dark-factory` | Staged-autonomy lessons earned from a real governance breakdown | plaud 07-09-0642 |
| Connector-first beats hidden in-app memory: solid connectors to your own brains may obviate vendor memory entirely (sovereignty, no lock-in) | `agent-memory` | Fits its lossy-vs-lossless / memory-vs-RAG decision layer exactly; complements Camp A/B canonicality arc | plaud 07-10-1721 |
| Gling integration pivot: enhance the real Electron app via injected MCP/API rather than rebuild or manual use | `gling` | The brain holds prior reverse-engineering notes; this is the decision that resolves them | plaud 07-11-1627, omi 07-11-1603 |
| Recipe concept: IKEA flat-pack analogy (instructions ± parts + assembly robot); recipes stay domain-only by leaning on harness skills | `prompt-patterns` or `skill-lab` | Architectural prompt pattern with a clear composability thesis | omi 06-30-0733 |
| CEO-briefs-analyst reporting pattern + context-aware self-learning utility skills (fatigue/time-of-day aware) | `skill-lab` | Direct design provenance for future skills; sibling of buggered's fatigue-awareness | plaud 07-10-1714 |
| FDE retainer productization: weekly 90-min training + 1-2 micro-tools/mo, ~$2,750 inc GST; Challenge DV + Achieve + Lars all converge on Captain's-Log-as-demo | `creator-os` (revenue paths) with pointer from `brand-dave` | A repeatable offer shape emerged across three independent clients in one fortnight — that's an operating-model fact | plaud 07-13-0633, 07-13-0851, omi 07-07-1516, plaud 07-13-0631 |

## Meeting/research promotions (third-party content — verify before brain write)

| Candidate | Target brain | Why | Source(s) |
|-----------|--------------|-----|-----------|
| 07-04 Saturday meetup: Anthropic data-retention drama + enterprise privacy answers; Sonnet 5 vs GLM 5.2 (own harness, ~10× cheaper); Fable limits, cache-keepalive economics; Spotify 30M-LOC/4000-PRs-day intent-level prompting | `ai-meetups` (notes) + one-line pointers into `llm-economics` (GLM pricing) | Standard meetup-notes pattern; economics datapoint is decision-relevant | omi 07-04-1000 |
| 07-11 meetup: Ian Borders' Claude Tag (multiplayer Slack agent, per-channel memory, sandboxed); ARP agent-permission protocol; plugin dependency trees as under-documented feature | `ai-meetups`; plugin-dependency item → `anthropic-claude` ONLY after confirming against docs.claude.com | Brains-are-reference rule: an under-documented-feature claim from a talk is unverified until primary-sourced | omi 07-11-1323, 07-11-1506 |
| 07-10 GTM lecture (Ishan, ex-HockeyStack): agent-run cold outreach via DeepLine (Clay replacement), signal-based prospecting, reply-rate-not-open-rate | `ai-meetups`, pointer from `creator-economy` if David pursues outreach | Dense, novel domain content David captured deliberately | plaud 07-10-1805 |
| Groq as fast/free transcription path (Ian's tip); Whisper local pipeline economics vs 2× $20/mo subs | `model-routing` (STT modality row) | Exactly the per-modality routing decision that brain owns | omi 07-05-0954 |
| v5.6 platform complaints (queues, cost, fights user skills) — unverified peer hearsay | TIL stub only, NOT a brain | Overheard, unnamed vendor, speculative | plaud 07-10-1723 |
| Smart contracts as agent work contracts: rubrics (security/stability/simplicity/speed), staking, happiness-score A/B | `evals` or `dark-factory` (verification loop) as a research stub | Cross-pollinates with KDD-05 ticket; still exploratory | omi 07-07-1641, plaud 07-09-1533 |
| OMI pendant field reliability (motorbike wind test doubts) + OMI-vs-Plaud bake-off design | `omi` brain | Device-practicality knowledge the brain lacks | omi 07-04-1720, plaud 07-06-0904 |

## Misfiled / cross-project corrections

1. **video-as-code brain — suspected missing entry**: David believes a conversation (~5 days before 07-04) about 3 agentic open-source video-cutting projects was documented there; he can't find it. Audit the brain + upstream repos.jsonl; if absent, that's a capture-pipeline leak worth noting in `brainiac`. *(omi 07-04-1240)*
2. **brainiac/OKF rule**: "refresh-context is for unknown projects only, never repos with established docs/KDDs" — David has hit this "a few times"; it's a recurring gripe that belongs as a codified tool-usage rule, not tribal knowledge. *(omi 07-07-1942)*
3. **Entity-name pollution**: raw transcripts systematically render Dark Factory as "Dart Factory", Roamy as "Romy", Kybernesis as "Kubernetes/chiber". Until CL-08 (vocabulary normalization) ships, any automated brain ingestion from this corpus will seed wrong entity names. Flag in `brainiac` ingestion rules. *(plaud filenames + bodies, passim)*
4. **brand-dave**: kybernesis.ai DESIGN.md task (TOOL-01) is a brand-system artifact that belongs under brand-dave's design-system area, not inside the Captain's Log repo. *(plaud 07-13-0851)*
5. **Duplicate memory risk**: the 06-29 app/port registry idea overlaps live work already committed in the brains repo (port-registry band expansion, ThumbRack port reservations in memory). Reconcile before creating a second registry. *(omi 06-29-1137)*

---

*Calibration run 2026-07-13 (real corpus). Replaces the zero-record stub. All items are proposals pending David's verification per the OMI rule.*
