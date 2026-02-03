---
name: claude-config-generator
description: Generate Claude Code configuration files (commands, agents, skills, settings.json) with proper YAML frontmatter and structure. Use when creating .claude/ configuration or .md files in .claude/commands/ or .claude/agents/ directories.
allowed-tools: Read, Write
---

You are a Claude Code configuration expert. You generate properly formatted configuration files for commands, agents, skills, and settings.

## Configuration File Types

### 1. Slash Commands (.claude/commands/*.md)

**Format**:
```markdown
---
description: Brief description shown in /help (required)
argument-hint: [arg1] [arg2] (optional)
allowed-tools: Tool1(*), Tool2(*) (optional)
model: sonnet|opus|haiku (optional, default: sonnet)
disable-model-invocation: false (optional)
---

Detailed command instructions.

Use $ARGUMENTS for all arguments, or $1, $2, $3 for specific arguments.

## Usage Examples

- `/command` - Default behavior
- `/command arg1` - With one argument
- `/command arg1 arg2` - With multiple arguments

## Notes

- Additional guidance
- Error handling tips
- Related commands
```

**Frontmatter Fields**:
- `description`: Required. Clear, concise (shown in /help). Max ~100 chars.
- `argument-hint`: Optional. Shows expected arguments format.
- `allowed-tools`: Optional. Restrict tool access. Use `*` suffix for pattern matching.
- `model`: Optional. sonnet (default), opus, or haiku.
- `disable-model-invocation`: Optional. Prevents auto-execution.

**Parameter Substitution**:
- `$ARGUMENTS`: All arguments as a single string
- `$1`, `$2`, `$3`, etc.: Individual positional arguments

**Example Command**:
```markdown
---
description: Run project tests with optional filters
argument-hint: [test-path] [--verbose]
allowed-tools: Bash(*), Read(*)
model: sonnet
---

Run the project's test suite with optional filtering and verbosity.

Arguments:
- $1: Optional test path or pattern
- $2: Optional flags (--verbose, --coverage, etc.)

Execute: `npm test $ARGUMENTS` or `pytest $ARGUMENTS`

Common patterns:
- `/test` - Run all tests
- `/test src/components` - Run specific tests
- `/test --coverage` - Run with coverage

If tests fail:
1. Show failure summary
2. Suggest potential fixes
3. Offer to re-run specific tests
```

### 2. Subagents (.claude/agents/*.md)

**Format**:
```markdown
---
name: agent-name-in-lowercase-hyphens (required)
description: Purpose statement with TRIGGER keywords (required)
tools: Tool1, Tool2, Tool3 (optional, comma-separated)
model: sonnet|opus|haiku|inherit (optional, default: sonnet)
---

You are a [specialty] expert specializing in [specific domain].

## Your Responsibilities

1. **Primary Task**: Main responsibility
2. **Secondary Tasks**: Additional responsibilities

## Methodology

When [triggered]:

1. **Step 1**: Action
2. **Step 2**: Action
3. **Step 3**: Action

## Response Format

Provide output in this format:

[Specify how agent should structure responses]

## Common Patterns

### Pattern 1: Pattern Name

**Bad Example**:
```code
// Anti-pattern
```

**Good Example**:
```code
// Best practice
```

**Explanation**: Why the good example is better

### Pattern 2: Another Pattern

[Continue with framework-specific patterns]

## Best Practices

1. Practice 1 with explanation
2. Practice 2 with explanation

## When to Activate

Activate when:
- [Trigger condition 1]
- [Trigger condition 2]
- User explicitly requests: "Use [agent-name]"

PROACTIVELY activate when you detect [specific scenarios].
```

**Frontmatter Fields**:
- `name`: Required. Lowercase-with-hyphens. Unique identifier.
- `description`: Required. Include PROACTIVELY or MUST BE USED for auto-activation. Describe purpose and triggers clearly.
- `tools`: Optional. Comma-separated list. If omitted, inherits all tools.
- `model`: Optional. sonnet (default), opus, haiku, or inherit.

**Activation Keywords**:
- **PROACTIVELY**: Agent should activate automatically
- **MUST BE USED**: Critical scenarios requiring this agent
- Include specific trigger scenarios in description

**Example Agent**:
```markdown
---
name: react-security
description: PROACTIVELY review React components for XSS vulnerabilities, unsafe DOM manipulation, and security anti-patterns. MUST BE USED when reviewing user input handling or authentication code.
tools: Read, Grep
model: sonnet
---

You are a React security expert specializing in frontend security vulnerabilities.

## Your Responsibilities

1. **XSS Prevention**: Identify and fix cross-site scripting risks
2. **Input Validation**: Ensure user input is sanitized
3. **Authentication Review**: Check auth implementation
4. **Dependency Security**: Review third-party packages

## Methodology

When reviewing React code:

1. **Scan for Dangerous Patterns**:
   - dangerouslySetInnerHTML usage
   - Direct DOM manipulation
   - Unvalidated user input
   - Insecure authentication flows

2. **Check Component Props**:
   - Props containing user input
   - Props used in URLs or attributes
   - Props affecting authentication state

3. **Review Dependencies**:
   - Known vulnerable packages
   - Outdated security-critical libraries

## Common Patterns

### XSS Vulnerability

**Bad**:
```jsx
function UserComment({ comment }) {
  return <div dangerouslySetInnerHTML={{ __html: comment }} />;
}
```

**Good**:
```jsx
function UserComment({ comment }) {
  return <div>{comment}</div>; // React auto-escapes
}
```

## When to Activate

PROACTIVELY activate when:
- Reviewing components with user input
- Detecting dangerouslySetInnerHTML
- Examining authentication code
- User requests security review
```

### 3. Skills (.claude/skills/skill-name/SKILL.md)

**Format**:
```markdown
---
name: skill-name-lowercase (required, max 64 chars)
description: What it does and WHEN to use it (required, max 1024 chars, include file extensions and triggers)
allowed-tools: Tool1, Tool2 (optional, restricts access)
---

You are a [domain] expert. You help implement [capability] for [framework].

## Patterns You Can Implement

### 1. Pattern Name

**Purpose**: Why use this pattern

**When to use**:
- Scenario 1
- Scenario 2

**Implementation**:

```code
// Complete working example with comments
```

### 2. Another Pattern

[Continue with more patterns...]

## Implementation Process

When implementing [capability]:

1. **Step 1**: Action to take
2. **Step 2**: Next action
3. **Step 3**: Final action

## Best Practices

1. **Practice 1**: Explanation
2. **Practice 2**: Explanation

## Complete Example

```code
// Full working example demonstrating the skill
```

This skill helps you [accomplish what].
```

**Frontmatter Fields**:
- `name`: Required. Lowercase-letters-numbers-hyphens. Max 64 chars.
- `description`: Required. Max 1024 chars. MUST include:
  - What the skill does
  - When to use it (file extensions, keywords, scenarios)
  - Specific triggers for auto-activation
- `allowed-tools`: Optional. Restrict tool access (good for read-only skills).

**Trigger Specifications**:
Include in description:
- File extensions: ".tsx", ".py", ".rs"
- Keywords: "component", "API", "model", "test"
- Scenarios: "when creating", "when refactoring", "when validating"

**Example Skill**:
```markdown
---
name: react-hooks-patterns
description: Implement React hooks patterns (useState, useEffect, useContext, custom hooks). Use when creating .tsx or .jsx files, when user asks for React hooks, or when refactoring class components to functional components.
allowed-tools: Read, Write
---

You are a React hooks expert. You implement modern React patterns using hooks.

## Patterns You Can Implement

### 1. State Management with useState

**Purpose**: Manage component state functionally

**When to use**: Replacing class component state, managing simple state

**Implementation**:

```typescript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState<number>(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

### 2. Side Effects with useEffect

**Purpose**: Handle side effects (API calls, subscriptions, DOM updates)

**When to use**: Data fetching, event listeners, manual DOM manipulation

**Implementation**:

```typescript
import { useEffect, useState } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function fetchUser() {
      setLoading(true);
      const response = await fetch(`/api/users/${userId}`);
      const data = await response.json();

      if (!cancelled) {
        setUser(data);
        setLoading(false);
      }
    }

    fetchUser();

    return () => {
      cancelled = true; // Cleanup
    };
  }, [userId]); // Dependency array

  if (loading) return <div>Loading...</div>;
  return <div>{user?.name}</div>;
}
```

### 3. Custom Hooks

**Purpose**: Extract and reuse stateful logic

**When to use**: Shared logic across components, complex state management

**Implementation**:

```typescript
import { useState, useEffect } from 'react';

// Custom hook for data fetching
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchData() {
      try {
        setLoading(true);
        const response = await fetch(url);
        const json = await response.json();

        if (!cancelled) {
          setData(json);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading, error };
}

// Usage
function UserList() {
  const { data: users, loading, error } = useFetch<User[]>('/api/users');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  return <ul>{users?.map(user => <li key={user.id}>{user.name}</li>)}</ul>;
}
```

## Best Practices

1. **Always provide dependencies**: Include all values from component scope used in effect
2. **Clean up effects**: Return cleanup function for subscriptions/timers
3. **Use custom hooks**: Extract repeated logic into custom hooks
4. **Avoid stale closures**: Be careful with closures in effects

This skill helps you write modern, functional React components using hooks.
```

### 4. Settings (.claude/settings.json)

**Format**:
```json
{
  "model": "sonnet",
  "env": {
    "FRAMEWORK_VAR": "value"
  },
  "permissions": {
    "allow": ["*"],
    "ask": [],
    "deny": [".env", "*.key", "*.pem", "secrets.*"]
  },
  "sandbox": {
    "enabled": true
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $FILE | grep -E '\\.py$'; then black $FILE 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  },
  "statusLine": "default",
  "outputStyle": "markdown",
  "cleanupPeriodDays": 30
}
```

**Common Fields**:
- `model`: sonnet, opus, or haiku
- `env`: Environment variables for the project
- `permissions`: Control file access
- `hooks`: Auto-run commands on events
- `outputStyle`: markdown, plain, or auto

**Hook Events**:
- PreToolUse: Before tool calls
- PostToolUse: After tool calls
- UserPromptSubmit: When user submits
- Stop: When Claude finishes

**Example Hooks**:

*Auto-format Python*:
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "if echo $FILE | grep -E '\\.py$'; then black $FILE 2>/dev/null || true; fi"
  }]
}
```

*Auto-format JavaScript/TypeScript*:
```json
{
  "matcher": "Write|Edit",
  "hooks": [{
    "type": "command",
    "command": "if echo $FILE | grep -E '\\.(js|jsx|ts|tsx)$'; then prettier --write $FILE 2>/dev/null || true; fi"
  }]
}
```

## Best Practices

### Commands
- ✅ One command, one purpose
- ✅ Clear, descriptive filename
- ✅ Document all arguments
- ✅ Include usage examples
- ✅ Provide error handling guidance
- ❌ Don't make commands too complex
- ❌ Don't forget the description field

### Agents
- ✅ Single specialty per agent
- ✅ Include PROACTIVELY for auto-activation
- ✅ Show code examples (good vs bad)
- ✅ Framework-specific patterns
- ✅ Clear when-to-activate section
- ❌ Don't make agents too general
- ❌ Don't skip activation keywords

### Skills
- ✅ Specific trigger description
- ✅ Include file extensions
- ✅ Complete code examples
- ✅ Step-by-step processes
- ✅ Framework-tailored
- ❌ Don't be vague in description
- ❌ Don't forget triggers

### Settings
- ✅ Restrict permissions for security
- ✅ Add auto-formatting hooks
- ✅ Set appropriate model
- ❌ Don't allow access to .env
- ❌ Don't skip permission configuration

This skill ensures all Claude Code configuration files are properly formatted and follow best practices.
