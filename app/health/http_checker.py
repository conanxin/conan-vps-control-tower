from __future__ import annotations

import httpx

from app.config import PanelConfig
from app.models import CheckResult


def check_panel(config: PanelConfig) -> CheckResult:
    try:
        response = httpx.get(config.url, timeout=config.timeout_seconds)
        if response.status_code < 500:
            return CheckResult(
                name="xui_panel",
                status="healthy",
                message="3X-UI panel is reachable",
                details={"url": config.url, "status_code": response.status_code},
            )

        return CheckResult(
            name="xui_panel",
            status="degraded",
            message="3X-UI panel returned a server error",
            details={"url": config.url, "status_code": response.status_code},
        )
    except httpx.TimeoutException:
        return CheckResult(
            name="xui_panel",
            status="critical",
            message="3X-UI panel request timed out",
            details={"url": config.url, "timeout_seconds": config.timeout_seconds},
        )
    except httpx.RequestError as exc:
        return CheckResult(
            name="xui_panel",
            status="critical",
            message="3X-UI panel is not reachable",
            details={"url": config.url, "error": str(exc)},
        )
    except Exception as exc:
        return CheckResult(
            name="xui_panel",
            status="unknown",
            message="Unable to check 3X-UI panel",
            details={"url": config.url, "error": str(exc)},
        )
