---
name: workos-rbac
description: Set up role-based access control for your application.
---

<!-- refined:sha256:f02c2083efa0 -->

# WorkOS Role-Based Access Control

## Step 1: Fetch Documentation (BLOCKING)

**STOP. Do not proceed until complete.**

WebFetch these URLs in order:

- `https://workos.com/docs/rbac/quick-start`
- `https://workos.com/docs/rbac/organization-roles`
- `https://workos.com/docs/rbac/integration`
- `https://workos.com/docs/rbac/index`
- `https://workos.com/docs/rbac/idp-role-assignment`
- `https://workos.com/docs/rbac/configuration`

These docs are the source of truth. If this skill conflicts with them, follow the docs.

## Step 2: Pre-Flight Validation

### Environment Variables

Check `.env` or `.env.local` for:

- `WORKOS_API_KEY` - starts with `sk_`
- `WORKOS_CLIENT_ID` - starts with `client_` (if using AuthKit integration)

**Verify:**

```bash
grep -E "WORKOS_API_KEY|WORKOS_CLIENT_ID" .env* 2>/dev/null || echo "FAIL: Environment variables missing"
```

### SDK Presence

Confirm WorkOS SDK is installed:

```bash
# For Node.js projects
npm list @workos-inc/node 2>/dev/null || echo "WARN: @workos-inc/node not found"

# For other SDKs, check package manager's list command
```

**Critical:** Do not write code using SDK methods until SDK is confirmed installed.

## Step 3: Configuration Strategy (Decision Tree)

```
Authorization model?
  |
  +-- Environment-level roles only
  |     |
  |     +-- Same roles for all orgs --> Configure in WorkOS Dashboard > Roles
  |
  +-- Organization-specific roles
        |
        +-- Different roles per org --> Configure per-org in Dashboard > Organizations > [Org] > Roles
```

**Key distinction:**

- **Environment roles**: Global across all organizations, slug format `role-slug`
- **Organization roles**: Per-org custom roles, slug format `org:role-slug` (prefix automatic)

**Critical:** Organization roles override environment roles. If an org has ANY custom roles, it gets its own default role and priority order.

## Step 4: Dashboard Configuration

### For Environment-Level Roles

Navigate to WorkOS Dashboard > Roles:

1. Click "Create role"
2. Define role slug (e.g., `admin`, `member`, `viewer`)
3. Assign permissions to role
4. Set default role for new organization memberships
5. Configure priority order (highest to lowest privilege)

**Verify:**

```bash
# API check for configured roles (requires jq)
curl -s -u "$WORKOS_API_KEY:" https://api.workos.com/roles \
  | jq -r '.data[].slug' \
  || echo "FAIL: Cannot fetch roles - check API key"
```

### For Organization-Specific Roles

Navigate to WorkOS Dashboard > Organizations > [Select Organization] > Roles:

1. Click "Create role" on organization's Roles tab
2. Define role slug (system adds `org:` prefix automatically)
3. Assign permissions
4. Note: First custom role triggers org-specific default role and priority order

**Critical:** Once an org has custom roles, new environment roles are still available to it but placed at BOTTOM of priority order.

## Step 5: Permission Model Setup

### Define Permissions

Permissions follow resource:action format (e.g., `video:create`, `settings:manage`).

**Best practice pattern:**

```
Resource categories:
  - Core features: video:create, video:view, video:delete
  - Management: user:manage, settings:manage
  - Reporting: analytics:view
```

Navigate to Dashboard > Roles > [Select Role] > Permissions:

1. Create permissions with resource:action format
2. Assign to appropriate roles
3. Test with lowest-privilege role first

### Permission Granularity Decision

```
How granular should permissions be?
  |
  +-- Resource-level (video:*)
  |     |
  |     +-- Simple apps, few roles --> video:view, video:manage
  |
  +-- Action-level (video:create, video:delete)
        |
        +-- Complex apps, many roles --> Fine-grained control per action
```

## Step 6: Role Assignment Integration (Decision Tree)

```
How are users getting roles?
  |
  +-- Manual via API
  |     |
  |     +-- Use Organization Membership API --> Step 6A
  |
  +-- Via Identity Provider
  |     |
  |     +-- SSO group mapping --> Step 6B
  |     +-- Directory Sync group mapping --> Step 6C
  |
  +-- Via AuthKit JIT provisioning
        |
        +-- Configure provisioning rules --> See workos-authkit-base skill
```

### Step 6A: Manual Role Assignment via API

Use Organization Membership API to assign/update roles:

```bash
# Example: Update organization membership role
curl -X PUT "https://api.workos.com/user_management/organization_memberships/{id}" \
  -u "$WORKOS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "role_slug": "admin"
  }'
```

**For multiple roles:**

```bash
# Assign multiple roles (if multiple roles feature enabled)
curl -X PUT "https://api.workos.com/user_management/organization_memberships/{id}" \
  -u "$WORKOS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "role_slugs": ["admin", "billing-manager"]
  }'
```

**Verify assignment:**

```bash
# Check membership roles
curl -s -u "$WORKOS_API_KEY:" \
  "https://api.workos.com/user_management/organization_memberships/{id}" \
  | jq -r '.role.slug' \
  || echo "FAIL: Cannot fetch membership"
```

### Step 6B: SSO Group Role Assignment

Navigate to Dashboard > SSO > [Connection] > Advanced:

1. Enable "Group role assignment"
2. Map IdP groups to WorkOS roles:
   - IdP group: `Engineering` → WorkOS role: `developer`
   - IdP group: `Admins` → WorkOS role: `admin`

**Behavior:** Role updates on EVERY authentication. Takes precedence over API/Dashboard assignments.

**Reference:** https://workos.com/docs/rbac/idp-role-assignment

### Step 6C: Directory Sync Group Role Assignment

Navigate to Dashboard > Directory Sync > [Connection] > Groups:

1. Enable "Group role assignment"
2. Map directory groups to roles
3. Enable directory provisioning in AuthKit if using automatic org membership creation

**Behavior:** Role updates on directory events (user added/removed from group). Takes precedence over API/Dashboard assignments.

**Reference:** https://workos.com/docs/rbac/idp-role-assignment

## Step 7: Access Control Implementation

### Reading Roles from Sessions (AuthKit Integration)

**For server-side components:**

```typescript
import { getUser } from '@workos-inc/authkit-nextjs';

const { user } = await getUser();

// Single role
const role = user?.role?.slug;

// Multiple roles (if enabled)
const roles = user?.roles?.map(r => r.slug) || [];
```

**For client-side components:**

```typescript
'use client';
import { useAuth } from '@workos-inc/authkit-nextjs';

function ProtectedComponent() {
  const { user } = useAuth();
  const role = user?.role?.slug;

  if (role !== 'admin') {
    return <div>Access denied</div>;
  }

  return <div>Admin content</div>;
}
```

### Checking Permissions

**Pattern 1: Role-based checks (simple)**

```typescript
const isAdmin = user?.role?.slug === 'admin';
const canManageSettings = ['admin', 'owner'].includes(user?.role?.slug);
```

**Pattern 2: Permission-based checks (recommended)**

```typescript
// Check if user has specific permission
const permissions = user?.role?.permissions || [];
const canCreateVideo = permissions.some(p => 
  p.resource === 'video' && p.action === 'create'
);

// Or use wildcard pattern if permissions include wildcards
const canManageUsers = permissions.some(p =>
  (p.resource === 'user' && p.action === 'manage') ||
  (p.resource === 'user' && p.action === '*') ||
  (p.resource === '*' && p.action === '*')
);
```

**Pattern 3: Helper function (reusable)**

```typescript
function hasPermission(
  user: User | null,
  resource: string,
  action: string
): boolean {
  if (!user?.role?.permissions) return false;

  return user.role.permissions.some(p =>
    (p.resource === resource || p.resource === '*') &&
    (p.action === action || p.action === '*')
  );
}

// Usage
if (hasPermission(user, 'video', 'delete')) {
  // Show delete button
}
```

### Multiple Roles Pattern

If multiple roles are enabled, aggregate permissions:

```typescript
function hasPermissionMultiRole(
  user: User | null,
  resource: string,
  action: string
): boolean {
  if (!user?.roles?.length) return false;

  // Check if ANY role grants the permission
  return user.roles.some(role =>
    role.permissions?.some(p =>
      (p.resource === resource || p.resource === '*') &&
      (p.action === action || p.action === '*')
    )
  );
}
```

## Step 8: API Route Protection

### Middleware Pattern (Recommended)

```typescript
// middleware.ts or lib/auth.ts
import { getUser } from '@workos-inc/authkit-nextjs';
import { NextResponse } from 'next/server';

export async function requireRole(
  allowedRoles: string[]
): Promise<User | NextResponse> {
  const { user } = await getUser();

  if (!user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const userRole = user.role?.slug;
  if (!userRole || !allowedRoles.includes(userRole)) {
    return NextResponse.json(
      { error: 'Forbidden' },
      { status: 403 }
    );
  }

  return user;
}

// Usage in API route
export async function DELETE(request: Request) {
  const result = await requireRole(['admin', 'owner']);
  if (result instanceof NextResponse) return result;

  const user = result;
  // Proceed with admin logic
}
```

### Permission-Based Protection

```typescript
export async function requirePermission(
  resource: string,
  action: string
): Promise<User | NextResponse> {
  const { user } = await getUser();

  if (!user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const hasPermission = user.role?.permissions?.some(p =>
    (p.resource === resource || p.resource === '*') &&
    (p.action === action || p.action === '*')
  );

  if (!hasPermission) {
    return NextResponse.json(
      { error: 'Forbidden - missing permission' },
      { status: 403 }
    );
  }

  return user;
}

// Usage
export async function POST(request: Request) {
  const result = await requirePermission('video', 'create');
  if (result instanceof NextResponse) return result;

  // Proceed with video creation
}
```

## Step 9: Organization Role Management

### When to Use Organization Roles

```
Does this organization need custom roles?
  |
  +-- No --> Use environment roles (default)
  |
  +-- Yes
        |
        +-- Why?
            |
            +-- Stricter permissions than standard --> Create org role with subset of permissions
            |
            +-- Different role names/structure --> Create org-specific roles
            |
            +-- Compliance requirements --> Create custom roles per org's policy
```

### Creating Organization Roles

**Via Dashboard:**

1. Navigate to Organizations > [Org] > Roles
2. Click "Create role"
3. Define slug (e.g., `limited-admin`)
4. System automatically prefixes with `org:` → final slug: `org:limited-admin`
5. Assign permissions subset

**Impact of first org role:**

- Organization gets its own default role setting
- Organization gets its own priority order
- Environment roles still available but at bottom of priority

**Critical:** If you delete an environment role that's the default for orgs, you MUST select a replacement default for affected orgs.

## Verification Checklist (ALL MUST PASS)

Run these commands to confirm integration:

```bash
# 1. Check environment variables exist
grep -q "WORKOS_API_KEY=sk_" .env* && echo "PASS: API key found" || echo "FAIL: API key missing or invalid format"

# 2. Check roles are configured (requires API key)
curl -s -u "$WORKOS_API_KEY:" https://api.workos.com/roles \
  | jq -r '.data | length' \
  | grep -q -v '^0$' \
  && echo "PASS: Roles configured" \
  || echo "FAIL: No roles found"

# 3. Check SDK is installed
npm list @workos-inc/node 2>/dev/null | grep -q "@workos-inc/node" \
  && echo "PASS: SDK installed" \
  || echo "WARN: SDK not found (may be using different SDK)"

# 4. Check for access control implementation
grep -r "role\.slug\|permissions\.some\|hasPermission" app/ src/ \
  | head -n 1 \
  | grep -q "." \
  && echo "PASS: Access control checks found" \
  || echo "FAIL: No access control implementation detected"

# 5. Build succeeds
npm run build 2>&1 | tail -n 5
```

**All checks must pass before considering integration complete.**

## Error Recovery

### "Forbidden - missing permission" (403)

**Root cause:** User's role lacks required permission for action.

Fix decision tree:

```
Is this the correct behavior?
  |
  +-- Yes (user shouldn't have access) --> Update UI to hide unauthorized actions
  |
  +-- No (user should have access)
        |
        +-- Check user's role in Dashboard
        |     |
        |     +-- Role correct? --> Add missing permission to role
        |     |
        |     +-- Wrong role? --> Update organization membership role
        |
        +-- Using IdP assignment? --> Check group mappings in SSO/Directory Sync settings
```

### "Unauthorized" (401)

**Root cause:** User not authenticated or session expired.

Fix:

1. Check AuthKit integration is working: `curl localhost:3000/api/auth/session`
2. Verify middleware is calling `getUser()` correctly
3. Check auth cookies are being sent with requests
4. For API routes, confirm Authorization header or cookie forwarding

### Role assignment not updating

**Symptom:** User assigned new role but session shows old role.

**Root cause:** Session not refreshed after role change.

Fix decision tree:

```
Assignment method?
  |
  +-- API/Dashboard manual assignment
  |     |
  |     +-- User must log out and log back in --> Session update needed
  |
  +-- IdP (SSO) assignment
  |     |
  |     +-- Updates on next authentication --> Force re-auth or wait for next login
  |
  +-- Directory Sync assignment
        |
        +-- Updates on directory events --> Check event delivery in Dashboard > Events
```

**Workaround:** Force session refresh by having user log out and back in.

### Organization role slug conflicts

**Symptom:** Cannot create org role with same slug as environment role.

**Expected behavior:** This is prevented by automatic `org:` prefix. Org role `admin` becomes `org:admin`, environment role is `admin`.

**If seeing conflict:** Check if slug already has `org:` prefix manually added (don't add it yourself).

### Multiple roles not working

**Root cause:** Multiple roles feature not enabled for environment.

**Check:** WebFetch https://workos.com/docs/rbac/integration to confirm feature availability and enablement process.

**Symptom:** API rejects `role_slugs` array, only accepts `role_slug` string.

**Fix:** Contact WorkOS support to enable multiple roles feature for your environment.

### Permission wildcards not matching

**Symptom:** Permission check fails despite wildcard permission (`video:*` or `*:*`).

**Root cause:** Permission matching logic doesn't handle wildcards.

Fix by updating permission check helper:

```typescript
function matchesPermission(
  granted: { resource: string; action: string },
  required: { resource: string; action: string }
): boolean {
  const resourceMatch = 
    granted.resource === '*' || 
    granted.resource === required.resource;

  const actionMatch = 
    granted.action === '*' || 
    granted.action === required.action;

  return resourceMatch && actionMatch;
}
```

### "Role not found" when assigning

**Root cause:** Role slug doesn't exist in environment or organization.

**Check:**

```bash
# List all roles for debugging
curl -s -u "$WORKOS_API_KEY:" https://api.workos.com/roles \
  | jq -r '.data[] | "\(.slug) - \(.name)"'

# For org-specific roles, check organization's roles in Dashboard
```

**Common mistakes:**

- Using `org:role-slug` for environment role (wrong prefix)
- Using `role-slug` for org role (missing prefix)
- Typo in slug (roles are case-sensitive)

### Default role not applied to new members

**Root cause:** Default role configuration missing or incorrect.

**Check:** Dashboard > Roles > Default role setting (or per-org if using org roles).

**Verify:**

```bash
# Create test membership and check assigned role
curl -X POST "https://api.workos.com/user_management/organization_memberships" \
  -u "$WORKOS_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_test_123",
    "organization_id": "org_test_123"
  }' \
  | jq -r '.role.slug'
```

Should return default role slug, not null.

## Related Skills

- **workos-authkit-nextjs**: For reading roles from AuthKit sessions
- **workos-fga**: For fine-grained authorization beyond role-based checks
- **workos-sso**: For IdP group role assignment via SSO
- **workos-directory-sync**: For IdP group role assignment via Directory Sync
- **workos-api-organization**: For managing organizations with custom roles
