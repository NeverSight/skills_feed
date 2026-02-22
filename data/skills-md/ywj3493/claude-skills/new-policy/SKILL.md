---
name: new-policy
description: Creates a new policy document in docs/policy/ with the standard format, and simultaneously creates its Korean translation in docs/dev/policy/. Use this when the team needs to establish a new working rule or standard. Triggered by "add a policy", "create a policy for X", "새 정책 만들어줘", "규칙 문서화", or describing a convention that needs to be formalized.
---

# new-policy

Adds a new policy document to the project following the standard format,
with an automatic Korean translation in `docs/dev/policy/`.

## When to Use

- User says "add a policy", "create a policy for X", "새 정책 추가", "규칙 만들어줘"
- A new convention needs to be formalized (branching strategy, review process, etc.)
- The user describes a working rule that isn't yet written down

## Step-by-Step Instructions

### Step 1: Gather Information

Ask the user (or infer from context):

1. **Policy name** — becomes the filename in kebab-case
   - Example: "branching strategy" → `branching-strategy.md`
2. **Purpose** — what does this policy govern and why?
3. **Rules** — the actual rules (numbered or bulleted)
4. **Exceptions** — when, if ever, the rules may be bypassed

If the user has described the policy in their message, draft the content and
ask for confirmation before writing.

### Step 2: Create the English Policy Document

Create `docs/policy/<policy-name>.md`:

```markdown
# <Policy Title>

## Purpose

<What this policy governs and why it exists>

## Rules

1. <Rule 1>
2. <Rule 2>

## Exceptions

<When the rules may be bypassed, or "None" if no exceptions apply>

## Revision History

- <YYYY-MM-DD>: Initial version
```

### Step 3: Create the Korean Mirror

Create `docs/dev/policy/<policy-name>.ko.md` with a full Korean translation.

Translation rules (same as sync-dev):
- All prose and headings → Korean
- Code blocks, file paths, technical identifiers → keep in English
- Checkbox and list markers → keep as-is

```markdown
# <정책 한국어 제목>

## 목적

<이 정책이 다루는 내용과 존재 이유>

## 규칙

1. <규칙 1>
2. <규칙 2>

## 예외

<규칙을 우회할 수 있는 경우, 또는 "없음">

## 개정 이력

- <YYYY-MM-DD>: 최초 작성
```

### Step 4: Reference in policy.md

After creating the files, remind the user:

> Consider adding an @-reference to this new policy in `docs/policy/policy.md`
> under the "Related Policy Files" section:
> `- [@docs/policy/<policy-name>.md](docs/policy/<policy-name>.md) — <description>`

Do **not** automatically edit `policy.md` — show the suggested line and let the
user decide.

### Step 5: Confirm and Report

Tell the user:

> Created:
> - `docs/policy/<policy-name>.md`
> - `docs/dev/policy/<policy-name>.ko.md`
>
> Add an @-reference to `docs/policy/policy.md` if appropriate.
