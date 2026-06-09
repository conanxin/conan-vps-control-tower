from __future__ import annotations

from typing import Any

from app.config import AlertsConfig


def _is_empty(value: str | None) -> bool:
    if not value:
        return True
    return not value.strip()


def _is_placeholder(value: str | None) -> bool:
    if _is_empty(value):
        return True
    value = value.strip()
    if value.startswith("${") and value.endswith("}"):
        return True
    if value.startswith("YOUR_"):
        return True
    return False


def _normalize_port(value: int | None) -> bool:
    return isinstance(value, int) and value > 0


def _is_valid_min_severity(value: str | None) -> bool:
    return value in {"warning", "degraded", "critical"}


def _channel_missing_telegram(config) -> list[str]:
    missing: list[str] = []
    if _is_placeholder(config.bot_token):
        missing.append("bot_token")
    if _is_placeholder(config.chat_id):
        missing.append("chat_id")
    return missing


def _channel_missing_email(config) -> list[str]:
    missing: list[str] = []
    if _is_placeholder(config.smtp_host):
        missing.append("smtp_host")
    if not _normalize_port(config.smtp_port):
        missing.append("smtp_port")
    if _is_placeholder(config.username):
        missing.append("username")
    if _is_placeholder(config.password):
        missing.append("password")
    if _is_placeholder(config.from_addr):
        missing.append("from_addr")
    if not config.to_addrs or any(_is_placeholder(item) for item in config.to_addrs):
        missing.append("to_addrs")
    return missing


def check_alert_config(config: AlertsConfig) -> dict[str, Any]:
    """Return alert setup readiness without sending anything.

    The result is a read-only diagnosis only and must never include sensitive values
    such as bot tokens, chat ids or SMTP passwords.
    """

    if not config.enabled:
        return {
            "status": "healthy",
            "enabled": False,
            "message": "告警当前已关闭，不会发送 Telegram 或 Email 通知。",
            "min_severity": config.min_severity,
            "cooldown_seconds": config.cooldown_seconds,
            "send_recovery": config.send_recovery,
            "state_file_ready": bool(config.state_file and str(config.state_file).strip()),
            "channels": {
                "telegram": {
                    "enabled": bool(config.telegram.enabled),
                    "ready": False,
                    "missing_fields": _channel_missing_telegram(config.telegram),
                    "message": "Telegram 告警未开启。",
                },
                "email": {
                    "enabled": bool(config.email.enabled),
                    "ready": False,
                    "missing_fields": _channel_missing_email(config.email),
                    "message": "Email 告警未开启。",
                },
            },
            "safe_to_test": False,
            "validations": {
                "min_severity_valid": _is_valid_min_severity(config.min_severity),
                "cooldown_seconds_valid": bool(config.cooldown_seconds > 0),
                "state_file_configured": bool(config.state_file and str(config.state_file).strip()),
                "telegram_enabled": bool(config.telegram.enabled),
                "email_enabled": bool(config.email.enabled),
            },
        }

    telegram_missing = _channel_missing_telegram(config.telegram)
    email_missing = _channel_missing_email(config.email)
    telegram_ready = bool(config.telegram.enabled and not telegram_missing)
    email_ready = bool(config.email.enabled and not email_missing)
    min_severity_valid = _is_valid_min_severity(config.min_severity)
    cooldown_valid = config.cooldown_seconds > 0
    state_file_ready = bool(config.state_file and str(config.state_file).strip())

    status = "healthy"
    if not min_severity_valid or not cooldown_valid or not state_file_ready:
        status = "warning"
    elif not telegram_ready and not email_ready:
        status = "warning"

    if status == "healthy":
        message = "告警配置可用，Telegram / Email 可用性正常。"
    elif not (config.telegram.enabled or config.email.enabled):
        message = "告警已开启，但未启用 Telegram / Email。"
    elif telegram_ready or email_ready:
        message = "告警已开启，至少有一个渠道可发送通知。"
    else:
        message = "告警已开启，但未完成可用渠道配置。"

    return {
        "status": status,
        "enabled": True,
        "message": message,
        "min_severity": config.min_severity,
        "cooldown_seconds": config.cooldown_seconds,
        "send_recovery": config.send_recovery,
        "state_file_ready": state_file_ready,
        "channels": {
            "telegram": {
                "enabled": bool(config.telegram.enabled),
                "ready": telegram_ready,
                "missing_fields": telegram_missing,
                "message": (
                    "Telegram 未开启。"
                    if not config.telegram.enabled
                    else ("Telegram 已开启且配置完整。" if telegram_ready else "Telegram 已开启，但缺少必要配置。")
                ),
            },
            "email": {
                "enabled": bool(config.email.enabled),
                "ready": email_ready,
                "missing_fields": email_missing,
                "message": (
                    "Email 未开启。"
                    if not config.email.enabled
                    else ("Email 已开启且配置完整。" if email_ready else "Email 已开启，但缺少必要配置。")
                ),
            },
        },
        "safe_to_test": bool(config.enabled and (telegram_ready or email_ready)),
        "validations": {
            "min_severity_valid": min_severity_valid,
            "cooldown_seconds_valid": cooldown_valid,
            "state_file_configured": state_file_ready,
            "telegram_enabled": bool(config.telegram.enabled),
            "email_enabled": bool(config.email.enabled),
        },
    }
