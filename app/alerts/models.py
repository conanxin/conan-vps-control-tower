from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AlertEvent:
    fingerprint: str
    title: str
    severity: str
    status: str
    module: str
    message: str
    summary: str
    checked_at: str
    is_recovery: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ChannelResult:
    channel: str
    success: bool
    skipped: bool = False
    message: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AlertResult:
    enabled: bool
    evaluated: bool
    sent: bool
    skipped: bool = False
    message: str = ""
    events: list[AlertEvent] = field(default_factory=list)
    channel_results: list[ChannelResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "evaluated": self.evaluated,
            "sent": self.sent,
            "skipped": self.skipped,
            "message": self.message,
            "events": [event.to_dict() for event in self.events],
            "channel_results": [result.to_dict() for result in self.channel_results],
            "errors": self.errors,
        }
