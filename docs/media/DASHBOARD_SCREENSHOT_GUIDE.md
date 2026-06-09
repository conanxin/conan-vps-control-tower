# Dashboard Screenshot Guide

This guide explains how to capture de-identified screenshots for README and docs.

## Access via SSH Tunnel

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Then open:

```text
http://127.0.0.1:3001
```

## Capture checklist

- Recommended file name (not committed yet):
  - `docs/media/dashboard-zh-local-only-v0.2.png`
- Current placeholder file:
  - `docs/media/dashboard-zh-local-only-v0.2.placeholder.md`
- Crop browser chrome; keep dashboard content only.
- Keep `127.0.0.1:3001` if shown.
- Do not expose real hostnames, sensitive keys, panel credentials, or account references.
- Suggested safe placeholders: `YOUR_VPS_HOST`, `YOUR_DOMAIN`.

## Suggested visible sections

- Title and top local-only runtime strip
- Overall Status
- Proxy Path
- Diagnostics Summary
- Core health cards (VPS / Proxy Core / 3X-UI / Ports)
- Active risks and optional checks
