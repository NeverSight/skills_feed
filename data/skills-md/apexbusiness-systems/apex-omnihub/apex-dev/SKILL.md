---
name: apex-dev
version: "1.0.0"
description: "Omniscient APEX Ecosystem development skill. Triggers: apex code, omnihub development, tradeline build, aspiral feature, apex bug, fix apex, apex architecture, omnidash component, triforce guardian, man mode, apex security, apex test, armageddon test, apex deploy, apex optimize, semantic translation, web2 web3 bridge. Produces: zero-drift, first-pass success code for APEX OmniHub, TradeLine 24/7, aSpiral, and all connected applications. Compatible with all LLMs."
license: "Proprietary - APEX Business Systems Ltd. Edmonton, AB, Canada. https://apexbusiness-systems.com | https://apexomnihub.icu"
author: "JR Mendoza, CEO - APEX Business Systems"
compatibility: "Claude, GPT-4/4o, Gemini, Llama 3, Mistral, Codex, any instruction-following LLM"
---

# APEX-DEV: Omniscient Development Skill

**Mission**: Enable any LLM to produce enterprise-grade, zero-drift, first-pass success code for the APEX ecosystem.

**Philosophy**: "Intelligence Designed" — Every output is deterministic, secure, portable, and production-ready.

---

## INPUT/OUTPUT CONTRACT

**Input**: Task description referencing APEX ecosystem (OmniHub, TradeLine, aSpiral, OmniDash, etc.)
**Output**: Production-ready code, architecture decisions, or fixes with verification steps
**Success**: Code passes lint, type-check, and relevant ARMAGEDDON test battery

---

## SYNTHETIC MEMORY ANCHOR

Before ANY action, internalize these invariants:

```
┌─────────────────────────────────────────────────────────────────────┐
│ APEX ECOSYSTEM TRUTH TABLE (Load into working memory)              │
├─────────────────────────────────────────────────────────────────────┤
│ Platform:     APEX OmniHub ("Intelligence Designed")               │
│ Domain:       apexomnihub.icu                                      │
│ Core Value:   Universal Orchestration (Web2 ↔ Web3 Semantic Bridge)│
│ Stack:        React 18 + Vite + TypeScript + Tailwind + shadcn UI  │
│ Backend:      Supabase (Auth, Storage, Edge Functions, Postgres)   │
│ Orchestrator: Temporal.io (Event Sourcing + Saga Pattern)          │
│ Security:     Guardian/Triforce + MAN Mode + Zero-Trust + RLS      │
│ Test Suite:   ARMAGEDDON (265 tests, 100% pass, Level 6 Adaptive)  │
│ Non-Negotiable: No vendor lock-in, no drift, no loops, no secrets  │
└─────────────────────────────────────────────────────────────────────┘
```

**DRIFT PREVENTION**: Re-read this anchor every 3 tool calls or context switches.

---

## DECISION TREE (Entry Point)

**What are you doing?**

```
Building new feature?     → Section A: FEATURE DEVELOPMENT
Fixing a bug?             → Section B: BUG RESOLUTION PROTOCOL
Optimizing performance?   → Section C: PERFORMANCE ENGINEERING
Security hardening?       → Section D: SECURITY POSTURE
Writing tests?            → Section E: ARMAGEDDON TEST PROTOCOL
Deploying/DevOps?         → Section F: DEPLOYMENT & OPS
Architecture decision?    → Section G: ARCHITECTURE PATTERNS
Working on specific app?  → Section H: APP-SPECIFIC PATTERNS
```

---

## SECTION A: FEATURE DEVELOPMENT

### A1. Pre-Flight Checklist

Before writing ANY code:

```
□ Identify target module (OmniDash | OmniConnect | OmniLink | Guardian | Edge)
□ Check existing patterns in that module (don't reinvent)
□ Verify abstraction layer exists (no direct provider calls)
□ Confirm test strategy (unit + integration + chaos)
□ Load relevant type definitions
```

### A2. File Placement Decision Tree

```
UI Component?
├─ Shared across apps → src/components/
├─ Page-specific → src/pages/{PageName}/components/
└─ shadcn primitive → src/components/ui/

Business Logic?
├─ API calls → src/lib/api/
├─ State management → src/contexts/ or src/stores/
├─ Utilities → src/lib/utils/
└─ Security → src/security/

Backend?
├─ Edge Function → supabase/functions/{name}/
├─ Workflow → orchestrator/workflows/
├─ Activity → orchestrator/activities/
└─ Migration → supabase/migrations/

Test?
├─ Unit → tests/{module}/
├─ E2E → tests/e2e/
├─ Chaos → tests/chaos/
└─ Security → tests/prompt-defense/
```

### A3. Component Template (React + TypeScript)

```typescript
// src/components/{ComponentName}.tsx
import { FC, memo } from 'react';
import { cn } from '@/lib/utils';

interface {ComponentName}Props {
  /** Required: Describe purpose */
  requiredProp: string;
  /** Optional: Describe default behavior */
  optionalProp?: boolean;
  className?: string;
}

/**
 * {ComponentName} - One-line description
 * @example <{ComponentName} requiredProp="value" />
 */
export const {ComponentName}: FC<{ComponentName}Props> = memo(({
  requiredProp,
  optionalProp = false,
  className,
}) => {
  return (
    <div className={cn('base-styles', className)}>
      {/* Implementation */}
    </div>
  );
});

{ComponentName}.displayName = '{ComponentName}';
```

### A4. Hook Template

```typescript
// src/hooks/use{HookName}.ts
import { useState, useCallback, useEffect } from 'react';

interface Use{HookName}Options {
  initialValue?: string;
}

interface Use{HookName}Return {
  value: string;
  setValue: (v: string) => void;
  isLoading: boolean;
  error: Error | null;
}

export function use{HookName}(options: Use{HookName}Options = {}): Use{HookName}Return {
  const [value, setValue] = useState(options.initialValue ?? '');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  // Cleanup on unmount (prevent memory leaks)
  useEffect(() => {
    return () => {
      // Cleanup timers, subscriptions, etc.
    };
  }, []);

  return { value, setValue, isLoading, error };
}
```

---

## SECTION B: BUG RESOLUTION PROTOCOL

### B1. Root Cause Analysis (Mandatory Steps)

```
1. REPRODUCE → Get exact steps, inputs, expected vs actual
2. ISOLATE   → Identify smallest code path that triggers bug
3. TRACE     → Follow data flow from input to failure point
4. IDENTIFY  → Name the root cause (not symptoms)
5. FIX       → Patch at root, not at symptom
6. VERIFY    → Regression test + add to ARMAGEDDON suite
7. DOCUMENT  → Update CHANGELOG, add test case comment
```

### B2. Common APEX Bug Patterns (Pre-empted)

| Symptom | Root Cause | Fix Pattern |
|---------|------------|-------------|
| "Cannot read property of undefined" | Missing null check on Supabase response | `data?.property ?? fallback` |
| Infinite re-render | Missing dependency in useEffect | Add dep or use useCallback |
| Stale data after mutation | React Query cache not invalidated | `queryClient.invalidateQueries(['key'])` |
| Auth token expired | Session refresh not triggered | Check AuthContext refresh logic |
| Type error in Edge Function | Deno vs Node type mismatch | Use Supabase Edge Function types |
| RLS policy blocking | Policy condition wrong | Check `auth.uid()` vs `user_id` |
| Guardian heartbeat stale | Loop not started | Verify `npm run guardian:status` |

### B3. Debug Command Sequence

```bash
# 1. Check build health
npm run build 2>&1 | head -50

# 2. Run type check
npm run typecheck

# 3. Run relevant test battery
npm test -- --grep "{module}"

# 4. Check Guardian status
npm run guardian:status

# 5. Verify security posture
npm run security:audit

# 6. Check for console errors in dev
npm run dev 2>&1 | grep -i error
```

---

## SECTION C: PERFORMANCE ENGINEERING

### C1. Performance Targets (ARMAGEDDON-Verified)

| Metric | Target | Current |
|--------|--------|---------|
| API Response (p95) | <100ms | <10ms ✓ |
| DB Query (p95) | <500ms | <20ms ✓ |
| State Update | <100ms | <5ms ✓ |
| Concurrent Users | 100+ | 100+ ✓ |
| WebSocket Messages/s | 1000+ | 1000+ ✓ |

### C2. Optimization Decision Tree

```
Slow API call?
├─ Add React Query caching → staleTime: 5 * 60 * 1000
├─ Check N+1 queries → Use Supabase .select('*, relation(*)')
└─ Add index → supabase/migrations/

Slow render?
├─ Add memo() to component
├─ Use useMemo/useCallback for expensive computations
└─ Lazy load with React.lazy + Suspense

Memory leak?
├─ Check useEffect cleanup
├─ Verify event listener removal
└─ Check timer/interval cleanup
```

### C3. React Query Pattern (Standard)

```typescript
// src/lib/api/{resource}.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/lib/supabase';

const STALE_TIME = 5 * 60 * 1000; // 5 minutes

export function use{Resource}s() {
  return useQuery({
    queryKey: ['{resource}s'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('{resource}s')
        .select('*')
        .order('created_at', { ascending: false });
      if (error) throw error;
      return data;
    },
    staleTime: STALE_TIME,
  });
}

export function useCreate{Resource}() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: Create{Resource}Payload) => {
      const { data, error } = await supabase
        .from('{resource}s')
        .insert(payload)
        .select()
        .single();
      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['{resource}s'] });
    },
  });
}
```

---

## SECTION D: SECURITY POSTURE

### D1. Security Invariants (NEVER Violate)

```
❌ NEVER commit secrets (API keys, tokens, passwords)
❌ NEVER trust user input without validation
❌ NEVER bypass RLS policies
❌ NEVER execute raw SQL from user input
❌ NEVER disable CSRF protection
❌ NEVER log PII to console in production

✅ ALWAYS use parameterized queries
✅ ALWAYS validate with Zod schemas
✅ ALWAYS use RLS for row-level access
✅ ALWAYS audit log security events
✅ ALWAYS use Guardian heartbeat for critical loops
```

### D2. MAN Mode (Manual Approval Node) Integration

Risk classification for agent actions:

| Lane | Behavior | Tool Examples |
|------|----------|---------------|
| GREEN | Auto-execute | `search_database`, `read_record`, `get_config` |
| YELLOW | Execute + Audit Log | Unknown tools, single high-risk param |
| RED | Isolate + Human Approval | `delete_record`, `transfer_funds`, `send_email` |
| BLOCKED | Never Execute | `execute_sql_raw`, `shell_execute` |

```typescript
// Use MAN Mode for high-risk actions
import { riskTriage } from '@/orchestrator/policies/man_policy';

const result = riskTriage({
  tool: 'delete_record',
  params: { id: recordId },
  context: { userId, sessionId }
});

if (result.lane === 'RED') {
  // Isolate and await human approval
  await createManTask(result);
  return { status: 'isolated', awaiting_approval: true };
}
```

### D3. Prompt Injection Defense

```typescript
// src/security/promptDefense.ts
import { evaluatePrompt } from './promptDefenseConfig';

// Always sanitize LLM inputs
function sanitizeUserInput(input: string): string {
  const result = evaluatePrompt(input);
  if (result.blocked) {
    auditLog.record({
      actionType: 'PROMPT_INJECTION_BLOCKED',
      metadata: { pattern: result.matchedPattern }
    });
    throw new SecurityError('Invalid input detected');
  }
  return result.sanitized;
}
```

### D4. Zero-Trust Device Registry

```typescript
// Verify device on every sensitive operation
import { deviceRegistry } from '@/zero-trust/deviceRegistry';

async function sensitiveOperation(userId: string, deviceId: string) {
  const device = await deviceRegistry.verify(userId, deviceId);
  if (device.status !== 'trusted') {
    throw new SecurityError('Device not trusted');
  }
  // Proceed with operation
}
```

---

## SECTION E: ARMAGEDDON TEST PROTOCOL

### E1. Test Battery Structure

```
tests/
├── chaos/                    # Chaos engineering tests
│   ├── battery.spec.ts       # Core chaos battery (21 tests)
│   ├── memory-stress.spec.ts # Memory leak detection (7 tests)
│   └── integration-stress.spec.ts # Integration stress (9 tests)
├── e2e/                      # End-to-end tests
│   ├── enterprise-workflows.spec.ts # Business flows (20 tests)
│   ├── errorHandling.spec.ts # Error scenarios (8 tests)
│   └── security.spec.ts      # Security tests (13 tests)
├── prompt-defense/           # Prompt injection tests
│   └── real-injection.spec.ts # Real-world attacks
└── {module}/                 # Unit tests per module
```

### E2. Test Template (Vitest)

```typescript
// tests/{module}/{feature}.spec.ts
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

describe('{Feature}', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should {expected behavior} when {condition}', async () => {
    // Arrange
    const input = { /* test data */ };

    // Act
    const result = await featureUnderTest(input);

    // Assert
    expect(result).toMatchObject({ /* expected */ });
  });

  it('should handle error when {error condition}', async () => {
    // Arrange
    vi.spyOn(dependency, 'method').mockRejectedValue(new Error('fail'));

    // Act & Assert
    await expect(featureUnderTest({})).rejects.toThrow('fail');
  });
});
```

### E3. Test Commands

```bash
# Run all tests
npm test

# Run specific battery
npm test -- --grep "chaos"

# Run prompt defense tests
npm run test:prompt-defense

# Run chaos simulation (CI-safe dry run)
npm run sim:dry

# Run E2E (requires server)
npm run test:e2e

# Full ARMAGEDDON suite
npm run armageddon
```

---

## SECTION F: DEPLOYMENT & OPS

### F1. Deployment Checklist

```
□ Build passes: npm run build
□ Type check passes: npm run typecheck
□ All tests pass: npm test
□ Security audit clean: npm run security:audit
□ No console.log in production code
□ Environment variables documented
□ Rollback plan documented
```

### F2. Environment Variables (Required)

```bash
# .env.example (NEVER commit actual values)
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=eyJ...
# Optional
VITE_SENTRY_DSN=https://xxx@sentry.io/xxx
```

### F3. Rollback Protocol

```bash
# 1. Identify failing deployment
vercel ls --prod

# 2. Rollback to previous
vercel rollback <deployment-url>

# 3. Verify rollback
curl -I https://apexomnihub.icu/health

# 4. Post-mortem within 24h
```

---

## SECTION G: ARCHITECTURE PATTERNS

### G1. Core Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER (React + shadcn UI)                              │
│ - OmniDash (Navigation UI)                                          │
│ - Pages (Route-level components)                                    │
│ - Components (Reusable UI)                                          │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│ APPLICATION LAYER (Hooks + Context + React Query)                   │
│ - AuthContext (Session management)                                  │
│ - useQuery/useMutation (Data fetching)                             │
│ - Business logic hooks                                              │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│ INTEGRATION LAYER (Adapters - Single Port Rule)                     │
│ - Supabase adapter (auth, db, storage)                             │
│ - OmniLink adapter (cross-app orchestration)                       │
│ - Web3 adapter (wallet, contracts)                                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│ ORCHESTRATION LAYER (Temporal.io)                                   │
│ - Event Sourcing (Canonical Data Model)                            │
│ - Saga Pattern (LIFO Compensation)                                 │
│ - Semantic Caching (70% cost reduction)                            │
│ - MAN Mode (Human-in-the-loop for RED lane)                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────────┐
│ SECURITY LAYER (Guardian/Triforce)                                  │
│ - Guardian heartbeats                                               │
│ - Zero-trust device registry                                        │
│ - Prompt injection defense                                          │
│ - RLS policies                                                      │
│ - Audit logging                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### G2. Portability Principle

```typescript
// ❌ BAD: Direct provider coupling
import { createClient } from '@supabase/supabase-js';
const data = await supabase.from('users').select('*');

// ✅ GOOD: Abstraction layer
// src/lib/database/interface.ts
interface Database {
  query<T>(table: string, options: QueryOptions): Promise<T[]>;
}

// src/lib/database/supabase.ts
export const supabaseDatabase: Database = {
  async query(table, options) {
    const { data } = await supabase.from(table).select(options.select);
    return data;
  }
};

// src/lib/database/index.ts
import { supabaseDatabase } from './supabase';
export const database: Database = supabaseDatabase; // Swap here for migration
```

### G3. Single Integration Port Rule

All external system calls go through ONE adapter module:

```
src/lib/
├── supabase/           # Single port for Supabase
│   ├── index.ts        # Re-exports
│   ├── auth.ts         # Auth methods
│   ├── database.ts     # Query methods
│   └── storage.ts      # Storage methods
├── web3/               # Single port for Web3
│   ├── index.ts
│   ├── wallet.ts
│   └── contracts.ts
└── omnilink/           # Single port for OmniLink orchestration
    ├── index.ts
    └── events.ts
```

---

## SECTION H: APP-SPECIFIC PATTERNS

### H1. OmniDash (Navigation UI)

```typescript
// Revolutionary icon-based navigation
// Location: src/components/OmniDashNavIconButton.tsx

// Pattern: Zero-overlap flexbox layout
<nav className="flex items-center justify-between">
  <OmniDashNavIconButton icon={Home} label="Dashboard" to="/" />
  <OmniDashNavIconButton icon={Settings} label="Settings" to="/settings" />
</nav>

// Mobile: Bottom tabs
// Desktop: Side navigation with tooltips
```

### H2. Guardian/Triforce (Security)

```typescript
// Guardian heartbeat pattern
// Location: src/guardian/heartbeat.ts

import { startHeartbeat, getStatus } from '@/guardian/heartbeat';

// Start on app mount
useEffect(() => {
  const cleanup = startHeartbeat('main-loop', 30000); // 30s interval
  return cleanup;
}, []);

// Check status
const status = getStatus('main-loop');
// { loopName: 'main-loop', lastSeen: Date, ageMs: number, status: 'healthy' | 'stale' }
```

### H3. Temporal Workflow Pattern

```python
# orchestrator/workflows/agent_saga.py

@workflow.defn
class AgentSagaWorkflow:
    @workflow.run
    async def run(self, goal: Goal) -> GoalResult:
        compensation_stack: List[CompensationStep] = []
        
        try:
            # Execute steps with compensation tracking
            for step in plan.steps:
                result = await workflow.execute_activity(
                    execute_tool,
                    step,
                    start_to_close_timeout=timedelta(seconds=30),
                )
                compensation_stack.append(step.compensation)
            
            return GoalResult(status="completed", events=events)
            
        except Exception as e:
            # LIFO compensation (rollback)
            for comp in reversed(compensation_stack):
                await workflow.execute_activity(compensate, comp)
            raise
```

---

## ANTI-DRIFT PROTOCOL

### Every 3 Tool Calls, Verify:

```
□ Am I still solving the ORIGINAL task?
□ Have I introduced any provider lock-in?
□ Does this code have a test?
□ Is security considered (RLS, validation, audit)?
□ Would this pass ARMAGEDDON Level 6?
```

### Loop Detection (ABORT if triggered):

```
IF same error appears 3x → STOP, re-read Section B (Bug Protocol)
IF same code pattern rewritten 3x → STOP, extract to utility
IF task scope expanded 2x → STOP, confirm with user
IF file touched 5x without progress → STOP, architectural issue
```

---

## FAILURE PRE-EMPTION (Common Mistakes)

| Mistake | Prevention |
|---------|------------|
| Importing from wrong path | Use `@/` alias, verify in tsconfig |
| Missing `key` prop in lists | Always use unique stable ID, never index |
| Async/await in useEffect | Wrap in IIFE or use separate async function |
| Direct state mutation | Always spread: `setState(prev => ({ ...prev, field: value }))` |
| Missing error boundary | Wrap route-level components |
| Console.log in production | Use conditional: `import.meta.env.DEV && console.log()` |
| Hardcoded URLs | Use env variables: `import.meta.env.VITE_API_URL` |
| Missing cleanup in useEffect | Always return cleanup function for subscriptions/timers |

---

## COMMAND REFERENCE (Quick Access)

```bash
# Development
npm run dev              # Start dev server
npm run build            # Production build
npm run preview          # Preview production build

# Quality
npm run typecheck        # TypeScript check
npm run lint             # ESLint
npm run lint:fix         # Auto-fix lint issues
npm test                 # Run all tests
npm run test:watch       # Watch mode

# Security
npm run security:audit   # Dependency audit
npm run test:prompt-defense  # Prompt injection tests

# Operations
npm run guardian:status  # Check guardian loops
npm run zero-trust:baseline  # Generate baseline metrics
npm run dr:test          # Disaster recovery test (dry-run)

# Simulation
npm run sim:dry          # Chaos simulation (safe)
npm run armageddon       # Full test suite
```

---

## SUCCESS CRITERIA

Every task is complete when:

```
✅ Code compiles: npm run build passes
✅ Types valid: npm run typecheck passes
✅ Tests pass: npm test passes
✅ Security clean: npm run security:audit clean
✅ No drift: Original task accomplished
✅ Documented: CHANGELOG updated if applicable
✅ Portable: No new vendor lock-in introduced
```

---

**Skill Version**: 1.0.0
**Last Updated**: 2026-01-20
**Maintained By**: APEX Business Systems Engineering
**License**: Proprietary - APEX Business Systems Ltd. Edmonton, AB, Canada
