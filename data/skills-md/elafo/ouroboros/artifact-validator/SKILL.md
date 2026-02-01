---
name: artifact-validator
description: Validate and grade Claude Code Skills, Commands, Subagents, and Hooks for quality and correctness. Check YAML syntax, verify naming conventions, validate required fields, test activation patterns, assess description quality. Generate quality scores using Q = 0.40R + 0.30C + 0.20S + 0.10E framework with specific improvement recommendations. Use when validating artifacts, checking quality, troubleshooting activation issues, or ensuring artifact correctness before deployment.
allowed-tools: Read, Bash, Grep, Glob
---

# Artifact Validator: Quality Assurance for Claude Code Artifacts

Comprehensive validation and quality grading system for Claude Code Skills, Commands, Subagents, and Hooks. Ensures artifacts meet technical requirements, follow best practices, and will activate/execute reliably.

## Core Capabilities

- **YAML Validation:** Check syntax, structure, and required fields
- **Naming Verification:** Ensure directory names match YAML names
- **Description Quality:** Grade activation potential for Skills
- **Field Validation:** Verify all required and optional fields
- **Activation Testing:** Simulate trigger scenarios for Skills
- **Quality Grading:** Apply Q = 0.40R + 0.30C + 0.20S + 0.10E framework
- **Improvement Recommendations:** Provide specific actionable feedback
- **Cross-Artifact Checks:** Detect conflicts and overlaps

## Methodology

### Step 1: Identify Artifact Type

First, determine what type of artifact to validate:

**Detection rules:**
- **Skill:** Located in `.claude/skills/*/SKILL.md`
- **Command:** Located in `.claude/commands/*.md`
- **Subagent:** Located in `.claude/agents/*.yaml`
- **Hook:** Configuration in `settings.json` under `hooks` key

**Example:**
```bash
# Auto-detect artifact type
if [[ -f ".claude/skills/my-skill/SKILL.md" ]]; then
  TYPE="skill"
elif [[ -f ".claude/commands/my-command.md" ]]; then
  TYPE="command"
elif [[ -f ".claude/agents/my-agent.yaml" ]]; then
  TYPE="subagent"
fi
```

### Step 2: YAML Syntax Validation

Validate YAML frontmatter is syntactically correct:

**For Skills and Commands:**
```bash
# Extract YAML frontmatter (between --- delimiters)
python3 -c "
import yaml
import sys

with open('SKILL.md') as f:
    content = f.read()
    parts = content.split('---')
    if len(parts) < 3:
        print('ERROR: Missing YAML frontmatter delimiters')
        sys.exit(1)

    try:
        data = yaml.safe_load(parts[1])
        print('✅ YAML syntax valid')
        print(f'Fields: {list(data.keys())}')
    except yaml.YAMLError as e:
        print(f'❌ YAML syntax error: {e}')
        sys.exit(1)
"
```

**For Subagents:**
```bash
# Full YAML file
python3 -c "
import yaml
with open('agent.yaml') as f:
    try:
        data = yaml.safe_load(f)
        print('✅ YAML syntax valid')
    except yaml.YAMLError as e:
        print(f'❌ YAML error: {e}')
"
```

**Common YAML errors:**
- Missing closing `---` delimiter
- Tab characters (use spaces only)
- Smart quotes instead of straight quotes
- Array syntax for comma-separated fields

### Step 3: Required Fields Validation

Check that all required fields are present and valid:

**Skill required fields:**
- `name` (string, matches directory name)
- `description` (string, ≤1024 characters)

**Skill optional fields:**
- `allowed-tools` (comma-separated string)

**Command required fields:**
- `description` (string)

**Command optional fields:**
- `argument-hint` (string)
- `allowed-tools` (comma-separated string)
- `disable-model-invocation` (boolean)

**Subagent required fields:**
- `name` (string)
- `description` (string)

**Subagent optional fields:**
- `tools` (array)
- `model` (enum: sonnet, opus, haiku)

**Validation example:**
```python
import yaml

with open('SKILL.md') as f:
    parts = f.read().split('---')
    data = yaml.safe_load(parts[1])

# Check required fields
required = ['name', 'description']
missing = [f for f in required if f not in data]

if missing:
    print(f"❌ Missing required fields: {missing}")
else:
    print("✅ All required fields present")

# Validate field types and constraints
if 'name' in data and not isinstance(data['name'], str):
    print("❌ 'name' must be a string")

if 'description' in data:
    if not isinstance(data['description'], str):
        print("❌ 'description' must be a string")
    elif len(data['description']) > 1024:
        print(f"❌ 'description' exceeds 1024 chars: {len(data['description'])}")
    else:
        print(f"✅ description length: {len(data['description'])}/1024")
```

### Step 4: Naming Convention Validation

Verify directory/file names match YAML fields:

**For Skills:**
```bash
# Directory name must match YAML 'name' field
SKILL_DIR=$(basename $(dirname SKILL.md))
YAML_NAME=$(grep "^name:" SKILL.md | cut -d: -f2 | xargs)

if [ "$SKILL_DIR" == "$YAML_NAME" ]; then
    echo "✅ Name matches: $SKILL_DIR"
else
    echo "❌ Mismatch: directory=$SKILL_DIR, YAML=$YAML_NAME"
fi
```

**Naming rules:**
- Lowercase only
- Hyphens for word separation (no underscores)
- No spaces
- Alphanumeric + hyphens only
- Max 64 characters

**Validation:**
```python
import re

def validate_name(name, artifact_type):
    """Validate artifact name follows conventions."""

    # Check length
    if len(name) > 64:
        return f"❌ Name too long: {len(name)} chars (max 64)"

    # Check pattern
    if not re.match(r'^[a-z0-9-]+$', name):
        return "❌ Name must be lowercase alphanumeric with hyphens only"

    # Check doesn't start/end with hyphen
    if name.startswith('-') or name.endswith('-'):
        return "❌ Name cannot start or end with hyphen"

    # Check no consecutive hyphens
    if '--' in name:
        return "❌ No consecutive hyphens allowed"

    return f"✅ Name '{name}' is valid"
```

### Step 5: Description Quality Assessment (Skills Only)

Grade Skill descriptions using activation quality criteria:

**Quality dimensions:**

1. **Action Verbs (0-10 points)**
   - Count action verbs in description
   - 5+ verbs = 10 points, scale down for fewer

2. **Capabilities Specificity (0-10 points)**
   - 10 points: Specific capabilities with details
   - 5 points: Generic capabilities
   - 0 points: Vague "helps with" language

3. **Technology Mentions (0-10 points)**
   - Count technologies/tools/file types mentioned
   - 3+ = 10 points, scale down for fewer

4. **Trigger Keywords (0-10 points)**
   - Count "Use when/for..." keywords
   - 10+ keywords = 10 points, scale down

5. **Character Efficiency (0-10 points)**
   - Optimal: 400-700 chars = 10 points
   - Scale down for too short (<200) or too long (>900)

**Scoring formula:**
```
Description Score = (Verbs + Specificity + Tech + Keywords + Efficiency) / 50 * 100
```

**Grade:**
- A (≥90): Excellent, will activate reliably
- B (80-89): Good, minor improvements possible
- C (70-79): Acceptable, needs improvements
- D (60-69): Poor, significant revision needed
- F (<60): Failing, complete rewrite required

**Example assessment:**
```python
def assess_description(description):
    """Grade Skill description quality."""

    # 1. Count action verbs
    action_verbs = ['extract', 'parse', 'test', 'validate', 'generate',
                    'optimize', 'convert', 'analyze', 'detect', 'compare']
    verb_count = sum(1 for verb in action_verbs if verb in description.lower())
    verb_score = min(10, verb_count * 2)

    # 2. Check specificity (heuristic: no vague terms)
    vague_terms = ['helps', 'various', 'multiple', 'different']
    has_vague = any(term in description.lower() for term in vague_terms)
    specificity_score = 5 if has_vague else 10

    # 3. Count technologies (file extensions, tool names)
    tech_indicators = ['.pdf', '.json', '.csv', 'api', 'sql', 'http',
                       'rest', 'openapi', 'yaml']
    tech_count = sum(1 for tech in tech_indicators if tech in description.lower())
    tech_score = min(10, tech_count * 3)

    # 4. Check for "Use when/for"
    has_triggers = 'use when' in description.lower() or 'use for' in description.lower()
    trigger_score = 10 if has_triggers else 0

    # 5. Character efficiency
    length = len(description)
    if 400 <= length <= 700:
        efficiency_score = 10
    elif 200 <= length < 400 or 700 < length <= 900:
        efficiency_score = 7
    elif length < 200 or length > 900:
        efficiency_score = 3
    else:
        efficiency_score = 0

    total = verb_score + specificity_score + tech_score + trigger_score + efficiency_score
    percentage = (total / 50) * 100

    if percentage >= 90:
        grade = 'A'
    elif percentage >= 80:
        grade = 'B'
    elif percentage >= 70:
        grade = 'C'
    elif percentage >= 60:
        grade = 'D'
    else:
        grade = 'F'

    return {
        'grade': grade,
        'score': percentage,
        'breakdown': {
            'verbs': verb_score,
            'specificity': specificity_score,
            'technologies': tech_score,
            'triggers': trigger_score,
            'efficiency': efficiency_score
        }
    }
```

### Step 6: Content Quality Validation

Check the artifact's content beyond YAML frontmatter:

**For Skills (SKILL.md):**
- [ ] Overview paragraph exists and explains purpose
- [ ] Core Capabilities section with 3+ capabilities
- [ ] Methodology section with step-by-step workflow
- [ ] At least 3 examples (recommend 5)
- [ ] Examples have code blocks with language specified
- [ ] No placeholder text (TODO, FIXME, Lorem Ipsum)
- [ ] Troubleshooting section present
- [ ] No broken markdown syntax

**For Commands:**
- [ ] Description explains what command does
- [ ] If arguments used, they're documented
- [ ] Command body has executable content
- [ ] No placeholder prompts

**For Subagents:**
- [ ] System prompt is substantial (>100 words)
- [ ] Clear focus/specialization explained
- [ ] Instructions are actionable

**Validation approach:**
```python
def validate_skill_content(filepath):
    """Check Skill content quality."""

    with open(filepath) as f:
        content = f.read()

    issues = []

    # Check for required sections
    required_sections = [
        'Core Capabilities',
        'Methodology',
        'Examples'
    ]

    for section in required_sections:
        if section not in content:
            issues.append(f"Missing section: {section}")

    # Count examples
    example_count = content.count('### Example')
    if example_count < 3:
        issues.append(f"Only {example_count} examples (need 3+)")

    # Check for placeholders
    placeholders = ['TODO', 'FIXME', 'PLACEHOLDER', 'Lorem ipsum']
    for placeholder in placeholders:
        if placeholder in content:
            issues.append(f"Contains placeholder: {placeholder}")

    # Check code blocks have language
    code_blocks = re.findall(r'```(\w*)\n', content)
    unnamed_blocks = [i for i, lang in enumerate(code_blocks) if not lang]
    if unnamed_blocks:
        issues.append(f"{len(unnamed_blocks)} code blocks missing language")

    if not issues:
        return "✅ Content quality: PASS"
    else:
        return f"⚠️ Content issues:\n" + "\n".join(f"  - {issue}" for issue in issues)
```

### Step 7: Activation Pattern Testing (Skills Only)

Simulate activation scenarios to predict reliability:

**Test categories:**
1. Direct keyword match
2. Contextual trigger
3. File extension trigger (if applicable)

**Example test suite:**
```python
def test_activation_potential(description):
    """Predict if Skill will activate for common scenarios."""

    # Extract keywords from description
    keywords = set(description.lower().split())

    test_scenarios = [
        {
            'name': 'Direct keyword match',
            'request': 'extract tables from pdf',
            'expected_keywords': ['extract', 'tables', 'pdf']
        },
        {
            'name': 'Technology mention',
            'request': 'use pdfplumber to get data',
            'expected_keywords': ['pdfplumber', 'data']
        }
    ]

    results = []
    for scenario in test_scenarios:
        request_words = set(scenario['request'].split())
        matches = sum(1 for kw in scenario['expected_keywords']
                     if kw in keywords)

        if matches >= 2:
            results.append(f"✅ {scenario['name']}: Likely activates")
        else:
            results.append(f"⚠️ {scenario['name']}: May not activate")

    return results
```

### Step 8: Generate Quality Report

Compile all validation results into comprehensive report:

**Report structure:**

```markdown
# Artifact Validation Report

**Artifact:** [name]
**Type:** [Skill/Command/Subagent/Hook]
**Date:** [YYYY-MM-DD]

## Overall Grade: [A/B/C/D/F]

### YAML Validation
- Syntax: [✅/❌]
- Required fields: [✅/❌]
- Optional fields: [list present fields]

### Naming Convention
- Directory/file name: [✅/❌]
- YAML name field: [✅/❌]
- Consistency: [✅/❌]

### Description Quality (Skills only)
- Grade: [A/B/C/D/F]
- Score: [X/100]
- Breakdown:
  - Action verbs: [X/10]
  - Specificity: [X/10]
  - Technologies: [X/10]
  - Triggers: [X/10]
  - Efficiency: [X/10]

### Content Quality
- Structure: [✅/❌/⚠️]
- Examples: [count] ([✅ if ≥3, ❌ if <3])
- Placeholders: [✅ none / ❌ found]
- Code blocks: [✅/⚠️]

### Activation Potential (Skills only)
- Direct keywords: [✅/⚠️/❌]
- Contextual triggers: [✅/⚠️/❌]
- File extensions: [✅/⚠️/❌/N/A]
- Predicted success rate: [X%]

## Issues Found

[List of all issues with severity]

## Recommendations

[Specific, actionable improvements]

## Quality Framework Score

Using Q = 0.40·R + 0.30·C + 0.20·S + 0.10·E:

- Relevance (R): [score] - [explanation]
- Completeness (C): [score] - [explanation]
- Consistency (S): [score] - [explanation]
- Efficiency (E): [score] - [explanation]

**Final Q score: [X.XX]**
**Grade: [A/B+/B/C/D/F]**
```

## Examples

### Example 1: Validate a Skill with Issues

**Scenario:** Check pdf-processor Skill for quality

**Validation steps:**

```bash
# Step 1: Check YAML syntax
python3 -c "
import yaml
with open('.claude/skills/pdf-processor/SKILL.md') as f:
    content = f.read()
    parts = content.split('---')
    yaml.safe_load(parts[1])
"
# Output: (no error = valid)
```

```bash
# Step 2: Verify name consistency
DIRNAME=$(basename .claude/skills/pdf-processor)
YAMLNAME=$(grep "^name:" .claude/skills/pdf-processor/SKILL.md | cut -d: -f2 | xargs)

if [ "$DIRNAME" == "$YAMLNAME" ]; then
  echo "✅ Names match: $DIRNAME"
else
  echo "❌ Mismatch: dir=$DIRNAME, yaml=$YAMLNAME"
fi
```

**Issues found:**
```
⚠️ Description only 45 characters (too short)
❌ Missing "Use when..." triggers
⚠️ Only 2 action verbs (need 5+)
❌ Missing Examples section
```

**Recommendations:**
```
1. Expand description to 400-700 characters
2. Add "Use when working with PDF files, document extraction..." clause
3. Add action verbs: parse, merge, split, convert
4. Create Examples section with 3-5 complete examples
```

**Quality grade: D (65/100)**

---

### Example 2: Validate High-Quality Skill

**Scenario:** Validate artifact-advisor Skill

**Results:**
```
✅ YAML syntax: Valid
✅ Name consistency: artifact-advisor (matches)
✅ Description: 586 characters (optimal range)
✅ Required fields: All present
✅ Action verbs: 7 (analyze, recommend, advise, choose, justify)
✅ Technologies: 4 (Skills, Commands, Subagents, Hooks)
✅ Triggers: Present ("Use when user asks...")
✅ Examples: 7 examples found
✅ No placeholders
✅ Code blocks: All have language specified
```

**Quality grade: A (94/100)**

**Quality framework:**
- Relevance: 0.95 (highly focused on artifact selection)
- Completeness: 0.92 (comprehensive examples and decision trees)
- Consistency: 0.90 (consistent terminology and structure)
- Efficiency: 0.88 (concise yet thorough)

**Q = 0.40(0.95) + 0.30(0.92) + 0.20(0.90) + 0.10(0.88) = 0.924**

**Final grade: A**

---

### Example 3: Validate Command

**Scenario:** Check deployment command

**Command file: `.claude/commands/deploy.md`**

```yaml
---
description: Deploy application to specified environment with pre-deployment checks
argument-hint: <environment> [branch]
allowed-tools: Bash
disable-model-invocation: true
---

Deploy to $1 environment from ${2:-main} branch.

Run tests, build, and deploy with validation.
```

**Validation:**
```
✅ YAML syntax: Valid
✅ Description: Present and descriptive
✅ argument-hint: Properly formatted
✅ disable-model-invocation: Correctly set (prevents accidental deployment)
✅ Command body: Uses $1, $2 arguments correctly
✅ No placeholders
```

**Quality grade: A (92/100)**

---

### Example 4: Batch Validation

**Scenario:** Validate all Skills in project

```bash
# Find all Skills
for skill_dir in .claude/skills/*/; do
  skill_name=$(basename "$skill_dir")
  skill_file="$skill_dir/SKILL.md"

  if [ -f "$skill_file" ]; then
    echo "Validating: $skill_name"

    # Run validation
    python3 validate.py "$skill_file"

    echo "---"
  fi
done
```

**Output:**
```
Validating: artifact-advisor
✅ Grade: A (94/100)
---
Validating: skill-builder
✅ Grade: A (92/100)
---
Validating: pdf-processor
⚠️ Grade: C (75/100)
Issues: Description too short, missing triggers
---
```

**Summary:**
```
Total Skills: 3
Grade A: 2 (67%)
Grade B: 0 (0%)
Grade C: 1 (33%)
Grade D or below: 0 (0%)

Recommendation: Fix pdf-processor description
```

---

### Example 5: Pre-Deployment Validation

**Scenario:** Validate Skill before git commit

**Workflow:**
```bash
# 1. Run full validation
python3 .claude/scripts/validate-artifact.py .claude/skills/new-skill/SKILL.md

# 2. Check for critical issues
if [ $? -ne 0 ]; then
  echo "❌ Validation failed - fix issues before committing"
  exit 1
fi

# 3. Check grade threshold
GRADE=$(python3 validate.py SKILL.md | grep "Grade:" | cut -d: -f2 | xargs | cut -c1)

if [ "$GRADE" != "A" ] && [ "$GRADE" != "B" ]; then
  echo "⚠️ Grade $GRADE - consider improving before deployment"
  echo "Proceed anyway? (y/n)"
  read response
  if [ "$response" != "y" ]; then
    exit 1
  fi
fi

# 4. All checks passed
echo "✅ Validation passed - ready to commit"
```

## Common Patterns

### Pattern 1: Quick Validation Check

Run a fast check for critical issues only:

```bash
validate_quick() {
  local file=$1

  # Check YAML syntax
  python3 -c "import yaml; yaml.safe_load(open('$file').read().split('---')[1])" 2>&1

  # Check name field exists
  grep -q "^name:" "$file" || echo "❌ Missing 'name' field"

  # Check description exists
  grep -q "^description:" "$file" || echo "❌ Missing 'description' field"

  # Check description length
  DESC_LEN=$(grep "^description:" "$file" | cut -d: -f2- | wc -c)
  if [ $DESC_LEN -gt 1024 ]; then
    echo "❌ Description too long: $DESC_LEN chars"
  fi
}
```

### Pattern 2: Continuous Integration Validation

Validate all artifacts in CI/CD pipeline:

```yaml
# .github/workflows/validate-artifacts.yml
name: Validate Claude Code Artifacts

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Validate Skills
        run: |
          for skill in .claude/skills/*/SKILL.md; do
            python3 scripts/validate.py "$skill" || exit 1
          done

      - name: Validate Commands
        run: |
          for cmd in .claude/commands/*.md; do
            python3 scripts/validate.py "$cmd" || exit 1
          done

      - name: Check grades
        run: |
          python3 scripts/grade-report.py
```

### Pattern 3: Interactive Validation with Fixes

Validate and offer to fix common issues:

```python
def validate_with_fixes(filepath):
    """Validate and optionally fix issues."""

    issues = validate_artifact(filepath)

    for issue in issues:
        print(f"\n{issue['severity']} {issue['message']}")

        if issue['fixable']:
            response = input("Apply automatic fix? (y/n): ")
            if response.lower() == 'y':
                apply_fix(filepath, issue)
                print("✅ Fixed")
```

## Troubleshooting

### Issue 1: "YAML syntax error" on valid YAML

**Symptoms:** Validator reports syntax error but YAML looks correct

**Cause:** Hidden characters (tabs, smart quotes, BOM)

**Solution:**
```bash
# Check for tabs
grep -P '\t' SKILL.md
# Replace tabs with spaces
sed -i 's/\t/    /g' SKILL.md

# Check for smart quotes
grep -P '[""]' SKILL.md
# Replace with straight quotes manually

# Remove BOM if present
sed -i '1s/^\xEF\xBB\xBF//' SKILL.md
```

### Issue 2: Name mismatch false positive

**Symptoms:** Validator says names don't match but they appear identical

**Cause:** Whitespace in YAML name field

**Solution:**
```bash
# Check exact value
grep "^name:" SKILL.md | cat -A
# Should see: name: skill-name$

# If you see: name: skill-name $ (space before $)
# Fix by trimming:
sed -i 's/^name: \(.*\) *$/name: \1/' SKILL.md
```

### Issue 3: Description passes validation but doesn't activate

**Symptoms:** Skill validated successfully but doesn't activate in practice

**Cause:** Validation checks structure, not real-world activation

**Solution:**
1. Run activation testing protocol (separate from validation)
2. Validation ≠ activation testing
3. Use activation-test-protocol.md for real tests
4. Validation ensures artifact CAN work, activation testing ensures it DOES work

### Issue 4: Grade seems too low

**Symptoms:** Skill feels high quality but gets low grade

**Cause:** Grading is strict and focuses on specific metrics

**Diagnosis:**
```
Check breakdown:
- Verbs: Low score? Add more action verbs to description
- Technologies: Low score? Mention specific tools/file types
- Triggers: 0 points? Missing "Use when..." clause
- Efficiency: Low score? Description too short or too long
```

**Fix:** Address lowest-scoring dimension first

## Best Practices

### Do's ✅

- ✅ Run validation before committing artifacts to git
- ✅ Aim for Grade A (≥90) on all artifacts
- ✅ Fix critical issues (YAML syntax, missing fields) immediately
- ✅ Address warnings (low description quality) before deployment
- ✅ Validate after every significant edit
- ✅ Use validation in CI/CD pipelines
- ✅ Keep validation scripts up to date with latest specs

### Don'ts ❌

- ❌ Don't deploy artifacts with validation errors
- ❌ Don't ignore warnings - they predict real problems
- ❌ Don't confuse validation with activation testing
- ❌ Don't over-optimize for validation score (natural quality matters)
- ❌ Don't skip validation because artifact "seems fine"
- ❌ Don't validate only new artifacts (validate existing ones too)

## Quality Framework Reference

The validation system uses the Centauro quality framework:

**Q = 0.40·Relevance + 0.30·Completeness + 0.20·Consistency + 0.10·Efficiency**

**Dimensions:**

**Relevance (R) - 40% weight:**
- Does artifact solve the stated problem?
- Is description focused and specific?
- Are examples relevant to use cases?

**Completeness (C) - 30% weight:**
- Are all required fields present?
- Does it have sufficient examples?
- Is methodology explained?

**Consistency (S) - 20% weight:**
- Naming conventions followed?
- Terminology consistent?
- Structure matches spec?

**Efficiency (E) - 10% weight:**
- Description concise but informative?
- No redundant content?
- Optimal length?

**Grading scale:**
- A: ≥0.90 (Excellent)
- B+: 0.85-0.89 (Very Good)
- B: 0.80-0.84 (Good)
- C: 0.70-0.79 (Acceptable)
- D: 0.60-0.69 (Poor)
- F: <0.60 (Failing)

## Related Skills

**Use with:**
- **skill-builder:** Create Skills, then validate with artifact-validator
- **artifact-advisor:** Decide artifact type, create it, then validate
- **artifact-troubleshooter:** If validation finds issues, use for deep debugging

**External tools:**
- **yamllint:** Advanced YAML linting
- **markdownlint:** Markdown syntax checking
- **pre-commit hooks:** Automatic validation before commits

---

**Validate early, validate often. Quality artifacts are the foundation of effective Claude Code workflows.**
