#!/usr/bin/env bash
set -euo pipefail

base="http://127.0.0.1:3000"

echo "Checking gateway..."
curl -fsS "$base/health" | grep -q 'ok'

echo "Checking aggregated services..."
curl -fsS "$base/api/status" > /tmp/polyglot-status.json
cat /tmp/polyglot-status.json

echo "Checking SQL-backed search..."
curl -fsS --get "$base/api/search" --data-urlencode 'q=alice' | grep -qi 'alice'

echo "Checking PHP file endpoint..."
curl -fsS --get "$base/api/files" --data-urlencode 'name=welcome.txt' | grep -qi 'training lab'

echo "Checking Java access-control demo..."
curl -fsS "$base/api/java/users?id=1" | grep -qi 'alice'

echo "Checking C# access-control demo..."
curl -fsS "$base/api/csharp/accounts/1" | grep -qi 'checking'

echo "Checking COBOL report..."
curl -fsS --get "$base/api/report" --data-urlencode 'name=Alice' | grep -qi 'Alice'

echo "Smoke test passed."
