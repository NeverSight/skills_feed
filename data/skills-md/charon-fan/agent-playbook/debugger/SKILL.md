---
name: debugger
description: Advanced debugging specialist for diagnosing and resolving code issues. Use when user encounters bugs, errors, unexpected behavior, or mentions debugging.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  hooks:
    after_complete:
      - trigger: self-improving-agent
        mode: background
        reason: "Learn from debugging patterns"
      - trigger: session-logger
        mode: auto
        reason: "Log debugging session"
---

# Debugger

An advanced debugging specialist that helps diagnose and resolve code issues systematically.

## When This Skill Activates

Activates when you:
- Report an error or bug
- Mention "debug this" or "help debug"
- Describe unexpected behavior
- Ask why something isn't working

## Debugging Process

### Phase 1: Understand the Problem

1. **Reproduce the issue**
   - What are the exact steps to reproduce?
   - What is the expected behavior?
   - What is the actual behavior?
   - What error messages appear?

2. **Gather context**
   ```bash
   # Check recent changes
   git log --oneline -10

   # Check error logs
   tail -f logs/error.log

   # Check environment
   env | grep -i debug
   ```

### Phase 2: Isolate the Issue

1. **Locate the error source**
   - Stack trace analysis
   - Error code lookup
   - Log correlation

2. **Narrow down scope**
   - Binary search (comment out half)
   - Minimize reproduction case
   - Identify affected components

### Phase 3: Analyze the Root Cause

#### Common Error Categories

| Category | Symptoms | Investigation Steps |
|----------|----------|---------------------|
| **Null/Undefined** | "Cannot read X of undefined" | Trace the variable origin |
| **Type Errors** | "X is not a function" | Check actual vs expected type |
| **Async Issues** | Race conditions, timing | Check promise handling, async/await |
| **State Issues** | Stale data, wrong state | Trace state mutations |
| **Network** | Timeouts, connection refused | Check endpoints, CORS, auth |
| **Environment** | Works locally, not in prod | Compare env vars, versions |
| **Memory** | Leaks, OOM | Profile memory usage |
| **Concurrency** | Deadlocks, race conditions | Check locks, shared state |

### Phase 4: Form Hypotheses

For each potential cause:
1. Form a hypothesis
2. Create a test to validate
3. Run the test
4. Confirm or reject

### Phase 5: Fix and Verify

1. **Implement the fix**
2. **Add logging if needed**
3. **Test the fix**
4. **Add regression test**

## Debugging Commands

### General Debugging

```bash
# Find recently modified files
find . -type f -mtime -1 -name "*.js" -o -name "*.ts" -o -name "*.py"

# Grep for error patterns
grep -r "ERROR\|FATAL\|Exception" logs/

# Search for suspicious patterns
grep -r "TODO\|FIXME\|XXX" src/

# Check for console.log left in code
grep -r "console\.log\|debugger" src/
```

### Language-Specific

**JavaScript/TypeScript:**
```bash
# Run with debug output
NODE_DEBUG=* node app.js

# Check syntax
node -c file.js

# Run tests in debug mode
npm test -- --inspect-brk
```

**Python:**
```bash
# Run with pdb
python -m pdb script.py

# Check syntax
python -m py_compile script.py

# Verbose mode
python -v script.py
```

**Go:**
```bash
# Race detection
go run -race main.go

# Debug build
go build -gcflags="-N -l"

# Profile
go test -cpuprofile=cpu.prof
```

## Common Debugging Patterns

### Pattern 1: Divide and Conquer

```python
# When you don't know where the bug is:
def process():
    step1()
    step2()
    step3()
    step4()

# Comment out half:
def process():
    step1()
    # step2()
    # step3()
    # step4()

# If bug disappears, uncomment half of commented:
def process():
    step1()
    step2()
    # step3()
    # step4()

# Continue until you isolate the bug
```

### Pattern 2: Add Logging

```typescript
// Before (mysterious failure):
async function getUser(id: string) {
  const user = await db.find(id);
  return transform(user);
}

// After (with logging):
async function getUser(id: string) {
  console.log('[DEBUG] getUser called with id:', id);
  const user = await db.find(id);
  console.log('[DEBUG] db.find returned:', user);
  const result = transform(user);
  console.log('[DEBUG] transform returned:', result);
  return result;
}
```

### Pattern 3: Minimal Reproduction

```typescript
// Complex code with bug:
function processBatch(items, options) {
  // 100 lines of complex logic
}

// Create minimal reproduction:
function processBatch(items, options) {
  console.log('Items:', items.length);
  console.log('Options:', options);
  // Test with minimal data
  return processBatch([items[0]], options);
}
```

## Error Message Analysis

### Common Error Messages

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| `Cannot read property 'X' of undefined` | Accessing property on null/undefined | Add null check, use optional chaining |
| `X is not a function` | Wrong type, shadowing | Check typeof, verify import |
| `Unexpected token` | Syntax error | Check line before error, validate syntax |
| `Module not found` | Import path wrong | Check relative path, verify file exists |
| `EADDRINUSE` | Port already in use | Kill existing process, use different port |
| `Connection refused` | Service not running | Start service, check port |
| `Timeout` | Request too slow | Increase timeout, check network |

## Debugging Checklist

- [ ] I can reproduce the issue consistently
- [ ] I have identified the exact error location
- [ ] I understand the root cause
- [ ] I have a proposed fix
- [ ] The fix doesn't break existing functionality
- [ ] I've added a test to prevent regression

## Scripts

Generate a debug report:
```bash
python scripts/debug_report.py <error-message>
```

## References

- `references/checklist.md` - Debugging checklist
- `references/patterns.md` - Common debugging patterns
- `references/errors.md` - Error message reference
