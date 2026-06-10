# Conan VPS Control Tower Operational Runbook

This runbook focuses on local-only operation and safe daily checks.

## Common commands

```bash
bash scripts/tower-status.sh
bash scripts/tower-logs.sh
bash scripts/tower-logs.sh follow
bash scripts/tower-stop-temporary-uvicorn.sh
sudo systemctl start conan-vps-control-tower
sudo systemctl stop conan-vps-control-tower
sudo systemctl disable conan-vps-control-tower
bash scripts/uninstall-systemd-local-only.sh
bash scripts/check-alert-config.sh
bash scripts/discover-panel-and-tower-local.sh
bash scripts/check-domain-access-readiness.sh
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

## Open dashboard

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

If Cloudflare domain access is configured, also open:

```text
https://tower.conanxin.com
```

Dashboard is Simplified Chinese by default; API fields stay English for compatibility.

## Start / Stop service

### Start as service

```bash
cd ~/apps/conan-vps-control-tower
bash scripts/deploy-local-only.sh
bash scripts/install-systemd-local-only.sh
```

### Stop service

```bash
sudo systemctl stop conan-vps-control-tower
```

To stop temporary uvicorn only:

```bash
bash scripts/tower-stop-temporary-uvicorn.sh
```

## Status and health checks

```bash
systemctl status conan-vps-control-tower --no-pager
bash scripts/check-systemd-local-only.sh
bash scripts/tower-status.sh
```

### History and event APIs

```bash
curl -s http://127.0.0.1:3001/api/history/summary
curl -s http://127.0.0.1:3001/api/history/recent
curl -s http://127.0.0.1:3001/api/events
```

### Management entry API

```bash
curl -s http://127.0.0.1:3001/api/management
```

Confirm:

- `panel_public_url`: private panel entry, e.g. `https://panel.conanxin.com` or with hidden path
- `panel_public_display_url`: masked display value, e.g. `panel.conanxin.com / 已配置隐藏路径`
- `panel_public_url` is used for button jump only
- no password / token / cookie / UUID in response

### Alert readiness and test

```bash
curl -s http://127.0.0.1:3001/api/alerts/status
curl -s http://127.0.0.1:3001/api/alerts/config-check
```

### Panel health repair after 3X-UI upgrade

If proxy still works but `xui_panel` reports abnormal, do not restart proxy services first. Run read-only checks:

```bash
ps -eo pid,comm,args,%cpu,%mem --sort=-%mem | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' | grep -v grep || true
systemctl list-units --type=service --state=running | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' || true
ss -lntup | grep -Ei ':3001|:YOUR_3XUI_PANEL_PORT|:80|:443' || true
```

Do not print or commit the real 3X-UI hidden path. Use masked placeholders in docs and reports, e.g. `/p-2...3f2/ len=52`.

## Logs

```bash
journalctl -u conan-vps-control-tower --no-pager -n 80
bash scripts/tower-logs.sh
bash scripts/tower-logs.sh follow
```

## Verify local-only

```bash
ss -lntup | grep 3001
```

Expected:

```text
127.0.0.1:3001
```

Forbidden:

```text
0.0.0.0:3001
```

Do not expose the dashboard to public internet.

## Domain access readiness

If using Cloudflare Tunnel + Access:

```bash
bash scripts/discover-panel-and-tower-local.sh
bash scripts/check-domain-access-readiness.sh
```

Expected targets:

```text
tower target: http://127.0.0.1:3001
panel target: https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

`80/443` output is informational only and should not be changed by this process.

## Upgrade

```bash
cd ~/apps/conan-vps-control-tower
git pull
bash scripts/deploy-local-only.sh
sudo systemctl restart conan-vps-control-tower
```

## Showcasing / screenshot

- Screenshot guide: `docs/media/DASHBOARD_SCREENSHOT_GUIDE.md`
- Demo walk-through: `docs/DEMO_WALKTHROUGH.md`

## Uninstall

```bash
bash scripts/uninstall-systemd-local-only.sh
```

This only removes `conan-vps-control-tower.service` and does not touch 3X-UI.

## Troubleshooting

### 1) 3001 is occupied

```bash
ss -lntup | grep -E ':3001'
```

### 2) .venv missing

```bash
bash scripts/deploy-local-only.sh
```

### 3) server host not local

```yaml
server:
  host: "127.0.0.1"
  port: 3001
```

### 4) API not reachable

```bash
bash scripts/check-systemd-local-only.sh
bash scripts/tower-status.sh
```

### 5) Dashboard not open

Confirm SSH and local bind:

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
ss -lntup | grep 3001
```
