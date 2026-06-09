from __future__ import annotations

import os
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 3001


class ChecksConfig(BaseModel):
    interval_seconds: int = 30


class SystemConfig(BaseModel):
    disk_warning_percent: float = 80
    ram_warning_percent: float = 80
    load_warning_1m: float = 1.5


class PanelConfig(BaseModel):
    url: str = "http://127.0.0.1:2053"
    timeout_seconds: float = 3


class ProxyConfig(BaseModel):
    process_names: list[str] = Field(default_factory=lambda: ["x-ui", "3x-ui", "xray"])
    service_names: list[str] = Field(default_factory=lambda: ["x-ui", "3x-ui"])
    ports: list[int] = Field(default_factory=lambda: [443])
    panel: PanelConfig = Field(default_factory=PanelConfig)


class TrafficConfig(BaseModel):
    monthly_limit_gb: float = 1000
    reset_day: int = 1
    warning_percent: float = 70
    degraded_percent: float = 85
    critical_percent: float = 95
    interfaces: list[str] = Field(default_factory=lambda: ["auto"])
    data_file: str = "data/traffic_state.json"
    note: str = "本地流量估算可能与服务商计费口径存在差异。"


class DomainConfig(BaseModel):
    enabled: bool = False
    names: list[str] = Field(default_factory=lambda: ["example.com"])
    expected_ips: list[str] = Field(default_factory=lambda: ["203.0.113.10"])
    timeout_seconds: float = 3


class TLSTargetConfig(BaseModel):
    host: str = "example.com"
    port: int = 443
    server_name: str = "example.com"
    warning_days: int = 21
    critical_days: int = 7
    timeout_seconds: float = 5


class TLSConfig(BaseModel):
    enabled: bool = False
    targets: list[TLSTargetConfig] = Field(default_factory=lambda: [TLSTargetConfig()])


class TelegramAlertConfig(BaseModel):
    enabled: bool = False
    bot_token: str = "${TELEGRAM_BOT_TOKEN}"
    chat_id: str = "${TELEGRAM_CHAT_ID}"
    timeout_seconds: float = 5


class EmailAlertConfig(BaseModel):
    enabled: bool = False
    smtp_host: str = "smtp.example.com"
    smtp_port: int = 587
    username: str = "${SMTP_USERNAME}"
    password: str = "${SMTP_PASSWORD}"
    from_addr: str = "alerts@example.com"
    to_addrs: list[str] = Field(default_factory=lambda: ["you@example.com"])
    use_tls: bool = True
    timeout_seconds: float = 10


class AlertsConfig(BaseModel):
    enabled: bool = False
    min_severity: str = "warning"
    cooldown_seconds: int = 1800
    send_recovery: bool = True
    state_file: str = "data/alert_state.json"
    telegram: TelegramAlertConfig = Field(default_factory=TelegramAlertConfig)
    email: EmailAlertConfig = Field(default_factory=EmailAlertConfig)


class HistoryConfig(BaseModel):
    enabled: bool = True
    data_file: str = "data/health_history.json"
    event_file: str = "data/event_log.json"
    max_snapshots: int = 2880
    max_events: int = 500
    min_record_interval_seconds: int = 60
    summary_window_hours: int = 24


class ManagementConfig(BaseModel):
    enabled: bool = True
    panel_name: str = "3X-UI 面板"
    panel_local_url: str = "https://127.0.0.1:2096"
    panel_public_url: str = "https://panel.conanxin.com"
    access_note: str = "建议通过 Cloudflare Access + 双重校验进行保护后访问。"
    open_in_new_tab: bool = True
    show_local_target: bool = True
    readonly_note: str = "Control Tower 不读取或修改 3X-UI 配置。"


class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    checks: ChecksConfig = Field(default_factory=ChecksConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    traffic: TrafficConfig = Field(default_factory=TrafficConfig)
    domain: DomainConfig = Field(default_factory=DomainConfig)
    tls: TLSConfig = Field(default_factory=TLSConfig)
    alerts: AlertsConfig = Field(default_factory=AlertsConfig)
    history: HistoryConfig = Field(default_factory=HistoryConfig)
    management: ManagementConfig = Field(default_factory=ManagementConfig)


ENV_PATTERN = re.compile(r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$")


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _expand_env_placeholders(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _expand_env_placeholders(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_env_placeholders(item) for item in value]
    if isinstance(value, str):
        match = ENV_PATTERN.match(value)
        if match:
            return os.getenv(match.group(1), value)
    return value


def load_config(path: str | Path | None = None) -> AppConfig:
    config_path = Path(path or os.getenv("CONAN_CONFIG_PATH", "config.yaml"))
    defaults = AppConfig().model_dump()

    if not config_path.exists():
        return AppConfig.model_validate(defaults)

    with config_path.open("r", encoding="utf-8") as file:
        loaded = yaml.safe_load(file) or {}

    if not isinstance(loaded, dict):
        raise ValueError(f"Config file must contain a YAML mapping: {config_path}")

    return AppConfig.model_validate(_expand_env_placeholders(_deep_merge(defaults, loaded)))
