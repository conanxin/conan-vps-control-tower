from __future__ import annotations

import socket
from contextlib import contextmanager
from typing import Iterator

from app.config import DomainConfig
from app.models import CheckResult, utc_now_iso


@contextmanager
def socket_timeout(timeout_seconds: float) -> Iterator[None]:
    previous = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout_seconds)
    try:
        yield
    finally:
        socket.setdefaulttimeout(previous)


def resolve_domain(name: str, timeout_seconds: float) -> list[str]:
    with socket_timeout(timeout_seconds):
        addrinfo = socket.getaddrinfo(name, None, type=socket.SOCK_STREAM)
    return sorted({item[4][0] for item in addrinfo})


def check_domain(config: DomainConfig) -> CheckResult:
    checked_at = utc_now_iso()
    if not config.enabled:
        return CheckResult(
            name="domain_dns",
            status="unknown",
            message="Domain check is not configured",
            checked_at=checked_at,
            ignored=True,
            details={
                "enabled": False,
                "names": config.names,
                "expected_ips": config.expected_ips,
                "resolved_ips": {},
                "mismatches": [],
                "errors": {},
                "checked_at": checked_at,
            },
        )

    resolved_ips: dict[str, list[str]] = {}
    mismatches: list[dict[str, list[str] | str]] = []
    errors: dict[str, str] = {}

    for name in config.names:
        try:
            resolved = resolve_domain(name, config.timeout_seconds)
            resolved_ips[name] = resolved
            if config.expected_ips and not set(resolved).intersection(config.expected_ips):
                mismatches.append({"name": name, "resolved_ips": resolved})
        except Exception as exc:
            errors[name] = str(exc)

    if errors:
        status = "critical"
        message = "DNS resolution failed for one or more domains"
    elif mismatches:
        status = "warning"
        message = "Domain resolves, but results do not match expected IPs"
    else:
        status = "healthy"
        message = "Domain resolves successfully"

    return CheckResult(
        name="domain_dns",
        status=status,
        message=message,
        checked_at=checked_at,
        details={
            "enabled": True,
            "names": config.names,
            "resolved_ips": resolved_ips,
            "expected_ips": config.expected_ips,
            "mismatches": mismatches,
            "errors": errors,
            "checked_at": checked_at,
        },
    )
