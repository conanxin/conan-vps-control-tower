# Phase 1F: systemd Persistence and Operational Polish Report

## 本阶段目标

将 Conan VPS Control Tower 从临时 `uvicorn` 运行切换为本项目 `systemd` 持久化服务，确保服务仅本地监听 `127.0.0.1:3001`，并验证不影响现有代理工具与网络边界。

## 新增 / 修改文件

- 新增：
  - `scripts/install-systemd-local-only.sh`
  - `scripts/check-systemd-local-only.sh`
  - `scripts/uninstall-systemd-local-only.sh`
  - `docs/OPERATIONAL_RUNBOOK.md`
  - `docs/SYSTEMD_PERSISTENCE_VERIFICATION.md`
  - `reports/PHASE_1F_SYSTEMD_PERSISTENCE_REPORT.md`（本报告）
- 修改：
  - `tests/test_systemd_scripts.py`（新增）
  - `tests/test_systemd_service_safety.py`（新增）

## 系统化设计理由

- 使用独立脚本安装本项目 service，避免手工重复配置。
- 脚本在安装前明确检查 `.venv`、`config.yaml` 与 `server.host`，把 local-only 前置条件放到安装动作前。
- 监听地址由 service `ExecStart` 显式固定为 `--host 127.0.0.1 --port 3001`，防止误绑公网。
- 校验脚本仅读取状态，不修改代理服务、不改防火墙、不中断现有代理运行。

## 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启代理（3X-UI / xray / sing-box / v2ray）：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否占用 80/443：否
- 是否自动执行诊断命令：否

## 本地测试结果

- pytest：待执行
- Shell 脚本语法检查：待执行

## 真实 VPS systemd 验证结果

- 状态：待执行
- service installed: pending
- enabled: pending
- active: pending
- listener 127.0.0.1:3001: pending
- no 0.0.0.0:3001: pending
- `/api/health`: pending
- `/api/diagnostics`: pending
- `/api/alerts/status`: pending

## 日志检查

- `journalctl -u conan-vps-control-tower --no-pager -n 80`（待执行）

## 当前状态

- 已完成本地脚本与文档补齐，正在进行真实 VPS systemd 持久化验证。

## 下一阶段建议

- Phase 2: Project Control Tower foundation
- Phase 1F.1: Operational hardening polish (optional)
