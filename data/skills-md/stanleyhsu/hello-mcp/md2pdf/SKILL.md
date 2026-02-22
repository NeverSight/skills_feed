---
name: md2pdf
description: Convert a markdown file to PDF using pandoc
---

# md2pdf

Convert markdown files to professionally formatted PDF documents using pandoc.

## Instructions

When the user asks to convert a markdown file to PDF, follow these steps:

1. **Verify pandoc is installed**
   - Run `pandoc --version` to check if pandoc is available
   - If not installed, provide installation instructions for the user's platform:
     - macOS: `brew install pandoc`
     - Linux: `sudo apt-get install pandoc` or `sudo yum install pandoc`
     - Windows: Download from https://pandoc.org/installing.html

2. **Check for PDF engine**
   - Pandoc requires a PDF engine (LaTeX). Check if available with `pdflatex --version`
   - If not installed:
     - macOS: `brew install --cask mactex-no-gui` (smaller) or `brew install --cask mactex` (full)
     - Linux: `sudo apt-get install texlive-latex-base texlive-fonts-recommended`
     - Alternative: Use `wkhtmltopdf` as PDF engine

3. **Convert the markdown file**
   - Basic conversion: `pandoc input.md -o output.pdf`
   - With options for better formatting:
     ```bash
     pandoc input.md -o output.pdf \
       --pdf-engine=pdflatex \
       -V geometry:margin=1in \
       -V fontsize=11pt \
       --highlight-style=tango
     ```

4. **Common options**
   - `--toc`: Add table of contents
   - `--toc-depth=2`: Set TOC depth
   - `-V geometry:margin=1in`: Set page margins
   - `-V fontsize=11pt`: Set font size (10pt, 11pt, 12pt)
   - `--highlight-style=tango`: Syntax highlighting for code blocks
   - `-V colorlinks=true`: Enable colored links in PDF
   - `--metadata title="Document Title"`: Set PDF title
   - `--metadata author="Author Name"`: Set PDF author

5. **Verify output**
   - Confirm the PDF was created successfully
   - Report the output file path to the user

## Examples

### Example 1: Basic conversion
```
User: Convert README.md to PDF
Assistant: I'll convert README.md to PDF using pandoc.

[Runs: pandoc README.md -o README.pdf]

Successfully converted README.md to README.pdf
```

### Example 2: Conversion with formatting options
```
User: Convert CLAUDE.md to PDF with a table of contents
Assistant: I'll convert CLAUDE.md to PDF with a table of contents and formatting.

[Runs: pandoc CLAUDE.md -o CLAUDE.pdf --toc -V geometry:margin=1in -V fontsize=11pt]

Successfully converted CLAUDE.md to CLAUDE.pdf with table of contents
```

### Example 3: Converting with custom output name
```
User: Convert docs/guide.md to a PDF called user-guide.pdf
Assistant: I'll convert docs/guide.md to user-guide.pdf

[Runs: pandoc docs/guide.md -o user-guide.pdf -V geometry:margin=1in --highlight-style=tango]

Successfully converted docs/guide.md to user-guide.pdf
```

### Example 4: Batch conversion
```
User: Convert all markdown files in the docs/ folder to PDF
Assistant: I'll convert all markdown files in docs/ to PDF

[Runs: for file in docs/*.md; do pandoc "$file" -o "${file%.md}.pdf"; done]

Successfully converted:
- docs/guide.md → docs/guide.pdf
- docs/api.md → docs/api.pdf
- docs/tutorial.md → docs/tutorial.pdf
```

## Troubleshooting

- If pandoc is not installed, guide the user to install it first
- If PDF engine is missing, suggest installing LaTeX or using an alternative engine
- For large documents, add `--pdf-engine-opt=-shell-escape` if needed
- If images are not rendering, ensure image paths are correct and accessible