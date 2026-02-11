---
name: forensics-tools
description: >
  Digital forensics tools for file carving, steganography detection, PCAP analysis,
  and entropy scanning in CTF challenges.
  Trigger: When analyzing files, steganography, PCAP traffic, or hidden data.
license: MIT
metadata:
  author: ctf-arsenal
  version: "1.0"
  category: forensics
---

# Digital Forensics Tools

## When to Use

Load this skill when:
- Analyzing suspicious files or unknown file formats
- Extracting hidden data or carved files
- Detecting steganography in images/audio
- Analyzing network PCAP files
- Scanning for high-entropy (encrypted/compressed) data
- Working with file signatures and magic bytes

## File Analysis and Carving

### Binwalk - Extract Embedded Files

```bash
# Scan for embedded files
binwalk suspicious.bin

# Extract all found files
binwalk -e suspicious.bin

# Extract with signature scan
binwalk --dd='.*' suspicious.bin

# Scan for specific file types
binwalk --signature image.png
```

### Common File Signatures (Magic Bytes)

| File Type | Signature (Hex) | Signature (ASCII) |
|-----------|----------------|-------------------|
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` |
| **JPEG** | `FF D8 FF E0/E1` | `ÿØÿà` |
| **GIF** | `47 49 46 38 37/39 61` | `GIF87a/GIF89a` |
| **ZIP** | `50 4B 03 04` | `PK..` |
| **PDF** | `25 50 44 46` | `%PDF` |
| **ELF** | `7F 45 4C 46` | `.ELF` |
| **RAR** | `52 61 72 21 1A 07` | `Rar!..` |

### Manual File Carving with dd

```bash
# Extract bytes from offset to end
dd if=input.bin of=output.bin skip=1024 bs=1

# Extract specific byte range
dd if=input.bin of=output.bin skip=1024 count=2048 bs=1

# Find PNG signature and extract
grep --only-matching --byte-offset --binary --text $'\x89PNG' file.bin
```

### Strings Analysis

```bash
# Extract ASCII strings
strings suspicious.bin

# Extract with minimum length
strings -n 10 suspicious.bin

# Search for specific patterns
strings suspicious.bin | grep -i "flag\|password\|key"

# Unicode strings (16-bit little-endian)
strings -el suspicious.bin

# With file offsets
strings -t x suspicious.bin
```

## Steganography Detection

### Image Steganography

```python
#!/usr/bin/env python3
"""Quick steganography checks"""
from PIL import Image
import numpy as np

def check_lsb(image_path):
    """Check LSB (Least Significant Bit) steganography"""
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # Extract LSBs
    lsb = pixels & 1
    
    # Visualize LSBs (amplify for visibility)
    lsb_img = Image.fromarray((lsb * 255).astype('uint8'))
    lsb_img.save('lsb_analysis.png')
    print("[+] LSB analysis saved to lsb_analysis.png")

def extract_lsb_data(image_path):
    """Extract data from LSBs"""
    img = Image.open(image_path)
    pixels = np.array(img).flatten()
    
    # Extract LSBs as bits
    bits = ''.join([str(p & 1) for p in pixels])
    
    # Convert to bytes
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            data.append(int(byte, 2))
    
    return bytes(data)

# Usage
check_lsb('suspicious.png')
data = extract_lsb_data('suspicious.png')
print(data[:100])  # First 100 bytes
```

### Common Steganography Tools

```bash
# Steghide (JPEG, BMP, WAV, AU)
steghide info suspicious.jpg
steghide extract -sf suspicious.jpg

# StegSolve (GUI tool for image analysis)
java -jar stegsolve.jar

# Zsteg (PNG, BMP)
zsteg suspicious.png
zsteg -a suspicious.png  # All checks

# Exiftool (metadata analysis)
exiftool suspicious.jpg
exiftool -all suspicious.jpg

# Foremost (file carving)
foremost -i suspicious.bin -o output/
```

### Audio Steganography

```bash
# Spectogram analysis with Sox
sox audio.wav -n spectrogram -o spectro.png

# Or with Python
python3 helpers/spectrogram.py audio.wav

# Audacity (GUI)
# File -> Open -> Analyze -> Plot Spectrum
```

## Network Forensics

### PCAP Analysis with tshark

```bash
# Basic statistics
tshark -r capture.pcap -q -z io,phs

# Extract HTTP objects
tshark -r capture.pcap --export-objects http,output/

# Filter by protocol
tshark -r capture.pcap -Y "http"
tshark -r capture.pcap -Y "dns"
tshark -r capture.pcap -Y "tcp.port == 80"

# Extract HTTP requests
tshark -r capture.pcap -Y "http.request" -T fields -e http.request.full_uri

# Extract HTTP POST data
tshark -r capture.pcap -Y "http.request.method == POST" -T fields -e http.file_data

# Follow TCP stream
tshark -r capture.pcap -z follow,tcp,ascii,0

# Extract files
tshark -r capture.pcap --export-objects http,extracted/
tshark -r capture.pcap --export-objects smb,extracted/
```

### Extract HTTP Traffic

```python
#!/usr/bin/env python3
"""Extract HTTP traffic from PCAP"""
from scapy.all import *

def extract_http(pcap_file):
    """Extract HTTP requests and responses"""
    packets = rdpcap(pcap_file)
    
    for pkt in packets:
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            payload = pkt[Raw].load
            
            # Check for HTTP
            if payload.startswith(b'GET') or payload.startswith(b'POST'):
                print("[HTTP Request]")
                print(payload.decode('latin-1', errors='ignore'))
                print("-" * 60)
            
            elif payload.startswith(b'HTTP/'):
                print("[HTTP Response]")
                print(payload.decode('latin-1', errors='ignore')[:200])
                print("-" * 60)

extract_http('capture.pcap')
```

### Reconstruct Files from PCAP

```bash
# NetworkMiner (Windows/Linux with Mono)
mono NetworkMiner.exe --nogui -r capture.pcap -o output/

# tcpflow - Reconstruct TCP sessions
tcpflow -r capture.pcap -o output/

# Wireshark export
# File -> Export Objects -> HTTP/SMB/TFTP
```

## Entropy Analysis

### Detect Encrypted/Compressed Data

```python
#!/usr/bin/env python3
"""Scan file for high-entropy regions"""
import math
from collections import Counter

def calculate_entropy(data):
    """Calculate Shannon entropy"""
    if not data:
        return 0
    
    entropy = 0
    counter = Counter(data)
    length = len(data)
    
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy

def scan_entropy(filename, block_size=256):
    """Scan file for high-entropy blocks"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Scanning {filename} for high-entropy regions...")
    print(f"Block size: {block_size} bytes")
    print("-" * 60)
    
    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        if len(block) < block_size // 2:
            continue
        
        entropy = calculate_entropy(block)
        
        # High entropy (> 7.5) indicates encryption/compression
        if entropy > 7.5:
            print(f"Offset 0x{i:08x}: Entropy = {entropy:.4f} [HIGH]")

# Usage
scan_entropy('suspicious.bin', block_size=512)
```

## Memory Forensics

### Volatility (if applicable in CTF)

```bash
# Identify profile
volatility -f memory.dmp imageinfo

# List processes
volatility -f memory.dmp --profile=Win7SP1x64 pslist

# Dump process memory
volatility -f memory.dmp --profile=Win7SP1x64 memdump -p 1234 -D output/

# Extract files
volatility -f memory.dmp --profile=Win7SP1x64 filescan
volatility -f memory.dmp --profile=Win7SP1x64 dumpfiles -Q 0x000000003e8b6f20 -D output/
```

## Quick Reference

| Task | Tool | Command |
|------|------|---------|
| **File carving** | binwalk | `binwalk -e file.bin` |
| **Strings** | strings | `strings -n 10 file.bin` |
| **Image LSB** | zsteg | `zsteg -a image.png` |
| **JPEG steg** | steghide | `steghide extract -sf image.jpg` |
| **Metadata** | exiftool | `exiftool image.jpg` |
| **PCAP HTTP** | tshark | `tshark -r file.pcap --export-objects http,out/` |
| **TCP stream** | tshark | `tshark -r file.pcap -z follow,tcp,ascii,0` |
| **Spectrogram** | sox | `sox audio.wav -n spectrogram -o spec.png` |
| **Entropy** | custom | `python3 helpers/entropy_scan.py file.bin` |

## Bundled Resources

### File Analysis

- `file_analysis/binwalk_extract.sh` - Wrapper for binwalk extraction

### Steganography

- `steganography/steg_quickcheck.py` - Automated steg detection
  - LSB analysis
  - Metadata extraction
  - Entropy visualization

### Network Forensics

- `network_forensics/pcap_extract_http.py` - Extract HTTP from PCAP
- `network_forensics/pcap_extract_files.py` - Reconstruct files from PCAP

### Helpers

- `helpers/entropy_scan.py` - Scan files for high-entropy regions
- `helpers/file_signature_check.py` - Verify file signatures
- `helpers/strings_smart.py` - Enhanced string extraction

## External Tools

```bash
# Install common forensics tools
sudo apt install binwalk foremost steghide exiftool

# Python tools
pip install pillow numpy scapy

# Specialized tools
# - StegSolve: https://github.com/zardus/ctf-tools (Java-based)
# - Audacity: https://www.audacityteam.org/ (audio analysis)
# - Wireshark: https://www.wireshark.org/ (PCAP GUI analysis)
```

## Keywords

forensics, digital forensics, file carving, binwalk, steganography, steg, LSB, least significant bit, PCAP, packet capture, network forensics, tshark, wireshark, entropy analysis, strings, metadata, exiftool, file signatures, magic bytes, audio steganography, spectrogram, image analysis, data extraction, hidden data
