---
name: readme-generator
description: This skill creates or updates a README.md file in the GitHub home directory of the current project. The README.md file it generates will conform to GitHub best practices, including badges, project overview, site metrics, getting started instructions, and comprehensive documentation.
license: MIT
---

# README Generator

Generate or update a comprehensive README.md file for GitHub repositories following best practices.

## Purpose

This skill automates the creation of professional, well-structured README.md files for GitHub repositories. It generates all essential sections including badges for technologies used, project overview, site metrics, getting started instructions, project structure, and contact information. The skill is particularly optimized for MkDocs-based intelligent textbook projects but can be adapted for any repository type.

## When to Use This Skill

Use this skill when:

- Starting a new GitHub repository that needs a README.md
- Updating an existing README.md to follow best practices
- After significant project changes that should be documented
- Before publishing or sharing a repository
- When migrating from another documentation system
- After adding new technologies or dependencies

## Workflow

### Step 1: Analyze Repository Context

Before generating the README, gather information about the repository:

1. Check if README.md already exists in the root directory
2. Identify the repository name from `.git/config` or the working directory
3. Read `mkdocs.yml` if it exists to extract:
   - Site name
   - Site description
   - Site URL (for GitHub Pages link)
   - Repository URL
4. Check for documentation in `/docs` directory
5. Identify technologies used (look for package.json, requirements.txt, mkdocs.yml, etc.)

**User Dialog Triggers:**

- If README.md exists: Ask "README.md already exists. Would you like to update it or create a backup first?"
- If repository URL not found: Ask "What is the GitHub repository URL? (e.g., https://github.com/username/repo-name)"
- If site URL not configured: Ask "Is this site deployed to GitHub Pages? If yes, what's the URL?"

### Step 2: Generate Badges

Create badges for all relevant technologies and platforms. Use shields.io format for consistency.

**Badge Order:**

1. MkDocs (if mkdocs.yml exists)
2. MkDocs Material (if theme is Material)
3. GitHub Pages live badge (if site is deployed)
4. Claude Code badge
5. Claude Skills badge (if .claude/skills or skills/ directory exists)
6. License badge
7. Additional technology badges (Python, JavaScript, p5.js, etc.)

**Badge Templates:**

```markdown
[![MkDocs](https://img.shields.io/badge/Made%20with-MkDocs-526CFE?logo=materialformkdocs)](https://www.mkdocs.org/)
[![Material for MkDocs](https://img.shields.io/badge/Material%20for%20MkDocs-526CFE?logo=materialformkdocs)](https://squidfunk.github.io/mkdocs-material/)
[![GitHub Pages](https://img.shields.io/badge/View%20on-GitHub%20Pages-blue?logo=github)](SITE_URL)
[![GitHub](https://img.shields.io/badge/GitHub-OWNER%2FREPO-blue?logo=github)](REPO_URL)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-DA7857?logo=anthropic)](https://claude.ai/code)
[![Claude Skills](https://img.shields.io/badge/Uses-Claude%20Skills-DA7857?logo=anthropic)](https://github.com/dmccreary/claude-skills)
```

**Check for these additional badges:**

- p5.js: `[![p5.js](https://img.shields.io/badge/p5.js-ED225D?logo=p5.js&logoColor=white)](https://p5js.org/)`
- Python: `[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)`
- JavaScript: `[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)`

### Step 3: Add License Badge

Look for license information in:

1. `LICENSE` file in root
2. `docs/license.md`
3. `mkdocs.yml` (copyright field)

**Default to Creative Commons BY-NC-SA 4.0 if not specified:**

```markdown
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
```

**Other common licenses:**

- MIT: `[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)`
- Apache 2.0: `[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)`
- GPL-3.0: `[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)`

### Step 4: Create Website Link Section

After badges, add a prominent link to the live website (if deployed):

```markdown
## View the Live Site

Visit the interactive textbook at: [https://username.github.io/repo-name](https://username.github.io/repo-name)
```

### Step 5: Write Overview/Short Description

Create a compelling 1-3 paragraph overview that answers:

- What is this project?
- Who is it for?
- Why is it valuable?
- What makes it unique or special?

**Guidelines:**

- Keep it concise but engaging
- Use active voice
- Highlight key features or benefits
- Mention the educational framework if applicable
- For textbooks: mention target audience (grade level, prerequisites)

**Example for Intelligent Textbook:**

```markdown
## Overview

This is an interactive, AI-generated intelligent textbook on [TOPIC] designed for [AUDIENCE]. Built using MkDocs with the Material theme, it incorporates learning graphs, concept dependencies, interactive MicroSims (p5.js simulations), and AI-assisted content generation.

The textbook follows Bloom's Taxonomy (2001 revision) for learning outcomes and uses concept dependency graphs to ensure proper prerequisite sequencing. All content is generated and curated using Claude AI skills, making it a Level 2+ intelligent textbook with interactive elements.

Whether you're a student learning [TOPIC] for the first time or an educator looking for structured course materials, this textbook provides comprehensive coverage with hands-on interactive elements that make complex concepts accessible and engaging.
```

### Step 6: Add Site Status and Metrics

Gather and display project metrics to show completeness and scope.

**Run Python script to collect metrics:**

Call `scripts/collect-site-metrics.py` (or create it if needed) to gather:

1. **Learning Graph Metrics** (from `docs/learning-graph/`):
   - Number of concepts in concept graph
   - Quality score
   - Taxonomy distribution

2. **Content Metrics**:
   - Number of chapters (count directories in `docs/chapters/`)
   - Number of markdown files (`.md` files in `docs/`)
   - Total word count (sum of all markdown files)
   - Number of code blocks
   - Number of lists and tables

3. **Interactive Elements**:
   - Number of MicroSims (directories in `docs/sims/`)
   - Number of quizzes (files named `quiz.md`)
   - Total quiz questions (count in quiz files)

4. **Educational Resources**:
   - Number of glossary terms (in `docs/glossary.md`)
   - Number of FAQ questions (in `docs/faq.md`)
   - Number of references (in `docs/references.md`)

5. **Media Assets**:
   - Number of images (`.png`, `.jpg`, `.svg` files)
   - Number of diagrams (Mermaid, vis-network)

**Format as a table:**

```markdown
## Site Status and Metrics

| Metric | Count |
|--------|-------|
| Concepts in Learning Graph | 200 |
| Chapters | 13 |
| Markdown Files | 87 |
| Total Words | 45,230 |
| MicroSims | 12 |
| Glossary Terms | 187 |
| FAQ Questions | 42 |
| Quiz Questions | 156 |
| Images | 34 |
| References | 28 |

**Completion Status:** Approximately 85% complete (content generation phase)
```

**Book-Specific Metrics:**

For specialized textbooks, add domain-specific metrics:

- **Circuits textbook**: Number of circuit diagrams, simulations
- **History textbook**: Number of timelines, maps, primary source documents
- **Programming textbook**: Number of code examples, exercises, projects
- **Math textbook**: Number of equations, proofs, worked examples

### Step 7: Add Getting Started Section

Provide clear instructions for using and customizing the project.

**Standard sections:**

1. **Prerequisites** (if any)
2. **Clone the Repository**
3. **Installation** (if dependencies needed)
4. **Building the Site**
5. **Local Development**
6. **Deployment**

**Example:**

```markdown
## Getting Started

### Clone the Repository

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

### Install Dependencies

This project uses MkDocs with the Material theme:

```bash
pip install mkdocs
pip install mkdocs-material
```

### Build and Serve Locally

Build the site:

```bash
mkdocs build
```

Serve locally for development (with live reload):

```bash
mkdocs serve
```

Open your browser to `http://localhost:8000`

### Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

This will build the site and push it to the `gh-pages` branch.

### Using the Book

**Navigation:**
- Use the left sidebar to browse chapters
- Click on the search icon to search all content
- Each chapter includes quizzes and practice exercises

**Interactive MicroSims:**
- Found in the "MicroSims" section
- Each simulation runs standalone in your browser
- Adjust parameters with sliders and controls

**Customization:**
- Edit markdown files in `docs/` to modify content
- Modify `mkdocs.yml` to change site structure
- Add your own MicroSims in `docs/sims/`
- Customize theme in `docs/css/extra.css`
```

### Step 8: Document Repository Structure

Create an ASCII tree diagram showing the repository structure with explanatory comments.

**Use this approach:**

- Don't list every single file
- Show representative examples
- Add comments explaining each major directory
- Keep it concise (10-20 lines)

**Example:**

```markdown
## Repository Structure

```
repo-name/
├── docs/                          # MkDocs documentation source
│   ├── chapters/                  # Chapter content
│   │   ├── 01-intro/
│   │   │   ├── index.md          # Chapter markdown
│   │   │   └── quiz.md           # Chapter quiz
│   │   └── 02-concepts/
│   ├── sims/                      # Interactive p5.js MicroSims
│   │   ├── graph-viewer/
│   │   │   ├── main.html         # Standalone simulation
│   │   │   └── index.md          # Documentation
│   ├── learning-graph/            # Learning graph data and analysis
│   │   ├── learning-graph.csv    # Concept dependencies
│   │   ├── learning-graph.json   # vis-network format
│   │   └── quality-metrics.md    # Quality analysis
│   ├── glossary.md                # ISO 11179-compliant definitions
│   ├── faq.md                     # Frequently asked questions
│   └── references.md              # Curated references
├── skills/                        # Claude AI skills (if present)
│   └── [skill-name]/
│       ├── SKILL.md               # Skill definition
│       └── *.py                   # Supporting scripts
├── mkdocs.yml                     # MkDocs configuration
└── README.md                      # This file
```
```

### Step 9: Add Issue Reporting Section

Direct users to the GitHub Issues page:

```markdown
## Reporting Issues

Found a bug, typo, or have a suggestion for improvement? Please report it:

[GitHub Issues](https://github.com/username/repo-name/issues)

When reporting issues, please include:

- Description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots (if applicable)
- Browser/environment details (for MicroSims)
```

### Step 10: Add License Information

Reinforce licensing terms and attribution requirements:

```markdown
## License

This work is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**You are free to:**

- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

**Under the following terms:**

- **Attribution** — Give appropriate credit with a link to the original
- **NonCommercial** — No commercial use without permission
- **ShareAlike** — Distribute contributions under the same license

See [LICENSE.md](docs/license.md) for full details.
```

### Step 11: Add Acknowledgements

Express gratitude to the open source community and key projects:

```markdown
## Acknowledgements

This project is built on the shoulders of giants in the open source community:

- **[MkDocs](https://www.mkdocs.org/)** - Static site generator optimized for project documentation
- **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** - Beautiful, responsive theme
- **[p5.js](https://p5js.org/)** - Creative coding library from NYU ITP
- **[vis-network](https://visjs.org/)** - Network visualization library for learning graphs
- **[Python](https://www.python.org/)** community - Data processing and analysis tools
- **[Claude AI](https://claude.ai)** by Anthropic - AI-assisted content generation
- **[GitHub Pages](https://pages.github.com/)** - Free hosting for open source projects

Special thanks to the educators and developers who contribute to making educational resources accessible and interactive.
```

**Customize based on actual dependencies:**

- Add Chart.js if using bubble charts
- Add Mermaid if using diagrams
- Add specific Python libraries if used (pandas, numpy, etc.)
- Add any other key dependencies

### Step 12: Add Contact Section

Provide a way for users to reach out:

```markdown
## Contact

**Dan McCreary**

- LinkedIn: [linkedin.com/in/danmccreary](https://www.linkedin.com/in/danmccreary/)
- GitHub: [@dmccreary](https://github.com/dmccreary)

Questions, suggestions, or collaboration opportunities? Feel free to connect on LinkedIn or open an issue on GitHub.
```

**Customize with actual maintainer information:**

- Replace with repository owner's name
- Update LinkedIn URL
- Update GitHub username
- Add email if desired (optional)
- Add website/blog if relevant

### Step 13: Add Optional Sections

Include these sections if relevant to the project:

**Contributing Guidelines:**

```markdown
## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.
```

**Citation Information:**

```markdown
## How to Cite

If you use this textbook in your research or teaching, please cite it as:

```
[Author Name]. (2024). [Textbook Title]. GitHub. https://github.com/username/repo-name
```

BibTeX:

```bibtex
@misc{repo-name-2024,
  author = {[Author Name]},
  title = {[Textbook Title]},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/username/repo-name}
}
```
```

**Changelog:**

```markdown
## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

**Recent Updates:**

- v1.0.0 (2024-11-11): Initial release with 13 chapters
- v0.9.0 (2024-11-01): Added 12 MicroSims and interactive elements
- v0.5.0 (2024-10-15): Completed learning graph and chapter structure
```

### Step 14: Validate and Format

Before finalizing the README:

1. **Check all links** - Verify GitHub URLs, site URLs, badge URLs
2. **Validate markdown** - Ensure proper formatting
3. **Test locally** - Render README on GitHub to check appearance
4. **Spell check** - Review for typos and grammar
5. **Consistency** - Ensure terminology matches project docs

**Quality checklist:**

- [ ] All badges render correctly
- [ ] Repository URL is correct
- [ ] Live site URL works (if applicable)
- [ ] Metrics are accurate and current
- [ ] Code blocks have proper syntax highlighting
- [ ] Links are not broken
- [ ] Table of contents matches sections (if auto-generated)
- [ ] License information is clear
- [ ] Contact information is current

### Step 15: Write README.md

Generate the final README.md file in the repository root with all sections in order:

1. Title (H1) with repository name
2. Badges
3. Live site link (if applicable)
4. Overview
5. Site Status and Metrics
6. Getting Started
7. Repository Structure
8. Reporting Issues
9. License
10. Acknowledgements
11. Contact
12. Optional sections (Contributing, Citation, Changelog)

**Formatting best practices:**

- Use ATX-style headers (`#` not underlines)
- Include blank lines before lists
- Use code fences with language specifiers
- Keep lines under 120 characters where practical
- Use relative links for internal documentation
- Add table of contents for longer READMEs (>500 lines)

## Supporting Scripts

The skill includes Python scripts for automated metrics collection:

**`scripts/collect-site-metrics.py`**

Scans the repository and generates a metrics report including:

- Markdown file count and word counts
- Chapter and section counts
- MicroSim count
- Glossary, FAQ, quiz statistics
- Image and diagram counts
- Learning graph statistics

Usage:
```bash
cd skills/readme-generator/scripts
python collect-site-metrics.py /path/to/repo
```

Output: JSON object with all metrics

**`scripts/validate-readme.py`**

Validates README.md for:

- Required sections present
- Working links
- Valid badge URLs
- Proper markdown formatting

Usage:
```bash
python validate-readme.py README.md
```

## Output Files

**Required:**

1. `README.md` - Complete README in repository root

**Optional:**

2. `README-backup.md` - Backup of previous README (if updating)
3. `docs/readme-metrics.json` - Metrics data in JSON format

## Example Session

**User:** "Generate a README for this repository"

**Claude (using this skill):**

1. Checks if README.md exists (found, create backup)
2. Reads `mkdocs.yml` to extract site info
3. Identifies technologies: MkDocs, Material, p5.js, Python
4. Scans `/docs` for metrics (chapters, MicroSims, glossary)
5. Runs `collect-site-metrics.py` to gather statistics
6. Generates badges for all identified technologies
7. Writes comprehensive README.md with all 12 sections
8. Validates links and formatting
9. Reports: "Created README.md with 15 sections, 8 badges, and current site metrics (200 concepts, 13 chapters, 87 files, 12 MicroSims). Previous README backed up to README-backup.md."

## Quality Standards

A high-quality README should have:

- All relevant badges displayed correctly
- Accurate, current metrics
- Clear, compelling overview (200-400 words)
- Complete getting started instructions
- Proper attribution and licensing
- Working links (100% functional)
- Professional formatting
- Contact information

## References

- [GitHub README Best Practices](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [Shields.io Badge Documentation](https://shields.io/)
- [Creative Commons License Chooser](https://creativecommons.org/choose/)
- [MkDocs Documentation](https://www.mkdocs.org/)
