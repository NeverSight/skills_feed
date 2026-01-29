---
name: your-skill-name
description: A clear description of what this skill does and when to use it. Include specific keywords that users would naturally say. Use when [specific scenarios].
allowed-tools: Read, Bash
---

# Your Skill Name

<!-- Replace this with a brief introduction to your skill -->
A brief description of what this skill does and how it helps users.

## Instructions

<!--
This section tells Claude HOW to use your skill.
Be specific and provide step-by-step guidance.
-->

When the user [describes the scenario when this skill should be used]:

1. **First Step**: [What Claude should do first]
   - [Additional details or substeps]
   - [Use bash, read files, etc.]

2. **Second Step**: [What Claude should do next]
   - [How to process or analyze information]
   - [What to look for]

3. **Final Step**: [How to complete the task]
   - [What output to provide]
   - [How to format the response]

## Examples

<!--
Show concrete examples of using this skill.
This helps Claude understand the expected behavior.
-->

### Example 1: [Scenario Name]

**User asks**: "[Example user question]"

**What the skill does**:
1. [First action]
2. [Second action]
3. [Result]

**Expected output**:
```
[Show example output]
```

### Example 2: [Another Scenario]

**User asks**: "[Another example question]"

**What the skill does**:
1. [Actions...]
2. [More actions...]

## Best Practices

<!-- List key guidelines for using this skill effectively -->

- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

## Common Patterns

<!-- Show common usage patterns or templates -->

### Pattern 1: [Pattern Name]

[Describe when to use this pattern]

```
[Example code or template]
```

## Limitations

<!-- Be transparent about what this skill CANNOT do -->

- [Limitation 1]
- [Limitation 2]
- [What to do instead]

## Configuration

<!-- If your skill is configurable, explain how -->

You can customize this skill by editing `scripts/config.json` after installation.

Available options:
- `option1`: [Description]
- `option2`: [Description]

## Additional Resources

<!-- Link to detailed documentation using Progressive Disclosure -->

For more detailed information:
- See [reference.md](reference.md) for complete API documentation
- See [examples.md](examples.md) for more usage examples

---

<!--
TIPS FOR WRITING EFFECTIVE SKILLS:

1. DESCRIPTION is crucial - Include specific keywords users would say
   ❌ Bad: "Helps with files"
   ✅ Good: "Analyzes Python files for syntax errors. Use when checking Python code, debugging syntax, or validating .py files."

2. Keep SKILL.md under 500 lines - Use reference.md for detailed docs

3. Be specific in instructions - Claude needs clear step-by-step guidance

4. Show examples - Concrete examples are more helpful than abstract descriptions

5. Test thoroughly - Install locally and verify Claude triggers it correctly
-->
