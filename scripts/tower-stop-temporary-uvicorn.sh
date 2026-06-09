#!/usr/bin/env bash
set -euo pipefail

echo "Stopping temporary local uvicorn instance (exact match)."

pkill -f 'uvicorn app.main:app --host 127.0.0.1 --port 3001' || true

echo "Temporary uvicorn stop attempt finished."
