#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:3001"
TEMPLATE="deploy/cloudflare-tunnel/config.example.yml"

echo "Conan VPS Control Tower domain-access readiness"
echo

echo "Service status:"
if command -v systemctl >/dev/null 2>&1; then
  systemctl is-active conan-vps-control-tower || true
  systemctl is-enabled conan-vps-control-tower || true
else
  echo "systemctl not available."
fi
echo

echo "Listener check:"
ss -lntup 2>/dev/null | grep -E ':3001\b' || true
if ss -lntup 2>/dev/null | grep -E '127\.0\.0\.1:3001\b' >/dev/null 2>&1; then
  echo "127.0.0.1:3001 listener present."
else
  echo "127.0.0.1:3001 listener missing."
fi
if ss -lntup 2>/dev/null | grep -E '(^|[[:space:]])(0\.0\.0\.0|\[::\]):3001\b' >/dev/null 2>&1; then
  echo "WARNING: public 3001 listener found."
else
  echo "No public 3001 listener found."
fi
echo

echo "API health:"
curl -s --show-error --max-time 5 "${BASE_URL}/api/health" || true
echo
echo

echo "API meta:"
META="$(curl -s --show-error --max-time 5 "${BASE_URL}/api/meta" || true)"
printf '%s\n' "${META}"
if printf '%s\n' "${META}" | grep -q '"local_only"[[:space:]]*:[[:space:]]*true'; then
  echo "local_only=true confirmed."
else
  echo "local_only flag not confirmed."
fi
echo

echo "cloudflared:"
if command -v cloudflared >/dev/null 2>&1; then
  cloudflared --version || true
else
  echo "cloudflared is not installed. This script will not install it."
fi
echo

echo "Template:"
if [ -f "${TEMPLATE}" ]; then
  echo "${TEMPLATE} exists."
else
  echo "${TEMPLATE} missing."
fi
echo

echo "This script does not authenticate cloudflared, create a tunnel, modify configs, or change firewall settings."
