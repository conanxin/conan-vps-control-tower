from datetime import UTC, datetime, timedelta

from app.config import TLSConfig, TLSTargetConfig
from app.health import tls_checker
from app.health.tls_checker import check_tls


def test_tls_disabled_is_ignored():
    result = check_tls(TLSConfig(enabled=False))

    assert result.status == "unknown"
    assert result.ignored is True
    assert result.details["enabled"] is False


def test_tls_critical_when_days_remaining_under_critical(monkeypatch):
    now = datetime.now(UTC)
    monkeypatch.setattr(tls_checker, "get_certificate_not_after", lambda target: now + timedelta(days=3))

    result = check_tls(
        TLSConfig(
            enabled=True,
            targets=[
                TLSTargetConfig(
                    host="example.com",
                    server_name="example.com",
                    warning_days=21,
                    critical_days=7,
                )
            ],
        )
    )

    assert result.status == "critical"
    assert result.details["targets"][0]["days_remaining"] <= 7


def test_tls_warning_when_days_remaining_under_warning(monkeypatch):
    now = datetime.now(UTC)
    monkeypatch.setattr(tls_checker, "get_certificate_not_after", lambda target: now + timedelta(days=14))

    result = check_tls(
        TLSConfig(
            enabled=True,
            targets=[
                TLSTargetConfig(
                    host="example.com",
                    server_name="example.com",
                    warning_days=21,
                    critical_days=7,
                )
            ],
        )
    )

    assert result.status == "warning"
    assert result.details["targets"][0]["days_remaining"] <= 21
