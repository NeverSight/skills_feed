---
name: "open-source-license"
description: "Open Source License guidance, selection, compliance review, and drafting. Use this skill when users ask about choosing open source licenses, checking license compatibility, reviewing projects for OSS compliance, generating LICENSE/NOTICE files, or understanding specific license terms. Triggers include questions about MIT, Apache, GPL, BSD, LGPL, AGPL, copyleft, permissive licenses, license compatibility, SPDX identifiers, or any OSS licensing topic."
metadata:
  author: "Skala Inc."
  license: "Apache-2.0"
  license-notice: "See LICENSE and NOTICE files in the repository"
  homepage: "https://skala.io/legal-skills"
  repository: "https://github.com/skala-io/legal-skills"
---

*First published on [Skala Legal Skills](https://www.skala.io/legal-skills)*

## Legal Disclaimer

This skill is provided for informational and educational purposes only and does not constitute legal advice. The analysis and information provided should not be relied upon as a substitute for consultation with a qualified attorney. No attorney-client relationship is created by using this skill. Open source licensing involves complex legal considerations that may vary by jurisdiction. Laws and regulations vary by jurisdiction and change over time. Always consult with a licensed attorney in your jurisdiction for advice on specific legal matters. The creators and publishers of this skill disclaim any liability for actions taken or not taken based on the information provided.

---

# Open Source License Skill

Comprehensive guidance for open source license selection, compliance review, and documentation drafting.

## Capabilities

### 1. License Selection
Help users choose the right license based on their goals using the decision tree.

### 2. License Comparison
Explain differences between licenses, compatibility, and trade-offs.

### 3. Compliance Review
Analyze projects for license compliance issues and compatibility conflicts.

### 4. License Drafting
Generate LICENSE files, NOTICE files, and source file headers using canonical texts.

## Workflow

### For License Selection Questions

1. Read `references/selection/decision-tree.md`
2. Ask clarifying questions based on the decision tree:
   - Primary goal (adoption vs keeping code open)?
   - Patent protection needed?
   - Library or application?
   - SaaS/network use?
3. Provide recommendation with reasoning
4. Reference notable projects using recommended license
5. Offer to generate LICENSE file if desired

### For License Comparison Questions

1. Read `references/selection/comparison-matrix.md`
2. Compare requested licenses across key dimensions:
   - Permissions (commercial use, distribution, modification)
   - Conditions (attribution, copyleft, source disclosure)
   - Limitations (liability, warranty)
3. Highlight key differences
4. Provide examples of projects using each license

### For Compliance Review

1. Read `references/compliance/compatibility.md` and `references/compliance/checklist.md`
2. Identify all licenses in the project
3. Check compatibility between licenses
4. Flag any copyleft licenses that may affect distribution
5. Note any missing attribution or compliance gaps
6. Provide actionable remediation steps
7. Reference `references/compliance/common-issues.md` for context

### For License/NOTICE File Generation

1. Read appropriate template from `references/templates/`
2. **CRITICAL: Always use canonical license text exactly as provided**
3. Never modify license terms or generate license text from scratch
4. Only fill in placeholders: `[YEAR]`, `[FULLNAME]`, `[PROJECT NAME]`
5. For NOTICE files, aggregate third-party attributions properly
6. For headers, use language-appropriate comment syntax

## Reference Files

| Topic | File |
|-------|------|
| Permissive licenses (MIT, Apache, BSD, ISC) | `references/licenses/permissive.md` |
| Copyleft licenses (GPL, LGPL, AGPL, MPL) | `references/licenses/copyleft.md` |
| Other licenses (CC, Boost, zlib) | `references/licenses/specialty.md` |
| License comparison table | `references/selection/comparison-matrix.md` |
| License selection guide | `references/selection/decision-tree.md` |
| License compatibility rules | `references/compliance/compatibility.md` |
| Compliance checklist | `references/compliance/checklist.md` |
| Common compliance mistakes | `references/compliance/common-issues.md` |
| LICENSE file templates | `references/templates/license-files.md` |
| NOTICE file templates | `references/templates/notice-files.md` |
| Source header templates | `references/templates/source-headers.md` |

## Key Rules

### Never Generate License Text

Always use canonical license text from templates. License texts are legal documents that must be exact. Do not:
- Paraphrase license terms
- Generate license text from memory
- Modify standard license language
- Create "custom" licenses

### Include Project Examples

When discussing licenses, mention notable projects that use them:
- **MIT:** React, Node.js, jQuery, Rails, Angular
- **Apache-2.0:** Kubernetes, TensorFlow, Android, Spark
- **GPL-3.0:** WordPress, GIMP, Bash
- **AGPL-3.0:** Nextcloud, Mastodon, Grafana
- **BSD-3-Clause:** Django, Flask, numpy
- **MPL-2.0:** Firefox, Thunderbird

### Flag Complex Scenarios

Recommend legal counsel for:
- Dual licensing strategies
- License changes mid-project
- Commercial projects with copyleft dependencies
- AGPL in SaaS environments
- Multi-jurisdictional distribution
- Patent-sensitive situations

## Quick Answers

### "What license should I use?"
→ Follow decision tree; default to MIT for simplicity or Apache-2.0 for patent protection.

### "Can I use GPL code in my proprietary app?"
→ Generally no, unless through LGPL dynamic linking or separate processes.

### "What's the difference between MIT and Apache-2.0?"
→ Apache-2.0 includes explicit patent grant and retaliation clause; MIT is simpler but no patent protection.

### "Is Apache-2.0 compatible with GPL?"
→ Apache-2.0 is compatible with GPL-3.0, but NOT with GPL-2.0.

### "Do I need to open source my code if I use AGPL?"
→ Only if you modify the AGPL code AND provide it as a network service. Using unmodified AGPL tools internally doesn't trigger copyleft.

## Output Format

When generating LICENSE files:
1. Confirm the license choice
2. Ask for copyright holder name and year
3. Output the complete canonical license text
4. Remind user to place it in repository root as `LICENSE` or `LICENSE.txt`

When reviewing compliance:
1. List all identified licenses
2. Show compatibility analysis
3. Flag any issues with severity (critical/warning/info)
4. Provide specific remediation steps
