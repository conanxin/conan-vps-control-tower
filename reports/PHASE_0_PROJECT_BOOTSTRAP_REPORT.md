# Phase 0 Project Bootstrap Report

## 本阶段目标

创建 Conan VPS Control Tower 的开源项目骨架，明确产品定位、架构、健康模型、路线图、部署方式和开源边界。

## 已创建文件

- `README.md`
- `LICENSE`
- `.gitignore`
- `.env.example`
- `config.example.yaml`
- `pyproject.toml`
- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/HEALTH_MODEL.md`
- `docs/ROADMAP.md`
- `docs/OPEN_SOURCE_PLAN.md`
- `docs/DEPLOYMENT.md`
- `reports/PHASE_0_PROJECT_BOOTSTRAP_REPORT.md`

## 设计理由

- 使用 FastAPI、原生前端和 YAML 配置，避免引入企业级复杂架构。
- 默认本地监听 `127.0.0.1:3001`，避免占用 80/443，也避免默认公网暴露。
- 明确只读边界，降低对 3X-UI、Xray、防火墙和现有代理链路的干扰风险。
- 将健康模型独立成文档，方便后续新增 checker 时保持一致返回结构。

## 修改影响分析

本阶段只创建项目文件，不读取、不修改、不重启任何 VPS 代理服务，不修改 3X-UI 配置，不修改防火墙。

## 当前状态

项目骨架已具备开源仓库基础结构，Phase 1A 可以开始实现可运行 MVP。

## 下一阶段建议

实现 FastAPI 服务、只读 checker、健康聚合器、静态 Dashboard、pytest 测试和 systemd 部署脚本。
