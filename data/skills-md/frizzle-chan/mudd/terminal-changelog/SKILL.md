---
name: terminal-changelog
description: >-
  Write in-game changelog updates as terminal documents in mansion.rec. Use when
  asked to write a changelog, add a terminal update, document recent changes, or
  catch users up on new features. Creates INBOX entries for the office terminal.
---

# Terminal Changelog

Add user-facing changelog entries as terminal documents in `data/worlds/mansion.rec`.

## Workflow

1. **Find the latest terminal document with a commit reference**
   ```bash
   grep -n "update as of" data/worlds/mansion.rec
   ```
   Extract the commit hash from the most recent entry.

2. **Fetch origin/master and get commits since that reference**
   ```bash
   git fetch origin master
   git log <commit>..origin/master --oneline --reverse
   ```

3. **Analyze feature commits** - Skip dependabot/CI bumps. For significant commits:
   ```bash
   git show <hash> --stat --format="%B" | head -50
   ```

4. **Write the terminal document** following the format below

5. **Validate**
   ```bash
   just entities
   ```

## Terminal Document Format

```rec
Id: terminal_inbox_<topic>
Name: INBOX - <Subject Line>
Prototype: terminal_document
Room: office
Container: office_terminal
DescriptionLong: ```
+ FROM: frizzle@mudd.local
+ TO: team@mudd.local
+ SUBJECT: <Subject Line>
+ DATE: <YYYY-MM-DD>
+ ----------------------------------------
+
+ (update as of <full-commit-hash>)
+
+ <Body content - each line starts with "+ ">
+
+ -Frizzle
+ ```
```

Insert after the previous terminal_inbox entry, before `# Gallery entities`.

## Content Guidelines

**Focus on user-facing changes:**
- New commands (`/pay`, `/use`, etc.)
- New items players can find or interact with
- New locations or entities
- Changes to game mechanics

**Include gameplay tips:**
- Where to find new things ("Check the lounge for the slot machine")
- How to use new features ("Use /pay to send yen to nearby players")
- Fun interactions ("Pull the handle to win prizes!")

**Tone:** Casual dev update from Frizzle. Excited about new features, hints at what's coming.

**Skip:** Internal refactors, CI updates, dependency bumps, bug fixes unless player-visible.
