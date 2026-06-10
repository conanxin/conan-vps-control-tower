# Dashboard Smoke Test

Use this checklist after local deployment, Cloudflare Tunnel updates, or Dashboard UI changes.

## Access

Preferred domain access:

```text
https://tower.conanxin.com
```

Fallback SSH tunnel:

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

## First Screen

Confirm the first screen contains:

- Product name: Conan VPS Control Tower
- Subtitle: 个人 VPS 代理健康控制塔
- 外部入口：`tower.conanxin.com`
- 保护方式：Cloudflare Access / Tunnel
- 本地只读：`127.0.0.1:3001`
- 公网直连：无
- Hero 总体状态
- 快速操作：进入 3X-UI 面板、查看诊断、查看最近事件
- 代理链路
- 核心状态卡：VPS、代理核心、3X-UI 面板、端口

## Management Entry

Confirm:

- 管理入口：3X-UI 面板
- 公开入口：`panel.conanxin.com / 已配置隐藏路径`
- 已脱敏
- 本地入口：HTTPS + local address
- 保护方式：Cloudflare Access + 3X-UI 登录
- 职责边界：Control Tower 不读取或修改 3X-UI 配置
- Button: `进入 3X-UI 面板`

The visible Dashboard must not show the real 3X-UI hidden path. The button may open the full private `panel_public_url`.

## Secondary Details

Confirm details/accordion sections exist:

- 可选检查
- 告警通知
- 健康历史
- 最近事件
- 诊断详情

When healthy, the diagnostic summary should say:

```text
当前未发现需要处理的问题。继续保持观察即可。
```

## API Smoke Check

```bash
curl -s http://127.0.0.1:3001/api/health | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/diagnostics | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/management | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/meta | python3 -m json.tool
curl -s http://127.0.0.1:3001/api/history/summary | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/history/recent | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/events | python3 -m json.tool | head -120
```

Expected:

- `/api/health` returns healthy when the node is healthy.
- `/api/diagnostics` returns all_healthy when no issues exist.
- `/api/management` returns healthy and masks `panel_public_display_url`.
- `/api/meta` returns `external_access_mode: Cloudflare Access + Tunnel`.
- `/api/history/summary` and `/api/history/recent` return health history without secrets.
- `/api/events` returns recent health events without secrets.
- No token, password, cookie, UUID, subscription link, or real hidden path is shown in visible UI.

## Safety

This smoke test does not modify 3X-UI, restart proxy services, change firewall rules, open public ports, or bind Control Tower to `0.0.0.0`.
