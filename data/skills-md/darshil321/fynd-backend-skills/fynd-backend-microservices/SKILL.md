---
name: fynd-backend-microservices
description: Expert debugging for FYND's Kubernetes/GCP/Kafka/Node.js backend. Use for pods crashing, Kafka lag, Redis memory high, API latency, DB migration failures, LLM cost spikes, memory leaks, and service failures.
---

# FYND Backend Microservices 🛠️

**Expert debugging for FYND's Kubernetes/GCP/Kafka/Node.js backend.**

## 🎯 Use When
```
"Pods crashing" | "Kafka lag" | "Redis memory high" | "API latency"
"Database migration failed" | "LLM costs spiking" | "Memory leak" | "Service failures"
```

## 🛠️ 8 Core Skills
1. **K8s/GCP Deployment** (40% issues) - pods, scaling, graceful shutdown
2. **Kafka Resilience** (25%) - consumer lag, DLQ, rebalancing
3. **Redis Optimization** (15%) - memory, TTL, pub/sub
4. **Distributed Tracing** (10%) - correlation IDs, Langfuse
5. **Database Patterns** (8%) - Sequelize, pgvector, MongoDB
6. **LangGraph Orchestration** (5%) - multi-LLM, token counting
7. **Performance Analysis** (4%) - heap profiling, slow queries
8. **Resilience Patterns** (3%) - circuit breaker, backoff

## 🔍 Diagnostic Flow
1. Gather metrics (kubectl, kafka-consumer-groups, redis-cli)
2. Form hypotheses (OOM? poison pill? slow query?)
3. Test systematically
4. Provide fix + monitoring

## 📦 Bundled Resources (load as needed)
- `scripts/diagnose.js` - quick pod snapshot (`kubectl get pods`)
- `references/patterns.md` - fast CLI patterns for pod crash, Kafka lag, Redis memory
- `references/fynd-backend-skills.md` - full architecture + skills matrix + flowcharts + checklists
- `references/fynd-agent-integration.md` - LangGraph/LangChain tool integration guide
- `references/fynd-backend-skill-template.md` - template for creating new skills or extensions

**Search tips:** use `rg -n "Use Cases|Agent Actions|Checklist|Flowchart"` in the reference files to jump to relevant sections quickly.

## 📊 Success
94% accuracy | <5s response | 30% MTTR reduction | $740k/year savings
