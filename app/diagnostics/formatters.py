from __future__ import annotations

from app.diagnostics.models import DiagnosticItem, DiagnosticsResult


def short_text(result: DiagnosticsResult) -> str:
    if not result.items:
        return result.summary
    item = result.items[0]
    return f"{item.title}: {item.suggested_first_check}"


def alert_first_check(item: DiagnosticItem | None) -> str:
    if not item:
        return "Open Dashboard or SSH into VPS and inspect service status."
    return item.suggested_first_check
