# Dashboard Smoke Test

Use this quick checklist after install or upgrade.

## Open Dashboard

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

## Check Visibility

- 总体状态（Overall Status）
- 代理链路（Proxy Path）
- 诊断摘要（Diagnostics Summary）
- VPS 状态（VPS Status）
- 代理核心状态（Proxy Core Status）
- 3X-UI 面板状态（3X-UI Panel Status）
- 端口状态（Port Status）
- 流量风险（Traffic Risk）
- 域名 / DNS
- TLS 证书
- 告警通知（Alerting）
- 诊断建议（Diagnostics）

## Status Interpretation

- 健康时：看得到“当前没有活跃风险”。
- 有异常时：在卡片中看到对应标题和风险提示，随后阅读诊断摘要。
- 未配置项：显示在“未配置的可选检查”，不应视作故障。

## API Smoke Check

Run：

```bash
curl -s http://127.0.0.1:3001/api/health | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/diagnostics | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/alerts/status | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/meta | python3 -m json.tool
```

Expected:

- `/api/health` returns JSON.
- `/api/diagnostics` returns list (empty or non-critical healthy summary).
- `/api/alerts/status` returns `enabled: false` unless configured.
- `/api/meta` returns local-only metadata.

## Alert Test

Click `测试告警`:

- If alerts are disabled, show skipped.
- If channels are enabled and configured, a test message may be sent.

## Screenshot Check

If screenshot is added:

- Do not include real IPs, real domains, tokens, UUIDs, subscription links, or panel passwords.
- Crop browser chrome, keep only dashboard content area.
