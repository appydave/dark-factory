# Front Desk — Cardputer-Adv device bundle

Stage-1 "Factory Front Desk": an M5Stack Cardputer ADV app that polls the
watchtower-board `GET /api/state` every ~2s over WiFi and shows
running / queued / done / swaggers counts with a status colour bar.

**Status**: working (flashed + running on Roamy's Cardputer, 2026-06-13).

> **General Cardputer/UIFlow/flashing knowledge** (download-mode dance, esptool
> version, app model, WiFi gotchas) lives in the **`stream-deck` brain** →
> `~/dev/ad/brains/stream-deck/cardputer-flashing.md`. This README is just the
> project runbook.

## Bundle layout (how install_apps maps it)

- `apps/frontdesk.py` → `/flash/apps/` (the app; shows in the UIFlow launcher)
- `wifi_event.py` → `/flash/` (WiFi connect helper; **gitignored** — holds real creds)
- `main.py` → `/flash/` (auto-run shim; presence makes install set `boot_option=2`)
- `tools/frontdesk-harness.py` → **not pushed** (host-side CPython parity test)

## Config (edit before pushing)

- **Board IP** — `BOARD = "192.168.1.138:7430"` at the top of `apps/frontdesk.py`.
  This is Roamy's LAN IP and **changes with DHCP** — update it if Roamy's IP moves.
- **WiFi** — `wifi_event.py` holds `SSID` + `PASSWORD` (currently `Appy Dave_2.4GHz`
  + the real password). **2.4 GHz only** — the Cardputer can't see 5 GHz networks.
  This file is gitignored; never commit real creds.

## Push to device (no flash, no button-dance)

```bash
PYTHONPATH=~/dev/upstream/repos/build-with-claude/.claude/skills/m5-onboard/scripts/vendor \
/tmp/m5venv/bin/python \
~/dev/upstream/repos/build-with-claude/.claude/skills/m5-onboard/scripts/install_apps.py \
  --port /dev/cu.usbmodemXXXX \
  --src ~/dev/ad/apps/dark-factory/experiments/watchtower-board/device
```
Because `main.py` is present, the device **auto-runs straight into the Front Desk**
on reboot (no launcher menu). Find the port with `ls /dev/cu.usbmodem*`.

## Pre-flight (prove the logic before flashing)

```bash
python3 tools/frontdesk-harness.py        # hits localhost:7430, same socket/parse logic
```

## Requirements to actually show data

1. The board server must be running on Roamy: `node ../server.mjs` (port 7430).
2. Roamy's LAN IP must match `BOARD` in `frontdesk.py`.
3. The Cardputer must be on the **same 2.4 GHz network** as Roamy.

## Run untethered (on battery)

Flip the device's **slide power switch ON** and let it charge over USB. Then it
runs the Front Desk on battery when unplugged. (With the switch off it only runs
while USB-powered — unplugging kills it.)
