from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import socket

from app.config import ManagementConfig
from app.management.models import ManagementPanelStatus, disabled_status
from app.models import utc_now_iso


def _is_local_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.hostname in {"127.0.0.1", "localhost"}


def _tcp_reachable(url: str, timeout: float = 3) -> bool:
    parsed = urlparse(url)
    if not parsed.hostname or not parsed.port:
        return False
    try:
        with socket.create_connection((parsed.hostname, parsed.port), timeout=timeout):
            return True
    except OSError:
        return False


def _local_panel_reachable(url: str, timeout: float = 3) -> tuple[bool, bool, str | None]:
    if not _is_local_http_url(url):
        return False, False, "panel_local_url must use localhost or 127.0.0.1"

    request = Request(url, headers={"User-Agent": "conan-vps-control-tower/management-check"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status < 500, response.status < 500, None
    except HTTPError as exc:
        # 3X-UI may answer with redirects/auth-related status codes; that still proves the local entry exists.
        if exc.code < 500:
            return True, True, None
        return _tcp_reachable(url, timeout), False, f"HTTP {exc.code}"
    except URLError as exc:
        error = type(exc.reason).__name__ if hasattr(exc, "reason") else type(exc).__name__
        return _tcp_reachable(url, timeout), False, error
    except Exception as exc:
        return _tcp_reachable(url, timeout), False, type(exc).__name__


def check_management_panel(config: ManagementConfig) -> ManagementPanelStatus:
    if not config.enabled:
        return disabled_status(
            config.panel_name,
            config.panel_local_url,
            config.panel_public_url,
            config.access_note,
            config.readonly_note,
            config.open_in_new_tab,
        )

    reachable, http_ok, error = _local_panel_reachable(config.panel_local_url)
    if reachable and http_ok:
        status = "healthy"
        message = f"{config.panel_name}本地入口可达。"
    elif reachable:
        status = "warning"
        extra = f"（HTTP 检查未完全通过：{error}）" if error else ""
        message = f"{config.panel_name}本地端口可连接{extra}；请确认面板 URL 协议是否为 http 或 https。"
    else:
        status = "warning" if config.panel_local_url else "unknown"
        extra = f"（{error}）" if error else ""
        message = f"{config.panel_name}本地入口暂不可达{extra}；代理服务可能仍在运行，请结合代理核心和端口状态判断。"

    return ManagementPanelStatus(
        enabled=True,
        panel_name=config.panel_name,
        panel_local_url=config.panel_local_url,
        panel_public_url=config.panel_public_url,
        local_reachable=reachable,
        status=status,
        message=message,
        access_note=config.access_note,
        readonly_note=config.readonly_note,
        open_in_new_tab=config.open_in_new_tab,
        checked_at=utc_now_iso(),
    )
