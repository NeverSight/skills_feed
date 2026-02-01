---
name: osint
description: Gathers intelligence from public sources. Use when searching for usernames, geolocating images, investigating social media, analyzing domains, or solving information gathering challenges.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# OSINT Skill

## Quick Workflow

```
Progress:
- [ ] Identify target type (username/image/domain)
- [ ] Extract metadata (exiftool for images)
- [ ] Cross-reference across platforms
- [ ] Check archives/caches
- [ ] Document findings
```

## Quick Commands

```bash
# Image metadata
exiftool image.jpg
exiftool -gpslatitude -gpslongitude image.jpg

# Username search
sherlock username

# DNS lookup
dig target.com ANY
whois target.com
```

## Reference Files

| Topic | Reference |
|-------|-----------|
| Image Analysis & Geolocation | [reference/image.md](reference/image.md) |
| Domain & IP OSINT | [reference/domain.md](reference/domain.md) |
| Social Media & Username | [reference/social.md](reference/social.md) |

## Useful Online Tools

| Tool | Purpose | URL |
|------|---------|-----|
| Shodan | IoT/device search | shodan.io |
| Censys | Internet scan data | censys.io |
| VirusTotal | File/URL analysis | virustotal.com |
| CyberChef | Data transformation | gchq.github.io/CyberChef |
| IntelX | Search engine | intelx.io |
| Maltego | Graph analysis | maltego.com |

## CTF Quick Patterns

```bash
# Find location from photo
exiftool -gpslatitude -gpslongitude image.jpg
# If no GPS: reverse image search, identify landmarks

# Find person from username
sherlock username
# Check: GitHub, Twitter, Instagram, Reddit

# Find deleted content
# Wayback Machine, Google cache, Archive.today
```
