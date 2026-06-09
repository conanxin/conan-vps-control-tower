# Domain Access via Cloudflare Tunnel

Phase 1K documents a safe way to access Conan VPS Control Tower and the 3X-UI panel from a browser, including mobile browsers, without exposing raw VPS ports.

This phase only provides templates, checks, and guidance. It does not create a Cloudflare Tunnel, install `cloudflared`, change DNS records, or modify any proxy configuration.

## Why domain access

SSH tunnel access is the safest default, but it is inconvenient on a phone. Domain access can make the dashboard easier to reach:

- `https://tower.example.com` for Conan VPS Control Tower
- `https://panel.example.com` for 3X-UI

Both names should be protected by Cloudflare Access before they reach the local services.

## Why not expose port 3001 directly

Do not open `3001` to the public internet. The dashboard is designed to bind to `127.0.0.1:3001` and stay local to the VPS. Public exposure would weaken the local-only safety model.

## Why not use Caddy or Nginx here

This project intentionally avoids taking over `80` or `443` on the VPS because those ports may already be used by proxy services. Cloudflare Tunnel can connect outbound to Cloudflare while keeping local services on loopback addresses.

## Recommended hostnames

Use separate subdomains:

```text
tower.example.com -> http://127.0.0.1:3001
panel.example.com -> https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

Do not mix these with your proxy main domain. Keep health access and proxy traffic clearly separated.

## Cloudflare Access

Add Cloudflare Access in front of both applications and allow only your own email:

```text
Allowed email: YOUR_EMAIL
```

This prevents the dashboard or 3X-UI panel from being exposed as a public bypass page.

## Mobile access

Open this on your phone:

```text
https://tower.example.com
```

After Cloudflare Access login, the request is proxied to:

```text
http://127.0.0.1:3001
```

## 3X-UI panel access

Open:

```text
https://panel.example.com
```

Cloudflare Access should challenge first. After that, the user still needs to log in to 3X-UI. Do not disable the 3X-UI login page.

After a 3X-UI upgrade, confirm the current local panel `webPort` and hidden `webBasePath` before editing Cloudflare Tunnel routes. The tunnel target should point to the confirmed local HTTPS origin, for example:

```text
panel.example.com -> https://127.0.0.1:YOUR_PANEL_PORT
```

If the browser also needs a hidden path, keep that path private. Do not commit it to GitHub. Dashboard display should show only a masked value such as `https://panel.example.com/隐藏路径`.

The local target should be:

```text
https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

Port `2096` may be HTTPS locally. HTTP failure does not always mean the panel is unavailable. If an HTTPS probe returns `404`, the HTTPS protocol is still reachable; the root path may simply not be the login entry.

If 3X-UI uses a hidden path, do not commit that path to the repository. `panel.conanxin.com` may need the hidden path in the browser after Cloudflare Access.

Control Tower's management card masks hidden paths in the visible Dashboard text. It may show:

```text
https://panel.conanxin.com/隐藏路径
```

while the button still opens the full private `panel_public_url` from the VPS `config.yaml`.

After Cloudflare Tunnel and Cloudflare Access are configured, the Dashboard `管理入口` button can point to:

```text
https://panel.conanxin.com
```

Control Tower still does not iframe 3X-UI, automatically log in, or call any 3X-UI write API.

For details, see [Panel Protocol Detection](PANEL_PROTOCOL_DETECTION.md).

## Safety properties

- Does not occupy VPS `80` or `443`.
- Does not open public firewall ports.
- Does not bind Conan VPS Control Tower to `0.0.0.0`.
- Does not modify 3X-UI configuration.
- Does not restart 3X-UI, Xray, sing-box, V2Ray, or other proxy services.
- Does not store Cloudflare tokens in this repository.

## Template

See:

```text
deploy/cloudflare-tunnel/config.example.yml
```

Replace placeholders only on the VPS or in a private deployment environment:

- `YOUR_TUNNEL_ID`
- `tower.example.com`
- `panel.example.com`
- `YOUR_3XUI_PANEL_PORT`

## Read-only discovery

Run:

```bash
bash scripts/discover-panel-and-tower-local.sh
```

It only reads local process/listener information and prints suggested targets. It does not install `cloudflared`, create a tunnel, change firewall rules, or restart services.
