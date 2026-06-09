# systemd Local-Only Runtime

Conan VPS Control Tower should run as a local-only service on `127.0.0.1:3001`.

It does not need public ports, Nginx, Caddy, Cloudflare Tunnel, Docker, or firewall changes.

## Install Service

The bundled service assumes the project lives at `/opt/conan-vps-control-tower`.

```bash
sudo cp scripts/conan-vps-control-tower.service /etc/systemd/system/conan-vps-control-tower.service
sudo systemctl daemon-reload
sudo systemctl enable conan-vps-control-tower
sudo systemctl start conan-vps-control-tower
```

## Confirm Local-Only Listening

```bash
ss -lntup | grep 3001
```

Correct result should show:

```text
127.0.0.1:3001
```

If you see `0.0.0.0:3001` or `[::]:3001`, stop using that configuration and check `config.yaml` and the systemd service command.

## View Logs

```bash
journalctl -u conan-vps-control-tower --no-pager -n 80
```

## SSH Tunnel Access

```bash
ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST
```

Then open:

```text
http://127.0.0.1:3001
```

Do not open public ports for the dashboard.
