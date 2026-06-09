# Systemd Persistence Verification

## Scope

This procedure validates local-only persistence using the project's own systemd unit.

## Validation checklist

- Checkout latest `main`.
- Run `bash scripts/deploy-local-only.sh`.
- Run `bash scripts/preflight-local-only.sh`.
- Stop temporary uvicorn process (if any).
- Install local-only service:

```bash
bash scripts/install-systemd-local-only.sh
```

- Run:

```bash
bash scripts/check-systemd-local-only.sh
```

- Confirm listener:

```bash
ss -lntup | grep 3001
```

- Run API smoke checks:

```bash
curl -s http://127.0.0.1:3001/api/health
curl -s http://127.0.0.1:3001/api/diagnostics
curl -s http://127.0.0.1:3001/api/alerts/status
```

- Check logs:

```bash
journalctl -u conan-vps-control-tower --no-pager -n 80
```

## Service expectation

`conan-vps-control-tower.service` must include:

- explicit local bind:
  - `--host 127.0.0.1`
  - `--port 3001`
- no `--host 0.0.0.0`

No 80/443 port binding by the service should be performed.

## local-only checks

- `127.0.0.1:3001` must be present.
- `0.0.0.0:3001` must be absent.
- 80/443 are monitored only for visibility and must remain unchanged.

## Journal check

- `journalctl -u conan-vps-control-tower --no-pager -n 80`

## Phase 1F real VPS result (summary)

- Phase 1F has been executed and passed on a real VPS.
- `conan-vps-control-tower` service: `installed`, `active`, `enabled`.
- local-only listener verification: `127.0.0.1:3001` present, `0.0.0.0:3001` absent.
- API smoke checks passed:
  - `/api/health` -> 200
  - `/api/diagnostics` -> 200
  - `/api/alerts/status` -> 200
- Proxy tooling impact: 3X-UI and proxy services remain unchanged, no restart actions executed.

No 3X-UI configuration or firewall changes are expected for this phase.

## Reboot recovery notes

If a VPS restart happens later, validate again by running:

```bash
systemctl status conan-vps-control-tower --no-pager
bash scripts/check-systemd-local-only.sh
```

This phase does not perform a reboot.
