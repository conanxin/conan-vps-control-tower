from __future__ import annotations

import socket

from app.models import CheckResult


def is_port_open(host: str, port: int, timeout_seconds: float = 1.0) -> bool:
    with socket.create_connection((host, port), timeout=timeout_seconds):
        return True


def check_ports(ports: list[int], host: str = "127.0.0.1", timeout_seconds: float = 1.0) -> CheckResult:
    results: list[dict[str, int | bool | str]] = []

    for port in ports:
        try:
            open_state = is_port_open(host, port, timeout_seconds)
            results.append({"host": host, "port": port, "open": open_state})
        except OSError as exc:
            results.append({"host": host, "port": port, "open": False, "error": str(exc)})
        except Exception as exc:
            results.append({"host": host, "port": port, "open": False, "error": str(exc)})

    open_ports = [item for item in results if item.get("open") is True]

    if not ports:
        return CheckResult(
            name="proxy_ports",
            status="unknown",
            message="No proxy ports are configured for checking",
            details={"ports": results},
        )

    if len(open_ports) == len(ports):
        status = "healthy"
        message = "All configured proxy ports are open"
    elif open_ports:
        status = "degraded"
        message = "Some configured proxy ports are closed"
    else:
        status = "critical"
        message = "All configured proxy ports appear closed"

    return CheckResult(name="proxy_ports", status=status, message=message, details={"ports": results})
