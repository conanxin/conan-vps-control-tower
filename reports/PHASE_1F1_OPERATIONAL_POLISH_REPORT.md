# Phase 1F.1: Operational Polish Report

## 本阶段目标

在 Phase 1F 已通过的 systemd 持久化基础上，完成运维抛光，降低日常巡检与排错成本，不新增产品能力，不改变只读与 local-only 边界。

## 新增 / 修改文件

- 新增：
  - `scripts/tower-status.sh`
  - `scripts/tower-logs.sh`
  - `scripts/tower-stop-temporary-uvicorn.sh`
  - `reports/PHASE_1F1_OPERATIONAL_POLISH_REPORT.md`
- 修改：
  - `docs/OPERATIONAL_RUNBOOK.md`
  - `docs/SYSTEMD_PERSISTENCE_VERIFICATION.md`
  - `README.md`
  - `CHANGELOG.md`
  - `tests/test_operational_scripts.py`

## 运维抛光内容

- 增加一键状态脚本 `tower-status.sh`：
  - 输出 `systemctl is-active`、`systemctl is-enabled`
  - 检查 `:3001` 监听与 0.0.0.0 安全边界
  - 调用 `api/health`、`api/diagnostics`、`api/alerts/status`
  - 输出项目最近日志
- 增加日志快速查看脚本 `tower-logs.sh`：
  - 默认显示 120 行
  - 支持 `follow` 参数，进入持续追踪模式
- 增加临时 uvicorn 清理脚本 `tower-stop-temporary-uvicorn.sh`：
  - 仅匹配 `uvicorn app.main:app --host 127.0.0.1 --port 3001`
  - 不影响 systemd service
- 更新运维 runbook 与系统验证文档，补充常用命令、日志、清理和 SSH 访问入口
- 更新 `README` 与 `CHANGELOG`，指向新运维文档

## 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启代理：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否占用 80/443：否
- 是否操作 3X-UI / xray / sing-box / v2ray：未做任何服务重启/启停

## 测试结果

- `python -m pytest`：通过
- docs 安全性测试：通过
- operational scripts 单测：已新增并通过

## 真实 VPS 是否执行验证

- 已执行 `dmit-control-tower` 远端验证：
  - `bash scripts/tower-status.sh`
  - `bash scripts/tower-logs.sh | head -80`
- 真实 VPS 均返回 expected local-only 状态与 API 可用

## 当前系统状态

- systemd 持久化与 local-only 运维抛光工作完成
- 本地-only 边界与服务边界保持不变
- 继续建议通过 `docs/OPERATIONAL_RUNBOOK.md` 执行日常巡检

## 下一阶段建议

- Phase 2: Project Control Tower foundation
