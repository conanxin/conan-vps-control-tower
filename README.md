# Conan VPS Control Tower

A lightweight, read-only health dashboard for personal VPS proxy nodes.

Conan VPS Control Tower is a local-only health observation layer for personal VPS proxy nodes. It keeps API compatibility in English and uses Simplified Chinese as the default dashboard language.

Current alpha: **v0.2.1-alpha**

## Status

- Project stage: **v0.2.1-alpha**
- Runtime mode: **local-only by default**
- Default bind: `127.0.0.1:3001`
- Target users: personal VPS / proxy node users
- Real VPS validated: yes
- Domain access validated: `tower.conanxin.com` through Cloudflare Access + Tunnel

## Quick access

- Control Tower: `https://tower.conanxin.com`
- 3X-UI management entry: open from Dashboard `进入 3X-UI 面板` button
- Protection: Cloudflare Access + Tunnel

## Screenshot / 界面预览

Dashboard screenshot is intentionally masked to avoid exposing the 3X-UI hidden path or any sensitive operational details.

- `docs/media/dashboard-v0.2.1-alpha.masked.png`
  (masked view showing `panel.conanxin.com / 已配置隐藏路径`)
- Screenshot policy: only masked 3X-UI entry (`panel.conanxin.com / 已配置隐藏路径`), no hidden path, no tokens/secrets.
A quick SSH fallback is still supported for local-only setup:
`ssh -L 3001:127.0.0.1:3001 YOUR_VPS_HOST`

## Safety boundary

- Read-only dashboard operations (health/diagnostics/alerts state)
- Local-only bind: `127.0.0.1:3001`
- No 3X-UI config mutation
- No proxy config mutation
- No firewall changes
- No proxy/core restart
- No secret exposure in UI

## Dashboard IA polish highlights

The homepage is organized as a compact operations console:

- Header with local-only + external entry + Cloudflare protection status
- Hero overall status with one-line summary
- Quick actions: `进入 3X-UI 面板`, `查看诊断`, `查看最近事件`
- 代理链路 cards
- Core cards: VPS / 代理核心 / 3X-UI / 端口
- Dedicated wide management entry card with masked public entry display
- Traffic overview and secondary sections for optional checks, alerts, history, events, and diagnostics

## Phase 1N acceptance prep status

- `Current alpha: v0.2.1-alpha: Cloudflare Access protected Dashboard with masked 3X-UI entry.`
- Acceptance pack, release-note draft, and boundary-focused docs prepared.
- Release phase: v0.2.1-alpha is published as a pre-release in GitHub.

## Why local-only?

Conan VPS Control Tower is a read-only observation layer beside your proxy stack:

- Does not replace 3X-UI.
- Does not modify proxy configuration.
- Does not restart proxy services.
- Defaults to `127.0.0.1:3001`.
- Access is via local-only bind + optional Cloudflare domain routing.

## What you can see

- VPS 状态
- 代理核心状态
- 3X-UI 面板状态
- 端口状态
- 流量风险
- 域名 / DNS
- TLS 证书
- 告警通知
- 健康历史
- 诊断建议

## Alert setup polish

- Added `/api/alerts/config-check` for lightweight channel readiness checks.
- Dashboard alert setup card now shows missing-field hints and disabled/safe fallback messages.
- Added systemd secret-loading guidance so tokens stay out of repository.

See:

- [Telegram alert setup](docs/TELEGRAM_ALERT_SETUP.md)
- [Systemd alert env guide](docs/ALERT_SYSTEMD_ENV.md)
- [Alert test playbook](docs/ALERT_TEST_PLAYBOOK.md)

## Health History and Event Log

- Recent state snapshots are recorded to `data/health_history.json`.
- Event transitions are recorded in `data/event_log.json`.
- Dashboard shows last 24-hour summary and recent events.

See:

- [Health History](docs/HEALTH_HISTORY.md)
- [Event Log](docs/EVENT_LOG.md)

## Domain access / 手机访问

- Cloudflare Tunnel + Access is recommended when using phone browser.
- Recommended split:
  - `tower.example.com` -> Control Tower at `http://127.0.0.1:3001`
  - `panel.example.com` -> 3X-UI panel at `https://127.0.0.1:YOUR_3XUI_PANEL_PORT`

Do not expose raw `3001` publicly, and do not use Caddy/Nginx to seize VPS `80/443`.

See:

- [Domain access via Cloudflare Tunnel](docs/DOMAIN_ACCESS_CLOUDFLARE_TUNNEL.md)
- [Cloudflare Access policy](docs/CLOUDFLARE_ACCESS_POLICY.md)

## 3X-UI management entry

Control Tower is the health and diagnosis layer. 3X-UI remains the configuration layer.

- 3X-UI management is only a navigation entry.
- Dashboard shows masked path text while the button keeps full target URL from `config.yaml`.
- If a hidden path exists, it should stay private and only masked output is shown, e.g. `panel.conanxin.com / 已配置隐藏路径`.

Recommended domain split:

- `tower.conanxin.com` -> Control Tower
- `panel.conanxin.com` -> 3X-UI panel

See:

- [Unified Management Entry](docs/UNIFIED_MANAGEMENT_ENTRY.md)
- [Control Tower and 3X-UI relationship](docs/CONTROL_TOWER_AND_3XUI_RELATIONSHIP.md)

## Real VPS validation

Phase 1E-Live / 1M.x validation passed in de-identified form:

- OS: `Ubuntu 24.04 LTS`
- Python: `3.12.3`
- Run mode: systemd local service
- Bind: `127.0.0.1:3001`
- Public bind: no `0.0.0.0:3001`
- /api/health: healthy
- /api/diagnostics: all_healthy
- /api/alerts/status: disabled
- /api/meta: returned local-only runtime info
- /api/history/summary: available
- /api/events: available
- 3X-UI modified: no
- proxy restarted: no
- firewall changed: no
- public port opened: no

## Core features

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

You can also use SSH tunnel access with command:
`ssh -L 3001:127.0.0.1:3001 YOUR_VPS_HOST` (SSH tunnel for local fallback).

Then open:

```text
http://127.0.0.1:3001
```

If you use Cloudflare Access, open domain:

```text
https://tower.conanxin.com
```

## Alpha Notice

This is the v0.2.1-alpha pre-release for personal VPS health control. Keep traffic local and prefer managed Cloudflare Access + Tunnel for mobile-friendly access.

## Roadmap
### Current baseline

- Current baseline: **v0.2.1-alpha**
- A read-only, Cloudflare-protected health dashboard for a personal VPS proxy stack.
- Focus: local-only observations + domain-protected access + unified operational UX.
- Core boundary:
  - Control Tower remains the health + diagnostic layer.
  - 3X-UI remains the configuration layer.

### Near-term: v0.2.x maintenance line

- Keep stability and maintain compatibility for:
  - Read-only monitoring checks (VPS / proxy core / 3X-UI / ports / traffic / history / alerts status)
  - Domain / TLS / DNS check reliability
  - Management entry stability (masking, CTA behavior, and health status consistency)
  - Documentation refresh and operation sanity checks
- Keep local-only safety model:
  - bind `127.0.0.1:3001`
  - no public bind of `3001`
  - no 3X-UI config mutation
- No feature expansion beyond proxy health observations during this line.

### Mid-term: v0.3.x operational polish

- Minor operational usability work only, including:
  - stronger long-term troubleshooting readability
  - clearer event/historical summaries
  - cleaner status grouping for optional checks vs active risks
  - documentation and acceptance polish for deployment handoff
- Still no proxy automation, no provider billing integration, no universal control-plane features.

### Longer-term possibilities

- Optional UX refinements if adoption grows.
- Future hardening of alert configuration and observability scripts for different deployment patterns.
- Additional language/format improvements for first-response playbooks.
- Better support docs for multi-device operators, while staying self-managed and local-first.

### Non-goals

- Does not replace or merge 3X-UI.
- Does not edit 3X-UI config.
- Does not restart proxy core/services.
- Does not modify firewall rules.
- Does not expose `3001` directly to internet.
- Does not store secrets or hidden paths in UI or repository.
- Does not become a general project-management platform.

### Design principles

- Personal VPS / proxy health first.
- Read-only by default.
- Security by minimizing exposure: local bind + Cloudflare Access + Tunnel.
- Minimal runtime footprint and compatibility-first implementation.
- Transparent status + diagnosis wording in Chinese UI, English-safe API fields.

## License

MIT License
