# Health Model

## Status Levels

### healthy

The check is passing and no immediate risk is visible.

### warning

The check is still usable, but one or more indicators are close to a configured threshold.

### degraded

The service or system is partially impaired. User traffic may be affected, but the node may still be usable.

### critical

The check indicates a serious failure or a likely outage.

### unknown

The checker could not determine status due to missing permissions, unavailable tools, unsupported platform behavior, timeout, or another contained error.

## Checker Return Shape

Every checker should return a structure similar to:

```json
{
  "name": "proxy_core",
  "status": "healthy",
  "message": "Proxy core process is running",
  "checked_at": "ISO8601",
  "details": {},
  "ignored": false
}
```

Optional checks such as Domain / DNS and TLS Certificate can be disabled. Disabled checks return `status: "unknown"` with `ignored: true`, remain visible in API/UI output, and do not affect `overall_status`.

## Aggregation Rule

Overall health uses the most severe status observed:

```text
critical > degraded > warning > unknown > healthy
```

`unknown` is treated as visible risk, but not worse than a known warning, degraded state, or critical failure.

Ignored optional checks are excluded from this aggregation rule.

## Alerting Severity

Phase 1C alerting can trigger for:

```text
warning, degraded, critical
```

`unknown` does not trigger alerts in Phase 1C. Alerting is disabled by default and only sends when `alerts.enabled=true`, at least one channel is configured, and status is at or above `alerts.min_severity`.

## Diagnostics

Diagnostics uses health status and severity as input, but it does not change health status. It is an explanation layer that generates likely cause, impact, suggested first check, and read-only command templates.

Disabled optional checks are treated as not configured, not as diagnostic failures.

## History and Event Status

History is an independent local layer and does not affect real-time `overall_status`.

- `snapshot`: one health sampling, generated during check cycle.
- `event`: a status-change record (for example `healthy -> warning`, recovery).
- `status`: health summary status used in UI only; it is derived from the selected summary window.

Unknown or empty history is treated as `unknown` for summary view and does not alter existing API compatibility.
