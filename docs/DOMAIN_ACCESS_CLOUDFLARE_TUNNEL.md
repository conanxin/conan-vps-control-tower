# Domain Access via Cloudflare Tunnel

Phase 1K provides a local-only safe access pattern for mobile/remote viewing:

- Do not expose `3001` to the public internet.
- Keep Control Tower binding at `127.0.0.1:3001`.
- Use Cloudflare Tunnel + Cloudflare Access for browser access.

## Recommended split hostnames

```text
tower.example.com -> http://127.0.0.1:3001
panel.example.com -> https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

Keep these hostnames separate from your proxy traffic domain.
Do not mix these Tunnel hostnames with your proxy service main domain.

## Why not Caddy/Nginx on VPS

This project avoids taking over `80/443` locally to prevent port conflicts with existing proxy/portal services.
Cloudflare Tunnel connects outbound and keeps local listeners unchanged.

## Access mode

- `tower.example.com` should go through Cloudflare Access and forward to `127.0.0.1:3001`.
- `panel.example.com` should go through Cloudflare Access and forward to the local 3X-UI panel origin (HTTPS).

If `panel.example.com` requires a hidden path, keep that path private in `config.yaml` and display only masked value on Dashboard.

## 3X-UI panel path handling

After upgrades, panel local port/path can change.
Use read-only probing to confirm current `webPort` and optional `webBasePath` in `/etc/x-ui/x-ui.db` (masked output only).

If HTTPS responds, configure Tunnel against HTTPS origin, for example:

```text
panel.example.com -> https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

If HTTPS returning `404` at a known root path, it usually means the origin path is different, not that HTTPS is unreachable.

If Cloudflare reports origin issues, keep `No TLS Verify` aligned with your local certificate mode in Cloudflare dashboard.

## Cloudflare Access policy

Create Access policies for both `tower.example.com` and `panel.example.com` and allow only your own email account.

This keeps access under identity control and avoids public bypass.

## Safety requirements

- Do not modify VPS firewall rules here.
- Do not bind Control Tower to `0.0.0.0`.
- Do not commit Cloudflare tokens.
- Do not expose raw hidden paths in public docs.
- Do not commit full panel hidden path values.

## Operational checks

```bash
bash scripts/discover-panel-and-tower-local.sh
bash scripts/check-domain-access-readiness.sh
```

These are read-only checks.

## Template

See: `deploy/cloudflare-tunnel/config.example.yml`

## After tunnel setup

Dashboard external status should show:

- 运行模式: local-only
- 外部入口: tower.conanxin.com
- 访问保护: Cloudflare Access
- 公网直连: 无

Management entry should display masked value:

- panel.conanxin.com / 已配置隐藏路径
- 已脱敏

The button still uses the full `panel_public_url` from `config.yaml`.
