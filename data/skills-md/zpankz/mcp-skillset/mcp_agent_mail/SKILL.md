---
name: mcp_agent_mail
description: FastMCP agent-to-agent communication system with messaging, file reservations, and multi-repo coordination
version: 1.0.0
triggers:
  - multi-agent tasks
  - parallel development
  - file coordination
  - agent collaboration
  - distributed work
  - code conflicts
  - team coordination
  - cross-repository
keywords:
  - agent communication
  - file locking
  - coordination
  - messaging
  - reservations
  - collaboration
  - multi-agent
server_type: fastmcp
server_port: 9743
dependencies:
  - sqlite3
  - git
related_skills:
  - task_orchestration
  - project_management
  - code_review
---

# MCP Agent Mail Skill

> **"Use mcp_agent_mail for ANY multi-agent coordination"**

FastMCP-based communication system enabling conflict-free collaboration between AI agents through structured messaging, advisory file locks, and cross-repository event coordination.

---

## Core Principle

**When multiple agents work on the same codebase, explicit coordination prevents:**
- Edit conflicts and merge disasters
- Duplicated work on same features
- Communication breakdowns
- Lost context during handoffs
- Race conditions on shared files

**Agent Mail transforms implicit coordination into explicit, traceable protocols.**

---

## When to Use This Skill

### Required Scenarios

Use mcp_agent_mail **always** when:

1. **Multiple Agents on Same Codebase**
   - Two or more agents editing project simultaneously
   - Parallel feature development
   - Concurrent bug fixes
   - Distributed refactoring

2. **File Conflict Risk**
   - Modifying shared configuration files
   - Editing core modules used by multiple features
   - Database migrations
   - API contract changes

3. **Task Dependencies**
   - Agent B needs Agent A's output
   - Sequential workflow steps (design → implement → test)
   - Work handoffs between agents
   - Integration of parallel work streams

4. **Cross-Repository Coordination**
   - Microservices that depend on each other
   - Monorepo multi-package changes
   - Deployment orchestration
   - Breaking changes affecting multiple services

### Recommended Scenarios

Use mcp_agent_mail for:
- Knowledge sharing between agents
- Architecture decision discussions
- Code review coordination
- Progress tracking on long-running tasks
- Emergency hotfix coordination

---

## Key Capabilities

### 1. Agent Registration & Discovery

**Register agent identity:**
```typescript
await tools.agent_mail.registerAgent({
  agent: {
    id: "claude-architect-1",
    name: "Claude Architect",
    role: "architect",
    capabilities: ["system-design", "typescript", "python"],
    contactPolicy: {
      acceptsDirectMessages: true,
      acceptsBroadcasts: true,
      priority: ["urgent", "high", "normal"],
      autoRespond: true
    },
    status: "active"
  }
});
```

**Query available agents:**
```bash
# Find all active implementers
agent-mail agents list --role implementer --status active

# Find agents with specific capability
agent-mail agents search --capability "react"
```

### 2. Structured Messaging

#### Direct Messages (Agent-to-Agent)
```typescript
await tools.agent_mail.sendMessage({
  from: "agent-architect",
  to: "agent-implementer",
  subject: "Task Assignment: User Authentication Module",
  body: {
    text: `Please implement OAuth2 authentication.

    Requirements:
    - Support Google and GitHub providers
    - Implement token refresh
    - Add integration tests

    Documentation: /docs/auth-spec.md
    Deadline: Friday EOD`,
    files: ["/docs/auth-spec.md", "/src/auth/types.ts"]
  },
  priority: "high",
  type: "task"
});
```

#### Broadcast Messages (One-to-Many)
```typescript
await tools.agent_mail.sendMessage({
  from: "coordinator",
  to: "broadcast",
  subject: "Code Freeze for Hotfix",
  body: {
    text: "Production incident. All agents please stop non-critical work and release file reservations."
  },
  priority: "urgent",
  type: "notification"
});
```

#### Threaded Conversations
```typescript
// Start thread
const thread = await tools.agent_mail.createThread({
  subject: "Database Migration Strategy",
  participants: ["agent-a", "agent-b", "agent-dba"]
});

// Reply in thread
await tools.agent_mail.replyToThread({
  threadId: thread.id,
  body: { text: "I propose using Flyway for migrations." }
});
```

### 3. File Reservation System

**Key Concept:** Advisory locks prevent edit conflicts through voluntary coordination.

#### Reserve File (Exclusive)
```typescript
// Reserve for editing
const reservation = await tools.agent_mail.reserveFile({
  agentId: "agent-a",
  path: "/src/auth/login.ts",
  purpose: "refactor",
  mode: "exclusive",  // Only I can access
  expiresIn: 3600,   // Auto-release after 1 hour
  metadata: {
    notes: "Extracting login logic to separate module"
  }
});

// Do work...
await modifyFile("/src/auth/login.ts");

// Release immediately after work
await tools.agent_mail.releaseReservation({
  reservationId: reservation.id
});
```

#### Reserve File (Shared)
```typescript
// Multiple agents can read, none can write
await tools.agent_mail.reserveFile({
  agentId: "agent-analyzer",
  path: "/src/complex-module.ts",
  purpose: "read",
  mode: "shared",  // Allow other readers
  expiresIn: 1800
});
```

#### Check Before Reserving
```typescript
// Always check first!
const existing = await tools.agent_mail.checkReservation({
  path: "/src/auth/login.ts"
});

if (existing.status === "active") {
  // File reserved by another agent
  await tools.agent_mail.sendMessage({
    to: existing.agentId,
    subject: "Request access to login.ts",
    body: { text: "Can we coordinate? I need to modify this file." }
  });
} else {
  // Free to reserve
  await tools.agent_mail.reserveFile({...});
}
```

### 4. Product Bus (Multi-Repo Events)

**Coordinate across repositories:**

```typescript
// Emit deployment event
await tools.agent_mail.emitEvent({
  productId: "user-service",
  event: "deployment",
  payload: {
    version: "2.3.1",
    environment: "production",
    timestamp: new Date().toISOString()
  }
});

// Subscribe to events from other services
await tools.agent_mail.subscribeToEvents({
  productId: "api-gateway",
  events: ["breaking_change", "deployment"]
});

// Receive notification when dependency changes
// → Automatically triggered when subscribed event occurs
```

---

## Common Workflows

### Workflow 1: Task Assignment

```
Coordinator                     Implementer
    │                               │
    │ 1. Send task message          │
    │──────────────────────────────>│
    │                               │
    │ 2. Acknowledge receipt        │
    │<──────────────────────────────│
    │                               │
    │                   3. Reserve files
    │                    4. Do work
    │                               │
    │ 5. Send completion update     │
    │<──────────────────────────────│
    │                               │
    │                  6. Release files
```

**Code:**
```typescript
// Step 1: Coordinator sends task
await tools.agent_mail.sendMessage({
  from: "coordinator",
  to: "implementer",
  subject: "Task: Implement Feature X",
  type: "task",
  body: { text: "See spec: /docs/feature-x.md" }
});

// Step 2: Implementer acknowledges
await tools.agent_mail.replyToMessage({
  messageId: "msg-123",
  body: { text: "Acknowledged. Starting now. ETA: 2 days." }
});

// Step 3: Reserve files
await tools.agent_mail.reserveFile({
  agentId: "implementer",
  path: "/src/feature-x/",
  purpose: "create",
  mode: "exclusive"
});

// Step 4: Do work
await implementFeature();

// Step 5: Notify completion
await tools.agent_mail.sendMessage({
  to: "coordinator",
  subject: "Task Complete: Feature X",
  type: "update",
  body: { text: "Feature X implemented. PR #456 ready for review." }
});

// Step 6: Release files
await tools.agent_mail.releaseReservation({ reservationId });
```

### Workflow 2: Parallel Development

```
Coordinator
    │
    ├─> Agent A: Frontend (no conflicts)
    └─> Agent B: Backend (no conflicts)

    Agents coordinate via messages
    Files reserved to prevent overlap
```

**Code:**
```typescript
// Coordinator broadcasts work distribution
await tools.agent_mail.sendMessage({
  from: "coordinator",
  to: "broadcast",
  subject: "Work Distribution: Feature Y",
  body: {
    text: `
    Agent A: Frontend UI (/src/ui/)
    Agent B: Backend API (/src/api/)
    Coordinate via thread "feature-y-dev"
    `
  }
});

// Each agent reserves their domain
await tools.agent_mail.reserveFile({
  agentId: "agent-a",
  path: "/src/ui/",
  purpose: "create",
  mode: "exclusive"
});

await tools.agent_mail.reserveFile({
  agentId: "agent-b",
  path: "/src/api/",
  purpose: "create",
  mode: "exclusive"
});

// Agents work in parallel without conflicts
```

### Workflow 3: Emergency Hotfix

```
1. Emergency broadcast → All agents stop
2. Release all reservations
3. Hotfix agent reserves critical files
4. Apply fix
5. All-clear broadcast → Resume work
```

**Code:**
```typescript
// Step 1: Emergency broadcast
await tools.agent_mail.sendMessage({
  to: "broadcast",
  subject: "🚨 EMERGENCY: Production Down",
  priority: "urgent",
  body: { text: "All agents: Stop work. Release reservations." }
});

// Step 2: All agents release
await tools.agent_mail.releaseAllReservations({
  agentId: myAgentId
});

// Step 3: Hotfix agent reserves
await tools.agent_mail.reserveFile({
  agentId: "hotfix-agent",
  path: "/src/critical-module.ts",
  purpose: "edit",
  mode: "exclusive"
});

// Step 4: Apply fix
await applyHotfix();

// Step 5: All-clear
await tools.agent_mail.sendMessage({
  to: "broadcast",
  subject: "✓ RESOLVED: Production Restored",
  priority: "high",
  body: { text: "Resume normal operations. Code freeze lifted." }
});
```

---

## Message Priority Levels

| Priority | Response Time | Use Case |
|----------|--------------|----------|
| **urgent** | < 5 min | Production incident, critical blocker |
| **high** | < 1 hour | Important bug, pending release |
| **normal** | Same day | Standard requests, questions |
| **low** | Best effort | FYI updates, optional improvements |

---

## Reservation Modes Explained

### Exclusive Mode
```typescript
{ mode: "exclusive" }
```
- **Only reserving agent** can access file
- Prevents both reads and writes by others
- Use for: editing, refactoring, deleting

### Shared Mode
```typescript
{ mode: "shared" }
```
- **Multiple agents** can reserve for reading
- **No agent** can write
- Use for: analysis, research, non-destructive operations

---

## Integration Patterns

### Pattern 1: Check-Reserve-Work-Release

**Always follow this sequence:**

```typescript
try {
  // 1. Check
  const existing = await tools.agent_mail.checkReservation({ path });
  if (existing.status === "active") {
    // Coordinate with owner
    return;
  }

  // 2. Reserve
  const reservation = await tools.agent_mail.reserveFile({
    agentId: myId,
    path,
    purpose: "edit",
    mode: "exclusive"
  });

  // 3. Work
  await doWork(path);

} finally {
  // 4. Release (always in finally block)
  await tools.agent_mail.releaseReservation({ reservationId });
}
```

### Pattern 2: Announce-Reserve-Execute

**For major work, announce intent first:**

```typescript
// 1. Announce
await tools.agent_mail.sendMessage({
  to: "broadcast",
  subject: "Planning auth refactor tomorrow",
  body: { text: "Will refactor /src/auth/ starting 9am." }
});

// Wait for objections...

// 2. Reserve
await tools.agent_mail.reserveFile({
  path: "/src/auth/",
  purpose: "refactor"
});

// 3. Execute
await refactorAuth();

// 4. Notify completion
await tools.agent_mail.sendMessage({
  to: "broadcast",
  subject: "Auth refactor complete",
  body: { text: "Changes pushed to main. Files released." }
});
```

### Pattern 3: Request-Acknowledge-Complete (RAC)

**Standard protocol for task assignment:**

```typescript
// Request
await sendMessage({ type: "task", subject: "Implement X" });

// Acknowledge (by receiver)
await replyToMessage({ body: { text: "Acknowledged. ETA: 2 days" } });

// Complete (by receiver)
await sendMessage({ type: "update", subject: "Task Complete" });
```

---

## Anti-Patterns to Avoid

### ❌ Silent Work
```typescript
// WRONG: Start editing without coordination
await modifyFile("/src/shared-module.ts");
// → Another agent modifies same file → conflict
```

```typescript
// RIGHT: Coordinate first
await tools.agent_mail.reserveFile({
  path: "/src/shared-module.ts",
  purpose: "edit"
});
await modifyFile("/src/shared-module.ts");
```

### ❌ Reservation Hoarding
```typescript
// WRONG: Reserve everything "just in case"
await reserveFile({ path: "/src/" }); // Entire directory
// → Blocks all other agents unnecessarily
```

```typescript
// RIGHT: Reserve only what you'll modify
await reserveFile({ path: "/src/specific-file.ts" });
```

### ❌ Ignoring Reservations
```typescript
// WRONG: Modify without checking
await modifyFile(path);
```

```typescript
// RIGHT: Always check first
const reservation = await checkReservation({ path });
if (reservation.status === "active") {
  await coordinateWithOwner(reservation.agentId);
}
```

### ❌ Forgetting to Release
```typescript
// WRONG: No cleanup
await reserveFile({ path });
await doWork(path);
// → File locked indefinitely
```

```typescript
// RIGHT: Always release
try {
  await reserveFile({ path });
  await doWork(path);
} finally {
  await releaseReservation({ reservationId });
}
```

---

## Best Practices

### Communication
1. ✅ **Check agent status** before sending urgent messages
2. ✅ **Use appropriate priorities** - don't overuse "urgent"
3. ✅ **Provide context** - include file paths, PRs, rationale
4. ✅ **Keep threads focused** - one topic per thread
5. ✅ **Archive resolved threads** - maintain clean history

### File Reservations
1. ✅ **Check before reserving** - verify file is available
2. ✅ **Reserve minimally** - only lock what you'll modify
3. ✅ **Set expiry times** - prevent indefinite locks
4. ✅ **Release promptly** - free files immediately after work
5. ✅ **Use shared mode** for read-only access

### Coordination
1. ✅ **Announce intent** before starting major work
2. ✅ **Update progress** on long-running tasks
3. ✅ **Handoff clearly** when transferring work
4. ✅ **Document decisions** in message threads
5. ✅ **Acknowledge receipts** to confirm understanding

---

## Quick Command Reference

```bash
# Agent registration
agent-mail agents register --id <id> --role <role>
agent-mail agents status --id <id>
agent-mail agents list --role <role> --status active

# Messaging
agent-mail send --to <agent-id> --subject "..." --body "..."
agent-mail broadcast --subject "..." --priority urgent
agent-mail threads list --status active
agent-mail messages read --thread <id>

# Reservations
agent-mail reserve <path> --purpose edit --mode exclusive
agent-mail check <path>
agent-mail release <reservation-id>
agent-mail reservations list --agent <id>

# Product Bus
agent-mail events emit --product <id> --event deployment
agent-mail events subscribe --product <id> --events build_failure
```

---

## Troubleshooting

### Problem: Message not received

**Check:**
```typescript
// 1. Recipient's contact policy
const agent = await tools.agent_mail.getAgent({ id: recipientId });
console.log(agent.contactPolicy);

// 2. Recipient's status
console.log(agent.status); // offline?

// 3. Priority filters
// Some agents filter out low-priority messages

// 4. Server connectivity
await tools.agent_mail.ping();
```

### Problem: Reservation conflict

**Resolution:**
```typescript
// 1. Check existing reservation
const reservation = await tools.agent_mail.checkReservation({ path });

// 2. Contact owner
await tools.agent_mail.sendMessage({
  to: reservation.agentId,
  subject: "Request access to file",
  body: { text: "Can we coordinate?" }
});

// 3. Or escalate to coordinator
await tools.agent_mail.sendMessage({
  to: "coordinator",
  priority: "high",
  subject: "Reservation conflict",
  body: { text: "Need resolution for file access." }
});
```

### Problem: Stale reservations

**Prevention:**
```typescript
// Always set expiry times
await tools.agent_mail.reserveFile({
  path,
  expiresIn: 3600, // 1 hour
  // Auto-releases if agent crashes or forgets
});

// Cleanup orphaned reservations
await tools.agent_mail.auditReservations({
  status: "stale"
});
```

---

## Configuration

### Server Setup

```bash
# Start Agent Mail server
agent-mail server start --port 9743

# Check server status
agent-mail server status
agent-mail server health
```

### Client Configuration

```typescript
// In MCP config
{
  "mcpServers": {
    "agent-mail": {
      "command": "agent-mail",
      "args": ["serve"],
      "env": {
        "AGENT_MAIL_DB_PATH": "~/.agent-mail/data.db",
        "AGENT_MAIL_ARCHIVE_PATH": "~/.agent-mail/archive/"
      }
    }
  }
}
```

---

## Related Resources

### Documentation
- **[Codebase README](../mcp_agent_mail-codebase/README.md)** - Architecture overview
- **[Agent Coordination Principles](../mcp_agent_mail-codebase/principles/agent-coordination.md)** - Communication patterns
- **[File Reservations Protocol](../mcp_agent_mail-codebase/principles/file-reservations.md)** - Conflict prevention
- **[Coordination Workflows](../mcp_agent_mail-codebase/templates/coordination-workflow.md)** - Copy-paste templates

### Quick References
- **[Cheatsheet](assets/cheatsheet.md)** - Command quick reference
- **[Messaging Patterns](references/messaging-patterns.md)** - Common message types
- **[Reservation Protocol](references/reservation-protocol.md)** - File locking patterns

### Scripts
- **[Server Health Check](scripts/server-health.sh)** - Verify server status
- **[Reservation Audit](scripts/audit-reservations.sh)** - Find stale locks
- **[Message Statistics](scripts/message-stats.sh)** - Communication metrics

---

## Success Metrics

Track these to measure coordination effectiveness:

- **Response Time** - How quickly agents acknowledge messages
- **Conflict Rate** - How often reservation conflicts occur
- **Reservation Duration** - Average file lock time
- **Thread Resolution Time** - How long discussions take
- **Message Read Rate** - % of messages acknowledged

**Healthy System:**
- Response time: < 5 minutes (urgent), < 1 hour (high)
- Conflict rate: < 5% of reservation attempts
- Reservation duration: < 30 minutes average
- Thread resolution: < 24 hours
- Read rate: > 95% within 1 hour

---

## Summary

**Use mcp_agent_mail when:**
- Multiple agents on same codebase
- Risk of file editing conflicts
- Task dependencies between agents
- Cross-repository coordination needed

**Key operations:**
- `registerAgent()` - Establish identity
- `sendMessage()` - Communicate intent
- `reserveFile()` - Lock before editing
- `releaseReservation()` - Unlock after work

**Remember:** Explicit coordination prevents implicit chaos. When in doubt, communicate!
