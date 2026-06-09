# Phase 1G: Health History and Event Log Report

## 本阶段目标

- 在不改变只读边界的前提下，增加本地健康历史与事件日志。
- 提供 24 小时稳定性摘要与状态变化记录。
- 为 Dashboard 增加“最近历史 / 最近事件”可读视图。

## 新增 / 修改文件

新增：

- `app/history/models.py`
- `app/history/store.py`
- `app/history/events.py`
- `app/history/summary.py`
- `app/history/recorder.py`
- `app/history/__init__.py`
- `docs/HEALTH_HISTORY.md`
- `docs/EVENT_LOG.md`
- `reports/PHASE_1G_HEALTH_HISTORY_AND_EVENT_LOG_REPORT.md`

修改：

- `app/main.py`
- `app/models.py`
- `app/static/app.js`
- `app/static/index.html`
- `app/static/styles.css`
- `app/config.py`
- `tests/test_config.py`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/DEMO_WALKTHROUGH.md`
- `docs/OPERATIONAL_RUNBOOK.md`
- `docs/DASHBOARD_SMOKE_TEST.md`
- `docs/HEALTH_MODEL.md`
- `README.md`

## 实现内容

- 新增历史记录配置段（默认启用）：
  - `history.enabled`, `data_file`, `event_file`, `max_snapshots`, `max_events`, `min_record_interval_seconds`, `summary_window_hours`。
- 新增快照持久化文件 `data/health_history.json` 与事件文件 `data/event_log.json`。
- `/api/history/summary` 输出窗口摘要。
- `/api/history/recent` 输出最近快照。
- `/api/events` 输出事件列表（支持 `limit` 与 `severity`）。
- `/api/health` 在读取时尝试写入快照和事件，失败时返回 warning 不影响服务可用性。
- Dashboard 新增“健康历史”区块和事件列表（最多展示 5 条）。

## 关键设计理由

- 继续沿用轻量 JSON 文件，避免数据库依赖。
- 使用写入节流避免频繁落盘。
- 只记录必要状态与文本，不记录 token、密码、chat id、真实 IP/域名。
- 将事件定义为状态变化，而不是每次心跳，降低噪音。

## 对现有代理工具影响分析

- 是否修改 3X-UI：否
- 是否重启代理：否
- 是否改防火墙：否
- 是否开放公网端口：否
- 是否占用 80/443：否
- 是否自动执行诊断命令：否

## 测试结果

- 新增/更新的历史模块和 API 使用 pytest 覆盖。
- 历史相关测试包括：
  - 文件读取/写入
  - 快照去重和裁剪
  - 状态变化事件生成
  - summary 统计
  - API 可用性
  - 前端历史文案检查

## 当前系统状态

- 本地运行正常，API 兼容性保持不变。
- Dashboard 使用简体中文，新增健康历史模块可见（若历史记录开启且有历史）。

## 下一阶段建议

### Phase 1H

- Alerting setup polish and Telegram guide

或

### Phase 1I

- Real screenshot and v0.2.1-alpha
