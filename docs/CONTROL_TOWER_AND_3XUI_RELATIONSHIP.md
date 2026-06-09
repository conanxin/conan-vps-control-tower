# Control Tower and 3X-UI Relationship

Conan VPS Control Tower and 3X-UI can feel like one operational console, but they remain separate tools.

## Responsibility boundary

Control Tower:

- observation layer
- diagnostics layer
- alerting layer
- history and event layer
- management entry layer

3X-UI:

- proxy configuration layer
- user/inbound management layer
- panel login and management layer

## Not a replacement

Control Tower does not replace 3X-UI. It helps users understand whether the VPS, proxy core, panel, ports, domain, TLS, traffic, alerts, and diagnostics look healthy.

3X-UI remains the place where proxy configuration is changed.

## Not a fork

Control Tower is not a 3X-UI fork and does not include 3X-UI code.

## Why only a jump entry

A jump entry keeps the product experience unified while preserving technical separation. Users can inspect health in Control Tower and enter 3X-UI only when configuration work is needed.

## Future read-only integrations

If future versions read 3X-UI data, that should be a separate phase, disabled by default, and limited to read-only APIs. It should not store 3X-UI passwords, cookies, tokens, UUIDs, subscription links, or panel secrets.
