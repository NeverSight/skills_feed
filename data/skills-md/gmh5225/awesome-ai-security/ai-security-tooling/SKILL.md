---
name: ai-security-tooling
description: Guide for AI security tooling (detectors, analyzers, guardrails, benchmarks) and consistent placement in README.md.
---

# AI Security Tooling

## Scope

Use this skill when adding or organizing:

- LLM security tools (guardrails, detectors)
- Adversarial ML libraries
- AI vulnerability scanners
- Model safety tools
- Security benchmarks and frameworks

## Tool Categories

### LLM Security Tools
- **Guardrails**: NeMo Guardrails, LLM Guard, Rebuff
- **Detectors**: Vigil-LLM, Nova Framework, Garak
- **Scanners**: ModelScan, AI Security Analyzer

### Adversarial ML Libraries
- **Attack libraries**: ART, CleverHans, Foolbox, TextAttack
- **Defense libraries**: SecML
- **Fuzzing**: OSS-Fuzz-Gen, Brainstorm

### AI Red Teaming
- **Microsoft**: Counterfit, PyRIT
- **Meta**: PurpleLlama
- **NVIDIA**: Garak, NeMo Guardrails

### Benchmarks
- **Robustness**: RobustBench
- **Jailbreak**: JailbreakBench
- **Safety**: Stanford AIR-Bench
- **Hallucination**: Vectara Leaderboard

### Standards & Frameworks
- **MITRE ATLAS**: AI threat matrix
- **NIST AI RMF**: Risk management framework
- **OWASP**: LLM Top 10, GenAI Security Project

## Categorization Rules

- **LLM guardrails/detectors** → `AI Security & Attacks → Model Security`
- **Prompt injection tools** → `AI Security & Attacks → Prompt Injection`
- **Adversarial ML libraries** → `AI Security & Attacks → Adversarial Attacks` or `AI Security Libraries`
- **AI RE/debugging tools** → `AI Security Tools & Frameworks → AI Reverse Engineering`
- **AI vulnerability scanners** → `AI Security Tools & Frameworks → AI Vulnerability Detection`
- **Benchmarks** → `Benchmarks & Standards`
- **MCP security tools** → `AI Pentesting & Red Teaming → AI Security MCP Tools`

## Quality Bar

- Prefer canonical repos
- Avoid forks unless they add meaningful features
- Add short descriptions
- Never duplicate an existing URL
- Tool must be AI/ML-focused

## Key Vendor Tools

| Vendor | Tools |
|--------|-------|
| Microsoft | Counterfit, PyRIT |
| Meta | PurpleLlama (Llama Guard, Prompt Guard, Code Shield) |
| NVIDIA | Garak, NeMo Guardrails |
| IBM | Adversarial Robustness Toolbox (ART) |
| Google | OSS-Fuzz-Gen |
| ProtectAI | Rebuff, LLM Guard, ModelScan |

## Notes

Keep additions:

- AI/ML security focused
- Non-duplicated URLs
- Minimal structural changes

## Data Source

For detailed and up-to-date resources, fetch the complete list from:

```
https://raw.githubusercontent.com/gmh5225/awesome-ai-security/refs/heads/main/README.md
```

Use this URL to get the latest curated links when you need specific tools, papers, or resources not covered in this skill.
