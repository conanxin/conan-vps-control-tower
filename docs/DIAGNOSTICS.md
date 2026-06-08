# Diagnostics and Suggested Actions

Diagnostics is a read-only explanation layer. It does not automatically repair anything, replace 3X-UI, replace human judgment, modify proxy configuration, restart services, change firewall rules, or execute commands.

Its job is to help personal VPS users decide what to inspect first.

## Inputs

Diagnostics uses existing health data from:

- `/api/health`
- `/api/system`
- `/api/proxy`
- `/api/domain`
- `/api/tls`
- `/api/traffic`
- alert event context, optionally in later phases

## Output Structure

Each diagnostic item contains:

- `diagnosis_id`
- `severity`
- `title`
- `summary`
- `impact`
- `likely_cause`
- `suggested_first_check`
- `read_only_commands`
- `related_modules`
- `confidence`
- `checked_at`

## Principles

- First decide whether proxy use is likely affected.
- Then identify the most likely layer.
- Suggest the smallest useful read-only commands.
- Do not provide repair commands.
- Do not expose sensitive information.
- Treat disabled optional modules as `Not configured`, not as failures.

## Typical Scenarios

- VPS resource risk
- Proxy core abnormal
- Proxy port not listening
- 3X-UI panel abnormal while proxy may still work
- Domain resolution failure
- Domain resolved IP mismatch
- TLS certificate approaching expiry
- TLS handshake failure
- Traffic approaching local estimate limit
- Multiple modules critical at the same time

## Read-Only Command Allowlist

Allowed examples:

- `systemctl status SERVICE_NAME --no-pager`
- `ps`
- `ss`
- `curl -I`
- `df -h`
- `free -h`
- `uptime`
- `hostnamectl`
- `journalctl -u SERVICE --no-pager -n 80`
- `cat /proc/net/dev`
- `ip addr show`

Command templates use placeholders such as `YOUR_PANEL_PORT`, `YOUR_DOMAIN`, `YOUR_PROXY_PORT`, and `SERVICE_NAME`.

## Disallowed Commands

Diagnostics must not suggest:

- `restart`, `stop`, `start`, `enable`, `disable`
- `rm`, `mv`, `chmod`, `chown`
- firewall mutations such as `ufw`, `iptables`, or `nft`
- writing config files
- installing or upgrading system packages
- any command that changes system state

## Safety

Commands are shown as text only. Conan VPS Control Tower does not execute them.
