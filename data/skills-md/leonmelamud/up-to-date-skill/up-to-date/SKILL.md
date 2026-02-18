---
name: up-to-date
description: "Fetches and validates current third-party API documentation, checks SDK version compatibility, and verifies correct method signatures and parameter shapes before writing or debugging integration code. Use when writing, editing, or refactoring code that calls any third-party SDK, API, or library method; debugging issues where an API call succeeds but the expected side-effect doesn't happen; installing or importing external packages; or when something 'doesn't work' and the code involves an external service."
license: MIT
---

# Up To Date

## Rule

**Before writing or debugging ANY code that touches an external package or API, fetch the real documentation first.** Training data is stale — the docs are the only source of truth for current API contracts, parameter shapes, and SDK method signatures.

Before proceeding, confirm none of these apply:
1. Writing or changing an API call without reading current docs
2. Guessing why an API call silently fails
3. Proposing a fix based on intuition without verifying the actual API contract

If any apply → complete the Mandatory Steps below before writing a single line of code.

## When This Triggers

This skill triggers on **any** of the following — load it BEFORE doing anything else:

### Direct triggers (writing code)
- Installing a package (`npm install`, `pip install`, `brew install`)
- Importing or using any third-party library
- Calling any external API (REST, GraphQL, SDK methods)
- Modifying or refactoring existing integration code
- Moving API calls between files (e.g., centralizing into a service module)

### Diagnostic triggers (debugging)
- **An API returns success but the expected side-effect didn't happen** — this is the #1 missed trigger
- User says something "doesn't work" and external services are involved
- The service dashboard shows the request was received but the expected result is missing
- A `try/catch` is swallowing errors and you need to understand what the API actually expects
- Any 4xx error from an API you haven't checked docs for recently

### Refactoring triggers
- Changing how an SDK is initialized (singleton, lazy, etc.)
- Changing how SDK method parameters are constructed
- Moving SDK calls to a different file or module (parameter shapes may need adjustment)

## Mandatory Steps

### 1. Check Version

```bash
# What's installed?
cat node_modules/<pkg>/package.json | grep '"version"'
# or: pip show <pkg> | grep Version

# What's latest?
npm info <pkg> version
# or: pip index versions <pkg>
```

Update if more than 1 major version behind.

### 2. Fetch Real Docs (pick one or more)

**Context7** (preferred for popular libraries):
```
resolve-library-id → query-docs with specific endpoint/method question
```

**Browser** (`fetch_webpage`):
```
Fetch the official API reference page for the specific endpoint or method being used
```

**DeepWiki** (if available):
```
Fetch from deepwiki.com for GitHub-based packages
```

Do NOT skip this step. Do NOT write integration code from memory. Do NOT diagnose failures from memory.

### 3. Compare Code vs Docs

Check for mismatches:
- Parameters code sends vs parameters docs accept
- **Value types and shapes** — does the parameter expect a specific type, object structure, or callback signature?
- Endpoint paths code hits vs current paths
- Response shape code expects vs current shape
- Required vs optional fields
- Removed or renamed parameters
- **How the SDK expects values to be constructed** — wrapper functions, factory methods, specific class instances vs plain objects

### 4. After Changes

- Remove deprecated env vars and parameters
- Update **all** call sites
- Build to verify types
- Test live and **verify the actual downstream effect** — don't just check the HTTP status code. Confirm the resource appears where expected (service dashboard, database, UI). A 200 with a valid-looking response body can still mean nothing happened.

## Common Failure Patterns

| Pattern | What Happens | Root Cause |
|---------|-------------|------------|
| **200 OK Trap** | API returns success, but resource is orphaned/invisible | Deprecated parameter silently ignored — new replacement exists in docs |
| **Wrong Diagnosis** | Multiple fix attempts blame infrastructure | SDK expects a specific value format (wrapper, factory, class instance) that differs from the plain value |

## Anti-Patterns

| Pattern | Risk |
|---------|------|
| Writing API code from memory | Parameters may not exist anymore |
| **Diagnosing API failures from memory** | **You'll guess wrong and waste turns on fake fixes** |
| Guessing infrastructure issues before checking API contract | The problem is usually in how you call the API, not the environment |
| `catch (e) { return { success: true } }` | Hides failures completely |
| `catch (e) { logger.error(e) }` with no rethrow or user feedback | Failure is logged but invisible to debugging flow |
| `if (CONFIG) { callAPI() }` with no else-log | Silent skip when config is missing |
| Passing extra params API won't reject | Silently ignored, feature broken |
| Trusting 200 + valid response body = success | Resource may exist but be orphaned/invisible |
| Verifying only the API response, not the downstream system | Missed side effects go undetected |
| Passing a plain value when the SDK expects a wrapped/constructed type | SDKs often require specific constructors, factory methods, or wrapper objects — not raw values |

## Decision Flowchart

```
User reports bug with external service
  │
  ├─ Is there a try/catch swallowing the error?
  │   └─ YES → Temporarily log the full error BEFORE guessing
  │
  ├─ Does the API return success but side-effect is missing?
  │   └─ YES → FETCH DOCS FIRST. Do NOT guess the cause.
  │            Compare exact parameter shapes, types, and values
  │            against what the docs specify.
  │
  └─ Is the error a 4xx?
      └─ YES → FETCH DOCS. Check which parameters are valid
               for the current SDK version.
```

## Bundled Resources

### `scripts/check_versions.py`
Automated version checker for npm and pip packages. Run it to quickly identify outdated dependencies:
```bash
# Check a single npm package
python3 scripts/check_versions.py npm resend
# Check all package.json dependencies
python3 scripts/check_versions.py npm --all
# Check a pip package
python3 scripts/check_versions.py pip requests
```

### `references/doc-urls.md`
Quick-reference table of official API documentation and changelog URLs for 30+ popular packages (email, payments, AI, databases, auth, cloud, analytics, frameworks). Consult this before searching — the correct URL may already be listed.

## Related Skills

- **dependency-management** — use alongside when resolving version conflicts or managing lockfiles
- **third-party-integration** — use alongside when implementing the actual integration patterns after verifying docs
- **api-versioning-strategy** — use when designing your own API's versioning, not checking upstream
