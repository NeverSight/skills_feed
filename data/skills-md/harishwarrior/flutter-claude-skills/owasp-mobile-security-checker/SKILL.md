---
name: owasp-mobile-security-checker
description: Analyze Flutter and mobile applications for OWASP Mobile Top 10 (2024) security compliance. Use this skill when performing security audits, vulnerability assessments, or compliance checks on mobile applications. Performs automated scans for hardcoded secrets, insecure storage, weak cryptography, network security issues, and provides detailed remediation guidance.
---

# OWASP Mobile Security Checker

Comprehensive security analysis tool for Flutter and mobile applications based on the OWASP Mobile Top 10 (2024) guidelines.

## Overview

This skill enables thorough security auditing of Flutter mobile applications by identifying vulnerabilities across all ten OWASP Mobile Top 10 risk categories. It combines automated scanning scripts with manual analysis guidelines to provide comprehensive security assessments and actionable remediation plans.

## Core Capabilities

### 1. Automated Vulnerability Scanning

Run Python-based scanners to detect common security issues:

## M1 - Hardcoded Secrets Scanner**

```bash
python3 scripts/scan_hardcoded_secrets.py /path/to/project
```

Detects API keys, tokens, passwords, AWS credentials, Firebase keys, and other hardcoded secrets in Dart code and configuration files.

## M2 - Dependency Security Checker**

```bash
python3 scripts/check_dependencies.py /path/to/project
```

Analyzes `pubspec.yaml` for outdated packages, insecure version constraints (`any`), and known vulnerabilities.

## M5 - Network Security Validator**

```bash
python3 scripts/check_network_security.py /path/to/project
```

Checks for HTTP vs HTTPS usage, certificate pinning, Android Network Security Config, and iOS App Transport Security settings.

## M9 - Storage Security Analyzer**

```bash
python3 scripts/analyze_storage_security.py /path/to/project
```

Identifies unencrypted SharedPreferences usage, plaintext file storage, unencrypted databases, and insecure backup configurations.

### 2. Manual Security Analysis

For risks requiring code review and architectural assessment:

- **M3 (Authentication/Authorization)**: Evaluate token management, MFA, biometrics, and session handling
- **M4 (Input/Output Validation)**: Check input sanitization, parameterized queries, and injection prevention
- **M6 (Privacy Controls)**: Review permissions, PII handling, consent mechanisms, and data minimization
- **M7 (Binary Protections)**: Verify obfuscation, root detection, and anti-debugging measures
- **M8 (Security Misconfiguration)**: Inspect debug flags, logging, and platform configurations
- **M10 (Cryptography)**: Validate algorithm choices, key management, and encryption modes

### 3. Comprehensive Security Reports

Generate detailed reports with:

- Severity-based prioritization (CRITICAL → HIGH → MEDIUM → LOW)
- Flutter-specific code examples (insecure vs secure patterns)
- Actionable remediation steps with implementation guidance
- OWASP Mobile Top 10 risk categorization

## Workflow Decision Tree

**Start here to determine your approach:**

```text
Is this a comprehensive security audit?
├─ YES → Run all 4 automated scanners → Review results → Perform manual analysis → Generate report
└─ NO → Continue...

Is this for a specific OWASP risk category?
├─ M1 (Credentials) → Run scan_hardcoded_secrets.py → Review findings
├─ M2 (Dependencies) → Run check_dependencies.py → Update packages
├─ M5 (Network) → Run check_network_security.py → Implement certificate pinning
├─ M9 (Storage) → Run analyze_storage_security.py → Use encrypted storage
└─ Other (M3/M4/M6/M7/M8/M10) → Load reference docs → Perform manual analysis

Is this a quick security check before release?
└─ YES → Run all automated scanners → Focus on CRITICAL/HIGH findings → Fix blockers
```

## Quick Start: Comprehensive Audit

Perform a complete OWASP security audit:

1. **Run automated scans** (from project root):

   ```bash
   python3 .claude/skills/owasp-mobile-security-checker/scripts/scan_hardcoded_secrets.py .
   python3 .claude/skills/owasp-mobile-security-checker/scripts/check_dependencies.py .
   python3 .claude/skills/owasp-mobile-security-checker/scripts/analyze_storage_security.py .
   python3 .claude/skills/owasp-mobile-security-checker/scripts/check_network_security.py .
   ```

2. **Review JSON outputs**:
   - `owasp_m1_secrets_scan.json`
   - `owasp_m2_dependencies_scan.json`
   - `owasp_m5_network_scan.json`
   - `owasp_m9_storage_scan.json`

3. **Prioritize by severity**: Address CRITICAL and HIGH findings first

4. **Load reference documentation** for detailed information:

   ```text
   Read references/owasp_mobile_top_10_2024.md
   ```

5. **Perform manual analysis** for remaining risks (M3, M4, M6, M7, M8, M10)

6. **Generate remediation plan** with code examples and timeline

## Manual Analysis Guidelines

### M3: Authentication & Authorization

**What to check:**

- Token storage using `flutter_secure_storage` (not SharedPreferences)
- Token expiration and refresh mechanisms
- Multi-factor authentication implementation
- Server-side authorization enforcement

**Code patterns to find:**

```dart
// Search for: SharedPreferences + setString with 'token', 'auth', 'password'
// Flag: Plaintext credential storage

// Verify: FlutterSecureStorage usage for sensitive data
// Check: Token expiration logic exists
```

### M4: Input/Output Validation

**What to check:**

- Input validation on all user inputs (forms, URLs, file paths)
- Parameterized database queries (no string interpolation)
- Output encoding in WebViews
- API response validation

**Code patterns to find:**

```dart
// Search for: rawQuery, rawInsert with string interpolation ($)
// Flag: SQL injection vulnerability

// Search for: WebView without proper sanitization
// Flag: XSS vulnerability
```

### M6: Privacy Controls

**What to check:**

- Minimal permission requests (only necessary)
- No PII in analytics events or logs
- Consent mechanisms for data collection
- Proper anonymization/pseudonymization

**Code patterns to find:**

```dart
// Search for: FirebaseAnalytics.logEvent with email, phone, name
// Flag: PII in analytics

// Search for: print(), log() with user data
// Flag: PII in logs
```

### M7: Binary Protections

**What to verify:**

```bash
# Check build commands use obfuscation:
flutter build apk --release --obfuscate --split-debug-info=./debug-info

# Search for root detection packages:
grep -r "flutter_jailbreak_detection" pubspec.yaml
grep -r "root_detector" pubspec.yaml

# Verify debug mode checks:
grep -r "kDebugMode" lib/
```

### M8: Security Misconfiguration

**What to check:**

- Debug flags disabled in production
- Logging levels appropriate for release
- Minimal platform permissions in manifests
- No development endpoints in production code

**Code patterns to find:**

```dart
// Flag: Debug code that executes in release builds
if (kDebugMode) { print("..."); } // This compiles in release!

// Preferred: assert(() { debugPrint("..."); return true; }());
```

### M10: Cryptography

**What to check:**

- Strong algorithms (AES-256 GCM, not MD5/SHA1)
- Secure key storage (Keystore/Keychain, not hardcoded)
- Proper encryption modes (GCM, not ECB)
- Cryptographically secure RNG (Random.secure())

**Code patterns to find:**

```dart
// Search for: md5, sha1, des (weak algorithms)
// Search for: AESMode.ecb (insecure mode)
// Search for: 'encryption_key', 'secret_key' (hardcoded keys)
```

## Understanding Scan Results

### Severity Levels

- **CRITICAL**: Immediate security risk requiring urgent action
  - Examples: Disabled certificate validation, exposed production credentials
  - Action: Fix immediately, do not release

- **HIGH**: Significant vulnerability requiring prompt remediation
  - Examples: Hardcoded API keys, unencrypted sensitive storage
  - Action: Fix before release

- **MEDIUM**: Security concern that should be addressed
  - Examples: Missing certificate pinning, outdated dependencies
  - Action: Plan remediation, fix in next sprint

- **LOW**: Best practice or minor improvement
  - Examples: Verbose logging, local networking allowed
  - Action: Address as time permits

### Common False Positives

Be aware of legitimate cases that may trigger findings:

- **M1**: Test/example API keys, environment placeholders (`YOUR_API_KEY`)
- **M5**: HTTP for localhost/127.0.0.1 during development
- **M9**: Non-sensitive data in SharedPreferences (user preferences)
- **M2**: Development dependencies (linters, test tools)

Always verify findings in context before flagging as vulnerabilities.

## Reference Documentation

The `references/owasp_mobile_top_10_2024.md` file provides:

- Detailed explanations of each OWASP Mobile Top 10 risk
- Real-world attack scenarios and examples
- Flutter-specific vulnerability patterns
- Complete mitigation strategies
- Secure vs insecure code examples
- Platform-specific considerations (Android/iOS)

**When to load this reference:**

- Need deep understanding of a specific risk category
- Creating detailed remediation documentation
- Explaining vulnerabilities to stakeholders
- Looking for Flutter-specific code patterns
- Researching platform-specific security configurations

## Example: Targeted Security Fix

**Scenario**: Found HIGH severity finding for hardcoded API key

1. **Locate the issue**:

   ```text
   File: lib/services/api_client.dart:15
   Issue: Hardcoded API key
   Code: const String apiKey = "sk_live_ABC123...";
   ```

2. **Understand the risk**: Load `references/owasp_mobile_top_10_2024.md` and review M1 section

3. **Implement fix**:

   ```dart
   // Before (INSECURE):
   const String apiKey = "sk_live_ABC123...";

   // After (SECURE):
   final secureStorage = FlutterSecureStorage();
   String? apiKey = await secureStorage.read(key: 'api_key');
   // Key injected at build time or fetched from secure backend
   ```

4. **Verify fix**: Re-run `scan_hardcoded_secrets.py` to confirm issue resolved

5. **Document**: Update security review with remediation details

## Best Practices

**For Development Teams:**

- Run automated scans in CI/CD pipeline on every PR
- Establish security gates (no CRITICAL findings in production)
- Conduct quarterly comprehensive security audits
- Maintain security backlog and track remediation

**For Security Auditors:**

- Combine automated scans with manual code review
- Test fixes to ensure they don't break functionality
- Document security exceptions with business justification
- Provide training on secure coding practices

**For All Users:**

- Keep scan scripts updated with latest patterns
- Share findings and recommendations with team
- Integrate security early in development cycle
- Treat OWASP compliance as ongoing, not one-time

## Integration Points

Recommended workflow integration:

- **Pre-commit**: Lightweight secret scanning
- **Pull Requests**: Automated scans with security report comment
- **Release Builds**: Comprehensive audit including manual analysis
- **Production**: Continuous monitoring and periodic reviews
- **Incident Response**: Targeted scans when vulnerabilities reported

## Additional Resources

This skill references authoritative sources:

- OWASP Mobile Top 10 Project (2024)
- Flutter Security Best Practices
- Android Security Guidelines (Keystore, Network Security Config)
- iOS Security Guide (Keychain, App Transport Security)
- Platform-specific documentation and security research
