# Phase 1F: systemd Persistence and Operational Polish Report

## 本阶段目标

完成 1F 本地-only systemd 持久化验证前置与落地，确保：

- 临时 `uvicorn` 切换为本项目 `systemd` 持久化运行
- 监听严格为 `127.0.0.1:3001`
- 不绑定/不暴露 `0.0.0.0:3001`
- 不影响现有代理运行

## 新增 / 修改文件

- 新增：
  - `scripts/install-systemd-local-only.sh`
  - `scripts/check-systemd-local-only.sh`
  - `scripts/uninstall-systemd-local-only.sh`
  - `docs/OPERATIONAL_RUNBOOK.md`
  - `docs/SYSTEMD_PERSISTENCE_VERIFICATION.md`
  - `tests/test_systemd_scripts.py`
  - `tests/test_systemd_service_safety.py`
  - `reports/PHASE_1F_SYSTEMD_PERSISTENCE_REPORT.md`
- 修改：
  - `tests/test_docs_safety.py`

## systemd 持久化设计理由

- 新增独立安装/校验/卸载脚本，避免重复手工 systemd 配置。
- 安装脚本显式要求：
  - `.venv` 已存在
  - `config.yaml` 存在
  - `server.host == 127.0.0.1`
  - 不接受 `0.0.0.0` 绑定
- 安装时动态生成 unit 文件，`ExecStart` 强制使用:
  - `--host 127.0.0.1 --port 3001`
- 校验脚本仅执行只读检查，不修改代理或防火墙。

## 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启代理（3X-UI / xray / sing-box / v2ray）：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否占用 80/443：否（由既有服务现状监听；本项目无改动）
- 是否自动执行诊断命令：否

## 本地测试结果

- pytest：53 passed
- Shell script syntax check：本地 Windows 环境未安装 `bash`，未能直接执行 `bash -n`，命令清单已按你要求保留

## 真实 VPS systemd 验证结果

- 执行时间：2026-06-09
- Commit used：`3ff6bde`
- service 安装：是
- service enabled：是
- service active：是
- listener `127.0.0.1:3001`：存在
- `0.0.0.0:3001`：未发现
- `/api/health`：200，`overall_status=healthy`
- `/api/diagnostics`：200，`all_healthy`
- `/api/alerts/status`：200，`alerts.enabled=false`

## 日志检查

- `journalctl -u conan-vps-control-tower --no-pager -n 80` 可见正常启动与 API 请求日志，无异常报错。

## 当前状态

- systemd 验证完成。
- 本项目现可在 VPS 以 local-only 方式持久运行。
- 3X-UI 与代理服务维持运行，无重启动作。
- 未修改防火墙。
- 未开放公网 127.0.0.1 外监听（未出现 0.0.0.0:3001）。

## 下一阶段建议

- Phase 2: Project Control Tower foundation
- Phase 1F.1: Operational hardening polish (optional)
