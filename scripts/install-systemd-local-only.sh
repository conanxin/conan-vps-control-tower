#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="conan-vps-control-tower"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SERVICE_SOURCE="${PROJECT_DIR}/scripts/${SERVICE_NAME}.service"
LOCAL_SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
CONFIG_PATH="${PROJECT_DIR}/config.yaml"

if [ ! -d "${PROJECT_DIR}/.venv" ]; then
  echo "Error: ${PROJECT_DIR}/.venv not found. Run scripts/deploy-local-only.sh first."
  exit 1
fi

if [ ! -f "${CONFIG_PATH}" ]; then
  echo "Error: config.yaml not found in project root."
  echo "Run scripts/deploy-local-only.sh to create one."
  exit 1
fi

if grep -Eq '^[[:space:]]*host:[[:space:]]*"0\.0\.0\.0"[[:space:]]*$' "${CONFIG_PATH}"; then
  echo "Error: config.yaml has server.host=0.0.0.0. Refuse to install local-only systemd service."
  exit 1
fi

if ! grep -Eq '^[[:space:]]*host:[[:space:]]*"127\.0\.0\.1"[[:space:]]*$' "${CONFIG_PATH}"; then
  echo "Error: config.yaml does not explicitly set host: \"127.0.0.1\"."
  echo "Current local-only safety requires host 127.0.0.1."
  exit 1
fi

if [ ! -f "${SERVICE_SOURCE}" ]; then
  echo "Error: service template not found: ${SERVICE_SOURCE}"
  exit 1
fi

cat > "${LOCAL_SERVICE_FILE}.tmp" <<EOF
[Unit]
Description=Conan VPS Control Tower
After=network.target

[Service]
Type=simple
WorkingDirectory=${PROJECT_DIR}
Environment=CONAN_CONFIG_PATH=${CONFIG_PATH}
ExecStart=${PROJECT_DIR}/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 3001
Restart=on-failure
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
EOF

sudo mv "${LOCAL_SERVICE_FILE}.tmp" "${LOCAL_SERVICE_FILE}"
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl start "${SERVICE_NAME}"

echo
echo "conan-vps-control-tower service installed and started."
echo "Installed unit: ${LOCAL_SERVICE_FILE}"
echo
echo "Next checks:"
echo "- systemctl status ${SERVICE_NAME} --no-pager"
echo "- bash scripts/check-systemd-local-only.sh"
echo "- ss -lntup | grep 3001"
