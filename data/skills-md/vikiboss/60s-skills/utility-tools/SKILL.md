---
name: utility-tools
description: 提供实用工具功能，包括IP地址查询、文本翻译、二维码生成、哈希计算、网页元数据提取、域名WHOIS查询和密码生成。Use when users need translation, IP lookup, QR codes, hashing, domain info, or password generation.
license: MIT
metadata:
  author: vikiboss
  version: "1.0"
  api_base: https://60s.viki.moe/v2
  tags:
    - utility
    - translation
    - tools
    - security
---

# Utility Tools Skill

This skill provides various utility functions for common tasks like translation, IP lookup, QR code generation, and more.

## Available Tools

1. **IP Address Lookup** - Get location and ISP info for any IP
2. **Text Translation** - Translate between multiple languages
3. **QR Code Generation** - Create QR codes for any text/URL
4. **Hash Calculation** - Calculate MD5, SHA1, SHA256, SHA512
5. **OG Metadata Extraction** - Extract Open Graph metadata from URLs
6. **WHOIS Lookup** - Domain registration information
7. **Password Generation** - Generate secure random passwords

## API Endpoints

| Tool | Endpoint | Method |
|------|----------|--------|
| IP Lookup | `/v2/ip` | GET |
| Translation | `/v2/fanyi` | POST |
| QR Code | `/v2/qrcode` | GET |
| Hash | `/v2/hash` | POST |
| OG Metadata | `/v2/og` | POST |
| WHOIS | `/v2/whois` | GET |
| Password | `/v2/password` | GET |

## 1. IP Address Lookup

```python
import requests

# Lookup specific IP
response = requests.get('https://60s.viki.moe/v2/ip', params={'ip': '8.8.8.8'})
ip_info = response.json()

print(f"IP: {ip_info['ip']}")
print(f"Location: {ip_info['location']}")
print(f"ISP: {ip_info['isp']}")

# Get your own IP info (no params)
my_ip = requests.get('https://60s.viki.moe/v2/ip').json()
```

## 2. Text Translation

```python
# Translate text
data = {
    'text': 'Hello World',
    'from': 'en',  # or 'auto' for auto-detection
    'to': 'zh'     # target language
}

response = requests.post('https://60s.viki.moe/v2/fanyi', json=data)
translation = response.json()

print(f"Original: {translation['text']}")
print(f"Translated: {translation['result']}")
print(f"From: {translation['from']} To: {translation['to']}")
```

**Supported Languages:**
- `zh` - Chinese
- `en` - English
- `ja` - Japanese
- `ko` - Korean
- `fr` - French
- `de` - German
- `es` - Spanish
- `ru` - Russian
- And more...

```python
# Get supported languages
response = requests.post('https://60s.viki.moe/v2/fanyi/langs')
languages = response.json()
```

## 3. QR Code Generation

```python
# Generate QR code
params = {
    'text': 'https://github.com/vikiboss/60s',
    'size': 300  # pixels, default 200, min 50, max 1000
}

response = requests.get('https://60s.viki.moe/v2/qrcode', params=params)

# Save the QR code image
with open('qrcode.png', 'wb') as f:
    f.write(response.content)
```

## 4. Hash Calculation

```python
# Calculate hash
data = {
    'text': 'Hello World',
    'algorithm': 'md5'  # md5, sha1, sha256, sha512
}

response = requests.post('https://60s.viki.moe/v2/hash', json=data)
result = response.json()

print(f"Algorithm: {result['algorithm']}")
print(f"Hash: {result['hash']}")
```

## 5. OG Metadata Extraction

```python
# Extract Open Graph metadata from URL
data = {'url': 'https://github.com/vikiboss/60s'}

response = requests.post('https://60s.viki.moe/v2/og', json=data)
metadata = response.json()

print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description']}")
print(f"Image: {metadata['image']}")
print(f"URL: {metadata['url']}")
```

## 6. WHOIS Lookup

```python
# Domain WHOIS information
params = {'domain': 'github.com'}

response = requests.get('https://60s.viki.moe/v2/whois', params=params)
whois_info = response.json()

print(f"Domain: {whois_info['domain']}")
print(f"Registrar: {whois_info['registrar']}")
print(f"Created: {whois_info['created_date']}")
print(f"Expires: {whois_info['expiration_date']}")
```

## 7. Password Generation

```python
# Generate secure password
params = {
    'length': 16,        # 6-128
    'numbers': True,     # include numbers
    'lowercase': True,   # include lowercase
    'uppercase': True,   # include uppercase
    'symbols': True      # include special characters
}

response = requests.get('https://60s.viki.moe/v2/password', params=params)
password_data = response.json()

print(f"Password: {password_data['password']}")
print(f"Strength: {password_data['strength']}")
```

## Example Use Cases

### Multi-language Chatbot

```python
def auto_translate(text, target_lang='zh'):
    data = {
        'text': text,
        'from': 'auto',
        'to': target_lang
    }
    response = requests.post('https://60s.viki.moe/v2/fanyi', json=data)
    return response.json()['result']

# Usage
user_input = "Hello, how are you?"
translated = auto_translate(user_input, 'zh')
print(translated)  # 你好，你好吗？
```

### URL Shortener with QR Code

```python
def create_qr_for_url(url, size=200):
    params = {'text': url, 'size': size}
    response = requests.get('https://60s.viki.moe/v2/qrcode', params=params)
    return response.content

# Generate and save
qr_image = create_qr_for_url('https://example.com')
with open('url_qr.png', 'wb') as f:
    f.write(qr_image)
```

### Security Tools

```python
def check_password_hash(password):
    """Generate multiple hashes for password"""
    algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    hashes = {}
    
    for algo in algorithms:
        data = {'text': password, 'algorithm': algo}
        response = requests.post('https://60s.viki.moe/v2/hash', json=data)
        hashes[algo] = response.json()['hash']
    
    return hashes

def generate_secure_password(length=16):
    params = {
        'length': length,
        'numbers': True,
        'lowercase': True,
        'uppercase': True,
        'symbols': True
    }
    response = requests.get('https://60s.viki.moe/v2/password', params=params)
    return response.json()['password']
```

### Website Preview Card

```python
def get_link_preview(url):
    """Get rich preview data for a URL"""
    data = {'url': url}
    response = requests.post('https://60s.viki.moe/v2/og', json=data)
    og = response.json()
    
    preview = f"""
    📄 {og['title']}
    📝 {og['description']}
    🖼️ {og['image']}
    🔗 {og['url']}
    """
    return preview
```

## Best Practices

1. **Translation**: Use 'auto' for source language when unsure
2. **QR Codes**: Keep size between 200-500px for most uses
3. **Hashing**: Use SHA256 or SHA512 for security applications
4. **Passwords**: Always use all character types for strong passwords
5. **Error Handling**: Always validate inputs and handle API errors

## Example Interactions

### User: "把这段话翻译成英文：你好世界"

```python
data = {'text': '你好世界', 'from': 'zh', 'to': 'en'}
response = requests.post('https://60s.viki.moe/v2/fanyi', json=data)
print(response.json()['result'])  # Hello World
```

### User: "生成一个强密码"

```python
params = {'length': 20, 'symbols': True, 'uppercase': True, 'lowercase': True, 'numbers': True}
response = requests.get('https://60s.viki.moe/v2/password', params=params)
print(f"🔐 生成的密码：{response.json()['password']}")
```

### User: "查询这个IP地址的位置：1.1.1.1"

```python
response = requests.get('https://60s.viki.moe/v2/ip', params={'ip': '1.1.1.1'})
info = response.json()
print(f"📍 IP: {info['ip']}")
print(f"🌍 位置: {info['location']}")
print(f"🏢 运营商: {info['isp']}")
```

## Related Resources

- [60s API Documentation](https://docs.60s-api.viki.moe)
- [GitHub Repository](https://github.com/vikiboss/60s)
