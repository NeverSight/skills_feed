---
name: haveibeenpwned
description: HaveIBeenPwned API Documentation - Check if email accounts or passwords have been compromised in data breaches
---

# Have I Been Pwned API Skill

Expert assistance for integrating the Have I Been Pwned (HIBP) API v3 to check for compromised accounts, passwords, and data breaches. This skill provides comprehensive guidance for building security tools, breach notification systems, and password validation features.

## When to Use This Skill

This skill should be triggered when:
- **Checking if emails/accounts appear in data breaches** - "check if this email was pwned"
- **Validating password security** - "check if password is in breach database"
- **Building breach notification systems** - "notify users about compromised accounts"
- **Implementing password validation** - "prevent users from choosing pwned passwords"
- **Querying stealer logs** - "check if credentials were stolen by malware"
- **Integrating HIBP into authentication flows** - "add breach checking to login"
- **Monitoring domains for compromised emails** - "track breaches affecting our domain"
- **Working with the HIBP API** - any questions about authentication, rate limits, or endpoints

## Quick Reference

### 1. Basic Account Breach Check

```python
import requests

def check_account_breaches(email, api_key):
    """Check if an account appears in any breaches"""
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MyApp/1.0'
    }

    url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # List of breach objects
    elif response.status_code == 404:
        return []  # Account not found in breaches
    else:
        response.raise_for_status()

# Usage
breaches = check_account_breaches('user@example.com', 'your-api-key')
print(f"Found in {len(breaches)} breaches")
```

### 2. Password Breach Check (k-Anonymity)

```python
import hashlib
import requests

def check_password_pwned(password):
    """Check if password appears in breaches using k-anonymity"""
    # Hash password with SHA-1
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    # Query API with first 5 characters only
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url)

    # Parse response for matching suffix
    hashes = (line.split(':') for line in response.text.splitlines())
    for hash_suffix, count in hashes:
        if hash_suffix == suffix:
            return int(count)  # Times password appears in breaches
    return 0  # Password not found

# Usage
count = check_password_pwned('password123')
if count > 0:
    print(f"⚠️ Password found {count} times in breaches!")
```

### 3. Get All Breaches in System

```python
import requests

def get_all_breaches(domain=None):
    """Retrieve all breaches, optionally filtered by domain"""
    url = 'https://haveibeenpwned.com/api/v3/breaches'
    params = {'domain': domain} if domain else {}

    headers = {'user-agent': 'MyApp/1.0'}
    response = requests.get(url, headers=headers, params=params)

    return response.json()

# Usage - no authentication required
breaches = get_all_breaches()
print(f"Total breaches: {len(breaches)}")

# Filter by domain
adobe_breaches = get_all_breaches(domain='adobe.com')
```

### 4. Monitor for New Breaches

```python
import requests
import time

def monitor_latest_breach(check_interval=3600):
    """Poll for new breaches every hour"""
    last_breach_name = None

    while True:
        url = 'https://haveibeenpwned.com/api/v3/latestbreach'
        headers = {'user-agent': 'MyApp/1.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            breach = response.json()
            if breach['Name'] != last_breach_name:
                print(f"🆕 New breach: {breach['Title']}")
                print(f"   Accounts affected: {breach['PwnCount']:,}")
                last_breach_name = breach['Name']

        time.sleep(check_interval)
```

### 5. Domain-Wide Breach Search

```python
import requests

def search_domain_breaches(domain, api_key):
    """Search for all breached emails in a verified domain"""
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MyApp/1.0'
    }

    url = f'https://haveibeenpwned.com/api/v3/breacheddomain/{domain}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        results = response.json()
        # Returns: {"alias1": ["Adobe"], "alias2": ["Adobe", "Gawker"]}
        total_affected = len(results)
        print(f"Found {total_affected} compromised accounts")
        return results
    else:
        response.raise_for_status()
```

### 6. Check Pastes for Account

```python
import requests

def check_pastes(email, api_key):
    """Check if email appears in any pastes"""
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MyApp/1.0'
    }

    url = f'https://haveibeenpwned.com/api/v3/pasteaccount/{email}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pastes = response.json()
        for paste in pastes:
            print(f"{paste['Source']}: {paste['Title']}")
            print(f"  Date: {paste['Date']}")
            print(f"  Emails found: {paste['EmailCount']}")
        return pastes
    elif response.status_code == 404:
        return []  # No pastes found
```

### 7. Enhanced Password Check with Padding

```python
import hashlib
import requests

def check_password_secure(password):
    """Check password with padding to prevent inference attacks"""
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    headers = {'Add-Padding': 'true'}
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url, headers=headers)

    # Parse response, ignore padded entries (count=0)
    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix and int(count) > 0:
            return int(count)
    return 0
```

### 8. Handle Rate Limiting

```python
import requests
import time

def api_call_with_retry(url, headers, max_retries=3):
    """Make API call with automatic retry on rate limit"""
    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            # Rate limited - wait and retry
            retry_after = int(response.headers.get('retry-after', 2))
            print(f"Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            continue

        return response

    raise Exception("Max retries exceeded")
```

### 9. Check Subscription Status

```python
import requests

def get_subscription_info(api_key):
    """Retrieve API subscription details and limits"""
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MyApp/1.0'
    }

    url = 'https://haveibeenpwned.com/api/v3/subscription/status'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        info = response.json()
        print(f"Plan: {info['SubscriptionName']}")
        print(f"Rate limit: {info['Rpm']} requests/minute")
        print(f"Valid until: {info['SubscribedUntil']}")
        return info
```

### 10. Stealer Logs Search

```python
import requests

def check_stealer_logs(email, api_key):
    """Check if credentials appear in info stealer malware logs"""
    headers = {
        'hibp-api-key': api_key,
        'user-agent': 'MyApp/1.0'
    }

    url = f'https://haveibeenpwned.com/api/v3/stealerlogsbyemail/{email}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        domains = response.json()  # List of website domains
        print(f"Credentials found for {len(domains)} websites")
        return domains
    elif response.status_code == 404:
        return []  # Not found in stealer logs

# Requires Pwned 5+ subscription
```

## Key Concepts

### Authentication
- **API Key Format**: 32-character hexadecimal string
- **Header**: `hibp-api-key: {your-key}`
- **User-Agent Required**: Must set valid user-agent header (returns 403 if missing)
- **Test Key**: `00000000000000000000000000000000` for integration testing

### k-Anonymity Model
The Pwned Passwords API uses **k-anonymity** to protect user privacy:
1. Client hashes password locally with SHA-1
2. Sends only **first 5 characters** of hash to API
3. API returns ~800 matching hash suffixes
4. Client checks locally if full hash matches

This ensures the actual password **never leaves your system**.

### Rate Limiting
- **Varies by subscription tier**: Pwned 5 = 1,000 requests/minute
- **HTTP 429 response** when exceeded with `retry-after` header
- **Pwned Passwords API**: No rate limit
- **Best practice**: Implement exponential backoff on 429 responses

### Breach Model Attributes
Key fields in breach objects:
- **Name**: Unique identifier (e.g., "Adobe")
- **Title**: Human-readable name
- **BreachDate**: When breach occurred (ISO 8601)
- **PwnCount**: Total compromised accounts
- **DataClasses**: Types of data exposed (emails, passwords, etc.)
- **IsVerified**: Breach authenticity confirmed
- **IsSensitive**: Excluded from public searches

### Response Codes
| Code | Meaning |
|------|---------|
| 200 | Success - data found |
| 404 | Not found (account not in breaches) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (missing user-agent) |
| 429 | Rate limit exceeded |

## Reference Files

This skill includes comprehensive API documentation in `references/`:

- **other.md** - Complete HIBP API v3 reference with all endpoints, authentication, and usage examples

The reference file contains:
- **All API endpoints** - Breaches, pastes, passwords, stealer logs
- **Request/response formats** - Headers, parameters, JSON structures
- **Authentication details** - API key setup and usage
- **Rate limiting information** - Subscription tiers and retry strategies
- **Test accounts** - Pre-configured test data for integration
- **Code examples** - Real-world implementation patterns

Use `view` to read the reference file when you need detailed information about specific endpoints or advanced features.

## Working with This Skill

### For Beginners
Start by understanding the core concepts:
1. **Password checking** - Use Pwned Passwords API (no authentication required)
2. **Account breaches** - Requires API key from haveibeenpwned.com
3. **k-Anonymity** - Learn how password hashing protects privacy

Begin with Quick Reference examples #1 (breach check) and #2 (password check).

### For Integration Projects
Focus on:
1. **Authentication setup** - Get API key and configure headers
2. **Rate limiting** - Implement retry logic (example #8)
3. **Error handling** - Handle 404, 401, 429 responses properly
4. **User experience** - Provide clear messaging about breach exposure

Review Quick Reference examples #5 (domain search) and #9 (subscription info).

### For Production Systems
Consider:
1. **Caching** - Store breach results to reduce API calls
2. **Background processing** - Check breaches asynchronously
3. **Monitoring** - Track new breaches with latest breach endpoint (example #4)
4. **Privacy** - Never log passwords, use k-anonymity model
5. **Compliance** - Follow attribution requirements (CC BY 4.0)

### For Security Tools
Advanced patterns:
1. **Stealer logs** - Check malware-stolen credentials (example #10)
2. **Domain monitoring** - Track all compromised accounts in your organization
3. **Paste monitoring** - Alert on email exposure in public pastes (example #6)
4. **Padding** - Use response padding to prevent inference attacks (example #7)

## Common Patterns

### Pattern 1: Sign-up Password Validation
```python
# Prevent users from choosing compromised passwords
def validate_signup_password(password):
    count = check_password_pwned(password)
    if count > 0:
        return False, f"This password appears in {count} data breaches"
    return True, "Password is secure"
```

### Pattern 2: Breach Notification System
```python
# Notify users when their account appears in new breach
def notify_affected_users():
    latest = get_latest_breach()
    affected_users = query_users_in_breach(latest['Name'])
    for user in affected_users:
        send_notification(user, latest)
```

### Pattern 3: Compliance Check
```python
# Verify all domain accounts for compliance reporting
def domain_security_audit(domain, api_key):
    breached = search_domain_breaches(domain, api_key)
    report = {
        'total_accounts': len(breached),
        'affected_accounts': breached,
        'timestamp': datetime.now()
    }
    return report
```

## API Endpoints Summary

### Authenticated Endpoints (Require API Key)
- `GET /breachedaccount/{account}` - Check account breaches
- `GET /pasteaccount/{account}` - Check pastes
- `GET /breacheddomain/{domain}` - Domain-wide search
- `GET /subscribeddomains` - List verified domains
- `GET /subscription/status` - Check subscription
- `GET /stealerlogsbyemail/{email}` - Stealer logs by email
- `GET /stealerlogsbywebsitedomain/{domain}` - Stealer logs by site
- `GET /stealerlogsbyemaildomain/{domain}` - Stealer logs by email domain

### Public Endpoints (No Authentication)
- `GET /breaches` - All breaches in system
- `GET /breach/{name}` - Single breach details
- `GET /latestbreach` - Most recent breach
- `GET /dataclasses` - List of data types
- `GET https://api.pwnedpasswords.com/range/{prefix}` - Password check

## Testing

### Test Accounts
Use these on domain `hibp-integration-tests.com`:
- `account-exists@` - Has breaches and pastes
- `multiple-breaches@` - Three different breaches
- `spam-list-only@` - Only spam-flagged breach
- `stealer-log@` - In stealer logs
- `opt-out@` - No results (opted out)

### Test API Key
Use `00000000000000000000000000000000` for integration testing.

## Best Practices

1. **Always set User-Agent** - Required header, returns 403 without it
2. **Use HTTPS only** - API requires TLS 1.2+
3. **Implement retry logic** - Handle 429 rate limits gracefully
4. **Cache breach data** - Reduce API calls for frequently checked accounts
5. **Never log passwords** - Use k-anonymity model, hash locally
6. **Provide attribution** - Link to haveibeenpwned.com (CC BY 4.0 license)
7. **Handle 404 gracefully** - "Not found" is good news for users
8. **Use padding for passwords** - Add `Add-Padding: true` header

## Resources

### Official Links
- API Documentation: https://haveibeenpwned.com/API/v3
- Get API Key: https://haveibeenpwned.com/API/Key
- Dashboard: https://haveibeenpwned.com/DomainSearch

### Community Tools
- **PwnedPasswordsDownloader** (GitHub) - Download full password database
- Integration libraries available for Python, JavaScript, Go, C#, and more

## Acceptable Use

**Permitted:**
- Security tools and breach notifications
- Password validation in authentication systems
- Compliance and security audits
- Educational and research purposes

**Prohibited:**
- Targeting or harming breach victims
- Denial-of-service attacks
- Circumventing security measures
- Misrepresenting data source
- Automating undocumented APIs

Violations may result in API key revocation or IP blocking.

## Notes

- Breach data licensed under **Creative Commons Attribution 4.0**
- Pwned Passwords has no licensing requirements
- CORS only supported for unauthenticated endpoints
- Never expose API keys in client-side code
- Service tracks **917+ breaches** as of API documentation date
