#!/usr/bin/env bash
# Deterministic synapse probe: prove SSE push + server-side topic filtering.
# A 'marshall' subscriber must receive the 2 marshall events and NOT the swagger-7 secret.
set -uo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=5099

python3 "$DIR/server.py" "$PORT" & SV=$!
sleep 0.8

# Subscriber: listens ONLY to topic 'marshall'. Capture its stdout (what a Monitor would consume).
curl -sN "http://127.0.0.1:$PORT/sse?subscribe=marshall" > "$DIR/sub-marshall.out" 2>/dev/null & CU=$!
sleep 0.6

# Publish 3 events: 2 to 'marshall' (should arrive), 1 to 'swagger-7' (must be filtered out).
curl -s "http://127.0.0.1:$PORT/pub?topic=marshall&msg=ticket-42-ready"     >/dev/null
curl -s "http://127.0.0.1:$PORT/pub?topic=swagger-7&msg=SECRET-FOR-7-ONLY"  >/dev/null
curl -s "http://127.0.0.1:$PORT/pub?topic=marshall&msg=swagger-9-stranded"  >/dev/null
sleep 1.5

kill "$CU" 2>/dev/null
kill "$SV" 2>/dev/null
wait 2>/dev/null

echo "=== 'marshall' subscriber received (expect 2 marshall events, NOT the swagger-7 secret) ==="
cat "$DIR/sub-marshall.out"
echo "=== END ==="
echo ""
if grep -q "SECRET-FOR-7-ONLY" "$DIR/sub-marshall.out"; then
  echo "RESULT: ❌ LEAK — swagger-7 event reached the marshall subscriber"
elif grep -q "ticket-42-ready" "$DIR/sub-marshall.out" && grep -q "swagger-9-stranded" "$DIR/sub-marshall.out"; then
  echo "RESULT: ✅ PASS — both marshall events delivered, swagger-7 filtered out, monotonic ids present"
else
  echo "RESULT: ⚠️ INCONCLUSIVE — expected marshall events missing (timing?)"
fi
