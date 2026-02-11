---
name: crypto-tools
description: >
  Cryptography tools for RSA attacks, classical ciphers, XOR analysis,
  and frequency analysis in CTF challenges.
  Trigger: When solving crypto challenges, RSA, XOR, Caesar, or Vigenere ciphers.
license: MIT
metadata:
  author: ctf-arsenal
  version: "1.0"
  category: cryptography
---

# Cryptography Tools and Techniques

## When to Use

Load this skill when:
- Solving cryptography CTF challenges
- Attacking weak RSA implementations
- Breaking classical ciphers (Caesar, Vigenere, XOR)
- Performing frequency analysis
- Analyzing encrypted data with unknown algorithms

## RSA Attacks

### Small Exponent Attack (e=3)

```python
#!/usr/bin/env python3
"""Attack RSA with small public exponent"""
import gmpy2

def small_e_attack(c, e, n):
    """
    If e is small (typically e=3) and message is short,
    we can take the e-th root directly
    """
    # Try taking e-th root
    for k in range(1000):
        m, exact = gmpy2.iroot(c + k * n, e)
        if exact:
            return int(m)
    return None

# Example
c = 12345678901234567890
e = 3
n = 98765432109876543210
m = small_e_attack(c, e, n)
if m:
    print(f"Message: {bytes.fromhex(hex(m)[2:])}")
```

### Wiener's Attack (Small Private Exponent)

```python
#!/usr/bin/env python3
"""Wiener's attack for small d"""
from fractions import Fraction

def wiener_attack(e, n):
    """
    Attack RSA when d < N^0.25
    Returns private key d if vulnerable
    """
    convergents = continued_fraction(Fraction(e, n))
    
    for k, d in convergents:
        if k == 0:
            continue
        
        phi = (e * d - 1) // k
        # Check if phi is valid
        s = n - phi + 1
        discr = s * s - 4 * n
        
        if discr >= 0:
            t = gmpy2.isqrt(discr)
            if t * t == discr and (s + t) % 2 == 0:
                return d
    return None

def continued_fraction(frac):
    """Generate continued fraction convergents"""
    convergents = []
    n, d = 0, 1
    
    for _ in range(1000):
        a = int(frac)
        convergents.append((n + a * 1, d + a * 1))
        
        frac = frac - a
        if frac == 0:
            break
        frac = 1 / frac
        
    return convergents
```

### Common Modulus Attack

```python
#!/usr/bin/env python3
"""Attack RSA when same message encrypted with different e, same N"""
import gmpy2

def common_modulus_attack(c1, c2, e1, e2, n):
    """
    Given:
    c1 = m^e1 mod n
    c2 = m^e2 mod n
    And gcd(e1, e2) = 1
    Recover m without knowing phi(n)
    """
    # Extended Euclidean algorithm
    gcd, s, t = gmpy2.gcdext(e1, e2)
    
    if gcd != 1:
        raise ValueError("e1 and e2 must be coprime")
    
    # Handle negative exponents
    if s < 0:
        c1 = gmpy2.invert(c1, n)
        s = -s
    if t < 0:
        c2 = gmpy2.invert(c2, n)
        t = -t
    
    m = (pow(c1, s, n) * pow(c2, t, n)) % n
    return m
```

### Fermat's Factorization (Close Primes)

```python
#!/usr/bin/env python3
"""Fermat factorization when p and q are close"""
import gmpy2

def fermat_factor(n):
    """
    Factor n when p and q are close: |p - q| is small
    Much faster than trial division
    """
    a = gmpy2.isqrt(n) + 1
    b2 = a * a - n
    
    for _ in range(1000000):
        b = gmpy2.isqrt(b2)
        if b * b == b2:
            p = a + b
            q = a - b
            return int(p), int(q)
        a += 1
        b2 = a * a - n
    
    return None, None

# Example
n = 123456789012345678901234567890
p, q = fermat_factor(n)
if p and q:
    print(f"p = {p}")
    print(f"q = {q}")
```

### RSA Common Template

```python
#!/usr/bin/env python3
"""Standard RSA operations"""
import gmpy2

def rsa_decrypt(c, d, n):
    """Decrypt ciphertext with private key"""
    m = pow(c, d, n)
    return m

def rsa_encrypt(m, e, n):
    """Encrypt message with public key"""
    c = pow(m, e, n)
    return c

def factor_n(p, q):
    """Compute n from primes"""
    return p * q

def compute_phi(p, q):
    """Compute Euler's totient"""
    return (p - 1) * (q - 1)

def compute_d(e, phi):
    """Compute private exponent from public exponent"""
    return int(gmpy2.invert(e, phi))

# Full RSA key recovery from factors
def recover_key_from_factors(p, q, e):
    """Given p, q, e, compute d"""
    n = factor_n(p, q)
    phi = compute_phi(p, q)
    d = compute_d(e, phi)
    return d, n

# Example
p = 1234567890123456789
q = 9876543210987654321
e = 65537

d, n = recover_key_from_factors(p, q, e)
print(f"n = {n}")
print(f"d = {d}")

# Decrypt
c = 12345678901234567890
m = rsa_decrypt(c, d, n)
print(f"Message: {m}")
```

## Classical Ciphers

### Caesar Cipher

```python
#!/usr/bin/env python3
"""Caesar cipher brute force"""

def caesar_decrypt(ciphertext, shift):
    """Decrypt Caesar cipher with given shift"""
    result = ""
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

def caesar_bruteforce(ciphertext):
    """Try all 26 possible shifts"""
    print("Caesar Cipher Bruteforce:")
    for shift in range(26):
        plaintext = caesar_decrypt(ciphertext, shift)
        print(f"Shift {shift:2d}: {plaintext}")

# Example
ciphertext = "Khoor Zruog"
caesar_bruteforce(ciphertext)
```

### Vigenere Cipher

```python
#!/usr/bin/env python3
"""Vigenere cipher attack"""

def vigenere_decrypt(ciphertext, key):
    """Decrypt Vigenere cipher"""
    result = ""
    key_index = 0
    key = key.upper()
    
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    
    return result

def guess_key_length(ciphertext):
    """Use Index of Coincidence to guess key length"""
    ic_values = []
    for key_len in range(1, 21):
        ic_sum = 0
        for i in range(key_len):
            substring = ciphertext[i::key_len]
            ic_sum += index_of_coincidence(substring)
        ic_values.append((key_len, ic_sum / key_len))
    
    # Sort by IC (higher is better, ~0.065 for English)
    ic_values.sort(key=lambda x: x[1], reverse=True)
    return ic_values[0][0]

def index_of_coincidence(text):
    """Calculate Index of Coincidence"""
    text = ''.join(c.upper() for c in text if c.isalpha())
    n = len(text)
    if n <= 1:
        return 0
    
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic
```

### XOR Cipher

```python
#!/usr/bin/env python3
"""XOR cipher attacks"""

def xor_single_byte(data, key):
    """XOR data with single-byte key"""
    return bytes([b ^ key for b in data])

def xor_bruteforce_single_byte(ciphertext):
    """Bruteforce single-byte XOR key"""
    results = []
    for key in range(256):
        plaintext = xor_single_byte(ciphertext, key)
        score = english_score(plaintext)
        results.append((key, score, plaintext))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]  # Top 5 candidates

def english_score(data):
    """Score text based on English letter frequency"""
    try:
        text = data.decode('ascii', errors='ignore').lower()
    except:
        return 0
    
    freq = {
        'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
        'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, ' ': 13.00,
    }
    
    score = sum(freq.get(c, 0) for c in text)
    return score / len(text) if len(text) > 0 else 0

def xor_repeating_key(data, key):
    """XOR data with repeating key"""
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def find_xor_key_length(ciphertext):
    """Find XOR key length using Hamming distance"""
    distances = []
    
    for keysize in range(2, 41):
        chunks = [ciphertext[i:i+keysize] for i in range(0, len(ciphertext), keysize)]
        if len(chunks) < 4:
            continue
        
        # Compare first 4 chunks
        dist = 0
        comparisons = 0
        for i in range(3):
            dist += hamming_distance(chunks[i], chunks[i+1])
            comparisons += 1
        
        normalized_dist = dist / comparisons / keysize
        distances.append((keysize, normalized_dist))
    
    distances.sort(key=lambda x: x[1])
    return distances[0][0]

def hamming_distance(b1, b2):
    """Calculate Hamming distance between two byte strings"""
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))
```

## Frequency Analysis

```python
#!/usr/bin/env python3
"""Frequency analysis for ciphertexts"""
from collections import Counter

def frequency_analysis(text):
    """Analyze letter frequency in text"""
    # Clean text
    text = ''.join(c.upper() for c in text if c.isalpha())
    
    # Count frequencies
    freq = Counter(text)
    total = len(text)
    
    # Calculate percentages
    freq_percent = {char: (count / total) * 100 
                    for char, count in freq.items()}
    
    # Sort by frequency
    sorted_freq = sorted(freq_percent.items(), 
                        key=lambda x: x[1], reverse=True)
    
    # English reference frequencies
    english_freq = {
        'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51,
        'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09,
    }
    
    print("Frequency Analysis:")
    print("-" * 40)
    print("Char | Count | % | English %")
    print("-" * 40)
    for char, percent in sorted_freq[:10]:
        count = freq[char]
        eng = english_freq.get(char, 0)
        print(f"  {char}  | {count:5d} | {percent:5.2f} | {eng:5.2f}")
```

## Quick Reference

| Attack | Condition | Tool |
|--------|-----------|------|
| **Small e** | e=3, short message | `rsa/small_e.py` |
| **Wiener** | d < N^0.25 | `rsa/wiener.py` |
| **Common Modulus** | Same N, diff e | `rsa/common_modulus.py` |
| **Fermat** | \|p-q\| small | `rsa/fermat.py` |
| **Caesar** | Shift cipher | `classic/caesar.py` (bruteforce 26 shifts) |
| **Vigenere** | Repeating key | `classic/vigenere.py` (IC analysis) |
| **XOR Single** | 1-byte key | `classic/xor_single_byte.py` |
| **XOR Repeating** | Multi-byte key | `classic/xor_repeating_key.py` |

## Bundled Resources

### RSA Tools

- `rsa/rsa_common.py` - Common RSA operations (encrypt/decrypt/factor)
- `rsa/small_e.py` - Small public exponent attack (e=3)
- `rsa/wiener.py` - Wiener's attack for small d
- `rsa/common_modulus.py` - Common modulus attack
- `rsa/fermat.py` - Fermat factorization for close primes

### Classical Ciphers

- `classic/caesar.py` - Caesar cipher bruteforce
- `classic/vigenere.py` - Vigenere cipher with IC analysis
- `classic/xor_single_byte.py` - Single-byte XOR bruteforce
- `classic/xor_repeating_key.py` - Multi-byte XOR key recovery
- `classic/frequency_analysis.py` - Letter frequency analysis tool

## External Tools

```bash
# RsaCtfTool (comprehensive RSA attack suite)
git clone https://github.com/Ganapati/RsaCtfTool.git
python3 RsaCtfTool.py -n <N> -e <E> --private

# CyberChef (web-based encoding/crypto tool)
# https://gchq.github.io/CyberChef/

# FactorDB (check if N is already factored)
# http://factordb.com/
```

## Keywords

cryptography, crypto, RSA, RSA attacks, small exponent, wiener attack, common modulus, fermat factorization, classical cipher, caesar cipher, vigenere cipher, XOR, XOR cipher, frequency analysis, index of coincidence, public key cryptography, modular arithmetic, CTF crypto
