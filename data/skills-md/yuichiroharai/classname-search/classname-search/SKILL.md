---
name: classname-search
description: A CLI tool that searches inside class and className attributes and matches against each class name individually. Use this instead of grep when searching or replacing class names.
---

# Class Name Search Guide

## Windows CLI Setup

1. Run `echo --%`
2. If output is empty (PowerShell): Add `--%` before arguments (e.g., `--% '^flex$'`)
3. If not PowerShell: Run `npx -y node -e "console.log(process.argv[1])" "^test"`. If output is `test` instead of `^test`, escape `^` as `^^` (e.g., `^flex$` → `^^flex$`)

See [CLI Reference](#cli-reference) for details.

## Count matched class names per file

> [!WARNING]  
> AI manual counting is unreliable. Always use this command to count class names.

**Command:**

```bash
npx classname-search stats 'src/**/*.jsx' 'text-'
```

**Output:**

```text
src/components/Header.jsx: 3 matches
src/components/Main.jsx: 4 matches

Total: 7 matches in 2 files
```

> [!NOTE]  
> By default, only files containing matched class names are listed.  
> Use the `--verbose` option if you want to include files with 0 matches in the output.

## Search for class names

**Command:**

```bash
npx classname-search search 'src/components/**/*.jsx' 'flex'
```

**Output (search):**

<!-- prettier-ignore-start -->
```jsonl
{"file":"src/components/Header.jsx","line":3,"matched":"flex","className":"flex","classValue":"flex flex-col"}
{"file":"src/components/Header.jsx","line":3,"matched":"flex","className":"flex-col","classValue":"flex flex-col"}
{"file":"src/components/Header.jsx","line":4,"matched":"flex","className":"inline-flex","classValue":"inline-flex"}
```
<!-- prettier-ignore-end -->

> [!IMPORTANT]  
> `matched` is the regex match; `className` is the full class name containing that match.

**File output:**

Redirect output to a file for large results or when requested by the user.  
Working from file output is **strongly recommended** to avoid truncation and hallucination.

```bash
npx classname-search search 'src/components/**/*.jsx' 'flex' > 'filename.jsonl'
```

## Search and replace class names

**Command:**

```bash
npx classname-search replace 'src/components/**/*.jsx' -- '-slate-(\d+)$' '-neutral-$1'
```

**Output:**

```text
Replaced 8 matches of "-slate-(\d+)$" with "-neutral-$1" in 3 files.
```

## Remove class names

**Command:**

```bash
npx classname-search remove 'src/components/**/*.jsx' '^font-normal$'
```

**Output:**

```text
Removed 5 matches of "^font-normal$" with "" in 2 files.
```

## CLI Reference

Fetch `https://raw.githubusercontent.com/yuichiroharai/classname-search/main/README.md`
