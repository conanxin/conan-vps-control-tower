from __future__ import annotations

import importlib.metadata
import re
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.alerts.manager import AlertManager
from app.config import AppConfig, load_config
from app.diagnostics.engine import diagnose
from app.health.domain_checker import check_domain
from app.health.evaluator import evaluate
from app.history.recorder import record_health_snapshot
from app.history.store import load_events, load_snapshots
from app.history.summary import build_summary
from app.health.http_checker import check_panel
from app.health.port_checker import check_ports
from app.health.process_checker import check_proxy_processes, check_proxy_services
from app.health.system_checker import check_system
from app.health.tls_checker import check_tls
from app.health.traffic_checker import check_traffic
from app.models import CheckResult, HealthResponse, MetaResponse
from app.alerts.config_check import check_alert_config

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
ROOT_DIR = APP_DIR.parent
PROJECT_VERSION = "0.2.0"

app = FastAPI(title="Conan VPS Control Tower", version="0.2.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def _project_version() -> str:
    pyproject = ROOT_DIR / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8")
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
    try:
        return importlib.metadata.version("conan-vps-control-tower")
    except importlib.metadata.PackageNotFoundError:
        return PROJECT_VERSION


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    return load_config()


def run_all_checks(config: AppConfig) -> list[CheckResult]:
    return [
        check_system(config.system),
        check_proxy_processes(config.proxy),
        check_proxy_services(config.proxy),
        check_panel(config.proxy.panel),
        check_ports(config.proxy.ports),
        check_domain(config.domain),
        check_tls(config.tls),
        check_traffic(config.traffic),
    ]


def run_system_checks(config: AppConfig) -> list[CheckResult]:
    return [check_system(config.system)]


def run_proxy_checks(config: AppConfig) -> list[CheckResult]:
    return [
        check_proxy_processes(config.proxy),
        check_proxy_services(config.proxy),
        check_panel(config.proxy.panel),
        check_ports(config.proxy.ports),
        check_traffic(config.traffic),
    ]


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health", response_model=HealthResponse)
def api_health() -> HealthResponse:
    config = get_config()
    health = evaluate(run_all_checks(config))
    history_result = {"recorded": False, "reason": "history disabled", "snapshot_id": None}
    if config.history.enabled:
        history_result = record_health_snapshot(health, config.history)
    health.history_recording = history_result
    if config.alerts.enabled:
        AlertManager(config.alerts).evaluate(health)
    return health


@app.get("/api/history/summary")
def api_history_summary() -> dict:
    config = get_config()
    if not config.history.enabled:
        return {
            "enabled": False,
            "message": "history disabled",
            "summary": None,
        }

    snapshots, snapshot_error = load_snapshots(config.history.data_file)
    events, event_error = load_events(config.history.event_file)
    summary = build_summary(
        snapshots,
        events,
        window_hours=config.history.summary_window_hours,
    )
    payload = summary.to_dict()
    payload["enabled"] = True
    if snapshot_error:
        payload["warning"] = snapshot_error
    if event_error:
        payload["warning"] = event_error
    return payload


@app.get("/api/history/recent")
def api_history_recent(limit: int = 50) -> dict:
    config = get_config()
    if not config.history.enabled:
        return {
            "enabled": False,
            "items": [],
            "limit": limit,
        }

    safe_limit = max(1, min(limit, 500))
    snapshots, snapshot_error = load_snapshots(config.history.data_file)
    items = [item.to_dict() for item in snapshots[-safe_limit:]]
    payload: dict[str, object] = {
        "enabled": True,
        "items": items,
        "limit": safe_limit,
        "window_hours": config.history.summary_window_hours,
    }
    if snapshot_error:
        payload["warning"] = snapshot_error
    return payload


@app.get("/api/events")
def api_events(limit: int = 50, severity: str | None = None) -> dict:
    config = get_config()
    if not config.history.enabled:
        return {
            "enabled": False,
            "items": [],
            "limit": max(1, min(limit, 500)),
            "severity": severity,
        }

    safe_limit = max(1, min(limit, 500))
    events, event_error = load_events(config.history.event_file)
    items = [item.to_dict() for item in events if severity is None or item.severity == severity]
    items = items[-safe_limit:]
    payload: dict[str, object] = {
        "enabled": True,
        "items": items,
        "limit": safe_limit,
        "severity": severity,
    }
    if event_error:
        payload["warning"] = event_error
    return payload


@app.get("/api/system", response_model=HealthResponse)
def api_system() -> HealthResponse:
    config = get_config()
    return evaluate(run_system_checks(config))


@app.get("/api/proxy", response_model=HealthResponse)
def api_proxy() -> HealthResponse:
    config = get_config()
    return evaluate(run_proxy_checks(config))


@app.get("/api/domain", response_model=HealthResponse)
def api_domain() -> HealthResponse:
    config = get_config()
    return evaluate([check_domain(config.domain)])


@app.get("/api/tls", response_model=HealthResponse)
def api_tls() -> HealthResponse:
    config = get_config()
    return evaluate([check_tls(config.tls)])


@app.get("/api/traffic", response_model=HealthResponse)
def api_traffic() -> HealthResponse:
    config = get_config()
    return evaluate([check_traffic(config.traffic)])


@app.get("/api/alerts/status")
def api_alerts_status() -> dict:
    config = get_config()
    return AlertManager(config.alerts).status()


@app.get("/api/alerts/config-check")
def api_alerts_config_check() -> dict:
    config = get_config()
    try:
        return check_alert_config(config.alerts)
    except Exception as exc:
        return {
            "status": "warning",
            "enabled": False,
            "message": f"告警配置检查失败，已安全回退：{type(exc).__name__}",
            "min_severity": config.alerts.min_severity,
            "cooldown_seconds": config.alerts.cooldown_seconds,
            "send_recovery": config.alerts.send_recovery,
            "state_file_ready": bool(config.alerts.state_file),
            "channels": {
                "telegram": {
                    "enabled": False,
                    "ready": False,
                    "missing_fields": [],
                    "message": "Telegram 告警未开启。",
                },
                "email": {
                    "enabled": False,
                    "ready": False,
                    "missing_fields": [],
                    "message": "Email 告警未开启。",
                },
            },
            "safe_to_test": False,
        }


@app.post("/api/alerts/test")
def api_alerts_test() -> dict:
    config = get_config()
    return AlertManager(config.alerts).send_test().to_dict()


@app.post("/api/alerts/evaluate")
def api_alerts_evaluate() -> dict:
    config = get_config()
    health = evaluate(run_all_checks(config))
    return AlertManager(config.alerts).evaluate(health).to_dict()


@app.get("/api/meta", response_model=MetaResponse)
def api_meta() -> MetaResponse:
    config = get_config()
    return MetaResponse(
        app_name="Conan VPS Control Tower",
        version=_project_version(),
        ui_language="zh-CN",
        configured_host=config.server.host,
        configured_port=config.server.port,
        local_only=True,
        access_hint="Use SSH tunnel to access the dashboard.",
        history_enabled=config.history.enabled,
        event_log=config.history.enabled,
        alert_config_check=True,
    )


@app.get("/api/diagnostics")
def api_diagnostics() -> dict:
    config = get_config()
    health = evaluate(run_all_checks(config))
    return diagnose(health).to_dict()
