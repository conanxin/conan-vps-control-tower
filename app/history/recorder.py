from __future__ import annotations

from datetime import UTC, datetime

from app.config import HistoryConfig
from app.diagnostics.engine import diagnose
from app.history.events import build_events, dedupe_events
from app.history.models import HealthEvent, HealthSnapshot
from app.history.store import append_event, append_snapshot, load_events, load_snapshots
from app.models import HealthResponse


def _to_iso() -> str:
    return datetime.now(UTC).isoformat()


def _safe_check_value(checks: list[object], name: str, fallback: str = "unknown") -> str:
    for check in checks:
        if isinstance(check, dict):
            if check.get("name") == name:
                return str(check.get("status", fallback))
        else:
            if getattr(check, "name", None) == name:
                return str(getattr(check, "status", fallback))
    return fallback


def _module_status_map(checks: list[object]) -> dict[str, str]:
    return {
        getattr(check, "name", ""): getattr(check, "status", "unknown")
        for check in checks
        if getattr(check, "name", None)
    }


def _is_check_enabled(details: object | None, is_ignored: bool) -> bool:
    # Domain / TLS are optional; when ignored they are treated as disabled for event generation.
    if is_ignored:
        return False
    if isinstance(details, dict):
        return bool(details.get("enabled", True))
    return True


def record_health_snapshot(
    health: HealthResponse,
    config: HistoryConfig,
) -> dict[str, object]:
    if not config.enabled:
        return {"recorded": False, "reason": "history disabled", "snapshot_id": None}

    try:
        checks = health.checks
        module_statuses = _module_status_map(checks)
        traffic_check = next((item for item in checks if getattr(item, "name", "") == "traffic"), None)
        traffic_usage_percent = 0.0
        traffic_estimated_used_gb = 0.0
        if traffic_check is not None:
            details = getattr(traffic_check, "details", {}) or {}
            traffic_usage_percent = float(details.get("usage_percent", 0.0))
            traffic_estimated_used_gb = float(details.get("estimated_used_gb", 0.0))

        now = _to_iso()
        existing_snapshots, load_error = load_snapshots(config.data_file)
        if load_error:
            existing_snapshots = []

        if existing_snapshots:
            last_checked = existing_snapshots[-1].checked_at
            try:
                delta = datetime.fromisoformat(now) - datetime.fromisoformat(last_checked)
                if delta.total_seconds() < config.min_record_interval_seconds:
                    return {
                        "recorded": False,
                        "reason": "record throttled by min_record_interval_seconds",
                        "snapshot_id": None,
                        "warning": load_error,
                    }
            except Exception:
                pass

        current_status = health.overall_status
        snapshot = HealthSnapshot(
            id=f"snapshot-{datetime.now().strftime('%Y%m%dT%H%M%S%f')}",
            checked_at=now,
            overall_status=current_status,
            module_statuses=module_statuses,
            proxy_core_status=_safe_check_value(checks, "proxy_core"),
            proxy_port_status=_safe_check_value(checks, "proxy_ports"),
            panel_status=_safe_check_value(checks, "xui_panel"),
            domain_status=_safe_check_value(checks, "domain_dns"),
            tls_status=_safe_check_value(checks, "tls_certificate"),
            traffic_status=_safe_check_value(checks, "traffic"),
            diagnostics_status=_derive_diagnostics_status(health),
            traffic_usage_percent=traffic_usage_percent,
            traffic_estimated_used_gb=traffic_estimated_used_gb,
            readable_summary=health.readable_summary,
        )

        append_snapshot(config.data_file, snapshot, max_snapshots=config.max_snapshots)

        diagnostics = diagnose(health)
        previous = existing_snapshots[-1] if existing_snapshots else None

        events, event_load_error = load_events(config.event_file)
        if event_load_error:
            events = []

        domain_enabled = any(
            getattr(check, "name", "") == "domain_dns" and not bool(getattr(check, "ignored", False))
            for check in checks
        )
        tls_enabled = any(
            getattr(check, "name", "") == "tls_certificate" and not bool(getattr(check, "ignored", False))
            for check in checks
        )

        new_events = build_events(snapshot, previous, diagnostics.status, domain_enabled, tls_enabled)
        for event in dedupe_events(new_events, events):
            append_event(config.event_file, event, max_events=config.max_events)

        return {
            "recorded": True,
            "reason": "ok",
            "snapshot_id": snapshot.id,
            "warning": load_error or event_load_error,
        }
    except Exception as exc:
        return {"recorded": False, "reason": f"history recording failed: {type(exc).__name__}", "snapshot_id": None}


def _derive_diagnostics_status(health: HealthResponse) -> str:
    try:
        return diagnose(health).status
    except Exception:
        return "unknown"
