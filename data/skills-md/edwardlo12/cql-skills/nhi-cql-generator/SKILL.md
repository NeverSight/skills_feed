---
name: nhi-cql-generator
description: Generate CQL Library and FHIR ValueSet artifacts for Taiwan NHI (National Health Insurance) reimbursement rules from rule text. Use when user asks to create CQL/ValueSet for 健保給付規則, 藥品審查, NHI CQL, 健保代碼, or payment審查. This skill applies patterns learned from 50+ GT examples.
---

# NHI CQL Generator

Generate CQL Library (.cql) and FHIR ValueSet (.json) files from Taiwan NHI reimbursement rules text.

## Overview

This skill generates standardized clinical decision support artifacts for Taiwan's National Health Insurance system:
1. **CQL Library** - Clinical Quality Language for payment審查邏輯
2. **FHIR ValueSet** - Code sets (適應症, 禁忌症, 藥品, etc.)
3. **Dependency Libraries** - Required CQL libraries that must accompany every generated CQL file

**Critical**: All patterns are learned from 50+ GT examples. Do NOT deviate from documented patterns.

### Required Dependency Libraries

Every generated CQL file depends on two shared libraries located in `.github/skills/nhi-cql-generator/assets/`:

1. **FHIRHelpers.cql** (version 4.0.1)
   - Provides FHIR data model interaction helpers
   - Converts FHIR types to CQL types
   - Required by all FHIR-based CQL libraries

2. **CDSConnectCommonsForFHIRv401.cql** (version 2.1.0, aliased as C3F)
   - Provides common clinical decision support functions that can be used directly
   - **Frequently used functions**:
     * `C3F.Confirmed(Conditions)` - Filter confirmed conditions
     * `C3F.Verified(Observations)` - Filter verified observations  
     * `C3F.MostRecent(Observations)` - Get most recent observation
     * `C3F.QuantityValue(Observation)` - Extract quantity value
     * `C3F.ObservationLookBack(Observations, LookBack)` - Observations in time window
     * `C3F.MostRecentProcedure(Procedures)` - Get most recent procedure
     * `C3F.ActiveCondition(Conditions)` - Filter active conditions
     * `C3F.PeriodToInterval(Period)` - Convert FHIR Period to CQL Interval
   - **Usage**: Directly use C3F functions with the `C3F.` prefix (e.g., `C3F.Confirmed([Condition: "code"])`)
   - **Note**: GT examples redundantly redefine these functions, but this is unnecessary - you should use C3F functions directly

**IMPORTANT**: When generating CQL artifacts, you MUST copy these two files to the output directory alongside the generated `.cql` files. Without them, the CQL will fail with error:
```
Could not load source for library CDSConnectCommonsForFHIRv401, version 2.1.0, namespace uri null.
```

## CQL Structure Patterns

### Library Declaration

```cql
library "[規則編號]" version '0.0.1'
```

- **Library name**: Exact rule code (e.g., "08111B", "12216C", "69041B")
- **Version**: Always `'0.0.1'`

### Standard Headers (Fixed Order)

```cql
library "[規則編號]" version '0.0.1'

using FHIR version '4.0.1'

include "FHIRHelpers" version '4.0.1' called FHIRHelpers
include "CDSConnectCommonsForFHIRv401" version '2.1.0' called C3F
```

**Never change**: FHIR version, FHIRHelpers version, C3F version, or aliases.

### ValueSet Declarations

After include statements, before codesystem declarations:

```cql
valueset "[中文名稱] valueset": '[ValueSet URL]'
```

**URL Pattern**: `https://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.[sequential-number]`

**Examples**:
- `valueset "17022B 呼氣一氧化氮監測(FeNO) valueset": 'https://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.6'`
- `valueset "糖尿病合併慢性腎病變 valueset": 'https://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.46'`

### CodeSystem URLs (Complete Approved List)

Use **ONLY** these codesystem URLs:

```cql
codesystem "ICD-10-CM": 'http://hl7.org/fhir/sid/icd-10-cm'
codesystem "ICD-10-PCS": 'http://www.cms.gov/Medicare/Coding/ICD10'
codesystem "LOINC": 'http://loinc.org'
codesystem "SCT": 'http://snomed.info/sct'
codesystem "TWMedicalServicePayment": 'https://twcore.mohw.gov.tw/ig/twcore/CodeSystem/medical-service-payment-tw'
codesystem "CONDVERSTATUS": 'http://terminology.hl7.org/CodeSystem/condition-ver-status'
codesystem "CONDCLINSTATUS": 'http://terminology.hl7.org/CodeSystem/condition-clinical'
codesystem "ActCode": 'http://terminology.hl7.org/CodeSystem/v3-ActCode'
```

### Context Declaration

```cql
context Patient
```

Always use `Patient` context.

### Define Statements Pattern

**Standard structure** observed in all examples:

```cql
define "[適應症或條件名稱]":
  exists ( C3F.Confirmed([Condition: "[valueset名稱]"]) )

define "MeetsInclusionCriteria":
  "[主要適應症]"
  
define "InPopulation":
  "MeetsInclusionCriteria"

define "Recommendation":
  if "InPopulation" then '健保給付[點數]點' 
    else null

define "Rationale":
  null

define "Links":
  null

define "Suggestions":
  null

define "Errors":
  null
```

### Using C3F Helper Functions

**Direct Usage** - Use C3F library functions directly without redefining them:

```cql
// ✅ Correct: Use C3F functions directly
define "適應症":
  exists ( C3F.Confirmed([Condition: "適應症 valueset"]) )

define "Recent Observations":
  C3F.ObservationLookBack([Observation: "code"], 1 year)

define "Lab Value":
  C3F.QuantityValue( C3F.MostRecent([Observation: "code"]) )
```

**Common C3F Functions**:
- `C3F.Confirmed(Conditions)` - Filters to confirmed conditions (verificationStatus = 'confirmed')
- `C3F.Verified(Observations)` - Filters to verified observations (status = 'final', 'corrected', or 'amended')
- `C3F.ObservationLookBack(Observations, LookBack)` - Observations within time window
- `C3F.MostRecent(Observations)` - Most recent observation by effective date
- `C3F.QuantityValue(Observation)` - Extract quantity value from observation
- `C3F.MostRecentProcedure(Procedures)` - Most recent procedure
- `C3F.ActiveCondition(Conditions)` - Active conditions (clinicalStatus = 'active', no abatement)
- `C3F.PeriodToInterval(Period)` - Convert FHIR Period to CQL Interval

**Note**: GT examples redundantly redefine these functions at the end of each file, but this is **unnecessary duplication**. Simply use `C3F.FunctionName()` directly.

## Common Logic Patterns

### Condition Checking

```cql
exists ( C3F.Confirmed([Condition: "[valueset名稱]"]) )
```

### Multiple Conditions (OR)

```cql
exists ( C3F.Confirmed([Condition: "valueset1"])
    union C3F.Confirmed([Condition: "valueset2"])
)
```

### Multiple Conditions (AND)

```cql
"condition1" and "condition2"
```

### Observation with Time Window

```cql
Count(C3F.ObservationLookBack([Observation: "[code]"], 1 year)) < 3
```

### Age Checking

```cql
AgeInYears() >= 6 and AgeInYears() < 13
```

### Encounter with Specialty

```cql
[Encounter: "[valueset]"] E
  where ( E.serviceType ~ "[specialty code]" )
```

### Procedure Lookback (using C3F)

```cql
C3F.ProcedureLookBack([Procedure: "[code]"], 6 months)
```

### Nested Conditionals (for複雜給付條件)

```cql
define "Recommendation":
  if "condition1" then if "condition2" then '說明A'
    else '說明B'
  else if "condition3" then '說明C'
  else null
```

### Subpopulations Pattern

For rules with multiple適應症 with different頻率:

```cql
define "subpopulation 1":
  if "InPopulation" is not true then null 
    else [specific condition for subpop1]

define "subpopulation 2":
  if "InPopulation" is not true then null 
    else [specific condition for subpop2]
    
define "Recommendation":
  if "subpopulation 1" then '健保給付[點數]點，[規範1]'
  else if "subpopulation 2" then '健保給付[點數]點，[規範2]'
  else null
```

## Medical Knowledge Mapping

### Spinal Disorders Coding

When rules mention "脊髓損傷或病變", include **ALL** three categories:

| Category | ICD-10-CM | Examples |
|----------|-----------|----------|
| **Trauma** | S14.*, S24.*, S34.*, S44.* | Spinal cord injury |
| **Disease** | G95.*, G82.* | Spinal cord disorders, paraplegia |
| **Degeneration** | M43.3, M47.1, M50.0, M51.0 | Spondylolisthesis, myelopathy, disc disorders |

**Critical**: "病變" includes both functional disease (G-codes) AND degenerative structural changes (M-codes).

### Stroke Sequelae Coding

For "腦中風後遺症" or "中風導致之肢體偏癱":

| Scope | ICD-10-CM | Purpose |
|-------|-----------|---------|
| **General stroke** | I69.* | All stroke sequelae |
| **Hemiplegia types** | I69.33-I69.35 | Dominant/non-dominant/unspecified side |
| **Specific sequelae** | I69.3, I69.33, I69.34, I69.35, I69.39 | Cerebral infarction aftereffects |

**Pattern**: Use I69.* for broad inclusion, add specific I69.3X codes when hemiplegia is explicitly mentioned.

### Peripheral Neuropathy

For "周邊神經病變":

- **Diabetic**: E11.4* (Type 2 DM with neurological complications)
- **General**: G62.* (polyneuropathy), G63.* (neuropathy in diseases)
- **Specific**: G62.9 (unspecified polyneuropathy)

### Observation Value Checking Pattern

For laboratory or measurement constraints:

```cql
define "低密度脂蛋白膽固醇異常":
  exists (
    [Observation: "LOINC code 18262-6"] O
      where O.value as Quantity > 100 'mg/dL'
        and O.status = 'final'
  )
```

### Complex Age Range Checks

For rules specifying age ranges with measurement timing:

```cql
define "符合年齡條件":
  ( AgeInYears() >= 10 and AgeInYears() <= 17 )
    or ( AgeInYears() >= 6 and AgeInYears() < 10 and "已測量過基線值" )
```

## Code Style Rules

- **Indentation**: 2 spaces (NO tabs)
- **String quotes**: Single quotes `'...'` for all strings
- **Line breaks**: Blank line between major sections (valuesets, codesystems, context, defines)
- **Comments**: Use `//` sparingly, written in Chinese when explaining業務邏輯
- **Naming**: Chinese variable names permitted (e.g., `define "氣喘":`, `define "懷孕糖尿病人、妊娠糖尿病人":`)
- **Boolean checks**: Use `"variable"` not `"variable" = true`

## NHI Rule Text Parsing

### Rule ID Format

Pattern: `[數字]{2,5}[字母]` (e.g., 08111B, 12216C, 69041B, 83102K)

### Common Phrases to Extract

**適應症 (Indications)**:
- "適應症：", "適應症包括："
- "限...使用", "限...申報"
- "適用於...", "符合..."

**禁忌症 (Contraindications)**:
- "禁忌症：", "不得用於..."
- "排除...", "不適用"

**支付規範 (Payment Rules)**:
- "支付規範：", "執行頻率："
- "每[時間]限申報[次數]次"
- "一年限申報[數字]次"
- "不得同時申報..."

**點數 (Points)**:
- "[數字]點" (e.g., "800點", "17350點")

**專科限制 (Specialty)**:
- "限...專科醫師", "限由...執行"

### Diagnosis Code Extraction

From text patterns like:
- "多發性硬化症、運動神經元疾病、脊髓損傷..." → Create valueset for ICD-10-CM codes
- "四肢自體動脈粥樣硬化（I70.2～I70.7）" → Code range with all subcodes
- "糖尿病酮酸中毒" → Look up ICD-10-CM code

### Frequency Constraints Encoding

| Rule Text | CQL Encoding |
|-----------|--------------|
| "一年限申報三次" | `Count(ObservationLookBack([Observation: ...], 1 year)) < 3` |
| "每四年限申報一次" | `Count(ObservationLookBack([Observation: ...], 4 years)) < 1` |
| "每人以申報一次為原則" | Track across patient lifetime |
| "每次就診...每次治療應間隔至少一週" | Date diff checking |

### Other Regulation Handling (其他規範處理)

**Critical**: Distinguish between **pre-authorization criteria** (事前資格檢查) and **post-payment rules** (事後支付規則).

#### Type 1: Pre-Authorization Criteria → Convert to CQL Logic

These MUST be encoded as executable logic in MeetsInclusionCriteria:

**Pattern: Specialist Restriction** ("限...專科醫師執行")

```cql
codesystem "SCT": 'http://snomed.info/sct'

code "Specialist code": '[SNOMED-code]' from "SCT" display '[specialist-type]'

define "performer_id":
  Last(Split(First("RecentProcedure".performer).actor.reference, '/'))

define "Performer_ref":
  [Practitioner] P where P.id = "performer_id"

define "Qualified_Practitioner":
  exists ( "Performer_ref".qualification q
    where q.code ~ "Specialist code" )

define "MeetsInclusionCriteria":
  "[適應症]" and "Qualified_Practitioner"
```

**Examples**:
- "限外科專科醫師執行" → SNOMED CT: 224555008 (Vascular surgeon)
- "限兒科專科" → SNOMED CT: 24251000087109 (General pediatric specialty)
- "限心臟血管外科" → SNOMED CT: 309296001 (Cardiac surgeon)

**Pattern: Procedure Type Restriction**

When rule specifies specific surgical procedures:

```cql
codesystem "ICD-10-PCS": 'http://www.cms.gov/Medicare/Coding/ICD10'

code "Procedure1 code": '[code]' from "ICD-10-PCS" display '[description]'
code "Procedure2 code": '[code]' from "ICD-10-PCS" display '[description]'

define "ApplicableProcedure":
  C3F.MostRecentProcedure ( [Procedure: "Procedure1 code"]
    union [Procedure: "Procedure2 code"]
  )

define "MeetsInclusionCriteria":
  "[適應症]" and exists("ApplicableProcedure")
```

**Pattern: Encounter Specialty Check**

For rules limiting to specific clinical departments:

```cql
code "Department specialty code": '[SNOMED-code]' from "SCT" display '[specialty]'

define "SpecialtyEncounter":
  [Encounter] E where E.serviceType ~ "Department specialty code"

define "encounter check":
  exists("SpecialtyEncounter")

define "Recommendation":
  if "InPopulation" is not true then null
    else if "encounter check" then '給付'
    else '非[科別]申報，不予給付'
```

#### Type 2: Post-Payment Rules → Include in Recommendation Text Only

These should appear in Recommendation string but NOT in MeetsInclusionCriteria:

**Examples**:
- "一般材料費得另加計百分之五十" → Include in Recommendation only
- "應事先申請" → Include in Recommendation only
- "需檢附...報告" → Include in Recommendation only
- "不得同時申報..." → Include in Recommendation as note

**Pattern**:
```cql
define "Recommendation":
  if "InPopulation" then '健保給付[點數]點，[描述]，一般材料費得另加計百分之五十'
  else null
```

#### Decision Logic: When to Convert to CQL vs Text Only

| Phrase Pattern | Type | Action |
|---------------|------|--------|
| 限...專科醫師執行 | Pre-auth | ✅ Convert to Practitioner.qualification check |
| 限...科別申報 | Pre-auth | ✅ Convert to Encounter.serviceType check |
| 限特定手術類型 | Pre-auth | ✅ Convert to Procedure code check |
| 材料費加計...% | Post-payment | ❌ Text only in Recommendation |
| 應事先申請 | Administrative | ❌ Text only in Recommendation |
| 需檢附報告 | Administrative | ❌ Text only in Recommendation |

**Critical Rule**: If the regulation affects **whether payment is approved**, it's pre-authorization → convert to CQL. If it only affects **how much** or **when** to pay, it's post-payment → text only.

## ValueSet Generation

### ValueSet JSON Template

Based on GT examples, use this complete structure:

```json
{
  "resourceType": "ValueSet",
  "id": "2.16.840.1.113762.1.4.1287.[number]",
  "meta": {
    "versionId": "1",
    "lastUpdated": "[timestamp]",
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/shareablevalueset",
      "http://hl7.org/fhir/us/cqfmeasures/StructureDefinition/computable-valueset-cqfm",
      "http://hl7.org/fhir/us/cqfmeasures/StructureDefinition/publishable-valueset-cqfm"
    ]
  },
  "extension": [
    {
      "url": "http://hl7.org/fhir/StructureDefinition/valueset-author",
      "valueContactDetail": {
        "name": "Industrial Technology Research Institute Author"
      }
    },
    {
      "url": "http://hl7.org/fhir/StructureDefinition/resource-lastReviewDate",
      "valueDate": "[YYYY-MM-DD]"
    },
    {
      "url": "http://hl7.org/fhir/StructureDefinition/valueset-effectiveDate",
      "valueDate": "[YYYY-MM-DD]"
    }
  ],
  "url": "http://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.[number]",
  "identifier": [
    {
      "system": "urn:ietf:rfc:3986",
      "value": "urn:oid:2.16.840.1.113762.1.4.1287.[number]"
    }
  ],
  "version": "[YYYYMMDD]",
  "name": "[EnglishCamelCaseName]",
  "title": "[English title or Chinese title]",
  "status": "active",
  "date": "[timestamp]",
  "publisher": "Industrial Technology Research Institute Steward",
  "description": "[規則編號，可多個用逗號分隔如 63007B, 63008B]",
  "jurisdiction": [
    {
      "extension": [
        {
          "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
          "valueCode": "unknown"
        }
      ]
    }
  ],
  "purpose": "(Clinical Focus: ...),(Data Element Scope: ...),(Inclusion Criteria: ...),(Exclusion Criteria: ...)",
  "compose": {
    "include": [
      {
        "system": "[CodeSystem URL]",
        "version": "2025",
        "filter": [
          {
            "property": "concept",
            "op": "[operator]",
            "value": "[code]"
          }
        ]
      }
    ]
  }
}
```

### ID Naming Convention

Pattern: `2.16.840.1.113762.1.4.1287.[sequential-number]`

The ID is the **full OID**, not a custom name. File name matches the ID:
- File: `2.16.840.1.113762.1.4.1287.6.json`
- ID: `"2.16.840.1.113762.1.4.1287.6"`

### URL Pattern

**Critical**: Use `http://` (NOT `https://`) in url field:
```json
"url": "http://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.[number]"
```

**In CQL**: Use `https://` in valueset declarations:
```cql
valueset "name": 'https://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.[number]'
```

### Filter Operators (from GT examples)

Use `filter` instead of explicit `concept` array:

**Common operators**:
- `"op": "descendent-of"` - Include code and all descendants (most common)
- `"op": "is-a"` - Include code and descendants
- `"op": "="` - Exact match single code
- `"op": "in"` - Multiple codes (comma-separated in value)

**Examples**:
```json
// All J45.* asthma codes
{"property": "concept", "op": "descendent-of", "value": "J45"}

// Specific codes
{"property": "concept", "op": "=", "value": "C79.81"}

// Multiple specific codes
{"property": "concept", "op": "in", "value": "E10.22,E13.22,E08.22"}
```

### Filter Operator Selection Strategy

Choose operator based on code specificity and clinical intent:

| Operator | Use When | ICD-10 Code Pattern | Example |
|----------|----------|---------------------|---------|
| **`=`** | Exact leaf code needed | 6-7 digits (e.g., G62.9, I69.398) | Single specific diagnosis |
| **`is-a`** | Mid-level category | 4-5 digits (e.g., J45.5, E11.4) | Specific subtype with few children |
| **`descendent-of`** | Broad family inclusion | 3-4 digits (e.g., J45, I69, G62) | All variants needed |
| **`in`** | Multiple unrelated codes | Mixed | Enumerate disparate codes |

**Code Granularity Guidelines**:
- **Preferred**: Mid-level codes (5-6 digits) - balance precision and coverage
- **Avoid**: Too broad (3 digits: J45 vs J45.*) or too narrow (7+ digits)
- **Quick judgment**: Code length 3-4 → descendent-of; 5-6 → is-a; 7+ → =

**Real Examples from GT**:
```json
// G62.9 (7 digits, leaf code) - use exact match
{"property": "concept", "op": "=", "value": "G62.9"}

// E11.4 (5 digits, mid-level) - use is-a
{"property": "concept", "op": "is-a", "value": "E11.4"}

// I69 (3 digits, broad family) - use descendent-of
{"property": "concept", "op": "descendent-of", "value": "I69"}

// Multiple unrelated codes - use in
{"property": "concept", "op": "in", "value": "M43.3,M47.1,M50.0,M51.0"}
```

**Decision Logic**:
1. If code explicitly ends with .0, .9, or has 6+ digits → `=`
2. If code has 4-5 digits and represents specific subtype → `is-a`
3. If code is 3-4 digits and needs all variants → `descendent-of`
4. If multiple disparate codes listed → `in`

### Purpose Field Format

Standard 4-part structure (observed in all GT examples):

```
(Clinical Focus: [臨床焦點]),(Data Element Scope: [資料元素範圍]),(Inclusion Criteria: [納入條件]),(Exclusion Criteria: [排除條件，若無則寫 No])
```

**Critical**: ValueSet.url in JSON **must exactly match** the valueset declaration URL in CQL (except http vs https).

### Common ValueSet Types

1. **Diagnosis codes** (ICD-10-CM) - Most common
   - System: `http://hl7.org/fhir/sid/icd-10-cm`
   - Version: `"2025"`
   - Use filters, not explicit concept lists
2. **Procedure codes** (ICD-10-PCS or TWMedicalServicePayment)
   - System: `http://www.cms.gov/Medicare/Coding/ICD10` or `https://twcore.mohw.gov.tw/ig/twcore/CodeSystem/medical-service-payment-tw`
3. **Lab tests** (LOINC)
   - System: `http://loinc.org`
4. **Clinical findings** (SNOMED CT)
   - System: `http://snomed.info/sct`

### Multiple Rules Sharing Same ValueSet

From GT examples, one ValueSet may support multiple rules:
- `"description": "63007B, 63008B"` - Modified radical mastectomy (single/bilateral)
- `"description": "13030B,13031B,13032B"` - Different H. pylori tests

When rules share indications, use the same ValueSet ID.

## Workflow

### Step 1: Collect Input

Ask user for:
- **規則編號** (Rule ID) - e.g., "08111B"
- **完整給付規則文字** (Full rule text including適應症, 禁忌症, 支付規範, 點數)

### Step 2: Parse Rule Text

Extract and identify:
- Rule ID
- 點數 (reimbursement points)
- 適應症 (indications) - list of diagnoses/conditions
- 禁忌症 (contraindications) - if any
- 執行頻率限制 (frequency limits)
- 不得同時申報項目 (cannot claim with)
- 專科限制 (specialty restrictions)
- 其他支付規範 (other payment rules)

### Step 3: Generate ValueSets

For **each distinct code set** identified:

1. Create JSON file: `2.16.840.1.113762.1.4.1287.[number].json`
2. Use complete template structure from GT examples
3. Assign sequential OID number
4. Set url with `http://` (NOT https)
5. Populate filter operators based on code patterns:
   - Use `descendent-of` for code families (e.g., J45 for all asthma)
   - Use `in` for multiple specific codes
   - Use `=` for single specific codes
6. Fill purpose field with 4-part structure
7. Save with UTF-8 encoding

**Important**: 
- File name = full OID (e.g., `2.16.840.1.113762.1.4.1287.6.json`)
- url field uses `http://` 
- CQL valueset declaration uses `https://`

### Step 4: Generate CQL Library

Following exact structure:

1. Library declaration with rule ID
2. using FHIR version
3. include statements (FHIRHelpers, C3F)
4. valueset declarations (URLs must match JSON files)
5. codesystem declarations
6. Standard code/concept for Confirmed
7. context Patient
8. define statements (適應症, conditions, InPopulation, Recommendation, etc.)
9. Standard define statements (Rationale, Links, Suggestions, Errors as null)
10. All five helper functions

### Step 5: Validate Generated Files

Checklist:

- ✓ CQL valueset declaration URLs **exactly match** ValueSet JSON url fields
- ✓ Only codesystem URLs from approved list used
- ✓ All five helper functions included at end
- ✓ Structure follows examples (headers, blank lines, 2-space indentation)
- ✓ Recommendation includes 點數 and key給付規範
- ✓ File encoding is UTF-8
- ✓ No tabs, only spaces

### Step 6: Provide Output

Deliver to user:

1. **CQL file**: `[規則編號].cql` (plain text)
2. **ValueSet file(s)**: One or more `2.16.840.1.113762.1.4.1287.[number].json` files
3. **Dependency libraries**: Copy from `.github/skills/nhi-cql-generator/assets/` to output directory:
   - `FHIRHelpers.cql`
   - `CDSConnectCommonsForFHIRv401.cql`
4. **Mapping table**: 

```markdown
| CQL ValueSet Declaration | ValueSet File | URL (CQL uses https, JSON uses http) |
|--------------------------|---------------|---------------------------------------|
| [中文名稱] valueset | 2.16.840.1.113762.1.4.1287.[N].json | https://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.[N] |
```

5. **Validation report**: Confirm all patterns followed ✓

**Critical**: The CQL file will NOT execute without the dependency libraries in the same directory. Always include them in the output.

## Examples

### Example 1: Simple Rule (08111B)

**Input**: 
- Rule ID: 08111B
- 點數: 800點
- 適應症: 凝血異常，疑有Von-willebrands disease者

**Output**:
- `08111B.cql` - With Von Willebrand disease codes
- `2.16.840.1.113762.1.4.1287.1.json` - ICD-10-CM codes with filter for VWD codes

### Example 2: Rule with Frequency (17022B)

**Input**:
- Rule ID: 17022B
- 點數: 748點  
- 適應症: 六歲以上至未滿十三歲確診氣喘患者追蹤使用
- 頻率: 一年最多申報三次
- 專科: 兒科

**Output**:
- `17022B.cql` - With age check, frequency check, and pediatric specialty check
- `2.16.840.1.113762.1.4.1287.6.json` - Uses `descendent-of` filter for J45 (asthma)

### Example 3: Multiple Subpopulations (12216C)

**Input**:
- Rule ID: 12216C
- 點數: 900點
- 適應症1: C型肝炎抗體陽性之HIV感染者、靜脈注射藥癮者 (每一年限一次)
- 適應症2: C型肝炎抗體陽性之慢性血液透析病人 (每四年限一次)

**Output**:
- `12216C.cql` - With subpopulation 1 and 2, different frequency rules
- `2.16.840.1.113762.1.4.1287.[N].json` - HIV codes with appropriate filters
- `2.16.840.1.113762.1.4.1287.[N+1].json` - Dialysis dependency codes

## Important Rules

1. **Never create new codesystem URLs** - Only use the eight approved URLs
2. **Never deviate from standard structure** - Follow examples exactly
3. **Always include all helper functions** - Even if not directly used
4. **CQL and ValueSet URLs must match** - This is absolutely critical
5. **Use patterns, don't innovate** - Combine existing patterns for new scenarios
6. **Chinese in variable names is OK** - This is standard practice
7. **Preserve exact indentation** - 2 spaces, no tabs

## Triggering Keywords

Activate when user mentions:
- NHI CQL, 健保 CQL
- 健保給付規則, 給付審查, 藥品審查
- CQL Library, 健保 ValueSet, 健保代碼
- Taiwan health insurance reimbursement
- Generate CQL for [rule code]

## Notes

- GT/ folder was used for learning only - **not available at runtime**
- All knowledge must come from patterns in this SKILL.md
- When uncertain, combine documented patterns rather than improvising
- 中文 and English 混用 is standard in NHI CQL (both in variable names and comments)

### Critical ValueSet URL Pattern Difference

**In ValueSet JSON** (url field):
```json
"url": "http://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.6"
```
Uses `http://` (no 's')

**In CQL** (valueset declaration):
```cql
valueset "name": 'https://example.org/fhir/ValueSet/2.16.840.1.113762.1.4.1287.6'
```
Uses `https://` (with 's')

This is intentional and follows GT examples exactly.

### ValueSet File Naming

- File name = Full OID: `2.16.840.1.113762.1.4.1287.6.json`
- NOT descriptive names like `17022B-indications.json`
- id field in JSON = file name without .json extension
