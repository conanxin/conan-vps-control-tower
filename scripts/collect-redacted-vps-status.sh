#!/usr/bin/env bash
set -euo pipefail

OUT="reports/live-vps-redacted-status.txt"
mkdir -p reports

redact() {
  sed -E \
    -e 's/([0-9]{1,3}\.){3}[0-9]{1,3}/REDACTED_IP/g' \
    -e 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/REDACTED_EMAIL/g' \
    -e 's/(token|password|chat_id|bot_token)[=:][^[:space:]]+/\1=REDACTED/Ig'
}

run_section() {
  local title="$1"
  shift
  {
    echo
    echo "## ${title}"
    "$@" 2>&1 || true
  } | redact >> "$OUT"
}

: > "$OUT"
echo "# Conan VPS Control Tower redacted live VPS status" >> "$OUT"
echo "Generated at: $(date -Is 2>/dev/null || date)" | redact >> "$OUT"

run_section "uname" uname -a
run_section "python" sh -c 'python3 --version 2>/dev/null || python --version'
run_section "git" git rev-parse --short HEAD
run_section "systemd status" systemctl status conan-vps-control-tower --no-pager
run_section "listening ports" sh -c "ss -lntup 2>/dev/null | grep -E ':3001\\b|:80\\b|:443\\b|:2053\\b|:8443\\b' || true"
run_section "api health" curl --silent --show-error --max-time 5 http://127.0.0.1:3001/api/health
run_section "api diagnostics" curl --silent --show-error --max-time 5 http://127.0.0.1:3001/api/diagnostics
run_section "api alerts status" curl --silent --show-error --max-time 5 http://127.0.0.1:3001/api/alerts/status

echo "Wrote redacted status to ${OUT}"
echo "Review this file manually before copying any summary into reports."
