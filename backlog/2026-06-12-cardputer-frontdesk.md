# Cardputer Front Desk — a physical head for the Watchtower board

**Raised**: 2026-06-12 (David). **Status**: opportunity / spike-proposal — not started.
**Relates to**: `experiments/watchtower-board/` (the software Front Desk that ALREADY EXISTS — this is its physical head), `experiments/watchtower-engine/` (the queue it reads/writes), `2026-06-06-dark-factory-sentinel.md` (the `waiting`/permission return-leg Stage 2 needs), `2026-06-06-observability.md`, problems #19 (return-leg), #8 (orphan alert).
**North Star**: observability as the primary enabler of higher autonomy stages (see `docs/north-star.md`). This is that thesis made physical.

## The idea (David)

We picked up an **M5Stack Cardputer-Adv** (ESP32-S3, 1.14" LCD, 56-key keyboard, speaker, IMU, WiFi, BLE) from an Anthropic Code-with-Claude event. Make it a **physical Front Desk** for the factory: an always-on desk device showing factory state ambiently, letting David **message the factory** and **approve prompts** without a terminal. The literal embodiment of the "lights-sparse / FANUC dark-factory" target — a pilot lamp for an autonomous software factory.

## The software version already exists — this is its physical head

**`experiments/watchtower-board/server.mjs`** is the v1 Front Desk: a read-only live board on **:7430** that READS the `watchtower-engine` dirs (`queue/ running/ done/ reports/`) + tmux `swagger-*` windows and renders the floor. It's a Viewer (AppyStack role): owns no state, deliberately NOT inside Switchboard, eventual home the AppyStack "Watchtower" instance. Every timestamp comes from the OS, never an LLM (capability-placement rule).

The Cardputer is **another head on that same board** — same data source, same Viewer role, same rules. It does not invent a parallel system. It already exposes everything we need:

- **`GET /api/state`** → `{queue, running, done, counts:{queued, running, done, swaggers}}` — the pilot lamp's data. **Poll it; no SSE stub needed.**
- **`POST /api/converge`** → writes a `queue/<id>.json` ticket (via the pure `buildConvergeTicket`). Proof that "post → enqueue" already works; the Cardputer inbox is the same move with a free-text ticket.

## Why it's on-grain (not a gimmick)

- **It can't cross the orchestrator wall.** watchtower-board is a read-only Viewer that never runs `claude`. The Cardputer is the same: it can **read state** and **drop a `queue/` ticket** (which an in-session `run-next-workflow` `/loop` later claims via atomic `rename(2)`), but it cannot dispatch or execute. It sits exactly where the board sits — behind the wall.
- **It reuses a proven device pattern.** Anthropic's `build-with-claude` "Claude Buddy" is a desk device that streams status and acts as a Y/N permission paddle. We point the same shape at the Watchtower instead of Claude Desktop. Audited clean (TLS-enforced, no injection surface); cloned at `~/dev/upstream/repos/build-with-claude/`, protocol at `buddy/references/protocol.md`.

## Architecture — how it wires into what exists

| Cardputer does | Plugs into |
|---|---|
| WiFi → **poll `GET :7430/api/state`** every ~2 s, render `running / queued / swaggers` on the LCD | watchtower-board `/api/state` (exists today) |
| Ambient pilot lamp: idle = dim · work running = green pulse · stale/orphan = red | board counts + staleness; reaper/orphan signal (#8) |
| Type a short line on the 56-key keyboard → **POST a free-text `queue/*.json` ticket** | same write path as `/api/converge`; engine queue entry shape (see engine README) |
| **(Stage 2, Sentinel-gated)** beep on a `waiting`/permission event; show tool+hint; **Y/N → POST decision** | the `david`-topic return-leg (#19) — **does not exist in the board yet**; needs the Sentinel |

**Transport is plain HTTP over the LAN** (or Tailscale when remote) — not BLE. The Buddy BLE path is the *pattern* we borrow; the wire is WiFi → the board server. Deliberately avoid UIFlow's BLE stack (unauthenticated on UIFlow 2.0).

## Staged build (each stage ships standalone value)

1. **Read-only pilot lamp** — poll `/api/state`, render counts + status colour. **Works against the board TODAY.** De-risks WiFi + HTTP-on-device. A real observability artifact on its own.
2. **Inbox** — keyboard → POST a free-text ticket into `queue/`. **Works against the engine TODAY** (board already writes tickets via `/api/converge`; add a sibling `/api/ticket` that takes `{text}` and builds a `kind:"instruction"` entry). Lands the "send the factory a message from the desk" half.
3. **Approval pager** *(gated on the Sentinel)* — sleep until a `waiting` event, become a tactile Y/N paddle that posts the decision on the `david` topic. **Blocked**: the permission return-leg (#19) lives in the Dark Factory Sentinel, which isn't built. Do this stage *after* the Sentinel probe stands up its SSE half. Until then the board has no `waiting`/permission lane to surface.

Build 1 → 2 now; 3 when the Sentinel exists. Note the reorder vs. the first sketch: **the board makes 1 and 2 the cheap, ready-today stages**, and pushes approvals behind the Sentinel where they actually belong.

## Dependencies / what already exists

- **Device onboarding is solved.** `cwc-makers` plugin: `/plugin install cwc-makers@claude-plugins-official` then `/maker-setup`. Or run the vendored skill directly: `~/dev/upstream/repos/build-with-claude/.claude/skills/m5-onboard/`. App push without re-flash: `install_apps.py --src <dir>`.
- **The board server.** `node experiments/watchtower-board/server.mjs` → :7430. `/api/state` is ready. For Stage 2 add a `/api/ticket {text}` route (5 lines, mirrors `/api/converge`).
- **The engine.** `experiments/watchtower-engine/` — queue dirs + atomic-claim mutex + `run-next-workflow` skill. A ticket the Cardputer drops gets claimed by an in-session `/loop`, same as any other.
- **No Sentinel / no SSE stub.** The earlier draft invented a throwaway SSE bus — unnecessary. Polling `/api/state` is simpler and hits real state. (If poll latency ever matters, add SSE to the board later; not now.)

## Smallest probe

`node experiments/watchtower-board/server.mjs`, drop a couple of fake `queue/*.json` entries, flash Appendix B `frontdesk.py` (Stage 1) → confirm the Cardputer shows live counts and the colour changes as tickets move queue→running→done. One afternoon, against the **real** board, no new server.

## Done when

- **Stage 1**: the device on the desk shows live `running/queued/swaggers` from `/api/state`; colour reflects health; survives the board restarting (reconnect).
- **Stage 2**: a line typed on the keyboard appears as a `queue/*.json` ticket the engine can claim.
- **Stage 3** *(post-Sentinel)*: a `waiting` event beeps the device; Y/N posts a decision the Sentinel receives on `david`.

## Risks / open questions

- **Auth on the LAN.** The board's write routes must not accept arbitrary POSTs from anything on the network. Stage 2 needs at least a shared token header before it writes tickets; mandatory before any Tailscale exposure. Stage 1 is read-only, lower stakes.
- **Where does the device bundle live in-repo?** Likely `experiments/watchtower-board/device/` (keep it next to its server) or a promoted `apps/watchtower/device/` once Watchtower graduates from spike. PO call before Dev starts.
- **The board is a spike, not a product.** Its eventual home is the AppyStack "Watchtower" instance. Pin the `/api/state` response shape (the device's only contract) so the device code survives the board → AppyStack migration. The JSON shape is the interface; honour it on both sides.
- **Don't reach for BLE.** WiFi/HTTP only — the Buddy BLE stack is unauthenticated on UIFlow 2.0.

---

## Appendix A — the endpoints already exist

No stub server. Stage 1 reads what `watchtower-board` already serves:

```
GET  /api/state   → { queue:[…], running:[…], done:[…],
                      counts:{ queued, running, done, swaggers } }     # poll every ~2s
```

Stage 2 adds one route to `server.mjs`, mirroring the existing `/api/converge` writer:

```js
// POST /api/ticket  {text}  → writes a free-text queue/*.json the engine can claim.
if (req.method === 'POST' && req.url.startsWith('/api/ticket')) {
  const { text } = JSON.parse(await readBody(req));
  const queue_id = 'q-' + Date.now() + '-desk';            // OS time, never an LLM
  const ticket = { queue_id, kind: 'instruction', prompt: String(text || ''),
                   requested_at: new Date().toISOString(), requested_by: 'cardputer' };
  await writeFile(join(ENGINE, 'queue', queue_id + '.json'), JSON.stringify(ticket, null, 2));
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ accepted: true, queue_id })); return;
}
```

## Appendix B — MicroPython app skeleton (Stage 1: pilot lamp, polling)

```python
# frontdesk.py — UIFlow 2.0 / Cardputer-Adv. Stage 1: poll the board, render counts.
# Stage 2 (keyboard → POST /api/ticket) and Stage 3 (Y/N approval) layer on top — TODO.
import socket, time, json, M5
from M5 import Lcd

BOARD = "192.168.1.50:7430"          # host:port of watchtower-board (LAN)
POLL_MS = 2000
# reuse wifi_event.connect() from the buddy bundle to associate before run().

def _hue(running, queued):
    if running: return 0x00C000      # green: work in flight
    if queued:  return 0xC0A000      # amber: queued, nothing running
    return 0x303030                  # dim idle

def _draw(c):
    Lcd.clear()
    Lcd.fillRect(0, 0, 240, 6, _hue(c.get("running",0), c.get("queued",0)))
    Lcd.setCursor(6, 18); Lcd.printf("running   %d", c.get("running", 0))
    Lcd.setCursor(6, 40); Lcd.printf("queued    %d", c.get("queued", 0))
    Lcd.setCursor(6, 62); Lcd.printf("done      %d", c.get("done", 0))
    Lcd.setCursor(6, 84); Lcd.printf("swaggers  %d", c.get("swaggers", 0))

def _get_state(host, port):
    s = socket.socket(); s.connect(socket.getaddrinfo(host, port)[0][-1])
    s.send(("GET /api/state HTTP/1.0\r\nHost: %s\r\n\r\n" % host).encode())
    buf = b""
    while True:
        d = s.recv(512)
        if not d: break
        buf += d
    s.close()
    body = buf.split(b"\r\n\r\n", 1)[1]              # strip headers
    return json.loads(body).get("counts", {})

def run():
    M5.begin()
    host, port = BOARD.split(":"); port = int(port)
    while True:
        try:
            _draw(_get_state(host, port))
        except Exception:
            pass                                     # board down / wifi drop → keep last screen
        time.sleep_ms(POLL_MS)

run()
```

> Stage 2 adds a text-entry mode → `POST /api/ticket {text}` (reuse the Buddy bundle's `MatrixKeyboard`). Stage 3 (post-Sentinel) subscribes to `waiting` events, beeps (`M5.Speaker.tone`), shows tool/hint, and POSTs a Y/N decision.
