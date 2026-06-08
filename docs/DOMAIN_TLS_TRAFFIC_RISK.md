# Domain / TLS / Traffic Risk

Phase 1B adds optional checks for common proxy-node external dependency risks while keeping the project read-only and local-only.

Conan VPS Control Tower does not replace 3X-UI, modify proxy configuration, restart proxy services, change firewall rules, or open public ports.

## Domain Check

The Domain / DNS checker resolves configured domain names with Python's standard library. It can verify that a domain resolves at all, and optionally compare resolved IPs with expected example values.

If `domain.enabled` is `false`, the checker returns `Not configured` and does not affect overall health.

Example:

```yaml
domain:
  enabled: true
  names:
    - "example.com"
  expected_ips:
    - "203.0.113.10"
  timeout_seconds: 3
```

How to read status:

- `healthy`: domain resolves, and expected IPs match if configured.
- `warning`: domain resolves but does not match expected IPs.
- `critical`: DNS resolution failed.
- `unknown`: checker is disabled or cannot determine status.

## TLS Check

The TLS checker connects to configured TLS targets using Python's `ssl` and `socket` modules. It reads certificate expiry metadata and calculates days remaining.

If `tls.enabled` is `false`, the checker returns `Not configured` and does not affect overall health.

Example:

```yaml
tls:
  enabled: true
  targets:
    - host: "example.com"
      port: 443
      server_name: "example.com"
      warning_days: 21
      critical_days: 7
      timeout_seconds: 5
```

How to read status:

- `healthy`: certificate was retrieved and is not near expiry.
- `warning`: days remaining is at or below `warning_days`.
- `critical`: TLS handshake failed, certificate metadata could not be read, or days remaining is at or below `critical_days`.
- `unknown`: checker is disabled.

The checker does not store the full certificate.

## Traffic Local Estimate

The traffic checker reads local Linux interface counters from:

```text
/sys/class/net/<interface>/statistics/rx_bytes
/sys/class/net/<interface>/statistics/tx_bytes
```

It creates a local baseline in `data/traffic_state.json` and estimates current cycle usage from that baseline.

This is a local estimate and may differ from provider billing. It is not authoritative VPS provider billing data.

Example:

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

How to read status:

- `healthy`: usage is below `warning_percent`.
- `warning`: usage is at or above `warning_percent`.
- `degraded`: usage is at or above `degraded_percent`.
- `critical`: usage is at or above `critical_percent`.
- `unknown`: local interface counters are unavailable or unreadable.

## Why These Checks Are Still Read-Only

These checks only read DNS answers, TLS certificate metadata, local interface counters, and local config values. They do not write proxy configuration, restart services, change firewall rules, or modify 3X-UI.

## Why Provider Billing API Is Not Included

Phase 1B intentionally avoids provider APIs because they add credentials, provider-specific behavior, account permissions, and security risk. Local traffic estimates are less authoritative, but they preserve the lightweight and private design.
