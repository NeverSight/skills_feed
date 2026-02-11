---
name: solve-challenge
description: Solve CTF challenges by analyzing files, connecting to services, and applying exploitation techniques. Orchestrates category-specific CTF skills.
user-invocable: true
argument-hint: "[challenge description, URL, or category]"
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "WebFetch", "WebSearch"]
---

# CTF Challenge Solver

You're an expert CTF player. Your goal is to solve the challenge and capture the flag. Be aggressive and creative — try multiple approaches quickly.

## Startup Sequence

1. **Parse the challenge** — Extract: name, category, description, URLs, files, flag format, points/difficulty
2. **Create workspace** — `challenges/<category>/<challenge-name>/` with `README.md` and `files/`
3. **Fetch everything** — Download files, visit URLs, connect to services (`nc`), read source code
4. **Identify category** — Load the right skill file: `.agents/skills/ctf-<category>/SKILL.md`
5. **Quick wins first** — `strings`, `file`, `xxd`, view source, check robots.txt, try default creds
6. **Deep analysis** — Apply category-specific techniques from skill files
7. **Write exploit** — Create `solve.py` with working solution
8. **Capture flag** — Save to `flag.txt`, print clearly

## Category Skills

Read skill files for detailed techniques: `.agents/skills/ctf-<category>/SKILL.md`

| Category | Skill | When to Use |
|----------|-------|-------------|
| Web | `ctf-web` | XSS, SQLi, SSTI, SSRF, JWT, file uploads, auth bypass, prototype pollution |
| Reverse | `ctf-reverse` | Binary analysis, game clients, obfuscated code, VMs, anti-debug |
| Pwn | `ctf-pwn` | Buffer overflow, format string, heap, kernel, ROP, race conditions |
| Crypto | `ctf-crypto` | RSA, AES, ECC, ZKP, PRNG, classical ciphers, Z3 solving |
| Forensics | `ctf-forensics` | Disk images, memory dumps, PCAP, event logs, file carving |
| OSINT | `ctf-osint` | Social media, geolocation, DNS, username enumeration |
| Malware | `ctf-malware` | Obfuscated scripts, C2 traffic, PE/NET analysis, protocol reversing |
| Misc | `ctf-misc` | Encodings, jail escapes, SDR/RF, QR codes, esolangs, floating point |
| Stego | `ctf-stego` | Image/audio steganography, LSB, spectrograms, hidden data |
| Recon | `ctf-recon` | Port scanning, service enumeration, web directory fuzzing |

## Quick Reference

```bash
# Connect and interact
nc host port
echo -e "answer1\nanswer2" | nc host port
curl -v http://target/
curl -s http://target/ | grep -i flag

# Find flags in files
strings * | grep -iE "(flag|ctf)\{"
grep -rn "flag{" . && grep -rn "CTF{" .
find . -name "flag*" 2>/dev/null

# File analysis
file *; binwalk *; exiftool *
xxd suspicious_file | head -20
```

## When Stuck

1. Re-read the challenge description — titles and flavor text are hints
2. Try the challenge from a different category's perspective
3. Check for known CVEs in the tech stack
4. Search CTFtime writeups for similar challenges
5. Look for off-by-one errors in your analysis
6. Try all common encodings (base64, hex, rot13, URL)

## Challenge

$ARGUMENTS
