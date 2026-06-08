from app.alerts.channels.email import send_email
from app.alerts.channels.telegram import send_telegram
from app.alerts.models import AlertEvent
from app.config import EmailAlertConfig, TelegramAlertConfig


def make_event():
    return AlertEvent(
        fingerprint="test",
        title="Conan VPS Control Tower test alert",
        severity="warning",
        status="test",
        module="alerting",
        message="This is a test notification, not a failure.",
        summary="test",
        checked_at="2026-06-08T00:00:00+00:00",
    )


def test_telegram_skipped_when_token_unconfigured():
    result = send_telegram(make_event(), TelegramAlertConfig(enabled=True))

    assert result.skipped is True
    assert result.success is False


def test_email_skipped_when_password_unconfigured():
    result = send_email(make_event(), EmailAlertConfig(enabled=True))

    assert result.skipped is True
    assert result.success is False
