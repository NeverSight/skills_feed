---
name: standards-professional-certifications
description: Map training to professional certification requirements including IT (CompTIA, AWS, Azure, Cisco), Project Management (PMI, PMP), Healthcare, Financial Services, and Teaching certifications. Use for certification-aligned training. Activates on "certification", "CompTIA", "AWS", "PMP", or "professional cert".
---

# Standards: Professional Certifications

Align training programs to professional certification requirements and exam objectives.

## When to Use

- Creating certification prep courses
- Corporate training programs
- Professional development courses
- Bootcamps and training providers
- Continuing education

## Major Certification Bodies

### IT Certifications

**CompTIA**:
- A+ (Hardware/OS)
- Network+
- Security+
- Linux+, Cloud+, PenTest+

**Cloud Providers**:
- **AWS**: Solutions Architect, Developer, SysOps, Specialty certs
- **Azure**: Administrator, Developer, Solutions Architect, Specialty
- **Google Cloud**: Associate, Professional certs

**Networking**:
- **Cisco**: CCNA, CCNP, CCIE
- **Juniper**: JNCIA, JNCIS, JNCIE

**Security**:
- CISSP (ISC²)
- CEH (Certified Ethical Hacker)
- CISM, CISA (ISACA)

**Development**:
- Oracle Java certifications
- Microsoft developer certs
- Red Hat certifications

### Project Management

**PMI (Project Management Institute)**:
- **PMP** (Project Management Professional)
- **CAPM** (Certified Associate)
- **PMI-ACP** (Agile)
- **PgMP** (Program Management)

**Agile/Scrum**:
- Scrum.org: PSM, PSPO
- Scrum Alliance: CSM, CSPO
- SAFe certifications

### Business/Finance

**Financial Services**:
- **CFA** (Chartered Financial Analyst)
- **CFP** (Certified Financial Planner)
- **Series 7, 63, 65** (FINRA)
- **CPA** (Certified Public Accountant)

**Business Analysis**:
- CBAP, CCBA (IIBA)
- PMI-PBA

### Healthcare

**Medical**:
- ACLS, BLS, PALS (American Heart Association)
- Nursing certifications (ANCC)
- Medical specialty boards

**Health IT**:
- CAHIMS, CPHIMS (HIMSS)

### Teaching

**K-12 Teaching**:
- State teaching licenses
- **NBPTS** (National Board for Professional Teaching Standards)
- Praxis exams

**Higher Education**:
- Discipline-specific certifications

### Manufacturing/Quality

**Lean/Six Sigma**:
- Six Sigma Green Belt, Black Belt
- Lean certifications

**Quality**:
- ASQ (American Society for Quality) certs

## Certification Mapping Process

### 1. Exam Blueprint Analysis

**Components**:
- Domains/categories
- Weightings (% of exam)
- Objectives/tasks
- Knowledge statements

### 2. Content Coverage Mapping

**Create Matrix**:
- Certification objective
- Course module/lesson
- Coverage depth
- Assessment alignment

### 3. Practice Exam Alignment

**Question Banks**:
- Map questions to objectives
- Ensure coverage of all domains
- Match difficulty and format
- Include performance-based questions

### 4. Gap Analysis

**Identify**:
- Uncovered objectives
- Under-covered domains
- Missing prerequisite knowledge

## Example: AWS Solutions Architect Associate

**Exam Domains**:
1. Design Resilient Architectures (30%)
2. Design High-Performing Architectures (28%)
3. Design Secure Applications and Architectures (24%)
4. Design Cost-Optimized Architectures (18%)

**Objectives per Domain**: 3-5 detailed objectives

**Mapping**:
- Module → Domain
- Lab → Objective
- Practice question → Specific task

## CLI Interface

```bash
# Map to certification
/standards.professional-certifications --training "aws-course/" --cert "AWS-SAA-C03"

# Coverage analysis
/standards.professional-certifications --content "pmp-prep/" --cert "PMI-PMP" --gap-analysis

# Multiple certifications
/standards.professional-certifications --course "cloud-fundamentals/" --certs "AWS-CLF,Azure-AZ900,GCP-ACE" --crosswalk

# Practice exam alignment
/standards.professional-certifications --questions "practice-exams/" --cert "CompTIA-Security-Plus" --validate-coverage
```

## Output

- Certification objectives coverage map
- Domain weightings and coverage
- Gap analysis with recommendations
- Practice exam alignment report
- Study plan based on exam blueprint

## Composition

**Input from**: `/curriculum.design`, `/curriculum.develop-content`, `/curriculum.develop-items`
**Works with**: `/standards.gap-analysis`, `/standards.coverage-validator`
**Output to**: Certification-aligned training programs

## Exit Codes

- **0**: Certification mapping complete
- **1**: Certification not recognized
- **2**: Exam blueprint not available
- **3**: Coverage gaps too large
