from __future__ import annotations

import os

import psutil

from app.config import SystemConfig
from app.models import CheckResult


def check_system(config: SystemConfig) -> CheckResult:
    try:
        disk = psutil.disk_usage("/")
        memory = psutil.virtual_memory()
        load_1m = os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0

        risks: list[str] = []
        status = "healthy"

        if disk.percent >= config.disk_warning_percent:
            risks.append(f"Disk usage is {disk.percent:.1f}%.")
        if memory.percent >= config.ram_warning_percent:
            risks.append(f"RAM usage is {memory.percent:.1f}%.")
        if load_1m >= config.load_warning_1m:
            risks.append(f"1-minute load is {load_1m:.2f}.")

        if risks:
            status = "warning"

        return CheckResult(
            name="vps_system",
            status=status,
            message="VPS resources look normal" if not risks else "VPS resource pressure detected",
            details={
                "disk_percent": disk.percent,
                "ram_percent": memory.percent,
                "load_1m": load_1m,
                "cpu_percent": psutil.cpu_percent(interval=0.0),
                "risks": risks,
            },
        )
    except Exception as exc:
        return CheckResult(
            name="vps_system",
            status="unknown",
            message="Unable to read VPS system status",
            details={"error": str(exc)},
        )
