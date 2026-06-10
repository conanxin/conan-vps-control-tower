# Conan VPS Control Tower Operational Runbook

This runbook focuses on local-only operation for personal VPS usage.

## Common Commands

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

## Open Dashboard

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

Dashboard is simplified Chinese by default; API fields remain English for compatibility.

## Start / Stop

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

## Status and Health Checks

```bash
systemctl status conan-vps-control-tower --no-pager
bash scripts/check-systemd-local-only.sh
bash scripts/tower-status.sh
```

### History / Event APIs

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

- `panel_local_url` is the local 3X-UI target, for example `https://127.0.0.1:2096`.
- `panel_public_url` is the protected public entry, for example `https://panel.conanxin.com`.
- The response does not contain password, token, cookie, UUID, or subscription links.
- `detected_scheme` can show `https` when the local panel port is HTTPS.
- `recommended_local_url` may be `https://127.0.0.1:2096`.
- HTTP failure does not always mean the panel is unavailable; HTTPS `404` can still indicate protocol reachability.
- If 3X-UI uses a hidden path, do not commit that path to the repository.
- `panel_public_url` may include the hidden path in private VPS config, but the Dashboard should display `panel_public_display_url`.
- The button uses the full `panel_public_url`; visible text uses the masked display URL.

### Repair panel health after a 3X-UI upgrade

If proxy traffic still works but `xui_panel` becomes critical after a 3X-UI upgrade, do not restart proxy services first. Read the current panel settings and update only Control Tower's private `config.yaml`.

Read-only checks:

```bash
ps -eo pid,comm,args,%cpu,%mem --sort=-%mem | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' | grep -v grep || true
systemctl list-units --type=service --state=running | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' || true
ss -lntup | grep -Ei ':3001|:YOUR_PANEL_PORT|:80|:443' || true
```

The 3X-UI `webBasePath` can be read from `/etc/x-ui/x-ui.db`, but the full hidden path must not be printed in reports or committed to GitHub. Use a masked value such as `/p-2...3f2/ len=52`.

For Control Tower health checks, prefer the confirmed local HTTPS target:

```text
https://127.0.0.1:YOUR_PANEL_PORT/<hidden>/
```

`curl -k` is appropriate for local self-signed HTTPS panel checks. `404` means the configured path is probably wrong; it is not the same as a proxy outage.

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

Do not expose dashboard publicly. Keep local-only.

## Domain access readiness

Domain access is optional. The safer default remains SSH Tunnel. If you want mobile browser access, use Cloudflare Tunnel + Cloudflare Access.

Run read-only discovery:

```bash
bash scripts/discover-panel-and-tower-local.sh
```

Confirm targets:

```text
tower target: http://127.0.0.1:3001
panel target: https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

Check readiness:

```bash
bash scripts/check-domain-access-readiness.sh
```

Confirm `80/443` are only shown for awareness and are not modified by these scripts. Do not expose `3001` directly, and do not mix `tower.example.com` / `panel.example.com` with the proxy main domain.

## Domain access operating state

When Cloudflare Access + Tunnel is configured, the normal browser entry is:

```text
https://tower.conanxin.com
```

The service itself must still listen only on:

```text
127.0.0.1:3001
```

The Dashboard may show `panel.conanxin.com / 已配置隐藏路径` for the management panel. This is intentionally masked. The full hidden path should remain only in the private VPS `config.yaml` and should not appear in screenshots, reports, or GitHub commits.

## Upgrade

```bash
cd ~/apps/conan-vps-control-tower
git pull
bash scripts/deploy-local-only.sh
sudo systemctl restart conan-vps-control-tower
```

## Showcasing / Screenshot

- Screenshot guidance: `docs/media/DASHBOARD_SCREENSHOT_GUIDE.md`
- Demo walk-through: `docs/DEMO_WALKTHROUGH.md`

## Uninstall

```bash
bash scripts/uninstall-systemd-local-only.sh
```

This only touches `conan-vps-control-tower.service`.

## Troubleshooting

### 1) 3001 is occupied

```bash
ss -lntup | grep -E ':3001'
```

### 2) .venv missing

```bash
bash scripts/deploy-local-only.sh
```

### 3) config host not local

Edit `config.yaml`:

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

Confirm SSH tunnel + local-only bind:

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
ss -lntup | grep 3001
```

## 健康历史与事件

- 历史写入开启时，建议定期查看：
  - `api/history/summary`
  - `api/events`
- 历史文件位于 `data/health_history.json` / `data/event_log.json`。
- 文件异常时 Dashboard 会提示“历史数据暂不可用”，服务不受影响。
