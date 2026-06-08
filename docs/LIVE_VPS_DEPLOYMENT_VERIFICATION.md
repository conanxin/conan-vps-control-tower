# Live VPS Deployment Verification

This guide verifies Conan VPS Control Tower on a real VPS while keeping the dashboard local-only.

The project is a read-only health observation layer. It does not replace 3X-UI, modify proxy configuration, restart proxy services, change firewall rules, or open public ports.

## Safety Rules

- Keep `server.host` as `127.0.0.1`.
- Keep the default port as `3001` unless you have a local-only reason to change it.
- Do not bind to `0.0.0.0`.
- Do not use port `80` or `443` for this dashboard.
- Do not submit real IPs, domains, tokens, UUIDs, passwords, subscription links, or proxy plaintext in reports.
- Access the dashboard through SSH tunnel instead of public exposure.

## 1. Clone the Repository

```bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/conanxin/conan-vps-control-tower.git
cd conan-vps-control-tower
```

For the alpha release:

```bash
git checkout v0.1.0-alpha
```

For latest `main`:

```bash
git checkout main
git pull
```

## 2. Install Dependencies

```bash
bash scripts/deploy-local-only.sh
```

This creates `.venv`, installs dependencies, and copies `config.example.yaml` to `config.yaml` if needed. It does not start the dashboard, change 3X-UI, inspect secret config, or enable systemd.

## 3. Edit config.yaml

```bash
nano config.yaml
```

Confirm:

```yaml
server:
  host: "127.0.0.1"
  port: 3001
```

Then adjust the read-only checker targets:

- `proxy.process_names`: expected process names such as `x-ui`, `3x-ui`, `xray`, `sing-box`, or `v2ray`.
- `proxy.service_names`: service names from `systemctl`.
- `proxy.ports`: real inbound proxy ports.
- `proxy.panel.url`: local 3X-UI panel URL, for example `http://127.0.0.1:YOUR_3XUI_PANEL_PORT`.
- `traffic.monthly_limit_gb`: temporary manual monthly limit, for example `1000`.
- `traffic.reset_day`: package reset day.

Do not add credentials, UUIDs, subscription links, panel passwords, or node plaintext to this file.

## 4. Read-Only Probe Commands

These commands help identify process names, service names, local listening ports, and panel reachability. They are read-only.

Sanitize output before adding it to reports. Do not commit real IPs, domains, tokens, UUIDs, passwords, subscription links, or proxy plaintext.

```bash
systemctl list-units --type=service --state=running | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' || true
```

```bash
ps -eo pid,comm,args,%cpu,%mem --sort=-%mem | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' | grep -v grep || true
```

```bash
ss -lntup | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray|:443|:8443|:2053' || true
```

```bash
curl -I --max-time 3 http://127.0.0.1:YOUR_3XUI_PANEL_PORT || true
```

## 5. Run Dev Mode

```bash
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 3001
```

Or:

```bash
bash scripts/run-dev.sh
```

The dashboard must remain local-only at `127.0.0.1:3001`.

## 6. Smoke Check APIs

Open another VPS shell:

```bash
bash scripts/check-local-only-status.sh
```

Or run manually:

```bash
curl http://127.0.0.1:3001/api/health
curl http://127.0.0.1:3001/api/system
curl http://127.0.0.1:3001/api/proxy
```

## 7. Verify Dashboard Through SSH Tunnel

From local Windows:

```bash
ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST
```

Then open:

```text
http://127.0.0.1:3001
```

Confirm the dashboard shows:

- Overall Status
- VPS status
- Proxy Core status
- 3X-UI Panel status
- Port status
- Traffic status
- Risk Summary
- Last Checked

## 8. Optional systemd Local-Only Verification

Only do this after dev mode works.

The bundled service file assumes the project lives at `/opt/conan-vps-control-tower`. If your project is under `~/apps`, either copy it to `/opt/conan-vps-control-tower` or adjust the service file before installing it.

Do not overwrite unrelated services.

```bash
sudo cp scripts/conan-vps-control-tower.service /etc/systemd/system/conan-vps-control-tower.service
sudo systemctl daemon-reload
sudo systemctl enable conan-vps-control-tower
sudo systemctl start conan-vps-control-tower
sudo systemctl status conan-vps-control-tower --no-pager
```

Then check:

```bash
curl http://127.0.0.1:3001/api/health
bash scripts/check-local-only-status.sh
```

Confirm:

- Service listens on `127.0.0.1:3001`.
- Service does not listen on `0.0.0.0:3001`.
- Service does not occupy `80` or `443`.
- Existing proxy services are still running.
- 3X-UI panel is still reachable.
- Proxy ports are still listening.
