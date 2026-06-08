#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"

if [ ! -f config.yaml ]; then
  cp config.example.yaml config.yaml
fi

echo "Installed Conan VPS Control Tower."
echo "Run: ./scripts/run-dev.sh"
