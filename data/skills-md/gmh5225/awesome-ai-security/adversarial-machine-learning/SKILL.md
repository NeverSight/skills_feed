---
name: adversarial-machine-learning
description: "Guide for adversarial machine learning: adversarial examples, data poisoning, model backdoors, and evasion attacks."
---

# Adversarial Machine Learning

## Scope

Use this skill when working on:

- Adversarial examples (perturbations that fool models)
- Data poisoning attacks
- Model backdoors and trojans
- Evasion attacks
- Membership inference and model inversion

## Attack Taxonomy

### Adversarial Examples
- White-box attacks (full model access)
- Black-box attacks (query-only access)
- Transferability attacks
- Physical-world adversarial examples
- Patch attacks

### Poisoning Attacks
- Label flipping
- Clean-label poisoning
- Gradient-matching poisoning
- Backdoor insertion during training

### Backdoor Attacks
- Trojan triggers (visual patterns, specific inputs)
- Instruction backdoors (for LLMs)
- Weight-space backdoors
- Supply chain backdoors

### Evasion Attacks
- Feature-space evasion
- Problem-space evasion
- Adaptive attacks against defenses

### Privacy Attacks
- Membership inference attacks (MIA)
- Model inversion attacks
- Training data extraction
- Model stealing/extraction

## Defense Categories

- Adversarial training
- Certified robustness
- Input preprocessing
- Anomaly detection
- Differential privacy

## Key Frameworks & Tools

- Adversarial Robustness Toolbox (ART) - IBM
- CleverHans - TensorFlow
- Foolbox - PyTorch/JAX/TensorFlow
- TextAttack - NLP adversarial attacks
- SecML - Secure ML library

## Where to Add Links in README

- Adversarial example tools: `AI Security & Attacks → Adversarial Attacks`
- Poisoning/backdoor research: `AI Security & Attacks → Poisoning & Backdoors`
- Privacy attacks: `AI Security & Attacks → Privacy & Extraction`
- Defense libraries: `AI Security Tools & Frameworks → AI Security Libraries`
- Benchmarks: `Benchmarks & Standards`

## Notes

Keep additions:

- ML/AI security focused
- Non-duplicated URLs
- Prefer peer-reviewed or well-maintained tools

## Data Source

For detailed and up-to-date resources, fetch the complete list from:

```
https://raw.githubusercontent.com/gmh5225/awesome-ai-security/refs/heads/main/README.md
```

Use this URL to get the latest curated links when you need specific tools, papers, or resources not covered in this skill.
