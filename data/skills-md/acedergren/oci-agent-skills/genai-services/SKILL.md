---
name: genai-services
description: Use when implementing OCI GenAI inference APIs, troubleshooting rate limits or token errors, optimizing GenAI costs, or handling sensitive data (PHI/PII) in prompts. Covers model selection, cost calculations, token management, response validation, and healthcare/compliance considerations.
license: MIT
metadata:
  author: alexander-cedergren
  version: "2.0.0"
---

# OCI Generative AI Services - Expert Knowledge

## 🏗️ Use OCI Landing Zone Terraform Modules

**Don't reinvent the wheel.** Use [oracle-terraform-modules/landing-zone](https://github.com/oracle-terraform-modules/terraform-oci-landing-zones) for GenAI infrastructure.

**Landing Zone solves:**
- ❌ Bad Practice #1: Generic compartments (Landing Zone creates AI/ML workload compartments)
- ❌ Bad Practice #4: Poor segmentation (Landing Zone isolates GenAI endpoints in private subnets)
- ❌ Bad Practice #10: No monitoring (Landing Zone configures GenAI usage alarms)

**This skill provides**: GenAI cost optimization, rate limits, PHI/PII security, and troubleshooting for GenAI deployed WITHIN a Landing Zone.

---

## ⚠️ OCI CLI/API Knowledge Gap

**You don't know OCI CLI commands or OCI API structure.**

Your training data has limited and outdated knowledge of:
- OCI CLI syntax and parameters (updates monthly)
- OCI GenAI API endpoints and request/response formats
- GenAI service CLI operations (`oci generative-ai`)
- Available models, token limits, and pricing (changes frequently)
- Latest GenAI features (Agents, RAG) and API changes

**When OCI operations are needed:**
1. Use exact CLI commands from this skill's references
2. Do NOT guess OCI CLI syntax or parameters
3. Do NOT assume model availability or pricing
4. Load reference files for detailed GenAI API documentation

**What you DO know:**
- General LLM concepts and prompting patterns
- Token estimation and context management
- API integration patterns

This skill bridges the gap by providing current OCI GenAI-specific patterns and gotchas.

---

You are an OCI GenAI expert. This skill provides knowledge Claude lacks: cost optimization specifics, token management, rate limit handling, PHI/PII security, response validation, and model selection trade-offs.

## NEVER Do This

❌ **NEVER send PHI/PII identifiers to GenAI APIs (HIPAA/GDPR violation)**
```python
# WRONG - patient identifiers sent to external service
prompt = f"Transcribe note for patient {patient_name}, MRN {mrn}, SSN {ssn}: {note}"

# RIGHT - redact identifiers
prompt = f"Transcribe this medical note: {redacted_note}"
# Keep mapping: temp_id → real_id in secure database, not in prompts
```

**Why critical**: GenAI service logs may retain data, violates healthcare regulations

❌ **NEVER trust GenAI output without validation (hallucination risk)**
```python
# WRONG - use response directly in critical systems
diagnosis = genai_response.text
db.execute("UPDATE patients SET diagnosis = ?", diagnosis)

# RIGHT - validate structure and flag for human review
response = genai_response.text
if validate_medical_format(response):
    db.execute("UPDATE patients SET ai_suggested_diagnosis = ?, status = 'PENDING_REVIEW'", response)
```

**Hallucination rate**: 5-15% for factual queries, higher for medical/legal domains

❌ **NEVER ignore token limits**
- **command-r-plus**: 128k context window (input + output)
- **command-r**: 4k context (much cheaper but limited)
- **Exceeding limit**: Request truncated silently or fails with 400 error

❌ **NEVER call GenAI without rate limit handling**
```python
# WRONG - no retry logic, fails on rate limit
response = genai_client.chat(request)

# RIGHT - exponential backoff
def call_with_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except oci.exceptions.ServiceError as e:
            if e.status == 429 and attempt < max_retries - 1:
                wait = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(f"Rate limited, retry in {wait:.2f}s")
                time.sleep(wait)
            else:
                raise
```

❌ **NEVER cache responses without consent (data privacy)**
- Caching saves costs BUT may violate privacy policies
- Get explicit user consent before caching medical/personal data
- Cache anonymized data only

❌ **NEVER use GenAI for deterministic tasks**
- Wrong: "Extract invoice total from OCR text" (use regex/structured parsing)
- Wrong: "Validate email format" (use validation library)
- Right: "Summarize patient history", "Generate report narrative" (creative tasks)

## Model Selection: Cost vs Performance

| Model | Context | Cost (per 1M tokens) | Best For | Avoid For |
|-------|---------|---------------------|----------|-----------|
| **command-r-plus** | 128k | ~$15 input, $75 output | Complex reasoning, long documents | Simple tasks (expensive) |
| **command-r** | 4k | ~$1.50 input, $7.50 output | Chat, short prompts, high volume | Long documents, RAG |
| **embed-english-v3** | N/A | ~$0.10 per 1M | Semantic search, clustering | Text generation |
| **llama-2-70b** | 4k | ~$2 input, $10 output | Open weights, cost-effective | Production (limited support) |

**Cost optimization strategy:**
1. **Use embeddings for search first** (1000x cheaper than generation)
2. **Cache responses** for repeated queries (with consent)
3. **Use command-r for simple tasks**, command-r-plus only when needed
4. **Truncate input** intelligently (keep relevant context only)

## Cost Calculation Examples

**Scenario: Medical transcription service**
- Average note: 500 tokens input, 300 tokens output = 800 tokens total
- 1000 notes/day = 800k tokens/day = 24M tokens/month

**Without optimization:**
```
Model: command-r-plus
Input:  12M × ($15/1M) = $180/month
Output: 12M × ($75/1M) = $900/month
Total: $1,080/month
```

**With optimization (30% cache hit, use command-r for simple notes):**
```
70% unique notes = 16.8M tokens
60% simple (command-r): 10M × $1.50 input + $7.50 output = $90
40% complex (command-r-plus): 6.72M × $15 input + $75 output = $605
Total: $695/month (36% savings)
```

## Token Management

### Token Limits by Model

| Model | Max Context | Max Output | Notes |
|-------|-------------|------------|-------|
| command-r-plus | 128k (input+output) | Varies | ~4 chars per token (rough) |
| command-r | 4k | 2k | Good for chat |
| embed-english-v3 | 512 | N/A | Embeddings only |

### Truncation Strategy

```python
def truncate_for_model(text: str, model: str = "command-r-plus", max_output: int = 2000):
    """Truncate input to fit token budget"""

    # Rough estimate: 1 token ≈ 4 characters
    if model == "command-r-plus":
        max_input_tokens = 128000 - max_output
    elif model == "command-r":
        max_input_tokens = 4000 - max_output
    else:
        max_input_tokens = 2000

    max_chars = max_input_tokens * 4

    if len(text) <= max_chars:
        return text

    # Keep most recent content (chronological data like logs, notes)
    logger.warning(f"Input exceeds {max_input_tokens} tokens, truncating")
    return "...[earlier content truncated]...\n" + text[-max_chars:]
```

### Prompt Optimization

**Inefficient** (wastes tokens):
```
Please carefully analyze the following medical record and provide a comprehensive
summary including all diagnoses, medications, allergies, and treatment plans. Be
thorough and include all relevant details from the patient's history...

[5000 word medical record]
```

**Optimized** (40% token reduction):
```
Summarize: diagnoses, meds, allergies, treatment plan.

[5000 word medical record]
```

**Token savings**: ~50 tokens on prompt × 1000 requests/day = 50k tokens/day saved = **$2.25/day** ($68/month)

## Rate Limits

### OCI GenAI Service Limits (per compartment):

| Model | Requests/Minute | Requests/Day | Tokens/Request |
|-------|-----------------|--------------|----------------|
| command-r-plus | 20 | 1000 | 128k |
| command-r | 60 | 3000 | 4k |
| Embeddings | 100 | 10000 | 512 |

### Error Handling

```python
import time
import random
from oci.exceptions import ServiceError

def generate_with_backoff(genai_client, request, max_retries=5):
    """Call GenAI with exponential backoff on rate limits"""

    for attempt in range(max_retries):
        try:
            response = genai_client.chat(request)
            return response.data.chat_response.text

        except ServiceError as e:
            if e.status == 429:  # Rate limit
                if attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Rate limited (429), retry {attempt+1}/{max_retries} in {wait:.1f}s")
                    time.sleep(wait)
                else:
                    logger.error(f"Rate limit exceeded after {max_retries} retries")
                    raise

            elif e.status == 400:  # Bad request (often token limit)
                logger.error(f"Bad request (400): {e.message}")
                if "token" in e.message.lower():
                    logger.error("Token limit exceeded - truncate input")
                raise

            else:
                logger.error(f"GenAI error ({e.status}): {e.message}")
                raise
```

## Response Validation (Critical for Healthcare)

```python
def validate_medical_response(response: str) -> tuple[bool, list[str]]:
    """Validate GenAI medical response for safety"""

    issues = []

    # Check 1: Response not empty
    if not response or len(response.strip()) < 10:
        issues.append("Response too short or empty")

    # Check 2: No obvious hallucination markers
    hallucination_markers = [
        "I don't have access",
        "I cannot",
        "As an AI",
        "[INSERT",
        "TODO",
    ]
    for marker in hallucination_markers:
        if marker.lower() in response.lower():
            issues.append(f"Potential hallucination marker: {marker}")

    # Check 3: Expected structure present (customize per use case)
    required_sections = ["Chief Complaint", "Assessment", "Plan"]
    missing_sections = [s for s in required_sections if s.lower() not in response.lower()]
    if missing_sections:
        issues.append(f"Missing sections: {missing_sections}")

    # Check 4: No PII leak (if input was redacted)
    pii_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b[A-Z]{2}\d{6,8}\b',     # MRN patterns
    ]
    for pattern in pii_patterns:
        if re.search(pattern, response):
            issues.append(f"Potential PII in response: {pattern}")

    is_valid = len(issues) == 0
    return is_valid, issues


# Usage
response_text = genai_response.data.chat_response.text
is_valid, issues = validate_medical_response(response_text)

if is_valid:
    store_for_review(response_text)
else:
    logger.warning(f"Invalid response: {issues}")
    flag_for_manual_review(response_text, issues)
```

## Healthcare-Specific Considerations

### HIPAA Compliance

**Minimum requirements:**
- ✅ Business Associate Agreement (BAA) with Oracle
- ✅ PHI redaction before sending to GenAI
- ✅ Audit logging of all GenAI API calls
- ✅ Encryption in transit and at rest
- ✅ Access controls (who can call GenAI)
- ✅ Data retention policies (how long to keep prompts/responses)

**Never assume GenAI is HIPAA-compliant by default** - verify BAA coverage with Oracle

### De-identification Strategy

```python
def redact_phi(text: str) -> tuple[str, dict]:
    """Remove PHI from text, return redacted text + mapping"""

    mapping = {}
    redacted = text

    # Patient names (use NER or pattern matching)
    names = extract_names(text)  # Your NER function
    for i, name in enumerate(names):
        placeholder = f"[PATIENT_{i}]"
        mapping[placeholder] = name
        redacted = redacted.replace(name, placeholder)

    # Medical Record Numbers
    mrn_pattern = r'\b(MRN|Medical Record):?\s*([A-Z0-9]{6,10})\b'
    redacted = re.sub(mrn_pattern, r'\1: [REDACTED]', redacted)

    # SSN
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    redacted = re.sub(ssn_pattern, '[SSN_REDACTED]', redacted)

    # Dates (optional - some use cases need dates)
    # date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
    # redacted = re.sub(date_pattern, '[DATE]', redacted)

    return redacted, mapping


# Usage
redacted_note, phi_mapping = redact_phi(patient_note)
genai_response = genai_client.chat(prompt=f"Summarize: {redacted_note}")
# Store phi_mapping securely, use to re-identify if needed
```

## Progressive Loading References

### OCI Generative AI Reference (Official Oracle Documentation)

**WHEN TO LOAD** [`oci-genai-reference.md`](references/oci-genai-reference.md):
- Need comprehensive GenAI API documentation
- Understanding all available models and capabilities
- Implementing RAG (Retrieval-Augmented Generation) with OCI
- Need official Oracle guidance on GenAI Agents
- Understanding fine-tuning and custom model deployment

**Do NOT load** for:
- Quick API usage examples (covered in this skill)
- Model selection guidance (decision tree above)
- Cost calculations (formulas above)

---

## When to Use This Skill

- GenAI API implementation: model selection, cost estimation, SDK usage
- Error troubleshooting: rate limits (429), token limits (400), authentication
- Cost optimization: caching strategy, model downgrade, prompt optimization
- Healthcare/compliance: PHI handling, HIPAA requirements, audit logging
- Response validation: hallucination detection, structure checking
- Production: rate limit handling, error recovery, monitoring
