# Phase 1N: Acceptance Pack and Release Prep Report

## Phase target

Prepare masked acceptance materials for `v0.2.1-alpha` candidate without adding monitoring functionality.

## Baseline

- Current branch: `main`
- Baseline commit: `62910bf` (latest stable baseline before 1N acceptance prep)

## Generated / updated files

- Added `docs/ACCEPTANCE_PACK_v0.2.1-alpha.md`
- Added `docs/release/RELEASE_NOTES_v0.2.1-alpha.md`
- Added `reports/PHASE_1N_ACCEPTANCE_PACK_RELEASE_PREP_REPORT.md` (this report)
- Updated `docs/media/README.md`
- Added/updated acceptance-oriented docs if they exist in repo edits:
  - `README.md`
  - `CHANGELOG.md`
  - `docs/DASHBOARD_SMOKE_TEST.md`
  - `docs/DEMO_WALKTHROUGH.md`
  - `docs/OPERATIONAL_RUNBOOK.md`
  - `docs/ROADMAP.md`
  - `docs/UNIFIED_MANAGEMENT_ENTRY.md`

## Acceptance results

- `python -m pytest`: `138 passed`
- Remote service checks:
  - `systemctl is-active conan-vps-control-tower`: `active`
  - `systemctl is-enabled conan-vps-control-tower`: `enabled`
  - `ss -lntup` shows `127.0.0.1:3001` only
  - no `0.0.0.0:3001` seen
- API checks:
  - `/api/health`: `healthy`
  - `/api/management`: `healthy`
  - `/api/diagnostics`: `healthy / all_healthy`
- External checks:
  - `https://tower.conanxin.com`: `302`
  - `https://panel.conanxin.com`: `302`

## Screenshot status

- No `docs/media/dashboard-v0.2.1-alpha.masked.png` committed in this phase.
- The screenshot is accepted as a later manual deliverable with de-identification requirements.
- The masked URL and de-identification requirements are documented in:
  - `docs/media/README.md`
  - `docs/media/DASHBOARD_SCREENSHOT_GUIDE.md`

## Leak checks

Executed scan on user-visible docs for banned sensitive terms and old placeholders. No banned runtime strings were introduced by this phase.

- No hidden full-path `panel.conanxin.com/<真实值>` committed in these docs.
- No internal panel-port placeholder text is retained in user-facing acceptance docs.
- No English legacy diagnostic-default sentence remains as default UI text.
- No SSH-tunnel-only wording used as default access statement for Cloudflare domain entry.
- No unknown-character placeholder remains in updated documentation.

## Impact on proxy tooling

- No 3X-UI config changes.
- No proxy service restarts.
- No firewall changes.
- No public port binding for Control Tower.

## Release prep status

- No new tags created.
- No GitHub Release created.
- Current artifacts are accepted as documentation and packaging draft for future `v0.2.1-alpha` prep.
