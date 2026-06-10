# Conan VPS Control Tower

A lightweight, read-only health dashboard for personal VPS proxy nodes.

Conan VPS Control Tower is a local-only health observation layer for personal VPS proxy nodes. It keeps API compatibility in English and uses Simplified Chinese as the default dashboard language.

Current stage: v0.2.0-alpha ready

## Status

- Project stage: v0.2.0-alpha ready
- Runtime mode: local-only by default
- Default bind: `127.0.0.1:3001`
- Target users: personal VPS / proxy node users
- Real VPS validated: yes
- Domain access validated: `tower.conanxin.com` through Cloudflare Access + Tunnel

## Dashboard IA Redesign

The homepage is now organized as a compact daily operations console:

- Hero overview with overall status, summary, and key chips.
- Quick actions for `进入 3X-UI 面板`, diagnostics, and recent events.
- Proxy path: VPS -> proxy core -> 3X-UI panel -> proxy port.
- Core health cards for VPS, proxy core, 3X-UI panel, and ports.
- A wide 3X-UI management entry card with masked public URL display.
- Traffic overview with local estimate and usage percentage.
- Secondary details for optional checks, alerts, health history, recent events, and diagnostic commands.

The UI remains Simplified Chinese by default. API field names remain English for compatibility.

## Domain Access UX

The Dashboard now treats Cloudflare Access + Tunnel as the primary external access path:

- Control Tower: `tower.conanxin.com`
- 3X-UI panel: `panel.conanxin.com / 已配置隐藏路径`
- Service bind: `127.0.0.1:3001`
- Direct public bind: no
- Protection: Cloudflare Access

The visible Dashboard masks the 3X-UI hidden path. The `进入 3X-UI 面板` button can still use the full private `panel_public_url` configured only on the VPS.

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
- It defaults to `127.0.0.1:3001`.
- Access is via local tunnel path, not public port forwarding.

## What you can see

- VPS 状态
- 代理核心状态
- 3X-UI 面板状态
- 端口状态
- 流量风险
- Domain / DNS
- TLS 证书
- 告警通知
- 诊断建议
- 健康历史
- 事件日志

## Alert setup polish

- Added `/api/alerts/config-check` read-only checker to verify whether Telegram / Email are ready.
- Added dashboard alert-setup status with missing-field hints and clear disabled/skipped messages.
- Added systemd environment variable guide for keeping secrets out of Git and checking readiness.

See:

- [Telegram alert setup](docs/TELEGRAM_ALERT_SETUP.md)
- [Systemd alert env guide](docs/ALERT_SYSTEMD_ENV.md)
- [Alert test playbook](docs/ALERT_TEST_PLAYBOOK.md)

## Health History and Event Log

- Recent state snapshots are recorded to `data/health_history.json`.
- Exception-like status transitions are recorded in `data/event_log.json`.
- Dashboard shows summary for the last 24 hours by default.
- Summary includes healthy ratio, worst status, snapshot count, event count, last problem, and last recovery.

See:

- [Health History](docs/HEALTH_HISTORY.md)
- [Event Log](docs/EVENT_LOG.md)

## Domain access / 手机访问

SSH Tunnel remains the recommended default access path. If you want to check the dashboard from a phone browser, use Cloudflare Tunnel + Access instead of exposing raw ports.

Recommended split:

- `tower.example.com` -> Conan VPS Control Tower at `http://127.0.0.1:3001`
- `panel.example.com` -> 3X-UI panel at `https://127.0.0.1:YOUR_3XUI_PANEL_PORT`

Keep these hostnames separate from your proxy main domain. Do not expose port `3001` publicly, and do not use Caddy/Nginx to take over VPS `80/443` for this project.

See:

- [Domain access via Cloudflare Tunnel](docs/DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md)
- [Cloudflare Access policy](docs/CLOUDFLARE_ACCESS_POLICY.md)

## 3X-UI 管理入口

Control Tower is the health and diagnosis layer. 3X-UI remains the configuration layer.

中文理解：Control Tower 负责看状态，3X-UI 负责改配置。Dashboard 提供 `进入 3X-UI 面板` 的统一入口，但不会读取或修改 3X-UI 配置，也不会保存 3X-UI 账号、密码、cookie 或 token。

If the 3X-UI panel uses a hidden path, keep the full URL only in the private VPS `config.yaml`. The Dashboard masks it as `https://panel.conanxin.com/隐藏路径` while the button still opens the full configured URL.

Recommended domain split:

- `tower.conanxin.com` -> Control Tower
- `panel.conanxin.com` -> 3X-UI panel

See:

- [Unified Management Entry](docs/UNIFIED_MANAGEMENT_ENTRY.md)
- [Control Tower and 3X-UI relationship](docs/CONTROL_TOWER_AND_3XUI_RELATIONSHIP.md)

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
- /api/history/summary: available when enabled
- /api/events: available when enabled
- 3X-UI modified: no
- proxy restarted: no
- firewall changed: no
- public port opened: no

## Core Features

- Read-only VPS/system checks
- Proxy core and service visibility
- 3X-UI panel reachability check
- Port checks
- Optional domain and TLS risk checks
- Local traffic estimate + risk thresholds
- Optional Telegram / Email alerting
- Read-only diagnostics and suggested checks
- Health history and event log
- Cloudflare Tunnel domain access guide
- Unified 3X-UI management entry
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
- [Domain access via Cloudflare Tunnel](docs/DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md)
- [Unified Management Entry](docs/UNIFIED_MANAGEMENT_ENTRY.md)

## What It Does Not Do

- Does not replace 3X-UI
- Does not modify proxy config
- Does not restart proxy services
- Does not collect proxy credentials
- Does not expose the dashboard publicly by default
- Does not call provider billing APIs
- Does not execute diagnostic commands automatically
- Does not enable alerting by default
- Does not build project registry or project control plane
- Does not merge 3X-UI code or call 3X-UI write APIs

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
- Phase 1C: Telegram / Email Alerts
- Phase 1D: Diagnostics and Suggested Actions
- Phase 1E: Local-only hardening and real VPS validation
- Phase 1E.1: v0.2.0-alpha release preparation
- Phase 1F: systemd persistence and operational polish
- Phase 1F.2: Chinese dashboard UX polish
- Phase 1F.3: README screenshot and demo docs
- Phase 1G: Health history and event log
- Phase 1K: Domain access via Cloudflare Tunnel
- Phase 1L: Unified 3X-UI management entry
- This project intentionally stays focused on personal VPS / proxy health monitoring.

## License

MIT License
