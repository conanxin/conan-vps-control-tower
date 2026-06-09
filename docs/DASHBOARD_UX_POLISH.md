# Dashboard UX Polish Notes

## 设计原则

- 默认中文界面，减少个人 VPS 运维使用摩擦。
- API 字段保持英文兼容，避免破坏现有脚本与工具。
- 风险语义分层：`warning / degraded / critical` 才是活跃风险。
- `not configured` 视为中性状态，不与故障混淆。

## 风险展示分离

- `活跃风险` 只展示 warning/degraded/critical。
- `未配置的可选检查` 单独展示 Domain/DNS 和 TLS 的可选项状态。
- 用户可快速判断“真实风险”和“尚未配置项”。

## 顶部运行状态条

顶部 local-only 信息条展示：

- 运行模式：本地只读
- 绑定地址：`127.0.0.1:3001`
- 访问方式：SSH Tunnel
- 公网暴露：无

该条用于让使用者快速确认“这台 Dashboard 在什么边界下运行”。

## 代理链路与诊断摘要上移

- 代理链路展示关键依赖顺序：
  - VPS 健康
  - 代理核心
  - 3X-UI 面板可达
  - 代理端口开放
- 诊断摘要放在关键区域上方，先告诉用户“最重要的排查方向”。
- 完整诊断列表仍在下方保留详细命令。

## 文案与状态映射

- `healthy` → 健康
- `warning` → 警告
- `degraded` → 降级
- `critical` → 严重
- `unknown` → 未知
- `not configured` / `disabled` / `enabled` 采用中性到对应说明文案。

## 截图建议

当添加正式截图时，优先裁掉浏览器顶部导航条：

- 标题
- 运行状态条
- 总体状态
- 代理链路
- 诊断摘要
- 核心卡片
- 风险摘要和未配置检查项

如果截图包含命令，确保只是只读建议，不带自动执行按钮。

## 安全提醒

- `/api/meta` 不返回 token/password/chat-id。
- 告警与诊断文案不展示敏感代理参数。
- 文档中持续使用 `127.0.0.1`、`YOUR_VPS_HOST`、`YOUR_DOMAIN` 等安全占位符。
