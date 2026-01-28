---
name: ctf-solver
description: Solve CTF (Capture The Flag) challenges by analyzing challenge descriptions, source code, and interacting with challenge environments to capture flags.
license: MIT
compatibility: Requires network access to challenge environment. Python3 with requests library recommended.
metadata:
  author: hacktron
  version: "1.0.0"
  category: security
  difficulty: variable
allowed-tools: Bash(*) Read Write Network
---

# CTF Solver

**IMPORTANT**: This skill activates when a user provides a CTF challenge with a description, source code, and/or environment endpoint. Your goal is to act as an expert CTF player and capture the flag.

## Critical Rules

**ALWAYS prefer Python scripts for testing and exploitation:**
- Write standalone Python scripts using `requests` for HTTP interactions
- Use `socket` with timeouts for TCP connections (never interactive)
- Scripts should be non-blocking and output results to stdout

**NEVER use blocking/interactive commands:**
- `nc` / `netcat` (blocks waiting for input)
- `vim` / `nano` / editors (requires interaction)
- `less` / `more` (requires interaction)
- `ssh` without `-o BatchMode=yes`
- Any command that waits for user input

**Instead use:**
- Python scripts with `requests` for HTTP
- Python `socket` with timeouts for TCP
- `curl` for simple HTTP requests
- `cat`, `head`, `tail` for file viewing
- Redirect output: `echo "data" | command`

---

## Core Mindset

Think like a competitive CTF player:
- **Curiosity**: Question every assumption, explore edge cases
- **Persistence**: If one approach fails, try another
- **Creativity**: Combine techniques in unexpected ways
- **Methodical**: Document findings, avoid repeating failed attempts

## Challenge Categories

Recognize and adapt your approach based on challenge type:

| Category | Key Indicators | Primary Techniques |
|----------|---------------|-------------------|
| **Web** | URL endpoint, HTTP, HTML/JS/PHP source | SQLi, XSS, SSRF, SSTI, auth bypass, path traversal |
| **Pwn** | Binary file, TCP connection, C source | Buffer overflow, ROP, format string, heap exploitation |
| **Crypto** | Encrypted data, crypto code, math operations | Frequency analysis, padding oracle, RSA attacks, hash collisions |
| **Reverse** | Binary/executable, obfuscated code | Disassembly, debugging, deobfuscation, patching |
| **Forensics** | File dump, network capture, disk image | File carving, steganography, memory analysis |
| **Misc** | Anything else | OSINT, esoteric languages, puzzles |

---

## Solving Methodology

### Phase 1: Reconnaissance

**Read everything carefully:**

```
┌─────────────────────────────────────────────────────────────┐
│ CHALLENGE INPUTS                                             │
├─────────────────────────────────────────────────────────────┤
│ 1. Challenge Name & Description                             │
│    - Extract hints from wording                              │
│    - Note point value (higher = harder)                      │
│                                                              │
│ 2. Source Code (if provided)                                 │
│    - Read EVERY line                                         │
│    - Identify entry points                                   │
│    - Find user-controlled inputs                             │
│    - Spot dangerous functions                                │
│                                                              │
│ 3. Environment / Attachments                                 │
│    - Map available endpoints                                  │
│    - Identify technologies (headers, errors)                 │
│    - Note versions for known CVEs                            │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Vulnerability Identification

**For each input, ask:**

1. **Where does user input go?** (database, filesystem, command, template)
2. **What sanitization exists?** (filters, encoding, validation)
3. **What's the trust boundary?** (client vs server, authenticated vs anonymous)
4. **What assumptions can be broken?** (type confusion, race conditions, logic flaws)

### Phase 3: Exploitation

**Build your exploit iteratively:**

```
Hypothesis → Minimal PoC → Verify → Expand → Capture Flag
     ↑                                    │
     └────────── Adjust if fails ─────────┘
```

### Phase 4: Flag Extraction

**Common flag locations:**
- Response body or headers
- Error messages
- Environment variables
- Files (`/flag`, `/flag.txt`, `/home/*/flag`)
- Database entries

---

## Solution Documentation

**After capturing the flag, document:**

```markdown
## Challenge: [Name]
**Category**: [Web/Pwn/Crypto/Rev/Forensics/Misc]

### Vulnerability
[What was the vulnerability]

### Exploitation
[Step-by-step exploitation]

### Payload
[Final working payload]

### Flag
FLAG{the_captured_flag}
```

---

## Success Criteria

**The challenge is solved when:**
1. Flag is captured from the challenge environment
2. Flag matches expected format
3. Exploit is reproducible
4. Solution is documented

**Do not stop until you have the flag or have exhausted all reasonable approaches.**

---

## Approach Summary

```
1. READ the challenge description carefully
2. ANALYZE all provided source code line by line
3. MAP the attack surface (inputs, endpoints, functions)
4. IDENTIFY potential vulnerabilities
5. WRITE Python scripts to test exploits
6. ITERATE if initial attempts fail
7. EXTRACT the flag
8. DOCUMENT the solution
```
