from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import AppConfig, load_config
from app.health.evaluator import evaluate
from app.health.http_checker import check_panel
from app.health.port_checker import check_ports
from app.health.process_checker import check_proxy_processes, check_proxy_services
from app.health.system_checker import check_system
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
    return evaluate(run_all_checks(config))


@app.get("/api/system", response_model=HealthResponse)
def api_system() -> HealthResponse:
    config = get_config()
    return evaluate(run_system_checks(config))


@app.get("/api/proxy", response_model=HealthResponse)
def api_proxy() -> HealthResponse:
    config = get_config()
    return evaluate(run_proxy_checks(config))
