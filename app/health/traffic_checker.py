from __future__ import annotations

import psutil

from app.config import TrafficConfig
from app.models import CheckResult


def check_traffic(config: TrafficConfig) -> CheckResult:
    try:
        counters = psutil.net_io_counters()
        total_bytes = counters.bytes_sent + counters.bytes_recv
        total_gb = total_bytes / (1024**3)
        usage_percent = (total_gb / config.monthly_limit_gb) * 100 if config.monthly_limit_gb > 0 else 0

        status = "healthy"
        message = "Traffic counters are readable"
        if usage_percent >= 90:
            status = "warning"
            message = "Traffic usage is close to the configured monthly limit"

        return CheckResult(
            name="traffic",
            status=status,
            message=message,
            details={
                "bytes_sent": counters.bytes_sent,
                "bytes_recv": counters.bytes_recv,
                "total_gb_since_boot": round(total_gb, 3),
                "monthly_limit_gb": config.monthly_limit_gb,
                "estimated_usage_percent_since_boot": round(usage_percent, 2),
                "reset_day": config.reset_day,
            },
        )
    except Exception as exc:
        return CheckResult(
            name="traffic",
            status="unknown",
            message="Unable to read traffic counters",
            details={"error": str(exc)},
        )
