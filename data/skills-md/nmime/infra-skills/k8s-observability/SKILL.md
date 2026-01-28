---
name: k8s-observability
description: VictoriaMetrics + Loki + Grafana. Light or full mode.
---

# K8s Observability

VictoriaMetrics v1.133.0 + Loki v3.6.3 + Grafana v12.3.1. (Updated: January 2026). All scripts are **idempotent** - uses `helm upgrade --install`.

## Known Issues

| Issue | Affected | Workaround |
|-------|----------|------------|
| Memory leak with OpenTelemetry | vmagent, vmsingle, vminsert | Skip affected versions or build from master |

## LTS Versions

VictoriaMetrics LTS releases (12 months support):
- **v1.122.x** - Current LTS
- **v1.110.x** - Previous LTS (support ends 2026-07)

## Modes

| Tier | Retention | Storage |
|------|-----------|--------|
| minimal/small | 7-14 days | 10-20GB |
| medium/production | 30 days | 50-100GB |

## Installation

See component references for tier-based installation:
- [references/victoriametrics.md](references/victoriametrics.md)
- [references/loki.md](references/loki.md)
- [references/grafana.md](references/grafana.md)

## Reference Files

- [references/victoriametrics.md](references/victoriametrics.md) - VictoriaMetrics setup
- [references/loki.md](references/loki.md) - Loki log aggregation
- [references/grafana.md](references/grafana.md) - Grafana dashboards
- [references/alerting.md](references/alerting.md) - Alerting configuration
- [references/light-mode.md](references/light-mode.md) - Light mode setup