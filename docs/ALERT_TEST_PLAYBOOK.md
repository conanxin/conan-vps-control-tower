# Alerting Test Playbook

Use this playbook to verify alerting setup safely.

## 1. Open local-only check points

```bash
ssh -L 3001:127.0.0.1:3001 dmit-control-tower
```

Open:

```text
http://127.0.0.1:3001
```

## 2. Check alert config

```bash
curl -s http://127.0.0.1:3001/api/alerts/config-check | python3 -m json.tool | head -120
curl -s http://127.0.0.1:3001/api/alerts/status | python3 -m json.tool | head -120
```

Expected:

- `alerts.config.enabled=false` -> test button should show skipped.
- `channels.telegram.ready=false` if token/chat_id missing.
- `channels.email.ready=false` if email fields are incomplete.

## 3. Trigger manual evaluation (no external actions)

```bash
curl -X POST http://127.0.0.1:3001/api/alerts/evaluate
```

If no channel is ready, no notification should be sent.

## 4. Test notification (only after readiness)

```bash
curl -X POST http://127.0.0.1:3001/api/alerts/test
```

Expected:

- If channels are not ready, response should include skipped details.
- If channels are ready, you should receive a test message and the service log
  should record a send attempt.

## 5. Optional logs

```bash
bash scripts/tower-logs.sh
```

You can also run:

```bash
bash scripts/tower-logs.sh follow
```

## 6. Cron recommendation

```text
*/5 * * * * curl -s -X POST http://127.0.0.1:3001/api/alerts/evaluate >/dev/null 2>&1
```

`cooldown_seconds` will prevent repeated alerts from short poll intervals.

## Constraints

- No public dashboard exposure.
- No firewall or proxy-service restart is needed.
- Test playbook only validates local service behavior.

