# 事件日志

## 事件是什么

事件日志是对状态变化的“只读快照记录”。

当健康状态发生变化（例如 `healthy -> warning`）时，系统会写入一条事件。
当状态恢复为健康时，会写入 `recovery` 类事件，帮助快速确认“是否已恢复”。

## 哪些变化会生成事件

- 总体状态变化（如 `healthy` 到 `warning / degraded / critical`）
- 总体恢复（`warning/degraded/critical -> healthy`）
- `proxy_core` 变成异常
- `proxy_ports` 变成异常
- `panel` 变成异常
- `traffic` 变成 warning/degraded/critical
- `domain_dns` 在启用时由异常变为异常或恢复时生成事件
- `tls_certificate` 在启用时由异常变为异常或恢复时生成事件
- `diagnostics` 由异常变更为更严重或恢复时生成事件

## 去重

事件以 `fingerprint` 去重。
相同故障如果在下一次健康周期中持续存在，不重复写入同类事件，避免“噪音淹没”。

## Recovery event

`is_recovery=true` 的事件表示状态已恢复，便于与“新故障”区分。

## 查看 API

- `GET /api/events?limit=50`
- `GET /api/events?severity=critical`

## 为什么只记录状态变化

不记录每次 `/api/health` 轮询内容，可以减少 I/O，并把日志聚焦于“需要关注的变化”。

## 不自动修复

事件日志只读，不执行任何修复动作。
