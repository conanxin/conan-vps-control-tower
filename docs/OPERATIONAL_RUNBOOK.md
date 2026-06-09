# Conan VPS Control Tower Operational Runbook

This runbook summarizes stable local-only operation on a personal VPS.

## Common Operations Cheatsheet

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

Open locally:

```text
http://127.0.0.1:3001
```

## Start

```bash
cd ~/apps/conan-vps-control-tower
bash scripts/deploy-local-only.sh
bash scripts/install-systemd-local-only.sh
```

## Stop

```bash
bash scripts/uninstall-systemd-local-only.sh
```

To stop a temporary uvicorn process started by hand:

```bash
bash scripts/tower-stop-temporary-uvicorn.sh
```

## Status

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

## Access Dashboard by SSH Tunnel

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

Do not expose the dashboard publicly.

## Verify local-only behavior

```bash
ss -lntup | grep 3001
```

Expected result:

```text
127.0.0.1:3001
```

There should be no `0.0.0.0:3001` listener.

## Upgrade code

```bash
cd ~/apps/conan-vps-control-tower
git pull
bash scripts/deploy-local-only.sh
sudo systemctl restart conan-vps-control-tower
```

Keep existing `config.yaml` values aligned with your VPS (especially proxy ports and check targets).

## Roll back to temporary uvicorn

```bash
bash scripts/uninstall-systemd-local-only.sh
bash scripts/tower-stop-temporary-uvicorn.sh
cd ~/apps/conan-vps-control-tower
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 3001
```

## Uninstall service

```bash
bash scripts/uninstall-systemd-local-only.sh
```

This only touches `conan-vps-control-tower.service`.

## Common troubleshooting

### 1) Port 3001 already in use

```bash
ss -lntup | grep -E ':3001'
```

Stop the process using that port or choose another port in `config.yaml` for non-production tests.

### 2) .venv does not exist

Run:

```bash
bash scripts/deploy-local-only.sh
```

### 3) config.yaml host is not 127.0.0.1

Edit `config.yaml` and set:

```yaml
server:
  host: "127.0.0.1"
  port: 3001
```

Then reinstall service.

### 4) API is not accessible

```bash
bash scripts/check-systemd-local-only.sh
bash scripts/tower-status.sh
```

Check service status, listener binding, and logs.

### 5) Dashboard cannot open

Confirm SSH tunnel command and local-only port exposure:

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
ss -lntup | grep 3001
```

Confirm `http://127.0.0.1:3001` is opened from local machine.

Do not change firewall rules as part of troubleshooting.
