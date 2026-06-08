from __future__ import annotations

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
from app.health.http_checker import check_panel
from app.health.port_checker import check_ports
from app.health.process_checker import check_proxy_processes, check_proxy_services
from app.health.system_checker import check_system
from app.health.tls_checker import check_tls
from app.health.traffic_checker import check_traffic
from app.models import CheckResult, HealthResponse

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"

app = FastAPI(title="Conan VPS Control Tower", version="0.1.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


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
    if config.alerts.enabled:
        AlertManager(config.alerts).evaluate(health)
    return health


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


@app.post("/api/alerts/test")
def api_alerts_test() -> dict:
    config = get_config()
    return AlertManager(config.alerts).send_test().to_dict()


@app.post("/api/alerts/evaluate")
def api_alerts_evaluate() -> dict:
    config = get_config()
    health = evaluate(run_all_checks(config))
    return AlertManager(config.alerts).evaluate(health).to_dict()


@app.get("/api/diagnostics")
def api_diagnostics() -> dict:
    config = get_config()
    health = evaluate(run_all_checks(config))
    return diagnose(health).to_dict()
