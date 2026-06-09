# Conan VPS Control Tower

A lightweight, read-only health dashboard for personal VPS proxy nodes.

Conan VPS Control Tower is a lightweight health control tower for personal VPS and proxy node users. It listens locally by default and helps observe VPS resources, proxy core state, 3X-UI panel reachability, proxy ports, DNS risk, TLS certificate risk, and local traffic estimate risk.

Conan VPS Control Tower 是一个面向个人 VPS / 代理节点用户的轻量健康控制塔。它默认只在本机监听，用于观察 VPS 状态、代理核心状态、3X-UI 面板状态、代理端口状态、DNS 风险、TLS 证书风险和本地流量估算风险。

Current stage: Phase 1B implemented on main / v0.1.0-alpha released

## Status

- Project stage: Phase 1B implemented on `main`
- Latest prerelease: `v0.1.0-alpha`
- Runtime mode: local-only by default
- Default bind: `127.0.0.1:3001`
- Target users: personal VPS / proxy node users

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
- Human-readable status summary and risk hints
- Local-only dashboard by default: `127.0.0.1:3001`

See [Domain / TLS / Traffic Risk](docs/DOMAIN_TLS_TRAFFIC_RISK.md) for configuration examples.
See [Alerting](docs/ALERTING.md) for Telegram and Email notification setup.
See [Diagnostics](docs/DIAGNOSTICS.md) for suggested read-only checks.
See [systemd local-only](docs/SYSTEMD_LOCAL_ONLY.md), [real VPS validation checklist](docs/REAL_VPS_VALIDATION_CHECKLIST.md), and [dashboard smoke test](docs/DASHBOARD_SMOKE_TEST.md) before running on a real VPS.

## What It Does Not Do

- Does not replace 3X-UI
- Does not modify proxy configuration
- Does not restart proxy services
- Does not collect proxy credentials
- Does not expose the dashboard publicly by default
- Does not call VPS provider billing APIs
- Does not enable alerting by default

## Non-Goals

- 不替代 3X-UI
- 不做自动修复
- 不采集代理配置、UUID、密码、订阅链接或节点明文
- 不运行重任务
- 不修改 3X-UI 配置
- 不重启代理服务
- 不修改防火墙
- 不默认暴露公网访问

## Screenshot

Dashboard screenshots will be added after validation on a real VPS. See [dashboard placeholder](docs/media/dashboard-placeholder.md).

## Alpha Notice

This is an early alpha project for a personal VPS health control tower. Use it locally or through an SSH tunnel first. Direct public exposure is not recommended.

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
- Phase 2: Project control tower
- Phase 3: Information radar and Agent command library

## License

MIT License
