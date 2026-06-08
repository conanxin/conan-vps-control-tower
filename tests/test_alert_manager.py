from app.alerts.manager import AlertManager
from app.alerts.models import ChannelResult
from app.config import AlertsConfig
from app.models import CheckResult
from app.health.evaluator import evaluate


def make_config(tmp_path, cooldown_seconds=1800):
    return AlertsConfig(
        enabled=True,
        min_severity="warning",
        cooldown_seconds=cooldown_seconds,
        send_recovery=True,
        state_file=str(tmp_path / "alert_state.json"),
    )


def test_alert_manager_filters_warning_and_sends(monkeypatch, tmp_path):
    monkeypatch.setattr(
        AlertManager,
        "_send",
        lambda self, event: [ChannelResult(channel="test", success=True, message="sent")],
    )
    manager = AlertManager(make_config(tmp_path))
    health = evaluate([CheckResult(name="traffic", status="warning", message="near limit")])

    result = manager.evaluate(health)

    assert result.sent is True
    assert result.events[0].module == "traffic"


def test_alert_manager_dedupes_with_cooldown(monkeypatch, tmp_path):
    calls = []

    def fake_send(self, event):
        calls.append(event.fingerprint)
        return [ChannelResult(channel="test", success=True, message="sent")]

    monkeypatch.setattr(AlertManager, "_send", fake_send)
    manager = AlertManager(make_config(tmp_path, cooldown_seconds=3600))
    health = evaluate([CheckResult(name="proxy_core", status="critical", message="down")])

    first = manager.evaluate(health)
    second = manager.evaluate(health)

    assert first.sent is True
    assert second.sent is False
    assert calls == ["proxy_core:critical"]


def test_alert_manager_sends_recovery(monkeypatch, tmp_path):
    calls = []

    def fake_send(self, event):
        calls.append(event.is_recovery)
        return [ChannelResult(channel="test", success=True, message="sent")]

    monkeypatch.setattr(AlertManager, "_send", fake_send)
    manager = AlertManager(make_config(tmp_path, cooldown_seconds=0))
    bad = evaluate([CheckResult(name="tls_certificate", status="critical", message="expired")])
    good = evaluate([CheckResult(name="tls_certificate", status="healthy", message="ok")])

    manager.evaluate(bad)
    recovery = manager.evaluate(good)

    assert recovery.sent is True
    assert calls == [False, True]
