from pathlib import Path

from app.history.models import HealthEvent, HealthSnapshot
from app.history.store import append_event, append_snapshot, build_id, load_events, load_snapshots, save_events, save_snapshots


def test_load_missing_files_returns_empty(tmp_path):
    snapshot_file = tmp_path / "missing_history.json"
    event_file = tmp_path / "missing_events.json"

    snapshots, snapshot_error = load_snapshots(snapshot_file)
    events, event_error = load_events(event_file)

    assert snapshots == []
    assert events == []
    assert snapshot_error is None
    assert event_error is None


def test_append_snapshot_and_trim(tmp_path):
    data_file = tmp_path / "history.json"

    for i in range(5):
        append_snapshot(
            data_file,
            HealthSnapshot(
                id=f"s-{i}",
                checked_at=f"2026-06-09T00:00:0{i}Z",
                overall_status="healthy",
                module_statuses={},
                proxy_core_status="healthy",
                proxy_port_status="healthy",
                panel_status="healthy",
                domain_status="healthy",
                tls_status="healthy",
                traffic_status="healthy",
                diagnostics_status="healthy",
                traffic_usage_percent=0.0,
                traffic_estimated_used_gb=0.0,
                readable_summary="ok",
            ),
            max_snapshots=3,
        )

    items, _ = load_snapshots(data_file)
    assert len(items) == 3
    assert items[0].id == "s-2"
    assert items[-1].id == "s-4"


def test_append_event_and_trim(tmp_path):
    data_file = tmp_path / "events.json"

    for i in range(4):
        append_event(
            data_file,
            HealthEvent(
                id=f"e-{i}",
                event_type="status_change",
                severity="warning" if i else "critical",
                title=f"事件{i}",
                message="m",
                module="proxy_core",
                previous_status="healthy",
                current_status="warning" if i else "critical",
                occurred_at=f"2026-06-09T00:00:0{i}Z",
                resolved_at=None,
                is_recovery=False,
                fingerprint="proxy_core:healthy->warning",
            ),
            max_events=2,
        )

    events, _ = load_events(data_file)
    assert len(events) == 2
    assert events[0].id == "e-2"
    assert events[1].id == "e-3"


def test_corrupt_file_load_returns_warning(tmp_path):
    history_file = tmp_path / "bad.json"
    history_file.write_text("{bad", encoding="utf-8")
    snapshots, error = load_snapshots(history_file)

    assert snapshots == []
    assert isinstance(error, str)


def test_build_id_format():
    value = build_id("snapshot")
    assert value.startswith("snapshot-")
