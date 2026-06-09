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
