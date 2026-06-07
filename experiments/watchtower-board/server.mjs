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
import { readdir, readFile, stat, writeFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve } from 'node:path';
import { parseConcepts, attachStaleness } from './parse-concepts.mjs';

const PORT = 7430;
const HERE = dirname(fileURLToPath(import.meta.url));
const ENGINE = resolve(HERE, '..', 'watchtower-engine');
const REPO_ROOT = resolve(HERE, '..', '..');           // two levels up from the board dir
const CONCEPTS_MD = resolve(REPO_ROOT, 'backlog', 'concepts.md');
const STALE_DAYS = 14;

// gitLineDates — RUNTIME helper (server only): git blame committer-times per line
// of backlog/concepts.md → {lineNumber: epochMs}. Lines 'not committed yet' are
// omitted (→ treated as fresh by attachStaleness). On ANY git failure returns {}.
function gitLineDates() {
  return new Promise((res) => {
    execFile('git', ['blame', '--line-porcelain', 'backlog/concepts.md'],
      { cwd: REPO_ROOT, timeout: 4000, maxBuffer: 8 * 1024 * 1024 }, (e, out) => {
        if (e || !out) return res({});
        const map = {};
        let lineNo = 0, committerTime = null, notCommitted = false;
        for (const ln of out.split('\n')) {
          if (/^[0-9a-f]{40} /.test(ln)) {
            // header: "<sha> <origLine> <finalLine> [<group>]" → final line is 3rd field
            lineNo = parseInt(ln.split(' ')[2], 10);
            committerTime = null;
            notCommitted = false;
          } else if (ln.startsWith('committer-time ')) {
            committerTime = parseInt(ln.slice('committer-time '.length).trim(), 10) * 1000;
          } else if (ln.startsWith('committer ')) {
            if (ln.slice('committer '.length).trim() === 'Not Committed Yet') notCommitted = true;
          } else if (ln.startsWith('\t')) {
            // the actual source line terminates this blame block
            if (lineNo && committerTime != null && !notCommitted) map[lineNo] = committerTime;
          }
        }
        res(map);
      });
  });
}

// --- v5 Floor↔Lanes BRIDGE (additive) — CONVERGE a cluster of lane concepts → ONE brief ---
// (v4's per-card 'promote' button + /api/promote endpoint were REMOVED: they skipped
//  the cluster-synthesis that is the whole point. A convergence selects >=2 related
//  concepts and emits ONE synthesis ticket instead of N vague 'elaborate' ones.)
//
// slugify — sanitize a concept into a safe queue_id fragment: lowercase, only
// [a-z0-9-], no '/', no '..', collapsed/trimmed dashes, capped at 40 chars.
export function slugify(s) {
  return String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'concept';
}

// buildConvergeTicket — PURE: (items, nowMs) → {queue_id, ticket}. No I/O, so it is
// self-checkable. items = [{concept, lane}, ...] (>=1). All time comes from nowMs (the
// caller passes Date.now()). The slug is derived from the first concept (sanitized, short).
export function buildConvergeTicket(items, nowMs) {
  const list = (Array.isArray(items) ? items : []).filter((it) => it && String(it.concept || '').trim());
  if (!list.length) throw new Error('converge needs at least one concept');
  const n = list.length;
  const slug = slugify(list[0].concept);
  const queue_id = 'q-' + nowMs + '-converge-' + slug;
  const lines = list.map((it, i) => (i + 1) + ') ' + String(it.lane || 'unsorted') + ': ' + String(it.concept)).join('\n');
  const prompt =
    'Converge these ' + n + ' related concepts into ONE cohesive brief. ' +
    'Decide the form (research brief | architecture decision | coding epic). Concepts:\n' +
    lines + '\n' +
    'Identify the through-line, what they collectively imply, and the concrete next work; ' +
    'write the brief to docs/watchtower/converged-briefs/' + slug + '.md.';
  const ticket = {
    queue_id,
    kind: 'instruction',
    experiment_id: 'exp-converge',
    requested_by: 'watchtower-board',
    requested_at: new Date(nowMs).toISOString(),
    args: { from: 'lanes-converge', count: n },
    prompt,
  };
  return { queue_id, ticket };
}

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
 .toggle{display:flex;gap:4px} .toggle button{font:inherit;cursor:pointer;color:var(--mut);background:#222b38;border:1px solid #2b3445;border-radius:7px;padding:2px 10px}
 .toggle button.on{color:var(--txt);background:#2b3445;border-color:var(--q)}
 .lanes{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;padding:16px;align-items:start}
 .lane h2{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:0 0 8px}
 .card.concept{border-left-color:#bc8cff} .badges{float:right;font-size:13px;letter-spacing:2px}
 .card.stale{opacity:.5;border-left-color:#46506180;border-color:#3a4252}
 .age{font-size:10px;color:var(--mut);margin-top:3px} .age.warn{color:var(--run)}
 .lane h2 .stalehint{font-size:10px;color:var(--run);text-transform:none;letter-spacing:0;margin-left:6px}
 .card.concept{cursor:pointer} .card.concept.sel{border-color:var(--q);border-left-color:var(--q);background:#1d2738;box-shadow:inset 0 0 0 1px var(--q)}
 .card.concept .chk{float:left;margin-right:8px;color:var(--mut);font-size:13px;user-select:none}
 .card.concept.sel .chk{color:var(--q)}
 #convbar{position:fixed;left:0;right:0;bottom:0;display:none;justify-content:center;align-items:center;gap:14px;
   padding:12px 18px;background:#11182480;backdrop-filter:blur(6px);border-top:1px solid var(--q);z-index:20}
 #convbar.show{display:flex} #convbtn{font:inherit;cursor:pointer;color:#06210f;background:var(--ok);border:0;border-radius:8px;padding:6px 16px;font-weight:600}
 #convbtn:hover{filter:brightness(1.08)} #convbtn:disabled{opacity:.5;cursor:default}
 #convmsg{position:fixed;left:50%;bottom:64px;transform:translateX(-50%);background:#11331c;color:var(--ok);
   border:1px solid var(--ok);border-radius:8px;padding:6px 14px;font-size:12px;opacity:0;transition:opacity .3s;pointer-events:none;z-index:21}
 #convmsg.show{opacity:1}
</style></head><body>
<header><b>🗼 Watchtower</b><span class="muted" id="subtitle">factory floor · live</span>
 <span class="toggle"><button id="tab-floor" class="on">Floor</button><button id="tab-lanes">Lanes</button></span>
 <span class="muted" id="counts"></span><span class="muted" style="margin-left:auto" id="upd"></span></header>
<div class="cols" id="view-floor">
 <div class="col"><h2>Queued (<span id="cq">0</span>)</h2><div id="queue"></div></div>
 <div class="col"><h2>Running (<span id="cr">0</span>)</h2><div id="running"></div></div>
 <div class="col"><h2>Done · recent</h2><div id="done"></div></div>
 <div class="col"><h2>Live Swaggers (tmux) (<span id="cs">0</span>)</h2><div id="swg"></div></div>
</div>
<div class="lanes" id="view-lanes" style="display:none"></div>
<div id="convbar"><span class="muted">cluster selected</span><button id="convbtn">Converge <span id="convn">0</span> concepts → brief ▶</button></div>
<div id="convmsg"></div>
<script>
const el=(id)=>document.getElementById(id);
const esc=(s)=>(s||'').replace(/[<&]/g,(c)=>({'<':'&lt;','&':'&amp;'}[c]));
const escA=(s)=>(s||'').replace(/[<&"]/g,(c)=>({'<':'&lt;','&':'&amp;','"':'&quot;'}[c]));
let view='floor';
function ticket(t,cls){return '<div class="card '+cls+'">'+
  (t.report?'<span class="badge '+t.report+'">'+t.report+'</span>':'')+
  '<div class="qid">'+esc(t.queue_id)+'</div><div class="k">'+esc(t.kind)+'</div>'+
  (t.prompt?'<div class="p">'+esc(t.prompt)+'</div>':'')+'</div>';}
function fill(id,rows,cls){el(id).innerHTML=rows.length?rows.map((r)=>ticket(r,cls)).join(''):'<div class="empty">— empty —</div>';}
async function tick(){
 if(view!=='floor')return;            // pause floor polling while Lanes is shown
 try{const s=await (await fetch('/api/state')).json();
  fill('queue',s.queue,'q');fill('running',s.running,'run');fill('done',s.done,'done');
  el('swg').innerHTML=s.swaggers.length?s.swaggers.map((w)=>'<div class="card swg"><div class="qid">'+esc(w.window)+'</div><div class="k">'+esc(w.session)+'</div></div>').join(''):'<div class="empty">— none —</div>';
  el('cq').textContent=s.counts.queued;el('cr').textContent=s.counts.running;el('cs').textContent=s.counts.swaggers;
  el('counts').innerHTML='<span class="pill">'+s.counts.queued+' queued</span> <span class="pill">'+s.counts.running+' running</span> <span class="pill">'+s.counts.swaggers+' swaggers</span>';
  el('upd').textContent='updated '+new Date(s.now).toLocaleTimeString();
 }catch(e){el('upd').textContent='server unreachable';}
}
tick();setInterval(tick,2000);

// --- Lanes view (concept register) — additive; does not touch Floor above ---
// v5: click-to-toggle multi-SELECT (no per-card button). Selection survives the
// innerHTML rebuild each tickLanes via the sel Map, keyed concept then lane.
const sel=new Map();                                   // key -> {concept, lane}
const selKey=(concept,lane)=>concept+'␟'+lane;
function ageLabel(it){return (it.ageDays===0)?'new':(it.ageDays+'d');}
function laneCard(it,lane){const k=selKey(it.concept,lane);const on=sel.has(k);
 return '<div class="card concept'+(it.stale?' stale':'')+(on?' sel':'')+'"'+
  ' data-concept="'+escA(it.concept)+'" data-lane="'+escA(lane)+'">'+
  '<span class="chk">'+(on?'☑':'☐')+'</span>'+
  '<span class="badges">'+esc(it.status)+' '+esc(it.pri)+'</span>'+
  '<div class="qid">'+esc(it.concept)+'</div>'+
  '<div class="age'+(it.stale?' warn':'')+'">'+ageLabel(it)+'</div></div>';}
function refreshConvBar(){const n=sel.size;el('convn').textContent=n;
 el('convbar').classList.toggle('show',view==='lanes'&&n>=2);}
async function tickLanes(){
 try{const s=await (await fetch('/api/concepts')).json();
  el('view-lanes').innerHTML=s.lanes.map((l)=>'<div class="lane"><h2>'+esc(l.lane)+
    ' ('+l.items.length+')'+(l.stale?'<span class="stalehint">cold · '+l.ageDays+'d</span>':'')+
    '</h2>'+(l.items.length?l.items.map((it)=>laneCard(it,l.lane)).join(''):'<div class="empty">— empty —</div>')+'</div>').join('');
  el('counts').innerHTML='<span class="pill">'+s.counts.lanes+' lanes</span> <span class="pill">'+s.counts.items+' concepts</span>';
  refreshConvBar();
 }catch(e){el('view-lanes').innerHTML='<div class="empty">concepts unreachable</div>';}
}
function show(v){view=v;
 el('view-floor').style.display=v==='floor'?'':'none';
 el('view-lanes').style.display=v==='lanes'?'':'none';
 el('tab-floor').classList.toggle('on',v==='floor');
 el('tab-lanes').classList.toggle('on',v==='lanes');
 el('subtitle').textContent=v==='floor'?'factory floor · live':'concept lanes · backlog/concepts.md';
 if(v==='lanes'){tickLanes();}else{tick();}
 refreshConvBar();
}
el('tab-floor').onclick=()=>show('floor');
el('tab-lanes').onclick=()=>show('lanes');
// click-to-toggle SELECT — delegated (innerHTML is rebuilt each tickLanes)
el('view-lanes').addEventListener('click',(ev)=>{
 const c=ev.target.closest('.card.concept');if(!c)return;
 const concept=c.dataset.concept,lane=c.dataset.lane,k=selKey(concept,lane);
 if(sel.has(k)){sel.delete(k);}else{sel.set(k,{concept,lane});}
 c.classList.toggle('sel');
 c.querySelector('.chk').textContent=sel.has(k)?'☑':'☐';
 refreshConvBar();
});
let convToast;
function toast(msg){const m=el('convmsg');m.textContent=msg;m.classList.add('show');
 clearTimeout(convToast);convToast=setTimeout(()=>m.classList.remove('show'),4000);}
// Converge N → ONE brief: emits a single converge ticket, then clears the selection
el('convbtn').onclick=async()=>{
 const items=[...sel.values()];if(items.length<2)return;
 const btn=el('convbtn');btn.disabled=true;
 try{const r=await fetch('/api/converge',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({items})});
  const j=await r.json();
  if(j.accepted){const n=items.length;sel.clear();tickLanes();
   toast('converged '+n+' concepts → '+j.queue_id);}
  else{toast('failed: '+(j.error||'?'));}
 }catch(e){toast('failed');}
 finally{btn.disabled=false;refreshConvBar();}
};
</script></body></html>`;

const server = http.createServer(async (req, res) => {
  if (req.method === 'POST' && req.url.startsWith('/api/converge')) {
    try {
      let body = '';
      for await (const chunk of req) body += chunk;
      const { items } = JSON.parse(body || '{}');
      const list = (Array.isArray(items) ? items : [])
        .filter((it) => it && String(it.concept || '').trim())
        .map((it) => ({ concept: String(it.concept), lane: String(it.lane || 'unsorted') }));
      if (list.length < 2) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ accepted: false, error: 'converge needs >=2 concepts' }));
        return;
      }
      const { queue_id, ticket } = buildConvergeTicket(list, Date.now());
      await writeFile(join(ENGINE, 'queue', queue_id + '.json'), JSON.stringify(ticket, null, 2));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ accepted: true, queue_id }));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ accepted: false, error: String(e) }));
    }
    return;
  }
  if (req.url.startsWith('/api/concepts')) {
    try {
      const lanes = parseConcepts(await readFile(CONCEPTS_MD, 'utf8'));
      const lineDates = await gitLineDates();        // {} on any git failure → all fresh
      attachStaleness(lanes, lineDates, Date.now(), STALE_DAYS);
      res.writeHead(200, { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache' });
      res.end(JSON.stringify({ lanes, counts: { lanes: lanes.length, items: lanes.reduce((n, l) => n + l.items.length, 0) } }));
    } catch (e) {
      res.writeHead(500); res.end(JSON.stringify({ error: String(e) }));
    }
    return;
  }
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
// Only bind the port when run directly (node server.mjs), not when imported
// (e.g. by selfcheck-converge.mjs) — so importing the pure functions can't
// collide with the already-running :7430 server.
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  server.listen(PORT, () => console.log(`watchtower-board on http://localhost:${PORT} (engine: ${ENGINE})`));
}
