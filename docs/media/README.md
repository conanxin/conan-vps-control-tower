# README for media assets

This folder stores masked media references and capture guidance for Conan VPS Control Tower.

## What is included

- `DASHBOARD_SCREENSHOT_GUIDE.md`: capture steps for a redacted dashboard screenshot.
- `dashboard-placeholder.md`: previous placeholder notes.
- `dashboard-zh-local-only-v0.2.placeholder.md`: placeholder for an earlier local-only screenshot.

## Screenshot policy

For `dashboard-v0.2.1-alpha.masked.png` (if provided):

- Only capture Control Tower dashboard.
- Do not capture 3X-UI backend config page.
- Avoid secrets and credential values.
- Keep placeholders and private values out of published media docs.
- Use de-identified placeholders such as `YOUR_VPS_HOST` and `YOUR_DOMAIN`.
- Do not expose raw hidden path values.
- De-identify long/public URLs to `panel.conanxin.com / 已配置隐藏路径` and `tower.conanxin.com` only.

If a masked screenshot is not available, keep the README reference in a placeholder state and avoid publishing unvetted captures.
