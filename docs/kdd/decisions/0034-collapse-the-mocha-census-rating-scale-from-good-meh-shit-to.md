> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0034: Collapse the Mocha Census rating scale from good/meh/shit to love/good/average + free-text label

**Status:** Proposed (reconstructed)


## Context
The first rating round (good/meh/shit) was meant to teach a design-taste model David's boundary between acceptable and bad work. Analysis then revealed the entire 'shit' tier was actually broken renders (data-fetch 404s), carrying no genuine design signal. David also wanted a way to record *why* he rated something, and wanted headroom above 'good' now that a false floor was gone.

## Decision
Replace the three-tier good/meh/shit scale with love-it/good/average, add a free-text label field per design, and re-seed the board from round-01 (good→good, meh→average, broken/shit designs left unrated) so David edits an existing pass rather than starting blank. Keyboard shortcuts kept on the left home row (A/S/D).

## Alternatives Considered
Keep good/meh/shit and just teach the extractor to exclude 'shit' entries at analysis time — rejected because the tier itself was misleading to rate against going forward, and it gave no headroom to distinguish merely-good from exceptional work.

## Consequences
Prior round-01 ratings needed a lossy re-map (meh→average) rather than a clean carry-forward. Tier counts are not stable across rounds — round-02 produced 47 'love' ratings, round-03 gave only 1 for largely the same designs — so the spec had to explicitly note that labels and relative ordering are the durable signal, not raw tier counts, or later analysis would misread rating drift as new information.

## Related
- Sessions: f2df9480

## Provenance
- **Sessions** (1): f2df9480 · 2026-06-08
- **Files** (candidate-level): tools/mocha-census/out/ratings/round-01.json, tools/mocha-census/out/shots/gallery.html
- **Commits** (candidate-level): —
