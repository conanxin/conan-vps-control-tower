# Panel Protocol Detection

Phase 1L.1 improves local 3X-UI panel protocol detection.

Some 3X-UI panel ports answer differently depending on whether the client uses HTTP or HTTPS. A plain HTTP probe can fail even when the panel port is alive.

## Confirmed example

For local port `2096`:

```bash
curl -I --max-time 5 http://127.0.0.1:2096
```

may fail with:

```text
Unsupported HTTP version in response
```

But:

```bash
curl -k -I --max-time 5 https://127.0.0.1:2096
```

may return:

```text
HTTP/1.1 404 Not Found
Content-Type: text/plain
```

The `404` does not mean the HTTPS protocol is unavailable. It means the HTTPS origin answered, while the root path may not be the actual 3X-UI login path.

## Recommended local target

Use:

```text
https://127.0.0.1:2096
```

For Cloudflare Tunnel:

```text
panel.example.com -> https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

If 3X-UI uses a self-signed local certificate, Cloudflare Tunnel may need origin TLS verification disabled or the matching origin TLS option configured in the Cloudflare Zero Trust dashboard.

## Hidden paths

If 3X-UI uses a hidden path, do not commit that path to this repository. Keep it private and configure it only in your private Cloudflare or browser workflow.

`panel.conanxin.com` may need the 3X-UI hidden path when accessed in a browser.

## After 3X-UI upgrades

3X-UI upgrades can change the effective local panel port or hidden `webBasePath`. If the proxy network still works but Control Tower reports `xui_panel` as abnormal, verify the current 3X-UI panel settings with read-only checks before changing Control Tower's own `config.yaml`.

The current `webPort` and `webBasePath` may be read from `/etc/x-ui/x-ui.db`. Do not print or commit the full hidden path. In reports, show only a masked value such as `/p-2...3f2/ len=52`.

For local HTTPS panel checks:

- `200`, `301`, `302`, `307`, `401`, and `403` mean the panel endpoint is reachable.
- `404` means the HTTPS protocol is reachable but the configured path may be wrong.
- HTTP failure does not necessarily mean the panel is down.

If the hidden path is required, configure only the private VPS `config.yaml`, for example:

```yaml
proxy:
  panel:
    url: "https://127.0.0.1:YOUR_PANEL_PORT/<hidden>/"
```

Do not commit the real hidden path to GitHub.

## What Control Tower detects

`/api/management` returns:

- `detected_scheme`
- `recommended_local_url`
- `protocol_warning`
- `tcp_reachable`

If the current config uses `http://127.0.0.1:2096` but HTTPS appears to answer, Control Tower returns `protocol_warning=true` and recommends `https://127.0.0.1:2096`.

## Safety boundary

Protocol detection is read-only:

- no 3X-UI login
- no cookie read
- no token read
- no write API calls
- no proxy config changes
- no service restarts
