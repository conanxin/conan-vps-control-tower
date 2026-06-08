#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "pyproject.toml" ] || [ ! -f "config.example.yaml" ] || [ ! -d "app" ]; then
  echo "Error: run this script from the conan-vps-control-tower project root."
  exit 1
fi

echo "Preparing Conan VPS Control Tower for local-only usage..."

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

if [ ! -f "config.yaml" ]; then
  cp config.example.yaml config.yaml
  echo "Created config.yaml from config.example.yaml."
else
  echo "config.yaml already exists; leaving it unchanged."
fi

if grep -Eq '^[[:space:]]*host:[[:space:]]*"127\.0\.0\.1"[[:space:]]*$' config.yaml; then
  echo "Verified config.yaml keeps host at 127.0.0.1."
else
  echo "Warning: config.yaml does not clearly contain host: \"127.0.0.1\"."
  echo "Edit config.yaml before starting the service. Do not bind to 0.0.0.0."
fi

echo
echo "Next steps:"
echo "1. Edit config.yaml with local, non-sensitive checker targets."
echo "2. Start local-only dev mode:"
echo "   source .venv/bin/activate"
echo "   uvicorn app.main:app --host 127.0.0.1 --port 3001"
echo "3. In another shell, run:"
echo "   bash scripts/check-local-only-status.sh"
echo
echo "This script does not modify 3X-UI, restart proxy services, change firewall rules, or enable systemd."
