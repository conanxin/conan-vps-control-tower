# Product Requirements Document

## Product Positioning

Conan VPS Control Tower is a personal, lightweight, read-only health dashboard for VPS proxy nodes. It helps an operator understand whether the VPS, proxy core, 3X-UI panel, proxy ports, and basic traffic situation look healthy without changing the running proxy environment.

## Target Users

- Personal VPS proxy node owners
- Users running 3X-UI or Xray-based proxy services
- Operators who want a small local dashboard instead of an enterprise monitoring stack
- Users who value safety, privacy, and minimal interference

## Core Problems

- It is hard to quickly know whether a proxy node is down, degraded, or only partially affected.
- Existing panels may show proxy configuration but not a plain health summary.
- Heavy monitoring systems are unnecessary for a single personal VPS.
- Operators need diagnostic hints without automatic changes to sensitive services.

## First Stage Scope

Phase 1A focuses on read-only health detection:

- VPS CPU, RAM, disk, and load status
- Proxy process and service visibility
- 3X-UI panel HTTP reachability
- Proxy port open/closed status
- Basic traffic counter visibility
- Aggregated health status and readable summary
- Local-only web dashboard

## User Stories

- As a VPS owner, I want to open a local dashboard and see whether my proxy node is healthy.
- As a 3X-UI user, I want to know whether the panel is reachable without exposing secrets.
- As an operator, I want warnings before disk, RAM, or load pressure becomes critical.
- As a cautious user, I want monitoring that never restarts services or changes firewall rules.

## MVP Feature List

- FastAPI web service
- Native HTML/CSS/JS dashboard
- JSON API endpoints for health, system, and proxy status
- YAML configuration file
- Read-only checkers
- Health evaluator with overall status
- pytest tests for core logic
- systemd service template

## What We Will Not Do

- Replace 3X-UI
- Modify proxy configuration
- Restart proxy services
- Change firewall rules
- Store UUIDs, passwords, subscription links, private keys, or node plaintext
- Run large background jobs
- Expose public access by default

## Success Criteria

- The app runs on `127.0.0.1:3001` by default.
- `/api/health`, `/api/system`, and `/api/proxy` return JSON successfully.
- Checker failures are contained and reported as `unknown` or `critical`.
- The dashboard refreshes automatically every 30 seconds.
- Tests pass with `pytest`.
- Documentation clearly explains scope, risks, and deployment.
