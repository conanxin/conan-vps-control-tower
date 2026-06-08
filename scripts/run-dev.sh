#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f config.yaml ]; then
  cp config.example.yaml config.yaml
fi

if [ -d .venv ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

exec uvicorn app.main:app --host 127.0.0.1 --port 3001 --reload
