---
name: clawhub-skill-vetting
description: Vet ClawHub skills before installation. Use when the user asks about evaluating, auditing, or safely installing OpenClaw/ClawHub skills, or when a skill’s trustworthiness is in question.
---

# ClawHub Skill Vetting

## Overview
Apply a strict, security‑first vetting workflow before installing any ClawHub skill. Prioritize code review, permission scope, domain listing, and risk scoring.

## Workflow
1) **Source check** — author reputation, stars/downloads, last update, reviews.
2) **Code review (MANDATORY)** — scan all files for exfiltration, secrets access, `eval/exec`, obfuscation.
3) **Permission scope** — files, commands, network; confirm minimal scope.
4) **Recent activity** — detect suspicious bursts.
5) **Community check** — Discord/GitHub Discussions.
6) **Install safely** — sandbox + inspect permissions.

## Reference
Use **`references/vetting-guide.md`** for the full checklist, commands, red flags, confidence scoring, and report template.

## Output expectations
- Produce the **SKILL VETTING REPORT** format.
- Provide a **go/no‑go** recommendation with reasons.
- If unclear, recommend **sandbox install only** or **reject**.
- Call out any **red flags** explicitly.
- Include a **confidence score** and threshold.
