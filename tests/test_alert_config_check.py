from app.alerts.config_check import check_alert_config
from app.config import AlertsConfig, EmailAlertConfig, TelegramAlertConfig


def test_config_check_disabled_returns_ready_message():
    config = AlertsConfig(enabled=False)
    result = check_alert_config(config)

    assert result["status"] in {"healthy", "unknown"}
    assert result["enabled"] is False
    assert "关闭" in result["message"]
    assert result["safe_to_test"] is False
    assert result["channels"]["telegram"]["ready"] is False
    assert result["channels"]["email"]["ready"] is False


def test_telegram_enabled_but_token_placeholder_is_missing():
    config = AlertsConfig(
        enabled=True,
        telegram=TelegramAlertConfig(enabled=True, bot_token="${TELEGRAM_BOT_TOKEN}", chat_id="12345"),
    )

    result = check_alert_config(config)

    assert result["channels"]["telegram"]["enabled"] is True
    assert result["channels"]["telegram"]["ready"] is False
    assert "bot_token" in result["channels"]["telegram"]["missing_fields"]


def test_telegram_enabled_but_chat_id_placeholder_is_missing():
    config = AlertsConfig(
        enabled=True,
        telegram=TelegramAlertConfig(enabled=True, bot_token="real-token", chat_id="YOUR_TELEGRAM_CHAT_ID"),
    )

    result = check_alert_config(config)

    assert result["channels"]["telegram"]["enabled"] is True
    assert result["channels"]["telegram"]["ready"] is False
    assert "chat_id" in result["channels"]["telegram"]["missing_fields"]


def test_email_enabled_but_password_placeholder_is_missing():
    config = AlertsConfig(
        enabled=True,
        email=EmailAlertConfig(
            enabled=True,
            smtp_host="smtp.example.com",
            smtp_port=587,
            username="u",
            password="${SMTP_PASSWORD}",
            from_addr="alerts@example.com",
            to_addrs=["you@example.com"],
        ),
    )

    result = check_alert_config(config)

    assert result["channels"]["email"]["enabled"] is True
    assert result["channels"]["email"]["ready"] is False
    assert "password" in result["channels"]["email"]["missing_fields"]


def test_config_check_does_not_leak_sensitive_values():
    config = AlertsConfig(
        enabled=True,
        telegram=TelegramAlertConfig(
            enabled=True,
            bot_token="secret-bot-token",
            chat_id="secret-chat-id",
        ),
        email=EmailAlertConfig(
            enabled=True,
            username="alerts-user",
            password="secret-password",
            to_addrs=["you@example.com"],
            smtp_host="smtp.example.com",
            smtp_port=587,
            from_addr="alerts@example.com",
        ),
    )
    result = check_alert_config(config)

    payload = str(result)
    assert "secret-bot-token" not in payload
    assert "secret-chat-id" not in payload
    assert "secret-password" not in payload
    assert "missing_fields" in payload
