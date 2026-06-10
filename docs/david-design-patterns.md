# David's Design Patterns — derived from rated work

**Status:** v2, from Mocha Census **round-02** (2026-06-08) — 156 of David's own designs rated on a
**love it › good › average** scale *with free-text labels* (the why, in his words).
**Method:** screenshots + mechanical feature-extraction (`extract.py`) + render-health filtering
(`check-health.py`) + label-theme mining. Source: `tools/mocha-census/out/ratings/{round-02,features,health,exemplars}.json`.
This is a *render-conditioning* spec. Brand colour/type tokens stay in DESIGN.md.

---

## ⚠️ CORRECTION (2026-06-09, round-04 feedback) — diagrams are SPARING, not the default

**This spec over-weighted "diagram/SVG" and it caused real harm.** The designs David loved that
*happened* to be flows/topologies (wave-*, agentic-os, the brain decks) made the `svg` feature average
higher in the love tier. That is **selection, not a rule.** Read as a prescription ("draw it as a
diagram"), it pushed the `comprehend-visualise` skill to convert *everything* to SVG node-graphs —
collapsing the varied, reliably-good HTML that is Mochaccino's actual strength. **David never asked for
a shape engine.** He praised shapes *used sparingly, where they genuinely made sense*, and the **eye for
where**. Everything below about "diagram = top love-trigger" is **overridden by these rules:**

- **HTML is the default and the strength.** Clean, varied, semantic HTML layouts are the baseline and
  the point — NOT a deficiency to be "fixed" by adding a diagram. Six months of good HTML is the asset.
- **Diagrams/shapes are situational and sparing.** Draw a diagram ONLY when the *content itself* is a
  flow / topology / relationship and a diagram genuinely clarifies it. Otherwise don't. **Never convert
  a working HTML layout wholesale to SVG.** Do **not** optimise `svg` count — it is descriptive, not a
  target. The judgment of *where a shape earns its place* IS the skill; it can't be reduced to a rule.
- **The data agrees:** a large share of the 46 love-tier exemplars are pure HTML with **no diagram** —
  `lexi-profile`, `layout-28/29`, the homepages, the ghost-text dashboards. Diagram is ONE love-form
  among several, apt for flow content only.
- The **form-agnostic** love-triggers still hold: disciplined semantic block colour, ghost text, kill
  orange-on-brown, ease density. It was specifically *"diagram = the gate to love"* that was wrong.

---

## Colour as Brand vs Colour as Data — the two-layer model (2026-06-10)

David's keystone colour rule, named by the `/frontend-design` lens and ratified by him:
**two palettes, two jobs, never swapped.** Designs feel right when each layer stays in its lane;
they break when one invades the other.

**① Colour as Brand** (warm — *the house*). Source of truth: `appydave/DESIGN.md`.
brown `#342d2d` · cream `#faf5ec`/`#f0ebe4` · gold `#ccba9d` · **yellow `#ffde59` (the bright
highlight / attention)** · amber `#c8841a` (numbered sequences 01/02/03 ONLY). **Job:** identity +
*content emphasis* — "this is AppyDave, look here, this matters." This is the **load-bearing** palette;
it carries every screen.

**② Colour as Data** (cool — *the diagram furniture*). Source of truth: `aitldr/semantic-colors.md`
(*"status signals and data category colors — not replacements for brand colors… they supplement the
brand palette"*). green/blue/purple/teal. **Job:** *structural/categorical encoding* — stages, roles,
nodes, pros/cons, legend keys. Layered **on top of** the warm base; **never replaces** it.

**The orange resolution (David, 2026-06-10): role right, value wrong.** "Kill orange-on-brown" never
meant "delete the warm highlight" — it meant *that muddy amber had no contrast on brown/beige.* The
brand's bright warm highlight is **yellow `#ffde59`** (real punch on brown AND cream); **amber
`#c8841a` is restricted to 01/02/03 numbered sequences**, never as fill or text-on-tint. The fix to a
brand-cold screen is **restore yellow as the warm anchor**, not add more cool.

**Two tests — apply BOTH before using Colour as Data:**
1. **Role test.** Is the coloured element *structure* (a stage / node / role / legend key in a diagram
   or an ordered set)? Then cool semantic is licensed. Is it *content* you read as substance (a card
   that is the point, not a node)? Then it wants **brand emphasis (warm)**, not a category colour.
2. **Dominance / anchor test.** Warm brand stays **load-bearing**; every screen keeps **≥1 bright warm
   anchor** (yellow). Cool semantic is a **sparing accent**. A cool-only screen reads off-brand
   (generic technical SaaS), even when nothing is technically "wrong."

**Diagnosis — the cortex "brain" deck (4 screens, 2026-06-10):** cool semantic was made *load-bearing*
on **content** cards (region tiles, memory-kind tiles) and warm brand — yellow especially — was
dropped → **brand-cold**. This is the predictable overshoot from round-04's "use semantic block colour
/ kill orange." His own gradient confirms the two tests: *Anatomy* (cool on content, no warm) =
worst; *Four-memories* (cool on content, a little ghost-text warmth) = better; *Remembers* (cool
anchored to a real diagram) = ok; *Sleeps* (cool on genuine ordered stages) = the right use. Fix:
restore yellow/cream as load-bearing, keep cool only on the genuine flow/legend elements.

> AppyDave brand reinforces this directly: *"Blue is a cool guest in a warm house — never a background
> fill."* The cortex deck used cool fills/top-bars as the dominant treatment. That is the violation.

---

## Slide Round 01 (2026-06-10) — RESTRAINT: colour must never overpower

**103 slides rated** (BMAD Solo Deck + POEM): **2 love · 24 good · 76 average.** That huge "average"
pile is the finding — most slides aren't *wrong*, they're **over-coloured**. David, in his words:
*"I didn't quite understand just how bad the colour stuff was — really bad contrast between the dark
browns and overuse of dark semantic colours."* The two-layer model (above) governs **where** colour
goes; this round adds the axis it was missing — **how much / how strong.** Both layers can be placed
correctly and the screen still fails by being *loud*.

**Both LOVE-tier slides win on the same word — "never overpowering":**
- `zero-to-app-chapters`: *"different stages, each gets its own colour section. **It's not overpowering.**"*
- `bmad-agents-presentation` (off-brand!): *"uses colour really well **without any colour ever overpowering.**"*
Off-brand colour can still reach LOVE if it is restrained. Loud on-brand colour cannot.

**The failure tally (from the labels, not impression):**

| signal | count | reading |
|---|--:|---|
| **OVERLOAD** — "too many colours / too bold / too heavy / overboard / flamboyant / busy" | **12** | the #1 failure, bigger than orange-on-brown by volume |
| **SINGLE-HUE FLOOD** — "too much green", "purple all the way through / on its own" | **10** | one hue flooding a whole slide reads wrong & childish |
| **CONTRAST fail** — "bad contrast / ugly pairing / harsh" (4 name dark brown) | **9** | esp. cool/saturated colour *on dark brown* |
| **UGLY/HORRIBLE/BROKEN/MESSY** | 7 | the worst cases — all over-coloured or clashing |
| *(positive)* SUBTLE / soft / toned / "not overpowering" | 8 | the winning move |
| *(positive)* BRAND-ONLY / yellow-on-brown | 6 | restraint + brand = reliably good |

**The reliable rules this adds (repeated many times — encode these):**

1. **Restraint is the master rule — colour must never overpower.** Fewer colours, used meaningfully.
   This sits *above* the two-layer model: even correctly-placed semantic colour fails if it shouts.
2. **Saturation/weight is a real axis, not just hue.** *"Too bold", "too heavy", "tone it down."* The
   winning pattern is a **mostly-neutral ground (grey/cream) + ONE semantic accent** — exemplar
   `cicd-phased-rollout`: *"only green made it in, everything else grey… very good."* (David's explicit
   caveat: he floated transparency but said *"don't make that a rule"* — so the rule is **soften /
   fewer**, not "use transparency.")
3. **A single hue flooding a slide fails.** Semantic colour **discriminates among items**; it is never a
   flood-fill of one colour. *"Purple all the way through isn't the best."*
4. **Contrast on dark brown is a hard constraint.** Dark brown takes **yellow / light-brown / white**
   well; **blue / green / purple / orange on dark brown reads badly** (generalises *kill orange-on-brown*).
   *"contrast issues, especially dark brown against blue."*
5. **Don't pile semantic colour ON brand colour densely** — David's named root cause: *"the real issue
   is mixing all the colours with the brand colours."* Keep ONE layer dominant, the other sparse
   (the density corollary to the two-layer model).
6. **One colour, one meaning, used once** — *"they only use each colour once, which is fine."*
7. **One pop is loved; a slide of pops is noise.** An unexpected stand-out colour on ONE element is a
   delight (*"look at me, I'm interesting"*, the pink `taylor`); the same multiplied reads childish.

> Net: the slide corpus says David's taste is **disciplined restraint**, not richness. The
> highest-leverage instruction to any render agent is now *"use fewer colours, softer, mostly neutral
> + one accent — never let colour overpower the content,"* layered on top of the where-rules above.

---

## Headline (revised from v1): tier is composition; the recurring *flaw* is colour

Round-01 said "taste = composition, not tokens." Round-02's labels **refine that**: which *tier*
something lands in is driven by composition + diagram + colour-discipline — but the single most
repeated *complaint*, even on designs he **loves**, is a specific colour failure. Both matter.

**What pushes a design to LOVE** (clean designs, love vs good vs average):

| signal | love | good | avg | read |
|---|--:|--:|--:|---|
| **svg** (diagram/flow) | **3.5** | 0.6 | 0.3 | love = *drawn as a diagram*, not laid out |
| **distinct colours** | **13** | 19 | 19 | love = **fewer**, disciplined, semantic |
| grid | 5.6 | 4.8 | 2.3 | more deliberate grid composition |
| sidebar | 4.3 | 1.8 | 0.7 | rich multi-panel chrome, fully developed |
| cards | 12 | 5 | 14 | card *count* no longer the tell — *use* is |

> LOVE = a **diagram with curvy connectors / legend / input-output header**, in a **disciplined,
> semantic, fewer-colour palette** (block/section colour-coding), often with **ghost text**. GOOD =
> competent but flat (no diagram, no colour-blocking). AVERAGE = thin card-grid (14 cards, ~490 lines,
> no diagram).

---

## The #1 fix: orange/amber on brown/beige

**13 separate gripes about "orange on brown/beige" — spanning average, good, AND love.** He loves a
design and *still* docks the orange. Verbatim: *"dontrealy like the analytics highlight orange on
brown"*, *"orange boxes on the beige don't look that good"*, *"orange on is a bit wrong"*, *"love it,
accept for the orange on the banner"*, *"I don't like the orange on brown text but the use of colours
throughout is good"*. This is the highest-leverage single change to his entire body of work.

**Rule (refined 2026-06-10 — see the two-layer model above):** the failure was the *value*, not the
*concept*. Muddy amber `#c8841a` as text/fill on brown/beige fails (poor contrast, reads cheap) — but
the warm-highlight *role* is right and necessary. **Use yellow `#ffde59` as the bright warm highlight**
(real contrast on brown and cream); keep **amber `#c8841a` for 01/02/03 numbered sequences only**;
never warm-on-matching-tint. Do NOT over-correct into a cool-only palette — that goes brand-cold (the
cortex deck). Cool semantic set (green/blue/purple) is for *structural blocks/diagrams*; warm yellow is
the *content/attention* anchor. Both layers present, each in its lane.

---

## ✅ VALIDATED (round-03): good → love

`05-dark-factory` v1 (good, *"busy"*) was re-rendered to this spec as `05-dark-factory-v2` and rated
**love** — the *only* love in David's entire round-03 re-rate. The spec moved a design up a tier. One
refinement from his label, now folded in below:

- **Colour belongs in the blocks, not the connectors.** *"I like the green, orange, blue on the box,
  but not so much on the lines — simpler lines would have been fine."* Semantic colour on
  boxes/lanes/tiles = yes; connector lines should be **thin and neutral** (small colour-dots at the
  endpoints are fine as a cue). Bold coloured curves are one step too much.

> **Methodology — tiers drift, labels don't.** Round-02 had 47 "love"s; round-03 had 1. David applies
> "love" *comparatively* and recalibrates each session. Don't track tier *counts* across rounds —
> anchor on the **labelled reasons** and the **relative ordering**. The labels are the stable signal.

## DO — what he loves (named in his words)

1. **Diagram / flow — ONLY for flow content, sparingly** (see the CORRECTION above; this is *not* the
   default). When the content genuinely IS a flow/topology, a drawn diagram is loved: *"curvey lines"*,
   *"the legend"*, *"inputs/outputs near the top"*, *"schema render EAV Envelope"* — thin/neutral
   connectors, colour in the blocks not the lines. But ~half the love exemplars use NO diagram; do not
   force one onto layout/document content.
   *(flow exemplars: wave-bar, wave-subagents, wave-handover, agentic-os 04, dark-factory 06/07/08.)*
2. **Disciplined semantic block colour** — *"wonderful use of block colours with contrast"*, *"mixed
   block/section colors"*, *"greens, blues, purple and orange for highlights"*. Alternating
   cream/dark-brown section **bands** + per-block accent. **Fewer** colours used meaningfully (13 vs 19).
   *(lexi-profile, frontmatter-examples, layout-29.)*
3. **Ghost text** — oversized tone-on-tone background lettering as a graphic device. His signature
   favourite: **27 label mentions** (loved it even on broken appyradar shells where it was *all* that
   rendered). *(appyradar suite, lexi-profile, layout-29 "angular ghost text".)*
4. **Uniqueness / asymmetry / randomness** — *"I like the randomness"*, *"unique elements in the yellow
   area"*, *"random shapes around AD"*, *"liked that this one was vertical"*. Reward the unexpected.

## CAPS at good (never love)

- **Off-brand palette** — flihub `recording-editor/relay-redesign/sync-hub` all *"not my brand
  color"* → all rated good, none love. Off-brand has a ceiling.
- **No semantic colour-blocking / no ghost text / off-spec colour** — a clean layout is already good;
  what lifts it to love is the *form-agnostic* set (semantic block colour, ghost text, apt structure),
  NOT adding a diagram. (Earlier wording here — "flat = no diagram" — was the over-weighting error;
  corrected. Many love-tier designs are flat HTML.)

## AVERAGE / fix-don't-learn

- **Card sprawl + thin** — 14 cards, ~490 lines, svg 0.3. The undifferentiated tile grid.
- **Broken renders (33 labels say "broken")** — appyradar suite + chain-* + several angeleye 404 their
  data and draw a shell. *Not a design verdict.* Always run `check-health.py` and exclude these.

## Watch-outs (soft dings, appear even on loves)

- **Busy / dense** (8 mentions: *"a bit busy"*, *"information dense"*, *"over the top with coloured
  blocks"*). Loved despite it — but ease density.
- **Too much dark brown** (*"overuse of dark brown near the footer"*, *"a little dark"*).
- **Childish iconography** (*"messy and childish with the icons"* — chat-panel-b top bar).

---

## Exemplar pack

46 **love-tier** clean designs in `tools/mocha-census/out/ratings/exemplars.json` (with his note per
design); screenshots in `out/shots/<repo>__<design_id>.png`. Lead references by archetype:

- **diagram-flow:** angeleye `wave-bar`, `wave-subagents`, `wave-handover`, `reference-landscape`
- **semantic-block + ghost text:** appydave-plugins `01-lexi-profile`, `02-frontmatter-examples`;
  appydave.com `layout-29`, `layout-28`
- **structured-layout:** appydave.com `homepage-authority/builder`, `layout-07/15/16/17/26`
- **diagram decks:** ruflo `01/03/06/07/08/09/10`, agentic-os `04-agent-orchestration`,
  dark-factory `06-blackboard-vs-poem`, `07-workflow-flows`, `08-poem-consolidation`

---

## Wire-in + eval loop

1. **Two layers:** DESIGN.md keeps colour/type; add this doc's grammar + the love-tier exemplar pack
   as positive references to the `frontend-design` / Mochaccino render step. Add the orange-on-brown
   rule as a hard DON'T.
2. **Eval target (concrete):** `05-dark-factory` is now rated **good** with label *"busy"*. Path to
   **love** = reduce density + kill orange-on-brown + add a diagram legend/I-O header. Re-render and
   re-rate — good→love is the measurable proof the skill internalised this.
3. **Every round:** `check-health.py` first; rate only clean renders.
