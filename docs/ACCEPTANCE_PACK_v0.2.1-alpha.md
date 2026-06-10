# Conan VPS Control Tower v0.2.1-alpha acceptance candidate

## Version candidate

Conan VPS Control Tower v0.2.1-alpha acceptance candidate

## Scope

- Chinese Dashboard with compact personal VPS operation layout
- Cloudflare Access + Tunnel domain access
- Unified management entry to 3X-UI
- Masked 3X-UI public link display
- VPS health checks and panel/core/path diagnostics
- Health history and event summary
- Alert readiness / alert status visibility

## Current ability

- VPS health checks (CPU / memory / load, process / service checks)
- Proxy core visibility
- 3X-UI panel reachability check (`https` local target)
- Proxy port checks
- Optional Domain / DNS checks
- Optional TLS checks
- Local traffic estimation
- Diagnostics with suggested actions
- Health history and event logs
- Alert configuration/readiness status
- Management entry with masked URL and safe CTA

## Access model

- Control Tower: `https://tower.conanxin.com`
- 3X-UI management entry: enter via Dashboard button
- Protection: Cloudflare Access + Tunnel
- Service bind: `127.0.0.1:3001`

## Safety boundary

- Read-only for health, diagnostics, and alert status.
- Does not modify 3X-UI configuration.
- Does not call 3X-UI write APIs.
- Does not store 3X-UI password, cookie, token, UUID, subscription link.
- Does not expose real hidden path in UI.
- Does not expose local port `3001` to public.
- Does not modify firewall rules.
- Does not restart proxy core services.

## Acceptance results (baseline)

- `python -m pytest`: 138 passed
- Remote service:
  - `systemctl is-active conan-vps-control-tower`: `active`
  - `systemctl is-enabled conan-vps-control-tower`: `enabled`
  - `ss -lntup` only shows `127.0.0.1:3001`, no `0.0.0.0:3001`
- API checks:
  - `/api/health`: `healthy`
  - `/api/management`: `healthy`
  - `/api/diagnostics`: `healthy / all_healthy`
- External entry status:
  - `https://tower.conanxin.com` -> HTTP 302
  - `https://panel.conanxin.com` -> HTTP 302

## Known limitations

- Optional Domain / TLS checks may remain unconfigured.
- Local traffic estimate is only local OS traffic, not provider billing.
- Alerts may be disabled by design.
- 3X-UI login remains in 3X-UI.

## Screenshot status

- Masked dashboard screenshot added after release publication:
  - `docs/media/dashboard-v0.2.1-alpha.masked.png`
- The screenshot is masked and only exposes `panel.conanxin.com / 已配置隐藏路径`.
