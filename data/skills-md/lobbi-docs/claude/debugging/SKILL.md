---
name: debugging
description: Debugging techniques for Python, JavaScript, and distributed systems. Activate for troubleshooting, error analysis, log investigation, and performance debugging. Includes extended thinking integration for complex debugging scenarios.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
related-skills:
  - extended-thinking
  - complex-reasoning
  - deep-analysis
---

# Debugging Skill

Provides comprehensive debugging capabilities with integrated extended thinking for complex scenarios.

## When to Use This Skill

Activate this skill when working with:
- Error troubleshooting
- Log analysis
- Performance debugging
- Distributed system debugging
- Memory and resource issues
- Complex, multi-layered bugs requiring deep reasoning

## Extended Thinking for Complex Debugging

### When to Enable Extended Thinking

Use extended thinking (Claude's deeper reasoning mode) for debugging when:

1. **Root Cause Unknown**: Multiple possible causes, unclear failure patterns
2. **Intermittent Issues**: Race conditions, timing issues, non-deterministic failures
3. **Multi-System Failures**: Distributed system bugs spanning multiple services
4. **Performance Mysteries**: Unexpected slowdowns without obvious bottlenecks
5. **Complex State Issues**: Bugs involving intricate state transitions or side effects
6. **Security Vulnerabilities**: Subtle security issues requiring careful analysis

### How to Activate Extended Thinking

```markdown
# In your debugging prompt
Claude, please use extended thinking to help debug this issue:

[Describe the problem with symptoms, context, and what you've tried]
```

Extended thinking will provide:
- Systematic hypothesis generation
- Multi-path investigation strategies
- Deeper pattern recognition
- Cross-domain insights (e.g., network + application + infrastructure)

## Hypothesis-Driven Debugging Framework

Use this structured approach for complex bugs:

### 1. Observation Phase
```
What happened?
- Error message/stack trace
- Frequency (always/intermittent)
- When it started
- Environmental context
- Recent changes
```

### 2. Hypothesis Generation
```
Generate 3-5 plausible hypotheses:

H1: [Most likely cause based on symptoms]
   Evidence for: [...]
   Evidence against: [...]
   Test: [How to validate/invalidate]

H2: [Alternative explanation]
   Evidence for: [...]
   Evidence against: [...]
   Test: [How to validate/invalidate]

H3: [Edge case or rare scenario]
   Evidence for: [...]
   Evidence against: [...]
   Test: [How to validate/invalidate]
```

### 3. Systematic Testing
```
Priority order (high to low confidence):
1. Test H1 → Result: [Pass/Fail/Inconclusive]
2. Test H2 → Result: [Pass/Fail/Inconclusive]
3. Test H3 → Result: [Pass/Fail/Inconclusive]

New evidence discovered:
- [Finding 1]
- [Finding 2]

Revised hypotheses if needed:
- [...]
```

### 4. Root Cause Identification
```
Confirmed root cause: [...]
Contributing factors: [...]
Why it wasn't caught earlier: [...]
```

### 5. Fix + Validation
```
Fix implemented: [...]
Tests added: [...]
Validation: [...]
Prevention: [...]
```

## Structured Debugging Templates

### Template 1: MECE Bug Analysis (Mutually Exclusive, Collectively Exhaustive)

```markdown
## Bug: [Title]

### Problem Statement
- **What**: [Precise description]
- **Where**: [System/component]
- **When**: [Conditions/triggers]
- **Impact**: [Severity/scope]

### MECE Hypothesis Tree

**Layer 1: System Boundaries**
- [ ] Frontend issue
- [ ] Backend API issue
- [ ] Database issue
- [ ] Infrastructure/network issue
- [ ] External dependency issue

**Layer 2: Component-Specific** (based on Layer 1 finding)
- [ ] [Sub-component A]
- [ ] [Sub-component B]
- [ ] [Sub-component C]

**Layer 3: Code-Level** (based on Layer 2 finding)
- [ ] Logic error
- [ ] State management
- [ ] Resource handling
- [ ] Configuration

### Investigation Log
| Time | Action | Result | Next Step |
|------|--------|--------|-----------|
| [HH:MM] | [What you tested] | [Finding] | [Decision] |

### Root Cause
[Final determination with evidence]

### Fix
[Solution with rationale]
```

### Template 2: 5 Whys Analysis

```markdown
## Issue: [Brief description]

**Symptom**: [Observable problem]

**Why 1**: Why did this happen?
→ [Answer]

**Why 2**: Why did [answer from Why 1] occur?
→ [Answer]

**Why 3**: Why did [answer from Why 2] occur?
→ [Answer]

**Why 4**: Why did [answer from Why 3] occur?
→ [Answer]

**Why 5**: Why did [answer from Why 4] occur?
→ [Root cause]

**Fix**: [Addresses root cause]
**Prevention**: [Process/check to prevent recurrence]
```

### Template 3: Timeline Reconstruction

```markdown
## Incident Timeline: [Event]

**Goal**: Reconstruct exact sequence leading to failure

| Time | Event | System State | Evidence |
|------|-------|--------------|----------|
| T-5min | [Normal operation] | [State] | [Logs] |
| T-2min | [Trigger event] | [State change] | [Logs/metrics] |
| T-30s | [Cascade starts] | [Degraded] | [Alerts] |
| T-0 | [Failure] | [Failed state] | [Error logs] |
| T+5min | [Recovery action] | [Recovering] | [Actions taken] |

**Critical Path**: [Sequence of events that led to failure]
**Alternative Scenarios**: [What could have prevented it at each step]
```

## Python Debugging Patterns

### Hypothesis-Driven Python Debugging Example

\`\`\`python
"""
Bug: API endpoint returns 500 error intermittently
Symptoms: 1 in 10 requests fail, always with same user IDs
Hypothesis: Race condition in user data caching
"""

# H1: Cache key collision between users
# Test: Add detailed logging around cache operations
import logging
logging.basicConfig(level=logging.DEBUG)

def get_user(user_id):
    cache_key = f"user:{user_id}"
    logging.debug(f"Fetching cache key: {cache_key} for user {user_id}")

    cached = cache.get(cache_key)
    if cached:
        logging.debug(f"Cache hit: {cache_key} -> {cached}")
        return cached

    user = db.query(User).filter_by(id=user_id).first()
    logging.debug(f"DB fetch for user {user_id}: {user}")

    cache.set(cache_key, user, timeout=300)
    logging.debug(f"Cache set: {cache_key} -> {user}")

    return user

# Result: Discovered cache_key had different format in different code paths
# Root cause: String formatting inconsistency (f"user:{id}" vs f"user_{id}")
\`\`\`

### Advanced Debugging with Context Managers

\`\`\`python
import time
from contextlib import contextmanager

@contextmanager
def debug_timer(operation_name):
    """Time operations and log if slow"""
    start = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        if duration > 1.0:  # Slow operation threshold
            logging.warning(
                f"{operation_name} took {duration:.2f}s",
                extra={'operation': operation_name, 'duration': duration}
            )

# Usage
with debug_timer("database_query"):
    results = db.query(User).filter(...).all()

@contextmanager
def hypothesis_test(hypothesis_name, expected_outcome):
    """Test and validate debugging hypotheses"""
    print(f"\n=== Testing: {hypothesis_name} ===")
    print(f"Expected: {expected_outcome}")
    start_state = capture_state()
    try:
        yield
    finally:
        end_state = capture_state()
        outcome = compare_states(start_state, end_state)
        print(f"Actual: {outcome}")
        print(f"Hypothesis {'CONFIRMED' if outcome == expected_outcome else 'REJECTED'}")

# Usage
with hypothesis_test(
    "H1: Database connection pool exhaustion",
    expected_outcome="pool_size increases during load"
):
    # Run load test
    for i in range(100):
        api_call()
\`\`\`

### pdb Debugger with Advanced Techniques

\`\`\`python
# Basic breakpoint
import pdb; pdb.set_trace()

# Python 3.7+
breakpoint()

# Conditional breakpoint
if user_id == 12345:
    breakpoint()

# Post-mortem debugging (debug after crash)
import pdb
try:
    risky_function()
except Exception:
    pdb.post_mortem()

# Common pdb commands
# n(ext)     - Execute next line
# s(tep)     - Step into function
# c(ontinue) - Continue execution
# p expr     - Print expression
# pp expr    - Pretty print
# l(ist)     - Show source code
# w(here)    - Show stack trace
# u(p)       - Move up stack frame
# d(own)     - Move down stack frame
# b(reak)    - Set breakpoint
# cl(ear)    - Clear breakpoint
# q(uit)     - Quit debugger

# Advanced: Programmatic debugging
import pdb
pdb.run('my_function()', globals(), locals())
\`\`\`

### Logging
\`\`\`python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
\`\`\`

### Exception Handling
\`\`\`python
import traceback

try:
    result = risky_operation()
except Exception as e:
    # Log full traceback
    logger.error(f"Operation failed: {e}")
    logger.error(traceback.format_exc())

    # Or get traceback as string
    tb = traceback.format_exception(type(e), e, e.__traceback__)
    error_details = ''.join(tb)
\`\`\`

## JavaScript/Node.js Debugging

### Hypothesis-Driven JavaScript Debugging Example

\`\`\`javascript
/**
 * Bug: Memory leak in websocket connections
 * Symptoms: Memory grows over time, eventually crashes
 * Hypothesis: Event listeners not cleaned up on disconnect
 */

// H1: Event listeners accumulating
// Test: Track listener counts
class WebSocketManager {
  constructor() {
    this.connections = new Map();
    this.debugListenerCounts = true;
  }

  addConnection(userId, socket) {
    console.debug(\`[H1 Test] Adding connection for user \${userId}\`);

    if (this.debugListenerCounts) {
      console.debug(\`[H1] Listener count before: \${socket.listenerCount('message')}\`);
    }

    socket.on('message', (data) => this.handleMessage(userId, data));
    socket.on('close', () => this.removeConnection(userId));

    if (this.debugListenerCounts) {
      console.debug(\`[H1] Listener count after: \${socket.listenerCount('message')}\`);
    }

    this.connections.set(userId, socket);
  }

  removeConnection(userId) {
    console.debug(\`[H1 Test] Removing connection for user \${userId}\`);

    const socket = this.connections.get(userId);
    if (socket) {
      const messageListenerCount = socket.listenerCount('message');
      console.debug(\`[H1] Listeners still attached: \${messageListenerCount}\`);

      // Result: Found 3+ listeners on same event!
      // Root cause: Not removing listeners on reconnect
      socket.removeAllListeners();
      this.connections.delete(userId);
    }
  }
}
\`\`\`

### Advanced Console Debugging

\`\`\`javascript
// Basic logging
console.log('Basic log');
console.error('Error message');
console.warn('Warning');

// Object inspection with depth
console.dir(object, { depth: null, colors: true });
console.table(array);

// Performance timing
console.time('operation');
// ... code ...
console.timeEnd('operation');

// Memory usage
console.memory; // Chrome only

// Stack trace
console.trace('Trace point');

// Grouping for organized logs
console.group('User Authentication Flow');
console.log('Step 1: Validate credentials');
console.log('Step 2: Generate token');
console.groupEnd();

// Conditional logging
const debug = (label, data) => {
  if (process.env.DEBUG) {
    console.log(\`[DEBUG] \${label}:\`, JSON.stringify(data, null, 2));
  }
};

// Hypothesis testing helper
function testHypothesis(name, test, expected) {
  console.group(\`Testing: \${name}\`);
  console.log(\`Expected: \${expected}\`);
  const actual = test();
  console.log(\`Actual: \${actual}\`);
  console.log(\`Result: \${actual === expected ? 'PASS' : 'FAIL'}\`);
  console.groupEnd();
  return actual === expected;
}

// Usage
testHypothesis(
  'H1: Cache returns stale data',
  () => cache.get('key').timestamp,
  Date.now()
);
\`\`\`

### Debugging Async/Promise Issues

\`\`\`javascript
// Track promise chains
const debugPromise = (label, promise) => {
  console.log(\`[\${label}] Started\`);
  return promise
    .then(result => {
      console.log(\`[\${label}] Resolved:\`, result);
      return result;
    })
    .catch(error => {
      console.error(\`[\${label}] Rejected:\`, error);
      throw error;
    });
};

// Usage
await debugPromise('DB Query', db.users.findOne({ id: 123 }));

// Debugging race conditions
async function debugRaceCondition() {
  const operations = [
    { name: 'Op1', fn: async () => { await delay(100); return 'A'; } },
    { name: 'Op2', fn: async () => { await delay(50); return 'B'; } },
    { name: 'Op3', fn: async () => { await delay(150); return 'C'; } }
  ];

  const results = await Promise.allSettled(
    operations.map(async op => {
      const start = Date.now();
      const result = await op.fn();
      const duration = Date.now() - start;
      console.log(\`\${op.name} completed in \${duration}ms: \${result}\`);
      return { op: op.name, result, duration };
    })
  );

  console.table(results.map(r => r.value));
}

// Debugging memory leaks with weak references
class DebugMemoryLeaks {
  constructor() {
    this.weakMap = new WeakMap();
    this.strongRefs = new Map();
  }

  trackObject(id, obj) {
    // Weak reference - will be GC'd if no other references
    this.weakMap.set(obj, { id, created: Date.now() });

    // Strong reference - prevents GC (potential leak source)
    this.strongRefs.set(id, obj);

    console.log(\`Tracking \${id}: Strong refs=\${this.strongRefs.size}\`);
  }

  release(id) {
    this.strongRefs.delete(id);
    console.log(\`Released \${id}: Strong refs=\${this.strongRefs.size}\`);
  }

  checkLeaks() {
    console.log(\`Potential leaks: \${this.strongRefs.size} strong references\`);
    return Array.from(this.strongRefs.keys());
  }
}
\`\`\`

### Node.js Inspector
\`\`\`bash
# Start with inspector
node --inspect app.js
node --inspect-brk app.js  # Break on first line

# Debug with Chrome DevTools
# Open chrome://inspect
\`\`\`

### VS Code Debug Configuration
\`\`\`json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Agent",
      "program": "${workspaceFolder}/src/index.js",
      "env": {
        "NODE_ENV": "development"
      }
    }
  ]
}
\`\`\`

## Container Debugging

### Docker
\`\`\`bash
# View logs
docker logs <container> --tail=100 -f

# Execute shell
docker exec -it <container> /bin/sh

# Inspect container
docker inspect <container>

# Resource usage
docker stats <container>

# Debug running container
docker run -it --rm \
  --network=container:<target> \
  nicolaka/netshoot
\`\`\`

### Kubernetes
\`\`\`bash
# Pod logs
kubectl logs <pod> -n agents -f
kubectl logs <pod> -n agents --previous  # Previous crash

# Execute in pod
kubectl exec -it <pod> -n agents -- /bin/sh

# Debug with ephemeral container
kubectl debug <pod> -n agents -it --image=busybox

# Port forward for local debugging
kubectl port-forward <pod> 8080:8080 -n agents

# Events
kubectl get events -n agents --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods -n agents
\`\`\`

## Log Analysis

### Pattern Matching
\`\`\`bash
# Search logs for errors
grep -i "error\|exception\|failed" app.log

# Count occurrences
grep -c "ERROR" app.log

# Context around matches
grep -B 5 -A 5 "OutOfMemory" app.log

# Filter by time range
awk '/2024-01-15 10:00/,/2024-01-15 11:00/' app.log
\`\`\`

### JSON Logs
\`\`\`bash
# Parse JSON logs with jq
cat app.log | jq 'select(.level == "error")'
cat app.log | jq 'select(.timestamp > "2024-01-15T10:00:00")'

# Extract specific fields
cat app.log | jq -r '[.timestamp, .level, .message] | @tsv'
\`\`\`

## Performance Debugging

### Python Profiling
\`\`\`python
# cProfile
import cProfile
cProfile.run('main()', 'output.prof')

# Line profiler
@profile
def slow_function():
    pass

# Memory profiler
from memory_profiler import profile

@profile
def memory_heavy():
    pass
\`\`\`

### Network Debugging
\`\`\`bash
# Check connectivity
ping <host>
telnet <host> <port>
nc -zv <host> <port>

# DNS resolution
nslookup <host>
dig <host>

# HTTP debugging
curl -v http://localhost:8080/health
curl -X POST -d '{"test": true}' -H "Content-Type: application/json" http://localhost:8080/api
\`\`\`

## Common Debug Checklist

1. **Check Logs**: Application, system, container logs
2. **Verify Configuration**: Environment variables, config files
3. **Test Connectivity**: Network, database, external services
4. **Check Resources**: CPU, memory, disk space
5. **Review Recent Changes**: Git log, deployment history
6. **Reproduce Locally**: Same environment, same data
7. **Binary Search**: Isolate the problem scope

## Debugging Decision Tree

Use this decision tree to determine the right debugging approach:

```
START: What kind of bug?
│
├─ Known error message/stack trace
│  └─ Use: Direct log analysis + Stack trace walkthrough
│
├─ Intermittent/Race condition
│  └─ Use: Extended thinking + Timeline reconstruction + Hypothesis-driven
│
├─ Performance degradation
│  └─ Use: Profiling + Hypothesis-driven + MECE analysis
│
├─ Distributed system failure
│  └─ Use: Extended thinking + Timeline reconstruction + Multi-system tracing
│
├─ Complex state bug
│  └─ Use: Extended thinking + Hypothesis-driven + pdb/debugger
│
├─ Memory leak
│  └─ Use: Memory profiling + Hypothesis-driven + Weak reference analysis
│
└─ Unknown root cause
   └─ Use: Extended thinking + MECE analysis + 5 Whys
```

## Best Practices for Complex Debugging

### 1. Document Your Investigation

Always maintain a debugging log:

```markdown
## Bug Investigation: [Title]
**Start Time**: 2024-01-15 10:00
**Investigator**: [Name]

### Timeline
- 10:00 - Started investigation, checked logs
- 10:15 - Found error pattern in auth service
- 10:30 - Hypothesis: Cache expiration race condition
- 10:45 - Added debug logging, confirmed hypothesis
- 11:00 - Implemented fix, testing

### Hypotheses Tested
- [x] H1: Cache race condition (CONFIRMED)
- [ ] H2: Database connection pool (REJECTED)
- [ ] H3: Network timeout (NOT TESTED)

### Root Cause
[Final determination]

### Fix Applied
[Solution details]

### Prevention
[How to prevent recurrence]
```

### 2. Use the Scientific Method

1. **Observe**: Gather symptoms, error messages, logs
2. **Hypothesize**: Generate 3-5 plausible explanations
3. **Predict**: What would you see if hypothesis is true?
4. **Test**: Design experiments to validate/invalidate
5. **Analyze**: Compare predictions vs actual results
6. **Conclude**: Confirm root cause with evidence

### 3. Leverage Extended Thinking

When to activate extended thinking:
- **Complexity threshold**: More than 3 interacting systems
- **Uncertainty high**: Multiple equally plausible causes
- **Stakes high**: Production outage, security issue, data loss
- **Pattern unclear**: No obvious error messages or logs
- **Time-sensitive**: Need systematic approach under pressure

### 4. Avoid Common Pitfalls

```markdown
AVOID:
- ❌ Changing multiple things at once (can't isolate cause)
- ❌ Assuming first hypothesis is correct (confirmation bias)
- ❌ Debugging without logs/evidence (guessing)
- ❌ Not documenting what you tried (repeating failed attempts)
- ❌ Skipping reproduction step (fix might not work)

DO:
- ✅ Change one variable at a time
- ✅ Test multiple hypotheses systematically
- ✅ Add instrumentation before debugging
- ✅ Keep investigation log
- ✅ Write regression test after fix
```

### 5. Debugging Instrumentation Patterns

```python
# Python: Comprehensive debugging decorator
import functools
import time
import logging

def debug_trace(func):
    """Decorator to trace function execution with timing and state"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__qualname__
        logger.debug(f"→ Entering {func_name}")
        logger.debug(f"  Args: {args}")
        logger.debug(f"  Kwargs: {kwargs}")

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            logger.debug(f"← Exiting {func_name} ({duration:.3f}s)")
            logger.debug(f"  Result: {result}")
            return result
        except Exception as e:
            duration = time.perf_counter() - start
            logger.error(f"✗ Exception in {func_name} ({duration:.3f}s): {e}")
            raise

    return wrapper

# Usage
@debug_trace
def complex_operation(user_id, data):
    # Your code here
    pass
```

```javascript
// JavaScript: Comprehensive debugging wrapper
function debugTrace(label) {
  return function(target, propertyKey, descriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function(...args) {
      console.log(\`→ Entering \${label || propertyKey}\`);
      console.log(\`  Args:\`, args);

      const start = performance.now();
      try {
        const result = await originalMethod.apply(this, args);
        const duration = performance.now() - start;
        console.log(\`← Exiting \${label || propertyKey} (\${duration.toFixed(2)}ms)\`);
        console.log(\`  Result:\`, result);
        return result;
      } catch (error) {
        const duration = performance.now() - start;
        console.error(\`✗ Exception in \${label || propertyKey} (\${duration.toFixed(2)}ms):\`, error);
        throw error;
      }
    };

    return descriptor;
  };
}

// Usage
class UserService {
  @debugTrace('UserService.getUser')
  async getUser(userId) {
    // Your code here
  }
}
```

## Cross-References and Related Skills

### Related Skills

This debugging skill integrates with:

1. **extended-thinking** (`.claude/skills/extended-thinking/SKILL.md`)
   - Use for: Complex bugs with unknown root causes
   - Activation: Add "use extended thinking" to your debugging prompt
   - Benefit: Deeper pattern recognition, systematic hypothesis generation

2. **complex-reasoning** (`.claude/skills/complex-reasoning/SKILL.md`)
   - Use for: Multi-step debugging requiring logical chains
   - Patterns: Chain-of-thought, tree-of-thought for bug investigation
   - Benefit: Structured reasoning through complex bug scenarios

3. **deep-analysis** (`.claude/skills/deep-analysis/SKILL.md`)
   - Use for: Post-mortem analysis, root cause investigation
   - Patterns: Comprehensive code review, architectural analysis
   - Benefit: Identifies systemic issues beyond surface bugs

4. **testing** (`.claude/skills/testing/SKILL.md`)
   - Use for: Writing regression tests after bug fix
   - Integration: Bug → Debug → Fix → Test → Validate
   - Benefit: Ensures bug doesn't recur

5. **kubernetes** (`.claude/skills/kubernetes/SKILL.md`)
   - Use for: Distributed system debugging in K8s
   - Tools: kubectl logs, exec, debug, events
   - Integration: Container debugging patterns

### When to Combine Skills

| Scenario | Skills to Combine | Reasoning |
|----------|------------------|-----------|
| Production outage | debugging + extended-thinking + kubernetes | Complex distributed system requires deep reasoning |
| Intermittent test failure | debugging + testing + complex-reasoning | Need systematic hypothesis testing |
| Performance regression | debugging + deep-analysis | Root cause may be architectural |
| Security vulnerability | debugging + extended-thinking + deep-analysis | Requires careful, thorough analysis |
| Memory leak | debugging + complex-reasoning | Multi-step investigation needed |

### Integration Examples

#### Example 1: Complex Production Bug

```bash
# Prompt combining skills
Claude, I have a complex production bug affecting multiple services.
Please use extended thinking and the debugging skill to help investigate.

Symptoms:
- API requests timeout intermittently (1 in 50 requests)
- Only affects authenticated users
- Started after recent deployment
- No obvious errors in logs

Please use:
1. MECE analysis to categorize possible causes
2. Hypothesis-driven debugging framework
3. Timeline reconstruction of recent changes
```

#### Example 2: Memory Leak Investigation

```bash
# Prompt combining skills
Claude, use complex reasoning and debugging skills to investigate a memory leak.

Context:
- Node.js service memory grows from 200MB to 2GB over 6 hours
- No errors logged
- Happens only in production, not staging

Apply:
1. Hypothesis-driven framework (generate 5 hypotheses)
2. Memory leak detection patterns (weak references)
3. Extended thinking for pattern recognition across codebase
```

## Quick Reference Card

### Debugging Workflow Summary

```
1. OBSERVE
   - Collect error messages, logs, metrics
   - Identify patterns (frequency, conditions, scope)
   - Document symptoms

2. HYPOTHESIZE (use extended thinking if complex)
   - Generate 3-5 plausible hypotheses
   - Rank by likelihood
   - Design tests for each

3. TEST
   - Change one variable at a time
   - Add instrumentation (logging, tracing)
   - Collect evidence

4. ANALYZE
   - Compare predictions vs results
   - Eliminate invalidated hypotheses
   - Refine remaining hypotheses

5. FIX
   - Implement solution
   - Add regression test
   - Document root cause

6. VALIDATE
   - Verify fix in affected environment
   - Monitor metrics
   - Update documentation
```

### Tool Selection Guide

| Problem Type | Primary Tool | Secondary Tools |
|--------------|-------------|-----------------|
| Logic error | pdb/debugger | Logging, unit tests |
| Performance | Profiler | Hypothesis testing, metrics |
| Memory leak | Memory profiler | Weak references, heap dumps |
| Async/timing | Timeline reconstruction | Extended thinking, logging |
| Distributed | Tracing (logs) | Kubernetes tools, MECE analysis |
| Unknown cause | Extended thinking | MECE, 5 Whys, hypothesis-driven |

---

**Skill version**: 2.0 (Enhanced with extended thinking integration)
**Last updated**: 2024-01-15
**Maintained by**: Golden Armada AI Agent Fleet
