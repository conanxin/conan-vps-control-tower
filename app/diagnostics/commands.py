from __future__ import annotations

from app.models import CheckResult

check_services_command = "systemctl status SERVICE_NAME --no-pager"
check_proxy_processes_command = "ps -eo pid,comm,args,%cpu,%mem --sort=-%mem | grep -Ei 'x-ui|3x-ui|xray|sing-box|v2ray' | grep -v grep || true"
check_listening_ports_command = "ss -lntup | grep -E ':YOUR_PROXY_PORT\\b' || true"
check_panel_http_command = "请先确认 3X-UI 面板端口。"
check_panel_port_command = "请先确认 3X-UI 面板端口。"
check_system_resources_command = "uptime && free -h && df -h"
check_disk_command = "df -h"
check_network_interfaces_command = "ip addr show"
check_tls_command = """python - <<'PY'
import socket, ssl
host = "YOUR_DOMAIN"
ctx = ssl.create_default_context()
with socket.create_connection((host, 443), timeout=5) as sock:
    with ctx.wrap_socket(sock, server_hostname=host) as ssock:
        print(ssock.getpeercert().get("notAfter"))
PY"""
check_domain_command = """python - <<'PY'
import socket
print(socket.getaddrinfo("YOUR_DOMAIN", None))
PY"""
check_proc_net_dev_command = "cat /proc/net/dev"
check_socket_summary_command = "ss -lntup"


def panel_commands(check: CheckResult | None) -> list[str]:
    if not check:
        return [check_panel_http_command]

    details = check.details or {}
    port = details.get("port")
    scheme = details.get("scheme") or "https"
    hidden = details.get("hidden_path_configured")
    if not isinstance(port, int):
        return [check_panel_http_command]

    path = "/<hidden>" if hidden else ""
    curl_flags = "-k -I" if scheme == "https" else "-I"
    return [
        f"curl {curl_flags} --max-time 3 {scheme}://127.0.0.1:{port}{path} || true",
        f"ss -lntup | grep -E ':{port}\\b' || true",
    ]

READ_ONLY_COMMANDS = [
    check_services_command,
    check_proxy_processes_command,
    check_listening_ports_command,
    check_panel_http_command,
    check_panel_port_command,
    check_system_resources_command,
    check_disk_command,
    check_network_interfaces_command,
    check_tls_command,
    check_domain_command,
    check_proc_net_dev_command,
    check_socket_summary_command,
]

DANGEROUS_WORDS = [
    " restart ",
    " stop ",
    " start ",
    " enable ",
    " disable ",
    " rm ",
    " mv ",
    " chmod ",
    " chown ",
    " ufw ",
    " iptables ",
    " nft ",
]
