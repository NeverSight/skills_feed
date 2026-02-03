---
name: multiversx-dapp-audit
description: Audit frontend dApp components for security vulnerabilities in wallet integration and transaction handling. Use when reviewing React/TypeScript dApps using sdk-dapp, or assessing client-side security.
---

# MultiversX dApp Auditor

Audit the frontend components of MultiversX applications built with `@multiversx/sdk-dapp`. This skill focuses on client-side security, transaction construction, and wallet integration vulnerabilities.

## When to Use

- Reviewing React/TypeScript dApp code
- Auditing wallet connection implementations
- Assessing transaction signing security
- Checking for XSS and data exposure vulnerabilities
- Validating frontend-backend security boundaries

## 1. Transaction Construction Security

### The Threat Model
The frontend constructs transaction payloads that users sign. Vulnerabilities here can trick users into signing malicious transactions.

### Payload Manipulation
```typescript
// VULNERABLE: User input directly in transaction data
const sendTransaction = async (userInput: string) => {
    const tx = new Transaction({
        receiver: Address.newFromBech32(recipientAddress),
        data: Buffer.from(userInput),  // Attacker controls data!
        // ...
    });
    await signAndSend(tx);
};

// SECURE: Validate and sanitize all inputs
const sendTransaction = async (functionName: string, args: string[]) => {
    // Whitelist allowed functions
    const allowedFunctions = ['stake', 'unstake', 'claim'];
    if (!allowedFunctions.includes(functionName)) {
        throw new Error('Invalid function');
    }

    // Validate arguments
    const sanitizedArgs = args.map(arg => validateArgument(arg));

    const tx = new Transaction({
        receiver: contractAddress,
        data: Buffer.from(`${functionName}@${sanitizedArgs.join('@')}`),
        // ...
    });
    await signAndSend(tx);
};
```

### Critical Checks
| Check | Risk | Mitigation |
|-------|------|------------|
| Receiver address validation | Funds sent to wrong address | Validate against known addresses |
| Data payload construction | Malicious function calls | Whitelist allowed operations |
| Amount validation | Incorrect value transfers | Confirm amounts with user |
| Gas limit manipulation | Transaction failures | Use appropriate limits |

## 2. Signing Security

### Blind Signing Risks
Users may sign transactions without understanding the content:

```typescript
// DANGEROUS: Signing opaque data
const signMessage = async (data: string) => {
    const hash = keccak256(data);
    return await wallet.signMessage(hash);  // User sees only hash!
};

// SECURE: Show clear message to user
const signMessage = async (message: string) => {
    // Display message to user before signing
    const confirmed = await showConfirmationDialog({
        title: 'Sign Message',
        content: `You are signing: "${message}"`,
        warning: 'Only sign messages you understand'
    });

    if (!confirmed) throw new Error('User rejected');
    return await wallet.signMessage(message);
};
```

### Transaction Preview Requirements
Before signing, users should see:
- Recipient address (with verification if known)
- Amount being transferred
- Token type (EGLD, ESDT, NFT)
- Function being called (if smart contract interaction)
- Gas cost estimate

## 3. Sensitive Data Handling

### Private Key Security

```typescript
// CRITICAL VULNERABILITY: Never do this
localStorage.setItem('privateKey', wallet.privateKey);
localStorage.setItem('mnemonic', wallet.mnemonic);
sessionStorage.setItem('seed', wallet.seed);

// Check for these patterns in code review:
// - Any storage of private keys, mnemonics, or seeds
// - Logging of sensitive data
// - Sending sensitive data to APIs
```

### Secure Patterns
```typescript
// CORRECT: Use sdk-dapp's secure session management
import { initApp } from '@multiversx/sdk-dapp/out/methods/initApp/initApp';

initApp({
    storage: {
        getStorageCallback: () => sessionStorage  // Session only, not persistent
    },
    dAppConfig: {
        nativeAuth: {
            expirySeconds: 3600  // Short-lived tokens
        }
    }
});
```

### Access Token Security
```typescript
// VULNERABLE: Token exposed in URL
window.location.href = `https://api.example.com?accessToken=${token}`;

// VULNERABLE: Token in console
console.log('Auth token:', accessToken);

// SECURE: Token in Authorization header, never logged
fetch(apiUrl, {
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});
```

## 4. XSS Prevention

### User-Generated Content
```typescript
// VULNERABLE: Direct HTML injection
const UserProfile = ({ bio }: { bio: string }) => {
    return <div dangerouslySetInnerHTML={{ __html: bio }} />;  // XSS!
};

// SECURE: React's default escaping
const UserProfile = ({ bio }: { bio: string }) => {
    return <div>{bio}</div>;  // Automatically escaped
};

// If HTML is necessary, sanitize first
import DOMPurify from 'dompurify';

const UserProfile = ({ bio }: { bio: string }) => {
    const sanitized = DOMPurify.sanitize(bio);
    return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
};
```

### URL Handling
```typescript
// VULNERABLE: Unvalidated redirect
const handleCallback = () => {
    const returnUrl = new URLSearchParams(window.location.search).get('returnUrl');
    window.location.href = returnUrl!;  // Open redirect!
};

// SECURE: Validate redirect URL
const handleCallback = () => {
    const returnUrl = new URLSearchParams(window.location.search).get('returnUrl');
    const allowed = ['/', '/dashboard', '/profile'];
    if (allowed.includes(returnUrl || '')) {
        window.location.href = returnUrl!;
    } else {
        window.location.href = '/';  // Default safe redirect
    }
};
```

## 5. API Communication Security

### HTTPS Enforcement
```typescript
// VULNERABLE: HTTP connection
const API_URL = 'http://api.example.com';  // Insecure!

// SECURE: Always HTTPS
const API_URL = 'https://api.example.com';

// Verify in code: all API URLs must use https://
```

### Request/Response Validation
```typescript
// VULNERABLE: Trusting API response blindly
const balance = await fetch('/api/balance').then(r => r.json());
displayBalance(balance.amount);  // What if API is compromised?

// SECURE: Validate response structure
const response = await fetch('/api/balance').then(r => r.json());
if (typeof response.amount !== 'string' || !/^\d+$/.test(response.amount)) {
    throw new Error('Invalid balance response');
}
displayBalance(response.amount);
```

## 6. Audit Tools and Techniques

### Network Traffic Analysis
```bash
# Use browser DevTools Network tab to inspect:
# - All API requests and responses
# - Transaction data being sent
# - Headers (especially Authorization)
# - WebSocket messages

# Or use proxy tools:
# - Burp Suite
# - mitmproxy
# - Charles Proxy
```

### Code Review Patterns
```bash
# Search for dangerous patterns
grep -r "localStorage" src/
grep -r "dangerouslySetInnerHTML" src/
grep -r "eval(" src/
grep -r "privateKey\|mnemonic\|seed" src/
grep -r "console.log" src/  # Check for sensitive data logging
```

### Browser Security Headers Check
```
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

## 7. Authentication Flow Audit

### Wallet Connection
```typescript
// Verify wallet connection flow:
// 1. User initiates connection
// 2. Wallet provider prompts for approval
// 3. Only public address shared with dApp
// 4. No private data transmitted

// Check UnlockPanelManager usage
const unlockPanelManager = UnlockPanelManager.init({
    loginHandler: () => {
        // Verify: no sensitive data handling here
        navigate('/dashboard');
    }
});
```

### Session Management
```typescript
// Verify session security:
// - Token expiration enforced
// - Logout clears all session data
// - No persistent sensitive storage

const handleLogout = async () => {
    const provider = getAccountProvider();
    await provider.logout();
    // Verify: session storage cleared
    sessionStorage.clear();
    navigate('/');
};
```

## 8. Audit Checklist

### Transaction Security
- [ ] All transaction data validated before signing
- [ ] User shown clear transaction preview
- [ ] Recipient addresses validated
- [ ] Amount confirmations for large transfers
- [ ] Gas limits appropriate for operation

### Data Security
- [ ] No private keys in any storage
- [ ] No sensitive data in console logs
- [ ] Access tokens not exposed in URLs
- [ ] HTTPS enforced for all API calls

### XSS Prevention
- [ ] No `dangerouslySetInnerHTML` with user input
- [ ] No `eval()` with user input
- [ ] URL redirects validated
- [ ] Content-Security-Policy headers present

### Session Security
- [ ] Token expiration enforced
- [ ] Logout clears all session data
- [ ] Protected routes properly guarded
- [ ] Re-authentication for sensitive operations

## 9. Report Template

```markdown
# dApp Security Audit Report

## Scope
- Application: [name]
- Version: [version]
- Files reviewed: [count]

## Findings

### Critical
| ID | Description | Location | Recommendation |
|----|-------------|----------|----------------|
| C1 | ... | ... | ... |

### High
...

### Medium
...

### Informational
...

## Recommendations Summary
1. [Priority recommendation]
2. ...

## Conclusion
[Overall assessment]
```
