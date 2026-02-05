---
name: business-intelligence
description: BI tools, dashboards, and enterprise analytics platforms
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 04-visualization-architect
bond_type: SECONDARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential

# Parameter Validation
parameters:
  tool_focus:
    type: string
    required: true
    enum: [tableau, powerbi, looker, all]
    default: all
  skill_level:
    type: string
    required: true
    enum: [beginner, intermediate, advanced]
    default: beginner

# Observability
observability:
  logging_level: info
  metrics: [dashboard_count, user_adoption, report_usage]
---

# Business Intelligence Skill

## Overview
Master enterprise BI tools and platforms to build scalable analytics solutions for organizations.

## Topics Covered
- Tableau, Power BI, Looker
- Dashboard design principles
- Data modeling for BI
- Self-service analytics
- Enterprise reporting architecture

## Learning Outcomes
- Build interactive dashboards
- Design data models
- Implement self-service BI
- Deploy enterprise analytics

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Data refresh failed | Source connection issue | Verify credentials, check network |
| Slow performance | Complex calculations | Optimize data model, use extracts |
| Permission errors | Access control | Configure row-level security |
| Visualization errors | Incompatible data types | Validate data model |

## Related Skills
- visualization (for design principles)
- databases-sql (for data modeling)
- reporting (for delivery mechanisms)
