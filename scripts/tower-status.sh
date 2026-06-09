#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="conan-vps-control-tower"
HOST="127.0.0.1"
PORT="3001"
BASE_URL="http://${HOST}:${PORT}"

echo "Conan VPS Control Tower status:"
echo

if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet "${SERVICE_NAME}"; then
    echo "systemctl is-active ${SERVICE_NAME}: yes"
  else
    echo "systemctl is-active ${SERVICE_NAME}: no"
  fi

  if systemctl is-enabled --quiet "${SERVICE_NAME}"; then
    echo "systemctl is-enabled ${SERVICE_NAME}: yes"
  else
    echo "systemctl is-enabled ${SERVICE_NAME}: no"
  fi
else
  echo "systemctl is not available."
fi

echo
echo "Listener check:"
if command -v ss >/dev/null 2>&1; then
  ss -lntup | grep 3001 || true
else
  echo "ss is not available."
fi

if ss -lnt | awk '{print $4}' | grep -Eq "(^|:)${HOST}:${PORT}$|(^|:)${PORT}$"; then
  echo "Local-only check: ${HOST}:${PORT} listener present"
else
  echo "Local-only check: ${HOST}:${PORT} listener missing"
fi

if ss -lnt | awk '{print $4}' | grep -Eq "0\.0\.0\.0:${PORT}$|\[::\]:${PORT}$"; then
  echo "Public bind check: found unexpected 0.0.0.0 or [::]:${PORT}"
else
  echo "Public bind check: no 0.0.0.0:${PORT} or [::]:${PORT}"
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
echo "Recent project logs:"
journalctl -u "${SERVICE_NAME}" --no-pager -n 40
