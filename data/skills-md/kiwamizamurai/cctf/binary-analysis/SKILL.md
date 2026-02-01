---
name: binary-analysis
description: Analyzes binary files for vulnerabilities and develops exploits. Use when working with ELF/PE executables, pwn challenges, buffer overflow, heap exploitation, ROP chains, format string bugs, or shellcode development.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Binary Analysis Skill

## Quick Workflow

```
Progress:
- [ ] Run checksec (identify protections)
- [ ] Identify binary type and dangerous functions
- [ ] Find vulnerability (BOF/format string/heap)
- [ ] Calculate offsets
- [ ] Develop exploit with pwntools
- [ ] Test locally, then remote
```

## Quick Analysis Pipeline

```bash
# 1. File identification
file <binary>

# 2. Security features
checksec --file=<binary>

# 3. Interesting strings
strings <binary> | grep -iE "flag|ctf|password|correct|wrong|win|shell|secret"

# 4. Function symbols
nm <binary> 2>/dev/null | grep -E " T | t " | head -20

# 5. Dangerous functions
objdump -d <binary> 2>/dev/null | grep -E "gets|strcpy|sprintf|scanf|system|exec"

# 6. Auto vulnerability scan
cwe_checker <binary>
```

## Reference Files

| Topic | Reference |
|-------|-----------|
| Protections & Vuln Detection | [reference/protections.md](reference/protections.md) |
| Exploitation Templates | [reference/exploits.md](reference/exploits.md) |
| Advanced Tools | [reference/tools.md](reference/tools.md) |

## Quick Commands

```bash
# Generate cyclic pattern
python3 -c "from pwn import *; print(cyclic(200))"

# Find offset
python3 -c "from pwn import *; print(cyclic_find(0x61616167))"

# Find ROP gadgets
ROPgadget --binary <binary> | grep "pop rdi"

# Find one_gadget
one_gadget <libc>
```

## Tools Summary

| Tool | Purpose |
|------|---------|
| checksec | Check binary protections |
| pwntools | Exploit development |
| ROPgadget | Find ROP gadgets |
| one_gadget | Find libc one-shot gadgets |
| cwe_checker | Auto vuln detection |
| qira | Runtime analysis |
| Triton | Symbolic execution |
