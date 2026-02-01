---
name: networking
description: Analyzes network traffic and exploits protocols. Use when working with PCAP files, Wireshark captures, packet analysis, protocol exploitation, traffic forensics, or data exfiltration detection.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Networking Skill

## Quick Workflow

```
Progress:
- [ ] Get protocol overview (tshark -z io,phs)
- [ ] Search strings for flag pattern
- [ ] Export HTTP/SMB objects
- [ ] Follow interesting streams
- [ ] Check for credentials/exfiltration
- [ ] Extract flag
```

## Quick Analysis Pipeline

```bash
# 1. Basic info
capinfos capture.pcap
file capture.pcap

# 2. Protocol hierarchy
tshark -r capture.pcap -z io,phs

# 3. Conversations
tshark -r capture.pcap -z conv,tcp

# 4. Quick string search
strings capture.pcap | grep -i flag
tshark -r capture.pcap -Y "frame contains flag"
```

## Reference Files

| Topic | Reference |
|-------|-----------|
| Wireshark Filters & tshark | [reference/wireshark.md](reference/wireshark.md) |
| Protocol Analysis (HTTP, DNS, FTP, etc.) | [reference/protocols.md](reference/protocols.md) |
| CTF Patterns & Attacks | [reference/ctf-patterns.md](reference/ctf-patterns.md) |

## Tools Quick Reference

| Tool | Purpose | Install |
|------|---------|---------|
| Wireshark | GUI packet analysis | `brew install wireshark` |
| tshark | CLI packet analysis | `brew install wireshark` |
| tcpdump | Packet capture | Built-in |
| tcpflow | TCP stream extraction | `brew install tcpflow` |
| nmap | Port scanning | `brew install nmap` |
| masscan | Fast port scanning | `brew install masscan` |
| scapy | Packet manipulation | `pip install scapy` |

## Scapy Quick Reference

```python
from scapy.all import *

# Read PCAP
packets = rdpcap('capture.pcap')

# Filter packets
http_packets = [p for p in packets if TCP in p and p[TCP].dport == 80]

# Extract data
for p in packets:
    if Raw in p:
        print(p[Raw].load)
```
