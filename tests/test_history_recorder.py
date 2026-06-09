from pathlib import Path

from app.config import load_config
from app.history.models import HealthSnapshot
from app.history.recorder import record_health_snapshot
from app.history.store import load_snapshots
from app.models import CheckResult, HealthResponse


def _health_response(overall_status: str = "healthy", module_status: str = "healthy") -> HealthResponse:
    return HealthResponse(
        overall_status=overall_status,
        readable_summary="ok",
        risk_summary=[],
        checks=[
            CheckResult(name="vps_system", status=module_status, message="ok"),
            CheckResult(name="proxy_core", status=module_status, message="ok"),
            CheckResult(name="xui_panel", status=module_status, message="ok"),
            CheckResult(name="proxy_ports", status=module_status, message="ok"),
            CheckResult(name="domain_dns", status="unknown", message="not configured", ignored=True),
            CheckResult(name="tls_certificate", status="unknown", message="not configured", ignored=True),
            CheckResult(name="traffic", status=module_status, message="ok"),
        ],
    )


def _write_history_enabled_config(tmp_path: Path, *, enabled: bool, min_interval: int = 60) -> Path:
    config_path = tmp_path / "config.yaml"
    base = tmp_path.as_posix()
    config_path.write_text(
        f"history:\n"
        f"  enabled: {str(enabled).lower()}\n"
        f"  data_file: \"{base}/health_history.json\"\n"
        f"  event_file: \"{base}/event_log.json\"\n"
        f"  max_snapshots: 20\n"
        f"  max_events: 20\n"
        f"  min_record_interval_seconds: {min_interval}\n"
        f"  summary_window_hours: 24\n",
        encoding="utf-8",
    )
    return config_path


def test_history_recorder_records_and_throttles(tmp_path, monkeypatch):
    _write_history_enabled_config(tmp_path, enabled=True, min_interval=60)
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(tmp_path / "config.yaml"))
    config = load_config()

    first = record_health_snapshot(_health_response(), config.history)
    second = record_health_snapshot(_health_response(), config.history)

    assert first["recorded"] is True
    assert second["recorded"] is False

    snapshots, _ = load_snapshots(config.history.data_file)
    assert len(snapshots) == 1


def test_history_recorder_disabled(tmp_path, monkeypatch):
    _write_history_enabled_config(tmp_path, enabled=False)
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(tmp_path / "config.yaml"))
    config = load_config()

    result = record_health_snapshot(_health_response(), config.history)
    assert result["recorded"] is False
    assert result["reason"] == "history disabled"

    snapshots, _ = load_snapshots(config.history.data_file)
    assert snapshots == []


def test_recorder_stores_snapshot_fields(tmp_path, monkeypatch):
    _write_history_enabled_config(tmp_path, enabled=True, min_interval=0)
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(tmp_path / "config.yaml"))
    config = load_config()

    result = record_health_snapshot(_health_response("critical", module_status="critical"), config.history)
    assert result["recorded"] is True

    snapshots, _ = load_snapshots(config.history.data_file)
    assert len(snapshots) == 1
    item = snapshots[0]
    assert isinstance(item, HealthSnapshot)
    assert item.overall_status == "critical"
    assert item.proxy_port_status == "critical"
    assert item.traffic_usage_percent >= 0.0
