# Demo Walkthrough

## 这是什么项目

Conan VPS Control Tower 是一个面向个人 VPS 代理节点的只读健康观察面板，不是项目管理系统。

- 目标：展示 VPS、核心代理、面板、端口、域名、TLS、流量、告警与诊断状态。
- 不做自动修复，仅给出只读判断与建议。

## 它不是什么

- 不会管理多个 GitHub 项目
- 不会替代 3X-UI
- 不会改写代理配置
- 不会公开监听 80/443（默认仅 `127.0.0.1:3001`）

## 如何打开 Dashboard

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

浏览器打开：

```text
http://127.0.0.1:3001
```

## 第一屏怎么看

1. 顶部 `总体状态`：整体健康等级。
2. `代理链路`：VPS -> 代理核心 -> 面板可达 -> 端口开放。
3. `活跃风险`：只列出 warning/degraded/critical，不把未配置项目视为风险。
4. `诊断摘要`：给出首要异常、影响和建议的先做检查。
5. `健康历史`：最近 24 小时稳定性、快照数量、事件数量、最后异常/恢复。

## 理解总体状态

- `healthy`: 当前主观健康。
- `warning/degraded/critical`: 需要核对对应模块。
- `unknown`: 有检查项不可判定。

## 理解代理链路

链路为代理核心可用性的快速阅读：
- `VPS 健康`异常通常是底层资源问题
- `代理核心状态`异常通常表示进程未见到/状态不佳
- `3X-UI 面板状态`异常通常是管理面板不可达
- `端口状态`异常通常会影响客户端连接

## 理解活跃风险

`活跃风险`卡片只显示有影响的问题，不会把“未配置”当作故障。

## 理解未配置检查项

`域名 / DNS`、`TLS 证书`默认可以未配置。显示为“未配置”时，表示本次不参与总体风险评估。

## 理解诊断建议

诊断来自当前 health + diagnostics 引擎，提供：
- 影响说明
- 优先级建议
- 只读命令（不会执行）

## 理解告警关闭

默认告警关闭。关闭时按钮/提示应显示“未开启”，`/api/alerts/status` 返回 `enabled: false`。

## 理解告警配置状态

在 `告警通知` 区域可看到：

- 告警总开关是否开启
- Telegram / Email 是否开启
- 每个渠道是否已就绪
- 缺少哪些字段

检查方式：

```bash
curl -s http://127.0.0.1:3001/api/alerts/config-check | python3 -m json.tool | head -120
```

如果配置未开启，页面通常会提示“告警当前已关闭，不会发送通知”。
如果通道开启但未完整配置，页面会提示“缺少必要配置”。
`safe_to_test` 为 `false` 表示不能直接发测试通知。

## 从 Dashboard 进入 3X-UI

`管理入口` 区块提供 `进入 3X-UI 面板` 按钮。

- Control Tower 负责看状态、风险、诊断和告警。
- 3X-UI 负责修改代理配置。
- 点击按钮会打开 `panel_public_url`，例如 `https://panel.conanxin.com`。
- Control Tower 不 iframe 嵌入 3X-UI，不自动登录，不保存 3X-UI 密码。

## 如何确认没有公网暴露

```bash
ss -lntup | grep 3001
```

应看到 `127.0.0.1:3001`；不应看到 `0.0.0.0:3001`。

## 常用命令

```bash
bash scripts/tower-status.sh
bash scripts/tower-logs.sh
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

## 健康历史怎么用

- `GET /api/history/summary` 看最近 24 小时趋势。
- `GET /api/history/recent` 查看最近快照。
- `GET /api/events` 查看状态变化事件（支持 `severity` 过滤）。
