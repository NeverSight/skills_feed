---
name: skill-validator
description: Validate agent skills for correctness, readability, workflow clarity, and isolation, ensuring they can be installed independently without dependencies on other skills.
---

# Skill Validator

## When to use this skill
Use this skill when you need to validate an agent skill folder, checking its structure, content, and adherence to best practices. This includes verifying frontmatter, readability, workflow definitions, validation steps, cross-references, and isolation from other skills.

## Validation steps

1. **Read the skill folder structure**: Ensure the folder contains a `SKILL.md` file. Check for optional subdirectories like `scripts/`, `references/`, `assets/`, but note that the skill must work in isolation without relying on other skills.

2. **Validate frontmatter**:
   - The `SKILL.md` file must start with YAML frontmatter containing at least `name` (short identifier) and `description` (clear indication of when to use the skill).
   - The description must be clear enough for agents to determine relevance without ambiguity.
   - The description should include either "When to use" or "Use this skill when" to clearly indicate applicability. If this phrasing is missing, it can lead to confusion about when the skill should be applied. To fix this, ensure the description contains a clear statement of the conditions or scenarios in which the skill is relevant, using one of the recommended phrases for clarity.

3. **Check cross-references**: Parse the markdown content for links and references. Ensure internal links (e.g., to headings) point to existing sections. For file references, verify they exist within the skill's directory.

4. **Assess readability and conciseness**:
   - Instructions should use clear, concise language.
   - Avoid overly verbose explanations; aim for direct, actionable content.
   - Check for grammar, spelling, and logical flow.

5. **Verify clear workflow definitions**:
   - The skill should provide step-by-step instructions for performing the task.
   - Workflows must be unambiguous, with clear prerequisites, steps, and expected outcomes.

6. **Check for validation steps**:
   - The skill must include steps at the end to validate that it was correctly executed (e.g., verify output, check for side effects).
   - This ensures the skill can confirm success or failure.

7. **Detect hallucinations**:
   - Ensure instructions do not assume or reference non-existent tools, libraries, or capabilities.
   - All referenced tools or methods must be realistic and available in standard environments.

8. **Confirm isolation**:
   - The skill should not reference or depend on other skills.
   - All necessary assets, scripts, and references must be bundled within the skill's directory.

9. **Detect duplicate content**:
   - Scan all files (SKILL.md and supporting files) for overlapping or duplicate sections/instructions.
   - Check for repeated explanations, examples, or workflows across multiple files.
   - Identify content that could be consolidated or cross-referenced more efficiently.
   - Flag redundant subsections within the same file (e.g., repeated step descriptions).
   - Duplicates waste token budget and confuse users; consolidate where possible.

10. **Estimate token cost (skill weight)**:
    - Calculate approximate token count for the entire skill (SKILL.md + references + assets)
    - Consider all text content, code examples, and documentation
    - Categorize the skill's "weight" based on token consumption:
      - **Lightweight** (< 2,000 tokens): Simple, focused skills
      - **Small** (2,000-4,000 tokens): Moderate skills with examples
      - **Medium** (4,000-8,000 tokens): Comprehensive skills with multiple sections
      - **Large** (8,000-15,000 tokens): Extensive skills with many examples
      - **Heavy** (15,000-25,000 tokens): Very comprehensive skills
      - **Overweight** (> 25,000 tokens): Potentially too large; consider splitting
    - Include weight in validation report for context awareness

11. **Security audit** ⭐ NEW:
     - Run the security validation module to check for common security vulnerabilities
     - Check for untrusted data sources (git, subprocess, files, APIs, user input)
     - Verify all untrusted data is properly sanitized before use
     - Identify high-privilege operations and verify they have user confirmation
     - Detect injection vulnerabilities (prompt, shell, SQL, code)
     - Verify error handling is comprehensive and doesn't leak sensitive data
     - Confirm secrets/credentials are not hardcoded and .env is documented
     - The security module will flag potential issues for remediation
     - **Tools**: Use `scripts/security_audit.py` to automatically scan the skill

12. **Summarize and validate execution**:
     - After completing all checks, provide a concise summary of the validation results, confirming the skill's status (valid or invalid), listing any issues, and suggesting fixes.
     - Categorize issues by severity (Critical 🚨, Warning ⚠️, Info ℹ️) and group them accordingly.
     - Include the skill's weight classification and token estimate.
     - If issues are found, include examples and suggestions for fixes. If no issues, confirm validity with a positive note.
     - This step ensures the validation process itself was correctly executed and provides closure.

 12. **Check for user information presentation examples**:
     - If the skill involves displaying or outputting information to the user (e.g., validation results, reports, or checklists), IT IS MANDATORY for it to include concrete examples of output formats.
     - Specify sample outputs, such as validation summaries with categorized issues (Critical 🚨, Warning ⚠️, Info ℹ️), checklists, or formatted messages.
     - This sets clear expectations and improves user experience by demonstrating the exact presentation style.
 
13. **Validate security audit report** (automated via scripts/security_audit.py):
     - The security audit script generates a detailed report with security findings
     - Review any flagged issues and ensure they are addressed
     - Critical issues (🚨) must be resolved before the skill is approved
     - Warnings (⚠️) should be reviewed and justified if not addressed
     - Info items (ℹ️) are recommendations for future improvements

## Examples

### When issues are found:
🚨 **Critical Issues:**
- Missing required frontmatter (e.g., no `name` field): Fix by adding the missing field to the YAML frontmatter.

⚠️ **Warnings:**
- Unclear description: Improve by making it more specific about when to use the skill.
- Duplicate instructions detected in SKILL.md and references/workflow.md: Consolidate by moving to one location and cross-referencing.

ℹ️ **Info:**
- Minor readability suggestions: Consider shortening verbose sections for conciseness.
- Skill weight: Medium (6,500 tokens) - Consider breaking into smaller, focused skills if it grows beyond 8,000 tokens.

### When no issues are found:
✅ **No issues found.** The skill is valid and ready for use.
- Skill weight: Lightweight (1,200 tokens) - Efficient for loading and execution.

## Duplicate Content Detection

### Detection Strategy

1. **Identify sections**: Extract all major sections (headers) from SKILL.md and all supporting files
2. **Extract content blocks**: For each section, identify paragraphs, lists, code blocks, and examples
3. **Semantic comparison**: Compare content blocks across files for:
   - Exact duplicates (word-for-word matches)
   - Near-duplicates (same concept, slightly different wording, > 80% similarity)
   - Partial duplicates (repeated phrases or examples within a file)
4. **Context analysis**: Determine if duplication serves a purpose or is redundant
5. **Report findings**: List all duplicates with file locations and consolidation suggestions

### Common Duplication Patterns to Flag

| Pattern | Example | Action |
|---------|---------|--------|
| Repeated workflow steps | Step description appears in both SKILL.md and references/workflow.md | Consolidate; cross-reference |
| Duplicate examples | Same code example shown in multiple sections | Keep in one place; reference from others |
| Overlapping explanations | Same concept explained twice with different wording | Merge explanations; remove redundancy |
| Repeated guidelines | Same best practices listed in two sections | Single source of truth; reference |
| Tool descriptions | Same tool explained in multiple files | Define once; reference elsewhere |

## Token Cost Estimation

### Token Calculation Method

1. **Estimate word count**: Count all words across all skill files
2. **Apply conversion ratio**: Use ~1.3 tokens per word for English text (average for LLM tokenization)
3. **Add overhead**: Account for:
   - YAML frontmatter (50 tokens base)
   - Markdown formatting overhead (+10% of content tokens)
   - Code blocks (count as 1.0 tokens per word due to tokenization patterns)
4. **Total calculation**: 
   ```
   Total Tokens = (SKILL.md words × 1.3) + (Reference files words × 1.3) + 
                  (Code blocks words × 1.0) + (Formatting overhead 10%) + 50
   ```

### Weight Classification

| Weight | Token Range | Description | Agent Impact |
|--------|-------------|-------------|--------------|
| 🟢 Lightweight | < 2,000 | Simple, focused skill | Minimal context usage; fast loading |
| 🟢 Small | 2,000-4,000 | Moderate skill with examples | Low context overhead; responsive |
| 🟡 Medium | 4,000-8,000 | Comprehensive skill | Balanced context usage; standard |
| 🟠 Large | 8,000-15,000 | Extensive skill with many examples | Significant context usage |
| 🔴 Heavy | 15,000-25,000 | Very comprehensive skill | High context consumption |
| 🔴 Overweight | > 25,000 | Too large; consider splitting | Problematic for context limits |

### Weight Assessment Examples

**Example 1: Lightweight Skill (1,200 tokens)**
- Simple workflow: 3-4 steps
- Minimal supporting files
- Few examples (1-2)
- Limited configuration options

**Example 2: Medium Skill (6,500 tokens)**
- Comprehensive workflow: 6-8 steps
- 2-3 reference files
- Multiple examples (4-6)
- Detailed configuration guide
- Best practices section

**Example 3: Heavy Skill (18,000 tokens)**
- Complex multi-phase workflow: 10+ steps
- 4-5 reference files with extensive content
- Many examples (8+) with detailed output
- Comprehensive configuration guide
- Multiple use cases and edge cases
- Troubleshooting section
- *Recommendation: Consider splitting into focused sub-skills*

## Output Format Example

### Skill Validation Report

```
═══════════════════════════════════════════════════════════
SKILL VALIDATION REPORT
═══════════════════════════════════════════════════════════

Skill: custom-agent-creator
Validation Date: 2024-02-21

───────────────────────────────────────────────────────────
GENERAL INFORMATION
───────────────────────────────────────────────────────────

Status: ✅ VALID
Skill Weight: 🟡 Medium (6,800 tokens)
Files Analyzed: 4
  - SKILL.md (3,200 tokens)
  - references/copilot-agents.md (1,500 tokens)
  - references/opencode-agents.md (1,400 tokens)
  - assets/ (2 templates, 700 tokens)

───────────────────────────────────────────────────────────
VALIDATION RESULTS
───────────────────────────────────────────────────────────

✅ Frontmatter: Valid
✅ Cross-References: All valid (3 internal, 2 file refs)
✅ Readability: Clear and concise
✅ Workflow: Well-defined (6 steps)
✅ Validation Steps: Comprehensive (5 categories)
✅ No Hallucinations: All tools/libraries verified
✅ Isolation: Self-contained (no skill dependencies)
✅ User Examples: 4 concrete examples with output
⚠️ Duplicate Content: 1 minor (see below)

───────────────────────────────────────────────────────────
DUPLICATE CONTENT DETECTED
───────────────────────────────────────────────────────────

⚠️ WARNING: Overlapping tool descriptions found

Location 1: SKILL.md, line 47 (OpenCode tools section)
Location 2: references/opencode-agents.md, line 282 (tools config section)

Issue: "Tool permissions are boolean or ask/allow/deny" 
       described in both locations with 85% similarity

Recommendation: Keep in SKILL.md (main reference), add cross-link 
              in references file for clarity

───────────────────────────────────────────────────────────
WEIGHT ANALYSIS
───────────────────────────────────────────────────────────

Total Content: 6,800 tokens
Content Distribution:
  - Instructions: 35% (2,380 tokens)
  - Examples: 40% (2,720 tokens)
  - References: 20% (1,360 tokens)
  - Formatting: 5% (340 tokens)

Classification: 🟡 MEDIUM
Impact: Balanced context usage; suitable for most use cases
Recommendation: Current size is optimal. No splitting needed.

If future expansion needed, consider:
- Moving Copilot agent examples to separate skill
- Creating OpenCode-specific variant
- Extracting template examples to assets folder

───────────────────────────────────────────────────────────
ISSUES SUMMARY
───────────────────────────────────────────────────────────

🚨 Critical Issues: 0
⚠️ Warnings: 1 (duplicate content - minor)
ℹ️ Info: 0

───────────────────────────────────────────────────────────
CONCLUSION
───────────────────────────────────────────────────────────

Status: ✅ APPROVED FOR PRODUCTION

The skill is well-structured, comprehensive, and ready for use.
Recommend addressing the minor duplicate content warning in the
next maintenance cycle for optimization.

═══════════════════════════════════════════════════════════
```

## Security Audit Module

The skill-validator now includes a built-in security audit module (`scripts/security_audit.py`) that checks for common security vulnerabilities. This module implements six comprehensive validation rules:

### Security Rules

**Rule 1: Untrusted Data Detection**
- Identifies external data sources (git, subprocess, files, APIs, user input)
- Flags sources that need sanitization
- Severity: HIGH (CRITICAL for git data and subprocess)

**Rule 2: Sanitization Requirement Verification**
- Verifies untrusted data is sanitized before use
- Checks for sanitization functions in the skill code
- Severity: CRITICAL if untrusted data found without sanitization

**Rule 3: High-Privilege Operation Detection**
- Identifies dangerous operations: file deletion, git push, shell execution
- Requires human confirmation for these operations
- Severity: CRITICAL for force operations

**Rule 4: Injection Risk Analysis**
- Detects potential injection vulnerabilities: prompt, shell, SQL, code
- Flags suspicious keywords that indicate attack attempts
- Severity: CRITICAL

**Rule 5: Error Handling Completeness**
- Verifies try/catch blocks for external operations
- Checks for timeout protection
- Ensures no sensitive data in error messages
- Severity: HIGH

**Rule 6: Secrets Protection**
- Detects hardcoded credentials
- Verifies .env and environment variables are documented
- Flags missing secrets protection
- Severity: CRITICAL for hardcoded secrets

### Running Security Audit

```bash
# Basic usage
python3 scripts/security_audit.py /path/to/SKILL.md

# Example output
════════════════════════════════════════════════════════════
SECURITY AUDIT REPORT
════════════════════════════════════════════════════════════

Skill: /path/to/SKILL.md
Status: ✅ PASSED

────────────────────────────────────────────────────────────
SUMMARY
────────────────────────────────────────────────────────────
🚨 Critical Issues: 0
⚠️  High Priority: 0
ℹ️  Medium Priority: 0
Total Issues: 0

✅ No security issues detected!
════════════════════════════════════════════════════════════
```

### Integration with Validation Workflow

The security audit is automatically run as **Step 11** of the validation process. Security issues are categorized by severity:

- **🚨 Critical**: Must be fixed before production deployment
- **⚠️ Warning**: Should be reviewed and justified
- **ℹ️ Info**: Recommendations for future improvements

## Tools to use
- File reading and parsing tools to examine `SKILL.md` and associated files.
- Markdown parsing for cross-reference checking and header extraction.
- Text analysis for readability assessment and duplicate detection.
- Token counting for weight estimation (approximate: 1.3 tokens/word).
- **Security audit**: `scripts/security_audit.py` for automated vulnerability scanning (NEW)
