---
name: forensics
description: Extracts hidden data from files and analyzes forensic artifacts. Use when working with images, memory dumps, disk images, steganography, file carving, or when searching for hidden flags in files.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Forensics Analysis Skill

## Quick Workflow

```
Progress:
- [ ] Identify file type (file, xxd)
- [ ] Check metadata (exiftool)
- [ ] Search strings for flag
- [ ] Check for embedded data (binwalk)
- [ ] Try steganography tools
- [ ] Extract hidden content
```

## Step 1: Quick Analysis

```bash
file suspicious_file
exiftool suspicious_file
strings suspicious_file | grep -iE "flag|ctf|secret|key"
binwalk suspicious_file
```

## Step 2: Identify Challenge Type

| File Type | Approach | Reference |
|-----------|----------|-----------|
| Image (PNG/JPG) | Steganography | [reference/steganography.md](reference/steganography.md) |
| Memory dump | Volatility | [reference/memory.md](reference/memory.md) |
| Unknown/corrupted | File analysis | [reference/file-analysis.md](reference/file-analysis.md) |
| PCAP | Network skill | Use `networking` skill |

## Image Stego - Quick Start

```bash
# Try AperiSolve first (online)
# https://www.aperisolve.com/

# PNG
zsteg image.png
zsteg -a image.png

# JPEG
steghide extract -sf image.jpg
stegseek image.jpg rockyou.txt  # Brute force
```

**Full techniques**: [reference/steganography.md](reference/steganography.md)

## Memory Dump - Quick Start

```bash
# Volatility 3
vol -f memory.dmp windows.info
vol -f memory.dmp windows.pslist
vol -f memory.dmp windows.filescan | grep -i flag
```

**Full techniques**: [reference/memory.md](reference/memory.md)

## File Carving - Quick Start

```bash
binwalk -e suspicious_file      # Extract embedded files
foremost -i file -o output/     # Carve files

# Fix corrupted header
xxd file | head -10             # Check magic bytes
```

**Full techniques**: [reference/file-analysis.md](reference/file-analysis.md)

## Online Tools

| Tool | URL | Purpose |
|------|-----|---------|
| AperiSolve | aperisolve.com | All-in-one stego |
| StegOnline | stegonline.georgeom.net | Image analysis |
| CyberChef | gchq.github.io/CyberChef | Data transform |

## Reference Files

- **[Steganography](reference/steganography.md)**: Image/audio stego, LSB, AperiSolve
- **[Memory](reference/memory.md)**: Volatility 2/3, process analysis
- **[File Analysis](reference/file-analysis.md)**: Magic bytes, binwalk, password cracking
