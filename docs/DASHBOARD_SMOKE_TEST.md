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

## First screen

Confirm first screen contains:

- Product name: `Conan VPS Control Tower`
- Subtitle: `个人 VPS 代理健康控制塔`
- 外部入口: `tower.conanxin.com`
- 访问保护: `Cloudflare Access / Tunnel`
- 本地只读: `127.0.0.1:3001`
- 公网直连: `无`
- Hero status (one-line summary)
- Quick actions: `进入 3X-UI 面板`, `查看诊断`, `查看最近事件`
- Proxy path: VPS -> 代理核心 -> 3X-UI -> 端口
- Core cards for VPS / 代理核心 / 3X-UI 面板 / 端口

## Management Entry

Confirm:

- 标题: `管理入口：3X-UI 面板`
- 公开入口显示: `panel.conanxin.com / 已配置隐藏路径`
- 说明显示 `已脱敏`
- 保护方式: `Cloudflare Access + 3X-UI 登录`
- Button text: `进入 3X-UI 面板`
- Button jump target uses full `panel_public_url` from `/api/management`
- Dashboard visible text does not include raw hidden path.

## Secondary details

- Active diagnostic summary shown on healthy state:

```text
当前未发现需要处理的问题。继续保持观察即可。
```

- Optional checks and details should be in collapsible areas.
- 健康历史 shows summary and recent trend, not raw raw raw history overflow.
- 最近事件默认展示最多 5 条。

## API smoke check

```bash
curl -s http://127.0.0.1:3001/api/health | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/diagnostics | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/management | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/meta | python3 -m json.tool
curl -s http://127.0.0.1:3001/api/history/summary | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/history/recent | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/events | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/alerts/config-check | python3 -m json.tool | head -120
```

Expected:

- `/api/health` returns healthy for normal state.
- `/api/management` returns healthy and includes `panel_public_display_url`.
- `/api/meta` returns external access fields (`external_access_mode: Cloudflare Access + Tunnel`).
- `/api/meta` `panel_public_url` remains for action, display uses masked value.
- `/api/diagnostics` summary uses Chinese and avoids exposing internal panel port placeholders in the UI.

## app.js / styles versioned references

- Ensure browser references include version query for cache-safe refresh:

```text
styles.css?v=...
app.js?v=...
```

## Safety checks

- No token / password / cookie / UUID / subscription link in visible UI.
- Do not expose `panel.conanxin.com/<hidden-path>` in UI text.
- 3X-UI config unchanged.
- No proxy/service restart.
- No firewall modification.
