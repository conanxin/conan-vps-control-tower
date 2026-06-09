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

- 总体状态
- VPS 状态
- 代理核心状态
- 3X-UI 面板状态
- 端口状态
- 域名 / DNS
- TLS 证书
- 流量风险
- 告警通知
- 诊断摘要 / 诊断建议

## Test Alert

Click `Test Alert`.

- If alerts are disabled, the UI should show skipped.
- If Telegram/Email is enabled and configured, a test notification should be sent.

## Diagnostics

- If no issue is active, it should show `未发现需要处理的诊断问题。`
- If an issue exists, it should show suggested first check.
- Commands are displayed only and are not executed automatically.

## Risk Summary Check

- Active risk section should show:
  - `当前没有活跃风险。` (when no warning/degraded/critical exists)
- Optional checks section should show:
  - `域名 / DNS：未配置`
  - `TLS 证书：未配置`

## Screenshots

Do not include real IPs, domains, tokens, chat IDs, UUIDs, passwords, or subscription links in screenshots.

Future redacted screenshots can be added to `docs/media`.
