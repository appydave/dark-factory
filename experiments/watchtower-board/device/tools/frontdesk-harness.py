#!/usr/bin/env python3
"""Host-side harness for frontdesk.py — pure CPython3, runs on the Mac.

Replicates the device's raw-socket GET /api/state + header-split +
de-chunk + json-parse logic against the watchtower-board server.
Passing here proves the device read/parse logic is sound BEFORE
flashing.

Usage:
    python3 frontdesk-harness.py [host] [port]   # default localhost 7430
    python3 frontdesk-harness.py host:port

Exit 0 on success (prints the four counts), non-zero on any failure.

Keep this parsing logic identical in spirit to apps/frontdesk.py.
"""

import json
import socket
import sys

HTTP_TIMEOUT_S = 5


def _dechunk(body: bytes) -> bytes:
    """Decode a chunked transfer-encoded body — same algorithm as
    frontdesk.py: <hex-size>\\r\\n<data>\\r\\n ... 0\\r\\n\\r\\n."""
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
        i = start + size + 2
    return out


def fetch_counts(host: str, port: int) -> dict:
    """Raw-socket HTTP/1.0 GET, read-until-EOF, de-chunk if needed.

    Pin AF_INET/SOCK_STREAM here: CPython getaddrinfo may return an
    IPv6 entry first, which breaks the default AF_INET socket. The
    device (MicroPython) uses the plain two-arg form and gets IPv4.
    """
    addr = socket.getaddrinfo(host, port, socket.AF_INET,
                              socket.SOCK_STREAM)[0][-1]
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
        raise ValueError("no header/body split in response")
    headers = raw[:sep].decode()
    body = raw[sep + 4:]

    status_line = headers.split("\r\n")[0]
    if " 200 " not in status_line + " ":
        raise ValueError("bad status: " + status_line)

    if "transfer-encoding: chunked" in headers.lower():
        body = _dechunk(body)

    state = json.loads(body)
    return state["counts"]


def main(argv) -> int:
    host, port = "localhost", 7430
    args = argv[1:]
    if len(args) == 1 and ":" in args[0]:
        host, p = args[0].split(":", 1)
        port = int(p)
    elif len(args) >= 1:
        host = args[0]
        if len(args) >= 2:
            port = int(args[1])

    try:
        counts = fetch_counts(host, port)
    except Exception as e:
        print("FAIL: {}: {}".format(type(e).__name__, e), file=sys.stderr)
        return 1

    for key in ("running", "queued", "done", "swaggers"):
        if key not in counts:
            print("FAIL: counts missing key '{}'".format(key), file=sys.stderr)
            return 2

    print("running={running} queued={queued} done={done} swaggers={swaggers}"
          .format(**counts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
