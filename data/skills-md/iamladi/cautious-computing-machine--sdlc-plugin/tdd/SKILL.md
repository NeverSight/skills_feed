---
name: tdd
description: TDD enforcement during implementation. Reads `tdd:` setting from CLAUDE.md. Modes - strict (human approval for escape), soft (warnings), off (disabled). Auto-invoked by /implement.
---

# TDD Enforcement Skill

Enforce Test-Driven Development during implementation based on project configuration.

## Configuration

Read `tdd:` setting from the project's `CLAUDE.md` file:

```yaml
# In CLAUDE.md
tdd: strict  # strict | soft | off
```

**Default**: `off` (if not specified)

## Modes

### Strict Mode (`tdd: strict`)

**Hard enforcement with human escape hatch.**

Before writing ANY implementation code:

1. **Check for existing test**
   - Search for test file matching implementation file
   - Look for test describing the functionality being added

2. **If no test exists**:
   - STOP implementation
   - Output: `TDD VIOLATION: No test found for [functionality]`
   - Ask user via `AskUserQuestion`:
     ```
     No test exists for this functionality. TDD strict mode requires tests first.

     Options:
     1. Write test first (Recommended)
     2. Prototype escape - proceed without test (requires justification)
     ```

3. **Prototype escape hatch**:
   - If user chooses escape: require written justification
   - Log: `TDD ESCAPE: [functionality] - Reason: [user justification]`
   - Remind user: "Remember to add tests before PR submission"

### Soft Mode (`tdd: soft`)

**Warnings without blocking.**

Before writing implementation code:

1. **Check for existing test**
2. **If no test exists**:
   - Output warning: `TDD WARNING: No test found for [functionality]. Consider writing tests first.`
   - Continue with implementation
   - Track untested functionality for summary

3. **After implementation complete**:
   - Summary: "The following functionality lacks tests: [list]"

### Off Mode (`tdd: off`)

**No TDD checks.**

Skip all TDD enforcement. Standard implementation flow.

## Reading CLAUDE.md

```typescript
// Pseudocode for reading TDD config
function getTddMode(projectRoot: string): 'strict' | 'soft' | 'off' {
  const claudeMdPaths = [
    `${projectRoot}/CLAUDE.md`,
    `${projectRoot}/.claude/CLAUDE.md`
  ]

  for (const path of claudeMdPaths) {
    const content = readFile(path)
    if (!content) continue

    // Look for tdd: setting
    const match = content.match(/^tdd:\s*(strict|soft|off)/m)
    if (match) return match[1]
  }

  return 'off' // default
}
```

## Integration with Implementer Agent

When dispatching the implementer agent, include TDD context:

```markdown
## TDD Mode: [strict|soft|off]

[Mode-specific instructions based on above]
```

The implementer agent MUST respect these instructions.

## Test File Discovery

When checking for tests, search in order:
1. `__tests__/[filename].test.ts`
2. `[filename].test.ts` (adjacent)
3. `[filename].spec.ts` (adjacent)
4. `test/[filename].test.ts`
5. `tests/[filename].test.ts`

For functionality within a file, search for:
- Test describing the function name
- Test describing the class name
- Test describing the exported method

## Examples

### Strict Mode - Test Exists
```
Checking TDD compliance for: addUser function
Found test: src/__tests__/user.test.ts:45 - "addUser creates user with valid input"
TDD: PASS - Proceeding with implementation
```

### Strict Mode - No Test
```
Checking TDD compliance for: deleteUser function
No test found for deleteUser functionality

TDD VIOLATION: No test found for deleteUser function

[AskUserQuestion presented]
```

### Soft Mode - No Test
```
Checking TDD compliance for: deleteUser function
No test found for deleteUser functionality

TDD WARNING: No test found for deleteUser. Consider writing tests first.
Continuing with implementation...
```

## Best Practices

When writing tests first (strict mode):

1. **Write the test that describes expected behavior**
2. **Run it - verify it fails** (Red)
3. **Write minimal implementation to pass** (Green)
4. **Refactor if needed** (Refactor)
5. **Commit both test and implementation together**

## Related Skills

- `/test` - Write tests following Kent C. Dodds principles
- `test-writer` agent - Auto-spawns for test-related tasks
