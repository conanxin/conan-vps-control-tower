# Deployment

## Default Runtime

Conan VPS Control Tower defaults to:

```text
127.0.0.1:3001
```

It should not bind to `0.0.0.0` unless the operator intentionally changes the configuration and understands the risk.

## Local Development

```bash
./scripts/run-dev.sh
```

## Install

```bash
./scripts/install.sh
```

The install script creates a Python virtual environment, installs dependencies, and copies `config.example.yaml` to `config.yaml` if needed.

## systemd

Copy the service file:

```bash
sudo cp scripts/conan-vps-control-tower.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start conan-vps-control-tower
```

Enable only after confirming the local dashboard works:

```bash
sudo systemctl enable conan-vps-control-tower
```

## Uninstall

```bash
./scripts/uninstall.sh
```

This script stops and disables the service if systemd is available. It does not remove proxy services, proxy configuration, firewall rules, or 3X-UI data.

## Optional Alert Evaluation Cron

If alerting is enabled, you can trigger evaluation through the local API:

```bash
curl -X POST http://127.0.0.1:3001/api/alerts/evaluate
```

Example crontab:

```text
*/5 * * * * curl -s -X POST http://127.0.0.1:3001/api/alerts/evaluate >/dev/null 2>&1
```

This does not require opening a public port, changing firewall rules, or exposing the Dashboard.
