---
name: omnidev
description: "Omniscient hyper-elite software engineering command center. Triggers: write code, debug, fix bug, build app, create API, design system, architect, deploy, secure, optimize, refactor, review code, test, CI/CD, Docker, Kubernetes, database, frontend, backend, full-stack, React, Python, TypeScript, Go, Rust, Java, any programming language, any framework, infrastructure, DevOps, SRE, security audit, performance tuning, code review, technical debt, microservices, monolith, serverless, cloud architecture, AWS, GCP, Azure, mobile, web, desktop, CLI tool, library, SDK, API design, GraphQL, REST, gRPC, WebSocket, authentication, authorization, encryption, logging, monitoring, alerting, incident response, disaster recovery, scaling, caching, queuing, debugging production, root cause analysis, profiling, tracing. Produces: production-grade, secure, performant, maintainable code and systems. Enables 10x development velocity with first-pass success."
---

# OmniDev

**Mission**: Enable 10x development velocity through omniscient software engineering mastery across all languages, frameworks, and domains.

## Decision Tree - Start Here

**What are you doing?**

| Task | Go To |
|------|-------|
| **Writing new code** | → [Code Generation](#code-generation) |
| **Fixing/debugging** | → [Debug Protocol](#debug-protocol) |
| **Designing system** | → [Architecture](#architecture) |
| **Deploying/DevOps** | → [Infrastructure](#infrastructure) |
| **Security work** | → [Security](#security) |
| **Performance issues** | → [Optimization](#optimization) |
| **Code review** | → [Review Protocol](#review-protocol) |

---

## Code Generation

**Input**: Requirements (natural language or specs)  
**Output**: Production-ready code in /mnt/user-data/outputs/  
**Success**: Passes lint, tests, security scan

### Language Selection

| Criteria | Language |
|----------|----------|
| Web API (speed critical) | Go, Rust |
| Web API (rapid dev) | Python FastAPI, Node/TypeScript |
| Enterprise/Android | Kotlin, Java |
| iOS/macOS | Swift |
| Systems/CLI | Rust, Go |
| ML/Data | Python |
| Frontend | TypeScript + React/Vue/Svelte |
| Scripts/Automation | Python, Bash |

### Code Quality Gates (ALWAYS)

```bash
# Before ANY code is complete:
1. Lint        → Language-specific linter (no warnings)
2. Type check  → mypy/tsc/go vet (strict mode)
3. Test        → pytest/jest/go test (>80% coverage)
4. Security    → bandit/npm audit/gosec (0 high/critical)
5. Format      → black/prettier/gofmt (auto-applied)
```

### Patterns by Domain

**API Endpoint** (FastAPI example):
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_item(db, item)
    except IntegrityError:
        raise HTTPException(409, "Item exists")
```

**React Component** (TypeScript):
```typescript
interface Props {
  items: Item[];
  onSelect: (id: string) => void;
}

export const ItemList: React.FC<Props> = ({ items, onSelect }) => {
  const [selected, setSelected] = useState<string | null>(null);
  
  const handleSelect = useCallback((id: string) => {
    setSelected(id);
    onSelect(id);
  }, [onSelect]);

  return (
    <ul role="listbox" aria-label="Items">
      {items.map(item => (
        <li key={item.id} onClick={() => handleSelect(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
};
```

---

## Debug Protocol

**Input**: Bug description, error message, or unexpected behavior  
**Output**: Root cause + fix  
**Success**: Issue resolved, regression test added

### Debug Decision Tree

```
1. REPRODUCE → Can you trigger the bug consistently?
   ├─ No  → Add logging, gather more data
   └─ Yes → Continue
   
2. ISOLATE → Where does it fail?
   ├─ Frontend → Browser DevTools, React DevTools
   ├─ API → Request/Response logging, curl testing
   ├─ Database → Query analysis, EXPLAIN
   └─ Infrastructure → Logs, metrics, traces
   
3. HYPOTHESIZE → What could cause this?
   ├─ List 3 most likely causes
   └─ Test each systematically
   
4. FIX → Apply minimal change
   
5. VERIFY → Run tests + manual verification
   
6. PREVENT → Add test covering this case
```

### Common Bug Patterns

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Works locally, fails prod | Env vars, secrets, config | Check env parity |
| Intermittent failure | Race condition, timeout | Add locks/retries |
| Memory leak | Unclosed resources, event listeners | Cleanup in finally/useEffect |
| Slow query | Missing index, N+1 | EXPLAIN ANALYZE, add index |
| CORS error | Missing headers | Configure CORS middleware |
| 401/403 | Token expired, wrong scope | Check auth flow |
| 500 error | Unhandled exception | Add try/catch, logging |

### Debug Commands

```bash
# Python
python -m pdb script.py          # Interactive debugger
python -c "import traceback; traceback.print_exc()"

# Node
node --inspect script.js         # Chrome DevTools debug
DEBUG=* node script.js           # Enable debug logging

# Go
dlv debug ./main.go              # Delve debugger
GODEBUG=gctrace=1 ./app          # GC tracing

# Logs
journalctl -u service -f         # Follow systemd logs
kubectl logs -f pod-name         # K8s pod logs
docker logs -f container         # Docker logs
```

---

## Architecture

**Input**: Business requirements, constraints, scale expectations  
**Output**: System design document, architecture diagram description  
**Success**: Meets requirements, scalable, maintainable

### Architecture Decision Tree

```
SCALE?
├─ <1K users → Monolith + PostgreSQL
├─ 1K-100K   → Modular monolith or simple microservices
├─ 100K-1M   → Microservices + caching + CDN
└─ >1M       → See references/scale.md

TEAM SIZE?
├─ 1-3 devs  → Monolith (always)
├─ 4-10 devs → Modular monolith
└─ >10 devs  → Consider microservices

LATENCY?
├─ <50ms  → Edge computing, caching, CDN
├─ <200ms → Regional deployment
└─ <1s    → Standard architecture
```

### Architecture Patterns

| Pattern | When | Example |
|---------|------|---------|
| **Monolith** | Small team, MVP, <100K users | Django/Rails app |
| **Modular Monolith** | Growing team, clear domains | Bounded contexts in one deploy |
| **Microservices** | Large team, independent scaling | Service per domain |
| **Serverless** | Event-driven, variable load | Lambda + API Gateway |
| **Event Sourcing** | Audit requirements, complex state | Banking, inventory |
| **CQRS** | Read/write asymmetry | High-read dashboards |

### System Design Template

```markdown
## [System Name]

### Requirements
- Functional: [What it must do]
- Non-functional: [Performance, scale, availability]
- Constraints: [Budget, timeline, team skills]

### High-Level Design
- Components: [List services/modules]
- Data flow: [How data moves]
- Storage: [Database choices]

### API Contracts
- [Endpoint definitions]

### Data Model
- [Entity relationships]

### Failure Modes
- [What can go wrong + mitigations]
```

---

## Infrastructure

**Input**: Application to deploy, environment requirements  
**Output**: Deployed, monitored, scalable infrastructure  
**Success**: 99.9%+ uptime, <5min deploy, automated rollback

### Deployment Decision Tree

```
WHERE?
├─ Static site     → Vercel/Netlify/Cloudflare Pages
├─ Container app   → K8s/ECS/Cloud Run
├─ Serverless      → Lambda/Cloud Functions
├─ VM needed       → EC2/GCE/Droplet
└─ Edge compute    → Cloudflare Workers/Lambda@Edge

CI/CD?
├─ GitHub      → GitHub Actions
├─ GitLab      → GitLab CI
├─ Self-hosted → Jenkins/Drone
└─ Simple      → scripts/deploy.sh
```

### Docker (Always Use Multi-Stage)

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 app && adduser -u 1001 -G app -s /bin/sh -D app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
USER app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Kubernetes Essentials

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    spec:
      containers:
      - name: app
        image: app:v1.0.0  # NEVER use :latest
        resources:
          requests: { memory: "128Mi", cpu: "100m" }
          limits: { memory: "256Mi", cpu: "500m" }
        livenessProbe:
          httpGet: { path: /health, port: 8080 }
          initialDelaySeconds: 10
        readinessProbe:
          httpGet: { path: /ready, port: 8080 }
        securityContext:
          runAsNonRoot: true
          readOnlyRootFilesystem: true
```

---

## Security

**Input**: System to secure, compliance requirements  
**Output**: Hardened system, security report  
**Success**: Passes security scan, meets compliance

### Security Checklist (ALWAYS)

| Area | Requirements |
|------|-------------|
| **Auth** | OAuth2/OIDC, JWT <15min expiry, bcrypt cost≥12, rate limiting |
| **Input** | Validate ALL, parameterized queries, escape output, CSRF tokens |
| **Transport** | TLS 1.3, HSTS, cert pinning for mobile |
| **Secrets** | Env vars or secrets manager, NEVER in code/logs, rotate regularly |

### OWASP Top 10 Quick Reference

| Vulnerability | Prevention |
|---------------|------------|
| **Injection** | Parameterized queries, ORM |
| **Broken Auth** | MFA, session management |
| **Sensitive Data** | Encrypt at rest/transit |
| **XXE** | Disable external entities |
| **Broken Access** | RBAC, deny by default |
| **Misconfig** | Hardening, security headers |
| **XSS** | Output encoding, CSP |
| **Deserialization** | Don't deserialize untrusted |
| **Vulnerable Deps** | `npm audit`, Dependabot |
| **Logging** | Centralized, tamper-proof |

---

## Optimization

**Input**: Slow system, performance requirements  
**Output**: Optimized system with metrics  
**Success**: Meets latency/throughput targets

### Performance Decision Tree

```
WHERE IS IT SLOW?
├─ Frontend
│  ├─ Initial load → Bundle size, code splitting
│  ├─ Runtime → React profiler, memoization
│  └─ Network → Caching, CDN, compression
├─ API
│  ├─ Database → Query optimization, indexing
│  ├─ Compute → Algorithm, caching, async
│  └─ Network → Connection pooling, keep-alive
└─ Infrastructure
   ├─ CPU bound → Horizontal scaling, optimize code
   ├─ Memory bound → Reduce allocations, streaming
   └─ I/O bound → Async, batching, caching
```

### Caching Strategy

| Data Type | Cache | TTL |
|-----------|-------|-----|
| Static assets | CDN | 1 year (versioned) |
| API responses | Redis | 1-60 min |
| Session data | Redis | Session length |
| DB queries | Application | 1-5 min |

---

## Review Protocol

**Input**: Code to review (PR/MR link or diff)  
**Output**: Actionable feedback  
**Success**: Issues caught, knowledge shared

### Review Checklist

| Category | Check |
|----------|-------|
| **Correctness** | Does what it claims? Edge cases? Error handling? |
| **Security** | Input validated? Auth correct? Secrets exposed? |
| **Performance** | N+1 queries? Memory leaks? Unnecessary compute? |
| **Maintainability** | Clear naming? Tests? Docs updated? |

---

## Critical Rules

| ALWAYS | NEVER |
|--------|-------|
| Run linters before commit | Commit secrets to git |
| Write tests for new code | Use `eval()` or dynamic code |
| Use env vars for secrets | Trust user input |
| Log errors with context | Ignore security warnings |
| Handle all error paths | Deploy without testing |
| Use typed/strict mode | Use `SELECT *` on large tables |
| Pin dependency versions | Swallow exceptions silently |

---

## References

- `references/languages.md` - Language-specific patterns for 20+ languages
- `references/databases.md` - SQL/NoSQL design, optimization, migrations
- `references/cloud.md` - AWS/GCP/Azure architecture patterns
- `references/testing.md` - Test strategies, TDD, coverage
- `references/scale.md` - High-scale architecture patterns
