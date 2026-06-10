# Unified Management Entry

Phase 1L keeps Clear responsibility separation: Control Tower is for health observation; 3X-UI is for configuration.

## What it is

Control Tower provides one read-only entry path to jump from health view into 3X-UI:

- It does not merge 3X-UI code.
- It does not call write APIs.
- It does not save credentials.
- It does not replace the 3X-UI login.

UI behavior:

- Show management state card.
- Show masked public entry text, e.g. `panel.conanxin.com / 已配置隐藏路径`.
- Show a warning label: `已脱敏` when a masked path is used.
- `进入 3X-UI 面板` opens the actual configured `panel_public_url` in a new tab.

## Why this boundary exists

- Keep project focus on personal VPS health observation.
- Avoid creating a second control plane.
- Avoid affecting proxy runtime.
- Avoid exposing sensitive panel paths in visible UI.

## How to use

1. Open Control Tower.
2. Read overall status and core cards first.
3. If configuration change is needed, use:

```text
panel.conanxin.com / 已配置隐藏路径
进入 3X-UI 面板
```

4. Complete login in Cloudflare Access and then in 3X-UI normally.

## Security model

- Dashboard path is read-only and shows monitoring state.
- 3X-UI panel configuration changes still happen in 3X-UI.
- No iframe embedding, no auto-login.
- No sensitive fields in API/UI logs.

## Domain access view

When Cloudflare Tunnel + Access is used:

- Control Tower entry: `tower.conanxin.com`
- Panel entry text: `panel.conanxin.com / 已配置隐藏路径`
- Protection: Cloudflare Access + 3X-UI login
- 直接公网: 无

## 3X-UI upgrade note

If `webPort` or path changes after upgrade:

- Keep using read-only checks only.
- Update only Control Tower private `config.yaml` values.
- Never commit real hidden path values.

Use masked samples only:

```text
https://panel.conanxin.com/已配置隐藏路径
```
