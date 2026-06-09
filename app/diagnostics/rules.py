from __future__ import annotations

from app.diagnostics import commands
from app.diagnostics.models import DiagnosticItem
from app.models import CheckResult, HealthResponse, utc_now_iso

ACTIONABLE = {"warning", "degraded", "critical"}


def by_name(health: HealthResponse) -> dict[str, CheckResult]:
    return {check.name: check for check in health.checks}


def make_item(
    diagnosis_id: str,
    severity: str,
    title: str,
    summary: str,
    impact: str,
    likely_cause: str,
    suggested_first_check: str,
    read_only_commands: list[str],
    related_modules: list[str],
    confidence: str = "medium",
) -> DiagnosticItem:
    return DiagnosticItem(
        diagnosis_id=diagnosis_id,
        severity=severity,
        title=title,
        summary=summary,
        impact=impact,
        likely_cause=likely_cause,
        suggested_first_check=suggested_first_check,
        read_only_commands=read_only_commands,
        related_modules=related_modules,
        confidence=confidence,
        checked_at=utc_now_iso(),
    )


def multiple_critical(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    critical = [name for name, check in checks.items() if not check.ignored and check.status == "critical"]
    if len(critical) < 2:
        return None
    return make_item(
        "multiple_critical",
        "critical",
        "Multiple critical modules detected",
        "Several key checks are critical at the same time.",
        "The VPS or proxy node may be broadly unavailable.",
        "System-level outage, proxy process failure, or network dependency failure.",
        "First confirm the VPS is responsive and system resources are not exhausted.",
        [commands.check_system_resources_command, commands.check_socket_summary_command],
        critical,
        "high",
    )


def proxy_core_critical(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("proxy_core")
    if not check or check.status not in {"critical", "degraded"}:
        return None
    return make_item(
        "proxy_core_critical",
        check.status,
        "Proxy core process risk",
        check.message,
        "Client proxy traffic is likely unavailable or unstable.",
        "Proxy core process may not be running, crashed, or process name config may be wrong.",
        "Inspect xray / 3x-ui / sing-box process and service status.",
        [commands.check_services_command, commands.check_proxy_processes_command],
        ["proxy_core"],
        "high",
    )


def proxy_port_not_listening(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("proxy_ports")
    if not check or check.status not in {"critical", "degraded"}:
        return None
    return make_item(
        "proxy_port_not_listening",
        check.status,
        "Proxy port is not fully listening",
        check.message,
        "Clients may fail to connect to the proxy inbound port.",
        "Proxy service may be down, inbound config may differ, or the checked port may be wrong.",
        "Check local listening state for the proxy inbound port.",
        [commands.check_listening_ports_command],
        ["proxy_ports"],
        "high",
    )


def panel_down_but_proxy_may_work(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    panel = checks.get("xui_panel")
    core = checks.get("proxy_core")
    ports = checks.get("proxy_ports")
    if not panel or panel.status not in ACTIONABLE:
        return None
    if not core or not ports or core.status != "healthy" or ports.status != "healthy":
        return None
    return make_item(
        "panel_down_but_proxy_may_work",
        panel.status,
        "3X-UI panel is abnormal but proxy may still work",
        f"{panel.message} 面板异常不一定影响代理转发。",
        "请先确认 3X-UI 面板端口。",
        "面板进程、面板端口、协议或隐藏路径配置可能不正常。",
        "建议先通过管理入口检查 3X-UI 面板 HTTPS 响应和本地监听端口，必要时再更新面板入口配置。",
        commands.panel_commands(panel),
        ["xui_panel", "proxy_core", "proxy_ports"],
        "medium",
    )


def system_resource_warning(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("vps_system")
    if not check or check.status not in ACTIONABLE:
        return None
    return make_item(
        "system_resource_warning",
        check.status,
        "VPS resource pressure detected",
        check.message,
        "High resource usage may affect proxy stability.",
        "Disk, RAM, or load may be close to configured limits.",
        "Check load, memory, and disk usage.",
        ["uptime", "free -h", commands.check_disk_command],
        ["vps_system"],
        "medium",
    )


def domain_resolution_failed(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("domain_dns")
    if not check or check.ignored or check.status != "critical":
        return None
    return make_item(
        "domain_resolution_failed",
        "critical",
        "Domain resolution failed",
        check.message,
        "Clients using a domain may be unable to find the VPS.",
        "DNS provider, record configuration, or resolver path may be failing.",
        "Check DNS resolution from the VPS with Python socket.",
        [commands.check_domain_command],
        ["domain_dns"],
        "high",
    )


def domain_expected_ip_mismatch(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("domain_dns")
    if not check or check.ignored or check.status not in {"warning", "degraded"}:
        return None
    return make_item(
        "domain_expected_ip_mismatch",
        check.status,
        "Domain resolved to unexpected address",
        check.message,
        "Clients may connect to a non-expected endpoint.",
        "DNS record, CDN setting, or expected IP config may not match.",
        "Check DNS provider / CDN / A record and compare socket resolution.",
        [commands.check_domain_command],
        ["domain_dns"],
        "medium",
    )


def tls_expiring(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("tls_certificate")
    if not check or check.ignored or check.status not in {"warning", "degraded"}:
        return None
    return make_item(
        "tls_expiring",
        check.status,
        "TLS certificate is approaching expiry",
        check.message,
        "TLS clients may fail after certificate expiry.",
        "Certificate renewal may be due soon.",
        "Check certificate notAfter date.",
        [commands.check_tls_command],
        ["tls_certificate"],
        "medium",
    )


def tls_handshake_failed(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("tls_certificate")
    if not check or check.ignored or check.status != "critical":
        return None
    return make_item(
        "tls_handshake_failed",
        "critical",
        "TLS check failed",
        check.message,
        "TLS clients may fail to connect.",
        "Certificate, SNI, port, or inbound TLS settings may be wrong.",
        "Check certificate metadata, SNI, port, and proxy inbound TLS settings.",
        [commands.check_tls_command, commands.check_listening_ports_command],
        ["tls_certificate"],
        "high",
    )


def traffic_near_limit(checks: dict[str, CheckResult]) -> DiagnosticItem | None:
    check = checks.get("traffic")
    if not check or check.status not in ACTIONABLE:
        return None
    return make_item(
        "traffic_near_limit",
        check.status,
        "Local traffic estimate is near limit",
        check.message,
        "Monthly traffic may approach provider limits; future service could be throttled or interrupted.",
        "Local estimate indicates high usage. Provider billing panel remains authoritative.",
        "Check provider panel for authoritative billing data and inspect local interface counters.",
        [commands.check_proc_net_dev_command],
        ["traffic"],
        "medium",
    )


def all_healthy(health: HealthResponse) -> DiagnosticItem:
    ignored = [check.name for check in health.checks if check.ignored]
    suffix = f" Not configured: {', '.join(ignored)}." if ignored else ""
    return make_item(
        "all_healthy",
        "healthy",
        "No active diagnostic issues detected",
        f"No warning, degraded, or critical checks are active.{suffix}",
        "No immediate proxy impact is visible from configured checks.",
        "Configured checks are healthy.",
        "Keep monitoring the Dashboard.",
        [],
        [],
        "medium",
    )


RULES = [
    multiple_critical,
    proxy_core_critical,
    proxy_port_not_listening,
    panel_down_but_proxy_may_work,
    system_resource_warning,
    domain_resolution_failed,
    domain_expected_ip_mismatch,
    tls_expiring,
    tls_handshake_failed,
    traffic_near_limit,
]
