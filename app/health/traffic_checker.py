from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from app.config import TrafficConfig
from app.models import CheckResult


SYS_CLASS_NET = Path("/sys/class/net")


def read_interface_bytes(interface: str, sys_class_net: Path = SYS_CLASS_NET) -> tuple[int, int]:
    interface_path = sys_class_net / interface / "statistics"
    rx_bytes = int((interface_path / "rx_bytes").read_text(encoding="utf-8").strip())
    tx_bytes = int((interface_path / "tx_bytes").read_text(encoding="utf-8").strip())
    return rx_bytes, tx_bytes


def select_interfaces(configured: list[str], sys_class_net: Path = SYS_CLASS_NET) -> list[str]:
    if not sys_class_net.exists():
        return []

    if configured == ["auto"]:
        interfaces = []
        for path in sorted(sys_class_net.iterdir()):
            if path.name == "lo":
                continue
            stats = path / "statistics"
            if (stats / "rx_bytes").exists() and (stats / "tx_bytes").exists():
                interfaces.append(path.name)
        return interfaces

    return [
        interface
        for interface in configured
        if (sys_class_net / interface / "statistics" / "rx_bytes").exists()
        and (sys_class_net / interface / "statistics" / "tx_bytes").exists()
    ]


def read_total_bytes(interfaces: list[str], sys_class_net: Path = SYS_CLASS_NET) -> tuple[int, int, dict[str, dict[str, int]]]:
    total_rx = 0
    total_tx = 0
    per_interface: dict[str, dict[str, int]] = {}

    for interface in interfaces:
        rx_bytes, tx_bytes = read_interface_bytes(interface, sys_class_net)
        total_rx += rx_bytes
        total_tx += tx_bytes
        per_interface[interface] = {"rx_bytes": rx_bytes, "tx_bytes": tx_bytes}

    return total_rx, total_tx, per_interface


def load_state(data_file: Path) -> dict[str, object]:
    if not data_file.exists():
        return {}
    with data_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(data_file: Path, state: dict[str, object]) -> None:
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with data_file.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2, sort_keys=True)


def build_baseline_state(config: TrafficConfig, rx_bytes: int, tx_bytes: int) -> dict[str, object]:
    return {
        "cycle_start_date": date.today().isoformat(),
        "reset_day": config.reset_day,
        "baseline_rx_bytes": rx_bytes,
        "baseline_tx_bytes": tx_bytes,
        "latest_rx_bytes": rx_bytes,
        "latest_tx_bytes": tx_bytes,
        "estimated_used_gb": 0.0,
        "monthly_limit_gb": config.monthly_limit_gb,
        "usage_percent": 0.0,
    }


def status_from_usage(config: TrafficConfig, usage_percent: float) -> str:
    if usage_percent >= config.critical_percent:
        return "critical"
    if usage_percent >= config.degraded_percent:
        return "degraded"
    if usage_percent >= config.warning_percent:
        return "warning"
    return "healthy"


def check_traffic(config: TrafficConfig, sys_class_net: Path = SYS_CLASS_NET) -> CheckResult:
    try:
        interfaces = select_interfaces(config.interfaces, sys_class_net)
        if not interfaces:
            return CheckResult(
                name="traffic",
                status="unknown",
                message="Local interface traffic statistics are not available",
                details={
                    "interfaces": config.interfaces,
                    "enabled_interfaces": [],
                    "note": config.note,
                    "error": "No readable /sys/class/net interfaces found",
                },
            )

        rx_bytes, tx_bytes, per_interface = read_total_bytes(interfaces, sys_class_net)
        data_file = Path(config.data_file)
        state = load_state(data_file)

        if not state:
            state = build_baseline_state(config, rx_bytes, tx_bytes)
            save_state(data_file, state)
            return CheckResult(
                name="traffic",
                status="healthy",
                message="Traffic baseline created; future refreshes will provide a better local estimate",
                details={
                    **state,
                    "enabled_interfaces": interfaces,
                    "per_interface": per_interface,
                    "data_file": str(data_file),
                    "note": config.note,
                },
            )

        baseline_rx = int(state.get("baseline_rx_bytes", rx_bytes))
        baseline_tx = int(state.get("baseline_tx_bytes", tx_bytes))
        used_bytes = max(0, rx_bytes - baseline_rx) + max(0, tx_bytes - baseline_tx)
        estimated_used_gb = used_bytes / (1024**3)
        usage_percent = (estimated_used_gb / config.monthly_limit_gb) * 100 if config.monthly_limit_gb > 0 else 0.0
        status = status_from_usage(config, usage_percent)

        state.update(
            {
                "reset_day": config.reset_day,
                "latest_rx_bytes": rx_bytes,
                "latest_tx_bytes": tx_bytes,
                "estimated_used_gb": round(estimated_used_gb, 3),
                "monthly_limit_gb": config.monthly_limit_gb,
                "usage_percent": round(usage_percent, 2),
            }
        )
        save_state(data_file, state)

        if status == "critical":
            message = "Local traffic estimate is at or above the critical threshold"
        elif status == "degraded":
            message = "Local traffic estimate is high"
        elif status == "warning":
            message = "Local traffic estimate is approaching the configured limit"
        else:
            message = "Local traffic estimate is within the configured limit"

        return CheckResult(
            name="traffic",
            status=status,
            message=message,
            details={
                **state,
                "enabled_interfaces": interfaces,
                "per_interface": per_interface,
                "data_file": str(data_file),
                "warning_percent": config.warning_percent,
                "degraded_percent": config.degraded_percent,
                "critical_percent": config.critical_percent,
                "note": config.note,
            },
        )
    except Exception as exc:
        return CheckResult(
            name="traffic",
            status="unknown",
            message="Unable to read local traffic estimate",
            details={"error": str(exc), "note": config.note},
        )
