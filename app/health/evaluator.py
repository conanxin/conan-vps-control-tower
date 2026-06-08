from __future__ import annotations

from typing import cast

from app.models import HealthStatus
from app.models import CheckResult, HealthResponse

STATUS_SEVERITY = {
    "healthy": 0,
    "unknown": 1,
    "warning": 2,
    "degraded": 3,
    "critical": 4,
}


def aggregate_status(checks: list[CheckResult]) -> str:
    active_checks = [check for check in checks if not check.ignored]
    if not active_checks:
        return "unknown"
    return max(active_checks, key=lambda item: STATUS_SEVERITY[item.status]).status


def build_readable_summary(overall_status: str, checks: list[CheckResult]) -> str:
    active_checks = [check for check in checks if not check.ignored]
    failing = [check for check in active_checks if check.status != "healthy"]
    ignored = [check for check in checks if check.ignored]
    ignored_names = ", ".join(check.name for check in ignored)

    if overall_status == "healthy":
        if ignored_names:
            return f"All configured health checks look healthy. Not configured: {ignored_names}."
        return "All monitored VPS and proxy health checks look healthy."
    if overall_status == "unknown" and failing:
        return "Some checks could not determine a status. Review permissions, platform support, and configuration."
    if failing:
        names = ", ".join(check.name for check in failing)
        return f"Attention needed for: {names}."
    return "Health status is unknown because no checks were executed."


def build_risk_summary(checks: list[CheckResult]) -> list[str]:
    risks: list[str] = []
    for check in checks:
        if check.ignored:
            risks.append(f"{check.name}: {check.message}")
            continue
        if check.status == "healthy":
            continue
        risks.append(f"{check.name}: {check.message}")
    return risks or ["No visible risks from current checks."]


def evaluate(checks: list[CheckResult]) -> HealthResponse:
    overall = aggregate_status(checks)
    return HealthResponse(
        overall_status=cast(HealthStatus, overall),
        readable_summary=build_readable_summary(overall, checks),
        risk_summary=build_risk_summary(checks),
        checks=checks,
    )
