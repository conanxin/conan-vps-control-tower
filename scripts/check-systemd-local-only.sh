#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="conan-vps-control-tower"
HOST="127.0.0.1"
PORT="3001"
BASE_URL="http://${HOST}:${PORT}"

echo "Checking conan-vps-control-tower systemd local-only status..."
echo

if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-enabled --quiet "${SERVICE_NAME}"; then
    echo "Service enabled: yes"
  else
    echo "Service enabled: no"
  fi

  if systemctl is-active --quiet "${SERVICE_NAME}"; then
    echo "Service active: yes"
  else
    echo "Service active: no"
  fi
else
  echo "systemctl not available on this environment."
fi

if command -v ss >/dev/null 2>&1; then
  if ss -lnt | awk '{print $4}' | grep -Eq "(^|:)${HOST}:${PORT}$|(^|:)${PORT}$"; then
    echo "Listener check: ${HOST}:${PORT} is listening."
  else
    echo "Listener check: ${HOST}:${PORT} is not listening."
  fi

  if ss -lnt | awk '{print $4}' | grep -Eq "0\.0\.0\.0:${PORT}$|\[::\]:${PORT}$"; then
    echo "Public bind check: found 0.0.0.0:${PORT} or [::]:${PORT}."
  else
    echo "Public bind check: none detected."
  fi
else
  echo "ss is not available; skip socket checks."
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
check_endpoint "/api/diagnostics"
check_endpoint "/api/alerts/status"

echo
echo "Recent logs:"
journalctl -u "${SERVICE_NAME}" --no-pager -n 80
