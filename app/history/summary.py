from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.history.models import HealthEvent, HealthSnapshot, HistorySummary

STATUS_SCORE = {
    "healthy": 0,
    "unknown": 1,
    "warning": 2,
    "degraded": 3,
    "critical": 4,
}


def _percent(current: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((current / total) * 100.0, 2)


def _within_window(item: HealthSnapshot, cutoff_iso: str) -> bool:
    return item.checked_at >= cutoff_iso


def _label_uptime(snapshot_count: int) -> str:
    if snapshot_count == 0:
        return "未记录到可用于统计的快照"
    if snapshot_count == 1:
        return "采样样本较少，建议继续观察"
    return f"共采样 {snapshot_count} 次"


def build_summary(
    snapshots: list[HealthSnapshot],
    events: list[HealthEvent],
    window_hours: int,
) -> HistorySummary:
    now = datetime.now(UTC)
    cutoff = now - timedelta(hours=max(1, window_hours))
    cutoff_iso = cutoff.isoformat()

    recent_sn = [item for item in snapshots if _within_window(item, cutoff_iso)]
    recent_events = [item for item in events if item.occurred_at >= cutoff_iso]

    if not recent_sn:
        return HistorySummary(
            status="unknown",
            window_hours=window_hours,
            snapshot_count=0,
            event_count=0,
            latest_status="unknown",
            worst_status="unknown",
            healthy_ratio=0.0,
            warning_count=0,
            degraded_count=0,
            critical_count=0,
            last_event=None,
            last_problem_at=None,
            last_recovery_at=None,
            uptime_label=_label_uptime(0),
            summary=f"最近{window_hours}小时内无历史快照，等待刷新后自动记录。",
        )

    latest = recent_sn[-1]
    snapshot_count = len(recent_sn)
    warning_count = sum(1 for item in recent_sn if item.overall_status == "warning")
    degraded_count = sum(1 for item in recent_sn if item.overall_status == "degraded")
    critical_count = sum(1 for item in recent_sn if item.overall_status == "critical")
    healthy_count = sum(1 for item in recent_sn if item.overall_status == "healthy")
    healthy_ratio = _percent(healthy_count, snapshot_count)

    worst = max(recent_sn, key=lambda item: STATUS_SCORE.get(item.overall_status, 1)).overall_status
    latest_problem = next(
        (event for event in sorted(recent_events, key=lambda item: item.occurred_at, reverse=True) if not event.is_recovery),
        None,
    )
    latest_recovery = next(
        (event for event in sorted(recent_events, key=lambda item: item.occurred_at, reverse=True) if event.is_recovery),
        None,
    )

    event_count = len(recent_events)
    if critical_count == 0 and degraded_count == 0 and warning_count == 0:
        summary = f"最近{window_hours}小时内未发现活跃异常，当前状态{latest.overall_status}。"
        status = "healthy"
    else:
        latest_problem_text = latest_problem.module if latest_problem else "unknown"
        summary = (
            f"最近{window_hours}小时出现{warning_count + degraded_count + critical_count}次告警，"
            f"最近异常来自 {latest_problem_text}。"
        )
        status = worst

    return HistorySummary(
        status=status,
        window_hours=window_hours,
        snapshot_count=snapshot_count,
        event_count=event_count,
        latest_status=latest.overall_status,
        worst_status=worst,
        healthy_ratio=healthy_ratio,
        warning_count=warning_count,
        degraded_count=degraded_count,
        critical_count=critical_count,
        last_event=recent_events[-1].title if recent_events else None,
        last_problem_at=latest_problem.occurred_at if latest_problem else None,
        last_recovery_at=latest_recovery.occurred_at if latest_recovery else None,
        uptime_label=_label_uptime(snapshot_count),
        summary=summary,
    )
