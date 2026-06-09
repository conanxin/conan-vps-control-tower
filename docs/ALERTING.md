# Alerting

Phase 1C adds optional Telegram and Email / SMTP notifications. Alerting is a read-only notification layer. It does not automatically repair anything, modify proxy configuration, restart proxy services, change firewall rules, or expose the dashboard publicly.

## Supported Channels

- Telegram Bot API
- Email / SMTP

Both channels are disabled by default.

## Trigger Sources

Alerts can be generated from:

- `overall_status`
- module status, such as `proxy_core`, `domain_dns`, `tls_certificate`, or `traffic`

## Severity

Alerting can trigger for:

- `warning`
- `degraded`
- `critical`

`unknown` does not trigger alerts in Phase 1C.

## Strategy

- `min_severity`: minimum status needed to send an alert.
- `cooldown_seconds`: prevents repeated notifications for the same alert.
- alert fingerprint: deduplicates repeated alerts by module and status.
- recovery notification: sends a recovery message when a previously active alert returns to healthy.

## Default Behavior

```yaml
alerts:
  enabled: false
  min_severity: "warning"
  cooldown_seconds: 1800
  send_recovery: true
```

Telegram and Email are also disabled by default.

## Sensitive Information

Use environment variables for secrets:

```yaml
alerts:
  telegram:
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
  email:
    username: "${SMTP_USERNAME}"
    password: "${SMTP_PASSWORD}"
```

Do not commit real tokens, passwords, chat IDs, private domains, UUIDs, subscription links, or panel passwords.

## Example Config

```yaml
alerts:
  enabled: true
  min_severity: "warning"
  cooldown_seconds: 1800
  send_recovery: true
  state_file: "data/alert_state.json"
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
    timeout_seconds: 5
  email:
    enabled: true
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

Set environment variables before starting the app:

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
export TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"
export SMTP_USERNAME="alerts@example.com"
export SMTP_PASSWORD="YOUR_SMTP_PASSWORD"
```

## Test Notification

Use the Dashboard `Test Alert` button, or call:

```bash
curl -X POST http://127.0.0.1:3001/api/alerts/test
```

The test notification says it is not a failure.

## Diagnostics Context

Alerts include a concise `Suggested first check` line. They do not include long command lists, and Conan VPS Control Tower never executes diagnostic commands automatically.

## Manual Evaluation

```bash
curl -X POST http://127.0.0.1:3001/api/alerts/evaluate
```

Dashboard refreshes can also trigger evaluation through `/api/health` when `alerts.enabled=true`. `cooldown_seconds` prevents refreshes from creating alert spam.

## Cron Example

```text
*/5 * * * * curl -s -X POST http://127.0.0.1:3001/api/alerts/evaluate >/dev/null 2>&1
```

Only `alerts.enabled=true` with a fully configured channel sends notifications. No public port, firewall change, reverse proxy, or exposed Dashboard is required.

Alerting does not require the Dashboard to be publicly exposed.

## Current Limits

- Delivery is not guaranteed.
- Telegram and SMTP availability are external dependencies.
- This is not an enterprise alert platform.
- There is no Celery, Redis, RabbitMQ, or database service.
