from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class HealthSnapshot:
    id: str
    checked_at: str
    overall_status: str
    module_statuses: dict[str, str]
    proxy_core_status: str
    proxy_port_status: str
    panel_status: str
    domain_status: str
    tls_status: str
    traffic_status: str
    diagnostics_status: str
    traffic_usage_percent: float
    traffic_estimated_used_gb: float
    readable_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "checked_at": self.checked_at,
            "overall_status": self.overall_status,
            "module_statuses": self.module_statuses,
            "proxy_core_status": self.proxy_core_status,
            "proxy_port_status": self.proxy_port_status,
            "panel_status": self.panel_status,
            "domain_status": self.domain_status,
            "tls_status": self.tls_status,
            "traffic_status": self.traffic_status,
            "diagnostics_status": self.diagnostics_status,
            "traffic_usage_percent": self.traffic_usage_percent,
            "traffic_estimated_used_gb": self.traffic_estimated_used_gb,
            "readable_summary": self.readable_summary,
        }


@dataclass
class HealthEvent:
    id: str
    event_type: str
    severity: str
    title: str
    message: str
    module: str
    previous_status: str
    current_status: str
    occurred_at: str
    resolved_at: str | None
    is_recovery: bool
    fingerprint: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "severity": self.severity,
            "title": self.title,
            "message": self.message,
            "module": self.module,
            "previous_status": self.previous_status,
            "current_status": self.current_status,
            "occurred_at": self.occurred_at,
            "resolved_at": self.resolved_at,
            "is_recovery": self.is_recovery,
            "fingerprint": self.fingerprint,
        }


@dataclass
class HistorySummary:
    status: str
    window_hours: int
    snapshot_count: int
    event_count: int
    latest_status: str
    worst_status: str
    healthy_ratio: float
    warning_count: int
    degraded_count: int
    critical_count: int
    last_event: str | None
    last_problem_at: str | None
    last_recovery_at: str | None
    uptime_label: str
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "window_hours": self.window_hours,
            "snapshot_count": self.snapshot_count,
            "event_count": self.event_count,
            "latest_status": self.latest_status,
            "worst_status": self.worst_status,
            "healthy_ratio": self.healthy_ratio,
            "warning_count": self.warning_count,
            "degraded_count": self.degraded_count,
            "critical_count": self.critical_count,
            "last_event": self.last_event,
            "last_problem_at": self.last_problem_at,
            "last_recovery_at": self.last_recovery_at,
            "uptime_label": self.uptime_label,
            "summary": self.summary,
        }
