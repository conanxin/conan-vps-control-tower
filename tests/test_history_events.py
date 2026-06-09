from app.history.events import build_events, dedupe_events
from app.history.models import HealthEvent, HealthSnapshot


def _snapshot(overall: str, proxy_core: str = "healthy", proxy_ports: str = "healthy", traffic: str = "healthy", diag: str = "healthy", panel: str = "healthy") -> HealthSnapshot:
    return HealthSnapshot(
        id="s",
        checked_at="2026-06-09T00:00:00Z",
        overall_status=overall,
        module_statuses={},
        proxy_core_status=proxy_core,
        proxy_port_status=proxy_ports,
        panel_status=panel,
        domain_status="healthy",
        tls_status="healthy",
        traffic_status=traffic,
        diagnostics_status=diag,
        traffic_usage_percent=0.0,
        traffic_estimated_used_gb=0.0,
        readable_summary="x",
    )


def test_healthy_to_warning_generates_events():
    previous = _snapshot("healthy", proxy_ports="healthy")
    current = _snapshot("warning", proxy_ports="warning")
    events = build_events(current, previous, diagnostics_status="healthy", enabled_domain=False, enabled_tls=False)

    assert events, "expect events when status changes"
    assert any(item.module == "overall" for item in events)
    assert any(item.module == "proxy_ports" for item in events)
    assert events[0].is_recovery is False


def test_warning_to_healthy_generates_recovery_event():
    previous = _snapshot("warning", proxy_ports="warning")
    current = _snapshot("healthy", proxy_ports="healthy")
    events = build_events(current, previous, diagnostics_status="healthy", enabled_domain=False, enabled_tls=False)

    assert any(item.is_recovery for item in events)
    assert any(item.module == "overall" for item in events)


def test_no_duplicate_events_for_same_fingerprint():
    first = HealthEvent(
        id="e1",
        event_type="status_change",
        severity="warning",
        title="x",
        message="x",
        module="overall",
        previous_status="healthy",
        current_status="warning",
        occurred_at="2026-06-09T00:00:00Z",
        resolved_at=None,
        is_recovery=False,
        fingerprint="overall:healthy->warning",
    )
    second = HealthEvent(
        id="e2",
        event_type="status_change",
        severity="warning",
        title="x",
        message="x",
        module="overall",
        previous_status="healthy",
        current_status="warning",
        occurred_at="2026-06-09T00:01:00Z",
        resolved_at=None,
        is_recovery=False,
        fingerprint="overall:healthy->warning",
    )
    assert dedupe_events([second], [first]) == []
