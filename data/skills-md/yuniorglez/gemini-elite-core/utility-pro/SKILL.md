---
name: utility-pro
id: utility-pro
version: 1.1.0
description: "Master of the Modern Utility Toolbelt, specialized in AI-enhanced CLI, structured data transformation, and advanced Unix forensics."
last_updated: "2026-01-22"
---

# Skill: Utility Pro (Standard 2026)

**Role:** The Utility Pro is the "Swiss Army Knife" of the Squaads AI Core. This role masters the command-line environment, turning raw text and unstructured data into actionable insights and clean code. In 2026, the Utility Pro moves beyond simple `grep` and `sed` to embrace structured shells (Nushell), AI-augmented terminals, and Rust-powered performance utilities.

## 🎯 Primary Objectives
1.  **Structured Data Mastery:** Treat the terminal as a database using Nushell and `jq`.
2.  **High-Performance Search:** Use `ripgrep` (rg) and `fzf` for near-instant codebase navigation.
3.  **Advanced Transformation:** Master RegEx, `awk`, and `sed` for complex multi-file refactoring.
4.  **Modern Web I/O:** Use `httpie` and `xh` for high-fidelity API interaction and debugging.

---

## 🏗️ The 2026 Utility Stack

### 1. The Core Moderns (Rust-Powered)
- **ripgrep (rg):** The gold standard for text search.
- **bat:** Syntax-highlighted `cat` replacement.
- **eza:** Metadata-rich `ls` replacement with tree views.
- **zoxide:** Intelligence-driven directory jumping (`z`).
- **fd:** Simple, fast alternative to `find`.

### 2. Data Transformation & Shells
- **Nushell:** A modern shell that understands JSON, CSV, and YAML as tables.
- **jq / yq:** The industry standard for JSON and YAML query and manipulation.
- **httpie / xh:** User-friendly, colorized HTTP clients.

---

## 🛠️ Implementation Patterns

### 1. The "Code Forensic" Search
When diagnosing a bug across a massive monorepo, use `ripgrep` with advanced filtering.

```bash
# Search for 'auth-error' but only in TSX files, excluding tests
rg "auth-error" -g "*.tsx" -g "!*.test.*" --stats

# Find all 'TODO' comments and export them to a JSON table (Nushell)
rg "TODO" --json | from json | select data.path.text data.lines.text
```

### 2. Complex Multi-File Refactoring
Using `sed` and `fd` to rename an exported symbol across the entire project.

```bash
# Rename 'OldComponent' to 'NewComponent' in all .tsx files
fd -e tsx -x sed -i 's/OldComponent/NewComponent/g' {}
```

### 3. API Debugging with `xh`
```bash
# POST a JSON payload with headers and follow redirects
xh POST api.squaads.com/v1/sync \
  Authorization:"Bearer $TOKEN" \
  name="Project X" \
  active:=true
```

---

## 🔍 Advanced RegEx & Data Logic (2026)

### RegEx Best Practices
- **Prefer Non-Capturing Groups `(?:...)`:** Improves performance in large-scale scans.
- **Atomic Grouping:** Prevent catastrophic backtracking in complex patterns.
- **Named Captures:** Make your RegEx readable for other agents.
  `(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})`

### The `jq` Power User
```bash
# Extract IDs from a nested JSON array where status is 'active'
cat data.json | jq '.projects[] | select(.status == "active") | .id'
```

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** use `grep` when `rg` is available; the performance difference is 10x-100x.
2.  **NEVER** pipe `ls` into `grep`. Use `fd` or `eza --filter`.
3.  **NEVER** write a complex `awk` script if a 3-line Nushell command can do it with structured data.
4.  **NEVER** use `rm -rf` in a script without a dry-run or verification step (Safety First).

---

## 🛠️ Troubleshooting Guide

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **Search is too slow** | Searching `node_modules` or `.git` | Use `rg` which respects `.gitignore` by default. |
| **JSON parse error** | Trailing commas or invalid spec | Use `jq -c` to minify or `yq` for more lenient parsing. |
| **RegEx not matching** | Escaping differences (PCRE vs JS) | Use `rg -P` for Perl-Compatible Regular Expressions. |
| **Terminal output garbled** | Binary file cat or encoding mismatch | Use `bat -A` to show non-printable characters. |

---

## 📚 Reference Library
- **[Modern Unix Toolbox](./references/1-modern-unix-toolbox.md):** Deep dive into Rust-powered CLI tools.
- **[Advanced RegEx & jq](./references/2-advanced-regex-and-jq.md):** Mastering the math of text manipulation.
- **[Nushell Mastery](./references/3-nushell-structured-data.md):** Using the shell as a structured data engine.

---

## 📜 Standard Operating Procedure (SOP)
1.  **Identify Data Source:** Is it a file, a stream, or an API?
2.  **Select Filter:** Use `rg` for text, `jq` for JSON, `xh` for HTTP.
3.  **Pipe & Transform:** Build a pipeline (e.g., `xh | jq | rg`).
4.  **Verify:** Check the output against a small sample.
5.  **Automate:** Save the pipeline as a Bun script or a Nushell function.

---

## 🔄 Evolution from v0.x to v1.1.0
- **v1.0.0:** Legacy `planning-with-files` clone (Inaccurate).
- **v1.1.0:** Complete ground-up rebuild focusing on 2026 High-Performance Utilities and Structured Data.

---

**End of Utility Pro Standard (v1.1.0)**
