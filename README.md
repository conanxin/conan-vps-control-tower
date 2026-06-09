# Conan VPS Control Tower

A lightweight, read-only health dashboard for personal VPS proxy nodes.

Conan VPS Control Tower is a local-only health observation layer for personal VPS proxy nodes. It keeps API compatibility in English and uses **Simplified Chinese** as the default dashboard language.

Current stage: v0.2.0-alpha ready

## Status

- Project stage: v0.2.0-alpha ready
- Runtime mode: local-only by default
- Default bind: `127.0.0.1:3001`
- Target users: personal VPS / proxy node users
- Real VPS validated: yes

## Screenshot / 界面预览

Dashboard is shown in Simplified Chinese by default.

- If no real screenshot is available yet: [Dashboard screenshot placeholder](docs/media/dashboard-zh-local-only-v0.2.placeholder.md).
- Access URL: `http://127.0.0.1:3001` (via SSH tunnel to avoid public exposure).
- Public expose: no by default.

## Why local-only?

Conan VPS Control Tower is a read-only observation layer beside your proxy stack:

- It does not replace 3X-UI.
- It does not modify proxy configuration.
- It does not restart proxy services.
- It does not require any firewall or Nginx/Caddy/Cloudflare Tunnel changes.
- It defaults to `127.0.0.1:3001`.
- Access path is local/SSH-tunnel only.

## What you can see

- VPS 状态（资源和系统）
- 代理核心状态
- 3X-UI 面板状态
- 端口状态
- 流量风险
- 域名 / DNS
- TLS 证书
- 告警通知
- 诊断建议

## Real VPS validation

Phase 1E-Live validation passed in de-identified form:

- OS: `Ubuntu 24.04 LTS`
- Python: `3.12.3`
- Run mode: systemd local service
- Bind: `127.0.0.1:3001`
- Public bind: no `0.0.0.0:3001`
- /api/health: healthy
- /api/diagnostics: all_healthy
- /api/alerts/status: disabled
- /api/meta: returned local-only runtime info
- 3X-UI modified: no
- proxy restarted: no
- firewall changed: no
- public port opened: no

## Why This Exists

3X-UI is the configuration and management panel.

Conan VPS Control Tower is the read-only health layer. It helps identify where to check first:

- VPS health
- proxy core
- 3X-UI panel reachability
- listening ports
- DNS and TLS checks
- local traffic estimate risk
- alerts and diagnostics context

## Core Features

- Read-only VPS/system checks
- Proxy core and service visibility
- 3X-UI panel reachability check
- Port checks
- Optional domain and TLS risk checks
- Local traffic estimate + risk thresholds
- Optional Telegram / Email alerting
- Read-only diagnostics and suggested checks
- Local-only systemd helper scripts

See:
- [Domain / TLS / Traffic Risk](docs/DOMAIN_TLS_TRAFFIC_RISK.md)
- [Alerting](docs/ALERTING.md)
- [Diagnostics](docs/DIAGNOSTICS.md)
- [Dashboard UX polish](docs/DASHBOARD_UX_POLISH.md)
- [Systemd local-only](docs/SYSTEMD_LOCAL_ONLY.md)
- [Real VPS validation checklist](docs/REAL_VPS_VALIDATION_CHECKLIST.md)
- [Dashboard smoke test](docs/DASHBOARD_SMOKE_TEST.md)
- [Operational runbook](docs/OPERATIONAL_RUNBOOK.md)
- [Dashboard screenshot guide](docs/media/DASHBOARD_SCREENSHOT_GUIDE.md)
- [Demo walkthrough](docs/DEMO_WALKTHROUGH.md)
- [Showcase notes](docs/README_SHOWCASE_NOTES.md)

## What It Does Not Do

- Does not replace 3X-UI
- Does not modify proxy config
- Does not restart proxy services
- Does not collect proxy credentials
- Does not expose the dashboard publicly by default
- Does not call provider billing APIs
- Does not execute diagnostic commands automatically
- Does not enable alerting by default

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

Prefer SSH tunnel for VPS usage:

```bash
ssh -L 3001:127.0.0.1:3001 user@YOUR_VPS_HOST
```

## Alpha Notice

This is an alpha project for personal VPS health control. Keep traffic local and prefer SSH tunnel access.

## Roadmap

- Phase 1A: Read-only health detection MVP
- Phase 1B: Domain / TLS / Traffic Risk Enhancement
- Phase 1C: Telegram and Email alerts
- Phase 1D: Diagnostics and Suggested Actions
- Phase 1E: Local-only hardening and real VPS validation
- Phase 1E.1: v0.2.0-alpha release preparation
- Phase 1F: systemd persistence and operational polish
- Phase 1F.2: Chinese dashboard UX polish
- Phase 1F.3: README screenshot and demo docs
- Phase 2A: Project Registry foundation
- Phase 2: Project Control Tower
- Phase 3: Information radar and Agent command library

## License

MIT License
