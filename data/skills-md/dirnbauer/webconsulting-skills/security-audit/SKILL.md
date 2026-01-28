---
name: security-audit
description: Security audit patterns for PHP/OWASP. Use when conducting security assessments, identifying vulnerabilities (XXE, SQL injection, XSS), or CVSS scoring.
version: 1.0.0
triggers:
  - security
  - audit
  - owasp
  - vulnerabilities
  - xxe
  - sql injection
  - xss
  - cvss
---

# Security Audit Skill

Security audits, vulnerability assessment, and secure coding patterns aligned with OWASP.

## Expertise Areas

- **Vulnerabilities**: XXE, SQL injection, XSS, CSRF, auth flaws, insecure deserialization
- **Risk Scoring**: CVSS v3.1 methodology
- **Secure Coding**: Input validation, output encoding, cryptography, session management

## OWASP Top 10 (2021)

| Rank | Category | Description |
|------|----------|-------------|
| A01 | Broken Access Control | Unauthorized access to resources |
| A02 | Cryptographic Failures | Weak encryption, exposed secrets |
| A03 | Injection | SQL, NoSQL, OS, LDAP injection |
| A04 | Insecure Design | Missing security controls by design |
| A05 | Security Misconfiguration | Default configs, verbose errors |
| A06 | Vulnerable Components | Outdated libraries with CVEs |
| A07 | Auth Failures | Broken authentication/session |
| A08 | Data Integrity Failures | Insecure deserialization, CI/CD |
| A09 | Logging Failures | Missing audit logs, monitoring |
| A10 | SSRF | Server-side request forgery |

## XXE Prevention

XML External Entity injection allows attackers to read files, perform SSRF, or DoS.

### Vulnerable Code

```php
// ❌ VULNERABLE - External entities enabled
$doc = new DOMDocument();
$doc->loadXML($userInput);
```

### Secure Code

```php
// ✅ SECURE - Disable external entities
$doc = new DOMDocument();
$doc->loadXML(
    $userInput,
    LIBXML_NONET | LIBXML_NOENT | LIBXML_DTDLOAD
);

// Or use libxml_disable_entity_loader for older PHP
libxml_disable_entity_loader(true); // Deprecated in PHP 8.0
```

### SimpleXML Secure Usage

```php
// ✅ SECURE
$xml = simplexml_load_string(
    $userInput,
    'SimpleXMLElement',
    LIBXML_NONET | LIBXML_NOENT
);
```

## SQL Injection Prevention

### Vulnerable Code

```php
// ❌ VULNERABLE - Direct string interpolation
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];
$result = $pdo->query($query);
```

### Secure Code - PDO

```php
// ✅ SECURE - Prepared statements
$stmt = $pdo->prepare('SELECT * FROM users WHERE id = ?');
$stmt->execute([$id]);
$result = $stmt->fetchAll();
```

### Secure Code - TYPO3 QueryBuilder

```php
// ✅ SECURE - TYPO3 QueryBuilder with named parameters
$queryBuilder = $this->connectionPool->getQueryBuilderForTable('users');
$result = $queryBuilder
    ->select('*')
    ->from('users')
    ->where(
        $queryBuilder->expr()->eq(
            'uid',
            $queryBuilder->createNamedParameter($id, Connection::PARAM_INT)
        )
    )
    ->executeQuery()
    ->fetchAllAssociative();
```

## XSS Prevention

### Output Encoding

```php
// ✅ SECURE - Escape all output
echo htmlspecialchars($userInput, ENT_QUOTES | ENT_HTML5, 'UTF-8');
```

### Fluid Templates

```html
<!-- ✅ SAFE - Auto-escaped -->
{variable}

<!-- ❌ DANGEROUS - Raw output, use only for trusted HTML -->
{variable -> f:format.raw()}

<!-- ✅ SAFE - Explicit escaping -->
{variable -> f:format.htmlspecialchars()}
```

### Content Security Policy

```php
// Set CSP header
header("Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';");
```

## CSRF Protection

### Form Tokens

```php
// Generate token
$token = bin2hex(random_bytes(32));
$_SESSION['csrf_token'] = $token;

// Validate token
if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    throw new SecurityException('CSRF token mismatch');
}
```

### TYPO3 CSRF Protection

```php
use TYPO3\CMS\Core\FormProtection\FormProtectionFactory;

// Generate
$formProtection = $this->formProtectionFactory->createFromRequest($request);
$token = $formProtection->generateToken('myForm');

// Validate
$isValid = $formProtection->validateToken($token, 'myForm');
```

## API Key Encryption at Rest

Never store API keys in plain text. Use sodium for encryption:

```php
<?php
declare(strict_types=1);

final class ApiKeyEncryption
{
    public function encrypt(string $apiKey, string $key): string
    {
        $nonce = random_bytes(SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        $encrypted = sodium_crypto_secretbox($apiKey, $nonce, $key);
        return 'enc:' . base64_encode($nonce . $encrypted);
    }

    public function decrypt(string $encrypted, string $key): string
    {
        if (!str_starts_with($encrypted, 'enc:')) {
            throw new \InvalidArgumentException('Invalid encrypted format');
        }

        $decoded = base64_decode(substr($encrypted, 4));
        $nonce = substr($decoded, 0, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);
        $ciphertext = substr($decoded, SODIUM_CRYPTO_SECRETBOX_NONCEBYTES);

        $decrypted = sodium_crypto_secretbox_open($ciphertext, $nonce, $key);
        if ($decrypted === false) {
            throw new \RuntimeException('Decryption failed');
        }

        return $decrypted;
    }
}
```

## Password Hashing

### Modern Password Hashing

```php
// ✅ SECURE - Use password_hash with Argon2id
$hash = password_hash($password, PASSWORD_ARGON2ID);

// Verify
if (password_verify($inputPassword, $storedHash)) {
    // Valid password
}

// Check if rehash needed (algorithm upgrade)
if (password_needs_rehash($storedHash, PASSWORD_ARGON2ID)) {
    $newHash = password_hash($password, PASSWORD_ARGON2ID);
    // Update stored hash
}
```

### TYPO3 Password Hashing

```php
use TYPO3\CMS\Core\Crypto\PasswordHashing\PasswordHashFactory;

$hashInstance = GeneralUtility::makeInstance(PasswordHashFactory::class)
    ->getDefaultHashInstance('BE');

$hash = $hashInstance->getHashedPassword($password);
$isValid = $hashInstance->checkPassword($password, $hash);
```

## CVSS v3.1 Scoring

### Base Metrics

| Metric | Values |
|--------|--------|
| Attack Vector (AV) | Network (N), Adjacent (A), Local (L), Physical (P) |
| Attack Complexity (AC) | Low (L), High (H) |
| Privileges Required (PR) | None (N), Low (L), High (H) |
| User Interaction (UI) | None (N), Required (R) |
| Scope (S) | Unchanged (U), Changed (C) |
| Confidentiality (C) | None (N), Low (L), High (H) |
| Integrity (I) | None (N), Low (L), High (H) |
| Availability (A) | None (N), Low (L), High (H) |

### Severity Ratings

| Score | Severity |
|-------|----------|
| 0.0 | None |
| 0.1 - 3.9 | Low |
| 4.0 - 6.9 | Medium |
| 7.0 - 8.9 | High |
| 9.0 - 10.0 | Critical |

### Example CVSS Vector

```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
Score: 9.8 (Critical)

Translation:
- Network accessible
- Low complexity
- No privileges required
- No user interaction
- Unchanged scope
- High impact on C/I/A
```

## Security Audit Checklist

### Authentication & Authorization
- [ ] Passwords hashed with Argon2id or bcrypt
- [ ] MFA enabled for privileged accounts
- [ ] Session tokens regenerated on login
- [ ] Proper logout (session destruction)
- [ ] Role-based access control (RBAC)

### Input Validation
- [ ] All input validated server-side
- [ ] Parameterized SQL queries (no interpolation)
- [ ] XML external entities disabled
- [ ] File uploads restricted (type, size, location)

### Output Encoding
- [ ] Context-appropriate encoding (HTML, JS, URL)
- [ ] Content Security Policy configured
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY or SAMEORIGIN

### Secrets Management
- [ ] API keys encrypted at rest
- [ ] Secrets not in version control
- [ ] Environment variables for config
- [ ] Key rotation policy

### Transport Security
- [ ] TLS 1.2+ enforced
- [ ] HSTS header set
- [ ] Certificate validity monitored

### Logging & Monitoring
- [ ] Authentication events logged
- [ ] Failed login attempts tracked
- [ ] Sensitive data not logged
- [ ] Audit trail for privileged actions

## Secure Configuration (TYPO3)

```php
// config/system/settings.php
return [
    'BE' => [
        'debug' => false,
        'lockIP' => 4,
        'lockSSL' => true,
    ],
    'FE' => [
        'debug' => false,
        'lockSSL' => true,
    ],
    'SYS' => [
        'displayErrors' => 0,
        'devIPmask' => '',
        'trustedHostsPattern' => 'example\\.com|www\\.example\\.com',
        'features' => [
            'security.backend.enforceReferrer' => true,
            'security.frontend.enforceContentSecurityPolicy' => true,
        ],
    ],
];
```

---

## Related Skills

- [security-incident-reporting](../security-incident-reporting/SKILL.md) - Post-incident documentation, NIST/SANS frameworks, DDoS post-mortem, CVE correlation
- [typo3-security](../typo3-security/SKILL.md) - TYPO3-specific hardening and configuration

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/security-audit-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
