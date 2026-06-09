# Conan VPS Control Tower

A lightweight, read-only health dashboard for personal VPS proxy nodes.

Conan VPS Control Tower is a local-only health control tower for personal VPS and proxy node users. It observes VPS resources, proxy core state, 3X-UI panel reachability, proxy ports, DNS risk, TLS certificate risk, local traffic estimate risk, alerting status, and diagnostics suggestions.

Current stage: v0.2.0-alpha ready

Dashboard language: Simplified Chinese by default (API fields remain English for compatibility).

## Status

- Project stage: v0.2.0-alpha ready
- Latest prerelease target: `v0.2.0-alpha`
- Runtime mode: local-only by default
- Default bind: `127.0.0.1:3001`
- Target users: personal VPS / proxy node users
- Real VPS validated: yes

## Real VPS Validation

Phase 1E-Live validation passed on a real VPS using:

- OS: Ubuntu 24.04 LTS
- Python: 3.12.3
- Run mode: temporary uvicorn
- Bind: `127.0.0.1:3001`
- Public bind: no `0.0.0.0:3001`
- Proxy disruption: none observed
- 3X-UI modified: no
- Proxy restarted: no
- Firewall changed: no
- Public port opened: no

No real VPS IP, domain, token, UUID, subscription link, or panel password is documented in this repository.

## Why This Exists

3X-UI is a configuration and management panel for proxy services.

Conan VPS Control Tower is a read-only health observation layer. It does not replace the panel. It helps users quickly understand which layer may be risky:

- VPS resources
- Proxy core process
- 3X-UI panel reachability
- Proxy port status
- Domain / DNS resolution
- TLS certificate expiry
- Local traffic estimate
- Alerting state
- Diagnostics and suggested first checks

## Core Features

- Read-only VPS health checks
- Proxy core process and service visibility
- 3X-UI panel reachability check
- Proxy port availability check
- Optional Domain / DNS risk check
- Optional TLS certificate expiry risk check
- Local traffic estimate with warning, degraded, and critical thresholds
- Optional Telegram / Email alerting with cooldown, dedupe, recovery, and test notifications
- Diagnostics and suggested read-only actions
- Local-only preflight and redacted VPS validation scripts
- Human-readable status summary and risk hints
- Local-only dashboard by default: `127.0.0.1:3001`
- 默认中文界面，API 字段维持英文兼容。

See [Domain / TLS / Traffic Risk](docs/DOMAIN_TLS_TRAFFIC_RISK.md) for configuration examples.
See [Alerting](docs/ALERTING.md) for Telegram and Email notification setup.
See [Diagnostics](docs/DIAGNOSTICS.md) for suggested read-only checks.
See [Dashboard UX polish](docs/DASHBOARD_UX_POLISH.md) for Chinese copy and diagnostics placement details.
See [systemd local-only](docs/SYSTEMD_LOCAL_ONLY.md), [real VPS validation checklist](docs/REAL_VPS_VALIDATION_CHECKLIST.md), and [dashboard smoke test](docs/DASHBOARD_SMOKE_TEST.md) before running on a real VPS.

Operationally, we now provide:

- [Operational runbook](docs/OPERATIONAL_RUNBOOK.md)
- [systemd persistence verification](docs/SYSTEMD_PERSISTENCE_VERIFICATION.md)

## What It Does Not Do

- Does not replace 3X-UI
- Does not modify proxy configuration
- Does not restart proxy services
- Does not collect proxy credentials
- Does not expose the dashboard publicly by default
- Does not call VPS provider billing APIs
- Does not enable alerting by default
- Does not execute diagnostic commands automatically

## Screenshot

Dashboard screenshots will be added with redaction after additional validation. See [dashboard placeholder](docs/media/dashboard-placeholder.md).

## Alpha Notice

This is an alpha project for a personal VPS health control tower. Use it locally or through an SSH tunnel. Direct public exposure is not recommended.

## Quick Start

```bash
cp config.example.yaml config.yaml
python -m venv .venv
. .venv/bin/activate
pip install -e .
uvicorn app.main:app --host 127.0.0.1 --port 3001
```

Then open:

```text
http://127.0.0.1:3001
```

For VPS usage, prefer an SSH tunnel:

```bash
ssh -L 3001:127.0.0.1:3001 user@YOUR_VPS_HOST
```

## Roadmap

- Phase 1A: Read-only health detection MVP
- Phase 1B: Domain / TLS / Traffic Risk Enhancement
- Phase 1C: Telegram and Email alerts
- Phase 1D: Diagnostic suggestions and common commands
- Phase 1E: Local-only hardening and real VPS validation
- Phase 1E.1: v0.2.0-alpha release preparation
- Phase 1F.2: Chinese dashboard UX polish
- Phase 2: Project control tower
- Phase 3: Information radar and Agent command library

## License

MIT License
