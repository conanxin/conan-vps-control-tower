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
