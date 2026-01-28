---
name: ai-pro
description: Professional AI and System Orchestrator. Specialized in GPT-5, autonomous agents, Auth.js v5, Stripe v13, Monorepos (Bun/pnpm), and large codebase intelligence. Optimized for January 2026 standards.
---

# AI-PRO: Professional AI & System Orchestrator

## Overview
**AI-PRO** is the definitive skill for managing modern, high-performance software ecosystems in 2026. It bridges the gap between raw AI capabilities (GPT-5, o3-deep-research) and enterprise-grade infrastructure (Auth.js v5, Stripe v13, Bun/pnpm Monorepos).

This skill is designed for the **Senior AI Engineer** who needs to orchestrate autonomous agents while maintaining strict security, performance, and architectural integrity.

## Core Pillars of the 2026 Stack

### 1. The AI Frontier (GPT-5 & Autonomous Agents)
The paradigm has shifted from "Chat" to "Agents". We utilize the GPT-5 family for complex tool-use and `o3-deep-research` for iterative discovery missions.
- **Reference**: [`references/ai-agents.md`](./references/ai-agents.md)

### 2. Identity & Security (Auth.js v5)
Security in 2026 is "Edge-First". Auth.js v5 provides 25% faster validation and native Edge support using the standardized `AUTH_` prefix.
- **Reference**: [`references/auth-v5.md`](./references/auth-v5.md)

### 3. Financial Infrastructure (Stripe v13+)
Modern API consumption leverages auto-paginating SDKs and deeply expanded objects to reduce network overhead and boilerplate.
- **Reference**: [`references/api-v13.md`](./references/api-v13.md)

### 4. Codebase Intelligence (Architect & Archive)
Managing massive codebases requires "Context Packing" with Repomix and high-performance search via `git grep` and indexed symbol maps.
- **Reference**: [`references/architect-archive.md`](./references/architect-archive.md)

---

## Strategic Implementation Guide

### The "Autonomous Orchestrator" Pattern
To build a system that can self-heal and evolve, follow the **O.R.C.A.** (Observe, Reason, Check, Act) pattern.

#### Example: Self-Healing API Integration
```typescript
import { gpt5 } from '@openai/provider';
import { generateText } from 'ai-sdk';
import { auth } from '@/auth';
import Stripe from 'stripe';

/**
 * AI-PRO Orchestrator: Automatically fixes API version mismatches
 */
async function selfHealingPayment(customerId: string) {
  const session = await auth(); // Auth.js v5 Edge-First
  const stripe = new Stripe(process.env.AUTH_STRIPE_SECRET!, {
    apiVersion: '2025-10-01',
  });

  try {
    const customer = await stripe.customers.retrieve(customerId, {
      expand: ['subscriptions.data.default_payment_method'],
    });
    // Business logic...
  } catch (error) {
    // If error is related to API versioning or schema change
    const diagnostic = await generateText({
      model: gpt5('gpt-5-pro'),
      prompt: `Analyze this Stripe error: ${error.message}. 
               Context: We are using SDK v13. 
               Suggest a fix or retry strategy.`,
    });
    
    console.log(`AI-PRO Diagnostic: ${diagnostic.text}`);
    // Implement auto-retry or fallback logic here
  }
}
```

---

## Advanced Search & Context Management

### Ripgrep Masterclass
When searching through million-line archives, speed is safety.

| Command | Use Case |
| :--- | :--- |
| `rg -l "pattern"` | List ONLY filenames containing the pattern. |
| `rg -C 5 "pattern"` | Show 5 lines of context around the match. |
| `rg -t typescript "pattern"` | Search ONLY in TypeScript files. |
| `rg --stats "pattern"` | Show performance stats (count, time). |

### Repomix Strategy
Before starting a complex refactor, generate a "Codebase Map":
```bash
bun x repomix --include "src/core/**,src/types/**" --output .ai-context/core-map.xml
```

---

## The "Do Not" List (Anti-Patterns to Avoid)

### ❌ AI & Agents
- **Do NOT** allow an agent to commit to `main` without a `strict-auditor` check.
- **Do NOT** hardcode model names; use a registry or environment variables to allow for easy upgrades (e.g., GPT-5 -> GPT-6).
- **Do NOT** use agents for deterministic tasks (like regex) where a simple script suffices.

### ❌ Authentication
- **Do NOT** use `process.env.NEXTAUTH_SECRET`; v5 expects `AUTH_SECRET`.
- **Do NOT** store PII (Personally Identifiable Information) in JWTs; keep tokens lean for Edge performance.
- **Do NOT** ignore the `AUTH_TRUST_HOST` requirement in non-Vercel environments.

### ❌ API & SDKs
- **Do NOT** manually handle Stripe pagination using `starting_after`; it is error-prone. Use `for await...of`.
- **Do NOT** neglect webhook signature verification; it is the #1 vector for payment fraud.

### ❌ Architecture
- **Do NOT** create "Monster Monorepos" without clear package boundaries. Use `pnpm-workspace.yaml`.
- **Do NOT** include `node_modules` in your `repomix` packs; it will blow your token budget.

---

## Evolution Roadmap (2026-2027)

### Q1 2026: The o3 Stabilization
- Deep integration of `o3-deep-research` into CI/CD pipelines for autonomous bug hunting.
- Standardization of the `AUTH_` prefix across all Squadds projects.

### Q2 2026: GPT-5 Multi-Modal Agents
- Native visual auditing: Agents that "see" the UI to find CSS regressions.
- Real-time audio debugging: Voice-driven system diagnostics.

### H2 2026: The GPT-6 Horizon
- Early testing of "Infinite Context" models.
- Transition from Monorepos to "Micro-Repos" managed by a Centralized AI Architect.

---

## Quick Reference Commands

### Identity Setup (Auth.js v5)
```bash
# Generate AUTH_SECRET
openssl rand -base64 32
```

### Dependency Sync (Bun + pnpm)
```bash
# Reinstall all workspace deps with Bun's speed
bun install --frozen-lockfile
```

### Context Packing
```bash
# Pack core logic for AI review
bun x repomix --style markdown --output review.md
```

### Large Scale Search
```bash
# Find all sensitive keys across the archive
git grep -E "(SECRET|KEY|PASSWORD)" -- ':!*.lockb'
```

---

## Troubleshooting

### Issue: "Missing AUTH_SECRET"
- **Cause**: Auth.js v5 requires this for encryption in production.
- **Fix**: Add `AUTH_SECRET` to your `.env` or CI secrets.

### Issue: "Stripe SDK Pagination Error"
- **Cause**: Trying to access `.data` on an async iterator.
- **Fix**: Use `for await (const item of stripe.customers.list())` directly.

### Issue: "Repomix Token Overflow"
- **Cause**: Packing too many files or large assets.
- **Fix**: Use `--ignore` or create a specific `repomix.config.json` for the module.

---

## Metadata
- **Version**: 2.0.0 (January 2026 Refactor)
- **Primary Agent**: AI-PRO
- **Sub-Agents**: `auth-expert`, `api-pro`, `architect-pro`, `archive-searcher`
- **Compatibility**: Next.js 16.1+, React 19.2+, Stripe 13.5+, Bun 1.2+

*Updated: January 22, 2026 - 15:20*
