# Conan VPS Control Tower v0.2.0-alpha

## Highlights

- Domain / DNS risk checks.
- TLS certificate expiry checks.
- Local traffic estimate with warning, degraded, and critical thresholds.
- Optional Telegram / Email alerting.
- Read-only diagnostics and suggested first checks.
- Local-only hardening scripts and validation docs.
- Real VPS validation passed.

## What Changed Since v0.1.0-alpha

- Added `/api/domain`, `/api/tls`, `/api/traffic`.
- Added `/api/alerts/status`, `/api/alerts/test`, `/api/alerts/evaluate`.
- Added `/api/diagnostics`.
- Added Dashboard cards for Domain / DNS, TLS Certificate, Traffic Risk, Alerting, and Diagnostics.
- Added local-only preflight and redacted VPS status collection scripts.
- Added documentation for real VPS validation and systemd local-only operation.

## Real VPS Validation Summary

Validation passed on a real VPS with:

- OS: Ubuntu 24.04 LTS
- Python: 3.12.3
- Project commit: `1ed4daf`
- Run mode: temporary uvicorn
- Bind: `127.0.0.1:3001`
- Public bind: no
- Health: healthy
- Diagnostics: all_healthy
- Alerts: disabled
- 3X-UI modified: no
- Proxy restarted: no
- Firewall changed: no
- Public port opened: no

No real IP, domain, token, UUID, subscription link, or panel password is included in this release.

## Local-Only Safety Model

- Default bind remains `127.0.0.1:3001`.
- No default public exposure.
- No automatic repairs.
- No proxy service restarts.
- No 3X-UI configuration changes.
- No firewall changes.
- Diagnostics display read-only commands only and never execute them.

## Known Limitations

- Traffic is a local estimate and may differ from VPS provider billing.
- Domain and TLS checks are disabled by default and need explicit configuration.
- Alerting is disabled by default and depends on third-party Telegram / SMTP delivery.
- systemd persistence still needs operator validation before a broader release.
- This is not an enterprise monitoring platform.

## Install / Upgrade Notes

```bash
git clone https://github.com/conanxin/conan-vps-control-tower.git
cd conan-vps-control-tower
git checkout v0.2.0-alpha
cp config.example.yaml config.yaml
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --host 127.0.0.1 --port 3001
```

For VPS use, prefer SSH tunnel access:

```bash
ssh -L 3001:127.0.0.1:3001 user@YOUR_VPS_HOST
```

## Next Steps

- Phase 1F: systemd persistence and operational polish.
- Optional Phase 2: Project Control Tower foundation.
