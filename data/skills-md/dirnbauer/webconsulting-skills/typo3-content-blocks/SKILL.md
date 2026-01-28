---
name: typo3-content-blocks
description: Expert guidance on creating Content Elements, Record Types, Page Types, and File Types using TYPO3 Content Blocks extension - the single source of truth for content modeling.
version: 1.4.0
typo3_compatibility: "13.0 - 14.x"
related_skills:
  - typo3-content-blocks-migration
triggers:
  - content-blocks
  - content-element
  - record-type
  - page-type
  - file-type
  - make:content-block
  - friendsoftypo3/content-blocks
  - irre
  - collection
---

# TYPO3 Content Blocks Development

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All code examples in this skill are designed to work on both TYPO3 v13 and v14.

## 1. The Single Source of Truth Principle

Content Blocks is the **modern approach** to creating custom content types in TYPO3. It eliminates redundancy by providing a **single YAML configuration** that generates:

- TCA (Table Configuration Array)
- Database schema (SQL)
- TypoScript rendering
- Backend forms and previews
- Labels and translations

### Why Content Blocks?

| Traditional Approach | Content Blocks Approach |
|---------------------|------------------------|
| Multiple TCA files | One `config.yaml` |
| Manual SQL definitions | Auto-generated schema |
| Separate TypoScript | Auto-registered rendering |
| Scattered translations | Single `labels.xlf` |
| Complex setup | Simple folder structure |

## 2. Installation

```bash
# Install via Composer (DDEV recommended)
ddev composer require friendsoftypo3/content-blocks

# After installation, clear caches
ddev typo3 cache:flush
```

### Security Configuration (Classic Mode)

For non-composer installations, deny web access to ContentBlocks folder:

```apache
# .htaccess addition
RewriteRule (?:typo3conf/ext|typo3/sysext|typo3/ext)/[^/]+/(?:Configuration|ContentBlocks|Resources/Private|Tests?|Documentation|docs?)/ - [F]
```

## 3. Content Types Overview

Content Blocks supports four content types:

| Type | Folder | Table | Use Case |
|------|--------|-------|----------|
| `ContentElements` | `ContentBlocks/ContentElements/` | `tt_content` | Frontend content (hero, accordion, CTA) |
| `RecordTypes` | `ContentBlocks/RecordTypes/` | Custom/existing | Structured records (news, products, team) |
| `PageTypes` | `ContentBlocks/PageTypes/` | `pages` | Custom page types (blog, landing page) |
| `FileTypes` | `ContentBlocks/FileTypes/` | `sys_file_metadata` | Extended file metadata (photographer, copyright) |

## 4. Folder Structure

```
EXT:my_sitepackage/
└── ContentBlocks/
    ├── ContentElements/
    │   └── my-hero/
    │       ├── assets/
    │       │   └── icon.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       ├── templates/
    │       │   ├── backend-preview.html
    │       │   ├── frontend.html
    │       │   └── partials/
    │       └── config.yaml
    ├── RecordTypes/
    │   └── my-record/
    │       ├── assets/
    │       │   └── icon.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       └── config.yaml
    ├── PageTypes/
    │   └── blog-article/
    │       ├── assets/
    │       │   ├── icon.svg
    │       │   ├── icon-hide-in-menu.svg
    │       │   └── icon-root.svg
    │       ├── language/
    │       │   └── labels.xlf
    │       ├── templates/
    │       │   └── backend-preview.html
    │       └── config.yaml
    └── FileTypes/
        └── image-extended/
            ├── language/
            │   └── labels.xlf
            └── config.yaml
```

## 5. Creating Content Elements

### Kickstart Command (Recommended)

```bash
# Interactive mode
ddev typo3 make:content-block

# One-liner
ddev typo3 make:content-block \
  --content-type="content-element" \
  --vendor="myvendor" \
  --name="hero-banner" \
  --title="Hero Banner" \
  --extension="my_sitepackage"

# After creation, update database
ddev typo3 cache:flush -g system
ddev typo3 extension:setup --extension=my_sitepackage
```

### Minimal Content Element

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/hero-banner/config.yaml
name: myvendor/hero-banner
fields:
  - identifier: header
    useExistingField: true
  - identifier: bodytext
    useExistingField: true
```

### Full Content Element Example

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/hero-banner/config.yaml
name: myvendor/hero-banner
group: default
description: "A full-width hero banner with image and CTA"
prefixFields: true
prefixType: full
basics:
  - TYPO3/Appearance
  - TYPO3/Links
fields:
  - identifier: header
    useExistingField: true
  - identifier: subheadline
    type: Text
    label: Subheadline
  - identifier: hero_image
    type: File
    minitems: 1
    maxitems: 1
    allowed: common-image-types
  - identifier: cta_link
    type: Link
    label: Call to Action Link
  - identifier: cta_text
    type: Text
    label: Button Text
```

### Frontend Template

```html
<!-- templates/frontend.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:cb="http://typo3.org/ns/TYPO3/CMS/ContentBlocks/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:asset.css identifier="hero-banner-css" href="{cb:assetPath()}/frontend.css"/>

<section class="hero-banner">
    <f:if condition="{data.hero_image}">
        <f:for each="{data.hero_image}" as="image">
            <f:image image="{image}" alt="{data.header}" class="hero-image"/>
        </f:for>
    </f:if>
    
    <div class="hero-content">
        <h1>{data.header}</h1>
        <f:if condition="{data.subheadline}">
            <p class="subheadline">{data.subheadline}</p>
        </f:if>
        
        <f:if condition="{data.cta_link}">
            <f:link.typolink parameter="{data.cta_link}" class="btn btn-primary">
                {data.cta_text -> f:or(default: 'Learn more')}
            </f:link.typolink>
        </f:if>
    </div>
</section>
</html>
```

### Backend Preview Template

```html
<!-- templates/backend-preview.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:be="http://typo3.org/ns/TYPO3/CMS/Backend/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="content-block-preview">
    <strong>{data.header}</strong>
    <f:if condition="{data.subheadline}">
        <br/><em>{data.subheadline}</em>
    </f:if>
    <f:if condition="{data.hero_image}">
        <f:for each="{data.hero_image}" as="image">
            <be:thumbnail image="{image}" width="100" height="100"/>
        </f:for>
    </f:if>
</div>
</html>
```

## 6. Creating Record Types (Custom Tables)

Record Types create **custom database tables** for structured data like teams, products, events, etc.

### Extbase-Compatible Table Naming

**IMPORTANT:** For Extbase compatibility, use the `tx_extensionkey_domain_model_*` naming convention:

```yaml
# ✅ CORRECT - Extbase compatible table name
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fields:
  - identifier: name
    type: Text
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
```

```yaml
# ❌ WRONG - Short table names don't work with Extbase
name: myvendor/team-member
table: team_member  # Won't work with Extbase!
```

### Minimal Record Type

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fields:
  - identifier: name
    type: Text
```

### Full Record Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/team-member/config.yaml
name: myvendor/team-member
table: tx_mysitepackage_domain_model_teammember
labelField: name
fallbackLabelFields:
  - email
languageAware: true
workspaceAware: true
sortable: true
softDelete: true
trackCreationDate: true
trackUpdateDate: true
internalDescription: true
restriction:
  disabled: true
  startTime: true
  endTime: true
security:
  ignorePageTypeRestriction: true  # Allow on normal pages
fields:
  - identifier: name
    type: Text
    required: true
  - identifier: position
    type: Text
  - identifier: email
    type: Email
  - identifier: phone
    type: Text
  - identifier: bio
    type: Textarea
    enableRichtext: true
  - identifier: photo
    type: File
    allowed: common-image-types
    maxitems: 1
  - identifier: social_links
    type: Collection
    labelField: platform
    fields:
      - identifier: platform
        type: Select
        items:
          - label: LinkedIn
            value: linkedin
          - label: Twitter/X
            value: twitter
          - label: GitHub
            value: github
      - identifier: url
        type: Link
```

### Multi-Type Records (Single Table Inheritance)

Create multiple types for one table:

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/person-employee/config.yaml
name: myvendor/person-employee
table: tx_mysitepackage_domain_model_person
typeField: person_type
typeName: employee
priority: 999  # Default type (loaded first)
labelField: name
languageAware: false
workspaceAware: false
fields:
  - identifier: name
    type: Text
  - identifier: department
    type: Text
```

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/person-contractor/config.yaml
name: myvendor/person-contractor
table: tx_mysitepackage_domain_model_person
typeName: contractor
fields:
  - identifier: name
    type: Text
  - identifier: company
    type: Text
  - identifier: contract_end
    type: DateTime
```

### Record Types as Collection Children

Define a record that can be used in IRRE collections:

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/slide/config.yaml
name: myvendor/slide
table: tx_mysitepackage_domain_model_slide
labelField: title
fields:
  - identifier: title
    type: Text
  - identifier: image
    type: File
    maxitems: 1
  - identifier: link
    type: Link
```

```yaml
# EXT:my_sitepackage/ContentBlocks/ContentElements/slider/config.yaml
name: myvendor/slider
fields:
  - identifier: slides
    type: Collection
    foreign_table: tx_mysitepackage_domain_model_slide
    shareAcrossTables: true
    shareAcrossFields: true
    minitems: 1
```

## 7. Creating Page Types (Custom doktypes)

Page Types extend the `pages` table with custom page types – ideal for blog articles, landing pages, news pages, or other page variants with special properties.

### When to Use Page Types

| Use Case | Example |
|----------|---------|
| Structured page properties | Blog with author, teaser image, publish date |
| Plugin integration | News lists, event calendars reading page properties |
| Different page behavior | Landing pages without navigation |
| SEO-specific fields | Custom meta fields per page type |

### Minimal Page Type

```yaml
# EXT:my_sitepackage/ContentBlocks/PageTypes/blog-article/config.yaml
name: myvendor/blog-article
typeName: 1705234567
fields:
  - identifier: author_name
    type: Text
```

### Full Page Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/PageTypes/blog-article/config.yaml
name: myvendor/blog-article
typeName: 1705234567   # Unix timestamp (unique identifier)
group: default         # Options: default, link, special
fields:
  - identifier: author_name
    type: Text
    label: Author
    required: true
  - identifier: teaser_text
    type: Textarea
    label: Teaser
  - identifier: hero_image
    type: File
    allowed: common-image-types
    maxitems: 1
  - identifier: publish_date
    type: DateTime
    label: Publish Date
  - identifier: reading_time
    type: Number
    label: Reading Time (minutes)
```

### Page Type Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `typeName` | integer | ✓ | Unique doktype number (use Unix timestamp) |
| `group` | string | | Group in selector: `default`, `link`, `special` |

**Reserved typeName values:** 199, 254 (cannot be used)

### Icons for Page States

Page Types support state-specific icons. Add these to your assets folder:

```
ContentBlocks/PageTypes/blog-article/
├── assets/
│   ├── icon.svg              # Default icon
│   ├── icon-hide-in-menu.svg # Hidden in menu state
│   └── icon-root.svg         # Site root state
└── config.yaml
```

### Backend Preview

Create a `backend-preview.html` to preview custom page properties:

```html
<!-- templates/backend-preview.html -->
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:be="http://typo3.org/ns/TYPO3/CMS/Backend/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="card card-size-medium">
    <div class="card-body">
        <be:link.editRecord uid="{data.uid}" table="{data.mainType}" fields="author_name">
            <strong>Author:</strong> {data.author_name}
        </be:link.editRecord>
        <f:if condition="{data.publish_date}">
            <br/><small>Published: <f:format.date format="d.m.Y">{data.publish_date}</f:format.date></small>
        </f:if>
    </div>
</div>
</html>
```

### Frontend Integration

Page Types have **no automatic frontend rendering**. Add the ContentBlocksDataProcessor to your TypoScript:

```typoscript
# Configuration/TypoScript/setup.typoscript
page = PAGE
page {
    10 = FLUIDTEMPLATE
    10 {
        templateName = Default
        templateRootPaths.10 = EXT:my_sitepackage/Resources/Private/Templates/
        
        dataProcessing {
            # Process Content Blocks page data
            1 = content-blocks
        }
    }
}
```

Then access fields in your Fluid template:

```html
<!-- Resources/Private/Templates/Default.html -->
<f:if condition="{data.author_name}">
    <p class="author">By {data.author_name}</p>
</f:if>

<f:if condition="{data.hero_image}">
    <f:for each="{data.hero_image}" as="image">
        <f:image image="{image}" class="hero-image"/>
    </f:for>
</f:if>
```

### Remove from Page Tree Drag Area

To hide your page type from the "Create new page" drag area:

```typoscript
# Configuration/user.tsconfig
options {
    pageTree {
        doktypesToShowInNewPageDragArea := removeFromList(1705234567)
    }
}
```

## 8. Creating File Types (Extended Metadata)

> New in version 1.2

File Types extend the `sys_file_metadata` table with custom fields – perfect for photographer credits, copyright notices, or additional file options.

### Available File Type Names

| typeName | File Types |
|----------|------------|
| `image` | JPEG, PNG, GIF, WebP, SVG |
| `video` | MP4, WebM, OGG |
| `audio` | MP3, WAV, OGG |
| `text` | TXT, PDF, Markdown |
| `application` | ZIP, Office formats |

### Minimal File Type

```yaml
# EXT:my_sitepackage/ContentBlocks/FileTypes/image-extended/config.yaml
name: myvendor/image-extended
typeName: image
fields:
  - identifier: photographer
    type: Text
    label: Photographer
```

### Full File Type Example

```yaml
# EXT:my_sitepackage/ContentBlocks/FileTypes/image-extended/config.yaml
name: myvendor/image-extended
typeName: image
prefixFields: false  # Keep original column names
fields:
  - identifier: image_overlay_palette
    type: Palette
    label: 'LLL:EXT:core/Resources/Private/Language/locallang_tca.xlf:sys_file_reference.imageoverlayPalette'
    fields:
      # Reuse existing TYPO3 core fields
      - identifier: alternative
        useExistingField: true
      - identifier: description
        useExistingField: true
      - type: Linebreak
      - identifier: link
        useExistingField: true
      - identifier: title
        useExistingField: true
      - type: Linebreak
      # Custom fields
      - identifier: photographer
        type: Text
        label: Photographer
      - identifier: copyright
        type: Text
        label: Copyright Notice
      - identifier: source_url
        type: Link
        label: Source URL
      - type: Linebreak
      - identifier: crop
        useExistingField: true
```

### File Type Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `typeName` | string | ✓ | One of: `text`, `image`, `audio`, `video`, `application` |
| `prefixFields` | boolean | | Disable prefixing (recommended: `false`) |

### Use Cases for File Types

| Use Case | Fields to Add |
|----------|---------------|
| Photography agency | `photographer`, `copyright`, `license_type`, `expiry_date` |
| Video platform | `director`, `duration`, `transcript`, `subtitles` |
| Document management | `document_version`, `author`, `confidentiality` |
| E-commerce | `product_sku`, `variant_color`, `variant_size` |

### Accessing File Type Fields

In Fluid templates, access custom metadata through FAL references:

```html
<f:for each="{data.images}" as="image">
    <figure>
        <f:image image="{image}" alt="{image.alternative}"/>
        <f:if condition="{image.properties.photographer}">
            <figcaption>
                Photo: {image.properties.photographer}
                <f:if condition="{image.properties.copyright}">
                    | © {image.properties.copyright}
                </f:if>
            </figcaption>
        </f:if>
    </figure>
</f:for>
```

## 9. Field Types Reference

### Simple Fields

| Type | Description | Example |
|------|-------------|---------|
| `Text` | Single line text | `type: Text` |
| `Textarea` | Multi-line text | `type: Textarea` |
| `Email` | Email address | `type: Email` |
| `Link` | Link/URL | `type: Link` |
| `Number` | Integer/Float | `type: Number` |
| `DateTime` | Date and/or time | `type: DateTime` |
| `Color` | Color picker | `type: Color` |
| `Checkbox` | Boolean checkbox | `type: Checkbox` |
| `Radio` | Radio buttons | `type: Radio` |
| `Slug` | URL slug | `type: Slug` |
| `Password` | Password field | `type: Password` |

### Relational Fields

| Type | Description | Example |
|------|-------------|---------|
| `File` | File references (FAL) | `type: File` |
| `Relation` | Record relations | `type: Relation` |
| `Select` | Dropdown selection | `type: Select` |
| `Category` | System categories | `type: Category` |
| `Collection` | Inline records (IRRE) | `type: Collection` |
| `Folder` | Folder reference | `type: Folder` |
| `Language` | Language selector | `type: Language` |

### Structural Fields

| Type | Description | Example |
|------|-------------|---------|
| `Tab` | Tab separator | `type: Tab` |
| `Palette` | Group fields | `type: Palette` |
| `Linebreak` | Line break in palette | `type: Linebreak` |
| `FlexForm` | FlexForm container | `type: FlexForm` |
| `Json` | JSON field | `type: Json` |

### Common Field Options

```yaml
fields:
  - identifier: my_field
    type: Text
    label: My Field Label           # Static label (or use labels.xlf)
    description: Help text          # Field description
    required: true                  # Make field required
    default: "Default value"        # Default value
    placeholder: "Enter text..."    # Placeholder text
    prefixField: false              # Disable prefixing for this field
    useExistingField: true          # Reuse existing TCA field
    displayCond: 'FIELD:other:=:1'  # Conditional display
    onChange: reload                # Reload form on change
```

### File Field Example

```yaml
fields:
  - identifier: gallery_images
    type: File
    allowed: common-image-types
    minitems: 1
    maxitems: 10
    appearance:
      createNewRelationLinkTitle: Add Image
      showAllLocalizationLink: true
    behaviour:
      allowLanguageSynchronization: true
```

### Select Field Example

```yaml
fields:
  - identifier: layout
    type: Select
    renderType: selectSingle
    default: default
    items:
      - label: Default Layout
        value: default
      - label: Wide Layout
        value: wide
      - label: Compact Layout
        value: compact
```

### Collection Field Example (Inline IRRE)

```yaml
fields:
  - identifier: accordion_items
    type: Collection
    labelField: title
    minitems: 1
    maxitems: 20
    appearance:
      collapseAll: true
      levelLinksPosition: both
    fields:
      - identifier: title
        type: Text
        required: true
      - identifier: content
        type: Textarea
        enableRichtext: true
      - identifier: is_open
        type: Checkbox
        label: Initially Open
```

## 10. Field Prefixing

Content Blocks automatically prefixes field identifiers to avoid collisions.

### Prefixing Types

```yaml
# Full prefix (default): myvendor_myblock_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: full

# Vendor prefix only: myvendor_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: vendor

# Custom vendor prefix: tx_custom_fieldname
name: myvendor/my-block
prefixFields: true
prefixType: vendor
vendorPrefix: tx_custom

# No prefix (use with caution!)
name: myvendor/my-block
prefixFields: false
```

### Disable Prefixing per Field

```yaml
fields:
  - identifier: my_custom_field
    type: Text
    prefixField: false  # This field won't be prefixed
```

## 11. Templating Features

### Accessing Data in Fluid

```html
<!-- Basic field access -->
{data.header}
{data.my_field}

<!-- Record metadata -->
{data.uid}
{data.pid}
{data.languageId}
{data.mainType}      <!-- Table name: tt_content -->
{data.recordType}    <!-- CType: myvendor_heroblock -->
{data.fullType}      <!-- tt_content.myvendor_heroblock -->

<!-- Raw database values -->
{data.rawRecord.some_field}

<!-- System properties -->
{data.systemProperties.createdAt}
{data.systemProperties.lastUpdatedAt}
{data.systemProperties.sorting}
{data.systemProperties.disabled}

<!-- Language info -->
{data.languageInfo.translationParent}
{data.languageInfo.translationSource}

<!-- Relations are auto-resolved! -->
<f:for each="{data.gallery_images}" as="image">
    <f:image image="{image}" width="400"/>
</f:for>

<!-- Nested collections -->
<f:for each="{data.accordion_items}" as="item">
    <h3>{item.title}</h3>
    <f:format.html>{item.content}</f:format.html>
</f:for>
```

### Asset ViewHelpers

```html
<!-- Include CSS from assets folder -->
<f:asset.css identifier="my-block-css" href="{cb:assetPath()}/frontend.css"/>

<!-- Include JS from assets folder -->
<f:asset.script identifier="my-block-js" src="{cb:assetPath()}/frontend.js"/>

<!-- Cross-block asset reference -->
<f:asset.css identifier="shared-css" href="{cb:assetPath(name: 'vendor/other-block')}/shared.css"/>
```

### Translation ViewHelper

```html
<!-- Access labels.xlf translations -->
<f:translate key="{cb:languagePath()}:my_label"/>

<!-- Cross-block translation -->
<f:translate key="{cb:languagePath(name: 'vendor/other-block')}:shared_label"/>
```

## 12. Extending Existing Tables

Add custom types to existing tables (like `tx_news`):

```yaml
# EXT:my_sitepackage/ContentBlocks/RecordTypes/custom-news/config.yaml
name: myvendor/custom-news
table: tx_news_domain_model_news
typeName: custom_news
fields:
  - identifier: title
    useExistingField: true
  - identifier: custom_field
    type: Text
```

## 13. Workflow with DDEV

### Standard Development Workflow

```bash
# 1. Create new Content Block
ddev typo3 make:content-block

# 2. Clear system caches
ddev typo3 cache:flush -g system

# 3. Update database schema
ddev typo3 extension:setup --extension=my_sitepackage

# Alternative: Use Database Analyzer in TYPO3 Backend
# Admin Tools > Maintenance > Analyze Database Structure
```

### Using webprofil/make Extension

If `webprofil/make` is installed:

```bash
# Create Content Block with webprofil/make
ddev make:content_blocks

# Clear caches and update database
ddev typo3 cache:flush
ddev typo3 database:updateschema
```

### Integration with Extbase

After creating Record Types with proper table names, generate Extbase models:

```bash
# If typo3:make:model is available
ddev typo3 make:model --extension=my_sitepackage

# Generate repository
ddev typo3 make:repository --extension=my_sitepackage
```

## 14. Defaults Configuration

Create a `content-blocks.yaml` in project root for default settings:

```yaml
# content-blocks.yaml
vendor: myvendor
extension: my_sitepackage
content-type: content-element
skeleton-path: content-blocks-skeleton

config:
  content-element:
    basics:
      - TYPO3/Appearance
      - TYPO3/Links
    group: common
    prefixFields: true
    prefixType: full
  
  record-type:
    prefixFields: true
    prefixType: vendor
    vendorPrefix: tx_mysitepackage
```

## 15. Best Practices

### DO ✅

1. **Use Extbase-compatible table names** for Record Types:
   ```yaml
   table: tx_myextension_domain_model_myrecord
   ```

2. **Reuse existing fields** when possible:
   ```yaml
   - identifier: header
     useExistingField: true
   ```

3. **Group related fields** with Tabs and Palettes:
   ```yaml
   - identifier: settings_tab
     type: Tab
     label: Settings
   ```

4. **Use meaningful identifiers** (snake_case):
   ```yaml
   - identifier: hero_background_image
   ```

5. **Clear caches after changes**:
   ```bash
   ddev typo3 cache:flush -g system
   ddev typo3 extension:setup --extension=my_sitepackage
   ```

6. **Use labels.xlf** for all user-facing labels

### DON'T ❌

1. **Don't use raw SQL** - Content Blocks generates schema automatically

2. **Don't duplicate TCA** - Config.yaml is the single source of truth

3. **Don't use short table names** for Extbase integration:
   ```yaml
   # ❌ Wrong
   table: team_member
   
   # ✅ Correct
   table: tx_mysitepackage_domain_model_teammember
   ```

4. **Don't use dashes in identifiers**:
   ```yaml
   # ❌ Wrong
   identifier: hero-image
   
   # ✅ Correct
   identifier: hero_image
   ```

5. **Don't forget shareAcross options** when using foreign_table in multiple places

## 16. Troubleshooting

### Content Block Not Appearing

```bash
# Clear all caches
ddev typo3 cache:flush

# Rebuild class loading
ddev composer dump-autoload

# Check extension setup
ddev typo3 extension:setup --extension=my_sitepackage
```

### Database Errors

```bash
# Update database schema
ddev typo3 database:updateschema

# Or use Compare Tool
# Admin Tools > Maintenance > Analyze Database Structure
```

### Field Not Saving

- Check field identifier is unique (use prefixing)
- Verify field type is correct
- Check for typos in config.yaml
- Ensure labels.xlf has matching keys

## 17. Version Constraints

```php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '1.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
            'content_blocks' => '2.0.0-2.99.99',
        ],
    ],
];
```

---

## Related Skills

For migration between classic TYPO3 extensions and Content Blocks, see the dedicated migration skill:

- **[typo3-content-blocks-migration](./SKILL-MIGRATION.md)** - Bidirectional migration guide with:
  - TCA → Content Blocks field mapping
  - Content Blocks → TCA reverse mapping
  - Data migration scripts
  - Step-by-step examples
  - Checklists for both directions

---

## 18. Package Management for v14 Compatibility

If extensions don't support TYPO3 v14 yet, fork and update:

```bash
# Add private fork as VCS repository in composer.json
# Then update extension for v14 using typo3-rector and typo3-update skills
```

Required private forks for webconsulting stack:
- `webprofil/wp-t3monitoring-client` (^13 → ^14)
- `webprofil/deployer` (^13 → ^14)
- `webprofil/crawler` (^1.0 → compatible with v14)
- `webprofil/make` (^1.1 → compatible with v14)

---

## References

- [Content Blocks Documentation](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/)
- [YAML Reference](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/YamlReference/Index.html)
- [Field Types](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/YamlReference/FieldTypes/Index.html)
- [Content Elements API](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/API/ContentElements/Index.html)
- [Record Types API](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/API/RecordTypes/Index.html)
- [Page Types API](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/API/PageTypes/Index.html)
- [File Types YAML Reference](https://docs.typo3.org/p/friendsoftypo3/content-blocks/main/en-us/YamlReference/ContentTypes/FileTypes/Index.html)
- [Migration Skill](./SKILL-MIGRATION.md)
- [Packagist: friendsoftypo3/content-blocks](https://packagist.org/packages/friendsoftypo3/content-blocks)

---

## Credits & Attribution

This skill incorporates information from the official Content Blocks documentation maintained by the **TYPO3 Content Types Team** and **Friends of TYPO3**.

Original documentation: https://docs.typo3.org/p/friendsoftypo3/content-blocks/

Adapted by webconsulting.at for this skill collection
