#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:3001"

echo "Conan VPS Control Tower domain-access discovery"
echo

echo "Control Tower listener:"
if ss -lntup 2>/dev/null | grep -E '127\.0\.0\.1:3001\b' >/dev/null 2>&1; then
  ss -lntup 2>/dev/null | grep -E '127\.0\.0\.1:3001\b' || true
  echo "tower target: http://127.0.0.1:3001"
else
  echo "127.0.0.1:3001 listener not found."
  echo "tower target: http://127.0.0.1:3001 (expected after service starts)"
fi
echo

echo "Public bind check for 3001:"
if ss -lntup 2>/dev/null | grep -E '(^|[[:space:]])(0\.0\.0\.0|\[::\]):3001\b' >/dev/null 2>&1; then
  echo "WARNING: public 3001 listener found. Review config before using domain access."
  ss -lntup 2>/dev/null | grep -E '(^|[[:space:]])(0\.0\.0\.0|\[::\]):3001\b' || true
else
  echo "No 0.0.0.0:3001 or [::]:3001 listener found."
fi
echo

echo "3X-UI / proxy related processes:"
ps -eo pid,comm,args,%cpu,%mem --sort=-%mem 2>/dev/null \
  | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' \
  | grep -v grep || true
echo

echo "Possible panel listeners:"
PANEL_LINES="$(ss -lntup 2>/dev/null | grep -Ei 'x-ui|3x-ui|:2053|:54321|:8443|:8080' || true)"
if [ -n "${PANEL_LINES}" ]; then
  printf '%s\n' "${PANEL_LINES}"
else
  echo "No obvious panel listener detected. Check your private 3X-UI panel port manually."
fi
echo

PANEL_PORT="$(printf '%s\n' "${PANEL_LINES}" \
  | sed -nE 's/.*:([0-9]+)[[:space:]].*/\1/p' \
  | grep -Ev '^(80|443|3001)$' \
  | head -n 1 || true)"

if [ -n "${PANEL_PORT}" ]; then
  echo "panel target: https://127.0.0.1:${PANEL_PORT}"
else
  echo "panel target: https://127.0.0.1:YOUR_3XUI_PANEL_PORT"
fi
echo

echo "Current 80/443 listeners (shown only, not changed):"
ss -lntup 2>/dev/null | grep -Ei ':80\b|:443\b' || true
echo

echo "This script is read-only. It does not install cloudflared, create tunnels, change firewall settings, or restart services."
