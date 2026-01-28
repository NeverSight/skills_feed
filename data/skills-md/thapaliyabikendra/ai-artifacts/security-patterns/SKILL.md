---
name: security-patterns
description: "Web application security patterns including STRIDE threat modeling, OWASP Top 10 compliance, ABP authorization, and security audit procedures. Use when: (1) conducting security audits, (2) implementing authentication/authorization, (3) creating threat models, (4) reviewing code for vulnerabilities."
layer: 3
tech_stack: [dotnet, csharp, typescript, react]
topics: [stride, owasp, threat-modeling, security-audit, xss, sql-injection, csrf]
depends_on: [openiddict-authorization]
complements: [abp-framework-patterns]
keywords: [STRIDE, OWASP, XSS, CSRF, SQLInjection, ThreatModel, SecurityAudit]
---

# Security Patterns for Web Applications

Security patterns and practices for building secure ABP Framework applications.

## When to Use

- Conducting security audits
- Implementing authentication/authorization
- Creating threat models (STRIDE)
- Reviewing code for OWASP Top 10 vulnerabilities
- Designing permission systems
- Validating input and sanitizing output

## STRIDE Threat Model

### Framework

| Category | Threat | Question | Mitigation |
|----------|--------|----------|------------|
| **S**poofing | Identity theft | Can attacker impersonate user? | Authentication, tokens |
| **T**ampering | Data modification | Can attacker modify data? | Integrity checks, signing |
| **R**epudiation | Denial of actions | Can user deny their actions? | Audit logging |
| **I**nformation Disclosure | Data exposure | Can attacker access sensitive data? | Encryption, access control |
| **D**enial of Service | Availability attack | Can attacker disrupt service? | Rate limiting, scaling |
| **E**levation of Privilege | Unauthorized access | Can attacker gain higher privileges? | Authorization, least privilege |

### Threat Model Template

```markdown
## Threat Model: [Feature Name]

**Date**: YYYY-MM-DD
**Reviewer**: [Name]

### Assets
| Asset | Sensitivity | Description |
|-------|-------------|-------------|
| Patient Data | HIGH | PII including medical records |
| User Credentials | CRITICAL | Passwords, tokens |
| Appointment Data | MEDIUM | Scheduling information |

### Threat Analysis
| ID | Category | Threat | Likelihood | Impact | Risk | Mitigation |
|----|----------|--------|------------|--------|------|------------|
| T1 | Spoofing | Attacker impersonates patient | Medium | High | HIGH | OAuth 2.0, MFA |
| T2 | Tampering | Attacker modifies appointment | Low | Medium | LOW | Authorization checks |
| T3 | Info Disclosure | Unauthorized patient data access | Medium | Critical | CRITICAL | Row-level security |
| T4 | Elevation | Receptionist gains admin access | Low | Critical | HIGH | Permission validation |

### Mitigations
| ID | Threat | Control | Status |
|----|--------|---------|--------|
| M1 | T1 | Implement OAuth 2.0 with OpenIddict | Implemented |
| M2 | T3 | Add row-level authorization in AppService | Pending |
```

## OWASP Top 10 Checklist

### 1. Injection (A01)

```csharp
// BAD: SQL Injection
var query = $"SELECT * FROM Users WHERE Email = '{email}'";

// GOOD: Parameterized query (EF Core does this automatically)
var user = await _dbContext.Users
    .FirstOrDefaultAsync(u => u.Email == email);

// BAD: Command injection
Process.Start("cmd", $"/c dir {userInput}");

// GOOD: Validate and sanitize input
if (!IsValidPath(userInput))
    throw new BusinessException("Invalid path");
```

### 2. Broken Authentication (A02)

```csharp
// Checklist:
// [ ] Use OAuth 2.0 / OpenIddict
// [ ] Implement token expiry (short-lived access, long-lived refresh)
// [ ] Hash passwords with modern algorithm (BCrypt, Argon2)
// [ ] Implement account lockout after failed attempts
// [ ] Use secure session management
// [ ] Implement MFA for sensitive operations
```

### 3. Sensitive Data Exposure (A03)

```csharp
// BAD: Logging PII
_logger.LogInformation("User {Email} logged in", user.Email);

// GOOD: Log identifiers only
_logger.LogInformation("User {UserId} logged in", user.Id);

// BAD: Returning sensitive data
return new UserDto { PasswordHash = user.PasswordHash };

// GOOD: Exclude sensitive fields
return new UserDto { Id = user.Id, Name = user.Name };
```

### 4. Security Misconfiguration (A05)

```csharp
// Checklist:
// [ ] Disable debug mode in production
// [ ] Remove default credentials
// [ ] Configure CORS properly
// [ ] Set secure headers (CSP, X-Frame-Options)
// [ ] Disable directory listing
// [ ] Keep frameworks updated
```

### 5. Broken Access Control (A01)

```csharp
// BAD: No authorization
public async Task<PatientDto> GetPatientAsync(Guid id)
{
    return await _repository.GetAsync(id);
}

// GOOD: Authorization enforced
[Authorize(ClinicPermissions.Patients.Default)]
public async Task<PatientDto> GetPatientAsync(Guid id)
{
    var patient = await _repository.GetAsync(id);

    // Additional check: Can user access this specific patient?
    await AuthorizationService.CheckAsync(patient, CommonOperations.Get);

    return ObjectMapper.Map<Patient, PatientDto>(patient);
}
```

## ABP Authorization Patterns

### Permission Definition

```csharp
public static class {ProjectName}Permissions
{
    public const string GroupName = "{ProjectName}";

    public static class {Feature}
    {
        public const string Default = GroupName + ".{Feature}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string ViewAll = Default + ".ViewAll";
    }
}
```

### AppService Authorization

```csharp
[Authorize({ProjectName}Permissions.{Feature}.Default)]
public class {Entity}AppService : ApplicationService
{
    [Authorize({ProjectName}Permissions.{Feature}.Create)]
    public async Task<{Entity}Dto> CreateAsync(CreateUpdate{Entity}Dto input)
    {
        // Create logic
    }

    [Authorize({ProjectName}Permissions.{Feature}.Edit)]
    public async Task<{Entity}Dto> UpdateAsync(Guid id, CreateUpdate{Entity}Dto input)
    {
        // Update logic
    }

    [Authorize({ProjectName}Permissions.{Feature}.Delete)]
    public async Task DeleteAsync(Guid id)
    {
        // Delete logic
    }
}
```

### Resource-Based Authorization

```csharp
public async Task<PatientDto> GetAsync(Guid id)
{
    var patient = await _repository.GetAsync(id);

    // Check if current user can access this specific patient
    if (patient.AssignedDoctorId != CurrentUser.Id)
    {
        await AuthorizationService.CheckAsync(
            {ProjectName}Permissions.{Feature}.ViewAll);
    }

    return ObjectMapper.Map<Patient, PatientDto>(patient);
}
```

## Security Audit Report Template

```markdown
## Security Audit Report

**Application**: [Name]
**Date**: YYYY-MM-DD
**Auditor**: [Name]
**Risk Level**: Critical | High | Medium | Low

### Executive Summary
[1-2 paragraph overview of findings]

### Findings

#### [VULN-001] [Title]
- **Severity**: Critical | High | Medium | Low
- **Category**: OWASP A01-A10 / STRIDE
- **Location**: `path/to/file.cs:line`
- **Description**: [What the vulnerability is]
- **Impact**: [What could happen if exploited]
- **Reproduction Steps**:
  1. [Step 1]
  2. [Step 2]
- **Recommendation**: [How to fix]
- **Code Example**:
```csharp
// Vulnerable code
[code here]

// Fixed code
[code here]
```

### Summary
| Severity | Count | Fixed | Pending |
|----------|-------|-------|---------|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 |
| Low | 0 | 0 | 0 |

### Recommendations
1. [Priority recommendation]
2. [Secondary recommendation]
```

## Security Checklist

### Authentication
- [ ] OAuth 2.0 / OpenID Connect implemented
- [ ] Token expiry configured (access: 15-60 min, refresh: 7-30 days)
- [ ] Password policy enforced (min length, complexity)
- [ ] Account lockout after failed attempts
- [ ] MFA available for sensitive operations
- [ ] Secure password reset flow

### Authorization
- [ ] All endpoints have `[Authorize]` attribute
- [ ] Permissions defined for all operations
- [ ] Role-based access enforced
- [ ] Resource-based authorization where needed
- [ ] No permission bypass vulnerabilities
- [ ] Least privilege principle applied

### Input Validation
- [ ] All DTOs have FluentValidation
- [ ] SQL uses parameterized queries (EF Core)
- [ ] File uploads restricted by type and size
- [ ] API rate limiting configured
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection enabled

### Data Protection
- [ ] PII not logged
- [ ] Sensitive data encrypted at rest
- [ ] TLS enforced (HTTPS only)
- [ ] Secure headers configured
- [ ] Error messages don't expose internals
- [ ] Connection strings secured

### Audit & Monitoring
- [ ] Security events logged
- [ ] Failed auth attempts tracked
- [ ] Admin actions audited
- [ ] Anomaly detection configured
- [ ] Log integrity protected

## Authorization Anti-Patterns (Quick Scan)

Use this table for rapid code review scanning:

| Pattern | Risk Level | Fix |
|---------|------------|-----|
| No `[Authorize]` on public method | 🔴 CRITICAL | Add `[Authorize(Permission)]` |
| `[Authorize]` only at class level | 🟡 MEDIUM | Add method-level permissions for mutations |
| No permission check for bulk operations | 🔴 HIGH | Check permission per operation or batch |
| Missing `[RequiresTenant]` on tenant-specific ops | 🔴 HIGH | Add `[RequiresTenant]` attribute |
| `_dataFilter.Disable<IMultiTenant>()` without comment | 🔴 CRITICAL | Add justification comment or remove |
| Hardcoded secrets in code | 🔴 CRITICAL | Use configuration/secrets management |
| PII in log messages | 🟡 MEDIUM | Log identifiers only, not PII |

## Multi-Tenancy Security

### Dangerous Pattern: Disabling Tenant Filter

```csharp
// ⚠️ DANGEROUS: Cross-tenant data exposure risk!
using (_dataFilter.Disable<IMultiTenant>())
{
    // This query now sees ALL tenants' data!
    var exists = await _repository.AnyAsync(x => x.Code == code);
}
```

**Risks:**
- Cross-tenant data leakage
- Incorrect validation results (e.g., "code already exists" when it exists in another tenant)
- Security audit failures

### When Disabling is Justified (Rare)

Only disable multi-tenancy with explicit justification comment:

```csharp
// ✅ JUSTIFIED: License plate numbers must be globally unique across all tenants
// to ensure physical warehouse operations don't conflict between tenants sharing facilities.
// Approved by: [Name] on [Date]
using (_dataFilter.Disable<IMultiTenant>())
{
    var existsGlobally = await _licensePlateRepository.AnyAsync(
        lp => lp.LicensePlateNumber == input.LicensePlateNumber && !lp.ShippedOut);
}
```

### Multi-Tenancy Security Checklist

- [ ] No `_dataFilter.Disable<IMultiTenant>()` without documented justification
- [ ] Cross-tenant uniqueness checks are truly required (not accidental)
- [ ] Error messages don't reveal other tenants' data
- [ ] Audit logging captures cross-tenant operations
- [ ] Unit tests verify tenant isolation

## Common Vulnerability Patterns

### Missing Authorization

```csharp
// VULNERABLE
public async Task<PatientDto> GetAsync(Guid id)
{
    return await _repository.GetAsync(id);
}

// SECURE
[Authorize({ProjectName}Permissions.Patients.Default)]
public async Task<PatientDto> GetAsync(Guid id)
{
    return await _repository.GetAsync(id);
}
```

### Information Disclosure in Errors

```csharp
// VULNERABLE
catch (Exception ex)
{
    return BadRequest(ex.ToString()); // Exposes stack trace
}

// SECURE
catch (Exception ex)
{
    _logger.LogError(ex, "Error processing request");
    throw new UserFriendlyException("An error occurred");
}
```

### Insecure Direct Object Reference

```csharp
// VULNERABLE: Any user can access any patient
[HttpGet("{id}")]
public async Task<PatientDto> Get(Guid id)
{
    return await _service.GetAsync(id);
}

// SECURE: Verify user can access this patient
[HttpGet("{id}")]
public async Task<PatientDto> Get(Guid id)
{
    var patient = await _service.GetAsync(id);
    if (!await CanAccessPatient(patient))
        throw new UnauthorizedAccessException();
    return patient;
}
```

## References

- [references/owasp-top-10-details.md](references/owasp-top-10-details.md) - Detailed OWASP guide
- [references/abp-security-config.md](references/abp-security-config.md) - ABP security configuration
