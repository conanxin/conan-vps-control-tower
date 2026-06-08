from __future__ import annotations

ORDER = {
    "healthy": 0,
    "unknown": 1,
    "warning": 2,
    "degraded": 3,
    "critical": 4,
}


def is_at_least(status: str, min_severity: str) -> bool:
    if status == "unknown":
        return False
    return ORDER.get(status, -1) >= ORDER.get(min_severity, ORDER["warning"])
