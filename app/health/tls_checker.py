from __future__ import annotations

import socket
import ssl
from datetime import UTC, datetime

from app.config import TLSConfig, TLSTargetConfig
from app.models import CheckResult, utc_now_iso


def get_certificate_not_after(target: TLSTargetConfig) -> datetime:
    context = ssl.create_default_context()
    server_name = target.server_name or target.host

    with socket.create_connection((target.host, target.port), timeout=target.timeout_seconds) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=server_name) as tls_socket:
            cert = tls_socket.getpeercert()

    not_after = cert.get("notAfter")
    if not not_after:
        raise ValueError("Certificate notAfter is missing")

    return datetime.fromtimestamp(ssl.cert_time_to_seconds(not_after), UTC)


def evaluate_tls_target(target: TLSTargetConfig, now: datetime | None = None) -> dict[str, object]:
    checked_at = now or datetime.now(UTC)
    not_after = get_certificate_not_after(target)
    days_remaining = (not_after - checked_at).days
    status = "healthy"

    if days_remaining <= target.critical_days:
        status = "critical"
    elif days_remaining <= target.warning_days:
        status = "warning"

    return {
        "host": target.host,
        "port": target.port,
        "server_name": target.server_name,
        "not_after": not_after.isoformat(),
        "days_remaining": days_remaining,
        "warning_days": target.warning_days,
        "critical_days": target.critical_days,
        "status": status,
        "error": None,
    }


def check_tls(config: TLSConfig) -> CheckResult:
    checked_at = utc_now_iso()
    if not config.enabled:
        return CheckResult(
            name="tls_certificate",
            status="unknown",
            message="TLS check is not configured",
            checked_at=checked_at,
            ignored=True,
            details={"enabled": False, "targets": [], "errors": [], "checked_at": checked_at},
        )

    target_results: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []

    for target in config.targets:
        try:
            target_results.append(evaluate_tls_target(target))
        except Exception as exc:
            error_result = {
                "host": target.host,
                "port": target.port,
                "server_name": target.server_name,
                "not_after": None,
                "days_remaining": None,
                "warning_days": target.warning_days,
                "critical_days": target.critical_days,
                "status": "critical",
                "error": str(exc),
            }
            target_results.append(error_result)
            errors.append(error_result)

    statuses = [str(item["status"]) for item in target_results]
    if "critical" in statuses:
        status = "critical"
        message = "TLS certificate check failed or a certificate is near expiry"
    elif "warning" in statuses:
        status = "warning"
        message = "TLS certificate is approaching expiry"
    else:
        status = "healthy"
        message = "TLS certificates look valid"

    return CheckResult(
        name="tls_certificate",
        status=status,
        message=message,
        checked_at=checked_at,
        details={"enabled": True, "targets": target_results, "errors": errors, "checked_at": checked_at},
    )
