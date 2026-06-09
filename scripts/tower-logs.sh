#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="conan-vps-control-tower"

if [ "${1:-}" = "follow" ]; then
  journalctl -u "${SERVICE_NAME}" --no-pager -f
  exit 0
fi

journalctl -u "${SERVICE_NAME}" --no-pager -n 120
