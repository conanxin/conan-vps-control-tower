# Unified Management Entry

Phase 1L adds a simple management entry inside Conan VPS Control Tower.

It lets users move from health observation to the 3X-UI panel when they need to change proxy configuration. It does not merge 3X-UI code, call 3X-UI write APIs, read panel passwords, or store login state.

## What it is

- A dashboard card named `管理入口`.
- A read-only local reachability check for the 3X-UI panel.
- A button that opens the configured public panel URL, such as `https://panel.conanxin.com`.

## What it is not

- Not a 3X-UI fork.
- Not a code-level merge with 3X-UI.
- Not a replacement for the 3X-UI login page.
- Not an iframe embed.
- Not an automatic login flow.
- Not a writer for proxy configuration.

## Why not merge code

Control Tower and 3X-UI have different responsibilities:

- Control Tower observes health, risks, alerts, diagnostics, and entry points.
- 3X-UI manages proxy configuration.

Keeping them separate reduces risk and avoids touching working proxy services.

## Why not iframe 3X-UI

Embedding 3X-UI in an iframe can create confusing login behavior and browser security issues. A normal link keeps the boundary clear and lets Cloudflare Access and the 3X-UI login page work naturally.

## Why not call 3X-UI write APIs

This project is intentionally read-only. Writing proxy configuration from Control Tower would create a new failure surface and could disrupt a working proxy node.

## How to use

1. Open Control Tower and check overall status.
2. Read diagnostics if there is a warning, degraded, or critical state.
3. If configuration changes are needed, click `进入 3X-UI 面板`.
4. Log in through Cloudflare Access and then 3X-UI.

Example access model:

```text
tower.conanxin.com -> Control Tower
panel.conanxin.com -> 3X-UI
```

For local target detection, port `2096` may need HTTPS:

```text
https://127.0.0.1:2096
```

HTTP failure does not always mean the panel is unavailable. HTTPS returning `404` can still prove the protocol is reachable while the root path is not the login path.

If 3X-UI uses a hidden path, do not commit that path to this repository.

## Public URL masking

`management.panel_public_url` may include the full 3X-UI hidden path in a private `config.yaml` on the VPS. Do not commit that value to GitHub.

The Dashboard uses `panel_public_display_url` for display:

```text
https://panel.conanxin.com/隐藏路径
```

The `进入 3X-UI 面板` button still uses the full `panel_public_url` so the entry remains usable. The masked display value is only for UI presentation.

## Domain access UX polish

When Cloudflare Tunnel and Cloudflare Access are active, the Dashboard should present the management entry as a domain-access console rather than a local debug page:

- Control Tower entry: `tower.conanxin.com`
- Panel entry display: `panel.conanxin.com / 已配置隐藏路径`
- Access protection: Cloudflare Access + 3X-UI login
- Direct public bind: none

The full hidden path can stay in the private VPS `config.yaml` as `management.panel_public_url`, but visible Dashboard text must use `panel_public_display_url` or an equivalent masked value. Do not show the real hidden path in screenshots, reports, issues, or docs.

## Phase 1M Dashboard placement

The management entry is now a dedicated wide card near the top of the Dashboard, after the proxy path and before secondary details. It is intentionally more prominent than optional checks because it is the natural action after reading health state.

The card still keeps the same boundary:

- Button uses the full private `panel_public_url`.
- Visible text uses `panel_public_display_url`.
- No iframe.
- No automatic login.
- No 3X-UI write API calls.
- No password, cookie, token, UUID, or subscription link storage.

## Health check URL and hidden path

The management entry and the health checker have different jobs:

- `management.panel_public_url` is used by the Dashboard button.
- `proxy.panel.url` is used by the read-only `xui_panel` health check.

After a 3X-UI upgrade, the panel `webPort` or hidden `webBasePath` may change. Update only Control Tower's private VPS `config.yaml` after confirming the current value from `/etc/x-ui/x-ui.db`.

Do not commit the real hidden path. In documentation or reports, write only masked examples such as:

```text
https://127.0.0.1:YOUR_PANEL_PORT/<hidden>/
https://panel.conanxin.com/隐藏路径
```

Recommended protection:

```text
Cloudflare Access + 3X-UI login
```

## Safety

- Does not modify 3X-UI.
- Does not restart proxy services.
- Does not change firewall rules.
- Does not expose raw local ports.
- Does not save passwords, cookies, tokens, UUIDs, or subscription links.
