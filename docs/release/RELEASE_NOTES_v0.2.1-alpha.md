# Conan VPS Control Tower v0.2.1-alpha

## Positioning

Cloudflare-protected Chinese VPS proxy health dashboard with a masked 3X-UI management entry.

## Highlights

- Cloudflare Access + Tunnel external access for dashboard and management entry.
- Redesigned Chinese dashboard and compact IA polish.
- Masked 3X-UI management entry to avoid hidden-path disclosure in UI.
- Runtime hotfix for management CTA and dashboard cache-resilience behavior.
- Read-only operational boundary kept for alerts, diagnostics, and health checks.
- Health / diagnostics / traffic / alert status overview with local history.
- Local-only service binding remains unchanged (`127.0.0.1:3001`).

## Safety model

- No direct public bind to `3001`.
- No 3X-UI configuration mutation.
- No proxy restart in Control Tower operations.
- No firewall policy mutation.
- No secrets or hidden paths exposed in Dashboard display.

## Validation

- pytest: all tests passed.
- Remote service: `systemctl active` + `enabled`.
- API baseline healthy:
  - `/api/health` healthy
  - `/api/management` healthy
  - `/api/diagnostics` healthy / all_healthy
- Tunnel entry points:
  - `tower.conanxin.com` returns HTTP 302 for Cloudflare Access challenge.
  - `panel.conanxin.com` returns HTTP 302/404 depending on entry path state; 302 is expected behind Access.
- Listen scope: `127.0.0.1:3001` only.

## Known limitations

- Domain/DNS and TLS optional checks may remain unconfigured.
- Traffic estimate is local only, not a billing-grade statistic.
- Alerts can be disabled.
- 3X-UI login and configuration remain separate in 3X-UI.

## Release status

Prepared only. Do not create tag or GitHub release during this phase.
