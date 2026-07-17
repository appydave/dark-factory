import json, glob, collections, os

RUN = "/Users/davidcruwys/dev/ad/apps/dark-factory/research/captains-log-archaeology/full-run-2026-07-13"
recs = []
for f in sorted(glob.glob(RUN + "/records/*.jsonl")):
    for line in open(f):
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception:
            pass

recs = [r for r in recs if isinstance(r, dict) and r.get("date") and r.get("thread_id")]
recs.sort(key=lambda r: r["date"])
LIVE = "2026-06-22"   # last-seen on/after -> still live (~last 3 weeks)
RECENT = "2026-05-15"

def tag(last):
    return "LIVE" if last >= LIVE else ("RECENT" if last >= RECENT else "STALE")

# threads
th = collections.defaultdict(list)
for r in recs:
    th[r["thread_id"]].append(r["date"])
threads = sorted(((k, len(v), min(v), max(v)) for k, v in th.items()), key=lambda x: -x[1])

# open loops
loops = collections.defaultdict(lambda: {"dates": [], "threads": set(), "ess": []})
for r in recs:
    lp = r.get("loop") or {}
    if lp.get("is_open") and lp.get("label"):
        k = lp["label"].strip()
        L = loops[k]
        L["dates"].append(r["date"]); L["threads"].add(r["thread_id"]); L["ess"].append((r["date"], r.get("essence", "")))
loop_rows = []
for k, L in loops.items():
    first, last, cnt = min(L["dates"]), max(L["dates"]), len(L["dates"])
    loop_rows.append((k, first, last, cnt, sorted(L["threads"]), tag(last), L["ess"][-1][1]))
loop_rows.sort(key=lambda x: (x[5] != "LIVE", -x[3], x[1]))  # live first, then count, then oldest-first

# tickets
tk = collections.defaultdict(list)
for r in recs:
    for a in (r.get("actions") or []):
        if isinstance(a, dict) and a.get("text"):
            tk[a.get("target") or "unassigned"].append((r["date"], a["text"]))
targets = sorted(((t, v) for t, v in tk.items()), key=lambda x: -len(x[1]))
total_actions = sum(len(v) for v in tk.values())
live_actions = sum(1 for v in tk.values() for d, _ in v if d >= LIVE)

noise = sum(1 for r in recs if r.get("kind") == "noise")
live_loops = [r for r in loop_rows if r[5] == "LIVE"]

os.makedirs(RUN, exist_ok=True)

# ---- EXECUTIVE SUMMARY ----
with open(RUN + "/00-EXECUTIVE-SUMMARY.md", "w") as o:
    o.write("# Captain's Log — 6-Month Archaeology (deterministic merge)\n\n")
    o.write(f"**Corpus:** {len(recs)} captures, {recs[0]['date']} → {recs[-1]['date']}, {noise} noise ({100*noise//len(recs)}%). "
            f"{len(threads)} threads · {len(loop_rows)} distinct open loops ({len(live_loops)} LIVE) · {len(targets)} ticket targets · {total_actions} raw actions ({live_actions} in the last 3 weeks).\n\n")
    o.write("> Merge done locally (Python) after the Fable run hit the monthly spend limit at the synthesis stage. Extraction (all 1,250 records) is complete and durable; narrative prose was skipped.\n\n")
    o.write("## Top threads by weight\n\n| Thread | Records | Span |\n|---|---|---|\n")
    for k, c, f, l in threads[:15]:
        o.write(f"| {k} | {c} | {f} → {l} |\n")
    o.write(f"\n## Hottest LIVE open loops (last seen ≥ {LIVE})\n\n| Loop | First | Last | ×seen | Threads |\n|---|---|---|---|---|\n")
    for k, f, l, c, thr, tg, ess in live_loops[:25]:
        o.write(f"| {k} | {f} | {l} | {c} | {', '.join(thr[:2])} |\n")
    o.write("\n## Ticket volume by target (top 20)\n\n| Target | Actions | Live (≥3wk) |\n|---|---|---|\n")
    for t, v in targets[:20]:
        lv = sum(1 for d, _ in v if d >= LIVE)
        o.write(f"| {t} | {len(v)} | {lv} |\n")

# ---- LOOP REGISTRY ----
with open(RUN + "/loop-registry.md", "w") as o:
    o.write(f"# Loop Registry — {len(loop_rows)} distinct open loops\n\nSorted: LIVE first, then by frequency, then oldest-first.\n\n")
    for k, f, l, c, thr, tg, ess in loop_rows:
        o.write(f"- **[{tg}]** {k} — first {f}, last {l}, seen {c}× ({', '.join(thr)})\n  - latest: {ess[:200]}\n")

# ---- TICKETS BY TARGET ----
with open(RUN + "/tickets-by-target.md", "w") as o:
    o.write(f"# Tickets by Target — {total_actions} raw actions across {len(targets)} targets\n\n")
    o.write("Each action tagged by recency of the capture it came from. LIVE = last 3 weeks.\n\n")
    for t, v in targets:
        lv = sum(1 for d, _ in v if d >= LIVE)
        o.write(f"\n## {t}  ({len(v)} actions, {lv} live)\n\n")
        for d, txt in sorted(v, reverse=True):
            o.write(f"- [{tag(d)} {d}] {txt}\n")

print(f"records={len(recs)} noise={noise} threads={len(threads)} loops={len(loop_rows)} live_loops={len(live_loops)} targets={len(targets)} actions={total_actions} live_actions={live_actions}")
print("TOP THREADS:", [(k, c) for k, c, f, l in threads[:8]])
print("TOP LIVE LOOPS:", [(k, c, l) for k, f, l, c, thr, tg, ess in live_loops[:8]])
print("TOP TARGETS:", [(t, len(v)) for t, v in targets[:8]])
