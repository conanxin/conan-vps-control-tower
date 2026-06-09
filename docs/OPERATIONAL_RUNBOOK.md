# Conan VPS Control Tower Operational Runbook

This runbook summarizes stable local-only operation on a personal VPS.

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
pkill -f 'uvicorn app.main:app --host 127.0.0.1 --port 3001' || true
```

## Status

```bash
systemctl status conan-vps-control-tower --no-pager
bash scripts/check-systemd-local-only.sh
```

## Logs

```bash
journalctl -u conan-vps-control-tower --no-pager -n 80
```

## Access Dashboard by SSH Tunnel

From local machine:

```bash
ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST
```

Then open `http://127.0.0.1:3001` locally.

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
pkill -f 'uvicorn app.main:app --host 127.0.0.1 --port 3001' || true
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
```

Check service status, listener binding, and logs.

### 5) Dashboard cannot open

Confirm SSH tunnel command and local-only port exposure:

```bash
ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST
ss -lntup | grep 3001
```

Confirm `http://127.0.0.1:3001` is opened from local machine.

Do not change firewall rules as part of troubleshooting.
