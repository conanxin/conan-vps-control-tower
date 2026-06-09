from __future__ import annotations

from datetime import UTC, datetime

from app.history.models import HealthEvent, HealthSnapshot
from app.history.store import build_id


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _normalize_status(status: str) -> str:
    return status if status in {"healthy", "warning", "degraded", "critical", "unknown"} else "unknown"


def _status_transition_is_relevant(prev: str, curr: str) -> bool:
    return prev != curr


def _is_recovery(prev: str, curr: str) -> bool:
    return prev in {"warning", "degraded", "critical"} and curr == "healthy"


def _make_event(
    *,
    module: str,
    prev: str,
    curr: str,
    title: str,
    message: str,
) -> HealthEvent:
    prev_status = _normalize_status(prev)
    curr_status = _normalize_status(curr)
    return HealthEvent(
        id=build_id(f"event-{module}"),
        event_type="status_change",
        severity=curr_status,
        title=title,
        message=message,
        module=module,
        previous_status=prev_status,
        current_status=curr_status,
        occurred_at=_now(),
        resolved_at=_now() if _is_recovery(prev_status, curr_status) else None,
        is_recovery=_is_recovery(prev_status, curr_status),
        fingerprint=f"{module}:{prev_status}->{curr_status}",
    )


def build_events(
    current: HealthSnapshot,
    previous: HealthSnapshot | None,
    diagnostics_status: str,
    enabled_domain: bool,
    enabled_tls: bool,
) -> list[HealthEvent]:
    if previous is None:
        return []

    events: list[HealthEvent] = []

    if _status_transition_is_relevant(previous.overall_status, current.overall_status):
        if _is_recovery(previous.overall_status, current.overall_status):
            events.append(
                _make_event(
                    module="overall",
                    prev=previous.overall_status,
                    curr=current.overall_status,
                    title="总体状态已恢复健康",
                    message="整体健康状态从异常恢复为健康。",
                )
            )
        else:
            events.append(
                _make_event(
                    module="overall",
                    prev=previous.overall_status,
                    curr=current.overall_status,
                    title="总体状态变为异常",
                    message="检测到整体健康状态发生异常，建议先检查核心链路。",
                )
            )

    module_pairs = [
        ("proxy_core", previous.proxy_core_status, current.proxy_core_status, "代理核心状态变为严重", "代理核心出现异常"),
        ("proxy_ports", previous.proxy_port_status, current.proxy_port_status, "代理端口出现异常", "代理端口状态出现变化"),
        ("panel", previous.panel_status, current.panel_status, "面板状态变更", "3X-UI 面板状态出现异常"),
        ("traffic", previous.traffic_status, current.traffic_status, "流量风险变更", "本地流量估算风险变化"),
        ("diagnostics", previous.diagnostics_status, current.diagnostics_status, "诊断状态变更", "诊断建议状态出现变化"),
    ]

    for module, prev, curr, title_base, msg in module_pairs:
        if _status_transition_is_relevant(prev, curr):
            title = title_base if curr != "healthy" else "状态已恢复"
            message = msg
            if curr == "critical":
                message = message + "（严重风险）。"
            elif curr in {"warning", "degraded"}:
                message = message + "（警告）。"
            if module == "panel":
                message = message.replace("诊断建议", "面板访问").replace("状态出现变化", "访问异常")
            events.append(_make_event(module=module, prev=prev, curr=curr, title=title, message=message))

    if enabled_domain:
        if previous.domain_status != current.domain_status:
            if current.domain_status != "healthy":
                events.append(
                    _make_event(
                        module="domain_dns",
                        prev=previous.domain_status,
                        curr=current.domain_status,
                        title="域名 / DNS 状态变为异常",
                        message="域名解析可能有问题，请先确认 DNS 解析返回地址是否正常。",
                    )
                )
            else:
                events.append(
                    _make_event(
                        module="domain_dns",
                        prev=previous.domain_status,
                        curr=current.domain_status,
                        title="域名 / DNS 状态已恢复健康",
                        message="域名解析恢复为正常。",
                    )
                )

    if enabled_tls:
        if previous.tls_status != current.tls_status:
            if current.tls_status != "healthy":
                events.append(
                    _make_event(
                        module="tls_certificate",
                        prev=previous.tls_status,
                        curr=current.tls_status,
                        title="TLS 证书状态变为异常",
                        message="TLS 证书状态出现异常，可能影响 TLS 连接。",
                    )
                )
            else:
                events.append(
                    _make_event(
                        module="tls_certificate",
                        prev=previous.tls_status,
                        curr=current.tls_status,
                        title="TLS 证书状态已恢复健康",
                        message="TLS 证书检查恢复为正常。",
                    )
                )

    # Diagnostics API can return status strings; if changed, include an event as context.
    if previous.diagnostics_status != diagnostics_status:
        events.append(
            _make_event(
                module="diagnostics",
                prev=previous.diagnostics_status,
                curr=diagnostics_status,
                title="诊断状态变更",
                message="诊断输出状态发生变化，请查看诊断建议。",
            )
        )

    # Keep only meaningful modules to avoid duplicate noise.
    return events


def dedupe_events(new_events: list[HealthEvent], previous_events: list[HealthEvent]) -> list[HealthEvent]:
    if not new_events:
        return []
    if not previous_events:
        return new_events

    latest_by_fingerprint: dict[str, HealthEvent] = {}
    for item in previous_events:
        prev = latest_by_fingerprint.get(item.fingerprint)
        if prev is None or item.occurred_at > prev.occurred_at:
            latest_by_fingerprint[item.fingerprint] = item

    deduped: list[HealthEvent] = []
    for event in new_events:
        previous = latest_by_fingerprint.get(event.fingerprint)
        if previous is None or previous.current_status != event.current_status:
            deduped.append(event)
    return deduped
