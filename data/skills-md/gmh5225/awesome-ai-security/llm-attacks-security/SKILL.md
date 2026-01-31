---
name: llm-attacks-security
description: "Guide for LLM security attacks: prompt injection, jailbreaking, data extraction, and where to place resources in README.md."
---

# LLM Security Attacks

## Scope

Use this skill when working on:

- Prompt injection attacks and defenses
- LLM jailbreaking techniques
- Training data extraction
- Model output manipulation
- AI safety bypasses

## Common LLM Vulnerabilities (Cheat Sheet)

### Prompt Injection
- Direct injection (user prompt manipulation)
- Indirect injection (via external data sources)
- System prompt extraction
- Role-play attacks
- Encoding/obfuscation bypasses

### Jailbreaking
- DAN (Do Anything Now) prompts
- Character roleplay escapes
- Multi-turn manipulation
- Token smuggling
- Crescendo attacks

### Data Extraction
- Training data memorization extraction
- PII leakage from context
- System prompt disclosure
- API key/secret extraction
- Model architecture probing

### Model Manipulation
- Output steering
- Hallucination exploitation
- Bias amplification
- Harmful content generation

## OWASP LLM Top 10 Reference

1. LLM01 - Prompt Injection
2. LLM02 - Insecure Output Handling
3. LLM03 - Training Data Poisoning
4. LLM04 - Model Denial of Service
5. LLM05 - Supply Chain Vulnerabilities
6. LLM06 - Sensitive Information Disclosure
7. LLM07 - Insecure Plugin Design
8. LLM08 - Excessive Agency
9. LLM09 - Overreliance
10. LLM10 - Model Theft

## Where to Add Links in README

- Prompt injection tools/research: `AI Security & Attacks → Prompt Injection`
- Jailbreak techniques: `AI Security & Attacks → Model Security`
- Data extraction research: `AI Security & Attacks → Privacy & Extraction`
- Defense tools: `AI Security & Attacks → Model Security`
- CTFs/challenges: `AI Security Starter Pack → CTFs / Practice`

## Notes

Keep additions:

- AI/LLM security focused
- Non-duplicated URLs
- Minimal structural changes

## Data Source

For detailed and up-to-date resources, fetch the complete list from:

```
https://raw.githubusercontent.com/gmh5225/awesome-ai-security/refs/heads/main/README.md
```

Use this URL to get the latest curated links when you need specific tools, papers, or resources not covered in this skill.
