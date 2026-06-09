# Telegram Alert Setup

Conan VPS Control Tower's alerting is read-only. Telegram setup is only for
notification, not for remote execution or auto-fix.

## What Telegram alerts are for

- Get a quick heads-up for `warning`, `degraded`, and `critical` health states.
- Know which module changed first (`proxy_core`, `domain_dns`, `tls_certificate`,
  `traffic`, etc.).
- Keep local-only operations safe without polling dashboards.

## Prepare Telegram credentials

1. Create a Telegram bot and get the bot token.
2. Get your chat ID where alerts should be sent.
3. Put values in environment file and enable in config:

```yaml
alerts:
  enabled: true
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
    timeout_seconds: 5
```

## Verify setup before opening alerts

Use:

```bash
curl -s http://127.0.0.1:3001/api/alerts/config-check | python3 -m json.tool | head -120
```

Expected:

- `status` is `warning` if configuration is incomplete.
- `channels.telegram.ready` becomes `true` when required values are valid.
- `channels.telegram.missing_fields` lists only field names.

## Test alert

Test alert is for connectivity verification only. It does not represent a real failure.

```bash
curl -X POST http://127.0.0.1:3001/api/alerts/test
```

or click `测试告警` in Dashboard.

## Cooldown and severity

- `cooldown_seconds`: prevents repeated notifications for the same risk.
- `min_severity`: smallest level that can trigger alerts.

Recommended:

- keep `min_severity: "warning"` unless you want fewer alerts.

## Recovery notification

If `send_recovery: true`, when a previously active risk resolves, a recovery
notification can be sent depending on channel readiness.

## Do not

- Do not expose secrets in logs, docs, or commits.
- Do not send Telegram test alerts in public or shared logs.
- Do not use real token/chat ID in documentation examples.

