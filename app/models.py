from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

HealthStatus = Literal["healthy", "warning", "degraded", "critical", "unknown"]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


class CheckResult(BaseModel):
    name: str
    status: HealthStatus
    message: str
    checked_at: str = Field(default_factory=utc_now_iso)
    details: dict[str, Any] = Field(default_factory=dict)
    ignored: bool = False


class HealthResponse(BaseModel):
    overall_status: HealthStatus
    readable_summary: str
    risk_summary: list[str]
    checked_at: str = Field(default_factory=utc_now_iso)
    checks: list[CheckResult]
    history_recording: dict[str, Any] | None = None


class MetaResponse(BaseModel):
    app_name: str
    version: str
    ui_language: str
    configured_host: str
    configured_port: int
    local_only: bool
    access_hint: str
    public_entry: str | None = None
    external_access_mode: str | None = None
    direct_public_bind: bool = False
    access_protection: str | None = None
    history_enabled: bool
    event_log: bool
    alert_config_check: bool
    management_entry: bool
