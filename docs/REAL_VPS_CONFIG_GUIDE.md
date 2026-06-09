# Real VPS Config Guide

This guide explains how to configure `config.yaml` on a real VPS.

Conan VPS Control Tower is a read-only health observation layer. It does not replace 3X-UI, modify proxy configuration, restart proxy services, change firewall rules, or open public ports.

## server

Keep the dashboard local-only:

```yaml
server:
  host: "127.0.0.1"
  port: 3001
```

Do not use `0.0.0.0`. Do not use `80` or `443` for this dashboard.

Run `bash scripts/preflight-local-only.sh` before starting on a VPS.

## checks

```yaml
checks:
  interval_seconds: 30
```

The UI refreshes every 30 seconds. Keep this lightweight for low-resource VPS instances.

## system

```yaml
system:
  disk_warning_percent: 80
  ram_warning_percent: 80
  load_warning_1m: 1.5
```

Tune these thresholds only if your VPS has a known resource profile.

## proxy.process_names

Set process names based on your real stack:

```yaml
proxy:
  process_names:
    - "x-ui"
    - "3x-ui"
    - "xray"
    - "sing-box"
    - "v2ray"
```

Use read-only commands to confirm process names:

```bash
ps -eo pid,comm,args,%cpu,%mem --sort=-%mem | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' | grep -v grep || true
```

## proxy.service_names

Set service names based on `systemctl` output:

```yaml
proxy:
  service_names:
    - "x-ui"
    - "3x-ui"
```

Read-only discovery:

```bash
systemctl list-units --type=service --state=running | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' || true
```

## proxy.ports

Set real inbound proxy ports:

```yaml
proxy:
  ports:
    - 443
```

If your proxy inbound is not `443`, replace it with the actual local listening port. Do not include sensitive credentials or URLs.

Read-only discovery:

```bash
ss -lntup | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray|:443|:8443|:2053' || true
```

## proxy.panel.url

Set the local 3X-UI panel URL:

```yaml
proxy:
  panel:
    url: "http://127.0.0.1:YOUR_3XUI_PANEL_PORT"
    timeout_seconds: 3
```

Do not include a username, password, token, subscription URL, or private path.

Read-only check:

```bash
curl -I --max-time 3 http://127.0.0.1:YOUR_3XUI_PANEL_PORT || true
```

## traffic

For Phase 1B, traffic configuration is still local and manual:

```yaml
traffic:
  monthly_limit_gb: 1000
  reset_day: 1
  warning_percent: 70
  degraded_percent: 85
  critical_percent: 95
  interfaces:
    - "auto"
  data_file: "data/traffic_state.json"
  note: "Local traffic is an estimate and may differ from provider billing."
```

`monthly_limit_gb` can be set to your VPS package limit. `reset_day` should match the package reset day. Traffic checking uses local Linux interface counters and is not exact provider billing data.

## domain

Domain checks are optional and disabled by default:

```yaml
domain:
  enabled: false
  names:
    - "example.com"
  expected_ips:
    - "203.0.113.10"
  timeout_seconds: 3
```

Use `YOUR_DOMAIN` in private notes and avoid committing real domains. If enabled, set `names` to the domain you want to resolve and `expected_ips` to expected public IPs only when you want mismatch detection.

## tls

TLS checks are optional and disabled by default:

```yaml
tls:
  enabled: false
  targets:
    - host: "example.com"
      port: 443
      server_name: "example.com"
      warning_days: 21
      critical_days: 7
      timeout_seconds: 5
```

If enabled, set `host` and `server_name` to the certificate target. Do not include tokens, credentials, subscription links, or private paths.

## Sensitive Data Rule

Do not store or commit:

- Real private IPs or private domains
- Tokens
- Proxy UUIDs
- Subscription links
- 3X-UI panel passwords
- Proxy node plaintext configuration

## alerts

Alerting is optional and disabled by default:

```yaml
alerts:
  enabled: false
  min_severity: "warning"
  cooldown_seconds: 1800
  send_recovery: true
  state_file: "data/alert_state.json"
  telegram:
    enabled: false
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
    timeout_seconds: 5
  email:
    enabled: false
    smtp_host: "smtp.example.com"
    smtp_port: 587
    username: "${SMTP_USERNAME}"
    password: "${SMTP_PASSWORD}"
    from_addr: "alerts@example.com"
    to_addrs:
      - "you@example.com"
    use_tls: true
    timeout_seconds: 10
```

Use environment variables for secrets. Do not commit real Telegram tokens, chat IDs, SMTP passwords, private domains, or proxy credentials.

## diagnostics command placeholders

Diagnostics displays read-only command templates. Replace placeholders locally before running them:

- `SERVICE_NAME`: your local service name, such as a 3X-UI or proxy service.
- `YOUR_PROXY_PORT`: your proxy inbound port.
- `YOUR_PANEL_PORT`: your local 3X-UI panel port.
- `YOUR_DOMAIN`: the domain you want to check.

Do not paste real domains, IPs, tokens, UUIDs, passwords, or subscription links into public reports.
