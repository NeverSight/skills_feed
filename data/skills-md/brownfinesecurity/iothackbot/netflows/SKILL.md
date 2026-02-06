---
name: netflows
description: Network flow extractor that analyzes pcap/pcapng files to identify outbound connections with automatic DNS hostname resolution. Use when you need to enumerate network destinations, identify what hosts a device communicates with, or map IP addresses to hostnames from packet captures.
---

# NetFlows - Network Flow Extractor with DNS Resolution

You are helping the user extract and analyze network flows from packet capture files using the netflows tool.

## Tool Overview

NetFlows analyzes pcap/pcapng files to:
- Extract unique TCP and UDP flows (destination IP:port pairs)
- Build a DNS resolution table from DNS responses in the capture
- Automatically resolve IP addresses to hostnames where possible
- Filter flows by source IP address
- Generate a summary of all network destinations contacted

This is particularly useful for IoT device analysis to understand what external services a device communicates with.

## Instructions

When the user asks to analyze network flows, extract destinations, or identify what hosts a device talks to:

1. **Gather requirements**:
   - Get the pcap/pcapng file path(s)
   - Ask if they want to filter by a specific source IP (e.g., the IoT device's IP)
   - Determine preferred output format

2. **Execute the analysis**:
   - Use the netflows command from the iothackbot bin directory

3. **Interpret results**:
   - Explain resolved hostnames and their significance
   - Note any unresolved IPs that may need further investigation
   - Highlight interesting patterns (cloud services, P2P connections, etc.)

## Usage

### Basic Analysis
Analyze a pcap file showing all flows:
```bash
netflows capture.pcap
```

### Filter by Source IP
Extract flows from a specific device:
```bash
netflows capture.pcap --source-ip 192.168.1.100
```

### Multiple Files
Analyze multiple capture files:
```bash
netflows capture1.pcap capture2.pcapng
```

### Output Formats
```bash
# Human-readable colored output (default)
netflows capture.pcap --format text

# Machine-readable JSON
netflows capture.pcap --format json

# Minimal output - just hostname:port list
netflows capture.pcap --format quiet
```

## Parameters

**Input:**
- `pcap_files`: One or more pcap/pcapng files to analyze (required)

**Filtering:**
- `-s, --source-ip`: Filter flows originating from this IP address

**Output:**
- `--format text|json|quiet`: Output format (default: text)
- `-v, --verbose`: Enable verbose output

## Examples

Analyze IoT device traffic:
```bash
netflows iot-capture.pcap --source-ip 192.168.1.50
```

Get just the flow list for scripting:
```bash
netflows capture.pcap -s 10.0.0.100 --format quiet
```

JSON output for parsing:
```bash
netflows capture.pcap --format json | jq '.data[].flow_summary'
```

## Output Information

**Text format includes:**
- DNS mappings discovered (IP -> hostname)
- TCP flows with hostname resolution status
- UDP flows with hostname resolution status
- Consolidated flow summary (hostname:port or ip:port)

**JSON format includes:**
- `dns_mappings`: Dictionary of IP to hostname mappings
- `tcp_flows`: List of TCP flow objects with hostname, ip, port
- `udp_flows`: List of UDP flow objects with hostname, ip, port
- `flow_summary`: List of "hostname:port" or "ip:port" strings
- `dns_queries`: List of DNS domains queried
- `total_packets`: Number of packets analyzed

## Use Cases

1. **IoT Device Profiling**: Identify all cloud services and endpoints an IoT device communicates with
2. **Network Forensics**: Enumerate destinations contacted during an incident
3. **Privacy Analysis**: Discover telemetry and tracking endpoints
4. **Firewall Rule Creation**: Generate allowlist/blocklist of endpoints
5. **Malware Analysis**: Identify C2 servers and exfiltration destinations

## Important Notes

- The tool resolves hostnames using DNS responses found within the same pcap file
- IPs without corresponding DNS lookups in the capture will show as "unresolved"
- Supports both pcap and pcapng formats
- Does not require elevated privileges (unlike live capture tools)
- Large pcap files may take time to process
