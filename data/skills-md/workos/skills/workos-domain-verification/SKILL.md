---
name: workos-domain-verification
description: Verify organization domains for SSO and directory sync.
---

<!-- refined:sha256:5ce9616c6d75 -->

# WorkOS Domain Verification

## Step 1: Fetch Documentation (BLOCKING)

**STOP. Do not proceed until complete.**

WebFetch these URLs for source of truth:
- https://workos.com/docs/domain-verification/index
- https://workos.com/docs/domain-verification/api

If this skill conflicts with the documentation, follow the documentation.

## Step 2: Pre-Flight Validation

### Environment Variables

Check for required WorkOS credentials:

- `WORKOS_API_KEY` - starts with `sk_`
- `WORKOS_CLIENT_ID` - starts with `client_`

**Verify:** Both variables are set in `.env` or `.env.local`

### SDK Installation

Confirm WorkOS SDK is installed:

```bash
# Check package.json contains @workos-inc/node
grep "@workos-inc/node" package.json || npm install @workos-inc/node
```

**CRITICAL:** SDK must be installed before writing any import statements.

## Step 3: Organization Exists (REQUIRED)

**All domains must belong to an Organization.** You cannot create or verify a domain without an Organization.

Check if organization already exists:

```bash
# If you have organization ID
curl https://api.workos.com/organizations/org_123 \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

If no organization exists, create one first using the Organizations API (see `workos-organizations` skill).

**Do NOT proceed to Step 4 until you have a valid Organization ID.**

## Step 4: Implementation Path (Decision Tree)

Choose based on your use case:

```
Domain verification flow?
  |
  +-- Self-serve (IT admin verifies) --> Admin Portal flow (Step 5A)
  |
  +-- Programmatic (you verify)      --> API flow (Step 5B)
```

**Self-serve** = Your customer's IT admin proves ownership via DNS TXT records through the Admin Portal UI

**Programmatic** = You integrate domain creation/verification directly into your application code

## Step 5A: Admin Portal Flow (Self-Serve)

### Create Portal Link

Generate a temporary Admin Portal session link (valid 5 minutes):

```typescript
import { WorkOS } from '@workos-inc/node';

const workos = new WorkOS(process.env.WORKOS_API_KEY);

const portalLink = await workos.portal.generateLink({
  organization: 'org_123',
  intent: 'domain_verification',
  return_url: 'https://yourapp.com/settings/domains'
});

// portalLink.link - redirect user here
```

**Check documentation for exact method signature** - may be `createLink` or `generateLink` depending on SDK version.

### User Flow

1. Redirect user to `portalLink.link`
2. User adds domain in Admin Portal
3. User adds DNS TXT record to their domain's DNS
4. WorkOS verifies TXT record automatically
5. User returns to `return_url` when complete

### Verification

Listen for webhook to know when domain is verified, or poll the domain status:

```bash
# Get domain status
curl https://api.workos.com/organization_domains/org_domain_123 \
  -H "Authorization: Bearer $WORKOS_API_KEY"
```

**Check documentation** for webhook event name - likely `domain.verified` or similar.

## Step 5B: API Flow (Programmatic)

### Create Domain

```typescript
import { WorkOS } from '@workos-inc/node';

const workos = new WorkOS(process.env.WORKOS_API_KEY);

const domain = await workos.organizationDomains.create({
  organization_id: 'org_123',
  domain: 'example.com'
});

// domain.id - save this
// domain.verification_token - share this with domain owner
```

**Check documentation for exact method path** - may be `workos.domains.create()` or similar.

### Share Verification Instructions

The domain owner must add this DNS TXT record:

```
Type: TXT
Host: _workos-challenge (or @ for root)
Value: [domain.verification_token from response]
```

**Check documentation** for exact TXT record format - host name may vary.

### Trigger Verification

After DNS TXT record is added, trigger verification check:

```typescript
await workos.organizationDomains.verify({
  domain_id: domain.id
});
```

**Check documentation** for exact method name - may be `verify()`, `checkVerification()`, or automatic.

### Poll for Status

Check if verification succeeded:

```typescript
const updatedDomain = await workos.organizationDomains.get(domain.id);

if (updatedDomain.state === 'verified') {
  // Domain verified successfully
} else if (updatedDomain.state === 'pending') {
  // Still waiting for DNS propagation
} else if (updatedDomain.state === 'failed') {
  // Verification failed - check TXT record
}
```

**Check documentation** for exact state values - may be `status` instead of `state`, may use different enum values.

## Step 6: List Domains for Organization

Retrieve all domains (verified and unverified) for an organization:

```typescript
const domains = await workos.organizationDomains.list({
  organization_id: 'org_123'
});

domains.data.forEach(domain => {
  console.log(`${domain.domain}: ${domain.state}`);
});
```

## Verification Checklist (ALL MUST PASS)

Run these commands to confirm integration:

```bash
# 1. Check environment variables exist
env | grep WORKOS_API_KEY && env | grep WORKOS_CLIENT_ID

# 2. Check SDK is installed
npm list @workos-inc/node 2>/dev/null || echo "FAIL: SDK not installed"

# 3. Verify organization exists (replace org_123 with your ID)
curl -s https://api.workos.com/organizations/org_123 \
  -H "Authorization: Bearer $WORKOS_API_KEY" | grep '"id"'

# 4. Test domain creation (replace with test domain)
curl -X POST https://api.workos.com/organization_domains \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"organization_id":"org_123","domain":"test.example.com"}'

# 5. Build succeeds
npm run build
```

**If check #3 fails:** Create organization first (see Step 3)
**If check #4 fails:** Check API key permissions or organization ID

## Error Recovery

### "Organization not found"

**Root cause:** No organization exists or wrong ID

**Fix:**
1. List organizations: `curl https://api.workos.com/organizations -H "Authorization: Bearer $WORKOS_API_KEY"`
2. If empty, create organization first
3. Use correct organization ID in domain creation

### "Invalid domain format"

**Root cause:** Domain contains invalid characters or format

**Fix:**
- Use bare domain: `example.com` not `https://example.com`
- No subdomains for verification (unless docs explicitly allow)
- Check documentation for allowed domain formats

### "Domain already exists"

**Root cause:** Domain already registered to this or another organization

**Fix:**
1. List domains: `workos.organizationDomains.list()`
2. If domain belongs to current org, use existing domain ID
3. If domain belongs to different org, cannot claim (security feature)

### "Verification failed" / "TXT record not found"

**Root cause:** DNS TXT record not added correctly or DNS not propagated

**Fix:**
1. Check TXT record exists: `dig TXT _workos-challenge.example.com` or `nslookup -type=TXT _workos-challenge.example.com`
2. Verify token matches exactly (no extra quotes or spaces)
3. Wait for DNS propagation (can take up to 48 hours, usually <15 minutes)
4. Check documentation for exact TXT record host format

### "API key does not have permission"

**Root cause:** API key lacks domain verification scope

**Fix:**
1. Go to WorkOS Dashboard → API Keys
2. Check key has required permissions
3. Generate new key if needed

### SDK method not found

**Root cause:** SDK version mismatch with documentation

**Fix:**
1. Check SDK version: `npm list @workos-inc/node`
2. Check documentation for method names matching your SDK version
3. Update SDK: `npm install @workos-inc/node@latest`

### Portal link expired

**Root cause:** Portal links are valid for 5 minutes only

**Fix:**
- Generate new portal link immediately before redirecting user
- Do not cache or reuse portal links

## Related Skills

- **workos-organizations**: Creating organizations (required before domain verification)
- **workos-sso**: SSO connections require verified domains
- **workos-directory-sync**: Directory Sync requires verified domains
- **workos-admin-portal**: General Admin Portal integration patterns
