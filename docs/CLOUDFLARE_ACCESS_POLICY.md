# Cloudflare Access Policy

Cloudflare Tunnel should be paired with Cloudflare Access. Tunnel alone routes traffic; Access decides who is allowed to enter.

## Applications

Create two Access applications:

```text
tower.example.com
panel.example.com
```

Suggested mapping:

- `tower.example.com` protects Conan VPS Control Tower.
- `panel.example.com` protects the 3X-UI panel.

## Policy

Use an allow policy limited to your own email:

```text
Action: Allow
Include: Emails
Value: YOUR_EMAIL
```

Recommended session duration:

- Short personal use: 12 hours
- Trusted personal device: 24 hours
- Shared or risky device: shorter than 12 hours

## 3X-UI login remains required

Do not disable the 3X-UI login page. Cloudflare Access is an outer gate, not a replacement for the 3X-UI account/password flow.

## Do not use public bypass

Do not configure `panel.example.com` or `tower.example.com` as public bypass applications. Both should require Access authentication.

## Secrets

Do not commit Cloudflare tokens, tunnel credentials, real domains, real IPs, UUIDs, subscription links, or panel passwords.

Use placeholders in public docs:

```text
YOUR_DOMAIN
YOUR_EMAIL
YOUR_TUNNEL_ID
YOUR_3XUI_PANEL_PORT
```

## Local-only model

The origin services should remain:

```text
http://127.0.0.1:3001
https://127.0.0.1:YOUR_3XUI_PANEL_PORT
```

No public VPS port is required. No firewall change is required. No proxy service restart is required.
