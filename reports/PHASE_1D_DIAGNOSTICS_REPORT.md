# Phase 1D Diagnostics Report

## 本阶段目标

在健康检测、风险判断和告警系统基础上，新增只读诊断建议能力，让系统说明可能问题层级、代理影响、优先检查方向，并提供安全只读命令模板。

## 新增 / 修改文件

新增：

- `app/diagnostics/`
- `docs/DIAGNOSTICS.md`
- `reports/PHASE_1D_DIAGNOSTICS_REPORT.md`
- `tests/test_diagnostics_rules.py`
- `tests/test_diagnostics_api.py`

修改：

- `app/main.py`
- `app/alerts/models.py`
- `app/alerts/formatters.py`
- `app/static/index.html`
- `app/static/styles.css`
- `app/static/app.js`
- `README.md`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/HEALTH_MODEL.md`
- `docs/REAL_VPS_CONFIG_GUIDE.md`
- `docs/ALERTING.md`
- `tests/test_alert_manager.py`

## 实现内容

- 新增 diagnostics models、commands、rules、engine、formatters。
- 新增 `/api/diagnostics`。
- Dashboard 新增 Diagnostics 区块。
- 告警事件支持 `suggested_first_check`。
- 增加只读命令安全测试。

## 关键设计理由

- 诊断模块只消费已有 health 结果，不读取额外敏感配置。
- 命令只作为字符串展示，不自动执行。
- 规则基于模块状态生成，不改变 health status。
- optional disabled 模块不作为故障。

## 对现有代理工具的影响分析

- 是否修改 3X-UI：否。
- 是否重启代理：否。
- 是否改防火墙：否。
- 是否开放公网端口：否。
- 是否占用代理端口：否。
- 是否自动执行命令：否。

## 只读命令白名单说明

允许展示 `systemctl status`、`ps`、`ss`、`curl -I`、`df -h`、`free -h`、`uptime`、`journalctl` 只读查看、`cat /proc/net/dev`、`ip addr show` 等命令模板。

## 危险命令排除说明

测试覆盖命令模板，避免出现 `restart`、`stop`、`start`、`enable`、`disable`、`rm`、`mv`、`chmod`、`chown`、`ufw`、`iptables`、`nft` 等危险词。

## 告警内容增强说明

告警文本支持一行 `Suggested first check`，不附加长命令列表，避免 Telegram / Email 刷屏。

## 测试结果

`python -m pytest` 已通过：

```text
40 passed
```

Diagnostics API smoke check 已通过：

```text
GET /api/diagnostics 200
```

## 当前系统状态

项目仍保持只读、local-only、低配 VPS 友好。Diagnostics 已加入 main，但不会执行任何命令。

## 下一阶段建议

优先建议 Phase 1E：Local-only hardening and real VPS validation。

备选建议 Phase 2：Project Control Tower。
