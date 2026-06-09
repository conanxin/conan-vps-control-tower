# Phase 1H Alerting Setup Polish Report

## 1. 本阶段目标

- 在不改变只读、local-only 安全模型的前提下，优化告警配置体验与可观测性。
- 提供只读的告警配置校验能力，便于用户快速判断告警是否会触发。
- 补齐 Telegram/Email 的配置说明、systemd 环境变量引导和测试告警检查步骤。
- 保持与现有诊断 / 历史功能兼容，不新增代理管理或部署能力。

## 2. 新增 / 修改文件

- 新增：
  - `app/alerts/config_check.py`
  - `scripts/check-alert-config.sh`
  - `docs/ALERT_SYSTEMD_ENV.md`
  - `docs/TELEGRAM_ALERT_SETUP.md`
  - `docs/ALERT_TEST_PLAYBOOK.md`
  - `reports/PHASE_1H_ALERTING_SETUP_POLISH_REPORT.md`
- 修改：
  - `app/main.py`
  - `app/models.py`
  - `app/static/index.html`
  - `app/static/app.js`
  - `README.md`
  - `CHANGELOG.md`
  - `docs/ALERTING.md`
  - `docs/OPERATIONAL_RUNBOOK.md`
  - `docs/DASHBOARD_SMOKE_TEST.md`
  - `docs/DEMO_WALKTHROUGH.md`
  - `docs/ROADMAP.md`

## 3. 告警配置检查实现

- 新增 `GET /api/alerts/config-check`，仅做配置就绪检查，不发送通知。
- 返回不含敏感值（`bot_token`、`chat_id`、`password`）的结果。
- 当 `alerts.enabled=false` 时返回清晰的中文说明：“告警当前已关闭，不会发送 Telegram 或 Email 通知。”
- 支持通道级缺失项：
  - Telegram：`bot_token`、`chat_id`
  - Email：`smtp_host`、`smtp_port`、`username`、`password`、`from_addr`、`to_addrs`
- 返回 `safe_to_test`、`message`、`channels[telegram|email].ready` 等字段，便于 UI 和手册展示。

## 4. Dashboard 告警卡片优化

- 告警卡片新增配置状态信息显示：
  - 告警总开关/开启状态
  - 最低告警等级
  - 冷却周期
  - 恢复通知开关
  - Telegram / Email 通道就绪状态（未开启、未就绪、可发送）
  - 测试告警是否可发送
- `Test Alert` 按钮保持原有行为，但输出明确区分“已发送”与“已跳过”。
- 不在前端展示 token / chat_id / password。

## 5. Telegram 设置与 systemd 指南

- 新增 `docs/TELEGRAM_ALERT_SETUP.md`，覆盖 Telegram 与 Email 开关、占位符、环境变量、通过 `/api/alerts/config-check` 进行预检、测试告警说明。
- 新增 `docs/ALERT_SYSTEMD_ENV.md`，说明为什么 `systemd` 场景建议用环境文件注入 secrets，并给出示例文件。
- 新增 `docs/ALERT_TEST_PLAYBOOK.md`，给出告警关闭、配置未完成、配置完整三类测试预期。

## 6. 敏感信息保护说明

- API 不返回敏感字段值；仅返回字段名列表 `missing_fields`。
- UI/脚本均不渲染 token/chat_id/password。
- 文档统一使用示例占位符：`YOUR_TELEGRAM_BOT_TOKEN`、`YOUR_TELEGRAM_CHAT_ID`、`YOUR_SMTP_PASSWORD`。
- 避免在输出、日志、测试中暴露真实 IPv4、域名、UUID、订阅链接、面板密码。

## 7. 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启代理核心/服务：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否占用 80/443：否
- 仅读配置与 API/页面展示层面，无自动重配置行为。

## 8. 测试结果

- 运行 `python -m pytest`：全部通过。
- 新增与更新测试覆盖：
  - `/api/alerts/config-check` 返回与错误场景
  - Telegram / Email 未配置时 `ready=false` 与 missing_fields
  - Dashboard 文案与脚本存在性检查
  - 文档敏感示例与安全示例主机检查
  - `/api/meta` 中新增 `alert_config_check=true`

## 9. 远端验证结果

- 执行时间：与 VPS SSH 一致
- 拉取与重启：已执行 `git pull`，`systemctl restart conan-vps-control-tower`
- `tower-status.sh`：
  - `systemctl is-active` 与 `is-enabled` 均为成功状态
  - 监听为 `127.0.0.1:3001`
  - 未发现 `0.0.0.0:3001`
- `/api/health`、`/api/diagnostics`、`/api/alerts/status` 可返回 200 JSON（当时为健康/告警关闭）
- 当前远端脚本文件尚未包含 `scripts/check-alert-config.sh`（将在本地提交并推送后再次 pull 覆盖）

## 10. 当前系统状态

- 健康监测、诊断、历史与告警链路持续运行。
- 本地-only 与端口策略与前期一致。
- 本阶段不改动代理管理策略，仅提升告警配置可观测性和文档体验。

## 11. 下一阶段建议

- Phase 1I：Real screenshot and v0.2.1-alpha
- 或 Phase 1J：Alert event history integration
