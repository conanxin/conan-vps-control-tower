# Alerting Environment Variables for systemd

Conan VPS Control Tower keeps all traffic local by default. When running as a
systemd service, environment variable placeholders in `config.yaml` are often
replaced at runtime.

## Why this is needed

`alerts.telegram.bot_token` and `alerts.email.password` should not be stored in
Git. In systemd, loading an environment file is a safe way to keep secrets out
of the repository.

## Recommended approach

Create a file such as:

`/etc/conan-vps-control-tower/alerts.env`

Only placeholders should be committed:

```text
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID
SMTP_USERNAME=YOUR_SMTP_USERNAME
SMTP_PASSWORD=YOUR_SMTP_PASSWORD
```

Then reference it in `config.yaml`:

```yaml
alerts:
  enabled: true
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
  email:
    enabled: true
    username: "${SMTP_USERNAME}"
    password: "${SMTP_PASSWORD}"
```

## Load env file in systemd

If your `conan-vps-control-tower.service` uses `EnvironmentFile`, it will load the
values at runtime:

```bash
sudo nano /etc/conan-vps-control-tower/alerts.env
sudo systemctl restart conan-vps-control-tower
```

## Check after change

```bash
bash scripts/tower-status.sh
bash scripts/check-alert-config.sh
```

## Important notes

- Do not expose the dashboard publicly.
- Do not change firewall settings for alerting.
- Do not restart proxy core services to make alerting work.
- Keep local-only binding (`127.0.0.1:3001`).

