# Dashboard Smoke Test

## Open SSH Tunnel

```bash
ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST
```

Open:

```text
http://127.0.0.1:3001
```

## Check Cards

- Overall Status
- VPS
- Proxy
- Domain / DNS
- TLS Certificate
- Traffic Risk
- Alerting
- Diagnostics

## Test Alert

Click `Test Alert`.

- If alerts are disabled, the UI should show skipped.
- If Telegram/Email is enabled and configured, a test notification should be sent.

## Diagnostics

- If no issue is active, it should show `No active diagnostic issues detected`.
- If an issue exists, it should show suggested first check.
- Commands are displayed only and are not executed automatically.

## Screenshots

Do not include real IPs, domains, tokens, chat IDs, UUIDs, passwords, or subscription links in screenshots.

Future redacted screenshots can be added to `docs/media`.
