---
name: workos-mfa
description: Add multi-factor authentication to your application.
---

<!-- refined:sha256:ef9462b4b924 -->

# WorkOS Multi-Factor Authentication

## Step 1: Fetch Documentation (BLOCKING)

**STOP. Do not proceed until complete.**

WebFetch these URLs — they are the source of truth:

- https://workos.com/docs/mfa/index
- https://workos.com/docs/mfa/example-apps
- https://workos.com/docs/mfa/ux/sign-in
- https://workos.com/docs/mfa/ux/enrollment

If this skill conflicts with fetched docs, follow the docs.

## Step 2: Pre-Flight Validation

### Account Setup

Check WorkOS Dashboard at `https://dashboard.workos.com`:

- API Keys section exists
- You have copied `WORKOS_API_KEY` (starts with `sk_`)
- You have copied `WORKOS_CLIENT_ID` (starts with `client_`)

### Environment Variables

Check `.env` or `.env.local` for:

```bash
WORKOS_API_KEY=sk_...
WORKOS_CLIENT_ID=client_...
```

**Verify before continuing:**

```bash
# Check both keys are set
env | grep WORKOS_API_KEY
env | grep WORKOS_CLIENT_ID
```

### SDK Installation

Detect package manager and verify WorkOS SDK is installed:

```bash
# Check SDK exists in node_modules
ls node_modules/@workos-inc/node 2>/dev/null || \
ls node_modules/@workos-inc/python 2>/dev/null || \
echo "SDK not found - install before proceeding"
```

**Do not proceed until SDK package exists.**

## Step 3: Factor Type Selection (Decision Tree)

```
MFA Factor Type?
  |
  +-- TOTP (Authenticator App)
  |     |
  |     +-- User has Google Authenticator, Authy, etc.
  |     +-- Use enrollFactor() with type: 'totp'
  |     +-- Display QR code + secret from response
  |
  +-- SMS (Text Message)
        |
        +-- User provides phone number
        +-- Validate phone number format BEFORE API call
        +-- Use enrollFactor() with type: 'sms'
        +-- Challenge expires after 10 minutes
```

**Critical:** Phone numbers must be E.164 format (`+1234567890`). Invalid formats return API error.

## Step 4: Enroll Authentication Factor

### TOTP Enrollment

**SDK Method:** `workos.mfa.enrollFactor()`

Parameters:
- `type`: `'totp'`
- `totp_issuer`: Your app name (shows in authenticator app)
- `totp_user`: User identifier (email or username)

**Response contains:**
- `id` — Factor ID (MUST persist in your user table)
- `qr_code` — Base64 data URI for QR code display
- `secret` — Manual entry code (for users who can't scan QR)

**Display pattern:**

```html
<!-- QR Code: src is the base64 data URI from response -->
<img src="{qr_code}" alt="Scan with authenticator app" />

<!-- Manual entry fallback -->
<p>Or enter code manually: {secret}</p>
```

### SMS Enrollment

**SDK Method:** `workos.mfa.enrollFactor()`

Parameters:
- `type`: `'sms'`
- `phone_number`: E.164 format string

**Phone validation (REQUIRED before API call):**

```javascript
// Example validation regex
const e164Regex = /^\+[1-9]\d{1,14}$/;
if (!e164Regex.test(phoneNumber)) {
  throw new Error('Phone must be E.164 format: +1234567890');
}
```

**Response contains:**
- `id` — Factor ID (MUST persist in your user table)

### Persist Factor ID (CRITICAL)

The `id` from enrollment response MUST be stored in your user database:

```sql
-- Example schema
ALTER TABLE users ADD COLUMN mfa_factor_id VARCHAR(255);
UPDATE users SET mfa_factor_id = ? WHERE user_id = ?;
```

**Do NOT proceed to verification without persisting factor ID.**

## Step 5: Create Challenge

**When:** User attempts sign-in after enrolling MFA.

**SDK Method:** `workos.mfa.challengeFactor()`

Parameters:
- `authentication_factor_id`: The factor ID from Step 4

**Response contains:**
- `id` — Challenge ID (needed for verification)
- `expires_at` — ISO timestamp (SMS only, 10 minutes from creation)

**SMS-specific behavior:**
- Challenge sends OTP to enrolled phone number
- Challenge expires after 10 minutes
- Expired challenges cannot be verified — create new challenge

## Step 6: Verify Challenge

**SDK Method:** `workos.mfa.verifyChallenge()`

Parameters:
- `authentication_challenge_id`: Challenge ID from Step 5
- `code`: OTP entered by user (6 digits for TOTP/SMS)

**Response:**
- `valid`: `true` (success) or `false` (incorrect code)

### Sign-In Flow Integration

```
Standard sign-in flow:
  1. User enters username + password
  2. Validate credentials
  3. --> Check if user has mfa_factor_id
     |
     +-- YES --> Redirect to MFA verification page
     |            |
     |            +-- Create challenge (Step 5)
     |            +-- User enters code
     |            +-- Verify challenge (Step 6)
     |            +-- If valid: create session
     |            +-- If invalid: show error, allow retry
     |
     +-- NO  --> Create session directly
```

**Do NOT grant session access until challenge verification returns `valid: true`.**

## Step 7: Error Handling Implementation

Add these specific error handlers to your verification code:

### Challenge Already Verified

**Error condition:** Attempting to verify same challenge twice.

**Response:** API returns error indicating challenge was already used.

**Fix:** Create a NEW challenge via `challengeFactor()`, do not reuse challenge IDs.

**Code pattern:**

```javascript
try {
  const result = await workos.mfa.verifyChallenge({
    authentication_challenge_id: challengeId,
    code: userCode
  });
} catch (error) {
  if (error.message.includes('already verified')) {
    // Create new challenge
    const newChallenge = await workos.mfa.challengeFactor({
      authentication_factor_id: factorId
    });
    // Prompt user to enter new code
  }
}
```

### Challenge Expired (SMS Only)

**Error condition:** Challenge created >10 minutes ago.

**Response:** API returns expired error.

**Fix:** Create a NEW challenge — expired challenges are permanently invalid.

**Code pattern:**

```javascript
catch (error) {
  if (error.message.includes('expired')) {
    const newChallenge = await workos.mfa.challengeFactor({
      authentication_factor_id: factorId
    });
    showMessage('Code expired. New code sent.');
  }
}
```

### Invalid Phone Number

**Error condition:** Phone not in E.164 format during enrollment.

**Response:** API returns validation error.

**Fix:** Validate phone format BEFORE calling `enrollFactor()` (see Step 4).

### Invalid Code Format

**Error condition:** User enters non-numeric or wrong-length code.

**Client-side validation (recommended):**

```javascript
if (!/^\d{6}$/.test(code)) {
  showError('Code must be 6 digits');
  return;
}
```

## Verification Checklist (ALL MUST PASS)

Run these commands to confirm integration:

```bash
# 1. Check environment variables are set
env | grep -E "WORKOS_(API_KEY|CLIENT_ID)" | wc -l
# Must output: 2

# 2. Check SDK is installed
ls node_modules/@workos-inc/node/package.json 2>/dev/null || echo "FAIL: SDK missing"

# 3. Check user schema has factor ID column
# (Adjust for your database - example for PostgreSQL)
psql -c "\d users" | grep mfa_factor_id || echo "FAIL: Schema missing MFA column"

# 4. Check enrollment endpoint exists
grep -r "enrollFactor" . --include="*.js" --include="*.ts" || echo "FAIL: No enrollment code"

# 5. Check verification endpoint exists
grep -r "verifyChallenge" . --include="*.js" --include="*.ts" || echo "FAIL: No verification code"

# 6. Check error handling exists
grep -r "already verified\|expired" . --include="*.js" --include="*.ts" || echo "FAIL: Missing error handlers"
```

**Do not mark complete until all checks pass.**

## Testing Procedure

### TOTP Flow Test

1. Enroll factor with type `totp`
2. Scan QR code with Google Authenticator
3. Create challenge
4. Enter 6-digit code from app
5. Verify challenge returns `valid: true`
6. Attempt to verify same challenge again — should error

### SMS Flow Test

1. Enroll factor with valid E.164 phone number
2. Create challenge — should receive SMS within 30 seconds
3. Enter 6-digit code from SMS
4. Verify challenge returns `valid: true`
5. Wait 11 minutes, create new challenge with same factor
6. Attempt to verify old challenge — should return expired error

### Invalid Input Tests

1. Attempt enrollment with phone `1234567890` (no `+`) — should error
2. Attempt enrollment with phone `+1 (555) 123-4567` (formatted) — should error
3. Attempt verification with code `12345` (5 digits) — should fail validation
4. Attempt verification with code `abc123` (non-numeric) — should fail validation

## Common Integration Patterns

### Express.js Middleware Pattern

```javascript
// middleware/mfa.js
async function requireMFA(req, res, next) {
  const user = req.user; // From your auth middleware
  
  if (!user.mfa_factor_id) {
    return next(); // No MFA enrolled, skip
  }
  
  if (req.session.mfaVerified) {
    return next(); // Already verified this session
  }
  
  return res.redirect('/mfa/verify');
}
```

### Next.js API Route Pattern

```javascript
// pages/api/auth/verify-mfa.js
export default async function handler(req, res) {
  const { challengeId, code } = req.body;
  
  try {
    const result = await workos.mfa.verifyChallenge({
      authentication_challenge_id: challengeId,
      code: code
    });
    
    if (result.valid) {
      req.session.mfaVerified = true;
      return res.json({ success: true });
    }
    
    return res.status(401).json({ error: 'Invalid code' });
  } catch (error) {
    // Handle specific errors per Step 7
  }
}
```

## Security Considerations

1. **Rate limiting:** Implement rate limits on verification endpoint (max 5 attempts per challenge recommended)
2. **Session handling:** Mark MFA as verified in session, do not re-verify on every request
3. **Factor ID exposure:** Factor IDs are sensitive — do not expose in client-side code or URLs
4. **Challenge reuse:** Never allow same challenge ID to be verified twice
5. **Code storage:** Never log or store OTP codes — they should only exist in transit

## WorkOS SSO Note

**CRITICAL:** Do NOT use MFA API with WorkOS SSO-authenticated users.

SSO providers (Okta, Azure AD, Google Workspace, etc.) have their own MFA:
- Users configure MFA in their IdP (Identity Provider)
- MFA is enforced at IdP during SSO flow
- WorkOS SSO inherits MFA state from IdP

**Use MFA API only for:**
- Username/password authenticated users
- Magic link authenticated users
- Any non-SSO authentication method

**Check authentication method before enabling MFA:**

```javascript
if (user.authMethod === 'sso') {
  // Do not offer MFA enrollment
  // MFA is handled by their SSO provider
}
```

## Related Skills

- **workos-authkit-base**: For primary authentication before MFA
- **workos-magic-link**: Alternative to password auth (can be combined with MFA)
