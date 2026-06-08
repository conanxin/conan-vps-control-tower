# Architecture

## Overview

```text
Browser UI
   |
   v
FastAPI API Layer
   |
   v
Health Evaluator
   |
   +--> System Checker
   +--> Process Checker
   +--> Port Checker
   +--> HTTP Checker
   +--> Traffic Checker
   |
   v
YAML Config Layer

systemd
   |
   v
uvicorn on 127.0.0.1:3001
```

## Checker Layer

The checker layer performs small read-only inspections. Each checker returns a structured result and catches its own failures so one broken check does not crash the whole service.

## Evaluator Layer

The evaluator combines checker results into:

- `overall_status`
- `readable_summary`
- `risk_summary`
- `checked_at`
- raw checker results

It does not mutate system state.

## API Layer

FastAPI exposes:

- `/api/health` for aggregated status
- `/api/system` for VPS status
- `/api/proxy` for proxy-related status
- `/` for the dashboard

## UI Layer

The UI uses native HTML, CSS, and JavaScript. It does not depend on CDN assets or a frontend framework, keeping the dashboard suitable for low-resource VPS environments.

## Configuration Layer

Configuration is stored in `config.yaml`, copied from `config.example.yaml`. The first version uses YAML only. SQLite can be added later for historical health snapshots.

## systemd Runtime

The systemd unit runs uvicorn with:

```text
--host 127.0.0.1 --port 3001
```

This avoids occupying proxy-facing ports such as 80 and 443, and avoids public exposure by default.

## Why Lightweight Architecture

This is a personal control tower, not an enterprise observability platform. A small FastAPI app with native UI, YAML config, and focused checkers reduces operational risk, avoids heavy dependencies, and keeps the monitoring process easy to inspect.
