from datetime import datetime, timedelta

from app.history.models import HealthEvent, HealthSnapshot
from app.history.summary import build_summary


def _iso(delta_seconds: int) -> str:
    return (datetime.utcnow() - timedelta(seconds=delta_seconds)).isoformat()


def test_build_summary_counts_and_worst_status():
    snapshots = [
        HealthSnapshot(
            id="s1",
            checked_at=_iso(30),
            overall_status="healthy",
            module_statuses={},
            proxy_core_status="healthy",
            proxy_port_status="healthy",
            panel_status="healthy",
            domain_status="healthy",
            tls_status="healthy",
            traffic_status="healthy",
            diagnostics_status="healthy",
            traffic_usage_percent=10.0,
            traffic_estimated_used_gb=1.0,
            readable_summary="ok",
        ),
        HealthSnapshot(
            id="s2",
            checked_at=_iso(10),
            overall_status="critical",
            module_statuses={},
            proxy_core_status="critical",
            proxy_port_status="healthy",
            panel_status="healthy",
            domain_status="healthy",
            tls_status="healthy",
            traffic_status="critical",
            diagnostics_status="warning",
            traffic_usage_percent=95.0,
            traffic_estimated_used_gb=950.0,
            readable_summary="bad",
        ),
    ]

    events = [
        HealthEvent(
            id="e1",
            event_type="status_change",
            severity="critical",
            title="x",
            message="critical",
            module="proxy_core",
            previous_status="healthy",
            current_status="critical",
            occurred_at=_iso(20),
            resolved_at=None,
            is_recovery=False,
            fingerprint="proxy_core:healthy->critical",
        )
    ]

    summary = build_summary(snapshots, events, window_hours=24)
    assert summary.snapshot_count == 2
    assert summary.event_count == 1
    assert summary.worst_status == "critical"
    assert summary.critical_count == 1
    assert summary.warning_count == 0
    assert summary.degraded_count == 0
    assert summary.status == "critical"
    assert summary.last_event == "x"
    assert summary.healthy_ratio == 50.0
