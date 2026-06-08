from __future__ import annotations

from app.alerts.severity import ORDER
from app.diagnostics.models import DiagnosticItem, DiagnosticsResult
from app.diagnostics.rules import RULES, all_healthy, by_name
from app.models import HealthResponse, utc_now_iso


def sort_items(items: list[DiagnosticItem]) -> list[DiagnosticItem]:
    return sorted(items, key=lambda item: ORDER.get(item.severity, -1), reverse=True)


def diagnose(health: HealthResponse) -> DiagnosticsResult:
    try:
        checks = by_name(health)
        items = [item for rule in RULES if (item := rule(checks))]
        if not items:
            items = [all_healthy(health)]
        items = sort_items(items)
        top = items[0]
        summary = top.summary if top.diagnosis_id != "all_healthy" else "No active diagnostic issues detected."
        return DiagnosticsResult(status=top.severity, items=items, summary=summary, checked_at=utc_now_iso())
    except Exception as exc:
        return DiagnosticsResult(
            status="unknown",
            items=[],
            summary=f"Diagnostics unavailable: {type(exc).__name__}",
            checked_at=utc_now_iso(),
        )
