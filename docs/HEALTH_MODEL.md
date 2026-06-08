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
