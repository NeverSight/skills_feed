---
name: misc-tools
description: >
  Miscellaneous CTF tools for programming challenges, esoteric languages, 
  QR/barcode scanning, and audio/video analysis.
  Trigger: When solving misc challenges, esoteric languages, QR codes, or media files.
license: MIT
metadata:
  author: ctf-arsenal
  version: "1.0"
  category: miscellaneous
---

# Miscellaneous CTF Tools

## When to Use

Load this skill when:
- Solving programming or algorithm challenges
- Decoding esoteric languages (Brainfuck, Malbolge, etc.)
- Scanning QR codes or barcodes
- Analyzing audio/video files
- Working with unconventional challenge types

## Programming Challenges

### Fast Input Parsing

```python
#!/usr/bin/env python3
"""Template for fast I/O in programming challenges"""
import sys

def fast_input():
    """Read all input at once (faster than input())"""
    return sys.stdin.read().strip().split('\n')

def solve():
    """Main solution"""
    lines = fast_input()
    n = int(lines[0])
    
    for i in range(1, n + 1):
        # Process each line
        data = list(map(int, lines[i].split()))
        result = process(data)
        print(result)

def process(data):
    """Process logic here"""
    return sum(data)

if __name__ == "__main__":
    solve()
```

### Common Algorithms

```python
# Binary Search
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# GCD (Greatest Common Divisor)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# LCM (Least Common Multiple)
def lcm(a, b):
    return abs(a * b) // gcd(a, b)

# Prime Check
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Factorial with memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Esoteric Languages

### Brainfuck Interpreter

```python
#!/usr/bin/env python3
"""Brainfuck interpreter"""

def brainfuck(code, input_data=""):
    """Execute Brainfuck code"""
    # Initialize
    tape = [0] * 30000
    ptr = 0
    code_ptr = 0
    output = []
    input_ptr = 0
    
    # Match brackets
    brackets = {}
    stack = []
    for i, cmd in enumerate(code):
        if cmd == '[':
            stack.append(i)
        elif cmd == ']':
            if stack:
                left = stack.pop()
                brackets[left] = i
                brackets[i] = left
    
    # Execute
    while code_ptr < len(code):
        cmd = code[code_ptr]
        
        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[ptr]))
        elif cmd == ',':
            if input_ptr < len(input_data):
                tape[ptr] = ord(input_data[input_ptr])
                input_ptr += 1
        elif cmd == '[':
            if tape[ptr] == 0:
                code_ptr = brackets[code_ptr]
        elif cmd == ']':
            if tape[ptr] != 0:
                code_ptr = brackets[code_ptr]
        
        code_ptr += 1
    
    return ''.join(output)

# Example
code = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
print(brainfuck(code))  # Output: "Hello World!\n"
```

### Common Esoteric Language Patterns

| Language | Detection | Tool |
|----------|-----------|------|
| **Brainfuck** | `+-<>[].,` characters only | `esolang/bf_decode.py` |
| **Malbolge** | Base-85 printable ASCII | Online interpreter |
| **Whitespace** | Only spaces, tabs, newlines | Online interpreter |
| **JSFuck** | `[]()!+` characters only | Browser console |
| **Ook!** | `Ook. Ook? Ook!` | Online interpreter |
| **Piet** | Colorful bitmap image | npiet compiler |

### Online Interpreters

```bash
# Try44 - Multi-language online interpreter
https://tio.run/

# Esoteric.codes
https://esoteric.codes/
```

## QR Codes and Barcodes

### Scan QR Codes

```bash
# Install zbar tools
sudo apt install zbar-tools

# Scan single QR code
zbarimg qrcode.png

# Scan multiple QR codes
zbarimg qr1.png qr2.png qr3.png

# Output to file
zbarimg qrcode.png > output.txt
```

### Scan All QR Codes in Directory

```bash
#!/bin/bash
# Scan all images in directory for QR/barcodes

for file in *.png *.jpg *.jpeg; do
    if [ -f "$file" ]; then
        echo "=== $file ==="
        zbarimg "$file" 2>/dev/null || echo "No code found"
        echo
    fi
done
```

### Generate QR Code

```bash
# Install qrencode
sudo apt install qrencode

# Generate QR code
qrencode -o output.png "Your text here"

# Generate with error correction
qrencode -l H -o output.png "Your text here"
# Levels: L (7%), M (15%), Q (25%), H (30%)
```

### Python QR Code

```python
from PIL import Image
import subprocess

def scan_qr(image_path):
    """Scan QR code from image"""
    result = subprocess.run(
        ['zbarimg', '--quiet', '--raw', image_path],
        capture_output=True, text=True
    )
    return result.stdout.strip()

# Usage
data = scan_qr('qrcode.png')
print(f"QR Code data: {data}")
```

## Audio and Video Analysis

### Audio Spectrogram

```bash
# Generate spectrogram with Sox
sox audio.wav -n spectrogram -o spectrogram.png

# With higher resolution
sox audio.wav -n spectrogram -x 3000 -y 513 -z 120 -w Kaiser -o spectrogram.png

# Extract specific frequency range
sox audio.wav -n spectrogram -o spec.png trim 0 10  # First 10 seconds
```

### Audio Metadata

```bash
# Extract metadata
exiftool audio.mp3
ffprobe audio.mp3

# Extract hidden data from LSB
python3 helpers/audio_lsb.py audio.wav
```

### Video Frame Extraction

```bash
# Extract all frames
ffmpeg -i video.mp4 frames/frame_%04d.png

# Extract every 10th frame
ffmpeg -i video.mp4 -vf "select='not(mod(n\,10))'" -vsync 0 frames/frame_%04d.png

# Extract frame at specific time
ffmpeg -i video.mp4 -ss 00:01:30 -vframes 1 frame.png
```

### DTMF Tone Decoding

```bash
# Install multimon-ng
sudo apt install multimon-ng

# Decode DTMF tones from audio
sox audio.wav -t raw -r 22050 -e signed -b 16 -c 1 - | multimon-ng -t raw -a DTMF /dev/stdin
```

## Encoding and Decoding

### Common Encodings

```python
import base64
import codecs

# Base64
data = base64.b64decode('SGVsbG8gV29ybGQ=')

# Base32
data = base64.b32decode('JBSWY3DPEBLW64TMMQ======')

# Base85
data = base64.b85decode(b'BOu!rD]j7BEbo7')

# Hex
data = bytes.fromhex('48656c6c6f')

# ROT13
data = codecs.decode('Uryyb Jbeyq', 'rot_13')

# URL encoding
from urllib.parse import unquote
data = unquote('Hello%20World')
```

### Multi-Layer Decoding

```python
def auto_decode(data):
    """Try common decodings recursively"""
    import base64
    import binascii
    
    if isinstance(data, bytes):
        try:
            data = data.decode('utf-8')
        except:
            return data
    
    # Try base64
    try:
        decoded = base64.b64decode(data)
        if decoded != data.encode():
            print("[+] Base64 decoded")
            return auto_decode(decoded)
    except:
        pass
    
    # Try hex
    try:
        decoded = bytes.fromhex(data)
        print("[+] Hex decoded")
        return auto_decode(decoded)
    except:
        pass
    
    return data

# Usage
result = auto_decode("NGE2MTY3N2I2MjYxNzM2NTM2MzQ1Zjc0Njg2OTcyNzQ3OTVmNzQ3Nzc2")
print(result)
```

## Quick Reference

| Challenge Type | Tool | Command |
|----------------|------|---------|
| **Brainfuck** | Python | `python3 esolang/bf_decode.py code.bf` |
| **QR Code** | zbar | `zbarimg qrcode.png` |
| **Barcode** | zbar | `zbarimg barcode.jpg` |
| **Spectrogram** | sox | `sox audio.wav -n spectrogram -o spec.png` |
| **DTMF** | multimon-ng | `multimon-ng -a DTMF audio.wav` |
| **Video frames** | ffmpeg | `ffmpeg -i video.mp4 frames/frame_%04d.png` |
| **Base64** | base64 | `base64 -d <<< "SGVsbG8="` |
| **Hex** | xxd | `xxd -r -p hex.txt output.bin` |

## Bundled Resources

### Programming

- `programming/fast_parse.py` - Fast I/O template for competitive programming
- `programming/algorithms.py` - Common algorithms (GCD, LCM, primes)

### Esoteric Languages

- `esolang/bf_decode.py` - Brainfuck interpreter
- `esolang/malbolge_helper.md` - Malbolge reference

### QR and Barcodes

- `qr_barcodes/qr_scan_all.sh` - Batch QR code scanner
- `qr_barcodes/qr_generate.sh` - QR code generator wrapper

### Audio and Video

- `audio_video/spectrogram.sh` - Generate audio spectrogram
- `audio_video/extract_frames.sh` - Extract video frames
- `audio_video/audio_lsb.py` - Audio LSB steganography

## External Tools

```bash
# Esoteric language interpreters
pip install bf  # Brainfuck

# QR/Barcode tools
sudo apt install zbar-tools qrencode

# Audio/Video tools
sudo apt install sox ffmpeg multimon-ng audacity

# Python libraries
pip install qrcode pillow pydub
```

## Keywords

miscellaneous, misc, programming, algorithms, esoteric languages, brainfuck, esolang, QR code, barcode, zbar, audio analysis, spectrogram, DTMF, video analysis, frame extraction, ffmpeg, sox, encoding, decoding, base64, hex, multi-layer decoding, competitive programming
