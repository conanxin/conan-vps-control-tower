from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.alerts.channels.email import send_email
from app.alerts.channels.telegram import send_telegram
from app.alerts.models import AlertEvent, AlertResult, ChannelResult
from app.alerts.severity import is_at_least
from app.alerts.state_store import AlertStateStore
from app.config import AlertsConfig
from app.models import CheckResult, HealthResponse, utc_now_iso


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


class AlertManager:
    def __init__(self, config: AlertsConfig):
        self.config = config
        self.store = AlertStateStore(config.state_file)

    def status(self) -> dict[str, Any]:
        return {
            "alerts": {
                "enabled": self.config.enabled,
                "min_severity": self.config.min_severity,
                "cooldown_seconds": self.config.cooldown_seconds,
                "send_recovery": self.config.send_recovery,
            },
            "telegram": {"enabled": self.config.telegram.enabled},
            "email": {"enabled": self.config.email.enabled},
            "state": self.store.summary(),
        }

    def evaluate(self, health: HealthResponse) -> AlertResult:
        if not self.config.enabled:
            return AlertResult(enabled=False, evaluated=False, sent=False, skipped=True, message="Alerts disabled")
        try:
            state = self.store.load()
            candidates = self._build_candidates(health)
            recoveries = self._build_recoveries(health, state)
            events = candidates + recoveries
            if not events:
                self._update_state(state, health, [])
                self.store.save(state)
                return AlertResult(enabled=True, evaluated=True, sent=False, skipped=True, message="No alert candidates")

            channel_results: list[ChannelResult] = []
            sent_events: list[AlertEvent] = []
            now = datetime.now(UTC)
            for event in events:
                if not event.is_recovery and not self._can_send(event, state, now):
                    continue
                results = self._send(event)
                channel_results.extend(results)
                if any(result.success for result in results):
                    sent_events.append(event)
                    state.setdefault("active_alerts", {})[event.fingerprint] = event.to_dict()
                    state["last_sent_at"] = utc_now_iso()
                    state["last_fingerprint"] = event.fingerprint
                    state["last_status"] = health.overall_status
                elif event.is_recovery:
                    state.get("active_alerts", {}).pop(event.fingerprint, None)

            self._update_state(state, health, candidates)
            self.store.save(state)
            return AlertResult(
                enabled=True,
                evaluated=True,
                sent=bool(sent_events),
                skipped=not bool(sent_events),
                message="Alert evaluation complete",
                events=sent_events,
                channel_results=channel_results,
            )
        except Exception as exc:
            return AlertResult(enabled=True, evaluated=False, sent=False, errors=[f"Alert evaluation failed: {type(exc).__name__}"])

    def send_test(self) -> AlertResult:
        if not self.config.enabled:
            return AlertResult(enabled=False, evaluated=False, sent=False, skipped=True, message="Alerts disabled; enable alerts first")
        event = AlertEvent(
            fingerprint="test-alert",
            title="Conan VPS Control Tower test alert",
            severity="warning",
            status="test",
            module="alerting",
            message="This is a test notification, not a failure.",
            summary="Test alert requested from local dashboard.",
            checked_at=utc_now_iso(),
        )
        results = self._send(event)
        return AlertResult(
            enabled=True,
            evaluated=True,
            sent=any(result.success for result in results),
            skipped=not any(result.success for result in results),
            message="Test alert evaluated",
            events=[event],
            channel_results=results,
        )

    def _build_candidates(self, health: HealthResponse) -> list[AlertEvent]:
        events = []
        for check in health.checks:
            if check.ignored or not is_at_least(check.status, self.config.min_severity):
                continue
            events.append(self._event_from_check(check, health))
        if not events and is_at_least(health.overall_status, self.config.min_severity):
            events.append(
                AlertEvent(
                    fingerprint=f"overall:{health.overall_status}",
                    title="Proxy risk detected",
                    severity=health.overall_status,
                    status=health.overall_status,
                    module="overall",
                    message=health.readable_summary,
                    summary=health.readable_summary,
                    checked_at=health.checked_at,
                )
            )
        return events

    def _build_recoveries(self, health: HealthResponse, state: dict[str, Any]) -> list[AlertEvent]:
        if not self.config.send_recovery:
            return []
        active = state.get("active_alerts", {})
        if not isinstance(active, dict):
            return []
        current = {event.fingerprint for event in self._build_candidates(health)}
        recoveries = []
        for fingerprint, stored in list(active.items()):
            if fingerprint in current:
                continue
            recoveries.append(
                AlertEvent(
                    fingerprint=fingerprint,
                    title="Proxy risk recovered",
                    severity="healthy",
                    status=health.overall_status,
                    module=str(stored.get("module", "unknown")),
                    message="Previously active alert recovered.",
                    summary=health.readable_summary,
                    checked_at=health.checked_at,
                    is_recovery=True,
                )
            )
        return recoveries

    def _event_from_check(self, check: CheckResult, health: HealthResponse) -> AlertEvent:
        return AlertEvent(
            fingerprint=f"{check.name}:{check.status}",
            title="Proxy risk detected",
            severity=check.status,
            status=health.overall_status,
            module=check.name,
            message=check.message,
            summary=health.readable_summary,
            checked_at=check.checked_at,
        )

    def _can_send(self, event: AlertEvent, state: dict[str, Any], now: datetime) -> bool:
        active = state.get("active_alerts", {})
        stored = active.get(event.fingerprint) if isinstance(active, dict) else None
        if not stored:
            return True
        last_sent = parse_time(state.get("last_sent_at"))
        if not last_sent:
            return True
        return (now - last_sent).total_seconds() >= self.config.cooldown_seconds

    def _send(self, event: AlertEvent) -> list[ChannelResult]:
        return [
            send_telegram(event, self.config.telegram),
            send_email(event, self.config.email),
        ]

    def _update_state(self, state: dict[str, Any], health: HealthResponse, candidates: list[AlertEvent]) -> None:
        active = state.setdefault("active_alerts", {})
        if isinstance(active, dict):
            current = {event.fingerprint for event in candidates}
            for fingerprint in list(active.keys()):
                if fingerprint not in current:
                    active.pop(fingerprint, None)
            for event in candidates:
                active.setdefault(event.fingerprint, event.to_dict())
        state["last_status"] = health.overall_status
