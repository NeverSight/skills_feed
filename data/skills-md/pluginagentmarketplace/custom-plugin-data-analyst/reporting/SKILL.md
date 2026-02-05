---
name: reporting
description: Automated reporting and business intelligence delivery
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 08-data-storytelling
bond_type: PRIMARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential

# Parameter Validation
parameters:
  report_type:
    type: string
    required: true
    enum: [executive, operational, analytical, ad_hoc]
    default: operational
  delivery_method:
    type: string
    required: false
    enum: [email, dashboard, pdf, presentation]
    default: dashboard

# Observability
observability:
  logging_level: info
  metrics: [report_views, delivery_success, engagement_rate]
---

# Reporting Skill

## Overview
Master automated reporting and business intelligence delivery for effective communication.

## Topics Covered
- Automated report generation
- Scheduled report delivery
- KPI dashboards and metrics
- Executive summary writing
- Report templates and standards

## Learning Outcomes
- Build automated reports
- Create executive summaries
- Design KPI dashboards
- Deliver insights effectively

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Delivery failed | Email/system error | Retry with backup method |
| Data stale | Refresh failed | Show last refresh timestamp |
| Format broken | Template issue | Validate template before send |
| Access denied | Permission error | Verify distribution list access |

## Related Skills
- visualization (for dashboard design)
- career (for executive communication)
- business-intelligence (for enterprise platforms)
