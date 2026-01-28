---
name: curriculum-package-common-cartridge
description: Generate IMS Common Cartridge 1.3 packages with QTI assessments, LTI tool links, discussion forums, and full gradebook integration. Use when creating portable, interoperable LMS packages for Canvas, Moodle, Blackboard. Activates on "create Common Cartridge", "CC package", "IMS CC", or "interoperable LMS package".
---

# Common Cartridge Package Generation

Create IMS Common Cartridge 1.3 packages with complete course structure, QTI 2.1 assessments, LTI tool integration, and gradebook setup for maximum interoperability across LMS platforms.

## When to Use

- Create portable LMS packages (works across Canvas, Moodle, Blackboard, D2L, Schoology)
- Export courses with QTI 2.1 assessments (portable assessment format)
- Include LTI tools in course packages
- Set up gradebook categories and weights
- Package courses with discussion forums
- Need better interoperability than SCORM provides

## Advantages Over SCORM

| Feature | SCORM | Common Cartridge |
|---------|-------|------------------|
| **Assessment Format** | Embedded in content | QTI 2.1 (portable) |
| **External Tools** | No | LTI 1.1/1.3 support |
| **Gradebook Setup** | Basic scoring | Full categories & weights |
| **Discussion Forums** | No | Native support |
| **Interoperability** | LMS-specific wrappers | Platform-agnostic |
| **Modern LMS Support** | Declining | Preferred format |

**Use Common Cartridge when:**
- You need QTI assessments (portable across systems)
- You want to embed LTI tools (e.g., YouTube, Google Docs, simulations)
- You need full gradebook configuration
- You want discussion forums in the package
- You need maximum interoperability

**Use SCORM when:**
- You need simple completion tracking
- Legacy LMS requires it
- Content is standalone module (not full course)

## Required Inputs

- **Curriculum Materials**: Lessons (HTML/Markdown), assessments (QTI 2.1), resources
- **Course Metadata**: Title, code, description, dates, copyright
- **Gradebook Configuration**: Assignment groups, weights, grading standards
- **Optional**: LTI tools, discussion forums, prerequisites

## Templates Available

All templates in `/templates/common-cartridge/`:
- `imsmanifest.xml` - Main manifest (required)
- `course-settings.xml` - Gradebook and course configuration
- `lti-tool.xml` - LTI Basic 1.0/1.1 tool links
- `discussion-topic.xml` - Discussion forums
- `assessment-meta.xml` - QTI assessment metadata
- `web-link.xml` - External web links

See `/templates/common-cartridge/README.md` for full documentation.

## Workflow

### 1. Gather Course Components

Collect and organize:
- **Course Information**: Title, code, description, dates, credits
- **Learning Objectives**: Aligned to standards (TEKS, CCSS, NGSS, etc.)
- **Lessons**: HTML files with content
- **Assessments**: QTI 2.1 XML files (use curriculum.export-qti skill)
- **Multimedia**: Images, videos, audio (optimized)
- **Resources**: PDFs, documents, handouts
- **LTI Tools** (optional): External tool configurations
- **Discussion Topics** (optional): Forum prompts and settings

### 2. Structure Course Hierarchy

Define organizational structure:

```
Course: Introduction to Biology (BIO-101)
├── Module 1: Cell Structure
│   ├── Lesson 1.1: Cell Membranes
│   ├── Lesson 1.2: Organelles
│   ├── Lab Activity: Microscope Use (LTI tool)
│   ├── Discussion: Cell Theory Debate
│   └── Assessment: Module 1 Quiz (QTI)
├── Module 2: Genetics
│   ├── Lesson 2.1: DNA Structure
│   ├── Lesson 2.2: Replication
│   ├── Interactive Sim: DNA Replication (LTI)
│   ├── Discussion: Ethics of Genetic Engineering
│   └── Assessment: Genetics Test (QTI)
└── Final Exam (QTI)
```

### 3. Configure Gradebook

Set up assignment groups and weights:

```xml
<assignment_groups>
  <assignment_group identifier="grp-quizzes">
    <title>Module Quizzes</title>
    <group_weight>30</group_weight>
  </assignment_group>
  <assignment_group identifier="grp-discussions">
    <title>Discussions</title>
    <group_weight>20</group_weight>
  </assignment_group>
  <assignment_group identifier="grp-labs">
    <title>Lab Activities</title>
    <group_weight>20</group_weight>
  </assignment_group>
  <assignment_group identifier="grp-exams">
    <title>Exams</title>
    <group_weight>30</group_weight>
  </assignment_group>
</assignment_groups>
```

Total weights should sum to 100%.

### 4. Generate Package Structure

Create directory structure:

```bash
course-package/
├── imsmanifest.xml              # Main manifest (required)
├── course-settings.xml          # Course config (optional but recommended)
├── lessons/
│   ├── lesson-1-1.html
│   ├── lesson-1-2.html
│   ├── lesson-2-1.html
│   └── lesson-2-2.html
├── assessments/
│   ├── module-1-quiz/
│   │   ├── assessment_meta.xml
│   │   └── assessment.xml       # QTI 2.1
│   ├── module-2-test/
│   │   ├── assessment_meta.xml
│   │   └── assessment.xml
│   └── final-exam/
│       ├── assessment_meta.xml
│       └── assessment.xml
├── discussions/
│   ├── cell-theory-debate.xml
│   └── ethics-genetic-eng.xml
├── lti-tools/
│   ├── microscope-sim.xml
│   └── dna-replication-sim.xml
├── resources/
│   ├── images/
│   │   ├── cell-diagram.png
│   │   └── dna-structure.png
│   ├── videos/
│   │   └── cell-division.mp4
│   └── documents/
│       └── lab-safety-guidelines.pdf
└── web-links/
    └── khan-academy-biology.xml
```

### 5. Generate imsmanifest.xml

Use template with variable substitution:

```xml
<manifest identifier="bio-101-2025">
  <metadata>
    <schema>IMS Common Cartridge</schema>
    <schemaversion>1.3.0</schemaversion>
    <lomimscc:lom>
      <lomimscc:general>
        <lomimscc:title>
          <lomimscc:string>Introduction to Biology</lomimscc:string>
        </lomimscc:title>
      </lomimscc:general>
    </lomimscc:lom>
  </metadata>

  <organizations>
    <organization identifier="org-bio-101" structure="rooted-hierarchy">
      <item identifier="root">
        <title>Introduction to Biology</title>

        <!-- Module 1 -->
        <item identifier="mod-1">
          <title>Module 1: Cell Structure</title>

          <!-- Lesson 1.1 -->
          <item identifier="lesson-1-1" identifierref="res-lesson-1-1">
            <title>Lesson 1.1: Cell Membranes</title>
          </item>

          <!-- Quiz -->
          <item identifier="quiz-1" identifierref="res-quiz-1">
            <title>Module 1 Quiz</title>
          </item>
        </item>
      </item>
    </organization>
  </organizations>

  <resources>
    <!-- Webcontent Resource -->
    <resource identifier="res-lesson-1-1" type="webcontent" href="lessons/lesson-1-1.html">
      <file href="lessons/lesson-1-1.html"/>
      <file href="resources/images/cell-diagram.png"/>
    </resource>

    <!-- QTI Assessment -->
    <resource identifier="res-quiz-1" type="imsqti_xmlv1p2/imscc_xmlv1p3/assessment" href="assessments/module-1-quiz/assessment_meta.xml">
      <file href="assessments/module-1-quiz/assessment_meta.xml"/>
      <dependency identifierref="res-quiz-1-qti"/>
    </resource>

    <resource identifier="res-quiz-1-qti" type="associatedcontent/imscc_xmlv1p3/learning-application-resource" href="assessments/module-1-quiz/">
      <file href="assessments/module-1-quiz/assessment.xml"/>
    </resource>
  </resources>
</manifest>
```

### 6. Add QTI Assessments

Export assessments to QTI 2.1 format:

```bash
# Use curriculum.export-qti skill
/curriculum.export-qti --assessment-file "module-1-quiz.json" --output "assessments/module-1-quiz/" --version "2.1"
```

Ensure QTI compliance:
- Item types: Multiple Choice, True/False, Fill-in-the-Blank, Essay, Matching, Ordering
- Response processing
- Feedback (correct/incorrect)
- Scoring

### 7. Add LTI Tools (Optional)

Create LTI tool configurations:

```xml
<!-- lti-tools/microscope-sim.xml -->
<cartridge_basiclti_link>
  <blti:title>Virtual Microscope Simulator</blti:title>
  <blti:launch_url>https://virtualmicroscope.edu/launch</blti:launch_url>
  <blti:custom>
    <lticm:property name="lab_id">cell-structure</lticm:property>
  </blti:custom>
  <blti:extensions platform="canvas.instructure.com">
    <lticm:property name="privacy_level">public</lticm:property>
  </blti:extensions>
</cartridge_basiclti_link>
```

### 8. Add Discussion Forums (Optional)

Create discussion topic configurations:

```xml
<!-- discussions/cell-theory-debate.xml -->
<topic>
  <title>Cell Theory Historical Debate</title>
  <text texttype="text/html">
    <![CDATA[
      <p>Read the historical context of cell theory discovery. Then, discuss:</p>
      <ul>
        <li>Why was cell theory controversial in the 1800s?</li>
        <li>How did microscopy advances enable this discovery?</li>
      </ul>
    ]]>
  </text>
  <discussion_type>threaded</discussion_type>
  <require_initial_post>true</require_initial_post>
  <assignment identifier="assign-discussion-1">
    <points_possible>10</points_possible>
    <grading_type>points</grading_type>
  </assignment>
</topic>
```

### 9. Package as .imscc

```bash
# Create ZIP archive
cd course-package
zip -r ../bio-101-2025.imscc *

# Verify structure
unzip -l ../bio-101-2025.imscc | head -20
```

**Required files:**
- `imsmanifest.xml` (must be at root)
- All resources referenced in manifest

**File naming:**
- Use lowercase, hyphens (not spaces)
- Consistent naming convention
- No special characters

### 10. Validate Package

```bash
# Validate CC 1.3 compliance
/curriculum.validate-cc --package bio-101-2025.imscc
```

**Validation checks:**
- Manifest schema validity (IMS CC 1.3 XSD)
- All file references exist
- QTI 2.1 compliance
- LTI configuration validity
- Resource types correct
- No orphaned files

### 11. Test Import

Test in target LMS platforms:

**Canvas:**
```
1. Go to Course Settings → Import Course Content
2. Select "Common Cartridge 1.x Package"
3. Upload .imscc file
4. Choose content to import (all or selective)
5. Wait for import to complete
6. Verify: modules, lessons, assessments, gradebook
```

**Moodle:**
```
1. Go to Course Administration → Restore
2. Upload .imscc file
3. Select import options
4. Restore to course
5. Verify content and settings
```

**Blackboard:**
```
1. Control Panel → Packages and Utilities → Import Package
2. Select .imscc file
3. Choose import options
4. Submit
5. Verify course content
```

## CLI Interface

```bash
# Basic CC package
/curriculum.package-common-cartridge \
  --materials "curriculum-artifacts/" \
  --output "course.imscc" \
  --course-id "BIO-101" \
  --course-title "Introduction to Biology"

# With gradebook configuration
/curriculum.package-common-cartridge \
  --materials "curriculum-artifacts/" \
  --output "course.imscc" \
  --course-id "BIO-101" \
  --course-title "Introduction to Biology" \
  --gradebook-config "gradebook.json"

# With QTI assessments
/curriculum.package-common-cartridge \
  --materials "curriculum-artifacts/" \
  --qti-dir "assessments/" \
  --output "course.imscc"

# With LTI tools
/curriculum.package-common-cartridge \
  --materials "curriculum-artifacts/" \
  --lti-config "lti-tools.json" \
  --output "course.imscc"

# Full example
/curriculum.package-common-cartridge \
  --materials "curriculum-artifacts/" \
  --qti-dir "assessments/" \
  --lti-config "lti-tools.json" \
  --discussions "discussions/" \
  --gradebook-config "gradebook.json" \
  --course-id "BIO-101" \
  --course-title "Introduction to Biology" \
  --course-code "BIO-101" \
  --start-date "2025-01-15" \
  --end-date "2025-05-15" \
  --output "bio-101-2025.imscc"

# Optimize for specific LMS
/curriculum.package-common-cartridge \
  --materials "curriculum-artifacts/" \
  --optimize-for "canvas" \
  --output "course.imscc"

# Help
/curriculum.package-common-cartridge --help
```

## Integration with Other Skills

**Before Packaging:**

1. **Export QTI Assessments:**
   ```bash
   /curriculum.export-qti --assessment "quiz-1.json" --output "assessments/quiz-1/" --version "2.1"
   ```

2. **Validate Content Accessibility:**
   ```bash
   /curriculum.review-accessibility --materials "lessons/" --standard "WCAG-2.1"
   ```

3. **Check Pedagogical Soundness:**
   ```bash
   /curriculum.review-pedagogy --materials "curriculum-artifacts/"
   ```

**After Packaging:**

4. **Validate CC Package:**
   ```bash
   /curriculum.validate-cc --package "course.imscc"
   ```

5. **Test in LMS (cc-validator agent):**
   ```bash
   /agent.cc-validator --action "test" --package "course.imscc" --lms-targets "canvas,moodle,blackboard"
   ```

## Output Artifacts

**Primary Output:**
- `course.imscc` - Common Cartridge package (ZIP format)

**Optional Outputs:**
- `manifest-validation-report.txt` - Validation results
- `package-structure.txt` - Package contents listing
- `import-instructions.md` - LMS-specific import instructions

## Best Practices

### File Organization

✅ **Do:**
- Use clear, descriptive file names
- Organize by content type (lessons/, assessments/, resources/)
- Use lowercase with hyphens (not spaces)
- Keep file paths under 255 characters

❌ **Don't:**
- Use spaces in file names
- Use special characters (except hyphens, underscores)
- Create deeply nested directories (>5 levels)
- Include absolute file paths

### QTI Assessments

✅ **Do:**
- Use QTI 2.1 format (most compatible)
- Include response processing
- Add feedback for correct/incorrect
- Specify point values
- Include metadata

❌ **Don't:**
- Use proprietary assessment formats
- Embed assessments in HTML (use QTI)
- Forget to link assessments in gradebook

### LTI Tools

✅ **Do:**
- Use HTTPS launch URLs
- Specify privacy level clearly
- Test tool launch in target LMS
- Include icon URLs
- Document custom parameters

❌ **Don't:**
- Use HTTP-only URLs (insecure)
- Forget to configure privacy settings
- Hardcode user information in URLs

### Gradebook Setup

✅ **Do:**
- Make weights sum to 100%
- Group similar assignments
- Specify grading standards
- Link assessments to gradebook
- Set reasonable due dates

❌ **Don't:**
- Leave assignments unweighted
- Create too many categories (4-6 ideal)
- Forget to specify points possible

### Metadata

✅ **Do:**
- Include complete course information
- Add keywords for searchability
- Specify copyright/license
- Include creation date
- Document prerequisites

❌ **Don't:**
- Leave metadata fields empty
- Use vague course descriptions
- Forget copyright information

## Troubleshooting

### Package Won't Import

**Symptom:** LMS rejects .imscc file

**Causes:**
1. Invalid manifest XML
2. Missing required files
3. Incorrect resource types
4. Schema validation failures

**Solutions:**
```bash
# Validate package
/curriculum.validate-cc --package course.imscc

# Check manifest syntax
xmllint --schema imscc_v1p3.xsd imsmanifest.xml

# Verify all files referenced exist
unzip -l course.imscc
```

### Assessments Don't Display

**Symptom:** QTI assessments show as blank or error

**Causes:**
1. Invalid QTI 2.1 XML
2. Missing item files
3. Incorrect resource type in manifest

**Solutions:**
```bash
# Validate QTI
/curriculum.export-qti --validate assessment.xml

# Check resource type in manifest
grep "imsqti_xmlv1p2/imscc_xmlv1p3/assessment" imsmanifest.xml
```

### Gradebook Not Configured

**Symptom:** Assignments don't appear in gradebook

**Causes:**
1. Missing course-settings.xml
2. Assignments not linked to groups
3. No assignment group weights

**Solutions:**
- Ensure course-settings.xml is included
- Link each assignment to assignment_group
- Verify weights sum to 100%

### LTI Tools Don't Launch

**Symptom:** Tool links show error or don't open

**Causes:**
1. Invalid launch URL
2. Missing privacy settings
3. Tool not configured in LMS

**Solutions:**
- Test launch URL manually
- Verify privacy_level is set
- Configure tool provider in LMS first

## Exit Codes

- **0**: Package created successfully
- **1**: Invalid course materials
- **2**: Missing required inputs
- **3**: QTI validation failed
- **4**: Manifest generation failed
- **5**: Packaging (ZIP) failed
- **6**: Validation failed

## References

- [IMS Common Cartridge 1.3 Specification](https://www.imsglobal.org/cc/ccv1p3/imscc_profilev1p3-html/)
- [IMS QTI 2.1 Specification](https://www.imsglobal.org/question/qtiv2p1/imsqti_infov2p1.html)
- [IMS Basic LTI 1.0](https://www.imsglobal.org/specs/ltiv1p0)
- [Canvas CC Documentation](https://canvas.instructure.com/doc/api/file.common_cartridge.html)
- Templates: `/templates/common-cartridge/README.md`
- Production Guide: [PRODUCTION_GUIDE.md](../../../PRODUCTION_GUIDE.md) Section 3

## See Also

- **curriculum.export-qti** - Export assessments to QTI 2.1
- **curriculum.validate-cc** - Validate CC packages
- **curriculum.package-lms** - Alternative LMS packaging (SCORM, Canvas, Moodle)
- **cc-validator agent** - Automated CC testing and validation
- **PRODUCTION_GUIDE.md** - Complete CC production workflows
