# T1-16 — Durable verdict + Prior-chained ledger for crash-recovery

| field | value |
|---|---|
| ticket | wg-t1-16-durable-verdict-ledger |
| track / size / priority | T1 Engine / M / normal |
| executor | sonnet Swagger via engine (once T1-14 + T1-15 land) |
| depends_on | wg-t1-15-independent-reverify-at-reap (the verdict this ledger records) |
| authored | 2026-07-08, from BMAD-Swagger research (Swagger's Log + sprint-status Prior-chain) |

## Mission

BMAD Swagger survives session death because every gate writes a durable line into the artifact
itself (`## Swagger's Log`) plus a `# Prior:`-chained queue ledger with a `Next:` self-dispatch
pointer — a crashed supervisor resumes purely from disk with zero re-litigation of cleared gates.
The engine has `audit.jsonl` (dispatch history) but no consolidated, human-readable, per-ticket
verdict trail: when an orchestrator dies mid-run (as one did today), the story of what was tried,
verified, and decided is scattered across `running/`, `results/`, `audit.jsonl`, and worker
transcripts. This ticket adds a **durable verdict record** — each reap writes a compact,
append-only ledger line (ticket · attempt · verdict · evidence-source · timestamp · next-action)
into a single `engine/store/ledger.jsonl` AND embeds the final verdict into the ticket JSON on
settle — so a fresh session (or a human) reconstructs full state from disk alone. Done looks like:
every settled ticket carries an embedded `verdict` block; `ledger.jsonl` has one line per reap
outcome with a `prior` pointer to the ticket's previous attempt; and a `--resume` status read
reconstructs "what happened to ticket X and what's next" without reading any transcript.

## Locked context
- Q4: sonnet Swagger dispatch. Interactive claude only.
- Append-only (`engine/store/.CONVENTION.md` idiom) — never rewrite a ledger line; corrections are
  new lines. Mirrors `audit.jsonl`.
- Folds in T7-04 (decision-lineage): the ledger IS the lightweight one-line-per-decision log —
  do not build a separate ADR system.
- Retention interplay: T1-10 (store retention) must exempt or archive `ledger.jsonl`, not truncate
  it blindly — note the dependency, don't build T1-10 here.

## Recon (verify before any work)
1. `grep -n "def settle\|def commit\|audit.jsonl\|def emit_event\|results\[tid\]" engine/orchestrator.py`
   → find the single settle/reap point where every terminal outcome passes through (the natural
   ledger write site).
2. `head -3 engine/store/audit.jsonl` → confirm the append-only JSONL idiom + fields to mirror
   (ticket, attempt, session_id, timestamps).
3. `python3 engine/status.py --json | python3 -m json.tool | head -40` → see what status already
   aggregates, so the ledger complements rather than duplicates it.
4. Check whether a prior-attempt link already exists (audit has `attempt` — T1-11 hit attempt 3);
   the `prior` pointer chains those.

## Moves
### Move 1 — Define the ledger line
- **Do:** One JSON object per terminal reap: `{ticket, attempt, verdict (done|failed(verify)|
  parked|aborted), verdict_source (engine|worker|hitl), evidence (short: which checks/commands),
  ts, prior (previous attempt's ledger id or null), next (queue|done|needs-decision|null)}`. Append
  to `engine/store/ledger.jsonl`.
- **Expect:** a schema that a `grep`/`jq` reconstructs a ticket's history from.
- **Failure signal:** overlaps confusingly with audit.jsonl.
- **Counter-move:** audit = dispatch attempts (input); ledger = outcomes/verdicts (result). State
  the split in a header comment; if it still overlaps, fold ledger fields INTO audit rather than
  making two files — one truth is better than two.

### Move 2 — Write on settle + embed in ticket
- **Do:** At the settle point (Move 1 recon), append the ledger line AND write a `verdict` block
  into the ticket JSON before it moves to `done/`. Chain `prior` to the ticket's previous
  `audit`/`ledger` attempt if one exists.
- **Expect:** T1-11-style multi-attempt tickets show a readable prior-chain.
- **Failure signal:** two orchestrators writing the ledger concurrently interleave/corrupt lines.
- **Counter-move:** append-only + one-line-per-write + O_APPEND is atomic for small lines (same
  assumption audit.jsonl already relies on); if lines exceed the atomic-write size, keep them
  compact (no embedded transcripts — pointers only).

### Move 3 — Resume read
- **Do:** Add `status.py --resume <ticket>` (or extend `--json`) that reconstructs a ticket's full
  story from `ledger.jsonl` + the embedded verdict — no transcript read required.
- **Expect:** for a crashed/re-attempted ticket it prints attempt chain, each verdict, and next-action.
- **Failure signal:** the chain has gaps (an attempt with no ledger line).
- **Counter-move:** gaps mean a crash between dispatch and settle — that's expected; render them as
  "attempt N: dispatched, no terminal verdict (crashed)" so the gap is legible, not hidden.

### Move 4 — Self-report, commit, push
- **Do:** results JSON + commit `feat(engine): durable verdict ledger + prior-chain — resume from disk, not transcripts (wg-t1-16)`.

## Assumptions ledger
1. `audit.jsonl`'s append-only atomicity holds for the ledger (small lines, O_APPEND) — if lines
   must carry more, keep pointers not payloads (Move 2 counter-move).
2. One settle point exists in orchestrator.py — if reap is multi-path, wrap them in one
   `record_verdict()` helper called from each.

## Abort conditions
- **A1 — no single settle chokepoint** (verdicts written in several unrelated places). Park to
  `needs-decision/` proposing a `record_verdict()` refactor as a prerequisite ticket rather than
  scattering ledger writes.

## Verification
```bash
test -f engine/store/ledger.jsonl && echo OK
python3 engine/status.py --resume <a-real-done-ticket>          # reconstructs from disk
grep -c "prior" engine/store/ledger.jsonl                       # chain present on re-attempts
```
Negative: `audit.jsonl` still written as before (not replaced); no transcript files read by the
resume path (`grep -n "\.jsonl" engine/status.py` shows only store ledgers, not
`.claude/projects/*` transcripts).

## Executor notes
- Scope fence: `engine/orchestrator.py` (settle-point ledger write + embed) and `engine/status.py`
  (resume read). Do not modify audit.jsonl's existing writes.
- This is the concrete piece research-swagger named as NOT-yet-ported: the persona (ADR-0042) came
  over; the Prior-chained resumable ledger did not. You are porting the mechanism, not the persona.
- Rabbit hole: a full state-machine/DB. Don't — it's an append-only JSONL + an embedded block +
  one read function. File-truth, same as the rest of the engine.
