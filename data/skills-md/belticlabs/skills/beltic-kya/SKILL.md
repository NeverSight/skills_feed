---
name: beltic-kya
description: |
  Guidance for working with the Beltic KYA (Know Your Agent) ecosystem - a credential-based trust framework for AI agents. Use when: (1) Working in any Beltic repository (beltic-spec, beltic-cli, beltic-sdk, fact-python, kya-platform, wizard, nasa), (2) Implementing agent credential signing/verification, (3) Using @belticlabs/kya SDK or beltic-sdk Python, (4) Understanding agent safety certification, (5) Working with verifiable credentials for AI. Triggers on: Beltic CLI commands, agent credentials, HTTP message signatures (RFC 9421), safety scores, KYB tier verification, trust chain validation.
---

# Beltic KYA Ecosystem

KYA (Know Your Agent) is an **in-development** credential-based trust framework for AI agents. It establishes trust through cryptographically verifiable credentials.

## Trust Chain
```
Developer (KYB Verified) --> Issues --> Agent Credential --> Verified by --> Merchant/Platform
```

**Status**: This is a testing/development product. APIs and schemas may change.

---

## Critical Rules

### Package Names
- TypeScript: `@belticlabs/kya` (NOT `kya` or `beltic`)
- Python: `beltic-sdk` (NOT `beltic` or `kya`)

### CLI Flags
- `--alg` (NOT `--algorithm`)
- `--out` (NOT `--output`)
- `--key`, `--payload`, `--pub` (correct)

### Platform Directory
**DO NOT EDIT** anything in `platform/` directory. Read-only reference only.

### Git Commits
- Commit as: `pranav-beltic`
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- Always update CHANGELOG.md for user-facing changes

---

## Monorepo Navigation

| Repository | Purpose | Language |
|------------|---------|----------|
| **beltic-spec** | JSON schemas & specification | JSON Schema |
| **beltic-cli** | CLI for signing/verification | Rust |
| **beltic-sdk** | TypeScript SDK | TypeScript |
| **fact-python** | Python SDK | Python |
| **kya-platform** | Verification platform & API | TS/Next.js/Hono |
| **wizard** | Claude-powered credential bootstrap | TypeScript |
| **nasa** | Documentation site | MDX/Next.js |
| **homebrew-tap** | Homebrew formula | Ruby |
| **platform** | Enterprise risk platform | DO NOT EDIT |

### Cross-Repository Change Order
When changes affect multiple repos, follow this order:
1. **beltic-spec** first (schema changes)
2. **beltic-sdk** and **fact-python** (SDK updates)
3. **beltic-cli** (CLI changes)
4. **kya-platform** (platform changes)
5. **nasa** (documentation)

### Key Files
- `context.md` - Comprehensive ecosystem context
- `{repo}/CLAUDE.md` - Repository-specific guidance
- `beltic-spec/schemas/` - JSON Schema definitions

---

## CLI Quick Reference

| Command | Description |
|---------|-------------|
| `beltic init` | Create agent manifest interactively |
| `beltic dev-init` | Create self-attested developer credential |
| `beltic fingerprint` | Generate SHA256 code fingerprint |
| `beltic keygen --alg EdDSA` | Generate Ed25519 keypair |
| `beltic sign --key KEY --payload FILE` | Sign credential as JWS |
| `beltic verify --key KEY --token FILE` | Verify JWS token |
| `beltic http-sign` | Sign HTTP request (RFC 9421) |
| `beltic sandbox` | Run compliance tests |
| `beltic auth login` | Authenticate with KYA platform |

### Typical Workflow
```bash
beltic init                              # Create .beltic.yaml
beltic fingerprint                       # Generate code fingerprint
beltic keygen --alg EdDSA               # Generate keypair
beltic sign --key .beltic/eddsa-*-private.pem --payload agent-manifest.json
beltic verify --key .beltic/eddsa-*-public.pem --token credential.jwt
```

---

## SDK Patterns

### TypeScript (@belticlabs/kya)
```typescript
import {
  validateAgentCredential,
  validateDeveloperCredential,
  signCredential,
  verifyCredential,
  verifyAgentTrustChain,
  signHttpRequest,
  generateKeyPair,
} from '@belticlabs/kya';

// Trust chain verification
const result = await verifyAgentTrustChain(agentToken, {
  keyResolver: async (header) => publicKey,
  fetchDeveloperCredential: async (id) => developerJwt,
  policy: {
    minKybTier: 'tier_1',
    minPromptInjectionScore: 80,
  },
});
```

### Python (beltic-sdk)
```python
from beltic import (
    validate_agent_credential,
    validate_developer_credential,
    sign_credential,
    verify_credential,
    verify_agent_trust_chain,
    sign_http_request,
)

# Trust chain verification
result = await verify_agent_trust_chain(
    agent_token,
    TrustChainOptions(
        key_resolver=resolve_key,
        fetch_developer_credential=fetch_dev_cred,
        policy=TrustPolicy(
            min_kyb_tier="tier_1",
            min_prompt_injection_score=80,
        ),
    ),
)
```

---

## Safety Concepts

### Four Robustness Metrics (0-100 scores)
| Metric | Description |
|--------|-------------|
| `harmfulContentRefusalScore` | Refusal of harmful content requests |
| `promptInjectionRobustnessScore` | Resistance to prompt injection attacks |
| `toolAbuseRobustnessScore` | Prevention of tool misuse |
| `piiLeakageRobustnessScore` | Protection against PII extraction |

**Calculation**: Score = (1 - Attack Success Rate) x 100

### KYB Tiers
| Tier | Name | Verification Level |
|------|------|-------------------|
| `tier_0` | Unverified | Self-attested only |
| `tier_1` | Basic | Email/domain verified |
| `tier_2` | Standard | Identity documents |
| `tier_3` | Enhanced | Background checks |
| `tier_4` | Maximum | Regulated industries |

### Assurance Levels
- **self_attested**: Developer claims without verification
- **beltic_verified**: Beltic validates through evaluation
- **third_party_verified**: Independent auditor verification

---

## Sensitive Operations - PROMPT USER

**ALWAYS ask user confirmation before:**

### Key Operations
- Generating new keypairs (`beltic keygen`)
- Signing credentials (`beltic sign`)
- Deleting or rotating keys
- Modifying `.beltic/` directory contents

### Code Modifications
- Changes to cryptographic code (signing, verification)
- Modifications to schema definitions in `beltic-spec/schemas/`
- Changes to SDK verification logic
- Modifications to trust chain validation

### Platform Changes
- Any modifications to `kya-platform/` API routes
- Database schema changes (Drizzle migrations)
- Authentication/authorization logic changes
- Webhook handler modifications

### When Agent Cannot Proceed
If an operation requires:
- Access to private keys the agent doesn't have
- Platform authentication the agent cannot perform
- Manual verification steps (KYB, safety evaluation)
- Human judgment on security decisions

**Tell the user clearly:**
```
I cannot perform [operation] because [reason].
To proceed, you would need to [specific action required].
```

---

## Security Rules

### Never Commit
- Private keys (`.pem` files with "private" in name)
- API keys, secrets, tokens
- `.env` files with credentials
- `credentials.json` files

### Never Log
- Private key contents
- API keys or tokens
- Credential payloads with sensitive data
- User PII

### Always Validate
- File paths before reading/writing
- JSON/YAML before parsing
- Credential schemas before signing
- Signatures before trusting credentials

### Secure Defaults
- Reject algorithm `none` (always)
- Use Ed25519 (EdDSA) for new keys
- Set file permissions to 0600 for private keys
- Require HTTPS for production endpoints

---

## Cryptographic Standards

- **Algorithms**: ES256 (P-256), EdDSA (Ed25519)
- **Format**: JWS/JWT with W3C VC-compatible structure
- **DIDs**: did:web, did:key, did:ion
- **Revocation**: W3C Status List 2021
- **HTTP Signatures**: RFC 9421

---

## Reference Files

For detailed information, see:

- [Repository Details](references/repository-details.md) - Per-repo patterns and guidance
- [Credential Schemas](references/credential-schemas.md) - Schema field specifications
- [API Endpoints](references/api-endpoints.md) - KYA Platform API reference
- [Error Codes](references/error-codes.md) - Validation and signature error codes

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| `SIG-003: Algorithm none not allowed` | Use `--alg EdDSA` or `--alg ES256` |
| Schema validation fails | Run `npm run validate:all` in beltic-spec |
| Key not found | Check `.beltic/` directory for PEM files |
| HTTP signature fails | Verify key directory URL is accessible |
| Trust chain fails | Check developer credential is valid and not revoked |

---

## Development Status

This is an **in-development** product. Expect:
- API changes between versions
- Schema updates requiring re-signing
- New features being added
- Documentation gaps

When unsure about implementation details:
1. Check `context.md` for comprehensive context
2. Read the relevant repository's `CLAUDE.md`
3. Look at existing code patterns
4. Ask the user for clarification
