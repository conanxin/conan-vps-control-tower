#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="conan-vps-control-tower"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl stop "${SERVICE_NAME}" 2>/dev/null || true
  sudo systemctl disable "${SERVICE_NAME}" 2>/dev/null || true
fi

if [ -f "${SERVICE_FILE}" ]; then
  sudo rm -f "${SERVICE_FILE}"
  echo "Removed ${SERVICE_FILE}."
else
  echo "Service file not found; nothing to remove."
fi

if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl daemon-reload
fi

echo "Conan VPS Control Tower systemd unit removed."
