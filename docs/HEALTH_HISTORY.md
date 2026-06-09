# 健康历史与稳定性回看

## 它是什么

健康历史是一个轻量的本地 JSON 记录层，用于回答“这台 VPS/代理最近是否稳定”这类问题。

当前 Dashboard 会把每次 `/api/health` 的聚合结果记录为一次快照，同时在状态发生变化时记录事件。记录内容不包含敏感信息（例如 token、UUID、订阅链接、面板密码、真实域名/IP）。

## 为什么用 JSON 文件

- 轻量：不引入数据库，不增加额外服务依赖。
- 易恢复：数据文件在 `data/` 目录下可直接查看。
- 可回滚：坏文件可自动重建（会回退为安全的空列表，不会让 API 崩溃）。

## 配置说明

`config.example.yaml` 中：

```yaml
history:
  enabled: true
  data_file: "data/health_history.json"
  event_file: "data/event_log.json"
  max_snapshots: 2880
  max_events: 500
  min_record_interval_seconds: 60
  summary_window_hours: 24
```

- `enabled`：是否启用历史与事件记录。
- `data_file`：快照文件。
- `event_file`：事件文件。
- `max_snapshots`：最多保留多少条快照。
- `max_events`：最多保留多少条事件。
- `min_record_interval_seconds`：最小写入间隔，避免每次 30 秒刷新都落盘。
- `summary_window_hours`：摘要窗口，例如 `24` 表示最近 24 小时。

## 记录频率

默认按 `/api/health` 调用触发记录，并受 `min_record_interval_seconds` 限制。
当间隔太短时，会记录为“未写入，节流”。

## 可用 API

- `GET /api/history/summary`
- `GET /api/history/recent?limit=50`
- `GET /api/events?limit=50`

## 指标理解

- `healthy_ratio`：快照中 `healthy` 占比。
- `worst_status`：窗口内最差状态。
- `snapshot_count`：窗口内采样数。
- `event_count`：窗口内事件数。
- `last_problem_at` / `last_recovery_at`：最近一次异常和恢复时间。

## 限制

- 记录是本地估算，不是第三方告警数据库。
- 文件损坏时服务仍可用，但该窗口会返回 warning 并降级为空数据。

## 安全说明

- 默认不记录任何代理秘钥类信息。
- 仅保存 `status / summary / 时间` 等健康相关字段。
