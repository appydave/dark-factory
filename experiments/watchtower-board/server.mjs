#!/usr/bin/env node
//
// watchtower-board — minimal live board for the Dark Factory floor (SPIKE).
//
// A read-only VIEW (AppyStack/Viewer role): it READS the engine dirs + tmux
// and renders them. It owns no state and deliberately does NOT live inside
// Switchboard — respecting the capability-placement / app-ownership principle.
// Eventual home: the AppyStack "Watchtower" instance. This is the v1 proof
// that you can SEE the threads instead of reading raw Swagger transcripts.
//
// Capability-placement note: every timestamp here comes from the OS
// (filesystem mtime / Date.now()), never a language model.
//
// Run:  node experiments/watchtower-board/server.mjs   (then open http://localhost:7430)

import http from 'node:http';
import { readdir, readFile, stat } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';

const PORT = 7430;
const ENGINE = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'watchtower-engine');

const execP = (cmd, args) =>
  new Promise((res) => execFile(cmd, args, { timeout: 4000 }, (e, out) => res(e ? '' : out)));

// Read every *.json in a queue dir → [{queue_id, kind, prompt, mtime}], newest first.
async function readTickets(sub) {
  const dir = join(ENGINE, sub);
  let names = [];
  try { names = (await readdir(dir)).filter((n) => n.endsWith('.json')); } catch { return []; }
  const rows = await Promise.all(names.map(async (n) => {
    const p = join(dir, n);
    try {
      const [raw, st] = await Promise.all([readFile(p, 'utf8'), stat(p)]);
      const j = JSON.parse(raw);
      return {
        queue_id: j.queue_id ?? n.replace(/\.json$/, ''),
        kind: j.kind ?? '?',
        prompt: (j.prompt ?? j.outcome ?? '').slice(0, 90),
        status: j.status,                       // present in reports/
        mtime: st.mtimeMs,
      };
    } catch { return null; }
  }));
  return rows.filter(Boolean).sort((a, b) => b.mtime - a.mtime);
}

// Live Swaggers = tmux windows named swagger-*  → [{window, session}]
async function readSwaggers() {
  const out = await execP('tmux', ['list-windows', '-a', '-F', '#{session_name}\t#{window_name}']);
  return out.split('\n').map((l) => l.split('\t'))
    .filter(([, w]) => w && w.startsWith('swagger-'))
    .map(([session, window]) => ({ session, window }));
}

async function snapshot() {
  const [queue, running, done, reports, swaggers] = await Promise.all([
    readTickets('queue'), readTickets('running'), readTickets('done'), readTickets('reports'), readSwaggers(),
  ]);
  // map queue_id -> report status, to badge done cards
  const status = Object.fromEntries(reports.map((r) => [r.queue_id, r.status]));
  return {
    now: Date.now(),
    queue, running,
    done: done.slice(0, 12).map((d) => ({ ...d, report: status[d.queue_id] ?? null })),
    swaggers,
    counts: { queued: queue.length, running: running.length, done: done.length, swaggers: swaggers.length },
  };
}

const PAGE = `<!doctype html><html><head><meta charset="utf8"><title>Watchtower · floor</title>
<style>
 :root{--bg:#0e1116;--card:#1b2230;--mut:#7d8aa0;--ok:#3fb950;--run:#d29922;--q:#58a6ff;--txt:#e6edf3}
 *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--txt);font:13px/1.4 ui-monospace,Menlo,monospace}
 header{padding:12px 18px;border-bottom:1px solid #222b38;display:flex;gap:18px;align-items:baseline}
 header b{font-size:15px} .muted{color:var(--mut)} .pill{padding:1px 7px;border-radius:9px;background:#222b38}
 .cols{display:grid;grid-template-columns:1fr 1fr 1.2fr 1fr;gap:14px;padding:16px}
 .col h2{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:0 0 8px}
 .card{background:var(--card);border:1px solid #29out;border-radius:8px;padding:8px 10px;margin-bottom:8px;border-left:3px solid #2b3445}
 .card.q{border-left-color:var(--q)} .card.run{border-left-color:var(--run)} .card.done{border-left-color:var(--ok)}
 .card.swg{border-left-color:#bc8cff} .qid{font-weight:600} .k{font-size:11px;color:var(--mut)}
 .p{color:#aeb9cc;font-size:11px;margin-top:3px} .badge{float:right;font-size:10px;padding:0 6px;border-radius:8px}
 .badge.complete{background:#11331c;color:var(--ok)} .badge.failed{background:#3d1418;color:#ff7b72}
 .empty{color:#46506180;font-style:italic;padding:6px 2px}
</style></head><body>
<header><b>🗼 Watchtower</b><span class="muted">factory floor · live</span>
 <span class="muted" id="counts"></span><span class="muted" style="margin-left:auto" id="upd"></span></header>
<div class="cols">
 <div class="col"><h2>Queued (<span id="cq">0</span>)</h2><div id="queue"></div></div>
 <div class="col"><h2>Running (<span id="cr">0</span>)</h2><div id="running"></div></div>
 <div class="col"><h2>Done · recent</h2><div id="done"></div></div>
 <div class="col"><h2>Live Swaggers (tmux) (<span id="cs">0</span>)</h2><div id="swg"></div></div>
</div>
<script>
const el=(id)=>document.getElementById(id);
const esc=(s)=>(s||'').replace(/[<&]/g,(c)=>({'<':'&lt;','&':'&amp;'}[c]));
function ticket(t,cls){return '<div class="card '+cls+'">'+
  (t.report?'<span class="badge '+t.report+'">'+t.report+'</span>':'')+
  '<div class="qid">'+esc(t.queue_id)+'</div><div class="k">'+esc(t.kind)+'</div>'+
  (t.prompt?'<div class="p">'+esc(t.prompt)+'</div>':'')+'</div>';}
function fill(id,rows,cls){el(id).innerHTML=rows.length?rows.map((r)=>ticket(r,cls)).join(''):'<div class="empty">— empty —</div>';}
async function tick(){
 try{const s=await (await fetch('/api/state')).json();
  fill('queue',s.queue,'q');fill('running',s.running,'run');fill('done',s.done,'done');
  el('swg').innerHTML=s.swaggers.length?s.swaggers.map((w)=>'<div class="card swg"><div class="qid">'+esc(w.window)+'</div><div class="k">'+esc(w.session)+'</div></div>').join(''):'<div class="empty">— none —</div>';
  el('cq').textContent=s.counts.queued;el('cr').textContent=s.counts.running;el('cs').textContent=s.counts.swaggers;
  el('counts').innerHTML='<span class="pill">'+s.counts.queued+' queued</span> <span class="pill">'+s.counts.running+' running</span> <span class="pill">'+s.counts.swaggers+' swaggers</span>';
  el('upd').textContent='updated '+new Date(s.now).toLocaleTimeString();
 }catch(e){el('upd').textContent='server unreachable';}
}
tick();setInterval(tick,2000);
</script></body></html>`;

const server = http.createServer(async (req, res) => {
  if (req.url.startsWith('/api/state')) {
    try {
      const data = JSON.stringify(await snapshot());
      res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache' });
      res.end(data);
    } catch (e) {
      res.writeHead(500); res.end(JSON.stringify({ error: String(e) }));
    }
    return;
  }
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end(PAGE);
});
server.listen(PORT, () => console.log(`watchtower-board on http://localhost:${PORT} (engine: ${ENGINE})`));
