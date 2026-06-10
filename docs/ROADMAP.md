# Roadmap

## Current baseline

- Current baseline: **v0.2.1-alpha**
- Project positioning: read-only, Cloudflare-protected dashboard for personal VPS proxy health.
- Core scope:
  - Control Tower handles health, diagnostics, traffic overview, and alert state visibility.
  - 3X-UI handles proxy configuration and management UI.
- Safety constraints: keep `127.0.0.1:3001` local bind and Cloudflare domain access for external entry.

## Near-term: v0.2.x maintenance line

- Keep existing features stable and reliable:
  - VPS / proxy / panel health checks
  - Diagnostics output robustness
  - Alert setup visibility and readiness
  - History and event display clarity
  - Management entry masking and CTA reliability
  - Cloudflare Access / Tunnel documentation hygiene
- Scope remains read-only monitoring and navigation entry only.
- No proxy-side mutation, no firewall changes, no public `3001` bind.

## Mid-term: v0.3.x operational polish

- Improve operational experience and documentation maturity:
  - better runbook guidance for daily check routines
  - clearer failure interpretation and first-response workflows
  - further language polish for Chinese dashboard copy
  - safer deployment and validation checks for multi-location usage
- Still no project management-plane expansion.

## Longer-term possibilities

- Small UX refinements based on field usage.
- More scenario-based runbooks for personal VPS operators.
- Optional support for additional read-only views if and only if still minimal and non-invasive.
- Maintain the rule: read-only first, no silent side effects.

## Non-goals

- Not replacing 3X-UI.
- Not editing 3X-UI configuration.
- Not restarting/redeploying proxy core from this project.
- Not changing firewall policies.
- Not exposing secrets or hidden 3X-UI paths in public UI text.
- Not becoming a generic project registry / agent command platform.
- Not creating public API calls that mutate infrastructure state.

## Design principles

- Keep local-first and privacy-first operations.
- Keep service binding local and domain access protected.
- Preserve deterministic read-only checks.
- Keep status understandable in Chinese and avoid English noise in dashboard copy.
- Keep technical debt low and avoid heavy runtime dependencies.

## Phase history

## Phase 1A: Read-Only Health Detection

- Status: implemented on `main`
- System resource checks
- Proxy process checks
- Proxy service visibility
- Port checks
- 3X-UI panel reachability
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
- Live validation: passed
- Improve local-only safety checks

## Phase 1E.1: v0.2.0-alpha Release Preparation

- Status: implemented and released
- Release notes and validation summary
- Local-only security checklist

## Phase 1F: systemd Persistence and Operational Polish

- Status: implemented on main
- Validate systemd persistence on real VPS
- Improve operational runbooks and helper scripts

## Phase 1F.2: Chinese Dashboard UX Polish

- Status: implemented on main
- Default Simplified Chinese dashboard
- Risk split for active vs optional checks
- Local runtime header and traffic percent formatting polish

## Phase 1F.3: README screenshot and demo docs

- Status: implemented on main
- Added screenshot docs and showcase notes

## Phase 1G: Health History and Event Log

- Status: implemented on main
- Add local snapshot history and event timeline
- Add `/api/history/summary`, `/api/history/recent`, `/api/events`
- Keep local JSON persistence and non-sensitive fields

## Phase 1H: Alerting setup polish and Telegram guide

- Status: implemented on main
- Alert readiness checks and local setup guidance
- Add systemd environment guidance and config-check visibility

## Phase 1K: Domain Access via Cloudflare Tunnel

- Status: implemented on main
- Domain split guidance for dashboard and management entry
- Cloudflare Access policy and tunnel config template
- Read-only discovery and readiness scripts

## Phase 1L: Unified Management Entry

- Status: implemented on main
- Read-only 3X-UI management entry in Dashboard
- Add `/api/management`
- Keep Control Tower for health/diagnostics, 3X-UI for configuration

## Phase 1L.1: Panel Protocol Detection

- Status: implemented on main
- Support panel protocol detection and recommended local target guidance

## Phase 1L.2: Management Entry URL Masking

- Status: implemented on main
- Mask hidden management paths in display text while preserving full jump target in CTA

## Phase 1L.3: Panel Health Check Repair and Diagnostics Polish

- Status: implemented on main
- Fix panel protocol/path regression and remove placeholder diagnostics command fragments

## Phase 1L.4: Dashboard Domain Access UX Polish

- Status: implemented on main
- Optimize domain-access wording and operational card layout
- Improve Cloudflare mode visibility and health history messaging

## Phase 1M: Dashboard IA Redesign and Visual System Polish

- Status: implemented on main
- Redesign information architecture for practical operational use
- Improve Chinese-first status hierarchy and layout density

## Phase 1M.1: Dashboard Runtime Hotfix and CTA Repair

- Status: implemented on main
- Resolve DOM null-safety issues and harden management CTA behavior

## Phase 1M.2: Browser verification and GitHub closure

- Status: implemented on main
- Completion checks and branch-ready closure for release prep

## Phase 1N: Acceptance Pack and Masked Screenshot Preparation

- Status: implemented on main
- Acceptance pack, release notes draft, and privacy-safe docs/media guidance

## Phase 1N.1: Add Masked Dashboard Screenshot

- Status: implemented on main
- Add masked screenshot asset and README/acceptance references

## Phase 1N.2: README Roadmap and Future Plans

- Status: implemented on this update
- Clarify long-term operating direction and explicit non-goals
- Keep roadmap focused on read-only proxy health monitoring
