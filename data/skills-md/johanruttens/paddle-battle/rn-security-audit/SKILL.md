---
name: rn-security-audit
description: Security audit skill for React Native applications. Use when reviewing code for vulnerabilities, detecting leaked secrets (API keys, tokens, credentials), identifying exposed personal data (PII), checking insecure storage, validating authentication flows, reviewing network security, and ensuring compliance with mobile security best practices (OWASP MASVS). Covers both JavaScript/TypeScript and native iOS/Android code.
---

# React Native Security Audit

Identify vulnerabilities and sensitive data exposure in React Native apps.

## Quick Scan Commands

### Find Hardcoded Secrets

```bash
# API keys and tokens
grep -rniE "(api[_-]?key|apikey|api[_-]?secret|access[_-]?token|auth[_-]?token|bearer|private[_-]?key|secret[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9]" --include="*.js" --include="*.ts" --include="*.tsx" --include="*.jsx" .

# AWS credentials
grep -rniE "(AKIA|ASIA)[A-Z0-9]{16}" --include="*.js" --include="*.ts" --include="*.json" .
grep -rniE "aws[_-]?(secret|access|key)" --include="*.js" --include="*.ts" --include="*.json" .

# Firebase/Google
grep -rniE "(AIza[0-9A-Za-z\-_]{35})" .
grep -rniE "firebase.*['\"][a-zA-Z0-9\-]+\.firebaseio\.com" .

# Generic secrets
grep -rniE "(password|passwd|pwd|secret)\s*[:=]\s*['\"][^'\"]{4,}" --include="*.js" --include="*.ts" --include="*.tsx" .

# Private keys
grep -rniE "-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY" .

# JWT tokens (hardcoded)
grep -rniE "eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*" .
```

### Find PII Exposure

```bash
# Email patterns in code
grep -rniE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" --include="*.js" --include="*.ts" .

# Phone numbers
grep -rniE "(\+?1?[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}" --include="*.js" --include="*.ts" .

# SSN patterns
grep -rniE "\b\d{3}[-]?\d{2}[-]?\d{4}\b" --include="*.js" --include="*.ts" .

# Credit card patterns
grep -rniE "\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b" .

# Console.log with sensitive data
grep -rniE "console\.(log|debug|info|warn)\s*\([^)]*?(password|token|secret|key|credential|ssn|credit)" --include="*.js" --include="*.ts" --include="*.tsx" .
```

### Find Insecure Patterns

```bash
# HTTP (not HTTPS)
grep -rniE "http://(?!localhost|127\.0\.0\.1|10\.|192\.168\.)" --include="*.js" --include="*.ts" --include="*.json" .

# Disabled SSL verification
grep -rniE "(rejectUnauthorized|SSL_VERIFY|verify.*false)" --include="*.js" --include="*.ts" .

# eval() usage
grep -rniE "\beval\s*\(" --include="*.js" --include="*.ts" --include="*.tsx" .

# innerHTML (XSS risk)
grep -rniE "(innerHTML|dangerouslySetInnerHTML)" --include="*.js" --include="*.ts" --include="*.tsx" .

# AsyncStorage (unencrypted)
grep -rniE "AsyncStorage\.(setItem|getItem|multiSet).*?(password|token|secret|key|credential)" --include="*.js" --include="*.ts" .

# Insecure random
grep -rniE "Math\.random\s*\(\)" --include="*.js" --include="*.ts" .
```

## Vulnerability Categories

### 1. Hardcoded Secrets (CRITICAL)

**What to find:**
- API keys, tokens, passwords in source code
- Credentials in config files committed to repo
- Secrets in environment files checked into git

**Check files:**
```bash
# Common locations for leaked secrets
cat .env .env.local .env.development .env.production 2>/dev/null
cat app.json app.config.js babel.config.js metro.config.js 2>/dev/null
cat ios/*/Info.plist android/app/src/main/AndroidManifest.xml 2>/dev/null
```

**Remediation:**
```javascript
// BAD
const API_KEY = "sk-1234567890abcdef";

// GOOD - use environment variables
import Config from 'react-native-config';
const API_KEY = Config.API_KEY;

// GOOD - use secure storage for runtime secrets
import * as Keychain from 'react-native-keychain';
await Keychain.setGenericPassword('api', token);
```

### 2. Insecure Data Storage (HIGH)

**Vulnerable patterns:**
```javascript
// INSECURE - AsyncStorage is unencrypted
await AsyncStorage.setItem('userToken', token);
await AsyncStorage.setItem('password', password);

// INSECURE - Storing in state/redux persistor unencrypted
const persistConfig = {
  key: 'root',
  storage: AsyncStorage, // Unencrypted!
  whitelist: ['auth']    // Contains tokens!
};
```

**Check for:**
```bash
# Find AsyncStorage usage with sensitive data
grep -rniE "AsyncStorage" --include="*.js" --include="*.ts" -A2 -B2 | grep -iE "(token|password|secret|key|auth|credential|session)"

# Check Redux persist config
grep -rniE "persistConfig|persistReducer" --include="*.js" --include="*.ts" -A10
```

**Secure alternatives:**
```javascript
// iOS Keychain / Android Keystore
import * as Keychain from 'react-native-keychain';
await Keychain.setGenericPassword('user', token);

// Encrypted storage
import EncryptedStorage from 'react-native-encrypted-storage';
await EncryptedStorage.setItem('token', token);

// Expo SecureStore
import * as SecureStore from 'expo-secure-store';
await SecureStore.setItemAsync('token', token);
```

### 3. Network Security (HIGH)

**Check for:**
```bash
# Find all URLs
grep -rniE "(https?://[^\s'\"]+)" --include="*.js" --include="*.ts" -o | sort -u

# Find fetch/axios configs
grep -rniE "(fetch|axios)\s*\(" --include="*.js" --include="*.ts" -A5

# Check for certificate pinning
grep -rniE "(pinning|certificate|ssl)" --include="*.js" --include="*.ts"
```

**Vulnerable patterns:**
```javascript
// INSECURE - No HTTPS
fetch('http://api.example.com/data');

// INSECURE - Disabled cert verification
const agent = new https.Agent({ rejectUnauthorized: false });

// INSECURE - No timeout
fetch(url); // Can hang indefinitely
```

**Secure patterns:**
```javascript
// SECURE - HTTPS with certificate pinning
import { fetch } from 'react-native-ssl-pinning';
fetch(url, {
  sslPinning: {
    certs: ['cert1', 'cert2']
  },
  timeoutInterval: 10000
});
```

### 4. Authentication & Session (HIGH)

**Check for:**
```bash
# Find auth-related code
grep -rniE "(login|logout|authenticate|authorize|session|jwt|oauth)" --include="*.js" --include="*.ts" -l

# Check token handling
grep -rniE "(access.?token|refresh.?token|bearer|authorization)" --include="*.js" --include="*.ts" -A3 -B3

# Find biometric auth
grep -rniE "(biometric|fingerprint|faceid|touchid)" --include="*.js" --include="*.ts"
```

**Vulnerable patterns:**
```javascript
// INSECURE - Token in URL
fetch(`https://api.com/data?token=${token}`);

// INSECURE - No token refresh
const token = await getToken(); // Never refreshes

// INSECURE - Logging tokens
console.log('Auth token:', token);

// INSECURE - Token in error messages
throw new Error(`Auth failed for token: ${token}`);
```

### 5. Input Validation & Injection (MEDIUM)

**Check for:**
```bash
# Find dynamic queries
grep -rniE "(query|sql|execute).*\$\{" --include="*.js" --include="*.ts"

# Find WebView usage
grep -rniE "WebView|injectJavaScript|postMessage" --include="*.js" --include="*.tsx"

# Find deep linking
grep -rniE "(Linking|DeepLink|universal.?link)" --include="*.js" --include="*.ts"
```

**Vulnerable patterns:**
```javascript
// INSECURE - SQL injection via string concatenation
db.execute(`SELECT * FROM users WHERE id = ${userId}`);

// INSECURE - WebView JavaScript injection
webViewRef.current.injectJavaScript(`
  document.getElementById('data').innerHTML = '${userInput}';
`);

// INSECURE - Deep link without validation
Linking.addEventListener('url', ({ url }) => {
  const route = url.split('/')[1];
  navigation.navigate(route); // No validation!
});
```

### 6. Logging & Debugging (MEDIUM)

**Check for:**
```bash
# Find all console statements
grep -rniE "console\.(log|debug|info|warn|error|trace)" --include="*.js" --include="*.ts" --include="*.tsx"

# Find debug flags
grep -rniE "(__DEV__|debug|DEBUG|devMode)" --include="*.js" --include="*.ts"

# Check for React Native Debugger/Flipper
grep -rniE "(flipper|reactotron|debug)" package.json

# Find error boundaries logging
grep -rniE "componentDidCatch|ErrorBoundary" --include="*.js" --include="*.tsx" -A10
```

**Vulnerable patterns:**
```javascript
// INSECURE - Logging sensitive data
console.log('User data:', userData);
console.log('Request:', { headers: { Authorization: token }});

// INSECURE - Debug code in production
if (__DEV__) {
  // This still ships in JS bundle!
}
```

### 7. Third-Party Dependencies (MEDIUM)

**Check for:**
```bash
# Audit npm packages
npm audit
npm audit --json > npm-audit.json

# Check for outdated packages
npm outdated

# Find known vulnerable packages
npx check-my-deps

# List all dependencies
cat package.json | jq '.dependencies, .devDependencies'
```

**High-risk packages to review:**
- Any package with native code
- Packages accessing: camera, location, contacts, storage
- Packages with network permissions
- Packages not updated in >1 year

### 8. Native Code Security (HIGH)

**iOS - Check Info.plist:**
```bash
# Find Info.plist
find . -name "Info.plist" -exec echo "=== {} ===" \; -exec cat {} \;

# Check for insecure settings
grep -E "(NSAllowsArbitraryLoads|NSExceptionDomains|NSAppTransportSecurity)" ios/*/Info.plist
```

**Android - Check AndroidManifest.xml:**
```bash
# Find manifests
find . -name "AndroidManifest.xml" -exec echo "=== {} ===" \; -exec cat {} \;

# Check permissions
grep -E "(permission|uses-permission)" android/app/src/main/AndroidManifest.xml

# Check for backup enabled (data extraction risk)
grep -E "android:allowBackup" android/app/src/main/AndroidManifest.xml

# Check for debuggable
grep -E "android:debuggable" android/app/src/main/AndroidManifest.xml

# Check exported components
grep -E "android:exported" android/app/src/main/AndroidManifest.xml
```

**Dangerous Android permissions:**
```xml
<!-- Review if truly needed -->
READ_CONTACTS, WRITE_CONTACTS
READ_CALL_LOG, WRITE_CALL_LOG
READ_SMS, SEND_SMS
ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
CAMERA, RECORD_AUDIO
READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
```

## Automated Scanning

### Run All Checks Script

```bash
#!/bin/bash
# rn-security-scan.sh

OUTPUT_DIR="./security-audit-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "=== React Native Security Scan ===" | tee "$OUTPUT_DIR/report.txt"

echo -e "\n[1/8] Scanning for hardcoded secrets..." | tee -a "$OUTPUT_DIR/report.txt"
grep -rniE "(api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token|private[_-]?key|secret[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9]" \
  --include="*.js" --include="*.ts" --include="*.tsx" --include="*.json" . 2>/dev/null | \
  grep -v node_modules | grep -v ".lock" > "$OUTPUT_DIR/secrets.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/secrets.txt") potential secrets"

echo -e "\n[2/8] Scanning for AWS credentials..." | tee -a "$OUTPUT_DIR/report.txt"
grep -rniE "(AKIA|ASIA)[A-Z0-9]{16}" --include="*.js" --include="*.ts" --include="*.json" . 2>/dev/null | \
  grep -v node_modules > "$OUTPUT_DIR/aws-keys.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/aws-keys.txt") potential AWS keys"

echo -e "\n[3/8] Scanning for insecure HTTP..." | tee -a "$OUTPUT_DIR/report.txt"
grep -rniE "http://(?!localhost|127\.0\.0\.1|10\.|192\.168\.)" \
  --include="*.js" --include="*.ts" --include="*.json" . 2>/dev/null | \
  grep -v node_modules > "$OUTPUT_DIR/insecure-http.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/insecure-http.txt") insecure HTTP URLs"

echo -e "\n[4/8] Scanning for AsyncStorage with sensitive data..." | tee -a "$OUTPUT_DIR/report.txt"
grep -rniE "AsyncStorage" --include="*.js" --include="*.ts" . 2>/dev/null | \
  grep -iE "(token|password|secret|key|auth|credential)" | \
  grep -v node_modules > "$OUTPUT_DIR/async-storage.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/async-storage.txt") AsyncStorage concerns"

echo -e "\n[5/8] Scanning for console.log with sensitive data..." | tee -a "$OUTPUT_DIR/report.txt"
grep -rniE "console\.(log|debug|info)\s*\([^)]*?(password|token|secret|key|credential|auth)" \
  --include="*.js" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
  grep -v node_modules > "$OUTPUT_DIR/console-leaks.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/console-leaks.txt") console logging concerns"

echo -e "\n[6/8] Scanning for eval() usage..." | tee -a "$OUTPUT_DIR/report.txt"
grep -rniE "\beval\s*\(" --include="*.js" --include="*.ts" . 2>/dev/null | \
  grep -v node_modules > "$OUTPUT_DIR/eval-usage.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/eval-usage.txt") eval() usages"

echo -e "\n[7/8] Running npm audit..." | tee -a "$OUTPUT_DIR/report.txt"
npm audit --json 2>/dev/null > "$OUTPUT_DIR/npm-audit.json"
echo "NPM audit complete"

echo -e "\n[8/8] Checking native configs..." | tee -a "$OUTPUT_DIR/report.txt"
grep -E "NSAllowsArbitraryLoads|android:allowBackup.*true|android:debuggable.*true" \
  ios/*/Info.plist android/app/src/main/AndroidManifest.xml 2>/dev/null > "$OUTPUT_DIR/native-config.txt"
echo "Found $(wc -l < "$OUTPUT_DIR/native-config.txt") native config concerns"

echo -e "\n=== Scan Complete ===" | tee -a "$OUTPUT_DIR/report.txt"
echo "Results saved to $OUTPUT_DIR"
```

### Using External Tools

```bash
# MobSF (Mobile Security Framework)
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf

# Semgrep for React Native
semgrep --config=p/react-native .

# GitLeaks for secret scanning
gitleaks detect --source=. --report-path=gitleaks-report.json

# Trivy for dependency scanning
trivy fs --security-checks vuln,secret .
```

## Security Checklist

### Pre-Release Audit

| Category | Check | Severity |
|----------|-------|----------|
| **Secrets** | No hardcoded API keys | CRITICAL |
| **Secrets** | No credentials in code | CRITICAL |
| **Secrets** | .env files in .gitignore | CRITICAL |
| **Storage** | Tokens in Keychain/Keystore | HIGH |
| **Storage** | No PII in AsyncStorage | HIGH |
| **Network** | All endpoints HTTPS | HIGH |
| **Network** | Certificate pinning enabled | MEDIUM |
| **Auth** | Tokens not logged | HIGH |
| **Auth** | Secure token refresh flow | HIGH |
| **Auth** | Biometrics properly implemented | MEDIUM |
| **Logging** | No sensitive data in logs | HIGH |
| **Logging** | Console.log stripped in prod | MEDIUM |
| **Native** | allowBackup=false (Android) | HIGH |
| **Native** | debuggable=false (Android) | HIGH |
| **Native** | ATS enabled (iOS) | MEDIUM |
| **Deps** | No critical npm vulnerabilities | HIGH |
| **Deps** | Dependencies up to date | MEDIUM |
| **Code** | No eval() usage | MEDIUM |
| **Code** | Input validation on deep links | MEDIUM |
| **Code** | WebView injection prevented | MEDIUM |

## OWASP MASVS Mapping

| MASVS Category | This Skill Covers |
|----------------|-------------------|
| V1: Architecture | Deep link validation, component security |
| V2: Data Storage | AsyncStorage, Keychain, encrypted storage |
| V3: Cryptography | Secure random, key storage |
| V4: Authentication | Token handling, biometrics, session |
| V5: Network | HTTPS, cert pinning, SSL verification |
| V6: Platform | Native permissions, manifest security |
| V7: Code Quality | Logging, debugging, input validation |
| V8: Resilience | Obfuscation checks, anti-tampering |

## Severity Reference

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Immediate exploitation risk, data breach | Fix before any release |
| **HIGH** | Significant security risk | Fix before production |
| **MEDIUM** | Defense-in-depth issue | Fix in next sprint |
| **LOW** | Minor issue, best practice | Track in backlog |
