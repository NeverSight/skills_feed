---
name: explaining-rules
description: Explains which coding rules apply to files and why they matter. Uses the rule index to discover all available rules dynamically. Use when the user asks about rules, coding standards, or best practices.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Explaining Rules Skill

<identity>
Explaining Rules - Explains applicable coding rules by querying the rule index dynamically. Discovers all 1,081+ rules without hard-coding.
</identity>

<capabilities>
- User asks "What rules apply to this file?"
- Explaining coding standards to team members
- Onboarding new developers
- Understanding rule coverage for a project
- Reviewing which rules are active
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Available Skills

Discover available skills by scanning the skills directory:

```bash
ls .claude/skills/
```

Skills contain domain-specific coding standards and best practices.

**Note**: Skills are self-contained in `.claude/skills/[skill-name]/SKILL.md`

### Step 2: Analyze Target File or Query

Determine what needs explanation:

- **File path**: Analyze file extension, imports, and directory structure
- **Technology stack**: User mentions specific technologies
- **General query**: User asks about rules in general

### Step 3: Detect Technologies

For file-based queries, detect technologies using:

- File extension (`.tsx` -> TypeScript, React)
- Import statements (`next` -> Next.js, `react` -> React)
- Directory structure (`app/` -> Next.js App Router)
- Framework-specific patterns

Match file patterns to relevant skills (e.g., `.tsx` files → react-expert, typescript-expert).

### Step 4: Find Matching Skills

Match technologies to expert skills:

| Technology | Skill                 |
| ---------- | --------------------- |
| React, JSX | react-expert          |
| TypeScript | typescript-expert     |
| Next.js    | nextjs-expert         |
| Python     | python-backend-expert |
| Node.js    | nodejs-expert         |
| Database   | database-expert       |
| Testing    | testing-expert        |

### Step 5: Load Relevant Skills

Read the matching skill files:

```bash
cat .claude/skills/[skill-name]/SKILL.md
```

Focus on 3-5 most relevant skills for the query.

### Step 6: Explain Skills

For each relevant skill, explain:

- **What it covers**: Main purpose and scope
- **Why it applies**: Connection to the file/query
- **Key requirements**: Most important standards
- **Examples**: Code examples showing compliance
  </execution_process>

<best_practices>

1. **Be Specific**: Explain why each rule applies, not just what it says
2. **Prioritize**: Master rules first, then archive rules
3. **Use Examples**: Show code examples from the rule files
4. **Progressive Disclosure**: Load only relevant rules, not all 1,081
5. **Context-Aware**: Adapt explanation to user's experience level
   </best_practices>
   </instructions>

<examples>
<formatting_example>
**Output Format**

Structure explanations clearly:

```markdown
## Skills Applicable to [file/query]

**Technologies Detected**: [list]

### Matching Skills

- **[Skill Name]**: [brief description]
  - **Applies because**: [reason]
  - **Key requirements**: [list]
  - **Example**: [code snippet]
```

</formatting_example>
</examples>

## Rules

- Scan skills directory to find applicable skills
- Explain why skills apply, not just what they say
- Focus on 3-5 most relevant skills

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
