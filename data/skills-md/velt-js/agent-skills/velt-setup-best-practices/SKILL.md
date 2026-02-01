---
name: velt-setup-best-practices
description: Velt collaboration SDK setup guide for React, Next.js, Angular, Vue, and HTML applications. Use this skill when setting up Velt for the first time, configuring VeltProvider, implementing user authentication, or initializing document collaboration.
license: MIT
metadata:
  author: velt
  version: "1.0.0"
---

# Velt Setup Best Practices

Comprehensive setup guide for Velt collaboration SDK. Contains 21 rules across 8 categories covering installation, authentication, document setup, and project organization.

## When to Apply

Reference these guidelines when:
- Setting up Velt in a new React, Next.js, Angular, Vue, or HTML project
- Configuring VeltProvider and API keys
- Implementing user authentication with Velt (userId, organizationId)
- Setting up JWT token generation for production
- Initializing documents with documentId
- Organizing Velt-related files in your project

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Installation | CRITICAL | `install-` |
| 2 | Provider Wiring | CRITICAL | `provider-` |
| 3 | Identity | CRITICAL | `identity-` |
| 4 | Document Identity | CRITICAL | `document-` |
| 5 | Config | HIGH | `config-` |
| 6 | Project Structure | MEDIUM | `structure-` |
| 7 | Routing Surfaces | MEDIUM | `surface-` |
| 8 | Debugging & Testing | LOW-MEDIUM | `debug-` |

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/react/installation/install-react-packages.md
rules/react/provider-wiring/provider-velt-provider-setup.md
rules/shared/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Verification checklist
- Source pointers to official docs

## Compiled Documents

- `AGENTS.md` — Compressed index of all rules with file paths (start here)
- `AGENTS.full.md` — Full verbose guide with all rules expanded inline
