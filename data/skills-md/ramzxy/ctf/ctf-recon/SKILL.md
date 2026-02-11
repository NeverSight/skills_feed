---
name: ctf-recon
description: Target reconnaissance and enumeration for CTF challenges. Use when you need to scan ports, discover services, enumerate web directories, or fingerprint technology stacks.
user-invocable: false
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "WebFetch", "WebSearch"]
---

# CTF Reconnaissance & Enumeration

## Web Reconnaissance

### Initial Checks
```bash
# Fetch and inspect
curl -v http://target/
curl -s http://target/ | head -100

# Check common paths
for path in robots.txt sitemap.xml .env .git/HEAD .well-known/ admin api debug; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://target/$path")
    [ "$code" != "404" ] && echo "[+] /$path -> $code"
done

# Response headers
curl -sI http://target/ | grep -iE "(server|x-|powered|content-type|set-cookie)"

# View page source for comments, JS, hidden forms
curl -s http://target/ | grep -iE "(<!--|flag|secret|admin|api|token|password)"
```

### Technology Fingerprinting
```bash
# Server identification
curl -sI http://target/ | grep -i "server:"
# X-Powered-By, X-Framework, etc.

# Common framework indicators
curl -s http://target/ | grep -ioE "(react|angular|vue|next|nuxt|flask|django|express|laravel|rails)"

# JavaScript bundles
curl -s http://target/ | grep -oE 'src="[^"]*\.js"' | head -20

# Check for source maps
curl -s http://target/main.js.map -o /dev/null -w "%{http_code}"
```

### Directory/File Discovery
```bash
# Common wordlist paths
# /usr/share/wordlists/dirb/common.txt
# /usr/share/seclists/Discovery/Web-Content/common.txt

# ffuf for fuzzing
ffuf -u http://target/FUZZ -w wordlist.txt -mc 200,301,302,403
ffuf -u http://target/FUZZ -w wordlist.txt -e .php,.txt,.html,.js,.bak

# gobuster alternative
gobuster dir -u http://target/ -w wordlist.txt
```

### API Enumeration
```bash
# Check common API paths
for path in api api/v1 api/v2 graphql api/docs swagger.json openapi.json; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://target/$path")
    [ "$code" != "404" ] && echo "[+] /$path -> $code"
done

# Extract API endpoints from JS bundles
curl -s http://target/static/js/main.js | grep -oE '"/api/[^"]*"' | sort -u

# GraphQL introspection
curl -s http://target/graphql -H "Content-Type: application/json" \
    -d '{"query":"{__schema{types{name fields{name}}}}"}'
```

## Network Reconnaissance

### Port Scanning
```bash
# Quick TCP scan
nmap -sV -sC -T4 target

# All ports
nmap -p- -T4 target

# UDP scan (slow but important)
nmap -sU --top-ports 20 target

# Service version detection
nmap -sV -p PORT target
```

### Service Interaction
```bash
# Banner grabbing
nc -v target port
echo "" | nc -w3 target port

# SSL/TLS info
openssl s_client -connect target:443 </dev/null 2>/dev/null | openssl x509 -noout -text

# DNS
dig target ANY
dig -t txt target
dig axfr @ns.target target  # Zone transfer attempt
```

## Source Code Reconnaissance

### Git Exposure
```bash
# Check for exposed .git
curl -s http://target/.git/HEAD
curl -s http://target/.git/config

# Dump with git-dumper
git-dumper http://target/.git/ ./dumped-repo

# Extract from downloaded .git
cd dumped-repo && git log --all --oneline
git diff HEAD~5..HEAD
git log --all --diff-filter=D --name-only  # Deleted files
git show HEAD~3:secret.txt                  # Recover deleted files
```

### Backup File Discovery
```bash
# Common backup extensions
for ext in .bak .old .orig .save .swp ~; do
    curl -s -o /dev/null -w "%{http_code}" "http://target/index.php${ext}"
done

# Editor backups
curl -s http://target/.index.php.swp  # vim swap
curl -s http://target/index.php~      # emacs backup
```

## CTF-Specific Patterns

- Challenge description is ALWAYS a hint — read every word
- Challenge title often reveals the technique (e.g., "Inject" = injection, "Token" = JWT)
- Points/difficulty indicate expected complexity
- If a port is unusual, try connecting with nc first to see the banner
- Multiple open ports often means chaining vulnerabilities across services
- Always check for custom HTTP headers in responses (X-Flag, X-Hint, etc.)
