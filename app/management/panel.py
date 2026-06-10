from __future__ import annotations

import socket
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import ssl
from urllib.error import HTTPError, URLError

from app.config import ManagementConfig
from app.management.models import ManagementPanelStatus, disabled_status
from app.models import utc_now_iso


def _is_local_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.hostname in {"127.0.0.1", "localhost", "::1"}


def _origin_url(url: str, scheme: str) -> str:
    parsed = urlparse(url)
    host = parsed.hostname or "127.0.0.1"
    port = f":{parsed.port}" if parsed.port else ""
    return f"{scheme}://{host}{port}"


def public_display_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return ""
    base = parsed.netloc
    has_hidden = bool(parsed.path and parsed.path not in {"", "/"}) or bool(parsed.query or parsed.fragment)
    if not has_hidden:
        return base
    return f"{base} / 已配置隐藏路径"


def _tcp_reachable(url: str, timeout: float = 3) -> bool:
    parsed = urlparse(url)
    if not parsed.hostname or not parsed.port:
        return False
    try:
        with socket.create_connection((parsed.hostname, parsed.port), timeout=timeout):
            return True
    except OSError:
        return False


def _probe_url(url: str, timeout: float = 3, skip_tls_verify: bool = False) -> tuple[bool, str | None]:
    if not _is_local_http_url(url):
        return False, "panel_local_url 需要本地 HTTP/HTTPS 地址"

    request = Request(url, headers={"User-Agent": "conan-vps-control-tower/management-check"})
    context = ssl._create_unverified_context() if skip_tls_verify else None
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            code = response.status
            return (200 <= code < 500), f"HTTP {code}"
    except HTTPError as exc:
        # 4xx 表示端点可达，仅 5xx 视为错误。
        return exc.code < 500, f"HTTP {exc.code}"
    except URLError as exc:
        return False, str(getattr(exc, "reason", type(exc).__name__))
    except Exception as exc:
        return False, type(exc).__name__


def _detect_panel_protocol(url: str, timeout: float = 3) -> dict[str, object]:
    parsed = urlparse(url)
    configured_scheme = parsed.scheme or "http"
    tcp_reachable = _tcp_reachable(url, timeout)

    configured_ok, configured_error = _probe_url(
        url,
        timeout=timeout,
        skip_tls_verify=(configured_scheme == "https"),
    )
    if configured_ok:
        return {
            "local_reachable": True,
            "tcp_reachable": tcp_reachable,
            "detected_scheme": configured_scheme,
            "recommended_local_url": _origin_url(url, configured_scheme),
            "protocol_warning": False,
            "error": configured_error,
        }

    if configured_scheme == "http" and tcp_reachable:
        https_url = _origin_url(url, "https")
        https_ok, https_error = _probe_url(https_url, timeout=timeout, skip_tls_verify=True)
        if https_ok:
            return {
                "local_reachable": True,
                "tcp_reachable": True,
                "detected_scheme": "https",
                "recommended_local_url": https_url,
                "protocol_warning": True,
                "error": https_error,
            }

    return {
        "local_reachable": tcp_reachable,
        "tcp_reachable": tcp_reachable,
        "detected_scheme": configured_scheme if tcp_reachable else "unknown",
        "recommended_local_url": _origin_url(url, "https" if tcp_reachable else (configured_scheme or "http")),
        "protocol_warning": False,
        "error": configured_error,
    }


def check_management_panel(config: ManagementConfig) -> ManagementPanelStatus:
    public_url_display = config.panel_public_display_url or public_display_url(config.panel_public_url)

    if not config.enabled:
        return disabled_status(
            config.panel_name,
            config.panel_local_url,
            config.panel_public_url,
            public_url_display,
            config.access_note,
            config.readonly_note,
            config.open_in_new_tab,
        )

    detection = _detect_panel_protocol(config.panel_local_url)
    reachable = bool(detection["local_reachable"])
    tcp_reachable = bool(detection["tcp_reachable"])
    detected_scheme = str(detection["detected_scheme"])
    recommended_local_url = str(detection["recommended_local_url"])
    protocol_warning = bool(detection["protocol_warning"])
    error = detection.get("error")

    if reachable and protocol_warning:
        status = "warning"
        message = (
            f"检测到面板端口更可能使用 HTTPS，建议将 panel_local_url 改为 {recommended_local_url}。"
        )
    elif reachable and detected_scheme == "https":
        status = "healthy"
        message = "管理面板本地入口可达。"
    elif reachable:
        status = "healthy"
        message = "管理面板本地入口可达。"
    else:
        status = "warning" if config.panel_local_url else "unknown"
        suffix = f"（{error}）" if error else ""
        message = f"管理面板本地入口暂不可达{suffix}，但不代表代理一定不可用。"

    return ManagementPanelStatus(
        enabled=True,
        panel_name=config.panel_name,
        panel_local_url=config.panel_local_url,
        panel_public_url=config.panel_public_url,
        panel_public_display_url=public_url_display,
        local_reachable=reachable,
        status=status,
        message=message,
        access_note=config.access_note,
        readonly_note=config.readonly_note,
        open_in_new_tab=config.open_in_new_tab,
        checked_at=utc_now_iso(),
        detected_scheme=detected_scheme,
        recommended_local_url=recommended_local_url,
        protocol_warning=protocol_warning,
        tcp_reachable=tcp_reachable,
    )
