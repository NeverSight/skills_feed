---
name: awesome-creator
description: Generate Awesome list README files following official sindresorhus/awesome standards. Use when creating, updating, or validating Awesome lists for GitHub repositories.
license: CC0-1.0
---

# Awesome Creator

Expert guidance for creating Awesome lists that comply with official sindresorhus/awesome standards. Awesome lists are curated collections of the best resources on specific topics, maintained by the community.

**When to use this skill:**
- Creating a new Awesome list from scratch
- Validating an existing Awesome list for compliance
- Updating an Awesome list with new entries
- Submitting an Awesome list to the official awesome repository
- Reviewing Awesome list pull requests

---

## Quick Start: Create Your Awesome List in 5 Minutes

Follow these steps to create a compliant Awesome list:

### Step 1: Set Up Your Repository (1 minute)

**Repository name:** `awesome-topic` (lowercase slug)
- ✅ `awesome-rust-gui`
- ✅ `awesome-python-testing`
- ❌ `awesome-RustGUI`
- ❌ `AwesomePythonTesting`

**Required files:**
```
awesome-topic/
├── README.md           # Your Awesome list
├── CONTRIBUTING.md     # Contribution guidelines
└── LICENSE             # CC0 license
```

### Step 2: Create the Header (30 seconds)

```markdown
# Awesome Topic

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Brief description of what this list covers.
```

**Key points:**
- Title case in heading: `# Awesome Topic`
- Badge on right side or next to title
- Succinct, objective description
- No marketing language

### Step 3: Add Table of Contents (1 minute)

```markdown
## Contents

- [Category One](#category-one)
- [Category Two](#category-two)
- [Category Three](#category-three)
```

**Requirements:**
- Named "Contents" (not "Table of Contents")
- First section in README
- One level deep (no nested bullets)
- Exclude "Contributing" and "Footnotes"

### Step 4: Add Your Entries (2 minutes)

```markdown
## Category One

- [Project Name](https://github.com/user/project#readme) - Objective description.
- [Another Project](https://github.com/user/another#readme) - What it does.
```

**Critical rules:**
- All GitHub links end with `#readme`
- Descriptions start with uppercase
- Descriptions end with period
- No marketing words ("best", "amazing")
- Describe what it is, not how great it is

### Step 5: Finalize (1 minute)

Add at the bottom:

```markdown
## Contributing

Please see [contributing.md](contributing.md)
```

Create `CONTRIBUTING.md` and `LICENSE` files using the templates in `templates/`.

---

## Awesome List Structure

### Required Elements

Every Awesome list MUST include:

#### 1. Awesome Badge
```markdown
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
```
- Placed on right side of heading or centered at top
- Links to `https://awesome.re`
- Use the flat version if preferred: `badge-flat.svg`

#### 2. Succinct Description
A brief, objective description at the top:

✅ Good:
```markdown
> Mobile operating system for Apple phones and tablets.
> Prototyping interactive UI designs.
```

❌ Bad:
```markdown
> Resources and tools for iOS development.
> The best collection of awesome Framer packages.
```

#### 3. Table of Contents
- Named exactly "Contents"
- First section after description
- Links to all major categories
- Excludes "Contributing" and "Footnotes"
- Preferably one level deep

#### 4. Categorized Entries
Organize entries into logical categories:
```markdown
## Networking

- [Alamofire](https://github.com/Alamofire/Alamofire#readme) - Elegant HTTP networking in Swift.

## UI Components

- [SnapKit](https://github.com/SnapKit/SnapKit#readme) - A Swift Autolayout DSL.
```

#### 5. Contributing Section
```markdown
## Contributing

Please see [contributing.md](contributing.md)
```
- Links to separate `CONTRIBUTING.md` file
- Placed at top or bottom of content
- NOT in Table of Contents

#### 6. LICENSE File
- Must use Creative Commons license (CC0 recommended)
- Code licenses (MIT, Apache, GPL) are NOT acceptable
- File named `LICENSE` or `license` in repo root
- Do NOT include license text in README

### Optional Elements

#### Project Logo
```markdown
> Description

<img src="logo.png" alt="Logo" width="400">

## Contents
```
- High-DPI image (max half original width)
- Links to project website
- Centered or right-aligned

#### Footnotes Section
```markdown
## Footnotes

- Some entries may be archived but historically significant.
- Last updated: January 2025
```
- For ancillary information
- NOT in Table of Contents
- Placed at very bottom

---

## Entry Quality Guidelines

### Curation Principles

**Core Philosophy:** Awesome lists are curations of the best, not collections of everything.

#### Only Include Awesome Items

✅ Include:
- Projects you personally recommend
- Well-maintained, active projects
- Projects with clear documentation
- High-quality resources

❌ Exclude:
- Unmaintained or archived repos
- Projects without documentation
- Deprecated tools
- Everything you can find (be selective!)

#### Objective Descriptions

Describe what the project is, not how great it is:

✅ Good:
```markdown
- [RxSwift](https://github.com/ReactiveX/RxSwift#readme) - Reactive programming in Swift.
- [Alamofire](https://github.com/Alamofire/Alamofire#readme) - Elegant HTTP networking.
```

❌ Bad:
```markdown
- [RxSwift](https://github.com/ReactiveX/RxSwift#readme) - The best reactive programming library.
- [Alamofire](https://github.com/Alamofire/Alamofire#readme) - An amazing networking framework.
```

#### Entry Format

Standard format for all entries:
```markdown
- [Project Name](https://github.com/user/project#readme) - Description ends with period.
```

**Rules:**
- Link text = project name (title case)
- GitHub URLs end with `#readme`
- Description starts with uppercase
- Description ends with period
- Separate link and description with dash
- One space on each side of dash

#### Consistent Naming

Use correct, consistent names:
- ✅ `Node.js`, ❌ `NodeJS`, ❌ `node.js`
- ✅ `iOS`, ❌ `ios`, ❌ `IOS`
- ✅ `Swift`, ❌ `swift`
- ✅ `macOS`, ❌ `MacOS`, ❌ `Mac OS`

---

## Advanced Features

### Progressive Disclosure

For detailed templates, examples, and official guidelines, see:

**Templates:**
- `templates/awesome-readme-template.md` - Base README structure
- `templates/contributing-template.md` - CONTRIBUTING.md template
- `templates/license-template.txt` - Full CC0 license text

**References:**
- `references/awesome-manifesto.md` - Official Awesome manifesto and philosophy
- `references/awesome-guidelines.md` - Complete submission requirements
- `references/examples.md` - Annotated examples from popular lists

### Validation

Before submitting your list:

1. **Run awesome-lint:**
   ```bash
   npx awesome-lint
   ```

2. **Check requirements:**
   - [ ] Repo name: `awesome-topic` (lowercase)
   - [ ] Title: `# Awesome Topic` (title case)
   - [ ] Awesome badge present
   - [ ] Table of Contents named "Contents"
   - [ ] All entries end with periods
   - [ ] All GitHub links include `#readme`
   - [ ] LICENSE file (CC0)
   - [ ] CONTRIBUTING.md exists
   - [ ] No marketing language
   - [ ] No CI badges
   - [ ] No hard-wrapping

3. **Age requirement:** List must be 30+ days old before submission

### Common Pitfalls

Avoid these frequent mistakes:

❌ **Marketing Language**
```markdown
- The best library for X
- An amazing tool
- Revolutionary framework
```
Use objective descriptions instead.

❌ **Missing #readme**
```markdown
- [Project](https://github.com/user/project) - Description.
```
Include `#readme` in GitHub URLs.

❌ **Wrong License**
```markdown
MIT License
```
Use CC0 or Creative Commons, not code licenses.

❌ **Self-Referential**
```markdown
> Resources and tools for X development
```
Describe the topic itself, not the list.

❌ **CI Badges**
```markdown
[![CI](https://github.com/user/workflow/badge.svg)](https://github.com/user/actions)
```
Don't include CI badges in Awesome lists.

❌ **Hard-Wrapping**
```markdown
- [Project](https://github.com/user/project#readme) - This is a
  description that wraps to the next line.
```
Let lines flow naturally without hard wraps.

---

## Progressive Disclosure

### Quick Reference

For rapid validation, use the **Quick Start** section above.

### Detailed Guidance

For comprehensive information, consult:

**Templates:**
- `templates/awesome-readme-template.md` - Full README template with structure
- `templates/contributing-template.md` - Complete CONTRIBUTING.md guide
- `templates/license-template.txt` - CC0 license full text

**Reference Documentation:**
- `references/awesome-manifesto.md` - Official Awesome manifesto
- `references/awesome-guidelines.md` - Complete PR submission guidelines
- `references/examples.md` - Annotated real-world examples

### Official Resources

- [Official Awesome Manifesto](https://github.com/sindresorhus/awesome/blob/main/awesome.md)
- [Create List Guide](https://github.com/sindresorhus/awesome/blob/main/create-list.md)
- [awesome.re](https://awesome.re) - Official Awesome hub

---

## Best Practices Summary

### Content Quality
- Curate, don't collect
- Only include items you recommend
- Research before adding
- Remove unmaintained projects

### Writing Style
- Be objective, not promotional
- Use consistent formatting
- Check spelling and grammar
- Keep descriptions concise

### Technical Standards
- Use CC0 license
- Include CONTRIBUTING.md
- Add Awesome badge
- Name repo correctly
- Run awesome-lint

### Community
- Accept constructive feedback
- Respect other opinions
- Review other PRs
- Contribute back

---

**Remember:** Awesome lists are curations of the best resources. Quality over quantity. When in doubt, leave it out.
