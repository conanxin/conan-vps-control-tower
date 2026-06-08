from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def empty_state(error: str | None = None) -> dict[str, Any]:
    state: dict[str, Any] = {"active_alerts": {}, "last_sent_at": None, "last_status": None}
    if error:
        state["state_error"] = error
    return state


class AlertStateStore:
    def __init__(self, state_file: str):
        self.path = Path(state_file)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return empty_state()
        try:
            with self.path.open("r", encoding="utf-8") as file:
                state = json.load(file)
            if not isinstance(state, dict):
                return empty_state("Alert state file did not contain an object")
            state.setdefault("active_alerts", {})
            return state
        except Exception as exc:
            return empty_state(f"Unable to read alert state: {exc}")

    def save(self, state: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(state, file, indent=2, sort_keys=True)

    def summary(self) -> dict[str, Any]:
        state = self.load()
        return {
            "active_alert_count": len(state.get("active_alerts", {})),
            "last_sent_at": state.get("last_sent_at"),
            "last_status": state.get("last_status"),
            "state_error": state.get("state_error"),
        }
