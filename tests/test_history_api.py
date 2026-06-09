from pathlib import Path

from fastapi.testclient import TestClient

from app.history.store import load_events, load_snapshots
from app.main import app, get_config


def _write_config(path: Path, *, enabled: bool = True, min_interval: int = 0) -> None:
    base = path.parent.as_posix()
    config_text = f"""
server:
  host: "127.0.0.1"
  port: 3001

history:
  enabled: {str(enabled).lower()}
  data_file: "{base}/health_history.json"
  event_file: "{base}/event_log.json"
  max_snapshots: 20
  max_events: 20
  min_record_interval_seconds: {min_interval}
  summary_window_hours: 24
""".strip()
    path.write_text(config_text, encoding="utf-8")


def test_history_endpoints_enabled_and_json_shape(tmp_path, monkeypatch):
    _write_config(tmp_path / "config.yaml", enabled=True, min_interval=0)
    monkeypatch.setenv("CONAN_CONFIG_PATH", str(tmp_path / "config.yaml"))
    get_config.cache_clear()

    client = TestClient(app)

    # Bootstrap one health check so history snapshot exists.
    response = client.get("/api/health")
    assert response.status_code == 200

    summary = client.get("/api/history/summary")
    assert summary.status_code == 200
    summary_payload = summary.json()
    assert summary_payload["enabled"] is True
    assert summary_payload["snapshot_count"] >= 1
    assert "status" in summary_payload

    recent = client.get("/api/history/recent?limit=10")
    assert recent.status_code == 200
    recent_payload = recent.json()
    assert recent_payload["enabled"] is True
    assert "items" in recent_payload
    assert isinstance(recent_payload["items"], list)
    assert recent_payload["limit"] == 10

    events = client.get("/api/events?limit=10")
    assert events.status_code == 200
    events_payload = events.json()
    assert events_payload["enabled"] is True
    assert "items" in events_payload
    assert isinstance(events_payload["items"], list)
    assert events_payload["limit"] == 10

    # Files should be readable JSON and not crash API consumption.
    snapshots, snapshot_error = load_snapshots(tmp_path / "health_history.json")
    events_data, event_error = load_events(tmp_path / "event_log.json")
    assert snapshot_error is None
    assert event_error is None
    assert snapshots
    assert isinstance(events_data, list)
