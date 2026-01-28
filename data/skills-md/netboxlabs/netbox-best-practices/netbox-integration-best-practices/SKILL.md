---
name: netbox-integration-best-practices
description: Best practices for building integrations with NetBox REST and GraphQL APIs. Use when building NetBox API integrations, reviewing integration code, troubleshooting NetBox performance issues, planning automation architecture, writing scripts that interact with NetBox, using pynetbox, configuring Diode for data ingestion, or implementing NetBox webhooks.
license: Apache-2.0
---

# NetBox Integration Best Practices Skill

This skill provides best practices guidance for building integrations and automations with NetBox REST and GraphQL APIs.

## Target Audience

- Engineers building integrations atop NetBox APIs
- Teams planning new automations with Claude
- Developers learning NetBox API best practices

**Scope:** This skill covers API integration patterns. It does NOT cover plugin development, custom scripts, or NetBox administration.

## NetBox Version Requirements

| Feature | Version Required |
|---------|-----------------|
| REST API | All versions |
| GraphQL API | 2.9+ |
| v2 Tokens | 4.5+ (use these!) |
| v1 Token Deprecation | 4.7+ (migrate before this) |

**Primary target:** NetBox 4.4+ with 4.5+ for v2 token features.

## When to Apply This Skill

Apply these practices when:
- Building new NetBox API integrations
- Reviewing existing integration code
- Troubleshooting performance issues
- Planning automation architecture
- Writing scripts that interact with NetBox

## Priority Levels

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Security vulnerabilities, data loss, severe performance | Must fix immediately |
| **HIGH** | Significant performance/reliability impact | Should fix soon |
| **MEDIUM** | Notable improvements, best practices | Plan to address |
| **LOW** | Minor improvements, optional | Consider when convenient |

## Quick Reference

### Authentication
- **Use v2 tokens** on NetBox 4.5+: `Bearer nbt_<key>.<token>`
- **Migrate from v1** before NetBox 4.7 (deprecation planned)

### REST API
- **Always paginate**: `?limit=100` (max 1000)
- **Use PATCH** for partial updates, not PUT
- **Use ?brief=True** for list operations
- **Exclude config_context**: `?exclude=config_context` (major performance impact)
- **Avoid ?q=** search filter at scale; use specific filters
- **Bulk operations** use list endpoints with JSON arrays (not separate endpoints)

### GraphQL
- **Use the query optimizer**: [netbox-graphql-query-optimizer](https://github.com/netboxlabs/netbox-graphql-query-optimizer)
- **Always paginate** every list query
- **Paginate at every level** of nesting
- **Beware offset pagination at scale**: Deep offsets are slow; use ID range filtering in 4.5.x, cursor-based in 4.6.0+ ([#21110](https://github.com/netbox-community/netbox/issues/21110))
- **Request only needed fields**
- **Keep depth ≤3**, never exceed 5

### Performance
- Exclude config_context from device lists
- Use brief mode for large lists
- Parallelize independent requests

### Data Ingestion (Diode)
- For high-volume data ingestion, use [Diode](https://github.com/netboxlabs/diode) instead of direct API
- **Specify dependencies by name**, not ID—Diode resolves or creates them
- **No dependency order needed**—Diode handles object creation order
- Use `pip install netboxlabs-diode-sdk` for Python
- Use REST/GraphQL API for reading; use Diode for writing/populating

## Rules by Category

### Authentication Rules

| Rule | Impact | Description |
|------|--------|-------------|
| [auth-use-v2-tokens](./references/rules/auth-use-v2-tokens.md) | CRITICAL | Use v2 tokens on NetBox 4.5+ |
| [auth-provisioning-endpoint](./references/rules/auth-provisioning-endpoint.md) | MEDIUM | Use provisioning endpoint for automated token creation |

### REST API Rules

| Rule | Impact | Description |
|------|--------|-------------|
| [rest-list-endpoint-bulk-ops](./references/rules/rest-list-endpoint-bulk-ops.md) | CRITICAL | Use list endpoints for bulk operations |
| [rest-pagination-required](./references/rules/rest-pagination-required.md) | HIGH | Always paginate list requests |
| [rest-patch-vs-put](./references/rules/rest-patch-vs-put.md) | HIGH | Use PATCH for partial updates |
| [rest-brief-mode](./references/rules/rest-brief-mode.md) | HIGH | Use ?brief=True for lists |
| [rest-field-selection](./references/rules/rest-field-selection.md) | HIGH | Use ?fields= to select fields |
| [rest-exclude-config-context](./references/rules/rest-exclude-config-context.md) | HIGH | Exclude config_context from device lists |
| [rest-avoid-search-filter-at-scale](./references/rules/rest-avoid-search-filter-at-scale.md) | HIGH | Avoid q= with large datasets |
| [rest-filtering-expressions](./references/rules/rest-filtering-expressions.md) | MEDIUM | Use lookup expressions |
| [rest-custom-field-filters](./references/rules/rest-custom-field-filters.md) | MEDIUM | Filter by custom fields |
| [rest-nested-serializers](./references/rules/rest-nested-serializers.md) | LOW | Understand nested serializers |
| [rest-ordering-results](./references/rules/rest-ordering-results.md) | LOW | Use ordering parameter |
| [rest-options-discovery](./references/rules/rest-options-discovery.md) | LOW | Use OPTIONS for discovery |

### GraphQL Rules

| Rule | Impact | Description |
|------|--------|-------------|
| [graphql-use-query-optimizer](./references/rules/graphql-use-query-optimizer.md) | CRITICAL | Use query optimizer |
| [graphql-always-paginate](./references/rules/graphql-always-paginate.md) | CRITICAL | Paginate every list query |
| [graphql-pagination-at-each-level](./references/rules/graphql-pagination-at-each-level.md) | HIGH | Paginate nested lists |
| [graphql-select-only-needed](./references/rules/graphql-select-only-needed.md) | HIGH | Request only needed fields |
| [graphql-calibrate-optimizer](./references/rules/graphql-calibrate-optimizer.md) | HIGH | Calibrate against production |
| [graphql-max-depth](./references/rules/graphql-max-depth.md) | HIGH | Keep depth ≤3 |
| [graphql-prefer-filters](./references/rules/graphql-prefer-filters.md) | MEDIUM | Filter server-side |
| [graphql-vs-rest-decision](./references/rules/graphql-vs-rest-decision.md) | MEDIUM | Choose appropriate API |
| [graphql-complexity-budgets](./references/rules/graphql-complexity-budgets.md) | LOW | Establish complexity budgets |

### Performance Rules

| Rule | Impact | Description |
|------|--------|-------------|
| [perf-exclude-config-context](./references/rules/perf-exclude-config-context.md) | HIGH | Exclude config_context |
| [perf-brief-mode-lists](./references/rules/perf-brief-mode-lists.md) | HIGH | Use brief mode for lists |

### Data Modeling Rules

| Rule | Impact | Description |
|------|--------|-------------|
| [data-dependency-order](./references/rules/data-dependency-order.md) | CRITICAL | Create objects in dependency order |
| [data-site-hierarchy](./references/rules/data-site-hierarchy.md) | MEDIUM | Understand site hierarchy |
| [data-ipam-hierarchy](./references/rules/data-ipam-hierarchy.md) | MEDIUM | Understand IPAM hierarchy |
| [data-custom-fields](./references/rules/data-custom-fields.md) | MEDIUM | Use custom fields properly |
| [data-tags-usage](./references/rules/data-tags-usage.md) | MEDIUM | Use tags for classification |
| [data-tenant-isolation](./references/rules/data-tenant-isolation.md) | MEDIUM | Use tenants for separation |
| [data-natural-keys](./references/rules/data-natural-keys.md) | MEDIUM | Use natural keys |

### Integration Rules

| Rule | Impact | Description |
|------|--------|-------------|
| [integ-diode-ingestion](./references/rules/integ-diode-ingestion.md) | HIGH | Use Diode for high-volume data ingestion |
| [integ-pynetbox-client](./references/rules/integ-pynetbox-client.md) | HIGH | Use pynetbox for Python |
| [integ-webhook-configuration](./references/rules/integ-webhook-configuration.md) | MEDIUM | Configure webhooks |
| [integ-change-tracking](./references/rules/integ-change-tracking.md) | LOW | Query object changes |

## External References

### Official Documentation
- [NetBox Documentation](https://netboxlabs.com/docs/netbox/en/stable/)
- [REST API Guide](https://netboxlabs.com/docs/netbox/en/stable/integrations/rest-api/)
- [GraphQL API Guide](https://netboxlabs.com/docs/netbox/en/stable/integrations/graphql-api/)

### Essential Tools
- [pynetbox](https://github.com/netbox-community/pynetbox) - Official Python client
- [netbox-graphql-query-optimizer](https://github.com/netboxlabs/netbox-graphql-query-optimizer) - Query analysis (essential for GraphQL)
- [Diode](https://github.com/netboxlabs/diode) - Data ingestion service (for high-volume writes)
- [Diode Python SDK](https://github.com/netboxlabs/diode-sdk-python) - Python client for Diode

### Community
- [NetBox GitHub](https://github.com/netbox-community/netbox)
- [NetBox Discussions](https://github.com/netbox-community/netbox/discussions)

## Reference Documentation

| Document | Purpose |
|----------|---------|
| [HUMAN.md](../../HUMAN.md) | Human-readable guide for engineers |
| [netbox-integration-guidelines.md](./references/netbox-integration-guidelines.md) | Comprehensive technical reference |
