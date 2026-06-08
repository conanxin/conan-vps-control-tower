# Conan VPS Control Tower v0.1.0-alpha

## Highlights

- First alpha release of a lightweight, read-only health dashboard for personal VPS proxy nodes.
- Local-only FastAPI service by default: `127.0.0.1:3001`.
- Native HTML/CSS/JS dashboard without CDN or frontend framework dependencies.
- Clear health model with human-readable summaries and risk hints.

## What Works

- `/api/health` returns aggregated health status.
- `/api/system` returns VPS resource health.
- `/api/proxy` returns proxy-related health checks.
- Dashboard refreshes every 30 seconds.
- Checkers handle failures without crashing the service.
- pytest covers evaluator logic, port checking, and config defaults.

## What Is Intentionally Not Included

- No automatic repair.
- No 3X-UI configuration changes.
- No proxy service restarts.
- No firewall changes.
- No public exposure by default.
- No collection of proxy credentials, UUIDs, passwords, or subscription links.

## Known Limitations

- Traffic is estimated from system network counters since boot.
- systemd service visibility depends on `systemctl`.
- The 3X-UI panel checker only tests reachability.
- Real VPS verification is planned for the next phase.

## Upgrade / Install Notes

For a fresh local install:

```bash
cp config.example.yaml config.yaml
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --host 127.0.0.1 --port 3001
```

For VPS usage, prefer SSH tunnel access:

```bash
ssh -L 3001:127.0.0.1:3001 user@your-vps
```

## Next Steps

Phase 1A.2 will verify the dashboard on a real VPS using local binding and SSH tunnel access.
