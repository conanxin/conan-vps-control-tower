# Changelog

## Unreleased

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
