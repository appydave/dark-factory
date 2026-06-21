# Plan: Factory Front Desk on the Cardputer-Adv (Stage 1)

**Job**: Get a working "Factory Front Desk" app running on the physical M5Stack Cardputer-Adv — a battery-powered desk device whose LCD shows live dark-factory state (running / queued / done / swaggers + a status-colour bar) polled over WiFi from the existing `watchtower-board` `/api/state` endpoint, with numbers that move in real time as tickets flow queue→running→done. The build front-loads **all** software verification into a Claude Code Workflow that touches no hardware, so the device is flashed exactly once for a clean flash-and-watch rather than an iterative on-device debug loop.

**Mode**: code

**Created**: 2026-06-12

---

## 1. Stack

- **Hardware**: M5Stack Cardputer-Adv (ESP32-S3, native USB, 1.14" LCD, 56-key keyboard, 1W speaker, BMI270 IMU, WiFi, 1750 mAh battery). Connected to Roamy via USB-C.
- **Current device firmware**: a non-UIFlow launcher — boots to "M5Stack BtnGOHome v0.2 — any key to start". Our app targets the UIFlow 2.0 MicroPython runtime, which is **not** present yet → Phase 3 flashes UIFlow 2.0 over this launcher.
- **Runtime (target)**: UIFlow 2.0 / MicroPython. On-device modules used: `M5` / `Lcd`, `network`, `socket`, `json`, `time`.
- **Onboarding tooling**: cwc-makers plugin (`/maker-setup`) **or** the vendored skill at `~/dev/upstream/repos/build-with-claude/.claude/skills/m5-onboard/` — `onboard.py` (full flash), `install_apps.py --skip-flash --src <dir>` (push only), `scripts/tail_serial.py` (serial log), `scripts/mpy_repl.py` (REPL).
- **Device-API idiom source (de-risk)**: `~/dev/upstream/repos/build-with-claude/buddy/device/apps/hello_cardputer.py` (LCD + keyboard conventions), `claude_buddy.py` (networking + speaker), `wifi_event.py` (STA connect pattern). Copy their exact UIFlow 2.0 calls — do not guess the API.
- **Data source**: `experiments/watchtower-board/server.mjs` on **:7430**, endpoint `GET /api/state` → `{ queue:[…], running:[…], done:[…], counts:{ queued, running, done, swaggers } }`. The board reads `experiments/watchtower-engine/{queue,running,done,reports}/` + tmux `swagger-*` windows; all timestamps from the OS, never an LLM.
- **Board host**: Roamy (this Mac), LAN IP **192.168.1.188** → app polls `http://192.168.1.188:7430/api/state`. (Tailscale 100.89.32.35 available as fallback.)
- **Build method**: a Claude Code **Workflow** (multi-agent) for the software-prep phase — see §How it runs.
- **Device bundle location**: `experiments/watchtower-board/device/` (`apps/frontdesk.py`, `wifi_event.py`, `tools/frontdesk-harness.py`).

## 2. In Scope

- A MicroPython app `frontdesk.py` that: associates to David's WiFi, polls `/api/state` every ~2 s, parses `counts`, renders running / queued / done / swaggers + a status-colour bar on the LCD, and survives WiFi/board drops (keeps last screen, retries on reconnect).
- A `wifi_event.py` override carrying David's real SSID/password — local, git-ignored, never committed.
- A host-side CPython harness (`frontdesk-harness.py`) that mirrors the device's socket+parse logic against the **real** `/api/state`, proving the contract before any flash.
- Flashing UIFlow 2.0 + installing the app on the physical device; bringing it live on battery.
- Dropping a handful of test `queue/*.json` tickets into `watchtower-engine/queue/` to demonstrate live movement.

## 3. Out of Scope

- **Stage 2** (keyboard → POST ticket) and **Stage 3** (approval pager / `waiting` events / the Sentinel return-leg). Separate, gated on the Sentinel.
- Any **BLE** path — UIFlow 2.0 BLE is unauthenticated; Stage 1 is WiFi/HTTP only.
- Building the **Dark Factory Sentinel** or an SSE bus.
- **Write/POST routes** on the board (Stage 1 is read-only; `/api/ticket` belongs to Stage 2).
- **Auth** on board routes (no writes happen in Stage 1).
- Promoting the board out of `experiments/` into AppyStack.
- Any change to `watchtower-engine/` or `run-next-workflow`.

## 4. Definition of Done

**David watches the four counts on the physical ADV screen change in real time** as test tickets move through the queue (queued↑ on drop → running↑ when an in-session loop claims → done↑ on completion), with the device running on battery (USB unplugged).

*Autonomous-/goal slice (machine-checkable, no hardware): AC 1–4 — the verified, ready-to-push software bundle plus a passing host harness against the live board. AC 5–8 require the physical device and David's eyes and are a human-gated follow-on, not part of the autonomous run.*

## 5. Acceptance Criteria

| # | Criterion | How to check |
|---|-----------|--------------|
| 1 | Board endpoint live & correctly shaped | `curl -s http://192.168.1.188:7430/api/state \| jq -e '.counts\|has("queued") and has("running") and has("done") and has("swaggers")'` exits 0 |
| 2 | Host harness parses real state | `python3 experiments/watchtower-board/device/tools/frontdesk-harness.py` exits 0 and prints the 4 counts matching the curl above |
| 3 | `frontdesk.py` verified | `experiments/watchtower-board/device/apps/frontdesk.py` exists; a CPython-shimmed copy passes `python3 -m py_compile`; adversarial-review verdict = pass |
| 4 | WiFi override present & uncommitted | `experiments/watchtower-board/device/wifi_event.py` carries the real SSID; `git check-ignore` reports it ignored |
| 5 | Device flashed + app installed | `install_apps.py` prints `WROTE /flash/apps/frontdesk.py`; device boots to the UIFlow launcher listing "frontdesk" |
| 6 | Device joins WiFi | `tail_serial.py` output shows the STA obtained an IP |
| 7 | Counts render on LCD | **David confirms** the four numbers + colour bar are visible on screen (eyes-on; the agent cannot read the LCD) |
| 8 | Numbers move live | drop 3 `queue/*.json` → David confirms `queued` increments within one poll (~2 s); `running`/`done` track as the engine claims and finishes |

## 6. Key References

- **Spec**: `/Users/davidcruwys/dev/ad/apps/dark-factory/backlog/2026-06-12-cardputer-frontdesk.md`
- **Board server**: `/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/watchtower-board/server.mjs`
- **Engine** (queue shape, mutex): `/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/watchtower-engine/README.md`
- **Onboard skill**: `/Users/davidcruwys/dev/upstream/repos/build-with-claude/.claude/skills/m5-onboard/SKILL.md`
- **Device idioms**: `/Users/davidcruwys/dev/upstream/repos/build-with-claude/buddy/device/apps/hello_cardputer.py`, `claude_buddy.py`, `wifi_event.py`
- **cwc-makers plugin**: `/plugin install cwc-makers@claude-plugins-official`

---

## How it runs — phases + the Workflow

| Phase | What | Device? | Owner |
|------|------|:--:|-----|
| **0 · Prereqs** | Confirm device state ✅, board host ✅ (Roamy 192.168.1.188), **provide WiFi SSID/password** | — | David |
| **1 · Software (Workflow)** | Pipeline: **[A** harvest device-API cheat-sheet from the buddy bundle · **B** verify `/api/state` contract from `server.mjs` + a live `curl`**]** → **C** write `frontdesk.py` + `wifi_event.py` override + host harness → **D** adversarial review (WiFi drop, board-down, malformed JSON, MicroPython-vs-CPython API mismatch, HTTP read semantics). Output: a **green, ready-to-push bundle**. | none | agents |
| **2 · Board up** | `node experiments/watchtower-board/server.mjs` (:7430); confirm `/api/state`; AC 1 + 2 green | — | agent |
| **3 · Flash + push** | `/maker-setup` flashes UIFlow 2.0 over BtnGOHome + installs `frontdesk.py`. **Native-USB button-dance** (hold BtnG0, tap BtnRST, release RST, hold G0 ~1 s, release). | yes | David (buttons) |
| **4 · Go live** | Boot; watch the STA connect (`tail_serial.py`); drop 3 test tickets → **David watches the numbers move** on the LCD. | yes | David + agent |
| **5 · Verify + capture** | Walk AC 1–8; mark the backlog item; write a short KDD/learnings note. | — | agent |

The Workflow is used **only where it adds value** — Phase 1's four strands are independent and the adversarial pass is a "verify before an expensive (physical) commit" gate. It is deliberately **not** sprayed across the trivial steps.

**Honesty on the gates**: AC 7 & 8 are eyes-on-David — the agent cannot read the LCD. `/goal` can drive Phases 1–2 autonomously to a verified bundle; it **cannot** press buttons or see the screen, so Phases 3–4 are a ~20-minute live session, walked through interactively, not an autonomous run.

---

## Suggested `/goal` condition

```
Stage-1 Factory Front Desk software bundle is built and verified WITHOUT touching the physical Cardputer, such that: (1) watchtower-board is running on Roamy and `curl -s http://192.168.1.188:7430/api/state | jq -e '.counts|has("queued") and has("running") and has("done") and has("swaggers")'` exits 0; (2) `python3 experiments/watchtower-board/device/tools/frontdesk-harness.py` runs against that live endpoint, prints the four counts, and exits 0; (3) `experiments/watchtower-board/device/apps/frontdesk.py` exists and a CPython-shimmed copy passes `python3 -m py_compile`; (4) `experiments/watchtower-board/device/wifi_event.py` exists with the real SSID and `git check-ignore` reports it ignored. Constraints that must NOT change: do not modify experiments/watchtower-engine/ or run-next-workflow; add no write/POST routes to server.mjs (Stage 1 is read-only); WiFi/HTTP only, never BLE; board is 192.168.1.188:7430. Do NOT flash or push to the device — physical flash + on-screen verification are a human-gated follow-on. Stop when criteria 1-4 are all green, or stop after 18 turns.
```
