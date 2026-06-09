# Dashboard Smoke Test

After install or upgrade, run this checklist in the local 127.0.0.1 tunnel view.

## Open Dashboard

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

## Check Visibility

- Overall Status
- Proxy Path
- Diagnostics Summary
- VPS Status
- Proxy Core Status
- 3X-UI Panel Status
- Port Status
- Traffic Risk
- Domain / DNS
- TLS Certificate
- Alerting
- Diagnostics
- 健康历史

## Status Interpretation

- Healthy: no visible blocker.
- Warning/Degraded/Critical: follow diagnostics + affected card and suggested first check.
- If `未配置` appears, it should only be a note, not a failure card.

## API Smoke Check

```bash
curl -s http://127.0.0.1:3001/api/health | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/diagnostics | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/alerts/status | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/meta | python3 -m json.tool
curl -s http://127.0.0.1:3001/api/history/summary | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/history/recent | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/events | python3 -m json.tool | head -120
```

Expected:

- `/api/health` returns JSON.
- `/api/diagnostics` returns summary + items.
- `/api/alerts/status` returns `enabled: false` unless configured.
- `/api/meta` returns local-only runtime info and history flags.
- `/api/history/*` returns JSON payload (or disabled/empty states when configured off).

## Alert Test

Click `测试告警`:

- If alerts are disabled, it should show skipped.
- If channels are enabled and configured, a test message may be sent.

## Screenshot Check

- Do not include real IPs, real domains, tokens, UUIDs, subscription links, or panel passwords.
- Crop browser chrome; keep only dashboard content.
