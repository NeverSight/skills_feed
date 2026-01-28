---
name: context-first
description: |
  Load relevant design documents and project context before working on any task.
  Use when user asks about features, requests implementation, discusses functionality,
  analyzes architecture, updates documentation, or mentions specific components like
  OAuth, authentication, Logto, sync, Happy Server, messaging, chat, terminal, command,
  zen mode, boxes, workspace. Ensures all work is grounded in documented design decisions.
  Prevents assumptions and misaligned solutions by loading context first.
---

# Context-First Skill

**Core Principle:** Understand the design intent before taking action.

**Project Detection:** Automatically identifies project root via git repository location.

## When This Skill Activates

This skill should activate for ANY task involving project features or functionality:

### Implementation Tasks ✅
- Implement/add/modify/fix functionality
- Write new code or refactor existing code
- Debug issues related to features
- Examples: "实现 OAuth 登录", "修复同步问题", "添加消息功能"

### Analysis & Discussion Tasks ✅
- Answer "how does X work?"
- Explain "why did we design it this way?"
- Discuss "can we add Y feature?"
- Architecture analysis
- Examples: "OAuth 流程是怎么设计的？", "为什么用 Logto？"

### Documentation Tasks ✅
- Update feature documentation
- Write user guides or technical specs
- Create or revise design documents
- Examples: "更新 OAuth 文档", "写一个同步功能的说明"

### Decision & Planning Tasks ✅
- Evaluate proposed changes
- Assess feature feasibility
- Review compatibility with existing design
- Examples: "可以添加第三方登录吗？", "这个改动合适吗？"

## Core Workflow

### Step 1: Identify Feature Domain

Extract feature keywords from the user's request. Common domains:

- **Authentication**: OAuth, auth, login, sign in, Logto, authentication, 登录, 认证
- **Synchronization**: sync, synchronization, Happy Server, upstream, 同步
- **Messaging**: message, messaging, chat, conversation, inbox, 消息, 聊天
- **Terminal**: terminal, command, shell, CLI, 终端, 命令
- **Workspace**: zen mode, boxes, workspace, session, 工作区
- **Architecture**: architecture, system design, components, modules, 架构
- **Product**: features, requirements, product, 产品, 需求

### Step 2: Search Design Documents

**ALWAYS check these locations in this order:**

1. **`docs/design/`** - Primary design documents (most important!)
   - `core-user-experience-v2.md` - Main UX design (most features described here)
   - `architecture.md` - System architecture and component design
   - `prd.md` - Product requirements and feature list
   - `white-paper.md` - Project vision and philosophy

2. **`docs/implementation/`** - Technical implementation plans
   - May reference design decisions
   - Contains specific setup guides

3. **`docs/research/`** - Background research and analysis
   - Understanding why certain technologies were chosen

4. **`docs/verification/`** - Test scenarios and acceptance criteria
   - Reveals requirements and expected behavior

**Search Strategy:**

Use Grep to search for keywords across documentation:

```bash
# Search by feature keyword in design docs
grep -r "oauth\|authentication\|logto" docs/design/
grep -r "sync\|synchronization\|happy.*server" docs/design/
grep -r "messaging\|chat\|conversation" docs/design/
grep -r "terminal\|command\|shell" docs/design/
grep -r "zen\|boxes\|workspace" docs/design/

# If design docs don't have it, search implementation
grep -r "keyword" docs/implementation/

# Search across all docs as fallback
grep -r "keyword" docs/
```

### Step 3: Load and Read Relevant Documents

**Priority loading order:**
1. Read the most relevant `docs/design/*.md` first (especially `core-user-experience-v2.md`)
2. Read related `docs/implementation/*.md` for technical details
3. Read `docs/research/*.md` for background context if needed

**Important:** Use the Read tool to actually read the documents. Don't assume you know the content.

### Step 4: Summarize Context

Before proceeding, present the loaded context to the user:

**Template:**
```
🔍 Context Loaded

I found and read these design documents:
- docs/design/core-user-experience-v2.md (Section: [relevant section])
- docs/implementation/[relevant-file].md

📋 Key Design Decisions:
- [Decision 1]
- [Decision 2]
- [Constraint or principle]

✅ Ready to proceed with this context in mind.
```

### Step 5: Proceed with Context

Only AFTER loading and summarizing the design context, proceed with the actual task.

## Feature → Document Quick Reference

Use this mapping to quickly identify which documents to read:

| User Mentions | Primary Documents to Load |
|--------------|---------------------------|
| OAuth, authentication, login, Logto, 登录, 认证 | `design/core-user-experience-v2.md` (Authentication section)<br>`implementation/logto-web-oauth-setup.md`<br>`research/authentication-system-analysis.md` |
| Sync, synchronization, Happy Server, upstream, 同步 | `design/architecture.md` (Sync section)<br>`design/core-user-experience-v2.md` (Sync section)<br>`research/authentication-system-analysis.md` |
| Message, messaging, chat, conversation, inbox, 消息 | `design/core-user-experience-v2.md` (Messaging section)<br>`design/prd.md` |
| Terminal, command, shell, CLI, 终端 | `design/core-user-experience-v2.md` (Terminal section)<br>`design/prd.md` |
| Zen mode, boxes, workspace, session, 工作区 | `design/core-user-experience-v2.md` (Workspace section)<br>`design/prd.md` |
| Architecture, system, components, modules, 架构 | `design/architecture.md`<br>`design/core-user-experience-v2.md` |
| Product, features, requirements, vision, 产品 | `design/prd.md`<br>`design/white-paper.md`<br>`design/core-user-experience-v2.md` |

**Tip:** When in doubt, `core-user-experience-v2.md` is usually the best starting point as it covers most features.

## If No Design Document Found

If you cannot find relevant design documentation:

1. ⚠️ **Alert the user clearly:**
   ```
   ⚠️ Design Context Missing

   I couldn't find design documentation for [feature/topic].

   This means:
   - No documented design decisions exist yet
   - Risk of misalignment with project vision
   - May need to create design doc first

   Options:
   1. Create design document first (recommended) - use three-doc-method skill
   2. Proceed with general project principles from CLAUDE.md
   3. Ask you for design guidance

   What would you like to do?
   ```

2. **Do NOT proceed with implementation** without explicit user approval

3. **Suggest creating documentation first** if this is a new feature

## Best Practices

1. ✅ **Always read, don't assume** - Even if you think you know the design, read the docs
2. ✅ **Read the full section** - Don't just skim, understand the complete context
3. ✅ **Check multiple documents** - Design decisions may be spread across files
4. ✅ **Summarize what you learned** - Make the context visible to the user
5. ✅ **When uncertain, read more** - Better to over-load context than miss key details

## Examples

### Example 1: Implementation Task

**User:** "实现 OAuth 登录的'记住我'功能"

**Skill Response:**
```
🔍 Context-First: Loading OAuth design context...

Found relevant documents:
- docs/design/core-user-experience-v2.md
- docs/implementation/logto-web-oauth-setup.md

Let me read these to understand the current OAuth design...

[After reading]

📋 Key Context:
- Current OAuth flow uses Logto with full-page redirect (not popup)
- Authentication state managed via Logto SDK hooks
- Design principle: "Zero Modification" - prefer Logto's built-in features
- User tokens stored in localStorage via Logto SDK

For "记住我" functionality, I should:
- Check if Logto SDK has built-in "remember me" support
- Maintain the full-page redirect flow
- Not modify upstream Logto code

Ready to proceed with implementation following these constraints.
```

### Example 2: Discussion Task

**User:** "Happy Server 的同步机制是怎么设计的？"

**Skill Response:**
```
🔍 Context-First: Loading sync architecture context...

Reading:
- docs/design/architecture.md
- docs/design/core-user-experience-v2.md (Sync section)

[After reading]

📋 Sync Architecture Summary:

[Provides detailed summary from the design docs]

Does this answer your question? Would you like me to dive deeper into any aspect?
```

### Example 3: Missing Context

**User:** "添加语音通话功能"

**Skill Response:**
```
🔍 Context-First: Searching for voice call design...

⚠️ Design Context Missing

I searched docs/design/ and couldn't find design documentation for voice call functionality.

This is a significant new feature that needs design documentation first.

Recommendation: Use the `three-doc-method` skill to create:
- Design document (why voice calls, what's the UX)
- Implementation plan (how to build it)
- Verification document (how to test it)

Should I help you create these documents first?
```

## Benefits of Context-First Approach

- ✅ **Prevents rework** - Understand requirements before coding
- ✅ **Maintains consistency** - Align with existing design decisions
- ✅ **Respects constraints** - Avoid violating architectural principles
- ✅ **Better decisions** - Context enables informed choices
- ✅ **Faster development** - No backtracking due to misunderstanding
- ✅ **Knowledge transfer** - Spread understanding of design decisions

## Related Skills

- **three-doc-method** - Create design documents for new features (use when context is missing)
- **e2e-test-runner** - Run tests after implementation (verification phase)

## Troubleshooting

**Q: Skill activates too often / too rarely?**
A: Check the description triggers in the YAML frontmatter. Adjust keywords as needed.

**Q: Can't find relevant documents?**
A: Use `find-docs.sh` script or search more broadly with `grep -r "keyword" docs/`

**Q: Found too many documents?**
A: Prioritize `docs/design/` and specifically `core-user-experience-v2.md` first.

**Q: Documents are outdated?**
A: Alert the user and suggest updating docs before proceeding with the task.
