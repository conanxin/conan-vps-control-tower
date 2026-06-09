# Changelog`r`n## Unreleased

### Phase 1K Domain Access via Cloudflare Tunnel

- Added Cloudflare Tunnel domain access guide for phone/browser access.
- Added Cloudflare Access policy guide for `tower.example.com` and `panel.example.com`.
- Added tunnel config template under `deploy/cloudflare-tunnel/`.
- Added read-only local discovery and domain-access readiness scripts.
- Kept the project local-only by default and did not create tunnels or store tokens.

### Phase 1L Unified Management Entry

- Added read-only 3X-UI management entry configuration.
- Added `/api/management` for local panel reachability and safe entry metadata.
- Added Dashboard `管理入口` card with `进入 3X-UI 面板` button.
- Added docs explaining the Control Tower / 3X-UI responsibility boundary.
- Kept 3X-UI configuration, credentials, cookies, and write APIs untouched.

### Phase 1L.1 Panel Protocol Detection Polish

- Added HTTPS fallback detection for local 3X-UI panel ports.
- Added `detected_scheme`, `recommended_local_url`, `protocol_warning`, and `tcp_reachable` to `/api/management`.
- Updated default local panel target to `https://127.0.0.1:2096`.
- Updated Cloudflare Tunnel template to use HTTPS for the 3X-UI panel origin.
- Added Dashboard protocol warning for mismatched local panel protocol.

### Phase 1L.2 Management Entry URL Masking

- Added `panel_public_display_url` for masked Dashboard display.
- Kept `panel_public_url` for the management button target.
- Masked hidden paths as `/隐藏路径` in the management entry card.
- Added long URL overflow protection in the Dashboard management card.
- Updated docs to keep 3X-UI hidden paths out of GitHub.

### Phase 1H Alerting setup polish

- Added non-intrusive alert config diagnostics endpoint `/api/alerts/config-check`.
- Added dashboard readiness fields for Telegram / Email and test-availability hints.
- Added systemd alert environment guidance and Telegram setup documentation.
- Added safe alert test playbook and local config-check script.
- Added alert configuration visibility to dashboard for missing fields and readiness.
- `/api/meta` now includes `alert_config_check`.

### Phase 1G Health History and Event Log

- Added health snapshot recorder and event logger with local JSON persistence.
- Added snapshot and event retention (`max_snapshots` / `max_events`).
- Added event dedupe and recovery detection on status transitions.
- Added dashboard Health History panel for 24h summary and recent events.
- Added docs for history/event usage and kept project scope on personal VPS / proxy monitoring.

### Phase 1F.3 README screenshot and demo docs

- Added screenshot guidance for SSH-tunnel based local-only display.
- Added README screenshot placeholder and media documentation workflow.
- Added demo walkthrough for first-run interpretation.
- Added README showcase note for display strategy and 30-second onboarding.

### Phase 1F.2 Dashboard UX polish

- Chinese dashboard by default, with English API payload retained for compatibility.
- Added dedicated optional-check and active-risk split.
- Added proxy path summary and diagnostics summary placement above full diagnostics panel.
- Improved traffic percent formatting for very low values.
- Added neutral styling for not-configured / disabled checks.
- Added lightweight `/api/meta` for local-only runtime display.

### Phase 1F.1 Operational Polish

- Added `scripts/tower-status.sh` for one-command local-only status and API checks.
- Added `scripts/tower-logs.sh` for fast project log viewing and follow mode.
- Added `scripts/tower-stop-temporary-uvicorn.sh` to stop only `uvicorn app.main:app --host 127.0.0.1 --port 3001`.
- Updated operational runbook and persistence verification docs for operational clarity.

## v0.2.0-alpha

### Domain / TLS / Traffic Risk

- Added optional Domain / DNS checker.
- Added optional TLS certificate expiry checker.
- Enhanced traffic checking with local interface baseline estimates and warning/degraded/critical thresholds.
- Added `/api/domain`, `/api/tls`, and `/api/traffic`.

### Telegram / Email Alerting

- Added optional alerting configuration, disabled by default.
- Added Telegram and Email / SMTP channels using lightweight clients.
- Added alert severity filtering, cooldown, fingerprint dedupe, recovery notifications, and test notifications.
- Added `/api/alerts/status`, `/api/alerts/test`, and `/api/alerts/evaluate`.

### Diagnostics and Suggested Actions

- Added read-only diagnostics engine and rule set.
- Added `/api/diagnostics`.
- Added Dashboard Diagnostics section with impact, likely first check, related modules, confidence, and read-only commands.

### Local-Only Hardening

- Added local-only preflight script.
- Added redacted live VPS status collection script.
- Added systemd local-only documentation.
- Added real VPS validation checklist and Dashboard smoke test guide.

### Real VPS Validation

- Passed real VPS validation on Ubuntu 24.04 LTS with Python 3.12.3.
- Verified temporary uvicorn on `127.0.0.1:3001`.
- Confirmed no `0.0.0.0:3001` public bind.
- Confirmed no 3X-UI modification, no proxy restart, no firewall change, and no public port opening.

### Phase 1E Local-Only Hardening and Real VPS Validation

- Added local-only preflight script.
- Added redacted live VPS status collection script.
- Added systemd local-only documentation.
- Added real VPS validation checklist and Dashboard smoke test guide.
- Added tests for local-only safety defaults and documentation examples.

### Phase 1D Diagnostics and Suggested Actions

- Added read-only diagnostics engine and rule set.
- Added `/api/diagnostics`.
- Added Dashboard Diagnostics section with impact, likely first check, related modules, confidence, and read-only commands.
- Added safety documentation for allowed and disallowed diagnostic commands.
- Alert formatter now supports a concise suggested first check line.

### Phase 1C Telegram / Email Alerting

- Added optional alerting configuration, disabled by default.
- Added Telegram and Email / SMTP channels using lightweight standard-library clients.
- Added alert severity filtering, cooldown, fingerprint dedupe, recovery notifications, and test notifications.
- Added `/api/alerts/status`, `/api/alerts/test`, and `/api/alerts/evaluate`.
- Added Dashboard alerting card without exposing tokens, passwords, or chat IDs.
- Added alerting documentation and tests.

### Phase 1B Domain / TLS / Traffic Risk Enhancement

- Added optional Domain / DNS checker.
- Added optional TLS certificate expiry checker.
- Enhanced traffic checking with local interface baseline estimates and warning/degraded/critical thresholds.
- Added `/api/domain`, `/api/tls`, and `/api/traffic`.
- Updated dashboard cards for Domain / DNS, TLS Certificate, and Traffic Risk.
- Added documentation for Domain / TLS / Traffic risk configuration and limitations.
- Kept checks read-only, local-only, and disabled by default where optional.

## v0.1.0-alpha

### Phase 0 Bootstrap

- Created the open-source project structure.
- Added README, MIT License, gitignore, environment example, configuration example, pyproject, and project docs.
- Documented the product requirements, architecture, health model, roadmap, deployment notes, and open-source plan.

### Phase 1A Read-Only Proxy Health Dashboard MVP

- Added FastAPI app with `/`, `/api/health`, `/api/system`, and `/api/proxy`.
- Added read-only checkers for VPS resources, proxy processes, systemd service visibility, 3X-UI panel reachability, proxy ports, and basic traffic counters.
- Added health evaluator for `overall_status`, `readable_summary`, and `risk_summary`.
- Added native HTML/CSS/JS dashboard with 30-second refresh.
- Added install, uninstall, dev-run, and systemd scripts.
- Added pytest coverage for evaluator logic, port checks, and config defaults.

### Known Limitations

- Traffic uses system counters since boot, not precise monthly billing records.
- Service checks depend on `systemctl` and return `unknown` on unsupported platforms.
- Panel checks only test HTTP reachability and do not log in.
- Default port checks are local to `127.0.0.1`.

### Next Planned Phases

- Phase 1A.2: Live VPS deployment verification.
- Phase 1B: Traffic, domain, TLS, and expiration reminders.
- Phase 1C: Telegram / Email alerts.
- Phase 1D: Diagnostic suggestions and common commands.

