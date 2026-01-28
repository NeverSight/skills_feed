---
name: search-domain-validator
description: This skill should be used when users need to validate domain name format, check domain availability, or search for available domain names. It activates when users ask about domain validation, domain availability checking, domain search, or domain name verification.
---

# Search Domain Name Validator

## Overview

This skill enables Claude to validate domain name formats, check domain availability status, and search for available domain names based on keywords. Claude will use this skill to implement domain validation logic, integrate with domain availability APIs, and provide domain search functionality.

## When to Use This Skill

This skill activates automatically when users:

- Need to validate domain name format or syntax
- Want to check if a domain is available for registration
- Need to search for available domain names based on keywords
- Require domain validation in forms or applications
- Need to verify domain name compliance with RFC standards
- Want to implement domain suggestion features

## Project Context Discovery

**Before providing domain validation guidance, discover the project's context:**

1. **Scan Project Documentation:**
   - Check for existing domain validation logic
   - Review form validation patterns
   - Look for API integration patterns
   - Check for environment variable usage

2. **Identify Existing Patterns:**
   - Review validation libraries in use
   - Check for API client patterns
   - Review error handling approaches
   - Check for domain-related utilities

3. **Use Project-Specific Skills:**
   - Check for `[project]-domain-validator` skill
   - Review project-specific validation patterns
   - Follow project's validation standards

## Core Capabilities

### 1. Domain Format Validation

Validate domain names according to RFC 1035 and RFC 1123 standards.

**Domain Name Rules:**

- Length: 1-253 characters total
- Labels: Up to 63 characters each
- Characters: Letters (a-z, A-Z), digits (0-9), hyphens (-)
- Labels cannot start or end with hyphens
- TLD (top-level domain) required
- Cannot contain consecutive hyphens

**Validation Implementation:**

```typescript
// TypeScript/JavaScript domain validation
function isValidDomain(domain: string): boolean {
  if (!domain || domain.length > 253) {
    return false;
  }

  // RFC 1035 compliant regex
  const domainRegex = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i;
  
  if (!domainRegex.test(domain)) {
    return false;
  }

  // Check label length (max 63 chars)
  const labels = domain.split('.');
  for (const label of labels) {
    if (label.length > 63 || label.length === 0) {
      return false;
    }
    // Labels cannot start or end with hyphen
    if (label.startsWith('-') || label.endsWith('-')) {
      return false;
    }
  }

  return true;
}
```

**Python Validation:**

```python
import re

def is_valid_domain(domain: str) -> bool:
    """Validate domain name format according to RFC 1035 and RFC 1123."""
    if not domain or len(domain) > 253:
        return False
    
    # RFC 1035 compliant regex
    domain_pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$'
    
    if not re.match(domain_pattern, domain, re.IGNORECASE):
        return False
    
    # Check label length (max 63 chars)
    labels = domain.split('.')
    for label in labels:
        if len(label) > 63 or len(label) == 0:
            return False
        # Labels cannot start or end with hyphen
        if label.startswith('-') or label.endswith('-'):
            return False
    
    return True
```

**NestJS Validation:**

```typescript
import { IsString, Matches, MaxLength, ValidateIf } from 'class-validator';

export class DomainDto {
  @IsString()
  @MaxLength(253)
  @Matches(
    /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i,
    {
      message: 'Invalid domain name format',
    }
  )
  domain: string;
}
```

### 2. Domain Availability Checking

Check if a domain is available for registration using domain availability APIs.

**Common Domain Availability APIs:**

- Namecheap API
- GoDaddy API
- Name.com API
- WHOIS lookups (for basic checks)

**Namecheap API Integration:**

```typescript
// Namecheap domain availability check
async function checkDomainAvailability(domain: string): Promise<boolean> {
  const apiUser = process.env.NAMECHEAP_API_USER;
  const apiKey = process.env.NAMECHEAP_API_KEY;
  const clientIp = process.env.NAMECHEAP_CLIENT_IP;
  
  const url = `https://api.namecheap.com/xml.response?ApiUser=${apiUser}&ApiKey=${apiKey}&UserName=${apiUser}&Command=namecheap.domains.check&ClientIp=${clientIp}&DomainList=${domain}`;
  
  try {
    const response = await fetch(url);
    const xml = await response.text();
    
    // Parse XML response
    // Available domains return <DomainCheckResult Domain="example.com" Available="true"/>
    return xml.includes('Available="true"');
  } catch (error) {
    console.error('Error checking domain availability:', error);
    throw error;
  }
}
```

**GoDaddy API Integration:**

```typescript
// GoDaddy domain availability check
async function checkGoDaddyAvailability(domain: string): Promise<boolean> {
  const apiKey = process.env.GODADDY_API_KEY;
  const apiSecret = process.env.GODADDY_API_SECRET;
  
  const url = `https://api.godaddy.com/v1/domains/available?domain=${domain}`;
  
  try {
    const response = await fetch(url, {
      headers: {
        'Authorization': `sso-key ${apiKey}:${apiSecret}`,
        'Content-Type': 'application/json',
      },
    });
    
    const data = await response.json();
    return data.available === true;
  } catch (error) {
    console.error('Error checking domain availability:', error);
    throw error;
  }
}
```

**NestJS Service Example:**

```typescript
import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class DomainService {
  constructor(private httpService: HttpService) {}

  async checkAvailability(domain: string): Promise<boolean> {
    const apiKey = process.env.DOMAIN_API_KEY;
    const apiSecret = process.env.DOMAIN_API_SECRET;
    
    try {
      const response = await firstValueFrom(
        this.httpService.get(`https://api.example.com/domains/check`, {
          params: { domain },
          headers: {
            'Authorization': `Bearer ${apiKey}`,
          },
        })
      );
      
      return response.data.available;
    } catch (error) {
      throw new Error(`Failed to check domain availability: ${error.message}`);
    }
  }
}
```

### 3. Domain Search Functionality

Search for available domain names based on keywords, generating suggestions and alternatives.

**Domain Suggestion Algorithm:**

```typescript
function generateDomainSuggestions(keyword: string, tlds: string[] = ['com', 'io', 'net', 'org']): string[] {
  const suggestions: string[] = [];
  const sanitized = keyword.toLowerCase().replace(/[^a-z0-9-]/g, '');
  
  // Direct combinations
  for (const tld of tlds) {
    suggestions.push(`${sanitized}.${tld}`);
  }
  
  // Common prefixes
  const prefixes = ['get', 'try', 'use', 'my', 'the'];
  for (const prefix of prefixes) {
    for (const tld of tlds) {
      suggestions.push(`${prefix}${sanitized}.${tld}`);
    }
  }
  
  // Common suffixes
  const suffixes = ['app', 'hub', 'ly', 'fy', 'io'];
  for (const suffix of suffixes) {
    for (const tld of tlds) {
      suggestions.push(`${sanitized}${suffix}.${tld}`);
    }
  }
  
  return suggestions;
}
```

**Batch Availability Check:**

```typescript
async function searchAvailableDomains(keyword: string): Promise<string[]> {
  const suggestions = generateDomainSuggestions(keyword);
  const availableDomains: string[] = [];
  
  // Check availability for all suggestions (with rate limiting)
  for (const domain of suggestions) {
    try {
      const isAvailable = await checkDomainAvailability(domain);
      if (isAvailable) {
        availableDomains.push(domain);
      }
      // Rate limiting delay
      await new Promise(resolve => setTimeout(resolve, 100));
    } catch (error) {
      console.error(`Error checking ${domain}:`, error);
    }
  }
  
  return availableDomains;
}
```

## Best Practices

### Validation

- Always validate domain format before checking availability
- Handle edge cases (internationalized domain names, subdomains)
- Provide clear error messages for invalid domains
- Consider validating TLD separately if needed

### API Integration

- Store API credentials in environment variables
- Implement rate limiting to avoid API throttling
- Handle API errors gracefully
- Cache availability results when appropriate
- Use appropriate timeouts for API calls

### User Experience

- Provide real-time validation feedback
- Show domain suggestions as user types
- Display availability status clearly
- Offer alternative TLD suggestions
- Handle loading states during availability checks

### Security

- Never expose API keys in client-side code
- Validate and sanitize all user input
- Implement proper error handling
- Use HTTPS for all API communications
- Follow API provider's security guidelines

## Example User Requests

**Example 1: "Validate this domain: example.com"**

- Use format validation to check if the domain follows RFC standards
- Return validation result with specific error details if invalid

**Example 2: "Check if example.com is available"**

- Validate domain format first
- Call domain availability API
- Return availability status

**Example 3: "Search for available domains with keyword 'techstartup'"**

- Generate domain suggestions based on keyword
- Check availability for each suggestion
- Return list of available domains with pricing if available

**Example 4: "Implement domain validation in this form"**

- Add domain validation to form component
- Integrate real-time validation
- Provide user feedback for invalid domains

## Common Domain TLDs

**Generic TLDs:**

- .com, .net, .org, .info, .biz

**New gTLDs:**

- .app, .dev, .io, .ai, .tech, .online, .xyz

**Country Code TLDs:**

- .us, .uk, .ca, .au, .de, .fr, .jp

When implementing domain search, consider including popular TLDs relevant to the user's context or industry.
