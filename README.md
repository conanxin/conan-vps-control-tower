# Conan VPS Control Tower

A lightweight, read-only health dashboard for personal VPS proxy nodes.

Conan VPS Control Tower 是一个面向个人 VPS 的轻量控制塔，用于只读监控代理节点健康状态。它关注 VPS 基础状态、代理核心进程、3X-UI 面板、代理端口和基础流量信息，并把检测结果转换成人能理解的健康判断与诊断建议。

当前阶段：Phase 1A planned

## Core Features

- Read-only VPS health checks
- Proxy core process and service visibility
- 3X-UI panel reachability check
- Proxy port availability check
- Basic traffic usage overview
- Human-readable status summary and risk hints
- Local-only dashboard by default: `127.0.0.1:3001`

## Non-Goals

- 不替代 3X-UI
- 不做自动修复
- 不采集代理配置、UUID、密码、订阅链接或节点明文
- 不运行重任务
- 不修改 3X-UI 配置
- 不重启代理服务
- 不修改防火墙
- 不默认暴露公网访问

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

## Roadmap

- Phase 1A: Read-only health detection MVP
- Phase 1B: Traffic, domain, TLS, and expiration reminders
- Phase 1C: Telegram and Email alerts
- Phase 1D: Diagnostic suggestions and common commands
- Phase 2: Project control tower
- Phase 3: Information radar and Agent command library

## License

MIT License
