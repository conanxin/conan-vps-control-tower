from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.models import utc_now_iso


class DiagnosticItem(BaseModel):
    diagnosis_id: str
    severity: str
    title: str
    summary: str
    impact: str
    likely_cause: str
    suggested_first_check: str
    read_only_commands: list[str] = Field(default_factory=list)
    related_modules: list[str] = Field(default_factory=list)
    confidence: str = "medium"
    checked_at: str = Field(default_factory=utc_now_iso)


class DiagnosticsResult(BaseModel):
    status: str
    items: list[DiagnosticItem] = Field(default_factory=list)
    summary: str
    checked_at: str = Field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()
