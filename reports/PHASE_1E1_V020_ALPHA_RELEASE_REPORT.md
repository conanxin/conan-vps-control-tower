# Phase 1E.1 v0.2.0-alpha Release Report

## Stage Goal

Prepare `v0.2.0-alpha` after Phase 1B, 1C, 1D, 1E, and Phase 1E-Live validation.

## Modified Files

- `README.md`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `pyproject.toml`
- `reports/PHASE_1E_LOCAL_ONLY_HARDENING_AND_VPS_VALIDATION_REPORT.md`

## Added Files

- `docs/release/RELEASE_NOTES_v0.2.0-alpha.md`
- `reports/PHASE_1E1_V020_ALPHA_RELEASE_REPORT.md`

## Release Rationale

`v0.2.0-alpha` captures the project after external dependency risk checks, alerting, diagnostics, local-only hardening, and successful real VPS validation.

## Included Features

- Domain / TLS / Traffic risk checks.
- Telegram / Email alerting.
- Diagnostics and suggested read-only actions.
- Local-only hardening scripts.
- Real VPS validation documentation.

## Real VPS Validation Summary

- OS: Ubuntu 24.04 LTS.
- Python: 3.12.3.
- Project commit: `1ed4daf`.
- Run mode: temporary uvicorn.
- Bind: `127.0.0.1:3001`.
- Public bind: no.
- Health: healthy.
- Diagnostics: all_healthy.
- Alerts: disabled.
- 3X-UI modified: no.
- Proxy restarted: no.
- Firewall changed: no.
- Public port opened: no.

## Safety Boundary

- No 3X-UI configuration changes.
- No proxy restart.
- No firewall changes.
- No public port exposure.
- No real IP, domain, token, UUID, subscription link, or panel password committed.

## Test Results

`python -m pytest` passed:

```text
45 passed
```

## Tag Status

Created and pushed:

```text
v0.2.0-alpha
```

## Release Status

GitHub prerelease created:

```text
https://github.com/conanxin/conan-vps-control-tower/releases/tag/v0.2.0-alpha
```

## Current System State

The repository is ready for `v0.2.0-alpha` release preparation.

## Next Stage Recommendation

Phase 1F: systemd persistence and operational polish.

Alternative: Phase 2, Project Control Tower foundation.
