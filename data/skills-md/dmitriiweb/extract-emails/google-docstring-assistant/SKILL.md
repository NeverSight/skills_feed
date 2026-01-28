---
name: google-docstring-assistant
description: Write Python docstrings following the Google Python Style Guide, using clear sections and examples.
---

# Google Docstring Assistant

## Quick start
- Write docstrings using the Google Python Style Guide structure (Args, Returns, Raises, Examples, Attributes, etc.).
- Keep sections as headers followed by indented blocks; break sections by resuming unindented text.
- When types are annotated in code, omit them in docstrings unless clarity is improved.
- Use `Examples` blocks with literal blocks (`::`) for commands or code snippets.
- Document module-level variables consistently (all in `Attributes` or inline), and list TODOs in a `Todo` section.
- See `references/google_docstring_rules.md` for full guidance and examples.

## Workflow
1) **Choose sections**  
   - Functions: include `Args`, `Returns`, and `Raises` as needed.  
   - Modules/classes: use `Attributes` and `Todo` when relevant; keep formatting consistent.  

2) **Write clearly**  
   - One docstring per object; keep it concise and informative.  
   - Use indentation under each section header; separate sections by returning to unindented text.  
   - Prefer Google-style wording; avoid duplicating annotated types unless helpful.  

3) **Examples and scripts**  
   - Use `Examples:` with indented literal blocks for shell commands or code snippets.  
   - Include multi-line descriptions when needed; keep formatting readable.  

## Reference
- `references/google_docstring_rules.md`: full style description and examples.
