---
name: ctf-stego
description: Steganography techniques for CTF challenges. Use when data is hidden in images, audio, video, or other media files.
user-invocable: false
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "WebFetch", "WebSearch"]
---

# CTF Steganography

## Quick Start — Try These First

```bash
# Basic analysis
file image.png
exiftool image.png          # EXIF metadata (flags hide here!)
strings image.png | grep -iE "flag|ctf"
binwalk image.png           # Embedded files
xxd image.png | tail        # Data appended after EOF

# Steganography tools
steghide extract -sf image.jpg          # JPEG stego (tries empty password)
steghide extract -sf image.jpg -p ""    # Explicit empty password
zsteg image.png                         # PNG/BMP LSB analysis
stegsolve                               # Visual bit-plane analysis (GUI)
```

## Image Steganography

### LSB (Least Significant Bit)
The most common image stego technique. Data hidden in the least significant bits of pixel values.

```python
from PIL import Image

img = Image.open('image.png')
pixels = list(img.getdata())

# Extract LSB from each channel
bits = ''
for pixel in pixels:
    for channel in pixel[:3]:  # R, G, B
        bits += str(channel & 1)

# Convert bits to bytes
flag = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
print(flag)
```

**Tools:**
- `zsteg` — Automated LSB analysis for PNG/BMP (try `zsteg -a image.png`)
- `stegsolve` — Visual analysis, toggle bit planes
- `Stegano` — Python library: `pip install stegano`

### Pixel Value Encoding
```python
# Values ARE the data (not hidden in LSB)
from PIL import Image
img = Image.open('image.png')
pixels = list(img.getdata())

# Each pixel R value is an ASCII char
flag = ''.join(chr(p[0]) for p in pixels if 32 <= p[0] < 127)

# Or pixel coordinates encode data
# Or specific color pixels spell out a message
```

### Image Format Tricks

**PNG chunks:**
```bash
pngcheck -v image.png        # Validate and list chunks
python3 -c "
import struct
with open('image.png', 'rb') as f:
    data = f.read()
# Look for custom chunks (tEXt, zTXt, iTXt)
idx = data.find(b'tEXt')
if idx > 0:
    print(data[idx:idx+100])
"
```

**JPEG markers:**
```bash
# Data after JPEG EOF marker (FF D9)
python3 -c "
with open('image.jpg', 'rb') as f:
    data = f.read()
eof = data.find(b'\xff\xd9')
if eof > 0 and eof + 2 < len(data):
    print(f'Data after EOF: {data[eof+2:eof+102]!r}')
"
```

**BMP:**
```bash
# BMP has a data offset field — gap between header and pixel data can hide data
xxd image.bmp | head -5
```

**GIF:**
```bash
# GIF frames may contain hidden data
ffmpeg -i image.gif frame_%03d.png  # Extract all frames
identify -verbose image.gif          # Frame details
```

### Image Dimension Tricks

**Wrong dimensions in header:**
```python
# PNG: Fix height to reveal hidden rows
import struct, zlib

with open('image.png', 'rb') as f:
    data = bytearray(f.read())

# PNG IHDR chunk starts at offset 16 (width at 16, height at 20)
# Try increasing height
struct.pack_into('>I', data, 20, 1000)  # Set height to 1000

with open('fixed.png', 'wb') as f:
    # Recalculate IHDR CRC
    ihdr_data = data[12:29]
    crc = zlib.crc32(ihdr_data) & 0xffffffff
    struct.pack_into('>I', data, 29, crc)
    f.write(data)
```

### Steghide (JPEG/WAV/BMP/AU)
```bash
steghide extract -sf file.jpg -p "password"
steghide info file.jpg                      # Check if data is embedded

# Brute force password
stegcracker file.jpg wordlist.txt
# Or use stegseek (much faster)
stegseek file.jpg wordlist.txt
```

### Visual Steganography
- Flags as tiny/low-contrast text in images
- Black text on dark background, white on light
- Check ALL corners and edges at full resolution
- Profile pictures and avatars are common hiding spots
- Zoom in on what looks like solid color areas

## Audio Steganography

### Spectrogram Analysis
```bash
# Generate spectrogram image
sox audio.wav -n spectrogram -o spectrogram.png

# Or use Audacity: View → Spectrogram
# Look for text/images drawn in frequency domain
```

### SSTV (Slow-Scan Television)
```bash
# Decode SSTV signal from audio
qsstv                    # GUI decoder
# Or sstv Python package
pip install sstv
sstv -d audio.wav -o output.png
```

### DTMF Tones
```bash
# Phone keypad tones
multimon-ng -t wav -a DTMF audio.wav
# Or via sox + multimon-ng:
sox audio.wav -t raw -r 22050 -e signed-integer -b 16 -c 1 - | multimon-ng -t raw -a DTMF -
```

### Audio LSB
```python
import wave
import struct

wav = wave.open('audio.wav', 'rb')
frames = wav.readframes(wav.getnframes())
samples = struct.unpack(f'<{len(frames)//2}h', frames)

# Extract LSB from samples
bits = ''.join(str(s & 1) for s in samples)
data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
print(data[:100])
```

### Morse Code
```bash
# Visual: look at waveform for long/short patterns
# Audio: listen for dots and dashes
# Automated: use online morse decoder or:
pip install morse-audio-decoder
```

## Text/Data Steganography

### Whitespace Stego
```bash
# Zero-width characters in text
python3 -c "
with open('text.txt', 'rb') as f:
    data = f.read()
# Zero-width space: U+200B, Zero-width joiner: U+200D
for b in data:
    if b in [0xe2]:  # Start of multi-byte UTF-8
        print(f'Found zero-width char at position')
"

# snow tool for whitespace stego
snow -C -p "password" stego.txt
```

### Unicode Stego
- Homoglyph substitution (Cyrillic а vs Latin a)
- Invisible Unicode characters between visible text
- Variation selectors and combining characters

### File Concatenation / Polyglots
```bash
# Multiple files concatenated
binwalk suspicious_file        # Find embedded files
foremost suspicious_file       # Carve out files

# ZIP at end of image
unzip image.png                # Works if ZIP appended after image data

# PDF + ZIP polyglot
# File is valid as both PDF and ZIP
```

## Network Steganography

### PCAP Hidden Data
- DNS queries encoding data in subdomain labels
- ICMP payloads carrying hidden messages
- TCP sequence numbers encoding data
- HTTP headers with encoded data
- TLS certificate fields

### DNS Exfiltration
```bash
tshark -r capture.pcap -Y "dns.qry.name" -T fields -e dns.qry.name | \
    sed 's/\.example\.com//' | tr -d '\n' | base64 -d
```

## Common Patterns

| Clue | Technique |
|------|-----------|
| "Look closer" / "More than meets the eye" | LSB or visual stego |
| Image looks normal but file is huge | Embedded/appended data |
| Audio with static/noise sections | Spectrogram or SSTV |
| "Password protected" | Steghide with password |
| PNG with wrong colors or glitches | Bit plane analysis |
| Text file with trailing whitespace | Whitespace stego |
| Challenge says "nothing to see here" | Definitely stego |
