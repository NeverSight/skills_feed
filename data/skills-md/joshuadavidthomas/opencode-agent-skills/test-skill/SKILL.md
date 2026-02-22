---
name: test-skill
description: A test skill to verify all plugin tools work correctly - use_skill, read_skill_file, run_skill_script, find_skills
---

# Test Skill

This skill exists to verify the OpenCode Skills Plugin API works correctly.

## Testing Checklist

Use this skill to verify:

1. **use_skill** - You're reading this, so it works!
2. **read_skill_file** - Load `example-config.json` or `helper-docs.md`
3. **run_skill_script** - Execute `greet` or `echo-args` scripts
4. **find_skills** - Should list this skill and others

## Available Files

- `SKILL.md` - This file (the main skill content)
- `helper-docs.md` - Additional documentation to test read_skill_file
- `example-config.json` - Sample config file to test non-markdown loading
- `scripts/greet` - Simple script that prints a greeting
- `scripts/echo-args` - Script that echoes back its arguments

## Example Workflow

```
1. find_skills              # List available skills
2. use_skill test-skill     # Load this skill (you're here!)
3. read_skill_file test-skill helper-docs.md    # Load supporting docs
4. run_skill_script test-skill greet            # Run a script
5. run_skill_script test-skill echo-args --foo bar  # Run with args
```

## Expected Outputs

When everything works:
- `use_skill` returns "Skill 'test-skill' loaded." with scripts listed
- `read_skill_file` returns "File 'X' from skill 'test-skill' loaded."
- `run_skill_script greet` returns "Hello from test-skill!"
- `run_skill_script echo-args` returns the arguments passed to it
