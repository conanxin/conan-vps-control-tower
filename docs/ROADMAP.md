# Roadmap

## Phase 1A: Read-Only Health Detection

- System resource checks
- Proxy process checks
- Proxy service visibility
- Port checks
- 3X-UI panel reachability
- Basic traffic status
- Local-only dashboard

## Phase 1B: Domain / TLS / Traffic Risk Enhancement

- Status: implemented on `main`
- Optional Domain / DNS risk checks
- Optional TLS certificate expiry risk checks
- Local traffic estimate with warning, degraded, and critical thresholds
- No provider billing API integration

## Phase 1C: Telegram / Email Alerts

- Status: implemented on `main`
- Optional Telegram alerts
- Optional Email alerts
- Alert cooldowns and severity filters
- Recovery notifications and test notifications

## Phase 1D: Diagnostic Suggestions and Common Commands

- Status: implemented on `main`
- Human-readable diagnosis
- Suggested read-only commands
- Safe troubleshooting playbooks

## Phase 1E: Local-Only Hardening and Real VPS Validation

- Status: implemented on `main`
- Validate diagnostics on a real VPS
- Improve local-only safety checks
- Prepare a possible `v0.2.0-alpha`

## Phase 1E.1: v0.2.0-alpha Release Preparation

- Status: next recommended phase if real VPS validation passes
- Prepare release notes
- Add redacted screenshots
- Verify CI and docs

## Phase 2: Project Control Tower

- Track personal projects
- Lightweight service registry
- Deployment notes and status cards

## Phase 3: Information Radar and Agent Command Library

- Personal information radar
- Curated command library
- Agent-assisted operational workflows
