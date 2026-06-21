"""Factory Front Desk — watchtower-board counts on the Cardputer-Adv.

Polls GET /api/state on the board every ~2s over a raw socket
(HTTP/1.0 + Connection: close → server closes after the body, so
read-until-EOF is safe; we still de-chunk if the response says
Transfer-Encoding: chunked, per the strand-B contract) and renders
counts.running / counts.queued / counts.done / counts.swaggers.

NOTE: counts.done is the TRUE total — the done[] array is capped at
12 items server-side. Always read counts, never len(done).

Launcher conventions: lives in /flash/apps/, defines run(), calls
run() bare at module bottom. ESC or Q exits back to the launcher via
machine.reset().
"""

import sys
for _p in ("/flash", "/flash/apps"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import M5
import machine
import time
import socket
import json

import wifi_event

# --- Config -------------------------------------------------------------
BOARD = "192.168.1.138:7430"   # host:port of the watchtower-board server (Roamy on AppyDave_2.4GHz)
POLL_MS = 2000                  # poll cadence
HTTP_TIMEOUT_S = 5              # per-request socket timeout

# --- Screen -------------------------------------------------------------
_W = 240
_H = 135

_BLACK = 0x000000
_ORANGE = 0xCC785C
_CREAM = 0xF0EEE6
_DARK = 0x1F1F1F
_GRAY_MID = 0x777777
_GREEN = 0x00FF00
_AMBER = 0xFFB000
_RED = 0xFF0000

_LCD = None  # set in run()


# --- HTTP: raw-socket GET /api/state ------------------------------------

def _dechunk(body):
    """Decode a chunked transfer-encoded body (bytes -> bytes).

    Format: <hex-size>\r\n<data>\r\n ... terminated by 0\r\n\r\n.
    """
    out = b""
    i = 0
    while True:
        j = body.find(b"\r\n", i)
        if j < 0:
            break
        size_line = body[i:j].split(b";")[0].strip()
        try:
            size = int(size_line, 16)
        except ValueError:
            break
        if size == 0:
            break
        start = j + 2
        out += body[start:start + size]
        i = start + size + 2  # skip trailing \r\n after the chunk
    return out


def _fetch_counts():
    """GET /api/state from BOARD, return the counts dict.

    Raises on any failure — caller wraps in try/except.
    """
    host, port = BOARD.split(":")
    port = int(port)

    addr = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    try:
        s.settimeout(HTTP_TIMEOUT_S)
        s.connect(addr)
        req = (
            "GET /api/state HTTP/1.0\r\n"
            "Host: {}:{}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).format(host, port)
        s.send(req.encode())

        # HTTP/1.0 + Connection: close → server closes after the body,
        # so read until EOF is safe here (unlike the keep-alive 1.1
        # case strand B warned about).
        raw = b""
        while True:
            chunk = s.recv(512)
            if not chunk:
                break
            raw += chunk
    finally:
        s.close()

    sep = raw.find(b"\r\n\r\n")
    if sep < 0:
        raise ValueError("no header/body split")
    headers = raw[:sep].decode()
    body = raw[sep + 4:]

    status_line = headers.split("\r\n")[0]
    if " 200 " not in status_line + " ":
        raise ValueError("bad status: " + status_line)

    headers_low = headers.lower()
    if "transfer-encoding: chunked" in headers_low:
        body = _dechunk(body)

    state = json.loads(body)
    return state["counts"]


# --- Rendering -----------------------------------------------------------

def _draw_static():
    _LCD.fillScreen(_BLACK)
    # Header band
    _LCD.fillRect(0, 0, _W, 20, _DARK)
    _LCD.setTextSize(1)
    _LCD.setTextColor(_ORANGE, _DARK)
    _LCD.drawString("FACTORY FRONT DESK", 6, 5)
    _LCD.setTextColor(_GRAY_MID, _DARK)
    _LCD.drawString(BOARD, _W - _LCD.textWidth(BOARD) - 6, 5)
    # Orange hairline under header
    _LCD.fillRect(0, 20, _W, 1, _ORANGE)
    # Hint strip
    _LCD.fillRect(0, _H - 18, _W, 18, _DARK)
    _LCD.setTextColor(_GRAY_MID, _DARK)
    _LCD.drawString("ESC/Q exit   poll 2s", 6, _H - 14)


def _draw_counts(counts):
    running = counts.get("running", 0)
    queued = counts.get("queued", 0)
    done = counts.get("done", 0)
    swaggers = counts.get("swaggers", 0)

    # Status colour bar: green if running, amber if queued, else dim
    if running > 0:
        bar = _GREEN
    elif queued > 0:
        bar = _AMBER
    else:
        bar = _GRAY_MID
    _LCD.fillRect(0, 22, _W, 6, bar)

    # Counts — blank the body region, then redraw
    _LCD.fillRect(0, 30, _W, _H - 18 - 30, _BLACK)
    _LCD.setTextSize(2)
    _LCD.setTextColor(_CREAM, _BLACK)
    _LCD.drawString("run {}   que {}".format(running, queued), 6, 36)
    _LCD.drawString("done {}".format(done), 6, 60)
    _LCD.setTextSize(1)
    _LCD.setTextColor(_GRAY_MID, _BLACK)
    _LCD.drawString("swaggers: {}".format(swaggers), 6, 86)


def _draw_status(msg, color):
    """Right side of the hint strip: last poll result / error."""
    _LCD.setTextSize(1)
    _LCD.fillRect(110, _H - 18, _W - 110, 18, _DARK)
    _LCD.setTextColor(color, _DARK)
    if _LCD.textWidth(msg) > _W - 116:
        msg = msg[:20]
    _LCD.drawString(msg, _W - _LCD.textWidth(msg) - 6, _H - 14)


# --- Keyboard ------------------------------------------------------------

def _is_exit_key(k):
    """ESC (0x1B) or 'q'/'Q' exits. get_key() may return int, len-1
    str, len-1 bytes/bytearray, or None — handle all forms."""
    if k is None:
        return False
    if isinstance(k, int):
        code = k
    elif isinstance(k, (bytes, bytearray)) and len(k) == 1:
        code = k[0]
    elif isinstance(k, str) and len(k) == 1:
        code = ord(k)
    else:
        return False
    return code == 0x1B or code in (ord("q"), ord("Q"))


# --- Main ----------------------------------------------------------------

def run():
    global _LCD
    try:
        M5.begin()  # idempotent — boot.py already ran it under boot_option=2
    except Exception:
        pass
    _LCD = M5.Lcd
    try:
        _LCD.setFont(_LCD.FONTS.DejaVu9)
    except Exception:
        pass  # some builds lack FONTS

    _draw_static()
    _LCD.setTextSize(1)
    _LCD.setTextColor(_CREAM, _BLACK)
    _LCD.drawString("connecting wifi...", 6, 36)

    st = wifi_event.connect()
    if st.get("ok"):
        _LCD.fillRect(0, 30, _W, 30, _BLACK)
        _LCD.setTextColor(_GRAY_MID, _BLACK)
        _LCD.drawString("wifi ok  {}".format(st.get("ip", "?")), 6, 36)
    else:
        _LCD.fillRect(0, 30, _W, 30, _BLACK)
        _LCD.setTextColor(_RED, _BLACK)
        _LCD.drawString("wifi FAIL: {}".format(st.get("err", "?"))[:38], 6, 36)
        # keep going — poll loop will retry-fail visibly via status strip

    # Keyboard — construct after hardware settles, debounce launch key
    from hardware import MatrixKeyboard
    time.sleep_ms(400)
    kb = MatrixKeyboard()
    time.sleep_ms(400)

    try:
        last_poll = time.ticks_ms() - POLL_MS  # poll immediately
        while True:
            kb.tick()
            if _is_exit_key(kb.get_key()):
                return

            now = time.ticks_ms()
            if time.ticks_diff(now, last_poll) >= POLL_MS:
                last_poll = now
                # Each poll fully guarded — never kill the loop. On
                # failure keep the last counts on screen and retry.
                try:
                    counts = _fetch_counts()
                    _draw_counts(counts)
                    _draw_status("ok", _GREEN)
                except Exception as e:
                    _draw_status("err: {}".format(e)[:20], _RED)

            time.sleep_ms(40)
    finally:
        # UIFlow 2.0 has no return-to-launcher API; soft-reboot back.
        _LCD.fillScreen(_BLACK)
        time.sleep_ms(200)
        machine.reset()


run()  # bare call at module bottom — launcher entrypoint (NOT __main__)
