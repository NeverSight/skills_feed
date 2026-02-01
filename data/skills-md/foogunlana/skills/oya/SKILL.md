---
name: oya
description: Plan and stay on track. Fast. Practical. Intentional. Oya is a productivity tool for doers who think strategically. It combines your long-term vision with daily adaptation by bringing together ideas from Getting Things Done (GTD) and the 7 Habits of Highly Effective People in a simple and lightning fast workflow. Daily use is recommended. Just say "oya" to get going.
---

# Oya

A planning skill that helps users start their day or week with intention and clarity.

> *Named for the Yoruba goddess of winds and change — Oya clears what no longer serves, making space for transformation.*

## Core Workflow

Weekly planning (10-15 min) → Daily planning (5 min) → Reflect (2 min)

See `references/branding.md` for visual diagrams.

## Two Flows

Oya has two distinct flows depending on whether the user has been onboarded:

| Condition                  | Flow                                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------- |
| No `.claude/oya.md` exists | **Onboarding Flow** - interactive, asks questions, guides user through first week + day |
| `.claude/oya.md` exists    | **Regular Flow** - FAST approach, no questions, proposes directly from context          |

---

## Onboarding Flow (First Run Only)

**Detection:** Check if `.claude/oya.md` exists. If no config exists, run this flow. Otherwise skip to Regular Flow.

**Goal:** Give user the "Aha" moment by creating authentic weekly goals first, then personalized daily tasks.

**Note:** This is the ONLY time oya asks questions and waits for user input.

**Step 1: Welcome & Branding**

Read `references/branding.md` and display verbatim:
1. Logo
2. Origin quote
3. Workflow diagram
4. Key concepts

---

*Let's set up your planning system...*

**Step 2: Create Weekly Note First**

Get current date with `date` command.

Create the weekly note immediately using the minimal template from `assets/templates/weekly.md`:
- Just the structure with `<!-- Add your goals and tasks here -->`
- No assumptions about user's goals
- Save to proper file path

**Step 3: Ask User to Edit Weekly Note**

Display:

```
I've created your weekly note: [path/to/weekly-note.md]

What's your goal this week? Go edit it now - add your goals and tasks.

When you're ready, come back and we'll personalize your planning experience.
```

**Wait for user to return.** Do not proceed until user signals they're ready.

**Step 4: Setup Wizard**

Use a single AskUserQuestion prompt to gather setup information:

```
Let's personalize your planning experience. You can skip any question and add it later in .claude/oya.md

1. What should I call you?

2. What's your guiding phrase (mantra)?
   Examples: "Give Everything." • "Make it happen." • "One day at a time."

3. What life areas do you want to track? (comma-separated)
   Examples: home, work, personal, health, creative

4. What values guide your decisions? (optional, shown in weekly notes)
   Examples: Focus, Balance, Connection, Growth, Service, Creativity
   Leave blank to disable.

5. Any personal nudges? (optional, shown in daily entries)
   Examples: "If not now, when?" • "Focus on service" • "What would future you thank you for?"
   Leave blank to disable.

6. Enable coaching? (yes/no)
   Coaching helps spot patterns like overloading or vague goals.
```

Parse user's free-text response and use sensible defaults for any skipped fields:
- mantra: "Give Everything."
- contexts: home, work, personal
- coaching: true

**Step 5: Write Config**

Generate `.claude/oya.md` with user's choices:

```yaml
name: "{user_name}"
mantra: "{chosen_mantra}"

# Optional - only include if user provided values
values:
  enabled: true
  list:
    - {value_1}
    - {value_2}

# Optional - only include if user provided nudges
nudges:
  enabled: true
  list:
    - "{nudge_1}"
    - "{nudge_2}"

contexts:
  - home
  - work
  - personal

context_display: hidden

coaching:
  enabled: {true|false}
```

**Step 6: Create Daily Tasks**

Read the weekly note the user just edited. Create today's daily entry based on:
- Tasks from weekly note (copy verbatim, only today's relevant items)
- Values/nudges from config
- User's contexts

Append to weekly note using template from `assets/templates/daily.md`.

**Step 7: Ask User to Edit Daily Tasks**

Display:

```
I've added today's tasks based on your weekly goals. Review and edit them in the same file.

When you're ready, come back for feedback.
```

**Wait for user to return.**

**Step 8: Automatic Critique**

Read the edited daily tasks. Provide coaching critique based on:
- Alignment with weekly goals
- Balance across contexts (work, home, personal)
- Coaching patterns if enabled

Then show success message:

```
🌀 Great start!

Your planning system is ready. Here's how it works:

1. Run /oya each day - creates or updates your notes
2. Edit the notes it proposes - make them yours
3. Notes carry forward until done - no task left behind

Run /oya anytime to continue planning.
```

**Exit after onboarding and critique.**

---

## Regular Flow (Every Subsequent Run)

**FAST approach - no questions, just propose:**
1. Gather context (previous days, weeks, config, references)
2. Propose note directly (leave `<!-- comments -->` where unsure)
3. User edits
4. Offer coaching critique (if enabled)

**Key principles:**
- **No questions** - Make assumptions from config and previous notes
- **Sparse context = minimal output** - If little info, keep todos minimal/empty
- **Guide for next time** - When sparse, note what user should add for better suggestions

### Step 1: Detection

1. **Get current date and time**: Run `date` in terminal - do not rely on system date. Note the time for reflection prompts.

2. **Check if weekend**: Saturday/Sunday → Use Weekend Flow

3. **Check for pending reflections**:
   - If after 5pm AND today's entry exists but has no reflections → Ask: "Want to reflect on today before wrapping up?"
   - If morning AND yesterday's entry has no reflections → Do yesterday's reflection before starting today

4. **Check what exists**:
   - Does current week's note exist? → If NO: Create weekly note
   - Does today's entry exist in weekly note? → If NO: Add daily entry

5. **Report findings**:
   ```
   "Good morning! Here's what I found:
   - [✓/✗] This week's note (Jan 27th - Jan 31st)
   - [✓/✗] Today's entry (Monday, January 27th)

   Let's set up what's missing..."
   ```

### Step 2: Load Config

Read `.claude/oya.md` (created during onboarding).

See `references/config-guide.md` for configuration options.

**Fallback defaults (if config missing):**
- mantra: "Give Everything."
- contexts: home, work, personal
- paths.base: "planning"
- coaching.enabled: true

### Step 3: Gather Context

Before proposing notes, read:
1. **Previous day's entry** - carry forward uncompleted `[ ]` and `[-]` items verbatim
2. **Last week's note** - unchecked items for carry-forward (if new week)
3. **Monthly goals** - if they exist, use as north star

### Step 4: Create/Update Notes

Based on detection results, use one of these flows:

#### Flow A: Weekly Note

**Propose directly** based on context gathered. Use template from `assets/templates/weekly.md`.

**DO NOT ask questions.** Just propose the note. Make assumptions from config and context.

**Key principles:**
- High signal, low noise
- Single task list (not separated into Must/Should/Could)
- Leave `<!-- comments -->` where unsure instead of asking questions
- Include tasks from all contexts (home, work, personal)
- If context is sparse, keep tasks minimal/empty

**When context is limited:**
- Propose minimal structure with `<!-- Add tasks for [context] here -->`
- After user edits, note: "Add more detail to previous notes to get better suggestions next time"

**After proposing:**
1. User edits the note
2. Offer coaching critique based on config patterns (if enabled)

#### Flow B: Daily Entry

**Propose directly.** Append to weekly note. Use template from `assets/templates/daily.md`.

**DO NOT ask questions.** Just propose the entry. Make assumptions from weekly tasks and config.

**Key principles:**
- Copy tasks VERBATIM from weekly list (same wording, same emoji)
- Preserve task state: `[-]` stays `[-]`, `[ ]` stays `[ ]`, `[x]` stays `[x]`
- Only include today's relevant tasks
- Include values nudge from config (if enabled)
- Balance work AND home/personal tasks (2-4 personal items per day)
- If weekly tasks are empty, propose minimal structure with `<!-- -->`

**When weekly tasks are sparse:**
- Propose minimal daily entry
- After user edits, note: "Add more tasks to weekly note to get better daily suggestions"

#### Flow C: Weekend

Skip work planning. Instead:
1. Make ONE tailored suggestion (rest, connection, or creative pursuit)
2. End with: "Enjoy your weekend - truly rest, truly connect, truly play."

## Task State Notation

- `[ ]` - Not started → carry forward
- `[-]` - In progress → carry forward
- `[x]` - Completed → don't carry

**Default task emojis:**
- 🔥 - Urgent (time-sensitive)
- ❗ - Important/must do
- ☀️ - Creation/creative work
- 😃 - People-focused
- 🕚 - Carried forward
- 🧠 - Protected thinking time

## Coaching Mode

After user edits their note, check for patterns:

| Pattern         | Challenge                                          |
| --------------- | -------------------------------------------------- |
| Overloaded      | "What can you delegate or defer?"                  |
| Vague goals     | "What exactly would success look like?"            |
| Missing balance | "Where's rest or creative time?"                   |
| Too safe        | "What would this look like if you thought bigger?" |

Only coach if `coaching.enabled: true` in config.

## File Paths

| Type   | Default Path                                                                            |
| ------ | --------------------------------------------------------------------------------------- |
| Base   | `{paths.base}/{Year}/{MM}-{Mon}/`                                                       |
| Weekly | `{Mon} {DD}{th/st/nd/rd} - {Mon} {DD}{th/st/nd/rd}.md` (e.g., `Jan 27th - Jan 31st.md`) |
| Config | `.claude/oya.md`                                                                        |

**Weekly file naming format:**
- Use full month name (Jan, Feb, Mar, etc.)
- Use ordinal indicators (27th, 1st, 2nd, 3rd, etc.)
- Format: `[Month] [Day with ordinal] - [Month] [Day with ordinal].md`
- Examples: `Jan 27th - Jan 31st.md`, `Feb 1st - Feb 5th.md`, `Dec 30th - Jan 3rd.md`

## Reflection (End of Day or Next Morning)

**When adding reflections:**

Triggered by detection (Step 1):
- After 5pm: If today's entry exists but has no reflections → Ask: "Want to reflect on today before wrapping up?"
- Next morning: If yesterday's entry has no reflections → Do yesterday's reflection before starting today

**Process:**
1. Ask ONE straightforward question: "What went well today? What didn't?"
2. Keep it minimal - bullet points only, no extra prose
3. Append under **Reflections** in that day's entry
4. No follow-up questions - user can elaborate if they want

**Sync completed tasks:**
- When tasks are checked off in daily list, also check them off in the weekly tasks list
- Keep both lists in sync

**Format:**
```
**Reflections**

- What went well: {user input}
- What didn't: {user input}
- Insights or blockers: {user input if provided}
```
