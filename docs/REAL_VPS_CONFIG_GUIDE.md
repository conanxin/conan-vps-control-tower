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

Do not use `0.0.0.0` in Phase 1A.2. Do not use `80` or `443` for this dashboard.

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

For Phase 1A.2, keep traffic configuration manual:

```yaml
traffic:
  monthly_limit_gb: 1000
  reset_day: 1
```

`monthly_limit_gb` can be set to your VPS package limit. `reset_day` should match the package reset day. Traffic checking currently uses system network counters since boot and is not exact billing data.

## Sensitive Data Rule

Do not store or commit:

- Real private IPs or private domains
- Tokens
- Proxy UUIDs
- Subscription links
- 3X-UI panel passwords
- Proxy node plaintext configuration
