# T6-12 — omi-fetch enrichment backlog

| field | value |
|---|---|
| ticket | wg-t6-12-omi-enrichment-backlog |
| track / size / priority | T6 Constellation / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The candidate brief ("tag the remaining ~244/274 records") is **stale — the backlog was cleared
the same morning this was authored**: omi-fetch commit `dc6d96b` ("data(store): full
re-enrichment on sonnet (289/291)", 2026-07-06) enriched all 291 indexed rows via the claude-cli
engine, leaving exactly 2 rows on the honest heuristic `stub` engine (A122, A159 — both fell to
stub on transient CLI failures; their archive files and Overviews exist and are healthy). What
remains is bringing the enrichment surface to a *clean steady state* and proving the on-demand
loop repeatable: retry the stub rows on the real engine, drain whatever new pending rows the
always-on pulse (launchd, every 600s) has ingested since authoring, spot-check quality, commit
the data, and leave the store at zero-pending. Done looks like: `enrich.py --dry-run` reports
`Targets: 0 (of 0 total pending`, stub-engine rows ≤ the 2 authoring-time residuals (0 if the
retries take), the data change committed in the omi-fetch repo, and no code touched anywhere.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this ticket runs as sonnet Swagger
  dispatch; it spawns no sessions of its own.
- **No `-p`/headless/SDK ever (wargame-spec)** — ⚠️ real tension: enrich.py's engine *is* a
  `claude -p` subprocess per record. Ruling applied here: omi-fetch commit `3d49f66`
  (2026-07-06, David-side) explicitly states "Enrichment runs on Claude Code session auth (not
  the metered API)", and the candidate brief itself names "the working claude-cli engine" as the
  mechanism. The portfolio ban targets *worker/session dispatch*, not this app's ratified
  internal engine. See Assumptions ledger #2 for the false branch.
- **Docs lag code (wargame-spec)** — proven on this very ticket: brief said 244/274 pending;
  disk says 291/291 enriched. Recon recounts everything live.
- **Q9 default "complement, don't replace"** — omi-fetch's index-level signal vocabulary
  (`direction|feedback|idea|noise`) is deliberately separate from the omi-extract skill's
  work/life/ambient brain-routing classification (stated in `lib/enrich.py`'s module docstring).
  Never conflate the two; never touch archive `.md` frontmatter.
- **No YLO/POEM work** — n/a here.

## Recon (verify before any work)

App root: `/Users/davidcruwys/dev/ad/apps/omi-fetch`. Run everything from there.

1. Repo present and at/after the full re-enrichment commit:
   `git -C /Users/davidcruwys/dev/ad/apps/omi-fetch merge-base --is-ancestor dc6d96b HEAD && echo OK`
   → expect `OK`. Repo missing or non-ancestor → you're on the wrong machine or a stale clone →
   **Abort A1**.
2. Live counts (this one-liner is reused between batches in Moves 2–3 — call it **COUNT**):
   ```
   python3 -c "
   import json
   total=pend=0; stubs=[]
   for line in open('/Users/davidcruwys/dev/ad/apps/omi-fetch/store/index.jsonl'):
       line=line.strip()
       if not line: continue
       r=json.loads(line); total+=1
       if not r.get('enriched_at'): pend+=1
       elif r.get('enrichment_engine')=='stub': stubs.append(r.get('code'))
   print('total',total,'pending',pend,'stub',stubs)"
   ```
   → expect `total` ≥ 291, `pending` 0–60 (pulse adds a handful of captures per day),
   `stub` ≈ `['A122', 'A159']` (work the LIVE list, not the authoring one). `pending` > 100 →
   state anomaly (enrichment fields wiped, or pulse flood) → **Abort A2**.
   Both `pending == 0` and `stub == []` → **Fork F2** (no-op close).
3. Engine probe: `python3 enrich.py --dry-run --limit 1`
   → expect first output line `Engine: claude-cli (claude CLI (subprocess, --model sonnet), existing session auth)`.
   `Engine: stub (...)` instead → run `command -v claude` and retry the probe once; still stub →
   **Abort A3**. Never batch-enrich while the probe reports stub.
4. Factory HALT: `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT 2>/dev/null`
   → expect no such file (absent = not halted; verified 2026-07-06). Present → stop immediately,
   do nothing; the factory is halted and the engine should not have dispatched you.
5. Repo dirt profile: `git -C /Users/davidcruwys/dev/ad/apps/omi-fetch status --porcelain`
   → expect clean (verified 2026-07-06) OR dirty only under `store/` (pulse writes
   `store/index.jsonl` on its 600s cadence without committing — that's normal). Record the
   snapshot. Dirty on any `*.py` or `lib/` path → someone is mid-change on your exact seam →
   **Abort A1**.
6. Stub-cause sanity (only if Recon 2's stub list is non-empty): for each stub code, confirm its
   `archive_path` file exists (verified at authoring for A122/A159 — files exist with 1052- and
   625-char Overviews, so the stub fallback was a transient claude-cli failure, not a data
   problem). A missing archive file means the retry will stub again on thin input — note it and
   expect **Fork F1** for that row.

## Moves

1. **Do:** Retry each live stub row on the real engine. For each code in Recon 2's `stub` list
   (authoring: A122, A159), from the app root run
   `python3 enrich.py --reextract --code <CODE>`.
   **Expect:** per-row output ending `(claude-cli)`, e.g.
   `[A122] Plugin Debugging And Omi Workflow Experiment ... -> signal=... tags=[...] (claude-cli)`,
   and a summary line `Enriched 1 record(s): {'claude-cli': 1}`.
   **Failure signal:** the row prints `(stub)` again — the engine call failed or returned
   malformed JSON for this record (enrich.py falls back per-record, silently).
   **Counter-move:** retry the same command once (the authoring-time stub cause was transient).
   A second `(stub)` on the same code → **Fork F1**. If EVERY stub-list row double-fails while
   Recon 3's probe still passes → treat as systematic → **Abort A2**.

2. **Do:** First pending batch + quality gate. If Recon 2 showed `pending == 0`, skip to Move 4.
   Otherwise run `python3 enrich.py --limit 30`, then re-run **COUNT**, then spot-check 3 rows
   just enriched (pick 3 codes from the batch output): for each, read its row out of
   `store/index.jsonl` and check `tags` is a 1–6 item lowercase list, `synopsis` is non-empty
   and ≤600 chars, `signal` ∈ {direction, feedback, idea, noise}; for ONE of the 3, open its
   `archive_path` and confirm the synopsis plausibly matches the `## Overview` content.
   **Expect:** summary `Enriched N record(s): {'claude-cli': N}` (no `'stub'` key), pending in
   COUNT dropped by ~N (pulse may add 1–2 new rows mid-run — a small shortfall is normal), and
   3/3 spot-checks pass.
   **Failure signal:** the summary dict contains `'stub': k` with k ≥ 3, or ≥2 of 3 spot-checks
   fail (garbage tags, empty synopsis, signal outside the vocab, synopsis unrelated to the
   Overview).
   **Counter-move:** stop batching. Re-run the Recon 3 probe: probe dead → **Abort A3**; probe
   alive but output garbage persists on a single re-try of one bad code
   (`--reextract --code <CODE>`) → the engine is misbehaving at scale → **Abort A2**. Isolated
   1–2 stub fallbacks in an otherwise-clean batch: retry those codes individually per Move 1,
   then continue.

3. **Do:** Drain the remainder. Repeat `python3 enrich.py --limit 30` followed by **COUNT**
   until COUNT reports `pending 0`. No spot-checks needed after Move 2's gate passed.
   **Expect:** pending decreases by ~30 per batch and reaches 0 (typically 0–2 batches at
   expected drift).
   **Failure signal:** pending fails to decrease across two consecutive batches, or increases.
   **Counter-move:** one increase between adjacent counts can be pulse landing new captures —
   run ONE more batch. Still non-decreasing after that → something is mass-producing or
   un-enriching rows → **Abort A2**.

4. **Do:** Verify the served surface. Run
   `python3 lookup.py --signal direction | head -5` and `python3 lookup.py A122` (or the first
   code from Recon 2's stub list; if that list was empty, any code from Move 2's batch).
   **Expect:** the signal query returns at least one capture line; the single-code lookup shows
   the record with its tags/synopsis/signal populated.
   **Failure signal:** lookup errors, or the enriched fields don't appear for a row enrich.py
   just reported writing.
   **Counter-move:** re-run **COUNT** and re-read that row straight from `store/index.jsonl` —
   if the JSONL row has the fields but lookup doesn't show them, the write worked and lookup has
   a display bug: NOT this ticket's scope — note it in the done summary and proceed. If the
   JSONL row lacks the fields, the write was lost (concurrent pulse write clobbered it) → re-run
   the single-code enrichment (`--reextract --code <CODE>`) once; lost again → **Abort A2**.

5. **Do:** Commit the data. From the app root:
   `git add store/ && git commit -m "data(store): clear enrichment residuals — stub retries + pending drain (wg-t6-12)"`
   — stage ONLY `store/` paths (matches the repo's existing `data(store):` convention, commits
   `dc6d96b`/`6057df2`). Then `git push`.
   **Expect:** commit succeeds; `git status --porcelain` afterwards is empty or shows only
   `store/` changes newer than your commit (pulse can land a row seconds later — fine, leave
   it). Push succeeds.
   **Failure signal:** nothing to commit (only possible via Fork F2 — then skip this move);
   push rejected or no remote configured.
   **Counter-move:** push failure → check `git remote -v`; no remote or auth failure → the
   commit stands locally, note "committed, not pushed: <reason>" in the done summary
   (Assumptions ledger #3). Never `git push --force`; never stage paths outside `store/`.

## Forks

**F1 — a stub row persists after two claude-cli attempts** (probe alive, same code returns
`(stub)` twice in Move 1).
- **Route A (default, ≤5 such rows):** accept the honest stub enrichment — it's real heuristic
  data, named honestly in `enrichment_engine`, and these rows were stub at authoring too. List
  the accepted codes in the Move 5 commit message body and the done summary. Proceed.
- **Route B (>5 rows persist-stub):** that's not per-record flakiness, it's a systematic parse
  or engine failure (e.g. the model's output format changed under the JSON-only system prompt)
  → **Abort A2**.

**F2 — nothing to do** (Recon 2: `pending == 0` AND `stub == []` — someone cleared the
residuals between authoring and execution).
- **Route A (both zero):** run the Verification section checks only, skip Moves 1–3 and 5
  (no data changed → nothing to commit), record "already clean at execution — no-op" in the
  done summary, and finish. This is success, not a failure.
- **Route B (either non-zero):** normal path — run the moves.

## Assumptions ledger

1. **Nested `claude -p` works from inside the executor's own Claude session.** Plausible: the
   289-row run on 2026-07-06 was itself performed from a Claude session on this machine, via
   the same `_call_claude_cli` path. If false (probe stubs with a nesting/auth error) →
   **Abort A3**; the needs-decision note should offer David the 1-command manual fallback
   (`python3 enrich.py --all` from a plain terminal).
2. **The portfolio's no-`-p` ban governs worker/session dispatch, not omi-fetch's internal
   engine.** Grounds: commit `3d49f66`'s rationale ("session auth (not the metered API)") and
   the candidate brief naming this exact engine. If David rules the ban absolute → executor
   parks to needs-decision with two options: (a) David runs enrich.py manually, (b) a future
   ticket adds an executor-inline enrichment path that writes the same index fields without
   subprocessing `claude`.
3. **omi-fetch has a pushable remote.** Not verified at authoring. If false → commit locally,
   note it in the done summary; do not treat as failure.
4. **The stub cause for A122/A159 was transient.** Verified-adjacent: both archive files exist
   with healthy Overviews, so the input wasn't the problem. If the retries stub anyway →
   Fork F1 Route A (accept), not an abort.
5. **`--model sonnet` is intentional; the brief's "haiku" is stale.** Proven: commit `3d49f66`
   deliberately switched haiku → sonnet for signal/synopsis quality, same day as authoring. Do
   NOT "fix" the model back to haiku. (Known cosmetic drift, leave it: the docstring inside
   `lib/enrich.py::_call_claude_cli` still says "--model haiku" — stale comment, report-only.)

## Abort conditions

Park action for all aborts: write
`/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/needs-decision/wg-t6-12-omi-enrichment-backlog.json`
containing `{"ticket": "wg-t6-12-omi-enrichment-backlog", "question": "<the specific question>",
"evidence": "<exact commands run + output observed>", "options": ["..."], "parked_at": "<UTC now>"}`;
leave the ticket in `running/`; never guess past an abort.

- **A1 — state drifted from authoring:** repo missing, `dc6d96b` not an ancestor of HEAD, or
  `*.py`/`lib/` paths dirty at Recon 5. Question for David: "omi-fetch is not in the state
  T6-12 was authored against — re-author or point me at the right clone?"
- **A2 — enrichment state anomaly:** pending > 100 at recon; pending non-decreasing across
  batches after the one-extra-batch grace; systematic garbage (≥2/3 spot-check failures
  persisting on retry); or >5 persist-stub rows (F1 Route B). Question: "the store or engine is
  misbehaving at scale — inspect before more LLM writes?" Include the COUNT output history.
- **A3 — claude CLI unusable:** engine probe reports `stub` twice (binary missing, auth error,
  or nested-session refusal). Question: "enrich.py's claude-cli engine won't run from a worker
  session — run manually, or ratify an alternative path?" Never batch-enrich on the stub
  engine.

## Verification

From `/Users/davidcruwys/dev/ad/apps/omi-fetch`:

1. **COUNT** (Recon 2 one-liner) → `pending 0`, `total` ≥ 291, and `stub` is `[]` or ⊆ the
   F1-accepted codes (max: the authoring residuals A122/A159 plus any F1 Route A acceptances,
   never more than 5).
2. `python3 enrich.py --dry-run` → header contains `Targets: 0 (of 0 total pending enrichment`
   (pulse may have landed a brand-new row in the minutes since Move 3 — a `Targets: 1` here is
   a race, not a failure: drain it with one more `--limit 30` run and re-verify).
3. `python3 lookup.py --signal direction | head -3` → at least one capture row printed.
4. `git -C . show --stat HEAD` → the HEAD commit touches ONLY `store/` paths and its subject
   starts `data(store):` — **unless** F2 Route A fired (no-op: HEAD is still `dc6d96b`-era and
   that's correct).
5. Negative checks:
   - `git diff dc6d96b..HEAD -- '*.py' lib/ launchd/` → empty (no code, no launchd changes).
   - `grep 'CLAUDE_CLI_MODEL = ' lib/enrich.py` → `CLAUDE_CLI_MODEL = "sonnet"` (unchanged).
   - No file under `/Users/davidcruwys/dev/raw-intake/omi/` was modified (enrichment is
     index-level only; spot-check the mtime of one archive file you read).
   - `launchctl list | grep com.appydave.omi-fetch` still shows the job loaded (pulse untouched).
   - dark-factory `research/` untouched (standing rule).

## Executor notes (sonnet)

- **Scope fence:** the ONLY file you change is
  `/Users/davidcruwys/dev/ad/apps/omi-fetch/store/index.jsonl`, and only via `enrich.py` —
  never hand-edit rows. No edits to `enrich.py`, `lib/`, `pulse.py`, `lookup.py`, `view/`,
  `launchd/`, or anything in dark-factory besides a possible needs-decision park file.
- **Do not touch `com.appydave.omi-sync`** — that's a *different*, known-failing launchd job
  (a separate T6 concern), not omi-fetch's `com.appydave.omi-fetch` pulse.
- **Do not touch the omi-extract skill or archive `.md` frontmatter** — different system,
  different vocabulary, deliberately separate (Locked context, Q9).
- **Style:** commit message follows the repo's `data(store): ...` convention; keep the done
  summary to counts + accepted-stub codes + anything parked.
- **HITL preference:** any doubt about scale or cost (pending unexpectedly large, engine
  behaving oddly) → park to needs-decision rather than pushing through; LLM writes are cheap
  but wrong-at-scale writes are not.
- **The rabbit hole (skip it):** running `--reextract --all` to "make everything consistent" —
  291 calls that change nothing material (every row is already sonnet-enriched as of
  `dc6d96b`), and NOT what this ticket asks. Same family: "fixing" the stale haiku docstring,
  switching the model, investigating omi-sync, or improving lookup.py display bugs found in
  Move 4. Note them; don't do them.
