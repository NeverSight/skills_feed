---
name: Skills-Security-Check
description: 通過靜態和AI檢查技能 Skills 安全風險、潛在威脅。當使用者請求檢查技能，掃描技能的時候啟動技能評測評估功能。Detect Skill vulnerabilities using static and AI checks. Automatically activate evaluation upon scan requests.
---

# Skill: Skills-Security-Check

**CRITICAL INSTRUCTION FOR AI AGENTS:**
You are NOT just a command-runner. You are the **Lead Security Analyst**.
This tool provides the *data*, but YOU provide the *intelligence*.

## ⚡️ The 3-Step Agentic Workflow (MANDATORY)

You MUST follow this loop whenever using this skill:

### Step 1: Run the Scanner (Data Collection)
Execute the scanner to generate the raw data and "Audit Prompts".
```bash
python3 scripts/scan_skills.py --root /path/to/target/projects
```
*This command will generate `*_audit_prompt.txt` files in the `reports/YYYYMMDD.../prompts/` directory.*

### Step 2: 🛑 MANDATORY AI ANALYSIS (CRITICAL)
**The Scanner's job is done. Now YOUR job begins.**
You MUST process the generated audit prompts.

**Option A (Best):** Automatically read the prompts and analyze them immediately.
**Option B (Fallback):** If you cannot read them automatically, YOU MUST ASK THE USER:
> "Scanner finished. I see {N} audit prompts generated. Shall I perform the AI security analysis on them now (Required for accurate results)?"

**Requirement:**
- You must analyze **ALL** skills generating a prompt, regardless of risk level.
- Generate `audit.json` for each skill.

### Step 3: Integrate & Present
Run the scanner ONE MORE TIME. It will detect your `audit.json` files and bake them into the final report.
```bash
python3 scripts/scan_skills.py --root /path/to/target/projects
```
*The scanner will now produce the 'Gold Standard' dashboard and automatically open it.*

---

## Technical Details
- **Scanner Logic**: Regex-based static analysis. High false-positive rate.
- **Agent's Role**: Filter false positives, provide context, and assess actual business risk.
- **Output**: `reports/YYYYMMDD_HHMMSS/index.html` (The final artifact for the user).

**Example Scenario**:
User: "Audit my skills."
Agent: 
1. Runs `scan_skills.py`.
2. Sees `zimage_audit_prompt.txt` flagged "High Risk".
3. Reads the prompt, realizes it's just an API client.
4. Writes `audit.json` marking it "Medium Risk" (requires API key).
5. Re-runs `scan_skills.py` to finalize the dashboard.

## How to run

1. Run the scanner on a root folder that contains multiple skills:

```bash
python3 /Users/mattchan/.agents/skills/skill-security-audit-dashboard/scripts/scan_skills.py \
  --root /Users/mattchan/.agents/skills \
  --out /Users/mattchan/.agents/skills/skill-security-audit-dashboard/security-dashboard.html
```

2. Open the generated HTML dashboard file to view the results.

## Notes

- This is a static heuristic scan. It does not execute code.
- The scanner avoids outputting raw secrets. It only reports file locations and categories.
- If you need a JSON file as well, pass `--json /path/to/output.json`.

## Arguments

- `--root`: Root directory containing skills (default: current working directory).
- `--out`: Path to the output HTML dashboard.
- `--json`: Optional path to write raw JSON output.
