# Real VPS Validation Checklist

## Pre-deployment

- Confirm proxy is currently working.
- Confirm 3X-UI panel is accessible.
- Confirm proxy ports.
- Confirm panel port.
- Confirm server has Python 3.11+ or a compatible Python version.
- Confirm there is no plan to expose the dashboard publicly.

## Deploy

```bash
git clone https://github.com/conanxin/conan-vps-control-tower.git
cd conan-vps-control-tower
git checkout main
bash scripts/deploy-local-only.sh
```

Then edit `config.yaml`, run `bash scripts/preflight-local-only.sh`, run service manually, check APIs, and install systemd only if manual run is OK.

## Validate

- `/api/health` returns 200.
- `/api/domain` returns expected disabled/healthy/warning.
- `/api/tls` returns expected disabled/healthy/warning.
- `/api/traffic` returns estimate.
- `/api/alerts/status` does not leak secrets.
- `/api/diagnostics` returns suggestions.
- Dashboard opens through SSH tunnel.
- No `0.0.0.0:3001` listener.
- No 80/443 conflict caused by this dashboard.
- Proxy remains usable.

## Post-validation

- Stop manual process if systemd is used.
- Keep dashboard local-only.
- Copy only redacted results into reports.
- Do not commit `data/*.json` or live status files.
