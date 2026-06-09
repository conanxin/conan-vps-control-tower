#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:3001"

echo "Checking alert setup..."
echo

for endpoint in \
  "/api/alerts/config-check" \
  "/api/alerts/status"; do
  echo "GET ${BASE_URL}${endpoint}"
  if command -v jq >/dev/null 2>&1; then
    curl -s --show-error --max-time 5 "${BASE_URL}${endpoint}" | jq
  else
    curl -s --show-error --max-time 5 "${BASE_URL}${endpoint}"
    echo
  fi
  echo
done

echo "No sensitive fields (bot_token/password/chat_id) should be shown above."

