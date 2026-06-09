#!/usr/bin/env bash
set -euo pipefail

echo "Conan VPS Control Tower local-only preflight"
echo

if [ ! -f "pyproject.toml" ] || [ ! -d "app" ] || [ ! -f "config.example.yaml" ]; then
  echo "Project root check: failed. Run this from the conan-vps-control-tower root."
  exit 1
fi

echo "Project root check: ok"
echo "Date: $(date -Is 2>/dev/null || date)"
echo "OS: $(uname -a 2>/dev/null || echo unknown)"
echo "Working directory: $(pwd)"
echo "Python: $(python3 --version 2>/dev/null || python --version 2>/dev/null || echo not found)"
echo

if [ -f "config.yaml" ]; then
  echo "config.yaml: found"
  if grep -Eq '^[[:space:]]*host:[[:space:]]*"127\.0\.0\.1"[[:space:]]*$' config.yaml; then
    echo "server.host: 127.0.0.1 confirmed"
  else
    echo "server.host: not clearly 127.0.0.1. Check config.yaml before starting."
  fi
else
  echo "config.yaml: missing. Copy config.example.yaml to config.yaml before running."
fi

echo
echo "Listening checks:"
if command -v ss >/dev/null 2>&1; then
  echo "- 127.0.0.1:3001:"
  ss -lntup 2>/dev/null | grep -E '127\.0\.0\.1:3001\b' || true
  echo "- 0.0.0.0:3001 or [::]:3001:"
  ss -lntup 2>/dev/null | grep -E '0\.0\.0\.0:3001\b|\[::\]:3001\b' || true
  echo "- ports 80/443 currently listening:"
  ss -lntup 2>/dev/null | grep -E ':80\b|:443\b' || true
else
  echo "ss is not available; skipping socket checks."
fi

echo
echo "Proxy-related process visibility:"
ps -eo pid,comm,args,%cpu,%mem --sort=-%mem 2>/dev/null | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' | grep -v grep || true

echo
echo "Next steps:"
echo "1. Keep server.host at 127.0.0.1 and port at 3001."
echo "2. Start manually with: uvicorn app.main:app --host 127.0.0.1 --port 3001"
echo "3. Check APIs with: bash scripts/check-local-only-status.sh"
echo "4. Use SSH tunnel from local machine: ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST"
echo
echo "This script did not start services, restart proxy tools, change firewall rules, install packages, or write system config."
