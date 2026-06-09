from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

import httpx

from app.config import PanelConfig
from app.models import CheckResult

REACHABLE_STATUS_CODES = {200, 301, 302, 307, 401, 403}
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _is_local_url(url: str) -> bool:
    try:
        host = urlsplit(url).hostname
    except ValueError:
        return False
    return host in LOCAL_HOSTS


def mask_panel_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return "<invalid-url>"
    if parsed.path and parsed.path not in {"", "/"}:
        return urlunsplit((parsed.scheme, parsed.netloc, "/<hidden>", "", ""))
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def _details(url: str, **extra: object) -> dict[str, object]:
    parsed = urlsplit(url)
    data: dict[str, object] = {
        "url": mask_panel_url(url),
        "scheme": parsed.scheme,
        "host": parsed.hostname or "",
        "port": parsed.port,
        "hidden_path_configured": bool(parsed.path and parsed.path not in {"", "/"}),
    }
    data.update(extra)
    return data


def check_panel(config: PanelConfig) -> CheckResult:
    try:
        local_https = config.url.lower().startswith("https://") and _is_local_url(config.url)
        response = httpx.get(config.url, timeout=config.timeout_seconds, verify=not local_https, follow_redirects=False)
        if response.status_code in REACHABLE_STATUS_CODES:
            return CheckResult(
                name="xui_panel",
                status="healthy",
                message="3X-UI panel is reachable",
                details=_details(config.url, status_code=response.status_code, tls_verify_skipped=local_https),
            )

        if response.status_code == 404:
            return CheckResult(
                name="xui_panel",
                status="warning",
                message="3X-UI panel responded with 404; panel protocol is reachable but the configured path may be wrong",
                details=_details(config.url, status_code=response.status_code, tls_verify_skipped=local_https),
            )

        return CheckResult(
            name="xui_panel",
            status="degraded",
            message="3X-UI panel returned a server error",
            details=_details(config.url, status_code=response.status_code, tls_verify_skipped=local_https),
        )
    except httpx.TimeoutException:
        return CheckResult(
            name="xui_panel",
            status="critical",
            message="3X-UI panel request timed out",
            details=_details(config.url, timeout_seconds=config.timeout_seconds),
        )
    except httpx.RequestError as exc:
        return CheckResult(
            name="xui_panel",
            status="critical",
            message="3X-UI panel is not reachable",
            details=_details(config.url, error=str(exc)),
        )
    except Exception as exc:
        return CheckResult(
            name="xui_panel",
            status="unknown",
            message="Unable to check 3X-UI panel",
            details=_details(config.url, error=str(exc)),
        )
