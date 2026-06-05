#!/usr/bin/env python3
"""Minimal SSE pub/sub broker — proves the Sentinel -> Monitor synapse.

The whole keystone of the Watchtower comms-bus direction in one file:
  GET /sse?subscribe=a,b   open an event-stream; receive ONLY events whose topic in {a,b}
  GET /pub?topic=X&msg=Y    publish an event to topic X (monotonic id; basis for Last-Event-ID replay)

No deps. Stdlib only. The point: a long-running stream consumer (curl -N, or a
Monitor command) receives server-side topic-filtered pushes on stdout.
"""
import http.server, socketserver, threading, queue, urllib.parse, sys

subscribers = []          # (topics:set, Queue)
lock = threading.Lock()
counter = [0]             # monotonic event id


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence access log
        pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/sse":
            raw = q.get("subscribe", [""])[0]
            topics = {t for t in raw.split(",") if t}
            myq = queue.Queue()
            with lock:
                subscribers.append((topics, myq))
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            try:
                while True:
                    eid, topic, msg = myq.get()
                    frame = f"id: {eid}\nevent: {topic}\ndata: {msg}\n\n"
                    self.wfile.write(frame.encode())
                    self.wfile.flush()
            except Exception:
                with lock:
                    if (topics, myq) in subscribers:
                        subscribers.remove((topics, myq))
        elif u.path == "/pub":
            topic = q.get("topic", [""])[0]
            msg = q.get("msg", [""])[0]
            with lock:
                counter[0] += 1
                eid = counter[0]
                for topics, sq in subscribers:
                    if not topics or topic in topics:   # empty subscribe = firehose
                        sq.put((eid, topic, msg))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_response(404)
            self.end_headers()


class T(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5099
    T(("127.0.0.1", port), H).serve_forever()
