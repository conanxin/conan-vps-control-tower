from __future__ import annotations

import json
import urllib.error
import urllib.request

from app.alerts.formatters import telegram_text
from app.alerts.models import AlertEvent, ChannelResult
from app.config import TelegramAlertConfig


def is_placeholder(value: str) -> bool:
    return not value or value.startswith("${") or value.endswith("}") or value.startswith("YOUR_")


def send_telegram(event: AlertEvent, config: TelegramAlertConfig) -> ChannelResult:
    if not config.enabled:
        return ChannelResult(channel="telegram", success=False, skipped=True, message="Telegram disabled")
    if is_placeholder(config.bot_token) or is_placeholder(config.chat_id):
        return ChannelResult(channel="telegram", success=False, skipped=True, message="Telegram token/chat_id not configured")

    url = f"https://api.telegram.org/bot{config.bot_token}/sendMessage"
    payload = json.dumps({"chat_id": config.chat_id, "text": telegram_text(event)}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
            if 200 <= response.status < 300:
                return ChannelResult(channel="telegram", success=True, message="Telegram alert sent")
            return ChannelResult(channel="telegram", success=False, error=f"Telegram HTTP {response.status}")
    except urllib.error.HTTPError as exc:
        return ChannelResult(channel="telegram", success=False, error=f"Telegram HTTP {exc.code}")
    except Exception as exc:
        return ChannelResult(channel="telegram", success=False, error=f"Telegram send failed: {type(exc).__name__}")
