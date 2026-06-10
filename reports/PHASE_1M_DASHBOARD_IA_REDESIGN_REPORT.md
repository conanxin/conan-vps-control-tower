# Phase 1M Dashboard IA Redesign and Visual System Polish Report

## 本阶段目标

将 Conan VPS Control Tower Dashboard 从功能堆叠页重构为更清晰、紧凑、中文化、适合日常查看和手机访问的个人 VPS 代理健康控制台。

本阶段只调整 Dashboard UI、展示逻辑、中文文案、前端健壮性和相关文档，不新增复杂监控功能。

## UI 问题

- 首页信息层级不够清晰，核心状态、管理入口、历史和诊断混在一起。
- 管理入口虽然可用，但不像一个明确的运维动作入口。
- 健康状态使用大面积浅绿色背景，页面显得过重。
- 健康历史里的历史最差状态容易与当前状态混淆。
- 管理入口 CTA 必须明确使用真实 `panel_public_url`，但可见文本只能展示脱敏入口。
- 部分英文健康消息需要在 UI 层统一中文化。

## 新信息架构

1. Header：产品名、外部入口、Cloudflare Access / Tunnel、本地只读地址、公网直连状态。
2. Hero 总览：总体状态、一句话摘要、关键状态 chips。
3. 快速操作：进入 3X-UI 面板、查看诊断、查看最近事件。
4. 代理链路：VPS -> 代理核心 -> 3X-UI 面板 -> 代理端口。
5. 核心状态区：VPS、代理核心、3X-UI 面板、端口。
6. 管理入口宽卡：3X-UI 面板入口、脱敏公开入口、本地入口、职责边界。
7. 流量概览：已用流量、月限额、使用率、本地估算说明。
8. 次级信息区：可选检查、告警通知、健康历史、最近事件、诊断详情。

## 管理入口 CTA 修复

- `进入 3X-UI 面板` 按钮读取 `/api/management` 的真实 `panel_public_url`。
- 点击使用 `window.open(panel_public_url, "_blank", "noopener,noreferrer")`。
- 如果弹窗被浏览器阻止，使用临时 `<a>` fallback。
- UI 展示只使用 `panel_public_display_url` 或脱敏 fallback，例如 `panel.conanxin.com / 已配置隐藏路径`。
- 不 iframe 嵌入 3X-UI，不自动登录，不保存凭据。

## 中文文案修复

- 常见健康检查英文消息在前端映射为中文。
- Hero、快速操作、管理入口、流量、诊断、历史均使用中文默认文案。
- Dashboard 主文案不再展示 `unknown`、`No active...`、`YOUR_PANEL_PORT` 或乱码。

## 健康历史优化

- 当前状态与最近 24 小时历史分开展示。
- 当前 healthy 但历史曾出现告警时，文案显示：当前状态健康；最近 24 小时曾出现告警，当前已恢复。
- 最近事件默认只显示 5 条，完整内容放在折叠区。

## 对代理影响分析

- 是否修改 3X-UI：否
- 是否重启 3X-UI：否
- 是否重启代理核心：否
- 是否修改防火墙：否
- 是否开放公网端口：否
- 是否绑定 `0.0.0.0`：否
- 是否调用 3X-UI 写接口：否
- 是否输出隐藏路径：否

## 测试结果

本地执行 `python -m pytest`：

```text
133 passed, 4 warnings
```

## 远端验证结果

已执行远端验证，仅重启 `conan-vps-control-tower.service`，未触碰 3X-UI、代理核心或防火墙。

- service 状态：active / enabled
- Control Tower 监听：`127.0.0.1:3001`
- 是否发现 `0.0.0.0:3001`：否
- `/api/health`：healthy
- `/api/management`：healthy
- `/api/management.panel_public_display_url`：`panel.conanxin.com / 已配置隐藏路径`
- `/api/management.panel_public_url`：真实完整地址存在，但报告中脱敏为 `https://panel.conanxin.com/隐藏路径`
- `/api/meta.external_access_mode`：Cloudflare Access + Tunnel
- `https://tower.conanxin.com`：HTTP 302
- `https://panel.conanxin.com`：HTTP 302
- 是否修改 3X-UI：否
- 是否重启代理：否
- 是否改防火墙：否
- 是否开放公网端口：否

## 当前状态

Phase 1M 本地实现、测试、提交、推送和远端验证均已完成。

## 下一阶段建议

Phase 1N：Masked screenshot capture and README visual refresh。
