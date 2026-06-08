#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="conan-vps-control-tower"

if command -v systemctl >/dev/null 2>&1; then
  sudo systemctl stop "$SERVICE_NAME" 2>/dev/null || true
  sudo systemctl disable "$SERVICE_NAME" 2>/dev/null || true
  sudo rm -f "/etc/systemd/system/${SERVICE_NAME}.service"
  sudo systemctl daemon-reload
fi

echo "Uninstalled systemd unit if present."
echo "Project files, config.yaml, and proxy services were not modified."
