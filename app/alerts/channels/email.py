from __future__ import annotations

import smtplib

from app.alerts.formatters import build_email_message
from app.alerts.models import AlertEvent, ChannelResult
from app.config import EmailAlertConfig


def is_placeholder(value: str) -> bool:
    return not value or value.startswith("${") or value.endswith("}") or value.startswith("YOUR_")


def send_email(event: AlertEvent, config: EmailAlertConfig) -> ChannelResult:
    if not config.enabled:
        return ChannelResult(channel="email", success=False, skipped=True, message="Email disabled")
    required = [config.smtp_host, config.username, config.password, config.from_addr, *config.to_addrs]
    if any(is_placeholder(value) for value in required):
        return ChannelResult(channel="email", success=False, skipped=True, message="Email SMTP settings not configured")

    try:
        message = build_email_message(event, config.from_addr, config.to_addrs)
        with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=config.timeout_seconds) as smtp:
            if config.use_tls:
                smtp.starttls()
            smtp.login(config.username, config.password)
            smtp.send_message(message)
        return ChannelResult(channel="email", success=True, message="Email alert sent")
    except Exception as exc:
        return ChannelResult(channel="email", success=False, error=f"Email send failed: {type(exc).__name__}")
