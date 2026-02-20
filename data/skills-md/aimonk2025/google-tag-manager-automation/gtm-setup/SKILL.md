---
name: gtm-setup
description: Automates Google Tag Manager API setup including googleapis installation, OAuth credential creation, token management, and prerequisites validation. Use when users need to "set up GTM API", "configure GTM API access", "get GTM OAuth credentials", "install googleapis", or encounter authentication errors. Handles complete technical setup from dependency installation through API connection verification.
---

# GTM Setup - Technical Prerequisites

Automate the complete GTM API setup process, from installing dependencies to validating API access.

## Workflow

### Phase 1: Prerequisites Check

**Step 1.1: Check Node.js Project**
```
Verify package.json exists:
- If missing → Error: "This must be run in a Node.js project"
- If exists → Continue
```

**Step 1.2: Check for Existing Setup**
```
Check for existing files:
- gtm-credentials.json → Already configured
- gtm-token.json → Already authorized
- gtm-config.json → Configuration exists

If all exist:
  → "GTM API already configured. Run validation to test connection."
  → Skip to Phase 6 (Validation)

If partial:
  → "Partial setup detected. Continuing from [step]..."
```

### Phase 2: Install googleapis

**Step 2.1: Auto-Install Package**
```
Run: npm install googleapis --save

Monitor output for:
✓ Success → Continue
✗ Error → Display error, suggest manual installation
```

**Step 2.2: Verify Installation**
```
Check package.json dependencies:
- "googleapis": "^..." present → Success
- Missing → Retry or manual install
```

### Phase 3: Google Cloud Project Setup

**Step 3.1: Guide Cloud Console Access**
```
Present clickable URLs:

Step 1: Create/Select Google Cloud Project
→ https://console.cloud.google.com/projectcreate

Step 2: Enable Google Tag Manager API
→ https://console.cloud.google.com/apis/library/tagmanager.googleapis.com

Step 3: Create OAuth 2.0 Credentials
→ https://console.cloud.google.com/apis/credentials

Wait for user confirmation at each step.
```

**Step 3.2: OAuth Credential Configuration**
```
Guide user through credential creation:

1. Click "Create Credentials" → "OAuth client ID"
2. Application type: "Desktop app"
3. Name: "GTM Automation Script"
4. Click "Create"
5. Download JSON file

Prompt: "Download the credentials JSON file and save it in your project root."
```

**Step 3.3: Save Credentials**
```
Ask user for downloaded file path:
→ "Where did you save the credentials file?"

Options:
a) File is in project root → Look for oauth2.keys.json or similar
b) User provides path → Copy to gtm-credentials.json
c) User pastes content → Write to gtm-credentials.json

Validate JSON structure:
- Has "installed" or "web" key
- Has "client_id", "client_secret", "redirect_uris"

If invalid → Error with specific issue
If valid → Save as gtm-credentials.json
```

### Phase 4: GTM Account & Container Configuration

**Step 4.1: Gather GTM Information**
```
Guide user to find GTM details:

"Open Google Tag Manager: https://tagmanager.google.com"

Q1: What is your GTM Account ID?
→ Hint: In GTM, go to Admin. Account ID is shown at top (format: 1234567890)

Q2: What is your GTM Container ID?
→ Hint: In GTM, select container. Container ID shown at top (format: GTM-XXXXXX)

Validate inputs:
- Account ID: Must be numeric
- Container ID: Must start with "GTM-"
```

**Step 4.2: Create Configuration File**
```
Generate gtm-config.json:

{
  "accountId": "[user input]",
  "containerId": "[user input]",
  "containerPublicId": "[user input]",
  "workspaceId": "1"
}

Save to project root.
```

### Phase 5: OAuth Authorization

**Step 5.1: Generate Auth URL**
```
Using googleapis library, generate OAuth consent URL.

Present to user:
"
=== Authorization Required ===

Open this URL in your browser to authorize access:

[Long Google OAuth URL]

This will:
1. Ask you to sign in to Google
2. Show permissions requested (Read/Write GTM access)
3. Redirect to a localhost URL with an authorization code

After authorizing, you'll see a page that says:
'The authentication flow has completed. You may close this window.'

Copy the FULL URL from your browser address bar.
"
```

**Step 5.2: Exchange Code for Token**
```
Prompt: "Paste the full redirect URL here:"

Extract authorization code from URL:
- URL format: http://localhost/?code=XXXX&scope=...
- Parse 'code' parameter

Exchange code for access/refresh tokens using OAuth2 client.

Save tokens to gtm-token.json:
{
  "access_token": "...",
  "refresh_token": "...",
  "scope": "...",
  "token_type": "Bearer",
  "expiry_date": 1234567890
}

Success message:
"✓ Authorization complete! Tokens saved to gtm-token.json"
```

### Phase 6: Validation & Testing

**Step 6.1: Test API Connection**
```
Using saved credentials and token, make test API call:

GET /tagmanager/v2/accounts/{accountId}/containers/{containerId}

Expected responses:
✓ 200 OK → Success! Container details returned
✗ 401 Unauthorized → Token invalid, re-authorize
✗ 403 Forbidden → Missing permissions, check API enable
✗ 404 Not Found → Wrong account/container ID
✗ Other → Display error details
```

**Step 6.2: Verify Permissions**
```
Check API response for required permissions:

Required GTM API scopes:
- tagmanager.edit.containers
- tagmanager.readonly

If missing scopes:
→ Error: "Insufficient permissions. Re-authorize with correct scopes."
→ Restart Phase 5
```

**Step 6.3: Final Confirmation**
```
Display success summary:

"
=== GTM API Setup Complete ===

✓ googleapis installed
✓ OAuth credentials configured (gtm-credentials.json)
✓ Access token obtained (gtm-token.json)
✓ GTM configuration saved (gtm-config.json)
✓ API connection validated

Account: [accountId]
Container: [containerPublicId]

Files created:
- gtm-credentials.json (OAuth credentials)
- gtm-token.json (Access token - DO NOT commit to git)
- gtm-config.json (GTM account/container info)

Next steps:
→ Add gtm-token.json to .gitignore
→ Invoke gtm-implementation skill to implement tracking

Ready to implement tracking? Invoke gtm-implementation skill.
"
```

## Scripts

Use the following scripts for automated steps:

### scripts/install-googleapis.js
```javascript
// Auto-install googleapis package
const { execSync } = require('child_process');

try {
  console.log('Installing googleapis...');
  execSync('npm install googleapis --save', { stdio: 'inherit' });
  console.log('✓ googleapis installed successfully');
} catch (error) {
  console.error('✗ Installation failed:', error.message);
  process.exit(1);
}
```

### scripts/validate-prerequisites.js
```javascript
// Validate existing setup files
const fs = require('fs');
const path = require('path');

const files = {
  'package.json': { required: true, description: 'Node.js project' },
  'gtm-credentials.json': { required: false, description: 'OAuth credentials' },
  'gtm-token.json': { required: false, description: 'Access token' },
  'gtm-config.json': { required: false, description: 'GTM configuration' }
};

console.log('Validating prerequisites...\n');

let allValid = true;
let setupStatus = {
  credentials: false,
  token: false,
  config: false
};

for (const [filename, config] of Object.entries(files)) {
  const exists = fs.existsSync(path.join(process.cwd(), filename));

  if (filename === 'gtm-credentials.json' && exists) setupStatus.credentials = true;
  if (filename === 'gtm-token.json' && exists) setupStatus.token = true;
  if (filename === 'gtm-config.json' && exists) setupStatus.config = true;

  const status = exists ? '✓' : (config.required ? '✗' : '○');
  console.log(`${status} ${filename} - ${config.description}`);

  if (config.required && !exists) {
    allValid = false;
  }
}

console.log('\nSetup status:');
if (setupStatus.credentials && setupStatus.token && setupStatus.config) {
  console.log('✓ Complete setup detected');
  console.log('→ Run test-connection.js to validate');
} else if (setupStatus.credentials || setupStatus.token || setupStatus.config) {
  console.log('○ Partial setup detected');
  if (!setupStatus.credentials) console.log('  Missing: OAuth credentials');
  if (!setupStatus.token) console.log('  Missing: Access token');
  if (!setupStatus.config) console.log('  Missing: GTM configuration');
} else {
  console.log('○ No setup detected');
  console.log('→ Start from Phase 3 (Google Cloud setup)');
}

process.exit(allValid ? 0 : 1);
```

### scripts/oauth-authorize.js
```javascript
// OAuth authorization flow
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const SCOPES = ['https://www.googleapis.com/auth/tagmanager.edit.containers'];
const TOKEN_PATH = path.join(process.cwd(), 'gtm-token.json');
const CREDENTIALS_PATH = path.join(process.cwd(), 'gtm-credentials.json');

// Load credentials
const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;

const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

// Generate auth URL
const authUrl = oAuth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: SCOPES,
});

console.log('\n=== GTM API Authorization ===\n');
console.log('Open this URL in your browser to authorize:\n');
console.log(authUrl);
console.log('\nAfter authorization, copy the full redirect URL from your browser.\n');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('Paste the redirect URL here: ', (redirectUrl) => {
  rl.close();

  // Extract code from URL
  const url = new URL(redirectUrl);
  const code = url.searchParams.get('code');

  if (!code) {
    console.error('✗ No authorization code found in URL');
    process.exit(1);
  }

  // Exchange code for token
  oAuth2Client.getToken(code, (err, token) => {
    if (err) {
      console.error('✗ Error retrieving access token:', err);
      process.exit(1);
    }

    // Save token
    fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2));
    console.log('\n✓ Token saved to', TOKEN_PATH);
    console.log('\n=== Authorization Complete ===\n');
    console.log('You can now use the GTM API.');
    console.log('\nIMPORTANT: Add gtm-token.json to .gitignore\n');
  });
});
```

### scripts/test-connection.js
```javascript
// Test GTM API connection
const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const TOKEN_PATH = path.join(process.cwd(), 'gtm-token.json');
const CREDENTIALS_PATH = path.join(process.cwd(), 'gtm-credentials.json');
const CONFIG_PATH = path.join(process.cwd(), 'gtm-config.json');

// Check files exist
if (!fs.existsSync(CREDENTIALS_PATH)) {
  console.error('✗ gtm-credentials.json not found');
  process.exit(1);
}

if (!fs.existsSync(TOKEN_PATH)) {
  console.error('✗ gtm-token.json not found. Run oauth-authorize.js first.');
  process.exit(1);
}

if (!fs.existsSync(CONFIG_PATH)) {
  console.error('✗ gtm-config.json not found');
  process.exit(1);
}

// Load files
const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
const token = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));

const { client_secret, client_id, redirect_uris } = credentials.installed || credentials.web;

// Create OAuth client
const oAuth2Client = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);
oAuth2Client.setCredentials(token);

// Create GTM client
const tagmanager = google.tagmanager({ version: 'v2', auth: oAuth2Client });

console.log('\n=== Testing GTM API Connection ===\n');
console.log(`Account ID: ${config.accountId}`);
console.log(`Container ID: ${config.containerPublicId}\n`);

// Test API call
const path_url = `accounts/${config.accountId}/containers/${config.containerId}`;

tagmanager.accounts.containers.get({ path: path_url })
  .then(response => {
    console.log('✓ Connection successful!\n');
    console.log('Container details:');
    console.log(`  Name: ${response.data.name}`);
    console.log(`  Public ID: ${response.data.publicId}`);
    console.log(`  Usage Context: ${response.data.usageContext.join(', ')}\n`);
    console.log('=== Setup Verified ===\n');
    console.log('Ready to use GTM API!\n');
  })
  .catch(error => {
    console.error('✗ Connection failed\n');

    if (error.code === 401) {
      console.error('Error: Unauthorized (401)');
      console.error('→ Token may be expired. Run oauth-authorize.js again.\n');
    } else if (error.code === 403) {
      console.error('Error: Forbidden (403)');
      console.error('→ Check that GTM API is enabled in Google Cloud Console.\n');
    } else if (error.code === 404) {
      console.error('Error: Not Found (404)');
      console.error('→ Check account ID and container ID in gtm-config.json.\n');
    } else {
      console.error('Error:', error.message, '\n');
    }

    process.exit(1);
  });
```

## References

- `references/google-cloud-setup.md` - Detailed Google Cloud Console setup guide with screenshots

## Important Guidelines

### Security Best Practices

1. **Never commit tokens**:
   - Add `gtm-token.json` to `.gitignore`
   - Tokens contain sensitive access credentials

2. **Credentials file security**:
   - `gtm-credentials.json` can be committed (contains no secrets for Desktop app type)
   - But recommend adding to `.gitignore` for extra security

3. **Token refresh**:
   - Tokens expire after 1 hour
   - Refresh token (included) allows automatic renewal
   - googleapis handles refresh automatically

### Common Issues

**Issue**: "googleapis not found"
→ Solution: Run `npm install googleapis --save`

**Issue**: "Invalid redirect URI"
→ Solution: Ensure OAuth client type is "Desktop app", not "Web application"

**Issue**: "403 Forbidden"
→ Solution: Enable GTM API in Google Cloud Console

**Issue**: "404 Not Found"
→ Solution: Verify account ID and container ID are correct

**Issue**: "Token expired"
→ Solution: Run oauth-authorize.js again to get new token

### Testing

After setup, verify with:
```bash
node scripts/test-connection.js
```

Expected output:
```
✓ Connection successful!

Container details:
  Name: My Website
  Public ID: GTM-XXXXXX
  Usage Context: web

=== Setup Verified ===
```

## Execution Checklist

- [ ] package.json exists (Node.js project)
- [ ] googleapis installed
- [ ] Google Cloud project created
- [ ] GTM API enabled
- [ ] OAuth credentials created and downloaded
- [ ] gtm-credentials.json saved
- [ ] GTM account ID obtained
- [ ] GTM container ID obtained
- [ ] gtm-config.json created
- [ ] OAuth authorization completed
- [ ] gtm-token.json saved
- [ ] API connection tested successfully
- [ ] gtm-token.json added to .gitignore

## Supporting Files

- `examples/sample.md` - Example setup session showing each phase output and files created

## Output Files

- **gtm-credentials.json** - OAuth 2.0 client credentials
- **gtm-token.json** - Access token and refresh token (SENSITIVE)
- **gtm-config.json** - GTM account and container configuration

## Handoff

After successful setup:
```
✓ GTM API configured and validated

Next step: Invoke gtm-implementation skill to:
- Implement dataLayer events in your code
- Create GTM variables, triggers, and tags via API

Ready to implement? Invoke gtm-implementation skill.
```

## Common Questions

**Q: Can I use the same credentials for multiple projects?**
A: Yes. Copy gtm-credentials.json to other projects. Each project needs its own token (gtm-token.json).

**Q: What if I have multiple GTM containers?**
A: Run setup for each container separately. Create different gtm-config.json files or use different project directories.

**Q: Do I need a Google Cloud billing account?**
A: No. GTM API is free to use. No billing account required.

**Q: Can I revoke access later?**
A: Yes. Go to https://myaccount.google.com/permissions and revoke access to "GTM Automation Script".

**Q: What scopes does this request?**
A: `tagmanager.edit.containers` - Read and write access to GTM containers. This allows creating/updating variables, triggers, tags.
