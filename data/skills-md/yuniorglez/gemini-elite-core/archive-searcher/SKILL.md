---
name: archive-searcher
id: archive-searcher
version: 2.0.0
description: "Professional Git Forensics and Archival Intelligence for deep historical recovery."
---

# 📂 Skill: archive-searcher v2.0.0
> **Optimized for Git 2.48+ and Conductor Track Management (2026 Standards)**

## 📋 Table of Contents
1. [Executive Summary](#executive-summary)
2. [Core Philosophy](#core-philosophy)
3. [The Art of Archival Investigation](#the-art-of-archival-investigation)
4. [Git Forensics: The Pickaxe Strategy (-S)](#git-forensics-the-pickaxe-strategy--s)
5. [Regex-Based Content Tracking (-G)](#regex-based-content-tracking--g)
6. [Reflog: The Ultimate Safety Net](#reflog-the-ultimate-safety-net)
7. [Archival Search: Conductor Tracks](#archival-search-conductor-tracks)
8. [Case Study: The Ghost of a Feature](#case-study-the-ghost-of-a-feature)
9. [Git Internal Object Analysis](#git-internal-object-analysis)
10. [Forensic Interviewing of Code](#forensic-interviewing-of-code)
11. [Advanced Forensic Interviewing Scenarios](#advanced-forensic-interviewing-scenarios)
12. [Historical Contextualization](#historical-contextualization)
13. [Integrating with AI Analysis](#integrating-with-ai-analysis)
14. [Comparison of Search Tools](#comparison-of-search-tools)
15. [Best Practices for Searchability](#best-practices-for-searchability)
16. [The "Do Not" List (Common Pitfalls)](#the-do-not-list-common-pitfalls)
17. [Step-by-Step Implementation Patterns](#step-by-step-implementation-patterns)
18. [Common Forensic Scenarios (2026 Edition)](#common-forensic-scenarios-2026-edition)
19. [Mental Models for Forensic Excellence](#mental-models-for-forensic-excellence)
20. [Advanced Troubleshooting & Recovery](#advanced-troubleshooting--recovery)
21. [The Bisect Walkthrough: Automated Regressions](#the-bisect-walkthrough-automated-regressions)
22. [Restoring Deleted Branches & History](#restoring-deleted-branches--history)
23. [Searching for File Renames & Moves](#searching-for-file-renames--moves)
24. [Archival Integrity & Verification](#archival-integrity--verification)
25. [Legal & Compliance Search (Audit Trails)](#legal--compliance-search-audit-trails)
26. [Archival Security & Privacy](#archival-security--privacy)
27. [Search Scenarios for 2026 AI Teams](#search-scenarios-for-2026-ai-teams)
28. [Integrating with External Search APIs](#integrating-with-external-search-apis)
29. [Recovery from Corrupt Repositories](#recovery-from-corrupt-repositories)
30. [Future-Proofing Your Archives](#future-proofing-your-archives)
31. [Common Questions and Answers (FAQ)](#common-questions-and-answers-faq)
32. [Glossary of Forensic Terms](#glossary-of-forensic-terms)
33. [Tooling & Scripts](#tooling--scripts)
34. [Reference Documentation](#reference-documentation)

---

## 🚀 Executive Summary
The `archive-searcher` skill is the definitive guide for high-precision historical analysis in modern software environments. It transforms the standard, often futile "grep" approach into a multi-layered, systematic forensic investigation. Whether you are hunting for a lost configuration from six months ago, tracing the exact commit that introduced a subtle race condition in a high-concurrency environment, or fulfilling a legal audit requirement, this skill provides the tactical commands and mental models needed to navigate deep history with absolute confidence.

In 2026, the landscape of software development has shifted. AI-driven code generation, automated refactors, and rapid experimentation have increased the "noise" in our repositories. The ability to reconstruct *why* a specific decision was made, what the constraints were at the time, and who the stakeholders were is now more valuable than the actual lines of code themselves. This skill focuses on both the "Git-Way" (raw historical data) and the "Conductor-Way" (structured mission context) of archiving and retrieving knowledge.

## 🧠 Core Philosophy
Information in a well-managed project is never truly "deleted"; it is simply "moved to the background." This skill is built upon four foundational pillars:
- **Persistence of Truth**: Git history is an immutable ledger (in most cases) that contains the "Why" behind the "What." Every line of code, every deleted file, and every merge conflict is a snapshot of a human or AI decision. We treat the repository as a living organism where every scar tells a story.
- **Context Over Content**: Finding the code is only Step 1. True archival search involves finding the surrounding commit message, the author, the timestamp, and the PR context. Without context, code is just text. We prioritize the "Meta-Data" of the change.
- **Surgical Efficiency**: We prioritize indexed and intelligent searches (like `git log -S`) over brute-forcing history. This saves time and reduces cognitive load during high-pressure debugging sessions. Efficiency is not just about speed; it's about accuracy.
- **Layered Defense Strategy**: If a piece of information isn't in the current branch, we check other branches. If it's not in the visible `git log`, we check `git reflog`. If it's completely missing from Git, we pivot to the `conductor` archives. We never stop at the first "no."

## 🎭 The Art of Archival Investigation
Investigating history is more like archaeology than engineering. You are looking for fragments of logic buried under layers of refactors.
- **Stratigraphy**: Understanding which "layer" of the project you are looking at (e.g., the Pre-Next.js era vs. the Modern era).
- **Artifact Analysis**: Treating every commit as an artifact that must be dated and attributed.
- **Reconstruction**: Using partial data to rebuild the full intent of a feature.

---

## 🛠 Git Forensics: The Pickaxe Strategy

### 1. The `-S` (Pickaxe) Search
The Pickaxe is the most efficient way to find when a specific string was introduced or removed. Unlike a standard grep, it only shows commits where the *number of occurrences* of the string changed.

**Why use it?**
- **Lifecycle Tracking**: To find when a function was first added and when it was finally retired.
- **Constant Hunting**: To find when a specific constant, magic number, or hardcoded API key was deleted.
- **Variable Forensics**: To trace how a specific variable name has migrated through the codebase over years of refactors.

```bash
# Find when 'DeprecatedAPI' was added or removed
# This will show you the exact commits where the usage count changed.
# The --patch flag is critical here to see the actual diff.
git log -S "DeprecatedAPI" --patch --oneline
```

**Advanced Usage**: Always use it with `--all` to search through every branch, including merged, orphaned, or abandoned ones.
```bash
git log -S "auth_token_v1" --all --graph --decorate --oneline
```

### 2. Regex-Based Content Tracking (-G)
While `-S` looks for changes in count, `-G` looks for changes that *match a regular expression*. This is much more powerful for finding structural changes or patterns that have many variations.

```bash
# Find commits where lines matching a regex were added/removed
# Example: Finding any change to a port number between 3000-3999
# This is perfect for security audits or infrastructure changes.
# Note: This is computationally more expensive than -S.
git log -G "port: 3[0-9]{3}" --patch
```

---

## 🕰 Reflog: The Ultimate Safety Net
`git reflog` is the "history of your history." It tracks every time the `HEAD` of a branch moves.

**What Reflog captures that Log does not**:
- **Commit Amends**: If you `git commit --amend`, the original commit is still accessible.
- **Rebase Casualties**: Pre-rebase commits are saved here.
- **Hard Resets**: Rescues you from an accidental `reset --hard`.
- **Deleted Branches**: Recovers the last known state of a deleted branch.

```bash
# View the reflog with relative dates for easier navigation
git reflog --date=relative
```

---

## 📂 Archival Search: Conductor Tracks
In the Squaads ecosystem, we use "Conductor" to manage mission tracks. This provides a semantic layer on top of raw Git commits.

### Archival Hierarchy
- `conductor/archive/`: Completed project-level archives.
- `conductor/tracks/<track_id>/archive/`: Internal history of a specific track.
- `conductor/index.md`: The central directory of all missions.

---

## 🕵️‍♂️ Case Study: The Ghost of a Feature
**Problem**: A "Team Collaboration Dashboard" was fully functional in Feb 2025. By Jan 2026, it is gone.

**Detailed Investigation Walkthrough**:
1. **Initial Search**: `git log --all --grep="Collaboration Dashboard"`
   - *Discovery*: Commit `e5f1b2c` (Oct 2025) says "Cleanup legacy UI".
2. **Blast Radius Analysis**: `git show e5f1b2c --stat`
   - *Discovery*: Massive deletion of components.
3. **Finding the Golden Version**: `git log --diff-filter=A -- src/components/Dashboard.tsx`
   - *Discovery*: Found original implementation in `a1b2c3d`.
4. **Context Recovery**: Locate `track-45` in `conductor/archive/`.
5. **Outcome**: Re-implementation possible with original context.

---

## 📦 Git Internal Object Analysis
Git stores everything as "objects".

### Inspecting a Blob
```bash
git cat-file -t <hash>  # Type check
git cat-file -p <hash>  # Content check
```

### Finding Lost Blobs
```bash
git fsck --lost-found
```

---

## 💬 Forensic Interviewing of Code
- **"Who authorized you?"**: Authored-by, PR links.
- **"What was your purpose?"**: Conductor specs.
- **"Why were you killed?"**: Surroundings of deletion.
- **"Who were your friends?"**: `git show --name-only`.

---

## 🎙 Advanced Forensic Interviewing Scenarios

### Scenario 1: The "Legacy Debt" Interview
When you find a block of commented-out code that says `// DO NOT REMOVE - CRITICAL FOR IE11`.
- **Question**: Is IE11 still supported in the 2026 build?
- **Action**: Check `conductor/product-guidelines.md` for current browser support tiers.
- **Follow-up**: If no, use `git log -S "IE11"` to find the commit where support was officially dropped.

### Scenario 2: The "Silent Fix" Interview
When a bug suddenly disappears but no one knows why.
- **Question**: Which commit fixed the issue without mentioning it in the message?
- **Action**: Use `git bisect` between the last "broken" version and the first "fixed" version.
- **Outcome**: You find a refactor that accidentally fixed a race condition by moving a hook call.

---

## 🌍 Historical Contextualization
- **Temporal Correlation**: Commits vs. Server Logs.
- **Environment Archeology**: `package.json` / `Dockerfile` history.
- **Branch Lineage**: Where did this change travel?

---

## 🤖 Integrating with AI Analysis
1. **Wide Sweep**: Parallel `grep` and `log`.
2. **Filter & Rank**: Candidate identification.
3. **Deep Read**: Diff analysis.
4. **Synthesis**: "Why" explanation.

---

## 📊 Comparison of Search Tools

| Tool | Best For | Speed | Deep History? |
| :--- | :--- | :--- | :--- |
| `grep -r` | Quick scan. | Fast | No |
| `ripgrep (rg)`| High-speed live search. | Ultra Fast | No |
| `git log -S` | String lifecycle. | Slow | **Yes** |
| `git log -G` | Regex history. | Very Slow | **Yes** |

---

## ✅ Best Practices for Searchability
- **Atomic Commits**: One change, one commit.
- **Semantic Messages**: Prefixes and clear intent.
- **Reference Everything**: Track IDs, PRs.
- **Tagging**: Milestone markers.

---

## 🚫 The "Do Not" List (Common Pitfalls)

| Anti-Pattern | Why it fails | Correct Approach |
| :--- | :--- | :--- |
| **Grep on live only** | Misses history. | Use `git log -S`. |
| **Ignoring Reflog** | Misses "undone" work. | Check `reflog` first. |
| **Searching without -p** | No code visibility. | Always use `--patch`. |
| **Partial Search** | Misses other branches. | Use `--all`. |

---

## 💡 Step-by-Step Implementation Patterns

### Scenario: Restoring a deleted config
1. **Identify**: `git log --all --full-history -- config/settings.yaml`
2. **Preview**: `git show <hash>:config/settings.yaml`
3. **Recover**: `git checkout <hash>^ -- config/settings.yaml`

---

## 🚀 Common Forensic Scenarios (2026 Edition)

### Scenario A: The "Accidental Rebase" Recovery
You rebased your branch and lost work.
- **Action**: `git reflog`. Find the hash before the rebase.
- **Fix**: `git reset --hard <safe_hash>`.

### Scenario B: The "Vanishing API Key"
Key accidentally committed.
- **Action**: `git log -G "AI_KEY_PATTERN" --all --patch`.
- **Result**: Immediate rotation of the found key.

---

## 🧠 Mental Models for Forensic Excellence
- **The Crime Scene Model**: Document current state first.
- **The Tree of Life Model**: Visualize the branch graph.
- **The Incremental Disclosure Model**: Broad search -> Zoom in.

---

## 🛠 Advanced Troubleshooting & Recovery

### Dealing with "Shallow" Clones
If the project was cloned with `--depth 1`, history search will fail.
- **Symptom**: `git log -S` returns nothing even for known strings.
- **Fix**: `git fetch --unshallow` to retrieve the full history.

### Recovering from a Corrupt Index
- **Symptom**: `fatal: index file corrupt`.
- **Fix**: `rm .git/index && git reset`.

### Finding "Dangling" Work
- **Action**: `git fsck --lost-found`.
- **Outcome**: Inspect `.git/lost-found/commit/` for commits that aren't on any branch.

---

## 🔄 The Bisect Walkthrough: Automated Regressions
1. **Start**: `git bisect start`
2. **Define Limits**: `git bisect bad HEAD`; `git bisect good v1.5.0`
3. **Automate**: `git bisect run bun test`
4. **Finalize**: `git bisect reset`

---

## 🔄 Restoring Deleted Branches & History
```bash
# Find deleted branch hash
git reflog | grep "feature/name"
# Restore
git checkout -b feature/name <hash>
```

---

## 📁 Searching for File Renames & Moves
```bash
git log --follow -- <new_path>
```

---

## 🛡 Archival Integrity & Verification
- **GPG Signing**: `git log --show-signature`.
- **Hashes**: Verify metadata JSONs in Conductor.

---

## ⚖️ Legal & Compliance Search (Audit Trails)
- **Author Activity**: `git log --author="Name"`.
- **Audit Export**: `git log --pretty=format:"%h %ad %s" > audit.txt`.

---

## 🔐 Archival Security & Privacy
- **GDPR**: History contains personal data.
- **Secret Hygiene**: Old keys are still dangerous.

---

## 🤖 Search Scenarios for 2026 AI Teams
- **Refactor Audit**: AI-driven breaking changes.
- **Agent Mission Reconstruction**: Auditing autonomous agents.
- **Prompt Injection Discovery**: Searching malicious prompt changes.

---

## 🌐 Integrating with External Search APIs
- **GitHub API**: Search across many repos.
- **Sourcegraph**: Cross-repo forensics.

---

## 🛠 Recovery from Corrupt Repositories
1. **Fix Index**: `rm .git/index && git reset`.
2. **Recover Objects**: `git fsck`.

---

## 🔮 Future-Proofing Your Archives
- **Standard Formats**: Markdown/JSON.
- **Avoid Dead Links**: Embed context in commits.

---

## ❓ Common Questions and Answers (FAQ)

**Q: Can I search for a string that was in a file I renamed?**
A: Yes. Use `git log --follow -S "string" -- path/to/new_name.ts`.

**Q: How do I find commits by a specific person that touched a specific directory?**
A: `git log --author="Name" -- path/to/directory/`.

**Q: I ran 'git gc' and now my reflog is smaller. Can I get it back?**
A: No. `git gc` prunes old entries.

**Q: What if the commit message is just a Jira ID?**
A: Use a browser tool to fetch the context or check Conductor archives.

---

## 📖 Glossary of Forensic Terms
- **Pickaxe**: String count lifecycle search.
- **Reflog**: Black box of branch head moves.
- **Blob**: File content object.
- **Tree**: Directory structure object.
- **Dangling Commit**: Unreachable commit.
- **Bisect**: Binary search regression finder.
- **OID**: Object ID (Hash).
- **Plumbing**: Low-level Git commands.
- **Porcelain**: High-level Git commands.
- **Detached HEAD**: Working on a commit instead of a branch.
- **Staging**: The prep area for commits.
- **G-Regex**: The use of `git log -G` for pattern matching.
- **Diff-Filter**: Filtering by addition (A), deletion (D), or modification (M).
- **Full History**: Disabling parent simplification for total visibility.
- **Cherry-Pick**: Applying a single commit from history to your current branch.
- **Revert**: Creating a new commit that inverses the changes of a historical commit.
- **Unshallow**: Converting a partial history clone into a complete one.
- **FSCK**: File System Check for repository integrity.
- **Commit Graph**: The directed acyclic graph (DAG) of all commits.
- **Reflog Expiration**: The time-to-live of reflog entries (defaults to 90 days).
- **Blob Hash**: The unique SHA identifier for a specific version of a file.
- **Git Flow**: A branching model for release management.
- **Trunk-Based Development**: A development model where developers frequently merge small updates to a core "trunk".
- **Merge Conflict**: A state where Git cannot automatically resolve differences between two commits.
- **Remote**: A version of the repository hosted on the internet or a network.

---

## 📜 Tooling & Scripts
- `deep-search.sh`: Multi-branch search wrapper.
- `track-forensics.py`: Squaads mission re-constructor.

---

## 📚 Reference Documentation
- [Git Forensics Deep Dive](./references/git-forensics.md)
- [Conductor Archival Standards](./references/conductor-archives.md)

---

### *Updated: January 22, 2026 - 15:18*