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
- 管理入口
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

Management entry:

```bash
curl -s http://127.0.0.1:3001/api/management | python3 -m json.tool
```

Expected:

- `panel_public_url` points to the configured panel domain.
- `detected_scheme` and `recommended_local_url` are present.
- If `protocol_warning=true`, the Dashboard shows the yellow protocol warning.
- No `password`, `token`, or `cookie` appears.
- Dashboard contains no iframe for 3X-UI.
- Button opens the configured `panel_public_url`.
- If `panel_public_url` contains a hidden path, Dashboard displays `panel_public_display_url` such as `https://panel.conanxin.com/隐藏路径`.
- The visible Dashboard text should not reveal the real hidden path.

If HTTPS returns `404`, treat it as protocol reachable. It may mean the root path is not the 3X-UI login path. Do not commit hidden paths.

Panel health repair check:

- If `xui_panel` is abnormal after a 3X-UI upgrade but proxy core and proxy ports are healthy, do not restart the proxy first.
- Confirm the current panel port and hidden path with read-only checks.
- The Dashboard diagnostics should not show `YOUR_PANEL_PORT`; it should either show the confirmed port or ask the user to confirm the 3X-UI panel port.
- Health check details should show masked URLs such as `https://127.0.0.1:YOUR_PANEL_PORT/<hidden>/`, not the real hidden path.

Also run:

```bash
curl -s http://127.0.0.1:3001/api/alerts/config-check | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/alerts/status | python3 -m json.tool | head -120
```

## Alert Test

Click `测试告警`:

- If alerts are disabled, it should show skipped.
- If channels are enabled and configured, a test message may be sent.
- If Telegram/Email is enabled but incomplete, skipped reason should explain missing fields.

## Screenshot Check

- Do not include real IPs, real domains, tokens, UUIDs, subscription links, or panel passwords.
- Crop browser chrome; keep only dashboard content.
