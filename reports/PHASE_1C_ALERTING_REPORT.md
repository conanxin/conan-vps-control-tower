# Phase 1C Alerting Report

## 本阶段目标

在现有只读健康检测和风险判断基础上，增加默认关闭的 Telegram / Email 告警能力，并支持冷却时间、告警去重、恢复通知和测试通知。

## 新增 / 修改文件

新增：

- `app/alerts/`
- `docs/ALERTING.md`
- `reports/PHASE_1C_ALERTING_REPORT.md`
- `tests/test_alert_severity.py`
- `tests/test_alert_state_store.py`
- `tests/test_alert_manager.py`
- `tests/test_alert_channels.py`
- `tests/test_alert_api.py`

修改：

- `config.example.yaml`
- `app/config.py`
- `app/main.py`
- `app/static/index.html`
- `app/static/styles.css`
- `app/static/app.js`
- `README.md`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/HEALTH_MODEL.md`
- `docs/REAL_VPS_CONFIG_GUIDE.md`
- `docs/DEPLOYMENT.md`
- `tests/test_config.py`

## 实现内容

- 新增 alerts 配置模型和环境变量占位符替换。
- 新增 severity、state store、formatter、Telegram channel、Email channel 和 AlertManager。
- 新增 `/api/alerts/status`、`/api/alerts/test`、`/api/alerts/evaluate`。
- `/api/health` 在 `alerts.enabled=true` 时安全执行告警评估。
- Dashboard 增加 Alerting 卡片和 Test Alert 按钮。

## 关键设计理由

- 告警默认关闭，避免新功能改变现有运行行为。
- 使用 JSON state 文件保存 active alerts 和 last sent metadata，避免引入数据库服务。
- 使用冷却时间和 fingerprint 去重，避免 Dashboard 刷新造成刷屏。
- Telegram 使用标准库 `urllib.request`，Email 使用标准库 `smtplib`。
- 所有发送失败返回结构化结果，不影响健康 API 和 Dashboard。

## 对现有代理工具的影响分析

- 是否修改 3X-UI：否。
- 是否重启代理：否。
- 是否改防火墙：否。
- 是否开放公网端口：否。
- 是否占用代理端口：否。

## 敏感信息处理说明

- Telegram token、chat_id、SMTP password 建议通过环境变量配置。
- API、UI、报告不输出 token、password、chat_id。
- 未配置或仍为占位符时，渠道返回 skipped，不抛异常。
- `data/alert_state.json` 被 `.gitignore` 忽略。

## 告警冷却与去重说明

- 告警 fingerprint 使用模块名和状态组成。
- 同 fingerprint 在 `cooldown_seconds` 内不会重复发送。
- 当 active alert 恢复为 healthy 且 `send_recovery=true` 时发送 recovery notification。

## 测试结果

`python -m pytest` 已通过：

```text
29 passed
```

Alert API smoke check 已通过：

```text
/api/alerts/status 200
/api/alerts/test 200
/api/alerts/evaluate 200
```

## 当前系统状态

项目仍保持轻量、只读、local-only。告警能力已加入但默认关闭，不影响未配置用户。

## 下一阶段建议

Phase 1D：Diagnostics and Suggested Actions

- 为常见风险提供只读诊断建议。
- 提供安全命令提示，但不自动执行修复。
- 继续保持不修改代理工具、不重启服务、不改防火墙。
