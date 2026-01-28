---
name: supabase-best-practices
description: Supabase security and performance guidelines with Clerk authentication integration. Contains 40+ rules across 10 categories covering RLS policies, Clerk setup, database security, and more.
license: MIT
metadata:
  author: AI Engineering Team
  version: "1.0.1"
  last_updated: "2025-01-27"
---

# Supabase Best Practices

Comprehensive security and performance optimization guide for Supabase applications with Clerk authentication integration. Contains 40+ rules across 10 categories, prioritized by impact to guide secure development and code review.

## When to Apply

Reference these guidelines when:
- Setting up a new Supabase project
- Integrating Clerk authentication with Supabase
- Writing Row Level Security (RLS) policies
- Designing database schemas
- Implementing real-time features
- Configuring Storage buckets
- Writing Edge Functions
- Reviewing code for security issues

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Row Level Security | CRITICAL | `rls-` |
| 2 | Clerk Integration | CRITICAL | `clerk-` |
| 3 | Database Security | HIGH | `db-` |
| 4 | Authentication Patterns | HIGH | `auth-` |
| 5 | API Security | HIGH | `api-` |
| 6 | Storage Security | MEDIUM-HIGH | `storage-` |
| 7 | Realtime Security | MEDIUM | `realtime-` |
| 8 | Edge Functions | MEDIUM | `edge-` |
| 9 | Testing | MEDIUM | `test-` |
| 10 | Security | MEDIUM | `security-` |

## Quick Reference

### 1. Row Level Security (CRITICAL)

- `rls-always-enable` - Always enable RLS on public schema tables
- `rls-wrap-functions-select` - Wrap auth functions with (SELECT ...) for performance
- `rls-add-indexes` - Add indexes on columns used in RLS policies
- `rls-specify-roles` - Specify roles with TO authenticated clause
- `rls-security-definer` - Use SECURITY DEFINER functions for complex policies
- `rls-minimize-joins` - Minimize joins in RLS policies
- `rls-explicit-auth-check` - Use explicit auth.uid() checks
- `rls-restrictive-policies` - Use RESTRICTIVE policies for additional constraints

### 2. Clerk Integration (CRITICAL)

- `clerk-setup-third-party` - Use Third-Party Auth integration (not JWT templates)
- `clerk-client-server-side` - Use accessToken callback for server-side clients
- `clerk-client-client-side` - Use useSession() hook for client-side clients
- `clerk-role-claim` - Configure role: authenticated claim in Clerk
- `clerk-org-policies` - Use organization claims for multi-tenant RLS
- `clerk-mfa-policies` - Enforce MFA with RESTRICTIVE policies
- `clerk-no-jwt-templates` - Never use deprecated JWT template integration

### 3. Database Security (HIGH)

- `db-migrations-versioned` - Use versioned migrations for schema changes
- `db-schema-design` - Follow proper schema design patterns
- `db-indexes-strategy` - Implement proper indexing strategy
- `db-foreign-keys` - Always use foreign key constraints
- `db-triggers-security` - Secure trigger functions properly
- `db-views-security-invoker` - Use SECURITY INVOKER for views

### 4. Authentication Patterns (HIGH)

- `auth-jwt-claims-validation` - Always validate JWT claims
- `auth-user-metadata-safety` - Treat user_metadata as untrusted
- `auth-app-metadata-authorization` - Use app_metadata for authorization
- `auth-session-management` - Implement proper session management

### 5. API Security (HIGH)

- `api-filter-queries` - Always filter queries even with RLS
- `api-publishable-keys` - Use publishable keys correctly
- `api-service-role-server-only` - Never expose service role key to client

### 6. Storage Security (MEDIUM-HIGH)

- `storage-rls-policies` - Enable RLS on storage.objects
- `storage-bucket-security` - Configure bucket-level security
- `storage-signed-urls` - Use signed URLs for private files

### 7. Realtime Security (MEDIUM)

- `realtime-private-channels` - Use private channels for sensitive data
- `realtime-rls-authorization` - RLS policies apply to realtime
- `realtime-cleanup-subscriptions` - Clean up subscriptions on unmount

### 8. Edge Functions (MEDIUM)

- `edge-verify-jwt` - Always verify JWT in edge functions
- `edge-cors-handling` - Handle CORS properly
- `edge-secrets-management` - Use secrets for sensitive data

### 9. Testing (MEDIUM)

- `test-pgtap-rls` - Test RLS policies with pgTAP
- `test-isolation` - Isolate tests properly
- `test-helpers` - Use test helper functions

### 10. Security (MEDIUM)

- `security-validate-inputs` - Validate all inputs before processing
- `security-audit-advisors` - Regularly run Security Advisor checks

## How to Use

Read individual rule files for detailed explanations and code examples:

```
references/rules/rls-always-enable.md
references/rules/clerk-setup-third-party.md
references/rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- When NOT to use the pattern
- Reference links to official documentation

## Full Compiled Document

For the complete guide with all rules expanded: `references/supabase-guidelines.md`
