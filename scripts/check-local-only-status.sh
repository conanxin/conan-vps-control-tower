#!/usr/bin/env bash
set -euo pipefail

HOST="127.0.0.1"
PORT="3001"
BASE_URL="http://${HOST}:${PORT}"

echo "Checking Conan VPS Control Tower local-only status..."

if command -v ss >/dev/null 2>&1; then
  if ss -lnt | awk '{print $4}' | grep -Eq "(^|:)${HOST}:${PORT}$|(^|:)${PORT}$"; then
    echo "Listener check: ${HOST}:${PORT} appears to be listening."
  else
    echo "Listener check: ${HOST}:${PORT} does not appear to be listening."
    echo "Start command:"
    echo "  source .venv/bin/activate"
    echo "  uvicorn app.main:app --host 127.0.0.1 --port 3001"
  fi

  if ss -lnt | awk '{print $4}' | grep -Eq "0\.0\.0\.0:${PORT}$|\[::\]:${PORT}$"; then
    echo "Warning: ${PORT} appears to be bound publicly. Phase 1A.2 expects local-only binding."
  else
    echo "Public bind check: no 0.0.0.0:${PORT} listener found."
  fi
else
  echo "Listener check: ss is not available; skipping socket inspection."
fi

check_endpoint() {
  local path="$1"
  local url="${BASE_URL}${path}"

  echo
  echo "GET ${url}"
  if curl --silent --show-error --max-time 5 "$url"; then
    echo
    echo "Result: ${path} OK"
  else
    echo
    echo "Result: ${path} failed"
  fi
}

check_endpoint "/api/health"
check_endpoint "/api/system"
check_endpoint "/api/proxy"

echo
echo "This script does not modify system services, 3X-UI, proxy configuration, or firewall rules."
