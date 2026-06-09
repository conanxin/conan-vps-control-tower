from __future__ import annotations

import socket
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from app.config import ManagementConfig
from app.management.models import ManagementPanelStatus, disabled_status
from app.models import utc_now_iso


def _is_local_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.hostname in {"127.0.0.1", "localhost"}


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
    base = f"{parsed.scheme}://{parsed.netloc}"
    has_hidden_part = (parsed.path and parsed.path != "/") or parsed.query or parsed.fragment
    return f"{base}/隐藏路径" if has_hidden_part else base


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
        return False, "panel_local_url must use localhost or 127.0.0.1"

    request = Request(url, headers={"User-Agent": "conan-vps-control-tower/management-check"})
    context = ssl._create_unverified_context() if skip_tls_verify else None
    try:
        with urlopen(request, timeout=timeout, context=context) as response:
            return response.status < 500, None
    except HTTPError as exc:
        # Any HTTP response below 500 proves the local protocol endpoint answered.
        if exc.code < 500:
            return True, f"HTTP {exc.code}"
        return False, f"HTTP {exc.code}"
    except URLError as exc:
        return False, type(exc.reason).__name__ if hasattr(exc, "reason") else type(exc).__name__
    except Exception as exc:
        return False, type(exc).__name__


def _detect_panel_protocol(url: str, timeout: float = 3) -> dict[str, object]:
    parsed = urlparse(url)
    configured_scheme = parsed.scheme or "http"
    tcp_reachable = _tcp_reachable(url, timeout)

    configured_ok, configured_error = _probe_url(
        url,
        timeout=timeout,
        skip_tls_verify=configured_scheme == "https",
    )
    if configured_ok:
        recommended = _origin_url(url, configured_scheme)
        return {
            "local_reachable": True,
            "tcp_reachable": tcp_reachable,
            "detected_scheme": configured_scheme,
            "recommended_local_url": recommended,
            "protocol_warning": False,
            "http_ok": True,
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
                "http_ok": False,
                "error": https_error or configured_error,
            }

    return {
        "local_reachable": tcp_reachable,
        "tcp_reachable": tcp_reachable,
        "detected_scheme": configured_scheme if tcp_reachable else "unknown",
        "recommended_local_url": _origin_url(url, configured_scheme),
        "protocol_warning": False,
        "http_ok": False,
        "error": configured_error,
    }


def check_management_panel(config: ManagementConfig) -> ManagementPanelStatus:
    if not config.enabled:
        return disabled_status(
            config.panel_name,
            config.panel_local_url,
            config.panel_public_url,
            public_display_url(config.panel_public_url),
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
            f"检测到{config.panel_name}端口更可能使用 HTTPS，"
            f"建议将 panel_local_url 改为 {recommended_local_url}。"
        )
    elif reachable and detected_scheme == "https":
        status = "healthy"
        message = f"{config.panel_name}本地 HTTPS 协议可达。"
    elif reachable:
        status = "healthy"
        message = f"{config.panel_name}本地入口可达。"
    else:
        status = "warning" if config.panel_local_url else "unknown"
        extra = f"（{error}）" if error else ""
        message = f"{config.panel_name}本地入口暂不可达{extra}；代理服务可能仍在运行，请结合代理核心和端口状态判断。"

    return ManagementPanelStatus(
        enabled=True,
        panel_name=config.panel_name,
        panel_local_url=config.panel_local_url,
        panel_public_url=config.panel_public_url,
        panel_public_display_url=public_display_url(config.panel_public_url),
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
