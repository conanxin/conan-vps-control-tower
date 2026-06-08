from __future__ import annotations

import subprocess

import psutil

from app.config import ProxyConfig
from app.models import CheckResult


def _process_matches(process_name: str, candidates: list[str]) -> bool:
    lowered_name = process_name.lower()
    return any(candidate.lower() in lowered_name for candidate in candidates)


def check_proxy_processes(config: ProxyConfig) -> CheckResult:
    try:
        matches: list[dict[str, str | int | None]] = []
        for process in psutil.process_iter(["pid", "name", "cmdline"]):
            info = process.info
            process_text = " ".join(
                [str(info.get("name") or ""), *[str(part) for part in info.get("cmdline") or []]]
            )
            if _process_matches(process_text, config.process_names):
                matches.append({"pid": info.get("pid"), "name": info.get("name")})

        if matches:
            return CheckResult(
                name="proxy_core",
                status="healthy",
                message="Proxy core process is running",
                details={"matched_processes": matches, "expected_names": config.process_names},
            )

        return CheckResult(
            name="proxy_core",
            status="critical",
            message="No expected proxy core process was found",
            details={"expected_names": config.process_names},
        )
    except Exception as exc:
        return CheckResult(
            name="proxy_core",
            status="unknown",
            message="Unable to inspect proxy core process",
            details={"error": str(exc)},
        )


def check_proxy_services(config: ProxyConfig) -> CheckResult:
    service_results: list[dict[str, str]] = []
    saw_systemctl = False

    for service in config.service_names:
        try:
            completed = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
            saw_systemctl = True
            service_results.append(
                {
                    "service": service,
                    "state": completed.stdout.strip() or completed.stderr.strip() or "unknown",
                }
            )
        except FileNotFoundError:
            return CheckResult(
                name="proxy_services",
                status="unknown",
                message="systemctl is not available on this platform",
                details={"expected_services": config.service_names},
            )
        except Exception as exc:
            service_results.append({"service": service, "state": f"unknown: {exc}"})

    active = [item for item in service_results if item["state"] == "active"]
    if active:
        return CheckResult(
            name="proxy_services",
            status="healthy",
            message="At least one expected proxy service is active",
            details={"services": service_results},
        )

    return CheckResult(
        name="proxy_services",
        status="unknown" if saw_systemctl else "unknown",
        message="No expected proxy service is confirmed active",
        details={"services": service_results},
    )
