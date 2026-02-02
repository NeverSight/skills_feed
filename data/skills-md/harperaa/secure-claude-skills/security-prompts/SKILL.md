---
name: security-prompts
description: Library of battle-tested security prompt templates for secure feature implementation. Use when implementing forms, endpoints, authentication, authorization, file uploads, or conducting security reviews. Triggers include "security prompt", "secure form", "RBAC", "threat model", "STRIDE", "admin endpoint", "file upload", "security testing", "code review", "OWASP".
---

# Security Prompt Templates Library

## Purpose

This skill provides ready-to-use security prompt templates following the Secure Vibe Coding methodology. Each template includes complete security controls, testing checklists, and customization guidance.

## When to Use This Skill

Use security prompt templates when:
- **Building features**: Forms, APIs, file uploads, admin panels
- **Implementing auth**: RBAC, permissions, ownership checks
- **Security reviews**: Threat modeling, code review, OWASP compliance
- **Testing**: Security test generation, vulnerability assessment

## Library Organization

### 📁 Prompt Engineering Templates (8 templates)
**Location**: `.claude/skills/security/security-prompts/prompt-engineering/`

Comprehensive prompts for implementing secure features:

1. **01_secure_form.md** - Public forms with full security stack
   - Triggers: "secure form", "contact form", "public form"
   - Controls: CSRF, rate limiting, XSS prevention, validation

2. **02_authenticated_endpoint.md** - Authenticated data modification
   - Triggers: "authenticated endpoint", "user update", "protected route"
   - Controls: Authentication, authorization, ownership checks

3. **03_public_endpoint.md** - Public APIs with pagination
   - Triggers: "public API", "public endpoint", "GET endpoint"
   - Controls: Rate limiting, validation, pagination

4. **04_admin_action.md** - Admin-only features with audit logging
   - Triggers: "admin endpoint", "admin feature", "admin action"
   - Controls: RBAC, audit logging, authorization

5. **05_file_upload.md** - Secure file handling
   - Triggers: "file upload", "image upload", "file handling"
   - Controls: Type validation, size limits, malware scanning

6. **06_composable_middleware.md** - Multiple security layers
   - Triggers: "middleware", "security layers", "composable security"
   - Controls: Proper middleware ordering, layer composition

7. **07_new_control.md** - Extending security architecture
   - Triggers: "new security control", "custom middleware", "security utility"
   - Controls: Creating new reusable security utilities

8. **08_security_testing.md** - Comprehensive security tests
   - Triggers: "security testing", "security tests", "test security"
   - Controls: Automated test generation for all controls

### 📁 Threat Modeling Templates (8 templates)
**Location**: `.claude/skills/security/security-prompts/threat-modeling/`

Prompts for security analysis and review:

1. **01_stride_analysis.md** - Complete STRIDE threat model
   - Triggers: "STRIDE", "threat model", "security analysis"

2. **02_feature_threats.md** - Feature-specific threat analysis
   - Triggers: "feature threats", "analyze feature security"

3. **03_architecture_impact.md** - Architecture change security impact
   - Triggers: "architecture security", "security impact"

4. **04_code_review.md** - Security vulnerability review
   - Triggers: "security review", "code review", "vulnerability review"

5. **05_security_tests.md** - Automated security test generation
   - Triggers: "generate security tests", "security test suite"

6. **06_owasp_check.md** - OWASP Top 10 compliance
   - Triggers: "OWASP", "OWASP check", "OWASP compliance"

7. **07_payment_security.md** - Payment security (Clerk Billing + Stripe)
   - Triggers: "payment security", "Stripe security", "billing security"

8. **08_update_model.md** - Update threat model after features
   - Triggers: "update threat model", "refresh threat model"

### 📁 Auth & Authorization Templates (4 templates)
**Location**: `.claude/skills/security/security-prompts/auth-authorization/`

Prompts for authentication and access control:

1. **01_rbac_implementation.md** - Role-based access control
   - Triggers: "RBAC", "role-based access", "user roles"

2. **02_permissions.md** - Granular permission system
   - Triggers: "permissions", "permission system", "granular access"

3. **03_ownership.md** - Resource ownership verification
   - Triggers: "ownership", "ownership check", "resource ownership"

4. **04_auth_testing.md** - Authorization testing
   - Triggers: "auth testing", "authorization tests", "test permissions"

### 📁 Built-In Controls Templates (3 templates)
**Location**: `.claude/skills/security/security-prompts/built-in-controls/`

Simple prompts using existing Secure Vibe Coding OS utilities:

1. **01_contact_form.md** - Quick contact form with security
   - Triggers: "contact form", "simple form"

2. **02_authenticated_update.md** - User data modification
   - Triggers: "update profile", "user update"

3. **03_public_api.md** - Public GET endpoints
   - Triggers: "public API", "read-only API"

## How to Use Security Prompts

### Quick Usage Pattern

1. **Identify your need** (e.g., "I need a secure contact form")
2. **Find the template** (use triggers or browse categories)
3. **Read the template** to understand security controls
4. **Copy and customize** the prompt for your specific needs
5. **Run the prompt** with Claude Code
6. **Verify** using the testing checklist

### Template Access Pattern

When a user asks for a security implementation:

```markdown
**Recommend the appropriate template:**

"I'll use the [TEMPLATE_NAME] security prompt template for this.

**Template**: `.claude/skills/security/security-prompts/[category]/[file].md`

**Security Controls Applied**:
- [List controls from template]

**Customizations needed**:
- [List what to customize]

Let me load the template and customize it for your needs..."

Then read and apply the template.
```

## Combining Prompts

Many features need multiple prompts:

**Example: Admin Dashboard**
1. First: `auth-authorization/01_rbac_implementation.md` (if RBAC not set up)
2. Then: `prompt-engineering/04_admin_action.md` (for each admin feature)
3. Test: `prompt-engineering/08_security_testing.md`
4. Review: `threat-modeling/04_code_review.md`
5. Update: `threat-modeling/08_update_model.md`

**Example: User Profile Edit**
1. Implement: `prompt-engineering/02_authenticated_endpoint.md`
2. Add ownership: `auth-authorization/03_ownership.md`
3. Test: `auth-authorization/04_auth_testing.md`

## Prompt Template Format

Each template follows this structure:

```markdown
# [Template Name]

**Category**: [Category]
**When to Use**: [Scenario]
**Module**: [Course module]
**Time to Implement**: [Estimate]

## Security Controls Applied
[Checklist of security features]

## The Prompt
[Copy-paste ready prompt with placeholders]

## Customization Tips
[How to adapt for specific needs]

## Testing Checklist
[Verification steps]

## Related Prompts
[Links to complementary templates]

## Version History
[Change tracking]
```

## Integration with Security Architecture

All prompts reference the Secure Vibe Coding OS:

- **Architecture**: `@docs/security/SECURITY_ARCHITECTURE.md`
- **Utilities**: `/lib` directory (withCsrf, withRateLimit, validateRequest, etc.)
- **Baseline**: 90/100 OWASP score
- **Stack**: Next.js, Clerk, Convex, Stripe

Always include architecture reference in prompts:
```
Reference: @docs/security/SECURITY_ARCHITECTURE.md
```

## Agent Usage Pattern

When security-focused agents (like security-scanner, threat-modeler) need prompt templates:

```typescript
// Agent can reference specific templates
"Use the STRIDE analysis template from .claude/skills/security/security-prompts/threat-modeling/01_stride_analysis.md to create a threat model"

// Or request template by trigger
"Apply the secure form security prompt template to implement this contact form"
```

## Skill Chaining

This skill works with other security skills:

- **security-awareness/*** - Understanding vulnerabilities
- **csrf-protection** - CSRF implementation details
- **rate-limiting** - Rate limiting patterns
- **input-validation** - Validation strategies
- **auth-security** - Clerk authentication
- **security-testing** - Testing approaches

## Quick Reference by Scenario

### "I need to add..."

**"...a contact form"**
→ `built-in-controls/01_contact_form.md`

**"...user profile editing"**
→ `prompt-engineering/02_authenticated_endpoint.md`
→ Then: `auth-authorization/03_ownership.md`

**"...admin features"**
→ `auth-authorization/01_rbac_implementation.md` (if needed)
→ Then: `prompt-engineering/04_admin_action.md`

**"...file uploads"**
→ `prompt-engineering/05_file_upload.md`

**"...a public API"**
→ `built-in-controls/03_public_api.md`

### "I need to review..."

**"...security before deploy"**
→ `prompt-engineering/08_security_testing.md`
→ `threat-modeling/04_code_review.md`

**"...OWASP compliance"**
→ `threat-modeling/06_owasp_check.md`

**"...payment security"**
→ `threat-modeling/07_payment_security.md`

### "I need to create..."

**"...a threat model"**
→ `threat-modeling/01_stride_analysis.md`

**"...role-based access"**
→ `auth-authorization/01_rbac_implementation.md`

**"...security tests"**
→ `prompt-engineering/08_security_testing.md`

## Best Practices

### Always Customize
- Replace placeholders with your specific values
- Adjust rate limits for your use case
- Modify validation rules for your data

### Always Test
- Use the testing checklist in each template
- Run security tests before deploying
- Verify all controls work as expected

### Always Update Threat Model
- After every feature: `threat-modeling/08_update_model.md`
- Maintain `docs/security/THREAT_MODEL.md`
- Version your threat model (v1.0, v1.1, etc.)

### Chain Appropriately
- Authentication → Authorization → Ownership
- Implementation → Testing → Review
- Feature → Threat Analysis → Model Update

## Supporting Files

Each category has its own SKILL.md with:
- Detailed trigger keywords
- Category-specific guidance
- Template descriptions
- Usage patterns

**Access supporting templates directly**:
```
Read: .claude/skills/security/security-prompts/[category]/[template].md
```

## Example Agent Integration

```markdown
# Security Implementation Agent

When implementing security features:

1. **Identify feature type** (form, API, auth, etc.)
2. **Load appropriate security-prompts skill template**
3. **Customize template** with user's specific requirements
4. **Generate secure implementation** following template
5. **Apply testing checklist** from template
6. **Recommend related prompts** for complete security

Use security-prompts skill as the authoritative source for implementation patterns.
```

## Version History

**v1.0** (2025-10-23): Initial skill creation from security-prompts library
- Converted 23 prompts to skill templates
- Organized into 4 categories
- Added trigger keywords for automatic activation
- Integrated with Secure Vibe Coding OS architecture

## Related Skills

- `course-lesson-builder` - Creating course content using these prompts
- `security/*` - All implementation-focused security skills
- `security-awareness/*` - Understanding vulnerability patterns

## Notes for Maintenance

When adding new security prompts:
1. Add template file to appropriate category subdirectory
2. Update category SKILL.md with new template info
3. Update this main SKILL.md quick reference
4. Add relevant trigger keywords
5. Link related prompts
6. Version the template

---

**Usage**: When users mention security implementations, threat modeling, or specific triggers, activate this skill to provide appropriate template guidance and direct them to the right security prompt for their needs.
