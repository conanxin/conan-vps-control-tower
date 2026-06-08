# SSH Tunnel Access

Conan VPS Control Tower defaults to `127.0.0.1:3001`. This means it is reachable only from the VPS itself unless you create an SSH tunnel.

The project is a read-only health observation layer. It does not replace 3X-UI, modify proxy configuration, restart proxy services, change firewall rules, or open public ports.

## Windows to VPS Tunnel

From local Windows PowerShell or Windows Terminal:

```bash
ssh -L 3001:127.0.0.1:3001 root@YOUR_VPS_HOST
```

Then open this URL in your local browser:

```text
http://127.0.0.1:3001
```

## Notes

- No public port needs to be opened.
- No firewall rule needs to be changed.
- No reverse proxy is needed.
- No Nginx, Caddy, Cloudflare Tunnel, or Docker is required for Phase 1A.2.
- Closing the SSH window disconnects the tunnel.
- If local port `3001` is already used, choose another local port:

```bash
ssh -L 3002:127.0.0.1:3001 root@YOUR_VPS_HOST
```

Then open:

```text
http://127.0.0.1:3002
```

Do not post real VPS hostnames, IP addresses, private domains, tokens, UUIDs, passwords, subscription links, or proxy plaintext in public issues or reports.
