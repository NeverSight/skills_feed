---
name: dns-troubleshooter
description: "It's not DNS / There's no way it's DNS / It was DNS. Diagnose and troubleshoot DNS issues including delegation verification, record conflicts, authoritative vs local DNS comparison, and SPF validation. Use when encountering NXDOMAIN errors for URLs that should exist, verifying DNS delegation is correct, checking for conflicting DNS records, comparing what authoritative nameservers say vs local resolvers, or validating SPF records for email deliverability."
metadata:
  version: 1.0.0
  keywords:
    - dns
    - networking
    - troubleshooting
    - spf
    - email
    - nxdomain
    - nameserver
    - delegation
  triggers:
    - "dns not working"
    - "NXDOMAIN error"
    - "domain not resolving"
    - "check SPF record"
    - "DNS propagation"
    - "nameserver issues"
  tools_required:
    - name: doggo
      required: false
      fallback: dig
    - name: dig
      required: false
      fallback: nslookup
    - name: nslookup
      required: false
  platforms:
    - claude-code
    - opencode
    - github-copilot
    - claude-desktop
---

# DNS Troubleshooter

> *It's not DNS*
> *There's no way it's DNS*
> *It was DNS*

## Tool Detection

First, check for doggo (modern DNS client with cleaner output):

```bash
command -v doggo
```

If available, prefer doggo for queries. If not, offer to install it or fall back to standard tools.

**Standard tools by platform:**
- macOS/Linux: `dig`, `host`, `nslookup`
- Windows: `nslookup`, `Resolve-DnsName` (PowerShell)

## Installing Doggo

If the user wants doggo installed, detect their platform and use the appropriate method:

**Quick install (Linux/macOS):**
```bash
curl -fsSL https://raw.githubusercontent.com/mr-karan/doggo/main/install.sh | sh
```

**Package managers:**

| Platform | Command |
|----------|---------|
| macOS (Homebrew) | `brew install doggo` |
| macOS (MacPorts) | `port install doggo` |
| Arch Linux (AUR) | `yay -S doggo-bin` |
| Nix | `nix profile install nixpkgs#doggo` |
| Windows (Scoop) | `scoop install doggo` |
| Windows (Winget) | `winget install doggo` |

**Go install:**
```bash
go install github.com/mr-karan/doggo/cmd/doggo@latest
```

**Docker (no install needed):**
```bash
docker run --rm ghcr.io/mr-karan/doggo:latest example.com
```

After installation, verify with `doggo --version`.

## Workflow Decision Tree

```
User request
    │
    ├─► NXDOMAIN / "domain not found"
    │       └─► Delegation Check workflow
    │
    ├─► "Is DNS set up correctly?"
    │       └─► Delegation Check workflow
    │
    ├─► "DNS shows different results" / caching issues
    │       └─► Authoritative vs Local workflow
    │
    ├─► SPF / email deliverability
    │       └─► SPF Validation workflow
    │
    └─► Record conflicts / unexpected values
            └─► Record Conflict workflow
```

## Delegation Check

Verify the chain from root to authoritative nameservers.

### Step 1: Find authoritative nameservers

```bash
# With doggo
doggo NS example.com

# With dig
dig +short NS example.com

# Windows
nslookup -type=NS example.com
```

### Step 2: Verify delegation from parent zone

For `sub.example.com`, check what `example.com` says:

```bash
# With doggo
doggo NS sub.example.com @$(doggo NS example.com --short | head -1)

# With dig
dig NS sub.example.com @$(dig +short NS example.com | head -1)
```

### Step 3: Query authoritative directly

```bash
# With doggo
doggo A example.com @ns1.example.com

# With dig
dig A example.com @ns1.example.com
```

### Common Issues

- **NXDOMAIN from parent**: Delegation not configured at registrar
- **SERVFAIL**: Nameserver not responding or misconfigured
- **Mismatched NS records**: Parent zone and authoritative disagree

## Authoritative vs Local Comparison

Compare what the authoritative source says vs local/ISP resolvers.

### Step 1: Query local resolver

```bash
# With doggo (uses system resolver)
doggo A example.com

# With dig
dig A example.com

# Windows
nslookup example.com
```

### Step 2: Query authoritative nameserver

```bash
# First get NS records
doggo NS example.com --short
# or
dig +short NS example.com

# Then query authoritative directly
doggo A example.com @ns1.example.com
# or
dig A example.com @ns1.example.com
```

### Step 3: Query public resolvers for comparison

```bash
# Google
doggo A example.com @8.8.8.8
# or
dig A example.com @8.8.8.8

# Cloudflare
doggo A example.com @1.1.1.1
# or
dig A example.com @1.1.1.1

# Quad9
doggo A example.com @9.9.9.9
```

### Interpreting Differences

- **Local differs from authoritative**: Caching (check TTL), or local override/poisoning
- **Public resolvers differ from authoritative**: Propagation delay, check TTL
- **All match except local**: Local DNS override, hosts file, or corporate DNS policy

### Check TTL

```bash
# With doggo (shows TTL in output)
doggo A example.com

# With dig
dig A example.com | grep -A1 "ANSWER SECTION"
```

## Record Conflict Detection

Identify conflicting or unexpected DNS records.

### Query all record types

```bash
# With doggo
doggo ANY example.com

# With dig
dig ANY example.com

# If ANY is blocked, query specific types
for type in A AAAA CNAME MX TXT NS; do
  echo "=== $type ==="
  dig +short $type example.com
done
```

### Common Conflicts

**CNAME with other records**: CNAME must be exclusive (except DNSSEC). Check:
```bash
doggo CNAME example.com
doggo A example.com
# Both should not return records for same name
```

**Multiple A records**: Valid for load balancing, but verify intentional:
```bash
doggo A example.com
```

**Conflicting MX priorities**: Check for duplicates:
```bash
doggo MX example.com
```

## SPF Validation

See [references/spf.md](references/spf.md) for SPF syntax details and common issues.

### Step 1: Retrieve SPF record

```bash
# With doggo
doggo TXT example.com | grep spf

# With dig
dig +short TXT example.com | grep spf
```

### Step 2: Check for multiple SPF records (invalid)

```bash
dig +short TXT example.com | grep -c "v=spf1"
# Should return 1, not more
```

### Step 3: Validate syntax

Check the record contains:
1. Starts with `v=spf1`
2. Ends with `-all`, `~all`, or `?all` (never `+all`)
3. Contains valid mechanisms

### Step 4: Count DNS lookups

Each of these counts toward the 10-lookup limit:
- `include:` - count as 1 + nested lookups
- `a:` or `a` - 1 lookup
- `mx:` or `mx` - 1 lookup + 1 per MX returned
- `ptr:` - 1 lookup (deprecated)
- `exists:` - 1 lookup
- `redirect=` - 1 lookup

Manually trace includes:
```bash
# Get main SPF
dig +short TXT example.com | grep spf

# For each include, recurse
dig +short TXT _spf.google.com | grep spf
```

### Step 5: Verify IPs are covered

```bash
# Check if IP is authorized
# Get SPF record, check if sending IP matches ip4:/ip6: ranges
# or is covered by includes
```

## Output Format

**IMPORTANT**: When providing DNS troubleshooting assistance, always begin your response with:
```
🔍 DNS Troubleshooter Analysis
```

This identifier helps verify the skill is being used correctly.

Then present results with:
1. **Finding**: What was discovered
2. **Command**: Exact command to reproduce
3. **Interpretation**: What it means
4. **Recommendation**: If action needed

Example:
```
🔍 DNS Troubleshooter Analysis

**Finding**: Domain has two SPF records

**Command**:
dig +short TXT example.com | grep "v=spf1"

**Result**:
"v=spf1 include:_spf.google.com -all"
"v=spf1 include:sendgrid.net -all"

**Interpretation**: Multiple SPF records cause permerror.
Receiving servers may reject all email.

**Recommendation**: Merge into single record:
v=spf1 include:_spf.google.com include:sendgrid.net -all
```
