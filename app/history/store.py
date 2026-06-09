from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from app.history.models import HealthEvent, HealthSnapshot


def _safe_load(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        return []

    items: list[dict[str, Any]] = []
    for item in payload:
        if isinstance(item, dict):
            items.append(item)
    return items


def _read_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return _safe_load(payload)


def _write_json_atomic(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=str(path.parent), delete=False, suffix=".tmp", encoding="utf-8") as tmp:
        json.dump(payload, tmp, ensure_ascii=False, indent=2)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def load_snapshots(path: str | Path) -> tuple[list[HealthSnapshot], str | None]:
    data_file = Path(path)
    try:
        raw = _read_json(data_file)
        snapshots: list[HealthSnapshot] = [
            HealthSnapshot(**item)
            for item in raw
            if isinstance(item, dict)
            and {"id", "checked_at", "overall_status"}.issubset(item.keys())
        ]
        snapshots.sort(key=lambda item: item.checked_at)
        return snapshots, None
    except Exception as exc:
        return [], f"Unable to read snapshot file: {type(exc).__name__}: {exc}"


def load_events(path: str | Path) -> tuple[list[HealthEvent], str | None]:
    data_file = Path(path)
    try:
        raw = _read_json(data_file)
        events: list[HealthEvent] = [
            HealthEvent(**item)
            for item in raw
            if isinstance(item, dict)
            and {"id", "occurred_at", "module", "current_status", "fingerprint"}.issubset(item.keys())
        ]
        events.sort(key=lambda item: item.occurred_at)
        return events, None
    except Exception as exc:
        return [], f"Unable to read event file: {type(exc).__name__}: {exc}"


def save_snapshots(path: str | Path, snapshots: list[HealthSnapshot]) -> None:
    _write_json_atomic(Path(path), [item.to_dict() for item in snapshots])


def save_events(path: str | Path, events: list[HealthEvent]) -> None:
    _write_json_atomic(Path(path), [item.to_dict() for item in events])


def append_snapshot(path: str | Path, snapshot: HealthSnapshot, max_snapshots: int = 2880) -> None:
    snapshots, _ = load_snapshots(path)
    snapshots.append(snapshot)
    snapshots.sort(key=lambda item: item.checked_at)
    if max_snapshots > 0:
        snapshots = snapshots[-max_snapshots:]
    save_snapshots(path, snapshots)


def append_event(path: str | Path, event: HealthEvent, max_events: int = 500) -> None:
    events, _ = load_events(path)
    events.append(event)
    events.sort(key=lambda item: item.occurred_at)
    if max_events > 0:
        events = events[-max_events:]
    save_events(path, events)


def build_id(prefix: str) -> str:
    from datetime import UTC, datetime

    now = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
    return f"{prefix}-{now}"
